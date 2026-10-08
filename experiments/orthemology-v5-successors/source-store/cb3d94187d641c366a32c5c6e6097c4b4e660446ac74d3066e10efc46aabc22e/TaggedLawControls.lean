import HiddenChangeTaggedLaw
open HiddenChange MeasureTheory
open Orthemology.Tranche2.PolicyEmbedding HiddenParity.Stochastic

namespace HiddenChangeLawTests
noncomputable def chooseOne : Adversary Unit 1 2 where
  choose := fun _ _ e => decide (e.2 = 1)
  measurable_choose := measurable_of_countable _

def oneAction : Policy Unit 1 2 := fun _ _ => 1
def zeroAction : Policy Unit 1 2 := fun _ _ => 0

def h0 : TaggedHistory 1 2 := [((0,(0,0)),0)]
def h1 : TaggedHistory 1 2 := [((1,(0,0)),0)]

example : eraseMode h0 = eraseMode h1 := rfl
example : (adaptivePolicy 0 oneAction chooseOne ((),()) []).1 = 1 := by decide +kernel
example : (adaptivePolicy 0 zeroAction chooseOne ((),()) []).1 = 0 := by decide +kernel
example : (adaptivePolicy 0 zeroAction chooseOne ((),()) h1).1 = 1 := by decide +kernel
example : (adaptivePolicy 0 oneAction chooseOne ((),()) h0).2 =
    (adaptivePolicy 0 oneAction chooseOne ((),()) h1).2 :=
  adaptivePolicy_no_leakage _ _ _ _ _ _ _ _ rfl
example : (fixedPolicy (some 1) 0 oneAction () []).1 = 0 := by decide +kernel
example : (fixedPolicy (some 1) 0 oneAction () h0).1 = 1 := by decide +kernel
example : (fixedPolicy (some 0) 0 oneAction () []).1 = 1 := by decide +kernel
example : (fixedPolicy none 0 oneAction () h1).1 = 0 := by decide +kernel

#check fixedPolicy_measurable
#check adaptivePolicy_measurable
#check adaptivePolicy_action_first
#check adaptivePolicy_irreversible
#check fixedLaw_eq_stack
#check adaptiveLaw_eq_stack
#check adaptive_seed_prefix_probability
#print axioms adaptivePolicy_measurable
#print axioms fixedLaw_eq_stack
#print axioms adaptiveLaw_eq_stack
end HiddenChangeLawTests
