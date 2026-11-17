# 已有数据的规范化合同

只描述用户已经持有的数据如何进入分析，不强制数据来源；真实UTV/ATV来源链另见案例说明。

## JSON v1

顶层仅允许：`schemaVersion,title,asOfDate,synthetic,coverage,comparison,thresholds,records`。`schemaVersion=1`，`synthetic` 必须为布尔值，`coverage` 为 `partial` 或 `complete`；后者只是输入声明，不表示脚本做过完整市场核验。未声明字段拒绝进入输出，防止误带私有附加信息。不要将带 URL、凭证或额外业务字段的原表直接交给公开构建。

```json
{
  "schemaVersion": 1,
  "title": "合成销量演示",
  "asOfDate": "2025-06-30",
  "synthetic": true,
  "coverage": "partial",
  "comparison": {
    "currentStart": "2025-01", "currentEnd": "2025-06",
    "baselineStart": "2024-01", "baselineEnd": "2024-06"
  },
  "thresholds": {"minCurrentUnits": 10000, "minAbsoluteChange": 1000, "rate": 0.1},
  "records": [
    {"market": "US", "seriesId": "aster.canyon", "brand": "Aster", "model": "Canyon",
     "segment": "SUV", "seriesScope": "model", "year": 2025, "month": 1,
     "units": 2600, "status": "reported"}
  ]
}
```

这是单行结构示例，不能作为完整六个月比较。完整合成输入在 `assets/demo.json`。

| 字段 | 类型、范围及规则 |
|---|---|
| `title` | 非空字符串，最长 160 字；不放私人备注 |
| `asOfDate` | ISO 日期；只允许月底已结束的月份为 reported；当月未结束数据暂不进完整月比较 |
| `comparison.*` | `YYYY-MM`，同一日历年中的连续月份；两窗口对应同月份、相差一年。已覆盖月份不足也保留，但不计算不完整序列的同比 |
| `market` | ISO 风格两位大写代码，示例 US/CA/MX；不得混加各国样本 |
| `seriesId` | 车系稳定主键；唯一键为 `market,assetType,metricKind,seriesId,year,month`；别名先在适配层人工核对 |
| `brand,model,segment` | 非空显示名，同一市场-载具类型-指标-系列的元数据必须一致；未知分类显式写 `Unclassified` |
| `seriesScope` | `model` 或 `family`；family 代表多子车型聚合，不拆成单车型 |
| `year,month` | 整数；1900–2100 / 1–12；日历年月，不是车型年 |
| `units` | reported 必须为非负整数、船舶单位“艘”，其他载具单位“台”；0 是真实零；其余状态必须为 null |
| `status` | `reported / missing / unreported_future`。没有记录也按缺失处理；future 必须指尚未结束的月份 |

所有字符串作为文本处理，HTML 转义；CSV 导出防范公式首字符。只导出白名单分析字段，不回传未知字段。

## 指标口径

1. 当前完整窗口销量 = 窗口内每个月均 reported 才可求和。`knownUnits` 只是已知小计，不能替代完整窗口。
2. 基期规则相同。两期完整且车系/市场/统计边界一致才可比。
3. `delta = currentUnits - baselineUnits`；`yoy = delta / baselineUnits`，基期为 0 则 yoy=null、标 `zero_base`，不显示无限增长。
4. 分类两期总量只能汇总同一组可比序列。总体、矩阵、分类条形图和占比一律注明“配对样本”。单期销量排名允许展示当前完整但基期缺失的车系，必须带不可比标签。
5. 排名受筛选条件影响；只在相同市场和统计窗口中排序，不能把 CA 与 US 混排后声称北美排名。
6. 年度汇总只在同年12个月都 reported 时标全年；不足时写“已知 N 个月小计”。不能把历史累计销量当保有量。
7. 不能由季度/年度数平分出月度数；该类输入另做原粒度表。YTD 同比使用相同截止月份；不同截止日先对齐，无法对齐则不比较。
8. 发现重复别名、历史回填改变、统计范围变更或代际聚合不一致时先隔离/解释，不用数学一致性替代真实性核验。

## 更新与差异

每次用新目录生成；比较输入 SHA-256、行级键和值，区分新增月份、历史修订、分类重映射和边界变化。历史修订不是当月增长。保留原版，不静默覆盖旧报告。脚本不自动做版本差异，助手需按此次请求补写说明。

## 跨载具兼容字段

每条record可选 `assetType`：`automobile / motorcycle / utv / atv / boat`，默认 `automobile`；可选 `metricKind`：`retail_sales / wholesale / deliveries / new_registrations`，默认 `retail_sales`。必须如实声明已有表的指标，不能把模糊“销量”悄悄改成零售。

两者进入去重键、分组、比较和页面筛选。相同seriesId出现在UTV与ATV，或者零售与批发，不是同一条数据；每次汇总只选一个类型、一个指标。船舶单位显示艘，其他数量显示台；舷外机/发动机/配件不得当作船舶数量。所有指标依然是月度流量，保有量和召回批次情景不属于这份schema。

年款/版本/船体或动力配置需更细时用独立稳定seriesId，声明family/model边界；同一数据集中不要同时收录父级合计与其子级拆分形成重计。只有合并数量时不能按版本平均分。
