"""Build an explicitly partial UTV recall-cohort scenario dataset.
No recall quantity is written to observed VIO or annual sales tables.
"""
import json,csv,re,math,hashlib,shutil,base64
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parent; OUT=ROOT.parent/'输出'; DATA=OUT/'data'; SNAP=DATA/'snapshots'
SNAP.mkdir(parents=True,exist_ok=True)
ASOF='2026-11-17'; YEAR=2026
recalls={r['RecallID']:r for r in json.loads((ROOT/'sources/cpsc-merged.json').read_bytes())}
models=[]; cohorts=[]
def model(mid,brand,name,category,parts,notes='',group=False,aliases='',sources=None):
    # parts: recall ID, oldest model year, newest model year, oldest sale year, optional unit override
    obj=dict(id=mid,brand=brand,name=name,category=category,group=group,aliases=aliases,notes=notes,
             source_ids=['cpsc-'+str(p[0]) for p in parts] if parts else (sources or []),parts=[])
    models.append(obj)
    for p in parts:
        rid,start,end,sale,*override=p; r=recalls[rid]; text=' / '.join(x['NumberOfUnits'] for x in r['Products'])
        us=override[0] if override else int(re.search(r'[\d,]+',text)[0].replace(',',''))
        def other(country):
            hit=re.search(r'(\d[\d,]*)\s+(?:(?:ROVs?|units?|vehicles?|were|was|sold|also)\s+){0,5}in\s+'+country,text,re.I)
            return int(hit[1].replace(',','')) if hit else None
        nums={'US':us,'CA':other('Canada'),'MX':other('Mexico')}
        for country,n in nums.items():
            if n is None:continue
            cid=f'{mid}.{country}.{rid}'; age=max(0,YEAR-min(start,sale))
            c=dict(component_id=cid,model_id=mid,country=country,recall_id=rid,source_id='cpsc-'+str(rid),source_url=r['URL'],
                   recall_number=r['RecallNumber'],recall_date=r['RecallDate'][:10],units_text=text,historical_units=n,
                   model_year_start=start,model_year_end=end,oldest_sale_year=sale,age_basis_year=min(start,sale),age=age,
                   selection_reason='同一车型重叠批次只保留已选代表批次；多个已选批次按不重叠年款相加',
                   window_basis='sales_or_manufacture_window' if rid in [5177,8215,8658,8025,9648,1497,7818,3039,3035,6477,9893,9187] else 'explicit_model_year',
                   source_scope='某些VIN/配置；并非全车型累计销量或当前登记量',confidence='low',methodology_id='recall-cohort-scenario-v1')
            cohorts.append(c);obj['parts'].append(cid)
    return obj

