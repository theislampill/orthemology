import CommonObservationBoundary
import GenericAuditControls

noncomputable section
open MeasureTheory Filter Set
open scoped ENNReal Topology
open Orthemology.Tranche2.CommonObservationBoundary
open Orthemology.Tranche2.FiniteAlphabetQuery GenericAuditControls

namespace CommonObservationControls

def bitTarget (b : Bool) : Set Bool := {b}
lemma disjoint_bit_targets : ¬∃ a : Bool, ∀ b : Bool, a ∈ bitTarget b := by
  rintro ⟨a,ha⟩
  have hf := ha false
  have ht := ha true
  simp only [bitTarget, Set.mem_singleton_iff] at hf ht
  exact Bool.false_ne_true (hf.symm.trans ht)

/-- Both laws may be dominated by one reference and still have incompatible
almost-sure targets. This is the reversed direction of the author theorem. -/
theorem reversed_domination_counterexample :
    (∀ b : Bool, (Measure.dirac b : Measure Bool) ≪ Measure.count) ∧
    (∀ b : Bool, ∀ᵐ ω ∂(Measure.dirac b : Measure Bool), ∀ᶠ _n : ℕ in atTop,
      ω ∈ bitTarget b) ∧ ¬∃ a : Bool, ∀ b : Bool, a ∈ bitTarget b := by
  refine ⟨?_, ?_, disjoint_bit_targets⟩
  · intro b
    exact absolutelyContinuous_of_singletons _ _ (fun x => by simp)
  · intro b
    simp only [ae_dirac_eq, Filter.eventually_pure]
    exact Filter.Eventually.of_forall (fun _ => rfl)

/-- The common reference must be nonzero; a zero measure gives no witness. -/
theorem zero_reference_counterexample :
    (∀ _b : Bool, (0 : Measure Bool) ≪ (0 : Measure Bool)) ∧
    (∀ b : Bool, ∀ᵐ _ω ∂(0 : Measure Bool), ∀ᶠ _n : ℕ in atTop,
      false ∈ bitTarget b) ∧ ¬∃ a : Bool, ∀ b : Bool, a ∈ bitTarget b := by
  exact ⟨fun _ => Measure.AbsolutelyContinuous.rfl, fun _ => by simp, disjoint_bit_targets⟩

/-- The infinite-target failure is realized under a genuine nonzero same law,
not merely as a bare family of filters. -/
theorem infinite_targets_same_probability_counterexample :
    (∀ θ : ℕ, ∀ᵐ _ω ∂(Measure.dirac () : Measure Unit), ∀ᶠ n : ℕ in atTop, θ ≤ n) ∧
      ¬∃ a : ℕ, ∀ θ : ℕ, θ ≤ a := by
  refine ⟨?_, infinite_target_counterexample.2⟩
  intro θ
  exact Filter.Eventually.of_forall (fun _ => eventually_ge_atTop θ)

/-- Finiteness of the action space is an alternative compactness condition:
with finite actions, an arbitrary target family still has a common action. -/
theorem finite_actions_rescue_arbitrary_targets
    {Θ Ω A : Type*} [Finite A] [MeasurableSpace Ω]
    (μ : Measure Ω) [NeZero μ] (ν : Θ → Measure Ω)
    (X : Ω → ℕ → A) (good : Θ → Set A)
    (hdom : ∀ θ, μ ≪ ν θ)
    (hsuccess : ∀ θ, ∀ᵐ ω ∂ν θ, ∀ᶠ n in atTop, X ω n ∈ good θ) :
    ∃ a, ∀ θ, a ∈ good θ := by
  classical
  by_contra! hnone
  choose bad hbad using hnone
  obtain ⟨a,ha⟩ := common_action_of_dominated_eventual_success μ (fun a => ν (bad a)) X
    (fun a => good (bad a)) (fun a => hdom (bad a)) (fun a => hsuccess (bad a))
  exact hbad a (ha a)

/-- Empty self-verifying support has no common-action content on its own. -/
theorem empty_self_verifying_control :
    (∀ b : Bool, Orthemology.Tranche2.SelfVerifying (fun b : Bool => {b})
      (fun _ _ _ => True) b ∅) ∧ ¬∃ a : Bool, ∀ b : Bool, a ∈ bitTarget b := by
  refine ⟨?_, disjoint_bit_targets⟩
  intro b
  exact ⟨Finset.empty_subset _, fun _ _ => Finset.empty_subset _⟩

def detector (o : ℕ → Bool) (n : ℕ) : Bool :=
  if ∀ k < n, o k = true then true else false

lemma detector_true (n : ℕ) : detector (fun _ => true) n = true := by simp [detector]
lemma detector_false_eventually (o : ℕ → Bool) (h : ∃ k, o k = false) :
    ∀ᶠ n in atTop, detector o n = false := by
  obtain ⟨k,hk⟩ := h
  apply eventually_atTop.mpr
  refine ⟨k+1, fun n hn => ?_⟩
  have hnot : ¬∀ i < n, o i = true := by
    intro hh
    have hi := hh k (by omega)
    rw [hk] at hi
    exact Bool.false_ne_true hi
  simp [detector,hnot]

