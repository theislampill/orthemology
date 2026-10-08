import NativeHistoryControls
namespace IndependentHistorySampleReview
open SharedAlias.Native
open ComposedExecution

theorem forged_first_row_shadows_authentic_second :
    policySample [(1, HistoryFixture.falsePolicy), (1, HistoryFixture.nextPolicy)] 1 =
      some HistoryFixture.falsePolicy := by decide

theorem event_equality_is_not_policy_authentication :
    (HistoryInput.deliver (m := 7) 1 HistoryFixture.falsePolicy).event =
      (HistoryInput.deliver (m := 7) 1 HistoryFixture.nextPolicy).event ∧
    ¬(HistoryInput.deliver (m := 7) 1 HistoryFixture.falsePolicy).Authentic Fixture.environment := by
  constructor
  · rfl
  · change HistoryFixture.falsePolicy ≠ Fixture.environment.source HistoryFixture.falsePolicy.epoch
    decide

theorem missing_tail_sample_fails_whole_constructor :
    (reconstruct Fixture.routes Fixture.before HistoryFixture.missingSamples
      [.hold, .request, .deliver 1 1]).isNone = true := by decide

theorem forged_content_is_constructible_but_not_authenticated :
    (reconstruct Fixture.routes Fixture.before [(0, {Fixture.policy with actor := "intruder"})]
      ([] : List (HistoryRequest 7))).map (fun C => C.defaultRoot.policy.actor) = some "intruder" := by decide

#print axioms forged_first_row_shadows_authentic_second
#print axioms event_equality_is_not_policy_authentication
#print axioms missing_tail_sample_fails_whole_constructor
#print axioms forged_content_is_constructible_but_not_authenticated
#eval ((policySample [(1, HistoryFixture.falsePolicy), (1, HistoryFixture.nextPolicy)] 1).map Policy.actor,
  (reconstruct Fixture.routes Fixture.before HistoryFixture.missingSamples [.hold, .deliver 1 1]).isNone)
end IndependentHistorySampleReview
