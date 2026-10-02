import GlobalParitySufficiency

noncomputable section
open MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
namespace HiddenParity.Cost
open HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Empirical
open HiddenParity.Adaptive HiddenParity.Necessity HiddenParity.Stage
universe u w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action] [Inhabited State]
variable [DecidableEq Model]

omit [DecidableEq State] [DecidableEq Action] [Inhabited State] [DecidableEq Model] in
/-- Uniform positive slack for the actual chosen tolerance. The hypothesis is
some-coordinate separation of each unequal row, not separation at every
coordinate. -/
theorem finite_test_margin (P : RationalKernel Model (State × Action) State)
    (B : Finset Model) (σ : Model) (ε : ℝ) (hε : 0 < ε)
    (hSep : ∀ θ ∈ B, ∀ e, P.row θ e ≠ P.row σ e →
      ∃ y, ε < |realRows P σ e y - realRows P θ e y|) :
    ∃ η : ℝ, 0 < η ∧ η < ε ∧ ∀ θ ∈ B, ∀ e, P.row θ e ≠ P.row σ e →
      ∃ y, ε + η < |realRows P σ e y - realRows P θ e y| := by
  classical
  let gaps : Finset ℝ := (B ×ˢ (Finset.univ : Finset (State × Action)) ×ˢ
    (Finset.univ : Finset State)).image (fun z =>
      |realRows P σ z.2.1 z.2.2 - realRows P z.1 z.2.1 z.2.2| - ε)
  let positive := gaps.filter (fun t => 0 < t)
  by_cases hp : positive.Nonempty
  · let η := min ε (positive.min' hp) / 2
    have hmin : 0 < positive.min' hp := (Finset.mem_filter.mp (Finset.min'_mem positive hp)).2
    have hηpos : 0 < η := by dsimp [η]; positivity
    have hηε : η < ε := by dsimp [η]; have := min_le_left ε (positive.min' hp); linarith
    refine ⟨η,hηpos,hηε,?_⟩
    intro θ hθ e hNe
    obtain ⟨y,hy⟩ := hSep θ hθ e hNe
    have hg : |realRows P σ e y - realRows P θ e y| - ε ∈ positive := by
      apply Finset.mem_filter.mpr
      refine ⟨?_,by linarith⟩
      exact Finset.mem_image.mpr ⟨(θ,e,y),by simp [hθ],rfl⟩
    have hle := Finset.min'_le positive _ hg
    have hη := min_le_right ε (positive.min' hp)
    refine ⟨y,?_⟩
    dsimp [η] at *
    linarith
  · refine ⟨ε/2,by positivity,by linarith,?_⟩
    intro θ hθ e hNe
    obtain ⟨y,hy⟩ := hSep θ hθ e hNe
    exfalso
    apply hp
    refine ⟨|realRows P σ e y - realRows P θ e y| - ε,?_⟩
    apply Finset.mem_filter.mpr
    refine ⟨?_,by linarith⟩
    exact Finset.mem_image.mpr ⟨(θ,e,y),by simp [hθ],rfl⟩

/-- Accuracy only of acquired row prefixes above the fixed threshold. It uses
σ for analysis, so it is not an implementable common-controller predicate. -/
def HistoryAccurate (P : RationalKernel Model (State × Action) State) (σ : Model)
    (η : ℝ) (N : ℕ) (h : History (State × Action) State) : Prop :=
  ∀ e y, N ≤ actionCount e h → |historyFrequency e y h - realRows P σ e y| < η

theorem true_test_false_of_accurate (P : RationalKernel Model (State × Action) State)
    (σ : Model) (ε η : ℝ) (hη : η ≤ ε) (N k : ℕ) (hNk : N ≤ k)
    (h : History (State × Action) State) (ha : HistoryAccurate P σ η N h) :
    empiricalReject P ε σ k h = false := by
  by_contra hn
  have ht : empiricalReject P ε σ k h = true := by
    cases he : empiricalReject P ε σ k h <;> simp_all
  obtain ⟨e,y,hc,hbad⟩ := (empiricalReject_iff P ε σ k h).mp ht
  have hg := ha e y (by omega)
  linarith

theorem mismatch_test_true_of_accurate (P : RationalKernel Model (State × Action) State)
    (σ θ : Model) (ε η : ℝ) (N k : ℕ) (h : History (State × Action) State)
    (ha : HistoryAccurate P σ η N h) (e : State × Action) (y : State)
    (hc : N ≤ actionCount e h) (hk : k < actionCount e h)
    (hgap : ε + η ≤ |realRows P σ e y - realRows P θ e y|) :
    empiricalReject P ε θ k h = true := by
  apply (empiricalReject_iff P ε θ k h).mpr
  refine ⟨e,y,hk,?_⟩
  have htrue := ha e y hc
  have htri := abs_sub_le (realRows P σ e y) (historyFrequency e y h) (realRows P θ e y)
  rw [abs_sub_comm (realRows P σ e y) (historyFrequency e y h)] at htri
  linarith

/-- Sharpen the predecessor's unbounded cyclic witness to a barrier in the next
cardinality-many indices. This works for the exact Fintype.equivFin cycle. -/
theorem exists_near_cycle_barrier (B : Finset Model) (fallback σ : Model)
    (hσ : σ ∈ B) (N : ℕ) :
    ∃ j, N ≤ j ∧ j < N + B.card ∧ cycleAction B fallback j = σ := by
  let i : B := ⟨σ,hσ⟩
  let d := Fintype.card B
  let q := N / d
  let r := N % d
  let k := (Fintype.equivFin B i).val
  have hd : 0 < d := by simpa [d] using Finset.card_pos.mpr (show B.Nonempty from ⟨σ,hσ⟩)
  have hk : k < d := (Fintype.equivFin B i).isLt
  have hr : r < d := Nat.mod_lt N hd
  have hN : q*d+r=N := by simpa [Nat.mul_comm] using Nat.div_add_mod N d
  have hcard : d = B.card := Fintype.card_coe B
  by_cases hle : r ≤ k
  · refine ⟨q*d+k,by omega,by omega,?_⟩
    exact cycleAction_at_index B fallback i q
  · refine ⟨(q+1)*d+k,?_,?_,?_⟩
    · nlinarith
    · nlinarith
    · exact cycleAction_at_index B fallback i (q+1)

/-- A chosen *analysis barrier*, distinct from the controller's memory. -/
def nearBarrier (B : Finset Model) (fallback σ : Model) (N : ℕ) : ℕ :=
  if hσ : σ ∈ B then Classical.choose (exists_near_cycle_barrier B fallback σ hσ N) else 0

theorem nearBarrier_spec (B : Finset Model) (fallback σ : Model) (N : ℕ) (hσ : σ ∈ B) :
    N ≤ nearBarrier B fallback σ N ∧ nearBarrier B fallback σ N < N + B.card ∧
      cycleAction B fallback (nearBarrier B fallback σ N) = σ := by
  simp only [nearBarrier,dif_pos hσ]
  exact Classical.choose_spec (exists_near_cycle_barrier B fallback σ hσ N)

variable [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- An actual generated-run bound, valid at every finite prefix whose acquired
statistics above N remain accurate. Resets are handled at their literal source
branch; no eventual support-stability or fresh restart samples are assumed. -/
theorem generated_index_bounded_of_accurate
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B₀ : Finset Model) (s₀ : State) (fallback : Model) (fallbackAction : Action)
    (ε η : ℝ) (hη : η ≤ ε) (N T : ℕ)
    (hs₀ : s₀ ∈ winningRegion P menu priority B₀) (σ : Model) (hσ : σ ∈ B₀)
    (z : Unit × FlatStack (State × Action) State)
    (hSupported : ∀ e k, 0 < realRows P σ e (z.2 (e,k)))
    (hAcc : ∀ t, t ≤ T → HistoryAccurate P σ η N
      (runHistory P menu priority B₀ s₀ fallback fallbackAction (empiricalReject P ε) z t)) :
    (runMemory P menu priority B₀ s₀ fallback fallbackAction (empiricalReject P ε) z T).index
      < N + B₀.card := by
  let reject := empiricalReject P ε
  let b := runSupport P menu priority B₀ s₀ fallback fallbackAction reject z
  let m := runMemory P menu priority B₀ s₀ fallback fallbackAction reject z
  have hmem : ∀ t, σ ∈ b t := by
    intro t
    exact (run_invariant P menu priority B₀ s₀ fallback fallbackAction reject hs₀ σ hσ z hSupported t).1
  have hbound : ∀ t, t ≤ T → (m t).index ≤ nearBarrier (b t) fallback σ N := by
    intro t
    induction t with
    | zero =>
        intro _
        change (currentMemory P menu priority B₀ s₀ fallback reject []).index ≤ _
        unfold currentMemory
        rw [normalizeMemory_index]
        change 0 ≤ _
        omega
    | succ t ih =>
        intro ht
        have hi := ih (by omega)
        by_cases hb : b (t+1) = b t
        · have hStep := run_phase_increment_cases P menu priority B₀ s₀ fallback fallbackAction reject z t hb
          have hBar := nearBarrier_spec (b t) fallback σ N (hmem t)
          by_cases heq : (m t).index = nearBarrier (b t) fallback σ N
          · have hTrue : phaseCandidate (b t) fallback (m t) = σ := by
              simpa only [phaseCandidate,heq] using hBar.2.2
            have hTest : reject σ (m t).index
                (runHistory P menu priority B₀ s₀ fallback fallbackAction reject z (t+1)) = false :=
              true_test_false_of_accurate P σ ε η hη N (m t).index (by omega) _ (hAcc (t+1) ht)
            have hStop := run_true_candidate_no_increment P menu priority B₀ s₀ fallback fallbackAction reject
              hs₀ σ hσ z hSupported t hb hTrue hTest
            change (m (t+1)).index = (m t).index at hStop
            rw [hb,hStop]
            exact hi
          · change (m (t+1)).index = (m t).index ∨ (m (t+1)).index = (m t).index+1 at hStep
            rw [hb]
            omega
        · have hZero : (m (t+1)).index = 0 := by
            dsimp [m]
            rw [runMemory_succ,normalizeMemory_index]
            change (advanceMemory (b t) (b (t+1)) _ (m t) _).index = 0
            simp only [advanceMemory,if_pos hb]
          rw [hZero]
          omega
  have hLast := hbound T le_rfl
  have hBar := nearBarrier_spec (b T) fallback σ N (hmem T)
  have hSub : b T ⊆ B₀ := liveHistory_subset P B₀ _
  have hCard := Finset.card_le_card hSub
  change (m T).index < N + B₀.card
  omega

end HiddenParity.Cost
