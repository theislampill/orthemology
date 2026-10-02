import GlobalCountBudget

noncomputable section
open Orthemology.Tranche2.PolicyEmbedding
namespace HiddenParity.Cost
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Adaptive
open HiddenParity.Necessity HiddenParity.Stage
universe u w

/-- The two modes of one phase, in the order actually visited by the source. -/
def modeBit {α : Type*} : Option α → ℕ
  | none => 0
  | some _ => 1

theorem modeBit_le_one {α : Type*} (o : Option α) : modeBit o ≤ 1 := by
  cases o <;> simp [modeBit]

/-- A finite chronological boundary census. The boundary after transition t
belongs to the next segment, so the initial segment is counted separately. -/
def segmentStarts {α : Type*} [DecidableEq α] (label : ℕ → α) (T : ℕ) : Finset ℕ :=
  (Finset.range T).filter (fun t => t=0 ∨ label t ≠ label (t-1))

/-- A strictly increasing bounded rank at label changes controls all finite
segment enumerations, including arbitrary repeated label values in other runs. -/
theorem segmentStarts_card_le {α : Type*} [DecidableEq α]
    (label : ℕ → α) (rank : ℕ → ℕ) (T K : ℕ)
    (hmono : ∀ i j, i ≤ j → j < T → rank i ≤ rank j)
    (hstep : ∀ t, t+1 < T → label (t+1) ≠ label t → rank t < rank (t+1))
    (hbound : ∀ t, t<T → rank t<K) :
    (segmentStarts label T).card ≤ K := by
  classical
  let f : segmentStarts label T → Fin K := fun t =>
    ⟨rank t,(hbound t (Finset.mem_range.mp (Finset.mem_filter.mp t.property).1))⟩
  have hinj : Function.Injective f := by
    intro i j he
    have hr : rank i=rank j := congrArg Fin.val he
    apply Subtype.ext
    by_contra hn
    have hi := Finset.mem_filter.mp i.property
    have hj := Finset.mem_filter.mp j.property
    have strict : ∀ a b : segmentStarts label T, (a:ℕ)<b → rank a<rank b := by
      intro a b hab
      have hb := Finset.mem_filter.mp b.property
      have hbT := Finset.mem_range.mp hb.1
      have hb0 : (b:ℕ)≠0 := by omega
      have hchange : label b≠label ((b:ℕ)-1) := hb.2.resolve_left hb0
      have hs := hstep ((b:ℕ)-1) (by omega) (by simpa only [Nat.sub_add_cancel (by omega : 1≤(b:ℕ))] using hchange)
      have hm := hmono a ((b:ℕ)-1) (by omega) (by omega)
      have hbEq : (b:ℕ)-1+1=b := Nat.sub_add_cancel (by omega)
      rw [hbEq] at hs
      exact hm.trans_lt hs
    rcases lt_or_gt_of_ne hn with h | h
    · have := strict i j h
      omega
    · have := strict j i h
      omega
  have hc := Fintype.card_le_of_injective f hinj
  simpa only [Fintype.card_coe,Fintype.card_fin] using hc

/-- Each final transition is charged to its ending segment, including the
last transition of a deterministic truncation. -/
def segmentEnds {α : Type*} [DecidableEq α] (label : ℕ → α) (T : ℕ) : Finset ℕ :=
  (Finset.range T).filter (fun t => t+1=T ∨ label (t+1)≠label t)

theorem segmentEnds_card_le {α : Type*} [DecidableEq α]
    (label : ℕ → α) (rank : ℕ → ℕ) (T K : ℕ)
    (hmono : ∀ i j, i≤j → j<T → rank i≤rank j)
    (hstep : ∀ t, t+1<T → label (t+1)≠label t → rank t<rank (t+1))
    (hbound : ∀ t, t<T → rank t<K) :
    (segmentEnds label T).card≤K := by
  classical
  let f : segmentEnds label T → Fin K := fun t =>
    ⟨rank t,hbound t (Finset.mem_range.mp (Finset.mem_filter.mp t.property).1)⟩
  have strict : ∀ a b : segmentEnds label T, (a:ℕ)<b → rank a<rank b := by
    intro a b hab
    have ha := Finset.mem_filter.mp a.property
    have hbT := Finset.mem_range.mp (Finset.mem_filter.mp b.property).1
    have hchange : label ((a:ℕ)+1)≠label a := ha.2.resolve_left (by omega)
    exact (hstep a (by omega) hchange).trans_le (hmono ((a:ℕ)+1) b (by omega) hbT)
  have hf : Function.Injective f := by
    intro i j he
    have hr : rank i=rank j := congrArg Fin.val he
    apply Subtype.ext
    by_contra hn
    rcases lt_or_gt_of_ne hn with h | h
    · have := strict i j h;omega
    · have := strict j i h;omega
  simpa only [Fintype.card_coe,Fintype.card_fin] using Fintype.card_le_of_injective f hf

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

