import urllib.request, urllib.parse, json, hashlib, concurrent.futures
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DEST=ROOT/'sources'; DEST.mkdir(exist_ok=True)
queries=['vehicle','Yamaha','Kawasaki','Honda','BRP','Deere','Kubota','CFMOTO','Hisun','American Landmaster','Massimo','Intimidator','Kymco','Mahindra','Arctic Cat','Textron','Kandi','Kohler']
def fetch(q):
    u='https://www.saferproducts.gov/RestWebServices/Recall?'+urllib.parse.urlencode({'format':'json','RecallTitle':q})
    path=DEST/('cpsc-'+q.lower().replace(' ','-')+'.json')
    try:
        if not path.exists():
            with urllib.request.urlopen(u,timeout=60) as r: path.write_bytes(r.read())
        b=path.read_bytes(); data=json.loads(b)
        return {'query':q,'url':u,'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(b).hexdigest(),'records':len(data),'latest':max((x['RecallDate'] for x in data),default='')}
    except Exception as e:return {'query':q,'url':u,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: manifest=list(pool.map(fetch,queries))
(DEST/'request-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
allrecs={}
for p in DEST.glob('cpsc-*.json'):
    try:
        for r in json.loads(p.read_bytes()):allrecs[r['RecallID']]=r
    except Exception:pass
data=sorted(allrecs.values(),key=lambda r:r['RecallDate'],reverse=True)
(DEST/'cpsc-merged.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(manifest,ensure_ascii=False)); print('unique',len(data)); print('fields',list(data[0]))
