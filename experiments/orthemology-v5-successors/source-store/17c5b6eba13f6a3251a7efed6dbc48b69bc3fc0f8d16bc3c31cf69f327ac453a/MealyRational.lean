import MealyHitting
import Mathlib.LinearAlgebra.FiniteDimensional.Basic

namespace Orthemology.Frontier.MealyMeasure
open Set MeasureTheory Filter
open scoped ENNReal Topology BigOperators
open P02A2.Q8Measure

variable {S : Type*}

/-- Split actual finite input words at their first bit. -/
theorem card_hittingBlocks_succ [Fintype S] (M : Mealy S) (s : S) (n : ℕ) :
    (hittingBlocks M s (n+1)).card =
      (hittingBlocks M (M.next s false) n).card + (hittingBlocks M (M.next s true) n).card := by
  classical
  simp only [hittingBlocks, Finset.card_filter]
  have he := Fintype.sum_equiv (Fin.consEquiv (fun _ : Fin (n+1) => Bool))
    (fun p : Bool × (Fin n → Bool) => if deterministicBit M
      (M.finalState (M.next s p.1) (List.ofFn p.2)) = true then 1 else 0)
    (fun w : Fin (n+1) → Bool => if deterministicBit M
      (M.finalState s (List.ofFn w)) = true then 1 else 0)
    (by intro p; simp [Fin.consEquiv, List.ofFn_succ, Mealy.finalState])
  rw [← he, Fintype.sum_prod_type]
  simp [Fintype.sum_bool, add_comm]

theorem hittingProbabilityQ_succ [Fintype S] (M : Mealy S) (s : S) (n : ℕ) :
    hittingProbabilityQ M s (n+1) =
      (hittingProbabilityQ M (M.next s false) n + hittingProbabilityQ M (M.next s true) n) / 2 := by
  simp only [hittingProbabilityQ, card_hittingBlocks_succ, Nat.cast_add, pow_succ]
  ring

noncomputable def hittingReal (M : Mealy S) (s : S) : ℝ := (fairCantor (hits M s)).toReal

theorem hittingProbabilityQ_tendsto [Fintype S] [Nonempty S] (M : Mealy S) (s : S) :
    Tendsto (fun n => (hittingProbabilityQ M s n : ℝ)) atTop (𝓝 (hittingReal M s)) := by
  have h := tendsto_measure_iUnion_atTop (μ := fairCantor) (hitAt_mono M s)
  rw [← hits_eq_iUnion_hitAt] at h
  have hr := (ENNReal.tendsto_toReal (measure_ne_top fairCantor _)).comp h
  simpa only [Function.comp_def, ← hittingProbabilityQ_correct, hittingReal] using hr

/-- The actual infinite-product hitting probability satisfies the fair one-step equations. -/
theorem hittingReal_harmonic [Fintype S] [Nonempty S] (M : Mealy S) (s : S) :
    hittingReal M s = (hittingReal M (M.next s false) + hittingReal M (M.next s true)) / 2 := by
  have hl := (hittingProbabilityQ_tendsto M s).comp (tendsto_add_atTop_nat 1)
  have hr := ((hittingProbabilityQ_tendsto M (M.next s false)).add
    (hittingProbabilityQ_tendsto M (M.next s true))).div_const 2
  apply tendsto_nhds_unique hl
  simpa only [Function.comp_def, hittingProbabilityQ_succ, Rat.cast_div, Rat.cast_add,
    Rat.cast_ofNat] using hr

/-- Finite-word reachability of the deterministic-output domain, including the empty word. -/
def Reaches (M : Mealy S) (s : S) : Prop :=
  ∃ u : List Bool, M.infiniteRel (M.finalState s u) (M.finalState s u)

theorem deterministic_reaches (M : Mealy S) (s : S) (hs : M.infiniteRel s s) : Reaches M s :=
  ⟨[], hs⟩

theorem hittingReal_eq_one [Finite S] (M : Mealy S) (s : S) (hs : M.infiniteRel s s) :
    hittingReal M s = 1 := by
  have he : hits M s = univ := by
    ext x
    simp only [hits, mem_setOf_eq, mem_univ, iff_true]
    exact ⟨0, hs⟩
  simp [hittingReal, he]

