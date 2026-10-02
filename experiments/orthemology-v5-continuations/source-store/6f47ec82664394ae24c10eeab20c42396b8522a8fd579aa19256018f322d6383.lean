import MealySolver
import TotalVariation

/-! A local, same-input refinement interface. The source carrier need not be
finite, countable, or equipped with a measurable structure. This is separate
from the predecessor's universal-input PER used to compute atomic mass. -/
namespace Orthemology.CertifiedObserver
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open Set MeasureTheory
open scoped ENNReal symmDiff
open P02A2.Q8Measure (fairCantor)

variable {S T : Type*}

/-- At a fixed time the state factors through a finite input word, regardless
of how large or unstructured the state carrier is. -/
theorem state_measurable [MeasurableSpace S] (M : Mealy S) (s : S) (n : ℕ) :
    Measurable (fun x : Cantor => state M s x n) := by
  have hp : Measurable (fun x : Cantor => fun i : Fin n => x i) :=
    measurable_pi_lambda _ (fun i => measurable_pi_apply (i : ℕ))
  have hf := (measurable_of_finite
    (fun w : Fin n → Bool => M.finalState s (List.ofFn w))).comp hp
  convert hf using 1
  funext x
  exact (state_prefix M s x n).symm

/-- No finite-state hypothesis is needed for a synchronous causal output. -/
theorem output_measurable (M : Mealy S) (s : S) : Measurable (output M s) := by
  letI : MeasurableSpace S := ⊤
  apply measurable_pi_lambda
  intro n
  have hp : Measurable (fun x : Cantor => fun i : Fin (n+1) => x i) :=
    measurable_pi_lambda _ (fun i => measurable_pi_apply (i : ℕ))
  have hf := (measurable_of_finite (fun w : Fin (n+1) → Bool =>
    M.out (M.finalState s (List.ofFn (fun i : Fin n => w ⟨i, by omega⟩)))
      (w ⟨n, by omega⟩))).comp hp
  convert hf using 1
  funext x
  change M.out (state M s x n) (x n) = M.out (M.finalState s (pref n x)) (x n)
  rw [state_prefix]

/-- The predecessor's literal law becomes a probability law for any carrier. -/
instance law_probability (M : Mealy S) (s : S) : IsProbabilityMeasure (law M s) := by
  constructor
  rw [law, Measure.map_apply (output_measurable M s) MeasurableSet.univ]
  simp

/-- Same-input relational simulation; it need not identify states or be a function. -/
structure Simulation (C : Mealy S) (A : Mealy T) where
  relates : S → T → Prop
  out_eq : ∀ {s t}, relates s t → ∀ b, C.out s b = A.out t b
  next_rel : ∀ {s t}, relates s t → ∀ b, relates (C.next s b) (A.next t b)

theorem simulation_states {C : Mealy S} {A : Mealy T} (R : Simulation C A)
    {s t} (h : R.relates s t) (x : Cantor) (n : ℕ) :
    R.relates (state C s x n) (state A t x n) := by
  induction n with
  | zero => exact h
  | succ n ih => exact R.next_rel ih (x n)

/-- The whole stream is derived from the local certificate, not a premise. -/
theorem simulation_output {C : Mealy S} {A : Mealy T} (R : Simulation C A)
    {s t} (h : R.relates s t) : output C s = output A t := by
  funext x n
  exact R.out_eq (simulation_states R h x n) (x n)

theorem simulation_law {C : Mealy S} {A : Mealy T} (R : Simulation C A)
    {s t} (h : R.relates s t) : law C s = law A t := by
  unfold law
  rw [simulation_output R h]

/-- Finite computation now applies to an arbitrary-state concrete observer. -/
theorem certified_defect_exact [Fintype T] [DecidableEq T] [Nonempty T]
    {C : Mealy S} {A : Mealy T} (R : Simulation C A) {s t} (h : R.relates s t) :
    (solveDefect A t : ℝ) = P02A2.defect (law C s) := by
  rw [simulation_law R h]
  exact solveDefect_correct A t

/-- A concrete certificate may be a state abstraction, without assuming an
inverse or a finite concrete carrier. -/
def simulationOfMap (C : Mealy S) (A : Mealy T) (α : S → T)
    (hout : ∀ s b, C.out s b = A.out (α s) b)
    (hnext : ∀ s b, α (C.next s b) = A.next (α s) b) : Simulation C A where
  relates s t := α s = t
  out_eq := by intro s t h b; subst t; exact hout s b
  next_rel := by intro s t h b; subst t; exact hnext s b

section Coupling
variable {X Y : Type*} [MeasurableSpace X] [MeasurableSpace Y]

/-- A same-source coupling bound on all measurable events. B is a whole-run
failure event; it is not a per-time discrepancy probability. -/
theorem map_eventTV_le_bad (μ : Measure X) [IsFiniteMeasure μ]
    {f g : X → Y} (hf : Measurable f) (hg : Measurable g)
    (B : Set X) (good : ∀ x, x ∉ B → f x = g x) :
    OrthemologyMeasure.eventTV (μ.map f) (μ.map g) ≤ (μ B).toReal := by
  apply (OrthemologyMeasure.eventTV_le_iff _ _ _).mpr
  intro E hE
  rw [Measure.map_apply hf hE, Measure.map_apply hg hE]
  have hs : (f ⁻¹' E) ∆ (g ⁻¹' E) ⊆ B := by
    intro x hx
    by_contra hn
    have he := good x hn
    simp only [mem_symmDiff, mem_preimage] at hx
    rcases hx with hx | hx
    · exact hx.2 (he ▸ hx.1)
    · exact hx.2 (he.symm ▸ hx.1)
  exact (abs_measureReal_sub_le_measureReal_symmDiff
    (hf hE).nullMeasurableSet (hg hE).nullMeasurableSet).trans
      (ENNReal.toReal_mono (measure_ne_top μ B) (measure_mono hs))
end Coupling

/-- The finite solver approximates the concrete infinite-law defect only
when whole-run disagreement has the given measure bound. -/
theorem certified_defect_error [Fintype T] [DecidableEq T] [Nonempty T]
    (C : Mealy S) (A : Mealy T) (s : S) (t : T) (B : Set Cantor)
    (good : ∀ x, x ∉ B → output C s x = output A t x) :
    |P02A2.defect (law C s) - (solveDefect A t : ℝ)| ≤ (fairCantor B).toReal := by
  rw [solveDefect_correct]
  exact (OrthemologyMeasure.defect_eventTV_bound (law C s) (law A t)).trans
    (map_eventTV_le_bad fairCantor (output_measurable C s) (output_measurable A t) B good)

end Orthemology.CertifiedObserver
