import BlockMismatch
import Q8Measure

namespace Orthemology.Frontier.MealyMeasure
open Set MeasureTheory Filter
open scoped ENNReal Topology BigOperators
open P02A2.Q8Measure
open Orthemology.Frontier

abbrev Cantor := P02A2.Q8Measure.Cantor

def shift (n : ℕ) (x : Cantor) : Cantor := fun k => x (n+k)
def pref (n : ℕ) (x : Cantor) : List Bool := List.ofFn (fun i : Fin n => x i)

def cylinder (u : List Bool) : Set Cantor := {x | pref u.length x = u}

theorem prefix_length (n : ℕ) (x : Cantor) : (pref n x).length = n := by
  simp [pref]

theorem prefix_succ (n : ℕ) (x : Cantor) :
    pref (n+1) x = x 0 :: pref n (shift 1 x) := by
  simp [pref, List.ofFn_succ, shift, Nat.add_comm]

theorem prefix_add (n k : ℕ) (x : Cantor) :
    pref (n+k) x = pref n x ++ pref k (shift n x) := by
  simp [pref, List.ofFn_add, shift]

theorem prefix_eq_iff (n : ℕ) (x z : Cantor) :
    pref n x = pref n z ↔ ∀ i < n, x i = z i := by
  simp only [pref, List.ofFn_inj]
  constructor
  · intro h i hi
    exact congrFun h ⟨i, hi⟩
  · intro h
    funext i
    exact h i i.isLt

theorem cylinder_prefix (n : ℕ) (x : Cantor) :
    cylinder (pref n x) = Set.pi (↑(Finset.range n) : Set ℕ) (fun i => {x i}) := by
  ext z
  simp only [cylinder, mem_setOf_eq, prefix_length, prefix_eq_iff, Set.mem_pi,
    Finset.mem_coe, Finset.mem_range, Set.mem_singleton_iff]

theorem measure_cylinder_prefix (n : ℕ) (x : Cantor) :
    fairCantor (cylinder (pref n x)) = (1/2 : ℝ≥0∞)^n := by
  rw [cylinder_prefix, fairCantor_cylinder, Finset.card_range]

def extend (u : List Bool) : Cantor := fun i => u[i]?.getD false

theorem prefix_extend (u : List Bool) : pref u.length (extend u) = u := by
  apply List.ext_getElem
  · simp [pref]
  · intro i hi hj
    simp [pref, extend, List.getElem?_eq_getElem hj]

theorem measure_cylinder (u : List Bool) :
    fairCantor (cylinder u) = (1/2 : ℝ≥0∞)^u.length := by
  have h := measure_cylinder_prefix u.length (extend u)
  simpa only [prefix_extend] using h

theorem measurableSet_cylinder (u : List Bool) : MeasurableSet (cylinder u) := by
  rw [← prefix_extend u, cylinder_prefix]
  exact MeasurableSet.pi (Finset.countable_toSet _) (fun _ _ => measurableSet_singleton _)

variable {S : Type*}

def state (M : Mealy S) (s : S) (x : Cantor) : ℕ → S
  | 0 => s
  | n+1 => M.next (state M s x n) (x n)

def output (M : Mealy S) (s : S) (x : Cantor) : Cantor :=
  fun n => M.out (state M s x n) (x n)

theorem state_add (M : Mealy S) (s : S) (x : Cantor) (n k : ℕ) :
    state M s x (n+k) = state M (state M s x n) (shift n x) k := by
  induction k with
  | zero => simp [state]
  | succ k ih => simp [state, ih, shift]

theorem state_one (M : Mealy S) (s : S) (x : Cantor) : state M s x 1 = M.next s (x 0) := rfl

theorem state_prefix (M : Mealy S) (s : S) (x : Cantor) (n : ℕ) :
    M.finalState s (pref n x) = state M s x n := by
  induction n generalizing s x with
  | zero => simp [pref, Mealy.finalState, state]
  | succ n ih =>
    rw [prefix_succ, Mealy.finalState, ih]
    simpa [Nat.add_comm, state_one] using (state_add M s x 1 n).symm

