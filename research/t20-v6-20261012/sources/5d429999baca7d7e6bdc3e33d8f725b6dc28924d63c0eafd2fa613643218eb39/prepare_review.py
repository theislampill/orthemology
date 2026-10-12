#!/usr/bin/env python3
"""Reviewer-authored custody and exact-header extraction, no proof-source edits."""
from pathlib import Path
import hashlib,json,re,shutil,zipfile,io,datetime
ROOT=Path(__file__).resolve().parent
WORK=ROOT.parents[1]
PACKET=WORK/'formal/semantic-controls/packet'
BASE=WORK/'baseline/seventh-components/controls'
MANIFEST='8981fe18fb0d182dfbab01142f250354846dfb691c873d8d1ced71d3f1df3f4c'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
write=lambda p,x:Path(p).write_text(json.dumps(x,indent=2)+'\n')
assert sha(PACKET/'SOURCE_MANIFEST.json')==MANIFEST
m=json.loads((PACKET/'SOURCE_MANIFEST.json').read_text())
paths=[r['path'] for r in m['sources']]
assert len(paths)==len(set(paths))
assert {str(p.relative_to(PACKET)) for p in PACKET.rglob('*.lean')}==set(paths)
for r in m['sources']:
 p=PACKET/r['path']; assert p.is_file() and not p.is_symlink() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],str(p)
new=m['new_modules'];runtime=list((PACKET/'runtime/src').rglob('*.lean'))
baseline=[]
for p in runtime:
 if p.stem in new:continue
 q=BASE/'runtime/src'/p.relative_to(PACKET/'runtime/src')
 assert p.read_bytes()==q.read_bytes(),str(p)
 baseline.append(str(p.relative_to(PACKET)))
assert len(baseline)==162
assert (PACKET/'cost/mutation/ActualExponentialMoments.lean').read_bytes()==(BASE/'mutations/cost/ActualExponentialMoments.lean').read_bytes()
assert (PACKET/'runtime/inherited-mutation/FullControllerCanonicalLaw.lean').read_bytes()==(BASE/'mutations/runtime/FullControllerCanonicalLaw.lean').read_bytes()
assert (PACKET/'cost/src/ActualExponentialMoments.lean').read_bytes()==(BASE/'original-source/cost/ActualExponentialMoments.lean').read_bytes()
custody=json.loads((PACKET/'cost/SOURCE_CUSTODY.json').read_text())
outer=WORK.parent/custody['outer_archive']
assert sha(outer)==custody['outer_sha256']
with zipfile.ZipFile(outer) as z:inner=z.read(custody['inner_member'])
assert hashlib.sha256(inner).hexdigest()==custody['inner_sha256']
with zipfile.ZipFile(io.BytesIO(inner)) as z:
 for r in custody['sources']:
  assert z.read(r['archive_member'])==(PACKET/r['path']).read_bytes(),r['path']
assert len(custody['sources'])==146
for suite,positive,negative,before,after in [
 ('cost','cost/src/ActualExponentialMoments.lean','cost/mutation/ActualExponentialMoments.lean','fallback fallbackAction ε\n    bad hpriority hs₀ σ hσ η hηpos hη hSep','fallback fallbackAction (ε/2)\n    bad hpriority hs₀ σ hσ η hηpos hη hSep'),
 ('runtime','runtime/src/FullControllerCanonicalLaw.lean','runtime/inherited-mutation/FullControllerCanonicalLaw.lean','(decodedHistory (policyProgram (withComputedTolerance c)) (sourcePolicy (withComputedTolerance c)) σ x)) := by','(decodedHistory (policyProgram c) (sourcePolicy (withComputedTolerance c)) σ x)) := by')]:
 a=(PACKET/positive).read_text();b=(PACKET/negative).read_text();assert a.count(before)==1 and a.replace(before,after)==b
