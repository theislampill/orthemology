import Stability

/-! Computational definitions are outside classical sections. Only their
correctness proofs use the frozen mathematical recurrence. -/
namespace GuardedTree.Executable
open Saturation
variable {J E R : Type*} [DecidableEq E] (G : Grammar J E R) [Fintype R]

/-- Explicit finite enumeration; does not use the predecessor's classical
`Fintype (RuleChoice G)` instance. Empty arity has one empty ordered tuple. -/
def choices : Finset (RuleChoice G) :=
  Finset.univ.sigma fun r => Fintype.piFinset fun _ : Fin (G.arity r) =>
    (grammarSupport G).powerset.attach

theorem mem_choices (x : RuleChoice G) : x ∈ choices G := by
  simp [choices]

section Decidable
variable [DecidableEq J] [gd : ∀ r s, Decidable (G.guard r s)]

instance enabledDecidable (D : Table (J := J) (E := E)) (x : RuleChoice G) :
    Decidable (enabled G D x) :=
  inferInstanceAs (Decidable ((∀ i, (D (G.premise x.1 i) (x.2 i).val).isSome) ∧
    G.guard x.1 (fun i => (x.2 i).val)))

/-- Retains the old exact key and evaluates all enabled ordered rule tuples. -/
def candidates (D : Table (J := J) (E := E)) (q : J) (S : Finset E) : Finset ℚ :=
  (D q S).toFinset ∪
    (((choices G).filter (fun x =>
      enabled G D x ∧ G.head x.1 = q ∧ outputSupport G x = S)).image (outputCost G D))

/-- Computational finite minimum: decidable nonemptiness and rational order. -/
def minimum (A : Finset ℚ) : Option ℚ :=
  if h : A.Nonempty then some (A.min' h) else none

def step (D : Table (J := J) (E := E)) : Table (J := J) (E := E) :=
  fun q S => minimum (candidates G D q S)

def round : ℕ → Table (J := J) (E := E)
  | 0 => fun _ _ => none
  | h + 1 => step G (round h)

theorem candidates_eq (D : Table (J := J) (E := E)) (q : J) (S : Finset E) :
    candidates G D q S = Saturation.candidates G D q S := by
  classical
  have hc : choices G = Finset.univ := Finset.eq_univ_of_forall (mem_choices G)
  ext c
  simp [candidates, Saturation.candidates, hc]

theorem minimum_eq (A : Finset ℚ) : minimum A = Saturation.minimum A := by
  classical
  simp only [minimum, Saturation.minimum]

theorem step_eq (D : Table (J := J) (E := E)) : step G D = Saturation.step G D := by
  funext q S
  simp only [step, Saturation.step, candidates_eq, minimum_eq]

theorem round_eq (h : ℕ) : round G h = Saturation.round G h := by
  induction h with
  | zero => rfl
  | succ h ih => simp only [round, Saturation.round, ih, step_eq]

#print axioms candidates_eq
#print axioms round_eq
end Decidable
end GuardedTree.Executable
