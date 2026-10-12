import AssemblyControls
namespace P01AC.ExtensionalRepair.InternalGraph.BridgeAssembly.IndependentReview
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness
open P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair.CompilerBodyControl
open FullPER.Application (originalQ)
example : scalarContext = [A, End, N] := rfl
example : twkTel [N] = [N] := rfl
example {Γ : Tel} {x : Poly} :
    theta Γ A x = Ty.identity (wk A) (pren Nat.succ x) (.var 0) :: A :: Γ := rfl
example (p q : Poly)
    (hp : HasE [A, End, N] p (.identity S
      (fstPoly (graphRun (.var 2) (.var 1) (.var 0))) (stateRun (.var 2))))
    (hq : HasE [A, End, N] q (.identity A
      (fstPoly (sndPoly (graphRun (.var 2) (.var 1) (.var 0))))
      (.app (.app (.var 2) (.var 1)) (.var 0)))) :
    HasE [] (abstract (abstract (abstract (.atom .i))))
      (.pi N (.all (.pi End (.pi A (.identity A
        (.app (.app (.var 2) (.var 1)) (.var 0))
        (.app (.app (.app P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed
          (.var 2)) (.var 1)) (.var 0))))))) :=
  scalar_fusion_from_bridges hp hq
#print axioms scalar_fusion_from_bridges
end P01AC.ExtensionalRepair.InternalGraph.BridgeAssembly.IndependentReview
