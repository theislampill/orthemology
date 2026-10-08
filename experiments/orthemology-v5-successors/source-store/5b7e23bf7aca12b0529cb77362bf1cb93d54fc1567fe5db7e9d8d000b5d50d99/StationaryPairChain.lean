import FiniteChainAvoidance
import EndComponents

noncomputable section
open scoped BigOperators

namespace HiddenParity.Recurrence

variable {State Pair : Type*} [Fintype State] [DecidableEq State] [DecidableEq Pair]

/-- Positive stationary action probabilities on retained pairs, normalized at
each used observed state. -/
structure StationaryChoices (source : Pair → State) (E : Finset Pair) where
  weight : E → ℝ
  positive : ∀ e, 0 < weight e
  normalized : ∀ s ∈ usedStates source E,
    ∑ e : E, (if source e = s then weight e else 0) = 1

/-- The concrete stationary pair transition multiplies the actual successor
probability by the chosen action probability at that observed successor. -/
def pairChain (source : Pair → State) (E : Finset Pair)
    (P : Pair → State → ℝ) (hP : ∀ e ∈ E, ∀ s, 0 ≤ P e s)
    (hN : ∀ e ∈ E, ∑ s, P e s = 1)
    (hClosed : ∀ e ∈ E, ∀ s, 0 < P e s → s ∈ usedStates source E)
    (choice : StationaryChoices source E) : FiniteChain E where
  prob e f := P e (source f) * choice.weight f
  nonnegative e f := mul_nonneg (hP e e.property (source f)) (choice.positive f).le
  normalized e := by
    calc
      (∑ f : E, P e (source f) * choice.weight f) =
          ∑ f : E, ∑ s : State, if source f = s then P e s * choice.weight f else 0 := by
        simp
      _ = ∑ s : State, P e s * (∑ f : E, if source f = s then choice.weight f else 0) := by
        rw [Finset.sum_comm]
        apply Finset.sum_congr rfl
        intro s _
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro f _
        split_ifs <;> simp_all
      _ = ∑ s : State, P e s := by
        apply Finset.sum_congr rfl
        intro s _
        by_cases hs : s ∈ usedStates source E
        · rw [choice.normalized s hs, mul_one]
        · have hz : P e s = 0 := le_antisymm
            (le_of_not_gt (fun hp => hs (hClosed e e.property s hp))) (hP e e.property s)
          simp [hz]
      _ = 1 := hN e e.property

omit [DecidableEq Pair] in
theorem pairChain_edge (source : Pair → State) (E : Finset Pair)
    (P : Pair → State → ℝ) (hP : ∀ e ∈ E, ∀ s, 0 ≤ P e s)
    (hN : ∀ e ∈ E, ∑ s, P e s = 1)
    (hClosed : ∀ e ∈ E, ∀ s, 0 < P e s → s ∈ usedStates source E)
    (choice : StationaryChoices source E) (e f : E) :
    0 < (pairChain source E P hP hN hClosed choice).prob e f ↔ 0 < P e (source f) := by
  exact mul_pos_iff_of_pos_right (choice.positive f)

def positiveSuccessors (P : Pair → State → ℝ) (e : Pair) : Finset State :=
  Finset.univ.filter (fun s => 0 < P e s)

