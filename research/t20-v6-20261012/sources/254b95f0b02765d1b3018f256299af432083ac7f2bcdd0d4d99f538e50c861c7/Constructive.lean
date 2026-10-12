import Initiality
namespace SigmaCompletion
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.ExtensionalRepair
open RigidityInitiality
open P01AC.ExtensionalRepair.InternalGraph
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def reconstruct (z : Poly) := pairPoly (fstPoly z) (sndPoly z)
def pairSub : Nat → Poly := cons (pairPoly (.var 1) (.var 0)) (fun n => .var (n+2))
def branchType (P : Ty) := subst pairSub P
def branchAt (d a b : Poly) := psub (cons b (cons a Poly.var)) d

theorem reconstruction_has {Γ A B z} (hc : Ctx Γ) (hA : Form Γ A)
    (hB : Form (A :: Γ) B) (hz : Has Γ z (.sigma A B)) :
    Has Γ (reconstruct z) (.sigma A B) := by
  have hf := Has.sigmaFst hA (.sigma hA hB) hz
  have hb := form_inst_source hc hB hf
  exact .sigmaIntro (.sigma hA hB) hb hf (.sigmaSnd (.sigma hA hB) hb hz)

theorem identity_sym {Γ X x y e} (hc : Ctx Γ) (hX : Form Γ X)
    (hx : Has Γ x X) (hy : Has Γ y X) (he : HasE Γ e (.identity X x y)) :
    HasE Γ (jPoly (.atom .i) y e) (.identity X y x) := by
  let P : Ty := .identity (wk X) (.var 0) (pren Nat.succ x)
  have cx := Ctx.ext hc hX
  have hw := form_wk hX hc hX
  have hP : Form (X :: Γ) P := .identity hw (.var hw .zero) (has_wk hx hc hX)
  have at_eq (v : Poly) : inst P v = .identity X v x := by
    simp only [P, inst, subst, subst_wk_cancel, subst_id, psub, cons]
    congr 1
    simpa only [psub_id] using P01DF.Syntactic.polynomial_shift_cancel x v Poly.var
  have base := Has.identityIntro (.identity hX hx hx) hx hx (P01DF.PolyConv.refl x)
  have h := transport_source hc hX hP hx hy he ((at_eq x).symm ▸ has_inclusion base)
  simpa only [at_eq] using h

theorem pair_substitution {Γ A B a b} (hc : Ctx Γ)
    (ha : Has Γ a A) (hb : Has Γ b (inst B a)) :
    MixedSubstitution (B :: A :: Γ) Γ (cons b (cons a Poly.var)) Ty.param := by
  refine ⟨fun _ => .param hc, ?_⟩
  intro n C h
  cases h with
  | zero => simpa only [mixed_param, subst_wk_cancel, cons] using hb
  | succ h =>
    cases h with
    | zero => simpa only [mixed_param, subst_wk_cancel, subst_id, cons] using ha
    | succ h => simpa only [mixed_param, subst_wk_cancel, subst_id, cons] using
        (Has.var (lookup_form hc h) h)

theorem branch_type_at (P : Ty) (a b : Poly) :
    subst (cons b (cons a Poly.var)) (branchType P) = inst P (pairPoly a b) := by
  rw [branchType, subst_comp]
  congr 1
  funext n; cases n <;> rfl

theorem branch_has {Γ A B P d a b} (hc : Ctx Γ)
    (hd : Has (B :: A :: Γ) d (branchType P))
    (ha : Has Γ a A) (hb : Has Γ b (inst B a)) :
    Has Γ (branchAt d a b) (inst P (pairPoly a b)) := by
  have h := has_mixed hd hc (pair_substitution hc ha hb)
  simpa only [mixed_param, branch_type_at] using h

def elim (d z e : Poly) := jPoly (branchAt d (fstPoly z) (sndPoly z)) z
  (jPoly (.atom .i) (reconstruct z) e)

