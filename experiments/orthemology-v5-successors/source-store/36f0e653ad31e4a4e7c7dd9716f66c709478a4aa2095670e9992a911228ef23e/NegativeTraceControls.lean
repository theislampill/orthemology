import HiddenChangeCertificate
import GreatestRegionControls
open HiddenChange
namespace HiddenChangeTests
example : negativeCheck (one 1 1) 0 ⟨[Finset.univ,∅,∅],[Finset.univ,∅,∅]⟩ = true := by decide +kernel
example : negativeCheck (one 0 0) 0 ⟨[∅,∅],[∅,∅]⟩ = false := by decide +kernel
example : negativeCheck (one 0 0) 0 ⟨[Finset.univ,∅,∅],[Finset.univ,∅,∅]⟩ = false := by decide +kernel
example : negativeCheck (one 1 1) 0 ⟨[Finset.univ,∅],[Finset.univ,∅]⟩ = false := by decide +kernel
example : negativeCheck separator 0 (canonicalNegative separator) = true := by decide +kernel
end HiddenChangeTests
namespace HiddenChangeTests
-- Extra repeated rounds do not evade the n+2 bound.
example : negativeCheck (one 1 1) 0
    ⟨[Finset.univ,∅,∅,∅],[Finset.univ,∅,∅,∅]⟩ = false := by decide +kernel
end HiddenChangeTests
