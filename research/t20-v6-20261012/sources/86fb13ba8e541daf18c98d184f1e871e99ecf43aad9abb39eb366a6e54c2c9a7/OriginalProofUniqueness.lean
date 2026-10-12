import DependentBranchApplication
import ClosedProofCanonicalisation

namespace P01AC.ExtensionalRepair.ProofUniqueness
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.Intensional.Plus (PolyConvPlus)

set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem identity_formed_inv {Γ A x y} (h : FormE Γ (.identity A x y)) :
    FormE Γ A ∧ HasE Γ x A ∧ HasE Γ y A := by
  cases h with
  | identity hA hx hy => exact ⟨hA,hx,hy⟩

/-- Actual Joint J transports along source identity, including new families. -/
theorem transport_source {Γ : Tel} {X P : Ty} {x y e d : Poly}
    (hc : CtxE Γ) (hX : FormE Γ X) (hP : FormE (X :: Γ) P)
    (hx : HasE Γ x X) (hy : HasE Γ y X)
    (he : HasE Γ e (.identity X x y)) (hd : HasE Γ d (inst P x)) :
    HasE Γ (jPoly d y e) (inst P y) := by
  have hM : FormE (theta Γ X x) (wk P) :=
    Structural.form_wk hP (.ext hc hX) (Structural.form_theta_head hc hX hx)
  have at_eq (v r : Poly) : motiveAt (wk P) v r = inst P v :=
    subst_wk_cancel P r (cons v Poly.var)
  have h := HasE.j hX hM (.identity hX hx hy)
    ((at_eq x (.atom .i)).symm ▸ Structural.form_inst hc hP hx)
    ((at_eq y e).symm ▸ Structural.form_inst hc hP hy) hx hy he
    ((at_eq x (.atom .i)).symm ▸ hd)
  simpa only [at_eq] using h

/-- The original J polynomial erases to d. Hence witness extraction preserves
its literal second-projection term rather than merely choosing a new realizer. -/
theorem transport_erased {Γ : Tel} {X P : Ty} {x y e d : Poly}
    (hc : CtxE Γ) (hX : FormE Γ X) (hP : FormE (X :: Γ) P)
    (hx : HasE Γ x X) (hy : HasE Γ y X)
    (he : HasE Γ e (.identity X x y)) (hd : HasE Γ d (inst P x)) :
    HasE Γ d (inst P y) := by
  have h := transport_source hc hX hP hx hy he hd
  have erasure : PolyConvPlus (jPoly d y e) d :=
    (PolyConvPlus.app (.k _ _) (.refl _)).trans (.k _ _)
  exact .conv (Structural.form_inst hc hP hy) h erasure (ClosedProofCanonicalisation.has_scope hd)


/-- Symmetry uses source J and its erasure, without proof-term uniqueness. -/
theorem identity_sym {Γ X x y e} (hc : CtxE Γ) (hX : FormE Γ X)
    (hx : HasE Γ x X) (hy : HasE Γ y X) (he : HasE Γ e (.identity X x y)) :
    HasE Γ (.atom .i) (.identity X y x) := by
  let P : Ty := .identity (wk X) (.var 0) (pren Nat.succ x)
  have hw := Structural.form_wk hX hc hX
  have hP : FormE (X :: Γ) P := .identity hw (.var hw .zero) (Structural.has_wk hx hc hX)
  have at_eq (v : Poly) : inst P v = .identity X v x := by
    simp only [P, inst, subst, subst_wk_cancel, subst_id, psub, cons]
    congr 1
    simpa only [psub_id] using P01DF.Syntactic.polynomial_shift_cancel x v Poly.var
  have base := HasE.identityIntro (.identity hX hx hx) hx hx (PolyConvPlus.refl x)
  have h := transport_erased hc hX hP hx hy he ((at_eq x).symm ▸ base)
  simpa only [at_eq] using h

