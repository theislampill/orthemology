import RoundRobinControls

noncomputable section
namespace HiddenParity.IndependentTarget
open MeasureTheory Filter
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
open HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Necessity HiddenParity.Sufficiency
open HiddenParity.Sufficiency.Controls
set_option maxRecDepth 100000
set_option maxHeartbeats 4000000

theorem one_state_support_exact :
    supportSuccessors (realRows oneStateKernel 0) = (fun _ => (Finset.univ : Finset S)) := by
  funext e
  ext y
  simp [supportSuccessors, realRows, oneStateKernel]

theorem one_state_actual_component :
    IsEndComponent Prod.fst (supportSuccessors (realRows oneStateKernel 0))
      (Finset.univ : Finset (S × A)) := by
  rw [one_state_support_exact]
  decide

theorem proper_closed_subset_without_fairness :
    IsEndComponent Prod.fst (supportSuccessors (realRows oneStateKernel 0))
      ({(0,0)} : Finset (S × A)) ∧
    ({(0,0)} : Finset (S × A)) ≠ Finset.univ := by
  rw [one_state_support_exact]
  decide

theorem literal_actual_recurrent_equality :
    ∀ᵐ H ∂markovHistoryLaw oneStateKernel 0 (0 : S)
      (roundRobinPolicy (Finset.univ : Finset (S × A)) (0 : A) 0) (Measure.dirac ()),
      recurrentSet (historyAction ((0 : S),(0 : A)) H) = Finset.univ := by
  exact roundRobin_markov_recurrent oneStateKernel 0 Finset.univ 0 0 (by decide)
    (Measure.dirac ()) one_state_actual_component (0,0)

/-- The actually winning cycling policy visits its odd-priority pair infinitely.
Thus an odd-visit budget cannot be inferred from local parity sufficiency. -/
theorem odd_pair_recurrent_on_actual_law :
    ∀ᵐ H ∂markovHistoryLaw oneStateKernel 0 (0 : S)
      (roundRobinPolicy (Finset.univ : Finset (S × A)) (0 : A) 0) (Measure.dirac ()),
      ∃ᶠ n in atTop, historyAction ((0 : S),(0 : A)) H n = ((0 : S),(1 : A)) := by
  filter_upwards [literal_actual_recurrent_equality] with H hH
  apply (mem_recurrentSet _ ((0 : S),(1 : A))).mp
  rw [hH]
  exact Finset.mem_univ _

theorem odd_pair_priority_three : priority (0 : M) ((0 : S),(1 : A)) = 3 := by decide

theorem initial_action_in_retained_menu :
    pairPolicy (0 : S) (roundRobinPolicy (Finset.univ : Finset (S × A)) (0 : A) 0)
      () [] ∈ (Finset.univ : Finset (S × A)) := Finset.mem_univ _

theorem cycling_ignores_private_seed {R : Type*} (E : Finset (S × A)) (r r' : R)
    (h : History A S) : roundRobinPolicy E (0 : A) (0 : S) r h =
      roundRobinPolicy E (0 : A) (0 : S) r' h := rfl

theorem departure_count_not_receipt_count :
    historyVisits (0 : Fin 2) 0 ([(0,1)] : History (Fin 1) (Fin 2)) = 1 ∧
    historyVisits (0 : Fin 2) 1 ([(0,1)] : History (Fin 1) (Fin 2)) = 0 := by decide

/-- Same positive support does not replace numerical full-row matching. -/
def unequalKernel : RationalKernel (Fin 2) ((Fin 2) × (Fin 1)) (Fin 2) where
  row := fun m _ y => if m = y then 1/3 else 2/3
  nonnegative := by intros; split <;> norm_num
  normalized := by intro m e; fin_cases m <;> norm_num [Fin.sum_univ_two]

def unequalPriority (m : Fin 2) (_ : (Fin 2) × (Fin 1)) : Nat := if m=0 then 2 else 1

theorem unequal_full_support (m : Fin 2) (e : (Fin 2) × (Fin 1)) (y : Fin 2) :
    0 < unequalKernel.row m e y := by
  change 0 < (if m=y then (1/3:ℚ) else 2/3)
  split <;> norm_num

theorem unequal_full_rows :
    ¬ Match unequalKernel.row 0 1 (Finset.univ : Finset ((Fin 2) × (Fin 1))) := by
  intro h
  have he := congrFun (h (0,0) (Finset.mem_univ _)) (0 : Fin 2)
  norm_num [unequalKernel] at he

theorem unequal_candidate_qualifies :
    MarkovQualifying unequalKernel Prod.fst Finset.univ unequalPriority 0
      Finset.univ Finset.univ := by
  have hi : internalSuccessors unequalKernel Finset.univ =
      (fun _ => (Finset.univ : Finset (Fin 2))) := by
    funext e
    ext y
    simp [mem_internalSuccessors, unequal_full_support]
  refine ⟨by decide, ?_, ?_, ?_⟩
  · intro e he y hy
    rw [hi]
    exact Finset.mem_univ _
  · rw [hi]
    decide
  intro σ hσ hm
  fin_cases σ
  · exact ⟨2, by decide, by decide⟩
  · exact (unequal_full_rows hm).elim

theorem unequal_rival_never_parity (x : Nat → (Fin 2) × (Fin 1)) :
    ¬ ParitySuccess (unequalPriority 1) x := by
  rintro ⟨k, ⟨⟨e, he, hk⟩, hmin⟩, heven⟩
  have hk1 : k = 1 := by simpa [unequalPriority] using hk.symm
  subst k
  norm_num [unequalPriority] at heven

end HiddenParity.IndependentTarget
