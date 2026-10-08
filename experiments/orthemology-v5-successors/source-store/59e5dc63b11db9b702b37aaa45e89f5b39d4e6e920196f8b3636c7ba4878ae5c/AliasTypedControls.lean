import AliasTypedWitness

namespace SharedAlias.Typed.Controls
open OperationalJoin
open OperationalJoin.Typed (interface BoundedEnvelope path mem_path)
noncomputable section
open Classical

def reordered : BoundedEnvelope 7 :=
  ⟨{ Witness.command.val with path := [1,0,2,3,4] }, by decide⟩

theorem same_nonce_and_support :
    reordered.val.nonce = Witness.command.val.nonce ∧ path reordered = path Witness.command := by
  constructor
  · rfl
  · ext i
    rw [mem_path, mem_path]
    change i.val ∈ ([1,0,2,3,4] : List Nat) ↔ i.val ∈ ([0,1,2,3,4] : List Nat)
    simp only [List.mem_cons, List.not_mem_nil, or_false]
    tauto

theorem different_full_command : reordered ≠ Witness.command := by
  intro eq
  have paths := congrArg (fun k : BoundedEnvelope 7 => k.val.path) eq
  have impossible : ([1,0,2,3,4] : List Nat) = [0,1,2,3,4] := paths
  contradiction

theorem full_command_tombstone_not_nonce :
    reordered ∉ ({Witness.command} : Finset (BoundedEnvelope 7)) := by
  simpa only [Finset.mem_singleton] using different_full_command

theorem prepared_aliases_share_one_store :
    Witness.env.rootOf 0 = Witness.env.rootOf 1 ∧
    Witness.command ∈ (Witness.prepared.roots (Witness.env.rootOf 1)).commitments := by
  constructor
  · decide
  · have opened := Witness.installation_lands.2 (1 : Fin 7)
      ((mem_path Witness.command 1).mpr (by decide)) (by decide)
    exact opened.1

theorem certified_cancellation_needs_three_real_labels :
    Witness.cancelled.cancelAcks Witness.command = {0,2,3} ∧
    1 ∉ Witness.cancelled.cancelAcks Witness.command := by
  have receipts : Witness.cancelled.cancelAcks Witness.command = {3,2,0} := by
    simp only [Witness.cancelled, cancelAck_receipts, Witness.prepared, prepare,
      setRoot, Witness.start, initial]
    rfl
  rw [receipts]
  decide

end
end SharedAlias.Typed.Controls
