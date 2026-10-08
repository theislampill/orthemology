import HiddenChangeBinding
import FiniteControls
open HiddenChange HiddenChangeTests
namespace HiddenChangeRepresentationReview
-- Lean permits a non-simple bounded stored path; Python valid_route rejects it.
example : OrthemicCertificate.Path.Valid
    (Finset.univ : Finset (Fin 3 × Fin 1)) (fun _ => Finset.univ) 0 0
    ⟨0,[(0,0)]⟩ := by decide +kernel
-- Lean permits recomputed redundant fixed repetitions within n+2.
example : ValidTrace (F1 (one 0 0)) [Finset.univ,Finset.univ,Finset.univ] := by decide +kernel
def twoOdd : HiddenChange.Input 2 1 := { disconnected with priorities := #[1,1,1,1] }
example : (canonicalNegative twoOdd).knownTrace = [Finset.univ,∅,∅,∅] := by decide +kernel
example : negativeCheck twoOdd 0 (canonicalNegative twoOdd) = true := by decide +kernel
end HiddenChangeRepresentationReview
