# 北美UTV/ATV数量数据渠道：原调查与核对方法

原调查日期2026-11-13；本包2026-11-17固定案例。公开产品说明不是已经获得数据，也不保证当前报价、账号权限、具体车型覆盖或历史长度。

包装时于2026-11-17重新打开PPM UTV/ATV产品页，仍可读到型号层零售统计、国家与频率说明；SSI本轮返回HTTP403，当前页面能力未重新确认。其他渠道沿用原调查日期，未冒称本轮全部刷新。

| 渠道 | 原调查确认的产品方向 | 粒度/口径与使用条件 |
|---|---|---|
| [PPM UTV](https://www.powerprods.com/?view=article&id=9:utility-vehicles-side-by-sides-and-low-speed-vehicles&catid=2) | 北美/加拿大UTV、美国分州、主要品牌月/季度跟踪 | 产品说明包含按型号零售销量及规格；商业服务。先拿样表核对国家、品牌、型号/版本、期间、台数、覆盖率与估算方法 |
| [PPM ATV](https://www.powerprods.com/?view=article&id=8:powersports-equipment&catid=2) | 美国成人/青少年、传统/非传统品牌、加拿大传统品牌ATV | 产品说明包含型号层零售销量和规格；加拿大非传统品牌和具体历史长度待询证 |
| [MIC](https://www.mic.org/#/statistics) Retail Sales Report | 参与厂商美国摩托车、ATV零售统计 | 品牌/车型类别不等于具体型号；不能据此推定UTV已覆盖。会员或购买条件以当期产品为准 |
| [MIC/S&P](https://www.mic.org/#/statistics) Powersports VIO | 摩托车、ATV、SxS品牌/型号/年款及注册/VIO方向 | 注册/在用量与零售销量分开；新旧车注册、地区和时点需核对产品定义 |
| [Statistical Surveys](https://www.statisticalsurveys.com/powersports/) | 美/加powersports新车注册和车型/地理维度 | 月度注册口径；目标ATV/UTV类别、州省、品牌与历史覆盖须核对样表 |
| [Lightspeed](https://www.lightspeeddms.com/resource-hub/data-services/) | 经销商成交、库存和相关交易样本 | 参与经销商样本不能直接外推全国；具体车型维度需供应商确认 |
| [Moto Canada](https://motocanada.com/reports-statistics/) | 加拿大公开行业报告和统计入口 | 行业总量与趋势补充；原调查未确认公开完整车型销量表 |
| [Polaris财报](https://ir.polaris.com/financial-information/quarterly-results/default.aspx)等厂商资料 | 自有品牌/部门财务与经营披露 | 收入、批发、终端零售、交付和增速须逐项区分；不是完整车型台数表 |

墨西哥完整车型级商业渠道在原调查中未确认，不能套用美加覆盖声明。没有购买、下载商业数据库，也没有联系卖家。

## 从渠道到可用表的验收

先定义问题：具体型号月销量、年度注册、还是某时点在用量。取得样表时确认以下字段；本包不自动购买或访问受限数据：

1. 国家/州省范围、品牌与型号版本、年款与统计期。
2. 零售、批发、交付、新注册、过户或VIO的精确定义。
3. 数值是观察、估算、校正还是不完整参与样本；覆盖率分母如何定义。
4. UTV/SxS/ROV/RUV和ATV分类是否分开，版本/座位是否可以拆量。
5. 历史长度、修订方式、缺失值、稳定主键与聚合边界。
6. 许可是否允许本地处理、公开汇总、展示原始数据或再分发。

## 本真实页面实际使用的公开证据

- [CPSC官方召回](https://www.cpsc.gov/Recalls)与公开API `https://www.saferproducts.gov/RestWebServices/Recall`：用RecallID去重，保存查询、原JSON、发布日期、检索日与SHA-256。
- 官方UTV目录：只确认型号身份和国家列示，不把目录存在当销量/保有量。详见[来源台账](输出/data/source_ledger.csv)及本地快照。
- 加拿大/墨西哥数量仅采用公告明确单列的台数。公告没有列出就unknown，不能按比例估计。

召回影响数量不是全年销量、完整在用量或全国车型样本。它只能支撑已选范围内的历史批次，以及标明假设的情景研究。
