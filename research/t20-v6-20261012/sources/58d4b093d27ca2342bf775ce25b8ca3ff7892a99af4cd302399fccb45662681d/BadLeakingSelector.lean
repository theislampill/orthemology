import BoundaryControls
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.Tranche2.PolicyEmbeddingAudit

-- Deliberately false: reading an unused stack coordinate is not noninterference.
example : leakingSelector ((),(Xzero,[])) = leakingSelector ((),(Xoutside,[])) := by decide
