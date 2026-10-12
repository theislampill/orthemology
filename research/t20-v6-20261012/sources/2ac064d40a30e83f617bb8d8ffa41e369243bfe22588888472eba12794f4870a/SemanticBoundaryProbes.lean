import GlobalControllerControls

noncomputable section
open MeasureTheory Filter
open Orthemology.Tranche2.PolicyEmbedding
namespace IndependentGlobalParityChallenge
open HiddenParity HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Necessity HiddenParity.Stage HiddenParity.Sufficiency
set_option maxRecDepth 100000
set_option maxHeartbeats 12000000

-- Nonemptiness is an explicit semantic boundary, rather than a vacuous ∀ model.
theorem empty_support_not_semantic {R : Type*} [MeasurableSpace R]
    (P : RationalKernel (Fin 2) ((Fin 2) × (Fin 2)) (Fin 2))
    (menu : Finset (Fin 2) → Fin 2 → Finset (Fin 2))
    (priority : Fin 2 → (Fin 2 × Fin 2) → ℕ) :
    ¬ SemanticWinning (R := R) P menu priority (0,0) ∅ 0 := by
  rintro ⟨w⟩
  exact Finset.not_nonempty_empty w.nonempty

-- The iff is specifically Unit-seed. It must not be silently strengthened to
-- an iff for every fixed seed space, because an empty seed space has no probability law.
theorem empty_seed_not_semantic
    (P : RationalKernel (Fin 2) ((Fin 2) × (Fin 2)) (Fin 2))
    (menu : Finset (Fin 2) → Fin 2 → Finset (Fin 2))
    (priority : Fin 2 → (Fin 2 × Fin 2) → ℕ) (B : Finset (Fin 2)) (s : Fin 2) :
    ¬ SemanticWinning (R := Fin 0) P menu priority (0,0) B s := by
  rintro ⟨w⟩
  letI := w.probability
  have hU : (Set.univ : Set (Fin 0)) = ∅ := by ext x; exact Fin.elim0 x
  have hz : w.seedLaw Set.univ = 0 := by rw [hU]; simp
  simp only [measure_univ, one_ne_zero] at hz

-- An empty hard menu rejects even a trivially even objective.
def emptyMenu (_ : Finset (Fin 2)) (_ : Fin 2) : Finset (Fin 2) := ∅
theorem empty_menu_computed_loses :
    winningRegion ControllerControls.coinKernel emptyMenu (fun _ _ => 2) Finset.univ = ∅ := by decide

theorem empty_menu_arbitrary_seed_loses {R : Type*} [MeasurableSpace R] :
    ¬ SemanticWinning (R := R) ControllerControls.coinKernel emptyMenu (fun _ _ => 2) (0,0) Finset.univ 0 := by
  apply computed_losing_excludes_common_policy
  rw [empty_menu_computed_loses]
  exact Finset.not_mem_empty _

-- Support-conditioned menus may change non-monotonically after actual feedback.
def revealingKernel : RationalKernel (Fin 2) (Fin 2 × Fin 2) (Fin 2) where
  row := fun m _ y => if y = m then 1 else 0
  nonnegative := by intros; split <;> norm_num
  normalized := by intro m e; fin_cases m <;> norm_num [Fin.sum_univ_two]

def handoffMenu (B : Finset (Fin 2)) (_ : Fin 2) : Finset (Fin 2) :=
  if B = {1} then {1} else {0}

def oppositePriority (m : Fin 2) (e : Fin 2 × Fin 2) : ℕ := if e.2 = m then 2 else 1

theorem revealing_support_menu_full :
    winningRegion revealingKernel handoffMenu oppositePriority Finset.univ = Finset.univ := by decide

def revealing_support_menu_witness :
    WinningPolicy (R := Unit) revealingKernel handoffMenu oppositePriority (0,0) Finset.univ 0 :=
  computedRegionWinningPolicy revealingKernel handoffMenu oppositePriority Finset.univ (by decide) 0
    (by rw [revealing_support_menu_full]; exact Finset.mem_univ _) (0,0)

-- Deleting every hard-menu action only after a proper support change defeats
-- the all-even objective at the parent as well.
def blockedChildMenu (B : Finset (Fin 2)) (_ : Fin 2) : Finset (Fin 2) :=
  if B = Finset.univ then Finset.univ else ∅

theorem blocked_child_menu_loses :
    winningRegion revealingKernel blockedChildMenu (fun _ _ => 2) Finset.univ = ∅ := by decide

-- A wrong global candidate is allowed when its retained rows coincide with the
-- true model. Requiring whole-model identification would be an unjustified strengthening.
def outsideDifferenceKernel : RationalKernel (Fin 2) (Fin 2 × Fin 2) (Fin 2) where
  row := fun m e y => if y = (if e.1 = 0 then 0 else m) then 1 else 0
  nonnegative := by intros; split <;> split <;> norm_num
  normalized := by intro m e; rcases e with ⟨s,a⟩; fin_cases s <;> fin_cases m <;> norm_num [Fin.sum_univ_two]

def retainedAtZero : Finset (Fin 2 × Fin 2) := {(0,0),(0,1)}
def higherOddPriority (_ : Fin 2) (e : Fin 2 × Fin 2) : ℕ := if e.2 = 0 then 2 else 3

