import MixedSpecializations
import TypeCodeSubstitution
namespace CodedMixedTransformations
open OrthemologyV2 OrthemologyV3 P01AC Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity CodedPolyTransformations
set_option maxRecDepth 8192
set_option maxHeartbeats 12000000

def tcPlainChildren (s : SubstState) : List SubstState :=
  if tag s.2 = 2 then [(s.1,arg1 s.2)]
  else if tag s.2 = 1 then [(s.1,arg1 s.2),(s.1,arg2 s.2)] else []

theorem primrec_tcPlainChildren : Primrec tcPlainChildren := by
  have ht := primrec_tag.comp (Primrec.snd : Primrec (fun s : SubstState => s.2))
  have ha : Primrec (fun s : SubstState => (s.1,arg1 s.2)) := Primrec.fst.pair (primrec_arg1.comp Primrec.snd)
  have hb : Primrec (fun s : SubstState => (s.1,arg2 s.2)) := Primrec.fst.pair (primrec_arg2.comp Primrec.snd)
  exact Primrec.ite (Primrec.eq.comp ht (.const 2)) (Primrec.list_cons.comp ha (.const []))
    (Primrec.ite (Primrec.eq.comp ht (.const 1))
      (Primrec.list_cons.comp ha (Primrec.list_cons.comp hb (.const []))) (.const []))

def supportStep (s : SubstState) (values : List Nat) : Nat :=
  if tag s.2 = 0 then varIndex s.2 + 1
  else if tag s.2 = 2 then (values[0]?.getD 0) - 1
  else if tag s.2 = 1 then max (values[0]?.getD 0) (values[1]?.getD 0)
  else 0

def finStep (s : SubstState) (values : List Nat) : Nat :=
  if tag s.2 = 0 then paramCode (varIndex s.2)
  else if tag s.2 = 2 then unary 2 (values[0]?.getD 0)
  else if tag s.2 = 1 then binary 4 (values[0]?.getD 0) (wkTyCode (values[1]?.getD 0))
  else encode Ty.bottom

theorem primrec_supportStep : Primrec₂ supportStep := by
  have hc : Primrec (fun p : SubstState × List Nat => p.1.2) := Primrec.snd.comp Primrec.fst
  have ht := primrec_tag.comp hc
  have h0 : Primrec (fun p : SubstState × List Nat => p.2[0]?.getD 0) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd (.const 0)) (.const 0)
  have h1 : Primrec (fun p : SubstState × List Nat => p.2[1]?.getD 0) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd (.const 1)) (.const 0)
  exact Primrec.ite (Primrec.eq.comp ht (.const 0)) (Primrec.succ.comp (primrec_varIndex.comp hc))
    (Primrec.ite (Primrec.eq.comp ht (.const 2)) (Primrec.pred.comp h0)
      (Primrec.ite (Primrec.eq.comp ht (.const 1)) (Primrec.nat_max.comp h0 h1) (.const 0)))

theorem primrec_finStep : Primrec₂ finStep := by
  have hc : Primrec (fun p : SubstState × List Nat => p.1.2) := Primrec.snd.comp Primrec.fst
  have ht := primrec_tag.comp hc
  have h0 : Primrec (fun p : SubstState × List Nat => p.2[0]?.getD 0) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd (.const 0)) (.const 0)
  have h1 : Primrec (fun p : SubstState × List Nat => p.2[1]?.getD 0) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd (.const 1)) (.const 0)
  exact Primrec.ite (Primrec.eq.comp ht (.const 0)) (primrec_paramCode.comp (primrec_varIndex.comp hc))
    (Primrec.ite (Primrec.eq.comp ht (.const 2)) ((primrec_unary_fixed 2).comp h0)
      (Primrec.ite (Primrec.eq.comp ht (.const 1))
        ((primrec_binary_fixed 4).comp h0 (primrec_wkTyCode.comp h1)) (.const _)))

def finSupportCode (c : Nat) : Nat := foldSubst tcPlainChildren supportStep (([],0),c)
def finCode (c : Nat) : Nat := foldSubst tcPlainChildren finStep (([],0),c)

theorem primrec_finSupportCode : Primrec finSupportCode :=
  (primrec_foldSubst primrec_tcPlainChildren primrec_supportStep).comp ((Primrec.const ([],0)).pair Primrec.id)
theorem primrec_finCode : Primrec finCode :=
  (primrec_foldSubst primrec_tcPlainChildren primrec_finStep).comp ((Primrec.const ([],0)).pair Primrec.id)

theorem supportFold_exact (env : List Nat × Nat) (A : TypeCode) :
    foldSubst tcPlainChildren supportStep (env,encode A) = finSupport A := by
  induction A with
  | var n => rw [foldSubst_eq]; simp [supportStep,finSupport,varIndex,leaf]
  | bottom => rw [foldSubst_eq]; simp [supportStep,finSupport]
  | all B ih =>
    rw [foldSubst_eq]
    have h := unary_child_lt 2 (encode B)
    simp [supportStep,tcPlainChildren,boundedInputs,h,ih,finSupport]
  | arrow A B iha ihb =>
    rw [foldSubst_eq]
    have ha := binary_left_lt 1 (encode A) (encode B)
    have hb := binary_right_lt 1 (encode A) (encode B)
    simp [supportStep,tcPlainChildren,boundedInputs,ha,hb,iha,ihb,finSupport]

theorem finFold_exact (env : List Nat × Nat) (A : TypeCode) :
    foldSubst tcPlainChildren finStep (env,encode A) = encode (fin A) := by
  induction A with
  | var n => rw [foldSubst_eq]; simp [finStep,fin,varIndex,leaf,paramCode]
  | bottom => rw [foldSubst_eq]; simp [finStep,fin]
  | all B ih =>
    rw [foldSubst_eq]
    have h := unary_child_lt 2 (encode B)
    simp [finStep,tcPlainChildren,boundedInputs,h,ih,fin]
  | arrow A B iha ihb =>
    rw [foldSubst_eq]
    have ha := binary_left_lt 1 (encode A) (encode B)
    have hb := binary_right_lt 1 (encode A) (encode B)
    simp [finStep,tcPlainChildren,boundedInputs,ha,hb,iha,ihb,fin,arr,wkTyCode_exact]

theorem finSupportCode_exact (A : TypeCode) : finSupportCode (encode A) = finSupport A := supportFold_exact _ A
theorem finCode_exact (A : TypeCode) : finCode (encode A) = encode (fin A) := finFold_exact _ A

#print axioms primrec_finSupportCode
#print axioms finCode_exact
end CodedMixedTransformations
