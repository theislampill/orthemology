import HiddenChangeTailTransport
open HiddenChange MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding HiddenParity.Stochastic HiddenParity.ResidualSeed
open HiddenParity.ResidualSeed.Continuation
namespace HiddenChangeLawTests

def lateFixture : HiddenChange.Input 2 1 where
  rows := #[0,1,0,1, 1,0,0,1]
  priorities := #[0,0,0,0]
  menus := [⟨[0,1],0,[0]⟩,⟨[0,1],1,[0]⟩]
  interpretation := ⟨["zero","one"],["start","tail"],["a"],"v1","state","exact","common"⟩

theorem lateFixture_valid : lateFixture.Valid := (by decide +kernel : Admissible lateFixture).1

def solePolicy : Policy Unit 2 1 := fun _ _ => 0
def latePrefix : PairHistory 2 1 := [((0,0),1)]
def tailPairs : PairSet 2 1 := {(1,0)}

example : HiddenParity.Match lateFixture.row 0 1 tailPairs := by decide +kernel
example : liftMode (some 1) ([((1,0),1),((0,0),1)] : PairHistory 2 1) =
    [((1,(1,0)),1),((0,(0,0)),1)] := by decide +kernel
example : fixedPrefixLikelihood lateFixture none latePrefix = 1 := by
  norm_num [fixedPrefixLikelihood, latePrefix, fixedMode, lateFixture, OrthemicCertificate.Input.row,
    Fin.prod_univ_succ]
example : fixedPrefixLikelihood lateFixture (some 0) latePrefix = 0 := by
  norm_num [fixedPrefixLikelihood, latePrefix, fixedMode, lateFixture, OrthemicCertificate.Input.row,
    Fin.prod_univ_succ]

-- The late prefix is legitimate even though it is impossible under stationary mode1.
example : fixedPhysicalLaw lateFixture lateFixture_valid none 0 (Measure.dirac ()) solePolicy
    {H | H latePrefix.length = latePrefix} = 1 := by
  rw [fixed_prefix_probability _ _ _ _ _ _ (measurable_of_countable _) ]
  norm_num [CompatibleSeeds, ActionCompatible, pairPolicy, currentState, erasePairSources,
    solePolicy, latePrefix, fixedPrefixLikelihood, fixedMode, lateFixture,
    OrthemicCertificate.Input.row, Fin.prod_univ_succ]
example : fixedPhysicalLaw lateFixture lateFixture_valid (some 0) 0 (Measure.dirac ()) solePolicy
    {H | H latePrefix.length = latePrefix} = 0 := by
  rw [fixed_prefix_probability _ _ _ _ _ _ (measurable_of_countable _) ]
  norm_num [CompatibleSeeds, ActionCompatible, pairPolicy, currentState, erasePairSources,
    solePolicy, latePrefix, fixedPrefixLikelihood, fixedMode, lateFixture,
    OrthemicCertificate.Input.row, Fin.prod_univ_succ]

example (C : Set (PairTrace 2 1)) (hC : MeasurableSet C) :
    fixedPhysicalLaw lateFixture lateFixture_valid none 0 (Measure.dirac ()) solePolicy
      {H | H latePrefix.length = latePrefix ∧
        continuationReadout latePrefix H ∈ C ∩ HistoryStays tailPairs (1,0)} =
    fixedPhysicalLaw lateFixture lateFixture_valid (some latePrefix.length) 0 (Measure.dirac ()) solePolicy
      {H | H latePrefix.length = latePrefix ∧
        continuationReadout latePrefix H ∈ C ∩ HistoryStays tailPairs (1,0)} :=
  noChange_switchAt_prefix_tail_eq _ _ _ _ _ (measurable_of_countable _)
    _ _ _ (by decide +kernel) C hC

#print axioms fixed_seed_prefix_probability
#print axioms fixed_none_eq_markov
#print axioms fixed_zero_eq_markov
#print axioms fixedConditionalLaw_eq_shifted_restart
#print axioms fixedConditionalLaw_eq_restart
#print axioms noChange_switchAt_prefix_tail_eq
end HiddenChangeLawTests

example : HiddenChange.shiftIndex (some 7) 3 = some 4 := by decide +kernel
example : HiddenChange.shiftIndex (some 1) 3 = some 0 := by decide +kernel
example : HiddenChange.shiftIndex none 3 = none := by decide +kernel
example : HiddenChange.fixedPrefixLikelihood HiddenChangeLawTests.lateFixture (some 1)
    ([((1,0),1),((0,0),1)] : HiddenChange.PairHistory 2 1) = 1 := by
  rw [HiddenChange.fixedPrefixLikelihood_eq_lift]
  simp only [HiddenChange.liftMode, rowLikelihood_cons]
  norm_num [HiddenChange.taggedRows, HiddenChange.fixedMode, HiddenChangeLawTests.lateFixture,
    OrthemicCertificate.Input.row, RowLikelihood, Fin.prod_univ_zero]
  exact Fin.prod_univ_zero _
