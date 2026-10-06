import WindowProgress
import TypedExamples

namespace SharedAlias.Progress.Witness
open OperationalJoin
open OperationalJoin.Typed (interface BoundedEnvelope)
namespace Fixture
abbrev before := OperationalJoin.Typed.Examples.before
abbrev installed := OperationalJoin.Typed.Examples.installed
abbrev source := OperationalJoin.Typed.Examples.source
abbrev installCommand := OperationalJoin.Typed.Examples.installCommand
end Fixture
noncomputable section
open Classical

def actor : ComposedExecution.Actor :=
  ⟨Fixture.source 0, Fixture.before, "A", 2, 1000⟩

def action : ComposedExecution.Action := .install Fixture.installCommand

def times (n : Nat) : Nat := 2 + n

theorem clock : ServiceClock actor.observedTime 2 22 21 times := by
  refine ⟨?_, ?_, ?_⟩
  · intro i j lower; simp only [times]; omega
  · intro n hn; change 2 ≤ 2 + n; omega
  · intro n hn; simp only [times]; omega

/-- A non-singleton authority window checked against the unchanged full source
localStep. It is not a premise that any distributed attempt succeeds. -/
theorem install_window (time : Nat) (lo : 2 ≤ time) (hi : time ≤ 22) :
    ComposedExecution.localStep Fixture.before (Fixture.source 0) time action = some Fixture.installed := by
  have valid : CriterionInstallation.InstallValid
      (ComposedExecution.ruleState Fixture.before (Fixture.source 0) time) Fixture.installCommand := by
    simp [CriterionInstallation.InstallValid, CriterionInstallation.InstallGrantValid,
      ComposedExecution.ruleState, Fixture.before, Fixture.source, Fixture.installCommand,
      OperationalJoin.Typed.Examples.before, OperationalJoin.Typed.Examples.source,
      OperationalJoin.Typed.Examples.policy, OperationalJoin.Typed.Examples.installCommand]
    omega
  have guard := (CriterionInstallation.guard_true_iff_valid _ _).mpr valid
  have allowed : ComposedExecution.policyAllows Fixture.before (Fixture.source 0) action = true := by decide
  simp only [ComposedExecution.localStep, allowed, if_true, action,
    CriterionInstallation.install, guard]
  rfl

/-- One fixed public actor/program works in every accepted fixed shared world
with seven labels and this authentic initial source policy. Root alias choice,
fault choice, and all bad service replies remain universally quantified.
The initial memories make exact 21-command freshness immediate. -/
theorem uniform_unknown_world_installation
    (E : Environment (interface 7)) (q : E.q = 5)
    (source0 : E.source 0 = Fixture.source 0)
    (badSync : Fin 7 → Bool) (bad : Nat → Replies 7) :
    ∃ specs events, compile actor action sevenPaths times bad = some specs ∧
      specs.length = 21 ∧
      SharedAlias.Trace E (SharedAlias.initial E Fixture.before) events
        (run E (actorSynchronize E actor badSync (SharedAlias.initial E Fixture.before)) actor.identity specs) ∧
      events.length = 259 ∧
      (run E (actorSynchronize E actor badSync (SharedAlias.initial E Fixture.before)) actor.identity specs).plant =
        Fixture.installed := by
  apply seven_protected_window_progress actor action E (SharedAlias.initial E Fixture.before)
    Fixture.installed 2 22 times badSync bad q
  · exact ⟨Fixture.before, [], .nil _⟩
  · rfl
  · rfl
  · exact source0.symm
  · rfl
  · decide
  · exact clock
  · intro t lo hi
    simpa only [SharedAlias.initial, source0] using install_window t lo hi
  · intro k member i good
    simp [SharedAlias.initial]

end
end SharedAlias.Progress.Witness
