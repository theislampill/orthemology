import QuantitativeEmpiricalGate

noncomputable section
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost
open HiddenParity.Adaptive HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Empirical
universe u v w
variable {R : Type v} {A Y : Type u} [Fintype A] [DecidableEq A] [Inhabited Y]

/-- Actual tape consumption never reuses a pair/index cell, regardless of the
history policy, support resets, phase changes, or adaptive gaps. -/
theorem consumed_pair_index_injective (π : R → History A Y → A) (z : R × FlatStack A Y) :
    Function.Injective (fun n => (stackActionTrajectory π z n,
      countBefore π z (stackActionTrajectory π z n) n)) := by
  intro i j hij
  have ha := congrArg Prod.fst hij
  have hc := congrArg Prod.snd hij
  by_contra hne
  have strict {i j : ℕ} (hlt : i < j)
      (ha : stackActionTrajectory π z i = stackActionTrajectory π z j)
      (hc : countBefore π z (stackActionTrajectory π z i) i =
        countBefore π z (stackActionTrajectory π z j) j) : False := by
    have hs := countBefore_succ π z (stackActionTrajectory π z i) i
    simp only [ite_true, eq_self_iff_true] at hs
    have hm := countBefore_mono π z (stackActionTrajectory π z i) (show i+1 ≤ j by omega)
    rw [← ha] at hc
    omega
  rcases lt_or_gt_of_ne hne with h | h
  · exact strict h ha hc
  · exact strict h ha.symm hc.symm

/-- Global, not per-phase, cap on marked executions with small cumulative
pre-counts. I may combine visits from arbitrarily many support/mode epochs. -/
theorem global_low_count_budget (π : R → History A Y → A) (z : R × FlatStack A Y)
    (I : Finset ℕ) (L : ℕ)
    (hLow : ∀ n ∈ I, countBefore π z (stackActionTrajectory π z n) n < L) :
    I.card ≤ Fintype.card A * L := by
  let f : I → A × Fin L := fun n => (stackActionTrajectory π z n,
    ⟨countBefore π z (stackActionTrajectory π z n) n,hLow n n.property⟩)
  have hf : Function.Injective f := by
    intro i j hij
    apply Subtype.ext
    apply consumed_pair_index_injective π z
    have h := congrArg (fun p : A × Fin L => (p.1,p.2.val)) hij
    exact h
  have hcard := Fintype.card_le_of_injective f hf
  simpa only [Fintype.card_coe,Fintype.card_prod,Fintype.card_fin] using hcard

/-- Inclusive completed-transition counts below L give q(L-1) nonterminal
mismatch charges across the whole run. This is the key linear-budget gain. -/
theorem global_postcount_budget (π : R → History A Y → A) (z : R × FlatStack A Y)
    (I : Finset ℕ) (L : ℕ)
    (hLow : ∀ n ∈ I, countBefore π z (stackActionTrajectory π z n) (n+1) < L) :
    I.card ≤ Fintype.card A * (L-1) := by
  apply global_low_count_budget π z I (L-1)
  intro n hn
  have hs := countBefore_succ π z (stackActionTrajectory π z n) n
  simp only [ite_true, eq_self_iff_true] at hs
  have h := hLow n hn
  omega

variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]

/-- A mismatching pair in a nonrejecting accurate history has not crossed the
uniform count threshold. Applied after each nonterminating actual transition,
this discharges the global counting lemma's only quantitative premise. -/
theorem nonrejecting_mismatch_count_lt
    (P : RationalKernel Model (State × Action) State) (σ θ : Model)
    (ε η : ℝ) (N k L : ℕ) (hNL : N ≤ L) (hkL : k < L)
    (h : History (State × Action) State) (ha : HistoryAccurate P σ η N h)
    (hNo : empiricalReject P ε θ k h = false)
    (e : State × Action) (y : State)
    (hgap : ε + η ≤ |realRows P σ e y - realRows P θ e y|) :
    actionCount e h < L := by
  by_contra hge
  have hCount : L ≤ actionCount e h := by omega
  have hYes := mismatch_test_true_of_accurate P σ θ ε η N k h ha e y
    (hNL.trans hCount) (by omega) hgap
  rw [hNo] at hYes
  cases hYes

end HiddenParity.Cost
