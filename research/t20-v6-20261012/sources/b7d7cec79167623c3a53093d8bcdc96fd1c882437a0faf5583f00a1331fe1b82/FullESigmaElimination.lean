/- Full actual-E dependent Sigma elimination using the unchanged, literal
   SigmaCompletion polynomials. No new source rules or eta axiom. -/
import Constructive
import FullEInitiality
namespace SigmaCompletion.FullE
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.InternalGraph
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

private abbrev form_wk := @Structural.form_wk
private abbrev has_wk := @Structural.has_wk
private abbrev has_form := @ClosedProofCanonicalisation.formed
private abbrev form_inst_source := @Structural.form_inst
private abbrev transport_source := @RigidityInitiality.FullE.transport_source
private abbrev sigma_body_form := @RigidityInitiality.FullE.sigma_body_form

theorem reconstruction_has {Γ A B z} (hc : CtxE Γ) (hA : FormE Γ A)
    (hB : FormE (A :: Γ) B) (hz : HasE Γ z (.sigma A B)) :
    HasE Γ (reconstruct z) (.sigma A B) := by
  have hf := HasE.sigmaFst hA (.sigma hA hB) hz
  have hb := form_inst_source hc hB hf
  exact .sigmaIntro (.sigma hA hB) hb hf (.sigmaSnd (.sigma hA hB) hb hz)

theorem identity_sym {Γ X x y e} (hc : CtxE Γ) (hX : FormE Γ X)
    (hx : HasE Γ x X) (hy : HasE Γ y X) (he : HasE Γ e (.identity X x y)) :
    HasE Γ (jPoly (.atom .i) y e) (.identity X y x) := by
  let P : Ty := .identity (wk X) (.var 0) (pren Nat.succ x)
  have cx := CtxE.ext hc hX
  have hw := form_wk hX hc hX
  have hP : FormE (X :: Γ) P := .identity hw (.var hw .zero) (has_wk hx hc hX)
  have at_eq (v : Poly) : inst P v = .identity X v x := by
    simp only [P, inst, subst, subst_wk_cancel, subst_id, psub, cons]
    congr 1
    simpa only [psub_id] using P01DF.Syntactic.polynomial_shift_cancel x v Poly.var
  have base := HasE.identityIntro (.identity hX hx hx) hx hx (P01AC.Intensional.Plus.polyConv_inclusion (P01DF.PolyConv.refl x))
  have h := transport_source hc hX hP hx hy he ((at_eq x).symm ▸ base)
  simpa only [at_eq] using h

theorem branch_has {Γ A B P d a b} (hc : CtxE Γ)
    (hd : HasE (B :: A :: Γ) d (branchType P))
    (ha : HasE Γ a A) (hb : HasE Γ b (inst B a)) :
    HasE Γ (branchAt d a b) (inst P (pairPoly a b)) :=
  Structural.dependent_branch_substitution hc hd ha hb

/-- An actual-E dependent branch and motive acquire elimination at any
actual-E Sigma input from an explicit HasE eta witness. -/
theorem elim_of_eta {Γ A B P d z e} (hc : CtxE Γ) (hA : FormE Γ A)
    (hB : FormE (A :: Γ) B) (hP : FormE (.sigma A B :: Γ) P)
    (hd : HasE (B :: A :: Γ) d (branchType P)) (hz : HasE Γ z (.sigma A B))
    (he : HasE Γ e (.identity (.sigma A B) z (reconstruct z))) :
    HasE Γ (elim d z e) (inst P z) := by
  have hf := HasE.sigmaFst hA (.sigma hA hB) hz
  have hs := HasE.sigmaSnd (.sigma hA hB) (form_inst_source hc hB hf) hz
  have hr := reconstruction_has hc hA hB hz
  exact transport_source hc (.sigma hA hB) hP hr hz
    (identity_sym hc (.sigma hA hB) hz hr he)
    (branch_has hc hd hf hs)


theorem eta_motive_formed {Γ A B} (hc : CtxE Γ) (hA : FormE Γ A)
    (hB : FormE (A :: Γ) B) : FormE (.sigma A B :: Γ) (etaMotive (.sigma A B)) := by
  have hS := FormE.sigma hA hB
  have cw := CtxE.ext hc hS
  have hw := form_wk hS hc hS
  have hv : HasE (.sigma A B :: Γ) (.var 0) (wk (.sigma A B)) := .var hw .zero
  have hAw : FormE (.sigma A B :: Γ) (wk A) := form_wk hA hc hS
  have hBw := sigma_body_form hw
  exact .identity hw hv (reconstruction_has cw hAw hBw hv)

