import JointSigmaFidelity

namespace JointCompletion.ExtractionFidelity
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness (N inputNumeral)
open P01AC.Intensional.Plus (PolyConvPlus)
open RigidityInitiality (shiftedFamily shifted_inst)
open JointCompletion.DependentExtraction (form_sigma_inv transport_source transport_erased extractSigma)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Dependent pair congruence at arbitrary Joint families. The second component
is transported using the actual identity hypothesis and existing J erasure;
no equality or uniqueness of proof terms is assumed. -/
theorem dependent_pair_congr {Γ : Tel} {X P : Ty} {x y b e : Poly}
    (hc : CtxJ Γ) (hX : FormJ Γ X) (hP : FormJ (X :: Γ) P)
    (hx : HasJ Γ x X) (hy : HasJ Γ y X)
    (he : HasJ Γ e (.identity X x y)) (hb : HasJ Γ b (inst P x)) :
    HasJ Γ (.atom .i) (.identity (.sigma X P) (pairPoly x b) (pairPoly y b)) := by
  let S : Ty := .sigma X P
  let H : Ty := .identity (wk X) (pren Nat.succ x) (.var 0)
  let P2 := shiftedFamily (shiftedFamily P)
  let x2 := pren Nat.succ (pren Nat.succ x)
  let b2 := pren Nat.succ (pren Nat.succ b)
  have hS : FormJ Γ S := .sigma hX hP
  have c1 : CtxJ (X :: Γ) := .ext hc hX
  have hH : FormJ (X :: Γ) H := Structural.form_theta_head hc hX hx
  have ct : CtxJ (theta Γ X x) := Structural.ctx_theta hc hX hx
  have hX2 : FormJ (theta Γ X x) (wk (wk X)) :=
    Structural.form_wk (Structural.form_wk hX hc hX) c1 hH
  have hx2 : HasJ (theta Γ X x) x2 (wk (wk X)) :=
    Structural.has_wk (Structural.has_wk hx hc hX) c1 hH
  have hv : HasJ (theta Γ X x) (.var 1) (wk (wk X)) := .var hX2 (.succ .zero)
  have hep : HasJ (theta Γ X x) (.var 0) (.identity (wk (wk X)) x2 (.var 1)) := by
    have h : HasJ (theta Γ X x) (.var 0) (wk H) :=
      .var (Structural.form_wk hH c1 hH) .zero
    simpa only [H, wk, subst, psub, pren, x2] using h
  have hS2 : FormJ (theta Γ X x) (wk (wk S)) :=
    Structural.form_wk (Structural.form_wk hS hc hX) c1 hH
  have shape : wk (wk S) = .sigma (wk (wk X)) P2 := by
    simp only [S, P2, shiftedFamily, wk, subst]
  have hP2 : FormJ (wk (wk X) :: theta Γ X x) P2 :=
    (form_sigma_inv (shape ▸ hS2)).2
  have hb2 : HasJ (theta Γ X x) b2 (inst P2 x2) := by
    simpa only [P2, x2, b2, shifted_inst] using
      Structural.has_wk (Structural.has_wk hb hc hX) c1 hH
  have hbv := transport_erased ct hX2 hP2 hx2 hv hep hb2
  have left : HasJ (theta Γ X x) (pairPoly x2 b2) (wk (wk S)) :=
    shape.symm ▸ HasJ.sigmaIntro (shape ▸ hS2) (Structural.form_inst ct hP2 hx2) hx2 hb2
  have right : HasJ (theta Γ X x) (pairPoly (.var 1) b2) (wk (wk S)) :=
    shape.symm ▸ HasJ.sigmaIntro (shape ▸ hS2) (Structural.form_inst ct hP2 hv) hv hbv
  let M : Ty := .identity (wk (wk S)) (pairPoly x2 b2) (pairPoly (.var 1) b2)
  have hM : FormJ (theta Γ X x) M := .identity hS2 left right
  have at_eq (v r : Poly) : motiveAt M v r =
      .identity S (pairPoly x b) (pairPoly v b) := by
    simp only [M, motiveAt, subst, subst_wk_cancel, subst_id,
      x2, b2, pairPoly, pren, psub_comp, psub, cons, psub_id]
  have left0 : HasJ Γ (pairPoly x b) S :=
    .sigmaIntro hS (Structural.form_inst hc hP hx) hx hb
  have hby := transport_erased hc hX hP hx hy he hb
  have right0 : HasJ Γ (pairPoly y b) S :=
    .sigmaIntro hS (Structural.form_inst hc hP hy) hy hby
  have base := HasJ.identityIntro (.identity hS left0 left0) left0 left0 (.refl _)
  have h := HasJ.j hX hM (.identity hX hx hy)
    ((at_eq x (.atom .i)).symm ▸ FormJ.identity hS left0 left0)
    ((at_eq y e).symm ▸ FormJ.identity hS left0 right0) hx hy he
    ((at_eq x (.atom .i)).symm ▸ base)
  have target : HasJ Γ (jPoly (.atom .i) y e)
      (.identity S (pairPoly x b) (pairPoly y b)) := by simpa only [at_eq] using h
  exact .conv (.identity hS left0 right0) target
    ((PolyConvPlus.app (.k _ _) (.refl _)).trans (.k _ _)) trivial

