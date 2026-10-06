/- Deliberate rejected interface use. This is not a logical independence proof. -/
import EffectivePartialObserver
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.IdentityComplexity

example {left right : Term} {ρ : OEnv} {η : Env} {n : Nat}
    (hr : F N ρ η right right)
    (cl : ∀ f x, Conv (.app (.app left f) x) (iterateTerm f n x))
    (cr : ∀ f x, Conv (.app (.app right f) x) (iterateTerm f n x)) :
    F N ρ η left right :=
  same_index_related (left := left) (right := right) cl hr cl cr
