import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'输出'
DATA=OUT/'data'
scenario=json.loads((DATA/'scenario_qa_report.json').read_bytes())
standard=json.loads((DATA/'qa_report.json').read_bytes())
qa=json.loads((DATA/'delivery_qa.json').read_bytes())
assert scenario['passed'] and standard['error_count']==0 and qa['passed']
assert qa['closed_all_test_pages'] and qa['closed_owned_browser']
qa['visual_review']={'desktop_1440':'inspected: table, source imagery and detail readable',
    'mobile_390':'inspected: cards display complete primary values; modal and method fit viewport',
    'workbook_eight_sheets':'rendered and inspected; values, labels and headers readable'}
qa['standard_data_qa']={'errors':standard['error_count'],'warnings':standard['warning_count'],
    'retained_warning_types':{'unknown_generation':76,'partial_market_coverage':1}}
qa['scenario_data_qa']={'passed':True,'checks':scenario['check_count']}
(DATA/'delivery_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')

entry='北美UTV保有量研究-20261117.html'
assert (OUT/entry).is_file() and (OUT/'研究说明.md').is_file()
assert not list(OUT.glob('*.ndjson'))
file_list=[]
for p in sorted(OUT.rglob('*')):
    if not p.is_file() or p.name=='交付清单.json':continue
    content=p.read_bytes()
    file_list.append({'path':p.relative_to(OUT).as_posix(),'bytes':len(content),
                      'sha256':hashlib.sha256(content).hexdigest()})
manifest={'schema_version':1,'delivery_id':'na-utv-population-20261117',
    'source_task_id':'01a1d30f-d97a-7532-9cae-759ea260d0fa',
    'source_task_title':'查找UTV和ATV销量渠道','business_project_id':None,
    'as_of_date':'2026-11-17','stage':'final-candidate','user_adopted':False,
    'entry':entry,'workbook':'北美UTV车型保有量保守情景-20261117.xlsx',
    'data_directory':'data','files':file_list,'hashed_files':len(file_list),
    'archive':{'status':'not_created','reason':'No confirmed business project for current source conversation; reference conversation project is not reused.'},
    'acceptance':{'public_sources_and_snapshots':105,'catalog_entries':124,
                  'quantified_country_entries':{'US':63,'CA':15,'MX':1},
                  'full_model_vio':'unknown for all entries','scenario_checks_passed':3053,
                  'browser_checks_passed':37,'formulas_sensitivity_passed':True,
                  'desktop_mobile_visual_review':'passed','reference_data_logic':'country -> series/explicit group -> cohort -> source'},
    'limits':['Not a complete UTV model inventory.','Cohort assumptions are not calibrated survival rates.','Known-cohort scenarios are not full population estimates, confidence intervals, strict bounds or market shares.']}
(OUT/'交付清单.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
for f in manifest['files']:
    assert hashlib.sha256((OUT/f['path']).read_bytes()).hexdigest()==f['sha256']
print(json.dumps({'delivery_id':manifest['delivery_id'],'files':len(file_list),'total_bytes':sum(f['bytes'] for f in file_list),'stage':manifest['stage'],'archive':manifest['archive']['status']}))
