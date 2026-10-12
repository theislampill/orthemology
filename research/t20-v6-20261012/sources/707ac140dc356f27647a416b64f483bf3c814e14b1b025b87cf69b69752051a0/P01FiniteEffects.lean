/- P01 U10 proposal. UNVERIFIED: no Lean runtime was available in this run.
   New declarations only. Does not alter EffectDerives or the accepted R1.
   This file proves support statements; it does not define probability mass. -/
import EffectsAndDependence
import RelationalFragment

namespace P01FiniteEffects
open OrthemologyV2 OrthemologyV3 OrthemologyV4Relations

theorem outcome_finite {e A} (h : EffectDerives e A) :
    ∀ t, Outcome e t → FiniteDerives t A := by
  induction h with
  | pure h =>
      intro t ho
      cases ho
      exact h
  | mix hl hr p ihl ihr =>
      intro t ho
      cases ho with
      | mixL _ h => exact ihl t h
      | mixR _ h => exact ihr t h
  | app hf hx ihf ihx =>
      intro t ho
      cases ho with
      | app hg hy => exact .app (ihf _ hg) (ihx _ hy)
  | allI h ih =>
      intro t ho
      exact .allI (ih t ho)
  | allE h A ih =>
      intro t ho
      exact .allE (ih t ho) A

theorem effect_fundamental_support {e A} (h : EffectDerives e A) :
    ∀ t, Outcome e t → ∀ rho, (relInterpret A rho).relates t t := by
  intro t ht rho
  exact finite_fundamental (outcome_finite h t ht) rho

/-- A single diagonal SUPPORT works for every relation environment.
    The separate ordinary proof assigns rational mass to this support. -/
theorem diagonal_support_relational {e A} (h : EffectDerives e A) :
    ∀ t u, Outcome e t → t = u →
      ∀ rho, (relInterpret A rho).relates t u := by
  intro t u ht htu rho
  cases htu
  exact effect_fundamental_support h t ht rho

end P01FiniteEffects
