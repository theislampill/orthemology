import ParsedObserverAbstraction

/-! A terminating executable search for one stack-fuel budget covering every
input stream through a fixed finite horizon. No uniform infinite-horizon fuel
or wall-clock bound follows. -/
namespace Orthemology.CertifiedObserver.ParsedQ8
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open P02A2.Q8Machine P02.Codec.UniformComputability

def extendBits {N : ℕ} (w : Fin N → Bool) : Cantor :=
  fun i => if h : i < N then w ⟨i,h⟩ else false

def completeThrough {n : ℕ} (M : Machine n) (N fuel : ℕ) : Prop :=
  ∀ w : Fin N → Bool, ∀ k : Fin N, (runtimeTick fuel M (extendBits w) k).isSome = true

instance completeThrough_decidable {n : ℕ} (M : Machine n) (N fuel : ℕ) :
    Decidable (completeThrough M N fuel) := by
  unfold completeThrough
  infer_instance

theorem runtime_tick_mono {n : ℕ} (M : Machine n) {fuel more : ℕ} (hle : fuel ≤ more)
    (x : Cantor) (k : ℕ) {b : Bool} (h : runtimeTick fuel M x k = some b) :
    runtimeTick more M x k = some b := by
  obtain ⟨v,hv,hb⟩ := Option.map_eq_some_iff.mp h
  unfold runtimeTick
  rw [evaluateIndexFuel_mono hle hv]
  exact congrArg some hb

theorem exists_completeThrough {n : ℕ} (M : Machine n) (hn : 0 < n) (N : ℕ) :
    ∃ fuel, completeThrough M N fuel := by
  classical
  let I := (Fin N → Bool) × Fin N
  have hex : ∀ z : I, ∃ f, ∀ more, f ≤ more →
      runtimeTick more M (extendBits z.1) z.2 =
        some (output (Q8.observer M) (initial n hn) (extendBits z.1) z.2) :=
    fun z => runtime_tick_complete M hn (extendBits z.1) z.2
  choose f hf using hex
  refine ⟨Finset.univ.sup f, ?_⟩
  intro w k
  have hb : f (w,k) ≤ Finset.univ.sup f := Finset.le_sup (Finset.mem_univ (w,k))
  rw [hf (w,k) _ hb]
  rfl

/-- Finite search over the actual parser/stack runtime. Every tested
completion predicate is decidable by finite computation. -/
def uniformFuel {n : ℕ} (M : Machine n) (hn : 0 < n) (N : ℕ) : ℕ :=
  Nat.find (exists_completeThrough M hn N)

theorem uniformFuel_complete {n : ℕ} (M : Machine n) (hn : 0 < n) (N : ℕ) :
    completeThrough M N (uniformFuel M hn N) := Nat.find_spec _

theorem inputWord_extend_prefix (x : Cantor) {N k : ℕ} (hk : k < N) :
    inputWord (extendBits (fun i : Fin N => x i)) k = inputWord x k := by
  unfold inputWord
  congr 2
  funext i
  simp [extendBits, show i.val < N by omega]

/-- The actual finite search budget works uniformly for every input stream
at every earlier logical tick, and successful extra fuel preserves the bits. -/
theorem uniform_runtime_trace {n : ℕ} (M : Machine n) (hn : 0 < n) (N more : ℕ)
    (hm : uniformFuel M hn N ≤ more) (x : Cantor) (k : ℕ) (hk : k < N) :
    runtimeTick more M x k = some (output (Q8.observer M) (initial n hn) x k) := by
  have h := uniformFuel_complete M hn N (fun i : Fin N => x i) ⟨k,hk⟩
  have he : runtimeTick (uniformFuel M hn N) M (extendBits (fun i : Fin N => x i)) k =
      runtimeTick (uniformFuel M hn N) M x k := by
    unfold runtimeTick
    rw [inputWord_extend_prefix x hk]
  rw [he] at h
  obtain ⟨b,hb⟩ := Option.isSome_iff_exists.mp h
  have hs := runtime_tick_sound M hn _ x k b hb
  rw [hs] at hb
  exact runtime_tick_mono M hm x k hb

namespace Fixtures
open Q8.Fixtures
#eval uniformFuel haltNow (by decide) 1
#eval uniformFuel grow (by decide) 1
end Fixtures
end Orthemology.CertifiedObserver.ParsedQ8
