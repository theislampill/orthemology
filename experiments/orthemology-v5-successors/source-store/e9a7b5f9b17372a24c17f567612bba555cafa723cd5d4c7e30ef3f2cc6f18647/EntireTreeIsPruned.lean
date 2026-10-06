import EffectiveRenewalBoundary
open EffectiveRenewal EffectiveRenewal.Pruning
-- Decidability and arbitrary finite height do not warrant global pruning.
example : RootedPruned diagonalTree := diagonal_not_rooted_pruned
