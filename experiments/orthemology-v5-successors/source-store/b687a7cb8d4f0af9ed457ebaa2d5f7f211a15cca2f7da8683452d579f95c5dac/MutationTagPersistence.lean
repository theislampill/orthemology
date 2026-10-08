import HiddenChangeFinite
import PolicyObservedLaw
import StackActionLaw
import MarkovSeedPosterior
import ConditionalPrefix

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators ENNReal
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity.Stochastic HiddenParity.ResidualSeed

namespace HiddenChange
variable {n k : ℕ} {R Z : Type*}

abbrev PublicHistory (n k : ℕ) := History (Action k) (State n)
abbrev PairHistory (n k : ℕ) := History (Pair n k) (State n)
abbrev PairTrace (n k : ℕ) := ℕ → PairHistory n k
abbrev TaggedPair (n k : ℕ) := Mode × Pair n k
abbrev TaggedHistory (n k : ℕ) := History (TaggedPair n k) (State n)
abbrev TaggedTrace (n k : ℕ) := ℕ → TaggedHistory n k
abbrev Policy (R : Type*) (n k : ℕ) := R → PublicHistory n k → Action k
abbrev ChangeIndex := Option ℕ

def fixedMode : ChangeIndex → ℕ → Mode
  | none, _ => 0
  | some N, t => if t < N then 0 else 1

def finalMode : ChangeIndex → Mode
  | none => 0
  | some _ => 1

def eraseMode (h : TaggedHistory n k) : PairHistory n k :=
  h.map (fun z => (z.1.2, z.2))
def eraseModeTrace (H : TaggedTrace n k) : PairTrace n k := fun t => eraseMode (H t)
def taggedRows (I : Input n k) (g : TaggedPair n k) (y : State n) : ℝ :=
  I.row g.1 g.2 y

def previousMode : TaggedHistory n k → Mode
  | [] => 0
  | (g, _) :: _ => g.1

def fixedPolicy (κ : ChangeIndex) (s : State n) (π : Policy R n k)
    (r : R) (h : TaggedHistory n k) : TaggedPair n k :=
  (fixedMode κ h.length, pairPolicy s π r (eraseMode h))

structure Adversary (Z : Type*) [MeasurableSpace Z] (n k : ℕ) where
  choose : Z → TaggedHistory n k → Pair n k → Bool
  measurable_choose : Measurable (fun z : Z × (TaggedHistory n k × Pair n k) =>
    choose z.1 z.2.1 z.2.2)

def adaptivePolicy [MeasurableSpace Z] (s : State n) (π : Policy R n k)
    (α : Adversary Z n k) (rz : R × Z) (h : TaggedHistory n k) : TaggedPair n k :=
  let e := pairPolicy s π rz.1 (eraseMode h)
  (if α.choose rz.2 h e = true then 1 else 0, e)

@[simp] theorem eraseMode_length (h : TaggedHistory n k) :
    (eraseMode h).length = h.length := by simp [eraseMode]
@[simp] theorem eraseMode_cons (g : TaggedPair n k) (y : State n) (h : TaggedHistory n k) :
    eraseMode ((g,y)::h) = (g.2,y)::eraseMode h := rfl
@[simp] theorem eraseMode_nil : eraseMode ([] : TaggedHistory n k) = [] := rfl

/-- The physical selected pair does not depend on hidden tags or adversary randomness. -/
theorem adaptivePolicy_no_leakage [MeasurableSpace Z] (s : State n) (π : Policy R n k)
    (α : Adversary Z n k) (r : R) (z z' : Z) (h h' : TaggedHistory n k)
    (he : eraseMode h = eraseMode h') :
    (adaptivePolicy s π α (r,z) h).2 = (adaptivePolicy s π α (r,z') h').2 := by
  simp only [adaptivePolicy, he]

/-- The adversary receives the action already selected from the physical history. -/
theorem adaptivePolicy_action_first [MeasurableSpace Z] (s : State n) (π : Policy R n k)
    (α : Adversary Z n k) (rz : R × Z) (h : TaggedHistory n k) :
    (adaptivePolicy s π α rz h).2 = pairPolicy s π rz.1 (eraseMode h) := rfl

theorem adaptivePolicy_irreversible [MeasurableSpace Z] (s : State n) (π : Policy R n k)
    (α : Adversary Z n k) (rz : R × Z) (h : TaggedHistory n k)
    (hh : previousMode h = 1) : (adaptivePolicy s π α rz h).1 = 1 := by
  simp [adaptivePolicy, hh]


end HiddenChange
