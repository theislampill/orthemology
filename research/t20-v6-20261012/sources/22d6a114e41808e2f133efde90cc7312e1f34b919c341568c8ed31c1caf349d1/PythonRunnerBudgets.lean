import PythonRunnerMachine

namespace P02.PythonRunner
open P02.PythonExpr

def Fits (trace : Bool) (c : Config) : Prop :=
  Room c.meter (remaining trace c).ticks ∧ Width c.meter (remaining trace c).bits

def commandExpr : Command → Option PyExpr
  | .set _ e | .loop _ e _ | .branch e _ _ => some e
  | .seq _ => none

theorem commandSummary_ticks_pos (trace : Bool) (s : Command) (d : Dictionary) :
    0 < (commandSummary trace s d).ticks := by
  cases s <;> simp [commandSummary, charge, Nat.add_assoc]

theorem repeatSummary_ticks_pos (body : Dictionary → Summary) (r k n : ℕ) (d : Dictionary) :
    0 < (repeatSummary body r k n d).ticks := by
  cases n <;> simp [repeatSummary, charge]

theorem taskSummary_ticks_pos (trace : Bool) (t : Task) (d : Dictionary) :
    0 < (taskSummary trace t d).ticks := by
  cases t with
  | stmt s => exact commandSummary_ticks_pos trace s d
  | «repeat» r count k body => exact repeatSummary_ticks_pos _ _ _ _ _

theorem command_expr_bounds (trace : Bool) (s : Command) (d : Dictionary) (e : PyExpr)
    (h : commandExpr s = some e) :
    1+cost e ≤ (commandSummary trace s d).ticks ∧
    neededBits d e ≤ (commandSummary trace s d).bits := by
  cases s with
  | set r e' =>
      simp only [commandExpr, Option.some.injEq] at h
      subst e
      simp [commandSummary]
  | seq ss => simp [commandExpr] at h
  | loop r e' body =>
      simp only [commandExpr, Option.some.injEq] at h
      subst e
      simp [commandSummary, charge]
  | branch e' s t =>
      simp only [commandExpr, Option.some.injEq] at h
      subst e
      simp [commandSummary, charge]

theorem initial_task_room (trace : Bool) (c : Config) (hne : c.work ≠ []) (hf : Fits trace c) :
    Room c.meter 1 := by
  have hp : 0 < (remaining trace c).ticks := by
    rcases c with ⟨work,d,m,events⟩
    cases work with
    | nil => exact (hne rfl).elim
    | cons t tail =>
        have ht := taskSummary_ticks_pos trace t d
        change 0 < (taskSummary trace t d).ticks +
          (tasksSummary trace tail (taskSummary trace t d).store).ticks
        omega
  intro bound hb
  have hs := hf.1 bound hb
  omega

theorem expression_fits (trace : Bool) (s : Command) (e : PyExpr) (tail : List Task)
    (d : Dictionary) (m : Meter) (events : List (ℕ × ℕ)) (he : commandExpr s = some e)
    (hf : Fits trace ⟨.stmt s::tail,d,m,events⟩) :
    Room {m with steps := m.steps+1} (cost e) ∧
    Width {m with steps := m.steps+1} (neededBits d e) := by
  have hh := command_expr_bounds trace s d e he
  constructor
  · intro bound hb
    have hs := hf.1 bound hb
    change m.steps + ((commandSummary trace s d).ticks +
      (tasksSummary trace tail (commandSummary trace s d).store).ticks) ≤ bound at hs
    change m.steps + 1 + cost e ≤ bound
    omega
  · intro bound hb
    have hs := hf.2 bound hb
    change max (commandSummary trace s d).bits
      (tasksSummary trace tail (commandSummary trace s d).store).bits ≤ bound at hs
    exact le_trans hh.2 (le_trans (Nat.le_max_left _ _) hs)

