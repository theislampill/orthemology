import AliasCuts
import Mathlib.Data.Fintype.Powerset
import Mathlib.Data.Fintype.Fin

namespace T20Grounded.CutControls

set_option maxRecDepth 4096
set_option maxHeartbeats 4000000

/-- Cardinality optimum, distinct from inclusion minimality. -/
def Cheapest {A : Type} (family : Finset (Finset A)) (cut : Finset A) : Prop :=
  Hits family cut ∧ ∀ other, Hits family other → cut.card ≤ other.card

def fourFamily : Finset (Finset (Fin 4)) := {{0}, {1,3}, {2,3}}
def fourOrigin (i : Fin 4) : Fin 2 := if i.val < 3 then 0 else 1

def k32Family : Finset (Finset (Fin 5)) :=
  {{0,3},{0,4},{1,3},{1,4},{2,3},{2,4}}
def k32Origin (i : Fin 5) : Fin 3 :=
  if i.val < 3 then 0 else if i.val = 3 then 1 else 2

 theorem four_unique_cheapest_label_cut (cut : Finset (Fin 4)) :
    Cheapest fourFamily cut ↔ cut = {0,3} := by
  revert cut
  unfold Cheapest Hits
  decide

 theorem four_unique_cheapest_root_cut (cut : Finset (Fin 2)) :
    Cheapest (imageFamily fourOrigin fourFamily) cut ↔ cut = {0} := by
  revert cut
  unfold Cheapest Hits
  decide

 theorem four_cheapest_label_image_cost :
    (({0,3} : Finset (Fin 4)).image fourOrigin).card = 2 := by decide

 theorem four_actual_root_cut_cost : ({0} : Finset (Fin 2)).card = 1 := by decide

 theorem four_discarded_cut_is_inclusion_minimal :
    MinimalCut fourFamily {0,1,2} := by
  unfold MinimalCut MinimalFor Hits
  decide

 theorem four_discarded_cut_recovers_root_optimum :
    ({0,1,2} : Finset (Fin 4)).image fourOrigin = {0} := by decide

 theorem k32_unique_cheapest_label_cut (cut : Finset (Fin 5)) :
    Cheapest k32Family cut ↔ cut = {3,4} := by
  revert cut
  unfold Cheapest Hits
  decide

 theorem k32_unique_cheapest_root_cut (cut : Finset (Fin 3)) :
    Cheapest (imageFamily k32Origin k32Family) cut ↔ cut = {0} := by
  revert cut
  unfold Cheapest Hits
  decide

 theorem k32_cheapest_label_image_cost :
    (({3,4} : Finset (Fin 5)).image k32Origin).card = 2 := by decide

 theorem k32_discarded_cut_is_inclusion_minimal :
    MinimalCut k32Family {0,1,2} := by
  unfold MinimalCut MinimalFor Hits
  decide

 theorem k32_discarded_cut_recovers_root_optimum :
    ({0,1,2} : Finset (Fin 5)).image k32Origin = {0} := by decide

end T20Grounded.CutControls
