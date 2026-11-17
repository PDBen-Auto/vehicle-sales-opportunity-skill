"""Acceptance checks for the exploratory cohort extension, not a VIO validation."""
import base64, csv, hashlib, io, json, math, re
from collections import defaultdict
from pathlib import Path
from PIL import Image
import openpyxl

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / '输出'
DATA = OUT / 'data'
d = json.loads((DATA / 'dataset.json').read_bytes())
errors, checks = [], []
def check(name, condition, detail=''):
    checks.append({'check': name, 'passed': bool(condition), 'detail': detail})
    if not condition: errors.append(name + (': ' + str(detail) if detail else ''))
def readcsv(name):
    with (DATA / name).open(encoding='utf-8-sig', newline='') as f: return list(csv.DictReader(f))
def rounding(n, up=False):
    unit = 100 if n >= 1000 else 10 if n >= 100 else 1
    return int((math.ceil(n/unit) if up else math.floor(n/unit))*unit)

models = {m['id']: m for m in d['models']}
sources = {s['source_id']: s for s in d['sources']}
components = {c['component_id']: c for c in d['components']}
check('unique_model_ids', len(models) == len(d['models']))
check('unique_source_ids', len(sources) == len(d['sources']))
check('unique_component_ids', len(components) == len(d['components']))
keys = [(r['country'], r['canonical_model_id']) for r in d['scenarios']]
check('unique_country_model_keys', len(keys) == len(set(keys)))
check('three_country_rows_per_catalog_entry', len(keys) == len(models)*3)
check('all_full_population_values_unknown', all(r['full_model_population'] is None for r in d['scenarios']))
check('all_standard_observed_tables_empty', all(not readcsv(f) for f in ['vehicle_population.csv', 'vehicle_population_rollup.csv', 'annual_sales.csv', 'country_controls.csv']))

for sid, s in sources.items():
    snap = DATA / s['local_snapshot']
    check('source_snapshot_' + sid, snap.is_file() and hashlib.sha256(snap.read_bytes()).hexdigest() == s['checksum_sha256'])
for mid, m in models.items():
    check('model_sources_' + mid, bool(m['source_ids']) and all(x in sources for x in m['source_ids']))
    if m.get('parent_id'):
        check('group_child_' + mid, m['parent_id'] in models and models[m['parent_id']]['group'] and not m['parts'])

by_model = defaultdict(list)
used_source_country = set()
for cid, c in components.items():
    check('component_fk_' + cid, c['model_id'] in models and c['source_id'] in sources)
    check('component_age_' + cid, c['age'] == max(0, 2026-min(c['model_year_start'], c['oldest_sale_year'])) and c['age_basis_year'] == min(c['model_year_start'], c['oldest_sale_year']))
    check('component_positive_units_' + cid, c['historical_units'] > 0)
    key = c['country'], c['source_id']
    check('source_not_reused_across_models_' + cid, key not in used_source_country)
    used_source_country.add(key)
    by_model[(c['country'], c['model_id'])].append(c)
    for p, v in d['method']['parameters'].items():
        exact = c['historical_units']*v['active']*v['retention']**c['age']
        check('component_math_' + p + '_' + cid, math.isclose(exact, c[p+'_unrounded'], rel_tol=1e-12))
    raw = json.loads((DATA/sources[c['source_id']]['local_snapshot']).read_bytes())
    check('source_country_quantity_' + cid, c['units_text'] == ' / '.join(p['NumberOfUnits'] for p in raw['Products']))
    if c['country'] != 'US':
        country = {'CA':'Canada','MX':'Mexico'}[c['country']]
        found = re.search(r'(\d[\d,]*)\s+(?:(?:ROVs?|units?|vehicles?|were|was|sold|also)\s+){0,5}in\s+' + country, c['units_text'], re.I)
        check('foreign_quantity_' + cid, found is not None and int(found[1].replace(',','')) == c['historical_units'])

for (country, mid), cc in by_model.items():
    spans = sorted((c['model_year_start'], c['model_year_end']) for c in cc)
    check('nonoverlapping_selected_windows_' + country + '_' + mid, all(spans[i][1] < spans[i+1][0] for i in range(len(spans)-1)))

for row in d['scenarios']:
    mid, country = row['canonical_model_id'], row['country']
    cc = by_model[(country, mid)]
    check('scenario_source_fk_' + country + '_' + mid, all(s in sources for s in row['source_ids'].split(';')))
    if not cc:
        check('no_unsupported_number_' + country + '_' + mid, all(row[k] is None for k in ['historical_affected_units','conservative_batch_scenario','severe_batch_scenario','less_severe_batch_scenario']))
        continue
    check('scenario_historical_' + country + '_' + mid, row['historical_affected_units'] == sum(c['historical_units'] for c in cc))
    for p in ['conservative','severe','less_severe']:
        check('scenario_math_' + p + '_' + country + '_' + mid, row[p+'_batch_scenario'] == rounding(sum(c[p+'_unrounded'] for c in cc), p=='less_severe'))
    check('scenario_order_' + country + '_' + mid, row['severe_batch_scenario'] <= row['conservative_batch_scenario'] <= row['less_severe_batch_scenario'])
    check('scenario_country_verified_' + country + '_' + mid, row['market_presence'] == 'historical_quantity_verified')

