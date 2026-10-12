import Controls
open GuardedTree GuardedTree.Controls

/- Deliberately false: pruning a negative-price wrapper increases cost from -1 to 1,
   even though validity and the exact state agree. -/
example : Tree.cost negativeGrammar negativeAlpha ≤
    Tree.cost negativeGrammar (Context.fill negativeGrammar negativeContext negativeAlpha) := by
  norm_num [negativeContext, negativeAlpha, negativeGrammar, Context.fill,
    Tree.cost, grammar, arity, Function.update]
