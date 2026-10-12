import SourceFoldApplication
import OriginalWNoninhabitation

namespace SourceFoldContract

/-- The generic schema is not an admissible metarule of original HasE.
    This is an external nonderivability result, not a source negation term. -/
theorem original_source_naturality_not_admissible : ¬SourceNaturality := by
  intro naturality
  exact HomogeneousOriginalW.original_c3_not_W (original_W_from_naturality naturality)

#print axioms original_source_naturality_not_admissible
end SourceFoldContract
