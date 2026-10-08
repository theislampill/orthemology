/- Dependent Pi laws from smaller syntax-induction conclusions. -/
import TypedLaws
namespace P01TC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

theorem type_pi {Γ A B} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hb : TypeLaws (A :: Γ) B) : TypeLaws Γ (.pi A B) := by
  have pf : ∀ {ρ η}, D Γ ρ η → RelLaws (F (.pi A B) ρ η) := by
    intro ρ η d
    have la := ha.per d
    exact {
      sym := by
        intro f g h a b ab
        have da : D (A :: Γ) ρ (cons a η) := ⟨d,la.left ab⟩
        have e : E (A :: Γ) ρ (cons b η) (cons a η) := ⟨hc.refl d,la.sym ab⟩
        have ba := (hb.per da).sym ((hb.transport e _ _).mp (h b a (la.sym ab)))
        exact ba
      trans := by
        intro f g h fg gh a b ab
        exact (hb.per ⟨d,la.left ab⟩).trans (fg a a (la.left ab)) (gh a b ab)
      raw := by
        intro f g f' g' cf cg h a b ab
        exact (hb.per ⟨d,la.left ab⟩).raw (.left cf a) (.left cg b) (h a b ab) }
  have ft : ∀ {ρ η ξ}, E Γ ρ η ξ → ∀ f g, F (.pi A B) ρ η f g ↔ F (.pi A B) ρ ξ f g := by
    intro ρ η ξ e f g
    have ds := hc.ends e
    constructor
    · intro h a b ab
      have ab' := (ha.transport e _ _).mpr ab
      exact (hb.transport ⟨e,(ha.per ds.1).left ab'⟩ _ _).mp (h a b ab')
    · intro h a b ab
      have ab' := (ha.transport e _ _).mp ab
      exact (hb.transport ⟨e,(ha.per ds.1).left ab⟩ _ _).mpr (h a b ab')
  exact {
    per := pf
    transport := ft
    ends := by intro r η ξ dη dξ f g h; exact ⟨h.1,h.2.1⟩
    respect := by
      intro r η ξ dη dξ f f' g g' ff gg h
      refine ⟨(pf dη).right ff,(pf dξ).right gg,?_⟩
      intro a b ab
      have ds := ha.ends dη dξ ab
      exact hb.respect ⟨dη,ds.1⟩ ⟨dξ,ds.2⟩ (ff a a ds.1) (gg b b ds.2) (h.2.2 a b ab)
    invariant := by
      intro r η η' ξ ξ' e f t u
      have dl := hc.ends e
      have dr := hc.ends f
      constructor
      · intro h
        refine ⟨(ft e _ _).mp h.1,(ft f _ _).mp h.2.1,?_⟩
        intro a b ab
        have ab' := (ha.invariant e f _ _).mpr ab
        have ds := ha.ends dl.1 dr.1 ab'
        exact (hb.invariant ⟨e,ds.1⟩ ⟨f,ds.2⟩ _ _).mp (h.2.2 a b ab')
      · intro h
        refine ⟨(ft e _ _).mpr h.1,(ft f _ _).mpr h.2.1,?_⟩
        intro a b ab
        have ab' := (ha.invariant e f _ _).mp ab
        have ds := ha.ends dl.1 dr.1 ab
        exact (hb.invariant ⟨e,ds.1⟩ ⟨f,ds.2⟩ _ _).mpr (h.2.2 a b ab')
    diagonal := by
      intro ρ η ξ e f g
      have ds := hc.ends e
      constructor
      · intro h a b ab
        exact (hb.diagonal ⟨e,ab⟩ _ _).mp (h.2.2 a b ((ha.diagonal e _ _).mpr ab))
      · intro h
        refine ⟨(pf ds.1).left h,(ft e _ _).mp ((pf ds.1).right h),?_⟩
        intro a b ab
        have ab' := (ha.diagonal e _ _).mp ab
        exact (hb.diagonal ⟨e,ab'⟩ _ _).mpr (h a b ab') }

end P01TC
