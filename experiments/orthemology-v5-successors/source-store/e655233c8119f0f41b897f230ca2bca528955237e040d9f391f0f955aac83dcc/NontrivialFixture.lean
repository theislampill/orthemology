import SelectorCertificateConstruction
import FullControllerCanonicalLaw
set_option autoImplicit false

noncomputable section
namespace Orthemology.Eighth.SemanticControls
open HiddenParity HiddenParity.Sufficiency HiddenParity.Necessity HiddenParity.Stage HiddenParity.Stochastic
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.RuntimeBridge
open Orthemology.RuntimeBridge.PhaseUpdate.FullController

abbrev fixtureKernel := Controller.Fixture.kernel
def bothMenu (_ : Finset Bool) (_ : Bool) : Finset Bool := Finset.univ
def actionPriority (θ : Bool) (e : Bool × Bool) : ℕ := if e.2 = θ then 2 else 1
def goodPairs (θ : Bool) : Finset (Bool × Bool) := Finset.univ.filter (fun e => e.2 = θ)

@[simp] theorem mem_goodPairs (θ : Bool) (e : Bool × Bool) : e ∈ goodPairs θ ↔ e.2 = θ := by
  simp [goodPairs]

theorem fixture_positive (θ : Bool) (e : Bool × Bool) (y : Bool) : 0 < fixtureKernel.row θ e y := by
  rcases e with ⟨s,a⟩
  cases θ <;> cases s <;> cases a <;> cases y <;> norm_num [fixtureKernel,Controller.Fixture.kernel]

@[simp] theorem fixture_internal (B : Finset Bool) (e : Bool × Bool) :
    internalSuccessors fixtureKernel B e = Finset.univ := by
  ext y
  simp [fixture_positive]

@[simp] theorem fixture_liveUpdate (B : Finset Bool) (e : Bool × Bool) (y : Bool) :
    liveUpdate fixtureKernel B e y = B := by
  ext θ
  simp [fixture_positive]

@[simp] theorem fixture_liveHistory (B : Finset Bool) (h : History (Bool × Bool) Bool) :
    liveHistory fixtureKernel B h = B := by
  ext θ
  simp [fixture_positive]

@[simp] theorem goodPairs_states (θ : Bool) : usedStates Prod.fst (goodPairs θ) = Finset.univ := by
  ext s
  simp only [usedStates,Finset.mem_image,mem_goodPairs,Finset.mem_univ,iff_true]
  exact ⟨(s,θ),rfl,rfl⟩

theorem goodPairs_component (B : Finset Bool) (θ : Bool) :
    IsEndComponent Prod.fst (internalSuccessors fixtureKernel B) (goodPairs θ) := by
  refine ⟨⟨(false,θ),by simp⟩,?_,?_,?_⟩
  · intro e he; simp
  · intro e he; simp
  · intro s hs t ht
    exact Relation.ReflTransGen.single ⟨(s,θ),by simp,rfl,by simp⟩

theorem fixture_match_eq (θ σ : Bool) (E : Finset (Bool × Bool)) (hE : E.Nonempty)
    (h : Match fixtureKernel.row θ σ E) : σ = θ := by
  obtain ⟨e,he⟩ := hE
  have hh := congrFun (h e he) true
  rcases e with ⟨s,a⟩
  cases θ <;> cases σ <;> cases s <;> cases a <;>
    norm_num [fixtureKernel,Controller.Fixture.kernel] at hh ⊢

theorem goodPairs_qualifying (B : Finset Bool) (θ : Bool) :
    MarkovQualifying fixtureKernel Prod.fst B actionPriority θ Finset.univ (goodPairs θ) := by
  refine ⟨Finset.subset_univ _,?_,goodPairs_component B θ,?_⟩
  · intro e he y hy; simp
  · intro σ hσ hm
    have hsame := fixture_match_eq θ σ _ ⟨(false,θ),by simp⟩ hm
    subst σ
    refine ⟨2,⟨⟨(false,θ),by simp,(by simp [actionPriority])⟩,?_⟩,by decide⟩
    intro e he
    simp [actionPriority,(mem_goodPairs θ e).mp he]

