import PythonRunnerBudgets

namespace P02.PythonRunner
open P02.PythonExpr

def expected (trace : Bool) (c : Config) : Dictionary × List (ℕ × ℕ) × ℕ :=
  ((remaining trace c).store,c.events++(remaining trace c).events,
    c.meter.steps+(remaining trace c).ticks)

theorem step_expected (trace : Bool) (c out : Config) (h : step trace c = .ok out) :
    expected trace c = expected trace out := by
  by_cases hw : c.work = []
  · have hs : step trace c = .ok c := by simp [step, hw]
    have he : out = c := Except.ok.inj (h.symm.trans hs)
    subst out
    rfl
  · rcases step_accounting trace c out hw h with ⟨hs,he,ht,_,_,_,_⟩
    exact Prod.ext hs (Prod.ext he ht)

theorem runSteps_expected (trace : Bool) (fuel : ℕ) (c out : Config)
    (h : runSteps trace fuel c = .ok out) : expected trace c = expected trace out := by
  induction fuel generalizing c out with
  | zero =>
      have he : c = out := by simpa [runSteps] using h
      subst out
      rfl
  | succ fuel ih =>
      cases hs : step trace c with
      | error err => simp [runSteps, hs] at h
      | ok next =>
          have hn : runSteps trace fuel next = .ok out := by simpa [runSteps, hs] using h
          exact (step_expected trace c next hs).trans (ih next out hn)

theorem runFuel_success (trace : Bool) (fuel : ℕ) (c out : Config)
    (h : runFuel trace fuel c = .ok (some out)) :
    runSteps trace fuel c = .ok out ∧ out.work = [] := by
  cases hr : runSteps trace fuel c with
  | error err => simp [runFuel, hr] at h
  | ok middle =>
      cases hw : middle.work with
      | nil =>
          simp [runFuel, hr, hw] at h
          cases h
          exact ⟨hr,hw⟩
      | cons t ts => simp [runFuel, hr, hw] at h

/-- Every successful finite-fuel run has the same source-model store, chronological
assignment trace, and exact task-plus-expression tick count. -/
theorem runner_success_summary (trace : Bool) (fuel : ℕ) (s : Command) (d : Dictionary)
    (m : Meter) (out : Config)
    (h : runFuel trace fuel (initial s d m) = .ok (some out)) :
    out.store = (commandSummary trace s d).store ∧
    out.events = (commandSummary trace s d).events ∧
    out.meter.steps = m.steps + (commandSummary trace s d).ticks := by
  obtain ⟨hr,hw⟩ := runFuel_success trace fuel (initial s d m) out h
  have he := runSteps_expected trace fuel (initial s d m) out hr
  have ho : remaining trace out = unchanged out.store := by simp [remaining, hw, tasksSummary]
  simp only [expected, remaining_initial, ho] at he
  simp [initial, unchanged] at he
  exact ⟨he.1.symm,he.2.1.symm,he.2.2.symm⟩

theorem runner_success_sound (trace : Bool) (fuel : ℕ) (s : Command) (d : Dictionary)
    (m : Meter) (out : Config)
    (h : runFuel trace fuel (initial s d m) = .ok (some out)) :
    dictionaryRead out.store = P02A2.ObserverCore.exec (lowerCommand s) (dictionaryRead d) := by
  rw [(runner_success_summary trace fuel s d m out h).1]
  exact commandSummary_store trace s d

theorem runner_success_ticks (trace : Bool) (fuel : ℕ) (s : Command) (d : Dictionary)
    (m : Meter) (out : Config)
    (h : runFuel trace fuel (initial s d m) = .ok (some out)) :
    out.meter.steps = m.steps + (commandSummary trace s d).ticks :=
  (runner_success_summary trace fuel s d m out h).2.2

theorem runner_success_events (trace : Bool) (fuel : ℕ) (s : Command) (d : Dictionary)
    (m : Meter) (out : Config)
    (h : runFuel trace fuel (initial s d m) = .ok (some out)) :
    out.events = (commandSummary trace s d).events :=
  (runner_success_summary trace fuel s d m out h).2.1

/-- The explicit logical budgets complete with all three successful observations.
The last register lookup has no max_bits check, matching the actual run API. -/
theorem runner_finite_observations (trace : Bool) (s : Command) (d : Dictionary) (output : ℕ) :
    let p := commandSummary trace s d
    ∃ out, runFuel trace p.pops (initial s d ⟨some p.ticks,some p.bits,0⟩) = .ok (some out) ∧
      dictionaryRead out.store output =
        P02A2.ObserverCore.exec (lowerCommand s) (dictionaryRead d) output ∧
      out.meter.steps = p.ticks ∧ out.events = p.events := by
  obtain ⟨out,h⟩ := runner_complete_finite trace s d
  refine ⟨out,h,?_,?_,?_⟩
  · exact congrFun (runner_success_sound trace _ s d _ out h) output
  · simpa using runner_success_ticks trace _ s d _ out h
  · exact runner_success_events trace _ s d _ out h

end P02.PythonRunner