# Individually attributable series and explicitly named source aggregates.
model('polaris.rzr-xp1000','Polaris','RZR XP 1000 / XP 4 1000','运动',[(8296,2014,2018,2013),(10106,2024,2025,2023)],'两个年款批次互不重叠；MY2019–2023及其余未入召回VIN均未补量。')
model('polaris.rzr-turbo-group','Polaris','RZR XP Turbo / Turbo S 合并组','运动',[(7847,2016,2016,2015),(9687,2021,2021,2021)],'MY2016的13,000已含先前2,230；MY2021的27,300已含部分旧召回。两年款互不重叠；XP Turbo与Turbo S不分摊。',True)
model('polaris.rzr-proxp-turbor-group','Polaris','RZR Pro XP 4 / Turbo R 4 合并组','运动',[(9632,2021,2023,2021)],'只覆盖4座指定VIN；无法拆分Pro XP与Turbo R。',True)
model('polaris.rzr-pro-r','Polaris','RZR Pro R / Pro R 4','运动',[(9296,2022,2022,2021)],'仅MY2022 Pro R 4 Premium/Ultimate批次；2025另一次910台可能重叠，未相加。')
model('polaris.rzr-570','Polaris','RZR 570 / S 570','运动',[(8096,2017,2017,2016)])
model('polaris.rzr-170','Polaris','RZR 170','青少年',[(8104,2015,2017,2015)])
model('polaris.rzr-200','Polaris','RZR 200','青少年',[(9798,2021,2024,2021)])
model('polaris.ranger-500','Polaris','RANGER 500 / CREW 500','工具',[(1795,2013,2013,2012)])
model('polaris.ranger-570','Polaris','RANGER 570 / CREW 570','工具',[(7780,2015,2016,2014)])
model('polaris.ranger-900','Polaris','RANGER XP 900 / CREW 900','工具',[(7853,2014,2014,2013),(8028,2015,2015,2014)],'MY2014与MY2015互不重叠；未推算其他年款。')
model('polaris.ranger-xp1000','Polaris','RANGER XP 1000 / CREW','工具',[(8797,2018,2020,2016),(10455,2025,2026,2025)],'旧批次与2025–2026 NorthStar批次年款互不重叠；NorthStar不能单独视为全系。')
model('polaris.ranger-xd1500','Polaris','RANGER XD 1500 / CREW','工具',[(10058,2024,2024,2023)],'原文另有1,336套绞盘，未计作车辆；2025另一次4,200台可能重叠，未相加。')
model('polaris.ranger-ev','Polaris','RANGER EV','工具',[(8572,2015,2019,2014)],'BEV；未与XP Kinetic合并。')
model('polaris.ranger-xp-kinetic','Polaris','RANGER XP Kinetic','工具',[(9797,2023,2024,2023)],'2025的4,900台混合RANGER与PRO XD Kinetic，不能全归RANGER。')
model('polaris.general','Polaris','GENERAL 1000 / XP 1000','多用途',[(8166,2016,2017,2015),(9106,2021,2021,2020)],'两组年款互不重叠；早期原文销售结束时间早于开始时间，保留原文并仅使用最早起售年。')
model('polaris.pro-xd','Polaris','PRO XD（柴油代表批次）','商用',[(8737,2019,2019,2017)],'跨品牌召回的RANGER、PRO XD、Bobcat不能整体计入本车型。')
model('polaris.brutus','Polaris','BRUTUS','商用',[(8736,2017,2018,2016)])
model('canam.commander','Can-Am','Commander','多用途',[(1301,2011,2013,2010)],'仅旧款2011–早期2013；不代表2021后车型及当前全系。')
model('canam.defender','Can-Am','Defender HD10（代表批次）','工具',[(9108,2020,2021,2019)],'召回涉及搭配Apache履带套件的风险；34,400为公告车辆数量，未推定HD5/HD7/HD8/HD9/HD11全系规模。')
model('canam.maverick-x3','Can-Am','Maverick X3','运动',[(7909,2017,2017,2016)],'仅首发早期批次；样本很小，禁止据此与Defender比较市场份额。')
model('honda.pioneer-700','Honda','Pioneer 700 / 700-4','工具',[(1967,2014,2014,2013),(8045,2017,2017,2016)],'MY2014与MY2017不重叠；未将700和1000混合召回118,600台分摊。')
model('honda.pioneer-1000','Honda','Pioneer 1000 / 1000-5','工具',[(8580,2016,2019,2015)],'82,000覆盖MY2016–2019；65,000及56,000等早期召回可能重复，未相加。')
model('honda.talon-1000','Honda','Talon 1000（2座 / 4座）','运动',[(9496,2019,2021,2019)],'34,000已含此前32,000；不能加成66,000。')
model('yamaha.rhino-group','Yamaha','Rhino 450 / 660 / 700 合并组','多用途',[(5177,2004,2009,2003,145000)],'120,000为450/660合计，另25,000为700，合计145,000；两部分不重叠。修复项目并非当前在用调查。',True)
model('yamaha.viking-group','Yamaha','Viking / Viking VI 合并组','工具',[(6360,2015,2015,2014),(9490,2022,2022,2022)],'早期3,500仅Viking VI；2022的500台混合3座与6座，不拆车型。',True)
model('yamaha.yxz1000r','Yamaha','YXZ1000R / SS','运动',[(6704,2016,2016,2015)])
model('yamaha.wolverine-rmax-group','Yamaha','Wolverine RMAX2 / RMAX4 合并组','多用途',[(9305,2021,2021,2021)],'4,130混合2座与4座，未拆分；820台RMAX4旧召回可能重叠。',True)
model('kawasaki.mule-pro-legacy-group','Kawasaki','MULE PRO 820汽油 / 柴油旧批次','工具',[(8780,2015,2020,2014)],'80,000含FX/FXR/FXT及DX/DXT；72,000汽油召回与之重叠，未相加。',True)
model('kawasaki.mule-pro1000-group','Kawasaki','MULE PRO-FX / FXR / FXT 1000','工具',[(10010,2024,2024,2023)],'2024年款汽油1000批次，与旧820/柴油组年款、动力范围分开。',True)
model('kawasaki.mule600-610-group','Kawasaki','MULE 600 / 610 旧批次','工具',[(3394,2005,2006,2004),(1185,2012,2012,2011)],'MY2005–2006与MY2012不重叠；未与MULE SX互相替代。',True)
model('kawasaki.mule-pro-mx','Kawasaki','MULE PRO-MX 700','工具',[(8509,2019,2019,2018)])
model('kawasaki.teryx-legacy-group','Kawasaki','Teryx / Teryx4 750–800 合并组','多用途',[(6600,2012,2016,2011)],'只采用公告首列19,500台；另提11,000和7,000可能重叠，保守不加。',True)
model('kawasaki.teryx-h2-group','Kawasaki','Teryx4 H2 / Teryx5 H2 合并组','运动',[(10814,2026,2026,2025)],'仅初期MY2026批次，不能拆4座与5座。',True)
model('kubota.rtv-x1100c','Kubota','RTV-X1100C','工具',[(9168,2013,2021,2013)],'48,875含早期11,500的重叠风险，未叠加；2025 RTV混合49,640也未分摊。')
model('kubota.sidekick','Kubota','Sidekick RTV-XG850','工具',[(9465,2018,2022,2018)],'2023另3,170台的Y序列与早期公告范围存在交叉，未相加。')
model('kubota.rtv400-500-group','Kubota','RTV400 / RTV500 合并组','工具',[(6729,2013,2015,2010)],'公告MY2013–2015却显示2010起售；采用更早的2010作为车龄压力基准，不修造日期。',True)
model('kubota.rtv900','Kubota','RTV900（早期）','工具',[(3039,2004,2004,2004)],'不等同于后续RTV-X900。')
model('deere.gator-xuv835','John Deere','Gator XUV835','工具',[(8658,2018,2019,2017)],'原文序列中含看似较新VIN，未从VIN区间反推销量。')
model('deere.gator-xuv590','John Deere','Gator XUV590i / E / M','工具',[(8025,2016,2017,2016),(9648,2023,2023,2022)],'2016–2017旧590i与MY2023 590E/M批次分开；年款由原文/销售期与2023VIN表对应。')
model('deere.gator-xuv825-855-group','John Deere','Gator XUV825 / XUV855 合并组','工具',[(8215,2012,2017,2012)],'跨汽油/柴油混合，来源没有可用拆分；年款范围为来源销售批次窗口，非车型完整生命周期。',True)
model('deere.gator-hpx','John Deere','Gator HPX','工具',[(3035,2004,2004,2003)])
model('deere.gator-rsx850i','John Deere','Gator RSX850i','运动',[(1497,2012,2012,2012)],'4,650与4,700所述生产区间重叠，仅保留4,700。')
model('deere.gator-rsx860i','John Deere','Gator RSX860i','运动',[(7818,2016,2016,2016)])
model('cfmoto.zforce950','CFMOTO','ZFORCE 950 Sport / HO Sport','运动',[(8910,2020,2021,2020),(10005,2022,2023,2022)],'两个批次年款不重叠；2020旧500台已经被627批次覆盖，未相加。')
model('cfmoto.zforce-legacy-group','CFMOTO','ZFORCE 500 / 800 / 1000 合并组','运动',[(8444,2018,2018,2018)],'只覆盖2018混合批次，不能按排量分摊。',True)
model('segway.fugleman','Segway','Fugleman UT10E / UT10X','工具',[(9350,2022,2022,2021)])
model('arcticcat.wildcat-trail-sport-group','Arctic Cat','Wildcat Trail / Sport 合并组','运动',[(8165,2014,2017,2013)],'14,100美国、5,300加拿大、100墨西哥分别建行；2014 Trail旧5,600可能重叠。',True)
model('arcticcat.hdx700','Arctic Cat','HDX 700 / Crew','工具',[(7835,2016,2017,2015)])
model('textron.havoc','Textron','Havoc','多用途',[(8562,2018,2019,2018)],'后续200台MY2019召回可能重叠。')
model('arcticcat-tracker.pro800sx-group','Arctic Cat / Tracker','Prowler Pro / Tracker 800SX 合并组','工具',[(9949,2022,2023,2021)],'10,300与7,000/6,800系列召回可能重叠；不加总、不拆品牌。',True)
model('tracker.ox-ev','Tracker','OX EV','工具',[(9893,2023,2023,2023)])
model('kymco.uxv450i','KYMCO','UXV 450i','工具',[(6672,2015,2016,2014)])
model('kymco.uxv500','KYMCO','UXV 500 / 500i','工具',[(1171,2009,2012,2008)])
model('bobcat.3400','Bobcat','3400 / 3400XL','商用',[(8372,2015,2018,2014)],'作为独立品牌车辆保留，未并入Polaris。')
model('bobcat.3650','Bobcat','3650','商用',[(8738,2017,2018,2016)])
model('gravely.atlas','Gravely','Atlas JSV 3000 / 6000','商用',[(8373,2015,2018,2014)])
model('cubcadet.challenger400','Cub Cadet','Challenger 400','工具',[(8434,2018,2018,2018)])
model('cubcadet.challenger-legacy-group','Cub Cadet','Challenger CX500 / 700 / 750 Crew 合并组','工具',[(6717,2015,2015,2015),(8089,2016,2016,2016)],'2015的1,300与2016的4,000按不重叠年款相加；不能拆排量。',True)
model('landmaster.l-series-group','Landmaster','L3 / L4 / L5 / L7 / EV 合并组','工具',[(9236,2021,2021,2021)],'仅非电助力转向批次；EV与燃油车型无法拆分。',True)
model('intimidator-mahindra.group','Intimidator / Mahindra','Intimidator / Retriever 多型号合并组','工具',[(9922,2013,2023,2013)],'750/800/1000柴油/GC1K/电动混合，无法拆型号或品牌；16,000旧批次可能重叠。',True)
model('hisun-rk.sector250-group','Hisun / RK','Sector 250 / RK Performance 250 合并组','青少年',[(9187,2015,2021,2014)],'品牌不可拆分；250cc UTV并非同品牌ATV。',True)
model('vanderhall.brawley','Vanderhall','Brawley GTS','运动',[(11050,2024,2026,2024)],'2026年8月公告约210，11月公告约190，范围均称全MY2024–2026；未解释差异，取较新较小190并保留冲突。')
model('asw.utility-group','American SportWorks','LandMaster / BullDog / ChuckWagon / TrailWagon 合并组','工具',[(6477,2014,2015,2014)],'6种型号混合；没有分车型数量。',True)

