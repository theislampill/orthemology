import ClosedChurchIdentity

namespace RawContextUniformity
open OrthemologyV2 OrthemologyV3 P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N NBody iterationPoly inputNumeral)
open P01AC.ExtensionalRepair.ExactScalarFusion (A End i)
open P01AC.Intensional.Plus (PolyConvPlus)
open ImportedOpenTermTransport (interp)
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

/-- All entries are literally the unchanged source Raw type. -/
def rawTel : Nat → Tel
  | 0 => []
  | m+1 => .raw :: rawTel m

@[simp] theorem rawTel_length (m : Nat) : (rawTel m).length = m := by
  induction m with
  | zero => rfl
  | succ m ih => simp [rawTel,ih]

theorem rawTel_ctx (m : Nat) : Ctx (rawTel m) := by
  induction m with
  | zero => exact .nil
  | succ m ih => exact .ext ih (.raw ih)

@[simp] theorem rawTel_twk (m : Nat) : twkTel (rawTel m) = rawTel m := by
  induction m with
  | zero => rfl
  | succ m ih => simpa only [rawTel,twkTel,List.map_cons,twk,trename] using congrArg (Ty.raw :: ·) ih

/-- FullPER requires a zero tail, including for finite nonempty contexts. -/
def truncate (m : Nat) (η : FullPER.Env) : FullPER.Env :=
  fun j => if j < m then η j else .zero

theorem truncate_admissible (m : Nat) (η : FullPER.Env) (ρ : FullPER.REnv) :
    FullPER.E (rawTel m) ρ (truncate m η) (truncate m η) := by
  induction m generalizing η with
  | zero =>
    have hz : truncate 0 η = FullPER.zeroEnv := by funext j; simp [truncate,FullPER.zeroEnv]
    exact ⟨hz,hz⟩
  | succ m ih =>
    have ht : FullPER.tail (truncate (m+1) η) = truncate m (fun j => η (j+1)) := by
      funext j; simp [FullPER.tail,truncate]
    change FullPER.E (rawTel m) ρ _ _ ∧ OpenTermStandardness.Conv _ _
    exact ⟨by rw [ht]; exact ih _,.refl _⟩

theorem interp_agree {p : Poly} {m : Nat} (hp : Scoped m p)
    (η ξ : FullPER.Env) (h : ∀ j, j < m → η j = ξ j) : interp p η = interp p ξ := by
  induction p with
  | var j => exact h j hp
  | atom t => rfl
  | app f a ihf iha => exact congrArg₂ OpenTermStandardness.T.app (ihf hp.1) (iha hp.2)

theorem raw_church {m : Nat} {n : Poly} (hn : HasE (rawTel m) n N) (η : FullPER.Env) :
    OpenTermStandardness.Church (interp n η) := by
  have hs : Scoped m n := by simpa using ClosedProofCanonicalisation.has_scope hn
  rw [interp_agree hs η (truncate m η) (by intro j hj; simp [truncate,hj])]
  exact FullPER.fundamental hn FullPER.Application.emptyEnv _ _
    FullPER.Application.emptyEnv_admissible (truncate_admissible m η _)

/-- Two source binders reserve indices 0 and 1; Raw hypotheses start at 2. -/
def observe (n : Poly) : Poly :=
  .app (.app (pren Nat.succ (pren Nat.succ n)) (.var 1)) (.var 0)

theorem raw_uniform_iteration {m : Nat} {n : Poly} (hn : HasE (rawTel m) n N) :
    ∃ k, PolyConvPlus (observe n) (iterationPoly k) := by
  obtain ⟨k,hk⟩ := OpenTermStandardness.church_standard _
    (raw_church hn (fun j => .var (j+2)))
  refine ⟨k,ClosedScalarInstances.generic_conversion_reflect ?_⟩
  simp only [observe,FullPER.interp_app,FullPER.interp_var,FullPER.interp_ren,
    ClosedScalarInstances.iteration_interp]
  exact hk (.var 1) (.var 0)


