import UniquenessIndependence
namespace IndependenceIndependentReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair
open SourceRigidity RigidityInitiality InternalRecursorPrinciple

example (p : Poly) : ¬ HasE [] p InternalRecursorPrinciple.Uniqueness :=
  internal_uniqueness_uninhabited p
example (p : Poly) : ¬ HasE [] p (arr InternalRecursorPrinciple.Uniqueness .bottom) :=
  internal_uniqueness_negation_uninhabited p
example : (¬ ∃ p, HasE [] p Uniqueness) ∧
    (¬ ∃ p, HasE [] p (arr Uniqueness .bottom)) := internal_uniqueness_independence
example : (¬ ∃ p, Has [] p Uniqueness) ∧
    (¬ ∃ p, Has [] p (arr Uniqueness .bottom)) := internal_uniqueness_independence_Has

-- Composition preserves arbitrary HasE evidence, without assuming structural weakening.
example {Γ : Tel} {X Y Z : Ty} {f g : Poly}
    (hX : Form Γ X) (hY : Form Γ Y) (hZ : Form Γ Z)
    (hf : HasE Γ f (arr Y Z)) (hg : HasE Γ g (arr X Y)) :
    HasE Γ (.app (.app (.atom .s) (.app (.atom .k) f)) g) (arr X Z) :=
  composeE hX hY hZ hf hg
#print axioms internal_uniqueness_independence
end IndependenceIndependentReview
