/- Represented dependent Sigma laws from smaller syntax-induction conclusions. -/
import TypedPiLaws
namespace P01TC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

theorem type_sigma {Γ A B} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hb : TypeLaws (A :: Γ) B) : TypeLaws Γ (.sigma A B) := by
  have pf : ∀ {ρ η}, D Γ ρ η → RelLaws (F (.sigma A B) ρ η) := by
    intro ρ η d
    have la := ha.per d
    exact {
      sym := by
        intro z w h
        have e : E (A :: Γ) ρ (cons (firstTerm z) η) (cons (firstTerm w) η) := ⟨hc.refl d,h.2.2.1⟩
        exact ⟨h.2.1,h.1,la.sym h.2.2.1,
          (hb.transport e _ _).mp ((hb.per ⟨d,la.left h.2.2.1⟩).sym h.2.2.2)⟩
      trans := by
        intro z w v h k
        have e : E (A :: Γ) ρ (cons (firstTerm z) η) (cons (firstTerm w) η) := ⟨hc.refl d,h.2.2.1⟩
        exact ⟨h.1,k.2.1,la.trans h.2.2.1 k.2.2.1,
          (hb.per ⟨d,la.left h.2.2.1⟩).trans h.2.2.2 ((hb.transport e _ _).mpr k.2.2.2)⟩
      raw := by
        intro z w z' w' cz cw h
        have fz := Conv.left cz .k
        have fw := Conv.left cw .k
        have sz := Conv.left cz (.app .k .i)
        have sw := Conv.left cw (.app .k .i)
        have e : E (A :: Γ) ρ (cons (firstTerm z) η) (cons (firstTerm z') η) :=
          ⟨hc.refl d,la.raw (.refl _) fz (la.left h.2.2.1)⟩
        exact ⟨represented_raw cz h.1,represented_raw cw h.2.1,la.raw fz fw h.2.2.1,
          (hb.transport e _ _).mp ((hb.per ⟨d,la.left h.2.2.1⟩).raw sz sw h.2.2.2)⟩ }
  have ft : ∀ {ρ η ξ}, E Γ ρ η ξ → ∀ z w, F (.sigma A B) ρ η z w ↔ F (.sigma A B) ρ ξ z w := by
    intro ρ η ξ e z w
    have ds := hc.ends e
    constructor
    · intro h
      have ex : E (A :: Γ) ρ (cons (firstTerm z) η) (cons (firstTerm z) ξ) :=
        ⟨e,(ha.per ds.1).left h.2.2.1⟩
      exact ⟨h.1,h.2.1,(ha.transport e _ _).mp h.2.2.1,(hb.transport ex _ _).mp h.2.2.2⟩
    · intro h
      have hz := (ha.transport e _ _).mpr h.2.2.1
      have ex : E (A :: Γ) ρ (cons (firstTerm z) η) (cons (firstTerm z) ξ) :=
        ⟨e,(ha.per ds.1).left hz⟩
      exact ⟨h.1,h.2.1,hz,(hb.transport ex _ _).mpr h.2.2.2⟩
  exact {
    per := pf
    transport := ft
    ends := by intro r η ξ dη dξ z w h; exact ⟨h.1,h.2.1⟩
    respect := by
      intro r η ξ dη dξ z z' w w' zz ww h
      have ds := ha.ends dη dξ h.2.2.2.2.1
      have ez : E (A :: Γ) r.left (cons (firstTerm z) η) (cons (firstTerm z') η) := ⟨hc.refl dη,zz.2.2.1⟩
      have ew : E (A :: Γ) r.right (cons (firstTerm w) ξ) (cons (firstTerm w') ξ) := ⟨hc.refl dξ,ww.2.2.1⟩
      exact ⟨(pf dη).right zz,(pf dξ).right ww,zz.2.1,ww.2.1,
        ha.respect dη dξ zz.2.2.1 ww.2.2.1 h.2.2.2.2.1,
        (hb.invariant ez ew _ _).mp (hb.respect ⟨dη,ds.1⟩ ⟨dξ,ds.2⟩ zz.2.2.2 ww.2.2.2 h.2.2.2.2.2)⟩
    invariant := by
      intro r η η' ξ ξ' e f z w
      have dl := hc.ends e
      have dr := hc.ends f
      constructor
      · intro h
        have ds := ha.ends dl.1 dr.1 h.2.2.2.2.1
        have ez : E (A :: Γ) r.left (cons (firstTerm z) η) (cons (firstTerm z) η') := ⟨e,ds.1⟩
        have ew : E (A :: Γ) r.right (cons (firstTerm w) ξ) (cons (firstTerm w) ξ') := ⟨f,ds.2⟩
        exact ⟨(ft e _ _).mp h.1,(ft f _ _).mp h.2.1,h.2.2.1,h.2.2.2.1,
          (ha.invariant e f _ _).mp h.2.2.2.2.1,(hb.invariant ez ew _ _).mp h.2.2.2.2.2⟩
      · intro h
        have xy := (ha.invariant e f _ _).mpr h.2.2.2.2.1
        have ds := ha.ends dl.1 dr.1 xy
        have ez : E (A :: Γ) r.left (cons (firstTerm z) η) (cons (firstTerm z) η') := ⟨e,ds.1⟩
        have ew : E (A :: Γ) r.right (cons (firstTerm w) ξ) (cons (firstTerm w) ξ') := ⟨f,ds.2⟩
        exact ⟨(ft e _ _).mpr h.1,(ft f _ _).mpr h.2.1,h.2.2.1,h.2.2.2.1,xy,
          (hb.invariant ez ew _ _).mpr h.2.2.2.2.2⟩
    diagonal := by
      intro ρ η ξ e z w
      have ds := hc.ends e
      constructor
      · intro h
        have xy := (ha.diagonal e _ _).mp h.2.2.2.2.1
        have ex : E (A :: Γ) ρ (cons (firstTerm z) η) (cons (firstTerm w) ξ) := ⟨e,xy⟩
        exact ⟨h.2.2.1,h.2.2.2.1,xy,(hb.diagonal ex _ _).mp h.2.2.2.2.2⟩
      · intro h
        have ex : E (A :: Γ) ρ (cons (firstTerm z) η) (cons (firstTerm w) ξ) := ⟨e,h.2.2.1⟩
        exact ⟨(pf ds.1).left h,(ft e _ _).mp ((pf ds.1).right h),h.1,h.2.1,
          (ha.diagonal e _ _).mpr h.2.2.1,(hb.diagonal ex _ _).mpr h.2.2.2⟩ }

end P01TC
