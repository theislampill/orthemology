#!/usr/bin/env python3
"""Require the kernel to reject theorem/interface mutations, in disposable copies."""
import json,pathlib,subprocess,sys
root=pathlib.Path(__file__).resolve().parent.parent
out=pathlib.Path(sys.argv[1]);lean=sys.argv[2]
mutdir=out/'mutants';mutdir.mkdir(exist_ok=True)
mutations=[
('wrong_complement','CoveringPortfolio.lean','Disjoint P T ↔ T ⊆ Pᶜ','Disjoint P T ↔ T ⊆ P'),
('wrong_portfolio_card','CoveringPortfolio.lean','(complements F).card = F.card :=','(complements F).card = F.card + 1 :='),
('missing_opacity','OpaqueSearch.lean','¬Disjoint P.val T → observe T n P = failedReply n P','¬Disjoint P.val T → failedReply n P = failedReply n P'),
('strict_attempt_bound','OpaqueSearch.lean','coveringNumber α (Fintype.card α-q) k ≤ N := by','coveringNumber α (Fintype.card α-q) k < N := by'),
('zero_measure_allowed','RandomizedSearch.lean','[IsProbabilityMeasure μ]',''),
('one_too_small','CoveringPortfolio.lean','coveringNumber α k k = (Fintype.card α).choose k :=','coveringNumber α k k = (Fintype.card α).choose k - 1 :=')]
results=[]
for name,filename,old,new in mutations:
    source=(root/filename).read_text()
    if old not in source: raise SystemExit('Mutation no longer matches '+name)
    p=mutdir/(name+'.lean');p.write_text(source.replace(old,new,1))
    run=subprocess.run([lean,str(p)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (mutdir/(name+'.log')).write_text(run.stdout)
    if run.returncode==0 or 'error:' not in run.stdout:
        raise SystemExit('Mutation was not rejected: '+name)
    if name == 'missing_opacity' and ('application type mismatch' not in run.stdout or 'invalid field notation' in run.stdout):
        raise SystemExit('Opacity mutant did not reach the intended lost-information obligation')
    results.append({'mutation':name,'exit_code':run.returncode,'result':'rejected'})
(out/'MUTATION_RESULTS.json').write_text(json.dumps({'status':'PASS','mutations':results},indent=2)+'\n')
