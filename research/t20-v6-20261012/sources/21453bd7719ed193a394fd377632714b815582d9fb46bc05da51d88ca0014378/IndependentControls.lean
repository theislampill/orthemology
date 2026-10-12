import UniquenessConverse
namespace ConverseIndependentReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open SourceRigidity RigidityInitiality InternalRecursorPrinciple

-- Two actual closed source implications between the exact unchanged formulas.
example : HasE [] (abstract uniqueUniformProof) (arr Rigidity Uniqueness) ∧
    HasE [] (abstract (abstract (abstract (abstract ident)))) (arr Uniqueness Rigidity) :=
  ⟨rigidity_implies_internal_uniqueness, internal_uniqueness_implies_rigidity⟩
example : Scoped 0 (abstract (abstract (abstract (abstract ident)))) :=
  hasE_scoped internal_uniqueness_implies_rigidity

-- Arbitrary source evidence has scope; no weakening or substitution rule is claimed.
example {Γ : Tel} {p : Poly} {X : Ty} (h : HasE Γ p X) : Scoped Γ.length p := hasE_scoped h

-- Actual All elimination at N preserves both exact recursor endpoints.
example {Γ : Tel} {w u z s : Poly} (hc : Ctx Γ)
    (hw : HasE Γ w Uniqueness) (hu : Has Γ u NT)
    (hz : Has Γ z (ZeroAt u)) (hs : Has Γ s (StepAt u)) :
    ∃ e, HasE Γ e (.pi N (.identity N
      (.app (pren Nat.succ u) (.var 0))
      (.app (.app (.var 0) P01AC.BooleanPrimitive.succPoly) zero))) :=
  uniqueness_nat_instance hc hw hu hz hs

-- Source piExt returns the exact Rigidity direction I=u, not its reverse.
example {Γ : Tel} {w u z s : Poly} (hc : Ctx Γ)
    (hw : Has Γ w Uniqueness) (hu : Has Γ u NT)
    (hz : Has Γ z (ZeroAt u)) (hs : Has Γ s (StepAt u)) :
    HasE Γ ident (.identity (arr N N) ident u) := uniqueness_endomorphism hc hw hu hz hs
#print axioms internal_uniqueness_implies_rigidity
end ConverseIndependentReview
