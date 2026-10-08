import NativeHistoryControls
namespace IndependentOwnerHistoryReview
open SharedAlias.Native
open ComposedExecution
open OperationalJoin.Typed (interface)
noncomputable section

def s0 := SharedAlias.initial Fixture.environment Fixture.before
def s1 := SharedAlias.request s0
def s2 := SharedAlias.acknowledge Fixture.environment s1 0
def s3 := SharedAlias.acknowledge Fixture.environment s2 2
def s4 := SharedAlias.acknowledge Fixture.environment s3 3
def s5 := SharedAlias.acknowledge Fixture.environment s4 4
def s6 := SharedAlias.acknowledge Fixture.environment s5 5
def s7 := SharedAlias.complete s6
def s8 := SharedAlias.deliver Fixture.environment s7 1 1

def actualInputs : List (HistoryInput 7) :=
  [.request, .acknowledge 0, .acknowledge 2, .acknowledge 3,
    .acknowledge 4, .acknowledge 5, .complete, .deliver 1 HistoryFixture.nextPolicy]

theorem exact_owner_trace : SharedAlias.Trace Fixture.environment s0
    (actualInputs.map HistoryInput.event) s8 := by
  exact .cons (.request s0 rfl)
    (.cons (.acknowledge s1 0 rfl)
      (.cons (.acknowledge s2 2 rfl)
        (.cons (.acknowledge s3 3 rfl)
          (.cons (.acknowledge s4 4 rfl)
            (.cons (.acknowledge s5 5 rfl)
              (.cons (.complete s6 rfl (by decide))
                (.cons (.deliver s7 1 1 (by decide)) (.nil s8))))))))

theorem owner_inputs_authentic :
    ∀ input ∈ actualInputs, input.Authentic Fixture.environment := by
  intro input member
  simp only [actualInputs, List.mem_cons, List.not_mem_nil, or_false] at member
  rcases member with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> simp [HistoryInput.Authentic, HistoryFixture.nextPolicy, Fixture.environment]
  rfl

theorem actual_constructor_matches_independent_endpoint :
    ∃ native, reconstruct Fixture.routes Fixture.before HistoryFixture.samples HistoryFixture.requests =
      some native ∧ view native = s8 := by
  exact reconstruct_from_accepted Fixture.routes Fixture.environment Fixture.routes_match
    Fixture.before HistoryFixture.samples HistoryFixture.requests Fixture.policy actualInputs
    rfl rfl rfl owner_inputs_authentic s8 exact_owner_trace

#print axioms exact_owner_trace
#print axioms owner_inputs_authentic
#print axioms actual_constructor_matches_independent_endpoint
end
end IndependentOwnerHistoryReview
