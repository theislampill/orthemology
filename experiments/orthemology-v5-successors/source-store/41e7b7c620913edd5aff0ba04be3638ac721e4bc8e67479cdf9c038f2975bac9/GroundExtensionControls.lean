import GroundExtension

namespace T20.GroundExtension.Controls

/-! A nonempty productive base. `false` is the necessary capable agent;
`true` is its contingent actual effect. Worlds are Booleans, actuality is false.
All finite controls are structural interpretations, not possible cosmologies. -/

def finiteE (w a : Bool) : Prop := a = false ∨ w = false
def finiteS (w a b : Bool) : Prop := w = false ∧ a = false ∧ b = true
def finiteG (_ _ _ : Bool) : Prop := False
def finiteH (a : Bool) : Prop := a = false

theorem finite_root : Root finiteE finiteS false false := by
  constructor
  · exact Or.inl rfl
  · intro a h
    cases h.2.2

theorem finite_effect_not_root : ¬ Root finiteE finiteS false true := by
  intro h
  exact h.2 false ⟨rfl, rfl, rfl⟩

theorem finite_roots_necessary :
    ∀ a, Root finiteE finiteS false a → Necessary finiteE a := by
  intro a h w
  cases a with
  | false => exact Or.inl rfl
  | true => exact False.elim (finite_effect_not_root h)

theorem finite_coverage : Coverage finiteE finiteS false := by
  intro a _
  refine ⟨false, finite_root, ?_⟩
  cases a with
  | false => exact Path.refl false
  | true => exact Path.tail (Path.refl false) ⟨rfl, rfl, rfl⟩

theorem finite_productive_nonempty :
    ∃ a b, finiteS false a b ∧ finiteH a ∧ finiteE false a ∧ finiteE false b := by
  exact ⟨false, true, ⟨rfl, rfl, rfl⟩, rfl, Or.inl rfl, Or.inr rfl⟩

theorem finite_productive_agents_capable :
    ∀ w a b, finiteS w a b → finiteH a := by
  intro _ _ _ h
  exact h.2.1

theorem finite_original_power_bearer :
    ∃ a, Root finiteE finiteS false a ∧ finiteH a := by
  exact ⟨false, finite_root, rfl⟩

theorem finite_ground_necessitates : GroundNecessitates finiteE finiteG := by
  intro _ _ _ h
  exact False.elim h

theorem finite_endpoints :
    ∀ w a b, finiteS w a b → finiteE w a ∧ finiteE w b := by
  intro w a b h
  exact ⟨Or.inl h.2.1, Or.inr h.1⟩

theorem finite_accessible_agent (w : Bool) : Acc (finiteS w) false := by
  apply Acc.intro
  intro a h
  cases h.2.2

theorem finite_wellFounded (w : Bool) : WellFounded (finiteS w) := by
  apply WellFounded.intro
  intro a
  cases a with
  | false => exact finite_accessible_agent w
  | true =>
    apply Acc.intro
    intro b h
    have hb : b = false := h.2.1
    subst b
    exact finite_accessible_agent w

theorem finite_extended_coverage :
    Coverage (liftExist finiteE) (extSupport finiteE finiteS false) false :=
  actual_coverage_preserved finiteE finiteS false finite_coverage

theorem finite_extended_ground_necessitates :
    GroundNecessitates (liftExist finiteE)
      (extGround finiteE finiteS finiteG false) :=
  ground_necessitation_preserved finiteE finiteS finiteG false
    finite_ground_necessitates finite_roots_necessary

theorem finite_extended_no_original_power :
    ¬ ∃ a, Root (liftExist finiteE) (extSupport finiteE finiteS false) false a ∧
      liftHolder finiteH a :=
  no_original_power_bearer finiteE finiteS false finiteH

theorem finite_extended_necessary_particular :
    ∃ a, Root (liftExist finiteE) (extSupport finiteE finiteS false) false a ∧
      Necessary (liftExist finiteE) a :=
  necessary_original_particular finiteE finiteS false

/-- Mixed support ancestry does NOT inherit grounding necessitation. -/
theorem mixed_support_countercontrol :
    ∃ a b,
      Path (extSupport finiteE finiteS false false) a b ∧
      liftExist finiteE true a ∧ ¬ liftExist finiteE true b := by
  refine ⟨none, some true, ?_, True.intro, ?_⟩
  · have start : Path (extSupport finiteE finiteS false false) none (some false) :=
      Path.tail (Path.refl none) finite_root
    exact Path.tail start ⟨rfl, rfl, rfl⟩
  · intro h
    cases h with
    | inl h => cases h
    | inr h => cases h

/-! A second control: all-world root uniqueness is not implied by actual coverage.
The old effect exists at both indices, but only has its old supporter actually. -/

def everywhereE (_ _ : Bool) : Prop := True

theorem everywhere_actual_root : Root everywhereE finiteS false false := by
  exact ⟨True.intro, fun _ h => Bool.noConfusion h.2.2⟩

theorem everywhere_roots_necessary :
    ∀ a, Root everywhereE finiteS false a → Necessary everywhereE a := by
  intro _ _ _
  exact True.intro

