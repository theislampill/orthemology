import BlockController

/-!
# A concrete shared, measurable support-block policy

Finite-list greedy maximization fixes ties independently of the true model.
History recursion reads exactly the already-sampled stack prefixes. This supplies
the maximum-likelihood rule used by the stochastic block-controller theorem.
-/

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped Topology

namespace Orthemology.Tranche2

variable {Θ A Y Ω : Type*} [Fintype Θ] [Fintype A]

/-- Fixed finite-list tie-breaking; no true-model index is an argument. -/
def greedyMax (score : Θ → ℝ) (best : Θ) : List Θ → Θ
  | [] => best
  | c :: cs => if score best ≤ score c then greedyMax score c cs else greedyMax score best cs

omit [Fintype Θ] in
lemma greedyMax_ge (score : Θ → ℝ) (best : Θ) (cs : List Θ) :
    ∀ σ, σ = best ∨ σ ∈ cs → score σ ≤ score (greedyMax score best cs) := by
  induction cs generalizing best with
  | nil =>
    intro σ h
    simp only [List.not_mem_nil, or_false] at h
    subst σ
    exact le_rfl
  | cons c cs ih =>
    intro σ h
    simp only [List.mem_cons] at h
    unfold greedyMax
    split_ifs with hc
    · rcases h with hb | hh | hmem
      · rw [hb]
        exact hc.trans (ih c c (Or.inl rfl))
      · rw [hh]
        exact ih c c (Or.inl rfl)
      · exact ih c σ (Or.inr hmem)
    · rcases h with hb | hh | hmem
      · rw [hb]
        exact ih best best (Or.inl rfl)
      · rw [hh]
        exact (le_of_not_ge hc).trans (ih best best (Or.inl rfl))
      · exact ih best σ (Or.inr hmem)

def historyCount (support : Θ → Finset A) (hist : List Θ) (a : A) : ℕ := by
  classical
  exact hist.countP (fun σ => a ∈ support σ)

def candidateFor (P : Θ → A → Y → ℝ) (support : Θ → Finset A)
    (X : A → ℕ → Ω → Y) (initial : Θ) (hist : List Θ) (ω : Ω) : Θ := by
  classical
  exact greedyMax (fun σ => prefixLikelihood (P σ) X (historyCount support hist) ω)
    initial Finset.univ.toList

def canonicalHistory (P : Θ → A → Y → ℝ) (support : Θ → Finset A)
    (X : A → ℕ → Ω → Y) (initial : Θ) : ℕ → Ω → List Θ
  | 0, _ => []
  | n+1, ω =>
      let hist := canonicalHistory P support X initial n ω
      hist ++ [candidateFor P support X initial hist ω]

def canonicalSelected (P : Θ → A → Y → ℝ) (support : Θ → Finset A)
    (X : A → ℕ → Ω → Y) (initial : Θ) (ω : Ω) (n : ℕ) : Θ :=
  candidateFor P support X initial (canonicalHistory P support X initial n ω) ω

lemma canonicalHistory_eq_range_map (P : Θ → A → Y → ℝ) (support : Θ → Finset A)
    (X : A → ℕ → Ω → Y) (initial : Θ) (ω : Ω) (n : ℕ) :
    canonicalHistory P support X initial n ω =
      (List.range n).map (canonicalSelected P support X initial ω) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [List.range_succ, List.map_append, List.map_singleton]
    change canonicalHistory P support X initial n ω ++
      [canonicalSelected P support X initial ω n] = _
    rw [ih]

lemma historyCount_eq_blockCount (P : Θ → A → Y → ℝ) (support : Θ → Finset A)
    (X : A → ℕ → Ω → Y) (initial : Θ) (ω : Ω) (n : ℕ) (a : A) :
    historyCount support (canonicalHistory P support X initial n ω) a =
      blockCount support (canonicalSelected P support X initial ω) a n := by
  classical
  rw [canonicalHistory_eq_range_map]
  simp [historyCount, blockCount, Nat.count, List.countP_map, Function.comp_def]

lemma canonicalSelected_maximizes (P : Θ → A → Y → ℝ) (support : Θ → Finset A)
    (X : A → ℕ → Ω → Y) (initial : Θ) (ω : Ω) (n : ℕ) (σ : Θ) :
    prefixLikelihood (P σ) X
      (fun a => blockCount support (canonicalSelected P support X initial ω) a n) ω ≤
    prefixLikelihood (P (canonicalSelected P support X initial ω n)) X
      (fun a => blockCount support (canonicalSelected P support X initial ω) a n) ω := by
  classical
  simp_rw [← historyCount_eq_blockCount P support X initial ω n]
  simpa only [canonicalSelected, candidateFor] using
    (greedyMax_ge (fun ζ => prefixLikelihood (P ζ) X
      (historyCount support (canonicalHistory P support X initial n ω)) ω)
      initial Finset.univ.toList σ (Or.inr (by simp)))

