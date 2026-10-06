import FairComponentParity
import MarkovSupportAdapter

noncomputable section
open MeasureTheory ProbabilityTheory Filter

namespace HiddenParity.Recurrence
variable {State Pair Model : Type*} [Fintype State] [DecidableEq State]
variable [Fintype Pair] [DecidableEq Pair] [MeasurableSpace Pair] [MeasurableSingletonClass Pair]

omit [Fintype State] [Fintype Pair] [DecidableEq Pair] [MeasurableSpace Pair] [MeasurableSingletonClass Pair] in
/-- End-component graph properties transport under equality of actual used successors. -/
theorem endComponent_successor_congr (source : Pair → State)
    (succ₁ succ₂ : Pair → Finset State) (E : Finset Pair)
    (hE : IsEndComponent source succ₁ E) (hEq : ∀ e ∈ E, succ₁ e = succ₂ e) :
    IsEndComponent source succ₂ E := by
  refine ⟨hE.nonempty, ?_, ?_, ?_⟩
  · intro e he
    rw [← hEq e he]
    exact hE.successors_nonempty e he
  · intro e he
    rw [← hEq e he]
    exact hE.closed e he
  · intro s hs t ht
    apply Relation.ReflTransGen.mono _ (hE.connected s hs t ht)
    intro u v huv
    obtain ⟨e, he, hsrc, hsucc⟩ := huv
    exact ⟨e, he, hsrc, by rwa [← hEq e he]⟩

def realProbability (P : RationalKernel Model Pair State) (σ : Model) (e : Pair) (y : State) : ℝ :=
  P.row σ e y

omit [DecidableEq State] [Fintype Pair] [DecidableEq Pair] [MeasurableSpace Pair] [MeasurableSingletonClass Pair] in
theorem realProbability_nonnegative (P : RationalKernel Model Pair State) (σ : Model)
    (E : Finset Pair) : ∀ e ∈ E, ∀ y, 0 ≤ realProbability P σ e y := by
  intro e _ y
  change (0 : ℝ) ≤ (P.row σ e y : ℝ)
  exact_mod_cast P.nonnegative σ e y

omit [DecidableEq State] [Fintype Pair] [DecidableEq Pair] [MeasurableSpace Pair] [MeasurableSingletonClass Pair] in
theorem realProbability_normalized (P : RationalKernel Model Pair State) (σ : Model)
    (E : Finset Pair) : ∀ e ∈ E, ∑ y, realProbability P σ e y = 1 := by
  intro e _
  change ∑ y, (P.row σ e y : ℝ) = 1
  exact_mod_cast P.normalized σ e

omit [DecidableEq State] [Fintype Pair] [DecidableEq Pair] [MeasurableSpace Pair] [MeasurableSingletonClass Pair] in
/-- The zero-exit support adapter identifies actual real positive successors with
the previously checked same-support graph for every live candidate. -/
theorem positiveSuccessors_eq_internal (P : RationalKernel Model Pair State)
    (B : Finset Model) (σ : Model) (hσ : σ ∈ B) (e : Pair) (hNo : NoExit P B σ e) :
    positiveSuccessors (realProbability P σ) e = internalSuccessors P B e := by
  rw [noExit_internal_eq_candidate_support P B σ hσ e hNo]
  ext y
  simp [positiveSuccessors, realProbability]

def uniformMarkovOperation (P : RationalKernel Model Pair State) (source : Pair → State)
    (E : Finset Pair) (σ : Model)
    (hClosed : ∀ e ∈ E, ∀ y, 0 < realProbability P σ e y → y ∈ usedStates source E)
    (initial : E) : Measure (ℕ → Pair) :=
  operatingPairLaw source E (realProbability P σ)
    (realProbability_nonnegative P σ E) (realProbability_normalized P σ E)
    hClosed (uniformChoices source E) initial

omit [Fintype Pair] [DecidableEq Pair] [MeasurableSpace Pair] [MeasurableSingletonClass Pair] in
/-- Full-row matching transfers the target's zero exit and actual transition closure. -/
theorem matching_component_closed (P : RationalKernel Model Pair State) (source : Pair → State)
    (B : Finset Model) (priority : Model → Pair → ℕ) (θ σ : Model) (allowed E : Finset Pair)
    (hQ : MarkovQualifying P source B priority θ allowed E) (hm : Match P.row θ σ E) :
    ∀ e ∈ E, ∀ y, 0 < realProbability P σ e y → y ∈ usedStates source E := by
  have hn := matching_noExit P B hm hQ.2.1
  intro e he y hy
  apply hQ.2.2.1.closed e he
  apply hn e he y
  change (0 : ℝ) < (P.row σ e y : ℝ) at hy
  exact_mod_cast hy

