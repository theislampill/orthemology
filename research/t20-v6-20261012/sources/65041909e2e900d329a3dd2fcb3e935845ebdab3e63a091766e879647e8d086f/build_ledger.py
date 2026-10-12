#!/usr/bin/env python3
from pathlib import Path
import hashlib, json
from datetime import datetime, timezone
root=Path(__file__).resolve().parent
workspace=root.parent
pin='7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'

def record(path, scope, repo_path=None, expected=None):
    p=workspace/path
    b=p.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    r={'local_path':str(path),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob_sha_of_local_bytes':blob,'read_scope':scope}
    if repo_path:
        r['repository_pin']=pin
        r['url']=f'https://github.com/theislampill/orthemology/blob/{pin}/{repo_path}'
    if expected:
        r['expected_git_blob_sha_from_prior_source_binding']=expected
        r['matches_prior_binding']=blob==expected
        assert blob==expected
    return r
sources=[
record('tensor-moment-continuation-20261009/RESULT.md','Whole result, finite known-support N−1 closure, finite controlled observation equivalence, product/direct-sum and semantic limits.'),
record('state-dependent-gradient-obstruction-20261009/RESULT.md','Whole result, state-dependent Fisher fibre obstruction and exact finite tensor hierarchy.'),
record('constructive-t20-20261009/sources/theory/lineages/h-formalisation/orthing_formalisation_v1.md','Continuous lines100–200 and895–958: direct-sum finite actualisation and future-safe quotient criterion; additional targeted search for measure/computability references. Not a whole manuscript review.','theory/lineages/h-formalisation/orthing_formalisation_v1.md','c094a9c44fae26484426df67ac5afd9e2190eb4d'),
record('tensor-moment-continuation-20261009/H_CONTINUATION_SOURCE.md','Continuous lines210–320, finite instrument and Theorem2 proof; earlier state-law definition and Theorem1 also inspected. Whole bytes available; no whole-paper review claim.','theory/lineages/h-continuation/continuation_complete_orthing.md','99d0434aad8b8a841f59eb078e2b70c0b961d226'),
record('warranted-learning-20261009/sources/theory/lineages/h-ics-v5/information-composition-and-self-revision-v5.tex','Continuous lines43–63 and234–256, general information criterion and finite observation congruence; targeted measure/computability scope searches.','theory/lineages/h-ics-v5/information-composition-and-self-revision-v5.tex','7672f79a105b8b2d051eea1cd29ef4e0ffd6a595'),
record('user-checkpoints/extracted/P02/proofs/U05_MEASURE_CORE.md','All99 lines read continuously: M2-01 to M2-06, inherited ordinary measure core and original-claim disposition. Local checkpoint source, not assumed to be identical to a current repository file.'),
record('user-checkpoints/extracted/P02/proofs/CV_C_HIERARCHY.md','All115 lines read continuously: effective observer and point-concentration defect hierarchy. Does not establish moment determinacy or tilt dynamics.'),
record('measure-moment-continuation-boundary-20261009/sources/DEFECT_COMPUTABILITY.md','Whole pinned source text read from GitHub connector, stored verbatim. URL is pinned; local text SHA is recorded, but no independent expected raw Git blob verification is claimed.','experiments/orthemology-v5/mathematics/DEFECT_COMPUTABILITY.md'),
]
external=[
{'author':'Jordan Stoyanov','year':2004,'title':'Stieltjes classes for moment-indeterminate probability distributions','publisher_url':'https://www.cambridge.org/core/journals/journal-of-applied-probability/article/stieltjes-classes-for-momentindeterminate-probability-distributions/3D6EA0EEC47B46B3DDA05BA0DC709F83','inspected_full_text_url':'https://www.researchgate.net/publication/305974332_Stieltjes_classes_for_moment-indeterminate_probability_distributions','read_scope':'Author-uploaded paper, §2 bounded/exponential-moment determinacy, §3 Stieltjes family theorem, §5 standard-lognormal sine family and historical attribution; web-extracted lines236–522 and735–902. Publisher metadata independently inspected. No full-paper reading claim.','ownership':'The lognormal sine family and classical moment-determinacy facts are prior mathematics. Exact Gaussian derivation is reproduced independently in RESULT.md.','doi_disposition':'Publisher displays10.1239/jap/1082552205; author-uploaded record also lists10.1017/S0021900200112355. Use publisher URL as unambiguous locator.'},
{'author':'C. C. Heyde','year':1963,'title':'On a Property of the Lognormal Distribution','url':'https://academic.oup.com/jrsssb/article/25/2/392/7035281','doi':'10.1111/j.2517-6161.1963.tb00521.x','read_scope':'Publisher abstract and bibliographic metadata only; no full-proof inspection. General lognormal attribution corroborated by Stoyanov§5.','ownership':'Classical general lognormal moment indeterminacy, not a result invented by this packet.'},
{'author':'Zenghu Li','year':2019,'title':'Continuous-state branching processes with immigration','url':'https://arxiv.org/pdf/1901.03521','version':'arXiv1901.03521v1','read_scope':'§1 first theorem and continuous proof, printed page3/PDF page7; web lines73–93. Finite-measure Laplace uniqueness via multiplicative family and monotone class. No branching-process theorem imported.','ownership':'Classical finite-measure Laplace uniqueness; packet supplies an independent compactification proof.'},
{'author':'Christian Kleiber','year':2013,'title':'The generalized lognormal distribution and the Stieltjes moment problem','url':'https://arxiv.org/pdf/1301.1277','read_scope':'Targeted §3 moment/MGF boundary and §4 Stieltjes class definition. Used as corroboration, not as source of a new general-lognormal theorem or of the tilt application.','ownership':'Classical lognormal placement and heavy-tail scope.'},
]
ledger={'created_at_utc':datetime.now(timezone.utc).isoformat(),'status':'ordinary mathematical proof and exact symbolic controls; no formal-kernel or novelty certification','repository_pin':pin,'scope':'Additive noncompact transfer test. Protected inherited files read only. Scoped source ownership comparison, not repository-wide absence.','local_sources':sources,'external_primary_sources':external,'standard_classical_theorems_used':['Stone–Weierstrass polynomial density on compact subsets of finite-dimensional real space','Finite Borel measure uniqueness from continuous test functions on compact metric spaces','Dominated and monotone convergence','Gaussian Fourier transform','Holomorphic differentiation under a dominated integral and identity theorem'],'source_priority_conclusion':'Actual-update fibre congruence already belongs to inherited sources; classical moment indeterminacy and Laplace uniqueness belong to prior mathematics. The newly assembled deliverable is their application to this declared infinite moment hierarchy and the compact/noncompact continuation boundary.'}
(root/'SOURCE_LEDGER.json').write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+'\n')
print('PASS source ledger with',len(sources),'local bindings; three inherited Git blob bindings matched')