/-- An original-source dependent branch and motive acquire elimination at any
original-source Sigma input from an explicit HasE eta witness. -/
theorem elim_of_eta {Γ A B P d z e} (hc : Ctx Γ) (hA : Form Γ A)
    (hB : Form (A :: Γ) B) (hP : Form (.sigma A B :: Γ) P)
    (hd : Has (B :: A :: Γ) d (branchType P)) (hz : Has Γ z (.sigma A B))
    (he : HasE Γ e (.identity (.sigma A B) z (reconstruct z))) :
    HasE Γ (elim d z e) (inst P z) := by
  have hf := Has.sigmaFst hA (.sigma hA hB) hz
  have hs := Has.sigmaSnd (.sigma hA hB) (form_inst_source hc hB hf) hz
  have hr := reconstruction_has hc hA hB hz
  exact transport_source hc (.sigma hA hB) hP hr hz
    (identity_sym hc (.sigma hA hB) hz hr he)
    (has_inclusion (branch_has hc hd hf hs))


theorem j_erases (d y e : Poly) : P01DF.PolyConv (jPoly d y e) d :=
  (P01DF.PolyConv.app (.k _ _) (.refl _)).trans (.k _ _)

theorem psub_rel (p : Poly) {σ τ : Nat → Poly}
    (h : ∀ n, P01DF.PolyConv (σ n) (τ n)) :
    P01DF.PolyConv (psub σ p) (psub τ p) := by
  induction p with
  | var n => exact h n
  | atom t => exact .refl _
  | app f x hf hx => exact .app hf hx

theorem elim_erases (d z e : Poly) :
    P01DF.PolyConv (elim d z e) (branchAt d (fstPoly z) (sndPoly z)) := j_erases _ _ _

/-- Canonical computation is raw source SKI conversion, regardless of the eta
proof supplied; no UIP or proof equality is used. -/
theorem elim_pair_computation (d a b e : Poly) :
    P01DF.PolyConv (elim d (pairPoly a b) e) (branchAt d a b) := by
  apply (elim_erases _ _ _).trans
  apply psub_rel
  intro n
  cases n with
  | zero => exact pair_second a b
  | succ n => cases n with
    | zero => exact pair_first a b
    | succ n => exact .refl _

def etaMotive (S : Ty) : Ty := .identity (wk S) (.var 0) (reconstruct (.var 0))

theorem eta_motive_formed {Γ A B} (hc : Ctx Γ) (hA : Form Γ A)
    (hB : Form (A :: Γ) B) : Form (.sigma A B :: Γ) (etaMotive (.sigma A B)) := by
  have hS := Form.sigma hA hB
  have cw := Ctx.ext hc hS
  have hw := form_wk hS hc hS
  have hv : Has (.sigma A B :: Γ) (.var 0) (wk (.sigma A B)) := .var hw .zero
  have hAw : Form (.sigma A B :: Γ) (wk A) := form_wk hA hc hS
  have hBw := sigma_body_form hw
  exact .identity hw hv (reconstruction_has cw hAw hBw hv)

theorem eta_motive_at (S : Ty) (z : Poly) :
    inst (etaMotive S) z = .identity S z (reconstruct z) := by
  simp only [etaMotive, inst, subst, subst_wk_cancel, subst_id]
  rfl

theorem shifted_body_at (B : Ty) :
    inst (subst (pup (fun n => Poly.var (n+2))) B) (.var 1) = wk B := by
  rw [inst, subst_comp]
  congr 1
  funext n; cases n <;> rfl

theorem generic_pair_has {Γ A B} (hc : Ctx Γ) (hA : Form Γ A)
    (hB : Form (A :: Γ) B) :
    Has (B :: A :: Γ) (pairPoly (.var 1) (.var 0)) (wk (wk (.sigma A B))) := by
  have ca := Ctx.ext hc hA
  have cb := Ctx.ext ca hB
  have hS := Form.sigma hA hB
  have hS2 := form_wk (form_wk hS hc hA) ca hB
  have hA2 := form_wk (form_wk hA hc hA) ca hB
  have ha : Has (B :: A :: Γ) (.var 1) (wk (wk A)) := .var hA2 (.succ .zero)
  have hb0 : Has (B :: A :: Γ) (.var 0) (wk B) := .var (form_wk hB ca hB) .zero
  have heq : wk (wk (.sigma A B)) = .sigma (wk (wk A))
      (subst (pup (fun n => Poly.var (n+2))) B) := by
    simp only [wk, subst, subst_comp]
    congr 1
    congr 1
    funext n; cases n <;> rfl
  rw [heq] at hS2 ⊢
  exact .sigmaIntro hS2 ((shifted_body_at B).symm ▸ form_wk hB ca hB)
    ha ((shifted_body_at B).symm ▸ hb0)

