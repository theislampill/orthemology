import FullCommandInterface
import ExactCap
import RepairStateBridge

open Finset MeasureTheory
namespace CoveringIndependent
open CoveringKernel

variable {α Action Obs Ω : Type*} [Fintype α] [DecidableEq α]

-- The optimum is genuinely positive when candidate worlds exist, including k=0.
theorem positive_feasible_cover (b k : ℕ) (hb : b ≤ Fintype.card α) (hk : k ≤ b) :
    0 < coveringNumber α b k := by
  obtain ⟨G, hu, hc, hcard⟩ := coveringNumber_attained b k hb hk
  obtain ⟨T, _, hT⟩ := exists_subset_card_eq
    (show k ≤ (univ : Finset α).card by simpa using hk.trans hb)
  obtain ⟨A, hA, _⟩ := hc T hT
  rw [← hcard]
  exact card_pos.mpr ⟨A, hA⟩

-- Smaller fault sets are handled by extension, not by independent-label worlds.
omit [DecidableEq α] in
theorem maximal_portfolio_handles_smaller (k : ℕ) (hk : k ≤ Fintype.card α)
    (F : Finset (Finset α)) (ha : Available k F)
    (T : Finset α) (hT : T.card ≤ k) : ∃ P ∈ F, Disjoint P T := by
  obtain ⟨U, hTU, _, hUk⟩ := exists_subsuperset_card_eq (subset_univ T) hT
    (show k ≤ (univ : Finset α).card by simpa using hk)
  obtain ⟨P, hP, hd⟩ := ha U hUk
  exact ⟨P, hP, hd.mono_right hTU⟩

-- No effect has occurred at time zero, regardless of command/observation data.
omit [Fintype α] [DecidableEq α] in
theorem no_zero_attempt_hit (support : Action → Finset α)
    (π : Actions.Policy Action Obs)
    (observe : Finset α → List (Action × Obs) → Action → Obs) (T : Finset α) :
    ¬ Actions.SuccessWithin support π observe T 0 := by
  rintro ⟨n, hn, _⟩
  omega

-- Even the empty universe has one empty maximal world and one empty-block cover.
theorem empty_universe_cover : coveringNumber (Fin 0) 0 0 = 1 := by
  simpa using coveringNumber_self (α := Fin 0) 0 (by simp)

-- Infeasible maxima are outside the advertised nonempty-candidate case.
omit [DecidableEq α] in
theorem no_world_if_too_large (k : ℕ) (hk : Fintype.card α < k) :
    ¬ ∃ T : Finset α, T.card = k := by
  rintro ⟨T, hT⟩
  have hb := card_le_univ T
  omega

-- An actual probability (or other nonzero measure) is needed to choose a coin.
theorem zero_measure_makes_every_cap_ae [MeasurableSpace Ω] (P : Ω → Prop) :
    ∀ᵐ ω ∂(0 : Measure Ω), P ω := by simp

-- Convert the exact main fixed-(A,S) conclusion to explicit positive outer measure.
theorem fixed_root_world_positive_outer_measure [MeasurableSpace Ω]
    (F : Finset (Finset α)) (support : Action → Finset α)
    (admitted : ∀ a, support a ∈ F)
    (μ : Measure Ω) [IsProbabilityMeasure μ] (π : Ω → Actions.Policy Action Obs)
    (observe : Finset α → List (Action × Obs) → Action → Obs)
    (failed : List (Action × Obs) → Action → Obs) (B c q N : ℕ)
    (hB : 1 ≤ B) (hc : 1 ≤ c) (hu : Uniform q F)
    (hop : ∀ ω, Actions.Opaque support (π ω) observe failed (B+c-1))
    (hsmall : N < coveringNumber α (Fintype.card α-q) (B+c-1)) :
    ∃ A : Finset α, A.card = c ∧ ∃ S : Finset (Option α),
      S ⊆ AttributionKernel.actualRoots A ∧ S.card = B ∧
      0 < μ {ω | ¬ Actions.SuccessWithin support (π ω) observe
        (AttributionKernel.taintedLabels A S) N} := by
  obtain ⟨A, hA, S, hSr, hS, hfail⟩ :=
    Actions.randomized_below_cover_fixed_root_world F support admitted μ π observe
      failed B c q N hB hc hu hop hsmall
  refine ⟨A, hA, S, hSr, hS, pos_iff_ne_zero.mpr ?_⟩
  simpa only [ae_iff] using hfail

