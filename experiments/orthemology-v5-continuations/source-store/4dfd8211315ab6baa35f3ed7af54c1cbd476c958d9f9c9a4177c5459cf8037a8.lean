import ConditionalContinuationLaw
import FiniteChainLaw

noncomputable section
open MeasureTheory
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost.HistoryPMF
attribute [local instance] Classical.propDecidable
open HiddenParity.ResidualSeed HiddenParity.ResidualSeed.Continuation
universe u
variable {A Y : Type u} [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]
variable (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y=1)

/-- The literal row's normalized one-receipt distribution. -/
def symbolPMF (a : A) : PMF Y :=
  PMF.ofFintype (fun y => ENNReal.ofReal (P a y)) (by
    rw [← ENNReal.ofReal_sum_of_nonneg (fun y _ => hP a y),hN a]
    simp)

@[simp] theorem symbolPMF_apply (a : A) (y : Y) : symbolPMF P hP hN a y=ENNReal.ofReal (P a y) :=
  PMF.ofFintype_apply _ _

variable (π : History A Y → A)

def step (h : History A Y) : PMF (History A Y) :=
  (symbolPMF P hP hN (π h)).map (fun y => (π h,y)::h)

def historyPMF : ℕ → PMF (History A Y)
  | 0 => PMF.pure []
  | n+1 => (historyPMF n).bind (step P hP hN π)

theorem step_nil (h : History A Y) : step P hP hN π h []=0 := by
  simp [step,PMF.map_apply]

theorem step_cons (h h' : History A Y) (a : A) (y : Y) :
    step P hP hN π h' ((a,y)::h)=
      if h=h' ∧ a=π h' then ENNReal.ofReal (P a y) else 0 := by
  classical
  by_cases hh : h=h'
  · subst h'
    by_cases ha : a=π h
    · subst a
      simp [step,PMF.map_apply,Prod.mk.injEq,List.cons.injEq,tsum_fintype,Finset.sum_ite_eq]
    · simp [step,PMF.map_apply,Prod.mk.injEq,List.cons.injEq,ha]
  · simp [step,PMF.map_apply,Prod.mk.injEq,List.cons.injEq,hh]

theorem historyPMF_succ_nil (n : ℕ) : historyPMF P hP hN π (n+1) []=0 := by
  simp only [historyPMF,PMF.bind_apply,step_nil,mul_zero,tsum_zero]

theorem historyPMF_succ_cons (n : ℕ) (a : A) (y : Y) (h : History A Y) :
    historyPMF P hP hN π (n+1) ((a,y)::h)=
      if a=π h then historyPMF P hP hN π n h * ENNReal.ofReal (P a y) else 0 := by
  classical
  rw [historyPMF,PMF.bind_apply]
  have hs : (∑' h', historyPMF P hP hN π n h' * step P hP hN π h' ((a,y)::h)) =
      historyPMF P hP hN π n h * step P hP hN π h ((a,y)::h) := by
    apply tsum_eq_single h
    intro h' hne
    rw [step_cons]
    simp [Ne.symm hne]
  rw [hs,step_cons]
  by_cases ha : a=π h <;> simp [ha]

/-- Exact finite-history mass, not a Markov or conditional-law hypothesis. -/
theorem historyPMF_mass (n : ℕ) (h : History A Y) :
    historyPMF P hP hN π n h = if n=h.length then
      (if ActionCompatible (fun (_ : Unit) h => π h) () h then 1 else 0) * RowLikelihood P h else 0 := by
  classical
  induction n generalizing h with
  | zero => cases h <;> simp [historyPMF,PMF.pure_apply,ActionCompatible,RowLikelihood]
  | succ n ih =>
      cases h with
      | nil => simp [historyPMF_succ_nil]
      | cons ay h =>
          rcases ay with ⟨a,y⟩
          rw [historyPMF_succ_cons,ih,rowLikelihood_cons]
          by_cases hl : n=h.length <;>
            by_cases hc : ActionCompatible (fun (_ : Unit) h => π h) () h <;>
            by_cases ha : a=π h <;>
            simp [hl,hc,ha,Ne.symm,ActionCompatible,mul_comm]

/-- The finite PMF is the actual canonical observed-history marginal for the
same deterministic history policy and original normalized rows. The proof uses
the accepted full-history cylinder factorization and Unit Dirac seed. -/
theorem actual_history_marginal_eq_pmf (n : ℕ) :
    (observedTraceLaw ∅ (fun (_ : Unit) h => π h) (Measure.dirac ()) P P hP hN hP hN).map
      (fun H => H n) = (historyPMF P hP hN π n).toMeasure := by
  classical
  let πu : Unit → History A Y → A := fun _ h => π h
  have hπ : Measurable (fun z : Unit × History A Y => πu z.1 z.2) := measurable_of_countable _
  apply Measure.ext_of_singleton
  intro h
  rw [PMF.toMeasure_apply_singleton _ h (measurableSet_singleton h)]
  unfold observedTraceLaw
  rw [Measure.map_map (measurable_pi_apply n) (historyTrajectory_measurable ∅ πu hπ)]
  have hm := history_marginal_formula ∅ πu hπ (Measure.dirac ()) P P hP hN hP hN
    (by intro a ha; exact (Finset.not_mem_empty a ha).elim) n h
  rw [historyPMF_mass]
  have hs : MeasurableSet {r : Unit | ActionCompatible πu r h} := (Set.toFinite _).measurableSet
  simpa only [πu,Measure.dirac_apply' _ hs,Set.mem_setOf_eq,RowLikelihood] using hm

end HiddenParity.Cost.HistoryPMF