theorem output_shift (M : Mealy S) (s : S) (x : Cantor) (n : ℕ) :
    shift n (output M s x) = output M (state M s x n) (shift n x) := by
  funext k
  simp [shift, output, state_add]

theorem output_prefix (M : Mealy S) (s : S) (x : Cantor) (n : ℕ) :
    M.outputWord s (pref n x) = pref n (output M s x) := by
  induction n generalizing s x with
  | zero => simp [pref, Mealy.outputWord]
  | succ n ih =>
    rw [prefix_succ, Mealy.outputWord, ih, prefix_succ]
    congr 1
    rw [output_shift, state_one]

theorem state_prefix_congr (M : Mealy S) (s : S) {x z : Cantor} {n : ℕ}
    (h : pref n x = pref n z) : state M s x n = state M s z n := by
  rw [← state_prefix, ← state_prefix, h]

theorem output_prefix_congr (M : Mealy S) (s : S) {x z : Cantor} {n : ℕ}
    (h : pref n x = pref n z) : pref n (output M s x) = pref n (output M s z) := by
  rw [← output_prefix, ← output_prefix, h]

theorem deterministic_output (M : Mealy S) (s : S) (hs : M.infiniteRel s s)
    (x z : Cantor) : output M s x = output M s z := by
  funext n
  have h := (M.approx_iff_words (n+1) s s).mp (hs (n+1))
    (pref (n+1) x) (pref (n+1) z) (prefix_length _ _) (prefix_length _ _)
  rw [output_prefix, output_prefix, prefix_eq_iff] at h
  exact h n (by omega)


theorem state_measurable [Finite S] [MeasurableSpace S] [MeasurableSingletonClass S]
    (M : Mealy S) (s : S) (n : ℕ) : Measurable (fun x : Cantor => state M s x n) := by
  induction n with
  | zero => exact measurable_const
  | succ n ih =>
    exact (measurable_of_finite (fun p : S × Bool => M.next p.1 p.2)).comp
      (ih.prodMk (measurable_pi_apply n))

theorem output_measurable [Finite S] (M : Mealy S) (s : S) : Measurable (output M s) := by
  letI : MeasurableSpace S := ⊤
  apply measurable_pi_lambda
  intro n
  exact (measurable_of_finite (fun p : S × Bool => M.out p.1 p.2)).comp
    ((state_measurable M s n).prodMk (measurable_pi_apply n))

noncomputable def law (M : Mealy S) (s : S) : Measure Cantor := fairCantor.map (output M s)

instance law_probability [Finite S] (M : Mealy S) (s : S) : IsProbabilityMeasure (law M s) := by
  constructor
  rw [law, Measure.map_apply (output_measurable M s) MeasurableSet.univ]
  simp

def hits (M : Mealy S) (s : S) : Set Cantor :=
  {x | ∃ n, M.infiniteRel (state M s x n) (state M s x n)}

theorem measurableSet_hits [Finite S] (M : Mealy S) (s : S) : MeasurableSet (hits M s) := by
  letI : MeasurableSpace S := ⊤
  have he : hits M s = ⋃ n, (fun x => state M s x n) ⁻¹' {q | M.infiniteRel q q} := by
    ext x
    simp [hits]
  rw [he]
  exact MeasurableSet.iUnion (fun n => (state_measurable M s n)
    (MeasurableSpace.measurableSet_top))

/-- Actual consecutive input blocks, not an abstract independent block process. -/
def blocks (L j : ℕ) (x : Cantor) : List (Mealy.Block L) :=
  List.ofFn (fun k : Fin j => fun i : Fin L => x (k*L+i))

def flattenBlocks {L : ℕ} (w : List (Mealy.Block L)) : List Bool :=
  (w.map List.ofFn).flatten

