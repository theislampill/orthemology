import LiteralSelectorObstruction
set_option autoImplicit false

noncomputable section
namespace Orthemology.Eighth.SemanticControls.LiteralAssessment
open HiddenParity HiddenParity.Sufficiency HiddenParity.Necessity HiddenParity.Stage HiddenParity.Stochastic
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.RuntimeBridge.PhaseUpdate
open Orthemology.RuntimeBridge.PhaseUpdate.FiniteSelectorSource

/-- Only singleton-support menus are restricted. Full-support operation retains both actions. -/
def sparseMenu (B : Finset Bool) (_ : Bool) : Finset Bool := if B.card = 1 then B else Finset.univ

def sparseAllowed (B : Finset Bool) : Finset (Bool × Bool) :=
  Finset.univ.filter (fun e => e.2 ∈ sparseMenu B e.1)

theorem member_sparseMenu (B : Finset Bool) (θ : Bool) (hθ : θ ∈ B) (s : Bool) :
    θ ∈ sparseMenu B s := by
  unfold sparseMenu
  split_ifs
  · exact hθ
  · simp

@[simp] theorem sparse_regionAllowed_univ (B : Finset Bool) (lower : Finset Bool → Finset Bool) :
    regionAllowed fixtureKernel sparseMenu B lower Finset.univ = sparseAllowed B := by
  ext e
  simp [mem_regionAllowed,sparseAllowed]

theorem sparse_good_qualifying (B : Finset Bool) (θ : Bool) (hθ : θ ∈ B) :
    MarkovQualifying fixtureKernel Prod.fst B actionPriority θ (sparseAllowed B) (goodPairs θ) := by
  refine ⟨?_,(goodPairs_qualifying B θ).2⟩
  intro e he
  simp only [sparseAllowed,Finset.mem_filter,Finset.mem_univ,true_and]
  rw [(mem_goodPairs θ e).mp he]
  exact member_sparseMenu B θ hθ e.1

@[simp] theorem sparse_regionStep_univ (B : Finset Bool) (lower : Finset Bool → Finset Bool) :
    regionStep fixtureKernel sparseMenu actionPriority B lower Finset.univ = Finset.univ := by
  ext s
  simp only [mem_regionStep,Finset.mem_univ,true_and,iff_true,sparse_regionAllowed_univ]
  intro θ hθ
  refine Or.inr ⟨s,?_,Relation.ReflTransGen.refl⟩
  exact (markovTargetStates_exact _ _ _ _ _ _ _).mpr
    ⟨goodPairs θ,sparse_good_qualifying B θ hθ,by simp⟩

@[simp] theorem sparse_computedRegion (n : ℕ) (B : Finset Bool) (hB : B.Nonempty) :
    computedRegion fixtureKernel sparseMenu actionPriority (n+1) B = Finset.univ := by
  rw [computedRegion,if_pos hB]
  simp only [Fintype.card_bool,descend,sparse_regionStep_univ]

@[simp] theorem sparse_winningRegion (B : Finset Bool) (hB : B.Nonempty) :
    winningRegion fixtureKernel sparseMenu actionPriority B = Finset.univ := by
  obtain ⟨n,hn⟩ := Nat.exists_eq_succ_of_ne_zero (Finset.card_ne_zero.mpr hB)
  rw [winningRegion,hn]
  exact sparse_computedRegion n B hB

@[simp] theorem sparse_stageActions (B : Finset Bool) (hB : B.Nonempty) :
    stageActions fixtureKernel sparseMenu actionPriority B = sparseAllowed B := by
  rw [stageActions,sparse_winningRegion B hB,sparse_regionAllowed_univ]

@[simp] theorem sparse_allowed_singleton (θ : Bool) : sparseAllowed {θ} = goodPairs θ := by
  ext e
  simp [sparseAllowed,sparseMenu]

@[simp] theorem sparse_allowed_full : sparseAllowed Finset.univ = Finset.univ := by
  ext e
  simp [sparseAllowed,sparseMenu]

@[simp] theorem sparse_stageActions_empty : stageActions fixtureKernel sparseMenu actionPriority ∅ = ∅ := by
  simp [stageActions,winningRegion,computedRegion,regionAllowed]

