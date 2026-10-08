import GenericFiniteQueryMeasure

namespace HiddenParity.Stochastic
open MeasureTheory ProbabilityTheory
open Orthemology.Tranche2.FiniteAlphabetQuery

variable {S Y E : Type*} [Inhabited Y]

/-- Before the first query both actual evaluator runs agree; after it both counters
are positive. The claim is proved from the recursive transition equation. -/
theorem zero_query_run_agreement
    (ask : S → Bool) (next : S → Y → S) (oracle other : ℕ → Y) (s : S) (n : ℕ) :
    ((run ask next oracle s n).2 = 0 ↔ (run ask next other s n).2 = 0) ∧
      ((run ask next oracle s n).2 = 0 → (run ask next oracle s n).1 = (run ask next other s n).1) := by
  induction n with
  | zero => exact ⟨Iff.rfl, fun _ => rfl⟩
  | succ n ih =>
      by_cases hzero : (run ask next oracle s n).2 = 0
      · have hother := ih.1.mp hzero
        have heq := ih.2 hzero
        cases hq : ask (run ask next oracle s n).1 with
        | false =>
            simp [run, advance, ← heq, hq, hzero, hother]
        | true =>
            simp only [run, advance, ← heq, hq, ↓reduceIte, Prod.snd, hzero, hother]
            simp
      · have hnother : (run ask next other s n).2 ≠ 0 := fun h => hzero (ih.1.mpr h)
        have h1 : (run ask next oracle s (n+1)).2 ≠ 0 := by
          have hm := counter_monotone ask next oracle s (Nat.le_succ n)
          change (run ask next oracle s n).2 ≤ (run ask next oracle s (n+1)).2 at hm
          omega
        have h2 : (run ask next other s (n+1)).2 ≠ 0 := by
          have hm := counter_monotone ask next other s (Nat.le_succ n)
          change (run ask next other s n).2 ≤ (run ask next other s (n+1)).2 at hm
          omega
        exact ⟨by simp [h1, h2], fun h => (h1 h).elim⟩

/-- Query count zero is exactly no querying action in the entire finite prefix. -/
theorem run_counter_zero_iff (ask : S → Bool) (next : S → Y → S)
    (oracle : ℕ → Y) (s : S) (n : ℕ) :
    (run ask next oracle s n).2 = 0 ↔
      ∀ k < n, ask (run ask next oracle s k).1 = false := by
  induction n with
  | zero => simp [run]
  | succ n ih =>
      rw [Nat.forall_lt_succ]
      cases hq : ask (run ask next oracle s n).1 with
      | false => simp [run, advance, hq, ih]
      | true => simp [run, advance, hq]

/-- Retain the readout up to the first query; then emit a fixed cemetery value.
The alive flag records when killing occurred. -/
def killedReadout (readout : S → E) (cemetery : E) (tr : Trace S) : ℕ → Bool × E :=
  fun n => if (tr n).2 = 0 then (true, readout (tr n).1) else (false, cemetery)

theorem killedReadout_oracle_independent
    (ask : S → Bool) (next : S → Y → S) (oracle other : ℕ → Y)
    (s : S) (readout : S → E) (cemetery : E) :
    killedReadout readout cemetery (run ask next oracle s) =
      killedReadout readout cemetery (run ask next other s) := by
  funext n
  have h := zero_query_run_agreement ask next oracle other s n
  by_cases hz : (run ask next oracle s n).2 = 0
  · simp only [killedReadout, hz, h.1.mp hz, ↓reduceIte, h.2 hz]
  · have hn : (run ask next other s n).2 ≠ 0 := fun hh => hz (h.1.mpr hh)
    simp only [killedReadout, hz, hn, ↓reduceIte]

section Measurable
variable [Countable Y] [MeasurableSpace Y] [MeasurableSingletonClass Y]
variable [MeasurableSpace S] [MeasurableSpace E]

theorem killedReadout_measurable (readout : S → E) (hm : Measurable readout) (cemetery : E) :
    Measurable (killedReadout readout cemetery) := by
  apply measurable_pi_lambda
  intro n
  apply Measurable.ite
    ((measurableSet_singleton (0 : ℕ)).preimage (measurable_pi_apply n).snd)
  · exact measurable_const.prodMk (hm.comp (measurable_pi_apply n).fst)
  · exact measurable_const

/-- The killed trace law factors through the common initial law alone. -/
theorem killed_traceLaw_factorization
    (ask : S → Bool) (next : S → Y → S)
    (ha : Measurable ask) (hn : ∀ y, Measurable (fun s => next s y))
    (ρ : Measure S) [SFinite ρ] (ν : Measure (Oracle Y)) [IsProbabilityMeasure ν]
    (readout : S → E) (hm : Measurable readout) (cemetery : E) :
    (traceLaw ask next ρ ν).map (killedReadout readout cemetery) =
      ρ.map (fun s => killedReadout readout cemetery (run ask next (fun _ => default) s)) := by
  have hRun := measurable_trajectory ask next ha hn
  have hKill := killedReadout_measurable readout hm cemetery
  have hFixed : Measurable (fun s => killedReadout readout cemetery
      (run ask next (fun _ => default) s)) :=
    hKill.comp (hRun.comp (measurable_id.prodMk measurable_const))
  unfold traceLaw
  rw [Measure.map_map hKill hRun]
  have heq : (fun z : S × Oracle Y =>
      killedReadout readout cemetery (run ask next z.2 z.1)) =
      (fun z : S × Oracle Y => killedReadout readout cemetery (run ask next (fun _ => default) z.1)) := by
    funext z
    exact killedReadout_oracle_independent ask next z.2 (fun _ => default) z.1 readout cemetery
  change (ρ.prod ν).map (fun z => killedReadout readout cemetery (run ask next z.2 z.1)) = _
  rw [heq]
  have hfst : Measurable (Prod.fst : S × Oracle Y → S) := measurable_fst
  calc
    _ = ((ρ.prod ν).map Prod.fst).map
        (fun s => killedReadout readout cemetery (run ask next (fun _ => default) s)) :=
      (Measure.map_map hFixed hfst).symm
    _ = _ := by rw [Measure.map_fst_prod]; simp

/-- Whole infinite killed-readout laws agree, not merely finite cylinder probabilities. -/
theorem killed_traceLaw_eq
    (ask : S → Bool) (next : S → Y → S)
    (ha : Measurable ask) (hn : ∀ y, Measurable (fun s => next s y))
    (ρ : Measure S) [SFinite ρ]
    (ν ν' : Measure (Oracle Y)) [IsProbabilityMeasure ν] [IsProbabilityMeasure ν']
    (readout : S → E) (hm : Measurable readout) (cemetery : E) :
    (traceLaw ask next ρ ν).map (killedReadout readout cemetery) =
      (traceLaw ask next ρ ν').map (killedReadout readout cemetery) := by
  rw [killed_traceLaw_factorization ask next ha hn ρ ν readout hm cemetery,
    killed_traceLaw_factorization ask next ha hn ρ ν' readout hm cemetery]

end Measurable
end HiddenParity.Stochastic
