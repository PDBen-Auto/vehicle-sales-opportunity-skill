"""Build the portable report from the same data used by the workbook."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / '输出'
DATA = OUT / 'data'
d = json.loads((DATA / 'dataset.json').read_bytes())
images = json.loads((DATA / 'vehicle_images.json').read_bytes())

def embedded(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

template = (ROOT / 'dashboard.template.html').read_text(encoding='utf-8')
assert template.count('__DATA__') == 1 and template.count('__IMAGES__') == 1
html = template.replace('__DATA__', embedded(d)).replace('__IMAGES__', embedded(images))
(OUT / '北美UTV保有量研究-20261117.html').write_text(html, encoding='utf-8')

rows = {r['canonical_model_id']: r for r in d['scenarios'] if r['country'] == 'US'}
examples = ['polaris.rzr-xp1000', 'polaris.ranger-xp1000', 'polaris.ranger-900',
            'honda.pioneer-1000', 'kawasaki.mule-pro-legacy-group', 'yamaha.rhino-group']
table = '\n'.join('| ' + ' | '.join([rows[mid]['make'] + ' ' + rows[mid]['model'],
    f"{rows[mid]['historical_affected_units']:,}",
    f"{rows[mid]['conservative_batch_scenario']:,}",
    f"{rows[mid]['severe_batch_scenario']:,}–{rows[mid]['less_severe_batch_scenario']:,}",
    rows[mid]['cohort_window']]) + ' |' for mid in examples)
source_list = '\n'.join(f"- [{s['title']}]({s['url']})（{s['published_at']}，检索 2026-11-17）"
    for s in d['sources'] if s['source_id'] in ['cpsc-8296','cpsc-10106','cpsc-8797','cpsc-8580','cpsc-8165'])
counts = d['counts']
report = f'''# 北美 UTV 车型保有量研究 · 首版

研究截止：2026-11-17。地区分别为美国、加拿大、墨西哥；单位为台。

目前能做的是已知历史车辆批次的保守在用情景，尚不能给出每款 UTV 的完整当前保有量。首版收录 {counts['catalog_entries']} 个目录条目：{counts['named_series_entries']} 个命名系列/子车型与 {counts['source_group_entries']} 个来源合并组。美国 63 个、加拿大 15 个、墨西哥 1 个条目有可计算批次。全量在用量、登记/VIO观察记录均未取得。

124 不是已完成全市场核对的车型总数，也不意味着每款都已核实在三个国家销售。页面及数据分别保留该国数量已核实、该国官方目录身份已核实、该国身份尚未核实三种状态。合并组与子车型不能相加。

## 查看与使用

- 直接打开 [交互研究面板](北美UTV保有量研究-20261117.html)，无需服务器或联网加载资源。可按国家、品牌、用途和数据范围筛选，查看历史车型图片、批次依据、计算、来源与缺口；可调整参数并导出当前筛选 CSV。
- [Excel 工作簿](北美UTV车型保有量保守情景-20261117.xlsx) 包含 8 张表。修改“参数”的黄色单元格后，“批次计算”和“车型估算”公式会重算。网页与 Excel 是独立副本，不会互相写回。
- [完整情景 CSV](data/cohort_scenarios.csv)、[批次输入 CSV](data/cohort_components.csv)、[来源台账](data/source_ledger.csv) 适合后续更新或导入。CSV 和网页初始值采用本次参数快照。
- 保持整个“输出”文件夹一起移动，Excel、说明和本地来源快照链接才会继续有效。HTML 本身已内嵌数据与图片。

## 部分结果示例

下表为美国已知批次，均不是完整车型保有量。顺序不能用于判断市场份额或销量排名。原始批次数也可能是公告约数。

| 车型 / 来源统计组 | 历史批次数 | 批次保守基准 | 更严–较缓情景 | 来源窗口 |
|---|---:|---:|---:|---|
{table}

例如 RZR XP 1000 / XP 4 1000：MY2014–2018 的约 107,000 台与 MY2024–2025 的约 21,000 台按不重叠批次建模。首版基准为 52,600 台；MY2019–2023、其余未覆盖 VIN 和新增销售均未补量。这个数字反映所选历史批次在假设下的留存量，不是该系列全车型当前存量。

## 方法与参数

每个历史批次分别计算，再合并到同国家、同系列或来源合并组：

`历史公告车辆数 × 兑现系数 × 年保留系数 ^ 压力车龄`

`压力车龄 = max(0, 2026 − min(来源窗口起年, 最早起售年))`

| 参数情景 | 兑现系数 | 年保留系数 |
|---|---:|---:|
| 更严压力 | 80% | 88% |
| 保守基准 | 90% | 93% |
| 较缓压力 | 95% | 97% |

以上均为研究者假设，未经 UTV 实证存活率标定。兑现系数只是对库存、停用等未核验影响的折减；年保留系数用于对报废、迁出和不活跃施压，不能解释成已观察到的实际概率。把整个批次都按最老年份计龄，偏向低估。保守基准和更严情景向下取整：计算值≥1,000按100台，≥100按10台，其余按1台；较缓情景向上取整。

压力情景区间不是统计置信区间，也不是严格存量上下界。没有证据能保证这些车辆至今仍在用、仍在原国家或全部已售给终端用户。

## 重复与异常处理

- 只对来源明确不重叠的年款批次求和。重叠召回、范围不明或混合来源保留在补充证据表，不重复增加数量。
- Honda Talon 的 34,000 已含此前 32,000，不能加成 66,000；Pioneer 1000 的 82,000 不再加早期 65,000 / 56,000。
- Rhino 450/660 的 120,000 与 Rhino 700 的 25,000 是来源明确列示的不同车型部分，合计 145,000；子车型不拆量。
- RANGER XD 1500 的 10,500 台车辆和另 1,336 套绞盘分开；安全带、轴承、加热器等配件公告及 ATV 均不计入。
- Brawley 两份公告分别约 210 与 190 台，均称 MY2024–2026。未解释差异，本版选较新较小的 190，保留冲突，不相加。
- GENERAL 销售期倒置、RTV400/500 年款与起售期矛盾均保留原文，使用可识别更早年份施压，不修造日期。
- 部分来源只给销售/生产窗口。页面明细与批次表保留 `window_basis`，不把窗口冒充完整代际或精确 MY。

## 与参考车型数据逻辑的对应

沿用“国家 → 稳定车型系列或明确来源合并组 → 批次/来源窗口 → 原始数量与来源”的下钻路径，保留筛选、车型详情和导出。未将累计销量、收入、生产、召回数量写成登记或 VIO；没有按年份平均分摊历史数量，也没有编造代际。

历史批次情景单独写入 `cohort_scenarios.csv`。标准 `vehicle_population.csv`、`vehicle_population_rollup.csv`、`annual_sales.csv` 和国家控制总量表保留空表头，防止被后续系统误当成已取得的观察数据。该做法是探索性研究扩展，不是已经校准的车型保有量模型。

## 来源与覆盖

数量主要来自美国 CPSC 官方公告/API；加拿大、墨西哥只采用公告明确另列的当地数量。车型身份补充来自官方目录。105 个来源保留 URL、发布日期、检索日、本地快照与 SHA-256。目录访问失败不能说明车型不存在。CPSC 全量抓取是候选资料，不代表本版已审计所有历史召回。

代表性数量来源：

{source_list}

车型图片取自对应 CPSC 历史公告，用来识别来源批次；不能据此判断现款外观、接口或配件适配。图片并非 AI 生成；本研究不承诺外部图片的公开商用授权。

## 使用边界与下一步

当前最适合用作“已取得哪些可追溯批次数量”的研究底表。不能将不同车型情景值直接比较为市场份额，不能计算北美总量，也不能据此直接给出配件需求或销量预测。召回发生不等于车辆已报废，也不证明其当前安全可用。

若要升级到完整分车型存量，需要取得同口径的历史零售/新登记、车型级 VIO 或不重叠地方登记，并补齐 UTV 适用的存活、迁移和停用参数。候选商业渠道包括 PPM、MIC/S&P、Statistical Surveys；ATV/UTV覆盖、国家、车型粒度、历史长度和许可仍须以供应商样本确认。本次没有购买数据库。

目录仍缺部分现售、停产及贴牌车型；加拿大未系统覆盖当地召回/登记，墨西哥仅一个合并组可算。缺口详见 [缺口表](data/known_gaps.csv)。后续每月更新应保留本次参数和输入版本，新增批次先检查年份/VIN重叠；不能简单累加每月召回数量。

## 检查记录

数据脚本的 3,053 项检查已通过，涵盖唯一键、来源关联、快照哈希、逐组件复算、舍入、合并组边界、重要重复/排除案例，以及网页、CSV、Excel初始数字一致性。检查结果在 `data/scenario_qa_report.json`。标准结构校验为 0 错误、77 警告：76 个代际未知、1 个市场覆盖不全，均保留为真实缺口；详见 `data/qa_report.json`。结构和公式检查通过不等于保有量已被实证验证。

Excel 已在 Artifact Tool 计算引擎进行参数敏感性和恢复检查；原生 Microsoft Excel 的重算尚未测试。网页桌面和手机视口的 37 项功能检查已通过，实际检查结果记录在 `data/delivery_qa.json`；52 张嵌入图片可解码。研究截止和参数不会自动随打开日期变化。

本次交付保存在本对话主题目录，状态为完成候选，尚未取得用户采用确认。当前对话没有已确认的业务项目归属，因此未另行复制到按项目组织的备份库。
'''
(OUT / '研究说明.md').write_text(report, encoding='utf-8')
print(json.dumps({'html_bytes': len(html.encode('utf-8')), 'models': len(d['models']), 'images': sum(bool(x.get('image_data')) for x in images)}))
