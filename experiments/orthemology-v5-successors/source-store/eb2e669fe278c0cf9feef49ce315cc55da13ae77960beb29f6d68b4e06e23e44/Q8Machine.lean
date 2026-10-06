import Q8Measure

/-! Finite typed two-counter machines with the instruction set of the recovered
P02-L1 compile_q8 implementation. Jump validity is represented by Fin n and
counter validity by Fin 2. These statements connect actual bounded execution
to actual fair-Cantor law; byte-code compiler refinement is a separate target. -/
namespace P02A2.Q8Machine
open P02A2.Q8Measure

inductive Instruction (n : ℕ) where
  | halt : Instruction n
  | inc : Fin 2 → Fin n → Instruction n
  | dec : Fin 2 → Fin n → Fin n → Instruction n
  deriving DecidableEq, Repr

abbrev Machine (n : ℕ) := Fin n → Instruction n

structure Config (n : ℕ) where
  pc : Fin n
  counter : Fin 2 → ℕ
  halted : Bool

def initial (n : ℕ) (hn : 0 < n) : Config n := ⟨⟨0, hn⟩, fun _ => 0, false⟩

def execute {n : ℕ} (instruction : Instruction n) (s : Config n) : Config n :=
  match instruction with
  | .halt => { s with halted := true }
  | .inc r next => { s with pc := next, counter := Function.update s.counter r (s.counter r + 1) }
  | .dec r zero next =>
      if s.counter r = 0 then { s with pc := zero }
      else { s with pc := next, counter := Function.update s.counter r (s.counter r - 1) }

def step {n : ℕ} (M : Machine n) (s : Config n) : Config n :=
  if s.halted then s else execute (M s.pc) s

def run {n : ℕ} (M : Machine n) (hn : 0 < n) : ℕ → Config n
  | 0 => initial n hn
  | k+1 => step M (run M hn k)

/-- Exactly n+1 inspected instructions, including immediate halt at output stage 0. -/
def boundedFlag {n : ℕ} (M : Machine n) (hn : 0 < n) (stage : ℕ) : Bool :=
  (run M hn (stage+1)).halted

def Halts {n : ℕ} (M : Machine n) (hn : 0 < n) : Prop :=
  ∃ k, (run M hn k).halted = true

theorem step_of_halted {n : ℕ} (M : Machine n) (s : Config n) (h : s.halted = true) :
    step M s = s := by simp [step, h]

theorem run_zero_not_halted {n : ℕ} (M : Machine n) (hn : 0 < n) :
    (run M hn 0).halted = false := rfl

theorem run_halted_persistent {n : ℕ} (M : Machine n) (hn : 0 < n) {k l : ℕ}
    (hk : (run M hn k).halted = true) (hkl : k ≤ l) :
    (run M hn l).halted = true := by
  induction l, hkl using Nat.le_induction with
  | base => exact hk
  | succ l hkl ih =>
      rw [run, step_of_halted M _ ih]
      exact ih

theorem boundedFlag_persistent {n : ℕ} (M : Machine n) (hn : 0 < n) {k l : ℕ}
    (hk : boundedFlag M hn k = true) (hkl : k ≤ l) : boundedFlag M hn l = true := by
  exact run_halted_persistent M hn hk (Nat.add_le_add_right hkl 1)

theorem halts_iff_boundedFlag {n : ℕ} (M : Machine n) (hn : 0 < n) :
    Halts M hn ↔ ∃ k, boundedFlag M hn k = true := by
  constructor
  · rintro ⟨k, hk⟩
    exact ⟨k, run_halted_persistent M hn hk (Nat.le_succ k)⟩
  · rintro ⟨k, hk⟩
    exact ⟨k+1, hk⟩

theorem not_halts_flags_false {n : ℕ} (M : Machine n) (hn : 0 < n)
    (h : ¬ Halts M hn) : ∀ k, boundedFlag M hn k = false := by
  intro k
  cases hk : boundedFlag M hn k
  · rfl
  · exact (h ((halts_iff_boundedFlag M hn).mpr ⟨k, hk⟩)).elim

theorem halts_eventually_flags_true {n : ℕ} (M : Machine n) (hn : 0 < n)
    (h : Halts M hn) : ∃ k, ∀ l, k ≤ l → boundedFlag M hn l = true := by
  rcases (halts_iff_boundedFlag M hn).mp h with ⟨k, hk⟩
  exact ⟨k, fun l hkl => boundedFlag_persistent M hn hk hkl⟩

noncomputable def outputLaw {n : ℕ} (M : Machine n) (hn : 0 < n) :=
  Q8Measure.law (boundedFlag M hn)

theorem nonhalting_law_dirac {n : ℕ} (M : Machine n) (hn : 0 < n)
    (h : ¬ Halts M hn) : outputLaw M hn = MeasureTheory.Measure.dirac (fun _ : ℕ => false) :=
  never_law_dirac _ (not_halts_flags_false M hn h)

theorem nonhalting_defect_zero {n : ℕ} (M : Machine n) (hn : 0 < n)
    (h : ¬ Halts M hn) : defect (outputLaw M hn) = 0 :=
  never_defect_zero _ (not_halts_flags_false M hn h)

theorem halting_singletons_zero {n : ℕ} (M : Machine n) (hn : 0 < n)
    (h : Halts M hn) (y : Cantor) : outputLaw M hn {y} = 0 := by
  rcases halts_eventually_flags_true M hn h with ⟨k, hk⟩
  exact eventually_singleton_zero _ k hk y

theorem halting_defect_one {n : ℕ} (M : Machine n) (hn : 0 < n)
    (h : Halts M hn) : defect (outputLaw M hn) = 1 := by
  rcases halts_eventually_flags_true M hn h with ⟨k, hk⟩
  exact eventually_defect_one _ k hk

theorem defect_zero_iff_nonhalting {n : ℕ} (M : Machine n) (hn : 0 < n) :
    defect (outputLaw M hn) = 0 ↔ ¬ Halts M hn := by
  constructor
  · intro hz hh
    have ho := halting_defect_one M hn hh
    linarith
  · exact nonhalting_defect_zero M hn

theorem defect_one_iff_halting {n : ℕ} (M : Machine n) (hn : 0 < n) :
    defect (outputLaw M hn) = 1 ↔ Halts M hn := by
  constructor
  · intro ho
    by_contra hh
    have hz := nonhalting_defect_zero M hn hh
    linarith
  · exact halting_defect_one M hn

end P02A2.Q8Machine
