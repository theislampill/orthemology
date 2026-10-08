import HiddenChangeContamination
open HiddenChange HiddenParity.Empirical HiddenParity.Sufficiency
open Orthemology.Tranche2.PolicyEmbedding
open OrthemicCertificate.Direct
open Filter
open scoped Topology

namespace HiddenChangeContaminationControls

def model : HiddenChange.Input 2 1 where
  rows := #[1,0,0,1,0,1,0,1]
  priorities := #[0,0,0,0]
  menus := [⟨[0,1],0,[0]⟩,⟨[0,1],1,[0]⟩]
  interpretation := ⟨["zero","one"],["s","t"],["a"],"v1","state","exact","common"⟩

theorem model_valid : model.Valid := (OrthemicCertificate.Input.inputCheck_iff model).mp (by decide +kernel)

def stale : PairHistory 2 1 := [((0,0),0)]

-- The actual rational test implements the same strict count gate and inclusive discrepancy.
example : rationalReject model 1 1 0 [] = false := by decide +kernel
example : rationalReject model 1 1 1 stale = false := by decide +kernel
example : rationalReject model 1 1 0 stale = true := by decide +kernel
example : rationalFrequency (0,0) 0 stale - model.row 1 (0,0) 0 = 1 := by decide +kernel
example : rationalReject model 1 1 2 [((0,0),0),((0,0),0)] = false := by decide +kernel
example : rationalReject model 1 1 1 [((0,0),0),((0,0),0)] = true := by decide +kernel

example : empiricalReject (model.kernel model_valid) 1 1 1 stale = false := by
  have h : rationalReject model 1 1 1 stale = false := by decide +kernel
  simpa only [rationalReject_eq_empiricalReject model model_valid, Rat.cast_one] using h
example : empiricalReject (model.kernel model_valid) 1 1 0 stale = true := by
  have h : rationalReject model 1 1 0 stale = true := by decide +kernel
  simpa only [rationalReject_eq_empiricalReject model model_valid, Rat.cast_one] using h

-- Source-derived gate-free mutant: the same exact row comparison with the
-- strict count conjunct deleted. Its stale-data guarantee is mathematically false.
def gateFreeReject (I : HiddenChange.Input 2 1) (δ : ℚ) (σ : Mode)
    (h : PairHistory 2 1) : Bool :=
  decide (∃ e : Pair 2 1, ∃ y : State 2, δ ≤ |rationalFrequency e y h - I.row σ e y|)

example : gateFreeReject model 1 1 stale = true := by decide +kernel
example : ¬ gateFreeReject model 1 1 stale = false := by decide +kernel

-- One old wrong sample is never revisited, while fresh accurate receipts
-- from another pair make the physical history arbitrarily long.
def staleForever (t : ℕ) : PairHistory 2 1 := List.replicate t ((1,0),1) ++ stale

theorem staleForever_count (t : ℕ) : actionCount (0,0) (staleForever t) = 1 := by
  simp [staleForever, HiddenChange.actionCount_append, actionCount, stale]

theorem staleForever_symbolCount (t : ℕ) : symbolCount (0,0) 0 (staleForever t) = 1 := by
  induction t with
  | zero => decide +kernel
  | succ t ih => simpa [staleForever, List.replicate_succ, symbolCount] using ih

theorem staleForever_mutant_rejects (t : ℕ) : gateFreeReject model 1 1 (staleForever t) = true := by
  unfold gateFreeReject
  apply decide_eq_true
  refine ⟨(0,0),0,?_⟩
  rw [rationalFrequency, staleForever_count, staleForever_symbolCount]
  norm_num [model, OrthemicCertificate.Input.row]

theorem gate_free_has_no_phase_barrier :
    ¬ ∃ K : ℕ, ∀ r, K ≤ r → ∀ t, gateFreeReject model 1 1 (staleForever t) = false := by
  rintro ⟨K,hK⟩
  have h := hK K le_rfl 0
  rw [staleForever_mutant_rejects] at h
  contradiction

example (pre : PairHistory 2 1) (H : ℕ → PairHistory 2 1) (p : ℝ)
    (hc : Tendsto (fun t => actionCount (0,0) (H t)) atTop atTop)
    (hf : Tendsto (fun t => historyFrequency (0,0) 1 (H t)) atTop (𝓝 p)) :
    Tendsto (fun t => historyFrequency (0,0) 1 (H t ++ pre)) atTop (𝓝 p) :=
  historyFrequency_tendsto_append _ _ pre H p hc hf

#check HiddenChange.fixed_law_rational_true_gate
#print axioms HiddenChange.fixed_law_rational_true_gate
#check HiddenChange.fixed_law_true_gate
#check HiddenChange.fixed_law_frequencies_tendsto
#check HiddenChange.fixed_law_wrong_row_eventually_rejected
#check HiddenChange.fixed_law_positive_successors_recur
#check HiddenChange.fixed_law_recurrent_counts
#check HiddenChange.fixed_law_rational_wrong_row_eventually_rejected
#print axioms HiddenChange.fixed_law_positive_successors_recur
#print axioms HiddenChange.fixed_law_rational_wrong_row_eventually_rejected
#print axioms HiddenChange.historyFrequency_tendsto_append
#print axioms HiddenChange.uniform_true_gate_of_pairwise_limits
#print axioms HiddenChange.fixed_law_true_gate
#print axioms HiddenChange.fixed_law_frequencies_tendsto
#print axioms HiddenChange.fixed_law_wrong_row_eventually_rejected
end HiddenChangeContaminationControls
