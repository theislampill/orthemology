import SourceRigidity
import OriginalIdentityNoninhabitation

namespace RigidityDiscriminator
open P01AC P01D
open P01AC.ExtensionalRepair (HasE has_inclusion)
open SourceRigidity
open OpenTermStandardness (T SatPER Conv Arrow arrowPER churchPER zeroTerm succTerm successorNumeral)
open ImportedOpenTermTransport (interp)

set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem zero_eval (η : FullPER.Env) : interp zero η = zeroTerm  := by
  simp [zero, P01AC.EffectiveCompleteness.inputNumeral,
    P01AC.EffectiveCompleteness.iterationPoly,
    P01AC.BooleanPrimitive.succPoly, P01AC.BooleanPrimitive.succBody,
    P01D.abstract, P01D.freeZero, P01D.drop, P01D.pren, P01D.psub,
    interp, ImportedOpenTermTransport.poly, ImportedOpenTermTransport.embed,
    OpenTermStandardness.zeroTerm, OpenTermStandardness.succTerm,
    OpenTermStandardness.inputNumeral, OpenTermStandardness.iterationPoly,
    OpenTermStandardness.succPoly, OpenTermStandardness.succBody,
    OpenTermStandardness.abstract, OpenTermStandardness.freeZero,
    OpenTermStandardness.drop, OpenTermStandardness.pren,
    OpenTermStandardness.psub, OpenTermStandardness.eval]

theorem succ_eval (η : FullPER.Env) :
    interp P01AC.BooleanPrimitive.succPoly η = succTerm  := by
  simp [zero, P01AC.EffectiveCompleteness.inputNumeral,
    P01AC.EffectiveCompleteness.iterationPoly,
    P01AC.BooleanPrimitive.succPoly, P01AC.BooleanPrimitive.succBody,
    P01D.abstract, P01D.freeZero, P01D.drop, P01D.pren, P01D.psub,
    interp, ImportedOpenTermTransport.poly, ImportedOpenTermTransport.embed,
    OpenTermStandardness.zeroTerm, OpenTermStandardness.succTerm,
    OpenTermStandardness.inputNumeral, OpenTermStandardness.iterationPoly,
    OpenTermStandardness.succPoly, OpenTermStandardness.succBody,
    OpenTermStandardness.abstract, OpenTermStandardness.freeZero,
    OpenTermStandardness.drop, OpenTermStandardness.pren,
    OpenTermStandardness.psub, OpenTermStandardness.eval]

-- The generic algebra argument uses standardness, not the special compiler.
theorem peano_rigidity {u : T}
    (uu : Arrow churchPER.rel churchPER.rel u u)
    (uz : churchPER.rel (u ⬝ zeroTerm) zeroTerm)
    (us : ∀ n, churchPER.rel n n → churchPER.rel
      (u ⬝ (succTerm ⬝ n)) (succTerm ⬝ (u ⬝ n))) :
    Arrow churchPER.rel churchPER.rel T.i u := by
  have ss : Arrow churchPER.rel churchPER.rel succTerm succTerm := by
    have h := FullPER.fundamental (has_inclusion P01AC.BooleanPrimitive.succ_has)
      FullPER.Application.emptyEnv FullPER.zeroEnv FullPER.zeroEnv
      FullPER.Application.emptyEnv_admissible ⟨rfl,rfl⟩
    simpa only [FullPER.Application.function_exact, succ_eval] using h
  have numeral : ∀ k, churchPER.rel (u ⬝ successorNumeral k) (successorNumeral k) := by
    intro k
    induction k with
    | zero => exact uz
    | succ k ih =>
      exact churchPER.trans (us _ (OpenTermStandardness.successorNumeral_church k)) (ss _ _ ih)
  intro n m nm
  have mm := churchPER.trans (churchPER.symm nm) nm
  obtain ⟨k, mk⟩ := GenericFoldTransport.church_related_numeral mm
  have um := churchPER.trans (uu _ _ mk) (numeral k)
  have nu := churchPER.trans (churchPER.trans nm mk) (churchPER.symm um)
  exact churchPER.saturated (Conv.i n).symm (.refl _) nu

