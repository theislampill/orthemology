import FiniteTypeCodeCompilation
namespace CodedRuleTemplates
open P01D P01AC Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity CodedPolyTransformations CodedMixedTransformations
set_option maxRecDepth 8192
set_option maxHeartbeats 10000000
attribute [local irreducible] Nat.pair

def pairPolyCode (x y : Nat) :=
  appCode (appCode (encode (Poly.atom .s))
    (appCode (appCode (encode (Poly.atom .s)) (encode (Poly.atom .i)))
      (appCode (encode (Poly.atom .k)) x))) (appCode (encode (Poly.atom .k)) y)
def fstPolyCode (z : Nat) := appCode z (encode (Poly.atom .k))
def sndPolyCode (z : Nat) := appCode z (encode (Poly.app (Poly.atom .k) (.atom .i)))
def jPolyCode (d y p : Nat) :=
  appCode (appCode (appCode (encode (Poly.atom .k)) (appCode (encode (Poly.atom .k)) d)) y) p

theorem primrec_pairPolyCode : Primrec₂ pairPolyCode :=
  primrec_appCode.comp
    (primrec_appCode.comp (.const _) (primrec_appCode.comp (.const _) (primrec_appCode.comp (.const _) Primrec.fst)))
    (primrec_appCode.comp (.const _) Primrec.snd)
theorem primrec_fstPolyCode : Primrec fstPolyCode := primrec_appCode.comp Primrec.id (.const _)
theorem primrec_sndPolyCode : Primrec sndPolyCode := primrec_appCode.comp Primrec.id (.const _)
theorem primrec_jPolyCode : Primrec (fun s : Nat × Nat × Nat => jPolyCode s.1 s.2.1 s.2.2) :=
  primrec_appCode.comp
    (primrec_appCode.comp (primrec_appCode.comp (.const _) (primrec_appCode.comp (.const _) Primrec.fst)) (Primrec.fst.comp Primrec.snd))
    (Primrec.snd.comp Primrec.snd)

@[simp] theorem pairPolyCode_exact (x y : Poly) : pairPolyCode (encode x) (encode y) = encode (pairPoly x y) := rfl
@[simp] theorem fstPolyCode_exact (z : Poly) : fstPolyCode (encode z) = encode (fstPoly z) := rfl
@[simp] theorem sndPolyCode_exact (z : Poly) : sndPolyCode (encode z) = encode (sndPoly z) := rfl
@[simp] theorem jPolyCode_exact (d y p : Poly) : jPolyCode (encode d) (encode y) (encode p) = encode (jPoly d y p) := rfl

theorem finiteEnv_double (a b : Poly) : finiteEnv [a,b] 0 = P01F.cons a (P01F.cons b Poly.var) := by
  funext n; cases n with
  | zero => rfl
  | succ n => cases n <;> simp [finiteEnv,P01F.cons]

def branchAtCode (d a b : Nat) := substituteCode ([b,a],0) d

theorem primrec_branchAtCode : Primrec (fun s : Nat × Nat × Nat => branchAtCode s.1 s.2.1 s.2.2) :=
  primrec_substituteCode.comp
    ((Primrec.list_cons.comp (Primrec.snd.comp Primrec.snd)
      (Primrec.list_cons.comp (Primrec.fst.comp Primrec.snd) (.const []))).pair (.const 0)) Primrec.fst

@[simp] theorem branchAtCode_exact (d a b : Poly) :
    branchAtCode (encode d) (encode a) (encode b) = encode (SigmaCompletion.branchAt d a b) := by
  simpa only [branchAtCode,List.map_cons,List.map_nil,finiteEnv_double,SigmaCompletion.branchAt] using substituteCode_exact [b,a] 0 d

def uncurriedStepCode (s : Nat) :=
  appCode (appCode (shiftCode 1 s) (encode (fstPoly (.var 0)))) (encode (sndPoly (.var 0)))
def totalStepCode (d : Nat) := abstractCode (pairPolyCode (encode RigidityInitiality.nextIndex) d)
def totalSeedCode (p : Nat) := pairPolyCode (encode SourceRigidity.zero) p
def sectionBodyCode (p s n : Nat) := sndPolyCode (appCode (appCode n (totalStepCode (uncurriedStepCode s))) (totalSeedCode p))
def sectionPolyCode (p s : Nat) := abstractCode (sectionBodyCode (shiftCode 1 p) (shiftCode 1 s) (encode (Poly.var 0)))

theorem primrec_uncurriedStepCode : Primrec uncurriedStepCode :=
  primrec_appCode.comp (primrec_appCode.comp (primrec_shiftCode.comp (.const 1) Primrec.id) (.const _)) (.const _)
theorem primrec_totalStepCode : Primrec totalStepCode :=
  primrec_abstractCode.comp (primrec_pairPolyCode.comp (.const _) Primrec.id)
theorem primrec_totalSeedCode : Primrec totalSeedCode := primrec_pairPolyCode.comp (.const _) Primrec.id
theorem primrec_sectionBodyCode : Primrec (fun s : Nat × Nat × Nat => sectionBodyCode s.1 s.2.1 s.2.2) :=
  primrec_sndPolyCode.comp (primrec_appCode.comp
    (primrec_appCode.comp (Primrec.snd.comp Primrec.snd)
      (primrec_totalStepCode.comp (primrec_uncurriedStepCode.comp (Primrec.fst.comp Primrec.snd))))
    (primrec_totalSeedCode.comp Primrec.fst))
theorem primrec_sectionPolyCode : Primrec₂ sectionPolyCode :=
  primrec_abstractCode.comp (primrec_sectionBodyCode.comp
    ((primrec_shiftCode.comp (.const 1) Primrec.fst).pair
      ((primrec_shiftCode.comp (.const 1) Primrec.snd).pair (.const _))))

@[simp] theorem uncurriedStepCode_exact (s : Poly) : uncurriedStepCode (encode s) = encode (RigidityInitiality.uncurriedStep s) := by
  simp only [uncurriedStepCode,shiftCode_one_exact,← encode_app,RigidityInitiality.uncurriedStep]
@[simp] theorem totalStepCode_exact (d : Poly) : totalStepCode (encode d) = encode (RigidityInitiality.totalStep d) := by
  simp only [totalStepCode,pairPolyCode_exact,abstractCode_exact,RigidityInitiality.totalStep]
@[simp] theorem totalSeedCode_exact (p : Poly) : totalSeedCode (encode p) = encode (RigidityInitiality.totalSeed p) := rfl
@[simp] theorem sectionBodyCode_exact (p s n : Poly) : sectionBodyCode (encode p) (encode s) (encode n) = encode (RigidityInitiality.sectionBody p s n) := by
  simp only [sectionBodyCode,uncurriedStepCode_exact,totalStepCode_exact,totalSeedCode_exact,← encode_app,sndPolyCode_exact,RigidityInitiality.sectionBody]
@[simp] theorem sectionPolyCode_exact (p s : Poly) : sectionPolyCode (encode p) (encode s) = encode (RigidityInitiality.sectionPoly p s) := by
  simp only [sectionPolyCode,shiftCode_one_exact,sectionBodyCode_exact,abstractCode_exact,RigidityInitiality.sectionPoly]

end CodedRuleTemplates
