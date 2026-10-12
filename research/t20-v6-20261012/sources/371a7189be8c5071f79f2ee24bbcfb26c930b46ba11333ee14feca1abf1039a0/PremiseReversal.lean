import Controls
open GuardedTree GuardedTree.Controls

/- Deliberately false: matching judgement and unchanged union support do not
   permit reversing the ordered child-support vector. -/
example : Tree.Valid grammar (licensed beta alpha) := by
  constructor
  · intro i
    fin_cases i <;>
      simp [licensed, pair, alpha, beta, Tree.Valid, Tree.judgement, grammar, arity]
  · change ({Root.beta} : Finset Root) = {Root.alpha} ∧ {Root.alpha} = {Root.beta}
    decide
