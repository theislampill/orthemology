import StoppedBlock

noncomputable section
namespace Orthemology.Tranche2
variable {A Y : Type*} [DecidableEq A]

/-- The actual old-phase action prefix, ending exactly at the exit observation. -/
def stoppedActions : (acts : List A) → StopObs Y acts.length → List A
  | [], _ => []
  | a::_, Sum.inl _ => [a]
  | a::as, Sum.inr (_,w) => a :: stoppedActions as w

omit [DecidableEq A] in
theorem stoppedActions_sublist (acts : List A) (w : StopObs Y acts.length) :
    (stoppedActions acts w).Sublist acts := by
  induction acts with
  | nil => exact List.Sublist.refl []
  | cons a as ih =>
    rcases w with y | ⟨y,w⟩
    · exact List.Sublist.cons_cons a (List.nil_sublist _)
    · exact List.Sublist.cons_cons a (ih w)

def plannedBadCount (good : Finset A) (acts : List A) : ℕ :=
  (acts.filter (fun a => a ∉ good)).length

/-- Every actually executed target-bad action is charged, even when an old-menu
block is interrupted. This is the direction not supplied by hcostBad alone. -/
theorem stopped_bad_count_le_planned (good : Finset A) (acts : List A)
    (w : StopObs Y acts.length) :
    plannedBadCount good (stoppedActions acts w) ≤ plannedBadCount good acts := by
  exact ((stoppedActions_sublist acts w).filter (fun a => a ∉ good)).length_le

theorem plannedBadCount_pos_iff (good : Finset A) (acts : List A) :
    0 < plannedBadCount good acts ↔ ¬ acts.toFinset ⊆ good := by
  simp only [plannedBadCount, List.length_filter_pos_iff, decide_eq_true_eq, Finset.subset_iff, List.mem_toFinset]
  push_neg
  rfl

section Live
variable {Θ : Type*} [DecidableEq Θ]

def livePlannedCost (good : Finset A) (live : Finset Θ) (acts : Θ → List A) (σ : Θ) : ℝ :=
  if σ ∈ live then (plannedBadCount good (acts σ) : ℝ) else 0

lemma livePlannedCost_nonneg (good : Finset A) (live : Finset Θ) (acts : Θ → List A) (σ : Θ) :
    0 ≤ livePlannedCost good live acts σ := by
  unfold livePlannedCost
  split_ifs <;> positivity

lemma livePlannedCost_positive (good : Finset A) (live : Finset Θ) (acts : Θ → List A) (σ : Θ)
    (hp : 0 < livePlannedCost good live acts σ) : σ ∈ live ∧ ¬ (acts σ).toFinset ⊆ good := by
  unfold livePlannedCost at hp
  split_ifs at hp with hl
  · refine ⟨hl, (plannedBadCount_pos_iff good (acts σ)).mp ?_⟩
    exact_mod_cast hp
  · exact (lt_irrefl 0 hp).elim

lemma stopped_bad_count_le_live_charge (good : Finset A) (live : Finset Θ) (acts : Θ → List A)
    (σ : Θ) (hσ : σ ∈ live) (w : StopObs Y (acts σ).length) :
    (plannedBadCount good (stoppedActions (acts σ) w) : ℝ) ≤ livePlannedCost good live acts σ := by
  rw [livePlannedCost, if_pos hσ]
  exact_mod_cast stopped_bad_count_le_planned good (acts σ) w

end Live
end Orthemology.Tranche2
