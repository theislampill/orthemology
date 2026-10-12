#!/usr/bin/env python3
from pathlib import Path
import importlib.util,sys,random,json,hashlib
root=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('prcodec',root/'recovered/prcodec.py'); c=importlib.util.module_from_spec(spec);sys.modules[spec.name]=c;spec.loader.exec_module(c)
rng=random.Random(20260930)
def le(e):
 if e[0]=='c':return f'(.constant {e[1]})'
 if e[0]=='v':return f'(.reg {e[1]})'
 return '(.'+e[0]+' '+' '.join(map(le,e[1:]))+')'
def ls(s):
 k=s[0]
 if k=='set':return f'(.set {s[1]} {le(s[2])})'
 if k=='seq':
  if len(s)==1:return '.skip'
  if len(s)!=3:raise ValueError('binary generated serializer expected')
  return f'(.seq {ls(s[1])} {ls(s[2])})'
 if k=='loop':return f'(.loop {s[1]} {le(s[2])} {ls(s[3])})'
 if k=='if':return f'(.branch {le(s[1])} {ls(s[2])} {ls(s[3])})'
def ge(d):
 if d==0:return (rng.choice(['c','v']),rng.randrange(5))
 op=rng.choice(['add','sub','mul','div','mod','le','eq','pow2','c','v'])
 if op in ['c','v']:return (op,rng.randrange(5))
 if op=='pow2':return ('pow2',('mod',ge(d-1),('c',4)))
 return (op,ge(d-1),ge(d-1))
def gs(d):
 if d==0:return ('set',rng.randrange(5),ge(2))
 k=rng.choice(['set','seq','loop','if'])
 if k=='set':return ('set',rng.randrange(5),ge(2))
 if k=='seq':return ('seq',gs(d-1),gs(d-1))
 if k=='loop':return ('loop',rng.randrange(5),('mod',ge(1),('c',4)),gs(d-1))
 return ('if',ge(1),gs(d-1),gs(d-1))
programs=[c.Program(2,2,('set',2,(op,('v',0),('v',1)))) for op in ['add','sub','mul','div','mod','le','eq']]
programs += [c.Program(2,2,('set',2,('pow2',('mod',('v',0),('c',4))))),c.Program(2,7,('seq',)),c.Program(2,0,('seq',))]
programs += [c.Program(2,2,('seq',('set',2,('c',1)),('loop',0,('v',0),('set',2,('add',('v',2),('v',0)))))),c.Program(2,2,('loop',2,('c',3),('set',2,('add',('v',2),('c',7)))))]
programs += [c.Program(2,rng.randrange(5),gs(3)) for _ in range(68)]
programs += [c.Program(1,0,('set',0,('c',1))),c.Program(0,0,('set',0,('c',1)))]
inputs=[(0,0),(1,2),(9,2),(4,21)]
checks=[];records=[]
for i,p in enumerate(programs):
 bp=list(c.encode_bytes(p));idx=c.encode(p);lp=f'(PackedProgram.mk {p.arity} {p.output} {ls(p.body)})'
 checks += [(f'bytes-{i}',f'encodeBytes {lp} == {bp}'),(f'index-{i}',f'programIndex {lp} == {idx}'),(f'roundtrip-{i}',f'decodeIndex {idx} == some {lp}')]
 vals=[]
 for n,w in inputs:
  expected=c.evaluate_index(idx,n,w,step_limit=None,max_bits=None);vals.append(expected)
  checks.append((f'eval-{i}-{n}-{w}',f'evaluateIndex {idx} {n} {w} == {expected}'))
 records.append({'program':p.__dict__,'bytes':bp,'index':str(idx),'values':vals})
base=list(c.MAGIC)
invalid=[[],[80,48,50,76,2,2,2,17,0],base+[128,0,2,17,0],base+[2,2,16,2,1,128],base+[2,2,20],base+[2,2,17,2,17,0],base+[2,2,17,0,0],base+[2,2,16,2,11],base+[2,2,17,255,127]]
for i,b in enumerate(invalid):
 assert c.decode_bytes(bytes(b)) is None
 checks.append((f'invalid-bytes-{i}',f'decodeBytes {b} == none'))