theorem blocks_length (L j : ℕ) (x : Cantor) : (blocks L j x).length = j := by
  simp [blocks]

theorem blocks_succ (L j : ℕ) (x : Cantor) :
    blocks L (j+1) x = (fun i : Fin L => x i) :: blocks L j (shift L x) := by
  simp only [blocks, List.ofFn_succ]
  congr 1
  · funext i
    simp
  · congr 1
    funext k i
    simp [shift, Nat.add_mul, Nat.add_assoc, Nat.add_left_comm]

theorem flattenBlocks_length {L : ℕ} (w : List (Mealy.Block L)) :
    (flattenBlocks w).length = w.length * L := by
  induction w with
  | nil => simp [flattenBlocks]
  | cons a w ih => simpa [flattenBlocks, Nat.add_mul, Nat.add_comm] using congrArg (L + ·) ih

theorem flatten_blocks (L j : ℕ) (x : Cantor) :
    flattenBlocks (blocks L j x) = pref (j*L) x := by
  simp only [flattenBlocks, blocks, List.map_ofFn, Function.comp_def, pref, List.ofFn_mul]

theorem blocks_mem_surviving [Finite S] [Nonempty S] (M : Mealy S)
    (s : S) (x y : Cantor) (j t : ℕ)
    (hm : ∀ k, output M s x k = y (t*(2*Nat.card S-1)+k))
    (ha : ∀ k, ¬ M.infiniteRel (state M s x k) (state M s x k)) :
    blocks (2*Nat.card S-1) j x ∈ BoundedPaths.words
      (M.survivingBlocks (2*Nat.card S-1)
        (fun t => pref (2*Nat.card S-1) (shift (t*(2*Nat.card S-1)) y)))
      (fun s w => M.finalState s (List.ofFn w)) j t s := by
  classical
  let L := 2*Nat.card S-1
  induction j generalizing s x t with
  | zero => simp [blocks, BoundedPaths.words]
  | succ j ih =>
    rw [blocks_succ]
    apply (BoundedPaths.mem_words_succ _ _ _ _ _ _).mpr
    refine ⟨(fun i : Fin L => x i), ?_, blocks L j (shift L x), ?_, rfl⟩
    · have hstart : ¬ M.infiniteRel s s := by simpa [state] using ha 0
      simp only [Mealy.survivingBlocks, if_neg hstart, Finset.mem_filter,
        Mealy.matchingBlocks, Finset.mem_univ, true_and]
      constructor
      · change M.outputWord s (pref L x) = pref L (shift (t*L) y)
        rw [output_prefix]
        apply (prefix_eq_iff _ _ _).mpr
        intro i hi
        exact hm i
      · change ¬ M.infiniteRel (M.finalState s (pref L x)) (M.finalState s (pref L x))
        simpa only [state_prefix] using ha L
    · change blocks L j (shift L x) ∈ BoundedPaths.words _ _ j (t+1)
        (M.finalState s (pref L x))
      rw [state_prefix]
      apply ih
      · intro k
        have h := hm (L+k)
        rw [← output_shift]
        simpa [shift, Nat.add_mul, Nat.add_assoc] using h
      · intro k
        simpa only [← state_add] using ha (L+k)


theorem flattenBlocks_injective_of_length {L : ℕ} {v w : List (Mealy.Block L)}
    (hl : v.length = w.length) (h : flattenBlocks v = flattenBlocks w) : v = w := by
  induction v generalizing w with
  | nil => simpa using hl.symm
  | cons a v ih =>
    cases w with
    | nil => simp at hl
    | cons b w =>
      have hab := List.append_inj h (by simp : (List.ofFn a).length = (List.ofFn b).length)
      have he : a = b := List.ofFn_injective hab.1
      have ht : v = w := ih (by simpa using hl) hab.2
      simp [he, ht]

