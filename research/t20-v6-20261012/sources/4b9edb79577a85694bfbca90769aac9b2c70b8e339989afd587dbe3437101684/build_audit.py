import json,hashlib,pathlib,re
P=pathlib.Path('t20-closure-audit-20261011/early_mathematics'); C=pathlib.Path('t20-consolidation-20261011/catalogue/objects'); V=pathlib.Path('deliverables/t20-v4-sealed/package'); B=P.parent/'pinned-baseline'
sm=json.load(open(B/'SOURCE_MAP.json'))['sources']; reg=json.load(open(B/'registry.json'))['results']
# Human-read scopes, not full-body or replay credit inferred from file custody.
held=[
('H_FORMALISATION','cd5070341a46658c0e4ac2c077d343d276cf16e50f0305f61ebb90ba0b624c2e',[[107,199],[333,504]],'Typed direct-sum algebra, contractions, obligation history and inquiry-value distinctions.'),
('H_CONTINUATION','626504b64c2d7817b882e74992ba989d83c7ef8e67b1467b537101c2b804edb9',[[136,368],[434,477],[611,672]],'Exact minimax defect, predictive-span theorem, sharp Walsh horizon spectrum, augmentation and conditional margins.'),
('CIRS','bd83f4c2bb1a41151405872a6aa57fe9bdc352f0b63db4cfb302e0068c8b0d4a',[[1,45]],'Model and iff with initial constructive-policy proof; not entire necessity proof reread.'),
('CORRELATED_RESTORATION','7163cb536782ccb8a91a10be4b91cdcc1113bbab3c467d6ac66dee0d59cb0caf',[[1,130]],'Hall exact coupling, constrained licensing, conditional Borel–Cantelli and hidden-event filtration.'),
('U05_MEASURE_CORE','33ba053c3113b297c5dbf72e28333386163ead926713a91a0e578245ae042cfe',[[1,99999]],'Whole ordinary M2-01–06 body; archive ancestry, not an exact public registry source identity.'),
('CV_R','887dac94aa4585444be7243725cd3db1e801c92bd70d5bf30a5e0890633e0e31',[[1,99999]],'Whole ordinary R2-01–07 body; actual formal descendant independently matched below.'),
('CV_C_HIERARCHY','cb9a698d4e0e9e0162aec3709bfdfdaebaf19a9bc19b9350f386e6d11709926d',[[1,110]],'Ordinary hierarchy compiler and finite Mealy proof; original report lineage, not all formal descendants.'),
('DEFECT_COMPUTABILITY','74333fb0f8232c6d91c0b8e6f8f15ad6d68a515d429bd044387c647d92689ee2',[[1,90]],'Effective observer domain, atom-mass formula and threshold summary.'),
('MEASURE_RESULTS','e22bd40d8726103e1d689c9487213c90de80905b9f52e0cad80f5c5f2447bba2',[[1,99999]],'Whole retained summary, with actual selected Lean endpoints inspected separately.'),
('GLOBAL_PARITY','4a93ef96999718cc4fc6ac566da899c6f9938d5a8cbce269d8ee20a3f459d9a3',[[1,99999]],'Full GlobalParitySufficiency.lean endpoint file; dependency source closure not replayed.'),
('MEALY_SOLVER','f037c56ca783feffbafc6d5643b5356e321cc388e0ade5baec961d62d43655b6',[[89,173]],'Executable rational matrix/Cramer solver and actual-law endpoint proof.'),
('ATOM_ENUMERATION','15a335e36b8d4a5b42c998b9b6999f2001cd13c840bc588b2a5b2f7bbd61f032',[[1,99999]],'Complete finite-word candidate/mass positive-atom theorem.'),
('TOTAL_VARIATION','7289c2117d990a40d53ab43925cebac082b15464d854a670968aa1e6dccb8fbf',[[1,99999]],'Actual defect is one-Lipschitz in whole-law event TV.'),
('RESIDUAL_STABILITY','41bfe7bba72a6f1e03195209bd6015b0f04756383f870a453ae60631b5678f6c',[[62,111]],'Actual law-dependent residual controlled by a common measurable event.'),
('OBSERVATION_IDENTITY','f74a3d14879ac7900f60e3460e75565c0d0c4f8649bd701de92ec8a9b86da08e',[[145,177]],'Exact formal full-observation identity retains infinite residual.'),
('SMOOTH_SCORE_RIGIDITY','3d1c584a1b91f4d0190605cd73d1cba8ae3bf631e461865de301b4711928d9be',[[1,50],[57,150]],'Forecast-second common repair S1/S2, sharp binary exception and three-state obstruction.')]
bind=[]
for label,h,scope,note in held:
 p=C/h[:2]/h; data=p.read_bytes(); assert hashlib.sha256(data).hexdigest()==h
 n=len(data.decode().splitlines()); scope=[[a,min(b,n)] for a,b in scope]
 ss=[s for s in sm if h in (s.get('sha256'),s.get('original_sha256'))]
 ids={s['id'] for s in ss}
 bind.append(dict(label=label,path=str(p),sha256=h,read_scope=scope,note=note,registry_source_ids=sorted(ids),registry_families=[r['id'] for r in reg if set(r['source_ids'])&ids],identity_matches=ss,no_new_replay=True))
