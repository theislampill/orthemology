from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parents[2];D=W/'t20-depth-reassessment-20261011';P=W/'t20-consolidation-20261011/projection/package-v4';V=P.with_name('package-v3')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(rel,x):
 p=P/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(x if isinstance(x,str) else json.dumps(x,indent=2,ensure_ascii=False)+'\n')
status='V4 COMPLETE RESEARCH HANDOFF; OWNER ACCEPTANCE PENDING'
put('CURRENT_STATUS.json',{'status':status,'programme':'T20','historical_tranche_cutoff_utc':'2026-10-11T11:32:55Z','current_research_scope':'Authorised 11 October 2026 T20 depth research through the final candidate seal; the historical tranche cutoff does not exclude these dated successor results from T20.','owner_acceptance':'pending','integration_authority':False,'T21_started':False,'historical_six_hour_compliance':'unverified','R3':'Reported second-order successor remains artifact-unavailable; overlap and within-T20 priority unknown.','repository_commit':'7efc6217c090b92d65f2c4cb8b011c18eb96bf7c','repository_tree':'906b592fb2591ed918c5f0caf485ef79dca513ab','readback':'depth/FINAL_BASELINE_READBACK.json'})
put('EDITION_V4.md','''# The integrated T20 successor edition

This v4 reader contains the complete v3 scientific payload and separately dated 11 October T20 successor research. The 11:32:55 UTC cutoff identifies the original frozen consolidation snapshot within T20. It is not the end of T20 research: the authorised depth work belongs to T20 through this edition's final seal. CURRENT_STATUS.json and the final seal control delivery status. T21 has not started. Owner acceptance, scientific closure and repository adoption are separate decisions.

## What the successor adds

1. Whole moving-state correction: a concrete second-order grouped update preserves positive represented laws, energy descent and the exact admitted audit square. This joins inherited geometry, reciprocal Taylor reweighting and classical discrete gradients; local solving, regularity, compact-interior and invariant algorithm-choice guards are essential. Reported unrecovered R3 may overlap; priority is unknown.
2. Semantic geometry: the actual inherited singular Gaussian correction preserves each member of a fixed uncountable conull repertoire while its measurable conjunction loses probability one. This is an exact mathematical application with domination/TV repair conditions, not a claim that human warrant equals probability one.
3. Proof and inquiry: a source-executed counterexample separates static proof cost from reuse of paid immutable checks. Exact-state cache macros give a bounded attained remaining-cost optimum. Dependency profiles, passive-check postponement and finite-memory CIRS boundaries keep their distinct hypotheses and inherited source interfaces.
4. Uncertainty and representation: exact four-trial calibration and exchangeability bodies lead to different conditioned minimax plans. Conversely one observation can saturate the ex ante minimax objective under the stated moment contract. Preserving all six per-model policy losses needs two continuous coordinates, while one fixed certified robust answer can be constant. Finite typed source lookup and rational joint-law transport retain their original owners.
5. Grounding: one common original provider does not erase the actual intermediary identities needed to compose secondary explanations. Exact endpoint lifts, downstream profiles and witness compatibility are different obligations; the finite routing-rank example counts mediation distinctions, not original sources.
6. Collective and effective continuation: the real T15 model pair supplies a conditional adaptive answer-law nonidentification proof, an exact linked-signal inquiry value and a recalibration/double-counting contrast. T16 distinguishes convergent finite recomputation from a computable committed infinite lineage; a pruned enumerable continuation region supplies the constructive repair under its stated promises.
7. Occurrence and source warrant: the actual seven-record T16 fixture needs sidecar alphabets 1, 2 or 3 for three declared record-view contracts. The separate source return preserves original permission, mistaken mediation and qualified inquiry duty without equating missing knowledge with missing opportunity. These are a bounded inherited-theorem application and a source-owned coverage refinement, not a new general warrant theorem.

The detailed integrated chapter is depth/cross_front_synthesis/RESULT.md. Its typed graph is depth/cross_front_synthesis/EDGES.json. Current reviews qualify their exact reports; stale author-freeze “pending” headings remain historical. The graph review covers only the final bytes it binds. The source-specific collective/occurrence reviews and the refreshed combined-graph delta review are included at those exact final identities.

## Preserved evidence levels

Original scientific sources and executable modules remain exact. Original locator registries that expose private custody are projected with separate original/public hashes, and selected executable targets receive actual portable fixtures. Historical source receipts stay historical. Fresh v4 replays are confined to DEPTH_REPLAY_VERIFICATION.json; no inherited mode, check count, copied file or inventory item is credited as another scientific achievement. No fresh Lean build, primary Arabic authentication, new empirical cohort, human specialist review, historical research-duration certification or repository-wide validation is asserted.

The inherited affirmative foundational judgement remains affirmative at its actual-field scope: warranted provisional common original-source appraisal, same-bearer necessity, essential independence, source-owned veracity and cumulative grounds. New mathematical examples neither replace those arguments nor silently enlarge them to every idle/disconnected original. The historical expected-publicity objection retains its own target.
''')
put('README_FIRST.md','''# Read first: complete T20 v4 research handoff

Read CURRENT_STATUS.json for the delivery state and EDITION_V4.md for the concise result. This is one integrated successor candidate, preserving v3's scientific content and all earlier source-owned results. The original 11:32:55 UTC snapshot and the later authorised 11 October depth results are both T20. T21 has not started; no repository adoption is claimed.

## Scientific route

1. EDITION_V4.md: substantive new results, ownership and limits.
2. depth/cross_front_synthesis/RESULT.md: the integrated mathematical/foundational argument.
3. depth/cross_front_synthesis/EDGES.json: typed implications, applications, shared ancestry, failed mappings and conditional interpretations.
4. MATHEMATICAL_SYNTHESIS.md, FOUNDATIONAL_CROSSWALK.md and coverage/CUMULATIVE_PROGRAMME_CROSSWALK.md: retained cumulative programme and original twelve avenues.
5. The source-specific RESULT.md and REVIEW.md files under depth/, with depth/REVIEW_CURRENTNESS.json controlling the reviewed byte identities.
6. CLAIM_REGISTER.json and DEPENDENCY_INDEX.json: navigation to inherited and successor source-owned claims. No universal master theorem is implied.

For efficient mechanical handling use CODEX_START_HERE.md. A reader-only integration is not an instruction to reread, re-prove or rerun every inherited proof family. Portable selected execution is bounded by REPLAY_SCOPE.json; original and public identities are distinguished in PUBLIC_PROJECTION.json and depth/LOCATOR_TRANSFORMATIONS.json.

R3 remains reported/artifact-unavailable, including unknown overlap with the present second-order construction. Historical six-hour compliance remains unverified. Primary research appraisals retain their owners and declared reading scope; source inventory is not deep-reading evidence. Private owner instructions, operational notes, raw transfer logs and bulk corpora are not republished.
''')
put('T21_CHARTER.md','''# T21 continuation charter: proposed, not initiated

T21 has not started. The original 11:32:55 UTC frozen T20 tranche is followed by authorised 11 October depth research, all within T20 through the final v4 seal. Completion of this bounded handoff does not claim that every mathematical, empirical or philosophical frontier has been exhausted. The owner decides whether to accept the integrated T20 stopping point and separately authorise any next programme.

The original charter is preserved verbatim at depth/inherited-v3/T21_CHARTER.md. Its proposed directions remain historical proposals, qualified by the successor results. Do not reopen an already settled local result simply because a general theory is incomplete.

## If a next programme is authorised

Choose a concrete remaining obligation and its source-bound input, rather than a generic request for more synthesis:

- Recover actual R3 proof/code bytes before deciding overlap or within-programme priority.
- Supply validated solver bounds/arithmetic for a particular intended numerical implementation; the local whole-state proof already exists.
- Specify the semantic query and admissible correction operations before claiming future-event preservation.
- Supply a real changed policy/horizon/observation contract before enlarging the finite uncertainty or source-sidecar model.
- For literal controller execution, establish the particular source/host/probability bridge rather than confusing finite program text with finite memory.
- For testimony or practical obligation, supply warranted actual attribution, content, basing and opportunity premises; formal bookkeeping cannot create them.

Each continuation should state its completion test, evidence level and boundaries. Repository integration, PR creation and adoption require their own explicit authority. None is granted by this document.
''')
put('CONSOLIDATION_CONTRACT.md','''# Integrated T20 handoff contract

Scope: preserve all v3 scientific source/result/delta bytes and incorporate the separately dated authorised T20 depth packets through final v4 sealing. The old cutoff is the original frozen consolidation snapshot within T20, not an exclusion of the later research from T20. Current reader/index amendments preserve their v3 preimages under depth/inherited-v3/; scientific owners are not rewritten.

Deliverable: one source-bound scientific reader, typed crosswalk, exact/derived public provenance, portable selected source closure, bounded fresh replay receipts and an efficient Codex handoff. Reading and execution claims are attributed precisely. Private custody metadata may be transformed only with original/public digest separation; no original receipt is silently transferred to changed bytes.

Limits: no repository mutation, application, commit, PR, merge, owner acceptance, new primary-source authentication, universal proof certification or T21 initiation. The baseline readback is read-only at 7efc621. R3 overlap/priority and historical hours remain unresolved. Current review bindings must match final report bytes before sealing; inventory and hash consistency are not mathematical review.
''')
put('CODEX_START_HERE.md','''# Codex: one bounded T20 v4 handoff

Read CURRENT_STATUS.json, EDITION_V4.md, INTEGRATION_PINS.json, the scope/exclusions of PUBLIC_PROJECTION.json, and REPLAY_SCOPE.json. This is a complete successor to v3, not a second separately installable tranche. Original T20 snapshot cutoff 2026-10-11T11:32:55Z remains historical; authorised same-day depth research belongs to T20 through the final seal. T21 has not begun.

## Validate once

    python -B validate_package.py
    python -B -m unittest discover -s tool-tests -v
    python -B validate_depth.py
    python -B replay_selected.py --list

Integrity is offline and standard-library only. The byte manifest is not a signature or proof certificate. depth/REVIEW_CURRENTNESS.json binds source reviews; DEPTH_REPLAY_VERIFICATION.json records selected fresh portable executions. All inherited receipts keep their original scopes. Do not replay unchanged source families merely to copy an unchanged reader. For a particular affected new target, run its declared suite, for example:

    python -B replay_selected.py --suite depth-proof-inquiry

Every advertised new suite copies exact source modules and explicit portable fixtures into a disposable directory. The runner installs and fetches nothing. Grounding is normal-only because its source uses bare assertions. Kernel source closure, inherited receipts, fresh kernel execution, ordinary proof and external human review are different axes.

## Apply only after explicit owner authority

Keep this package outside a clean target checkout. Exact approved base: commit 7efc6217c090b92d65f2c4cb8b011c18eb96bf7c, tree 906b592fb2591ed918c5f0caf485ef79dca513ab, theislampill/orthemology. The supplied readback does not rerun CI. Do not change pins to work around drift.

    python -B apply_additive.py /path/to/clean/checkout
    python -B apply_additive.py /path/to/clean/checkout --apply

The second command requires separate authority. It adds only research/t20-consolidated-20261011 and does not stage, commit, push, modify authored state, apply DAEE or replace historical CP sources. It refuses dirty/drifted preimages and existing destination. Preserve repository conventions; do not create a global schema, blanket waiver or dummy targets.

After authorised staging, use the repository's documented derived-state/release-manifest regeneration and current gates, including tests/test_internal_references.py, scripts/validate_internal_references.py, scripts/generate_current_state.py --check, scripts/validate_v5_successors.py, scripts/validate_repo.py and git diff --check --cached. Report unchanged-source whitespace advisories honestly; do not normalize original source bytes or report blanket strict PASS. Existing exact-path attribute proposals remain review-only.

## Scientific reading only when needed

For result interpretation read depth/cross_front_synthesis/RESULT.md and its typed EDGES.json; then the relevant RESULT/REVIEW pair and source-owned claim. The complete old programme remains in the original chapters and coverage crosswalk. No wholesale corpus rereading, universal re-proof or new research campaign is requested. If one current binding or dependency fails, isolate that target and report it without silently weakening the claim.

R3 reported second-order overlap and priority remain unknown, historical hours unverified, and repository adoption absent. Completion of a local sealed handoff must not be described as a merge, fresh all-corpus execution or T21 start.
''')
put('CODEX_KICKOFF_PROMPT.txt','''Proposed owner-to-Codex instruction. Pasting this prompt is the owner's instruction for the bounded integration below; the package alone grants no authority.

Please integrate this single sealed T20 v4 research handoff into theislampill/orthemology as one additive research/t20-consolidated-20261011 subtree and open a draft pull request for my review. Do not merge, push to a protected branch, start T21, or alter scientific source/result bytes.

Read CODEX_START_HERE.md, CURRENT_STATUS.json, EDITION_V4.md, INTEGRATION_PINS.json and REPLAY_SCOPE.json. Verify package integrity and current depth bindings. The 11:32:55 UTC boundary is the historical frozen consolidation snapshot; the authorised later 11 October depth research is also T20 through this edition's seal. Preserve all previous results/deltas, exact versus derived provenance, current reviews and source ownership.

Require the pinned baseline 7efc6217c090b92d65f2c4cb8b011c18eb96bf7c and tree 906b592fb2591ed918c5f0caf485ef79dca513ab. If the target has drifted, stop and report the difference for reconciliation; do not change pins or overwrite a pre-existing destination. Use the additive installer, preserve repository conventions/authored state, and run the established derived-state/release-manifest workflow and required gates. Reuse unchanged source-bound inherited receipts; rerun only an affected selected cluster, not every historical proof family. Use existing dependencies; install official pinned dependencies only if a required affected check needs them. Do not expand scientific scope.

Report actual files changed, tests run and any scoped advisories in the draft PR. Do not normalize historical scientific bytes, weaken validators, apply DAEE, or equate finite controls/hash integrity with universal proof. R3 overlap/priority and historical hours remain unresolved. The proposed PR is for review only; owner acceptance and merging remain separate decisions.
''')
# Add source-owned claims and a small explicit navigation layer for reports without their own register.
claims=[]
def addclaim(id,lane,title,statement,kind,limits,section,dependencies=[]):
 claims.append({'id':id,'title':title,'statement':statement,'contribution_class':kind,'source_owner':{'path':'depth/'+lane+'/RESULT.md','sha256':sha(P/'depth'/lane/'RESULT.md'),'section':section},'hypotheses_and_limits':limits,'dependencies':dependencies,'evidence':'Ordinary source-owned proof/application plus separately scoped finite controls and exact-byte review; current binding is in depth/REVIEW_CURRENTNESS.json.','repository_adoption':False})