theorem block_event_eq_union {L j : ℕ} (F : Finset (List (Mealy.Block L)))
    (hF : ∀ w ∈ F, w.length = j) :
    {x : Cantor | blocks L j x ∈ F} = ⋃ w ∈ F, cylinder (flattenBlocks w) := by
  ext x
  constructor
  · intro hx
    refine mem_iUnion.mpr ⟨blocks L j x, mem_iUnion.mpr ⟨hx, ?_⟩⟩
    simp [cylinder, flattenBlocks_length, blocks_length, flatten_blocks, prefix_length]
  · intro hx
    obtain ⟨w, hw⟩ := mem_iUnion.mp hx
    obtain ⟨hw, hxw⟩ := mem_iUnion.mp hw
    have hl := hF w hw
    have he : blocks L j x = w := by
      apply flattenBlocks_injective_of_length
      · simp [blocks_length, hl]
      · simpa [flatten_blocks, cylinder, flattenBlocks_length, hl] using hxw
    simpa [he] using hw

/-- Exact product-measure interpretation of a finite collection of actual block words. -/
theorem measure_block_event {L j : ℕ} (F : Finset (List (Mealy.Block L)))
    (hF : ∀ w ∈ F, w.length = j) :
    fairCantor {x : Cantor | blocks L j x ∈ F} =
      F.card * (1/2 : ℝ≥0∞)^(j*L) := by
  rw [block_event_eq_union F hF]
  rw [measure_biUnion_finset]
  · simp only [measure_cylinder, flattenBlocks_length]
    have he : (∑ w ∈ F, (1/2 : ℝ≥0∞)^(w.length*L)) =
        ∑ _w ∈ F, (1/2 : ℝ≥0∞)^(j*L) :=
      Finset.sum_congr rfl (fun w hw => by rw [hF w hw])
    rw [he]
    simp
  · intro v hv w hw hne
    apply Set.disjoint_left.mpr
    intro x hxv hxw
    apply hne
    apply flattenBlocks_injective_of_length ((hF v hv).trans (hF w hw).symm)
    change pref (flattenBlocks v).length x = flattenBlocks v at hxv
    change pref (flattenBlocks w).length x = flattenBlocks w at hxw
    simp only [flattenBlocks_length, hF v hv, hF w hw] at hxv hxw
    exact hxv.symm.trans hxw
  · intro w hw
    exact measurableSet_cylinder _

def avoidMatch (M : Mealy S) (s : S) (y : Cantor) : Set Cantor :=
  {x | output M s x = y ∧ x ∉ hits M s}

/-- The earlier finite path count now bounds an event in the actual fair infinite product. -/
theorem avoidMatch_measure_bound [Finite S] [Nonempty S] (M : Mealy S)
    (s : S) (y : Cantor) (j : ℕ) :
    fairCantor (avoidMatch M s y) ≤
      (((2^(2*Nat.card S-1)-1 : ℕ) : ℝ≥0∞) *
        (1/2 : ℝ≥0∞)^(2*Nat.card S-1))^j := by
  classical
  let L := 2*Nat.card S-1
  let target := fun t => pref L (shift (t*L) y)
  let F := BoundedPaths.words (M.survivingBlocks L target)
    (fun s w => M.finalState s (List.ofFn w)) j 0 s
  have hsub : avoidMatch M s y ⊆ {x | blocks L j x ∈ F} := by
    intro x hx
    apply blocks_mem_surviving M s x y j 0
    · intro k
      simpa using congrFun hx.1 k
    · simpa [hits] using hx.2
  have hbound := measure_mono (μ := fairCantor) hsub
  rw [measure_block_event F (fun w hw => BoundedPaths.length_of_mem_words _ _ _ _ _ _ hw)] at hbound
  have hcount : (F.card : ℝ≥0∞) ≤ (((2^L-1)^j : ℕ) : ℝ≥0∞) := by
    exact_mod_cast M.surviving_input_words_bound target j s
  calc
    _ ≤ F.card * (1/2 : ℝ≥0∞)^(j*L) := hbound
    _ ≤ (((2^L-1)^j : ℕ) : ℝ≥0∞) * (1/2 : ℝ≥0∞)^(j*L) :=
      mul_le_mul_right' hcount _
    _ = _ := by rw [Nat.cast_pow, mul_pow, Nat.mul_comm j L, pow_mul]

