import PolyAnalysis
open P01D
-- Intentionally false: the actual compiler chooses K for a closed body.
example : abstract (Poly.app (.atom .i) (.atom .k)) =
    Poly.app (.app (.atom .s) (.app (.atom .k) (.atom .i))) (.app (.atom .k) (.atom .k)) := by
  simp [abstract,freeZero,drop,pren,psub]
