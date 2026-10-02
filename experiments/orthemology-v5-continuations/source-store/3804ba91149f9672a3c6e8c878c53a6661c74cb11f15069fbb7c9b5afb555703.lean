import FrozenRotorKernel

noncomputable section
namespace HiddenParity.Cost.FrozenRotor
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive
open HiddenParity.Necessity HiddenParity.Stage FiniteChainHitting
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

omit [Inhabited State] [MeasurableSpace State] [MeasurableSingletonClass State] [MeasurableSpace Action] [MeasurableSingletonClass Action] in
/-- The actual all-source residue representation has at most s*a^s live
vertices, plus its kill state. Empty unused menus get only one residue. -/
theorem aug_card_bound (F : Finset (State × Action)) (fallback : Action) :
    Fintype.card (Aug F)-1 ≤ Fintype.card State * Fintype.card Action ^ Fintype.card State := by
  have ha : 1 ≤ Fintype.card Action := by
    have hp := Fintype.card_pos_iff.mpr (show Nonempty Action from ⟨fallback⟩)
    omega
  have hprod : (∏ s : State, max 1 (retainedActions F s).card) ≤
      Fintype.card Action ^ Fintype.card State := by
    calc
      _ ≤ ∏ _s : State, Fintype.card Action := Finset.prod_le_prod (by intro s _; omega)
        (by intro s _; exact max_le ha (Finset.card_le_univ _))
      _ = _ := by simp
  simp only [Aug,Fintype.card_option,Nat.add_sub_cancel,Fintype.card_prod,Residues,Fintype.card_pi,Fintype.card_fin]
  exact Nat.mul_le_mul_left _ hprod

def mismatching (P : RationalKernel Model (State × Action) State) (θ σ : Model)
    (e : State × Action) : Prop := P.row θ e ≠ P.row σ e