addclaim('V4-J01','joint_correction','Whole-state positive descending audit-covariant second-order update','Internal second-order descending steps joined to endpoint-average positive mass reweighting give the full moving grouped flow order two, descent and audit covariance.','Joined constructive interface; inherited geometry and classical discrete gradients','C3 chart potentials, C2 mobility or supplied qualified maps; certified local branch, invariant algorithm choices, compact interior and separate finite-solver accuracy/descent obligations. R3 overlap/priority unknown.','§§1–4',['DR-01','GEO-17'])
addclaim('V4-J02','joint_correction','Moving-law topology boundary','Second-order coordinates and W1 do not imply TV convergence or generic second-order W2 with moving support and variable masses.','Exact control and topology qualification','Common Euclidean bounded carrier; no collision or rank preservation conclusion.','§6',['V4-J01'])
addclaim('V4-S01','semantic_geometry','Fixed semantic conjunction along Gaussian correction','Every member of a fixed uncountable conull repertoire stays conull while its measurable universal conjunction falls from probability one to zero along the inherited singular flow.','Inherited-theorem application and interface qualification','Singular infinite-KL start; finite-action competitor uses time change. Not a human-warrant model.','§§3–5',['MOM-01'])
addclaim('V4-S02','semantic_geometry','Exact event-preservation repair','Preserving every initially conull measurable event is equivalent to absolute continuity of the successor; TV quantitatively controls each event.','Elementary exact repair condition','No automatic future-operation closure or infinite weak-limit preservation.','§6',['V4-S01'])
addclaim('V4-G01','grounding_provenance','Endpoint lifts versus actual witness composition','Summary composition is exact iff every summarized endpoint has a genuine intermediary lift; submitted-witness compatibility needs actual middle identity.','Bounded relation theorem and foundational interface','Does not establish productive actuality, common-source truth or arbitrary continuation closure.','§§2–5',['FND-001'])
addclaim('V4-G02','grounding_provenance','Provider unity and derivative routing rank','A common original provider can coexist with diagonal routing rank n; quotienting intermediary identities invents n(n−1) routes.','Exact finite countercontrol and source-engine application','Rank counts represented mediation distinctions, not original providers.','§§6–8',['V4-G01'])
addclaim('V4-D01','decision_representation','Profile representation versus fixed robust output','The exact six-policy loss profile on C4/E4 requires two continuous coordinates; with posterior retained one further real coordinate suffices and countable tags fail on a nondegenerate fibre.','Restricted-family corollary of inherited continuation/sidecar machinery','Per-model profile, uncertainty set and a fixed minimax answer are separate objects; no psychological or physical memory bound.','§§1–5',['UI-03','PT-19','PT-20'])
addclaim('V4-O01','occurrence_warrant','Actual source-record sidecar application','The seven supplied T16 claim records require alphabet sizes 1, 2 and 3 for row-only, row-plus-voice and row/voice/named-work-exclusion contracts.','Bounded application of inherited D1/D2','One-way record view, not all linguistic readings, source truth, actual uptake or human-warrant memory.','§§1–2',['D1','D2'])
addclaim('V4-O02','occurrence_warrant','Original permission and circumstance-relative inquiry duty','The separate source return preserves original permission alongside mistaken mediation and a real qualified-inquiry duty, without deriving unavailable opportunity from missing knowledge.','Inherited source-owned coverage refinement','No new primary Arabic authentication; no change to original ruling or source veracity; no universal maximal-disclosure demand.','§§3–4',['FND-031'])
for lane,file in [('proof_inquiry','CLAIMS.json'),('uncertainty_inquiry','CLAIMS.json'),('collective_continuation','SCOPED_CLAIMS.json')]:
 d=json.loads((P/'depth'/lane/file).read_text());items=d if isinstance(d,list) else d['claims']
 for c in items:
  claims.append({**c,'title':c.get('title',c.get('claim',c['id'])),'statement':c.get('statement',c.get('conclusion',c.get('claim'))),'source_owner':{'path':'depth/'+lane+'/'+file,'sha256':sha(P/'depth'/lane/file)},'registration_scope':'Exact source-owned claim data; current review status is separately bound, not retroactively written into the author freeze.'})
