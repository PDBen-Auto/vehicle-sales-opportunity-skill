# 车辆销量可视化与机会调研 Skill

**已有数据之后，怎样把销量表做成可读、可核对、能启动调研的可视化内容。**

适合北美车型月报、同级车比较、车型异动复盘，以及汽车配件/服务的机会研究。全流程是：

**已有数据 → 口径整理 → 同期比较 → 交互看板 → 异动识别 → 研究假设 → 最小验证。**

线上呈现示例：**[北美车型销量看板](https://north-america-vehicle-dashboard.pages.dev/)**。链接指向原项目，不是本仓库的合成数据页面；页面访问条件和可用性以实际状态为准。Skill 本身可以完全离线使用。

本仓库不包含车辆销量数据来源、来源清单、数据获取教程、采集脚本或原始销量库。没有账号、激活码、登录态、私有业务案例或真实用户记录。演示车型和数字全部为合成案例，不能用于市场判断。

## 能完成什么

| 模块 | 结果 |
|---|---|
| 数据整理 | 区分市场、日历期间、完整月、缺失、真实零值与聚合车系 |
| 同期比较 | 当前/基期销量、绝对增减、同比、配对样本分类汇总 |
| 可视化 | 自包含 HTML：市场/分类/搜索/排序、规模×增速矩阵、分类对比、月度下钻、筛选CSV |
| 机会识别 | 规模增长、小基数、下降、零基期、缺数和持续观察，全部保留 |
| 研究设计 | 将信号转为用户场景、代际适配、竞品、渠道与经济验证问题，并写停止条件 |

脚本产生数字、看板和**研究候选**；助手结合获准材料才可形成业务评审。销量增长不能直接证明配件需求、产品适配、竞争迁移、收入或利润。

## 前置条件

- 一份用户已经持有、允许处理的车辆销量表，以及统计单位、市场、车系和期间说明。
- 使用附带脚本：Python **3.10+**，仅标准库，无需 `pip install`、API、账号或密钥。
- 一个可写的本地新目录和可打开 HTML 的浏览器。
- 完整 Skill 流程需要 Codex 或能读取 `SKILL.md` 的助手。Excel 输入需要宿主已有表格工具转换；脚本直接接受规范 JSON。
- 真实机会验证还需要用户已持有或另外授权的用户反馈、产品/代际/适配、竞争、成本、渠道等材料。没有材料时保留待验证，不编造证据。

## 安装到 Codex

将仓库中的 **`skills/vehicle-sales-opportunity` 整个目录**复制到用户技能目录 `~/.codex/skills/vehicle-sales-opportunity`。Windows 通常是 `%USERPROFILE%\.codex\skills\vehicle-sales-opportunity`。不要把整个仓库当作单个 Skill 目录。

若当前会话未发现新技能，重新打开会话以重新加载。它不需要联网服务，也不依赖线上示例站的访问权限。

调用示例：

```text
使用 $vehicle-sales-opportunity，把我已有的美加墨车型月度销量做成可交互看板，
比较本年1–6月与上年同期，并围绕SUV储物配件设计可验证的机会清单。
只用已有数据，不涉及数据来源或采集。
```

## 三分钟运行合成案例

从仓库根目录执行（`out/demo` 必须尚不存在）：

```sh
python skills/vehicle-sales-opportunity/scripts/build_dashboard.py \
  --input skills/vehicle-sales-opportunity/assets/demo.json \
  --output out/demo
```

Windows PowerShell 可用单行：

```powershell
python skills/vehicle-sales-opportunity/scripts/build_dashboard.py --input skills/vehicle-sales-opportunity/assets/demo.json --output out/demo
```

直接打开 `out/demo/dashboard.html`，无需服务器、CDN或远程字体。也可下载仓库中的 [完整合成演示 HTML](docs/demo/dashboard.html) 后直接打开。

输出：`dashboard.html`、`analysis.json`、`opportunities.json`、`report.md`、`qa.json`。助手还应根据研究任务撰写 `research-review.md`，示例见 [合成研究评审](docs/demo/research-review.md)。

## 使用自己的数据：完整流程

### 1. 整理而不改造事实

按照 [输入合同](skills/vehicle-sales-opportunity/references/data-contract.md) 将已有表规范化。保持日历年 CY 与车型年 MY 分开；稳定车系 ID 不随显示名变化；聚合车系不可拆成子车型。销量、登记量与保有量分开。

附带脚本处理**月度**数据。只有季度或年度数据时，可以让助手按原粒度作图，不能平均拆成月度数据以适配脚本。缺失用 null，不用0。

### 2. 定义比较窗与样本

比较相同国家、相同车系边界、相同月份，例如2025年1–6月对2024年1–6月。部分年度不能直接与完整年度比。两期都完整才进入同比和分类配对汇总；基期为0不计算百分比。

### 3. 构建与核对

替换命令的 `--input` 和 `--output` 为自己的路径。运行只读输入、写入新目录，不覆盖旧交付。核对输入指纹、不可比清单及关键车系数字；QA通过仅证明内部检查通过。

### 4. 设计阅读路径

先看市场与窗口，再看总量、规模×增速、分类、车系明细和月度数据。页面所有卡片和图表随筛选联动。显示样本边界与不可比项，提供数字表和导出。详见 [可视化方法](skills/vehicle-sales-opportunity/references/visualization.md)。

### 5. 把异动转成研究问题

以绝对量、变化率、基数、生命周期及业务目标筛选入口；再确认“谁在什么场景遇到什么问题”。不要把高增长车系自动认定为高利润机会。详见 [机会调研方法](skills/vehicle-sales-opportunity/references/opportunity-research.md)。

### 6. 验证与交付

用获准材料核对需求、代际适配、替代方案、渠道与成本，保留反证、下一步、窗口和停止条件。检查桌面/手机、筛选、详情和导出。共享前审阅内容，脚本不会替你脱敏真实输入，也不会自动发布网页。

## 合成案例说明

虚构 Aster Canyon 美国SUV：2024年1–6月12000辆，2025同期15600辆，增3600辆、30%。这足以进入“研究一个使用场景”的候选队列，仍不能证明某种配件需求增长30%。

包内同时演示下降、微小基数高增、零基期、缺失和跨国分开统计。没有借用真实车型销量或私有案例数值。

## 验证与边界

```sh
python -B -m unittest discover -s tests -v
```

测试覆盖真实数学结果、缺失/零值、窗口一致性、重复键、未来月份、元数据冲突、字段白名单、HTML安全嵌入、输出文件和覆盖拒绝。CI仅执行标准库测试，不需要秘密。

发布前的结构、隐私、触发和浏览器检查记录在 [验证说明](docs/VALIDATION.md)。基础生成器没有自动代际推断、完整年度趋势图、图片或真实商业验证；需要时按Skill方法在相应材料与权限具备后扩展。

公开可见不意味着本包提供了原项目的数据、平台账号、访问权限或市场完整性保证。