theorem fair_block_contraction (L : ℕ) :
    ((2^L-1 : ℕ) : ℝ≥0∞) * (1/2 : ℝ≥0∞)^L = 1 - (1/2 : ℝ≥0∞)^L := by
  rw [ENNReal.natCast_sub, Nat.cast_pow]
  norm_num only [Nat.cast_ofNat, Nat.cast_one]
  rw [ENNReal.sub_mul (by intros; exact ENNReal.pow_ne_top (by norm_num)), one_mul]
  congr 1
  rw [← mul_pow]
  rw [one_div, ENNReal.mul_inv_cancel (by norm_num) (by norm_num), one_pow]

/-- Every fixed output has zero probability among inputs whose trajectory never enters D. -/
theorem avoidMatch_null [Finite S] [Nonempty S] (M : Mealy S) (s : S) (y : Cantor) :
    fairCantor (avoidMatch M s y) = 0 := by
  apply le_antisymm _ (zero_le _)
  apply ge_of_tendsto' (ENNReal.tendsto_pow_atTop_nhds_zero_of_lt_one (r :=
    1 - (1/2 : ℝ≥0∞)^(2*Nat.card S-1)) ?_)
  · intro j
    simpa only [fair_block_contraction] using avoidMatch_measure_bound M s y j
  · exact ENNReal.sub_lt_self (by simp) (by simp) (ENNReal.pow_ne_zero (by norm_num) _)


/-- Upon entering D, the entire output is fixed by the input prefix already read. -/
theorem hitting_prefix_determines_output (M : Mealy S) (s : S) (x : Cantor) (n : ℕ)
    (hn : M.infiniteRel (state M s x n) (state M s x n))
    {z : Cantor} (hz : pref n z = pref n x) : output M s z = output M s x := by
  funext k
  by_cases hk : k < n
  · exact (prefix_eq_iff _ _ _).mp (output_prefix_congr M s hz) k hk
  · have he : state M s z n = state M s x n := state_prefix_congr M s hz
    have ht := deterministic_output M (state M s x n) hn (shift n z) (shift n x)
    have hout : shift n (output M s z) = shift n (output M s x) := by
      rw [output_shift, output_shift, he]
      exact ht
    have hv := congrFun hout (k-n)
    simpa [shift, Nat.add_sub_of_le (by omega : n ≤ k)] using hv

/-- Every input that hits D produces a genuinely positive singleton atom. -/
theorem hits_output_positive [Finite S] (M : Mealy S) (s : S) {x : Cantor}
    (hx : x ∈ hits M s) : output M s x ∈ P02A2.positive (law M s) := by
  obtain ⟨n, hn⟩ := hx
  change 0 < law M s {output M s x}
  rw [law, Measure.map_apply (output_measurable M s) (measurableSet_singleton _)]
  have hsub : cylinder (pref n x) ⊆ output M s ⁻¹' {output M s x} := by
    intro z hz
    apply hitting_prefix_determines_output M s x n hn
    simpa [cylinder, prefix_length] using hz
  have hp : 0 < fairCantor (cylinder (pref n x)) := by
    rw [measure_cylinder_prefix]
    exact ENNReal.pow_pos (by norm_num) _
  exact hp.trans_le (measure_mono hsub)

