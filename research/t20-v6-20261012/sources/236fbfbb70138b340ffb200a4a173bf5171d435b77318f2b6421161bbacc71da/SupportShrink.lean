import Controls
open GuardedTree GuardedTree.Controls

/- Deliberately false: empty has the same judgement and smaller support than alpha,
   but the parent licence requires alpha's exact support in its first position. -/
example : Tree.Valid grammar (licensed empty beta) := by
  constructor
  · intro i
    fin_cases i <;>
      simp [licensed, pair, empty, beta, Tree.Valid, Tree.judgement, grammar, arity]
  · change (∅ : Finset Root) = {Root.alpha} ∧ {Root.beta} = {Root.beta}
    decide
