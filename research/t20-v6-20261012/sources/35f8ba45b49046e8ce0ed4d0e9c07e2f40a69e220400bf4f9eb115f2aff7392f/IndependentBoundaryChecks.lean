import RawContextControls

/- Independent boundary checks on the exact frozen extension. No author files
   or inherited modules are modified by this review. -/
namespace RawContextReview
open OrthemologyV2 OrthemologyV3 P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N inputNumeral iterationPoly)
open P01AC.ExtensionalRepair.ExactScalarFusion (i)
open P01AC.Intensional.Plus (PolyConvPlus)
open OpenTermStandardness (T Conv iter)
open ImportedOpenTermTransport (interp)
open RawContextUniformity
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

/-- Every accepted finite environment, at every type, has its literal zero tail. -/
theorem environment_tail_zero {Γ : Tel} {ρ : FullPER.REnv}
    {η ξ : FullPER.Env} (h : FullPER.E Γ ρ η ξ) : η Γ.length = .zero := by
  induction Γ generalizing η ξ with
  | nil => exact congrFun h.1 0
  | cons A Γ ih => exact ih h.1

/-- Dropping the truncation step really is invalid, even with only Raw entries. -/
theorem generic_environment_not_admissible (m : Nat) (ρ : FullPER.REnv) :
    ¬ FullPER.E (rawTel m) ρ T.var T.var := by
  intro h
  have e := environment_tail_zero h
  cases e

/-- The actual truncate bridge repairs exactly that obstruction. -/
theorem truncated_environment_is_admissible (m : Nat) (ρ : FullPER.REnv) :
    FullPER.E (rawTel m) ρ (truncate m T.var) (truncate m T.var) :=
  truncate_admissible m T.var ρ

/-- One common count covers the source identity, every syntactic substitution,
    and every subsequent open-term valuation of every substituted endpoint. -/
theorem same_count_everywhere {m : Nat} {n : Poly} (hn : HasE (rawTel m) n N) :
    ∃ k, HasE (rawTel m) i (.identity N n (inputNumeral k)) ∧
      (∀ σ : Nat → Poly, PolyConvPlus (observe (psub σ n)) (iterationPoly k)) ∧
      ∀ (σ : Nat → Poly) (η : FullPER.Env) (f a : T),
        Conv ((interp (psub σ n) η).app f |>.app a) (iter f a k) := by
  obtain ⟨k, hid, hsub⟩ := raw_uniform_substitutions hn
  refine ⟨k, hid, hsub, ?_⟩
  intro σ η f a
  have h := ImportedOpenTermTransport.source_plus_sound (hsub σ)
    (OpenTermStandardness.cons a (OpenTermStandardness.cons f η))
  rw [ClosedChurchIdentity.interp_iteration] at h
  simpa only [observe,FullPER.interp_app,FullPER.interp_var,FullPER.interp_ren,
    OpenTermStandardness.cons] using h

/-- Nonvacuity at every numeral count and every genuine finite Raw coordinate. -/
def erasedNumeral (k j : Nat) : Poly :=
  .app (.app (.atom .k) (inputNumeral k)) (.var j)

theorem erasedNumeral_has (k : Nat) {m j : Nat} (hj : j < m) :
    HasE (rawTel m) (erasedNumeral k j) N := by
  have hn := Structural.has_closed (has_inclusion (EffectiveCompleteness.inputNumeral_has k))
    (ctx_inclusion (rawTel_ctx m))
  have hs : Scoped m (inputNumeral k) := scoped_mono
    (has_scoped (EffectiveCompleteness.inputNumeral_has k)) (Nat.zero_le m)
  apply HasE.conv (ClosedChurchIdentity.formN (rawTel_ctx m)) hn
    (PolyConvPlus.k (inputNumeral k) (.var j)).symm
  simpa only [rawTel_length] using And.intro (And.intro trivial hs) hj

theorem erasedNumeral_count (k j : Nat) :
    PolyConvPlus (observe (erasedNumeral k j)) (iterationPoly k) := by
  have h1 := Structural.polyConvPlus_subst
    (PolyConvPlus.k (inputNumeral k) (.var j)) (fun j => .var (Nat.succ j))
  have h := Structural.polyConvPlus_subst h1 (fun j => .var (Nat.succ j))
  have hc : PolyConvPlus (observe (erasedNumeral k j)) (observe (inputNumeral k)) :=
    .app (.app h (.refl (.var 1))) (.refl (.var 0))
  exact hc.trans (numeral_observation k)

theorem erasedNumeral_identity (k : Nat) {m j : Nat} (hj : j < m) :
    HasE (rawTel m) i (.identity N (erasedNumeral k j) (inputNumeral k)) :=
  raw_canonicity_at_count (erasedNumeral_has k hj) (erasedNumeral_count k j)

/-- An unrestricted substitution can escape the original telescope's scope. -/
def escapingSubstitution : Nat → Poly := fun _ => .var 100

theorem escaped_endpoint_not_typed :
    ¬ HasE (rawTel 1) (psub escapingSubstitution Controls.opaqueInput) N := by
  intro h
  have hs := ClosedProofCanonicalisation.has_scope h
  change (True ∧ True) ∧ 100 < 1 at hs
  exact (by decide : ¬ 100 < 1) hs.2

