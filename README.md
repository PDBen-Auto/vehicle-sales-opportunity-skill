# 汽车 · 摩托车 · UTV · ATV · 船舶：数量可视化与机会调研 Skill

把已有数量表变成可核对的交互看板，再把变化转为有证据边界的机会研究。支持五类载具，零售销量、批发出货、交付量与新注册量分开计算；附上 UTV/ATV 从数据渠道调查到研究页面的完整真实案例。

Skill ID 保留为 `vehicle-sales-opportunity`，升级已有安装即可，不需要安装一个新名字。

**[直接打开在线案例](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/)** · **[UTV真实研究页面](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/cases/utv-atv/)**

## 从这里开始

| 入口 | 内容 |
|---|---|
| [完整 UTV/ATV 真实案例](cases/utv-atv/README.md) | 来源渠道、原始证据、去重与计算、页面设计、Excel、可离线复现脚本 |
| [案例来源渠道](cases/utv-atv/channels.md) | PPM、MIC/S&P、SSI、经销商样本、厂商及官方公告的口径与访问条件 |
| [真实 UTV 研究页面](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/cases/utv-atv/) | 浏览器直接打开；真实品牌、车型、数量、图片和来源 |
| [五类载具合成演示](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/multitype-demo/dashboard.html) | 浏览器直接打开；五类载具切换，UTV 零售与批发隔离 |
| [原汽车合成演示](https://pdben-auto.github.io/vehicle-sales-opportunity-skill/demo/dashboard.html) | 浏览器直接打开；同期分析、矩阵、分类、明细、月度下钻和 CSV |
| [Skill 入口与输入输出](skills/vehicle-sales-opportunity/SKILL.md) | 完整执行方法、依赖、错误处理和验收标准 |

原项目线上示例：[北美车型销量看板](https://north-america-vehicle-dashboard.pages.dev/)。这是原项目的在线版本，不是本仓库的合成演示；访问条件以实际页面为准，离线 Skill 不依赖它。

上方在线链接无需下载、安装或登录；由GitHub Pages展示实际HTML。也可下载对应目录离线打开 `.html`，无需 localhost、CDN 或远程字体。源码中的HTML文件页仅供查看代码，使用案例请点在线链接。

## 功能和流程

**业务问题 → 数量口径 → 数据校验 → 同窗口比较 → 交互页面 → 观察与假设 → 最小研究验证 → 交付验收。**

1. 定义国家、载具类型、型号边界、日历期间、指标与单位。汽车用车系/代际，摩托车用型号/排量/用途，UTV 用平台/座位/版本，ATV 独立，船舶用船体/型号/长度/动力。年款 MY 与统计年 CY 分开。
2. 整理已有数据，保留缺失、真实零值与合并组；按国家、类型、指标和稳定系列 ID 去重。不能把批发、零售、注册或不同类型混加。
3. 比较同一国家、类型、指标、系列和月份。两期都完整才进入配对汇总；零基期不算百分比；年度/季度不能平均拆月。
4. 设计从总览到矩阵、分类、明细、月度数据的阅读路径。所有卡片、图表和 CSV 随筛选联动，显示样本边界及未知项。
5. 从规模、绝对增减、变化率、生命周期和业务目标提出调研问题，再核对用户场景、适配、竞争、渠道与成本，写下一步、窗口和停止条件。
6. 检查输入指纹、关键算术、桌面/手机、筛选、详情、导出及文件搬迁后的完整性。

数量变化只提供研究入口，不能直接证明需求、适配、收入或利润。摩托车、ATV、船舶在通用工具中有合成运行示例，不代表已取得完整真实市场数据库。

## 前置条件

| 任务 | 必需条件 | 缺失时 |
|---|---|---|
| 通用月度看板 | 已有且获准处理的规范 JSON、Python 3.10+ 标准库、可写新目录 | 按[输入合同](skills/vehicle-sales-opportunity/references/data-contract.md)适配；不补造数据 |
| 原数据为 Excel/CSV | 宿主已有转换或表格工具 | 导出为约定 JSON；核心生成器不自动安装库 |
| 完整 Skill 流程 | Codex 或能读取 Agent Skills 的助手 | Python 仍能生成数字、页面和研究候选；候选不等于业务评审 |
| 页面验收 | 浏览器，可直接打开本地 HTML | 可先读 JSON/Markdown，视觉验收明确未完成 |
| 真实 UTV 案例复现 | Python 3.10+ 标准库、本仓库缓存、可写新目录 | 保留原快照，不联网、不覆盖 |
| 原案例完整扩展 QA / Excel 重建 | Pillow/openpyxl；Excel 构建另需 Node 与 `@oai/artifact-tool` | 标准库验证仍可运行；原 Excel 保留，不假称重建过 |
| 机会实证研究 | 获准使用的用户、产品、适配、竞争及经营材料 | 仅交付待验证假设和研究设计 |
| 商业数据或重新采集 | 合法账号/许可、网络、目标来源和相应授权 | 只读已包含快照；不购买、不登录受限系统 |

核心工具不需要 API、密钥、账号或付费 MCP。安装不自动发布网页，也不会启用定时任务。

## 安装与使用

将 **`skills/vehicle-sales-opportunity` 整个目录**复制到 `~/.codex/skills/vehicle-sales-opportunity`；Windows 通常为 `%USERPROFILE%\.codex\skills\vehicle-sales-opportunity`。已有安装用本目录更新。若当前会话尚未发现，重新打开会话加载。

```text
使用 $vehicle-sales-opportunity，把已有的汽车、摩托车、UTV、ATV和船舶月度表做成看板，
同比窗口一致，不混合零售、批发和新注册量，再列出可以验证的配件/服务研究问题。
```

仓库根目录运行通用演示，输出目录须不存在：

```sh
python skills/vehicle-sales-opportunity/scripts/build_dashboard.py --input skills/vehicle-sales-opportunity/assets/demo-multitype.json --output out/multitype
```

输出 `dashboard.html`、`analysis.json`、`opportunities.json`、`report.md`、`qa.json`。助手还应根据具体任务撰写 `research-review.md`，明确事实、假设、缺口和停止条件；[汽车合成评审示例](docs/demo/research-review.md)可参考。

## 完整真实案例：UTV / ATV

从仓库根目录执行：

```sh
python cases/utv-atv/reproduce.py --workdir out/utv-case
```

先核对原完成清单与 105 个来源快照 SHA-256，复算情景与关键去重，再复制到新目录离线重建数据和 HTML，要求数据语义与已完成快照一致。不会联网，不重建 Excel，不改原快照。

案例固定 2026-11-17 首个完成版本：124 个目录条目，US 63 / CA 15 / MX 1 个条目有可计算历史批次；所有完整车型保有量均为 `unknown`。页面展示的是**已知历史批次在假设下的情景**，不是完整 VIO、统计置信区间或严格上下界。召回数量不等于销量，不能喂入通用月度销量工具。

**ATV 完成的是渠道调查；实际数据页面研究 UTV，排除 ATV 和配件。** 原对话后续年款/版本细化、缺图修复与精度改进仍在进行，本包不冒称已完成。原 3053 项检查、37 项浏览器检查是历史证据；本次包装与复现的检查另行记录。

真实案例按用户授权保留原品牌、型号、数量和来源，不用合成数替换。没有包含凭证、登录态或原始聊天。第三方图片、商标和来源内容权利仍属于各自权利人；不因本仓库公开而授予额外商业再分发权，不更改原许可。

## 开发验证

```sh
python -B -m unittest discover -s tests -v
node tests/test_frontend.mjs
python -B cases/utv-atv/reproduce.py --verify-only
```

检查范围与未验证事项见[验证说明](docs/VALIDATION.md)。CI 还会实际离线重建案例。通过内部检查不证明完整覆盖、市场事实或商业机会成立。
