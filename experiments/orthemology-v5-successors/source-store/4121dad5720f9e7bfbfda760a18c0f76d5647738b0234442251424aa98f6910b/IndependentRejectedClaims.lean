import IndependentJoiningTests
open JointFinite IndependentJoining

-- Six additional joining overclaims, each decided false at a concrete witness.
example : AnchoredSourceBridge.GlobalCoverage switched .g := by
  simp only [switched, swapSource]; table_check
example : ∃ c, account.Req .k c ∧ contributionBearer c = B.h := by table_check
example : ∃ s, AnchoredSourceBridge.GlobalCoverage enlarged s := by
  simp only [enlarged]; table_check
example : speech.actual .w2 .x .actX := by table_check
example : speech.trueAt .w2 .absent → speech.asserts .w2 .x .v .absent := by table_check
example : framework.intrinsic .g .rx := by table_check
