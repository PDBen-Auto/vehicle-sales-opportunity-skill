# 跨载具销量可视化与机会调研

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

按用户明确指定的语言输出，否则跟随请求语言。保留命令、技能 ID、JSON 键、枚举值、单位和来源原文；翻译与原文分开，不通过语言推定国家、币种或司法辖区。先读取完整规范中与任务相关的详细引用，执行原有校验和授权要求。

## 安装与使用

下载或克隆仓库，将下列技能目录连同其 references、scripts、assets 等现有依赖一起放入宿主的技能目录。保留目录名和 SKILL.md；仅更换说明语言无需重复安装。安装命令供用户自行选择，不表示已安装或启用。

```sh
git clone https://github.com/PDBen-Auto/vehicle-sales-opportunity-skill.git
```

## 跨载具销量可视化与机会调研

`vehicle-sales-opportunity`

将汽车、摩托车、UTV、ATV和船舶已有数量数据可视化，同期比较并设计有据机会研究。

技能目录: `skills/vehicle-sales-opportunity`

**实现依据与依赖**

获准数据与市场/日历期/指标/单位；脚本需Python3.10+标准库，视觉检查需浏览器；核心离线无需账号/API；研究验证需产品/用户/适配/成本证据。

**输入**

必需月度dataset JSON、同月基准窗口和新输出目录；可选阈值、简报、支持材料；保留缺失、assetType和metricKind；季度/年度不能平分月份。

**输出**

dashboard.html、analysis.json、opportunities.json、report.md、qa.json；助手另写research-review.md；候选和算术PASS不代表需求/适配/ROI成立。

[执行流程 · 边界与停止条件 · 示例请求](skills/vehicle-sales-opportunity/references/i18n/zh-CN.md)

> 请使用 `$vehicle-sales-opportunity` — 比较美加墨1–6月与上年同月；销量+30%只是研究信号，不能推出配件需求也+30%；用简体中文输出，保留证据、未知项与操作边界。

[Online examples](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/) · [UTV case](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/cases/utv-atv/) · [Original vehicle dashboard](https://north-america-vehicle-dashboard.pages.dev/)

## 语言覆盖与验证

这是本技能的本地化操作指南，覆盖用途、依赖、输入输出、步骤、示例及边界，不是全部引用文档的逐句翻译。详细技术引用、历史案例、脚本错误、示例网页及图片保留原文；助手可按请求解释它们。本次文档经过结构、链接和关键约束核对，尚无逐语种母语人工审校。

交付前逐项核对输入、证据、缺失值、输出文件和原有完成标准；未执行的步骤标为未验证，不把脚本退出成功当业务成功。
