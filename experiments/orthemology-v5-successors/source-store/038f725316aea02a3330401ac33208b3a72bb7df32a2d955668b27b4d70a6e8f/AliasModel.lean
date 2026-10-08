import JoinOperations
import MapTransport

/-! A mathematical shared-store realization. The class and fixed actual faults
are environment parameters, not controller observations. Events address labels.
No scheduling, transcript equivalence or actual physical implementation is asserted. -/
namespace SharedAlias
open OperationalJoin
noncomputable section
open Classical

structure Environment {m : Nat} (I : Interface m) where
  aliasClass : Finset (Fin m)
  class_positive : 1 ≤ aliasClass.card
  budget : Nat
  budget_positive : 1 ≤ budget
  actualFaults : Finset (Option (Fin m))
  actual_faults : actualFaults ⊆ AttributionKernel.actualRoots aliasClass
  actual_budget : actualFaults.card ≤ budget
  non_saturated : budget < m - aliasClass.card + 1
  q : Nat
  r : Nat
  overlap : m + (budget + aliasClass.card - 1) < q + r
  repair_available : q + (budget + aliasClass.card - 1) ≤ m
  revoke_available : r + (budget + aliasClass.card - 1) ≤ m
  source : Nat → I.Policy
  source_epoch : ∀ e, I.policyEpoch (source e) = e

open Environment

def Environment.labelBudget {m} {I : Interface m} (E : Environment I) : Nat :=
  E.budget + E.aliasClass.card - 1

def Environment.rootOf {m} {I : Interface m} (E : Environment I) : Fin m → Option (Fin m) :=
  AttributionKernel.rootMap E.aliasClass

def Environment.labelFaults {m} {I : Interface m} (E : Environment I) : Finset (Fin m) :=
  AttributionKernel.taintedLabels E.aliasClass E.actualFaults

theorem label_budget {m} {I : Interface m} (E : Environment I) :
    E.labelFaults.card ≤ E.labelBudget := by
  have bound := AttributionKernel.tainted_label_budget E.aliasClass E.actualFaults E.class_positive
  have actual := E.actual_budget
  unfold labelFaults labelBudget
  omega

theorem label_budget_lt {m} {I : Interface m} (E : Environment I) : E.labelBudget < m := by
  have size := Finset.card_le_univ E.aliasClass
  have positive := E.class_positive
  have nonSat := E.non_saturated
  simp only [Fintype.card_fin] at size
  unfold labelBudget
  omega

def Environment.labelConfig {m} {I : Interface m} (E : Environment I) : Config I where
  budget := E.labelBudget
  q := E.q
  r := E.r
  faulty := E.labelFaults
  budget_bound := label_budget E
  overlap := E.overlap
  budget_lt_roots := label_budget_lt E
  repair_available := E.repair_available
  revoke_available := E.revoke_available
  source := E.source
  source_epoch := E.source_epoch

@[simp] theorem good_iff {m} {I : Interface m} (E : Environment I) (i : Fin m) :
    Good E.labelConfig i ↔ E.rootOf i ∉ E.actualFaults := by
  simp [Good, labelConfig, labelFaults, AttributionKernel.taintedLabels, rootOf]

theorem good_same_root {m} {I : Interface m} (E : Environment I) (i j : Fin m)
    (same : E.rootOf i = E.rootOf j) : Good E.labelConfig i ↔ Good E.labelConfig j := by
  simp only [good_iff, same]

theorem exact_one_class {m} {I : Interface m} (E : Environment I) :
    AttributionKernel.ExactOneClassMap E.aliasClass E.rootOf :=
  AttributionKernel.canonical_exact E.aliasClass

/-- Ambient unused root names are not counted and cannot be addressed by an event. -/
structure State {m} (I : Interface m) where
  epoch : Nat
  roots : Option (Fin m) → RootState I
  pending : Bool
  acks : Finset (Fin m)
  certificates : Nat → Finset (Fin m)
  cancelAcks : I.Command → Finset (Fin m)
  plant : I.Plant

def initial {m} {I : Interface m} (E : Environment I) (p : I.Plant) : State I :=
  ⟨0, fun _ => ⟨E.source 0, ∅, ∅, ∅⟩, false, ∅, fun _ => ∅, fun _ => ∅, p⟩

def setRoot {m} {I : Interface m} (C : State I) (r : Option (Fin m))
    (z : RootState I) : State I :=
  { C with roots := Function.update C.roots r z }

def request {m} {I : Interface m} (C : State I) : State I :=
  { C with pending := true, acks := ∅ }

def acknowledge {m} {I : Interface m} (E : Environment I) (C : State I)
    (i : Fin m) : State I :=
  { C with acks := (Finset.univ.filter (fun j => E.rootOf j = E.rootOf i)) ∪ C.acks
           roots := if Good E.labelConfig i then Function.update C.roots (E.rootOf i)
             { C.roots (E.rootOf i) with revoked := insert C.epoch (C.roots (E.rootOf i)).revoked }
             else C.roots }

def complete {m} {I : Interface m} (C : State I) : State I :=
  { C with epoch := C.epoch + 1, pending := false, acks := ∅,
           certificates := Function.update C.certificates C.epoch C.acks }