for m in json.load(open(P/'FETCH_METADATA.json')):
 p=P/'sources'/m['name']; data=p.read_bytes(); h=hashlib.sha256(data).hexdigest(); g=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(); assert g==m['sha']
 ss=[s for s in sm if s.get('sha256')==h]; assert ss
 # ActualExponential first prefix proof was scoped; other fetched reports explicitly read in full or sections below.
 scope=[[113,198]] if m['name']=='ActualExponentialMoments.lean' else [[1,len(data.decode().splitlines())]]
 if m['name']=='TWO_COIN_MINIMAX_REPORT.md':scope=[[31,120]]
 ids={s['id'] for s in ss}
 bind.append(dict(label=m['name'],path=str(p),sha256=h,git_blob=g,source_url=m['display_url'],read_scope=scope,registry_source_ids=sorted(ids),registry_families=[r['id'] for r in reg if set(r['source_ids'])&ids],identity_matches=ss,no_new_replay=True))
json.dump({'baseline':'7efc6217c090b92d65f2c4cb8b011c18eb96bf7c','bindings':bind},open(P/'SOURCE_BINDINGS.json','w'),indent=2)
# Scoped reader-content search excludes code/custody archives deliberately; absence below is not source loss.
reader=[V/'geometry/GEOMETRY_MOMENTS_SYNTHESIS.md',V/'geometry/GEOMETRY_MOMENTS_CLAIMS.json',V/'proofs/PROOF_TYPE_INQUIRY_SYNTHESIS.md',V/'proofs/PROOF_TYPE_INQUIRY_CLAIMS.json',V/'evidence/EVIDENCE_TRANSPORT_SYNTHESIS.md',V/'evidence/MATERIAL_CLAIMS.json',V/'coverage/CUMULATIVE_PROGRAMME_CROSSWALK.md']
terms=['Mealy','extinction','small-cell','full smooth jet','continuum standards','two-coin','inverse moments','nonconvexity','common exponential','H-Continuation','inquiry landscape','no-disappearance']
search=[]
for p in reader:
 lines=p.read_text().splitlines();search.append(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),terms={t:[{'line':i,'text':l} for i,l in enumerate(lines,1) if t.lower() in l.lower()] for t in terms}))
