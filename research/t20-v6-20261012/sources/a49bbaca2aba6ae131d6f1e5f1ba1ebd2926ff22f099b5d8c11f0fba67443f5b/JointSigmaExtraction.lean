import JointTypedCanonicity

/- Numeric existential witnesses with their actual dependent source evidence.
No new typing rule, semantic reflection, or raw eta law is introduced. -/
namespace JointCompletion.DependentExtraction
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness (N inputNumeral iterationPoly)
open P01AC.Intensional.Plus (PolyConvPlus)
open ClosedScalarInstances (scalarLeft)
open P01AC.ExtensionalRepair.Structural
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem form_sigma_inv {Γ A B} (h : FormJ Γ (.sigma A B)) :
    FormJ Γ A ∧ FormJ (A :: Γ) B := by
  cases h with
  | formBase h => cases h with | sigma hA hB => exact ⟨.formBase hA,.formBase hB⟩
  | sigma hA hB => exact ⟨hA,hB⟩

/-- Actual Joint J transports along source identity, including new families. -/
theorem transport_source {Γ : Tel} {X P : Ty} {x y e d : Poly}
    (hc : CtxJ Γ) (hX : FormJ Γ X) (hP : FormJ (X :: Γ) P)
    (hx : HasJ Γ x X) (hy : HasJ Γ y X)
    (he : HasJ Γ e (.identity X x y)) (hd : HasJ Γ d (inst P x)) :
    HasJ Γ (jPoly d y e) (inst P y) := by
  have hM : FormJ (theta Γ X x) (wk P) :=
    Structural.form_wk hP (.ext hc hX) (Structural.form_theta_head hc hX hx)
  have at_eq (v r : Poly) : motiveAt (wk P) v r = inst P v :=
    subst_wk_cancel P r (cons v Poly.var)
  have h := HasJ.j hX hM (.identity hX hx hy)
    ((at_eq x (.atom .i)).symm ▸ Structural.form_inst hc hP hx)
    ((at_eq y e).symm ▸ Structural.form_inst hc hP hy) hx hy he
    ((at_eq x (.atom .i)).symm ▸ hd)
  simpa only [at_eq] using h

/-- The original J polynomial erases to d. Hence witness extraction preserves
its literal second-projection term rather than merely choosing a new realizer. -/
theorem transport_erased {Γ : Tel} {X P : Ty} {x y e d : Poly}
    (hc : CtxJ Γ) (hX : FormJ Γ X) (hP : FormJ (X :: Γ) P)
    (hx : HasJ Γ x X) (hy : HasJ Γ y X)
    (he : HasJ Γ e (.identity X x y)) (hd : HasJ Γ d (inst P x)) :
    HasJ Γ d (inst P y) := by
  have h := transport_source hc hX hP hx hy he hd
  have erasure : PolyConvPlus (jPoly d y e) d :=
    (PolyConvPlus.app (.k _ _) (.refl _)).trans (.k _ _)
  exact .conv (Structural.form_inst hc hP hy) h erasure (Structural.has_scoped hd)

/-- The first projection's count is computational data. All remaining fields
are actual frozen-grammar proofs, erased at runtime. -/
structure NumeralFiber (P : Ty) (z : Poly) where
  count : Nat
  observation : PolyConvPlus (scalarLeft (fstPoly z)) (iterationPoly count)
  index_identity : HasJ [] (.atom .i) (.identity N (fstPoly z) (inputNumeral count))
  fiber_has : HasJ [] (sndPoly z) (inst P (inputNumeral count))
  representative_has : HasJ [] (pairPoly (inputNumeral count) (sndPoly z)) (.sigma N P)

/-- Every closed actual Joint natural-indexed Sigma supplies an executable
numeric index and a source witness in that literal numeral-indexed fiber. -/
def extractSigma (P : Ty) (z : Poly) (hz : HasJ [] z (.sigma N P)) : NumeralFiber P z := by
  have hS := Structural.has_form hz
  have hP := (form_sigma_inv hS).2
  have hn : HasJ [] (fstPoly z) N := .sigmaFst (Structural.form_nat .nil) hS hz
  let result := EffectiveNumerals.extractIteration (fstPoly z) hn
  have hk : HasJ [] (inputNumeral result.val) N :=
    .hasBase (EffectiveNumerals.old_numeral_has result.val)
  have hi : HasJ [] (.atom .i) (.identity N (fstPoly z) (inputNumeral result.val)) :=
    canonicity_at_count hn result.property
  have hd : HasJ [] (sndPoly z) (inst P (fstPoly z)) :=
    .sigmaSnd hS (Structural.form_inst .nil hP hn) hz
  have hdk := transport_erased .nil (Structural.form_nat .nil) hP hn hk hi hd
  exact ⟨result.val, result.property, hi, hdk,
    .sigmaIntro hS (Structural.form_inst .nil hP hk) hk hdk⟩

/-- The extracted index is unique even for an independently supplied finite
applied-conversion certificate. No equality of fiber proof terms is imposed. -/
theorem extractSigma_unique {P : Ty} {z : Poly} (hz : HasJ [] z (.sigma N P))
    {k : Nat} (hk : PolyConvPlus (scalarLeft (fstPoly z)) (iterationPoly k)) :
    (extractSigma P z hz).count = k :=
  EffectiveNumerals.extractIteration_unique
    (.sigmaFst (Structural.form_nat .nil) (Structural.has_form hz) hz) hk

/-- A downstream actual Joint branch can consume the numeric witness and its
literal preserved evidence. Both dependent binders are simultaneously substituted. -/
theorem extracted_continuation {P R : Ty} {z d : Poly}
    (hz : HasJ [] z (.sigma N P))
    (hd : HasJ [P, N] d (SigmaCompletion.branchType R)) :
    HasJ []
      (SigmaCompletion.branchAt d (inputNumeral (extractSigma P z hz).count) (sndPoly z))
      (inst R (pairPoly (inputNumeral (extractSigma P z hz).count) (sndPoly z))) := by
  let k := (extractSigma P z hz).count
  have hn : HasJ [] (inputNumeral k) N := .hasBase (EffectiveNumerals.old_numeral_has k)
  have hb := (extractSigma P z hz).fiber_has
  have hs : Structural.TypedSubstitution [P,N] []
      (cons (sndPoly z) (cons (inputNumeral k) Poly.var)) := by
    constructor
    intro n C h
    cases h with
    | zero => simpa only [subst_wk_cancel, cons] using hb
    | succ h =>
      cases h with
      | zero => simpa only [subst_wk_cancel, subst_id, cons] using hn
      | succ h => cases h
  have h := Structural.has_subst hd .nil hs
  simpa only [SigmaCompletion.branchAt,
    show SigmaCompletion.branchType R = P01AC.ExtensionalRepair.Structural.branchType R from rfl,
    P01AC.ExtensionalRepair.Structural.branch_type_at] using h

#print axioms transport_source
#print axioms transport_erased
#print axioms extractSigma
#print axioms extractSigma_unique
#print axioms extracted_continuation
end JointCompletion.DependentExtraction
