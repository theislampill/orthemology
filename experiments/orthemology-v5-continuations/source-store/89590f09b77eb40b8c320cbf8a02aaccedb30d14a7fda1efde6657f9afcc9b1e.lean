import MealyRefinement
import Mathlib.Data.List.OfFn
import Mathlib.Data.Finset.Sigma

/-!
# Quantitative finite-word mismatch from the sharp refinement bound

No measure-theoretic claim is imported into these statements. The central theorem
counts actual finite block-input paths that keep matching a prescribed output while
avoiding deterministic-output states. IID fair-input probabilities are obtained by
normalising by the explicit total number of input blocks.
-/

namespace Orthemology.Frontier

namespace BoundedPaths

variable {S I : Type*} [DecidableEq I]

/-- Actual accepted block sequences, retaining the entire input word as the witness. -/
def words (allowed : ℕ → S → Finset I) (next : S → I → S) :
    ℕ → ℕ → S → Finset (List I)
  | 0, _, _ => {[]}
  | n+1, t, s => ((allowed t s).sigma
      (fun a => words allowed next n (t+1) (next s a))).image
        (fun pair => pair.1 :: pair.2)

/-- The tree cardinality really is the sum over its distinct first input blocks. -/
theorem card_words_succ (allowed : ℕ → S → Finset I) (next : S → I → S)
    (n t : ℕ) (s : S) :
    (words allowed next (n+1) t s).card =
      ∑ a ∈ allowed t s, (words allowed next n (t+1) (next s a)).card := by
  rw [words, Finset.card_image_of_injective]
  · exact Finset.card_sigma _ _
  · intro a b h
    cases a with
    | mk a as =>
      cases b with
      | mk b bs =>
        obtain ⟨rfl, rfl⟩ := List.cons.inj h
        rfl

/-- A local maximum of `K` surviving input blocks gives at most `K^n` surviving paths. -/
theorem card_words_le_pow (allowed : ℕ → S → Finset I) (next : S → I → S)
    (K : ℕ) (local_bound : ∀ t s, (allowed t s).card ≤ K)
    (n t : ℕ) (s : S) : (words allowed next n t s).card ≤ K^n := by
  induction n generalizing t s with
  | zero => simp [words]
  | succ n ih =>
    rw [card_words_succ]
    calc
      ∑ a ∈ allowed t s, (words allowed next n (t+1) (next s a)).card
          ≤ ∑ _a ∈ allowed t s, K^n := Finset.sum_le_sum (fun a _ => ih _ _)
      _ = (allowed t s).card * K^n := by simp
      _ ≤ K * K^n := Nat.mul_le_mul_right _ (local_bound t s)
      _ = K^(n+1) := by rw [pow_succ, Nat.mul_comm]

/-- Membership exposes the complete, state-dependent path semantics. -/
theorem mem_words_succ (allowed : ℕ → S → Finset I) (next : S → I → S)
    (n t : ℕ) (s : S) (word : List I) :
    word ∈ words allowed next (n+1) t s ↔
      ∃ a ∈ allowed t s, ∃ tail ∈ words allowed next n (t+1) (next s a),
        a :: tail = word := by
  simp [words]
  aesop

/-- Every accepted path contains exactly the declared number of input blocks. -/
theorem length_of_mem_words (allowed : ℕ → S → Finset I) (next : S → I → S)
    (n t : ℕ) (s : S) (word : List I) (h : word ∈ words allowed next n t s) :
    word.length = n := by
  induction n generalizing t s word with
  | zero => simpa [words] using h
  | succ n ih =>
    obtain ⟨a, ha, tail, ht, rfl⟩ := (mem_words_succ _ _ _ _ _ _).mp h
    simp [ih _ _ _ ht]

/-- The complete sample space has exactly `card I ^ n` distinct block words. -/
theorem card_all_words [Fintype I] (next : S → I → S) (n t : ℕ) (s : S) :
    (words (fun _ _ => Finset.univ) next n t s).card = (Fintype.card I)^n := by
  induction n generalizing t s with
  | zero => simp [words]
  | succ n ih =>
    rw [card_words_succ]
    simp [ih, pow_succ, Nat.mul_comm]

