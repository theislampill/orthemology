import ExecutablePruning
namespace HiddenParity.Reviewer
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000
abbrev One := Fin 1
abbrev Two := Fin 2
abbrev Three := Fin 3
abbrev Four := Fin 4

def selfSource (e : Two) : Two := e
def selfSucc (e : Two) : Finset Two := {e}
def rows (_ : Two) (_ : Two) : Nat := 0
def evenP (_ : Two) (_ : Two) : Nat := 2

theorem disconnected_is_not_component :
    ¬ IsEndComponent selfSource selfSucc (Finset.univ : Finset Two) := by decide

theorem disconnected_components_separate :
    executableOutput selfSource selfSucc Finset.univ rows evenP 0 Finset.univ =
      ({({0} : Finset Two), {1}} : Finset (Finset Two)) := by decide

def oneSource (_ : Three) : One := 0
def oneSucc (_ : Three) : Finset One := {0}
def sameRow (_ : Two) (_ : Three) : Nat := 0
def allOdd (_ : Two) (e : Three) : Nat := 2 * e.val + 1

theorem fuel_two_insufficient :
    executableIterate oneSource oneSucc Finset.univ sameRow allOdd 0 2 Finset.univ =
      ({2} : Finset Three) := by decide

theorem fuel_three_sufficient :
    executableIterate oneSource oneSucc Finset.univ sameRow allOdd 0 3 Finset.univ =
      (∅ : Finset Three) := by decide

theorem penultimate_component_is_invalid :
    ¬ Valid (endComponentFamily oneSource oneSucc) (Finset.univ : Finset Two)
      sameRow allOdd 0 ({2} : Finset Three) := by
  intro h
  obtain ⟨d,hd,he⟩ := h.2 0 (by simp) (by intro e _; rfl)
  obtain ⟨e,heE,hpe⟩ := hd.1
  have : e = 2 := Finset.mem_singleton.mp heE
  subst e
  norm_num [allOdd] at hpe
  omega

def hugePriority (_ : Two) (e : Three) : Nat :=
  if e = 0 then 100000000000000000000000000000000000001 else 100000000000000000000000000000000000002

theorem large_priorities_do_not_require_numeric_loop :
    executableOutput oneSource oneSucc Finset.univ sameRow hugePriority 0 Finset.univ =
      ({({1,2} : Finset Three)} : Finset (Finset Three)) := by decide

def oddCandidate (_ : One) (_ : Three) : Nat := 1
def oneRow (_ : One) (_ : Three) : Nat := 0

theorem empty_live_set_is_vacuous :
    executableOutput oneSource oneSucc (∅ : Finset One) oneRow oddCandidate 0 Finset.univ =
      ({(Finset.univ : Finset Three)} : Finset (Finset Three)) := by decide

def candidateOnlyOdd (m : Two) (_ : Three) : Nat := if m = 0 then 1 else 2

theorem absent_candidate_priority_unchecked :
    executableOutput oneSource oneSucc ({1} : Finset Two) sameRow candidateOnlyOdd 0 Finset.univ =
      ({(Finset.univ : Finset Three)} : Finset (Finset Three)) := by decide

theorem present_candidate_priority_checked :
    executableOutput oneSource oneSucc (Finset.univ : Finset Two) sameRow candidateOnlyOdd 0 Finset.univ =
      (∅ : Finset (Finset Three)) := by decide

def chain (s t : Four) : Prop := t.val = s.val+1
instance : DecidableRel chain := fun _ _ => inferInstanceAs (Decidable (_ = _))

theorem long_reach : 3 ∈ FiniteReachability.reachable chain (0 : Four) := by decide
theorem direction_matters : 0 ∉ FiniteReachability.reachable chain (3 : Four) := by decide
theorem zero_length_reach : 3 ∈ FiniteReachability.reachable chain (3 : Four) := by decide

def shortSrc (_ : One) : Two := 0
def noSucc (_ : One) : Finset Two := ∅
def outsideSucc (_ : One) : Finset Two := {1}

theorem zero_path_not_enough_for_component :
    ¬ IsEndComponent shortSrc noSucc (Finset.univ : Finset One) := by decide

theorem successor_outside_used_states_rejected :
    ¬ IsEndComponent shortSrc outsideSucc (Finset.univ : Finset One) := by decide

def zeroSrc (e : Fin 0) : One := Fin.elim0 e
def zeroSucc (e : Fin 0) : Finset One := Fin.elim0 e
def zeroRows (_ : One) (e : Fin 0) : Nat := Fin.elim0 e
def zeroPriority (_ : One) (e : Fin 0) : Nat := Fin.elim0 e

theorem no_pairs_no_output :
    executableOutput zeroSrc zeroSucc Finset.univ zeroRows zeroPriority 0 Finset.univ =
      (∅ : Finset (Finset (Fin 0))) := by decide

-- Generic rows really are equality labels; no normalization is hidden in the theorem.
def unnormalizedRow (_ : One) (_ : Three) (_ : Two) : Nat := 7
def allEven (_ : One) (_ : Three) : Nat := 2

theorem generic_theorem_does_not_validate_probability_rows :
    executableOutput oneSource oneSucc Finset.univ unnormalizedRow allEven 0 Finset.univ =
      ({(Finset.univ : Finset Three)} : Finset (Finset Three)) := by decide

-- Validity is not downward closed: a higher odd pair can coexist with an even minimum.
def mixedPriority (_ : One) (e : Three) : Nat := if e = 0 then 2 else 3

theorem mixed_component_retained :
    executableOutput oneSource oneSucc Finset.univ oneRow mixedPriority 0 Finset.univ =
      ({(Finset.univ : Finset Three)} : Finset (Finset Three)) := by decide

theorem its_odd_subcomponent_rejected :
    executableOutput oneSource oneSucc Finset.univ oneRow mixedPriority 0 {1} =
      (∅ : Finset (Finset Three)) := by decide

theorem subset_not_same_as_target_output :
    executableTargetStates oneSource oneSucc Finset.univ oneRow mixedPriority 0 {1} =
      (∅ : Finset One) := by decide

end HiddenParity.Reviewer