theorem hittingReal_eq_zero [Finite S] [Nonempty S] (M : Mealy S) (s : S)
    (hs : ¬ Reaches M s) : hittingReal M s = 0 := by
  have h := (atomic_mass_zero_iff_unreachable M s).mpr (by simpa [Reaches] using hs)
  rw [atomic_mass_eq_hitting_probability] at h
  simp [hittingReal, h]


noncomputable section MaximumPrinciple
local instance (p : Prop) : Decidable p := Classical.propDecidable p
variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

/-- Finite maximum principle with D and all non-reaching components pinned to zero.
    No claim that every non-D state is transient is used. -/
theorem homogeneous_nonpos [Fintype S] [Nonempty S] (M : Mealy S) (f : S → K)
    (hD : ∀ q, M.infiniteRel q q → f q = 0)
    (hR : ∀ q, ¬ Reaches M q → f q = 0)
    (hh : ∀ q, ¬ M.infiniteRel q q → Reaches M q →
      2 * f q = f (M.next q false) + f (M.next q true)) : ∀ q, f q ≤ 0 := by
  obtain ⟨q, hq, hmax⟩ := Finset.exists_max_image (Finset.univ : Finset S) f Finset.univ_nonempty
  have hmax' : ∀ r, f r ≤ f q := fun r => hmax r (Finset.mem_univ _)
  by_contra hn
  push_neg at hn
  obtain ⟨r, hr⟩ := hn
  have hp : 0 < f q := hr.trans_le (hmax' r)
  have hreach : Reaches M q := by
    by_contra hn
    rw [hR q hn] at hp
    exact lt_irrefl _ hp
  obtain ⟨u, hu⟩ := hreach
  have hprop : ∀ (u : List Bool) (q : S), (∀ r, f r ≤ f q) → 0 < f q →
      f (M.finalState q u) = f q := by
    intro u
    induction u with
    | nil => intros; rfl
    | cons b u ih =>
      intro q hmax hp
      have hnD : ¬ M.infiniteRel q q := by
        intro h
        rw [hD q h] at hp
        exact lt_irrefl _ hp
      have hnR : Reaches M q := by
        by_contra h
        rw [hR q h] at hp
        exact lt_irrefl _ hp
      have he := hh q hnD hnR
      have hb : f (M.next q b) = f q := by
        have h0 := hmax (M.next q false)
        have h1 := hmax (M.next q true)
        cases b <;> linarith
      change f (M.finalState (M.next q b) u) = f q
      rw [ih (M.next q b) (by simpa only [hb] using hmax) (by simpa only [hb] using hp), hb]
  have he := hprop u q hmax' hp
  rw [hD _ hu] at he
  exact (ne_of_gt hp) he.symm

/-- Uniqueness for the homogeneous reachability equations, valid over ℚ and ℝ. -/
theorem homogeneous_eq_zero [Fintype S] [Nonempty S] (M : Mealy S) (f : S → K)
    (hD : ∀ q, M.infiniteRel q q → f q = 0)
    (hR : ∀ q, ¬ Reaches M q → f q = 0)
    (hh : ∀ q, ¬ M.infiniteRel q q → Reaches M q →
      2 * f q = f (M.next q false) + f (M.next q true)) : f = 0 := by
  have hle := homogeneous_nonpos M f hD hR hh
  have hge := homogeneous_nonpos M (fun q => -f q)
    (fun q h => by simp [hD q h]) (fun q h => by simp [hR q h])
    (by intro q hd hr; have h := hh q hd hr; dsimp; linarith)
  funext q
  have hl := hle q
  have hg := hge q
  dsimp at hg ⊢
  linarith

/-- The finite linear system uses boundary equations on D and on non-reaching components,
    and the literal fair-transition harmonic equation on the remaining states. -/
noncomputable def hittingSystem (M : Mealy S) : (S → K) →ₗ[K] (S → K) := by
  classical
  exact
    { toFun := fun f q => if M.infiniteRel q q ∨ ¬ Reaches M q then f q
        else 2*f q - f (M.next q false) - f (M.next q true)
      map_add' := by
        intro f g
        funext q
        dsimp
        split_ifs <;> ring
      map_smul' := by
        intro a f
        funext q
        simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
        split_ifs <;> ring }

omit [LinearOrder K] [IsStrictOrderedRing K] in
theorem hittingSystem_apply (M : Mealy S) (f : S → K) (q : S) :
    hittingSystem M f q = if M.infiniteRel q q ∨ ¬ Reaches M q then f q
      else 2*f q - f (M.next q false) - f (M.next q true) := rfl

/-- Injectivity is derived from finite path reachability and the maximum principle. -/
theorem hittingSystem_injective [Fintype S] [Nonempty S] (M : Mealy S) :
    Function.Injective (hittingSystem (K := K) M) := by
  classical
  apply LinearMap.ker_eq_bot.mp
  apply LinearMap.ker_eq_bot'.mpr
  intro f hf
  apply homogeneous_eq_zero M f
  · intro q hq
    have h := congrFun hf q
    simpa [hittingSystem_apply, hq] using h
  · intro q hq
    have h := congrFun hf q
    simpa [hittingSystem_apply, hq] using h
  · intro q hd hr
    have h := congrFun hf q
    simp only [hittingSystem_apply, hd, hr, not_true_eq_false, or_self, ↓reduceIte,
      Pi.zero_apply] at h
    linarith

/-- The finite rational coefficient system has a unique rational solution.
    Existence follows from injective⇒surjective in finite dimension, not an assumed inverse. -/
theorem exists_rational_solution [Fintype S] [Nonempty S] (M : Mealy S) :
    ∃ f : S → ℚ, ∀ q, hittingSystem M f q = if M.infiniteRel q q then 1 else 0 := by
  classical
  obtain ⟨f, hf⟩ := LinearMap.surjective_of_injective (hittingSystem_injective (K := ℚ) M)
    (fun q => if M.infiniteRel q q then 1 else 0)
  exact ⟨f, fun q => congrFun hf q⟩

/-- The actual measured hitting law satisfies the very same finite boundary system. -/
theorem hittingReal_system [Fintype S] [Nonempty S] (M : Mealy S) (q : S) :
    hittingSystem M (hittingReal M) q = if M.infiniteRel q q then 1 else 0 := by
  rw [hittingSystem_apply]
  by_cases hd : M.infiniteRel q q
  · simp [hd, hittingReal_eq_one M q hd]
  · by_cases hr : Reaches M q
    · simp only [hd, hr, not_true_eq_false, or_self, ↓reduceIte]
      have h := hittingReal_harmonic M q
      linarith
    · simp [hd, hr, hittingReal_eq_zero M q hr]

/-- Rationality of the actual infinite-horizon hitting probabilities.
    The graph-to-system and measure-to-system correspondences are both proved. -/
theorem rational_hitting_probability [Fintype S] [Nonempty S] (M : Mealy S) :
    ∃ f : S → ℚ, ∀ q, (f q : ℝ) = hittingReal M q := by
  obtain ⟨f, hf⟩ := exists_rational_solution M
  refine ⟨f, ?_⟩
  have hcast : hittingSystem M (fun q => (f q : ℝ)) = hittingSystem M (hittingReal M) := by
    funext q
    rw [hittingReal_system]
    have hq := hf q
    rw [hittingSystem_apply] at hq ⊢
    by_cases hd : M.infiniteRel q q
    · simp only [hd, true_or, ↓reduceIte] at hq ⊢
      exact_mod_cast hq
    · by_cases hr : Reaches M q
      · simp only [hd, hr, not_true_eq_false, or_self, ↓reduceIte] at hq ⊢
        exact_mod_cast hq
      · simp only [hd, hr, not_false_eq_true, or_true, ↓reduceIte] at hq ⊢
        exact_mod_cast hq
  have he := hittingSystem_injective (K := ℝ) M hcast
  exact fun q => congrFun he q

/-- The total atomic mass of a finite-state output law is an actual rational number. -/
theorem atomic_mass_rational [Fintype S] [Nonempty S] (M : Mealy S) (s : S) :
    ∃ r : ℚ, (r : ℝ) = (P02A2.mass (law M s)).toReal := by
  obtain ⟨f, hf⟩ := rational_hitting_probability M
  refine ⟨f s, ?_⟩
  rw [atomic_mass_eq_hitting_probability]
  exact hf s

/-- Consequently the real-valued nonatomic defect is rational too. -/
theorem defect_rational [Fintype S] [Nonempty S] (M : Mealy S) (s : S) :
    ∃ r : ℚ, (r : ℝ) = P02A2.defect (law M s) := by
  obtain ⟨r, hr⟩ := atomic_mass_rational M s
  refine ⟨1-r, ?_⟩
  simp [P02A2.defect, hr]

end MaximumPrinciple

end Orthemology.Frontier.MealyMeasure
