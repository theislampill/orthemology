import MicroQueue

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators

namespace Orthemology.Tranche2.MicroPolicy
open PolicyEmbedding
variable {A Y Ω : Type*}

/-- Likelihood of precisely the acquired transcript; newest-first storage is harmless
because the score multiplication is commutative. -/
def historyScore (p : A → Y → ℝ) (h : History A Y) : ℝ :=
  (h.map (fun ay => p ay.1 ay.2)).prod

@[simp] lemma historyScore_nil (p : A → Y → ℝ) : historyScore p [] = 1 := rfl

@[simp] lemma historyScore_cons (p : A → Y → ℝ) (a : A) (y : Y)
    (h : History A Y) : historyScore p ((a,y) :: h) = p a y * historyScore p h := rfl

variable [DecidableEq A]

@[simp] lemma actionCount_nil (a : A) : actionCount a ([] : History A Y) = 0 := rfl

lemma actionCount_cons (a b : A) (y : Y) (h : History A Y) :
    actionCount a ((b,y) :: h) = actionCount a h + if a = b then 1 else 0 := by
  by_cases hab : a = b
  · subst b; simp [actionCount]
  · simp [actionCount,hab,Ne.symm hab]

/-- Feeding a list performs exactly its action multiplicities. -/
theorem feed_count (X : A → ℕ → Y) (h : History A Y) (as : List A) (a : A) :
    actionCount a (feed X h as) = actionCount a h + as.count a := by
  induction as generalizing h with
  | nil => simp [feed]
  | cons b as ih =>
    rw [feed,ih,actionCount_cons]
    by_cases hab : a = b
    · subst b; simp [Nat.add_assoc,Nat.add_comm,Nat.add_left_comm]
    · simp [hab,Ne.symm hab]

/-- A nonduplicating support block adds one observation exactly on its support. -/
theorem feed_count_nodup (X : A → ℕ → Y) (h : History A Y) (as : List A)
    (hn : as.Nodup) (a : A) :
    actionCount a (feed X h as) = actionCount a h + if a ∈ as then 1 else 0 := by
  rw [feed_count,List.count_eq_of_nodup hn]

/-- This applies to arbitrary finite supports, including multi-action blocks. -/
theorem feed_count_finset (X : A → ℕ → Y) (h : History A Y) (s : Finset A) (a : A) :
    actionCount a (feed X h s.toList) = actionCount a h + if a ∈ s then 1 else 0 := by
  simpa using feed_count_nodup X h s.toList s.nodup_toList a

section Likelihood
variable [Fintype A]

/-- Appending one fresh stack observation multiplies the prefix likelihood by
exactly that observation's score. No positivity or probability assumptions occur. -/
theorem prefixLikelihood_update (p : A → Y → ℝ) (X : A → ℕ → Ω → Y)
    (N : A → ℕ) (ω : Ω) (a : A) :
    prefixLikelihood p X (Function.update N a (N a + 1)) ω =
      p a (X a (N a) ω) * prefixLikelihood p X N ω := by
  let f : A → ℝ := fun b => ∏ i ∈ Finset.range (N b), p b (X b i ω)
  have hf : (fun b => ∏ i ∈ Finset.range (Function.update N a (N a + 1) b),
      p b (X b i ω)) = Function.update f a (f a * p a (X a (N a) ω)) := by
    funext b
    by_cases hba : b = a
    · subst b; simp [f,Finset.prod_range_succ]
    · simp [Function.update_of_ne hba,f]
  unfold prefixLikelihood
  rw [hf,Finset.prod_update_of_mem (Finset.mem_univ a)]
  change (f a * p a (X a (N a) ω)) * _ = p a (X a (N a) ω) * ∏ b, f b
  rw [Finset.prod_eq_mul_prod_diff_singleton (Finset.mem_univ a) f]
  ring

omit [Fintype A] in
/-- Counts after a fresh transcript step are a single-coordinate update. -/
lemma actionCount_fresh_eq_update (X : A → ℕ → Y) (h : History A Y) (a : A) :
    (fun b => actionCount b ((a, X a (actionCount a h)) :: h)) =
      Function.update (fun b => actionCount b h) a (actionCount a h + 1) := by
  funext b
  rw [actionCount_cons]
  by_cases hba : b = a
  · subst b; simp
  · simp [hba,Function.update_of_ne hba]

/-- The acquired-transcript likelihood invariant is preserved by a fresh action. -/
theorem historyScore_fresh (p : A → Y → ℝ) (X : A → ℕ → Ω → Y)
    (h : History A Y) (ω : Ω) (a : A)
    (hh : historyScore p h = prefixLikelihood p X (fun b => actionCount b h) ω) :
    historyScore p ((a,X a (actionCount a h) ω) :: h) =
      prefixLikelihood p X
        (fun b => actionCount b ((a,X a (actionCount a h) ω) :: h)) ω := by
  rw [historyScore_cons,hh,actionCount_fresh_eq_update (fun b i => X b i ω),
    prefixLikelihood_update]

/-- Replay preserves the exact acquired-history / stack-prefix likelihood bridge. -/
theorem historyScore_feed (p : A → Y → ℝ) (X : A → ℕ → Ω → Y)
    (h : History A Y) (ω : Ω) (as : List A)
    (hh : historyScore p h = prefixLikelihood p X (fun b => actionCount b h) ω) :
    historyScore p (feed (fun b i => X b i ω) h as) =
      prefixLikelihood p X
        (fun b => actionCount b (feed (fun b i => X b i ω) h as)) ω := by
  induction as generalizing h with
  | nil => exact hh
  | cons a as ih =>
    apply ih ((a,X a (actionCount a h) ω)::h)
    exact historyScore_fresh p X h ω a hh

/-- Every finite history generated from the empty history has exactly the usual
per-action stack-prefix likelihood. -/
theorem historyScore_feed_nil (p : A → Y → ℝ) (X : A → ℕ → Ω → Y)
    (ω : Ω) (as : List A) :
    historyScore p (feed (fun b i => X b i ω) [] as) =
      prefixLikelihood p X
        (fun b => actionCount b (feed (fun b i => X b i ω) [] as)) ω := by
  apply historyScore_feed
  simp [prefixLikelihood]

/-- The same bridge with the action counts read directly from the execution list. -/
theorem historyScore_feed_nil_counts (p : A → Y → ℝ) (X : A → ℕ → Ω → Y)
    (ω : Ω) (as : List A) :
    historyScore p (feed (fun b i => X b i ω) [] as) =
      prefixLikelihood p X (fun b => as.count b) ω := by
  simpa only [feed_count, actionCount_nil, Nat.zero_add] using
    historyScore_feed_nil p X ω as

end Likelihood
end Orthemology.Tranche2.MicroPolicy
