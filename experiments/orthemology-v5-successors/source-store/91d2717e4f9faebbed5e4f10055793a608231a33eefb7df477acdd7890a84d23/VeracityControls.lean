import VeracityBoundary
set_option synthInstance.maxSize 100000

/-! Finite relative interpretations. In particular weak_stress_A/C do NOT
preserve the full T17 perfect-knowledge/profile or an independently established
genuine-ownership interpretation. All five coordinates are Boolean in fixtures;
the general theorem keeps their sorts independently parameterized. -/
namespace VeracityBoundary.Controls

abbrev Fixture := Model Bool Bool Bool Bool Bool

def fixture (knowledge awareness control defect fits : Bool) : Fixture where
  asserts := fun _ _ _ q => q = false
  trueAt := fun _ q => q = true
  knowsFalse := fun _ _ q => knowledge = true ∧ q = false
  aware := fun _ _ _ _ => awareness = true
  deliberate := fun _ _ _ => control = true
  exercise := id
  actual := fun _ _ _ => True
  fitting := fun _ _ _ => fits = true
  shortcoming := fun _ _ _ => defect = true

def dropK := fixture false true true false true
def dropA := fixture true false true false true
def dropC := fixture true true false false true
def dropD := fixture true true true false true
def dropN := fixture true true true true true
def dropP := fixture true true true true false

def FalseOwned (m : Fixture) : Prop :=
  m.asserts false false false false ∧ ¬ m.trueAt false false

theorem deletion_K :
    A dropK false ∧ C dropK false ∧ D dropK false ∧ N dropK false ∧ P dropK false ∧
    ExerciseBridge dropK false ∧ Factive dropK false ∧
    ¬ K dropK false ∧ FalseOwned dropK ∧ ¬ Veracity dropK false := by
  simp only [A, C, D, N, P, ExerciseBridge, Factive, K, FalseOwned, Veracity,
    Counterfeit, dropK, fixture, id]
  decide

/-- Weak signature only, not full perfect knowledge/source profile. -/
theorem weak_stress_A :
    K dropA false ∧ C dropA false ∧ D dropA false ∧ N dropA false ∧ P dropA false ∧
    ExerciseBridge dropA false ∧ Factive dropA false ∧
    ¬ A dropA false ∧ FalseOwned dropA ∧ ¬ Veracity dropA false := by
  simp only [K, C, D, N, P, ExerciseBridge, Factive, A, FalseOwned, Veracity,
    Counterfeit, dropA, fixture, id]
  decide

/-- Weak signature only, not independently warranted genuine ownership. -/
theorem weak_stress_C :
    K dropC false ∧ A dropC false ∧ D dropC false ∧ N dropC false ∧ P dropC false ∧
    ExerciseBridge dropC false ∧ Factive dropC false ∧
    ¬ C dropC false ∧ FalseOwned dropC ∧ ¬ Veracity dropC false := by
  simp only [K, A, D, N, P, ExerciseBridge, Factive, C, FalseOwned, Veracity,
    Counterfeit, dropC, fixture, id]
  decide

theorem deletion_D :
    K dropD false ∧ A dropD false ∧ C dropD false ∧ N dropD false ∧ P dropD false ∧
    ExerciseBridge dropD false ∧ Factive dropD false ∧
    ¬ D dropD false ∧ FalseOwned dropD ∧ ¬ Veracity dropD false := by
  simp only [K, A, C, N, P, ExerciseBridge, Factive, D, FalseOwned, Veracity,
    Counterfeit, dropD, fixture, id]
  decide

/-- Respect-specific shortcoming and overall fittingness remain distinct. -/
theorem deletion_N :
    K dropN false ∧ A dropN false ∧ C dropN false ∧ D dropN false ∧ P dropN false ∧
    ExerciseBridge dropN false ∧ Factive dropN false ∧
    ¬ N dropN false ∧ FalseOwned dropN ∧ ¬ Veracity dropN false := by
  simp only [K, A, C, D, P, ExerciseBridge, Factive, N, FalseOwned, Veracity,
    Counterfeit, dropN, fixture, id]
  decide

/-- Known, controlled, intrinsically shortcoming-laden unfitting exercise. -/
theorem deletion_P :
    K dropP false ∧ A dropP false ∧ C dropP false ∧ D dropP false ∧ N dropP false ∧
    ExerciseBridge dropP false ∧ Factive dropP false ∧
    ¬ P dropP false ∧ FalseOwned dropP ∧ ¬ Veracity dropP false := by
  simp only [K, A, C, D, N, ExerciseBridge, Factive, P, FalseOwned, Veracity,
    Counterfeit, dropP, fixture, id]
  decide