def operatingAfter (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (E : Finset (State × Action)) (e : State × Action) (y : State) : Prop :=
  liveUpdate P B e y ≠ B ∨ y ∉ usedStates Prod.fst E

/-- In a genuinely mismatching qualifying operation, every closed class of
the literal frozen killed rotor kernel contains the kill state. -/
theorem operation_classes_hit_kill
    (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (priority : Model → (State × Action) → ℕ) (θ σ : Model) (hσ : σ ∈ B)
    (allowed E : Finset (State × Action))
    (hQ : MarkovQualifying P Prod.fst B priority θ allowed E)
    (hNe : ¬ Match P.row θ σ E) (fallback : Action) (s₀ : State)
    (C : Finset (Aug E))
    (hC : ClosedClass (fun q q' => 0 < (kernel E fallback s₀ (mismatching P θ σ)
      (operatingAfter P B E) P σ).row q q') C) : (none : Aug E) ∈ C := by
  classical
  by_contra hKill
  let R := witness_of_closed_class E fallback s₀ (mismatching P θ σ) (operatingAfter P B E) P σ C hC hKill
  obtain ⟨q,hq,hmis⟩ := R.operation_has_mismatch B priority θ hσ allowed hQ hNe
  change q ∈ C at hq
  obtain ⟨s,r,hqr,_,hnot⟩ := class_valid E fallback s₀ (mismatching P θ σ) (operatingAfter P B E) P σ C hC hKill q hq
  subst q
  exact hnot hmis

def navigationBefore (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (θ σ : Model) (e : State × Action) : Prop :=
  mismatching P θ σ e ∨ e.1 ∉ winningRegion P menu priority B ∨ e.1 ∈ stageTargets P menu priority B θ

def navigationAfter (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (θ : Model) (e : State × Action) (y : State) : Prop :=
  liveUpdate P B e y ≠ B ∨ y ∉ winningRegion P menu priority B ∨ y ∈ stageTargets P menu priority B θ

/-- The computed stage's target-or-exit certificate excludes every avoiding
closed class of the explicit true-row rotor kernel. -/
theorem navigation_classes_hit_kill
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (θ σ : Model) (hθ : θ ∈ B)
    (fallback : Action) (s₀ : State)
    (C : Finset (Aug (stageActions P menu priority B)))
    (hC : ClosedClass (fun q q' => 0 < (kernel (stageActions P menu priority B) fallback s₀
      (navigationBefore P menu priority B θ σ) (navigationAfter P menu priority B θ) P σ).row q q') C) :
    (none : Aug (stageActions P menu priority B)) ∈ C := by
  classical
  by_contra hKill
  let F := stageActions P menu priority B
  let before := navigationBefore P menu priority B θ σ
  let after := navigationAfter P menu priority B θ
  let R := witness_of_closed_class F fallback s₀ before after P σ C hC hKill
  have hvalid (q) (hq : q ∈ R.C) :
      ∃ s r, q=some (s,r) ∧ s ∈ usedStates Prod.fst F ∧ ¬ before (s,chosen F fallback s r) :=
    class_valid F fallback s₀ before after P σ C hC hKill q hq
  have hRegion : ∀ q ∈ R.C, R.source q ∈ winningRegion P menu priority B := by
    intro q hq
    obtain ⟨s,r,rfl,_,hb⟩ := hvalid q hq
    change s ∈ winningRegion P menu priority B
    simp only [before,navigationBefore,not_or,not_not] at hb
    exact hb.2.1
  have hMatch : Match P.row θ σ R.project := by
    intro e he
    obtain ⟨q,hq,hqe⟩ := Finset.mem_image.mp he
    obtain ⟨s,r,rfl,_,hb⟩ := hvalid q hq
    have hh : ¬ mismatching P θ σ (s,chosen F fallback s r) := fun h => hb (Or.inl h)
    have hEq : P.row θ (s,chosen F fallback s r) = P.row σ (s,chosen F fallback s r) := by
      simpa only [mismatching,not_not] using hh
    change (s,chosen F fallback s r)=e at hqe
    simpa only [hqe] using hEq.symm
  have hNo : ∀ e ∈ R.project, NoExit P B σ e := by
    intro e he y hy
    obtain ⟨q,hq,hqe⟩ := Finset.mem_image.mp he
    obtain ⟨s,r,rfl,_,_⟩ := hvalid q hq
    change (s,chosen F fallback s r)=e at hqe
    have hreal : 0 < weight F fallback s₀ P σ (some (s,r)) y := by
      change (0 : ℝ) < (P.row σ (s,chosen F fallback s r) y : ℝ)
      rw [hqe]
      exact_mod_cast hy
    have hn := class_next_nonterminal F fallback s₀ before after P σ C hC hKill _ hq y hreal
    have ha := (next_nonterminal_iff F fallback before after s r y).mp hn |>.2.2
    have hStable : liveUpdate P B e y=B := by
      have hh : ¬ liveUpdate P B (s,chosen F fallback s r) y ≠ B := fun h => ha (Or.inl h)
      simpa only [hqe,not_not] using hh
    exact (liveUpdate_eq_iff_internal P B e y).mp hStable
  obtain ⟨t,ht,htr⟩ := R.navigation_hits_target menu priority B θ hθ rfl hRegion hMatch hNo
  obtain ⟨e,he,het⟩ := Finset.mem_image.mp htr
  obtain ⟨q,hq,hqe⟩ := Finset.mem_image.mp he
  obtain ⟨s,r,rfl,_,hb⟩ := hvalid q hq
  have hsrc : s=t := (congrArg Prod.fst hqe).trans het
  exact hb (Or.inr (Or.inr (hsrc.symm ▸ ht)))

/-- Universal explicit finite-state dimension for the original source-counter
representation, independent of its current support, phase, or component. -/
def dimension (State Action : Type u) [Fintype State] [Fintype Action] : ℕ :=
  Fintype.card State * Fintype.card Action ^ Fintype.card State

/-- Actual finite-horizon PMF tail for the explicit killed frozen rotor kernel,
using the derived cardinality and positive-path bounds. -/
theorem kernel_geometric_tail
    (F : Finset (State × Action)) (fallback : Action) (s₀ : State)
    (before : State × Action → Prop) (after : (State × Action) → State → Prop)
    (P : RationalKernel Model (State × Action) State) (σ : Model)
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hmin : ∀ e y, 0 < realRows P σ e y → p ≤ realRows P σ e y)
    (hclasses : ∀ C, ClosedClass (fun q q' => 0 < (kernel F fallback s₀ before after P σ).row q q') C →
      (none : Aug F) ∈ C)
    (k : ℕ) (q : Aug F) :
    (absorbedLaw (kernel F fallback s₀ before after P σ) (fun q => q=none)
      (k*dimension State Action) q).toMeasure {q | q≠none} ≤
      ENNReal.ofReal ((1-p^dimension State Action)^k) := by
  classical
  have hreach := reaches_goal_of_no_avoiding_class
    (fun q q' => 0 < (kernel F fallback s₀ before after P σ).row q q')
    (fun q : Aug F => q=none) (by intro C hC; exact ⟨none,hclasses C hC,rfl⟩)
  apply absorbedLaw_geometric_survival (kernel F fallback s₀ before after P σ) (fun q => q=none)
    p hp hp1 (kernel_min_positive F fallback s₀ before after P σ p hmin)
    (dimension State Action) ?_ k q
  intro u
  obtain ⟨t,ht,hu⟩ := hreach u
  obtain ⟨n,hn,hpath⟩ := reachable_short_path
    (fun q q' => 0 < (kernel F fallback s₀ before after P σ).row q q') u t hu
  exact ⟨t,n,ht,hn.trans (aug_card_bound F fallback),hpath⟩

/-- Quantitative PMF progress in the selected *actual qualifying component*
when at least one of its rows differs from the true live model. -/
theorem operation_geometric_tail
    (P : RationalKernel Model (State × Action) State) (B : Finset Model)
    (priority : Model → (State × Action) → ℕ) (θ σ : Model) (hσ : σ ∈ B)
    (allowed E : Finset (State × Action))
    (hQ : MarkovQualifying P Prod.fst B priority θ allowed E)
    (hNe : ¬ Match P.row θ σ E) (fallback : Action) (s₀ : State)
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hmin : ∀ e y, 0 < realRows P σ e y → p ≤ realRows P σ e y)
    (k : ℕ) (q : Aug E) :
    (absorbedLaw (kernel E fallback s₀ (mismatching P θ σ) (operatingAfter P B E) P σ)
      (fun q => q=none) (k*dimension State Action) q).toMeasure {q | q≠none} ≤
      ENNReal.ofReal ((1-p^dimension State Action)^k) := by
  classical
  exact kernel_geometric_tail E fallback s₀ (mismatching P θ σ) (operatingAfter P B E) P σ p hp hp1 hmin
    (operation_classes_hit_kill P B priority θ σ hσ allowed E hQ hNe fallback s₀) k q

/-- Quantitative PMF progress in navigation using the actual computed stage
menu/target definitions. No recurrent-set or fairness input is supplied. -/
theorem navigation_geometric_tail
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (θ σ : Model) (hθ : θ ∈ B)
    (fallback : Action) (s₀ : State)
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hmin : ∀ e y, 0 < realRows P σ e y → p ≤ realRows P σ e y)
    (k : ℕ) (q : Aug (stageActions P menu priority B)) :
    (absorbedLaw (kernel (stageActions P menu priority B) fallback s₀
      (navigationBefore P menu priority B θ σ) (navigationAfter P menu priority B θ) P σ)
      (fun q => q=none) (k*dimension State Action) q).toMeasure {q | q≠none} ≤
      ENNReal.ofReal ((1-p^dimension State Action)^k) := by
  classical
  exact kernel_geometric_tail (stageActions P menu priority B) fallback s₀
    (navigationBefore P menu priority B θ σ) (navigationAfter P menu priority B θ) P σ p hp hp1 hmin
    (navigation_classes_hit_kill P menu priority B θ σ hθ fallback s₀) k q

end HiddenParity.Cost.FrozenRotor
