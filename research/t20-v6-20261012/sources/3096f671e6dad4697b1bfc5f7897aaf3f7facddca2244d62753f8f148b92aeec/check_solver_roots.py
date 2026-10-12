#!/usr/bin/env python3
"""Source-bound executable-root guard, with in-memory shortcut mutations.

This source inspection complements the definitionally checked Lean probes. It
does not establish asymptotic runtime or replace the refinement theorem.
"""
from pathlib import Path
import hashlib,json,re
base=Path(__file__).resolve().parents[1]/'source-snapshot'
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()

def definitions(text):
    text=re.sub(r'/\-[\s\S]*?\-/','',text)
    text=re.sub(r'--[^\n]*','',text)
    starts=list(re.finditer(r'(?m)^(?:noncomputable\s+)?(?:def|theorem|instance|namespace|end)\s+([^\s(:]+)',text))
    result={}
    for i,m in enumerate(starts):
        if re.match(r'(?:noncomputable\s+)?def\s',m.group(0)):
            result[m.group(1)]=text[m.start():starts[i+1].start() if i+1<len(starts) else len(text)]
    return result

files={n:(base/'src/dependencies'/(n+'.lean')).read_text() for n in ('SCCRegionAlgorithm','SCCParity','SCCPruning')}
expect={
    ('SCCRegionAlgorithm','winningRegion'):['computedRegion','B.card'],
    ('SCCRegionAlgorithm','computedRegion'):['regionStep','Necessity.descend'],
    ('SCCRegionAlgorithm','regionStep'):['SCCPruning.markovTarget','Necessity.regionAllowed'],
    ('SCCParity','markovTarget'):['targetStates','zeroExitPairs'],
    ('SCCParity','targetStates'):['parityOutput'],
    ('SCCParity','parityOutput'):['mecs','parityIterate'],
    ('SCCParity','parityIterate'):['parityStep'],
    ('SCCParity','parityStep'):['mecs','BadWithin'],
    ('SCCPruning','mecs'):['iterate','K.image','cluster'],
    ('SCCPruning','cluster'):['FiniteReachability.reachable'],
    ('SCCPruning','step'):['Keep'],
    ('SCCPruning','iterate'):['step'],
    ('SCCPruning','Keep'):['FiniteReachability.reachable']}
forbidden=['powerset','executableMEC','executableTarget','executableOutput','executableStep','markovTargetStates','Necessity.winningRegion','Necessity.computedRegion','Necessity.regionStep']
def audit(fs):
    parsed={n:definitions(t) for n,t in fs.items()}
    rows=[]
    for (file,name),needed in expect.items():
        body=parsed[file][name]
        assert all(x in body for x in needed),(name,'missing required executable call')
        assert not any(x in body for x in forbidden),(name,'forbidden exhaustive shortcut')
        rows.append({'file':file,'definition':name,'body_sha256':sha(body),'required_calls':needed})
    return rows
rows=audit(files)
mutations=[('stage-exhaustive-target','SCCRegionAlgorithm','SCCPruning.markovTarget','HiddenParity.markovTargetStates'),
    ('public-reference-alias','SCCRegionAlgorithm',':= computedRegion P menu priority B.card B',':= Necessity.computedRegion P menu priority B.card B'),
    ('target-exhaustive-output','SCCParity','(parityOutput source succ B row priority theta U).biUnion','(executableOutput source succ B row priority theta U).biUnion'),
    ('mec-powerset-shortcut','SCCPruning','K.image (fun a => cluster source succ K (source a))','U.powerset')]
rejected=[]
for label,file,old,new in mutations:
    assert old in files[file]
    altered=dict(files);altered[file]=files[file].replace(old,new,1)
    try:audit(altered)
    except AssertionError:rejected.append(label)
    else:raise AssertionError('mutation escaped guard: '+label)
print(json.dumps({'status':'PASS_SOURCE_ROOT_AND_MUTATION_GUARD','definitions_checked':len(rows),'roots':rows,'mutations_rejected':rejected,'scope':'Exact source-root inspection only; no asymptotic runtime, extraction or arbitrary parser-refinement claim'},indent=2,sort_keys=True))