/-- false source = g; true source = h. At occasion false, g asserts true and
    h asserts false. g additionally has a fitting auxiliary exercise. -/
def positive : Fixture where
  asserts := fun c s t q => c = false ∧
    ((s = false ∧ t = false ∧ q = true) ∨ (s = true ∧ t = true ∧ q = false))
  trueAt := fun _ q => q = true
  knowsFalse := fun _ _ q => q = false
  aware := fun _ _ _ _ => True
  deliberate := fun _ _ _ => True
  exercise := id
  actual := fun c s e => c = false ∧ (s = false ∨ (s = true ∧ e = true))
  fitting := fun _ s _ => s = false
  shortcoming := fun c s e => c = false ∧ s = true ∧ e = true

def supplies (s t : Bool) : Prop := s = false ∧ (t = false ∨ t = true)

theorem positive_package : Package positive false ∧ Factive positive false ∧
    D positive true ∧ Veracity positive false := by
  simp only [Package, K, A, C, D, N, P, ExerciseBridge, Factive, Veracity,
    Counterfeit, positive, id]
  decide

theorem positive_nonvacuity :
    positive.asserts false false false true ∧
    positive.actual false false true ∧ positive.fitting false false true ∧
    Counterfeit positive true false true false ∧
    positive.shortcoming false true true ∧
    ¬ positive.asserts true false false true := by
  simp only [Counterfeit, positive, id]
  decide

theorem created_false_is_not_source_owned :
    supplies false true ∧ positive.asserts false true true false ∧
    ¬ positive.trueAt false false ∧ ¬ positive.asserts false false true false := by
  simp only [supplies, positive]
  decide

def nonconforming : Fixture :=
  { positive with fitting := fun _ s e => s = false ∧ e = false }

theorem truthful_not_conforming : Veracity nonconforming false ∧
    ¬ P nonconforming false ∧ nonconforming.actual false false true ∧
    ¬ nonconforming.fitting false false true := by
  simp only [Veracity, P, nonconforming, positive, id]
  decide

/-- At the second occasion only weak assertion remains, with no awareness.
    This witnesses a semantic-scope boundary, not a gap in a full omniscience premise. -/
def localGlobal : Fixture where
  asserts := fun c s t q => s = false ∧ t = c ∧ q = !c
  trueAt := fun _ q => q = true
  knowsFalse := fun _ _ q => q = false
  aware := fun c _ _ _ => c = false
  deliberate := fun _ _ _ => True
  exercise := id
  actual := fun _ _ _ => True
  fitting := fun _ _ _ => True
  shortcoming := fun _ _ _ => False

theorem local_global_separation : K localGlobal false ∧ C localGlobal false ∧
    D localGlobal false ∧ N localGlobal false ∧ P localGlobal false ∧
    ExerciseBridge localGlobal false ∧ Factive localGlobal false ∧
    localGlobal.asserts false false false true ∧ localGlobal.aware false false false true ∧
    localGlobal.trueAt false true ∧ ¬ A localGlobal false ∧ ¬ Veracity localGlobal false := by
  simp only [K, C, D, N, P, ExerciseBridge, Factive, A, Veracity,
    Counterfeit, localGlobal, id]
  decide

theorem strong_ownership_noncollapse :
    Veracity (informedOwnership localGlobal) false ∧ ¬ Veracity localGlobal false ∧
    (informedOwnership localGlobal).asserts false false false true ∧
    ¬ (informedOwnership localGlobal).asserts true false true false := by
  simp only [Veracity, informedOwnership, localGlobal]
  decide

/-- Strong ownership includes awareness/control, never truth or normative fitness. -/
theorem strong_ownership_not_truth_by_definition :
    (informedOwnership dropN).asserts false false false false ∧
    ¬ (informedOwnership dropN).trueAt false false ∧
    A (informedOwnership dropN) false ∧ C (informedOwnership dropN) false ∧
    ¬ Veracity (informedOwnership dropN) false := by
  simp only [A, C, Veracity, informedOwnership, dropN, fixture]
  decide

theorem positive_equivalence_instance :
    Veracity positive false ↔ NoCounterfeit positive false :=
  veracity_iff_no_counterfeit positive false positive_package.1.1
    positive_package.1.2.1 positive_package.1.2.2.1 positive_package.2.1

end VeracityBoundary.Controls
