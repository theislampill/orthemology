"""Independent deterministic cross-language examples, not an equivalence proof."""
import importlib.util,json,random
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('review_diagnostic',ROOT/'sources/diagnostic.py')
d=importlib.util.module_from_spec(spec); spec.loader.exec_module(d)
rng=random.Random(20261010)
leaves=[('var',0),('var',1),('var',42),('i',),('k',),('s',),('zero',),('one',)]
def app(f,x):return ('app',f,x)
def random_term(depth):
    if depth<=0 or rng.random()<.38:return rng.choice(leaves)
    children=[random_term(depth-1) for _ in range(3)]
    shape=rng.randrange(5)
    if shape==0:return app(('i',),children[0])
    if shape==1:return app(app(('k',),children[0]),children[1])
    if shape==2:return app(app(app(('s',),children[0]),children[1]),children[2])
    return app(children[0],children[1])
def lean(t):
    if t[0]=='app':return f'(.app {lean(t[1])} {lean(t[2])})'
    if t[0]=='var':return f'(.var {t[1]})'
    return '.'+t[0]
def poly(t):
    # Mix compound literal atoms and polynomial applications, retaining variables.
    if t[0]=='var':return ['var',t[1]]
    def closed(x):return x[0]!='var' and (x[0]!='app' or (closed(x[1]) and closed(x[2])))
    if closed(t) and rng.random()<.6:return ['atom',d.thaw(t)]
    if t[0]=='app':return ['app',poly(t[1]),poly(t[2])]
    return ['atom',[t[0]]]
terms=leaves+[random_term(5) for _ in range(256)]
terms += [app(app(('i',),('i',)),('var',0)),d.interpret(['atom',d.SOURCE['omega']])]
lines=['import OpenDevelopments','namespace CrossLanguageReview','open OpenTermStandardness OpenDevelopments','set_option maxRecDepth 32768','set_option maxHeartbeats 8000000']
records=[]
for i,t in enumerate(terms):
    out,trace=d.develop(t,d.Budget(100000,1000000))
    assert d.replay_checked(t,trace)==out,(i,'trace')
    p=poly(t)
    assert d.interpret(p)==t,(i,'interp')
    lines += [f'example : dev ({lean(t)} : T) = {lean(out)} := by decide',f'example : ImportedOpenTermTransport.interp ({d.lean_poly(p)} : P01D.Poly) T.var = {lean(t)} := by decide']
    records.append({'index':i,'input':d.thaw(t),'output':d.thaw(out),'trace':trace,'poly':p})
lines+=['end CrossLanguageReview']
(ROOT/'CrossLanguageReview.lean').write_text('\n'.join(lines)+'\n')
(ROOT/'validation/CROSS_LANGUAGE_CASES.json').write_text(json.dumps(records,separators=(',',':'))+'\n')
print('PASS',len(terms),'Python complete development and independent address replays; Lean obligations generated.')
