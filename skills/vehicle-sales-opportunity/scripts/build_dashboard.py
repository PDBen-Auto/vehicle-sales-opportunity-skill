#!/usr/bin/env python3
"""Offline monthly sales analysis. Python 3.10+, standard library only."""
from __future__ import annotations

import argparse
import calendar
import hashlib
import json
import re
import shutil
import tempfile
from collections import defaultdict
from datetime import date
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
TOP_FIELDS = {"schemaVersion", "title", "asOfDate", "synthetic", "coverage", "comparison", "thresholds", "records"}
RECORD_FIELDS = {"market", "seriesId", "brand", "model", "segment", "seriesScope", "year", "month", "units", "status"}
DEFAULT_THRESHOLDS = {"minCurrentUnits": 10000, "minAbsoluteChange": 1000, "rate": 0.1}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def plain_object(value, allowed, required, label):
    require(isinstance(value, dict), f"{label}: expected object")
    require(not set(value) - allowed, f"{label}: unexpected fields")
    require(required <= set(value), f"{label}: missing required fields")


def text_field(value, label):
    require(isinstance(value, str) and bool(value.strip()) and len(value) <= 160, f"{label}: invalid text")
    require(not any(ord(ch) < 32 for ch in value), f"{label}: control character")


def month_window(start, end):
    require(isinstance(start, str) and isinstance(end, str), "comparison: invalid month")
    require(bool(re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", start)) and bool(re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", end)), "comparison: use YYYY-MM")
    y1, m1 = map(int, start.split("-"))
    y2, m2 = map(int, end.split("-"))
    require(1900 <= y1 <= 2100 and y1 == y2 and m1 <= m2, "comparison: window must be within one calendar year")
    return [(y1, m) for m in range(m1, m2 + 1)]