put('depth/CLAIMS.json',{'schema':'t20-depth-claims-v4','claims':claims,'scope':'Additive source-bound claims; report sections control all hypotheses. Existing claims remain unchanged.'})
register=json.loads((V/'CLAIM_REGISTER.json').read_text())
for c in claims:register['claims'].append({'id':c['id'],'track':'T20_depth_v4','title':c['title'],'statement':c['statement'],'record_file':'depth/CLAIMS.json','record_file_sha256':sha(P/'depth/CLAIMS.json'),'record_selector':{'array':'claims','id':c['id']},'evidence':c.get('evidence',c.get('status','source-owned claim and scoped review')),'dependencies_as_declared':c.get('dependencies',c.get('ancestry',[])),'interpretation':'Source record controls hypotheses; current review and execution evidence are independent axes.'})
register['claim_count']=len(register['claims']);register['current_edition']='v4; authorised 11 October depth research remains T20 through final seal';put('CLAIM_REGISTER.json',register)
edges=json.loads((V/'DEPENDENCY_INDEX.json').read_text())
graph=json.loads((P/'depth/cross_front_synthesis/EDGES.json').read_text())
for e in graph['edges']:edges['edges'].append({'claim':'V4-X:'+e.get('id',str(len(edges['edges']))),'relationship':e.get('type',e.get('kind')),'owner_file':'depth/cross_front_synthesis/EDGES.json','source_owned_typed_edge':e,'reference_status':'source-owned cross-front node identifiers; exact graph controls direction and guard'})
edges['edge_count']=len(edges['edges']);put('DEPENDENCY_INDEX.json',edges)
print('Wrote current readers;',len(claims),'additive claims;',len(graph['edges']),'cross-front typed edges')

