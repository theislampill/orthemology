from html.parser import HTMLParser
from pathlib import Path
import urllib.request,json,hashlib,re
class Plain(HTMLParser):
 def __init__(self):super().__init__();self.out=[];self.skip=0
 def handle_starttag(self,t,attrs):
  if t in ('script','style'):self.skip+=1
  if t in ('br','p','div','h1','h2','h3','title'):self.out.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip-=1
  if t in ('p','div','h1','h2','h3','title'):self.out.append('\n')
 def handle_data(self,d):
  if not self.skip:self.out.append(d)
out=Path(__file__).parent
r=[]
for name,url in [('safadiyya002','https://www.islamicbook.ws/amma/alsfdit-002.html'),('dar013','https://www.islamicbook.ws/amma/dr-taardh-alaql-walnql-013.html')]:
 try:
  b=urllib.request.urlopen(url,timeout=30).read();(out/(name+'.html')).write_bytes(b)
  s=Plain();s.feed(b.decode('utf-8'));ls=[re.sub(r'\s+',' ',x).strip() for x in ''.join(s.out).splitlines() if x.strip()]
  (out/(name+'.txt')).write_text('\n'.join(f'L{i:04} {l}' for i,l in enumerate(ls,1))+'\n')
  r.append({'name':name,'url':url,'html_sha256':hashlib.sha256(b).hexdigest(),'line_count':len(ls),'status':'acquisition only; read ranges separately'})
 except Exception as e:r.append({'name':name,'url':url,'error':str(e)})
p=out/'ACQUISITION.json';p.write_text(json.dumps(json.loads(p.read_text())+r,indent=2));print(json.dumps(r,indent=2))
