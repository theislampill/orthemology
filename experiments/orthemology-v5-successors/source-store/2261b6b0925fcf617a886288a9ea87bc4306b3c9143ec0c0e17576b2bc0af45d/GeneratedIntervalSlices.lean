import GeneratedIntervalHistory

noncomputable section
attribute [local instance] Classical.propDecidable
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive HiddenParity.Empirical
open HiddenParity.Necessity HiddenParity.Stage
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]
variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]
variable (P : RationalKernel Model (State × Action) State)
variable (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
variable (B₀ : Finset Model) (s₀ : State) (fallback : Model) (fallbackAction : Action)
variable (reject : Model → ℕ → History (State × Action) State → Bool)
local notation "b" => runSupport P menu priority B₀ s₀ fallback fallbackAction reject
local notation "m" => runMemory P menu priority B₀ s₀ fallback fallbackAction reject
local notation "H" => runHistory P menu priority B₀ s₀ fallback fallbackAction reject
local notation "x" => runAction P menu priority B₀ s₀ fallback fallbackAction reject
local notation "label" => generatedSegmentLabel P menu priority B₀ s₀ fallback fallbackAction reject
local notation "tail" => runTail P menu priority B₀ s₀ fallback fallbackAction reject
local notation "progress" => runProgress P menu priority B₀ s₀ fallback fallbackAction reject

theorem generated_active_run (z : Unit × FlatStack (State × Action) State) (t : ℕ) :
    GeneratedSlice.active P menu priority B₀ s₀ fallback reject (H z t)=
      activePairs P menu priority (b z t) (m z t) := by
  simp only [GeneratedSlice.active,runHistory_augment]
  rfl

/-- A chronological no-progress window is a literal continuing-slice event
once its actual active-set and progress guards are verified at each step. -/
theorem run_continues_of_guards
    (z : Unit × FlatStack (State × Action) State) (s n : ℕ)
    (F : Finset (State × Action)) (before : State × Action → Prop) (after : State × Action → State → Prop)
    (hF : ∀ i, i < n → activePairs P menu priority (b z (s+i)) (m z (s+i))=F)
    (hBefore : ∀ i, i < n → ¬before (x z (s+i)))
    (hAfter : ∀ i, i < n → ¬after (x z (s+i)) (x z (s+i+1)).1) :
    GeneratedSlice.Continues P menu priority B₀ s₀ fallback reject F before after (fun _ => False)
      (H z s) (tail z s n) := by
  induction n with
  | zero => trivial
  | succ n ih =>
      rw [runTail_succ]
      refine ⟨ih (by intro i hi;exact hF i (by omega))
        (by intro i hi;exact hBefore i (by omega)) (by intro i hi;exact hAfter i (by omega)),?_,
        hBefore n (by omega),hAfter n (by omega),not_false⟩
      rw [runTail_append,generated_active_run]
      exact hF n (by omega)

/-- Literal no-progress navigation gives all guards of the source-instantiated
conditional rotor tail. In particular target entry cannot be silently skipped. -/
theorem run_navigation_continues
    (hs₀ : s₀  ∈  winningRegion P menu priority B₀) (σ : Model) (hσ : σ  ∈  B₀)
    (z : Unit × FlatStack (State × Action) State)
    (hSupported : ∀ e k,0<realRows P σ e (z.2 (e,k)))
    (s n : ℕ) (hNav : (m z s).retained=none)
    (hp : ∀ i,s ≤ i → i < s+n → ¬progress σ z i) :
    GeneratedSlice.Continues P menu priority B₀ s₀ fallback reject (stageActions P menu priority (b z s))
      (FrozenRotor.navigationBefore P menu priority (b z s) (phaseCandidate (b z s) fallback (m z s)) σ)
      (FrozenRotor.navigationAfter P menu priority (b z s) (phaseCandidate (b z s) fallback (m z s)))
      (fun _ => False) (H z s) (tail z s n) := by
  have hl : ∀ i,i ≤ n → label z (s+i)=label z s := by
    intro i hi
    exact run_label_eq_of_no_progress P menu priority B₀ s₀ fallback fallbackAction reject σ z s i
      (by intro j hjs hji;exact hp j hjs (by omega))
  have hb : ∀ i,i ≤ n → b z (s+i)=b z s := fun i hi => congrArg Prod.fst (hl i hi)
  have hi : ∀ i,i ≤ n → (m z (s+i)).index=(m z s).index := fun i hi => congrArg (fun v => v.2.1) (hl i hi)
  have hr : ∀ i,i ≤ n → (m z (s+i)).retained=none := by
    intro i hi
    exact (congrArg (fun v => v.2.2) (hl i hi)).trans hNav
  have hc : ∀ i,i ≤ n → phaseCandidate (b z (s+i)) fallback (m z (s+i))=phaseCandidate (b z s) fallback (m z s) := by
    intro i hit
    simp only [phaseCandidate,hb i hit,hi i hit]
  have hstate : ∀ i,i ≤ n → (x z (s+i)).1  ∈  winningRegion P menu priority (b z s) ∧
      (x z (s+i)).1  ∉  stageTargets P menu priority (b z s) (phaseCandidate (b z s) fallback (m z s)) := by
    intro i hit
    have hv := run_invariant P menu priority B₀ s₀ fallback fallbackAction reject hs₀ σ hσ z hSupported (s+i)
    have ht := run_navigation_avoids_target P menu priority B₀ s₀ fallback fallbackAction reject z (s+i) (hr i hit)
    rw [hc i hit,hb i hit] at ht
    exact ⟨hb i hit ▸ hv.2.1,ht⟩
  apply run_continues_of_guards
  · intro i hin
    simp only [activePairs,hr i (by omega),Option.getD_none,hb i (by omega)]
  · intro i hin
    have hp' := hp (s+i) (by omega) (by omega)
    rw [runProgress_iff] at hp'
    have he := (not_or.mp hp').2
    rw [hc i (by omega)] at he
    exact not_or.mpr ⟨he,not_or.mpr ⟨not_not.mpr (hstate i (by omega)).1,(hstate i (by omega)).2⟩⟩
  · intro i hin
    have he := runSupport_succ P menu priority B₀ s₀ fallback fallbackAction reject z (s+i)
    rw [hb i (by omega)] at he
    have hh := hb (i+1) (by omega)
    rw [← Nat.add_assoc] at hh
    rw [he] at hh
    exact not_or.mpr ⟨not_not.mpr hh,not_or.mpr
      ⟨not_not.mpr (by simpa only [Nat.add_assoc] using (hstate (i+1) (by omega)).1),
        by simpa only [Nat.add_assoc] using (hstate (i+1) (by omega)).2⟩⟩

/-- Operation window binding uses the exact retained component, original true
rows, and actual successor invariant; no fairness or reset assumption is added. -/
theorem run_operation_continues
    (hs₀ : s₀  ∈  winningRegion P menu priority B₀) (σ : Model) (hσ : σ  ∈  B₀)
    (z : Unit × FlatStack (State × Action) State)
    (hSupported : ∀ e k,0<realRows P σ e (z.2 (e,k)))
    (s n : ℕ) (E : Finset (State × Action)) (hOp : (m z s).retained=some E)
    (hp : ∀ i,s ≤ i → i < s+n → ¬progress σ z i) :
    GeneratedSlice.Continues P menu priority B₀ s₀ fallback reject E
      (FrozenRotor.mismatching P (phaseCandidate (b z s) fallback (m z s)) σ)
      (FrozenRotor.operatingAfter P (b z s) E) (fun _ => False) (H z s) (tail z s n) := by
  have hl : ∀ i,i ≤ n → label z (s+i)=label z s := by
    intro i hi
    exact run_label_eq_of_no_progress P menu priority B₀ s₀ fallback fallbackAction reject σ z s i
      (by intro j hjs hji;exact hp j hjs (by omega))
  have hb : ∀ i,i ≤ n → b z (s+i)=b z s := fun i hi => congrArg Prod.fst (hl i hi)
  have hi : ∀ i,i ≤ n → (m z (s+i)).index=(m z s).index := fun i hi => congrArg (fun v => v.2.1) (hl i hi)
  have hr : ∀ i,i ≤ n → (m z (s+i)).retained=some E := by
    intro i hi
    exact (congrArg (fun v => v.2.2) (hl i hi)).trans hOp
  apply run_continues_of_guards
  · intro i hin
    simp only [activePairs,hr i (by omega),Option.getD_some]
  · intro i hin
    have hp' := hp (s+i) (by omega) (by omega)
    rw [runProgress_iff] at hp'
    have he := (not_or.mp hp').2
    simpa only [FrozenRotor.mismatching,phaseCandidate,hb i (by omega),hi i (by omega)] using he
  · intro i hin
    have he := runSupport_succ P menu priority B₀ s₀ fallback fallbackAction reject z (s+i)
    rw [hb i (by omega)] at he
    have hh := hb (i+1) (by omega)
    rw [← Nat.add_assoc] at hh
    rw [he] at hh
    have hv := run_invariant P menu priority B₀ s₀ fallback fallbackAction reject hs₀ σ hσ z hSupported (s+(i+1))
    have hs := (hv.2.2 E (hr (i+1) (by omega))).2
    exact not_or.mpr ⟨not_not.mpr hh,not_not.mpr (by simpa only [Nat.add_assoc] using hs)⟩

end HiddenParity.Cost