/-- Composition preserves the first evidence polynomial by J erasure. -/
theorem identity_trans {Γ X x y z e f} (hc : CtxE Γ) (hX : FormE Γ X)
    (hx : HasE Γ x X) (hy : HasE Γ y X) (hz : HasE Γ z X)
    (he : HasE Γ e (.identity X x y)) (hf : HasE Γ f (.identity X y z)) :
    HasE Γ e (.identity X x z) := by
  let P : Ty := .identity (wk X) (pren Nat.succ x) (.var 0)
  have hw := Structural.form_wk hX hc hX
  have hP : FormE (X :: Γ) P := .identity hw (Structural.has_wk hx hc hX) (.var hw .zero)
  have at_eq (v : Poly) : inst P v = .identity X x v := by
    simp only [P, inst, subst, subst_wk_cancel, subst_id, psub, cons]
    congr 1
    simpa only [psub_id] using P01DF.Syntactic.polynomial_shift_cancel x v Poly.var
  have h := transport_erased hc hX hP hy hz hf ((at_eq y).symm ▸ he)
  simpa only [at_eq] using h


/-- Canonicalization is source J, in arbitrary contexts and newly formed types. -/
theorem canonical_identity {Γ A x y e} (hc : CtxE Γ)
    (he : HasE Γ e (.identity A x y)) :
    HasE Γ (.atom .i) (.identity A x y) := by
  obtain ⟨hA,hx,hy⟩ := identity_formed_inv (ClosedProofCanonicalisation.formed he)
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
theorem identity_contract {Γ A x y e} (hc : CtxE Γ)
    (he : HasE Γ e (.identity A x y)) :
    HasE Γ (.atom .i) (.identity (.identity A x y) e (.atom .i)) := by
  obtain ⟨hA,hx,hy⟩ := identity_formed_inv (ClosedProofCanonicalisation.formed he)
  let H : Ty := .identity (wk A) (pren Nat.succ x) (.var 0)
  have hH : FormE (A :: Γ) H := Structural.form_theta_head hc hA hx
  have hcA := CtxE.ext hc hA
  have hcT : CtxE (theta Γ A x) := Structural.ctx_theta hc hA hx
  have hwH : FormE (theta Γ A x) (wk H) := Structural.form_wk hH hcA hH
  have hv : HasE (theta Γ A x) (.var 0) (wk H) := .var hwH .zero
  have hi : HasE (theta Γ A x) (.atom .i) (wk H) := by
    exact canonical_identity hcT hv
  have hM : FormE (theta Γ A x) (proofMotive A x) := .identity hwH hv hi
  have hxx := HasE.identityIntro (.identity hA hx hx) hx hx (PolyConvPlus.refl x)
  have hbaseF := FormE.identity (.identity hA hx hx) hxx hxx
  have hbase := HasE.identityIntro hbaseF hxx hxx (PolyConvPlus.refl (.atom .i))
  have hiEnd := canonical_identity hc he
  have hEndF := FormE.identity (.identity hA hx hy) he hiEnd
  have hj := HasE.j hA hM (.identity hA hx hy)
    ((proofMotive_at A x x (.atom .i)).symm ▸ hbaseF)
    ((proofMotive_at A x y e).symm ▸ hEndF) hx hy he
    ((proofMotive_at A x x (.atom .i)).symm ▸ hbase)
  have hj' : HasE Γ (jPoly (.atom .i) y e)
      (.identity (.identity A x y) e (.atom .i)) := by
    simpa only [proofMotive_at] using hj
  exact .conv hEndF hj' ((PolyConvPlus.app (.k _ _) (.refl _)).trans (.k _ _)) trivial

/-- Uniqueness of arbitrary source identity proofs, not raw conversion. -/
theorem identity_proof_unique {Γ A x y e f} (hc : CtxE Γ)
    (he : HasE Γ e (.identity A x y)) (hf : HasE Γ f (.identity A x y)) :
    HasE Γ (.atom .i) (.identity (.identity A x y) e f) := by
  have hId := ClosedProofCanonicalisation.formed he
  have hi := canonical_identity hc he
  exact identity_trans hc hId he hi hf (identity_contract hc he)
    (identity_sym hc hId hf hi (identity_contract hc hf))

#print axioms canonical_identity
#print axioms identity_contract
#print axioms identity_proof_unique
end P01AC.ExtensionalRepair.ProofUniqueness