def point (n : Poly) : Poly := .app (pren Nat.succ n) (.var 0)

theorem point_has {Γ : Tel} {n : Poly} (hΓ : Ctx Γ) (hn : HasE Γ n N) :
    HasE (End :: Γ) (point n) End := by
  have hE := ClosedChurchIdentity.formEnd hΓ
  have hΓ1 : Ctx (End :: Γ) := .ext hΓ (ExactScalarFusion.End_form hΓ)
  have hw := Structural.has_wk hn (ctx_inclusion hΓ) hE
  have hwN : HasE (End :: Γ) (pren Nat.succ n) N := by
    simpa [wk,subst,N,NBody,End,A,arr] using hw
  exact .piElim (ClosedChurchIdentity.formBody hΓ1)
    (ClosedChurchIdentity.formEnd hΓ1) (ClosedChurchIdentity.body_of_N hΓ1 hwN)
    (.var (ClosedChurchIdentity.formEnd hΓ1) .zero)

theorem observation_has {Γ : Tel} {n : Poly} (hΓ : Ctx Γ) (hn : HasE Γ n N) :
    HasE (A :: End :: Γ) (observe n) A := by
  have hΓ1 : Ctx (End :: Γ) := .ext hΓ (ExactScalarFusion.End_form hΓ)
  have hΓ2 : Ctx (A :: End :: Γ) := .ext hΓ1 (ExactScalarFusion.A_form hΓ1)
  have hw := Structural.has_wk (point_has hΓ hn) (ctx_inclusion hΓ1)
    (form_inclusion (ExactScalarFusion.A_form hΓ1))
  have hwE : HasE (A :: End :: Γ) (pren Nat.succ (point n)) End := by
    simpa [wk,subst,End,A,arr] using hw
  have hp : HasE (A :: End :: Γ) (.app (pren Nat.succ (point n)) (.var 0)) A :=
    .piElim (ClosedChurchIdentity.formEnd hΓ2) (.param (ctx_inclusion hΓ2)) hwE
      (.var (.param (ctx_inclusion hΓ2)) .zero)
  simpa only [point,observe,pren,psub] using hp

/-- Actual source extensionality, retaining every original grammar premise.
    Type-parameter extension fixes the all-Raw telescope literally. -/