/-- The next model choice is invariant under changing every unacquired stack entry. -/
lemma candidateFor_prefix_local (P : Θ → A → Y → ℝ) (support : Θ → Finset A)
    (X : A → ℕ → Ω → Y) (initial : Θ) (hist : List Θ) (ω ω' : Ω)
    (h : ∀ a i, i < historyCount support hist a → X a i ω = X a i ω') :
    candidateFor P support X initial hist ω = candidateFor P support X initial hist ω' := by
  classical
  have hs : (fun σ => prefixLikelihood (P σ) X (historyCount support hist) ω) =
      (fun σ => prefixLikelihood (P σ) X (historyCount support hist) ω') := by
    funext σ
    apply Finset.prod_congr rfl
    intro a _
    apply Finset.prod_congr rfl
    intro i hi
    rw [h a i (Finset.mem_range.mp hi)]
  unfold candidateFor
  rw [hs]

section Measurability
variable [Fintype Y]
variable [MeasurableSpace Θ] [MeasurableSingletonClass Θ]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y] [MeasurableSpace Ω]

omit [Fintype Θ] [MeasurableSingletonClass Θ] in
lemma greedyMax_measurable (scores : Ω → Θ → ℝ)
    (hs : ∀ σ, Measurable (fun ω => scores ω σ)) (best : Θ) (cs : List Θ) :
    Measurable (fun ω => greedyMax (scores ω) best cs) := by
  induction cs generalizing best with
  | nil => exact measurable_const
  | cons c cs ih =>
    exact Measurable.ite (measurableSet_le (hs best) (hs c)) (ih c) (ih best)

omit [MeasurableSingletonClass Θ] in
lemma candidateFor_measurable (P : Θ → A → Y → ℝ) (support : Θ → Finset A)
    (X : A → ℕ → Ω → Y) (initial : Θ) (hist : List Θ)
    (hX : ∀ a n, Measurable (X a n)) :
    Measurable (candidateFor P support X initial hist) := by
  classical
  apply greedyMax_measurable
  intro σ
  apply Finset.measurable_prod
  intro a _
  apply Finset.measurable_prod
  intro i _
  exact (measurable_of_countable (P σ a)).comp (hX a i)

lemma measurable_countable_diagonal {D E : Type*} [MeasurableSpace D]
    [MeasurableSingletonClass D] [Countable D] [MeasurableSpace E]
    (f : D → Ω → E) (hf : ∀ d, Measurable (f d))
    (g : Ω → D) (hg : Measurable g) : Measurable (fun ω => f (g ω) ω) := by
  have hj : Measurable (fun z : Ω × D => f z.2 z.1) :=
    measurable_from_prod_countable hf
  exact hj.comp (measurable_id.prodMk hg)

theorem canonicalSelected_measurable (P : Θ → A → Y → ℝ) (support : Θ → Finset A)
    (X : A → ℕ → Ω → Y) (initial : Θ) (n : ℕ)
    (hX : ∀ a n, Measurable (X a n)) :
    Measurable (fun ω => canonicalSelected P support X initial ω n) := by
  classical
  letI : MeasurableSpace (List Θ) := ⊤
  have hh : ∀ n, Measurable (canonicalHistory P support X initial n) := by
    intro n
    induction n with
    | zero => exact measurable_const
    | succ n ih =>
      have hc := measurable_countable_diagonal
        (candidateFor P support X initial)
        (fun hist => candidateFor_measurable P support X initial hist hX)
        (canonicalHistory P support X initial n) ih
      have happ : Measurable (fun z : List Θ × Θ => z.1 ++ [z.2]) := measurable_of_countable _
      exact happ.comp (ih.prodMk hc)
  exact measurable_countable_diagonal
    (candidateFor P support X initial)
    (fun hist => candidateFor_measurable P support X initial hist hX)
    (canonicalHistory P support X initial n) (hh n)

end Measurability

section Probability
variable [Fintype Y]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]
variable [MeasurableSpace Ω] {μ : Measure Ω} [IsProbabilityMeasure μ]

/-- A concrete shared selector, not an assumed maximization oracle, obtains
almost-sure eventual nonempty target-good support blocks under the true model. -/
theorem canonical_block_policy_eventually_good
    (P : Θ → A → Y → ℝ) (good support : Θ → Finset A) (θ initial : Θ)
    (X : A → ℕ → Ω → Y)
    (hP : ∀ σ a y, 0 < P σ a y)
    (hPsum : ∀ σ a, ∑ y, P σ a y = 1)
    (hnonempty : ∀ σ, (support σ).Nonempty)
    (hsupport : ∀ σ, SelfVerifying good (fun η ζ a => P η a = P ζ a) σ (support σ))
    (hX : ∀ a n, Measurable (X a n))
    (hindep : iIndepFun (fun an : A × ℕ => X an.1 an.2) μ)
    (hident : ∀ a n, IdentDistrib (X a n) (X a 0) μ μ)
    (hLaw : ∀ a y, (Measure.map (X a 0) μ).real {y} = P θ a y) :
    ∀ᵐ ω ∂μ, ∀ᶠ n : ℕ in atTop,
      (support (canonicalSelected P support X initial ω n)).Nonempty ∧
      support (canonicalSelected P support X initial ω n) ⊆ good θ := by
  apply likelihood_block_controller_eventually_good P good support θ X
    (canonicalSelected P support X initial) hP hPsum hnonempty hsupport hX hindep hident hLaw
  exact canonicalSelected_maximizes P support X initial

end Probability
end Orthemology.Tranche2
