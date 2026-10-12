import SourceRaw

/- A finite observation summary is not automatically a full algebra quotient.
This file states all extra premises needed for the quotient obstruction. -/
namespace FiniteRawObstruction.Source
open OrthemologyV2 OrthemologyV3
universe u

/-- Every element is represented by a closed source raw term; application is
total/compositional and every actual raw conversion is respected as equality. -/
structure ClosedRawImage (A : Type u) where
  denote : Term → A
  app : A → A → A
  denote_app : ∀ t u, denote (.app t u) = app (denote t) (denote u)
  conversion : ∀ {t u}, Conv t u → denote t = denote u
  surjective : Function.Surjective denote

def ClosedRawImage.toTotalK {A : Type u} (D : ClosedRawImage A) : TotalK A where
  app := D.app
  k := D.denote .k
  k_law := by
    intro x y
    obtain ⟨t, rfl⟩ := D.surjective x
    obtain ⟨u, rfl⟩ := D.surjective y
    simpa only [D.denote_app] using D.conversion (Conv.step (Step.k t u))

theorem finite_closed_image_subsingleton {A : Type u} [Finite A]
    (D : ClosedRawImage A) : Subsingleton A :=
  D.toTotalK.finite_subsingleton

theorem finite_closed_image_no_separation {A : Type u} [Finite A]
    (D : ClosedRawImage A) (t u : Term) : D.denote t = D.denote u :=
  (finite_closed_image_subsingleton D).elim _ _

/-- The conventional full applicative-congruence-quotient contract. -/
def quotientImage (r : Setoid Term)
    (app_congr : ∀ {t t' u u'}, r.r t t' → r.r u u' →
      r.r (.app t u) (.app t' u'))
    (includes_conversion : ∀ {t u}, Conv t u → r.r t u) :
    ClosedRawImage (Quotient r) where
  denote := Quotient.mk r
  app := Quotient.map₂ Term.app (fun _ _ h _ _ g => app_congr h g)
  denote_app := fun _ _ => rfl
  conversion := fun h => Quotient.sound (includes_conversion h)
  surjective := Quotient.mk_surjective

theorem finite_raw_congruence_quotient_subsingleton (r : Setoid Term)
    [Finite (Quotient r)]
    (app_congr : ∀ {t t' u u'}, r.r t t' → r.r u u' →
      r.r (.app t u) (.app t' u'))
    (includes_conversion : ∀ {t u}, Conv t u → r.r t u) :
    Subsingleton (Quotient r) :=
  finite_closed_image_subsingleton (quotientImage r app_congr includes_conversion)

/-- Hence such a finite congruence relates every pair of original raw terms. -/
theorem finite_raw_congruence_universal (r : Setoid Term)
    [Finite (Quotient r)]
    (app_congr : ∀ {t t' u u'}, r.r t t' → r.r u u' →
      r.r (.app t u) (.app t' u'))
    (includes_conversion : ∀ {t u}, Conv t u → r.r t u) (t u : Term) :
    r.r t u := by
  exact Quotient.exact
    ((finite_raw_congruence_quotient_subsingleton r app_congr includes_conversion).elim
      (Quotient.mk r t) (Quotient.mk r u))

#print axioms ClosedRawImage.toTotalK
#print axioms finite_closed_image_subsingleton
#print axioms finite_raw_congruence_quotient_subsingleton
#print axioms finite_raw_congruence_universal
end FiniteRawObstruction.Source
