import StructuredContextControls

/- Independent controls for the exact frozen structured-context extension.
   These controls do not replace or modify any source rule. -/
namespace StructuredContextReview
open OrthemologyV2 OrthemologyV3 P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N NBody inputNumeral iterationPoly)
open P01AC.ExtensionalRepair.ExactScalarFusion (i)
open P01AC.Intensional.Plus (PolyConvPlus)
open OpenTermStandardness (T Conv iter)
open ImportedOpenTermTransport (interp)
open RawContextUniformity (observe truncate)
open StructuredContextUniformity
open StructuredContextUniformity.Controls
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

/-- Every accepted finite context has a zero tail, regardless of its grammar. -/
theorem environment_tail_zero {Γ : Tel} {ρ : FullPER.REnv}
    {η ξ : FullPER.Env} (h : FullPER.E Γ ρ η ξ) : η Γ.length = .zero := by
  induction Γ generalizing η ξ with
  | nil => exact congrFun h.1 0
  | cons B Γ ih => exact ih h.1

theorem generic_environment_never_admissible (Γ : Tel) (ρ : FullPER.REnv) :
    ¬ FullPER.E Γ ρ T.var T.var := by
  intro h
  have e := environment_tail_zero h
  cases e

theorem structured_truncation_repairs (Γ : Tel) (hΓ : OpaqueTel Γ)
    (ρ : FullPER.REnv) :
    FullPER.E Γ ρ (truncate Γ.length T.var) (truncate Γ.length T.var) :=
  truncated_admissible hΓ T.var ρ

/-- One k precedes the source identity, arbitrary substitutions and evaluations. -/
theorem one_count_for_identity_substitution_evaluation {Γ : Tel} {n : Poly}
    (hΓ : OpaqueTel Γ) (hn : HasE Γ n N) :
    ∃ k, HasE Γ i (.identity N n (inputNumeral k)) ∧
      (∀ σ : Nat → Poly, PolyConvPlus (observe (psub σ n)) (iterationPoly k)) ∧
      ∀ (σ : Nat → Poly) (η : FullPER.Env) (f a : T),
        Conv ((interp (psub σ n) η).app f |>.app a) (iter f a k) := by
  obtain ⟨k,hid,hsub⟩ := opaque_uniform_substitutions hΓ hn
  refine ⟨k,hid,hsub,?_⟩
  intro σ η f a
  have h := ImportedOpenTermTransport.source_plus_sound (hsub σ)
    (OpenTermStandardness.cons a (OpenTermStandardness.cons f η))
  rw [ClosedChurchIdentity.interp_iteration] at h
  simpa only [observe,FullPER.interp_app,FullPER.interp_var,FullPER.interp_ren,
    OpenTermStandardness.cons] using h

/-- Opaque is deliberately only a shape test: it does not certify formation. -/
def unformedOpaque : Ty := .pi (.identity .raw (.var 100) (.var 100)) .raw

theorem unformedOpaque_opaque : Opaque unformedOpaque := .pi (.identity _ _ _) .raw

theorem unformedOpaque_not_formed : ¬ FormE [] unformedOpaque := by
  intro h
  cases h with
  | pi hD hB =>
    cases hD with
    | identity hR hp hq =>
      have hs := ClosedProofCanonicalisation.has_scope hp
      exact Nat.not_lt_zero 100 hs

/-- Negative identity domains may relate nonconvertible endpoints, while their
    proof representatives still reflect Raw conversion. -/
def etaPoly : Poly := .app (.app (.atom .s) (.app (.atom .k) (.var 1))) (.atom .i)

theorem rigid_identity_has_nonraw_endpoints (ρ : FullPER.REnv) :
    Rigid (.identity RawEnd (.var 1) etaPoly) ∧
      FullPER.F (.identity RawEnd (.var 1) etaPoly) ρ T.var .i .i ∧
      ¬ Conv (interp (.var 1) T.var) (interp etaPoly T.var) := by
  exact ⟨.identity _ _ _,⟨rawEnd_eta_related ρ T.var,.refl _,.refl _⟩,
    rawEnd_eta_not_raw⟩

/-- Bottom and a free parameter are not positive opaque entries. -/
theorem bottom_not_opaque : ¬ Opaque .bottom := by
  intro h
  exact opaque_admits h FullPER.Application.emptyEnv FullPER.zeroEnv (Conv.refl .i)

theorem parameter_not_opaque : ¬ Opaque (.param 0) := by
  intro h
  exact opaque_admits h (fun _ _ _ => False) FullPER.zeroEnv (Conv.refl .i)

/-- A proper type-parameter change occurs at the whole telescope, not only
    within an isolated type expression. -/