# Named children retained as unavailable, never assigned arbitrary shares of a source group.
children=[
('polaris.rzr-xp-turbo','Polaris','RZR XP Turbo','运动','polaris.rzr-turbo-group'),('polaris.rzr-turbo-s','Polaris','RZR Turbo S','运动','polaris.rzr-turbo-group'),
('polaris.rzr-pro-xp','Polaris','RZR Pro XP','运动','polaris.rzr-proxp-turbor-group'),('polaris.rzr-turbo-r','Polaris','RZR Turbo R','运动','polaris.rzr-proxp-turbor-group'),
('yamaha.rhino450','Yamaha','Rhino 450','多用途','yamaha.rhino-group'),('yamaha.rhino660','Yamaha','Rhino 660','多用途','yamaha.rhino-group'),('yamaha.rhino700','Yamaha','Rhino 700','多用途','yamaha.rhino-group'),
('yamaha.viking','Yamaha','Viking（3座）','工具','yamaha.viking-group'),('yamaha.viking-vi','Yamaha','Viking VI（6座）','工具','yamaha.viking-group'),
('yamaha.rmax2','Yamaha','Wolverine RMAX2 1000','多用途','yamaha.wolverine-rmax-group'),('yamaha.rmax4','Yamaha','Wolverine RMAX4 1000','多用途','yamaha.wolverine-rmax-group'),
('kawasaki.mule-pro-fx','Kawasaki','MULE PRO-FX','工具','kawasaki.mule-pro-legacy-group'),('kawasaki.mule-pro-fxr','Kawasaki','MULE PRO-FXR','工具','kawasaki.mule-pro-legacy-group'),('kawasaki.mule-pro-fxt','Kawasaki','MULE PRO-FXT','工具','kawasaki.mule-pro-legacy-group'),('kawasaki.mule-pro-dx','Kawasaki','MULE PRO-DX','工具','kawasaki.mule-pro-legacy-group'),('kawasaki.mule-pro-dxt','Kawasaki','MULE PRO-DXT','工具','kawasaki.mule-pro-legacy-group'),
('kawasaki.teryx','Kawasaki','Teryx 750 / 800','多用途','kawasaki.teryx-legacy-group'),('kawasaki.teryx4','Kawasaki','Teryx4 750 / 800','多用途','kawasaki.teryx-legacy-group'),('kawasaki.teryx4-h2','Kawasaki','Teryx4 H2','运动','kawasaki.teryx-h2-group'),('kawasaki.teryx5-h2','Kawasaki','Teryx5 H2','运动','kawasaki.teryx-h2-group'),
('kubota.rtv400','Kubota','RTV400','工具','kubota.rtv400-500-group'),('kubota.rtv500','Kubota','RTV500','工具','kubota.rtv400-500-group'),
('deere.xuv825','John Deere','Gator XUV825','工具','deere.gator-xuv825-855-group'),('deere.xuv855','John Deere','Gator XUV855','工具','deere.gator-xuv825-855-group'),
('cfmoto.zforce500','CFMOTO','ZFORCE 500 Trail','运动','cfmoto.zforce-legacy-group'),('cfmoto.zforce800','CFMOTO','ZFORCE 800 Trail','运动','cfmoto.zforce-legacy-group'),('cfmoto.zforce1000','CFMOTO','ZFORCE 1000','运动','cfmoto.zforce-legacy-group'),
('arcticcat.wildcat-trail','Arctic Cat','Wildcat Trail','运动','arcticcat.wildcat-trail-sport-group'),('arcticcat.wildcat-sport','Arctic Cat','Wildcat Sport','运动','arcticcat.wildcat-trail-sport-group'),
('arcticcat.prowler-pro','Arctic Cat','Prowler Pro / Pro Crew','工具','arcticcat-tracker.pro800sx-group'),('tracker.800sx','Tracker','800SX / Crew','工具','arcticcat-tracker.pro800sx-group'),
('landmaster.l3','Landmaster','L3','工具','landmaster.l-series-group'),('landmaster.l4','Landmaster','L4','工具','landmaster.l-series-group'),('landmaster.l5','Landmaster','L5 / L5W','工具','landmaster.l-series-group'),('landmaster.l7','Landmaster','L7','工具','landmaster.l-series-group'),('landmaster.ev','Landmaster','EV','工具','landmaster.l-series-group'),
('intimidator.gc1k','Intimidator','GC1K','工具','intimidator-mahindra.group'),('intimidator.750','Intimidator','750','工具','intimidator-mahindra.group'),('intimidator.800','Intimidator','800','工具','intimidator-mahindra.group'),('intimidator.diesel1000','Intimidator','1000 Diesel','工具','intimidator-mahindra.group'),('mahindra.retriever','Mahindra','Retriever 750 / 1000 Diesel / TGB','工具','intimidator-mahindra.group'),
('hisun.sector250','Hisun','Sector 250','青少年','hisun-rk.sector250-group'),('rk.performance250','RK','Performance 250','青少年','hisun-rk.sector250-group')]
byid={m['id']:m for m in models}
for mid,brand,name,cat,parent in children:
    p=byid[parent];obj=model(mid,brand,name,cat,[],f'数量只存在于“{p["name"]}”；单车型数量未知，不按份额拆分。',sources=p['source_ids']);obj['parent_id']=parent

