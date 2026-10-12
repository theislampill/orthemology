import InternalUniqueness
namespace InternalUniquenessIndependentReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open SourceRigidity RigidityInitiality InternalRecursorPrinciple

-- Exact existing source formula, no surrogate predicate or schema in the conclusion.
example : HasE [] (abstract uniqueUniformProof)
    (arr SourceRigidity.Rigidity InternalRecursorPrinciple.Uniqueness) :=
  rigidity_implies_internal_uniqueness
example : InternalRecursorPrinciple.Uniqueness = .all
    (.pi A (.pi End (.pi (arr N A) (.pi ZeroLaw (.pi StepLaw
      (.pi N (.identity A (.app (.var 3) (.var 0))
        (.app (.app (.var 0) (.var 4)) (.var 5))))))))) := rfl
example : uniqueUniformProof =
    abstract (abstract (abstract (abstract (abstract (abstract uniquePointProof))))) := rfl
example : HasE [N, StepLaw, ZeroLaw, arr N A, End, A, Rigidity] uniquePointProof
    (.identity A (.app (.var 3) (.var 0)) (.app (.app (.var 0) (.var 4)) (.var 5))) :=
  internal_unique_point
example : twk Rigidity = Rigidity := rigidity_type_closed
example (σ : Nat → Poly) : subst σ Uniqueness = Uniqueness := uniqueness_term_closed σ
example : Scoped 0 (abstract uniqueUniformProof) :=
  scoped_abstract (scoped_abstract (scoped_abstract (scoped_abstract
    (scoped_abstract (scoped_abstract (scoped_abstract uniquePointProof_scoped))))))
#print axioms rigidity_implies_internal_uniqueness
end InternalUniquenessIndependentReview
