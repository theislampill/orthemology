import KilledQueryLaw
import PolicyTraceBinding

noncomputable section
open MeasureTheory ProbabilityTheory Set
open Orthemology.Tranche2.FiniteAlphabetQuery
open Orthemology.Tranche2.PolicyEmbedding

namespace HiddenParity.Stochastic
universe u v
variable {R : Type v} {A Y : Type u}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- Every selected action before time n was inside the retained component. -/
def AlivePrefix (D : Finset A) (d : A) (H : ℕ → History A Y) (n : ℕ) : Prop :=
  ∀ k ∈ Finset.range n, historyAction d H k ∈ D

instance alivePrefixDecidable (D : Finset A) (d : A) (H : ℕ → History A Y) (n : ℕ) :
    Decidable (AlivePrefix D d H n) := by
  unfold AlivePrefix
  infer_instance

/-- The actually observed history until the first outside pair. Its receipt and
all following receipts are erased; the infinite alive/dead sequence retains kill time. -/
def killedHistory (D : Finset A) (d : A) (H : ℕ → History A Y) :
    ℕ → Bool × History A Y :=
  fun n => if AlivePrefix D d H n then (true, H n) else (false, [])

omit [DecidableEq A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
theorem measurable_alivePrefix (D : Finset A) (d : A) (n : ℕ) :
    MeasurableSet {H : ℕ → History A Y | AlivePrefix D d H n} := by
  simp only [AlivePrefix, Set.setOf_forall]
  apply MeasurableSet.iInter
  intro k
  by_cases hk : k ∈ Finset.range n
  · simpa only [hk, Set.iInter_true] using
      D.measurableSet.preimage ((measurable_pi_apply k).comp (historyAction_measurable d))
  · simp [hk]

omit [MeasurableSpace Y] [MeasurableSingletonClass Y] in
theorem killedHistory_measurable (D : Finset A) (d : A) :
    Measurable (killedHistory (Y := Y) D d) := by
  apply measurable_pi_lambda
  intro n
  exact Measurable.ite (measurable_alivePrefix (Y := Y) D d n)
    (measurable_const.prodMk (measurable_pi_apply n)) measurable_const

omit [Fintype A] [Fintype Y] [MeasurableSpace R] [MeasurableSpace A]
    [MeasurableSingletonClass A] [MeasurableSpace Y] [MeasurableSingletonClass Y] in
/-- The stopped-counter semantics and observed-history kill map agree on every
actual evaluator run, including arbitrary initial evaluator state. -/
theorem killedReadout_history_agreement
    (D : Finset A) (π : R → History A Y → A)
    (oracle : Oracle (A → Y)) (s : EvalState R A Y) (d : A) :
    killedReadout (fun x : EvalState R A Y => x.2.2) []
        (run (query D π) (Orthemology.Tranche2.PolicyEmbedding.step D π) oracle s) =
      killedHistory D d (historyReadout
        (run (query D π) (Orthemology.Tranche2.PolicyEmbedding.step D π) oracle s)) := by
  funext n
  have hiff : (run (query D π) (Orthemology.Tranche2.PolicyEmbedding.step D π) oracle s n).2 = 0 ↔
      AlivePrefix D d (historyReadout
        (run (query D π) (Orthemology.Tranche2.PolicyEmbedding.step D π) oracle s)) n := by
    rw [run_counter_zero_iff]
    unfold AlivePrefix
    simp only [Finset.mem_range]
    apply forall_congr'
    intro k
    apply imp_congr_right
    intro _
    have hr := congrFun (action_readout_on_run D π oracle s d) k
    change selected π (run (query D π) (Orthemology.Tranche2.PolicyEmbedding.step D π) oracle s k).1 =
      historyAction d (historyReadout (run (query D π)
        (Orthemology.Tranche2.PolicyEmbedding.step D π) oracle s)) k at hr
    simp only [query, decide_eq_false_iff_not, not_not, hr]
  simp only [killedReadout, killedHistory, ← hiff, historyReadout]

theorem traceLaw_killed_history_readout
    (D : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure (EvalState R A Y)) (ν : Measure (Oracle (A → Y))) (d : A) :
    ((traceLaw (query D π) (Orthemology.Tranche2.PolicyEmbedding.step D π) ρ ν).map historyReadout).map
        (killedHistory D d) =
      (traceLaw (query D π) (Orthemology.Tranche2.PolicyEmbedding.step D π) ρ ν).map
        (killedReadout (fun x : EvalState R A Y => x.2.2) []) := by
  have hRun := measurable_trajectory (query D π) (Orthemology.Tranche2.PolicyEmbedding.step D π)
    (query_measurable D π hπ) (step_measurable D π hπ)
  have hKH := killedHistory_measurable (Y := Y) D d
  have hHR := historyReadout_measurable (R := R) (A := A) (Y := Y)
  have hKR := killedReadout_measurable (fun x : EvalState R A Y => x.2.2)
    measurable_snd.snd ([] : History A Y)
  rw [Measure.map_map hKH hHR]
  unfold traceLaw
  rw [Measure.map_map (hKH.comp hHR) hRun, Measure.map_map hKR hRun]
  congr 1
  funext z
  exact (killedReadout_history_agreement D π z.2 z.1 d).symm

/-- Equality of entire killed observed-history laws for the genuine canonical
adaptive policy experiments. Full row equality is required only on retained D.
The common measurable seed policy can use unbounded memory. -/
theorem canonical_killed_historyLaw_eq
    (D : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2))
    (ρ : Measure R) [IsProbabilityMeasure ρ] (P Q : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hPN : ∀ a, ∑ y, P a y = 1)
    (hQ : ∀ a y, 0 ≤ Q a y) (hQN : ∀ a, ∑ y, Q a y = 1)
    (hagree : ∀ a ∈ D, P a = Q a) (d : A) :
    (observedTraceLaw ∅ π ρ P P hP hPN hP hPN).map (killedHistory D d) =
      (observedTraceLaw ∅ π ρ Q Q hQ hQN hQ hQN).map (killedHistory D d) := by
  have hp := traceLaw_historyReadout D π hπ ρ P P hP hPN hP hPN
  rw [observedTraceLaw_eq_all_query D π hπ ρ P P hP hPN hP hPN (fun _ _ => rfl)] at hp
  have hq := traceLaw_historyReadout D π hπ ρ P Q hP hPN hQ hQN
  rw [observedTraceLaw_eq_all_query D π hπ ρ P Q hP hPN hQ hQN hagree] at hq
  rw [← hp, ← hq, traceLaw_killed_history_readout D π hπ,
    traceLaw_killed_history_readout D π hπ]
  exact killed_traceLaw_eq (query D π) (Orthemology.Tranche2.PolicyEmbedding.step D π)
    (query_measurable D π hπ) (step_measurable D π hπ) (seedLaw ρ P hP hPN)
    (iidOracle (rowMeasure P hP hPN)) (iidOracle (rowMeasure Q hQ hQN))
    (fun x : EvalState R A Y => x.2.2) measurable_snd.snd []

end HiddenParity.Stochastic
