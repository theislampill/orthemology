import BoundaryControls
open Orthemology.Tranche2.PolicyEmbedding
open Orthemology.Tranche2.PolicyEmbeddingAudit

-- Deliberately false: policy observations can agree while retained seed fields differ.
example : (policyRun goodU alwaysFalse zeroOracle () Xzero 0).1.2.1 true 0 =
    (policyRun goodU alwaysFalse zeroOracle () Xoutside 0).1.2.1 true 0 := by decide
