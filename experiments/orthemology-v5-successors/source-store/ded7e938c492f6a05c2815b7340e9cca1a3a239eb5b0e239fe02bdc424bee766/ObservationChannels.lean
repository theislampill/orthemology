import FiniteMealyCompiler

namespace Orthemology.RuntimeBridge
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open Orthemology.CertifiedObserver
open MeasureTheory
open P02A2.Q8Measure (fairCantor)

variable {S : Type*} {N W : ℕ}

/-- Effective numbering supplied as finite data. No Classical.choose. -/
def numberMachine (e : S ≃ Fin N) (M : Mealy S) : Mealy (Fin N) where
  next q b := e (M.next (e.symm q) b)
  out q b := M.out (e.symm q) b

theorem number_state (e : S ≃ Fin N) (M : Mealy S) (s : S) (x : Cantor) (k : ℕ) :
    state (numberMachine e M) (e s) x k = e (state M s x k) := by
  induction k with
  | zero => rfl
  | succ k ih =>
      simp only [state, ih]
      simp [numberMachine]

theorem number_output (e : S ≃ Fin N) (M : Mealy S) (s : S) :
    output (numberMachine e M) (e s) = output M s := by
  funext x k
  simp only [output, number_state]
  simp [numberMachine]

theorem numbered_runtime_output (e : S ≃ Fin N) (M : Mealy S) (s : S) :
    Indexed.runtimeOutput (index (numberMachine e M) (e s)) = output M s := by
  rw [compiled_runtime_output, number_output]

/-- A finite machine with an explicitly encoded vector-valued observation. -/
structure Channels (N W : ℕ) where
  next : Fin N → Bool → Fin N
  observe : Fin N → Bool → Fin W → Bool

def channel (C : Channels N W) (j : Fin W) : Mealy (Fin N) where
  next := C.next
  out q b := C.observe q b j

def channelIndex (C : Channels N W) (s : Fin N) (j : Fin W) : ℕ :=
  index (channel C j) s

/-- All coordinates use the same acquired fair tape. They are not independent
replications of the runtime law. -/
def runtimeChannels (C : Channels N W) (s : Fin N) (x : Cantor) (k : ℕ) (j : Fin W) : Bool :=
  Indexed.runtimeOutput (channelIndex C s j) x k

def idealChannels (C : Channels N W) (s : Fin N) (x : Cantor) (k : ℕ) (j : Fin W) : Bool :=
  output (channel C j) s x k

/-- Exact joint stream equality, retaining correlations across coordinates and
time. Any receipt/acknowledgment decoder must consume this joint stream. -/
theorem runtime_channels_exact (C : Channels N W) (s : Fin N) :
    runtimeChannels C s = idealChannels C s := by
  funext x k j
  exact congrFun (congrFun (compiled_runtime_output (channel C j) s) x) k

theorem runtime_channels_law (C : Channels N W) (s : Fin N) :
    fairCantor.map (runtimeChannels C s) = fairCantor.map (idealChannels C s) := by
  rw [runtime_channels_exact]

/-- A readout is transported only after its explicit vector encoding has been
identified on the same input. This includes joint full-history observations. -/
theorem runtime_channels_measurable (C : Channels N W) (s : Fin N) :
    Measurable (runtimeChannels C s) := by
  apply measurable_pi_lambda
  intro k
  apply measurable_pi_lambda
  intro j
  exact (measurable_pi_apply k).comp (Indexed.runtime_output_measurable (channelIndex C s j))

theorem decoded_runtime_probability {Ω : Type*} [MeasurableSpace Ω]
    (C : Channels N W) (s : Fin N) (decode : (ℕ → Fin W → Bool) → Ω)
    (hdecode : Measurable decode) :
    IsProbabilityMeasure (fairCantor.map (fun x => decode (runtimeChannels C s x))) := by
  constructor
  change (fairCantor.map (decode ∘ runtimeChannels C s)) Set.univ = 1
  rw [Measure.map_apply (hdecode.comp (runtime_channels_measurable C s)) MeasurableSet.univ]
  simp

theorem decoded_runtime_law {Ω : Type*} [MeasurableSpace Ω]
    (C : Channels N W) (s : Fin N) (decode : (ℕ → Fin W → Bool) → Ω)
    (_hdecode : Measurable decode) :
    fairCantor.map (fun x => decode (runtimeChannels C s x)) =
      fairCantor.map (fun x => decode (idealChannels C s x)) := by
  rw [runtime_channels_exact]

end Orthemology.RuntimeBridge