json.dump({'scope':'Seven top-level mathematical reader chapters/registers/crosswalk; no source-loss inference from absence.','results':search},open(P/'V4_READER_SEARCH.json','w'),indent=2)
# Per-family status is source-depth-sensitive. No sibling source or same-suite ownership creates whole-row credit.
rows={
'T1-P02':('selected_source_directly_examined','partly_cross_contributed; measure-history branch reference_only',['OBSERVATION_IDENTITY','TOTAL_VARIATION','RESIDUAL_STABILITY'],'PT-23–29 carries atomic-defect compiler; missing explicit infinite residual J, full pattern/TV stability in reader synthesis.'),
'T1-MEALY':('selected_source_directly_examined','indexed_preserved_not_reader_reconciled',['MEALY_SOLVER','ATOM_ENUMERATION'],'Exact finite-state rational solver and positive-atom enumeration are distinct positive counterweight to general observer undecidability.'),
'T1-COMPUTABLE':('ordinary_ancestor_directly_examined','directly_cross_contributed_at_selected_endpoint',['CV_C_HIERARCHY','DEFECT_COMPUTABILITY'],'PT-23–29 preserves ordinary classification and subsequent literal refinement; no fresh whole numeric-source proof audit.'),
'T2-GEOMETRY':('selected_source_directly_examined','partial_ancestry_not_equivalent_successor',['SMOOTH_SCORE_RIGIDITY'],'Forecast-second, all-state common repair S2 for n>=3 is not GEO-03 first-argument simplex normalization.'),
'T2-INFORMATION':('selected_source_directly_examined','indexed_preserved_not_reader_reconciled',['STATISTICAL_REPAIR_BRIDGE.md'],'Exact unknown-score repair local-minimax lower bound counts fresh probes, not copied evidence; ET root discipline is compatible but not an equivalent theorem.'),
'T2-RESTORATION':('selected_source_scoped_read','crosswalk_substantively_summarized_not_subsumed',['CIRS'],'Crosswalk §4 preserves self-verifying supports. PT-21 exact stopping has a different target; keep positive coBuchi result separately.'),
'T2-COUNTABILITY':('selected_source_directly_examined','indexed_preserved_not_reader_reconciled',['CONTINUUM_RESTORATION_OBSTRUCTION.md'],'Positive eventual successful continuum standards are countable under finite-query domination and shrinking repair demand; sharp tolerance and blind-guess exception retained.'),
'T3-GEOMETRY':('selected_source_directly_examined','indexed_preserved_related_counterpart_not_equivalent',['FULL_JET_REPAIR_BOUNDARY.md'],'Exact common repair differs despite same full smooth jets; MOM-10 Fisher endpoint jet pair is related but different target/domain.'),
'T5-GLOBAL':('endpoint_source_directly_examined','crosswalk_summary_reference_only',['GLOBAL_PARITY'],'Finite rational observed-state minimum-even parity iff and arbitrary-seed deterministic-witness existence; PT-21 explicitly does not subsume it.'),
'T5-BENCHMARK':('independent_review_body_directly_examined','indexed_preserved_not_reader_reconciled',['TWO_COIN_MINIMAX_REPORT.md'],'Exact ordinary mistake minimax 1/(8 delta²)-1/2 post-acquisition and +1/2 initial-inclusive; not finite-state and not a gap-weighted regret objective.'),
'T6-NONCONVEX':('ordinary_owner_directly_examined','indexed_preserved_not_reader_reconciled',['NONCONVEXITY_THEOREM.md'],'Two infinite priors individually finite-budget; every proper mixture universally infinite budget under common information contract; not ET-16 geometric hull nonconvexity.'),
'S6F-19':('successor_scope_and_endpoint_dependency_read','crosswalk_summary_reference_only',['SIXTH_COMPOSITION_SCOPE.md','ActualExponentialMoments.lean'],'Actual chronological composition is not rederived here; scope document states complete-history weighted-product mechanism rather than independent durations.'),
'S6F-20':('actual_endpoint_source_directly_examined','crosswalk_summary_reference_only',['ActualExponentialMoments.lean','SIXTH_COMPOSITION_SCOPE.md'],'Full exponential integrand transported through action-law equality, plus explicit a.e. finite badCount; no physical-time result.'),
'S6F-21':('complete_endpoint_source_directly_examined','crosswalk_summary_reference_only',['FiniteModelExponentialUniformity.lean','SIXTH_COMMON_RANGE_README.md'],'Same policy/tolerance before true model; finite min positive rate and finite max integral, one fixed finite family; no arbitrary-instance uniformity.')}
other=['T4-PRIOR','T5-SCC','T5-CONTINUATION','T5-SPARSE','T5-SPARSE-EXAMPLE','T5-ENDPOINT','T5-ATOMS','T5-TRANSPORT','T6-COST','T6-CONCENTRATION','T6-WIDTH','T6-RATIONAL','T6-LOSS','T6-ROTOR','T6-HISTORY','T6-MOMENTS','T6-INTEGER','S6F-23','S6F-24','S6F-25']
for rid in other:rows[rid]=('registry_and_source_identity_only','indexed_preserved_reference_only',[],'No fresh source-body appraisal for this individual family. Read exact claim/limit and mapped source identities; do not propagate neighbor inspection or replay credit.')
out=[]
for r in reg:
 if r['id'] not in rows:continue
 depth,disp,src,note=rows[r['id']]
 out.append(dict(id=r['id'],title=r['title'],inherited_claim=r['claim'],inherited_limit=r['limit'],audit_depth=depth,v4_disposition=disp,examined_source_labels=src,conclusion=note,exact_source_ids=r['source_ids'],review_source_ids=r['review_source_ids'],new_proof=False,new_kernel_replay=False))
extra=[
 dict(id='H-TYPED-TENSOR',audit_depth='selected_source_directly_examined',v4_disposition='directly_examined_and_cross_contributed',sources=['H_FORMALISATION'],mapping='GEO-01/02 reconstruct exact finite typed support, fibre condition, parity and contraction boundary; no gap in those selected claims.'),
 dict(id='H-CONTINUATION',audit_depth='selected_source_directly_examined',v4_disposition='partly_cross_contributed_partly_crosswalk_only',sources=['H_CONTINUATION'],mapping='ET-05A exact invariant predictive quotient and ET-07 policy weights faithfully apply Theorem 2. Exact defect and augmentation summarized in crosswalk; Theorem 3 sharp Walsh horizon formula not developed in reader.'),
 dict(id='H-INQUIRY-OPTIONS',audit_depth='selected_source_directly_examined',v4_disposition='crosswalk_summary_only',sources=['H_FORMALISATION','H_CONTINUATION'],mapping='Correct-result closure versus future feasible options/value and historical ecology versus objective/certifiable landscape remain independent from PT-01 proof prices and ET-17 fixed-model risk.'),
 dict(id='H-CORRELATED-RESTORATION',audit_depth='selected_source_directly_examined',v4_disposition='crosswalk_substantively_summarized_not_subsumed',sources=['CORRELATED_RESTORATION'],mapping='Hall deficit under joint availability, licensed/incentive polytopes, adapted-event summability; no generic greedy dynamic optimality or public-certificate-to-physical restoration transfer.')]
json.dump({'scope':'34 selected early registry families plus four separate H lineages; not all T1–6 or 68 rows. Individual-depth classification.','families':out,'separate_lineages':extra,'summary':{'registry_rows':len(out),'body_inspected_rows':sum(bool(r['examined_source_labels']) for r in out),'identity_only_rows':sum(not r['examined_source_labels'] for r in out),'new_proofs':0,'new_kernel_replays':0}},open(P/'COVERAGE.json','w'),indent=2)
print('bindings',len(bind),'registry rows',len(out),'body-scoped rows',sum(bool(r['examined_source_labels']) for r in out))