/-- Acceptance removes words from that complete uniform input sample space. -/
theorem words_subset_all [Fintype I] (allowed : ℕ → S → Finset I) (next : S → I → S)
    (n t : ℕ) (s : S) :
    words allowed next n t s ⊆ words (fun _ _ => Finset.univ) next n t s := by
  induction n generalizing t s with
  | zero => exact fun _ h => h
  | succ n ih =>
    intro word hw
    obtain ⟨a, ha, tail, ht, rfl⟩ := (mem_words_succ _ _ _ _ _ _).mp hw
    exact (mem_words_succ _ _ _ _ _ _).mpr
      ⟨a, Finset.mem_univ _, tail, ih _ _ ht, rfl⟩

end BoundedPaths

namespace Mealy
variable {S : Type*}

def finalState (M : Mealy S) : S → List Bool → S
  | s, [] => s
  | s, b :: bs => M.finalState (M.next s b) bs

/-- Once a state has input-independent infinite output, every successor does too. -/
theorem deterministic_domain_closed (M : Mealy S) {s : S}
    (hs : M.infiniteRel s s) (b : Bool) :
    M.infiniteRel (M.next s b) (M.next s b) := by
  intro n
  exact (hs (n+1) b b).2

theorem deterministic_finalState (M : Mealy S) {s : S}
    (hs : M.infiniteRel s s) (u : List Bool) :
    M.infiniteRel (M.finalState s u) (M.finalState s u) := by
  induction u generalizing s with
  | nil => exact hs
  | cons b bs ih => exact ih (M.deterministic_domain_closed hs b)

abbrev Block (L : ℕ) := Fin L → Bool

/-- Convert any length-`L` list witness into a finite block function without changing it. -/
theorem exists_block_of_length {L : ℕ} (u : List Bool) (hu : u.length = L) :
    ∃ w : Block L, List.ofFn w = u := by
  subst L
  exact ⟨u.get, List.ofFn_get u⟩

/-- At least one input block mismatches any proposed target block outside the deterministic domain. -/
theorem exists_mismatch_block [Finite S] [Nonempty S] (M : Mealy S)
    (s : S) (hs : ¬ M.infiniteRel s s) (target : List Bool) :
    ∃ w : Block (2 * Nat.card S - 1), M.outputWord s (List.ofFn w) ≠ target := by
  obtain ⟨u, v, hu, hv, hne⟩ := M.distinguishing_words s hs
  obtain ⟨wu, hwu⟩ := exists_block_of_length u hu
  obtain ⟨wv, hwv⟩ := exists_block_of_length v hv
  by_cases hut : M.outputWord s u = target
  · refine ⟨wv, ?_⟩
    rw [hwv]
    intro hvt
    exact hne (hut.trans hvt.symm)
  · exact ⟨wu, by simpa [hwu] using hut⟩

/-- All matching blocks, before imposing domain avoidance. -/
noncomputable def matchingBlocks (M : Mealy S) (L : ℕ) (s : S) (target : List Bool) :
    Finset (Block L) := by
  classical
  exact Finset.univ.filter (fun w => M.outputWord s (List.ofFn w) = target)

/-- The sharp finite witness excludes at least one of the `2^L` possible blocks. -/
theorem card_matchingBlocks_le [Finite S] [Nonempty S] (M : Mealy S)
    (s : S) (hs : ¬ M.infiniteRel s s) (target : List Bool) :
    (M.matchingBlocks (2 * Nat.card S - 1) s target).card ≤
      2^(2 * Nat.card S - 1) - 1 := by
  classical
  obtain ⟨w, hw⟩ := M.exists_mismatch_block s hs target
  have hproper : M.matchingBlocks (2 * Nat.card S - 1) s target ⊂ Finset.univ := by
    apply Finset.filter_ssubset.mpr
    exact ⟨w, Finset.mem_univ _, hw⟩
  have hc := Finset.card_lt_card hproper
  have huniv : (Finset.univ : Finset (Block (2 * Nat.card S - 1))).card =
      2^(2 * Nat.card S - 1) := by simp [Block, Fintype.card_fun]
  rw [huniv] at hc
  omega