theorem everywhere_actual_coverage : Coverage everywhereE finiteS false := by
  intro a _
  refine ⟨false, everywhere_actual_root, ?_⟩
  cases a with
  | false => exact Path.refl false
  | true => exact Path.tail (Path.refl false) ⟨rfl, rfl, rfl⟩

theorem other_world_old_root :
    Root (liftExist everywhereE) (extSupport everywhereE finiteS false) true
      (some true) := by
  constructor
  · exact True.intro
  · intro a h
    cases a with
    | none => exact h.2 false ⟨rfl, rfl, rfl⟩
    | some a => cases h.1

/-- Omitting necessary roots can invalidate the new ground's necessitation. -/
def contingentE (w : Bool) (_ : Unit) : Prop := w = false
def emptyS (_ : Bool) (_ _ : Unit) : Prop := False

theorem contingent_root : Root contingentE emptyS false () := by
  exact ⟨rfl, fun _ h => h⟩

theorem contingent_root_not_necessary : ¬ Necessary contingentE () := by
  intro h
  have hbad := h true
  cases hbad

theorem missing_necessity_countercontrol :
    ¬ GroundNecessitates (liftExist contingentE)
      (extGround contingentE emptyS emptyS false) := by
  intro h
  have hbad := h false none (some ()) contingent_root true True.intro
  cases hbad

theorem finite_extended_productive_nonempty :
    ∃ a b, liftProductive finiteS false a b ∧ liftHolder finiteH a ∧
      liftExist finiteE false a ∧ liftExist finiteE false b := by
  exact ⟨some false, some true, ⟨rfl, rfl, rfl⟩, rfl,
    Or.inl rfl, Or.inr rfl⟩

/-- Granting standing power to the original fact does not add actual production. -/
theorem finite_capable_ground_control :
    (∃ a, Necessary (liftExist finiteE) a ∧
      (∀ w, Root (liftExist finiteE) (extSupport finiteE finiteS false) w a) ∧
      liftHolderWith True finiteH a) ∧
    ¬ ∃ a, Root (liftExist finiteE) (extSupport finiteE finiteS false) false a ∧
      ∃ b, liftProductive finiteS false a b :=
  capable_ground_without_actual_production finiteE finiteS finiteS false finiteH

/-! Infinite positive control: original coverage does not require
well-founded subordinate ancestry. There are no cycles, but the chain
... → 3 → 2 → 1 → 0 has predecessors indefinitely. An old root supports
every chain node directly. This control is independent of metaphysical
possibility and does not reject genuine received efficacy. -/

def down (a b : Nat) : Prop := b < a

theorem down_path_le {a b : Nat} (h : Path down a b) : b ≤ a := by
  induction h with
  | refl => exact Nat.le_refl _
  | tail h e ih => exact Nat.le_trans (Nat.le_of_lt e) ih

theorem down_acyclic : Acyclic down := by
  intro a b hab hp
  exact Nat.not_lt_of_ge (down_path_le hp) hab

def infiniteS (_ : Unit) : Option Nat → Option Nat → Prop :=
  addRoot down (fun _ => True)

def infiniteE (_ : Unit) (_ : Option Nat) : Prop := True
def infiniteH (_ : Option Nat) : Prop := True

theorem infinite_root : Root infiniteE infiniteS () none := by
  exact ⟨True.intro, no_edge_to_new down (fun _ => True)⟩

theorem infinite_coverage : Coverage infiniteE infiniteS () := by
  intro a _
  refine ⟨none, infinite_root, ?_⟩
  cases a with
  | none => exact Path.refl none
  | some a => exact Path.tail (Path.refl none) True.intro

theorem infinite_acyclic : Acyclic (infiniteS ()) :=
  acyclic_preserved down (fun _ => True) down_acyclic

theorem infinite_accessible_only_root {a : Option Nat}
    (h : Acc (infiniteS ()) a) : a = none := by
  induction h with
  | intro a h ih =>
    cases a with
    | none => rfl
    | some n =>
      have hbad := ih (some (n + 1)) (Nat.lt_succ_self n)
      cases hbad

theorem infinite_not_wellFounded : ¬ WellFounded (infiniteS ()) := by
  intro h
  have hbad := infinite_accessible_only_root (h.apply (some 0))
  cases hbad

theorem infinite_roots_necessary :
    ∀ a, Root infiniteE infiniteS () a → Necessary infiniteE a := by
  intro _ _ _
  exact True.intro

theorem infinite_productive_agents_capable :
    ∀ w a b, infiniteS w a b → infiniteH a := by
  intro _ _ _ _
  exact True.intro

theorem infinite_extended_coverage :
    Coverage (liftExist infiniteE) (extSupport infiniteE infiniteS ()) () :=
  actual_coverage_preserved infiniteE infiniteS () infinite_coverage

theorem infinite_extended_no_original_power :
    ¬ ∃ a, Root (liftExist infiniteE) (extSupport infiniteE infiniteS ()) () a ∧
      liftHolder infiniteH a :=
  no_original_power_bearer infiniteE infiniteS () infiniteH

end T20.GroundExtension.Controls
