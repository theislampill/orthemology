from pathlib import Path
import json
R=Path(__file__).resolve().parent
header='''import IndependentTemplateControls
namespace IndependentRuleMapReview
open Encodable CodedRuleTemplates CodedPolyTransformations P01D P01AC JointCertificates AuxiliaryCertificates OrthemologyV2
set_option maxRecDepth 32768
set_option maxHeartbeats 4000000
'''
# Each negative assertion intentionally states an observably wrong actual code-map result.
cases={
'WrongBranchOrientation':('branchAtCode (encode (Poly.var 0)) (encode (Poly.atom .i)) (encode (Poly.atom .k)) = encode (Poly.atom .i)','rw [branchAtCode_exact]; apply congrArg encode; decide'),
'WrongMotiveOrientation':('motiveAtCode (encode (Ty.identity .raw (.var 0) (.var 1))) (encode (Poly.atom .i)) (encode (Poly.atom .k)) = encode (Ty.identity .raw (.atom .i) (.atom .k))','rw [motiveAtCode_exact]; apply congrArg encode; decide'),
'WrongFullInstantiationTail':('branchAtCode (encode (Poly.var 2)) (encode (Poly.atom .i)) (encode (Poly.atom .k)) = encode (Poly.var 2)','rw [branchAtCode_exact]; apply congrArg encode; decide'),
'WrongBranchOffset':('branchTypeCode (encode (Ty.identity .raw (.var 1) (.var 2))) = encode (Ty.identity .raw (.var 1) (.var 2))','rw [branchTypeCode_exact]; apply congrArg encode; decide'),
'WrongBranchPiBinder':('branchTypeCode (encode (Ty.pi .raw (.identity .raw (.var 1) (.var 2)))) = encode (Ty.pi .raw (.identity .raw (pairPoly (.var 1) (.var 0)) (.var 2)))','rw [branchTypeCode_exact]; apply congrArg encode; decide'),
'WrongMotiveAllLift':('motiveAtCode (encode (Ty.all (.identity .raw (.var 0) (.var 1)))) (encode (Poly.var 3)) (encode (Poly.var 4)) = encode (Ty.all (.identity .raw (.var 5) (.var 4)))','rw [motiveAtCode_exact]; apply congrArg encode; decide'),
'WrongMotivePiNoLift':('motiveAtCode (encode (Ty.pi .raw (.identity .raw (.var 1) (.var 2)))) (encode (Poly.var 3)) (encode (Poly.var 4)) = encode (Ty.pi .raw (.identity .raw (.var 4) (.var 3)))','rw [motiveAtCode_exact]; apply congrArg encode; decide'),
'WrongThetaOrder':('thetaCode (encode ([Ty.bottom] : Tel)) (encode Ty.raw) (encode (Poly.var 0)) = encode ([Ty.raw, .identity .raw (.var 1) (.var 0), .bottom] : Tel)','rw [thetaCode_exact]; apply congrArg encode; decide'),
'WrongSectionSeedShift':('shiftCode 1 (encode (Poly.var 0)) = encode (Poly.var 0)','rw [shiftCode_one_exact]; apply congrArg encode; decide'),
'WrongUncurriedShift':('uncurriedStepCode (encode (Poly.var 0)) = encode (Poly.app (.app (.var 0) (fstPoly (.var 0))) (sndPoly (.var 0)))','rw [uncurriedStepCode_exact]; apply congrArg encode; decide'),
'WrongConclusionTag':('conclusionCode (encode (Rule.FormE_raw [])) = encode (Claim.formJ [] .raw)','rw [conclusionCode_exact]; apply congrArg encode; decide'),
'IgnoreActualLookup':('checkSideCode (encode (Rule.HasJ_var [.raw] .raw 1 (.zero [] .raw))) = true','rw [checkSideCode_exact]; decide'),
'IgnoreActualPoly':('checkSideCode (encode (Rule.HasE_identityIntro [] .raw (.atom .i) (.atom .k) (.refl (.atom .i)))) = true','rw [checkSideCode_exact]; decide'),
'IgnoreFiniteSupport':('checkSideCode (encode (Rule.HasJ_finite (.arrow (.var 0) (.var 0)) [] .i [] (.i (.var 0)))) = true','rw [checkSideCode_exact]; decide'),
'IgnoreConvScope':('checkSideCode (encode (Rule.HasE_conv [] .raw (.var 0) (.var 0) (.refl (.var 0)))) = true','rw [checkSideCode_exact]; decide'),
'MalformedAsValidator':('checkSideCode (AuxiliaryCodeComputability.pack 1 [SourceFamilyComputability.leaf 99]) = false','rw [malformed_side_accepted]; decide'),
}
for ext in ['J','E']:
 r=f'Rule.Has{ext}_finite (.arrow .bottom .bottom) [] .i [.raw,.bottom,.raw] (.i .bottom)'
 final='(Ty.pi .bottom .bottom)'
 cases['DropUnusedImages'+ext]=(f'premisesCode (encode ({r})) = ([Claim.form{ext} [] {final}] : List Claim).map encode','rw [premisesCode_exact]; apply congrArg (List.map encode); decide')
 cases['ReorderImages'+ext]=(f'premisesCode (encode ({r})) = ([Claim.form{ext} [] .bottom, .form{ext} [] .raw, .form{ext} [] .raw, .form{ext} [] ({final})] : List Claim).map encode','rw [premisesCode_exact]; apply congrArg (List.map encode); decide')
 cases['DropDuplicateImages'+ext]=(f'premisesCode (encode ({r})) = ([Claim.form{ext} [] .raw, .form{ext} [] .bottom, .form{ext} [] ({final})] : List Claim).map encode','rw [premisesCode_exact]; apply congrArg (List.map encode); decide')
r='Rule.HasJ_sigmaElim [] .raw .bottom .raw (.var 0) (.atom .i)'
cases['MissingSigmaSourceRoot']=(f'premisesCode (encode ({r})) = (({r}).premises.tail).map encode','rw [premisesCode_exact]; apply congrArg (List.map encode); decide')
r='Rule.HasJ_natInduction [] .raw (.atom .i) (.atom .k)'
cases['MissingInductionSourceRoot']=(f'premisesCode (encode ({r})) = (({r}).premises.tail).map encode','rw [premisesCode_exact]; apply congrArg (List.map encode); decide')
for n,(statement,proof) in cases.items(): (R/'negative'/(n+'.lean')).write_text(header+'example : '+statement+' := by\n  '+proof+'\nend IndependentRuleMapReview\n')
(R/'INDEPENDENT_NEGATIVE_TARGETS.json').write_text(json.dumps(list(cases),indent=2)+'\n')