theorem generic_pair_has {Γ A B} (hc : CtxE Γ) (hA : FormE Γ A)
    (hB : FormE (A :: Γ) B) :
    HasE (B :: A :: Γ) (pairPoly (.var 1) (.var 0)) (wk (wk (.sigma A B))) := by
  have ca := CtxE.ext hc hA
  have cb := CtxE.ext ca hB
  have hS := FormE.sigma hA hB
  have hS2 := form_wk (form_wk hS hc hA) ca hB
  have hA2 := form_wk (form_wk hA hc hA) ca hB
  have ha : HasE (B :: A :: Γ) (.var 1) (wk (wk A)) := .var hA2 (.succ .zero)
  have hb0 : HasE (B :: A :: Γ) (.var 0) (wk B) := .var (form_wk hB ca hB) .zero
  have heq : wk (wk (.sigma A B)) = .sigma (wk (wk A))
      (subst (pup (fun n => Poly.var (n+2))) B) := by
    simp only [wk, subst, subst_comp]
    congr 1
    congr 1
    funext n; cases n <;> rfl
  rw [heq] at hS2 ⊢
  exact .sigmaIntro hS2 ((shifted_body_at B).symm ▸ form_wk hB ca hB)
    ha ((shifted_body_at B).symm ▸ hb0)

theorem canonical_eta_branch {Γ A B} (hc : CtxE Γ) (hA : FormE Γ A)
    (hB : FormE (A :: Γ) B) :
    HasE (B :: A :: Γ) (.atom .i) (branchType (etaMotive (.sigma A B))) := by
  have ca := CtxE.ext hc hA
  have cb := CtxE.ext ca hB
  have hp := generic_pair_has hc hA hB
  have hS2 := has_form hp
  have ha2 := form_wk (form_wk hA hc hA) ca hB
  have hr := reconstruction_has cb ha2 (sigma_body_form hS2) hp
  have conv : P01DF.PolyConv (pairPoly (.var 1) (.var 0))
      (reconstruct (pairPoly (.var 1) (.var 0))) :=
    (pair_poly_congr (pair_first _ _) (pair_second _ _)).symm
  have h := HasE.identityIntro (.identity hS2 hp hr) hp hr (P01AC.Intensional.Plus.polyConv_inclusion conv)
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

/-- Input-local eta, separating a pointwise completion obligation from the
    uniform schema. The proof polynomial may depend on this input. -/
def EtaAt (Γ : Tel) (A B : Ty) (z : Poly) : Prop :=
  ∃ e, HasE Γ e (.identity (.sigma A B) z (reconstruct z))

def EliminationAt (Γ : Tel) (A B : Ty) (z : Poly) : Prop :=
  ∀ (P : Ty) (d : Poly), FormE (.sigma A B :: Γ) P →
  HasE (B :: A :: Γ) d (branchType P) →
  ∃ t, HasE Γ t (inst P z) ∧ P01DF.PolyConv t (branchAt d (fstPoly z) (sndPoly z))

def WeakEliminationAt (Γ : Tel) (A B : Ty) (z : Poly) : Prop :=
  ∀ (P : Ty) (d : Poly), FormE (.sigma A B :: Γ) P →
  HasE (B :: A :: Γ) d (branchType P) → ∃ t, HasE Γ t (inst P z)

/-- Exact completion equivalence already at each admissible actual-E input.
    The converse asks only for all formed motives and typed branches. -/
theorem eta_iff_weak_elimination_at {Γ A B z} (hc : CtxE Γ)
    (hA : FormE Γ A) (hB : FormE (A :: Γ) B) (hz : HasE Γ z (.sigma A B)) :
    EtaAt Γ A B z ↔ WeakEliminationAt Γ A B z := by
  constructor
  · rintro ⟨e,he⟩ P d hP hd
    exact ⟨elim d z e, elim_of_eta hc hA hB hP hd hz he⟩
  · intro h
    obtain ⟨e,he⟩ := h (etaMotive (.sigma A B)) (.atom .i)
      (eta_motive_formed hc hA hB) (canonical_eta_branch hc hA hB)
    exact ⟨e, (eta_motive_at _ _) ▸ he⟩

theorem eta_iff_elimination_at {Γ A B z} (hc : CtxE Γ)
    (hA : FormE Γ A) (hB : FormE (A :: Γ) B) (hz : HasE Γ z (.sigma A B)) :
    EtaAt Γ A B z ↔ EliminationAt Γ A B z := by
  constructor
  · rintro ⟨e,he⟩ P d hP hd
    exact ⟨elim d z e, elim_of_eta hc hA hB hP hd hz he, elim_erases d z e⟩
  · intro h
    apply (eta_iff_weak_elimination_at hc hA hB hz).mpr
    intro P d hP hd
    obtain ⟨t, ht, _⟩ := h P d hP hd
    exact ⟨t,ht⟩

