import ScaleReadback

noncomputable section
open ExplicitANDScale PolynomialBounds
open scoped BigOperators

namespace IndependentScaleAudit

def fixture : Data := ⟨1/4,1/2,1/2,1,0,0,0⟩

lemma fixture_valid : fixture.valid := by norm_num [fixture,Data.valid]

/-- Literal kernel evaluation matches the independent exact-rational 20-row calculation. -/
theorem fixture_delta : fixture.delta=(31562496:ℝ)/25265441833 := by
  norm_num [Data.delta,ConstraintBounds.radius,Data.heads,Data.budgets,
    Data.gHead,Data.fHead,Data.bary0,Data.bary1,Data.bary2,Data.p0,Data.hvec,
    Data.e,Data.b,Data.g,fixture,ANDScore.variance,ANDScore.mean,
    ANDCorrection.beta,ANDCorrection.gamma,ANDCorrection.leadG,ANDCorrection.leadF,
    PolynomialAND.curvature,ANDScore.truth,budget,gCoefficients,fCoefficients,
    Fintype.sum_prod_type,Fin.sum_univ_succ]
  all_goals dsimp only [Matrix.cons_val]
  all_goals simp only [abs_div,abs_one,Nat.abs_ofNat]
  all_goals norm_num

example : ConstraintBounds.radius (fun _ : Unit => (1/100:ℝ)) (fun _ => (1:ℝ))=1/401 := by
  norm_num [ConstraintBounds.radius]

/-- Multiplying by a small head instead of dividing allows an invalid scale. -/
example : (0:ℝ)<1/4 ∧ (1/4:ℝ)<1/(1+2*(1+1)*(1/100)) ∧
    (1/100:ℝ)+(1/4)*(-1)<0 := by norm_num

/-- The signed coefficient sum cannot replace the absolute coefficient budget. -/
example : value (![1,-1] : Fin 2 → ℝ) 0=1 ∧
    (∑ i : Fin 2, (![1,-1] : Fin 2 → ℝ) i)=0 := by
  norm_num [value,Fin.sum_univ_succ]

#check @ExplicitANDScale.intrinsic_explicit_strict_repair
#check @ConstraintBounds.radius_lt_each
#check @fixture_delta
#print axioms fixture_delta
#print axioms fixture_valid
#print ExplicitANDScale.Data.heads
#print ExplicitANDScale.Data.budgets
#print ExplicitANDScale.Data.rem
#print ExplicitANDScale.Data.delta
#print ConstraintBounds.radius
end IndependentScaleAudit
