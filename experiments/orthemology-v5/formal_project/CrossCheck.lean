/- Direct use of the pinned upstream theorem. Not an additional foundational axiom.
   Candidate source: kernel acceptance requires the real build and audit. -/
import Counterexamples.Girard

namespace OrthemologyConvergence
universe u

theorem upstreamGirard
    (pi : (Type u → Type u) → Type u)
    (lam : ∀ {A : Type u → Type u}, (∀ x, A x) → pi A)
    (app : ∀ {A}, pi A → ∀ x, A x)
    (beta : ∀ {A : Type u → Type u} (f : ∀ x, A x) (x), app (lam f) x = f x) : False :=
  Counterexample.girard pi lam app beta

end OrthemologyConvergence