/-- Restricting the off-path menu removes the formerly nonunique target choices. -/
theorem component_within_good_unique (θ : Bool) (E : Finset (Bool × Bool))
    (hsub : E ⊆ goodPairs θ) (hE : IsEndComponent Prod.fst
      (internalSuccessors fixtureKernel {θ}) E) : E = goodPairs θ := by
  apply Finset.Subset.antisymm hsub
  intro e he
  obtain ⟨f,hf⟩ := hE.nonempty
  have hs : e.1 ∈ usedStates Prod.fst E := hE.closed f hf (by simp)
  obtain ⟨g,hg,hgs⟩ := Finset.mem_image.mp hs
  have hga := (mem_goodPairs θ g).mp (hsub hg)
  have hea := (mem_goodPairs θ e).mp he
  have hge : g = e := Prod.ext hgs (hga.trans hea.symm)
  simpa [hge] using hg

theorem sparse_singleton_qualifying (θ candidate : Bool) :
    MarkovQualifying fixtureKernel Prod.fst {θ} actionPriority candidate
      (goodPairs θ) (goodPairs θ) := by
  refine ⟨Finset.Subset.refl _,?_,goodPairs_component {θ} θ,?_⟩
  · intro e he y hy; simp
  · intro σ hσ hm
    have hs : σ = θ := Finset.mem_singleton.mp hσ
    subst σ
    have hc := fixture_match_eq candidate θ _ ⟨(false,θ),by simp⟩ hm
    subst candidate
    exact (goodPairs_qualifying {θ} θ).2.2.2 θ (by simp) (fun _ _ => rfl)

@[simp] theorem sparse_target_singleton (θ candidate s : Bool) :
    s ∈ stageTargets fixtureKernel sparseMenu actionPriority {θ} candidate := by
  unfold stageTargets
  rw [sparse_stageActions _ (Finset.singleton_nonempty _),sparse_allowed_singleton]
  exact (markovTargetStates_exact _ _ _ _ _ _ _).mpr
    ⟨goodPairs θ,sparse_singleton_qualifying θ candidate,by simp⟩

@[simp] theorem sparse_target_full (candidate s : Bool) :
    s ∈ stageTargets fixtureKernel sparseMenu actionPriority Finset.univ candidate := by
  unfold stageTargets
  rw [sparse_stageActions _ Finset.univ_nonempty,sparse_allowed_full]
  exact fixture_target_all _ _ _

theorem sparse_choose_singleton (θ candidate s : Bool) :
    chooseTarget fixtureKernel sparseMenu actionPriority {θ} candidate s = goodPairs θ := by
  have hh := chooseTarget_spec fixtureKernel sparseMenu actionPriority {θ} candidate s
    (sparse_target_singleton θ candidate s)
  have hs : chooseTarget fixtureKernel sparseMenu actionPriority {θ} candidate s ⊆ goodPairs θ := by
    simpa only [sparse_stageActions _ (Finset.singleton_nonempty _),sparse_allowed_singleton] using hh.1.1
  exact component_within_good_unique θ _ hs hh.1.2.2.1

theorem sparse_choose_full (candidate s : Bool) :
    chooseTarget fixtureKernel sparseMenu actionPriority Finset.univ candidate s = goodPairs candidate := by
  have hh := chooseTarget_spec fixtureKernel sparseMenu actionPriority Finset.univ candidate s
    (sparse_target_full candidate s)
  apply qualifying_unique Finset.univ candidate (Finset.mem_univ _)
  simpa only [sparse_stageActions _ Finset.univ_nonempty,sparse_allowed_full] using hh.1

@[simp] theorem sparse_target_empty (candidate s : Bool) :
    s ∉ stageTargets fixtureKernel sparseMenu actionPriority ∅ candidate := by
  intro h
  unfold stageTargets at h
  rw [sparse_stageActions_empty] at h
  obtain ⟨E,hE,hs⟩ := (markovTargetStates_exact _ _ _ _ _ _ _).mp h
  have he : E = ∅ := Finset.subset_empty.mp hE.1
  have hh := hE.2.2.1.nonempty
  simpa only [he,Finset.not_nonempty_empty] using hh

def expectedTarget (B : Finset Bool) (candidate : Bool) : Option (Finset (Bool × Bool)) :=
  if B = ∅ then none else if B = {false} then some (goodPairs false)
    else if B = {true} then some (goodPairs true) else some (goodPairs candidate)
def expectedStage (B : Finset Bool) : Finset (Bool × Bool) :=
  if B = ∅ then ∅ else if B = {false} then goodPairs false
    else if B = {true} then goodPairs true else Finset.univ

