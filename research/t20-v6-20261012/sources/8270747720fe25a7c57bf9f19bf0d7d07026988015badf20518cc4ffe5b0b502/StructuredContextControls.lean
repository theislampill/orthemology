import StructuredContextUniformity
import RawContextControls

namespace StructuredContextUniformity.Controls
open OrthemologyV2 OrthemologyV3 P01D P01AC P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness (N inputNumeral iterationPoly)
open P01AC.ExtensionalRepair.ExactScalarFusion (i)
open P01AC.Intensional.Plus (PolyConvPlus)
open OpenTermStandardness (T Conv)
open ImportedOpenTermTransport (interp)
open RawContextUniformity (observe)

abbrev RawEnd : Ty := arr .raw .raw
abbrev RawPair : Ty := .sigma .raw .raw
abbrev Higher : Ty := arr RawEnd .raw

theorem rawEnd_opaque : Opaque RawEnd := .pi .raw .raw
theorem rawPair_opaque : Opaque RawPair := .sigma .raw .raw

def sampleCtx : Tel := [RawEnd,RawPair,.raw]

theorem sampleCtx_original : Ctx sampleCtx := by
  have h0 : Ctx [Ty.raw] := .ext .nil (.raw .nil)
  have h1 : Ctx [RawPair,Ty.raw] :=
    .ext h0 (.sigma (.raw h0) (.raw (.ext h0 (.raw h0))))
  exact .ext h1 (.pi (.raw h1) (.raw (.ext h1 (.raw h1))))

theorem sampleCtx_opaque : OpaqueTel sampleCtx := by
  intro B hB
  simp only [sampleCtx,List.mem_cons,List.not_mem_nil,or_false] at hB
  rcases hB with rfl | rfl | rfl
  · exact rawEnd_opaque
  · exact rawPair_opaque
  · exact .raw

/-- The positive example really uses typed application and Sigma projection. -/
def rawObservation : Poly := .app (.var 0) (fstPoly (.var 1))

theorem rawObservation_has : HasE sampleCtx rawObservation .raw := by
  have hΓ := ctx_inclusion sampleCtx_original
  have hraw : FormE sampleCtx .raw := .raw hΓ
  have hp : FormE sampleCtx RawPair := .sigma hraw (.raw (.ext hΓ hraw))
  have hf : FormE sampleCtx RawEnd := .pi hraw (.raw (.ext hΓ hraw))
  exact .piElim hf hraw (.var hf .zero)
    (.sigmaFst hraw hp (.var hp (.succ .zero)))

def structuredInput : Poly := .app (.app (.atom .k) (.atom .i)) rawObservation

theorem structuredInput_has : HasE sampleCtx structuredInput N := by
  have hΓ := sampleCtx_original
  have he := ctx_inclusion hΓ
  have hN := EffectiveCompleteness.N_form hΓ
  have hR : Form sampleCtx Ty.raw := .raw hΓ
  have hk : HasE sampleCtx (.atom .k) (arr N (arr .raw N)) :=
    .k (form_inclusion hN) (form_inclusion hR)
      (form_inclusion (form_arr hN (form_arr hR hN)))
  have hi := Structural.has_closed ClosedChurchIdentity.Controls.iTyping he
  have hki : HasE sampleCtx (.app (.atom .k) (.atom .i)) (arr .raw N) :=
    .piElim (form_inclusion (form_arr hN (form_arr hR hN)))
      (form_inclusion (form_arr hR hN)) hk hi
  exact .piElim (form_inclusion (form_arr hR hN)) (form_inclusion hN)
    hki rawObservation_has

theorem structuredInput_count :
    PolyConvPlus (observe structuredInput) (iterationPoly 1) := by
  change PolyConvPlus
    (.app (.app (.app (.app (.atom .k) (.atom .i)) _) (.var 1)) (.var 0)) _
  exact (PolyConvPlus.app (PolyConvPlus.app (.k _ _) (.refl _)) (.refl _)).trans
    (.app (.i _) (.refl _))

theorem structuredInput_identity :
    HasE sampleCtx i (.identity N structuredInput (inputNumeral 1)) :=
  opaque_canonicity_at_count structuredInput_has structuredInput_count

theorem every_sample_church_uniform {n : Poly} (hn : HasE sampleCtx n N) :
    ∃ k, HasE sampleCtx i (.identity N n (inputNumeral k)) :=
  opaque_canonicity sampleCtx_opaque hn

/-- The class includes genuinely varying type-parameter syntax in a negative
    identity domain; literal twk invariance is therefore not its premise. -/
def parameterSensitive : Ty :=
  .pi (.identity (arr (.param 0) (.param 0)) (.atom .i) (.atom .i)) .raw

