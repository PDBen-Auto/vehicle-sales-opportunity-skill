#!/usr/bin/env python3
"""Build a static public examples site from the already reviewed repository files."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def build(output):
    output=Path(output).resolve()
    if output.exists():raise ValueError('Output directory already exists; choose a new directory')
    case=ROOT/'cases/utv-atv'
    spec=importlib.util.spec_from_file_location('case_verify',case/'reproduce.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    verification=module.verify()
    manifest=json.loads((case/'输出/交付清单.json').read_bytes())
    copies=[(ROOT/'docs/index.html',Path('index.html'))]
    for folder in ['demo','multitype-demo']:
        for p in sorted((ROOT/'docs'/folder).iterdir()):
            if p.is_file():copies.append((p,Path(folder)/p.name))
    for item in manifest['files']:
        rel=Path(item['path'])
        source=(case/'输出'/rel).resolve()
        if not source.is_relative_to((case/'输出').resolve()):raise ValueError('Invalid public case path')
        if hashlib.sha256(source.read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Case source hash drift')
        copies.append((source,Path('cases/utv-atv')/rel))
    copies.append((case/'输出/交付清单.json',Path('cases/utv-atv/交付清单.json')))
    copies.append((case/'输出'/manifest['entry'],Path('cases/utv-atv/index.html')))
    if len({str(rel)for _,rel in copies})!=len(copies):raise ValueError('Duplicate public path')
    output.mkdir(parents=True)
    for source,rel in copies:
        dest=output/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
        if hashlib.sha256(dest.read_bytes()).digest()!=hashlib.sha256(source.read_bytes()).digest():raise ValueError('Public file copy mismatch')
    (output/'.nojekyll').write_text('',encoding='utf-8')
    return {'status':'pass','files':len(copies)+1,'caseVerification':verification,'output':str(output),'caseEntry':'cases/utv-atv/','syntheticEntries':['demo/dashboard.html','multitype-demo/dashboard.html']}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True,type=Path);args=parser.parse_args()
    try:result=build(args.output)
    except(ValueError,OSError)as exc:parser.exit(2,str(exc)+'\n')
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
