import FullEComputationLaws
import RigidityDiscriminator
namespace RigidityInitiality.FullE.InductionConverse
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem zeroAt_shift (u : Poly) : wk (ZeroAt u) = ZeroAt (pren Nat.succ u) := by
  simp [ZeroAt, wk, subst, N, NBody, arr, pren, psub, zero,
    P01AC.BooleanPrimitive.psub_closed (P01AC.has_scoped (inputNumeral_has 0))]

theorem stepAt_shift (u : Poly) : wk (StepAt u) = StepAt (pren Nat.succ u) := by
  simp [StepAt, wk, subst, N, NBody, arr, pren, psub, pup, psub_comp,
    P01AC.BooleanPrimitive.psub_closed (P01AC.has_scoped succ_has)]

theorem resultAt_shift (u : Poly) : wk (ResultAt u) = ResultAt (pren Nat.succ u) := by
  simp [ResultAt, NT, ident, wk, subst, N, NBody, arr, pren, psub]

/-- External weak section-existence schema at one context. No computation laws. -/
def WeakInductionAt (Γ : Tel) : Prop :=
  ∀ (P : Ty) (p s : Poly), FormE (N :: Γ) P →
    HasE Γ p (inst P zero) → HasE Γ s (dependentStepType P) →
    ∃ t, HasE Γ t (.pi N P)

def WeakInduction : Prop := ∀ Γ, CtxE Γ → WeakInductionAt Γ

def EqFamily (u : Poly) : Ty := .identity N (.app (pren Nat.succ u) (.var 0)) (.var 0)

theorem family_at (u n : Poly) : inst (EqFamily u) n = .identity N (.app u n) n := by
  simp [EqFamily, inst, subst, N_subst, pren, psub, psub_comp, cons, psub_id]

theorem family_shift (u : Poly) : shiftedFamily (EqFamily u) = EqFamily (pren Nat.succ u) := by
  simp [shiftedFamily, EqFamily, subst, N_subst, pren, psub, psub_comp, pup]

theorem family_form {Γ : Tel} {u : Poly} (hc : CtxE Γ) (hu : HasE Γ u NT) :
    FormE (N :: Γ) (EqFamily u) := by
  have cN := CtxE.ext hc (N_form hc)
  have hu1 : HasE (N :: Γ) (pren Nat.succ u) NT := has_wk hu hc (N_form hc)
  have hn : HasE (N :: Γ) (.var 0) N := .var (N_form cN) .zero
  exact .identity (N_form cN)
    (app_has (form_arr (N_form cN) (N_form cN)) (N_form cN) hu1 hn) hn

theorem nat_congr {Γ : Tel} {f x y e : Poly} (hc : CtxE Γ)
    (hf : HasE Γ f NT) (hx : HasE Γ x N) (hy : HasE Γ y N)
    (he : HasE Γ e (.identity N x y)) :
    ∃ d, HasE Γ d (.identity N (.app f x) (.app f y)) := by
  let P : Ty := .identity N (pren Nat.succ (.app f x)) (.app (pren Nat.succ f) (.var 0))
  have cN := CtxE.ext hc (N_form hc)
  have hfx := app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) hf hx
  have hfx1 : HasE (N :: Γ) (pren Nat.succ (.app f x)) N := has_wk hfx hc (N_form hc)
  have hf1 : HasE (N :: Γ) (pren Nat.succ f) NT := has_wk hf hc (N_form hc)
  have hn : HasE (N :: Γ) (.var 0) N := .var (N_form cN) .zero
  have hP : FormE (N :: Γ) P := .identity (N_form cN) hfx1
    (app_has (form_arr (N_form cN) (N_form cN)) (N_form cN) hf1 hn)
  have eq (v : Poly) : inst P v = .identity N (.app f x) (.app f v) := by
    simp [P, inst, subst, N_subst, pren, psub, psub_comp, cons, psub_id]
  have hb : HasE Γ ident (.identity N (.app f x) (.app f x)) :=
    identityIntro_raw (.identity (N_form hc) hfx hfx) hfx hfx (.refl _)
  exact ⟨_, eq y ▸ transport_source hc (N_form hc) hP hx hy he ((eq x).symm ▸ hb)⟩

