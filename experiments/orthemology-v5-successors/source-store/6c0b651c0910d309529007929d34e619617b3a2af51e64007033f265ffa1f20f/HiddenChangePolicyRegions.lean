import HiddenChangeTailTransport
import HiddenChangeCertificate

/-! Policy-relative finite regions constructed from the actual fixed-index laws.
The regions are proof witnesses only. They do not enter the submitted checker.
No winning, fairness, coupling, or semantic safe-region premise is used here. -/
noncomputable section
open MeasureTheory ProbabilityTheory Set
open scoped BigOperators ENNReal
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity HiddenParity.Stochastic HiddenParity.ResidualSeed
open HiddenParity.ResidualSeed.Continuation

namespace HiddenChange
variable {n k : ℕ} [NeZero n] {R : Type*} [MeasurableSpace R]

/-- Positive probability of an actual finite physical history. -/
def PositivePrefix (I : Input n k) (hI : I.Valid) (κ : ChangeIndex)
    (s : State n) (ρ : Measure R) (π : Policy R n k) (h : PairHistory n k) : Prop :=
  0 < fixedPhysicalLaw I hI κ s ρ π {H | H h.length = h}

/-- Seeds consistent with all past selected actions and the selected next pair. -/
def SelectedSeeds (s : State n) (π : Policy R n k) (h : PairHistory n k)
    (e : Pair n k) : Set R :=
  CompatibleSeeds (pairPolicy s π) h ∩ {r | pairPolicy s π r h = e}

def PositiveSelected (s : State n) (ρ : Measure R) (π : Policy R n k)
    (h : PairHistory n k) (e : Pair n k) : Prop := 0 < ρ (SelectedSeeds s π h e)

/-- All-history lawfulness, including histories having probability zero. -/
def PolicyLawful (I : Input n k) (s : State n) (π : Policy R n k) : Prop :=
  ∀ r h, π r (erasePairSources h) ∈ commonMenu I (currentState s h)

/-- State witnesses are positive original fixed-N prefixes after the switch. -/
def policyKnownRegion (I : Input n k) (hI : I.Valid)
    (s : State n) (ρ : Measure R) (π : Policy R n k) : Region n := by
  classical
  exact Finset.univ.filter (fun t => ∃ N h, N ≤ h.length ∧
    PositivePrefix I hI (some N) s ρ π h ∧ currentState s h = t)

/-- State witnesses are positive original no-change prefixes. -/
def policyUncertainRegion (I : Input n k) (hI : I.Valid)
    (s : State n) (ρ : Measure R) (π : Policy R n k) : Region n := by
  classical
  exact Finset.univ.filter (fun t => ∃ h,
    PositivePrefix I hI none s ρ π h ∧ currentState s h = t)

omit [NeZero n] in
@[simp] theorem mem_policyKnownRegion (I : Input n k) (hI : I.Valid)
    (s : State n) (ρ : Measure R) (π : Policy R n k) (t : State n) :
    t ∈ policyKnownRegion I hI s ρ π ↔ ∃ N h, N ≤ h.length ∧
      PositivePrefix I hI (some N) s ρ π h ∧ currentState s h = t := by
  classical
  simp [policyKnownRegion]

omit [NeZero n] in
@[simp] theorem mem_policyUncertainRegion (I : Input n k) (hI : I.Valid)
    (s : State n) (ρ : Measure R) (π : Policy R n k) (t : State n) :
    t ∈ policyUncertainRegion I hI s ρ π ↔ ∃ h,
      PositivePrefix I hI none s ρ π h ∧ currentState s h = t := by
  classical
  simp [policyUncertainRegion]

omit [NeZero n] [MeasurableSpace R] in
@[simp] theorem compatibleSeeds_cons (s : State n) (π : Policy R n k)
    (h : PairHistory n k) (e : Pair n k) (y : State n) :
    CompatibleSeeds (pairPolicy s π) ((e,y)::h) = SelectedSeeds s π h e := by
  rfl

omit [NeZero n] in
theorem fixedPrefixLikelihood_cons (I : Input n k) (κ : ChangeIndex)
    (h : PairHistory n k) (e : Pair n k) (y : State n) :
    fixedPrefixLikelihood I κ ((e,y)::h) =
      ENNReal.ofReal (I.row (fixedMode κ h.length) e y : ℝ) * fixedPrefixLikelihood I κ h := by
  rw [fixedPrefixLikelihood_eq_lift, liftMode, rowLikelihood_cons,
    ← fixedPrefixLikelihood_eq_lift]
  rfl

theorem positive_prefix_factors (I : Input n k) (hI : I.Valid) (κ : ChangeIndex)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (h : PairHistory n k) :
    PositivePrefix I hI κ s ρ π h ↔
      0 < ρ (CompatibleSeeds (pairPolicy s π) h) ∧ 0 < fixedPrefixLikelihood I κ h := by
  rw [PositivePrefix, fixed_prefix_probability I hI κ s ρ π hπ]
  exact CanonicallyOrderedAdd.mul_pos