theorem qualifying_unique (B : Finset Bool) (θ : Bool) (hθ : θ ∈ B)
    (E : Finset (Bool × Bool))
    (hE : MarkovQualifying fixtureKernel Prod.fst B actionPriority θ Finset.univ E) :
    E = goodPairs θ := by
  obtain ⟨d,⟨⟨f,hf,hfd⟩,hmin⟩,hd⟩ := hE.2.2.2 θ hθ (fun _ _ => rfl)
  have hd2 : d = 2 := by
    unfold actionPriority at hfd
    split_ifs at hfd <;> omega
  have hsub : E ⊆ goodPairs θ := by
    intro e he
    have hh := hmin e he
    rw [hd2] at hh
    by_contra hnot
    have ha : e.2 ≠ θ := by simpa using hnot
    simp [actionPriority,ha] at hh
  apply Finset.Subset.antisymm hsub
  intro e he
  obtain ⟨f,hf⟩ := hE.2.2.1.nonempty
  have hs : e.1 ∈ usedStates Prod.fst E := hE.2.2.1.closed f hf (by simp)
  obtain ⟨g,hg,hgs⟩ := Finset.mem_image.mp hs
  have hga := (mem_goodPairs θ g).mp (hsub hg)
  have hea := (mem_goodPairs θ e).mp he
  have hge : g = e := Prod.ext hgs (hga.trans hea.symm)
  simpa [hge] using hg

@[simp] theorem fixture_regionAllowed_univ (B : Finset Bool) (lower : Finset Bool → Finset Bool) :
    regionAllowed fixtureKernel bothMenu B lower Finset.univ = Finset.univ := by
  ext e
  simp [mem_regionAllowed,bothMenu]

theorem fixture_target_all (B : Finset Bool) (θ s : Bool) :
    s ∈ markovTargetStates fixtureKernel Prod.fst B actionPriority θ Finset.univ := by
  apply (markovTargetStates_exact _ _ _ _ _ _ _).mpr
  exact ⟨goodPairs θ,goodPairs_qualifying B θ,by simp⟩

@[simp] theorem fixture_regionStep_univ (B : Finset Bool) (lower : Finset Bool → Finset Bool) :
    regionStep fixtureKernel bothMenu actionPriority B lower Finset.univ = Finset.univ := by
  ext s
  simp only [mem_regionStep,Finset.mem_univ,true_and,iff_true,fixture_regionAllowed_univ]
  intro θ hθ
  exact Or.inr ⟨s,fixture_target_all B θ s,Relation.ReflTransGen.refl⟩

@[simp] theorem fixture_computedRegion (n : ℕ) (B : Finset Bool) (hB : B.Nonempty) :
    computedRegion fixtureKernel bothMenu actionPriority (n+1) B = Finset.univ := by
  rw [computedRegion,if_pos hB]
  simp only [Fintype.card_bool,descend,fixture_regionStep_univ]

@[simp] theorem fixture_winningRegion (B : Finset Bool) (hB : B.Nonempty) :
    winningRegion fixtureKernel bothMenu actionPriority B = Finset.univ := by
  obtain ⟨n,hn⟩ := Nat.exists_eq_succ_of_ne_zero (Finset.card_ne_zero.mpr hB)
  rw [winningRegion,hn]
  exact fixture_computedRegion n B hB

@[simp] theorem fixture_stageActions (B : Finset Bool) (hB : B.Nonempty) :
    stageActions fixtureKernel bothMenu actionPriority B = Finset.univ := by
  rw [stageActions,fixture_winningRegion B hB,fixture_regionAllowed_univ]

@[simp] theorem fixture_stageTargets (B : Finset Bool) (hB : B.Nonempty) (θ : Bool) :
    stageTargets fixtureKernel bothMenu actionPriority B θ = Finset.univ := by
  ext s
  simp only [stageTargets,fixture_stageActions B hB,Finset.mem_univ,iff_true]
  exact fixture_target_all B θ s