-- A richer history is permissible after a success, while opacity remains exact
-- on every compatible failed prefix. The initial action is fixed, later actions
-- may depend on all preceding observations in the general theorem.
def supportOne (_ : Unit) : Finset (Fin 2) := {0}
def chooseOne : Actions.Policy Unit Bool := fun _ => ()
def falseReply (_ : List (Unit × Bool)) (_ : Unit) : Bool := false
def afterSuccessReply (T : Finset (Fin 2)) (h : List (Unit × Bool)) (_ : Unit) : Bool :=
  if h.any (fun z => z.2) then true else decide (Disjoint (supportOne ()) T)

theorem false_history_contains_no_true (n : ℕ) :
    (Actions.history chooseOne falseReply n).any (fun z => z.2) = false := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [Actions.history, falseReply, chooseOne] using ih

theorem compatible_prefix_opacity :
    Actions.Opaque supportOne chooseOne afterSuccessReply falseReply 1 := by
  intro T _ n hn
  have hd := hn n le_rfl
  simp only [Actions.spine, chooseOne] at hd
  simp [afterSuccessReply, false_history_contains_no_true, falseReply, hd]

theorem unreachable_failure_reply_may_differ :
    afterSuccessReply ({0} : Finset (Fin 2)) [((), true)] () ≠
      falseReply [((), true)] () := by decide

-- The lower bound is not restricted to a fixed preselected query order:
-- any full-action policy selecting uniform supports is included in the all-q family.
theorem any_uniform_action_policy_lower
    (support : Action → Finset α) (π : Actions.Policy Action Obs)
    (observe : Finset α → List (Action × Obs) → Action → Obs)
    (failed : List (Action × Obs) → Action → Obs) (q k N : ℕ)
    (hsize : ∀ a, (support a).card = q)
    (hop : Actions.Opaque support π observe failed k)
    (hcap : ∀ T : Finset α, T.card = k → Actions.SuccessWithin support π observe T N) :
    coveringNumber α (Fintype.card α-q) k ≤ N := by
  let F := (univ : Finset α).powersetCard q
  apply Actions.deterministic_cap_lower_bound F support ?_ π observe failed q k N ?_ hop hcap
  · intro a
    exact mem_powersetCard.mpr ⟨subset_univ _, hsize a⟩
  · intro P hP
    exact (mem_powersetCard.mp hP).2

#print axioms any_uniform_action_policy_lower

-- Instantiate the quantitative utility at the actual finite candidate family,
-- then realize the selected candidate by one map/fault set outside the coin scope.
open scoped ENNReal in
theorem fixed_root_world_quantitative_failure [MeasurableSpace Ω]
    (F : Finset (Finset α)) (support : Action → Finset α)
    (admitted : ∀ a, support a ∈ F)
    (μ : Measure Ω) [IsProbabilityMeasure μ] (π : Ω → Actions.Policy Action Obs)
    (observe : Finset α → List (Action × Obs) → Action → Obs)
    (failed : List (Action × Obs) → Action → Obs) (B c q N : ℕ)
    (hB : 1 ≤ B) (hc : 1 ≤ c) (hk : B+c-1 ≤ Fintype.card α)
    (hu : Uniform q F)
    (hop : ∀ ω, Actions.Opaque support (π ω) observe failed (B+c-1))
    (hsmall : N < coveringNumber α (Fintype.card α-q) (B+c-1)) :
    ∃ A : Finset α, A.card = c ∧ ∃ S : Finset (Option α),
      S ⊆ AttributionKernel.actualRoots A ∧ S.card = B ∧
      1 / ((Fintype.card α).choose (B+c-1) : ℝ≥0∞) ≤
        μ {ω | ¬ Actions.SuccessWithin support (π ω) observe
          (AttributionKernel.taintedLabels A S) N} := by
  classical
  let W := ↥((univ : Finset α).powersetCard (B+c-1))
  obtain ⟨T, _, hT⟩ := exists_subset_card_eq
    (show B+c-1 ≤ (univ : Finset α).card by simpa using hk)
  letI : Nonempty W := ⟨⟨T, mem_powersetCard.mpr ⟨subset_univ T, hT⟩⟩⟩
  have hcover : ∀ ω, ∃ w : W, ¬ Actions.SuccessWithin support (π ω) observe w.val N := by
    intro ω
    by_contra hn
    push_neg at hn
    have hcap : ∀ T : Finset α, T.card = B+c-1 →
        Actions.SuccessWithin support (π ω) observe T N := by
      intro T hT
      exact hn ⟨T, mem_powersetCard.mpr ⟨subset_univ T, hT⟩⟩
    have hl := Actions.deterministic_cap_lower_bound F support admitted (π ω)
      observe failed q (B+c-1) N hu (hop ω) hcap
    omega
  obtain ⟨w, hw⟩ := RandomizedFinite.exists_fixed_failure_ge_inv_card μ
    (fun (w : W) ω => ¬ Actions.SuccessWithin support (π ω) observe w.val N) hcover
  have hw' : 1 / ((Fintype.card α).choose (B+c-1) : ℝ≥0∞) ≤
      μ {ω | ¬ Actions.SuccessWithin support (π ω) observe w.val N} := by
    simpa [W] using hw
  obtain ⟨A, hA, S, hSr, hS, hST⟩ := AttributionKernel.maximal_taint_realizable
    B c hB hc w.val (mem_powersetCard.mp w.property).2
  exact ⟨A, hA, S, hSr, hS, hST ▸ hw'⟩

