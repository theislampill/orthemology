from html.parser import HTMLParser
from pathlib import Path
class BodyParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.active=False; self.depth=0; self.hidden=0; self.parts=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if not self.active and tag=='div' and attrs.get('id')=='pagebody':
            self.active=True; self.depth=1; return
        if self.active:
            if tag=='div': self.depth+=1
            if tag in ['br','p']: self.parts.append('\n')
            if tag=='span' and ('display:none' in attrs.get('style','') or attrs.get('class','').endswith('att')): self.hidden+=1
    def handle_endtag(self,tag):
        if self.active:
            if tag=='div':
                self.depth-=1
                if self.depth==0: self.active=False
            if tag=='span' and self.hidden: self.hidden-=1
    def handle_data(self,data):
        if self.active and not self.hidden: self.parts.append(data)
root=Path(__file__).resolve().parent/'sources'
for path in sorted(root.glob('item*.html')):
    parser=BodyParser(); parser.feed(path.read_text())
    paras=[' '.join(x.split()) for x in ''.join(parser.parts).split('\n') if x.strip()]
    path.with_suffix('.txt').write_text('\n'.join(f'L{i:03d} {p}' for i,p in enumerate(paras,1))+'\n')
    print(path.stem, len(paras))