theorem step_point {Γ : Tel} {u s n e : Poly} (hc : CtxE Γ)
    (hu : HasE Γ u NT) (hs : HasE Γ s (StepAt u)) (hn : HasE Γ n N)
    (he : HasE Γ e (.identity N (.app u n) n)) :
    ∃ d, HasE Γ d (.identity N (.app u (.app succPoly n)) (.app succPoly n)) := by
  have hT := form_arr (N_form hc) (N_form hc)
  have hsucc := succ_has_NT hc
  have hun := app_has hT (N_form hc) hu hn
  have hsn := app_has hT (N_form hc) hsucc hn
  have husn := app_has hT (N_form hc) hu hsn
  have hsun := app_has hT (N_form hc) hsucc hun
  have hsform := stepAt_formed hc hu
  have step : HasE Γ (.app s n) (.identity N (.app u (.app succPoly n)) (.app succPoly (.app u n))) := by
    have h := HasE.piElim hsform (form_inst_source hc (pi_body_form hsform) hn) hs hn
    simpa [StepAt, inst, subst, N_subst, pren, psub, psub_comp, cons, psub_id,
      P01AC.BooleanPrimitive.psub_closed (P01AC.has_scoped succ_has)] using h
  obtain ⟨d, hd⟩ := nat_congr hc hsucc hun hn he
  exact ⟨_, nat_identity_trans hc husn hsun hsn step hd⟩

theorem family_step {Γ : Tel} {u s : Poly} (hc : CtxE Γ)
    (hu : HasE Γ u NT) (hs : HasE Γ s (StepAt u)) :
    ∃ d, HasE Γ d (dependentStepType (EqFamily u)) := by
  let P := EqFamily u
  have hP := family_form hc hu
  have cN := CtxE.ext hc (N_form hc)
  have hQ := successorFamily_form hc hP
  have cP := CtxE.ext cN hP
  have hu1 : HasE (N :: Γ) (pren Nat.succ u) NT := has_wk hu hc (N_form hc)
  have hu2 : HasE (P :: N :: Γ) (pren Nat.succ (pren Nat.succ u)) NT := has_wk hu1 cN hP
  have hs1 : HasE (N :: Γ) (pren Nat.succ s) (StepAt (pren Nat.succ u)) :=
    stepAt_shift u ▸ has_wk hs hc (N_form hc)
  have hs2 := stepAt_shift (pren Nat.succ u) ▸ has_wk hs1 cN hP
  have hn : HasE (P :: N :: Γ) (.var 1) N := .var (N_form cP) (.succ .zero)
  have he0 : HasE (P :: N :: Γ) (.var 0) (wk P) := .var (form_wk hP cN hP) .zero
  have he : HasE (P :: N :: Γ) (.var 0)
      (.identity N (.app (pren Nat.succ (pren Nat.succ u)) (.var 1)) (.var 1)) := by
    simpa [P, EqFamily, wk, subst, N_subst, pren, psub, psub_comp] using he0
  obtain ⟨d, hd⟩ := step_point cP hu2 hs2 hn he
  have hd' : HasE (P :: N :: Γ) d (wk (successorFamily P)) := by
    simpa [P, EqFamily, successorFamily, wk, subst, N_subst, pren, psub, psub_comp, cons,
      P01AC.BooleanPrimitive.psub_closed (P01AC.has_scoped succ_has)] using hd
  have inner := HasE.piIntro (form_arr hP hQ) hd' (scoped_abstract (has_scoped hd'))
  exact ⟨_, HasE.piIntro (.pi (N_form hc) (form_arr hP hQ)) inner
    (scoped_abstract (has_scoped inner))⟩



