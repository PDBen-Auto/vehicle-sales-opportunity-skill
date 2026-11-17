#!/usr/bin/env python3
"""Verify a frozen real case and rebuild offline into a new directory."""
from __future__ import annotations
import argparse,csv,hashlib,json,math,shutil,subprocess,sys,zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def load(path):return json.loads(Path(path).read_bytes())

def verify(case_root=ROOT):
    root=Path(case_root);out=root/'输出';data=out/'data';checks=0
    def check(value,message):
        nonlocal checks
        checks+=1
        if not value:raise ValueError(message)
    manifest=load(out/'交付清单.json')
    for item in manifest['files']:
        path=(out/item['path']).resolve()
        check(path.is_relative_to(out.resolve()),'Invalid snapshot path')
        check(hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'],'Snapshot drift: '+item['path'])
    d=load(data/'dataset.json');sources={s['source_id']:s for s in d['sources']};models={m['id']:m for m in d['models']}
    check(len(models)==124 and len(sources)==105,'Frozen case count changed')
    for source in sources.values():
        check(hashlib.sha256((data/source['local_snapshot']).read_bytes()).hexdigest()==source['checksum_sha256'],'Source snapshot mismatch')
    groups=defaultdict(list)
    for c in d['components']:
        check(c['model_id']in models and c['source_id']in sources,'Broken component FK')
        check(c['age']==max(0,2026-min(c['model_year_start'],c['oldest_sale_year'])),'Age mismatch')
        for scenario,p in d['method']['parameters'].items():
            check(math.isclose(c['historical_units']*p['active']*p['retention']**c['age'],c[scenario+'_unrounded'],rel_tol=1e-12),'Component arithmetic mismatch')
        groups[(c['country'],c['model_id'])].append(c)
    def rounded(n,up=False):
        unit=100 if n>=1000 else 10 if n>=100 else 1
        return int((math.ceil(n/unit)if up else math.floor(n/unit))*unit)
    seen=set()
    for row in d['scenarios']:
        key=(row['country'],row['canonical_model_id']);cc=groups[key]
        check(key not in seen,'Duplicate scenario key');seen.add(key)
        check(row['full_model_population']is None,'Scenario misrepresented as full VIO')
        if not cc:
            check(row['historical_affected_units']is None and row['conservative_batch_scenario']is None,'Unsupported number')
            continue
        check(row['historical_affected_units']==sum(c['historical_units']for c in cc),'Historical sum mismatch')
        spans=sorted((c['model_year_start'],c['model_year_end'])for c in cc)
        check(all(spans[i][1]<spans[i+1][0]for i in range(len(spans)-1)),'Overlapping selected windows')
        for scenario in ('severe','conservative','less_severe'):
            check(row[scenario+'_batch_scenario']==rounded(sum(c[scenario+'_unrounded']for c in cc),scenario=='less_severe'),'Scenario arithmetic mismatch')
    counts={country:sum(r['country']==country and r['historical_affected_units']is not None for r in d['scenarios'])for country in ['US','CA','MX']}
    check(counts=={'US':63,'CA':15,'MX':1},'Country counts changed')
    us={r['canonical_model_id']:r for r in d['scenarios']if r['country']=='US'}
    for model_id,expected in [('honda.talon-1000',34000),('honda.pioneer-1000',82000),('polaris.ranger-xd1500',10500),('yamaha.rhino-group',145000),('vanderhall.brawley',190)]:
        check(us[model_id]['historical_affected_units']==expected,'Deduplication regression: '+model_id)
    check(us['polaris.rzr-xp1000']['conservative_batch_scenario']==52600,'Reference scenario changed')
    for table in ['annual_sales.csv','vehicle_population.csv','vehicle_population_rollup.csv','country_controls.csv']:
        with (data/table).open(encoding='utf-8-sig',newline='')as f:check(not list(csv.DictReader(f)),'Unknown observed data fabricated')
    html=(out/manifest['entry']).read_text(encoding='utf-8')
    encoded,rest=html.split('<script>const D=',1)[1].split(';const IM=',1)
    check(json.loads(encoded.replace('<\\/','</'))==d,'HTML and dataset differ')
    images=json.loads(rest.split(';\nconst $=',1)[0].replace('<\\/','</'))
    check(images==load(data/'vehicle_images.json'),'HTML image payload differs')
    check(sum(bool(x.get('image_data'))for x in images)==52,'Historical image count changed')
    with zipfile.ZipFile(out/manifest['workbook'])as z:
        check(z.testzip()is None,'XLSX ZIP damaged')
        check(len([n for n in z.namelist()if n.startswith('xl/worksheets/sheet')and n.endswith('.xml')])==8,'Workbook sheet count changed')
        check(any(any(e.tag.rsplit('}',1)[-1]=='f' for e in ET.fromstring(z.read(n)).iter())for n in z.namelist()if n.startswith('xl/worksheets/')and n.endswith('.xml')),'Workbook formulas missing')
    return {'status':'pass','checks':checks,'countryCounts':counts,'catalogEntries':124,'sources':105,'fullModelPopulation':'unknown','scope':'frozen_snapshot_and_internal_arithmetic_not_market_truth'}

def rebuild(workdir):
    result=verify();work=Path(workdir).resolve()
    if work.exists():raise ValueError('Workdir already exists; choose a new directory')
    if work.is_relative_to(ROOT):raise ValueError('Workdir must be outside the frozen case directory')
    shutil.copytree(ROOT,work)
    data_before=load(ROOT/'输出/data/dataset.json')
    for name in ['build_dataset.py','build_report.py']:
        run=subprocess.run([sys.executable,'-B',str(work/'过程'/name)],capture_output=True,text=True,encoding='utf-8')
        if run.returncode:raise RuntimeError(f'{name} failed: {run.stderr[:600]}')
    data_after=load(work/'输出/data/dataset.json')
    if data_after!=data_before:raise ValueError('Offline rebuild changed the completed business dataset')
    result|={'rebuild':'pass','datasetSemanticEquality':True,'networkRequests':0,'newWorkdir':str(work),'checkedAt':datetime.now(timezone.utc).isoformat(),'workbookRebuild':'not_run_original_workbook_preserved'}
    (work/'reproduction-receipt.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--workdir',type=Path);parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
    try:
        if not args.workdir and not args.verify_only:parser.error('Use --workdir NEW_DIRECTORY or --verify-only')
        result=verify()if args.verify_only else rebuild(args.workdir)
    except (ValueError,OSError,RuntimeError)as exc:parser.exit(2,str(exc)+'\n')
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
