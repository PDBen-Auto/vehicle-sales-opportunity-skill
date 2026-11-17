from pathlib import Path
import json,urllib.request,concurrent.futures,hashlib,io
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parent;DATA=ROOT.parent/'输出/data';PROC=ROOT/'images';PROC.mkdir(exist_ok=True)
d=json.loads((DATA/'dataset.json').read_bytes());recalls={r['RecallID']:r for r in json.loads((ROOT/'sources/cpsc-merged.json').read_bytes())}
def task(m):
 sid=next((s for s in m['source_ids'] if s.startswith('cpsc-')),None)
 if not sid or m.get('parent_id'):return None
 r=recalls[int(sid.split('-')[-1])]
 if not r['Images']:return None
 im=r['Images'][0];u=im['URL'];p=PROC/(sid+'.raw')
 try:
  if not p.exists():
   with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as f:p.write_bytes(f.read())
  img=Image.open(p).convert('RGB');img.thumbnail((520,340));b=io.BytesIO();img.save(b,format='WEBP',quality=78)
  import base64
  return {'model_id':m['id'],'image_data':'data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode(),'url':u,'caption':im.get('Caption',''),'source_id':sid,'source_page':r['URL'],'original_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'width':img.width,'height':img.height,'usage_note':'CPSC公告中的历史召回车型图；不代表当前全系或配件适配。'}
 except Exception as e:return {'model_id':m['id'],'error':str(e),'url':u}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:rows=[x for x in pool.map(task,d['models']) if x]
(DATA/'vehicle_images.json').write_text(json.dumps(rows,ensure_ascii=False),encoding='utf8')
print('images',sum('image_data'in x for x in rows),'failed',sum('error'in x for x in rows))