/-- A positive next-action seed event licenses every positive governing receipt. -/
theorem positive_prefix_extend (I : Input n k) (hI : I.Valid) (κ : ChangeIndex)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (h : PairHistory n k) (e : Pair n k) (y : State n)
    (hp : PositivePrefix I hI κ s ρ π h) (he : PositiveSelected s ρ π h e)
    (hy : 0 < I.row (fixedMode κ h.length) e y) :
    PositivePrefix I hI κ s ρ π ((e,y)::h) := by
  apply (positive_prefix_factors I hI κ s ρ π hπ _).mpr
  refine ⟨he, ?_⟩
  rw [fixedPrefixLikelihood_cons]
  apply CanonicallyOrderedAdd.mul_pos.mpr
  constructor
  · exact ENNReal.ofReal_pos.mpr (by exact_mod_cast hy)
  · exact ((positive_prefix_factors I hI κ s ρ π hπ h).mp hp).2

omit [NeZero n] in
theorem selected_source (s : State n) (ρ : Measure R) (π : Policy R n k)
    (h : PairHistory n k) (e : Pair n k) (he : PositiveSelected s ρ π h e) :
    e.1 = currentState s h := by
  obtain ⟨r, hr⟩ := nonempty_of_measure_ne_zero (ne_of_gt he)
  exact (congrArg Prod.fst hr.2).symm

omit [NeZero n] in
theorem selected_menu (I : Input n k) (s : State n) (ρ : Measure R)
    (π : Policy R n k) (hL : PolicyLawful I s π)
    (h : PairHistory n k) (e : Pair n k) (he : PositiveSelected s ρ π h e) :
    e.2 ∈ commonMenu I e.1 := by
  obtain ⟨r, hr⟩ := nonempty_of_measure_ne_zero (ne_of_gt he)
  have hh := hL r h
  rw [← hr.2]
  exact hh

theorem initial_mem_policyUncertainRegion (I : Input n k) (hI : I.Valid)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2)) :
    s ∈ policyUncertainRegion I hI s ρ π := by
  apply (mem_policyUncertainRegion I hI s ρ π s).mpr
  refine ⟨[], ?_, rfl⟩
  rw [PositivePrefix, fixed_prefix_probability I hI none s ρ π hπ]
  simp [CompatibleSeeds, ActionCompatible, fixedPrefixLikelihood]

/-- Every positively selected pair after an original post-switch prefix is
safe for every P1-positive receipt in the same policy-relative known region. -/
theorem selected_knownAllowed (I : Input n k) (hI : I.Valid)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (hL : PolicyLawful I s π) (N : ℕ) (h : PairHistory n k) (e : Pair n k)
    (hN : N ≤ h.length) (hp : PositivePrefix I hI (some N) s ρ π h)
    (he : PositiveSelected s ρ π h e) :
    e ∈ knownAllowed I (policyKnownRegion I hI s ρ π) := by
  apply (mem_knownAllowed I _ e).mpr
  refine ⟨?_, selected_menu I s ρ π hL h e he, ?_⟩
  · exact (mem_policyKnownRegion I hI s ρ π e.1).mpr
      ⟨N,h,hN,hp,(selected_source s ρ π h e he).symm⟩
  · intro y hy
    apply (mem_policyKnownRegion I hI s ρ π y).mpr
    refine ⟨N,(e,y)::h,by simp; omega,?_,rfl⟩
    apply positive_prefix_extend I hI (some N) s ρ π hπ h e y hp he
    simpa only [fixedMode, if_neg (not_lt.mpr hN)] using hy

/-- Full uncertain safety is derived from the original no-change prefix and
switching at exactly its length, after the next action has been selected. -/
theorem selected_uncertainAllowed (I : Input n k) (hI : I.Valid)
    (s : State n) (ρ : Measure R) [IsProbabilityMeasure ρ] (π : Policy R n k)
    (hπ : Measurable (fun z : R × PublicHistory n k => π z.1 z.2))
    (hL : PolicyLawful I s π) (h : PairHistory n k) (e : Pair n k)
    (hp : PositivePrefix I hI none s ρ π h) (he : PositiveSelected s ρ π h e) :
    e ∈ uncertainAllowed I (policyKnownRegion I hI s ρ π)
      (policyUncertainRegion I hI s ρ π) := by
  apply (mem_uncertainAllowed I _ _ e).mpr
  refine ⟨?_, selected_menu I s ρ π hL h e he, ?_, ?_⟩
  · exact (mem_policyUncertainRegion I hI s ρ π e.1).mpr
      ⟨h,hp,(selected_source s ρ π h e he).symm⟩
  · intro y hy
    exact (mem_policyUncertainRegion I hI s ρ π y).mpr
      ⟨(e,y)::h,positive_prefix_extend I hI none s ρ π hπ h e y hp he hy,rfl⟩
  · intro y hy _
    apply (mem_policyKnownRegion I hI s ρ π y).mpr
    refine ⟨h.length,(e,y)::h,by simp,?_,rfl⟩
    have hp' : PositivePrefix I hI (some h.length) s ρ π h := by
      unfold PositivePrefix at hp ⊢
      rwa [← prefix_mass_noChange_switchAt I hI s ρ π hπ h]
    apply positive_prefix_extend I hI (some h.length) s ρ π hπ h e y hp' he
    simpa only [fixedMode, lt_self_iff_false, if_false] using hy

end HiddenChange
