import ControllerFixtures
open HiddenChange HiddenParity HiddenParity.Sufficiency
open Orthemology.Tranche2.PolicyEmbedding
open HiddenChangeControllerTests
open OrthemicCertificate.Direct

namespace HiddenChangeControllerReview

-- Empty known-mode region is permitted when no revealing receipt can occur.
def noKnownBody : PositiveBody 1 2 :=
  { oneBody with K := ∅, D1 := ∅, known := [] }
example : positiveCheck one 0 noKnownBody = true := by decide +kernel
example : WinsAll one oneAdmissible.1 0 (MeasureTheory.Measure.dirac ())
    (compile one oneAdmissible 0 noKnownBody) (0,0) :=
  compiled_winsAll one oneAdmissible 0 noKnownBody (by decide +kernel) (0,0)

-- Equal mode rows impose the rival parity obligation even at candidate zero.
def oddRival : Input 1 2 := {one with priorities := #[0,0,1,1]}
example : positiveCheck oddRival 0 oneBody = false := by decide +kernel
-- A body must cover both candidates, not only mode zero.
example : positiveCheck one 0 {oneBody with uncertain :=
    [⟨0,0,.component ⟨0,[]⟩ Finset.univ⟩]} = false := by decide +kernel

-- Tolerance is half the minimum full coordinate gap; identical rows use one.
example : tolerance one Finset.univ = 1 := by decide +kernel
example : tolerance reveal Finset.univ = 1/2 := by decide +kernel
example : tolerance fullSupport Finset.univ = 1/6 := by decide +kernel
-- The empty history cannot reject at phase zero, even with positive error.
example : rationalReject reveal (1/2) 1 0 [] = false := by decide +kernel
-- Discrepancy equals tolerance: rejection is non-strict in the discrepancy.
example : rationalReject reveal (1/2) 0 1 [((0,0),0),((0,0),1)] = true := by decide +kernel
-- The inclusive discrepancy operator also applies to its zero boundary.
example : rationalReject one 0 0 0 [((0,0),0)] = true := by decide +kernel
-- The count gate is strict, independently of the discrepancy boundary.
example : rationalReject reveal (1/2) 0 2 [((0,0),0),((0,0),1)] = false := by decide +kernel

-- The just-received observation affects the current update, not the next one.
example : (memory fullSupport revealBody 0 [(0,0)]).phase = 1 := by decide +kernel
-- Old physical observations and pair/receipt counts remain present after revelation.
example : actionCount (0,0) (augmentHistory (0 : Fin 2) ([(0,1),(0,0)] : PublicHistory 2 1)) = 2 := by decide +kernel
example : symbolCount (0,0) 0 (augmentHistory (0 : Fin 2) ([(0,1),(0,0)] : PublicHistory 2 1)) = 1 := by decide +kernel
example : symbolCount (0,0) 1 (augmentHistory (0 : Fin 2) ([(0,1),(0,0)] : PublicHistory 2 1)) = 1 := by decide +kernel
example : (memory reveal revealBody 0 [(0,1),(0,0)]).known1 = true := by decide +kernel
-- Both source visits are counted despite different prior chosen actions.
example : historyVisits (0 : Fin 1) 0 [(1,0),(0,0)] = 2 := by decide +kernel

-- Candidate-one components are selected without consulting a live support set.
example : availableComponents revealBody ⟨false,1,none⟩ = [] := by decide +kernel
example : availableComponents revealBody ⟨false,2,none⟩ = [{(0,0)}] := by decide +kernel
example : availableComponents revealBody ⟨true,1,none⟩ = [{(1,0)}] := by decide +kernel
-- Preparation preserves an existing retained component, even if another is first.
example : prepare oneBody 0 ⟨false,0,some {(0,1)}⟩ = ⟨false,0,some {(0,1)}⟩ := by decide +kernel
-- Known off-policy exit clears retention, but not layer or phase.
example : advance reveal (1,0) 0 ⟨true,7,some {(1,0)}⟩ true =
    ⟨true,7,none⟩ := by decide +kernel
-- Lawfulness is unconditional in body validity and history reachability.
example (c : PositiveBody 1 2) : AllHistoryLawful one 0 (compile one oneAdmissible 0 c) :=
  compiled_all_history_lawful one oneAdmissible 0 c

-- A stable candidate can be globally wrong when all actually retained rows match.
def localMatch : Input 2 1 :=
  {reveal with rows := #[1,0,0,1,1,0,1,0], priorities := #[0,0,0,1]}
def localBody : PositiveBody 2 1 :=
  ⟨∅,{0},∅,{(0,0)},[],[⟨0,0,.component ⟨0,[]⟩ {(0,0)}⟩,
    ⟨0,1,.component ⟨0,[]⟩ {(0,0)}⟩]⟩
def localAdmissible : Admissible localMatch := by decide +kernel
example : localMatch.row 0 (1,0) 0 ≠ localMatch.row 1 (1,0) 0 := by decide +kernel
example : Match localMatch.row 0 1 {(0,0)} := by decide +kernel
example : positiveCheck localMatch 0 localBody = true := by decide +kernel
example : (memory localMatch localBody 0 [(0,0),(0,0),(0,0)]).phase = 0 := by decide +kernel
example : WinsAll localMatch localAdmissible.1 0 (MeasureTheory.Measure.dirac ())
    (compile localMatch localAdmissible 0 localBody) (0,0) :=
  compiled_winsAll localMatch localAdmissible 0 localBody (by decide +kernel) (0,0)
-- Support equality alone does not trigger the rival's parity requirement.
-- This is deliberately a local component control, not an accepted full body.
def unequalSameSupport : Input 2 1 := {fullSupport with priorities := #[0,0,1,1]}
example : succ unequalSameSupport 0 (0,0) = succ unequalSameSupport 1 (0,0) := by decide +kernel
example : UncertainGood unequalSameSupport 0 Finset.univ := by decide +kernel
example : ¬ EvenMinimum unequalSameSupport 1 Finset.univ := by decide +kernel

end HiddenChangeControllerReview
