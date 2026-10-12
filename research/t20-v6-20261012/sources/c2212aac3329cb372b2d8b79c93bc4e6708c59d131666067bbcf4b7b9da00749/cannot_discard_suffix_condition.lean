import EndpointChecks
open P02.Codec P02.Codec.UniformComputability P02A2.ObserverCore
example (original rest : List ℕ) (table : List ExprResult) (fuel : ℕ) (ht : ∀ i, i ≤ original.length → table.getD i none = readExpr fuel (original.drop i)) : exprLookup original table rest = readExpr fuel rest := by
  exact exprLookup_correct original table fuel ht rest