theorem nat_symE {Γ : Tel} {x y e : Poly} (hc : CtxE Γ)
    (hx : HasE Γ x N) (hy : HasE Γ y N) (he : HasE Γ e (.identity N x y)) :
    ∃ d, HasE Γ d (.identity N y x) := by
  let P : Ty := .identity N (.var 0) (pren Nat.succ x)
  have cN := CtxE.ext hc (N_form hc)
  have hx1 : HasE (N :: Γ) (pren Nat.succ x) N := has_wk hx hc (N_form hc)
  have hP : FormE (N :: Γ) P := .identity (N_form cN) (.var (N_form cN) .zero) hx1
  have eq (v : Poly) : inst P v = .identity N v x := by
    simp [P, inst, subst, N_subst, pren, psub, psub_comp, cons, psub_id]
  have hb := identityIntro_raw (.identity (N_form hc) hx hx) hx hx (.refl _)
  exact ⟨_, eq y ▸ transport_source hc (N_form hc) hP hx hy he ((eq x).symm ▸ hb)⟩

/-- Weak sections at this very context force each supplied Peano endomorphism
    to satisfy the literal rigidity conclusion. -/
theorem endomorphism_rigid {Γ : Tel} {u z s : Poly} (hc : CtxE Γ)
    (ind : WeakInductionAt Γ) (hu : HasE Γ u NT)
    (hz : HasE Γ z (ZeroAt u)) (hs : HasE Γ s (StepAt u)) :
    HasE Γ ident (ResultAt u) := by
  have hP := family_form hc hu
  obtain ⟨d, hd⟩ := family_step hc hu hs
  have seed : HasE Γ z (inst (EqFamily u) zero) := (family_at u zero).symm ▸ hz
  obtain ⟨t, ht⟩ := ind (EqFamily u) z d hP seed hd
  have cN := CtxE.ext hc (N_form hc)
  have hu1 : HasE (N :: Γ) (pren Nat.succ u) NT := has_wk hu hc (N_form hc)
  have ht1 : HasE (N :: Γ) (pren Nat.succ t) (.pi N (EqFamily (pren Nat.succ u))) := by
    simpa [wk, subst, N_subst, EqFamily, pren, psub, psub_comp, pup] using has_wk ht hc (N_form hc)
  have hn : HasE (N :: Γ) (.var 0) N := .var (N_form cN) .zero
  have point : HasE (N :: Γ) (.app (pren Nat.succ t) (.var 0))
      (.identity N (.app (pren Nat.succ u) (.var 0)) (.var 0)) := by
    have hf := has_form ht1
    exact family_at _ _ ▸ HasE.piElim hf (form_inst_source cN (pi_body_form hf) hn) ht1 hn
  have hT := form_arr (N_form hc) (N_form hc)
  have hT1 := form_arr (N_form cN) (N_form cN)
  have hi := i_T hc
  have hi1 := i_T cN
  have left := app_has hT1 (N_form cN) hi1 hn
  have right := app_has hT1 (N_form cN) hu1 hn
  obtain ⟨e, he⟩ := nat_symE cN right hn point
  have link := identityIntro_raw (.identity (N_form cN) left hn) left hn (.i _)
  have body := nat_identity_trans cN left hn right link he
  have hM := FormE.identity (N_form cN) left right
  have hPiM := FormE.pi (N_form hc) hM
  have hh := HasE.piIntro hPiM body (scoped_abstract (has_scoped body))
  exact HasE.piExt (N_form hc) (N_form cN) hT hi hu hM hPiM hh
    (resultAt_formed hc hu) (has_scoped hi) (has_scoped hu)
    (scoped_abstract (has_scoped body))
    (Structural.form_scoped (N_form hc)) (Structural.form_scoped (N_form cN))

/-- Only one generic three-assumption context is needed by the converse. -/
def GenericContext : Tel := [StepAt (.var 1), ZeroAt (.var 0), NT]

