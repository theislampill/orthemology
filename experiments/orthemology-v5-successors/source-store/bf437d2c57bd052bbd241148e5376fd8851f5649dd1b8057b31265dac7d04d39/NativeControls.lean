import NativeRefinement
import TypedExamples

namespace SharedAlias.Native
open ComposedExecution
open OperationalJoin.Typed (BoundedEnvelope interface)
namespace Fixture
abbrev before := OperationalJoin.Typed.Examples.before
abbrev installed := OperationalJoin.Typed.Examples.installed
abbrev policy := OperationalJoin.Typed.Examples.source 0
abbrev command := OperationalJoin.Typed.Examples.installCommand

def routes : Routing 7 := ⟨[0,1], [some 6], 2, 5, 5⟩
def badRoutes : Routing 7 := ⟨[0,1], [none], 2, 5, 5⟩
def environment : SharedAlias.Environment (interface 7) where
  aliasClass := {0,1}
  class_positive := by decide
  budget := 1
  budget_positive := by decide
  actualFaults := {some 6}
  actual_faults := by decide
  actual_budget := by decide
  non_saturated := by decide
  q := 5
  r := 5
  overlap := by decide
  repair_available := by decide
  revoke_available := by decide
  source := OperationalJoin.Typed.Examples.source
  source_epoch := by intro e; rfl

theorem routes_match : RoutingMatches routes environment := by
  constructor <;> decide

def start : FiniteState 7 := initial policy before

theorem start_exact : view start = SharedAlias.initial environment before := by rfl

theorem start_reachable : SharedAlias.Reachable environment (view start) :=
  ⟨before, [], by rw [start_exact]; exact .nil _⟩

def k : BoundedEnvelope 7 := ⟨⟨.install command, installed, 1001, [0,2,3,4,5]⟩, by decide⟩
def reordered : BoundedEnvelope 7 := ⟨⟨.install command, installed, 1001, [2,0,3,4,5]⟩, by decide⟩
def changedSuccessor : BoundedEnvelope 7 :=
  ⟨⟨.install command, { installed with unrelated := [] }, 1001, [0,2,3,4,5]⟩, by decide⟩
def shortK : BoundedEnvelope 7 := ⟨⟨.install command, installed, 1001, [0,2]⟩, by decide⟩
def cancelled : FiniteState 7 := cancelSlot routes start 0 k "A" false

def preparedGood : FiniteState 7 :=
  ([0,2,3,4,5] : List (Fin 7)).foldl (fun C i => prepareSlot routes C i k "A" 2 true) start

def malformed : ComposedExecution.Envelope :=
  ⟨.install command, installed, 1001, [0,0,2,3,4]⟩

def preparedBad : FiniteState 7 :=
  ([0,2,3,4,5] : List (Fin 7)).foldl (fun C i => prepareSlot badRoutes C i k "A" 2 true) start
end Fixture

/-- One shared veto, one addressed real receipt. No sibling receipt exists. -/
theorem sibling_veto_without_receipt :
    Fixture.k.val ∈ (rootAt Fixture.cancelled (rootOf Fixture.routes 1)).cancelled ∧
    0 ∈ receipts Fixture.cancelled Fixture.k.val ∧
    1 ∉ receipts Fixture.cancelled Fixture.k.val := by decide

theorem fixture_cancellation_accepted :
    SharedAlias.Step Fixture.environment (view Fixture.start)
      (.cancelAck 0 Fixture.k "A") (view Fixture.cancelled) := by
  exact cancel_emitted_step Fixture.routes Fixture.environment Fixture.routes_match
    Fixture.start 0 Fixture.k "A" false

/-- Same nonce and support are insufficient for complete command equality. -/
theorem ordered_identity_distinct :
    Fixture.k ≠ Fixture.reordered ∧
    OperationalJoin.Typed.path Fixture.k = OperationalJoin.Typed.path Fixture.reordered ∧
    Fixture.k.val.nonce = Fixture.reordered.val.nonce := by decide

/-- A veto of one complete ordered command does not veto its permutation. -/
theorem ordered_veto_exact :
    ¬ComposedExecution.Eligible Fixture.before 2
      (rootAt Fixture.cancelled (rootOf Fixture.routes 1)) Fixture.k.val "A" ∧
    ComposedExecution.Eligible Fixture.before 2
      (rootAt Fixture.cancelled (rootOf Fixture.routes 1)) Fixture.reordered.val "A" := by decide

/-- Different full successor data fails unchanged source eligibility. -/
theorem changed_successor_rejected :
    prepareAllowed Fixture.routes Fixture.start 0 Fixture.changedSuccessor "A" 2 true = false := by decide