theorem parameterSensitive_opaque : Opaque parameterSensitive :=
  .pi (.identity _ _ _) .raw

theorem parameterSensitive_twk_changes : twk parameterSensitive ≠ parameterSensitive := by
  intro h
  cases h

theorem parameterSensitive_original : Ctx [parameterSensitive] := by
  have ha : Form [] (Ty.param 0) := .param .nil
  have he := form_arr ha ha
  have hi : Has [] (.atom .i) (arr (.param 0) (.param 0)) := .i ha he
  have hid := Form.identity he hi hi
  exact .ext .nil (.pi hid (.raw (.ext .nil hid)))

theorem parameterSensitive_uniform {n : Poly} (hn : HasE [parameterSensitive] n N) :
    ∃ k, HasE [parameterSensitive] i (.identity N n (inputNumeral k)) := by
  apply opaque_canonicity _ hn
  intro B hb
  exact (List.mem_singleton.mp hb).symm ▸ parameterSensitive_opaque

theorem empty_to_church_opaque : Opaque (.pi .bottom N) := .emptyPi N

/-- A strict countercontrol to using Raw→Raw as a Raw-reflecting Pi domain.
    Eta expansion is pointwise convertible, but not Raw-convertible. -/
def etaVariable : T := .app (.app .s (.app .k (.var 1))) .i

theorem etaVariable_apply (x : T) : Conv (.app etaVariable x) (.app (.var 1) x) :=
  (Conv.s _ _ _).trans (.app (.k _ _) (.i _))

theorem rawEnd_eta_related (ρ : FullPER.REnv) (η : FullPER.Env) :
    FullPER.F RawEnd ρ η (.var 1) etaVariable := by
  intro x y hxy
  exact (Conv.app (.refl _) hxy).trans (etaVariable_apply y).symm

theorem var_normal (j : Nat) : OpenDevelopments.Normal (.var j) := by
  intro t h; cases h; rfl

theorem etaVariable_normal : OpenDevelopments.Normal etaVariable := by
  intro t h
  cases h with
  | app hf ha =>
    cases ha
    cases hf with
    | app hf ha =>
      cases hf
      cases ha with
      | app hk hv => cases hk; cases hv; rfl

theorem variable_application_normal {x : T} (j : Nat)
    (hx : OpenDevelopments.Normal x) : OpenDevelopments.Normal (.app (.var j) x) := by
  intro t h
  cases h with
  | app hf ha => cases hf; exact congrArg (T.app (.var j)) (hx _ ha)

theorem rawEnd_eta_not_raw : ¬ Conv (.var 1) etaVariable := by
  intro h
  have e := OpenDevelopments.normal_unique (var_normal 1) etaVariable_normal h
  cases e

theorem rawEnd_not_rigid : ¬ Rigid RawEnd := by
  intro h
  exact rawEnd_eta_not_raw (rigid_reflects h FullPER.Application.emptyEnv FullPER.zeroEnv
    (rawEnd_eta_related _ _))

theorem higher_generic_variable_not_admissible (ρ : FullPER.REnv) (η : FullPER.Env) :
    ¬ FullPER.F Higher ρ η (.var 0) (.var 0) := by
  intro h
  have hc := h (.var 1) etaVariable (rawEnd_eta_related ρ η)
  have e := OpenDevelopments.normal_unique
    (variable_application_normal 0 (var_normal 1))
    (variable_application_normal 0 etaVariable_normal) hc
  have e' := T.app.inj e |>.2
  cases e'

theorem higher_not_opaque : ¬ Opaque Higher := by
  intro h
  exact higher_generic_variable_not_admissible FullPER.Application.emptyEnv FullPER.zeroEnv
    (opaque_admits h _ _ (.refl _))

/-- The original n:N boundary is still excluded, for its checked reason. -/
theorem church_not_opaque : ¬ Opaque N := by
  intro h
  exact RawContextUniformity.Controls.variable_no_count
    (opaque_uniform_iteration (Γ := [N]) (by intro B hb; have e : B = N := List.mem_singleton.mp hb; exact e.symm ▸ h)
      RawContextUniformity.Controls.church_variable_has)

#print axioms rawObservation_has
#print axioms structuredInput_identity
#print axioms every_sample_church_uniform
#print axioms parameterSensitive_opaque
#print axioms parameterSensitive_original
#print axioms parameterSensitive_uniform
#print axioms empty_to_church_opaque
#print axioms rawEnd_eta_not_raw
#print axioms higher_generic_variable_not_admissible
#print axioms rawEnd_not_rigid
#print axioms higher_not_opaque
#print axioms church_not_opaque
end StructuredContextUniformity.Controls
