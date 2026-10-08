import AliasTyped

namespace SharedAlias.Typed
open OperationalJoin
open OperationalJoin.Typed (interface BoundedEnvelope)
noncomputable section
open Classical

/-- Exact list-membership view of one shared store for the unchanged source gate. -/
def rawRoot {m} (z : RootState (interface m)) : ComposedExecution.Root :=
  ⟨z.descriptor, z.revoked.toList, z.commitments.toList.map Subtype.val,
    z.cancelled.toList.map Subtype.val⟩

theorem mem_raw_commands {m} (ks : Finset (BoundedEnvelope m)) (k : BoundedEnvelope m) :
    k.val ∈ ks.toList.map Subtype.val ↔ k ∈ ks := by
  simp only [List.mem_map, Finset.mem_toList]
  constructor
  · rintro ⟨j, member, same⟩
    have eq : j = k := Subtype.ext same
    simpa only [eq] using member
  · intro member; exact ⟨k, member, rfl⟩

theorem rawRoot_represents {m} (z : RootState (interface m)) :
    OperationalJoin.Typed.RootRepresents (rawRoot z) z := by
  refine ⟨rfl, ?_, ?_, ?_⟩
  · intro e; exact Finset.mem_toList.symm
  · intro k; exact (mem_raw_commands z.commitments k).symm
  · intro k; exact (mem_raw_commands z.cancelled k).symm

/-- This literal gate snapshot need not be reachable in the common system;
the separately proved weak relation supplies common reachability instead. -/
def literalSnapshot {m} (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) : OperationalJoin.State (interface m) :=
  ⟨C.epoch, fun i => C.roots (E.rootOf i), C.pending, C.acks,
    C.certificates, C.cancelAcks, C.plant, false⟩

/-- A proof-side gate adapter, not an actor API and not a lifecycle state match.
Completed certificate lists are irrelevant to attempt and deliberately not
invented. No claim is made for compiled preparation/certification/cancellation. -/
def gateWorld {m} (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (time : Nat) : ComposedExecution.World where
  n := m
  budget := E.labelBudget
  q := E.q
  r := E.r
  effectivePolicy := E.source C.epoch
  plant := C.plant
  now := time
  roots := fun i => if bound : i < m then rawRoot (C.roots (E.rootOf ⟨i,bound⟩))
    else rawRoot (⟨E.source 0, ∅, ∅, ∅⟩ : RootState (interface m))
  tainted := fun i => if bound : i < m then decide (E.rootOf ⟨i,bound⟩ ∈ E.actualFaults)
    else false
  completed := []

theorem gateWorld_represents {m} (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (time : Nat) :
    OperationalJoin.Typed.RuntimeRepresents E.labelConfig (gateWorld E C time) (literalSnapshot E C) := by
  refine ⟨rfl, rfl, rfl, ?_, ?_⟩
  · intro i
    simp only [gateWorld, dif_pos i.isLt, decide_eq_false_iff_not, good_iff]
  · intro i
    simpa only [gateWorld, literalSnapshot, dif_pos i.isLt] using
      rawRoot_represents (C.roots (E.rootOf i))

theorem compiled_success_lands {m} (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (time : Nat) (k : BoundedEnvelope m)
    (who : String) (badOpen : Bool)
    (success : (ComposedExecution.attempt (gateWorld E C time) k.val who badOpen).2 = true) :
    SharedAlias.Lands E C time k who := by
  exact OperationalJoin.Typed.successful_attempt_lands (gateWorld E C time) (literalSnapshot E C)
    (gateWorld_represents E C time) k who badOpen success

/-- Exact source Boolean correspondence only when its one shared faulty-gate
Boolean is true. False may additionally withhold. -/
theorem compiled_attempt_iff {m} (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (time : Nat) (k : BoundedEnvelope m) (who : String) :
    (ComposedExecution.attempt (gateWorld E C time) k.val who true).2 = true ↔
      SharedAlias.Lands E C time k who := by
  exact OperationalJoin.Typed.open_attempt_iff_lands (gateWorld E C time) (literalSnapshot E C)
    (gateWorld_represents E C time) k who

theorem compiled_success_exact_effect {m} {E : Environment (interface m)}
    {C : SharedAlias.State (interface m)} (reach : SharedAlias.Reachable E C)
    (time : Nat) (k : BoundedEnvelope m) (who : String) (badOpen : Bool)
    (success : (ComposedExecution.attempt (gateWorld E C time) k.val who badOpen).2 = true) :
    ComposedExecution.localStep C.plant (E.source C.epoch) time k.val.action = some k.val.successor ∧
      (ComposedExecution.attempt (gateWorld E C time) k.val who badOpen).1.plant =
        (SharedAlias.land C k).plant := by
  have admitted := compiled_success_lands E C time k who badOpen success
  exact ⟨(finite_history_admission reach time k who admitted).2.2,
    ComposedExecution.applied_attempt_exact_successor (gateWorld E C time) k.val who badOpen success⟩

theorem compiled_rejection_identity {m} (E : Environment (interface m))
    (C : SharedAlias.State (interface m)) (time : Nat) (k : BoundedEnvelope m)
    (who : String) (badOpen : Bool)
    (failure : (ComposedExecution.attempt (gateWorld E C time) k.val who badOpen).2 = false) :
    (ComposedExecution.attempt (gateWorld E C time) k.val who badOpen).1 = gateWorld E C time :=
  ComposedExecution.rejected_attempt_full_identity _ _ _ _ failure

end
end SharedAlias.Typed