/-- Operational soundness of the checked self-verifying target: uniform retained
actions win the actual hidden parity objective almost surely under every
full-row-matching live model, from every retained initial pair. -/
theorem qualifying_uniform_wins_matching
    (P : RationalKernel Model Pair State) (source : Pair → State)
    (B : Finset Model) (priority : Model → Pair → ℕ) (θ σ : Model) (hσ : σ ∈ B)
    (allowed E : Finset Pair) (hQ : MarkovQualifying P source B priority θ allowed E)
    (hm : Match P.row θ σ E) (initial : E) :
    ∀ᵐ x ∂uniformMarkovOperation P source E σ
      (matching_component_closed P source B priority θ σ allowed E hQ hm) initial,
      PairParitySuccess (priority σ) x := by
  have hNo := matching_noExit P B hm hQ.2.1
  have hEC : IsEndComponent source (positiveSuccessors (realProbability P σ)) E :=
    endComponent_successor_congr source (internalSuccessors P B)
      (positiveSuccessors (realProbability P σ)) E hQ.2.2.1
      (fun e he => (positiveSuccessors_eq_internal P B σ hσ e (hNo e he)).symm)
  exact uniform_component_parity source E (realProbability P σ)
    (realProbability_nonnegative P σ E) (realProbability_normalized P σ E)
    hEC initial (priority σ) (hQ.2.2.2 σ hσ hm)

/-- The same operation visits every retained pair infinitely often, including any
higher odd priority. Its parity proof does not discard those visits. -/
theorem qualifying_uniform_all_pairs_recur
    (P : RationalKernel Model Pair State) (source : Pair → State)
    (B : Finset Model) (priority : Model → Pair → ℕ) (θ σ : Model) (hσ : σ ∈ B)
    (allowed E : Finset Pair) (hQ : MarkovQualifying P source B priority θ allowed E)
    (hm : Match P.row θ σ E) (initial : E) :
    ∀ᵐ x ∂uniformMarkovOperation P source E σ
      (matching_component_closed P source B priority θ σ allowed E hQ hm) initial,
      Orthemology.Tranche2.RecurrentSupport.recurrentSet x = E := by
  have hNo := matching_noExit P B hm hQ.2.1
  have hEC : IsEndComponent source (positiveSuccessors (realProbability P σ)) E :=
    endComponent_successor_congr source (internalSuccessors P B)
      (positiveSuccessors (realProbability P σ)) E hQ.2.2.1
      (fun e he => (positiveSuccessors_eq_internal P B σ hσ e (hNo e he)).symm)
  exact stationary_component_all_pairs_recur source E (realProbability P σ)
    (realProbability_nonnegative P σ E) (realProbability_normalized P σ E)
    hEC (uniformChoices source E) initial

/-- End-to-end executable target certificate: every state returned by the finite
solver has a concrete entry pair and uniform operation that wins in every
matching live model under the actual normalized transition probabilities. -/
theorem computed_target_uniform_certificate
    (P : RationalKernel Model Pair State) (source : Pair → State)
    (B : Finset Model) (priority : Model → Pair → ℕ) (θ : Model)
    (allowed : Finset Pair) (s : State)
    (hs : s ∈ markovTargetStates P source B priority θ allowed) :
    ∃ E : Finset Pair, ∃ hQ : MarkovQualifying P source B priority θ allowed E,
      ∃ initial : E, source initial = s ∧
        ∀ (σ : Model) (_hσ : σ ∈ B) (hm : Match P.row θ σ E),
          ∀ᵐ x ∂uniformMarkovOperation P source E σ
            (matching_component_closed P source B priority θ σ allowed E hQ hm) initial,
            PairParitySuccess (priority σ) x := by
  obtain ⟨E, hQ, hsE⟩ := (markovTargetStates_exact P source B priority θ allowed s).mp hs
  obtain ⟨e, he, hsrc⟩ := Finset.mem_image.mp hsE
  refine ⟨E, hQ, ⟨e, he⟩, hsrc, ?_⟩
  intro σ hσ hm
  exact qualifying_uniform_wins_matching P source B priority θ σ hσ allowed E hQ hm ⟨e, he⟩

end HiddenParity.Recurrence