theorem support_cases (B : Finset Bool) :
    B = ∅ ∨ B = {false} ∨ B = {true} ∨ B = Finset.univ := by
  exact (by decide : ∀ B : Finset Bool, B = ∅ ∨ B = {false} ∨ B = {true} ∨ B = Finset.univ) B

theorem sparse_actualTarget (B : Finset Bool) (candidate s : Bool) :
    actualTarget fixtureKernel sparseMenu actionPriority B candidate s = expectedTarget B candidate := by
  rcases support_cases B with rfl | rfl | rfl | rfl
  · simp [actualTarget,expectedTarget]
  · simp [actualTarget,expectedTarget,sparse_choose_singleton]
  · simp [actualTarget,expectedTarget,sparse_choose_singleton]
  · rw [actualTarget,if_pos (sparse_target_full candidate s),sparse_choose_full]
    rfl

theorem sparse_stage_exact (B : Finset Bool) :
    stageActions fixtureKernel sparseMenu actionPriority B = expectedStage B := by
  rcases support_cases B with rfl | rfl | rfl | rfl
  · simp [expectedStage]
  · simp [expectedStage,sparse_stageActions]
  · simp [expectedStage,sparse_stageActions]
  · rw [sparse_stageActions _ Finset.univ_nonempty,sparse_allowed_full]
    rfl

/-- Explicit numeric tables: only the full-support cycle orientation varies. -/
def literalData (orientation : Bool) : Data :=
  ⟨if orientation then 24332 else 44812,428783445879334172098560,64080⟩

def expectedCycle (orientation : Bool) (B : Finset Bool) (fallback residue : Bool) : Bool :=
  if B = ∅ then fallback else if B = {false} then false else if B = {true} then true
    else if residue then !orientation else orientation

theorem literal_cycle_digits : ∀ (orientation : Bool) (B : Finset Bool) (fallback residue : Bool),
    cycleDigit (literalData orientation) B fallback residue =
      bitNat (expectedCycle orientation B fallback residue) := by decide

theorem literal_target_digits : ∀ (orientation : Bool) (B : Finset Bool) (candidate s : Bool),
    targetDigit (literalData orientation) B candidate s = retainedCode (expectedTarget B candidate) := by decide

theorem literal_stage_digits : ∀ (orientation : Bool) (B : Finset Bool),
    stageDigit (literalData orientation) B = targetCode (expectedStage B) := by decide

theorem retained_cycle_exact (orientation : Bool) (hO : initialCandidate = orientation)
    (B : Finset Bool) (fallback residue : Bool) :
    cycleAction B fallback (bitNat residue) = expectedCycle orientation B fallback residue := by
  rcases support_cases B with rfl | rfl | rfl | rfl
  · simp [cycleAction,expectedCycle]
  · simp [cycle_singleton,expectedCycle]
  · simp [cycle_singleton,expectedCycle]
  · cases residue
    · rw [show bitNat false = 0 from rfl,full_cycle_fallback fallback false 0]
      change initialCandidate = orientation
      exact hO
    · rw [show bitNat true = 1 from rfl,full_cycle_one fallback]
      change Bool.not initialCandidate = Bool.not orientation
      rw [hO]

/-- Every off-path cell is certified. The premise selects a retained orientation
mathematically; it does not evaluate the opaque classical cycle choice. -/
theorem literal_certificate (orientation : Bool) (hO : initialCandidate = orientation) :
    Certificate (literalData orientation) fixtureKernel sparseMenu actionPriority := by
  constructor
  · intro B f r
    rw [literal_cycle_digits,retained_cycle_exact orientation hO]
  · intro B c s
    rw [literal_target_digits,sparse_actualTarget]
  · intro B
    rw [literal_stage_digits,sparse_stage_exact]

/-- At least one of the two fully explicit numeral records certifies the exact
retained choices. No particular record is asserted to be the evaluated choice. -/
theorem explicit_two_table_certificate :
    Certificate (literalData false) fixtureKernel sparseMenu actionPriority ∨
      Certificate (literalData true) fixtureKernel sparseMenu actionPriority := by
  cases h : initialCandidate
  · exact Or.inl (literal_certificate false h)
  · exact Or.inr (literal_certificate true h)

end Orthemology.Eighth.SemanticControls.LiteralAssessment