theorem fixture_chooseTarget (B : Finset Bool) (θ : Bool) (hθ : θ ∈ B) (s : Bool) :
    chooseTarget fixtureKernel bothMenu actionPriority B θ s = goodPairs θ := by
  have hh := chooseTarget_spec fixtureKernel bothMenu actionPriority B θ s
    (by rw [fixture_stageTargets B ⟨θ,hθ⟩];simp)
  apply qualifying_unique B θ hθ
  simpa only [fixture_stageActions B ⟨θ,hθ⟩] using hh.1

end Orthemology.Eighth.SemanticControls

namespace Orthemology.Eighth.SemanticControls
open HiddenParity HiddenParity.Sufficiency HiddenParity.Necessity HiddenParity.Stage HiddenParity.Stochastic
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.RuntimeBridge
open Orthemology.RuntimeBridge.PhaseUpdate.FullController

/-- Every empirical frequency lies in the unit interval, including empty cells. -/
theorem frequency_bounds (e : Bool × Bool) (y : Bool) (h : History (Bool × Bool) Bool) :
    0 ≤ RationalGate.frequency e y h ∧ RationalGate.frequency e y h ≤ 1 := by
  have hcount : RationalGate.symbolCount e y h ≤ actionCount e h := by
    apply List.countP_mono_left
    intro z hz
    simp only [Bool.decide_and, Bool.and_eq_true, decide_eq_true_eq]
    exact And.left
  constructor
  · unfold RationalGate.frequency; positivity
  · unfold RationalGate.frequency
    by_cases hz : actionCount e h = 0
    · simp [hz]
    · apply (div_le_one (by exact_mod_cast Nat.pos_of_ne_zero hz : (0:ℚ) < actionCount e h)).mpr
      exact_mod_cast hcount

theorem fixture_row_le_one (θ : Bool) (e : Bool × Bool) (y : Bool) : fixtureKernel.row θ e y ≤ 1 := by
  rcases e with ⟨s,a⟩
  cases θ <;> cases s <;> cases a <;> cases y <;> norm_num [fixtureKernel,Controller.Fixture.kernel]

@[simp] theorem reject_two_false (θ : Bool) (k : ℕ) (h : History (Bool × Bool) Bool) :
    RationalGate.reject fixtureKernel 2 θ k h = false := by
  simp only [RationalGate.reject,decide_eq_false_iff_not]
  rintro ⟨e,y,hk,hd⟩
  have hf := frequency_bounds e y h
  have hp := fixture_positive θ e y
  have hq := fixture_row_le_one θ e y
  have hb : |RationalGate.frequency e y h - fixtureKernel.row θ e y| ≤ 1 := by
    apply abs_le.mpr
    constructor <;> linarith
  linarith

/-- The fixed actual model is chosen once from the retained cycle, outside all tape quantifiers. -/
noncomputable def initialCandidate : Bool := cycleAction (Finset.univ : Finset Bool) false 0

theorem normalize_initial (s : Bool) :
    normalizeMemory fixtureKernel bothMenu actionPriority false Finset.univ s
      (⟨0,none⟩ : PhaseMemory Bool Bool) = ⟨0,some (goodPairs initialCandidate)⟩ := by
  simp only [normalizeMemory,phaseCandidate,initialCandidate]
  rw [if_pos (by rw [fixture_stageTargets _ Finset.univ_nonempty];simp)]
  rw [fixture_chooseTarget _ _ (Finset.mem_univ _) s]

theorem normalize_retained_initial (s : Bool) :
    normalizeMemory fixtureKernel bothMenu actionPriority false Finset.univ s
      (⟨0,some (goodPairs initialCandidate)⟩ : PhaseMemory Bool Bool) =
        ⟨0,some (goodPairs initialCandidate)⟩ := rfl