lemma fair_detects_false : ∀ᵐ o ∂iidOracle fairBit, ∀ᶠ n in atTop, detector o n = false := by
  have hnot : ∀ᵐ o ∂iidOracle fairBit, ¬∀ i, o i = true := by
    rw [ae_iff]
    simpa using fair_all_true_zero
  filter_upwards [hnot] with o ho
  apply detector_false_eventually
  push_neg at ho
  obtain ⟨i,hi⟩ := ho
  exact ⟨i,Bool.eq_false_of_not_eq_true hi⟩

def pathLaw (b : Bool) : Measure (ℕ → Bool) := if b then Measure.dirac (fun _ => true) else iidOracle fairBit

lemma path_success : ∀ b : Bool, ∀ᵐ o ∂pathLaw b, ∀ᶠ n in atTop, detector o n ∈ bitTarget b := by
  intro b
  cases b
  · simpa only [pathLaw, Bool.false_eq_true, ↓reduceIte, bitTarget, Set.mem_singleton_iff] using fair_detects_false
  · simp only [pathLaw, ↓reduceIte, ae_dirac_eq, Filter.eventually_pure]
    exact Filter.Eventually.of_forall (fun n => detector_true n)

/-- A common dominating reference at EVERY FINITE PREFIX is insufficient.
These laws admit eventual perfect target selection, but no accepted common action. -/
theorem finite_prefix_overlap_not_full_path :
    (∀ N : ℕ, ∃ μ : Measure (Fin N → Bool), μ ≠ 0 ∧
      ∀ b : Bool, μ ≪ (pathLaw b).map (prefixSymbols N)) ∧
    (∀ b : Bool, ∀ᵐ o ∂pathLaw b, ∀ᶠ n in atTop, detector o n ∈ bitTarget b) ∧
    ¬∃ a : Bool, ∀ b : Bool, a ∈ bitTarget b := by
  refine ⟨?_, path_success, disjoint_bit_targets⟩
  intro N
  refine ⟨Measure.dirac (fun _ : Fin N => true), by simp, ?_⟩
  intro b
  cases b
  · exact absolutelyContinuous_of_singletons _ _ (iidOracle_prefix_nonzero fairBit fairBit_full N)
  · simp only [pathLaw, ↓reduceIte]
    rw [Measure.map_dirac (measurable_prefixSymbols N)]
    exact Measure.AbsolutelyContinuous.rfl

/-- The finite-prefix counterexample cannot secretly satisfy the needed
nonzero full-path common-reference premise. -/
theorem no_nonzero_common_path_reference :
    ¬∃ μ : Measure (ℕ → Bool), μ ≠ 0 ∧ ∀ b : Bool, μ ≪ pathLaw b := by
  rintro ⟨μ,hμ,hd⟩
  letI : NeZero μ := ⟨hμ⟩
  exact disjoint_bit_targets (common_action_of_dominated_eventual_success μ pathLaw detector bitTarget hd path_success)


/-- The prefix references above are even projections of ONE fixed nonzero path
measure; consistency of the prefix references does not repair the gap. -/
theorem fixed_reference_prefix_domination (N : ℕ) (b : Bool) :
    ((Measure.dirac (fun _ : ℕ => true)).map (prefixSymbols N)) ≪
      (pathLaw b).map (prefixSymbols N) := by
  rw [Measure.map_dirac (measurable_prefixSymbols N)]
  cases b
  · exact absolutelyContinuous_of_singletons _ _ (iidOracle_prefix_nonzero fairBit fairBit_full N)
  · simp only [pathLaw, ↓reduceIte]
    rw [Measure.map_dirac (measurable_prefixSymbols N)]

lemma detector_measurable (n : ℕ) : Measurable (fun o : ℕ → Bool => detector o n) := by
  have hs : MeasurableSet {o : ℕ → Bool | ∀ k < n, o k = true} := by
    simp only [Set.setOf_forall]
    apply MeasurableSet.iInter
    intro k
    apply MeasurableSet.iInter
    intro _hk
    exact (measurableSet_singleton true).preimage (measurable_pi_apply k)
  exact Measurable.ite hs measurable_const measurable_const

lemma detector_prefix_local (o q : ℕ → Bool) (n : ℕ) (h : ∀ k < n, o k = q k) :
    detector o n = detector q n := by
  have heq : (∀ k < n, o k = true) ↔ (∀ k < n, q k = true) := by
    constructor <;> intro hh k hk
    · rw [← h k hk]; exact hh k hk
    · rw [h k hk]; exact hh k hk
  simp only [detector,heq]

#print axioms reversed_domination_counterexample
#print axioms finite_actions_rescue_arbitrary_targets
#print axioms finite_prefix_overlap_not_full_path
end CommonObservationControls