theorem parameter_context_changes : twkTel [parameterSensitive] ≠ [parameterSensitive] := by
  intro h
  apply parameterSensitive_twk_changes
  exact List.cons.inj h |>.1

abbrev paramEnd : Ty := arr (.param 0) (.param 0)
abbrev paramProof : Ty := .identity paramEnd (.atom .i) (.atom .i)

/-- The parameter-sensitive hypothesis is actually used by typed elimination. -/
def parameterObservation : Poly := .app (.var 0) (.atom .i)

theorem parameterObservation_has : HasE [parameterSensitive] parameterObservation .raw := by
  have hΓ := ctx_inclusion parameterSensitive_original
  have hA : FormE [parameterSensitive] (.param 0) := .param hΓ
  have hEnd : FormE [parameterSensitive] paramEnd :=
    .pi hA (.param (.ext hΓ hA))
  have hi : HasE [parameterSensitive] (.atom .i) paramEnd := .i hA hEnd
  have hId : FormE [parameterSensitive] paramProof := .identity hEnd hi hi
  have he : HasE [parameterSensitive] (.atom .i) paramProof :=
    .identityIntro hId hi hi (.refl _)
  have hFun : FormE [parameterSensitive] parameterSensitive :=
    .pi hId (.raw (.ext hΓ hId))
  exact .piElim hFun (.raw hΓ) (.var hFun .zero) he

def parameterInput (k : Nat) : Poly :=
  .app (.app (.atom .k) (inputNumeral k)) parameterObservation

theorem parameterInput_has (k : Nat) : HasE [parameterSensitive] (parameterInput k) N := by
  have hΓ := parameterSensitive_original
  have he := ctx_inclusion hΓ
  have hN := EffectiveCompleteness.N_form hΓ
  have hR : Form [parameterSensitive] Ty.raw := .raw hΓ
  have hKR := form_inclusion (form_arr hN (form_arr hR hN))
  have hRN := form_inclusion (form_arr hR hN)
  have hk : HasE [parameterSensitive] (.atom .k) (arr N (arr .raw N)) :=
    .k (form_inclusion hN) (form_inclusion hR) hKR
  have hn := Structural.has_closed
    (has_inclusion (EffectiveCompleteness.inputNumeral_has k)) he
  exact .piElim hRN (form_inclusion hN) (.piElim hKR hRN hk hn) parameterObservation_has

theorem parameterInput_count (k : Nat) :
    PolyConvPlus (observe (parameterInput k)) (iterationPoly k) := by
  have h1 := Structural.polyConvPlus_subst
    (PolyConvPlus.k (inputNumeral k) parameterObservation) (fun j => .var (Nat.succ j))
  have h2 := Structural.polyConvPlus_subst h1 (fun j => .var (Nat.succ j))
  have hc : PolyConvPlus (observe (parameterInput k)) (observe (inputNumeral k)) :=
    .app (.app h2 (.refl _)) (.refl _)
  exact hc.trans (RawContextUniformity.numeral_observation k)

theorem parameterInput_actual_source_identity (k : Nat) :
    HasE [parameterSensitive] i (.identity N (parameterInput k) (inputNumeral k)) :=
  opaque_canonicity_at_count (parameterInput_has k) (parameterInput_count k)

/-- General observation-to-identity remains available in [N], without making
    [N] opaque or deriving a numeral observation for its variable. -/
theorem observation_identity_in_nonopaque_context :
    HasE [N] i (.identity N (.var 0) (.var 0)) ∧ ¬ OpaqueTel [N] := by
  refine ⟨identity_of_observation RawContextUniformity.Controls.church_variable_has
    RawContextUniformity.Controls.church_variable_has (.refl _),?_⟩
  intro h
  exact church_not_opaque (h N (by simp))

/-- The higher-order counterexample has a formed source context and a real
    typed source hypothesis; semantic generic inadmissibility is not emptiness. -/
theorem higher_source_context : Ctx [Higher] := by
  have hR : Form [] Ty.raw := .raw .nil
  exact .ext .nil (form_arr (form_arr hR hR) hR)

theorem higher_source_variable : HasE [Higher] (.var 0) Higher := by
  have hΓ := ctx_inclusion higher_source_context
  have hR : FormE [Higher] Ty.raw := .raw hΓ
  have hD : FormE [Higher] RawEnd := .pi hR (.raw (.ext hΓ hR))
  have hH : FormE [Higher] Higher := .pi hD (.raw (.ext hΓ hD))
  exact .var hH .zero

