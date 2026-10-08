import AliasSimulation
import ModelControls

namespace SharedAlias.SimulationControls
open OperationalJoin
open ModelControls
noncomputable section
open Classical

def selectedCommand : testInterface.Command := (0, {1,2,3,4,5})
def openRoot : RootState testInterface := ⟨(0 : Nat), ∅, {selectedCommand}, ∅⟩
def closedRoot : RootState testInterface := ⟨(0 : Nat), {0}, {selectedCommand}, ∅⟩
def unpreparedRoot : RootState testInterface := ⟨(0 : Nat), ∅, ∅, ∅⟩

theorem extra_veto_relation : RootRefines testInterface 1 closedRoot openRoot := by
  refine ⟨rfl, ?_, by simp [openRoot], by simp [openRoot]⟩
  intro k
  simp only [openRoot, closedRoot, Finset.mem_singleton]
  constructor
  · intro eq; subst k; exact ⟨rfl, by decide⟩
  · exact And.left

theorem extra_veto_breaks_converse :
    Permits () 0 openRoot selectedCommand () ∧ ¬Permits () 0 closedRoot selectedCommand () := by
  simp [Permits, Envelope, openRoot, closedRoot, selectedCommand, testInterface]

theorem wrong_veto_direction_is_detected :
    ¬RootRefines testInterface 1 openRoot closedRoot := by
  intro h
  have impossible := h.revoked (show 0 ∈ closedRoot.revoked by simp [closedRoot])
  simp [openRoot] at impossible

theorem missing_selected_commitment_is_detected :
    ¬RootRefines testInterface 1 openRoot unpreparedRoot ∧
    ¬Permits () 0 unpreparedRoot selectedCommand () := by
  constructor
  · intro h
    have prepared := (h.commitments selectedCommand).mpr ⟨by simp [openRoot], by decide⟩
    simp [unpreparedRoot] at prepared
  · simp [Permits, unpreparedRoot]

theorem preparation_expansion_has_no_receipts {m} {I : Interface m}
    (s : OperationalJoin.State I) (labels : Finset (Fin m)) (k : I.Command) :
    (prepareLabels s labels k).acks = s.acks ∧
    (prepareLabels s labels k).cancelAcks = s.cancelAcks ∧
    (prepareLabels s labels k).certificates = s.certificates := ⟨rfl, rfl, rfl⟩

theorem delivery_expansion_has_no_receipts {m} {I : Interface m} (c : Config I)
    (s : OperationalJoin.State I) (labels : Finset (Fin m)) (e : Nat) :
    (deliverLabels c s labels e).acks = s.acks ∧
    (deliverLabels c s labels e).cancelAcks = s.cancelAcks ∧
    (deliverLabels c s labels e).certificates = s.certificates := ⟨rfl, rfl, rfl⟩

end
end SharedAlias.SimulationControls