def validate(data):
    plain_object(data, TOP_FIELDS, TOP_FIELDS - {"thresholds"}, "dataset")
    require(type(data["schemaVersion"]) is int and data["schemaVersion"] == 1, "schemaVersion: expected 1")
    require(type(data["synthetic"]) is bool, "synthetic: expected boolean")
    text_field(data["title"], "title")
    require(data["coverage"] in ("partial", "complete"), "coverage: invalid")
    require(isinstance(data["asOfDate"], str) and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", data["asOfDate"])), "asOfDate: use ISO date")
    as_of = date.fromisoformat(data["asOfDate"])
    fields = {"currentStart", "currentEnd", "baselineStart", "baselineEnd"}
    comp = data["comparison"]
    plain_object(comp, fields, fields, "comparison")
    current = month_window(comp["currentStart"], comp["currentEnd"])
    baseline = month_window(comp["baselineStart"], comp["baselineEnd"])
    require(len(current) == len(baseline) and all(cy == by + 1 and cm == bm for (cy, cm), (by, bm) in zip(current, baseline)), "comparison: use matching months one year apart")
    require(date(current[-1][0], current[-1][1], calendar.monthrange(*current[-1])[1]) <= as_of, "comparison: current window is not closed")
    thresholds = data.get("thresholds", {})
    plain_object(thresholds, set(DEFAULT_THRESHOLDS), set(), "thresholds")
    thresholds = DEFAULT_THRESHOLDS | thresholds
    for key in ("minCurrentUnits", "minAbsoluteChange"):
        require(type(thresholds[key]) is int and thresholds[key] > 0, f"{key}: expected positive integer")
    require(type(thresholds["rate"]) in (int, float) and 0 < thresholds["rate"] <= 10, "rate: expected finite ratio in (0,10]")
    records = data["records"]
    require(isinstance(records, list) and len(records) > 0, "records: expected nonempty list")
    seen, metadata = set(), {}
    for n, row in enumerate(records):
        label = f"record {n + 1}"
        plain_object(row, RECORD_FIELDS, RECORD_FIELDS, label)
        for key in ("market", "seriesId", "brand", "model", "segment"):
            text_field(row[key], f"{label}.{key}")
        require(bool(re.fullmatch(r"[A-Z]{2}", row["market"])), f"{label}: invalid market")
        require(row["seriesScope"] in ("model", "family"), f"{label}: invalid seriesScope")
        require(type(row["year"]) is int and 1900 <= row["year"] <= 2100, f"{label}: invalid year")
        require(type(row["month"]) is int and 1 <= row["month"] <= 12, f"{label}: invalid month")
        require(row["status"] in ("reported", "missing", "unreported_future"), f"{label}: invalid status")
        closed = date(row["year"], row["month"], calendar.monthrange(row["year"], row["month"])[1]) <= as_of
        if row["status"] == "reported":
            require(type(row["units"]) is int and 0 <= row["units"] <= 10**12, f"{label}: units must be nonnegative integer")
            require(closed, f"{label}: reported month is not closed")
        else:
            require(row["units"] is None, f"{label}: unknown units must be null")
            require(row["status"] != "unreported_future" or not closed, f"{label}: future status on a closed month")
        key = row["market"], row["seriesId"], row["year"], row["month"]
        require(key not in seen, f"{label}: duplicate market-series-month")
        seen.add(key)
        series_key = key[:2]
        meta = tuple(row[k] for k in ("brand", "model", "segment", "seriesScope"))
        require(series_key not in metadata or metadata[series_key] == meta, f"{label}: conflicting series metadata")
        metadata[series_key] = meta
    return current, baseline, thresholds


def window_summary(months, values):
    reported = [values[m]["units"] for m in months if m in values and values[m]["status"] == "reported"]
    missing = [f"{y:04d}-{m:02d}" for y, m in months if (y, m) not in values or values[(y, m)]["status"] != "reported"]
    return {"units": sum(reported) if not missing else None, "knownUnits": sum(reported), "reportedMonths": len(reported), "expectedMonths": len(months), "missingMonths": missing}


def candidate(row, thresholds):
    a, b, change, rate = row["currentUnits"], row["baselineUnits"], row["delta"], row["yoy"]
    if not row["comparable"]:
        signal, question = "insufficient_data", "补齐或解释同窗口缺失与车系范围，之后再比较。"
    elif b == 0:
        signal, question = "zero_base", "确认基期零值、车系定义与上市阶段，不能把零基期自动认作新品。"
    elif rate >= thresholds["rate"]:
        signal = "scale_growth" if a >= thresholds["minCurrentUnits"] and change >= thresholds["minAbsoluteChange"] else "small_base_growth"
        question = "核对绝对规模，研究一个具体用户场景与未满足需求，再核对代际接口和现有方案。"
    elif rate <= -thresholds["rate"] and -change >= thresholds["minAbsoluteChange"]:
        signal, question = "decline_review", "区分供给、生命周期、竞争、价格与统计变化，不能仅从销量断言原因。"
    else:
        signal, question = "watch", "保留观察；如有具体业务问题再设计验证，不凭小幅变化做商业承诺。"
    return {"id": f"{row['market']}:{row['seriesId']}", "market": row["market"], "seriesId": row["seriesId"], "signal": signal,
            "status": "candidate_only", "facts": {k: row[k] for k in ("currentUnits", "baselineUnits", "delta", "yoy", "reason")},
            "hypothesis": "是否存在值得验证的细分使用场景；尚未证实。", "nextStep": question,
            "verificationQuestions": ["谁遇到什么问题，频率与严重程度如何？", "具体代际/配置的接口和尺寸是否适配？", "现有竞品、渠道需求及单位经济能否支持小规模验证？"],
            "stopCondition": "关键适配不成立、需求证据不足、成本不可行或缺少授权时停止扩展。"}


def analyze(data, input_hash):
    current, baseline, thresholds = validate(data)
    groups = defaultdict(list)
    for record in data["records"]:
        groups[(record["market"], record["seriesId"])].append(record)
    rows = []
    for (market, series_id), records in sorted(groups.items()):
        values = {(r["year"], r["month"]): r for r in records}
        c, b = window_summary(current, values), window_summary(baseline, values)
        comparable = c["units"] is not None and b["units"] is not None
        delta = c["units"] - b["units"] if comparable else None
        rate = delta / b["units"] if comparable and b["units"] != 0 else None
        reason = ("zero_base" if b["units"] == 0 else "comparable") if comparable else "incomplete_window"
        row = {k: records[0][k] for k in ("brand", "model", "segment", "seriesScope")}
        row |= {"market": market, "seriesId": series_id, "current": c, "baseline": b, "currentUnits": c["units"], "baselineUnits": b["units"], "delta": delta, "yoy": rate, "comparable": comparable, "reason": reason,
                "monthly": [{"year": y, "month": m, "units": r["units"], "status": r["status"]} for (y, m), r in sorted(values.items())]}
        row["signal"] = candidate(row, thresholds)["signal"]
        rows.append(row)
    segments = []
    for market, segment in sorted({(r["market"], r["segment"]) for r in rows}):
        pair = [r for r in rows if (r["market"], r["segment"]) == (market, segment) and r["comparable"]]
        a, b = sum(r["currentUnits"] for r in pair), sum(r["baselineUnits"] for r in pair)
        segments.append({"market": market, "segment": segment, "pairedSeries": len(pair), "currentUnits": a if pair else None, "baselineUnits": b if pair else None, "delta": a - b if pair else None, "yoy": (a - b) / b if b else None})
    analysis = {"schemaVersion": 1, "title": data["title"], "asOfDate": data["asOfDate"], "synthetic": data["synthetic"], "coverage": data["coverage"], "unit": "vehicles", "comparison": data["comparison"], "thresholds": thresholds, "inputSha256": input_hash, "series": rows, "segments": segments}
    opportunities = {"schemaVersion": 1, "inputSha256": input_hash, "status": "candidate_only", "items": [candidate(r, thresholds) for r in rows]}
    qa = {"schemaVersion": 1, "status": "pass", "scope": "structure_and_internal_arithmetic_only", "inputSha256": input_hash, "recordCount": len(data["records"]), "seriesCount": len(rows), "pairedSeries": sum(r["comparable"] for r in rows), "exclusions": [{"market": r["market"], "seriesId": r["seriesId"], "reason": r["reason"], "currentMissing": r["current"]["missingMonths"], "baselineMissing": r["baseline"]["missingMonths"]} for r in rows if not r["comparable"]]}
    return analysis, opportunities, qa


def markdown_report(analysis, opportunities):
    comp = analysis["comparison"]
    lines = ["# 车辆销量分析", "", "**合成演示：车型与数字均为虚构。**" if analysis["synthetic"] else "用户提供数据；请按授权范围保存及共享。", "", f"窗口：{comp['currentStart']} 至 {comp['currentEnd']}；基期：{comp['baselineStart']} 至 {comp['baselineEnd']}。单位：辆。", "", "口径：配对样本；各国分别统计。销量不是保有量。脚本QA不证明数据真实性或市场完整性。", ""]
    for market in sorted({r["market"] for r in analysis["series"]}):
        pair = [r for r in analysis["series"] if r["market"] == market and r["comparable"]]
        a, b = sum(r["currentUnits"] for r in pair), sum(r["baselineUnits"] for r in pair)
        if not pair:
            lines.append(f"- {market}：无完整配对样本。")
            continue
        growth = f"{(a-b)/b:+.1%}" if b else "未知（零基期）"
        lines.append(f"- {market}：{len(pair)} 个可比车系；{b:,} → {a:,} 辆，变化 {a-b:+,} 辆，同比 {growth}。")
    lines += ["", "## 逐项研究入口", "", "以下仅为候选，尚未完成真实需求、适配或经济验证。", ""]
    for item in opportunities["items"]:
        # Input-derived names are inline code, not executable Markdown/HTML.
        label = item["id"].replace("`", "").replace("<", "&lt;").replace(">", "&gt;")
        lines.append(f"- `{label}` — {item['signal']}：{item['nextStep']}")
    lines += ["", "下一步由助手结合获准材料另写 research-review.md；没有材料时列出缺口与停止条件，不称研究完成。", "", f"输入 SHA-256：{analysis['inputSha256']}", ""]
    return "\n".join(lines)


def build(input_path, output):
    raw = Path(input_path).read_bytes()
    # Reject duplicate JSON properties rather than silently accepting the last one.
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "JSON: duplicate property")
            result[key] = value
        return result
    data = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError("JSON: nonfinite number")))
    analysis, opportunities, qa = analyze(data, hashlib.sha256(raw).hexdigest())
    template = (SKILL_ROOT / "assets" / "dashboard.html").read_text(encoding="utf-8")
    require(template.count("__ANALYSIS_JSON__") == 1, "template: expected one payload marker")
    payload = json.dumps(analysis, ensure_ascii=False, allow_nan=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    output = Path(output).resolve()
    require(not output.exists(), "output directory already exists; choose a new version")
    output.parent.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix=".vehicle-build-", dir=output.parent))
    try:
        (work / "dashboard.html").write_text(template.replace("__ANALYSIS_JSON__", payload), encoding="utf-8", newline="\n")
        (work / "report.md").write_text(markdown_report(analysis, opportunities), encoding="utf-8", newline="\n")
        for name, obj in (("analysis.json", analysis), ("opportunities.json", opportunities), ("qa.json", qa)):
            (work / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8", newline="\n")
        work.rename(output)
    except BaseException:
        shutil.rmtree(work, ignore_errors=True)
        raise
    return qa


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Existing monthly JSON matching references/data-contract.md")
    parser.add_argument("--output", required=True, type=Path, help="New output directory; never overwrite")
    args = parser.parse_args()
    try:
        qa = build(args.input, args.output)
    except (OSError, ValueError, TypeError) as exc:
        parser.exit(2, f"Build stopped: {exc}\n")
    print(json.dumps({"status": qa["status"], "seriesCount": qa["seriesCount"], "pairedSeries": qa["pairedSeries"]}))


if __name__ == "__main__":
    main()
