"""Read-only extraction of the first Islamweb articleBody (unvocalized layer).
HTML is authoritative retained retrieval; footnote superscripts/hidden nav omitted.
No manuscript or print-page collation is performed.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
class P(HTMLParser):
 def __init__(self): super().__init__();self.depth=0;self.out=[];self.skip=0
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='div' and a.get('id')=='pagebody':self.depth=1;return
  if self.depth:
   if t=='div':self.depth+=1
   if t=='br':self.out.append('\n')
   if a.get('class')=='mainsubjatt' or t=='sup':self.skip+=1
 def handle_endtag(self,t):
  if self.depth and t=='div':self.depth-=1
  if self.skip and t in ('span','sup'):self.skip-=1
 def handle_data(self,d):
  if self.depth and not self.skip:self.out.append(d)
if __name__=='__main__':
 for p in Path(__file__).parent.glob('*.html'):
  x=P();x.feed(p.read_text());ls=[re.sub(r'\s+',' ',l).strip() for l in ''.join(x.out).splitlines() if l.strip()]
  p.with_suffix('.txt').write_text('\n'.join(f'L{i:03} {l}' for i,l in enumerate(ls,1))+'\n')
  print(p.name,len(ls))
