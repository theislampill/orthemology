import SignedService
import DirectEndpoint

/-! Final program-producing signed service. This file is intentionally not part
of the standalone negative replay: it is admitted only after DirectEndpoint has
an actual successful fresh compile. No extraction success is assumed here. -/
namespace OrthemicCertificate.Signed
open MeasureTheory
open HiddenParity HiddenParity.Sufficiency HiddenParity.Stochastic HiddenParity.Necessity
open Orthemology.Tranche2.PolicyEmbedding
variable {q n k : Nat}

abbrev CompiledPolicy (n k : Nat) := Unit → History (Fin k) (Fin n) → Fin k

inductive CompiledSignedResult (q n k : Nat) where
  | invalidInput
  | emptySupport
  | positive (body : Body q n k) (policy : CompiledPolicy n k)
  | negative (certificate : Negative q n k)

/-- The positive result includes the literal accepted submitted body and its
finite-history executable policy. The validity proof is runtime-erased dimension
evidence; it is not a success oracle. Both negative and invalid cases remain
separate and carry no compiled policy. -/
def solveCompiled (I : Input q n k) (B : Support q) (s : Fin n) : CompiledSignedResult q n k :=
  if hI : I.inputCheck = true then
    match solve I B s with
    | .invalidInput => .invalidInput
    | .emptySupport => .emptySupport
    | .positive c => .positive c (Direct.compile I ((Input.inputCheck_iff I).mp hI) B s c)
    | .negative d => .negative d
  else .invalidInput

/-- The actual returned positive policy is measurable, lawful and almost-sure
parity winning for every initial live model under its original history law. -/
def CompiledSignedResult.Correct (I : Input q n k) (B : Support q) (s : Fin n) :
    CompiledSignedResult q n k → Prop
  | .invalidInput => ¬ I.Valid
  | .emptySupport => I.Valid ∧ ¬ B.Nonempty
  | .negative d => negativeCheck I B s d = true
  | .positive c π => ∃ hI : I.Valid, check I c B s = true ∧
      π = Direct.compile I hI B s c ∧
      Measurable (fun z : Unit × History (Fin k) (Fin n) => π z.1 z.2) ∧
      (letI : NeZero n := ⟨Nat.ne_of_gt hI.1.2.1⟩
       Lawful (I.kernel hI) I.menu B s π (Measure.dirac ()) ∧
         ∀ d : Pair n k, ∀ σ ∈ B,
           ∀ᵐ H ∂markovHistoryLaw (I.kernel hI) σ s π (Measure.dirac ()),
             ParitySuccess (I.priority σ) (historyAction d H))

theorem solveCompiled_correct (I : Input q n k) (B : Support q) (s : Fin n) :
    (solveCompiled I B s).Correct I B s := by
  unfold solveCompiled
  split
  next hI =>
    let hv : I.Valid := (Input.inputCheck_iff I).mp hI
    have hs := solve_correct I B s
    cases h : solve I B s with
    | invalidInput => simpa [h, SignedResult.Correct, CompiledSignedResult.Correct] using hs
    | emptySupport => simpa [h, SignedResult.Correct, CompiledSignedResult.Correct] using hs
    | negative d => simpa [h, SignedResult.Correct, CompiledSignedResult.Correct] using hs
    | positive c =>
      have hc : check I c B s = true := by simpa [h, SignedResult.Correct] using hs
      refine ⟨hv,hc,rfl,Direct.compiled_measurable I hv B s c,?_⟩
      exact ⟨Direct.compiled_lawful I hv B s c hc,
        fun d => Direct.compiled_parity I hv B s c hc d⟩
  next hI =>
    intro hv
    exact hI ((Input.inputCheck_iff I).mpr hv)

/-- Completeness of signs remains Ninth's inherited semantic existence iff,
combined with the new complete negative presentation. -/
theorem signed_semantic_alternatives [NeZero n] (I : Input q n k) (hI : I.Valid)
    (B : Support q) (hB : B.Nonempty) (s : Fin n) (d : Pair n k) :
    (SemanticWinning (R := Unit) (I.kernel hI) I.menu I.priority d B s ↔
      ∃ c, check I c B s = true) ∧
    (¬ SemanticWinning (R := Unit) (I.kernel hI) I.menu I.priority d B s ↔
      ∃ certificate, negativeCheck I B s certificate = true) :=
  ⟨semantic_iff_certificate I hI B s d,
    (negativeCheck_iff_not_semantic I hI B hB s d).symm⟩

theorem solveCompiled_positive_iff_semantic [NeZero n] (I : Input q n k) (hI : I.Valid)
    (B : Support q) (hB : B.Nonempty) (s : Fin n) (d : Pair n k) :
    (∃ c π, solveCompiled I B s = .positive c π) ↔
      SemanticWinning (R := Unit) (I.kernel hI) I.menu I.priority d B s := by
  rw [← solve_positive_iff_semantic I hI B hB s d]
  unfold solveCompiled
  rw [dif_pos ((Input.inputCheck_iff I).mpr hI)]
  cases solve I B s <;> simp

theorem solveCompiled_negative_iff_not_semantic [NeZero n] (I : Input q n k) (hI : I.Valid)
    (B : Support q) (hB : B.Nonempty) (s : Fin n) (d : Pair n k) :
    (∃ certificate, solveCompiled I B s = .negative certificate) ↔
      ¬ SemanticWinning (R := Unit) (I.kernel hI) I.menu I.priority d B s := by
  rw [← solve_negative_iff_not_semantic I hI B hB s d]
  unfold solveCompiled
  rw [dif_pos ((Input.inputCheck_iff I).mpr hI)]
  cases solve I B s <;> simp

end OrthemicCertificate.Signed