for i,n in enumerate([0,2,255,256,257,512,65535,65536]):
 assert c.decode(n) is None
 checks.append((f'invalid-index-{i}',f'decodeIndex {n} == none'))
# A legitimate one-child Seq is lowered to its child: semantic, not byte identity.
seqp=c.Program(2,2,c.Seq(c.Set(2,c.C(1))))
seqb=list(c.encode_bytes(seqp)); normalized='(PackedProgram.mk 2 2 (.set 2 (.constant 1)))'
assert c.decode_bytes(bytes(seqb))==seqp
checks.append(('sequence-one-normalization',f'decodeBytes {seqb} == some {normalized}'))
checks.append(('sequence-one-not-reserialized-identically',f'encodeBytes {normalized} != {seqb}'))
# Differential parser mutation cases include accepted non-binary Seq trees.
def normalize(s):
 k=s[0]
 if k=='seq':
  ss=[normalize(x) for x in s[1:]]
  if not ss:return ('seq',)
  out=ss[-1]
  for x in reversed(ss[:-1]):out=('seq',x,out)
  return out
 if k=='loop':return (k,s[1],s[2],normalize(s[3]))
 if k=='if':return (k,s[1],normalize(s[2]),normalize(s[3]))
 return s
mutations=[]
for i in range(160):
 p=programs[rng.randrange(20)]; b=list(c.encode_bytes(p)); kind=i%4
 if kind==0:b=b[:rng.randrange(len(b)+1)]
 elif kind==1:b.append(rng.randrange(256))
 elif kind==2:b[rng.randrange(len(b))]=rng.randrange(256)
 else:b.insert(rng.randrange(len(b)+1),rng.randrange(256))
 q=c.decode_bytes(bytes(b))
 expected='none' if q is None else f'some (PackedProgram.mk {q.arity} {q.output} {ls(normalize(q.body))})'
 checks.append((f'parser-mutation-{i}',f'decodeBytes {b} == {expected}'))
 mutations.append({'bytes':b,'accepted':q is not None})
for ar in range(5):
 p=c.Program(2,2,c.Seq(*(c.Set(2,c.C(j)) for j in range(ar))))
 b=list(c.encode_bytes(p));q=normalize(p.body)
 checks.append((f'variadic-seq-{ar}',f'decodeBytes {b} == some (PackedProgram.mk 2 2 {ls(q)})'))
resource={}
for label,kwargs in [('steps',{'step_limit':0}),('bits',{'max_bits':1})]:
 try:c.evaluate_index(c.encode(c.Program(2,2,c.Set(2,c.C(128)))),0,1,**kwargs)
 except c.ResourceLimit as ex:resource[label]={'exception':type(ex).__name__,'message':str(ex)}
 else:raise AssertionError('resource exhaustion returned a semantic value')
text='import CodecIndexPrimrec\nimport Pi3IndexReduction\nopen P02.Codec P02A2.ObserverCore\nset_option maxRecDepth 100000\nset_option maxHeartbeats 8000000\n'
text += 'def main : IO Unit := do\n'
for label,expr in checks:text+='  unless ('+expr+').toBool do throw (IO.userError "'+label+'")\n' if False else '  unless ('+expr+') do throw (IO.userError "'+label+'")\n'
text+=f'  IO.println "PASS {len(checks)} differential checks ({len(programs)} generated programs)"\n'
(root/'Differential.lean').write_text(text)
(root/'DIFFERENTIAL_VECTORS.json').write_text(json.dumps({'seed':20260930,'source_sha256':hashlib.sha256((root/'recovered/prcodec.py').read_bytes()).hexdigest(),'programs':records,'inputs':inputs,'invalid_bytes':invalid,'mutations':mutations,'checks':len(checks),'program_count':len(programs),'resource_exhaustion':resource},indent=2)+'\n')
print(len(checks),len(programs),resource)
