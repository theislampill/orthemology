import urllib.request,concurrent.futures,pathlib,json,hashlib,datetime,re
from html.parser import HTMLParser
root=pathlib.Path(__file__).parent/'sources'
class Text(HTMLParser):
 def __init__(self): super().__init__(); self.out=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'): self.skip+=1
  if t in ('p','br','div','li'): self.out.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style'): self.skip=max(0,self.skip-1)
  if t in ('p','div','li'): self.out.append('\n')
 def handle_data(self,x):
  if not self.skip:self.out.append(x)
def fetch(n):
 u=f'https://www.islamweb.net/ar/library/content/413/{n}/'
 try:
  r=urllib.request.urlopen(u,timeout=90);b=r.read(); (root/f'dar-{n}.html').write_bytes(b)
  p=Text();p.feed(b.decode('utf-8'));txt='\n'.join(x.strip() for x in ''.join(p.out).splitlines() if x.strip());(root/f'dar-{n}.txt').write_text(txt)
  return dict(id=n,url=u,status=r.status,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e:return dict(id=n,url=u,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex: data=list(ex.map(fetch,[1270,1271,920,921,922]))
(root/'ACQUISITION.json').write_text(json.dumps(data,indent=2));print(json.dumps(data,indent=2))