/-- Nevertheless its observation keeps the original count, so conversion
    preservation cannot be conflated with HasE substitution admissibility. -/
theorem escaped_observation_count :
    PolyConvPlus (observe (psub escapingSubstitution Controls.opaqueInput))
      (iterationPoly 1) := by
  simpa only [observe_subst,iteration_subst] using
    Structural.polyConvPlus_subst Controls.opaqueInput_count
      (pup (pup escapingSubstitution))

theorem unrestricted_substitution_typing_is_false :
    ¬ (∀ {m : Nat} {n : Poly}, HasE (rawTel m) n N →
      ∀ σ : Nat → Poly, HasE (rawTel m) (psub σ n) N) := by
  intro h
  exact escaped_endpoint_not_typed (h Controls.opaqueInput_has escapingSubstitution)

/-- Observation reflection is genuinely generic. Soundness at a single
    collapsed valuation has no unrestricted syntactic converse. -/
theorem nongeneric_semantic_reflection_is_false :
    ¬ (∀ {p q : Poly}, Conv (interp p FullPER.zeroEnv) (interp q FullPER.zeroEnv) →
      PolyConvPlus p q) := by
  intro h
  have hc := ImportedOpenTermTransport.source_plus_sound
    (h (p := .var 0) (q := .var 1) (.refl .zero)) T.var
  have h0 : OpenDevelopments.Normal (.var 0) := by intro u hu; cases hu; rfl
  have h1 : OpenDevelopments.Normal (.var 1) := by intro u hu; cases hu; rfl
  have e := OpenDevelopments.normal_unique h0 h1 hc
  cases e

/-- A Church-typed hypothesis is not source-identical to any fixed numeral,
    regardless of the identity witness. This tests source identity, not just
    the stronger generic-observation premise used by the author's control. -/
theorem church_variable_no_numeral_identity (k : Nat) (r : Poly) :
    ¬ HasE [N] r (.identity N (.var 0) (inputNumeral k)) := by
  intro h
  let η := FullPER.cons (OpenTermStandardness.successorNumeral (k+1)) FullPER.zeroEnv
  have he : FullPER.E [N] FullPER.Application.emptyEnv η η :=
    ⟨⟨rfl,rfl⟩, FullPER.Application.church_nonvacuous _ _ (k+1)⟩
  have rel := (FullPER.fundamental h FullPER.Application.emptyEnv η η
    FullPER.Application.emptyEnv_admissible he).1
  change OpenTermStandardness.churchPER.rel
    (OpenTermStandardness.successorNumeral (k+1)) (interp (inputNumeral k) η) at rel
  have obs := rel (OpenTermStandardness.orbit (.var 1) (.var 0))
    (.var 1) (.var 1) (OpenTermStandardness.orbit_step _ _)
    (.var 0) (.var 0) (OpenTermStandardness.orbit_seed _ _)
  have hk := ImportedOpenTermTransport.source_plus_sound (numeral_observation k)
    (OpenTermStandardness.cons (.var 0) (OpenTermStandardness.cons (.var 1) η))
  rw [ClosedChurchIdentity.interp_iteration] at hk
  have hk' : Conv ((interp (inputNumeral k) η).app (.var 1) |>.app (.var 0))
      (iter (.var 1) (.var 0) k) := by
    simpa only [observe,FullPER.interp_app,FullPER.interp_var,FullPER.interp_ren,
      OpenTermStandardness.cons] using hk
  have hc := (OpenTermStandardness.successorNumeral_application (k+1) (.var 1) (.var 0)).symm.trans
    (obs.1.trans hk')
  have e := OpenDevelopments.iter_conv_injective hc
  exact Nat.succ_ne_self k e

theorem arbitrary_context_source_canonicity_is_false :
    ¬ (∀ {Γ : Tel} {n : Poly}, HasE Γ n N →
      ∃ k r, HasE Γ r (.identity N n (inputNumeral k))) := by
  intro h
  obtain ⟨k,r,hr⟩ := h Controls.church_variable_has
  exact church_variable_no_numeral_identity k r hr

/-- Extensional source identity is not raw conversion, in an all-Raw context. -/
theorem closed_fragment_still_raw_distinct :
    HasE (rawTel 0) i (.identity N (.atom .i) (.atom P01R.skk)) ∧
      ¬ PolyConvPlus (.atom .i) (.atom P01R.skk) :=
  ClosedChurchIdentity.Controls.source_equal_raw_distinct

#print axioms environment_tail_zero
#print axioms generic_environment_not_admissible
#print axioms same_count_everywhere
#print axioms erasedNumeral_identity
#print axioms escaped_endpoint_not_typed
#print axioms escaped_observation_count
#print axioms unrestricted_substitution_typing_is_false
#print axioms nongeneric_semantic_reflection_is_false
#print axioms church_variable_no_numeral_identity
#print axioms arbitrary_context_source_canonicity_is_false
#print axioms closed_fragment_still_raw_distinct
end RawContextReview