snapshot=ROOT/'snapshot';assert not snapshot.exists();shutil.copytree(PACKET,snapshot)
assert not list(snapshot.rglob('*.olean'))
# Exact substring extraction; colon separating the universal binder block and
# conclusion is the sole syntax conversion from theorem header to proposition.
src=snapshot/'runtime/inherited-mutation/FullControllerCanonicalLaw.lean'
s=src.read_text();mark='theorem full_phase_computed_tolerance_decoded_parity'
assert s.count(mark)==1
start=s.index(mark)+len(mark);end=s.index(' := by',start)
header=s[start:end]
assert header.count(' :\n    ∀ᵐ')==1
prop='∀'+header.replace(' :\n    ∀ᵐ',',\n    ∀ᵐ')
(ROOT/'EXTRACTED_MUTANT_HEADER.txt').write_text(mark+header+'\n')
opening='''import ExactRuntimeCounterexample
set_option autoImplicit false
noncomputable section
namespace SemanticControlIndependentReview
open MeasureTheory
open HiddenParity HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Necessity
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.RuntimeBridge
open Orthemology.RuntimeBridge.PhaseUpdate.FullController
open Orthemology.RationalLaw.CanonicalBinding
open Orthemology.Eighth.SemanticControls
open P02A2.Q8Measure (fairCantor)
'''
extracted=opening+'\ndef ExtractedMutantStatement : Prop :=\n'+prop+'\n\n'
extracted+='''theorem extracted_statement_exact : ExtractedMutantStatement = MutatedRuntimeClaim := rfl

theorem extracted_statement_refuted : ¬ ExtractedMutantStatement :=
  exact_mutated_runtime_claim_false

-- A positive set here is a measurable fair-Cantor event, not merely outer measure.
theorem exact_failure_event_measurable (d : Bool × Bool) :
    MeasurableSet {x | ¬ ParitySuccess (actionPriority initialCandidate) (historyAction d
      (decodedHistory (policyProgram oldConfig)
        (sourcePolicy (withComputedTolerance oldConfig)) initialCandidate x))} := by
  exact (paritySuccess_measurable (actionPriority initialCandidate)).compl.preimage
    ((historyAction_measurable d).comp (decodedHistory_measurable _ _ _))

theorem fixture_computed_tolerance : RationalGate.tolerance fixtureKernel Finset.univ = 1/6 := by
  decide

theorem exact_computed_binding :
    ((withComputedTolerance oldConfig).toleranceNumerator : ℚ) /
      (withComputedTolerance oldConfig).toleranceDenominator = 1/6 := by
  rw [computed_tolerance_exact]
  exact fixture_computed_tolerance

theorem actual_model_membership : initialCandidate ∈ oldConfig.initialSupport := Finset.mem_univ _

theorem finite_prior_probability : IsProbabilityMeasure (Measure.dirac ()) := inferInstance

theorem fixed_fair_input_probability : IsProbabilityMeasure fairCantor := inferInstance

#print axioms extracted_statement_exact
#print axioms extracted_statement_refuted
#print axioms exact_failure_event_measurable
#print axioms fixture_computed_tolerance
#print axioms exact_computed_binding
#print axioms actual_model_membership
#print axioms finite_prior_probability
#print axioms fixed_fair_input_probability
end SemanticControlIndependentReview
'''
(ROOT/'ExactStatementReview.lean').write_text(extracted)
# The wrong old/old surrogate and original computed/computed statement must not
# pass an rfl correspondence test for the inherited mixed statement.
for label,replaced in [
 ('WrongOldOld',prop.replace('(sourcePolicy (withComputedTolerance c))','(sourcePolicy c)')),
 ('WrongComputedComputed',prop.replace('(policyProgram c)','(policyProgram (withComputedTolerance c))'))]:
 assert replaced!=prop
 (ROOT/(label+'.lean')).write_text(opening+'\ndef WrongStatement : Prop :=\n'+replaced+'\n\nexample : WrongStatement = MutatedRuntimeClaim := rfl\nend SemanticControlIndependentReview\n')
# Audit every named declaration in the five new modules, including definitions.
newdecl=[]
for mod in new:
 text=(snapshot/'runtime/src'/f'{mod}.lean').read_text()
 for kind,name in re.findall(r'(?m)^(?:@\[[^\n]*\]\s*)?(?:noncomputable\s+)?(theorem|lemma|def|abbrev|instance)\s+(\w+)',text):
  newdecl.append({'module':mod,'kind':kind,'name':'Orthemology.Eighth.SemanticControls.'+name})
assert len(newdecl)==80
(ROOT/'EveryNewAxiom.lean').write_text('import ExactRuntimeCounterexample\n'+''.join('#print axioms '+d['name']+'\n' for d in newdecl))
write(ROOT/'NEW_DECLARATIONS.json',newdecl)
write(ROOT/'CUSTODY_REVIEW.json',{
 'status':'PASS_SOURCE_AND_PROVENANCE','verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'source_manifest_sha256':MANIFEST,'source_count':len(paths),'runtime_baseline_modules_byte_equal':len(baseline),
 'cost_archive_modules_byte_equal':len(custody['sources']),'exact_inherited_mutant_bytes':True,
 'snapshot_custom_objects':0,'snapshot_files':len(list(snapshot.rglob('*'))),
 'extracted_from':str(src.relative_to(ROOT)),'extracted_from_sha256':sha(src),
 'extracted_header_sha256':sha(ROOT/'EXTRACTED_MUTANT_HEADER.txt'),
 'extraction_transformation':'The exact theorem binder/conclusion substring becomes a forall proposition; the sole binder/result separator colon becomes a comma. No hypothesis or conclusion term is altered.',
 'generated_review_sha256':sha(ROOT/'ExactStatementReview.lean'),'new_named_declarations':len(newdecl),
 'historical_receipts_unmodified':True,'canonical_repository_edits':False})
print('PASS_SOURCE_AND_PROVENANCE',len(paths),'sources; 162 baseline and 146 archive byte equal; 80 new declaration readbacks prepared')
