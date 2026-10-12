import JointSigmaExtraction

namespace JointCompletion.ExtractionFidelity
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.Intensional.Plus (PolyConvPlus)
open SigmaCompletion
open P01AC.ExtensionalRepair.InternalGraph
open JointCompletion.DependentExtraction (form_sigma_inv transport_source transport_erased)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

private abbrev form_wk := @Structural.form_wk
private abbrev has_wk := @Structural.has_wk
private abbrev has_form := @Structural.has_form
private abbrev form_inst_source := @Structural.form_inst
private theorem sigma_body_form {Γ A B} (h : FormJ Γ (.sigma A B)) : FormJ (A :: Γ) B :=
  (form_sigma_inv h).2

theorem reconstruction_has {Γ A B z} (hc : CtxJ Γ) (hA : FormJ Γ A)
    (hB : FormJ (A :: Γ) B) (hz : HasJ Γ z (.sigma A B)) :
    HasJ Γ (reconstruct z) (.sigma A B) := by
  have hf := HasJ.sigmaFst hA (.sigma hA hB) hz
  have hb := form_inst_source hc hB hf
  exact .sigmaIntro (.sigma hA hB) hb hf (.sigmaSnd (.sigma hA hB) hb hz)

theorem eta_motive_formed {Γ A B} (hc : CtxJ Γ) (hA : FormJ Γ A)
    (hB : FormJ (A :: Γ) B) : FormJ (.sigma A B :: Γ) (etaMotive (.sigma A B)) := by
  have hS := FormJ.sigma hA hB
  have cw := CtxJ.ext hc hS
  have hw := form_wk hS hc hS
  have hv : HasJ (.sigma A B :: Γ) (.var 0) (wk (.sigma A B)) := .var hw .zero
  have hAw : FormJ (.sigma A B :: Γ) (wk A) := form_wk hA hc hS
  have hBw := sigma_body_form hw
  exact .identity hw hv (reconstruction_has cw hAw hBw hv)

theorem generic_pair_has {Γ A B} (hc : CtxJ Γ) (hA : FormJ Γ A)
    (hB : FormJ (A :: Γ) B) :
    HasJ (B :: A :: Γ) (pairPoly (.var 1) (.var 0)) (wk (wk (.sigma A B))) := by
  have ca := CtxJ.ext hc hA
  have cb := CtxJ.ext ca hB
  have hS := FormJ.sigma hA hB
  have hS2 := form_wk (form_wk hS hc hA) ca hB
  have hA2 := form_wk (form_wk hA hc hA) ca hB
  have ha : HasJ (B :: A :: Γ) (.var 1) (wk (wk A)) := .var hA2 (.succ .zero)
  have hb0 : HasJ (B :: A :: Γ) (.var 0) (wk B) := .var (form_wk hB ca hB) .zero
  have heq : wk (wk (.sigma A B)) = .sigma (wk (wk A))
      (subst (pup (fun n => Poly.var (n+2))) B) := by
    simp only [wk, subst, subst_comp]
    congr 1
    congr 1
    funext n; cases n <;> rfl
  rw [heq] at hS2 ⊢
  exact .sigmaIntro hS2 ((shifted_body_at B).symm ▸ form_wk hB ca hB)
    ha ((shifted_body_at B).symm ▸ hb0)