/-- Any supplied source identity of first projections gives fidelity of the
whole dependent package, with the same erased second component. -/
theorem repack_identity {Γ X P z y e} (hc : CtxJ Γ) (hX : FormJ Γ X)
    (hP : FormJ (X :: Γ) P) (hz : HasJ Γ z (.sigma X P))
    (hy : HasJ Γ y X) (he : HasJ Γ e (.identity X (fstPoly z) y)) :
    HasJ Γ (.atom .i) (.identity (.sigma X P) z (pairPoly y (sndPoly z))) := by
  have hS := FormJ.sigma hX hP
  have hx := HasJ.sigmaFst hX hS hz
  have hb := HasJ.sigmaSnd hS (Structural.form_inst hc hP hx) hz
  have hr := reconstruction_has hc hX hP hz
  have hby := transport_erased hc hX hP hx hy he hb
  have hnew := HasJ.sigmaIntro hS (Structural.form_inst hc hP hy) hy hby
  exact identity_trans hc hS hz hr hnew (sigma_eta hc hX hP hz)
    (dependent_pair_congr hc hX hP hx hy he hb)

/-- The extracted numeral package is source-identical to the original
package at its actual dependent Sigma type, rather than merely observing
the same numeric first component. -/
theorem extracted_package_identity {P : Ty} {z : Poly} (hz : HasJ [] z (.sigma N P)) :
    HasJ [] (.atom .i) (.identity (.sigma N P) z
      (pairPoly (inputNumeral (extractSigma P z hz).count) (sndPoly z))) :=
  repack_identity .nil (Structural.form_nat .nil)
    (form_sigma_inv (Structural.has_form hz)).2 hz
    (.hasBase (EffectiveNumerals.old_numeral_has _)) (extractSigma P z hz).index_identity

/-- Every formed dependent consumer of the original package keeps its exact
original target. The branch polynomial is unchanged by the final J transport. -/
theorem extracted_continuation_original {P R : Ty} {z d : Poly}
    (hz : HasJ [] z (.sigma N P)) (hR : FormJ [.sigma N P] R)
    (hd : HasJ [P, N] d (SigmaCompletion.branchType R)) :
    HasJ []
      (SigmaCompletion.branchAt d (inputNumeral (extractSigma P z hz).count) (sndPoly z))
      (inst R z) := by
  have hS := Structural.has_form hz
  have hrep := (extractSigma P z hz).representative_has
  have back := identity_sym .nil hS hz hrep (extracted_package_identity hz)
  exact transport_erased .nil hS hR hrep hz back
    (DependentExtraction.extracted_continuation hz hd)

#print axioms repack_identity
#print axioms extracted_package_identity
#print axioms extracted_continuation_original
#print axioms dependent_pair_congr
end JointCompletion.ExtractionFidelity