/-- With sufficient future check-site budgets, the exact source step cannot fail.
This does not impose a width bound on initial values or unchecked loop writes. -/
theorem step_exists_of_fits (trace : Bool) (c : Config) (hne : c.work ≠ [])
    (hf : Fits trace c) : ∃ out, step trace c = .ok out := by
  have ht := tick_of_room c.meter (initial_task_room trace c hne hf)
  rcases c with ⟨work,d,m,events⟩
  cases work with
  | nil => exact (hne rfl).elim
  | cons task tail =>
      cases task with
      | «repeat» r count k body =>
          by_cases hk : k < count
          · exact ⟨_,by simp [step, ht, hk]; rfl⟩
          · exact ⟨_,by simp [step, ht, hk]; rfl⟩
      | stmt s =>
          cases s with
          | seq ss => exact ⟨_,by simp [step, ht]; rfl⟩
          | set r e =>
              have he := expression_fits trace (.set r e) e tail d m events rfl hf
              have hx := expression_bounded d e {m with steps := m.steps+1} he.1 he.2
              exact ⟨_,by simp [step, ht, hx]; rfl⟩
          | loop r e body =>
              have he := expression_fits trace (.loop r e body) e tail d m events rfl hf
              have hx := expression_bounded d e {m with steps := m.steps+1} he.1 he.2
              exact ⟨_,by simp [step, ht, hx]; rfl⟩
          | branch e s t =>
              have he := expression_fits trace (.branch e s t) e tail d m events rfl hf
              have hx := expression_bounded d e {m with steps := m.steps+1} he.1 he.2
              exact ⟨_,by simp [step, ht, hx]; rfl⟩

theorem fits_after_step (trace : Bool) (c out : Config) (hne : c.work ≠ [])
    (hf : Fits trace c) (hs : step trace c = .ok out) : Fits trace out := by
  rcases step_accounting trace c out hne hs with ⟨_,_,ht,_,hb,hl,hmax⟩
  constructor
  · intro bound hbound
    have h := hf.1 bound (hl.symm.trans hbound)
    change out.meter.steps + (remaining trace out).ticks ≤ bound
    rw [← ht]
    exact h
  · intro bound hbound
    exact le_trans hb (hf.2 bound (hmax.symm.trans hbound))

/-- Finite mathematical task fuel equals the pure profile's task pops. The
meter budget counts task pops PLUS embedded expression work and is different. -/
theorem complete_at_pops (trace : Bool) (c : Config) (hf : Fits trace c) :
    ∃ out, runSteps trace (remaining trace c).pops c = .ok out ∧ out.work = [] := by
  by_cases hw : c.work = []
  · refine ⟨c,?_,hw⟩
    simp [remaining, hw, tasksSummary, unchanged, runSteps]
  · obtain ⟨next,hs⟩ := step_exists_of_fits trace c hw hf
    have hn := fits_after_step trace c next hw hf hs
    have hp := (step_accounting trace c next hw hs).2.2.2.1
    obtain ⟨out,hr,hout⟩ := complete_at_pops trace next hn
    refine ⟨out,?_,hout⟩
    rw [← hp, runSteps, hs, result_bind_ok, hr]
termination_by (remaining trace c).pops

def initial (s : Command) (d : Dictionary) (m : Meter) : Config := ⟨[.stmt s],d,m,[]⟩

@[simp] theorem remaining_initial (trace : Bool) (s : Command) (d : Dictionary) (m : Meter) :
    remaining trace (initial s d m) = commandSummary trace s d := by
  simp [remaining, initial, tasksSummary, taskSummary]

/-- Explicit finite source-meter budgets for each typed finite command/store.
No uniform all-input finite cap or physical execution guarantee is asserted. -/
theorem runner_complete_finite (trace : Bool) (s : Command) (d : Dictionary) :
    let p := commandSummary trace s d
    ∃ out, runFuel trace p.pops
      (initial s d ⟨some p.ticks,some p.bits,0⟩) = .ok (some out) := by
  let p := commandSummary trace s d
  let c := initial s d ⟨some p.ticks,some p.bits,0⟩
  have hf : Fits trace c := by
    constructor
    · intro bound hb
      have he := Option.some.inj hb
      simpa only [c, remaining_initial, Nat.zero_add] using le_of_eq he
    · intro bound hb
      have he := Option.some.inj hb
      simpa only [c, remaining_initial] using le_of_eq he
  obtain ⟨out,hr,hw⟩ := complete_at_pops trace c hf
  refine ⟨out,?_⟩
  have hp : (remaining trace c).pops = p.pops := by simp [c,p]
  rw [hp] at hr
  change runFuel trace p.pops c = .ok (some out)
  simp only [runFuel, hr, result_bind_ok, hw]

end P02.PythonRunner
