import BoundaryControls
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.Tranche2.PolicyEmbeddingAudit

-- Deliberately false: inside-U actions must not consume oracle rows.
example : (policyRun goodU alwaysFalse zeroOracle () Xzero 3).2 = 3 := by decide