theorem identity_of_observation {Γ : Tel} {p q : Poly}
    (hΓ : Ctx Γ) (htwk : twkTel Γ = Γ)
    (hp : HasE Γ p N) (hq : HasE Γ q N)
    (hc : PolyConvPlus (observe p) (observe q)) :
    HasE Γ i (.identity N p q) := by
  have hΓ1 : Ctx (End :: Γ) := .ext hΓ (ExactScalarFusion.End_form hΓ)
  have hΓ2 : Ctx (A :: End :: Γ) := .ext hΓ1 (ExactScalarFusion.A_form hΓ1)
  have sp := ClosedProofCanonicalisation.has_scope hp
  have sq := ClosedProofCanonicalisation.has_scope hq
  have hp1 := point_has hΓ hp
  have hq1 := point_has hΓ hq
  have hp2 := observation_has hΓ hp
  have hq2 := observation_has hΓ hq
  have hf2 : FormE (A :: End :: Γ) (.identity A (observe p) (observe q)) :=
    .identity (.param (ctx_inclusion hΓ2)) hp2 hq2
  have hi2 : HasE (A :: End :: Γ) i (.identity A (observe p) (observe q)) :=
    .identityIntro hf2 hp2 hq2 hc
  have ep : .app (pren Nat.succ (point p)) (.var 0) = observe p := rfl
  have eq : .app (pren Nat.succ (point q)) (.var 0) = observe q := rfl
  have hfpi : FormE (End :: Γ) (.pi A (.identity A (observe p) (observe q))) :=
    .pi (.param (ctx_inclusion hΓ1)) hf2
  have hhpi : HasE (End :: Γ) (abstract i)
      (.pi A (.identity A (observe p) (observe q))) :=
    .piIntro hfpi hi2 (scoped_abstract trivial)
  have hi1 : HasE (End :: Γ) i (.identity End (point p) (point q)) := by
    apply HasE.piExt (.param (ctx_inclusion hΓ1)) (.param (ctx_inclusion hΓ2))
      (ClosedChurchIdentity.formEnd hΓ1) hp1 hq1
    · simpa only [ep,eq] using hf2
    · simpa only [ep,eq] using hfpi
    · simpa only [ep,eq] using hhpi
    · exact .identity (ClosedChurchIdentity.formEnd hΓ1) hp1 hq1
    · exact ClosedProofCanonicalisation.has_scope hp1
    · exact ClosedProofCanonicalisation.has_scope hq1
    · exact scoped_abstract trivial
    · trivial
    · trivial
  have hp0 := ClosedChurchIdentity.body_of_N hΓ hp
  have hq0 := ClosedChurchIdentity.body_of_N hΓ hq
  have hf1 : FormE (End :: Γ) (.identity End (point p) (point q)) :=
    .identity (ClosedChurchIdentity.formEnd hΓ1) hp1 hq1
  have hf0 : FormE Γ (.pi End (.identity End (point p) (point q))) :=
    .pi (ClosedChurchIdentity.formEnd hΓ) hf1
  have hh0 : HasE Γ (abstract i) (.pi End (.identity End (point p) (point q))) :=
    .piIntro hf0 hi1 (scoped_abstract trivial)
  have hi0 : HasE Γ i (.identity NBody p q) := by
    apply HasE.piExt (ClosedChurchIdentity.formEnd hΓ) (ClosedChurchIdentity.formEnd hΓ1)
      (ClosedChurchIdentity.formBody hΓ) hp0 hq0
    · exact hf1
    · exact hf0
    · exact hh0
    · exact .identity (ClosedChurchIdentity.formBody hΓ) hp0 hq0
    · exact sp
    · exact sq
    · exact scoped_abstract trivial
    · exact ⟨trivial,trivial⟩
    · exact ⟨trivial,trivial⟩
  exact HasE.allExt (h := i) (htwk.symm ▸ ClosedChurchIdentity.formBody hΓ)
    (ClosedChurchIdentity.formN hΓ) hp hq
    (htwk.symm ▸ FormE.identity (ClosedChurchIdentity.formBody hΓ) hp0 hq0)
    (htwk.symm ▸ hi0) (.identity (ClosedChurchIdentity.formN hΓ) hp hq)
    sp sq trivial ⟨⟨trivial,trivial⟩,⟨trivial,trivial⟩⟩


theorem numeral_observation (k : Nat) :
    PolyConvPlus (observe (inputNumeral k)) (iterationPoly k) := by
  have hs := has_scoped (EffectiveCompleteness.inputNumeral_has k)
  simpa only [observe,ExactScalarFusion.pren_closed hs] using
    ClosedChurchIdentity.numeral_observation k

/-- One actual source identity under the entire telescope, rather than a
    family of closed-instance semantic equalities. -/
theorem raw_canonicity_at_count {m : Nat} {n : Poly} {k : Nat}
    (hn : HasE (rawTel m) n N)
    (hk : PolyConvPlus (observe n) (iterationPoly k)) :
    HasE (rawTel m) i (.identity N n (inputNumeral k)) :=
  identity_of_observation (rawTel_ctx m) (rawTel_twk m) hn
    (Structural.has_closed (has_inclusion (EffectiveCompleteness.inputNumeral_has k))
      (ctx_inclusion (rawTel_ctx m)))
    (hk.trans (numeral_observation k).symm)

