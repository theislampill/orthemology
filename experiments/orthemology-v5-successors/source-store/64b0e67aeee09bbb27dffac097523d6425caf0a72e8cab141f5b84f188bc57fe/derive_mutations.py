#!/usr/bin/env python3
"""Derive bounded executable fault probes from frozen production definitions; no theorem edits."""
from pathlib import Path
import hashlib,json
r=Path(__file__).resolve().parent;out=r/'mutations';out.mkdir(exist_ok=True)
rows=[]
def save(name,text,source,anchor,replacement):
 p=out/(name+'.lean');p.write_text(text)
 rows.append({'module':name,'source':source,'source_sha256':hashlib.sha256((r/source).read_bytes()).hexdigest(),'anchor':anchor,'replacement':replacement,'mutant_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'expected_exit':1,'expected_diagnostic':'did not evaluate to'})
# Compiler-level submitted witness suppression, retaining the exact original checker gate.
s=(r/'src/DirectEndpoint.lean').read_text();s=s[:s.index('theorem compiled_measurable')]
s=s.replace('namespace OrthemicCertificate.Direct','namespace OrthemicCertificate.DirectWitnessIgnored\nopen OrthemicCertificate.Direct')
a='(submittedFamily c)';assert s.count(a)==1;s=s.replace(a,'(submittedFamily [])')
s+='''\ndef checkedAction {q n k : ℕ} (I : Input q n k) (B : Support q) (s : Fin n)
    (c : Body q n k) (h : List (Fin k × Fin n)) : Option (Fin k) :=
  if hc : check I c B s = true then some (compile I ((check_iff I c B s).mp hc).1.1 B s c () h)
  else none
end OrthemicCertificate.DirectWitnessIgnored
open OrthemicCertificate.Fixtures
#guard OrthemicCertificate.DirectWitnessIgnored.checkedAction choices {0} 1 [choicesNode 2 1] [] = some 1
'''
s='import NativeControllerControls\n'+s
save('WitnessIgnored',s,'src/DirectEndpoint.lean',a,'(submittedFamily [])')
# Counter mutation in the actual generated policy body. Keep all other causal definitions.
s=(r/'src/DirectController.lean').read_text();s=s[:s.index('theorem generatedPhasePolicy_measurable')]
s=s.replace('namespace OrthemicCertificate.Direct','namespace OrthemicCertificate.DirectCounterReset\nopen OrthemicCertificate.Direct')
a='(historyVisits s₀ s h)';assert s.count(a)==1;s=s.replace(a,'0')
for helper in ['cycleAction','stageTargets','chooseTarget','stageActions']:
 s=s.replace(helper,'OrthemicCertificate.Direct.'+helper)
s+='''\ndef checkedAction {q n k : ℕ} (I : Input q n k) (B : Support q) (s : Fin n)
    (c : Body q n k) (h : List (Fin k × Fin n)) : Option (Fin k) :=
  if hc : check I c B s = true then
    let hI := ((check_iff I c B s).mp hc).1.1
    letI : NeZero n := ⟨Nat.ne_of_gt hI.1.2.1⟩
    some (generatedPhasePolicy (I.kernel hI) I.menu I.priority (submittedFamily c) B s
      ⟨0,hI.1.1⟩ ⟨0,hI.1.2.2.1⟩ (rationalReject I (tolerance I B)) () h)
  else none
end OrthemicCertificate.DirectCounterReset
open OrthemicCertificate.Fixtures
#guard OrthemicCertificate.DirectCounterReset.checkedAction choices {0} 1 [fairNode] [(0,1)] = some 1
'''
s='import NativeControllerControls\n'+s
save('CounterReset',s,'src/DirectController.lean',a,'0')
# The exact rational runtime definitions, with one altered guard/statistic each.
base=(r/'src/RationalTest.lean').read_text();base=base[:base.index('@[simp] theorem rationalReject_iff')]
for name,ns,anchor,repl,control in [
 ('NonStrictCountGuard','DirectNonStrict','r < actionCount e h','r ≤ actionCount e h', '#guard !(rationalReject latent (1/6) 0 0 [])'),
 ('EmpiricalHistoryTruncated','DirectTruncated','rationalFrequency e y h - I.row','rationalFrequency e y (h.take 1) - I.row','#guard !(rationalReject latent (1/6) 0 0 [((0,0),1),((0,0),0),((0,0),0)])')]:
 s=base.replace('namespace OrthemicCertificate.Direct','namespace OrthemicCertificate.'+ns)
 assert s.count(anchor)==1;s=s.replace(anchor,repl)
 s='import NativeControllerControls\n'+s+'\nopen OrthemicCertificate.Fixtures\n'+control+'\nend OrthemicCertificate.'+ns+'\n'
 save(name,s,'src/RationalTest.lean',anchor,repl)
(out/'DERIVATION.json').write_text(json.dumps(rows,indent=2)+'\n')
