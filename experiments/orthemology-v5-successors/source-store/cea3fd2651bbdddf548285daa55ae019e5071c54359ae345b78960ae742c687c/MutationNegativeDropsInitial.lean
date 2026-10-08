import EndpointFixtures
open HiddenChangeEndpointTests

/-! Complete raw input and initial-state binding for submitted finite evidence.
No parser, byte encoding, or external trust attestation is claimed. -/
open HiddenChange
namespace EndpointBindingMutation
variable {n k : ℕ}
structure SubmittedPositive (n k : ℕ) where
  input : Input n k
  initial : State n
  body : PositiveBody n k
  deriving DecidableEq
structure SubmittedNegative (n k : ℕ) where
  input : Input n k
  initial : State n
  body : NegativeBody n
  deriving DecidableEq

def boundPositiveCheck (I : Input n k) (s : State n) (c : SubmittedPositive n k) : Bool :=
  I.sameInput c.input && decide (s = c.initial) && positiveCheck I s c.body
def boundNegativeCheck (I : Input n k) (s : State n) (c : SubmittedNegative n k) : Bool :=
  I.sameInput c.input && negativeCheck I s c.body


example : boundNegativeCheck separator 1 ⟨separator,0,canonicalNegative separator⟩ = false := by
  have actual : boundNegativeCheck separator 1 ⟨separator,0,canonicalNegative separator⟩ = true := by decide +kernel
  simp only [actual, Bool.true_eq_false]
end EndpointBindingMutation