/-- Uniform source schema: eta at every actual-E typed Sigma term. -/
def EtaSchema : Prop := ∀ (Γ : Tel) (A B : Ty) (z : Poly),
  CtxE Γ → FormE Γ A → FormE (A :: Γ) B → HasE Γ z (.sigma A B) →
  ∃ e, HasE Γ e (.identity (.sigma A B) z (reconstruct z))

/-- Genuine dependent elimination, with an arbitrary actual-E motive
and branch. The conclusion includes raw erased computation. -/
def EliminationSchema : Prop := ∀ (Γ : Tel) (A B P : Ty) (d z : Poly),
  CtxE Γ → FormE Γ A → FormE (A :: Γ) B → FormE (.sigma A B :: Γ) P →
  HasE (B :: A :: Γ) d (branchType P) → HasE Γ z (.sigma A B) →
  ∃ t, HasE Γ t (inst P z) ∧ P01DF.PolyConv t (branchAt d (fstPoly z) (sndPoly z))

theorem eta_implies_elimination (h : EtaSchema) : EliminationSchema := by
  intro Γ A B P d z hc hA hB hP hd hz
  obtain ⟨e,he⟩ := h Γ A B z hc hA hB hz
  exact ⟨elim d z e,elim_of_eta hc hA hB hP hd hz he,elim_erases d z e⟩

theorem elimination_implies_eta (h : EliminationSchema) : EtaSchema := by
  intro Γ A B z hc hA hB hz
  obtain ⟨e,he,_⟩ := h Γ A B (etaMotive (.sigma A B)) (.atom .i) z hc hA hB
    (eta_motive_formed hc hA hB) (canonical_eta_branch hc hA hB) hz
  exact ⟨e,(eta_motive_at _ _) ▸ he⟩

theorem eta_iff_elimination : EtaSchema ↔ EliminationSchema :=
  ⟨eta_implies_elimination,elimination_implies_eta⟩


/-- Even elimination without a computation requirement suffices for eta. -/
def WeakEliminationSchema : Prop := ∀ (Γ : Tel) (A B P : Ty) (d z : Poly),
  CtxE Γ → FormE Γ A → FormE (A :: Γ) B → FormE (.sigma A B :: Γ) P →
  HasE (B :: A :: Γ) d (branchType P) → HasE Γ z (.sigma A B) →
  ∃ t, HasE Γ t (inst P z)

theorem weak_elimination_implies_eta (h : WeakEliminationSchema) : EtaSchema := by
  intro Γ A B z hc hA hB hz
  obtain ⟨e,he⟩ := h Γ A B (etaMotive (.sigma A B)) (.atom .i) z hc hA hB
    (eta_motive_formed hc hA hB) (canonical_eta_branch hc hA hB) hz
  exact ⟨e,(eta_motive_at _ _) ▸ he⟩

theorem eta_iff_weak_elimination : EtaSchema ↔ WeakEliminationSchema := by
  refine ⟨?_,weak_elimination_implies_eta⟩
  intro h Γ A B P d z hc hA hB hP hd hz
  obtain ⟨t,ht,_⟩ := eta_implies_elimination h Γ A B P d z hc hA hB hP hd hz
  exact ⟨t,ht⟩

/-- Canonical computation also has a typed propositional witness. Both endpoints
are formed and typed independently; raw computation was proved separately. -/
theorem elim_pair_identity {Γ A B P d a b e} (hc : CtxE Γ) (hA : FormE Γ A)
    (hB : FormE (A :: Γ) B) (hP : FormE (.sigma A B :: Γ) P)
    (hd : HasE (B :: A :: Γ) d (branchType P))
    (ha : HasE Γ a A) (hb : HasE Γ b (inst B a))
    (he : HasE Γ e (.identity (.sigma A B) (pairPoly a b) (reconstruct (pairPoly a b)))) :
    HasE Γ (.atom .i) (.identity (inst P (pairPoly a b))
      (elim d (pairPoly a b) e) (branchAt d a b)) := by
  have hp := HasE.sigmaIntro (FormE.sigma hA hB) (form_inst_source hc hB ha) ha hb
  have ht := elim_of_eta hc hA hB hP hd hp he
  have hd' := branch_has hc hd ha hb
  have hf := form_inst_source hc hP hp
  exact .identityIntro (.identity hf ht hd') ht hd'
    (P01AC.Intensional.Plus.polyConv_inclusion (elim_pair_computation d a b e))


#print axioms eta_iff_elimination_at
#print axioms eta_iff_weak_elimination_at
#print axioms elim_of_eta
#print axioms canonical_eta_branch
#print axioms eta_iff_elimination
#print axioms eta_iff_weak_elimination
#print axioms elim_pair_identity
end SigmaCompletion.FullE