theorem raw_canonicity {m : Nat} {n : Poly} (hn : HasE (rawTel m) n N) :
    ∃ k, HasE (rawTel m) i (.identity N n (inputNumeral k)) := by
  obtain ⟨k,hk⟩ := raw_uniform_iteration hn
  exact ⟨k,raw_canonicity_at_count hn hk⟩

/-- Lift substitutions past the two test variables without changing them. -/
theorem observe_subst (n : Poly) (σ : Nat → Poly) :
    psub (pup (pup σ)) (observe n) = observe (psub σ n) := by
  change Poly.app (.app (psub (pup (pup σ)) (pren Nat.succ (pren Nat.succ n))) (.var 1)) (.var 0) = _
  rw [P01DF.Syntactic.polynomial_shift_substitution,
    P01DF.Syntactic.polynomial_shift_substitution]
  rfl

theorem iteration_subst (k : Nat) (σ : Nat → Poly) :
    psub (pup (pup σ)) (iterationPoly k) = iterationPoly k := by
  induction k with
  | zero => rfl
  | succ k ih => exact congrArg (Poly.app (.var 1)) ih

/-- The same count survives arbitrary source-polynomial replacements of all
    Raw coordinates. No new type-substitution theorem is assumed. -/
theorem raw_uniform_substitutions {m : Nat} {n : Poly} (hn : HasE (rawTel m) n N) :
    ∃ k, HasE (rawTel m) i (.identity N n (inputNumeral k)) ∧
      ∀ σ : Nat → Poly, PolyConvPlus (observe (psub σ n)) (iterationPoly k) := by
  obtain ⟨k,hk⟩ := raw_uniform_iteration hn
  refine ⟨k,raw_canonicity_at_count hn hk,?_⟩
  intro σ
  simpa only [observe_subst,iteration_subst] using
    Structural.polyConvPlus_subst hk (pup (pup σ))


/-- Quantifiers are ordered with one count before every Raw valuation. -/
theorem raw_uniform_evaluation {m : Nat} {n : Poly} (hn : HasE (rawTel m) n N) :
    ∃ k, ∀ (η : FullPER.Env) (f a : OpenTermStandardness.T),
      OpenTermStandardness.Conv ((interp n η).app f |>.app a)
        (OpenTermStandardness.iter f a k) := by
  obtain ⟨k,hk⟩ := raw_uniform_iteration hn
  refine ⟨k,?_⟩
  intro η f a
  have h := ImportedOpenTermTransport.source_plus_sound hk
    (OpenTermStandardness.cons a (OpenTermStandardness.cons f η))
  rw [ClosedChurchIdentity.interp_iteration] at h
  simpa only [observe,FullPER.interp_app,FullPER.interp_var,FullPER.interp_ren,
    OpenTermStandardness.cons] using h

theorem all_raw_eq (Γ : Tel) (h : ∀ A ∈ Γ, A = Ty.raw) : Γ = rawTel Γ.length := by
  induction Γ with
  | nil => rfl
  | cons A Γ ih =>
    have ha : A = Ty.raw := h A (by simp)
    have hg := ih (fun B hb => h B (by simp [hb]))
    simpa only [List.length_cons,rawTel] using congrArg₂ List.cons ha hg

theorem all_raw_canonicity {Γ : Tel} {n : Poly}
    (hΓ : ∀ A ∈ Γ, A = Ty.raw) (hn : HasE Γ n N) :
    ∃ k, HasE Γ i (.identity N n (inputNumeral k)) := by
  have e := all_raw_eq Γ hΓ
  obtain ⟨k,hk⟩ := raw_canonicity (e ▸ hn)
  exact ⟨k,e.symm ▸ hk⟩

#print axioms raw_uniform_evaluation
#print axioms all_raw_canonicity
#print axioms raw_canonicity_at_count
#print axioms raw_canonicity
#print axioms raw_uniform_substitutions
#print axioms raw_church
#print axioms raw_uniform_iteration
#print axioms identity_of_observation
end RawContextUniformity

