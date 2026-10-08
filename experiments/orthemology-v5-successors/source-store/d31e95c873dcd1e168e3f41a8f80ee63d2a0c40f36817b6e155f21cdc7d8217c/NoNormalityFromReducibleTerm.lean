import UnaryCurrentIdentityBoundary
open OrthemologyV2 OrthemologyV3 P01AC.UnaryIdentity.IntensionalBoundary
example : normalCheck (Term.app .i .i) = true := by decide