/-- Retain only output-matching blocks whose endpoints both avoid the deterministic domain. -/
noncomputable def survivingBlocks (M : Mealy S) (L : ℕ) (target : ℕ → List Bool)
    (t : ℕ) (s : S) : Finset (Block L) := by
  classical
  exact if M.infiniteRel s s then ∅ else
    (M.matchingBlocks L s (target t)).filter (fun w =>
      let s' := M.finalState s (List.ofFn w)
      ¬ M.infiniteRel s' s')

/-- Uniform local survivor bound, including states already in the deterministic domain. -/
theorem card_survivingBlocks_le [Finite S] [Nonempty S] (M : Mealy S)
    (target : ℕ → List Bool) (t : ℕ) (s : S) :
    (M.survivingBlocks (2 * Nat.card S - 1) target t s).card ≤
      2^(2 * Nat.card S - 1) - 1 := by
  classical
  by_cases hs : M.infiniteRel s s
  · simp [survivingBlocks, hs]
  · simp only [survivingBlocks, if_neg hs]
    exact (Finset.card_filter_le _ _).trans (M.card_matchingBlocks_le s hs (target t))

/-- The exact exponential count bound for arbitrary fixed output-block targets. -/
theorem surviving_input_words_bound [Finite S] [Nonempty S] (M : Mealy S)
    (target : ℕ → List Bool) (j : ℕ) (s : S) :
    (BoundedPaths.words (M.survivingBlocks (2 * Nat.card S - 1) target)
      (fun s w => M.finalState s (List.ofFn w)) j 0 s).card ≤
        (2^(2 * Nat.card S - 1) - 1)^j := by
  classical
  exact BoundedPaths.card_words_le_pow _ _ _ (M.card_survivingBlocks_le target) _ _ _

/-- Normalising the actual finite input count gives the geometric fair-block bound.
This is a rational finite-sample-space statement, not an assertion about infinite measures. -/
theorem surviving_uniform_fraction_bound [Finite S] [Nonempty S] (M : Mealy S)
    (target : ℕ → List Bool) (j : ℕ) (s : S) :
    ((BoundedPaths.words (M.survivingBlocks (2 * Nat.card S - 1) target)
      (fun s w => M.finalState s (List.ofFn w)) j 0 s).card : ℚ) /
        ((2 : ℚ)^(2 * Nat.card S - 1))^j ≤
          (1 - 1 / (2 : ℚ)^(2 * Nat.card S - 1))^j := by
  classical
  let L := 2 * Nat.card S - 1
  have hcount := M.surviving_input_words_bound target j s
  have hc : ((BoundedPaths.words (M.survivingBlocks L target)
      (fun s w => M.finalState s (List.ofFn w)) j 0 s).card : ℚ) ≤
      (((2^L - 1)^j : ℕ) : ℚ) := by exact_mod_cast hcount
  have hpos : 0 < (2 : ℚ)^L := by positivity
  have hcast : ((2^L - 1 : ℕ) : ℚ) = (2 : ℚ)^L - 1 := by
    have hnpos : 0 < (2 : ℕ)^L := by positivity
    have hn : 1 ≤ (2 : ℕ)^L := by omega
    rw [Nat.cast_sub hn, Nat.cast_pow]
    norm_num
  calc
    _ ≤ (((2^L - 1)^j : ℕ) : ℚ) / ((2 : ℚ)^L)^j :=
      div_le_div_of_nonneg_right hc (by positivity)
    _ = (((2 : ℚ)^L - 1) / (2 : ℚ)^L)^j := by rw [Nat.cast_pow, hcast, div_pow]
    _ = _ := by
      congr 1
      dsimp [L]
      field_simp

end Mealy
end Orthemology.Frontier
