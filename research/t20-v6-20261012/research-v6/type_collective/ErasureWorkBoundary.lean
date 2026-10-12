import SourceControls
import SourceExportBoundary

namespace V6ErasureWorkBoundary
open P03Source OrthemologyV2 OrthemologyV3

def original : SourceProof := .allI (.i (.var 0))
def repeated : SourceProof := .reduce original [.i]

/-- The exact source-to-Cert erasure does not preserve charged source work. -/
theorem same_certificate_different_work :
    encode original = encode repeated ∧
    sourceRun 0 original = some ((.i, identityCode), 22) ∧
    sourceRun 0 repeated = some ((.i, identityCode), 34) ∧
    sourceCheck 0 original = sourceCheck 0 repeated ∧
    exportWork original = 2 ∧ exportWork repeated = 3 := by
  exact ⟨rfl, by decide⟩

#print axioms same_certificate_different_work
end V6ErasureWorkBoundary