/-- Exact whole-type validity, for a fixed source polynomial, at arbitrary environments. -/
theorem rigidity_valid (ρ : FullPER.REnv) (η : FullPER.Env) :
    FullPER.F Rigidity ρ η
      (interp P01AC.ExtensionalRepair.ExactScalarFusion.c3 η)
      (interp P01AC.ExtensionalRepair.ExactScalarFusion.c3 η) := by
  simp only [Rigidity, FullPER.F, FullPER.F_arr]
  intro u v uv z z' zz e e' ss
  refine ⟨?_, FullPER.Application.c3_application η u z e,
    FullPER.Application.c3_application η v z' e'⟩
  have uu := (arrowPER churchPER churchPER).trans uv ((arrowPER churchPER churchPER).symm uv)
  apply peano_rigidity uu
  · simpa only [FullPER.Application.church_exact, FullPER.interp_app, FullPER.interp_var, FullPER.cons, zero_eval] using zz.1
  · intro n nn
    simpa only [FullPER.Application.church_exact, FullPER.interp_app, FullPER.interp_var, FullPER.cons, pren, psub, succ_eval] using (ss n n nn).1

/-- Validity also covers two arbitrary related outer environments. -/
theorem rigidity_fundamental (Γ : Tel) : FullPER.Fundamental Γ
    P01AC.ExtensionalRepair.ExactScalarFusion.c3 Rigidity := by
  intro ρ η ξ _ _
  have hc : interp P01AC.ExtensionalRepair.ExactScalarFusion.c3 ξ =
      interp P01AC.ExtensionalRepair.ExactScalarFusion.c3 η :=
    (FullPER.Application.c3_eval ξ).trans (FullPER.Application.c3_eval η).symm
  rw [hc]
  exact rigidity_valid ρ η

theorem rigidity_uninhabited (r : Poly) : ¬ HasE [] r Rigidity := by
  intro h
  have hi := identity_from_rigidityE Ctx.nil h
  rw [result_exact] at hi
  exact HomogeneousOriginalIdentity.original_identity_uninhabited _ hi

theorem no_internal_negation (r : Poly) :
    ¬ HasE [] r (arr Rigidity .bottom) := by
  intro h
  have hr := FullPER.fundamental h FullPER.Application.emptyEnv
    FullPER.zeroEnv FullPER.zeroEnv FullPER.Application.emptyEnv_admissible ⟨rfl,rfl⟩
  rw [FullPER.F_arr] at hr
  exact hr _ _ (rigidity_valid FullPER.Application.emptyEnv FullPER.zeroEnv)

/-- Both failures quantify over every proof polynomial in the unchanged HasE calculus. -/
theorem source_independence :
    (¬ ∃ r, HasE [] r Rigidity) ∧
    (¬ ∃ r, HasE [] r (arr Rigidity .bottom)) :=
  ⟨fun ⟨r, hr⟩ => rigidity_uninhabited r hr,
   fun ⟨r, hr⟩ => no_internal_negation r hr⟩

/-- The smaller original Has calculus inherits both exclusions by inclusion. -/
theorem source_independence_Has :
    (¬ ∃ r, Has [] r Rigidity) ∧
    (¬ ∃ r, Has [] r (arr Rigidity .bottom)) :=
  ⟨fun ⟨r, hr⟩ => rigidity_uninhabited r (has_inclusion hr),
   fun ⟨r, hr⟩ => no_internal_negation r (has_inclusion hr)⟩

#print axioms rigidity_fundamental
#print axioms source_independence
#print axioms source_independence_Has
#print axioms peano_rigidity
#print axioms rigidity_valid
#print axioms rigidity_uninhabited
#print axioms no_internal_negation
end RigidityDiscriminator