/-- Positive output fibres outside the hitting event form a countable union of null sets. -/
theorem positive_avoiding_null [Finite S] [Nonempty S] (M : Mealy S) (s : S) :
    fairCantor ((output M s ⁻¹' P02A2.positive (law M s)) \ hits M s) = 0 := by
  letI : Countable (P02A2.positive (law M s)) := (P02A2.positive_countable (law M s)).to_subtype
  have hsub : ((output M s ⁻¹' P02A2.positive (law M s)) \ hits M s) ⊆
      ⋃ y : P02A2.positive (law M s), avoidMatch M s y.val := by
    intro x hx
    exact mem_iUnion.mpr ⟨⟨output M s x, hx.1⟩, rfl, hx.2⟩
  apply measure_mono_null hsub
  exact measure_iUnion_null (fun y => avoidMatch_null M s y.val)

/-- Total atomic output mass equals the probability of ever reaching the computed
    deterministic-output domain, for the actual fair infinite-input law. -/
theorem atomic_mass_eq_hitting_probability [Finite S] [Nonempty S]
    (M : Mealy S) (s : S) : P02A2.mass (law M s) = fairCantor (hits M s) := by
  unfold P02A2.mass
  rw [law, Measure.map_apply (output_measurable M s) (P02A2.positive_measurable _)]
  change fairCantor (output M s ⁻¹' P02A2.positive (law M s)) = _
  have hsub : hits M s ⊆ output M s ⁻¹' P02A2.positive (law M s) :=
    fun x hx => hits_output_positive M s hx
  have he := measure_inter_add_diff (μ := fairCantor)
    (output M s ⁻¹' P02A2.positive (law M s)) (measurableSet_hits M s)
  rw [inter_eq_right.mpr hsub, positive_avoiding_null, add_zero] at he
  exact he.symm

/-- An atom exists exactly when some finite input word can reach D. -/
theorem positive_iff_hitting_prefix [Finite S] [Nonempty S] (M : Mealy S) (s : S)
    (y : Cantor) : y ∈ P02A2.positive (law M s) ↔
      ∃ x : Cantor, output M s x = y ∧ x ∈ hits M s := by
  constructor
  · intro hy
    by_contra hn
    have hsub : output M s ⁻¹' {y} ⊆ avoidMatch M s y := by
      intro x hx
      refine ⟨hx, ?_⟩
      intro hhit
      exact hn ⟨x, hx, hhit⟩
    have hz := measure_mono_null hsub (avoidMatch_null M s y)
    have hpos : 0 < fairCantor (output M s ⁻¹' {y}) := by
      simpa only [P02A2.positive, mem_setOf_eq, law,
        Measure.map_apply (output_measurable M s) (measurableSet_singleton y)] using hy
    exact (ne_of_gt hpos) hz
  · rintro ⟨x, rfl, hx⟩
    exact hits_output_positive M s hx


theorem deterministic_state (M : Mealy S) (s : S) (hs : M.infiniteRel s s)
    (x : Cantor) (n : ℕ) : M.infiniteRel (state M s x n) (state M s x n) := by
  rw [← state_prefix]
  exact M.deterministic_finalState hs _

/-- Only the finite output horizon and its endpoint are needed in the geometric estimate. -/
theorem blocks_mem_surviving_finite [Finite S] [Nonempty S] (M : Mealy S)
    (s : S) (x y : Cantor) (j t : ℕ)
    (hm : ∀ k < j*(2*Nat.card S-1), output M s x k = y (t*(2*Nat.card S-1)+k))
    (ha : ¬ M.infiniteRel (state M s x (j*(2*Nat.card S-1)))
      (state M s x (j*(2*Nat.card S-1)))) :
    blocks (2*Nat.card S-1) j x ∈ BoundedPaths.words
      (M.survivingBlocks (2*Nat.card S-1)
        (fun t => pref (2*Nat.card S-1) (shift (t*(2*Nat.card S-1)) y)))
      (fun s w => M.finalState s (List.ofFn w)) j t s := by
  classical
  let L := 2*Nat.card S-1
  induction j generalizing s x t with
  | zero => simp [blocks, BoundedPaths.words]
  | succ j ih =>
    rw [blocks_succ]
    apply (BoundedPaths.mem_words_succ _ _ _ _ _ _).mpr
    refine ⟨(fun i : Fin L => x i), ?_, blocks L j (shift L x), ?_, rfl⟩
    · have hstart : ¬ M.infiniteRel s s := fun hs => ha (deterministic_state M s hs x _)
      simp only [Mealy.survivingBlocks, if_neg hstart, Finset.mem_filter,
        Mealy.matchingBlocks, Finset.mem_univ, true_and]
      constructor
      · change M.outputWord s (pref L x) = pref L (shift (t*L) y)
        rw [output_prefix]
        apply (prefix_eq_iff _ _ _).mpr
        intro i hi
        exact hm i (by change i < (j+1)*L; nlinarith)
      · change ¬ M.infiniteRel (M.finalState s (pref L x)) (M.finalState s (pref L x))
        rw [state_prefix]
        intro hs
        have h := deterministic_state M (state M s x L) hs (shift L x) (j*L)
        rw [← state_add] at h
        apply ha
        simpa [Nat.add_mul, Nat.add_comm, L] using h
    · change blocks L j (shift L x) ∈ BoundedPaths.words _ _ j (t+1)
        (M.finalState s (pref L x))
      rw [state_prefix]
      apply ih
      · intro k hk
        have h := hm (L+k) (by change L+k < (j+1)*L; nlinarith)
        rw [← output_shift]
        simpa [shift, Nat.add_mul, Nat.add_assoc] using h
      · rw [← state_add]
        simpa [Nat.add_mul, Nat.add_comm, L] using ha

/-- Literal finite-horizon estimate: match the target through jL ticks while
    still avoiding D at time jL. Transition closure makes this full avoidance. -/
theorem finite_survivor_measure_bound [Finite S] [Nonempty S] (M : Mealy S)
    (s : S) (y : Cantor) (j : ℕ) :
    fairCantor {x | pref (j*(2*Nat.card S-1)) (output M s x) =
        pref (j*(2*Nat.card S-1)) y ∧
      ¬ M.infiniteRel (state M s x (j*(2*Nat.card S-1)))
        (state M s x (j*(2*Nat.card S-1)))} ≤
      (1 - (1/2 : ℝ≥0∞)^(2*Nat.card S-1))^j := by
  classical
  let L := 2*Nat.card S-1
  let target := fun t => pref L (shift (t*L) y)
  let F := BoundedPaths.words (M.survivingBlocks L target)
    (fun s w => M.finalState s (List.ofFn w)) j 0 s
  have hsub : {x | pref (j*L) (output M s x) = pref (j*L) y ∧
      ¬ M.infiniteRel (state M s x (j*L)) (state M s x (j*L))} ⊆
      {x | blocks L j x ∈ F} := by
    intro x hx
    apply blocks_mem_surviving_finite M s x y j 0
    · simpa using (prefix_eq_iff _ _ _).mp hx.1
    · exact hx.2
  have hbound := measure_mono (μ := fairCantor) hsub
  rw [measure_block_event F (fun w hw => BoundedPaths.length_of_mem_words _ _ _ _ _ _ hw)] at hbound
  have hcount : (F.card : ℝ≥0∞) ≤ (((2^L-1)^j : ℕ) : ℝ≥0∞) := by
    exact_mod_cast M.surviving_input_words_bound target j s
  calc
    _ ≤ F.card * (1/2 : ℝ≥0∞)^(j*L) := hbound
    _ ≤ (((2^L-1)^j : ℕ) : ℝ≥0∞) * (1/2 : ℝ≥0∞)^(j*L) :=
      mul_le_mul_right' hcount _
    _ = (((2^L-1 : ℕ) : ℝ≥0∞) * (1/2 : ℝ≥0∞)^L)^j := by
      rw [Nat.cast_pow, mul_pow, Nat.mul_comm j L, pow_mul]
    _ = _ := by rw [fair_block_contraction]

end Orthemology.Frontier.MealyMeasure
