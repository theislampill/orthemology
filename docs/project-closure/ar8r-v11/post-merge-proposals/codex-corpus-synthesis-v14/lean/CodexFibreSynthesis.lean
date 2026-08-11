/-!
Standalone Lean proposal for the bounded Codex corpus synthesis V14.

This file formalizes elementary fibre-factorization guard repairs.  It creates
no historical theorem identity, novelty credit, repository adoption, source-to-
world bridge, meniscus result, or natural-closure claim.
-/

universe uX uO uQ uG uR

namespace AR8R.CodexCorpusSynthesisV14

variable {X : Type uX} {Obs : Type uO} {QVal : Type uQ}

/-- The target is constant on every fibre of the observation map. -/
def FiberConstant (E : X → Obs) (Q : X → QVal) : Prop :=
  ∀ ⦃x y : X⦄, E x = E y → Q x = Q y

/-- The attained observation image, carrying an explicit witness of attainment. -/
def AttainedImage (E : X → Obs) := {o : Obs // ∃ x : X, E x = o}

/-- Exact decoding only on observations that the declared map actually attains. -/
def FactorsThroughAttainedImage (E : X → Obs) (Q : X → QVal) : Prop :=
  ∃ d : AttainedImage E → QVal,
    ∀ x : X, d ⟨E x, ⟨x, rfl⟩⟩ = Q x

/-- The elementary attained-image factorization theorem. -/
theorem attainedImageFactor_iff_fiberConstant
    (E : X → Obs) (Q : X → QVal) :
    FactorsThroughAttainedImage E Q ↔ FiberConstant E Q := by
  constructor
  · rintro ⟨d, hd⟩ x y hE
    have hsub :
        (⟨E x, ⟨x, rfl⟩⟩ : AttainedImage E) =
        ⟨E y, ⟨y, rfl⟩⟩ := Subtype.ext hE
    calc
      Q x = d ⟨E x, ⟨x, rfl⟩⟩ := (hd x).symm
      _ = d ⟨E y, ⟨y, rfl⟩⟩ := congrArg d hsub
      _ = Q y := hd y
  · intro hQ
    classical
    let d : AttainedImage E → QVal := fun o =>
      Q (Classical.choose o.property)
    refine ⟨d, ?_⟩
    intro x
    exact hQ (Classical.choose_spec (show ∃ y : X, E y = E x from ⟨x, rfl⟩))

/-- Exact decoding through the entire declared observation codomain. -/
def FactorsThroughFullCodomain (E : X → Obs) (Q : X → QVal) : Prop :=
  ∃ d : Obs → QVal, ∀ x : X, d (E x) = Q x

theorem fullFactor_implies_fiberConstant
    (E : X → Obs) (Q : X → QVal) :
    FactorsThroughFullCodomain E Q → FiberConstant E Q := by
  rintro ⟨d, hd⟩ x y hE
  calc
    Q x = d (E x) := (hd x).symm
    _ = d (E y) := congrArg d hE
    _ = Q y := hd y

theorem fiberConstant_fullFactor_of_surjective
    (E : X → Obs) (Q : X → QVal)
    (hE : Function.Surjective E) (hQ : FiberConstant E Q) :
    FactorsThroughFullCodomain E Q := by
  classical
  let representative : Obs → X := fun o => Classical.choose (hE o)
  have hrepresentative : ∀ o : Obs, E (representative o) = o := by
    intro o
    exact Classical.choose_spec (hE o)
  refine ⟨fun o => Q (representative o), ?_⟩
  intro x
  exact hQ (hrepresentative (E x))

theorem fiberConstant_fullFactor_of_nonempty
    (E : X → Obs) (Q : X → QVal) [Nonempty QVal]
    (hQ : FiberConstant E Q) :
    FactorsThroughFullCodomain E Q := by
  classical
  let d : Obs → QVal := fun o =>
    if h : ∃ x : X, E x = o then Q (Classical.choose h)
    else Classical.choice inferInstance
  refine ⟨d, ?_⟩
  intro x
  have h : ∃ y : X, E y = E x := ⟨x, rfl⟩
  simp only [d, dif_pos h]
  exact hQ (Classical.choose_spec h)

theorem fullFactor_implies_extension_guard
    (E : X → Obs) (Q : X → QVal) :
    FactorsThroughFullCodomain E Q →
      (Function.Surjective E ∨ Nonempty QVal) := by
  classical
  rintro ⟨d, hd⟩
  by_cases hObs : Nonempty Obs
  · right
    exact ⟨d (Classical.choice hObs)⟩
  · left
    intro o
    exact (hObs ⟨o⟩).elim

/--
Full-codomain decoding needs fibre constancy plus either attained-image coverage
or an off-range target value.  The quotient/attained-image theorem needs no
such extension guard.
-/
theorem fullFactor_iff_fiberConstant_and_extension_guard
    (E : X → Obs) (Q : X → QVal) :
    FactorsThroughFullCodomain E Q ↔
      FiberConstant E Q ∧ (Function.Surjective E ∨ Nonempty QVal) := by
  constructor
  · intro h
    exact ⟨fullFactor_implies_fiberConstant E Q h,
      fullFactor_implies_extension_guard E Q h⟩
  · rintro ⟨hQ, hE | hNonempty⟩
    · exact fiberConstant_fullFactor_of_surjective E Q hE hQ
    · letI : Nonempty QVal := hNonempty
      exact fiberConstant_fullFactor_of_nonempty E Q hQ

section GuardProduct

variable {Guard : Type uG}

/-- Correct content and a guard product are fibre-constant exactly coordinatewise. -/
theorem pairFiberConstant_iff
    (E : X → Obs) (Q : X → QVal) (G : X → Guard) :
    FiberConstant E (fun x => (Q x, G x)) ↔
      FiberConstant E Q ∧ FiberConstant E G := by
  constructor
  · intro h
    constructor
    · intro x y hE
      exact congrArg Prod.fst (h hE)
    · intro x y hE
      exact congrArg Prod.snd (h hE)
  · rintro ⟨hQ, hG⟩ x y hE
    exact Prod.ext (hQ hE) (hG hE)

end GuardProduct

section Refinement

variable {Refinement : Type uR}

/-- A refinement restores exact target decoding only through joint fibres. -/
theorem jointRefinement_fiberConstant_iff
    (E : X → Obs) (R : X → Refinement) (Q : X → QVal) :
    FiberConstant (fun x => (E x, R x)) Q ↔
      ∀ ⦃x y : X⦄, E x = E y → R x = R y → Q x = Q y := by
  constructor
  · intro h x y hE hR
    exact h (Prod.ext hE hR)
  · intro h x y hER
    exact h (congrArg Prod.fst hER) (congrArg Prod.snd hER)

end Refinement

end AR8R.CodexCorpusSynthesisV14

#print axioms AR8R.CodexCorpusSynthesisV14.fullFactor_iff_fiberConstant_and_extension_guard
#print axioms AR8R.CodexCorpusSynthesisV14.attainedImageFactor_iff_fiberConstant
#print axioms AR8R.CodexCorpusSynthesisV14.pairFiberConstant_iff
#print axioms AR8R.CodexCorpusSynthesisV14.jointRefinement_fiberConstant_iff