theorem pair_poly_congr {a a' b b'} (ha : P01DF.PolyConv a a')
    (hb : P01DF.PolyConv b b') : P01DF.PolyConv (pairPoly a b) (pairPoly a' b') :=
  .app (.app (.refl _) (.app (.refl _) (.app (.refl _) ha))) (.app (.refl _) hb)

theorem canonical_eta_branch {Γ A B} (hc : Ctx Γ) (hA : Form Γ A)
    (hB : Form (A :: Γ) B) :
    Has (B :: A :: Γ) (.atom .i) (branchType (etaMotive (.sigma A B))) := by
  have ca := Ctx.ext hc hA
  have cb := Ctx.ext ca hB
  have hp := generic_pair_has hc hA hB
  have hS2 := has_form hp
  have ha2 := form_wk (form_wk hA hc hA) ca hB
  have hr := reconstruction_has cb ha2 (sigma_body_form hS2) hp
  have conv : P01DF.PolyConv (pairPoly (.var 1) (.var 0))
      (reconstruct (pairPoly (.var 1) (.var 0))) :=
    (pair_poly_congr (pair_first _ _) (pair_second _ _)).symm
  have h := Has.identityIntro (.identity hS2 hp hr) hp hr conv
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

/-- Uniform source schema: eta at every original-source typed Sigma term. -/
def EtaSchema : Prop := ∀ (Γ : Tel) (A B : Ty) (z : Poly),
  Ctx Γ → Form Γ A → Form (A :: Γ) B → Has Γ z (.sigma A B) →
  ∃ e, HasE Γ e (.identity (.sigma A B) z (reconstruct z))

/-- Genuine dependent elimination, with an arbitrary original-source motive
and branch. The conclusion includes raw erased computation. -/
def EliminationSchema : Prop := ∀ (Γ : Tel) (A B P : Ty) (d z : Poly),
  Ctx Γ → Form Γ A → Form (A :: Γ) B → Form (.sigma A B :: Γ) P →
  Has (B :: A :: Γ) d (branchType P) → Has Γ z (.sigma A B) →
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
  Ctx Γ → Form Γ A → Form (A :: Γ) B → Form (.sigma A B :: Γ) P →
  Has (B :: A :: Γ) d (branchType P) → Has Γ z (.sigma A B) →
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
theorem elim_pair_identity {Γ A B P d a b e} (hc : Ctx Γ) (hA : Form Γ A)
    (hB : Form (A :: Γ) B) (hP : Form (.sigma A B :: Γ) P)
    (hd : Has (B :: A :: Γ) d (branchType P))
    (ha : Has Γ a A) (hb : Has Γ b (inst B a))
    (he : HasE Γ e (.identity (.sigma A B) (pairPoly a b) (reconstruct (pairPoly a b)))) :
    HasE Γ (.atom .i) (.identity (inst P (pairPoly a b))
      (elim d (pairPoly a b) e) (branchAt d a b)) := by
  have hp := Has.sigmaIntro (Form.sigma hA hB) (form_inst_source hc hB ha) ha hb
  have ht := elim_of_eta hc hA hB hP hd hp he
  have hd' := has_inclusion (branch_has hc hd ha hb)
  have hf := form_inclusion (form_inst_source hc hP hp)
  exact .identityIntro (.identity hf ht hd') ht hd'
    (P01AC.Intensional.Plus.polyConv_inclusion (elim_pair_computation d a b e))

#print axioms elim_pair_identity
#print axioms eta_iff_weak_elimination
#print axioms canonical_eta_branch
#print axioms elim_pair_computation
#print axioms eta_iff_elimination
#print axioms elim_of_eta
end SigmaCompletion
