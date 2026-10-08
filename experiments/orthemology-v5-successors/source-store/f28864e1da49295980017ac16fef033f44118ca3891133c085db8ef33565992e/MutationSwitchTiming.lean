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
  | some N, t => if t ≤ N then 0 else 1

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
  (if previousMode h = 1 ∨ α.choose rz.2 h e = true then 1 else 0, e)

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

theorem fixedPolicy_measurable [MeasurableSpace R]
    (κ : ChangeIndex) (s : State n) (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) :
    Measurable (fun z : R × TaggedHistory n k => fixedPolicy κ s π z.1 z.2) := by
  exact ((measurable_of_countable (fun h : TaggedHistory n k => fixedMode κ h.length)).comp
    measurable_snd).prodMk ((pairPolicy_measurable s π hπ).comp
      (measurable_fst.prodMk ((measurable_of_countable eraseMode).comp measurable_snd)))

theorem adaptivePolicy_measurable [MeasurableSpace R] [MeasurableSpace Z]
    (s : State n) (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (α : Adversary Z n k) :
    Measurable (fun z : (R × Z) × TaggedHistory n k => adaptivePolicy s π α z.1 z.2) := by
  have he : Measurable (fun z : (R × Z) × TaggedHistory n k =>
      pairPolicy s π z.1.1 (eraseMode z.2)) :=
    (pairPolicy_measurable s π hπ).comp
      (measurable_fst.fst.prodMk ((measurable_of_countable eraseMode).comp measurable_snd))
  have hc := α.measurable_choose.comp (measurable_fst.snd.prodMk (measurable_snd.prodMk he))
  have hp := (measurable_of_countable (previousMode (n := n) (k := k))).comp
    (measurable_snd : Measurable (fun z : (R × Z) × TaggedHistory n k => z.2))
  exact (measurable_const.ite ((hp (measurableSet_singleton 1)).union
    (hc (measurableSet_singleton true))) measurable_const).prodMk he

theorem taggedRows_nonnegative (I : Input n k) (hI : I.Valid) :
    ∀ g y, 0 ≤ taggedRows I g y := by
  intro g y
  change (0 : ℝ) ≤ (I.row g.1 g.2 y : ℝ)
  exact_mod_cast hI.2.2.1 g.1 g.2 y

theorem taggedRows_normalized (I : Input n k) (hI : I.Valid) :
    ∀ g, ∑ y, taggedRows I g y = 1 := by
  intro g
  change ∑ y, (I.row g.1 g.2 y : ℝ) = 1
  exact_mod_cast hI.2.2.2 g.1 g.2

variable [NeZero n]
def fixedLaw [MeasurableSpace R] (I : Input n k) (hI : I.Valid) (κ : ChangeIndex)
    (s : State n) (ρ : Measure R) (π : Policy R n k) : Measure (TaggedTrace n k) :=
  observedTraceLaw ∅ (fixedPolicy κ s π) ρ (taggedRows I) (taggedRows I)
    (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)
    (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)

def adaptiveLaw [MeasurableSpace R] [MeasurableSpace Z]
    (I : Input n k) (hI : I.Valid) (s : State n)
    (ρ : Measure R) (π : Policy R n k) (η : Measure Z) (α : Adversary Z n k) :
    Measure (TaggedTrace n k) :=
  observedTraceLaw ∅ (adaptivePolicy s π α) (ρ.prod η) (taggedRows I) (taggedRows I)
    (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)
    (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)

def fixedPhysicalLaw [MeasurableSpace R] (I : Input n k) (hI : I.Valid)
    (κ : ChangeIndex) (s : State n) (ρ : Measure R) (π : Policy R n k) :
    Measure (PairTrace n k) := (fixedLaw I hI κ s ρ π).map eraseModeTrace

def TaggedParity (I : Input n k) (d : Pair n k) (H : TaggedTrace n k) : Prop :=
  ParitySuccess (fun g : TaggedPair n k => I.priority g.1 g.2)
    (historyAction (0,d) H)

/-- Whole-law stack binding, inherited finite-alphabet theorem instantiated at
internal mode tags. This is not a new generic iid or law-equivalence theorem. -/
theorem fixedLaw_eq_stack [MeasurableSpace R] (I : Input n k) (hI : I.Valid)
    (κ : ChangeIndex) (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ]
    (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) :
    fixedLaw I hI κ s ρ π =
      (ρ.prod (stackMeasure (taggedRows I) (taggedRows_nonnegative I hI)
        (taggedRows_normalized I hI))).map (stackHistoryTrajectory (fixedPolicy κ s π)) := by
  unfold fixedLaw
  rw [← observedTraceLaw_eq_all_query Finset.univ (fixedPolicy κ s π)
    (fixedPolicy_measurable κ s π hπ) ρ (taggedRows I) (taggedRows I)
    (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)
    (taggedRows_nonnegative I hI) (taggedRows_normalized I hI) (fun _ _ => rfl)]
  exact observedTraceLaw_univ_eq_stack _ (fixedPolicy_measurable κ s π hπ) _ _ _ _

theorem adaptiveLaw_eq_stack [MeasurableSpace R] [MeasurableSpace Z]
    (I : Input n k) (hI : I.Valid) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (η : Measure Z) [IsProbabilityMeasure η] (α : Adversary Z n k) :
    adaptiveLaw I hI s ρ π η α =
      ((ρ.prod η).prod (stackMeasure (taggedRows I) (taggedRows_nonnegative I hI)
        (taggedRows_normalized I hI))).map (stackHistoryTrajectory (adaptivePolicy s π α)) := by
  unfold adaptiveLaw
  rw [← observedTraceLaw_eq_all_query Finset.univ (adaptivePolicy s π α)
    (adaptivePolicy_measurable s π hπ α) (ρ.prod η) (taggedRows I) (taggedRows I)
    (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)
    (taggedRows_nonnegative I hI) (taggedRows_normalized I hI) (fun _ _ => rfl)]
  exact observedTraceLaw_univ_eq_stack _ (adaptivePolicy_measurable s π hπ α) _ _ _ _

/-- Selected departure source is always the latest physical receipt. -/
theorem adaptivePolicy_source [MeasurableSpace Z] (s : State n) (π : Policy R n k)
    (α : Adversary Z n k) (rz : R × Z) (h : TaggedHistory n k) :
    (adaptivePolicy s π α rz h).2.1 = currentState s (eraseMode h) := rfl

def currentObserved (s : State n) : PublicHistory n k → State n
  | [] => s
  | (_,y)::_ => y

def AllHistoryLawful (I : Input n k) (s : State n) (π : Policy R n k) : Prop :=
  ∀ r h, π r h ∈ commonMenu I (currentObserved s h)

theorem adaptivePolicy_lawful [MeasurableSpace Z] (I : Input n k) (s : State n)
    (π : Policy R n k) (hlaw : AllHistoryLawful I s π) (α : Adversary Z n k)
    (rz : R × Z) (h : TaggedHistory n k) :
    (adaptivePolicy s π α rz h).2.2 ∈ commonMenu I (currentState s (eraseMode h)) := by
  have hh := hlaw rz.1 (erasePairSources (eraseMode h))
  cases h <;> exact hh

/-- The current governing tag owns both its sampled row and its acceptance
priority; neither value is supplied as an extra controller observation. -/
theorem governing_row_priority (I : Input n k) (g : TaggedPair n k) (y : State n) :
    taggedRows I g y = (I.row g.1 g.2 y : ℝ) ∧
      (fun a : TaggedPair n k => I.priority a.1 a.2) g = I.priority g.1 g.2 := ⟨rfl,rfl⟩

/-- Joint seed/transcript weights for the actual adaptive law. This exposes the
fresh selected tagged row with action-before-tag ordering in the concrete selector. -/
theorem adaptive_seed_prefix_probability [MeasurableSpace R] [MeasurableSpace Z]
    (I : Input n k) (hI : I.Valid) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (η : Measure Z) [IsProbabilityMeasure η] (α : Adversary Z n k)
    (D : Set (R × Z)) (h : TaggedHistory n k) :
    CanonicalInput (ρ.prod η) (taggedRows I) (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)
      {z | z.1 ∈ D ∧ historyTrajectory ∅ (adaptivePolicy s π α) z h.length = h} =
      (ρ.prod η) (D ∩ CompatibleSeeds (adaptivePolicy s π α) h) * RowLikelihood (taggedRows I) h :=
  private_transcript_cylinder_probability ∅ (adaptivePolicy s π α) (ρ.prod η)
    (taggedRows I) (taggedRows I) (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)
    (taggedRows_nonnegative I hI) (taggedRows_normalized I hI) (fun _ _ => rfl) D h

/-- After the concrete selector has chosen the governing tagged pair, the next
receipt has precisely that row factor. The remaining coefficient is independent
of y, even for arbitrary private controller and adversary seeds. -/
theorem adaptive_next_receipt_factor [MeasurableSpace R] [MeasurableSpace Z]
    (I : Input n k) (hI : I.Valid) (s : State n)
    (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (η : Measure Z) [IsProbabilityMeasure η] (α : Adversary Z n k)
    (h : TaggedHistory n k) (g : TaggedPair n k) (y : State n) :
    CanonicalInput (ρ.prod η) (taggedRows I) (taggedRows_nonnegative I hI) (taggedRows_normalized I hI)
      {z | historyTrajectory ∅ (adaptivePolicy s π α) z (h.length+1) = (g,y)::h} =
      ((ρ.prod η) {rz | ActionCompatible (adaptivePolicy s π α) rz h ∧
        adaptivePolicy s π α rz h = g} * RowLikelihood (taggedRows I) h) *
        ENNReal.ofReal (taggedRows I g y) := by
  have hp := adaptive_seed_prefix_probability I hI s ρ π η α Set.univ ((g,y)::h)
  simp only [Set.mem_univ, true_and, Set.univ_inter, CompatibleSeeds, ActionCompatible,
    List.length_cons, HiddenParity.ResidualSeed.Continuation.rowLikelihood_cons] at hp
  rw [hp]
  ac_rfl

end HiddenChange

example : HiddenChange.fixedMode (some 0) 0 = 1 := by decide +kernel