theorem extended_induction_implies_rigidity {Γ : Tel} (hc : CtxE Γ)
    (ind : WeakInductionAt ([StepAt (.var 1), ZeroAt (.var 0), NT] ++ Γ)) :
    HasE Γ (abstract (abstract (abstract ident))) Rigidity := by
  have hNT := form_arr (N_form hc) (N_form hc)
  have cT := CtxE.ext hc hNT
  have hu0 : HasE (NT :: Γ) (.var 0) NT :=
    .var (form_arr (N_form cT) (N_form cT)) .zero
  have hZ := zeroAt_formed cT hu0
  have cZ := CtxE.ext cT hZ
  have hu1 : HasE (ZeroAt (.var 0) :: NT :: Γ) (.var 1) NT :=
    .var (form_arr (N_form cZ) (N_form cZ)) (.succ .zero)
  have hS := stepAt_formed cZ hu1
  have cS := CtxE.ext cZ hS
  have hu2 : HasE (StepAt (.var 1) :: ZeroAt (.var 0) :: NT :: Γ) (.var 2) NT :=
    .var (form_arr (N_form cS) (N_form cS)) (.succ (.succ .zero))
  have hz0 : HasE (StepAt (.var 1) :: ZeroAt (.var 0) :: NT :: Γ) (.var 1) (wk (wk (ZeroAt (.var 0)))) :=
    .var (Structural.lookup_form cS (.succ .zero)) (.succ .zero)
  have hz : HasE (StepAt (.var 1) :: ZeroAt (.var 0) :: NT :: Γ) (.var 1) (ZeroAt (.var 2)) := by
    simpa only [zeroAt_shift, pren, psub] using hz0
  have hs0 : HasE (StepAt (.var 1) :: ZeroAt (.var 0) :: NT :: Γ) (.var 0) (wk (StepAt (.var 1))) :=
    .var (form_wk hS cZ hS) .zero
  have hs : HasE (StepAt (.var 1) :: ZeroAt (.var 0) :: NT :: Γ) (.var 0) (StepAt (.var 2)) := by
    simpa only [stepAt_shift, pren, psub] using hs0
  have body := endomorphism_rigid cS ind hu2 hz hs
  have first : HasE (ZeroAt (.var 0) :: NT :: Γ) (abstract ident)
      (arr (StepAt (.var 1)) (ResultAt (.var 1))) := by
    apply HasE.piIntro (form_arr hS (resultAt_formed cZ hu1))
    · simpa only [resultAt_shift, pren, psub] using body
    · exact scoped_abstract trivial
  have second : HasE (NT :: Γ) (abstract (abstract ident))
      (arr (ZeroAt (.var 0)) (arr (StepAt (.var 0)) (ResultAt (.var 0)))) := by
    apply HasE.piIntro (form_arr hZ (form_arr (stepAt_formed cT hu0) (resultAt_formed cT hu0)))
    · have ew (X Y : Ty) : wk (arr X Y) = arr (wk X) (wk Y) := subst_arr X Y _
      simpa only [ew, stepAt_shift, resultAt_shift, pren, psub] using first
    · exact scoped_abstract (scoped_abstract trivial)
  exact HasE.piIntro (rigidity_formed hc) second
    (scoped_abstract (scoped_abstract (scoped_abstract trivial)))


theorem generic_induction_implies_closed_rigidity (ind : WeakInductionAt GenericContext) :
    HasE [] (abstract (abstract (abstract ident))) Rigidity :=
  extended_induction_implies_rigidity CtxE.nil ind


theorem generic_context_formed : CtxE GenericContext := by
  have hT := form_arr (N_form CtxE.nil) (N_form CtxE.nil)
  have cT := CtxE.ext CtxE.nil hT
  have hu : HasE [NT] (.var 0) NT := .var (form_arr (N_form cT) (N_form cT)) .zero
  have cZ := CtxE.ext cT (zeroAt_formed cT hu)
  have hu1 : HasE [ZeroAt (.var 0), NT] (.var 1) NT :=
    .var (form_arr (N_form cZ) (N_form cZ)) (.succ .zero)
  exact CtxE.ext cZ (stepAt_formed cZ hu1)

theorem weak_induction_implies_closed_rigidity (ind : WeakInduction) :
    HasE [] (abstract (abstract (abstract ident))) Rigidity :=
  generic_induction_implies_closed_rigidity (ind GenericContext generic_context_formed)