theorem old_currentMemory (h : History Bool Bool) :
    currentMemory fixtureKernel bothMenu actionPriority Finset.univ false false
      (RationalGate.reject fixtureKernel 2) h = ⟨0,some (goodPairs initialCandidate)⟩ := by
  have hm : ∀ h : History Bool Bool,
      phaseMemory fixtureKernel bothMenu actionPriority Finset.univ false false
        (RationalGate.reject fixtureKernel 2) h =
          if h = [] then ⟨0,none⟩ else ⟨0,some (goodPairs initialCandidate)⟩ := by
    intro h
    induction h with
    | nil => rfl
    | cons ay h ih =>
      rcases ay with ⟨a,y⟩
      rw [phaseMemory,ih]
      simp only [fixture_liveHistory,reject_two_false]
      by_cases hh : h = []
      · subst h
        simp only [if_pos rfl,normalize_initial,advanceMemory,ne_eq,not_true_eq_false,
          Bool.false_eq_true,↓reduceIte,goodPairs_states,Finset.mem_univ,List.cons_ne_self]
      · simp only [if_neg hh,normalize_retained_initial,advanceMemory,ne_eq,not_true_eq_false,
          Bool.false_eq_true,↓reduceIte,goodPairs_states,Finset.mem_univ,List.cons_ne_nil]
  unfold currentMemory
  rw [fixture_liveHistory,hm]
  by_cases hh : h = []
  · rw [if_pos hh,normalize_initial]
  · rw [if_neg hh,normalize_retained_initial]

@[simp] theorem retainedActions_good (θ s : Bool) : retainedActions (goodPairs θ) s = {θ} := by
  ext a
  simp

theorem cycle_singleton (θ fallback : Bool) (n : ℕ) : cycleAction {θ} fallback n = θ := by
  exact Finset.mem_singleton.mp (cycleAction_mem {θ} fallback (Finset.singleton_nonempty _) n)

theorem old_generated_constant (h : History Bool Bool) :
    generatedPhasePolicy fixtureKernel bothMenu actionPriority Finset.univ false false false
      (RationalGate.reject fixtureKernel 2) () h = initialCandidate := by
  unfold generatedPhasePolicy
  rw [fixture_liveHistory,old_currentMemory]
  simp only [activePairs,Option.getD_some,retainedActions_good,cycle_singleton]

noncomputable def oldConfig : Config where
  selectors := certifiedData fixtureKernel bothMenu actionPriority
  kernel := fixtureKernel
  toleranceNumerator := 2
  toleranceDenominator := 1
  rowDenominator := 3
  rowNumerator θ e y := if y then (if e.2 = θ then 1 else 2) else (if e.2 = θ then 2 else 1)
  initialSupport := Finset.univ
  initialState := false
  fallbackModel := false
  fallbackAction := false

theorem oldConfig_certificate : Certificate oldConfig bothMenu actionPriority := by
  refine ⟨certifiedData_certificate _ _ _,by decide,by decide,?_⟩
  intro θ e y
  rcases e with ⟨s,a⟩
  cases θ <;> cases s <;> cases a <;> cases y <;>
    norm_num [oldConfig,fixtureKernel,Controller.Fixture.kernel]

theorem oldConfig_winning : oldConfig.initialState ∈
    winningRegion oldConfig.kernel bothMenu actionPriority oldConfig.initialSupport := by
  change false ∈ winningRegion fixtureKernel bothMenu actionPriority Finset.univ
  rw [fixture_winningRegion _ Finset.univ_nonempty]
  simp

theorem old_policy_constant (h : History Bool Bool) :
    policy oldConfig bothMenu actionPriority h = initialCandidate := by
  change generatedPhasePolicy fixtureKernel bothMenu actionPriority Finset.univ false false false
    (RationalGate.reject fixtureKernel ((2:ℚ)/1)) () h = initialCandidate
  simpa only [div_one] using old_generated_constant h

theorem old_source_constant (h : History Bool Bool) :
    HistoryRuntime.historyPolicy (sourcePolicy oldConfig) () h = initialCandidate := by
  rw [HistoryRuntime.historyPolicy,source_policy_retained_exact oldConfig bothMenu actionPriority oldConfig_certificate]
  exact old_policy_constant h

end Orthemology.Eighth.SemanticControls