omit [DecidableEq Pair] in
/-- Actual state-graph strong connectivity plus positive stationary choices
derives strong connectivity of the concrete retained-pair chain. -/
theorem pairChain_strongly_connected (source : Pair → State) (E : Finset Pair)
    (P : Pair → State → ℝ) (hP : ∀ e ∈ E, ∀ s, 0 ≤ P e s)
    (hN : ∀ e ∈ E, ∑ s, P e s = 1)
    (hEC : IsEndComponent source (positiveSuccessors P) E)
    (choice : StationaryChoices source E) :
    ∀ e f : E, Relation.ReflTransGen
      (fun e f => 0 < (pairChain source E P hP hN
        (fun e he s hs => hEC.closed e he (by simp [positiveSuccessors, hs])) choice).prob e f) e f := by
  let hc : ∀ e ∈ E, ∀ s, 0 < P e s → s ∈ usedStates source E :=
    fun e he s hs => hEC.closed e he (by simp [positiveSuccessors, hs])
  let K := pairChain source E P hP hN hc choice
  intro e f
  change Relation.ReflTransGen (fun e f => 0 < K.prob e f) e f
  have lift : ∀ s, Reach source (positiveSuccessors P) E s (source f) →
      ∀ g : E, 0 < P g s → Relation.ReflTransGen (fun e f => 0 < K.prob e f) g f := by
    intro s hPath
    induction hPath using Relation.ReflTransGen.head_induction_on with
    | refl =>
        intro g hg
        exact Relation.ReflTransGen.single ((pairChain_edge source E P hP hN hc choice g f).mpr hg)
    | @head s t hEdge _ ih =>
        intro g hg
        obtain ⟨a, haE, haSource, hSucc⟩ := hEdge
        let aE : E := ⟨a, haE⟩
        have hga : 0 < K.prob g aE :=
          (pairChain_edge source E P hP hN hc choice g aE).mpr (by simpa [aE, haSource] using hg)
        have hat : 0 < P aE t := (Finset.mem_filter.mp hSucc).2
        exact (show Relation.ReflTransGen (fun e f => 0 < K.prob e f) g aE from
          Relation.ReflTransGen.single hga).trans (ih aE hat)
  obtain ⟨s, hs⟩ := hEC.successors_nonempty e e.property
  have hsUsed := hEC.closed e e.property hs
  have hfUsed : source f ∈ usedStates source E := Finset.mem_image.mpr ⟨f, f.property, rfl⟩
  exact lift s (hEC.connected s hsUsed (source f) hfUsed) e (Finset.mem_filter.mp hs).2

/-- Uniform stationary choice, constructed rather than hypothesized. -/
def actionFiber (source : Pair → State) (E : Finset Pair) (s : State) : Finset E :=
  Finset.univ.filter (fun e => source e = s)

omit [Fintype State] [DecidableEq Pair] in
theorem actionFiber_nonempty (source : Pair → State) (E : Finset Pair) (s : State)
    (hs : s ∈ usedStates source E) : (actionFiber source E s).Nonempty := by
  obtain ⟨e, he, hes⟩ := Finset.mem_image.mp hs
  exact ⟨⟨e, he⟩, by simp [actionFiber, hes]⟩

def uniformWeight (source : Pair → State) (E : Finset Pair) (e : E) : ℝ :=
  ((actionFiber source E (source e)).card : ℝ)⁻¹

omit [Fintype State] [DecidableEq Pair] in
theorem uniformWeight_positive (source : Pair → State) (E : Finset Pair) (e : E) :
    0 < uniformWeight source E e := by
  apply inv_pos.mpr
  exact_mod_cast Finset.card_pos.mpr
    (actionFiber_nonempty source E (source e) (Finset.mem_image.mpr ⟨e, e.property, rfl⟩))

def uniformChoices (source : Pair → State) (E : Finset Pair) : StationaryChoices source E where
  weight := uniformWeight source E
  positive := uniformWeight_positive source E
  normalized s hs := by
    let F := actionFiber source E s
    have hCard : (F.card : ℝ) ≠ 0 := by
      exact_mod_cast (Finset.card_pos.mpr (actionFiber_nonempty source E s hs)).ne'
    change ∑ e : E, (if source e = s then uniformWeight source E e else 0) = 1
    calc
      _ = ∑ e ∈ F, uniformWeight source E e := by simp [F, actionFiber, Finset.sum_filter]
      _ = ∑ _e ∈ F, (F.card : ℝ)⁻¹ := by
        apply Finset.sum_congr rfl
        intro e he
        have hes : source e = s := (Finset.mem_filter.mp he).2
        simp [uniformWeight, hes, F]
      _ = 1 := by simp [hCard]

end HiddenParity.Recurrence
