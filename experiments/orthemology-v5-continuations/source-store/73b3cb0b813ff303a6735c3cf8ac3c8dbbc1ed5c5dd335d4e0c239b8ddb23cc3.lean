import IndexedObserver
import UniformRuntimeTrace

namespace Orthemology.CertifiedObserver.Indexed
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open P02.Codec P02.Codec.UniformComputability
open Set MeasureTheory
open P02A2.Q8Measure (fairCantor)
open ParsedQ8 (inputWord extendBits inputWord_extend_prefix)

/-- The actual numeric-index explicit-stack runtime. -/
def tick (fuel index : ℕ) (x : Cantor) (k : ℕ) : Option Bool :=
  (evaluateIndexFuel fuel index k (inputWord x k)).map (fun v => decide (v % 2 = 1))

theorem tick_sound {fuel index : ℕ} {x : Cantor} {k : ℕ} {b : Bool}
    (h : tick fuel index x k = some b) : b = output (machine index) initial x k := by
  obtain ⟨v,hv,hb⟩ := Option.map_eq_some_iff.mp h
  have he := evaluateIndexFuel_sound hv
  subst v
  rw [source_output_exact]
  exact hb.symm

theorem tick_complete (index : ℕ) (x : Cantor) (k : ℕ) :
    ∃ fuel, ∀ more, fuel ≤ more → tick more index x k = some (output (machine index) initial x k) := by
  obtain ⟨f,hf⟩ := evaluateIndexFuel_eventually index k (inputWord x k)
  refine ⟨f, fun more hm => ?_⟩
  unfold tick
  rw [hf more hm, source_output_exact]
  rfl

def searchTick (index : ℕ) (x : Cantor) (k : ℕ) : Part Bool :=
  (evaluateIndexSearch index k (inputWord x k)).map (fun v => decide (v % 2 = 1))

theorem search_tick_exact (index : ℕ) (x : Cantor) (k : ℕ) :
    searchTick index x k = Part.some (output (machine index) initial x k) := by
  unfold searchTick
  rw [evaluateIndexSearch_exact, source_output_exact]
  rfl

theorem tick_mono {fuel more index : ℕ} (hle : fuel ≤ more)
    {x : Cantor} {k : ℕ} {b : Bool} (h : tick fuel index x k = some b) :
    tick more index x k = some b := by
  obtain ⟨v,hv,hb⟩ := Option.map_eq_some_iff.mp h
  unfold tick
  rw [evaluateIndexFuel_mono hle hv]
  exact congrArg some hb

def completeThrough (index N fuel : ℕ) : Prop :=
  ∀ w : Fin N → Bool, ∀ k : Fin N, (tick fuel index (extendBits w) k).isSome = true

instance completeThrough_decidable (index N fuel : ℕ) :
    Decidable (completeThrough index N fuel) := by unfold completeThrough; infer_instance

theorem exists_completeThrough (index N : ℕ) : ∃ fuel, completeThrough index N fuel := by
  classical
  let I := (Fin N → Bool) × Fin N
  have hex : ∀ z : I, ∃ f, ∀ more, f ≤ more →
      tick more index (extendBits z.1) z.2 =
        some (output (machine index) initial (extendBits z.1) z.2) :=
    fun z => tick_complete index (extendBits z.1) z.2
  choose f hf using hex
  refine ⟨Finset.univ.sup f, ?_⟩
  intro w k
  have hb : f (w,k) ≤ Finset.univ.sup f := Finset.le_sup (Finset.mem_univ (w,k))
  rw [hf (w,k) _ hb]
  rfl

/-- Executable exhaustive search on the literal decoded runtime. -/
def uniformFuel (index N : ℕ) : ℕ := Nat.find (exists_completeThrough index N)

theorem uniformFuel_complete (index N : ℕ) : completeThrough index N (uniformFuel index N) :=
  Nat.find_spec _

theorem uniform_tick (index N more : ℕ) (hm : uniformFuel index N ≤ more)
    (x : Cantor) (k : ℕ) (hk : k < N) :
    tick more index x k = some (output (machine index) initial x k) := by
  have h := uniformFuel_complete index N (fun i : Fin N => x i) ⟨k,hk⟩
  have he : tick (uniformFuel index N) index (extendBits (fun i : Fin N => x i)) k =
      tick (uniformFuel index N) index x k := by
    unfold tick
    rw [inputWord_extend_prefix x hk]
  rw [he] at h
  obtain ⟨b,hb⟩ := Option.isSome_iff_exists.mp h
  have hs := tick_sound hb
  rw [hs] at hb
  exact tick_mono hm hb

/-- A predetermined per-stage fuel schedule, independent of the input stream.
Each tick is proved successful before its optional result is projected. -/
def runtimeOutput (index : ℕ) (x : Cantor) (k : ℕ) : Bool :=
  (tick (uniformFuel index (k+1)) index x k).getD false

theorem scheduled_tick_success (index : ℕ) (x : Cantor) (k : ℕ) :
    tick (uniformFuel index (k+1)) index x k = some (output (machine index) initial x k) :=
  uniform_tick index (k+1) _ (le_refl _) x k (Nat.lt_succ_self k)

/-- No whole-run termination hypothesis, free initializer, or hidden law
transfer premise remains: the actual scheduled bits form exactly the source stream. -/
theorem runtime_output_exact (index : ℕ) : runtimeOutput index = output (machine index) initial := by
  funext x k
  simp only [runtimeOutput, scheduled_tick_success, Option.getD_some]

theorem runtime_output_measurable (index : ℕ) : Measurable (runtimeOutput index) := by
  rw [runtime_output_exact]
  exact output_measurable _ _

theorem runtime_law_exact (index : ℕ) : fairCantor.map (runtimeOutput index) = sourceLaw index := by
  rw [runtime_output_exact, source_law_exact]
  rfl

theorem runtime_finite_solver (index : ℕ)
    {T : Type*} [Fintype T] [DecidableEq T] [Nonempty T] (A : Mealy T)
    (R : Simulation (machine index) A) (t : T) (h : R.relates initial t) :
    (solveDefect A t : ℝ) = P02A2.defect (fairCantor.map (runtimeOutput index)) := by
  rw [runtime_law_exact]
  exact certified_index_defect index A R t h

end Orthemology.CertifiedObserver.Indexed