us = {r['canonical_model_id']: r for r in d['scenarios'] if r['country']=='US'}
check('talon_not_double_counted', us['honda.talon-1000']['historical_affected_units'] == 34000)
check('brawley_newer_smaller_selected', us['vanderhall.brawley']['historical_affected_units'] == 190)
check('xd1500_winch_excluded', us['polaris.ranger-xd1500']['historical_affected_units'] == 10500)
check('accessories_atv_excluded', not ({8889,10175,10224,8407} & {c['recall_id'] for c in components.values()}))
check('rhino_distinct_subsets_145000', us['yamaha.rhino-group']['historical_affected_units'] == 145000)
check('pioneer_overlap_excluded', us['honda.pioneer-1000']['historical_affected_units'] == 82000)
check('rzr_xp1000_baseline_example', us['polaris.rzr-xp1000']['conservative_batch_scenario'] == 52600)
check('different_mule_generations_scoped', max(c['model_year_end'] for c in by_model[('US','kawasaki.mule-pro-legacy-group')]) < min(c['model_year_start'] for c in by_model[('US','kawasaki.mule-pro1000-group')]))

csv_rows = readcsv('cohort_scenarios.csv')
check('csv_row_count_matches', len(csv_rows)==len(d['scenarios']))
for n, r in enumerate(csv_rows):
    x=d['scenarios'][n]
    check('csv_values_' + str(n), r['country']==x['country'] and r['canonical_model_id']==x['canonical_model_id'] and all(r[k]==('' if x[k] is None else str(x[k])) for k in ['historical_affected_units','conservative_batch_scenario','severe_batch_scenario','less_severe_batch_scenario','full_model_population']))

book = OUT / '北美UTV车型保有量保守情景-20261117.xlsx'
wb = openpyxl.load_workbook(book, data_only=True, read_only=True)
check('eight_workbook_sheets', len(wb.sheetnames)==8)
ws=wb['车型估算']
for i, row in enumerate(d['scenarios'], 5):
    values = [ws.cell(i,col).value for col in range(6,11)]
    expected = [row[k] if row[k] is not None else 'unknown' for k in ['historical_affected_units','conservative_batch_scenario','severe_batch_scenario','less_severe_batch_scenario','full_model_population']]
    check('xlsx_cached_values_' + str(i), values==expected, '' if values==expected else repr((values,expected)))
for i,country in enumerate(['US','CA','MX'],8):
    n=sum(r['country']==country and r['historical_affected_units'] is not None for r in d['scenarios'])
    check('xlsx_country_count_'+country,wb['概览'].cell(i,2).value==n)
formula_errors=[]
for sheet in wb:
    for cells in sheet:
        for cell in cells:
            if cell.data_type=='e':formula_errors.append([sheet.title,cell.coordinate,cell.value])
check('no_workbook_cached_errors',not formula_errors,repr(formula_errors))
check('xlsx_parameter_values', [wb['参数'].cell(i,2).value for i in range(5,12)]==[2026,.9,.93,.8,.88,.95,.97])
wb.close()
formulas = openpyxl.load_workbook(book, data_only=False, read_only=True)
check('xlsx_preserves_editable_formulas', formulas['车型估算']['G5'].value.startswith('=FLOOR(') and formulas['批次计算']['I5'].value.startswith('=H5*'))
formulas.close()
check('workbook_sensitivity_and_restore',json.loads((ROOT/'qa/workbook-sensitivity.json').read_bytes())['passed'])

html=(OUT/'北美UTV保有量研究-20261117.html').read_text(encoding='utf-8')
data_s, image_s = html.split('<script>const D=',1)[1].split(';const IM=',1)
check('html_embedded_data_matches',json.loads(data_s.replace('<\\/','</'))==d)
im=json.loads(image_s.split(';\nconst $=',1)[0].replace('<\\/','</'))
check('html_embedded_images_match',im==json.loads((DATA/'vehicle_images.json').read_bytes()))
successful=0
for x in im:
    if not x.get('image_data'):continue
    img=Image.open(io.BytesIO(base64.b64decode(x['image_data'].split(',',1)[1])))
    img.verify();successful+=1
    check('image_source_'+x['model_id'],x['source_id'] in sources and x['model_id'] in models)
check('52_images_decode',successful==52)
check('no_remote_runtime_dependencies', not re.search(r'<(?:script|link)[^>]+(?:src|href)=[\"\']https?://',html))
check('no_placeholder_left', '__DATA__' not in html and '__IMAGES__' not in html)
check('no_replacement_characters', '\ufffd' not in html and '\ufffd' not in (OUT/'研究说明.md').read_text(encoding='utf-8'))
local_links=re.findall(r'href="([^"#]+)"',html.split('<script>',1)[0])
check('all_static_local_links_exist',all((OUT/h).is_file() for h in local_links if not re.match(r'\w+:',h)))
result={'as_of_date':d['as_of_date'],'passed':not errors,'check_count':len(checks),'errors':errors,'checks':checks,
    'limits':['Checks confirm structural, arithmetic and delivery consistency only.','Analyst parameters are not empirically validated UTV survival rates.','This is not a complete model-level VIO or market coverage validation.'],
    'summary':{'catalog_entries':len(models),'quantified_rows':len([r for r in d['scenarios'] if r['historical_affected_units'] is not None]),'components':len(components),'sources':len(sources),'decoded_images':successful}}
(DATA/'scenario_qa_report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['checks','limits']},ensure_ascii=True))
if errors:raise SystemExit(1)
