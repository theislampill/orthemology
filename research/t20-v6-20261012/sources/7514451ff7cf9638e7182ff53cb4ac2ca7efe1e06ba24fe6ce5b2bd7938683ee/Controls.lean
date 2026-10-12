import GuardedTree
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum

/-! Kernel-checked finite controls for ordered exact-support replacement.
The licence needs alpha in position 0 and beta in position 1, and nothing else.
No monotonicity of the guard is available. -/
namespace GuardedTree.Controls

inductive Judgement | claim | licensed deriving DecidableEq
inductive Root | alpha | beta | extra deriving DecidableEq
inductive Rule | alpha | beta | empty | pad | enlarge | licence deriving DecidableEq

instance : Fintype Judgement := ⟨{.claim, .licensed}, by intro j; cases j <;> simp⟩
instance : Fintype Root := ⟨{.alpha, .beta, .extra}, by intro e; cases e <;> simp⟩
instance : Fintype Rule := ⟨{.alpha, .beta, .empty, .pad, .enlarge, .licence}, by intro r; cases r <;> simp⟩

theorem univ_fin_two : (Finset.univ : Finset (Fin 2)) = {0, 1} := by decide

abbrev arity : Rule → ℕ
  | .pad => 1
  | .enlarge => 1
  | .licence => 2
  | _ => 0

abbrev grammar : Grammar Judgement Root Rule where
  arity := arity
  head r := match r with | .licence => .licensed | _ => .claim
  premise _ _ := .claim
  localSupport r := match r with
    | .alpha => {.alpha}
    | .beta => {.beta}
    | .enlarge => {.extra}
    | _ => ∅
  price r := match r with | .pad => 2 | _ => 1
  guard r := match r with
    | .licence => fun s => s 0 = {.alpha} ∧ s 1 = {.beta}
    | _ => fun _ => True

abbrev T := Tree grammar

def alpha : T := .node .alpha Fin.elim0
def beta : T := .node .beta Fin.elim0
def empty : T := .node .empty Fin.elim0
def paddedAlpha : T := .node .pad (fun _ => alpha)
def enlargedAlpha : T := .node .enlarge (fun _ => alpha)
def pair (a b : T) : Fin 2 → T := fun i => if i = 0 then a else b
def licensed (a b : T) : T := .node .licence (pair a b)
def licenceContext : Context grammar :=
  .step .licence 0 (pair empty beta) .hole

@[simp] theorem alpha_valid : Tree.Valid grammar alpha := by
  simp [alpha, Tree.Valid, grammar, arity]
@[simp] theorem beta_valid : Tree.Valid grammar beta := by
  simp [beta, Tree.Valid, grammar, arity]
@[simp] theorem empty_valid : Tree.Valid grammar empty := by
  simp [empty, Tree.Valid, grammar, arity]
@[simp] theorem paddedAlpha_valid : Tree.Valid grammar paddedAlpha := by
  simp [paddedAlpha, Tree.Valid, grammar, arity, alpha, Tree.judgement]
@[simp] theorem alpha_support : Tree.support grammar alpha = {Root.alpha} := by
  simp [alpha, Tree.support, grammar, arity]
@[simp] theorem beta_support : Tree.support grammar beta = {Root.beta} := by
  simp [beta, Tree.support, grammar, arity]
@[simp] theorem empty_support : Tree.support grammar empty = ∅ := by
  simp [empty, Tree.support, grammar, arity]
@[simp] theorem paddedAlpha_support :
    Tree.support grammar paddedAlpha = {Root.alpha} := by
  simp [paddedAlpha, Tree.support, grammar, arity, alpha]

/-- A genuine nonmonotone guard: adding a root in one position disables it. -/
theorem guard_not_upward_closed :
    ∃ s t : Fin 2 → Finset Root,
      (∀ i, s i ⊆ t i) ∧ grammar.guard .licence s ∧
      ¬ grammar.guard .licence t := by
  let s : Fin 2 → Finset Root := fun i => if i = 0 then {.alpha} else {.beta}
  let t : Fin 2 → Finset Root := fun i => if i = 0 then {.alpha, .extra} else {.beta}
  refine ⟨s, t, ?_, ?_, ?_⟩
  · intro i; fin_cases i <;> simp [s, t]
  · simp [grammar, s]
  · simp [grammar, t, Finset.ext_iff]

theorem original_valid : Tree.Valid grammar (licensed paddedAlpha beta) := by
  simp [licensed, Tree.Valid, grammar, arity, pair, Fin.forall_fin_two,
    paddedAlpha, alpha, beta, Tree.judgement, Tree.support]

theorem context_fills (a : T) :
    Context.fill grammar licenceContext a = licensed a beta := by
  change Tree.node Rule.licence _ = Tree.node Rule.licence _
  congr 1
  funext i
  fin_cases i <;> simp [Context.fill, licenceContext, licensed, pair]

/-- The replacement theorem is actually instantiated through a nonempty context. -/
theorem same_support_replacement :
    Tree.Valid grammar (licensed alpha beta) ∧
    Tree.judgement grammar (licensed alpha beta) =
      Tree.judgement grammar (licensed paddedAlpha beta) ∧
    Tree.support grammar (licensed alpha beta) =
      Tree.support grammar (licensed paddedAlpha beta) := by
  have h := context_replacement grammar licenceContext paddedAlpha alpha
    (by rw [context_fills]; exact original_valid) alpha_valid
    (by rfl) (by simp)
  simpa only [context_fills] using h

