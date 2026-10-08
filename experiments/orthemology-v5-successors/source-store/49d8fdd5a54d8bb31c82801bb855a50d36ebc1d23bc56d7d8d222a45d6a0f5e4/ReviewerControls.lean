import PrefixTransportControls
import ContaminationControls
import HiddenChangeFixedIndex

noncomputable section
open HiddenChange MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding HiddenParity.Stochastic HiddenParity.ResidualSeed
open HiddenParity.ResidualSeed.Continuation OrthemicCertificate.Direct
open HiddenChangeLawTests HiddenChangeContaminationControls

namespace HiddenChangeIndependentReview
-- These are coherent finite histories. No probability-one statement follows
-- from their being one selected infinite support path.
def coherent : ℕ → PairHistory 2 1
  | 0 => []
  | t+1 => List.replicate t ((1,0),1) ++ latePrefix

theorem coherent_step (t : ℕ) :
    coherent (t+1) = (pairPolicy 0 solePolicy () (coherent t),1)::coherent t := by
  cases t with
  | zero => rfl
  | succ t =>
    cases t <;> simp [coherent, List.replicate_succ, latePrefix,
      pairPolicy, currentState, erasePairSources, solePolicy]

theorem coherent_compatible (t : ℕ) :
    ActionCompatible (pairPolicy 0 solePolicy) () (coherent t) := by
  induction t with
  | zero => trivial
  | succ t ih => rw [coherent_step]; exact ⟨ih,rfl⟩

theorem coherent_length (t : ℕ) : (coherent t).length = t := by
  cases t <;> simp [coherent, latePrefix]

theorem coherent_stale_count (t : ℕ) : actionCount (0,0) (coherent (t+1)) = 1 := by
  simp [coherent, HiddenChange.actionCount_append, actionCount, latePrefix]

theorem coherent_stale_symbol (t : ℕ) : symbolCount (0,0) 1 (coherent (t+1)) = 1 := by
  induction t with
  | zero => decide +kernel
  | succ t ih => simpa [coherent, List.replicate_succ, symbolCount] using ih

theorem coherent_gate_free (t : ℕ) : gateFreeReject lateFixture 1 1 (coherent (t+1)) = true := by
  unfold gateFreeReject
  apply decide_eq_true
  refine ⟨(0,0),1,?_⟩
  rw [rationalFrequency, coherent_stale_count, coherent_stale_symbol]
  norm_num [lateFixture, OrthemicCertificate.Input.row]

-- Universal phase obstruction is arithmetic; it is not controller parity.
theorem coherent_no_phase_barrier :
    ¬ ∃ K : ℕ, ∀ r, K ≤ r → ∀ t,
      gateFreeReject lateFixture 1 1 (coherent (t+1)) = false := by
  rintro ⟨K,h⟩
  have hbad := h K le_rfl 0
  rw [coherent_gate_free] at hbad
  contradiction

-- Literal initial and tail transition rows are deterministic and supported.
example : lateFixture.row 0 (0,0) 1 = 1 := by decide +kernel
example : lateFixture.row 1 (1,0) 1 = 1 := by decide +kernel
example : lateFixture.row 1 (0,0) 1 = 0 := by decide +kernel

-- Zero-prefix conditioning is zero, and cannot be treated as a probability restart.
example : fixedConditionalLaw lateFixture lateFixture_valid (some 0) 0
    (Measure.dirac ()) solePolicy latePrefix = 0 := by
  apply fixedConditionalLaw_eq_zero
  rw [fixed_prefix_probability _ _ _ _ _ _ (measurable_of_countable _)]
  norm_num [CompatibleSeeds, ActionCompatible, pairPolicy, currentState, erasePairSources,
    solePolicy, latePrefix, fixedPrefixLikelihood, fixedMode, lateFixture,
    OrthemicCertificate.Input.row, Fin.prod_univ_succ]

-- Schedule indexing must not drop the old policy memory.
def remembersFirst : Policy Unit 1 2 := fun _ h => if h.isEmpty then 0 else 1
example : remembersFirst () [] = 0 := by decide +kernel
example : restartPolicy remembersFirst [(0,0)] () [] = 1 := by decide +kernel

#print axioms coherent_no_phase_barrier
end HiddenChangeIndependentReview