theorem wrong_requester_rejected :
    prepareAllowed Fixture.routes Fixture.start 0 Fixture.k "intruder" 2 true = false ∧
    cancelAllowed Fixture.routes 0 Fixture.k "intruder" true = false := by decide

/-- A valid proposal's lease can expire by the actual sampled service time. -/
theorem expired_service_rejected :
    prepareAllowed Fixture.routes Fixture.start 0 Fixture.k "A" 90 true = false := by decide

/-- The exact one shared badOpen bit is retained. Bad storage contents alone
cannot open a gate that this environmental bit withholds. -/
theorem single_bad_open_retained :
    applied Fixture.badRoutes Fixture.preparedBad Fixture.k "A" 2 false = false ∧
    applied Fixture.badRoutes Fixture.preparedBad Fixture.k "A" 2 true = true := by decide

theorem duplicate_receipts_do_not_close :
    closed Fixture.routes { Fixture.start with cancelRows := [(Fixture.k.val, [0,0,0])] } Fixture.k = false ∧
    closed Fixture.routes { Fixture.start with cancelRows := [(Fixture.k.val, [0,2,3])] } Fixture.k = true := by decide

theorem first_match_receipt_table :
    closed Fixture.routes { Fixture.start with cancelRows :=
      [(Fixture.k.val, [0]), (Fixture.k.val, [0,2,3])] } Fixture.k = false := by decide

theorem wrong_order_receipts_do_not_close :
    closed Fixture.routes { Fixture.start with cancelRows :=
      [(Fixture.reordered.val, [0,2,3])] } Fixture.k = false := by decide

theorem wrong_quorum_rejected :
    prepareAllowed Fixture.routes Fixture.start 0 Fixture.shortK "A" 2 true = false ∧
    applied Fixture.routes Fixture.start Fixture.shortK "A" 2 true = false := by decide

theorem honest_path_ignores_bad_open :
    applied Fixture.routes Fixture.preparedGood Fixture.k "A" 2 false = true ∧
    applied Fixture.routes Fixture.preparedGood Fixture.k "A" 2 true = true := by decide

theorem wrong_policy_rejected :
    prepareAllowed Fixture.routes { Fixture.start with defaultRoot :=
      { Fixture.start.defaultRoot with policy := { Fixture.policy with actor := "other" } } }
      0 Fixture.k "A" 2 true = false := by decide

theorem revoked_epoch_rejected :
    prepareAllowed Fixture.routes { Fixture.start with defaultRoot :=
      { Fixture.start.defaultRoot with revoked := [0] } } 0 Fixture.k "A" 2 true = false := by decide

theorem absent_commitment_rejected :
    applied Fixture.routes Fixture.start Fixture.k "A" 2 true = false := by decide

theorem existing_tombstone_rejected :
    prepareAllowed Fixture.routes Fixture.cancelled 0 Fixture.k "A" 2 true = false := by decide

theorem faulty_receipt_without_tombstone :
    0 ∈ receipts (cancelSlot Fixture.badRoutes Fixture.start 0 Fixture.k "intruder" true) Fixture.k.val ∧
    (rootAt (cancelSlot Fixture.badRoutes Fixture.start 0 Fixture.k "intruder" true) none).cancelled = [] := by decide

theorem malformed_key_does_not_close :
    closed Fixture.routes { Fixture.start with cancelRows :=
      [(Fixture.malformed, [0,2,3])] } Fixture.k = false := by decide

theorem malformed_historical_memory_ignored :
    OperationalJoin.Typed.memory (n := 7) [Fixture.malformed] = ∅ := by
  ext e
  simp only [OperationalJoin.Typed.mem_memory, List.mem_singleton, Finset.not_mem_empty, iff_false]
  intro same
  have nodup := e.property.1
  rw [same] at nodup
  simp [Fixture.malformed] at nodup

/-- False source attempts preserve every native field, including finite tables. -/
theorem rejection_full_identity :
    attemptSlot Fixture.badRoutes Fixture.preparedBad Fixture.k "A" 2 false = Fixture.preparedBad :=
  rejected_identity _ _ _ _ _ _ single_bad_open_retained.1

/- This is compiled evaluation of the new shared-store program fragment. -/
#eval (decide (Fixture.k.val ∈ (rootAt Fixture.cancelled (rootOf Fixture.routes 1)).cancelled),
  (receipts Fixture.cancelled Fixture.k.val).map Fin.val,
  applied Fixture.badRoutes Fixture.preparedBad Fixture.k "A" 2 false,
  applied Fixture.badRoutes Fixture.preparedBad Fixture.k "A" 2 true)

end SharedAlias.Native