theorem replacement_different_shape : alpha ≠ paddedAlpha := by
  intro h
  have hnodes := congrArg (Tree.nodes grammar) h
  norm_num [alpha, paddedAlpha, Tree.nodes, grammar, arity] at hnodes

theorem replacement_strictly_cheaper :
    Tree.cost grammar (licensed alpha beta) <
      Tree.cost grammar (licensed paddedAlpha beta) := by
  change (1 + ∑ i : Fin 2, Tree.cost grammar (pair alpha beta i)) <
    (1 + ∑ i : Fin 2, Tree.cost grammar (pair paddedAlpha beta i))
  simp only [univ_fin_two]
  norm_num [pair, Tree.cost, alpha, beta, paddedAlpha, grammar, arity]

/-- The proposed smaller proof is valid and has the right judgement. -/
theorem shrinking_candidate :
    Tree.Valid grammar empty ∧
    Tree.judgement grammar empty = Tree.judgement grammar alpha ∧
    Tree.support grammar empty ⊂ Tree.support grammar alpha := by
  simp [empty, alpha, Tree.Valid, Tree.judgement, Tree.support, grammar, arity]

/-- Shrinking exact support destroys the licence despite valid matching premises. -/
theorem support_shrinking_rejected :
    ¬ Tree.Valid grammar (licensed empty beta) := by
  intro h
  have hs := h.2.1
  change (∅ : Finset Root) = {Root.alpha} at hs
  exact (by decide : (∅ : Finset Root) ≠ {Root.alpha}) hs

/-- Both premises have the same judgement, so only ordered guards reject reversal. -/
theorem premise_reversal_rejected :
    ¬ Tree.Valid grammar (licensed beta alpha) := by
  simp [licensed, Tree.Valid, grammar, arity, pair, Tree.support, beta]

/-- Enlargement is realized by an actual valid proof, not only a support vector. -/
theorem enlarged_candidate :
    Tree.Valid grammar enlargedAlpha ∧
    Tree.judgement grammar enlargedAlpha = Tree.judgement grammar alpha ∧
    Tree.support grammar alpha ⊂ Tree.support grammar enlargedAlpha := by
  simp [enlargedAlpha, alpha, Tree.Valid, Tree.judgement, Tree.support, grammar, arity]
  decide

theorem support_enlarging_rejected :
    ¬ Tree.Valid grammar (licensed enlargedAlpha beta) := by
  intro h
  have hs := h.2.1
  have he : Root.extra ∈ Tree.support grammar enlargedAlpha := by
    simp [enlargedAlpha, Tree.support, grammar, arity]
  have hh : Root.extra ∈ ({Root.alpha} : Finset Root) := hs ▸ he
  simp at hh

/-- Reversal retains the total support union; rejection uses ordered positions. -/
theorem reversal_same_total_support :
    Tree.support grammar (licensed beta alpha) =
      Tree.support grammar (licensed alpha beta) := by
  change (∅ ∪ (Finset.univ : Finset (Fin 2)).biUnion
    (fun i => Tree.support grammar (pair beta alpha i))) =
      (∅ ∪ (Finset.univ : Finset (Fin 2)).biUnion
        (fun i => Tree.support grammar (pair alpha beta i)))
  simp [univ_fin_two, pair, Finset.union_comm]

/-- The same finite syntax with a negative wrapper occurrence price. -/
abbrev negativeGrammar : Grammar Judgement Root Rule :=
  { grammar with price := fun r => match r with | .pad => -2 | _ => 1 }
def negativeAlpha : Tree negativeGrammar := .node .alpha Fin.elim0
def negativeContext : Context negativeGrammar :=
  .step .pad 0 (fun _ => negativeAlpha) .hole

theorem negative_price_pruning_counterexample :
    negativeContext ≠ .hole ∧
    Tree.Valid negativeGrammar (Context.fill negativeGrammar negativeContext negativeAlpha) ∧
    Tree.Valid negativeGrammar negativeAlpha ∧
    Tree.judgement negativeGrammar negativeAlpha =
      Tree.judgement negativeGrammar (Context.fill negativeGrammar negativeContext negativeAlpha) ∧
    Tree.support negativeGrammar negativeAlpha =
      Tree.support negativeGrammar (Context.fill negativeGrammar negativeContext negativeAlpha) ∧
    Tree.nodes negativeGrammar negativeAlpha <
      Tree.nodes negativeGrammar (Context.fill negativeGrammar negativeContext negativeAlpha) ∧
    ¬ Tree.cost negativeGrammar negativeAlpha ≤
      Tree.cost negativeGrammar (Context.fill negativeGrammar negativeContext negativeAlpha) := by
  constructor
  · intro h; cases h
  · norm_num [negativeContext, negativeAlpha, negativeGrammar, Context.fill,
    Tree.Valid, Tree.judgement, Tree.support, Tree.nodes, Tree.cost, grammar, arity,
    Function.update]

#print axioms guard_not_upward_closed
#print axioms same_support_replacement
#print axioms support_shrinking_rejected
#print axioms enlarged_candidate
#print axioms support_enlarging_rejected
#print axioms reversal_same_total_support
#print axioms premise_reversal_rejected
#print axioms negative_price_pruning_counterexample
end GuardedTree.Controls
