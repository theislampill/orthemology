import PolicyTraceBinding
import ChainPhysicalBudget

noncomputable section
set_option linter.unusedSectionVars false
open MeasureTheory ProbabilityTheory Finset
open scoped BigOperators ENNReal
attribute [local instance] Classical.propDecidable
namespace Orthemology.Tranche3.CanonicalMicro
open Orthemology.Tranche2.PolicyEmbedding
variable {A Y : Type*} [Fintype A] [Fintype Y] [DecidableEq A]

/-- One genuine finite observation PMF at the currently selected action. -/
def actionObsPMF (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y)
    (hN : ∀ a, ∑ y, P a y = 1) (a : A) : PMF Y :=
  PMF.ofFintype (fun y => ENNReal.ofReal (P a y)) (by
    rw [← ENNReal.ofReal_sum_of_nonneg (fun y _ => hP a y), hN, ENNReal.ofReal_one])

def nextHistoryPMF (π : History A Y → A) (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y) : PMF (History A Y) :=
  (actionObsPMF P hP hN (π h)).map (fun y => (π h,y)::h)

/-- A finite micro-step experiment, directly on acquired histories. -/
def historyPMF (π : History A Y → A) (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) : ℕ → PMF (History A Y)
  | 0 => PMF.pure []
  | n+1 => (historyPMF π P hP hN n).bind (nextHistoryPMF π P hP hN)

omit [Fintype A] [DecidableEq A] in
lemma nextHistoryPMF_nil (π : History A Y → A) (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) (h : History A Y) :
    nextHistoryPMF π P hP hN h [] = 0 := by
  simp [nextHistoryPMF,PMF.map_apply]

omit [Fintype A] in
lemma nextHistoryPMF_cons (π : History A Y → A) (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (h k : History A Y) (a : A) (y : Y) :
    nextHistoryPMF π P hP hN k ((a,y)::h) =
      if k = h ∧ π h = a then ENNReal.ofReal (P a y) else 0 := by
  classical
  unfold nextHistoryPMF
  rw [PMF.map_apply]
  by_cases hk : k = h
  · subst k
    by_cases ha : π h = a
    · simp only [ha,List.cons.injEq,Prod.mk.injEq,true_and,and_true]
      rw [tsum_eq_single y]
      · simp [actionObsPMF]
      · intro z hz
        simp [Ne.symm hz]
    · simp [ha,Ne.symm ha]
  · simp [hk,Ne.symm hk]

omit [Fintype A] [DecidableEq A] in
lemma historyPMF_succ_nil (π : History A Y → A) (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1) (n : ℕ) :
    historyPMF π P hP hN (n+1) [] = 0 := by
  simp [historyPMF,PMF.bind_apply,nextHistoryPMF_nil]

omit [Fintype A] in
lemma historyPMF_succ_cons (π : History A Y → A) (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (n : ℕ) (h : History A Y) (a : A) (y : Y) :
    historyPMF π P hP hN (n+1) ((a,y)::h) =
      if π h = a then historyPMF π P hP hN n h * ENNReal.ofReal (P a y) else 0 := by
  classical
  rw [historyPMF,PMF.bind_apply]
  simp_rw [nextHistoryPMF_cons]
  rw [tsum_eq_single h]
  · by_cases ha : π h = a <;> simp [ha]
  · intro k hk
    simp [hk]

omit [Fintype A] in
/-- Exact probability of each acquired transcript, with zeros admitted. -/
theorem historyPMF_apply (π : History A Y → A) (P : A → Y → ℝ)
    (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y = 1)
    (n : ℕ) (h : History A Y) :
    historyPMF π P hP hN n h =
      if n = h.length ∧ ActionCompatible (fun (_ : Unit) h => π h) () h then
        ∏ i : Fin h.length, ENNReal.ofReal (P h[i].1 h[i].2) else 0 := by
  classical
  induction n generalizing h with
  | zero =>
    cases h with
    | nil => simp [historyPMF,ActionCompatible]
    | cons ay h => simp [historyPMF]
  | succ n ih =>
    cases h with
    | nil => simp [historyPMF_succ_nil]
    | cons ay h =>
      rcases ay with ⟨a,y⟩
      rw [historyPMF_succ_cons,ih]
      simp only [List.length_cons,ActionCompatible,Fin.prod_univ_succ,List.getElem_cons_zero,
        List.getElem_cons_succ,Prod.fst,Prod.snd]
      by_cases hn : n = h.length <;> by_cases hc : ActionCompatible (fun (_ : Unit) h => π h) () h <;>
        by_cases ha : π h = a <;> simp [hn,hc,ha,mul_comm]

section Mean
variable {α β : Type*}

def pmfMean (p : PMF α) (f : α → ℝ≥0∞) : ℝ≥0∞ := ∑' a, p a * f a

lemma pmfMean_pure (a : α) (f : α → ℝ≥0∞) : pmfMean (PMF.pure a) f = f a := by
  classical
  unfold pmfMean
  rw [tsum_eq_single a]
  · simp [PMF.pure_apply]
  · intro b hb
    simp [PMF.pure_apply,hb]

lemma pmfMean_bind (p : PMF α) (q : α → PMF β) (f : β → ℝ≥0∞) :
    pmfMean (p.bind q) f = pmfMean p (fun a => pmfMean (q a) f) := by
  simp only [pmfMean,PMF.bind_apply,← ENNReal.tsum_mul_right]
  rw [ENNReal.tsum_comm]
  simp only [mul_assoc,ENNReal.tsum_mul_left]

lemma pmfMean_map (p : PMF α) (g : α → β) (f : β → ℝ≥0∞) :
    pmfMean (p.map g) f = pmfMean p (fun a => f (g a)) := by
  change pmfMean (p.bind fun a => PMF.pure (g a)) f = _
  rw [pmfMean_bind]
  simp_rw [pmfMean_pure]

lemma pmfMean_mono_on_support (p : PMF α) (f g : α → ℝ≥0∞)
    (h : ∀ a, p a ≠ 0 → f a ≤ g a) : pmfMean p f ≤ pmfMean p g := by
  apply ENNReal.tsum_le_tsum
  intro a
  by_cases hp : p a = 0
  · simp [hp]
  · exact mul_le_mul_left' (h a hp) _

lemma pmfMean_add (p : PMF α) (f g : α → ℝ≥0∞) :
    pmfMean p (fun a => f a + g a) = pmfMean p f + pmfMean p g := by
  simp only [pmfMean,mul_add,ENNReal.tsum_add]

lemma pmfMean_const (p : PMF α) (c : ℝ≥0∞) : pmfMean p (fun _ => c) = c := by
  rw [pmfMean,ENNReal.tsum_mul_right,PMF.tsum_coe,one_mul]
end Mean
end Orthemology.Tranche3.CanonicalMicro