/-- Every certified e is allowed, including delayed/repeated deliveries.
Only the stored descriptor advances; older deliveries leave the state unchanged. -/
def deliver {m} {I : Interface m} (E : Environment I) (C : State I)
    (i : Fin m) (e : Nat) : State I :=
  if I.policyEpoch (C.roots (E.rootOf i)).descriptor < e then
    setRoot C (E.rootOf i) { C.roots (E.rootOf i) with descriptor := E.source e }
  else C

def prepare {m} {I : Interface m} (E : Environment I) (C : State I)
    (i : Fin m) (k : I.Command) : State I :=
  setRoot C (E.rootOf i)
    { C.roots (E.rootOf i) with commitments := insert k (C.roots (E.rootOf i)).commitments }

def cancelAck {m} {I : Interface m} (E : Environment I) (C : State I)
    (i : Fin m) (k : I.Command) : State I :=
  { C with cancelAcks := Function.update C.cancelAcks k (insert i (C.cancelAcks k))
           roots := if Good E.labelConfig i then Function.update C.roots (E.rootOf i)
             { C.roots (E.rootOf i) with cancelled := insert k (C.roots (E.rootOf i)).cancelled }
             else C.roots }

def land {m} {I : Interface m} (C : State I) (k : I.Command) : State I :=
  { C with plant := I.effect C.plant k }

def Lands {m} {I : Interface m} (E : Environment I) (C : State I)
    (time : Nat) (k : I.Command) (who : I.Requester) : Prop :=
  ValidPath E.labelConfig k ∧ ∀ i ∈ I.commandPath k, Good E.labelConfig i →
    Permits C.plant time (C.roots (E.rootOf i)) k who

/-- Label addressing is kept unchanged. A corrupt event is environmental and
may affect all aliases of one lifetime-bad actual root. -/
inductive Step {m} {I : Interface m} (E : Environment I) :
    State I → Event I → State I → Prop where
  | request (C) (idle : C.pending = false) : Step E C .request (request C)
  | acknowledge (C i) (pending : C.pending = true) :
      Step E C (.acknowledge i) (acknowledge E C i)
  | complete (C) (pending : C.pending = true) (quorum : C.acks.card = E.r) :
      Step E C .complete (complete C)
  | deliver (C i e) (cert : 0 < e ∧ e ≤ C.epoch) :
      Step E C (.deliver i e) (deliver E C i e)
  | prepare (C i k who time) (selected : i ∈ I.commandPath k)
      (path : ValidPath E.labelConfig k)
      (grant : i ∈ E.labelConfig.faulty ∨
        Envelope C.plant time (C.roots (E.rootOf i)) k who) :
      Step E C (.prepare i k who time) (prepare E C i k)
  | cancelAck (C i k who) (selected : i ∈ I.commandPath k)
      (auth : i ∈ E.labelConfig.faulty ∨ who = I.recipient k) :
      Step E C (.cancelAck i k who) (cancelAck E C i k)
  | close (C k) (certificate : E.labelBudget < (C.cancelAcks k).card) :
      Step E C (.close k) C
  | land (C k who time) (admitted : Lands E C time k who) :
      Step E C (.land k who time) (land C k)
  | hold (C) : Step E C .hold C
  | corrupt (C i z) (bad : i ∈ E.labelConfig.faulty) :
      Step E C (.corrupt i z) (setRoot C (E.rootOf i) z)

inductive Trace {m} {I : Interface m} (E : Environment I) :
    State I → List (Event I) → State I → Prop where
  | nil (C) : Trace E C [] C
  | cons {C D F a as} : Step E C a D → Trace E D as F → Trace E C (a :: as) F

def Reachable {m} {I : Interface m} (E : Environment I) (C : State I) : Prop :=
  ∃ p events, Trace E (initial E p) events C

@[simp] theorem acknowledge_receipts {m} {I : Interface m} (E : Environment I)
    (C : State I) (i : Fin m) : (acknowledge E C i).acks = insert i C.acks := rfl

@[simp] theorem cancelAck_receipts {m} {I : Interface m} (E : Environment I)
    (C : State I) (i : Fin m) (k : I.Command) :
    (cancelAck E C i k).cancelAcks k = insert i (C.cancelAcks k) := by
  simp [cancelAck]

theorem shared_prepare {m} {I : Interface m} (E : Environment I) (C : State I)
    (i j : Fin m) (k : I.Command) (same : E.rootOf j = E.rootOf i) :
    k ∈ ((prepare E C i k).roots (E.rootOf j)).commitments := by
  simp [prepare, setRoot, same]

theorem shared_cancel {m} {I : Interface m} (E : Environment I) (C : State I)
    (i j : Fin m) (k : I.Command) (same : E.rootOf j = E.rootOf i)
    (good : Good E.labelConfig i) :
    k ∈ ((cancelAck E C i k).roots (E.rootOf j)).cancelled := by
  simp only [cancelAck, if_pos good, same, Function.update_self, Finset.mem_insert_self]

end
end SharedAlias
