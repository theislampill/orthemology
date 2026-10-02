import MealyMeasure

namespace Orthemology.Frontier.MealyMeasure
open Set MeasureTheory Filter
open scoped ENNReal Topology BigOperators
open P02A2.Q8Measure

variable {S : Type*}

/-- A constructive decision procedure for each finite universal-input approximant. -/
instance approxRelDecidable (M : Mealy S) (n : ℕ) : DecidableRel (M.approx n).rel := by
  induction n with
  | zero => exact fun _ _ => isTrue trivial
  | succ n ih =>
    letI := ih
    intro s t
    change Decidable (∀ b c, M.out s b = M.out t c ∧ (M.approx n).rel (M.next s b) (M.next t c))
    infer_instance

/-- Executable finite-state membership in D at the sharp, proved horizon. -/
def deterministicBit [Fintype S] (M : Mealy S) (s : S) : Bool :=
  decide ((M.approx (2 * Fintype.card S - 1)).rel s s)

theorem deterministicBit_spec [Fintype S] [Nonempty S] (M : Mealy S) (s : S) :
    deterministicBit M s = true ↔ M.infiniteRel s s := by
  simp only [deterministicBit, decide_eq_true_eq]
  simpa only [Nat.card_eq_fintype_card] using M.bound_iff_infinite s s

/-- All n-bit input prefixes whose execution has reached D by time n. -/
def hittingBlocks [Fintype S] (M : Mealy S) (s : S) (n : ℕ) : Finset (Mealy.Block n) :=
  Finset.univ.filter (fun w => deterministicBit M (M.finalState s (List.ofFn w)) = true)

/-- A fully executable exact rational finite-horizon hitting probability. -/
def hittingProbabilityQ [Fintype S] (M : Mealy S) (s : S) (n : ℕ) : ℚ :=
  (hittingBlocks M s n).card / (2 : ℚ)^n

def hitAt (M : Mealy S) (s : S) (n : ℕ) : Set Cantor :=
  {x | M.infiniteRel (state M s x n) (state M s x n)}

theorem hitAt_mono (M : Mealy S) (s : S) : Monotone (hitAt M s) := by
  intro n k hnk x hx
  have h := deterministic_state M (state M s x n) hx (shift n x) (k-n)
  simpa [← state_add, Nat.add_sub_of_le hnk] using h

theorem hits_eq_iUnion_hitAt (M : Mealy S) (s : S) : hits M s = ⋃ n, hitAt M s n := by
  ext x
  simp [hits, hitAt]

/-- Exact fair-product formula for any finite collection of length-n input blocks. -/
theorem measure_prefix_event (n : ℕ) (A : Finset (Mealy.Block n)) :
    fairCantor {x : Cantor | (fun i : Fin n => x i) ∈ A} =
      A.card * (1/2 : ℝ≥0∞)^n := by
  classical
  let F : Finset (List (Mealy.Block n)) := A.image (fun w => [w])
  have he : {x : Cantor | (fun i : Fin n => x i) ∈ A} =
      {x : Cantor | blocks n 1 x ∈ F} := by
    ext x
    simp [F, blocks, List.ofFn_succ]
  have hl : ∀ w ∈ F, w.length = 1 := by
    intro w hw
    obtain ⟨a, ha, rfl⟩ := Finset.mem_image.mp hw
    rfl
  have hc : F.card = A.card := Finset.card_image_of_injective _ (by
    intro a b h
    simpa using h)
  rw [he, measure_block_event F hl, hc, one_mul]

theorem hitAt_eq_prefix_event [Fintype S] [Nonempty S] (M : Mealy S) (s : S) (n : ℕ) :
    hitAt M s n = {x : Cantor | (fun i : Fin n => x i) ∈ hittingBlocks M s n} := by
  ext x
  simp only [hitAt, mem_setOf_eq, hittingBlocks, Finset.mem_filter,
    Finset.mem_univ, true_and, deterministicBit_spec]
  change M.infiniteRel (state M s x n) (state M s x n) ↔
    M.infiniteRel (M.finalState s (pref n x)) (M.finalState s (pref n x))
  rw [state_prefix]

/-- The computed finite cardinality equals an actual infinite-product event probability. -/
theorem measure_hitAt [Fintype S] [Nonempty S] (M : Mealy S) (s : S) (n : ℕ) :
    fairCantor (hitAt M s n) = (hittingBlocks M s n).card / (2 : ℝ≥0∞)^n := by
  rw [hitAt_eq_prefix_event, measure_prefix_event]
  simp [div_eq_mul_inv, ENNReal.inv_pow]

/-- The executable rational value is exactly the real value of the genuine event probability. -/
theorem hittingProbabilityQ_correct [Fintype S] [Nonempty S] (M : Mealy S) (s : S) (n : ℕ) :
    (hittingProbabilityQ M s n : ℝ) = (fairCantor (hitAt M s n)).toReal := by
  rw [measure_hitAt]
  simp [hittingProbabilityQ, ENNReal.toReal_div, ENNReal.toReal_pow]

/-- Atomic mass is the increasing limit of the exact computed finite-horizon probabilities.
    This limit statement alone does not assert rationality of the infinite-horizon value. -/
theorem atomic_mass_tendsto_finite_hitting [Fintype S] [Nonempty S] (M : Mealy S) (s : S) :
    Tendsto (fun n => (hittingBlocks M s n).card / (2 : ℝ≥0∞)^n)
      atTop (𝓝 (P02A2.mass (law M s))) := by
  have h := tendsto_measure_iUnion_atTop (μ := fairCantor) (hitAt_mono M s)
  rw [← hits_eq_iUnion_hitAt, ← atomic_mass_eq_hitting_probability] at h
  simpa only [Function.comp_def, measure_hitAt] using h

/-- A finite word reaching D puts its whole, positive-measure input cylinder in the hitting event. -/
theorem reaching_cylinder_subset_hits (M : Mealy S) (s : S) (u : List Bool)
    (hu : M.infiniteRel (M.finalState s u) (M.finalState s u)) :
    cylinder u ⊆ hits M s := by
  intro x hx
  refine ⟨u.length, ?_⟩
  rw [← state_prefix, hx]
  exact hu

/-- Zero atomic mass has an exact finite-word reachability characterization. -/
theorem atomic_mass_zero_iff_unreachable [Finite S] [Nonempty S] (M : Mealy S) (s : S) :
    P02A2.mass (law M s) = 0 ↔
      ∀ u : List Bool, ¬ M.infiniteRel (M.finalState s u) (M.finalState s u) := by
  rw [atomic_mass_eq_hitting_probability]
  constructor
  · intro hz u hu
    have hle := measure_mono (μ := fairCantor) (reaching_cylinder_subset_hits M s u hu)
    rw [measure_cylinder, hz] at hle
    have hp : 0 < (1/2 : ℝ≥0∞)^u.length := ENNReal.pow_pos (by norm_num) _
    exact (not_le_of_gt hp) hle
  · intro h
    have he : hits M s = ∅ := by
      ext x
      simp only [hits, mem_setOf_eq, mem_empty_iff_false, iff_false, not_exists]
      intro n hn
      exact h (pref n x) (by simpa [state_prefix] using hn)
    rw [he, measure_empty]

end Orthemology.Frontier.MealyMeasure
