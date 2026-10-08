#!/usr/bin/env python3
"""Independent boundary deletions in disposable full-action modules."""
import pathlib,subprocess,sys,json
source=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);lean=sys.argv[3]
out.mkdir(parents=True,exist_ok=True)
mutations=[
 ('full_action_opacity_deleted','OpaqueActions.lean',
  'observe T (history π failed n) (spine π failed n) =\n      failed (history π failed n) (spine π failed n)',
  'failed (history π failed n) (spine π failed n) =\n      failed (history π failed n) (spine π failed n)'),
 ('full_action_probability_deleted','OpaqueActions.lean','[IsProbabilityMeasure μ]',''),
 ('full_action_cover_cap_decreased','OpaqueActions.lean',
  'coveringNumber α (Fintype.card α-q) k ≤ N := by',
  'coveringNumber α (Fintype.card α-q) k < N := by'),
 ('nonce_reuse_upper','FullCommandInterface.lean',
  'else ⟨hne.choose, hne.choose_spec⟩, h.length, body⟩',
  'else ⟨hne.choose, hne.choose_spec⟩, 0, body⟩'),
 ('maximal_world_omitted','CoveringPortfolio.lean',
  '∀ T : Finset α, T.card = k → ∃ A ∈ G, T ⊆ A',
  '∀ T : Finset α, T.card < k → ∃ A ∈ G, T ⊆ A'),
 ('minimum_block_uniformity_deleted','CoveringPortfolio.lean',
  '∀ P ∈ F, P.card = q',
  '∀ P ∈ F, P.card ≤ q+1')]
r=[]
for name,fn,old,new in mutations:
 s=(source/fn).read_text()
 if s.count(old)!=1 and name not in {'full_action_probability_deleted','full_action_cover_cap_decreased'}: raise RuntimeError((name,s.count(old)))
 if old not in s: raise RuntimeError(name+' no match')
 p=out/(name+'.lean');p.write_text(s.replace(old,new,1))
 x=subprocess.run([lean,str(p)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 (out/(name+'.log')).write_text(x.stdout)
 if x.returncode==0 or 'error:' not in x.stdout: raise RuntimeError(name+' was not rejected')
 if 'unexpected token' in x.stdout or 'unknown namespace' in x.stdout: raise RuntimeError(name+' rejected at syntax/import boundary')
 r.append({'name':name,'exit_code':x.returncode,'result':'REJECTED','source_module':fn})
(out/'RESULTS.json').write_text(json.dumps({'status':'PASS','mutations':r},indent=2)+'\n')
print(json.dumps(r,indent=2))
