/- A non-diagonal common-coupling witness with different raw output laws.
   Observers must respect the typed relation; raw representation tests need not. -/
import P01EffectMass
import P01ModelWitnesses
import Mathlib.Tactic.NormNum
import Mathlib.Algebra.BigOperators.Fin
namespace P01R
open scoped BigOperators
open OrthemologyV2 OrthemologyV3 P01D P01Probability

def fairWeight : Weight := ⟨1,2,by decide,by decide⟩
def witnessContext : P01F.Context := fun _ => identityCode

def witnessEffect : EExpr :=
  .mix fairWeight (.pure (.var 0)) (.pure (.atom .i))

def leftValues : P01D.Env := fun _ => .i
def rightValues : P01D.Env := fun _ => skk

theorem witness_typed : EHas witnessContext witnessEffect identityCode :=
  .mix (.pureCurry (.var witnessContext 0)) (.pureFinite finite_polymorphic_I) fairWeight

theorem witness_inputs_related (r : REnv) : ValRelated witnessContext r leftValues rightValues :=
  fun _ => recursive_polymorphic_I_skk r

theorem left_I_mass : outputMass witnessEffect leftValues .i = 1 := by
  rw [witnessEffect,output_mass_mixture,output_mass_pure,output_mass_pure]
  norm_num [fairWeight,leftValues,eval]

theorem right_I_mass : outputMass witnessEffect rightValues .i = 1/2 := by
  rw [witnessEffect,output_mass_mixture,output_mass_pure,output_mass_pure]
  norm_num [fairWeight,rightValues,eval,skk] <;> decide

theorem right_skk_mass : outputMass witnessEffect rightValues skk = 1/2 := by
  rw [witnessEffect,output_mass_mixture,output_mass_pure,output_mass_pure]
  norm_num [fairWeight,rightValues,eval,skk] <;> decide

theorem non_diagonal_mass : outputCoupling witnessEffect leftValues rightValues .i skk = 1/2 := by
  have hl0 : run witnessEffect leftValues ((0 : Fin 2),(),()) = .i := rfl
  have hl1 : run witnessEffect leftValues ((1 : Fin 2),(),()) = .i := rfl
  have hr0 : run witnessEffect rightValues ((0 : Fin 2),(),()) = skk := rfl
  have hr1 : run witnessEffect rightValues ((1 : Fin 2),(),()) = .i := rfl
  have hne : (Term.i : Term) ≠ skk := by decide
  unfold outputCoupling jointMass
  change (∑s : Fin 2 × Unit × Unit, _) = _
  simp only [Fintype.sum_prod_type]
  norm_num only [Fin.sum_univ_two, Fintype.sum_unique, hl0,hl1,hr0,hr1, hne,
    eq_self_iff_true,true_and,and_self,if_true,if_false]
  norm_num [seedWeight,witnessEffect,Seed,fairWeight]

theorem different_raw_output_laws :
    outputMass witnessEffect leftValues ≠ outputMass witnessEffect rightValues := by
  intro h
  have hi := congrFun h .i
  rw [left_I_mass,right_I_mass] at hi
  exact (by norm_num : (1 : ℚ) ≠ 1/2) hi

theorem witness_one_coupling_for_all_relations (r : REnv) (t u : Term)
    (h : 0 < outputCoupling witnessEffect leftValues rightValues t u) :
    (interpret identityCode).rel r t u := by
  obtain ⟨s,rfl,rfl⟩ := joint_positive_has_seed (seedWeight witnessEffect)
    (run witnessEffect leftValues) (run witnessEffect rightValues) h
  exact shared_seed_fundamental witness_typed r leftValues rightValues (witness_inputs_related r) s

theorem witness_all_respectful_observations_agree {O : Type*} [DecidableEq O]
    (r : REnv) (leftObs rightObs : Term → O)
    (h : ∀t u, (interpret identityCode).rel r t u → leftObs t = rightObs u) :
    ∀o, pushMass (seedWeight witnessEffect) (leftObs ∘ run witnessEffect leftValues) o =
      pushMass (seedWeight witnessEffect) (rightObs ∘ run witnessEffect rightValues) o :=
  related_observations_equal witness_typed r leftValues rightValues (witness_inputs_related r) leftObs rightObs h

end P01R
