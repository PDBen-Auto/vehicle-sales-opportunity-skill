# 载具数量分析

**合成演示：型号与数字均为虚构。**

窗口：2025-01 至 2025-06；基期：2024-01 至 2024-06。单位：船舶为艘，其他为台。

口径：配对样本；各国、载具类型与指标分别统计。流量不是保有量。脚本QA不证明数据真实性或市场完整性。

- CA / automobile / retail_sales：1 个可比系列；1,200 → 1,560 台/艘，变化 +360 台/艘，同比 +30.0%。
- MX / automobile / retail_sales：1 个可比系列；2,400 → 2,580 台/艘，变化 +180 台/艘，同比 +7.5%。
- US / automobile / retail_sales：6 个可比系列；44,520 → 44,820 台/艘，变化 +300 台/艘，同比 +0.7%。

## 逐项研究入口

以下仅为候选，尚未完成真实需求、适配或经济验证。

- `CA:automobile:retail_sales:aster.canyon` — small_base_growth：核对绝对规模，研究一个具体用户场景与未满足需求，再核对代际接口和现有方案。
- `MX:automobile:retail_sales:aster.canyon` — watch：保留观察；如有具体业务问题再设计验证，不凭小幅变化做商业承诺。
- `US:automobile:retail_sales:aster.canyon` — scale_growth：核对绝对规模，研究一个具体用户场景与未满足需求，再核对代际接口和现有方案。
- `US:automobile:retail_sales:boreal.ridge` — decline_review：区分供给、生命周期、竞争、价格与统计变化，不能仅从销量断言原因。
- `US:automobile:retail_sales:cedar.spark` — small_base_growth：核对绝对规模，研究一个具体用户场景与未满足需求，再核对代际接口和现有方案。
- `US:automobile:retail_sales:dune.trace` — insufficient_data：补齐或解释同窗口缺失与车系范围，之后再比较。
- `US:automobile:retail_sales:ember.launch` — zero_base：确认基期零值、车系定义与上市阶段，不能把零基期自动认作新品。
- `US:automobile:retail_sales:fjord.glide` — watch：保留观察；如有具体业务问题再设计验证，不凭小幅变化做商业承诺。
- `US:automobile:retail_sales:gale.van` — watch：保留观察；如有具体业务问题再设计验证，不凭小幅变化做商业承诺。

下一步由助手结合获准材料另写 research-review.md；没有材料时列出缺口与停止条件，不称研究完成。

输入 SHA-256：d02bbd3b2048456b6f4285612d81d927fa074b2263c051dfbe51c505c701bfde
