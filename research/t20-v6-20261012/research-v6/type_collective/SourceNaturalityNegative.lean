import SourceFoldApplication
import OriginalWNoninhabitation

/-- V6 source-level join, not yet freshly compiled in this environment. -/
theorem source_naturality_fails : ¬ SourceFoldContract.SourceNaturality := by
  intro h
  exact HomogeneousOriginalW.original_c3_not_W
    (SourceFoldContract.original_W_from_naturality h)
