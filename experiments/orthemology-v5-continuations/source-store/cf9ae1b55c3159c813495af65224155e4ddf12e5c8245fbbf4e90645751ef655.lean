import RecursiveCausalPolicy

noncomputable section
set_option linter.unusedSectionVars false
open Finset
namespace Orthemology.Tranche3
open Orthemology.Tranche2 CausalTree
open Orthemology.Tranche2.PolicyEmbedding
universe u v
variable {Θ A Y : Type u} [Fintype Θ] [Fintype Y] [DecidableEq Θ] [DecidableEq A]
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)

/-- Exact public live support, computed from the actually acquired transcript. -/
def historySupport (B₀ : Finset Θ) : History A Y → Finset Θ
  | [] => B₀
  | (a,y)::h => supportUpdate P (historySupport B₀ h) a y

/-- At each physical node, the action is licensed by the support BEFORE its
observation. Positive observation edges update that exact support. -/
def LicensedTree (θ : Θ) : Finset Θ → ActionTree A Y (RecursiveMacroState P good menu) → Prop
  | B, .leaf s => recursiveMacroValid P good menu θ s ∧ s.1.val = B
  | B, .node a k => a ∈ menu B ∧ ∀ y, 0 < P θ a y →
      LicensedTree θ (supportUpdate P B a y) (k y)

omit [Fintype Θ] [Fintype Y] [DecidableEq Θ] [DecidableEq A] in
lemma stoppedSupport_complete (B : Finset Θ) (acts : List A) (w : StopObs Y acts.length)
    (hw : stopCompleted w = true) : stoppedSupport P B acts w = B := by
  induction acts with
  | nil => rfl
  | cons a as ih =>
    rcases w with y | ⟨y,w⟩
    · simp [stopCompleted] at hw
    · exact ih w hw

omit [Fintype Θ] [Fintype Y] in
/-- The first-exit physical tree obeys every intermediate menu, not only the
menu at a completed-record boundary. -/
theorem stopTree_licensed (θ : Θ) (B : Finset Θ) (acts : List A)
    (finish : StopObs Y acts.length → RecursiveMacroState P good menu)
    (hm : acts.toFinset ⊆ menu B)
    (hf : ∀ w, 0 < stoppedMass (P θ) (supportStay P B) acts w →
      recursiveMacroValid P good menu θ (finish w) ∧
        (finish w).1.val = stoppedSupport P B acts w) :
    LicensedTree P good menu θ B (stopTree (supportStay P B) acts finish) := by
  induction acts with
  | nil => exact hf PUnit.unit (by simp [stoppedMass])
  | cons a as ih =>
    constructor
    · exact hm (by simp)
    · intro y hy
      cases hs : supportStay P B a y
      · simp only [stopTree,hs,Bool.false_eq_true,↓reduceIte,LicensedTree]
        exact hf (Sum.inl y) (by simpa only [stoppedMass,hs,Bool.false_eq_true,↓reduceIte] using hy)
      · have hu : supportUpdate P B a y = B := by simpa [supportStay] using hs
        simp only [stopTree,hs,↓reduceIte,hu]
        apply ih
        · intro b hb
          exact hm (by simpa using Finset.mem_insert_of_mem hb)
        · intro w hw
          exact hf (Sum.inr (y,w)) (by simpa only [stoppedMass,hs,↓reduceIte] using mul_pos hy hw)

/-- Reset and completion leaves are linked to the literal support filter. -/
theorem recursiveSpawn_licensed
    (hP : ∀ θ a y, 0 ≤ P θ a y) (θ : Θ) (s : RecursiveMacroState P good menu)
    (hs : recursiveMacroValid P good menu θ s) :
    LicensedTree P good menu θ s.1.val
      (.node (recursiveSpawn P good menu s).1 (recursiveSpawn P good menu s).2) := by
  rw [recursiveSpawn_asTree]
  apply stopTree_licensed P good menu θ s.1.val
  · exact (phaseActs_spec P good menu s.1 _).2.1
  · intro w hw
    refine ⟨recursiveMacroValid_next P good menu hP θ s hs w hw,?_⟩
    rcases s with ⟨p,h⟩
    cases hk : recursiveKeep P good menu p (recursivePolicy P good menu p h) w
    · have hu : resetUpdate (recursiveKeep P good menu) (phaseNext P good menu) (recursivePolicy P good menu)
        ⟨p,h⟩ w = ⟨phaseNext P good menu p (recursivePolicy P good menu p h) w,[]⟩ := by simp [resetUpdate,hk]
      rw [hu]
      exact (phaseNext_actual_support P good menu hP θ p _ w hs.1 hk hw).1
    · have hu : resetUpdate (recursiveKeep P good menu) (phaseNext P good menu) (recursivePolicy P good menu)
        ⟨p,h⟩ w = ⟨p,⟨recursivePolicy P good menu p h,w⟩::h⟩ := by simp [resetUpdate,hk]
      rw [hu]
      exact (stoppedSupport_complete P p.val _ w hk).symm

