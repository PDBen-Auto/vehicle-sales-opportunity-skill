import urllib.request, json, hashlib, concurrent.futures,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent; DEST=ROOT/'sources'
catalogs=[
('polaris','https://www.polaris.com/en-us/off-road/'),
('canam','https://can-am.brp.com/off-road/us/en/models/side-by-side-vehicles.html'),
('honda','https://powersports.honda.com/sxs'),
('yamaha','https://yamahamotorsports.com/side-by-side'),
('kawasaki','https://www.kawasaki.com/en-us/side-x-side'),
('cfmoto','https://www.cfmotousa.com/'),
('segway','https://www.segwaypowersports.us/'),
('arcticcat','https://arcticcat.txtsv.com/side-by-side'),
('deere','https://www.deere.com/en/gator-utility-vehicles/'),
('kubota','https://www.kubotausa.com/products/utility-vehicles'),
('h isun'.replace(' ',''),'https://www.hisunmotors.com/'),
('massimo','https://www.massimomotor.com/'),
('kawasaki-ca','https://www.kawasaki.ca/en-ca/side-x-side'),
('canam-ca','https://can-am.brp.com/off-road/ca/en/models/side-by-side-vehicles.html'),
('canam-mx','https://can-am.brp.com/off-road/mx/es/modelos/side-by-side.html'),
('landmaster','https://landmaster.com/'),
('kymco','https://kymcousa.com/side-x-sides/'),
]
def fetch(item):
 sid,u=item; p=DEST/('catalog-'+sid+'.html')
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=45) as r:b=r.read(); final=r.url
  p.write_bytes(b)
  return {'source_id':'catalog-'+sid,'url':u,'resolved_url':final,'local_snapshot':str(p.relative_to(ROOT)).replace('\\','/'),'checksum_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'title':re.search(r'<title[^>]*>(.*?)</title',b.decode('utf8',errors='replace'),re.S|re.I).group(1).strip()}
 except Exception as e:return {'source_id':'catalog-'+sid,'url':u,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: rows=list(pool.map(fetch,catalogs))
(DEST/'catalog-manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(rows,ensure_ascii=False))