# Precisely repair inherited reader defects; historical bytes remain available.
for rel in ['geometry/GEOMETRY_MOMENTS_SYNTHESIS.md','proofs/PROOF_TYPE_INQUIRY_SYNTHESIS.md','coverage/CUMULATIVE_PROGRAMME_CROSSWALK.md']:
 put('depth/inherited-v3/'+rel,(V/rel).read_text())
 t=(V/rel).read_text()
 if rel.startswith('geometry/'):
  t=t.replace('Overlapping partition families remain an unclassified extension.','The all-positive overlapping-partition gradient case is classified by DR-01 under its full metric/product-domain contract. Restricted groups, changed metrics, and semantic identification of actual source revisions remain separate obligations.')
 if rel.startswith('proofs/'):
  t=t.replace('guard[OMITTED_PRIVATE_MACHINE_PATH] histograms','guard/root/output-subset histograms')
 if rel.startswith('coverage/'):
  t+='\n\n## v4 usable methodology routes\n\nS25–S28 now resolve through coverage/methodology selected-field ledgers and SELECTED_SOURCE_READS.json. These safe projections distinguish original/private custody identity from derived public bytes. They add no primary reading or execution credit; S28 remains an index summary, not the complete reading ledger.\n'
 put(rel,t)

for rel in ['OWNER_REVIEW_CASE.md','FIELD_GUIDE.md']:
 put('depth/inherited-v3/'+rel,(V/rel).read_text())
