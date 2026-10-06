import RotorProjection
import FinitePushforwardRows

/-! Explicit finite killed rotor kernel, retaining all source residues. The
raw receipt is drawn from the original true row and deterministically pushed
through the rotor update/kill guard. No new fair or randomized action policy is
substituted for the source's deterministic cycle. -/
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

abbrev Residues (F : Finset (State × Action)) := (s : State) → Fin (max 1 (retainedActions F s).card)
abbrev Aug (F : Finset (State × Action)) := Option (State × Residues F)

instance augMeasurableSpace (F : Finset (State × Action)) : MeasurableSpace (Aug F) := ⊤
instance augMeasurableSingletonClass (F : Finset (State × Action)) : MeasurableSingletonClass (Aug F) :=
  ⟨fun _ => by trivial⟩

variable (F : Finset (State × Action)) (fallback : Action) (s₀ : State)

def chosen (s : State) (r : Residues F) : Action :=
  cycleAction (retainedActions F s) fallback (r s).val

def bump (r : Residues F) (s : State) : Residues F := fun t =>
  ⟨((r t).val + if s=t then 1 else 0) % max 1 (retainedActions F t).card,
    Nat.mod_lt _ (lt_of_lt_of_le (by decide : 0<1) (Nat.le_max_left _ _))⟩

def source : Aug F → State | none => s₀ | some z => z.1

def action : Aug F → Action | none => fallback | some z => chosen F fallback z.1 z.2

def residue : Aug F → State → ℕ | none => fun _ => 0 | some z => fun s => (z.2 s).val

variable (before : State × Action → Prop) (after : (State × Action) → State → Prop)

def next (q : Aug F) (y : State) : Aug F := by
  classical
  exact match q with
  | none => none
  | some (s,r) => if s ∉ usedStates Prod.fst F ∨ before (s,chosen F fallback s r) ∨ after (s,chosen F fallback s r) y
      then none else some (y,bump F r s)

variable (P : RationalKernel Model (State × Action) State) (σ : Model)

def weight (q : Aug F) (y : State) : ℝ := realRows P σ (source F s₀ q,action F fallback q) y

def kernel : Rows (Aug F) := by
  classical
  exact pushRows (weight F fallback s₀ P σ)
    (fun q y => realRows_nonnegative P σ _ y) (fun q => realRows_normalized P σ _)
    (next F fallback before after)

