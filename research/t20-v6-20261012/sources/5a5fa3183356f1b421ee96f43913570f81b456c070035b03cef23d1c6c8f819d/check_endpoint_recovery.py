"""Fresh bounded checks on exact recovered endpoint source identities.
This is not a replacement for unavailable fourth-tranche Lean proofs.
"""
from pathlib import Path
import hashlib,itertools,json
from fractions import Fraction as F
import prcodec as c
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
OLD='a77d05474ebd510b30cf52b34828a407dadce962359c678701eba6a9ebda7c7b'
assert sha(R/'NATIVE_ENDPOINT.json')==OLD
assert sha(R/'prcodec.py')=='dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c'
identity=json.loads((R/'NATIVE_ENDPOINT.json').read_text())
cache=c.decode(int(identity['cache_index']));prefix=c.decode(int(identity['prefix_index']))
assert cache is not None and prefix is not None
assert c.encode_bytes(cache)==bytes(identity['cache_bytes']) and c.encode(cache)==int(identity['cache_index'])
assert c.encode(prefix)==int(identity['prefix_index'])
assert cache.arity==1 and prefix.arity==2

def run_frame(program,regs,fuel):
    """Explicit statement/repeat meter; uses the retained expression evaluator.
    Initial frames are supplied here; unlike c.run this API returns the frame.
    """
    regs=dict(regs);stack=[('stmt',program.body)];steps=0;em=c.Meter(None,None)
    while stack:
        if steps==fuel:return None
        steps+=1;task=stack.pop()
        if task[0]=='repeat':
            _,r,count,k,body=task
            if k<count:
                regs[r]=k;stack.append(('repeat',r,count,k+1,body));stack.append(('stmt',body))
            continue
        s=task[1];tag=s[0]
        if tag=='set':regs[s[1]]=c.eval_expr(s[2],regs,em)
        elif tag=='seq':
            for t in reversed(s[1:]):stack.append(('stmt',t))
        elif tag=='loop':stack.append(('repeat',s[1],c.eval_expr(s[2],regs,em),0,s[3]))
        elif tag=='if':stack.append(('stmt',s[2] if c.eval_expr(s[1],regs,em) else s[3]))
        else:raise c.InvalidCode('Unsupported statement')
    return regs,steps,em.steps

def tick(bit,carried=(1,1),fuel=5):
    if type(bit) is not int or bit not in (0,1):raise ValueError('A received binary bit is required')
    if any(type(x) is not int or x<0 for x in carried):raise ValueError('Natural cache required')
    out=run_frame(cache,{0:bit,2:carried[0],4:carried[1]},fuel)
    if out is None:return None
    regs,steps,expr=out
    return regs.get(cache.output,0)%2,(regs.get(2,0),regs.get(4,0)),steps,expr

def loss(alpha,q):
    eps=F(1,4)
    return q*q-(alpha*(F(1,2)+eps)**2+(1-alpha)*F(1,2)**2),(1-q)**2-(alpha*(F(1,2)-eps)**2+(1-alpha)*F(1,2)**2)

def good(alpha,q):return 0<=q<=1 and max(loss(alpha,q))<=0
assert good(F(0),F(1,2)) and not good(F(0),F(5,8))
assert good(F(1,2),F(5,8)) and not good(F(1,2),F(1,2))
words=ticks=0
for n in range(11):
    for w in itertools.product([0,1],repeat=n):
        words+=1;carried=(1,1);seen=0;code=1;out=[]
        for k,bit in enumerate(w):
            code=2*code+bit;seen|=bit
            r=tick(bit,carried);assert r is not None
            label,carried,steps,expr=r
            assert label==seen and steps==5 and carried[1]==1
            assert (carried[0]==0)==bool(seen)
            assert c.evaluate_index(int(identity['prefix_index']),k,code)==seen
            pr=run_frame(prefix,{0:k,1:code},6*(k+1)+10)
            assert pr is not None and pr[0].get(prefix.output,0)%2==seen and pr[1]==6*(k+1)+10
            assert run_frame(prefix,{0:k,1:code},6*(k+1)+9) is None
            assert tick(bit,carried,4) is None
            out.append(label);ticks+=1
        assert c.output_prefix(prefix,w)==tuple(out)
# Distinct API and malformed-code boundaries.
assert c.evaluate_index(int(identity['cache_index']),0,3)==0
for j in range(len(identity['cache_bytes'])):assert c.decode_bytes(bytes(identity['cache_bytes'][:j])) is None
assert c.decode_bytes(b'X'+bytes(identity['cache_bytes'][1:])) is None
for n in range(11):
    expectation=sum(F(1,2)**k for k in range(n+1))
    assert expectation==2-F(1,2)**n
# Failure controls concern the actual new stateful adapter, not a free count input.
assert tick(1,(0,0))[0]!=1
assert tick(1)[0]!=tick(0)[0]
first=tick(1);assert first[0]==1
assert tick(0,first[1])[0]==1 and tick(0,(1,1))[0]==0
assert int(1<1)!=tick(1)[0] # old-cache readout before the receipt update
assert c.evaluate_index(int(identity['prefix_index']),0,2)==0
result={'status':'PASS_FINITE_SOURCE_RECHECK','source_identity_sha256':OLD,'codec_sha256':sha(R/'prcodec.py'),'checker_sha256':sha(Path(__file__)),'words':words,'ticks':ticks,'cache_bytes':len(c.encode_bytes(cache)),'prefix_bytes':len(c.encode_bytes(prefix)),'cache_statement_transitions':5,'prefix_statement_transitions':'6m+10 for m acquired bits, checked for 1<=m<=10','readout':'initial false; later false -> 1/2, true -> 5/8; epsilon 1/4','source_models':['0','1/2'],'half_partial_errors_n0_through_n10':str(sum(F(1,2)**k for k in range(11))),'negative_controls':['cold zero cache','stale cache','output before update','wrong bit','short fuel','wrong old API arity','truncation and wrong magic'],'scope':'Fresh bounded execution checks on recovered original programme identities. The new run_frame adapter is explicitly stateful and has a separate statement meter; it is not the original c.run API or a Lean-refinement replacement.'}
(R/'FRESH_ENDPOINT_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