theorem closed_rigidity_implies_weak_induction {r : Poly} (hr : HasE [] r Rigidity) :
    WeakInduction := by
  intro Γ hc P p s hP hp hs
  exact ⟨sectionPoly p s, section_has hc hP hp hs (Structural.has_closed hr hc)⟩

/-- Exact external admissibility boundary, not a new internal proposition. -/
theorem weak_induction_iff_closed_rigidity :
    WeakInduction ↔ ∃ r, HasE [] r Rigidity :=
  ⟨fun hi => ⟨_, weak_induction_implies_closed_rigidity hi⟩,
   fun ⟨_, hr⟩ => closed_rigidity_implies_weak_induction hr⟩

/-- The general schema already reduces to its one generic context. -/
theorem weak_induction_iff_generic_context :
    WeakInduction ↔ WeakInductionAt GenericContext :=
  ⟨fun hi => hi GenericContext generic_context_formed,
   fun hi => closed_rigidity_implies_weak_induction (generic_induction_implies_closed_rigidity hi)⟩

/-- Inherited closed-R exclusion rules out admissibility of weak induction.
    This is not an internal source negation of the schema. -/
theorem weak_induction_not_admissible : ¬ WeakInduction := by
  intro hi
  exact RigidityDiscriminator.rigidity_uninhabited _ (weak_induction_implies_closed_rigidity hi)

theorem generic_induction_not_admissible : ¬ WeakInductionAt GenericContext := by
  intro hi
  exact RigidityDiscriminator.rigidity_uninhabited _ (generic_induction_implies_closed_rigidity hi)


/-- Closure under well-formed finite telescope extensions is explicit. -/
def ContextualWeakInduction (Γ : Tel) : Prop :=
  ∀ Δ, CtxE (Δ ++ Γ) → WeakInductionAt (Δ ++ Γ)

theorem rigidity_weaken_prefix {Γ : Tel} {r : Poly} (hr : HasE Γ r Rigidity)
    (Δ : Tel) (hc : CtxE (Δ ++ Γ)) : ∃ t, HasE (Δ ++ Γ) t Rigidity := by
  induction Δ with
  | nil => exact ⟨r, hr⟩
  | cons A Δ ih =>
    cases hc with
    | ext hc hA =>
      obtain ⟨t, ht⟩ := ih hc
      exact ⟨pren Nat.succ t, by simpa only [wk, rigidity_subst] using has_wk ht hc hA⟩

theorem contextual_weak_induction_iff_rigidity {Γ : Tel} (hc : CtxE Γ) :
    ContextualWeakInduction Γ ↔ ∃ r, HasE Γ r Rigidity := by
  constructor
  · intro hi
    have hT := form_arr (N_form hc) (N_form hc)
    have cT := CtxE.ext hc hT
    have hu : HasE (NT :: Γ) (.var 0) NT := .var (form_arr (N_form cT) (N_form cT)) .zero
    have cZ := CtxE.ext cT (zeroAt_formed cT hu)
    have hu1 : HasE (ZeroAt (.var 0) :: NT :: Γ) (.var 1) NT :=
      .var (form_arr (N_form cZ) (N_form cZ)) (.succ .zero)
    have cS := CtxE.ext cZ (stepAt_formed cZ hu1)
    exact ⟨_, extended_induction_implies_rigidity hc (hi _ cS)⟩
  · rintro ⟨r, hr⟩ Δ cΔ P p s hP hp hs
    obtain ⟨t, ht⟩ := rigidity_weaken_prefix hr Δ cΔ
    exact ⟨_, section_has cΔ hP hp hs ht⟩

#print axioms contextual_weak_induction_iff_rigidity

#print axioms family_step
#print axioms endomorphism_rigid
#print axioms weak_induction_implies_closed_rigidity
#print axioms closed_rigidity_implies_weak_induction
#print axioms weak_induction_iff_closed_rigidity
#print axioms weak_induction_not_admissible
end RigidityInitiality.FullE.InductionConverse