theorem models_differ_globally : outsideDifferenceKernel.row 0 ≠ outsideDifferenceKernel.row 1 := by decide

theorem models_match_retained : Match outsideDifferenceKernel.row 0 1 retainedAtZero := by decide

theorem wrong_global_candidate_component_qualifies :
    MarkovQualifying outsideDifferenceKernel Prod.fst Finset.univ higherOddPriority 0 Finset.univ retainedAtZero := by
  unfold MarkovQualifying
  refine ⟨by decide, by decide, by decide, ?_⟩
  intro σ _ _
  refine ⟨2, ?_, by decide⟩
  change IsMinimum (fun e : Fin 2 × Fin 2 => if e.2 = 0 then 2 else 3) retainedAtZero 2
  decide

theorem higher_odd_pair_is_retained : (0,1) ∈ retainedAtZero ∧ higherOddPriority 1 (0,1) = 3 := by decide

-- The dummy pair is only a total readout fallback; it cannot change Unit-seed
-- semantic existence at an actual generated history law.
theorem readout_fallback_irrelevant
    (P : RationalKernel (Fin 2) (Fin 2 × Fin 2) (Fin 2))
    (menu : Finset (Fin 2) → Fin 2 → Finset (Fin 2))
    (priority : Fin 2 → (Fin 2 × Fin 2) → ℕ) (B : Finset (Fin 2)) (s : Fin 2)
    (d d' : Fin 2 × Fin 2) :
    SemanticWinning (R := Unit) P menu priority d B s ↔ SemanticWinning (R := Unit) P menu priority d' B s :=
  (computed_region_iff_common_parity_policy P menu priority B s d).symm.trans
    (computed_region_iff_common_parity_policy P menu priority B s d')

-- A policy may violate the menu at an impossible action history. Its actual
-- compatible histories still satisfy the exact lawfulness contract.
def copyLast (_ : Unit) : History (Fin 2) (Fin 1) → Fin 2
  | [] => 0
  | (a,_)::_ => a

def singletonKernel : RationalKernel (Fin 1) (Fin 1 × Fin 2) (Fin 1) where
  row := fun _ _ _ => 1
  nonnegative := by intros; norm_num
  normalized := by intros; simp

def onlyZero (_ : Finset (Fin 1)) (_ : Fin 1) : Finset (Fin 2) := {0}

theorem copyLast_compatible_zero (h : History (Fin 1 × Fin 2) (Fin 1))
    (hc : ActionCompatible (pairPolicy 0 copyLast) () h) :
    (pairPolicy 0 copyLast () h).2 = 0 := by
  induction h with
  | nil => rfl
  | cons ey h ih =>
    have ht := ih hc.1
    have ha := congrArg Prod.snd hc.2
    change (pairPolicy 0 copyLast () ((ey.1,ey.2)::h)).2 = 0
    change ey.1.2 = 0
    exact ha.symm.trans ht

theorem offpolicy_violation : copyLast () [(1,0)] ∉ onlyZero Finset.univ 0 := by decide

theorem offpolicy_still_lawful : Lawful singletonKernel onlyZero Finset.univ 0 copyLast (Measure.dirac ()) := by
  intro h _
  apply ae_of_all
  intro r hc
  cases r
  simp only [onlyZero,Finset.mem_singleton]
  exact copyLast_compatible_zero h hc

#check empty_support_not_semantic
#print axioms empty_support_not_semantic
#check empty_seed_not_semantic
#print axioms empty_seed_not_semantic
#check emptyMenu
#print axioms emptyMenu
#check empty_menu_computed_loses
#print axioms empty_menu_computed_loses
#check empty_menu_arbitrary_seed_loses
#print axioms empty_menu_arbitrary_seed_loses
#check revealingKernel
#print axioms revealingKernel
#check handoffMenu
#print axioms handoffMenu
#check oppositePriority
#print axioms oppositePriority
#check revealing_support_menu_full
#print axioms revealing_support_menu_full
#check revealing_support_menu_witness
#print axioms revealing_support_menu_witness
#check blockedChildMenu
#print axioms blockedChildMenu
#check blocked_child_menu_loses
#print axioms blocked_child_menu_loses
#check outsideDifferenceKernel
#print axioms outsideDifferenceKernel
#check retainedAtZero
#print axioms retainedAtZero
#check higherOddPriority
#print axioms higherOddPriority
#check models_differ_globally
#print axioms models_differ_globally
#check models_match_retained
#print axioms models_match_retained
#check wrong_global_candidate_component_qualifies
#print axioms wrong_global_candidate_component_qualifies
#check higher_odd_pair_is_retained
#print axioms higher_odd_pair_is_retained
#check readout_fallback_irrelevant
#print axioms readout_fallback_irrelevant
#check copyLast
#print axioms copyLast
#check singletonKernel
#print axioms singletonKernel
#check onlyZero
#print axioms onlyZero
#check copyLast_compatible_zero
#print axioms copyLast_compatible_zero
#check offpolicy_violation
#print axioms offpolicy_violation
#check offpolicy_still_lawful
#print axioms offpolicy_still_lawful
end IndependentGlobalParityChallenge