# Additional OEM-current candidates; model availability does not establish installed population.
catalog_candidates=[
('yamaha.wolverine-x2','Yamaha','Wolverine X2 850 / 1000','多用途','catalog-yamaha'),('yamaha.wolverine-x4','Yamaha','Wolverine X4 850','多用途','catalog-yamaha'),
('canam.maverick-r','Can-Am','Maverick R','运动','catalog-canam-ca'),('canam.maverick-sport','Can-Am','Maverick Sport','运动','catalog-canam-ca'),('canam.maverick-trail','Can-Am','Maverick Trail','运动','catalog-canam-ca'),('canam.defender-hd11','Can-Am','Defender HD11 / XU','工具','catalog-canam-ca'),
('landmaster.n7','Landmaster','N7','工具','catalog-landmaster'),('landmaster.amp','Landmaster','AMP','工具','catalog-landmaster'),
('hisun.sector400','Hisun','Sector 400','工具','catalog-hisun'),('hisun.strike250r','Hisun','Strike 250R','青少年','catalog-hisun'),('hisun.strike550r','Hisun','Strike 550R','运动','catalog-hisun'),
('massimo.tboss560','Massimo','T-BOSS 560 / 560L / 560X','工具','catalog-massimo'),('massimo.tboss760','Massimo','T-BOSS 760 / 760L','工具','catalog-massimo'),('massimo.tboss900l','Massimo','T-BOSS 900L','工具','catalog-massimo'),('massimo.tboss1000','Massimo','T-BOSS 1000','工具','catalog-massimo'),('massimo.warrior1500xd','Massimo','Warrior 1500 XD','工具','catalog-massimo'),
('polaris.xpedition','Polaris','XPEDITION XP / ADV','多用途','catalog-polaris-dom'),('polaris.rzr-pro-r-boost','Polaris','RZR Pro R Boost','运动','catalog-polaris-dom')]
for mid,brand,name,cat,sid in catalog_candidates:
    o=model(mid,brand,name,cat,[],'官方目录已发现车型；没有公开、可单独归属的数量输入。',sources=[sid]);o['catalog_only']=True

