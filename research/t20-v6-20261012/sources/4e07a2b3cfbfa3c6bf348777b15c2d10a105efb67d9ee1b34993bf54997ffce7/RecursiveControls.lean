import RecursivePhysicalDecoder
import RecursiveKernelEquivalence
import ZeroSupportFixture

noncomputable section
open Finset
open Orthemology.Tranche2
namespace RecursiveAudit

def reveal (θ _a y : Bool) : ℝ := if y = θ then 1 else 0
def targets (θ : Bool) : Finset Bool := {θ}
def menus (B : Finset Bool) : Finset Bool := B

theorem reveal_support (a y : Bool) : supportUpdate reveal univ a y = {y} := by
  ext θ
  cases θ <;> cases y <;> norm_num [supportUpdate, reveal]

theorem strict_reveal (a y : Bool) : supportStay reveal univ a y = false := by
  rw [supportStay_false, reveal_support]
  intro h
  have hn : (!y) ∈ ({y} : Finset Bool) := by rw [h]; exact mem_univ _
  cases y <;> simp at hn

theorem singleton_winning (θ : Bool) : RecursiveWinning reveal targets menus {θ} := by
  apply RecursiveWinning.intro {θ} (by simp) (fun _ => [θ])
  · simp
  · simp [menus]
  · intro σ hσ a ha y hn hstrict
    have ha' : a = θ := by simpa using ha
    subst a
    have hsub := supportUpdate_subset reveal ({θ} : Finset Bool) θ y
    obtain ⟨ζ,hζ⟩ := hn
    have hz : ζ = θ := by simpa using hsub hζ
    have heq : supportUpdate reveal {θ} θ y = {θ} := by
      apply Finset.Subset.antisymm hsub
      intro z hz'
      have : z = θ := by simpa using hz'
      subst z
      simpa [hz] using hζ
    exact (hstrict heq).elim
  · intro σ hσ
    have hs : σ = θ := by simpa using hσ
    subst σ
    right
    constructor
    · simp [targets]
    · intro η hη _
      have he : η = θ := by simpa using hη
      subst η
      simp [targets]

theorem reveal_winning : RecursiveWinning reveal targets menus univ := by
  apply RecursiveWinning.intro univ (by simp) (fun σ => [σ])
  · simp
  · simp [menus]
  · intro σ _ a ha y _ _
    rw [reveal_support]
    exact singleton_winning y
  · intro σ _
    left
    exact ⟨σ,by simp,σ,strict_reveal σ σ,by norm_num [reveal]⟩

theorem empty_support_loses : ¬ RecursiveWinning reveal targets menus ∅ := by
  intro h
  simpa using recursiveWinning_nonempty reveal targets menus h

theorem empty_menu_loses (B : Finset Bool) :
    ¬ RecursiveWinning reveal targets (fun _ => ∅) B := by
  intro h
  obtain ⟨θ,hθ⟩ := recursiveWinning_nonempty reveal targets (fun _ => ∅) h
  obtain ⟨as,hn,hm,_⟩ := recursiveWinning_witness reveal targets (fun _ => ∅) h θ hθ
  obtain ⟨a,ha⟩ := List.exists_mem_of_ne_nil as hn
  have := hm (List.mem_toFinset.mpr ha)
  simpa using this

-- An impossible symbol must not force an empty successor certificate.
def deterministic (_θ _a y : Bool) : ℝ := if y then 0 else 1

theorem impossible_symbol_empty (B : Finset Bool) (a : Bool) :
    supportUpdate deterministic B a true = ∅ := by
  simp [supportUpdate, deterministic]

theorem possible_symbol_retains (B : Finset Bool) (a : Bool) :
    supportUpdate deterministic B a false = B := by
  simp [supportUpdate, deterministic]

theorem identical_laws_disjoint_targets_lose :
    ¬ RecursiveWinning deterministic targets menus univ := by
  intro h
  obtain ⟨as,hn,hm,hc,hs⟩ := recursiveWinning_witness deterministic targets menus h false (mem_univ _)
  rcases hs with hp | hsv
  · obtain ⟨a,ha,y,hy,hpos⟩ := hp
    cases y
    · have he : supportStay deterministic (univ : Finset Bool) a false = true := by
        simp [supportStay,possible_symbol_retains]
      have hf : (true : Bool) = false := he.symm.trans hy
      cases hf
    · norm_num [deterministic] at hpos
  · obtain ⟨a,ha⟩ := List.exists_mem_of_ne_nil as hn
    have hfalse := hsv.1 (List.mem_toFinset.mpr ha)
    have htrue := hsv.2 true (mem_univ _) (fun b _ => rfl) (List.mem_toFinset.mpr ha)
    have hf : a = false := by simpa [targets] using hfalse
    have ht : a = true := by simpa [targets] using htrue
    exact Bool.false_ne_true (hf.symm.trans ht)

theorem no_empty_executed_repair (as : List Bool) (h : as ≠ [])
    (w : StopObs Bool as.length) : stoppedActions as w ≠ [] :=
  stoppedActions_nonempty as h w

theorem first_exit_drops_suffix :
    stoppedActions [true,false] (Sum.inl true : StopObs Bool 2) = [true] := rfl

theorem completed_records_keep_order :
    stoppedActions [true,false] (Sum.inr (false, Sum.inr (true, PUnit.unit)) : StopObs Bool 2)
      = [true,false] := rfl

theorem revealing_exit_positive :
    stoppedMass (ZeroSupportFixture.P true) (ZeroSupportFixture.stay false) [true,false]
      (Sum.inl true : StopObs Bool 2) = 16/25 := by
  norm_num [stoppedMass,ZeroSupportFixture.P,ZeroSupportFixture.stay]

theorem revealing_exit_impossible_for_other :
    stoppedMass (ZeroSupportFixture.P false) (ZeroSupportFixture.stay false) [true,false]
      (Sum.inl true : StopObs Bool 2) = 0 := by
  norm_num [stoppedMass,ZeroSupportFixture.P,ZeroSupportFixture.stay]

theorem forbidden_suffix_not_executed :
    false ∉ stoppedActions [true,false] (Sum.inl true : StopObs Bool 2) ∧
    false ∉ ZeroSupportFixture.allowed true := by
  simp [stoppedActions,ZeroSupportFixture.allowed]

abbrev RObs (_p _σ : Bool) := Bool
def stopAlways (_p _σ _y : Bool) := false
def nextAlways (_p _σ _y : Bool) := true
def chooseFalse (_p : Bool) (_h : PhaseHistory (Obs := RObs) _p) := false
def state0 : RecordedState (Obs := RObs) := (⟨false,[]⟩,none)

theorem record_survives_reset :
    (recordedUpdate stopAlways nextAlways chooseFalse state0 true).2 =
      some (⟨false,false,true⟩ : ObservationRecord (Obs := RObs)) := rfl

theorem exit_resets_memory :
    (recordedUpdate stopAlways nextAlways chooseFalse state0 true).1 = ⟨true,[]⟩ := rfl

theorem distinct_exit_records :
    recordedUpdate stopAlways nextAlways chooseFalse state0 true ≠
      recordedUpdate stopAlways nextAlways chooseFalse state0 false := by
  intro h
  have h' := congrArg Prod.snd h
  simp [recordedUpdate] at h'

end RecursiveAudit
