import FiniteHistoryPMF
import FinitePushforwardRows

noncomputable section
open MeasureTheory
open scoped ENNReal BigOperators
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost.HistoryPMF
attribute [local instance] Classical.propDecidable
open FiniteChainHitting
universe u v
variable {A Y : Type u} {Q : Type v}
variable [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]
variable [MeasurableSpace A] [MeasurableSingletonClass A]
variable [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- Memory readout from the exact newest-first history. It does not reset or
replace any past history supplied as the initial memory. -/
def memory (update : Q → Y → Q) (q₀ : Q) : History A Y → Q
  | [] => q₀
  | (_,y)::h => update (memory update q₀ h) y

def iteratePMF (K : Q → PMF Q) : ℕ → Q → PMF Q
  | 0, q => PMF.pure q
  | n+1, q => (iteratePMF K n q).bind K

theorem iteratePMF_succ_left (K : Q → PMF Q) (n : ℕ) (q : Q) :
    iteratePMF K (n+1) q = (K q).bind (iteratePMF K n) := by
  induction n with
  | zero => simp [iteratePMF,PMF.pure_bind,PMF.bind_pure]
  | succ n ih =>
      rw [iteratePMF,ih,PMF.bind_bind]
      rfl

variable (P : A → Y → ℝ) (hP : ∀ a y, 0 ≤ P a y) (hN : ∀ a, ∑ y, P a y=1)
variable (choose : Q → A) (update : Q → Y → Q)

def transition (q : Q) : PMF Q := (symbolPMF P hP hN (choose q)).map (update q)

theorem historyPMF_map_memory (q₀ : Q) (n : ℕ) :
    (historyPMF P hP hN (fun h => choose (memory update q₀ h)) n).map (memory update q₀) =
      iteratePMF (transition P hP hN choose update) n q₀ := by
  induction n with
  | zero => simp [historyPMF,PMF.pure_map,memory,iteratePMF]
  | succ n ih =>
      rw [historyPMF,PMF.map_bind]
      have hstep : ∀ h, (step P hP hN (fun h => choose (memory update q₀ h)) h).map (memory update q₀) =
          transition P hP hN choose update (memory update q₀ h) := by
        intro h
        rw [step,PMF.map_comp]
        rfl
      simp_rw [hstep]
      change (historyPMF P hP hN (fun h => choose (memory update q₀ h)) n).bind
        ((transition P hP hN choose update) ∘ memory update q₀) = _
      rw [← PMF.bind_map,ih]
      rfl

variable [MeasurableSpace Q] [MeasurableSingletonClass Q]

/-- A finite-memory readout of the genuine canonical observed law equals the
finite PMF constructed from its original row/choice/update functions. -/
theorem actual_memory_marginal (q₀ : Q) (n : ℕ) :
    (observedTraceLaw ∅ (fun (_ : Unit) h => choose (memory update q₀ h))
      (Measure.dirac ()) P P hP hN hP hN).map (fun H => memory update q₀ (H n)) =
      (iteratePMF (transition P hP hN choose update) n q₀).toMeasure := by
  have hm : Measurable (memory (A:=A) update q₀) := measurable_of_countable _
  change Measure.map ((memory (A:=A) update q₀) ∘ (fun H : ℕ → History A Y => H n))
    (observedTraceLaw ∅ (fun (_ : Unit) h => choose (memory update q₀ h))
      (Measure.dirac ()) P P hP hN hP hN) = _
  rw [← Measure.map_map hm (measurable_pi_apply n),actual_history_marginal_eq_pmf,
    PMF.toMeasure_map _ _ hm,historyPMF_map_memory]

variable [Fintype Q] [DecidableEq Q]

/-- The transition PMF is exactly the finite pushforward-row PMF, not an
assumed equality between two stochastic experiments. -/
theorem transition_eq_push_rowPMF (q : Q) :
    transition P hP hN choose update q = rowPMF
      (pushRows (fun q y => P (choose q) y) (fun q y => hP (choose q) y)
        (fun q => hN (choose q)) update) q := by
  classical
  apply PMF.ext
  intro q'
  simp only [transition,PMF.map_apply,symbolPMF_apply,tsum_fintype,rowPMF_apply,pushRows]
  rw [ENNReal.ofReal_sum_of_nonneg (by
    intro y _
    split_ifs <;> [exact hP (choose q) y; exact le_rfl])]
  apply Finset.sum_congr rfl
  intro y _
  by_cases he : update q y=q'
  · simp [he]
  · simp [he,Ne.symm he]

/-- An absorbing goal changes no finite-law distribution; this identifies the
right-recursive Markov iterate with the already proved absorbed hitting law. -/
theorem iteratePMF_eq_absorbed (K : Rows Q) (goal : Q → Prop) [DecidablePred goal]
    (habs : ∀ q, goal q → rowPMF K q=PMF.pure q) (n : ℕ) (q : Q) :
    iteratePMF (rowPMF K) n q = absorbedLaw K goal n q := by
  induction n generalizing q with
  | zero => rfl
  | succ n ih =>
      rw [iteratePMF_succ_left]
      rw [show iteratePMF (rowPMF K) n = absorbedLaw K goal n from funext ih]
      by_cases hq : goal q
      · rw [habs q hq,PMF.pure_bind]
        cases n <;> simp [absorbedLaw,hq]
      · exact (if_neg hq).symm

end HiddenParity.Cost.HistoryPMF
