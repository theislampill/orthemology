import ModalCapacityControl

namespace T20.IndependentGroundReview
open T20.GroundExtension
open T20.GroundExtension.Controls

/-- Positive-length reachability is distinct from the author's reflexive Path. -/
def StrictPath {A : Type} (R : A → A → Prop) (a b : A) : Prop :=
  ∃ c, R a c ∧ Path R c b

theorem old_strict_paths_exact {A : Type} (R : A → A → Prop)
    (B : A → Prop) (a b : A) :
    StrictPath (addRoot R B) (some a) (some b) ↔ StrictPath R a b := by
  constructor
  · rintro ⟨c, hfirst, hrest⟩
    cases c with
    | none => exact False.elim hfirst
    | some c => exact ⟨c, hfirst, (old_path_iff R B c b).mp hrest⟩
  · rintro ⟨c, hfirst, hrest⟩
    exact ⟨some c, hfirst, path_lift hrest⟩

theorem new_root_no_positive_return {A : Type} (R : A → A → Prop)
    (B : A → Prop) : ¬ StrictPath (addRoot R B) none none := by
  rintro ⟨c, hfirst, hrest⟩
  have hc := path_to_new hrest
  subst c
  exact hfirst

theorem production_in_support_preserved {W A : Type}
    (E : W → A → Prop) (S P : W → A → A → Prop) (w₀ : W)
    (h : ∀ w a b, P w a b → S w a b) :
    ∀ w a b, liftProductive P w a b → extSupport E S w₀ w a b := by
  intro w a b hp
  cases a with
  | none => cases b <;> exact False.elim hp
  | some a =>
    cases b with
    | none => exact False.elim hp
    | some b => exact h w a b hp

theorem powerless_extended_finite_full_control :
    Coverage (liftExist finiteE) (extSupport finiteE finiteS false) false ∧
    (∀ w, WellFounded (extSupport finiteE finiteS false w)) ∧
    GroundNecessitates (liftExist finiteE) (extGround finiteE finiteS finiteG false) ∧
    (∃ a b, liftProductive finiteS false a b ∧ liftHolder finiteH a ∧
      liftExist finiteE false a ∧ liftExist finiteE false b) ∧
    ¬ ∃ a, Root (liftExist finiteE) (extSupport finiteE finiteS false) false a ∧
      liftHolder finiteH a := by
  exact ⟨finite_extended_coverage,
    (fun w => wellFounded_preserved (finiteS w) (Root finiteE finiteS false)
      (finite_wellFounded w)), finite_extended_ground_necessitates,
    finite_extended_productive_nonempty, finite_extended_no_original_power⟩

/-- The capacity witness has existing endpoints, actually absent extra, and a
nonactual index. It is not just an uninterpreted capable label. -/
theorem nonactual_capacity_witness_is_real :
    (true : Bool) ≠ false ∧ modalP true ModalNode.ground ModalNode.extra ∧
    modalE true ModalNode.ground ∧ modalE true ModalNode.extra ∧
    ¬ modalE false ModalNode.extra := by
  exact ⟨Bool.noConfusion, Or.inr ⟨rfl, rfl, rfl⟩, True.intro, rfl,
    Bool.noConfusion⟩

#print axioms old_strict_paths_exact
#print axioms new_root_no_positive_return
#print axioms production_in_support_preserved
#print axioms powerless_extended_finite_full_control
#print axioms nonactual_capacity_witness_is_real
end T20.IndependentGroundReview
