import GenericFiniteQueryMeasure

noncomputable section
open MeasureTheory ProbabilityTheory Finset
open scoped BigOperators

namespace Orthemology.Tranche2.PolicyEmbedding
variable {R A Y : Type*} [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y]

abbrev History (A Y : Type*) := List (A × Y)
abbrev Stack (A Y : Type*) := A → ℕ → Y
abbrev EvalState (R A Y : Type*) := R × (Stack A Y × History A Y)

/-- The policy reads only its private seed and observed history, never a fresh
row or a future stack entry. Histories are stored newest first. -/
def selected (π : R → History A Y → A) (s : EvalState R A Y) : A := π s.1 s.2.2

def query (U : Finset A) (π : R → History A Y → A) (s : EvalState R A Y) : Bool :=
  decide (selected π s ∉ U)

def actionCount (a : A) (h : History A Y) : ℕ := h.countP (fun ay => ay.1 = a)

def step (U : Finset A) (π : R → History A Y → A) (s : EvalState R A Y) (row : A → Y) : EvalState R A Y :=
  let a := selected π s
  let y := if query U π s then row a else s.2.1 a (actionCount a s.2.2)
  (s.1, (s.2.1, (a,y)::s.2.2))

omit [Fintype A] [Fintype Y] [Inhabited Y] in
lemma step_preserves_seed (U : Finset A) (π : R → History A Y → A) (s : EvalState R A Y) (row : A → Y) :
    (step U π s row).1 = s.1 ∧ (step U π s row).2.1 = s.2.1 := ⟨rfl,rfl⟩

omit [Fintype A] [Fintype Y] [Inhabited Y] in
lemma step_history_length (U : Finset A) (π : R → History A Y → A) (s : EvalState R A Y) (row : A → Y) :
    (step U π s row).2.2.length = s.2.2.length + 1 := rfl

omit [Fintype A] [Fintype Y] [Inhabited Y] in
/-- Unqueried rows are completely ignored on U-actions. -/
theorem step_inside_row_independent (U : Finset A) (π : R → History A Y → A)
    (s : EvalState R A Y) (hU : selected π s ∈ U) (row other : A → Y) :
    step U π s row = step U π s other := by simp [step,query,hU]

omit [Fintype A] [Fintype Y] [Inhabited Y] in
/-- A query exports only the chosen coordinate, not the counterfactual row. -/
theorem step_outside_coordinate_only (U : Finset A) (π : R → History A Y → A)
    (s : EvalState R A Y) (hU : selected π s ∉ U) (row other : A → Y)
    (heq : row (selected π s) = other (selected π s)) : step U π s row = step U π s other := by
  simp [step,query,hU,heq]

def policyRun (U : Finset A) (π : R → History A Y → A) (oracle : ℕ → A → Y)
    (seed : R) (X : Stack A Y) :=
  FiniteAlphabetQuery.run (query U π) (step U π) oracle (seed,(X,[]))

def actionAt (U : Finset A) (π : R → History A Y → A) (oracle : ℕ → A → Y)
    (seed : R) (X : Stack A Y) (n : ℕ) : A := selected π (policyRun U π oracle seed X n).1

omit [Fintype A] [Fintype Y] in
/-- Exact P6: the generic query counter is the number of outside-U actions
actually selected before n. It is not an unrelated abstract resource counter. -/
theorem query_counter_eq_outside_actions (U : Finset A) (π : R → History A Y → A)
    (oracle : ℕ → A → Y) (seed : R) (X : Stack A Y) (n : ℕ) :
    (policyRun U π oracle seed X n).2 =
      ∑ t ∈ Finset.range n, if actionAt U π oracle seed X t ∉ U then 1 else 0 := by
  induction n with
  | zero => simp [policyRun,FiniteAlphabetQuery.run]
  | succ n ih =>
    rw [Finset.sum_range_succ]
    change (FiniteAlphabetQuery.advance (query U π) (step U π) oracle
      (policyRun U π oracle seed X n)).2 = _
    simp only [actionAt] at ih ⊢
    by_cases h : selected π (policyRun U π oracle seed X n).1 ∉ U
    · simp [FiniteAlphabetQuery.advance,query,h,ih]
    · simp [FiniteAlphabetQuery.advance,query,h,ih]

section Measurable
variable [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
  [MeasurableSpace Y] [MeasurableSingletonClass Y]

instance historyMeasurableSpace : MeasurableSpace (History A Y) := ⊤
instance : MeasurableSingletonClass (History A Y) := ⟨fun _ => trivial⟩

omit [Fintype A] [Fintype Y] [DecidableEq A] [Inhabited Y] [MeasurableSingletonClass A] [MeasurableSingletonClass Y] in
lemma selected_measurable (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) : Measurable (selected π) :=
  hπ.comp (measurable_fst.prodMk measurable_snd.snd)

omit [Fintype Y] [Inhabited Y] [MeasurableSingletonClass Y] in
lemma query_measurable (U : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) : Measurable (query U π) := by
  exact (measurable_of_countable (fun a : A => decide (a ∉ U))).comp (selected_measurable π hπ)

omit [Inhabited Y] in
/-- Exact P2: the row evaluator satisfies the generic primitive's measurability
contract, even for an arbitrary measurable private-seed space. -/
theorem step_measurable (U : Finset A) (π : R → History A Y → A)
    (hπ : Measurable (fun z : R × History A Y => π z.1 z.2)) (row : A → Y) :
    Measurable (fun s => step U π s row) := by
  have ha := selected_measurable π hπ
  have hcount : Measurable (fun s : EvalState R A Y => actionCount (selected π s) s.2.2) :=
    (measurable_of_countable (fun z : A × History A Y => actionCount z.1 z.2)).comp
      (ha.prodMk measurable_snd.snd)
  have heval : Measurable (fun z : Stack A Y × (A × ℕ) => z.1 z.2.1 z.2.2) :=
    measurable_from_prod_countable (fun an => (measurable_pi_apply an.2).comp (measurable_pi_apply an.1))
  have hstack : Measurable (fun s : EvalState R A Y => s.2.1 (selected π s) (actionCount (selected π s) s.2.2)) :=
    heval.comp (measurable_snd.fst.prodMk (ha.prodMk hcount))
  have hrow : Measurable (fun s : EvalState R A Y => row (selected π s)) :=
    (measurable_of_countable row).comp ha
  have hq := query_measurable U π hπ
  have hy : Measurable (fun s : EvalState R A Y => if query U π s then row (selected π s)
      else s.2.1 (selected π s) (actionCount (selected π s) s.2.2)) :=
    Measurable.ite ((measurableSet_singleton true).preimage hq) hrow hstack
  have hhist : Measurable (fun s : EvalState R A Y =>
      (selected π s, if query U π s then row (selected π s)
      else s.2.1 (selected π s) (actionCount (selected π s) s.2.2))::s.2.2) :=
    (measurable_of_countable (fun z : (A × Y) × History A Y => z.1::z.2)).comp
      ((ha.prodMk hy).prodMk measurable_snd.snd)
  exact measurable_fst.prodMk (measurable_snd.fst.prodMk hhist)

end Measurable
end Orthemology.Tranche2.PolicyEmbedding
