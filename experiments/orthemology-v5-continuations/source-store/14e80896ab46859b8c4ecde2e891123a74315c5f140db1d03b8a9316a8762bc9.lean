import SCCParity
import AdapterTests

namespace HiddenParity.SCCControls
open HiddenParity.Controls
set_option maxRecDepth 100000
set_option maxHeartbeats 8000000

def deadSource (e : Two) : Three := ⟨e.val, by omega⟩
def deadSucc (e : Two) : Finset Three := if e = 0 then {0,1} else {0,2}

theorem first_dead_cleanup :
    SCCPruning.step deadSource deadSucc Finset.univ = ({0} : Finset Two) := by decide

theorem second_dead_cleanup :
    SCCPruning.step deadSource deadSucc ({0} : Finset Two) = (∅ : Finset Two) := by decide

theorem dead_source_cascade_rejected :
    SCCPruning.mecs deadSource deadSucc Finset.univ = (∅ : Finset (Finset Two)) := by decide

-- Sources remain, but the reverse path disappears after the escaping action is removed.
def reverseSource (e : Four) : Three := if e.val < 2 then 0 else 1
def reverseSucc (e : Four) : Finset Three :=
  if e = 0 then {0} else if e = 1 then {1} else if e = 2 then {1} else {0,2}

theorem first_reverse_cleanup :
    SCCPruning.step reverseSource reverseSucc Finset.univ = ({0,1,2} : Finset Four) := by decide

theorem second_reverse_cleanup :
    SCCPruning.step reverseSource reverseSucc ({0,1,2} : Finset Four) = ({0,2} : Finset Four) := by decide

theorem stable_scc_split :
    SCCPruning.mecs reverseSource reverseSucc Finset.univ =
      ({({0} : Finset Four), {2}} : Finset (Finset Four)) := by decide

theorem empty_successor_rejected :
    SCCPruning.mecs singleSource emptySucc Finset.univ = (∅ : Finset (Finset One)) := by decide

theorem missing_source_rejected :
    SCCPruning.mecs singleSource openSucc Finset.univ = (∅ : Finset (Finset One)) := by decide

theorem empty_input :
    SCCPruning.mecs sourceOne succOne (∅ : Finset Three) = (∅ : Finset (Finset Three)) := by decide

theorem same_state_pairs_form_one_component :
    SCCPruning.mecs sourceOne succOne Finset.univ =
      ({(Finset.univ : Finset Three)} : Finset (Finset Three)) := by decide

theorem closed_cycle_retained :
    SCCPruning.mecs cycleSource cycleSucc Finset.univ =
      ({(Finset.univ : Finset Two)} : Finset (Finset Two)) := by decide

theorem parity_cascade :
    SCCPruning.parityOutput sourceOne succOne Finset.univ sameRow cascadePriority 0 Finset.univ =
      ({({2} : Finset Three)} : Finset (Finset Three)) := by decide

theorem newly_matching_rival :
    SCCPruning.parityOutput zeroSource zeroSucc Finset.univ revealRow revealPriority 0 Finset.univ =
      ({({2} : Finset Three)} : Finset (Finset Three)) := by decide

theorem higher_odd_cycle_retained :
    SCCPruning.parityOutput cycleSource cycleSucc Finset.univ cycleRow cycle23 0 Finset.univ =
      ({(Finset.univ : Finset Two)} : Finset (Finset Two)) := by decide

theorem cobuchi_bad_cycle_rejected :
    SCCPruning.parityOutput cycleSource cycleSucc Finset.univ cycleRow cycle21 0 Finset.univ =
      (∅ : Finset (Finset Two)) := by decide

theorem graph_splits_after_parity_deletion :
    SCCPruning.parityOutput splitSource splitSucc Finset.univ splitRow splitPriority 0 Finset.univ =
      ({({0} : Finset Four)} : Finset (Finset Four)) := by decide

theorem full_row_difference_retains :
    SCCPruning.parityOutput singleSource singleSucc Finset.univ exitRow oppositePriority 0 Finset.univ =
      ({(Finset.univ : Finset One)} : Finset (Finset One)) := by decide

theorem matching_odd_rival_rejects :
    SCCPruning.parityOutput singleSource singleSucc Finset.univ sameSingleRow oppositePriority 0 Finset.univ =
      (∅ : Finset (Finset One)) := by decide

theorem normalized_candidate_target :
    SCCPruning.markovTarget exitKernel singleSource Finset.univ oppositePriority 0 Finset.univ =
      ({0} : Finset Two) := by decide

theorem normalized_rival_exit :
    SCCPruning.markovTarget exitKernel singleSource Finset.univ oppositePriority 1 Finset.univ =
      (∅ : Finset Two) := by decide

end HiddenParity.SCCControls
