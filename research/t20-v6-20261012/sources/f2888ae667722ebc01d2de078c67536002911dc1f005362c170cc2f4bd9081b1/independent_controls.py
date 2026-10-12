#!/usr/bin/env python3
"""Independent finite checks. Explicit failures remain active under python -O."""
import hashlib, importlib.util, importlib.machinery, json, sys, runpy
from pathlib import Path
from itertools import product
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
AUTHOR = HERE.parent/'grounding_provenance'
def require(p, message):
    if not p: raise RuntimeError(message)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def partitions(n):
    for q in product(range(n), repeat=n):
        if q[0] == 0 and all(q[i] <= max(q[:i])+1 for i in range(1,n)):
            yield q
def edge(mask, i, j, width): return bool(mask & (1 << (i*width+j)))
def compose(l,r,q=None):
    return {(x,y) for x in range(2) for y in range(2)
            if any(edge(l,x,m,3) and edge(r,n,y,2) and
                   (m==n if q is None else q[m]==q[n])
                   for m in range(3) for n in range(3))}
def profile(r,m): return tuple(edge(r,m,y,2) for y in range(2))
def uniform(r,q): return all(q[m]!=q[n] or profile(r,m)==profile(r,n)
                             for m in range(3) for n in range(3))
def main():
    snapshots={str(p.relative_to(ROOT)):digest(p) for p in AUTHOR.iterdir() if p.is_file()}
    bindings=json.loads((AUTHOR/'INPUT_BINDINGS.json').read_text())
    source_checks=[]
    for s in bindings['sources']:
        p=ROOT/s['path']; actual=digest(p)
        require(actual==s['sha256'] and p.stat().st_size==s['bytes'],s['id']+' binding mismatch')
        snapshots[s['path']]=actual
        source_checks.append({'id':s['id'],'sha256':actual,'bytes':p.stat().st_size})
    fixed=uniform_cases=0
    for r in range(64):
        for q in partitions(3):
            exact_all=True
            for l in range(64):
                c=compose(l,r); cq=compose(l,r,q)
                lift=all(any(edge(l,x,k,3) and edge(r,k,y,2) for k in range(3))
                         for x in range(2) for y in range(2) for m in range(3) for n in range(3)
                         if edge(l,x,m,3) and edge(r,n,y,2) and q[m]==q[n])
                require(c <= cq and ((c==cq)==lift),'fixed lifting')
                active_l={m for m in range(3) if any(edge(l,x,m,3) for x in range(2))}
                active_r={m for m in range(3) if any(edge(r,m,y,2) for y in range(2))}
                accepted={(m,n) for m in active_l for n in active_r if q[m]==q[n]}
                genuine={(m,m) for m in active_l & active_r}
                require((accepted==genuine)==all(m==n for m,n in accepted),'active witness')
                if len(set(q))==1:
                    rectangle={(x,y) for x in range(2) for y in range(2)
                               if any(edge(l,x,m,3) for m in range(3)) and any(edge(r,n,y,2) for n in range(3))}
                    require(cq==rectangle,'constant rectangle')
                exact_all &= c==cq; fixed+=1
            require(exact_all==uniform(r,q),'uniform criterion'); uniform_cases+=1
    # Two-relation continuation families, arbitrary pre-existing summary, and
    # brute-force minimal fixed alphabet (including reuse across q-fibres).
    sidecars=0
    for r1 in range(64):
        for r2 in range(64):
            profiles=[(profile(r1,m),profile(r2,m)) for m in range(3)]
            for q in partitions(3):
                expected=max(len({profiles[m] for m in range(3) if q[m]==z}) for z in set(q))
                minimum=None
                for d in range(1,4):
                    if any(all(q[m]!=q[n] or h[m]!=h[n] or profiles[m]==profiles[n]
                               for m in range(3) for n in range(3)) for h in product(range(d),repeat=3)):
                        minimum=d; break
                require(minimum==expected,'sidecar minimum'); sidecars+=1
    # Direct Boolean rectangle-cover lower/upper bound, independently computed.
    boolean=[]
    for n in range(1,7):
        diagonal={(i,i) for i in range(n)}
        usable=[]
        for a in range(1,1<<n):
            for b in range(1,1<<n):
                rect={(i,j) for i in range(n) for j in range(n) if a>>i&1 and b>>j&1}
                if rect <= diagonal: usable.append(rect)
        require(len(usable)==n and all(len(r)==1 for r in usable),'diagonal rectangles')
        require(set().union(*usable)==diagonal,'attainable Boolean rank')
        boolean.append({'n':n,'nonempty_usable_rectangles':len(usable),'minimum_cover':n})
    # Execute the exact author's bytes without writing its VERIFICATION.json.
    require(not sys.flags.optimize,'Author replay only allowed with assertions enabled')
    ns=runpy.run_path(str(AUTHOR/'verify.py'),run_name='independent_author_replay')
    replay=HERE/'author_replay'; replay.mkdir(exist_ok=True)
    ns['main'].__globals__['HERE']=replay
    ns['main']()
    # Negative operational controls: inactive candidate and missing actual input.
    s=next(s for s in bindings['sources'] if s['id']=='S04'); p=ROOT/s['path']
    name='independent_grounding_engine'
    loader=importlib.machinery.SourceFileLoader(name,str(p)); spec=importlib.util.spec_from_loader(name,loader)
    engine=importlib.util.module_from_spec(spec); sys.modules[name]=engine; loader.exec_module(engine)
    m0,m1,e0,e1=[engine.Event(k,'created') for k in ['m0','m1','e0','e1']]
    rules=(engine.rule('left0','A',output=m0),engine.rule('left1','A',output=m1),
           engine.rule('right0',(),inputs=['m0'],output=e0),engine.rule('right1',(),inputs=['m1'],output=e1),
           engine.rule('inactive-cross','B',inputs=['m0'],output=e1))
    run=engine.run(rules,'A')
    require({p.rule for p in run.proofs['e1']}=={'right1'},'dormant candidate must not be actual')
    cut=engine.run(rules,'A',disabled=['left1'])
    require(set(cut.events)=={'m0','e0'},'missing actual input cannot be supplied by same root label')
    require(all(run.productive_roots(k)==frozenset('A') for k in run.events),'one source retained')
    for name,sha in snapshots.items(): require(digest(ROOT/name)==sha,'input changed: '+name)
    out={'status':'PASS','source_bindings':source_checks,'fixed_endpoint_and_active_witness_cases':fixed,
         'uniform_upstream_cases':uniform_cases,'two_continuation_sidecar_cases':sidecars,
         'boolean_diagonal_covers':boolean,'engine_negative_controls':['dormant B cross-route excluded','disabled m1 producer prevents e1 despite shared A'],
         'author_replay':'exact code, assertions enabled, output redirected to review directory',
         'optimized_author_verification_credit':False,'inputs_unchanged':True,'input_hashes':snapshots}
    (HERE/'CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['input_hashes','source_bindings']},indent=2))
if __name__=='__main__': main()