/-- Literal segment label: full support, phase index and retained component.
Changing a component is not identified with merely remaining in operation. -/
def generatedSegmentLabel (z : Unit × FlatStack (State × Action) State) (t : ℕ) :=
  (b z t,(m z t).index,(m z t).retained)

/-- Shrinking support consumes an entire block of phase/mode ranks. -/
def generatedSegmentRank (L : ℕ) (z : Unit × FlatStack (State × Action) State) (t : ℕ) : ℕ :=
  2*((B₀.card-(b z t).card)*L+(m z t).index)+modeBit (m z t).retained

theorem runSupport_step_subset (z : Unit × FlatStack (State × Action) State) (t : ℕ) :
    b z (t+1) ⊆ b z t := by
  rw [runSupport_succ]
  exact Finset.filter_subset _ _

/-- Once operation begins within an unchanged phase, the exact component
persists; before then the only possible mode change is navigation to operation. -/
theorem generated_mode_step (z : Unit × FlatStack (State × Action) State) (t : ℕ)
    (hb : b z (t+1)=b z t) (hi : (m z (t+1)).index=(m z t).index) :
    modeBit (m z t).retained ≤ modeBit (m z (t+1)).retained ∧
      ((m z (t+1)).retained≠(m z t).retained →
        modeBit (m z t).retained < modeBit (m z (t+1)).retained) := by
  cases he : (m z t).retained with
  | none =>
      cases hn : (m z (t+1)).retained <;> simp [he,hn,modeBit]
  | some E =>
      have hn := run_constant_phase_mode_persists P menu priority B₀ s₀ fallback fallbackAction reject z t hb hi E he
      simp [he,hn,modeBit]

/-- Every literal segment boundary strictly increases the bounded rank. -/
theorem generated_rank_step (L : ℕ) (z : Unit × FlatStack (State × Action) State) (t : ℕ)
    (hlo : (m z t).index<L) :
    generatedSegmentRank P menu priority B₀ s₀ fallback fallbackAction reject L z t ≤
      generatedSegmentRank P menu priority B₀ s₀ fallback fallbackAction reject L z (t+1) ∧
    (generatedSegmentLabel P menu priority B₀ s₀ fallback fallbackAction reject z (t+1)≠
      generatedSegmentLabel P menu priority B₀ s₀ fallback fallbackAction reject z t →
      generatedSegmentRank P menu priority B₀ s₀ fallback fallbackAction reject L z t <
      generatedSegmentRank P menu priority B₀ s₀ fallback fallbackAction reject L z (t+1)) := by
  have hm0 := modeBit_le_one (m z t).retained
  have hm1 := modeBit_le_one (m z (t+1)).retained
  have hc0 : (b z t).card≤B₀.card := Finset.card_le_card (liveHistory_subset P B₀ _)
  have hc1 : (b z (t+1)).card≤B₀.card := Finset.card_le_card (liveHistory_subset P B₀ _)
  by_cases hb : b z (t+1)=b z t
  · have hi := run_phase_increment_cases P menu priority B₀ s₀ fallback fallbackAction reject z t hb
    rcases hi with hi | hi
    · have hm := generated_mode_step P menu priority B₀ s₀ fallback fallbackAction reject z t hb hi
      constructor
      · dsimp [generatedSegmentRank]
        rw [hb,hi]
        omega
      · intro hne
        have hr : (m z (t+1)).retained≠(m z t).retained := by
          intro he
          apply hne
          simp only [generatedSegmentLabel,hb,hi,he]
        have hs := hm.2 hr
        dsimp [generatedSegmentRank]
        rw [hb,hi]
        omega
    · constructor <;> dsimp [generatedSegmentRank] <;> rw [hb,hi] <;> omega
  · have hs : b z (t+1) ⊂ b z t := Finset.ssubset_iff_subset_ne.mpr
        ⟨runSupport_step_subset P menu priority B₀ s₀ fallback fallbackAction reject z t,hb⟩
    have hcard := Finset.card_lt_card hs
    have hd : B₀.card-(b z t).card+1≤B₀.card-(b z (t+1)).card := by omega
    have hprod := Nat.mul_le_mul_right L hd
    rw [Nat.add_mul,Nat.one_mul] at hprod
    dsimp [generatedSegmentRank]
    constructor <;> omega

