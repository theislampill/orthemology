import RawImages
import Mathlib.Data.Fintype.EquivFin

namespace FiniteRawReview
open FiniteRawObstruction FiniteRawObstruction.Source OrthemologyV2 OrthemologyV3
universe u

/-- Only values actually denoted by terms are subject to the K law. Unreachable
summary states need neither a K law nor a preimage under the summary map. -/
def reachableImage {A : Type u} (q : Term → A) (δ : A → A → A)
    (compositional : ∀ t₁ t, q (.app t₁ t) = δ (q t₁) (q t))
    (conversion : ∀ {t₁ t}, Conv t₁ t → q t₁ = q t) :
    ClosedRawImage { a : A // ∃ t, q t = a } where
  denote := fun t => ⟨q t, t, rfl⟩
  app := fun a b => ⟨δ a.val b.val, by
    obtain ⟨t₁, hs⟩ := a.property
    obtain ⟨t, ht⟩ := b.property
    exact ⟨.app t₁ t, by rw [compositional, hs, ht]⟩⟩
  denote_app := fun t₁ t => Subtype.ext (compositional t₁ t)
  conversion := fun h => Subtype.ext (conversion h)
  surjective := by
    intro a
    obtain ⟨t, ht⟩ := a.property
    exact ⟨t, Subtype.ext ht⟩

/-- An exact, conversion-respecting summary of every raw application is
constant whenever its summary carrier is finite. No whole-carrier surjectivity
is assumed. Finite bounded, restricted, or non-compositional summaries are
outside this theorem. -/
theorem finite_exact_summary_constant {A : Type u} [Finite A]
    (q : Term → A) (δ : A → A → A)
    (compositional : ∀ t₁ t, q (.app t₁ t) = δ (q t₁) (q t))
    (conversion : ∀ {t₁ t}, Conv t₁ t → q t₁ = q t) (t₁ t : Term) :
    q t₁ = q t := by
  letI : Finite { a : A // ∃ t, q t = a } :=
    Finite.of_injective Subtype.val Subtype.val_injective
  let D := reachableImage q δ compositional conversion
  have h := finite_closed_image_no_separation D t₁ t
  exact congrArg Subtype.val h

/-- Partial application does not evade the finite obstruction if every
K-first application and every resulting constant't₁ application is defined. -/
structure PartialKSlice (A : Type u) where
  app : A → A → Option A
  k : A
  encode : A → A
  k_apply : ∀ x, app k x = some (encode x)
  encoded_apply : ∀ x y, app (encode x) y = some x

theorem finite_partial_K_subsingleton {A : Type u} [Finite A]
    (M : PartialKSlice A) : Subsingleton A := by
  have hi : Function.Injective M.encode := by
    intro x y he
    have h := congrArg (fun z => M.app z M.k) he
    change M.app (M.encode x) M.k = M.app (M.encode y) M.k at h
    rw [M.encoded_apply, M.encoded_apply] at h
    exact Option.some.inj h
  obtain ⟨a, ha⟩ := Finite.surjective_of_injective hi M.k
  have hc (x : A) : M.encode x = a := by
    have h := M.k_apply x
    rw [← ha, M.encoded_apply] at h
    exact (Option.some.inj h).symm
  exact ⟨fun x y => hi ((hc x).trans (hc y).symm)⟩

/-- Whole-carrier surjectivity matters: a finite carrier may contain
unreachable junk while satisfying closed compositional conversion soundness. -/
def junkSummary : Term → Bool := fun _ => false
def junkTransition : Bool → Bool → Bool := fun a b => a || b

theorem junk_compositional (t₁ t : Term) :
    junkSummary (.app t₁ t) = junkTransition (junkSummary t₁) (junkSummary t) := rfl

theorem junk_conversion {t₁ t : Term} (_h : Conv t₁ t) :
    junkSummary t₁ = junkSummary t := rfl

theorem junk_not_surjective : ¬ Function.Surjective junkSummary := by
  intro h
  obtain ⟨t, ht⟩ := h true
  cases ht

theorem junk_whole_carrier_K_fails :
    ¬ (∀ x y, junkTransition (junkTransition (junkSummary .k) x) y = x) := by
  intro h
  have e := h false true
  cases e

/-- Compositionality alone is not enough: syntax shape is a nonconstant finite
summary with a total binary transition, but it does not respect conversion. -/
def shapeSummary : Term → Bool
  | .app _ _ => true
  | _ => false

def shapeTransition : Bool → Bool → Bool := fun _ _ => true

theorem shape_compositional (t₁ t : Term) :
    shapeSummary (.app t₁ t) = shapeTransition (shapeSummary t₁) (shapeSummary t) := rfl

theorem shape_nonconstant : shapeSummary .k ≠ shapeSummary (.app .k .k) := by decide

theorem shape_not_conversion_sound :
    ¬ (∀ {t₁ t}, Conv t₁ t → shapeSummary t₁ = shapeSummary t) := by
  intro h
  have e := h (Conv.step (Step.k .k .k))
  cases e

#print axioms finite_exact_summary_constant
#print axioms finite_partial_K_subsingleton
#print axioms junk_not_surjective
#print axioms junk_whole_carrier_K_fails
#print axioms shape_not_conversion_sound
end FiniteRawReview