#print axioms fixed_root_world_quantitative_failure

-- The source interpretation needs the defective start; the bridge transports
-- actual target achievement, not a fresh definition of an allegedly successful state.
theorem defective_target_cap_lower
    (support : Action → Finset α) (π : Actions.Policy Action Obs)
    (observe : Finset α → List (Action × Obs) → Action → Obs)
    (failed : List (Action × Obs) → Action → Obs) (q k N : ℕ)
    (hsize : ∀ a, (support a).card = q)
    (hop : Actions.Opaque support π observe failed k)
    (hcap : ∀ T : Finset α, T.card = k →
      RepairState.after false (fun i => Disjoint
        (support (π (Actions.history π (observe T) i))) T) N = true) :
    coveringNumber α (Fintype.card α-q) k ≤ N := by
  apply any_uniform_action_policy_lower support π observe failed q k N hsize hop
  intro T hT
  exact (RepairState.defective_start_iff_successWithin support π observe T N).mp (hcap T hT)

#print axioms defective_target_cap_lower

-- Concrete reachable post-success histories are unconstrained as well.
def pointSupport (a : Fin 2) : Finset (Fin 2) := {a}
def switchPolicy : Actions.Policy (Fin 2) Bool := fun h => if h.isEmpty then 1 else 0
def switchFailure (_ : List (Fin 2 × Bool)) (_ : Fin 2) : Bool := false
def switchObserve (T : Finset (Fin 2)) (h : List (Fin 2 × Bool)) (a : Fin 2) : Bool :=
  if h.any (fun z => z.2) then true else decide (Disjoint (pointSupport a) T)

theorem switch_failure_history_contains_no_true (n : ℕ) :
    (Actions.history switchPolicy switchFailure n).any (fun z => z.2) = false := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [Actions.history, switchFailure] using ih

theorem switch_compatible_prefix_opacity :
    Actions.Opaque pointSupport switchPolicy switchObserve switchFailure 1 := by
  intro T _ n hn
  have hd := hn n le_rfl
  simp only [Actions.spine] at hd
  simp [switchObserve, switch_failure_history_contains_no_true, switchFailure, Actions.spine, hd]

theorem reachable_post_success_failure_reply_may_differ :
    let T : Finset (Fin 2) := {0}
    let h := Actions.history switchPolicy (switchObserve T) 1
    ¬Disjoint (pointSupport (switchPolicy h)) T ∧
      switchObserve T h (switchPolicy h) ≠ switchFailure h (switchPolicy h) := by decide

#print axioms switch_compatible_prefix_opacity
#print axioms reachable_post_success_failure_reply_may_differ
#print axioms positive_feasible_cover
#print axioms maximal_portfolio_handles_smaller
#print axioms no_zero_attempt_hit
#print axioms empty_universe_cover
#print axioms no_world_if_too_large
#print axioms zero_measure_makes_every_cap_ae
#print axioms fixed_root_world_positive_outer_measure
#print axioms compatible_prefix_opacity
#print axioms unreachable_failure_reply_may_differ
end CoveringIndependent
