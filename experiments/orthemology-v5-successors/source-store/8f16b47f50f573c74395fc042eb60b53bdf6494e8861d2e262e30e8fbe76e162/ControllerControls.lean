import ControllerFixtures
open HiddenChange HiddenParity HiddenParity.Sufficiency
open Orthemology.Tranche2.PolicyEmbedding
open HiddenChangeControllerTests
namespace HiddenChangeControllerTests

example : positiveCheck one 0 oneBody = true := by decide +kernel
example : positiveCheck reveal 0 revealBody = true := by decide +kernel
example : candidate 0 = 0 ∧ candidate 1 = 1 ∧ candidate 2 = 0 ∧ candidate 3 = 1 := by decide +kernel
example : (memory one oneBody 0 []).known1 = false ∧ (memory one oneBody 0 []).phase = 0 := by decide +kernel
example : (currentMemory one oneBody 0 []).retained = some Finset.univ := by decide +kernel
-- Literal increasing action order and global visit counts, including finite offset.
#guard compile one oneAdmissible 0 oneBody () [] = 0
#guard compile one oneAdmissible 0 oneBody () [(0,0)] = 1
#guard compile one oneAdmissible 0 oneBody () [(1,0),(0,0)] = 0
-- P1-zero at (0,0)->0 cannot set known1 or permanently delete candidate 1.
example : reveal.row 1 (0,0) 0 = 0 ∧
    (memory reveal revealBody 0 [(0,0)]).known1 = false := by decide +kernel
-- Actual revelation takes precedence over simultaneous rejection/exit; phase is preserved.
example : advance reveal (0,0) 1 ⟨false,7,some {(0,0)}⟩ true =
    ⟨true,7,none⟩ := by decide +kernel
-- Reject+exit increments only once, using a P0-positive receipt.
example : advance fullSupport (0,0) 1 ⟨false,7,some {(0,0)}⟩ true =
    ⟨false,8,none⟩ := by decide +kernel
-- Pure component exit increments even with no empirical rejection.
example : advance fullSupport (0,0) 1 ⟨false,7,some {(0,0)}⟩ false =
    ⟨false,8,none⟩ := by decide +kernel
-- A known component ignores even a true rejection flag and remains known.
example : advance reveal (1,0) 1 ⟨true,7,some {(1,0)}⟩ true =
    ⟨true,7,some {(1,0)}⟩ := by decide +kernel
example : (currentMemory reveal revealBody 0 [(0,1)]).known1 = true ∧
    (currentMemory reveal revealBody 0 [(0,1)]).retained = some {(1,0)} := by decide +kernel
-- The new receipt is present in the numerical test and histories are not reset.
example : (memory fullSupport revealBody 0 [(0,0)]).phase = 1 := by decide +kernel
example : (memory fullSupport revealBody 0 [(0,0),(0,0)]).phase = 2 := by decide +kernel
example : actionCount (0,0) (augmentHistory (0 : Fin 2) [(0,0),(0,0)]) = 2 := by decide +kernel
example : OrthemicCertificate.Direct.rationalReject reveal (1/2) 1 1 [((0,0),0)] = false := by decide +kernel
example : OrthemicCertificate.Direct.rationalReject reveal (1/2) 1 0 [((0,0),0)] = true := by decide +kernel
-- The first containing component follows body order, not a graph re-selection.
example : firstContaining (0 : Fin 1) ([{(0,1)},{(0,0)}] : List (PairSet 1 2)) = some {(0,1)} := by decide +kernel
-- Malformed body and off-policy history still return a common-menu action.
example : compile one oneAdmissible 0 {oneBody with D := ∅, D1 := ∅, known := [], uncertain := []}
    () [(1,0),(1,0)] = 0 := by decide +kernel

-- Actual-law endpoint instantiated on accepted concrete positive bodies.
example (κ : ChangeIndex) :
    ∀ᵐ H ∂fixedLaw one oneAdmissible.1 κ 0 (MeasureTheory.Measure.dirac ())
      (compile one oneAdmissible 0 oneBody), TaggedParity one (0,0) H :=
  compiled_fixed_parity one oneAdmissible 0 oneBody (by decide +kernel) κ (0,0)
example : WinsAll reveal revealAdmissible.1 0 (MeasureTheory.Measure.dirac ())
    (compile reveal revealAdmissible 0 revealBody) (0,0) :=
  compiled_winsAll reveal revealAdmissible 0 revealBody (by decide +kernel) (0,0)

end HiddenChangeControllerTests