/-- Positive true support supplies at most |B₀| support-rank blocks. -/
theorem generated_rank_lt (L : ℕ) (z : Unit × FlatStack (State × Action) State) (t : ℕ)
    (hlo : (m z t).index < L) (hlive : (b z t).Nonempty) :
    generatedSegmentRank P menu priority B₀ s₀ fallback fallbackAction reject L z t < 2*B₀.card*L := by
  have hc : (b z t).card≤B₀.card := Finset.card_le_card (liveHistory_subset P B₀ _)
  have hp : 0 < (b z t).card := Finset.card_pos.mpr hlive
  have hd : B₀.card-(b z t).card+1≤B₀.card := by omega
  have hprod := Nat.mul_le_mul_right L hd
  rw [Nat.add_mul,Nat.one_mul] at hprod
  have hm := modeBit_le_one (m z t).retained
  dsimp [generatedSegmentRank]
  rw [Nat.mul_assoc]
  omega

/-- The exact source label, rather than an assumed abstract episode schedule,
has at most 2|B₀|L segments in every bounded-index finite actual prefix. -/
theorem generated_segment_budget (L T : ℕ) (z : Unit × FlatStack (State × Action) State)
    (hlo : ∀ t, t<T → (m z t).index<L)
    (hlive : ∀ t, t<T → (b z t).Nonempty) :
    (segmentStarts (generatedSegmentLabel P menu priority B₀ s₀ fallback fallbackAction reject z) T).card
      ≤ 2*B₀.card*L := by
  classical
  apply segmentStarts_card_le _
    (generatedSegmentRank P menu priority B₀ s₀ fallback fallbackAction reject L z) T
  · intro i j hij hj
    induction j,hij using Nat.le_induction with
    | base => exact le_rfl
    | succ j hij ih =>
        have hp := generated_rank_step P menu priority B₀ s₀ fallback fallbackAction reject L z j
          (hlo j (by omega))
        exact (ih (by omega)).trans hp.1
  · intro t ht hc
    exact (generated_rank_step P menu priority B₀ s₀ fallback fallbackAction reject L z t
      (hlo t (by omega))).2 hc
  · intro t ht
    exact generated_rank_lt P menu priority B₀ s₀ fallback fallbackAction reject L z t (hlo t ht) (hlive t ht)

/-- Endpoint version of the same exact generated segment budget. -/
theorem generated_segment_end_budget (L T : ℕ) (z : Unit × FlatStack (State × Action) State)
    (hlo : ∀ t, t<T → (m z t).index<L)
    (hlive : ∀ t, t<T → (b z t).Nonempty) :
    (segmentEnds (generatedSegmentLabel P menu priority B₀ s₀ fallback fallbackAction reject z) T).card
      ≤ 2*B₀.card*L := by
  classical
  apply segmentEnds_card_le _
    (generatedSegmentRank P menu priority B₀ s₀ fallback fallbackAction reject L z) T
  · intro i j hij hj
    induction j,hij using Nat.le_induction with
    | base => exact le_rfl
    | succ j hij ih =>
        exact (ih (by omega)).trans (generated_rank_step P menu priority B₀ s₀ fallback fallbackAction reject
          L z j (hlo j (by omega))).1
  · intro t ht hc
    exact (generated_rank_step P menu priority B₀ s₀ fallback fallbackAction reject L z t
      (hlo t (by omega))).2 hc
  · intro t ht
    exact generated_rank_lt P menu priority B₀ s₀ fallback fallbackAction reject L z t (hlo t ht) (hlive t ht)

/-- Source-bound accurate-prefix segment count. This includes the first segment,
proper support resets, candidate increments, target entry, and exact retained
component changes. It can be applied to every deterministic truncation before
the first inaccurate completed history. -/
theorem accurate_generated_segment_budget
    (ε η : ℝ) (hη : η≤ε) (N T : ℕ)
    (hs₀ : s₀∈winningRegion P menu priority B₀) (σ : Model) (hσ : σ∈B₀)
    (z : Unit × FlatStack (State × Action) State)
    (hSupported : ∀ e k, 0<realRows P σ e (z.2 (e,k)))
    (hAcc : ∀ t, t<T → HistoryAccurate P σ η N
      (runHistory P menu priority B₀ s₀ fallback fallbackAction (empiricalReject P ε) z t)) :
    (segmentStarts
      (generatedSegmentLabel P menu priority B₀ s₀ fallback fallbackAction (empiricalReject P ε) z) T).card
      ≤ 2*B₀.card*(N+B₀.card) := by
  apply generated_segment_budget
  · intro t ht
    exact generated_index_bounded_of_accurate P menu priority B₀ s₀ fallback fallbackAction ε η hη N t
      hs₀ σ hσ z hSupported (by intro i hi;exact hAcc i (by omega))
  · intro t ht
    exact ⟨σ,(run_invariant P menu priority B₀ s₀ fallback fallbackAction (empiricalReject P ε)
      hs₀ σ hσ z hSupported t).1⟩

end HiddenParity.Cost