for m in models:
    if m['id'] in ['canam.commander','canam.defender','canam.maverick-x3']:m['source_ids'].append('catalog-canam-ca')
    if m['id'] in ['canam.defender','canam.defender-hd11','canam.maverick-x3','canam.maverick-r']:m['source_ids'].append('catalog-canam-mx')

polaris_extract={'url':'https://www.polaris.com/en-us/off-road/','retrieved_at':ASOF,'capture_type':'visible_dom_excerpt','title':'Off-Road Vehicles (ORV): Polaris SxS, UTVs, ATVs & Four Wheelers','excerpts':['The 2027 Polaris Off Road lineup is here','OUR OFF-ROAD BRANDS','RANGER','RZR','POLARIS XPEDITION','GENERAL','2027 RZR PRO R BOOST'],'note':'In-app browser visible DOM verified; full lineup navigation timed out. Excerpt supports series identity only.'}
(SNAP/'catalog-polaris-dom.json').write_text(json.dumps(polaris_extract,ensure_ascii=False,indent=2),encoding='utf8')

def writecsv(name,rows,fields=None):
    if fields is None:fields=list(rows[0]) if rows else []
    with (DATA/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def hashfile(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ledger=[]
used={int(s.split('-')[-1]) for m in models for s in m['source_ids'] if s.startswith('cpsc-')}
# Include alternative evidence in the audit pool, separate from quantitative selected components.
pool_ids=[6709,6537,9258,8954,8839,9176,9803,9524,10259,9949,10070,9755,10315,10127,8798,8781,6594,8327,8454,10909,9804,8889,10175,10224,8407]
used.update(pool_ids)
for rid in sorted(used):
    r=recalls[rid];p=SNAP/f'cpsc-{rid}.json';p.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf8')
    ledger.append(dict(source_id=f'cpsc-{rid}',title=r['Title'],publisher='U.S. CPSC',url=r['URL'],source_tier=1,source_family='government_catalog',geography='US',metric='recall affected units; model identity',published_at=r['RecallDate'][:10],retrieved_at=ASOF,license_or_access='Public',notes='API原文快照；召回数量并非登记、销量或在用量。加拿大/墨西哥仅使用原文明确另列数量。',snapshot_status='captured',checksum_sha256=hashfile(p),local_snapshot='snapshots/'+p.name,source_period_start='',source_period_end=''))
for r in json.loads((ROOT/'sources/catalog-manifest.json').read_bytes()):
    if r.get('error') or r['source_id']=='catalog-deere':continue
    src=ROOT/r['local_snapshot'];p=SNAP/src.name;shutil.copyfile(src,p)
    ledger.append(dict(source_id=r['source_id'],title=r['title'],publisher=r['source_id'][8:],url=r['resolved_url'],source_tier=1,source_family='oem_official',geography='CA' if r['source_id'].endswith('-ca') else 'MX' if r['source_id'].endswith('-mx') else 'US',metric='model identity',published_at='',retrieved_at=ASOF,license_or_access='Public',notes='目录仅证明车型身份/页面列示，不证明销量、在用量或全部国家在售。',snapshot_status='captured',checksum_sha256=hashfile(p),local_snapshot='snapshots/'+p.name,source_period_start='',source_period_end=''))
p=SNAP/'catalog-polaris-dom.json';ledger.append(dict(source_id='catalog-polaris-dom',title=polaris_extract['title'],publisher='Polaris',url=polaris_extract['url'],source_tier=1,source_family='oem_official',geography='US',metric='model identity',published_at='',retrieved_at=ASOF,license_or_access='Public',notes='浏览器可见DOM摘录；仅证明系列身份，未完成全品牌审计。',snapshot_status='captured',checksum_sha256=hashfile(p),local_snapshot='snapshots/'+p.name,source_period_start='',source_period_end=''))
writecsv('source_ledger.csv',ledger); sl={s['source_id']:s for s in ledger}

PARAMS={'severe':{'label':'更严压力','active':0.80,'retention':0.88},'conservative':{'label':'保守基准','active':0.90,'retention':0.93},'less_severe':{'label':'较缓压力','active':0.95,'retention':0.97}}
def rnd(n,direction='down'):
    unit=100 if n>=1000 else 10 if n>=100 else 1
    return int((math.ceil(n/unit) if direction=='up' else math.floor(n/unit))*unit)
for c in cohorts:
    for k,p in PARAMS.items():c[k+'_unrounded']=c['historical_units']*p['active']*(p['retention']**c['age'])

scenarios=[]
for m in models:
    for country in ['US','CA','MX']:
        cc=[c for c in cohorts if c['model_id']==m['id'] and c['country']==country]
        row=dict(as_of_date=ASOF,country=country,canonical_model_id=m['id'],make=m['brand'],model=m['name'],aggregation_level='source_group' if m['group'] else 'series',
                 category=m['category'],full_model_population=None,full_model_population_status='not available at model level',
                 historical_affected_units=sum(c['historical_units'] for c in cc) if cc else None,
                 conservative_batch_scenario=rnd(sum(c['conservative_unrounded'] for c in cc)) if cc else None,
                 severe_batch_scenario=rnd(sum(c['severe_unrounded'] for c in cc)) if cc else None,
                 less_severe_batch_scenario=rnd(sum(c['less_severe_unrounded'] for c in cc),'up') if cc else None,
                 scenario_status='modeled_partial_cohort_scenario' if cc else 'not_quantified',confidence='low' if cc else 'unknown',
                 cohort_window='; '.join(str(c['model_year_start'])+'–'+str(c['model_year_end']) for c in cc),
                 component_ids=';'.join(c['component_id'] for c in cc),source_ids=';'.join(m['source_ids']),
                 source_urls=';'.join(sl[s]['url'] for s in m['source_ids']),parent_id=m.get('parent_id',''),notes=m['notes'],
                 methodology_id='recall-cohort-scenario-v1' if cc else '',unit='vehicles')
        row['market_presence']='historical_quantity_verified' if cc else 'catalog_identity_verified' if any(sl[s]['geography']==country for s in m['source_ids'] if s.startswith('catalog-')) else 'not_verified_for_country'
        scenarios.append(row)
writecsv('cohort_scenarios.csv',scenarios);writecsv('cohort_components.csv',cohorts)
writecsv('model_catalog.csv',[{**{k:v for k,v in m.items() if k not in ['parts','source_ids']},'source_ids':';'.join(m['source_ids']),'full_fleet_count_status':'unknown','scope_status':'partial'} for m in models],['id','brand','name','category','group','parent_id','catalog_only','aliases','notes','source_ids','full_fleet_count_status','scope_status'])

# Skill schema keeps official VIO and observed registrations empty. The requested exploratory
# scenarios have their own tables because assumed attrition is not a sourced survival curve.
schemas={
'vehicle_population.csv':'record_id,as_of_date,country,canonical_model_id,aggregation_level,model_year,powertrain,count,count_type,lower_bound,upper_bound,methodology_id,input_source_ids,input_source_urls,coverage_scope,unit,is_primary,retrieved_at',
'vehicle_population_rollup.csv':'record_id,as_of_date,country,canonical_model_id,make,model,total_count,count_type,powertrains,component_records,component_record_ids,source_ids,source_urls,coverage_scope,unit,is_primary,retrieved_at',
'annual_sales.csv':'country,canonical_model_id,make,model,calendar_year,units,metric,period_start,period_end,is_partial_year,months_reported,source_model_aliases,source_id,source_url,retrieved_at,notes',
'country_controls.csv':'country,as_of_date,metric_label,count,scope,source_id,source_url,comparability,notes',
'news_events.csv':'event_id,canonical_model_id,country,event_type,headline,summary,announced_at,effective_date_start,effective_date_end,effective_date_precision,model_year,status,confidence,importance_score,source_1_id,source_1_url,source_2_id,source_2_url,retrieved_at,change_class,change_label_cn,change_magnitude,iteration_relation,change_rationale,key_changes,model_context',
'news_coverage.csv':'country,brand,window_start,window_end,coverage_status,official_source_ids,event_count,known_gap,checked_at'}
for name,header in schemas.items():writecsv(name,[],header.split(','))
master=[];universe=[]
for c in cohorts:
    if c['window_basis']!='explicit_model_year':continue
    m=next(m for m in models if m['id']==c['model_id']);s=sl[c['source_id']]
    master.append(dict(country=c['country'],canonical_model_id=m['id'],make=m['brand'],model=m['name'],nameplate=m['name'],model_year=c['model_year_start'],generation='unknown',body_style='UTV_source_group' if m['group'] else 'UTV',powertrain='other',status='on_sale',on_sale_start='',on_sale_end='',source_id=c['source_id'],source_url=s['url'],retrieved_at=ASOF,notes='历史来源批次中的在售身份；并不代表当前仍在售。混合动力信息未拆分。'))
    universe.append(dict(country=c['country'],model_year=c['model_year_start'],source_name='CPSC historical cohort candidates',source_id=c['source_id'],source_url=s['url'],source_make=m['brand'],source_model_name=m['name'],candidate_id=c['component_id'],canonical_model_id=m['id'],resolution_status='included',exclusion_reason='',retrieved_at=ASOF))
dedup={tuple(r[k] for k in ['country','canonical_model_id','model_year','powertrain']):r for r in master}
writecsv('model_master.csv',list(dedup.values()));writecsv('market_universe.csv',universe)
coverage=[]
for country,my in sorted({(u['country'],u['model_year']) for u in universe}):
    uu=[u for u in universe if u['country']==country and u['model_year']==my]
    sids=sorted({u['source_id'] for u in uu})
    coverage.append(dict(country=country,model_year=my,scope_status='partial',source_families='government_catalog',source_ids=';'.join(sids),candidate_count=len(uu),included_count=len(uu),excluded_count=0,pending_count=0,resolution_rate=1,included_mapping_rate=1,brands_checked=len({u['source_make'] for u in uu}),oem_reconciliation_status='partial',known_gaps='仅已选召回批次；该行100%仅是已收录来源行的映射率，不是市场车型或保有量覆盖率。未完成品牌/年款审计。',checked_at=ASOF))
writecsv('market_coverage.csv',coverage)

pool=[]
for rid in pool_ids:
    r=recalls[rid];note='重叠/混合车型的补充证据，不进入情景计算'
    if rid in [8889,10175,10224]:note='排除：数量是配件（安全带/轴承/加热器），不是车辆'
    if rid==8407:note='排除：CFORCE为ATV，超出本版UTV范围'
    if rid==10909:note='数量冲突：约210与后续190均称全MY2024–2026；取较新较小190，不相加'
    pool.append(dict(recall_id=rid,source_id='cpsc-'+str(rid),date=r['RecallDate'][:10],title=r['Title'],units_text=' / '.join(p['NumberOfUnits'] for p in r['Products']),decision=note,source_url=r['URL']))
writecsv('evidence_pool.csv',pool)
gaps=[
 {'area':'全车型当前在用量','status':'unknown','gap':'本版所有条目的全量VIO均未知；没有可公开复核的分车型在用调查。','next_input':'取得MIC/S&P或同等口径车型VIO；核对UTV覆盖和许可'},
 {'area':'美国','status':'partial','gap':'召回只覆盖部分VIN、配置、年份；召回频率不同造成严重样本偏差。','next_input':'分车型历史零售/新登记＋适用UTV存活/迁移参数'},
 {'area':'加拿大','status':'partial','gap':'只采用美国公告明确另列的加拿大数量；未系统采集全部加拿大召回与登记。','next_input':'加拿大车型VIO/各省非重叠登记，及独立车型目录'},
 {'area':'墨西哥','status':'partial','gap':'仅Wildcat Trail/Sport选中批次有可归属数量；Can-Am 34台为跨系列混合池。','next_input':'车型级UTV销售/存量和PROFECO等当地来源'},
 {'area':'目录完整性','status':'partial','gap':'目录为已发现条目，未覆盖全部现售/停产及贴牌品牌；100%来源行映射不等于全市场覆盖。','next_input':'补查CFMOTO UFORCE/Z10、Kawasaki KRX/SX、Honda 500/520、Segway Villain、ODES、Bennche、Kandi、Cazador、Rural King等'},
 {'area':'单车型拆分','status':'unknown','gap':'合并组的子车型不按平均份额、关注度、车源数量或价格拆量。','next_input':'同口径分车型数量或可复核分配表'},
 {'area':'估算参数','status':'assumption','gap':'0.80/0.90/0.95兑现系数及0.88/0.93/0.97年保留系数为研究假设，未经UTV实证标定。','next_input':'车型/用途/车龄存活率研究或登记跟踪样本'},
 {'area':'原文异常','status':'retained','gap':'GENERAL原文销售期倒置、Kubota RTV400/500年款与起售期矛盾、Brawley两份数量差异均保留。','next_input':'OEM修订或VIN清单，不从VIN首尾做减法'},
 {'area':'代际/适配','status':'unknown','gap':'本版来源窗口不是完整代际，存量规模不能证明配件接口、适配或需求。','next_input':'OEM零件号、安装接口、分代/车架与实车验证'},
]
writecsv('known_gaps.csv',gaps)
method={
 'methodology_id':'recall-cohort-scenario-v1','as_of_date':ASOF,'unit':'vehicles','purpose':'从官方可识别历史批次构建保守存量研究基准，保留全量未知',
 'formula':'historical_affected_units × active_factor × annual_retention ^ (2026 − min(oldest_model_year, oldest_sale_year))',
 'parameters':PARAMS,'parameter_provenance':'Analyst assumptions authorized for exploratory estimation, NOT empirically estimated UTV survival rates.',
 'rules':['只计算被明确列示的历史批次，不对遗漏年份、新销量、无召回车型或未覆盖VIN作上调。','按最老年份对整个批次施压，偏向低估；不是批次平均车龄。','只对明确不同年款的选中批次求和；其他重叠只取代表记录。','混合组保留组名，子车型全量与批次情景均不强制填充。','不同国家分别计算；不做北美总量、不做全市场占比或跨车型市场份额排名。','区间是参数压力情景，不是统计置信区间、严格上下界或当前安全可用车辆数。','召回修复、事故报废、出口、停用与实际活跃状态未逐车核验；兑现系数只是折减假设。','展示基准向下舍入：≥1,000按100台，≥100按10台，其余按1台；较缓情景向上舍入。'],
 'full_fleet_population':'unknown for every catalog entry','observed_vio_records':0,'observed_registration_records':0,
 'reference_logic':['country -> canonical model/explicit source group -> cohort detail','annual sales separated from population','model-year windows retained without invented generation split','row-level evidence, coverage gaps, export, interactive detail'],
 'reference_chat_id':'019fca97-cd97-7171-b05a-ec6b5428d00e','reference_chat_title':'优化北美车型数据统计 - 每月',
 'deviation_from_skill':'Exploratory assumptions are held in cohort_scenarios.csv, not vehicle_population.csv. No sourced UTV survival curve was acquired, so these are not validated cohort-survival VIO estimates.'}
(DATA/'methodology.json').write_text(json.dumps(method,ensure_ascii=False,indent=2),encoding='utf8')
payload=dict(as_of_date=ASOF,models=models,components=cohorts,scenarios=scenarios,sources=ledger,evidence_pool=pool,gaps=gaps,method=method,
             country_summary=[dict(country=c,quantified_entries=sum(r['country']==c and r['historical_affected_units'] is not None for r in scenarios),model_rows=sum(r['country']==c for r in scenarios),full_population=None,scope='partial') for c in ['US','CA','MX']],
             counts=dict(catalog_entries=len(models),source_group_entries=sum(m['group'] for m in models),named_series_entries=sum(not m['group'] for m in models),source_count=len(ledger),components=len(cohorts),observed_vio=0))
(DATA/'dataset.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(payload['counts'],ensure_ascii=False));print(json.dumps(payload['country_summary'],ensure_ascii=False))
