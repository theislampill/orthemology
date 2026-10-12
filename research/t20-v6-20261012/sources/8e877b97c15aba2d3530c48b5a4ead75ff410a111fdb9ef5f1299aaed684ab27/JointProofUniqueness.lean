import JointSigmaFidelity

namespace JointCompletion.ProofUniqueness
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.Intensional.Plus (PolyConvPlus)
open ExtractionFidelity
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem identity_formed_inv {Γ A x y} (h : FormJ Γ (.identity A x y)) :
    FormJ Γ A ∧ HasJ Γ x A ∧ HasJ Γ y A := by
  cases h with
  | formBase h => cases h with | identity hA hx hy => exact ⟨.formBase hA, .hasBase hx, .hasBase hy⟩
  | identity hA hx hy => exact ⟨hA,hx,hy⟩

/-- Canonicalization is source J, in arbitrary contexts and newly formed types. -/
theorem canonical_identity {Γ A x y e} (hc : CtxJ Γ)
    (he : HasJ Γ e (.identity A x y)) :
    HasJ Γ (.atom .i) (.identity A x y) := by
  obtain ⟨hA,hx,hy⟩ := identity_formed_inv (Structural.has_form he)
  exact identity_sym hc hA hy hx (identity_sym hc hA hx hy he)

def proofMotive (A : Ty) (x : Poly) : Ty :=
  .identity (wk (.identity (wk A) (pren Nat.succ x) (.var 0))) (.var 0) (.atom .i)

theorem proofMotive_at (A : Ty) (x y e : Poly) :
    motiveAt (proofMotive A x) y e = .identity (.identity A x y) e (.atom .i) := by
  simp only [proofMotive, motiveAt, subst, psub, cons]
  rw [subst_wk_cancel]
  simp only [subst, subst_wk_cancel, subst_id, psub, cons]
  congr 2
  simpa only [psub_id] using P01DF.Syntactic.polynomial_shift_cancel x y Poly.var

/-- Every identity witness is propositionally equal to the canonical witness. -/
theorem identity_contract {Γ A x y e} (hc : CtxJ Γ)
    (he : HasJ Γ e (.identity A x y)) :
    HasJ Γ (.atom .i) (.identity (.identity A x y) e (.atom .i)) := by
  obtain ⟨hA,hx,hy⟩ := identity_formed_inv (Structural.has_form he)
  let H : Ty := .identity (wk A) (pren Nat.succ x) (.var 0)
  have hH : FormJ (A :: Γ) H := Structural.form_theta_head hc hA hx
  have hcA := CtxJ.ext hc hA
  have hcT : CtxJ (theta Γ A x) := Structural.ctx_theta hc hA hx
  have hwH : FormJ (theta Γ A x) (wk H) := Structural.form_wk hH hcA hH
  have hv : HasJ (theta Γ A x) (.var 0) (wk H) := .var hwH .zero
  have hi : HasJ (theta Γ A x) (.atom .i) (wk H) := by
    exact canonical_identity hcT hv
  have hM : FormJ (theta Γ A x) (proofMotive A x) := .identity hwH hv hi
  have hxx := HasJ.identityIntro (.identity hA hx hx) hx hx (PolyConvPlus.refl x)
  have hbaseF := FormJ.identity (.identity hA hx hx) hxx hxx
  have hbase := HasJ.identityIntro hbaseF hxx hxx (PolyConvPlus.refl (.atom .i))
  have hiEnd := canonical_identity hc he
  have hEndF := FormJ.identity (.identity hA hx hy) he hiEnd
  have hj := HasJ.j hA hM (.identity hA hx hy)
    ((proofMotive_at A x x (.atom .i)).symm ▸ hbaseF)
    ((proofMotive_at A x y e).symm ▸ hEndF) hx hy he
    ((proofMotive_at A x x (.atom .i)).symm ▸ hbase)
  have hj' : HasJ Γ (jPoly (.atom .i) y e)
      (.identity (.identity A x y) e (.atom .i)) := by
    simpa only [proofMotive_at] using hj
  exact .conv hEndF hj' ((PolyConvPlus.app (.k _ _) (.refl _)).trans (.k _ _)) trivial

/-- Uniqueness of arbitrary source identity proofs, not raw conversion. -/
theorem identity_proof_unique {Γ A x y e f} (hc : CtxJ Γ)
    (he : HasJ Γ e (.identity A x y)) (hf : HasJ Γ f (.identity A x y)) :
    HasJ Γ (.atom .i) (.identity (.identity A x y) e f) := by
  have hId := Structural.has_form he
  have hi := canonical_identity hc he
  exact identity_trans hc hId he hi hf (identity_contract hc he)
    (identity_sym hc hId hf hi (identity_contract hc hf))

#print axioms canonical_identity
#print axioms identity_contract
#print axioms identity_proof_unique
end JointCompletion.ProofUniqueness
