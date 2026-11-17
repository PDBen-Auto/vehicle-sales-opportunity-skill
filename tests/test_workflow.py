"""Meaningful offline invariants; no third party test dependencies."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "vehicle-sales-opportunity"
spec = importlib.util.spec_from_file_location("builder", SKILL / "scripts" / "build_dashboard.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def fixture():
    return json.loads((SKILL / "assets" / "demo.json").read_text(encoding="utf-8"))


class AnalysisTests(unittest.TestCase):
    def run_data(self, data=None):
        return builder.analyze(data or fixture(), "f" * 64)

    def test_exact_same_window_math(self):
        analysis, _, _ = self.run_data()
        row = next(r for r in analysis["series"] if r["seriesId"] == "aster.canyon" and r["market"] == "US")
        self.assertEqual((row["baselineUnits"], row["currentUnits"], row["delta"]), (12000, 15600, 3600))
        self.assertAlmostEqual(row["yoy"], 0.3)
        self.assertEqual(row["signal"], "scale_growth")

    def test_missing_not_zero_and_excluded_from_paired_total(self):
        analysis, _, qa = self.run_data()
        row = next(r for r in analysis["series"] if r["seriesId"] == "dune.trace")
        self.assertIsNone(row["currentUnits"])
        self.assertEqual(row["current"]["knownUnits"], 5000)
        self.assertIsNone(row["delta"])
        self.assertIn("2025-03", row["current"]["missingMonths"])
        self.assertTrue(any(r["seriesId"] == "dune.trace" for r in qa["exclusions"]))
        suv = next(s for s in analysis["segments"] if s["market"] == "US" and s["segment"] == "SUV")
        self.assertEqual(suv["currentUnits"], sum(r["currentUnits"] for r in analysis["series"] if r["market"] == "US" and r["segment"] == "SUV" and r["comparable"]))

    def test_zero_base_no_infinite_yoy(self):
        analysis, _, _ = self.run_data()
        row = next(r for r in analysis["series"] if r["seriesId"] == "ember.launch")
        self.assertTrue(row["comparable"])
        self.assertEqual(row["baselineUnits"], 0)
        self.assertIsNone(row["yoy"])
        self.assertEqual(row["signal"], "zero_base")

    def test_markets_remain_separate(self):
        analysis, _, _ = self.run_data()
        rows = [r for r in analysis["series"] if r["seriesId"] == "aster.canyon"]
        self.assertEqual({r["market"] for r in rows}, {"US", "CA", "MX"})
        self.assertEqual(len(rows), 3)
        self.assertNotEqual(rows[0]["currentUnits"], rows[1]["currentUnits"])

    def test_duplicate_is_rejected(self):
        data = fixture()
        data["records"].append(data["records"][0].copy())
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.run_data(data)

    def test_bad_units_and_status_are_rejected(self):
        for key, value in [("units", -1), ("units", 0.5), ("units", True), ("status", "estimated")]:
            with self.subTest(key=key, value=value):
                data = fixture()
                data["records"][0][key] = value
                with self.assertRaises(ValueError):
                    self.run_data(data)

    def test_null_reported_rejected(self):
        data = fixture()
        data["records"][0]["units"] = None
        with self.assertRaises(ValueError):
            self.run_data(data)

    def test_future_reported_rejected(self):
        data = fixture()
        data["records"][0]["year"] = 2026
        with self.assertRaisesRegex(ValueError, "not closed"):
            self.run_data(data)

    def test_future_placeholder_not_zero(self):
        data = fixture()
        row = copy.deepcopy(data["records"][0])
        row.update(year=2025, month=12, units=None, status="unreported_future")
        data["records"].append(row)
        analysis, _, _ = self.run_data(data)
        self.assertEqual(analysis["series"][0]["currentUnits"], self.run_data()[0]["series"][0]["currentUnits"])

    def test_mismatched_month_windows_rejected(self):
        data = fixture()
        data["comparison"]["baselineEnd"] = "2024-12"
        with self.assertRaisesRegex(ValueError, "matching months"):
            self.run_data(data)

    def test_metadata_conflict_rejected(self):
        data = fixture()
        data["records"][1]["seriesScope"] = "family"
        with self.assertRaisesRegex(ValueError, "conflicting"):
            self.run_data(data)

    def test_unknown_fields_not_leaked(self):
        for where in ("top", "row"):
            data = fixture()
            target = data if where == "top" else data["records"][0]
            target["private_extra"] = "not-for-output"
            with self.assertRaisesRegex(ValueError, "unexpected fields"):
                self.run_data(data)

    def test_all_unknown_no_false_zero(self):
        data = fixture()
        for row in data["records"]:
            row.update(units=None, status="missing")
        analysis, _, qa = self.run_data(data)
        self.assertEqual(qa["pairedSeries"], 0)
        self.assertTrue(all(r["currentUnits"] is None for r in analysis["series"]))
        self.assertTrue(all(s["currentUnits"] is None for s in analysis["segments"]))

    def test_all_candidates_preserved(self):
        analysis, opportunities, _ = self.run_data()
        self.assertEqual(len(analysis["series"]), len(opportunities["items"]))
        self.assertTrue(all(i["status"] == "candidate_only" for i in opportunities["items"]))

    def test_optional_thresholds_default_and_override(self):
        data = fixture()
        data.pop("thresholds", None)
        a, _, _ = self.run_data(data)
        self.assertEqual(a["thresholds"]["minCurrentUnits"], 10000)
        data["thresholds"] = {"minCurrentUnits": 1000000}
        a, _, _ = self.run_data(data)
        row = next(r for r in a["series"] if r["seriesId"] == "aster.canyon" and r["market"] == "US")
        self.assertEqual(row["signal"], "small_base_growth")

    def test_safe_html_embedding_and_output_set(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp) / "input.json", Path(tmp) / "out"
            data = fixture()
            data["title"] = '</script><script>alert("x")</script>'
            src.write_text(json.dumps(data), encoding="utf-8")
            builder.build(src, out)
            html = (out / "dashboard.html").read_text(encoding="utf-8")
            self.assertNotIn(data["title"], html)
            self.assertIn("\\u003c/script>", html)
            self.assertEqual({p.name for p in out.iterdir()}, {"dashboard.html", "analysis.json", "report.md", "qa.json", "opportunities.json"})
            with self.assertRaisesRegex(ValueError, "already exists"):
                builder.build(src, out)

    def test_invalid_input_does_not_create_deliverable(self):
        with tempfile.TemporaryDirectory() as tmp:
            src, out = Path(tmp) / "bad.json", Path(tmp) / "out"
            src.write_text('{"schemaVersion":1,"schemaVersion":2}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate property"):
                builder.build(src, out)
            self.assertFalse(out.exists())

    def test_missing_file_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(OSError):
                builder.build(Path(tmp) / "absent.json", Path(tmp) / "out")


if __name__ == "__main__":
    unittest.main()