omit [Inhabited State] [DecidableEq Model] [MeasurableSpace State] [MeasurableSingletonClass State] [MeasurableSpace Action] [MeasurableSingletonClass Action] in
theorem kernel_positive_iff (q q' : Aug F) :
    0 < (kernel F fallback s₀ before after P σ).row q q' ↔
      ∃ y, 0 < weight F fallback s₀ P σ q y ∧ next F fallback before after q y=q' := by
  classical
  exact pushRows_positive_iff _ _ _ _ q q'

omit [Inhabited State] [DecidableEq Model] [MeasurableSpace State] [MeasurableSingletonClass State] [MeasurableSpace Action] [MeasurableSingletonClass Action] in
theorem kernel_min_positive (p : ℝ)
    (hmin : ∀ e y, 0 < realRows P σ e y → p ≤ realRows P σ e y) :
    ∀ q q', 0 < (kernel F fallback s₀ before after P σ).row q q' →
      p ≤ (kernel F fallback s₀ before after P σ).row q q' := by
  classical
  exact pushRows_min_positive _ _ _ _ p (fun q y hy => hmin _ y hy)

theorem bump_val (r : Residues F) (s : State) (hs : s ∈ usedStates Prod.fst F) (t : State) :
    (bump F r s t).val = ((r t).val + if s=t then 1 else 0)%(retainedActions F t).card := by
  have hc : 0 < (retainedActions F s).card := Finset.card_pos.mpr (retainedActions_nonempty F s hs)
  by_cases hz : (retainedActions F t).card=0
  · have hrt : (r t).val=0 := by have hh := (r t).isLt; simp only [hz,max_eq_left (by decide : 0≤1)] at hh; omega
    have hst : s ≠ t := by intro he; subst t; omega
    simp [bump,hz,hst,hrt]
  · have hm : max 1 (retainedActions F t).card=(retainedActions F t).card := max_eq_right (by omega)
    simp only [bump,hm]

omit [Fintype State] [Inhabited State] [MeasurableSpace State] [MeasurableSingletonClass State] [MeasurableSpace Action] [MeasurableSingletonClass Action] in
theorem next_nonterminal_iff (s : State) (r : Residues F) (y : State) :
    next F fallback before after (some (s,r)) y ≠ none ↔
      s ∈ usedStates Prod.fst F ∧ ¬ before (s,chosen F fallback s r) ∧ ¬ after (s,chosen F fallback s r) y := by
  classical
  simp [next,not_or]

theorem next_of_nonterminal (s : State) (r : Residues F) (y : State)
    (h : next F fallback before after (some (s,r)) y ≠ none) :
    next F fallback before after (some (s,r)) y=some (y,bump F r s) := by
  classical
  obtain ⟨hs,hb,ha⟩ := (next_nonterminal_iff F fallback before after s r y).mp h
  simp [next,hs,hb,ha]

omit [Inhabited State] [DecidableEq Model] [MeasurableSpace State] [MeasurableSingletonClass State] [MeasurableSpace Action] [MeasurableSingletonClass Action] in
theorem pre_stop_kills (s : State) (r : Residues F)
    (h : s ∉ usedStates Prod.fst F ∨ before (s,chosen F fallback s r)) :
    (kernel F fallback s₀ before after P σ).row (some (s,r)) none=1 := by
  classical
  apply pushRows_constant
  intro y
  rcases h with hs | hb
  · simp [next,hs]
  · simp [next,hb]

variable (C : Finset (Aug F))
variable (hC : ClosedClass (fun q q' => 0 < (kernel F fallback s₀ before after P σ).row q q') C)
variable (hKill : (none : Aug F) ∉ C)
include hC hKill

/-- A closed class avoiding the actual kill state cannot contain an invalid
source or a pre-stop pair. -/
theorem class_valid (q : Aug F) (hq : q ∈ C) :
    ∃ s r, q=some (s,r) ∧ s ∈ usedStates Prod.fst F ∧ ¬ before (s,chosen F fallback s r) := by
  classical
  cases q with
  | none => exact (hKill hq).elim
  | some z =>
      rcases z with ⟨s,r⟩
      refine ⟨s,r,rfl,?_⟩
      by_contra hh
      have hstop : s ∉ usedStates Prod.fst F ∨ before (s,chosen F fallback s r) := by tauto
      have he := pre_stop_kills F fallback s₀ before after P σ s r hstop
      exact hKill (hC.2.1 _ hq none (by change 0 < (kernel F fallback s₀ before after P σ).row (some (s,r)) none; rw [he]; norm_num))

/-- Every positive receipt from such a class yields a nonterminal actual rotor
successor. In particular, no post-stop guard can fire there. -/
theorem class_next_nonterminal (q : Aug F) (hq : q ∈ C) (y : State)
    (hy : 0 < weight F fallback s₀ P σ q y) :
    next F fallback before after q y ≠ none := by
  intro he
  have hedge : 0 < (kernel F fallback s₀ before after P σ).row q none :=
    (kernel_positive_iff F fallback s₀ before after P σ q none).mpr ⟨y,hy,he⟩
  exact hKill (hC.2.1 q hq none hedge)

/-- Construct the local source-counter graph witness from the explicit killed
kernel. Its fairness and component/target consequences follow from previously
proved projection theorems; none is assumed here. -/
def witness_of_closed_class : RotorClassWitness (Q:=Aug F) P σ F fallback where
  source := source F s₀
  action := action F fallback
  residue := residue F
  edge q q' := 0 < (kernel F fallback s₀ before after P σ).row q q'
  C := C
  closed := hC
  source_used := by
    intro q hq
    obtain ⟨s,r,rfl,hs,_⟩ := class_valid F fallback s₀ before after P σ C hC hKill q hq
    exact hs
  action_cycle := by
    intro q hq
    obtain ⟨s,r,rfl,_,_⟩ := class_valid F fallback s₀ before after P σ C hC hKill q hq
    rfl
  rotor_step := by
    intro q hq q' hedge t
    obtain ⟨s,r,rfl,hs,_⟩ := class_valid F fallback s₀ before after P σ C hC hKill q hq
    obtain ⟨y,hy,hnext⟩ := (kernel_positive_iff F fallback s₀ before after P σ _ _).mp hedge
    have hnon := class_next_nonterminal F fallback s₀ before after P σ C hC hKill _ hq y hy
    have he := next_of_nonterminal F fallback before after s r y hnon
    have hq' : q'=some (y,bump F r s) := hnext.symm.trans he
    rw [hq']
    exact bump_val F r s hs t
  positive_lift := by
    intro q hq y hy
    obtain ⟨s,r,rfl,hs,hb⟩ := class_valid F fallback s₀ before after P σ C hC hKill q hq
    have hreal : 0 < weight F fallback s₀ P σ (some (s,r)) y := by
      change (0 : ℝ) < (P.row σ (s,chosen F fallback s r) y : ℝ)
      exact_mod_cast hy
    have hnon := class_next_nonterminal F fallback s₀ before after P σ C hC hKill _ hq y hreal
    have he := next_of_nonterminal F fallback before after s r y hnon
    refine ⟨some (y,bump F r s),?_,rfl⟩
    exact (kernel_positive_iff F fallback s₀ before after P σ _ _).mpr ⟨y,hreal,he⟩

end HiddenParity.Cost.FrozenRotor