theorem higher_has_closed_inhabitant : HasE [] (.app (.atom .k) (.atom .i)) Higher := by
  have hR : Form [] Ty.raw := .raw .nil
  have hD := form_arr hR hR
  have hH := form_arr hD hR
  have hK := form_arr hR hH
  exact .piElim (form_inclusion hK) (form_inclusion hH)
    (.k (form_inclusion hR) (form_inclusion hD) (form_inclusion hK))
    (.rawAtom (form_inclusion hR))

/-- Unrestricted polynomial substitution can leave the source telescope even
    though the same observed numeral count persists. -/
def escaping : Nat → Poly := fun _ => .var 100

theorem escaping_parameterInput_not_typed :
    ¬ HasE [parameterSensitive] (psub escaping (parameterInput 1)) N := by
  intro h
  have hs := ClosedProofCanonicalisation.has_scope h
  change (True ∧ Scoped 1 (psub escaping (inputNumeral 1))) ∧ (100 < 1 ∧ True) at hs
  exact (by decide : ¬ 100 < 1) hs.2.1

theorem escaping_parameterInput_still_observes :
    PolyConvPlus (observe (psub escaping (parameterInput 1))) (iterationPoly 1) := by
  simpa only [RawContextUniformity.observe_subst,RawContextUniformity.iteration_subst] using
    Structural.polyConvPlus_subst (parameterInput_count 1) (pup (pup escaping))

/-- Direct source-level exclusion: no witness proves the Church hypothesis
    identical to a fixed numeral. This is stronger than merely lacking a count. -/
theorem church_variable_no_source_identity (k : Nat) (r : Poly) :
    ¬ HasE [N] r (.identity N (.var 0) (inputNumeral k)) := by
  intro h
  let η := FullPER.cons (OpenTermStandardness.successorNumeral (k+1)) FullPER.zeroEnv
  have he : FullPER.E [N] FullPER.Application.emptyEnv η η :=
    ⟨⟨rfl,rfl⟩,FullPER.Application.church_nonvacuous _ _ (k+1)⟩
  have rel := (FullPER.fundamental h FullPER.Application.emptyEnv η η
    FullPER.Application.emptyEnv_admissible he).1
  change OpenTermStandardness.churchPER.rel
    (OpenTermStandardness.successorNumeral (k+1)) (interp (inputNumeral k) η) at rel
  have obs := rel (OpenTermStandardness.orbit (.var 1) (.var 0))
    (.var 1) (.var 1) (OpenTermStandardness.orbit_step _ _)
    (.var 0) (.var 0) (OpenTermStandardness.orbit_seed _ _)
  have hk := ImportedOpenTermTransport.source_plus_sound
    (RawContextUniformity.numeral_observation k)
    (OpenTermStandardness.cons (.var 0) (OpenTermStandardness.cons (.var 1) η))
  rw [ClosedChurchIdentity.interp_iteration] at hk
  have hk' : Conv ((interp (inputNumeral k) η).app (.var 1) |>.app (.var 0))
      (iter (.var 1) (.var 0) k) := by
    simpa only [observe,FullPER.interp_app,FullPER.interp_var,FullPER.interp_ren,
      OpenTermStandardness.cons] using hk
  have hc := (OpenTermStandardness.successorNumeral_application
    (k+1) (.var 1) (.var 0)).symm.trans (obs.1.trans hk')
  exact Nat.succ_ne_self k (OpenDevelopments.iter_conv_injective hc)

theorem arbitrary_context_canonicity_is_false :
    ¬ (∀ {Γ : Tel} {n : Poly}, HasE Γ n N →
      ∃ k r, HasE Γ r (.identity N n (inputNumeral k))) := by
  intro h
  obtain ⟨k,r,hr⟩ := h RawContextUniformity.Controls.church_variable_has
  exact church_variable_no_source_identity k r hr

#print axioms church_variable_no_source_identity
#print axioms arbitrary_context_canonicity_is_false
#print axioms environment_tail_zero
#print axioms generic_environment_never_admissible
#print axioms structured_truncation_repairs
#print axioms one_count_for_identity_substitution_evaluation
#print axioms unformedOpaque_not_formed
#print axioms rigid_identity_has_nonraw_endpoints
#print axioms bottom_not_opaque
#print axioms parameter_not_opaque
#print axioms parameter_context_changes
#print axioms parameterObservation_has
#print axioms parameterInput_actual_source_identity
#print axioms observation_identity_in_nonopaque_context
#print axioms higher_source_context
#print axioms higher_source_variable
#print axioms higher_has_closed_inhabitant
#print axioms escaping_parameterInput_not_typed
#print axioms escaping_parameterInput_still_observes
end StructuredContextReview
