/- P01 U09 proposal. UNVERIFIED at Lean 4.19.0.
   Generic positive-simulation lemma only. No System F typing, translation,
   or System F normalisation theorem is silently supplied as an axiom. -/
import Init
namespace P01SNReflection
universe u v

inductive Star {X : Sort u} (r : X → X → Prop) : X → X → Prop where
  | refl (x : X) : Star r x x
  | tail {x y z : X} : r x y → Star r y z → Star r x z

def Positive {X : Sort u} (r : X → X → Prop) (x y : X) : Prop :=
  ∃ z, r x z ∧ Star r z y

def SN {X : Sort u} (r : X → X → Prop) (x : X) : Prop :=
  Acc (fun y x => r x y) x

private theorem reflect_aux {X : Sort u} {Y : Sort v}
    (r : X → X → Prop) (s : Y → Y → Prop) (f : X → Y)
    (simulation : ∀ {a b}, r a b → Positive s (f a) (f b))
    {y : Y} (hy : SN s y) :
    ∀ a, Star s y (f a) → SN r a := by
  induction hy with
  | intro y next ih =>
      intro a path
      cases path with
      | refl =>
          apply Acc.intro
          intro b hab
          obtain ⟨z, first, rest⟩ := simulation hab
          exact ih z first b rest
      | tail first rest => exact ih _ first a rest

theorem positive_simulation_reflects_SN {X : Sort u} {Y : Sort v}
    (r : X → X → Prop) (s : Y → Y → Prop) (f : X → Y)
    (simulation : ∀ {a b}, r a b → Positive s (f a) (f b))
    {a : X} (h : SN s (f a)) : SN r a :=
  reflect_aux r s f simulation h a (.refl _)

end P01SNReflection