theorem canonical_eta_branch {Γ A B} (hc : CtxJ Γ) (hA : FormJ Γ A)
    (hB : FormJ (A :: Γ) B) :
    HasJ (B :: A :: Γ) (.atom .i) (branchType (etaMotive (.sigma A B))) := by
  have ca := CtxJ.ext hc hA
  have cb := CtxJ.ext ca hB
  have hp := generic_pair_has hc hA hB
  have hS2 := has_form hp
  have ha2 := form_wk (form_wk hA hc hA) ca hB
  have hr := reconstruction_has cb ha2 (sigma_body_form hS2) hp
  have conv : P01DF.PolyConv (pairPoly (.var 1) (.var 0))
      (reconstruct (pairPoly (.var 1) (.var 0))) :=
    (pair_poly_congr (pair_first _ _) (pair_second _ _)).symm
  have h := HasJ.identityIntro (.identity hS2 hp hr) hp hr (P01AC.Intensional.Plus.polyConv_inclusion conv)
  have eqt : branchType (etaMotive (.sigma A B)) =
      .identity (wk (wk (.sigma A B))) (pairPoly (.var 1) (.var 0))
        (reconstruct (pairPoly (.var 1) (.var 0))) := by
    have hs : subst pairSub (wk (.sigma A B)) = wk (wk (.sigma A B)) := by
      change subst (cons (pairPoly (.var 1) (.var 0)) (fun n => .var (n+2))) (wk (.sigma A B)) = _
      rw [subst_wk_cancel, wk, wk, subst_comp]
      rfl
    change Ty.identity (subst pairSub (wk (.sigma A B))) _ _ = _
    rw [hs]
    rfl
  exact eqt.symm ▸ h

/-- Full Joint Sigma elimination proves propositional eta at the unchanged
input, including arbitrary newly formed dependent fibers. -/
theorem sigma_eta {Γ A B z} (hc : CtxJ Γ) (hA : FormJ Γ A)
    (hB : FormJ (A :: Γ) B) (hz : HasJ Γ z (.sigma A B)) :
    HasJ Γ (.atom .i) (.identity (.sigma A B) z (reconstruct z)) := by
  have h := HasJ.sigmaElim hc hA hB (eta_motive_formed hc hA hB)
    (canonical_eta_branch hc hA hB) hz
  simpa only [eta_motive_at, branchAt, psub] using h

/-- Symmetry uses source J and its erasure, without proof-term uniqueness. -/
theorem identity_sym {Γ X x y e} (hc : CtxJ Γ) (hX : FormJ Γ X)
    (hx : HasJ Γ x X) (hy : HasJ Γ y X) (he : HasJ Γ e (.identity X x y)) :
    HasJ Γ (.atom .i) (.identity X y x) := by
  let P : Ty := .identity (wk X) (.var 0) (pren Nat.succ x)
  have hw := form_wk hX hc hX
  have hP : FormJ (X :: Γ) P := .identity hw (.var hw .zero) (has_wk hx hc hX)
  have at_eq (v : Poly) : inst P v = .identity X v x := by
    simp only [P, inst, subst, subst_wk_cancel, subst_id, psub, cons]
    congr 1
    simpa only [psub_id] using P01DF.Syntactic.polynomial_shift_cancel x v Poly.var
  have base := HasJ.identityIntro (.identity hX hx hx) hx hx (PolyConvPlus.refl x)
  have h := transport_erased hc hX hP hx hy he ((at_eq x).symm ▸ base)
  simpa only [at_eq] using h

/-- Composition preserves the first evidence polynomial by J erasure. -/
theorem identity_trans {Γ X x y z e f} (hc : CtxJ Γ) (hX : FormJ Γ X)
    (hx : HasJ Γ x X) (hy : HasJ Γ y X) (hz : HasJ Γ z X)
    (he : HasJ Γ e (.identity X x y)) (hf : HasJ Γ f (.identity X y z)) :
    HasJ Γ e (.identity X x z) := by
  let P : Ty := .identity (wk X) (pren Nat.succ x) (.var 0)
  have hw := form_wk hX hc hX
  have hP : FormJ (X :: Γ) P := .identity hw (has_wk hx hc hX) (.var hw .zero)
  have at_eq (v : Poly) : inst P v = .identity X x v := by
    simp only [P, inst, subst, subst_wk_cancel, subst_id, psub, cons]
    congr 1
    simpa only [psub_id] using P01DF.Syntactic.polynomial_shift_cancel x v Poly.var
  have h := transport_erased hc hX hP hy hz hf ((at_eq y).symm ▸ he)
  simpa only [at_eq] using h

#print axioms sigma_eta
#print axioms identity_sym
#print axioms identity_trans
end JointCompletion.ExtractionFidelity
