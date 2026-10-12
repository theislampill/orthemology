/- Independent audit controls: zero/full/nonreduced weights; repeated syntax is
   independently sampled within a run, whereas relational comparison needs a
   correlated coupling. These controls do not modify the successor. -/
import P01CouplingWitness
namespace SuccessorIndependentAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01Probability
open scoped BigOperators

def ctx : P01F.Context := fun _ => .var 0
def vals : P01D.Env := fun n => if n = 0 then .i else skk
def rawEnv : REnv := diagEnv (fun _ => rawPER)
def varied : EExpr := .mix fairWeight (.pure (.var 0)) (.pure (.var 1))

theorem varied_typed : EHas ctx varied (.var 0) :=
  .mix (.pureCurry (.var ctx 0)) (.pureCurry (.var ctx 1)) fairWeight

theorem actual_related_valuations : ValRelated ctx rawEnv vals vals := by
  intro n
  exact Conv.refl _

theorem half_i : outputMass varied vals .i = 1/2 := by
  rw [varied,output_mass_mixture,output_mass_pure,output_mass_pure]
  norm_num [fairWeight, vals,eval,skk] <;> decide

theorem half_skk : outputMass varied vals skk = 1/2 := by
  rw [varied,output_mass_mixture,output_mass_pure,output_mass_pure]
  norm_num [fairWeight, vals,eval,skk] <;> decide

theorem raw_relation_separates : ¬ (P01R.interpret (.var 0)).rel rawEnv .i skk :=
  P01Source.I_SKK_not_convertible

theorem independent_product_has_forbidden_mass :
    outputMass varied vals .i * outputMass varied vals skk = 1/4 := by
  rw [half_i,half_skk]
  norm_num

theorem common_coupling_removes_forbidden_mass :
    outputCoupling varied vals vals .i skk = 0 := by
  unfold outputCoupling jointMass
  apply Finset.sum_eq_zero
  intro s hs
  apply if_neg
  intro h
  have he : (Term.i : Term) = skk := h.1.symm.trans h.2
  exact (by decide : (Term.i : Term) ≠ skk) he

theorem independent_product_not_relationally_supported :
    ¬ (∀ t u, 0 < outputMass varied vals t * outputMass varied vals u →
      (P01R.interpret (.var 0)).rel rawEnv t u) := by
  intro h
  apply raw_relation_separates
  apply h .i skk
  rw [independent_product_has_forbidden_mass]
  norm_num

def zeroW : Weight := ⟨0,7,by decide,by decide⟩
def fullW : Weight := ⟨7,7,by decide,by decide⟩
def repeatedHalf : Weight := ⟨2,4,by decide,by decide⟩

theorem zero_weight_branch_exact (l r : EExpr) (θ : P01D.Env) (t : Term) :
    outputMass (.mix zeroW l r) θ t = outputMass r θ t := by
  rw [output_mass_mixture]
  norm_num [zeroW]

theorem full_weight_branch_exact (l r : EExpr) (θ : P01D.Env) (t : Term) :
    outputMass (.mix fullW l r) θ t = outputMass l θ t := by
  rw [output_mass_mixture]
  norm_num [fullW]

theorem nonreduced_weight_law_exact (l r : EExpr) (θ : P01D.Env) (t : Term) :
    outputMass (.mix repeatedHalf l r) θ t = outputMass (.mix fairWeight l r) θ t := by
  rw [output_mass_mixture,output_mass_mixture]
  norm_num [repeatedHalf,fairWeight]

theorem branch_collision_mass_is_summed (p : Weight) (θ : P01D.Env) (t : Term) :
    outputMass (.mix p (.pure (.atom t)) (.pure (.atom t))) θ t = 1 := by
  rw [output_mass_mixture]
  simp only [output_mass_pure,eval,ite_true,mul_one]
  rw [← add_div, ← Nat.cast_add, Nat.add_sub_of_le p.bounded]
  exact div_self (ne_of_gt (Nat.cast_pos.mpr p.positiveDen))

theorem duplicated_expression_samples_independently :
    outputMass (.app varied varied) vals (.app .i skk) = 1/4 := by
  unfold outputMass pushMass
  change (∑s : (Fin 2 × Unit × Unit) × (Fin 2 × Unit × Unit), _) = _
  simp only [Fintype.sum_prod_type]
  have h0 : run varied vals ((0 : Fin 2),(),()) = .i := rfl
  have h1 : run varied vals ((1 : Fin 2),(),()) = skk := rfl
  simp only [run, Fin.sum_univ_two, Fintype.sum_unique, h0, h1]
  norm_num [seedWeight,Seed,varied,fairWeight,skk]

#print axioms independent_product_not_relationally_supported
#print axioms duplicated_expression_samples_independently
#print axioms branch_collision_mass_is_summed
end SuccessorIndependentAudit