put('OWNER_REVIEW_CASE.md',f'''# Owner review: complete integrated T20 v4 handoff

The proposed stopping deliverable now includes the original programme, all v3 results and the reviewed 11 October depth work: whole-state correction, semantic geometry, cache/inquiry transport, uncertainty games, exact representation, grounding provenance, collective/effective continuation and actual occurrence/source-warrant application. The integrated chapter and 49 typed edges connect these without inventing one master theorem.

CLAIM_REGISTER has {len(register['claims'])} navigation records, including {len(claims)} additive source-bound records. Counts describe navigation, not distinct discoveries. The eight fresh portable execution targets and nine new source-specific/combined review routes are separate evidence counts; the inherited v3 review remains separately preserved.

Review whether this preserves the programme adequately and supplies a usable T20 stopping point and Codex handoff. Acceptance of this research edition, authorisation of its draft PR and repository merge are separate. T21 has not begun. The proposed paste-ready prompt gives bounded integration/draft-PR authority only when the owner chooses to issue it to Codex.

The affirmative foundational appraisal is retained. Actual source-content, basing, authority and opportunity premises remain explicit; mathematical reductions cannot create them. R3 second-order overlap/priority and historical hours remain unknown. These precise residuals do not erase the completed local results.

Use EDITION_V4.md for the concise result, depth/cross_front_synthesis/RESULT.md for the broad argument, and depth/REVIEW_CURRENTNESS.json for current reviewed-byte identities. The original owner-review case remains in depth/inherited-v3/OWNER_REVIEW_CASE.md as history.
''')
put('FIELD_GUIDE.md','''# Field guide to the integrated T20 v4 reader

One major current mathematical theme is what a specified task must retain, and which declared operations preserve it. The programme joins source-owned foundational arguments, exact proof/type interfaces, correction geometry, uncertainty/inquiry and provenance. The original guide remains verbatim in depth/inherited-v3/FIELD_GUIDE.md.

Start at EDITION_V4.md. Then read depth/cross_front_synthesis/RESULT.md: common refinement has different mathematical causes in gradients, convex cone stability and reachable controls; moving correction needs both an audit square and a suitable observation topology; exact law profiles can exceed one fixed decision's needs; paid proof reuse requires actual immutable identities and validity; common original provenance does not erase actual mediation or acquisition distinctions.

The collective bridge uses an actual older model to show when linked acquisition changes inquiry value and why correct finite recomputation does not produce an indefinitely committed plan. The occurrence bridge uses actual T16 source records and a separate source-return owner: its finite sidecar service preserves supplied distinctions without pretending to authenticate the Arabic interpretation or confer human warrant.

MATHEMATICAL_SYNTHESIS.md, FOUNDATIONAL_CROSSWALK.md, the four inherited track chapters and coverage/CUMULATIVE_PROGRAMME_CROSSWALK.md retain the cumulative programme and original twelve avenues. New reports/reviews are under depth/. Current typed claims, source locators, replay closures and provenance distinguish exact inherited bytes from derived public readers.

The original 11:32:55 UTC cutoff is a frozen consolidation snapshot within T20. The authorised later 11 October research is integrated as its T20 successor. T21 is not started, no repository adoption is claimed, and the scope does not become an invitation to rerun every historical source.
''')

# Keep the cumulative substantive guide accessible in the current edition.
guide=(P/'FIELD_GUIDE.md').read_text()
body=(V/'FIELD_GUIDE.md').read_text().split('## The programme in plain language',1)[1]
put('FIELD_GUIDE.md',guide+'\n## The programme in plain language'+body)
