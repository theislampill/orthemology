import SourceUniqueness
namespace UniquenessIndependentReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open SourceRigidity RigidityInitiality

-- Exact carrier is the source's generic type parameter A, with arbitrary ambient Γ.
example {Γ : Tel} {f a u z t r n : Poly} (hc : Ctx Γ)
    (hf : Has Γ f End) (ha : Has Γ a A) (hu : Has Γ u (arr N A))
    (hz : Has Γ z (.identity A (.app u zero) a)) (ht : Has Γ t (RecStep f u))
    (hr : HasE Γ r Rigidity) (hn : Has Γ n N) :
    HasE Γ (sndPoly (.app (.app n (totalStep (recTotalStep t))) (totalSeed z)))
      (.identity A (.app u n) (.app (.app n f) a)) :=
  recursor_unique_source hc hf ha hu hz ht hr hn

example (f a u n : Poly) : inst (RecFamily f a u) n =
    .identity A (.app u n) (.app (.app n f) a) := rec_family_at f a u n
example (f u n : Poly) : inst (RecStepBody f u) n =
    .identity A (.app u (.app P01AC.BooleanPrimitive.succPoly n))
      (.app f (.app u n)) := rec_step_at f u n
example {Γ : Tel} {f a u z : Poly} (hc : Ctx Γ)
    (hf : Has Γ f End) (ha : Has Γ a A) (hu : Has Γ u (arr N A))
    (hz : Has Γ z (RecStep f u)) :
    Has (total (RecFamily f a u) :: Γ) (recTotalStep z)
      (totalStepType (RecFamily f a u)) := rec_total_step_has hc hf ha hu hz

-- The uniform function computes to the exact body, for arbitrary raw polynomials.
example (p s n : Poly) : P01DF.PolyConv
    (.app (sectionPoly p s) n) (sectionBody p s n) := section_application_beta p s n
#print axioms recursor_unique_source
end UniquenessIndependentReview