/-- A one-step update always uses the observed support, including an immediate
reset after the exit-triggering action and before any formerly planned suffix. -/
theorem recursiveAdvance_licensed
    (hP : ∀ θ a y, 0 ≤ P θ a y) (θ : Θ) (B : Finset Θ)
    (s : NodeState A Y (RecursiveMacroState P good menu))
    (hs : LicensedTree P good menu θ B (.node s.1 s.2))
    (y : Y) (hy : 0 < P θ s.1 y) :
    LicensedTree P good menu θ (supportUpdate P B s.1 y)
      (.node (advance (recursiveSpawn P good menu) s y).1 (advance (recursiveSpawn P good menu) s y).2) := by
  have hh := hs.2 y hy
  cases hk : s.2 y with
  | leaf q =>
    have hq : recursiveMacroValid P good menu θ q ∧ q.1.val = supportUpdate P B s.1 y := by
      simpa only [hk,LicensedTree] using hh
    simpa only [advance,hk,hq.2] using recursiveSpawn_licensed P good menu hP θ q hq.1
  | node a k => simpa only [advance,hk] using hh

/-- The physical policy is licensed on every action-consistent history with a
nonempty true-model support, including all early target errors. -/
theorem recursiveHistoryPolicy_licensed_of_live
    {R : Type v} (hP : ∀ θ a y, 0 ≤ P θ a y) (p : WinningPhase P good menu)
    (r : R) (h : History A Y) (θ : Θ)
    (hc : ActionCompatible (recursiveHistoryPolicy (R := R) P good menu p) r h)
    (ht : θ ∈ historySupport P p.val h) :
    LicensedTree P good menu θ (historySupport P p.val h)
      (.node (replayObserved (recursiveSpawn P good menu) (recursiveSpawn P good menu ⟨p,[]⟩) h).1
        (replayObserved (recursiveSpawn P good menu) (recursiveSpawn P good menu ⟨p,[]⟩) h).2) := by
  induction h with
  | nil => exact recursiveSpawn_licensed P good menu hP θ ⟨p,[]⟩ ⟨ht,by simp [dHistoryMass]⟩
  | cons ay h ih =>
    rcases ay with ⟨a,y⟩
    obtain ⟨hc,ha⟩ := hc
    obtain ⟨ht,hy⟩ := (mem_supportUpdate P (historySupport P p.val h) a y θ).mp ht
    have hh := ih hc ht
    have he : (replayObserved (recursiveSpawn P good menu) (recursiveSpawn P good menu ⟨p,[]⟩) h).1 = a := ha
    simpa only [replayObserved,historySupport,he] using
      recursiveAdvance_licensed P good menu hP θ (historySupport P p.val h) _ hh y (by simpa only [he] using hy)

/-- Uniform public-menu safety for every feasible consistent history. There is
no requirement to produce a licensed action at impossible empty-support histories. -/
theorem recursiveHistoryPolicy_licensed
    {R : Type v} (hP : ∀ θ a y, 0 ≤ P θ a y) (p : WinningPhase P good menu)
    (r : R) (h : History A Y)
    (hc : ActionCompatible (recursiveHistoryPolicy (R := R) P good menu p) r h)
    (hne : (historySupport P p.val h).Nonempty) :
    recursiveHistoryPolicy P good menu p r h ∈ menu (historySupport P p.val h) := by
  obtain ⟨θ,ht⟩ := hne
  exact (recursiveHistoryPolicy_licensed_of_live P good menu hP p r h θ hc ht).1
end Orthemology.Tranche3
