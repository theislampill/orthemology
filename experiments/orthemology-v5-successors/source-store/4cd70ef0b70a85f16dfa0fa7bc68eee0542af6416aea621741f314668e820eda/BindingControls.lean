import HiddenChangeBinding
import CertificateControls
open HiddenChange
namespace HiddenChangeTests

def evenSubmission : SubmittedPositive 1 1 := ⟨one 0 0, 0, evenBody⟩
example : boundPositiveCheck (one 0 0) 0 evenSubmission = true := by decide +kernel
example : boundPositiveCheck (one 0 1) 0 evenSubmission = false := by decide +kernel
example : boundPositiveCheck
    ({one 0 0 with interpretation := {(one 0 0).interpretation with modelRevision := "stale"}} : HiddenChange.Input 1 1)
    0 evenSubmission = false := by decide +kernel
example : boundPositiveCheck reveal 1 ⟨reveal,0,revealBody⟩ = false := by decide +kernel
end HiddenChangeTests
