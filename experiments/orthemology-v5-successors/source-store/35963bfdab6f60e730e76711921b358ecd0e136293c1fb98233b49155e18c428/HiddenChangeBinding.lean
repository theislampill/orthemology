import HiddenChangeCertificate

/-! Complete raw input and initial-state binding for submitted finite evidence.
No parser, byte encoding, or external trust attestation is claimed. -/
namespace HiddenChange
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
  I.sameInput c.input && decide (s = c.initial) && negativeCheck I s c.body

@[simp] theorem boundPositiveCheck_iff (I : Input n k) (s : State n) (c : SubmittedPositive n k) :
    boundPositiveCheck I s c = true ↔
    I = c.input ∧ s = c.initial ∧ positiveCheck I s c.body = true := by
  simp [boundPositiveCheck, and_assoc]
@[simp] theorem boundNegativeCheck_iff (I : Input n k) (s : State n) (c : SubmittedNegative n k) :
    boundNegativeCheck I s c = true ↔
    I = c.input ∧ s = c.initial ∧ negativeCheck I s c.body = true := by
  simp [boundNegativeCheck, and_assoc]

theorem boundPositiveCheck_iff_region (I : Input n k) (hI : Admissible I) (s : State n) :
    (∃ c, boundPositiveCheck I s c = true) ↔ s ∈ uncertainRegion I := by
  constructor
  · rintro ⟨c,hc⟩
    exact positiveCheck_sound I s c.body ((boundPositiveCheck_iff I s c).mp hc).2.2
  · intro hs
    obtain ⟨c,hc⟩ := (positiveCheck_iff_region I hI s).mpr hs
    exact ⟨⟨I,s,c⟩,(boundPositiveCheck_iff I s _).mpr ⟨rfl,rfl,hc⟩⟩
theorem boundNegativeCheck_iff_region (I : Input n k) (hI : Admissible I) (s : State n) :
    (∃ c, boundNegativeCheck I s c = true) ↔ s ∉ uncertainRegion I := by
  constructor
  · rintro ⟨c,hc⟩
    exact negativeCheck_sound I s c.body ((boundNegativeCheck_iff I s c).mp hc).2.2
  · intro hs
    obtain ⟨c,hc⟩ := (negativeCheck_iff_region I hI s).mpr hs
    exact ⟨⟨I,s,c⟩,(boundNegativeCheck_iff I s _).mpr ⟨rfl,rfl,hc⟩⟩

theorem signed_finite_alternatives (I : Input n k) (hI : Admissible I) (s : State n) :
    ((∃ c, boundPositiveCheck I s c = true) ∧ ¬ ∃ c, boundNegativeCheck I s c = true) ∨
    ((∃ c, boundNegativeCheck I s c = true) ∧ ¬ ∃ c, boundPositiveCheck I s c = true) := by
  rw [boundPositiveCheck_iff_region I hI s, boundNegativeCheck_iff_region I hI s]
  by_cases h : s ∈ uncertainRegion I
  · exact Or.inl ⟨h,fun hn => hn h⟩
  · exact Or.inr ⟨h,h⟩
end HiddenChange
