import UniformRuntimeTrace
import ContextualFixtures

namespace IndependentSourceRuntimeControls
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open Orthemology.CertifiedObserver
open P02A2.Q8Machine
open ParsedQ8

def delayHalt : Machine 2 := fun pc => if pc=0 then .inc 0 1 else .halt

theorem first_tick_precedes_halt (x : Cantor) :
    output (Q8.observer delayHalt) (initial 2 (by decide)) x 0 = false := rfl

theorem second_tick_reads_current_bit (x : Cantor) :
    output (Q8.observer delayHalt) (initial 2 (by decide)) x 1 = x 1 := rfl

theorem source_bytes_roundtrip :
    P02.Codec.decodeBytes (P02.Codec.encodeBytes (packed delayHalt)) = some (packed delayHalt) :=
  generated_bytes_exact delayHalt

theorem source_index_roundtrip : P02.Codec.decodeIndex (code delayHalt) = some (packed delayHalt) :=
  decoded_source_exact delayHalt

theorem malformed_empty_bytes : P02.Codec.decodeBytes [] = none := rfl

theorem no_timeout_bit (x : Cantor) (k : ℕ) : runtimeTick 0 delayHalt x k = none :=
  ParsedQ8.Fixtures.zero_fuel_is_not_zero delayHalt x k

theorem successful_tick_is_source_tick (f : ℕ) (x : Cantor) (k : ℕ) (b : Bool)
    (h : runtimeTick f delayHalt x k = some b) :
    b = output (Q8.observer delayHalt) (initial 2 (by decide)) x k :=
  runtime_tick_sound delayHalt (by decide) f x k b h

theorem chosen_horizon_uniform (N : ℕ) (x : Cantor) (k : ℕ) (hk : k<N) :
    runtimeTick (uniformFuel delayHalt (by decide) N) delayHalt x k =
      some (output (Q8.observer delayHalt) (initial 2 (by decide)) x k) :=
  uniform_runtime_trace delayHalt (by decide) N _ le_rfl x k hk

theorem no_horizon_zero_tick : ¬ (0 < (0:ℕ)) := Nat.lt_irrefl 0

theorem prefix_cutoff_is_strict :
    inputWord (extendBits (fun (_ : Fin 0) => false)) 0 ≠ inputWord (fun _ => true) 0 := by decide

theorem old_clock_loses_real_first_output :
    output (Q8.Fixtures.wrongClock Q8.Fixtures.haltNow) (initial 1 (by decide)) (fun _ => true) 0 ≠
      output (Q8.observer Q8.Fixtures.haltNow) (initial 1 (by decide)) (fun _ => true) 0 := by decide

theorem actual_counter_is_unbounded (k : ℕ) :
    (run Q8.Fixtures.grow (by decide) k).counter 0 = k :=
  (Q8.Fixtures.grow_run_unbounded k).2

theorem concrete_carriers_differ :
    Fintype.card (ContextFixtures.observer.State (ContextFixtures.iSub.map ())) ≠
      Fintype.card (ContextFixtures.observer.State (ContextFixtures.iiSub.map ())) := by
  rw [ContextFixtures.genuinely_different_state_carriers.1,ContextFixtures.genuinely_different_state_carriers.2]
  decide

#eval runtimeTick 0 delayHalt (fun _ => true) 0
#eval runtimeTick 500 delayHalt (fun _ => true) 0
#eval runtimeTick 500 delayHalt (fun _ => true) 1
#eval runtimeTick 500 delayHalt (fun _ => false) 1
#eval uniformFuel delayHalt (by decide) 0
#eval uniformFuel delayHalt (by decide) 2
end IndependentSourceRuntimeControls
