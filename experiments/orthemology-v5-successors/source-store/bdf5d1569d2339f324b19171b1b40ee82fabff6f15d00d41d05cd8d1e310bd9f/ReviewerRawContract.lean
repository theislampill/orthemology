import SelectorTableNormalForm
set_option autoImplicit false

namespace Orthemology.Ninth.SelectorExtraction.Reviewer
open HiddenParity HiddenParity.Sufficiency
open Orthemology.RuntimeBridge.PhaseUpdate
open Orthemology.RuntimeBridge.PhaseUpdate.FiniteSelectorSource
open Orthemology.Eighth.SemanticControls
open Orthemology.Eighth.SemanticControls.LiteralAssessment

/-- Independent full finite-image checks, rather than only decoded-value agreement. -/
theorem support_image_exact :
    (∀ B : Finset Bool, supportCode B < 4) ∧
    (∀ n : Fin 4, ∃ B : Finset Bool, supportCode B = n.val) := by decide

theorem target_image_exact :
    (∀ E : Finset (Bool × Bool), targetCode E < 16) ∧
    (∀ n : Fin 16, ∃ E : Finset (Bool × Bool), targetCode E = n.val) := by decide

theorem retained_image_exact :
    (∀ E : Option (Finset (Bool × Bool)), retainedCode E < 17) ∧
    (∀ n : Fin 17, ∃ E : Option (Finset (Bool × Bool)), retainedCode E = n.val) := by decide

theorem semantic_cell_inverse : ∀ B : Finset Bool, ∀ a b : Bool,
    cellSupport (cellIndex B a b) = B ∧
    cellFirst (cellIndex B a b) = a ∧
    cellSecond (cellIndex B a b) = b := by decide

theorem full_support_orientation_slot :
    (cellIndex Finset.univ false false).val = 12 := by decide

theorem supportCode_exact_injective : Function.Injective supportCode := by
  intro B C h
  exact (support_code_injective B C).mp h

/-- Presence and absence can be reconstructed from raw certificate numerals. -/
theorem certificate_zero_iff_absent (d : Data)
    (P : RationalKernel Bool (Bool × Bool) Bool)
    (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate d P menu priority) (B : Finset Bool) (c s : Bool) :
    targetDigit d B c s = 0 ↔ actualTarget P menu priority B c s = none := by
  rw [hc.target_eq]
  change retainedCode (actualTarget P menu priority B c s) = retainedCode none ↔ _
  exact ⟨fun h => retained_encoding_injective h, fun h => congrArg retainedCode h⟩

theorem certificate_one_iff_present_empty (d : Data)
    (P : RationalKernel Bool (Bool × Bool) Bool)
    (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ)
    (hc : Certificate d P menu priority) (B : Finset Bool) (c s : Bool) :
    targetDigit d B c s = 1 ↔ actualTarget P menu priority B c s = some ∅ := by
  rw [hc.target_eq]
  change retainedCode (actualTarget P menu priority B c s) = retainedCode (some ∅) ↔ _
  exact ⟨fun h => retained_encoding_injective h, fun h => congrArg retainedCode h⟩

/-- A raw payload above 16 rules out the original Certificate for every kernel. -/
theorem invalid_payload_rejects_original_certificate (d : Data)
    (P : RationalKernel Bool (Bool × Bool) Bool)
    (menu : Finset Bool → Bool → Finset Bool)
    (priority : Bool → (Bool × Bool) → ℕ)
    (B : Finset Bool) (candidate state : Bool)
    (hbad : 16 < targetDigit d B candidate state) :
    ¬ Certificate d P menu priority := by
  intro hc
  rw [hc.target_eq] at hbad
  have hbound := retained_image_exact.1 (actualTarget P menu priority B candidate state)
  omega

/-- The scalar equality required by the original certificate distinguishes presence. -/
theorem none_cannot_equal_present_empty :
    retainedCode (none : Option (Finset (Bool × Bool))) ≠ retainedCode (some ∅) := by decide

/-- Direct finite readback of the executable reader, with no certificate premise. -/
theorem reader_on_literal_inputs : ∀ o : Bool, recoveredOrientation (literalData o) = o := by decide

/-- The exact source theorem also has the intended fully numeric field-level statement. -/
theorem numeric_certificate_contract (d : Data) :
    Certificate d fixtureKernel sparseMenu actionPriority ↔
      d.cycleTable % 65536 = (if initialCandidate then 24332 else 44812) ∧
      d.targetTable % 1208925819614629174706176 = 428783445879334172098560 ∧
      d.stageTable % 65536 = 64080 := by
  rw [certificate_iff_exact_normalForm]
  simp only [normalizeData, literalData, Data.mk.injEq]
  norm_num

/-- Concrete certification would determine the retained enumeration, in both directions. -/
theorem false_literal_obligation :
    Certificate (Data.mk 44812 428783445879334172098560 64080)
      fixtureKernel sparseMenu actionPriority ↔ initialCandidate = false :=
  literal_certificate_iff false

theorem true_literal_obligation :
    Certificate (Data.mk 24332 428783445879334172098560 64080)
      fixtureKernel sparseMenu actionPriority ↔ initialCandidate = true :=
  literal_certificate_iff true

/-- The boundary is substantive even for two genuinely certified records. -/
theorem certified_but_raw_component_not_extensional :
    ∃ d e : Data, Certificate d fixtureKernel sparseMenu actionPriority ∧
      Certificate e fixtureKernel sparseMenu actionPriority ∧ SameCells d e ∧
      P02A2.PRProgram.denote (cycleProgram d) ![4,0,0] ≠
      P02A2.PRProgram.denote (cycleProgram e) ![4,0,0] := by
  let d := literalData initialCandidate
  refine ⟨d, addHighDigits d 1 0 0, literal_certificate initialCandidate rfl, ?_, ?_⟩
  · exact (certificate_addHighDigits_iff d 1 0 0 _ _ _).mpr
      (literal_certificate initialCandidate rfl)
  · exact sameCells_but_malformed_input_differs initialCandidate

#print axioms supportCode_exact_injective
#print axioms certificate_zero_iff_absent
#print axioms certificate_one_iff_present_empty
#print axioms support_image_exact
#print axioms target_image_exact
#print axioms retained_image_exact
#print axioms semantic_cell_inverse
#print axioms full_support_orientation_slot
#print axioms invalid_payload_rejects_original_certificate
#print axioms none_cannot_equal_present_empty
#print axioms reader_on_literal_inputs
#print axioms numeric_certificate_contract
#print axioms false_literal_obligation
#print axioms true_literal_obligation
#print axioms certified_but_raw_component_not_extensional
end Orthemology.Ninth.SelectorExtraction.Reviewer
