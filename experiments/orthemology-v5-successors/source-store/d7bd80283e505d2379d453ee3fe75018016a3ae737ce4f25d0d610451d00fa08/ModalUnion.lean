/-
Modal union source certificates. Lean 4.19.0, core only.
All admissibility and provenance predicates are assumptions, not metaphysical claims.
-/
namespace ModalUnion
universe u v w l

structure Frame (V : Type u) (W : Type w) where
  admissible : W → Prop
  crossing : W → V → V → Prop

variable {V : Type u} {W : Type w} {S : Type v}

def UnionEdge (F : Frame V W) (x y : V) : Prop :=
  ∃ z, F.admissible z ∧ (F.crossing z x y ∨ F.crossing z y x)

/-- The finite equivalence closure; witnesses need not use a common world. -/
inductive Connected (F : Frame V W) : V → V → Prop
  | refl (x) : Connected F x x
  | edge {x y} : UnionEdge F x y → Connected F x y
  | symm {x y} : Connected F x y → Connected F y x
  | trans {x y z} : Connected F x y → Connected F y z → Connected F x z

def EdgeLaw (F : Frame V W) (a : V → S) : Prop :=
  ∀ z x y, F.admissible z → F.crossing z x y → a x = a y

theorem unionEdge_equal {F : Frame V W} {a : V → S}
    (law : EdgeLaw F a) {x y} (h : UnionEdge F x y) : a x = a y := by
  obtain ⟨z, hz, hxy | hyx⟩ := h
  · exact law z x y hz hxy
  · exact (law z y x hz hyx).symm

theorem connected_equal {F : Frame V W} {a : V → S}
    (law : EdgeLaw F a) {x y} (h : Connected F x y) : a x = a y := by
  induction h with
  | refl => rfl
  | edge h => exact unionEdge_equal law h
  | symm _ ih => exact ih.symm
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂

/-- Source universe is the carrier universe: Quotient V is an allowed source type. -/
def ForcedEqual (F : Frame V W) (x y : V) : Prop :=
  ∀ (S' : Type u) (a : V → S'), EdgeLaw F a → a x = a y

def componentSetoid (F : Frame V W) : Setoid V where
  r := Connected F
  iseqv := ⟨Connected.refl, Connected.symm, Connected.trans⟩

def component (F : Frame V W) (x : V) : Quotient (componentSetoid F) :=
  Quotient.mk (componentSetoid F) x

theorem component_edgeLaw (F : Frame V W) : EdgeLaw F (component F) := by
  intro z x y hz hxy
  exact Quotient.sound (Connected.edge ⟨z, hz, Or.inl hxy⟩)

theorem component_equal_iff (F : Frame V W) (x y : V) :
    component F x = component F y ↔ Connected F x y := by
  constructor
  · exact Quotient.exact
  · intro h
    exact @Quotient.sound V (componentSetoid F) x y h

theorem forcedEqual_iff_connected (F : Frame V W) (x y : V) :
    ForcedEqual F x y ↔ Connected F x y := by
  constructor
  · intro h
    exact (component_equal_iff F x y).mp
      (h (Quotient (componentSetoid F)) (component F) (component_edgeLaw F))
  · intro h S' a law
    exact connected_equal law h

theorem disconnected_component_separator {F : Frame V W} {x y : V}
    (h : ¬ Connected F x y) :
    EdgeLaw F (component F) ∧ component F x ≠ component F y := by
  exact ⟨component_edgeLaw F, fun heq => h ((component_equal_iff F x y).mp heq)⟩

theorem edgeLaw_of_faithful_transport {F : Frame V W} (a : V → S)
    {Local : W → Type l} (transport : (z : W) → S → Local z)
    (localSource : (z : W) → V → Local z)
    (reflect : ∀ z s t, transport z s = transport z t → s = t)
    (retain : ∀ z x y, F.admissible z → F.crossing z x y →
      localSource z x = transport z (a x) ∧ localSource z y = transport z (a y))
    (localUnity : ∀ z x y, F.admissible z → F.crossing z x y →
      localSource z x = localSource z y) : EdgeLaw F a := by
  intro z x y hz he
  obtain ⟨hx, hy⟩ := retain z x y hz he
  exact reflect z (a x) (a y) (hx.symm.trans ((localUnity z x y hz he).trans hy))

/-- Sw, transports and labels vary; the world/crossing frame stays fixed. -/
structure FaithfulInterpretation (F : Frame V W) where
  Source : Type u
  anchor : V → Source
  Local : W → Type u
  transport : (z : W) → Source → Local z
  localSource : (z : W) → V → Local z
  reflects : ∀ z s t, transport z s = transport z t → s = t
  retains : ∀ z x y, F.admissible z → F.crossing z x y →
    localSource z x = transport z (anchor x) ∧ localSource z y = transport z (anchor y)
  unity : ∀ z x y, F.admissible z → F.crossing z x y →
    localSource z x = localSource z y

def identityExpansion {F : Frame V W} (S' : Type u) (a : V → S')
    (law : EdgeLaw F a) : FaithfulInterpretation F where
  Source := S'
  anchor := a
  Local := fun _ => S'
  transport := fun _ s => s
  localSource := fun _ => a
  reflects := fun _ _ _ h => h
  retains := fun _ _ _ _ _ => ⟨rfl, rfl⟩
  unity := law

theorem FaithfulInterpretation.edgeLaw {F : Frame V W}
    (I : FaithfulInterpretation F) : EdgeLaw F I.anchor :=
  edgeLaw_of_faithful_transport I.anchor I.transport I.localSource I.reflects I.retains I.unity

def ExpandedForced (F : Frame V W) (x y : V) : Prop :=
  ∀ I : FaithfulInterpretation F, I.anchor x = I.anchor y

theorem expandedForced_iff_forced (F : Frame V W) (x y : V) :
    ExpandedForced F x y ↔ ForcedEqual F x y := by
  constructor
  · intro h S' a law
    exact h (identityExpansion S' a law)
  · intro h I
    exact h I.Source I.anchor I.edgeLaw

theorem expandedForced_iff_connected (F : Frame V W) (x y : V) :
    ExpandedForced F x y ↔ Connected F x y :=
  (expandedForced_iff_forced F x y).trans (forcedEqual_iff_connected F x y)

theorem target_constancy {F : Frame V W} {a : V → S} (law : EdgeLaw F a)
    (target : V → Prop) (root : V)
    (paths : ∀ x, target x → Connected F root x) :
    ∀ x, target x → a x = a root := by
  intro x hx
  exact (connected_equal law (paths x hx)).symm

def TargetForced (F : Frame V W) (target : V → Prop) (root : V) : Prop :=
  ∀ (S' : Type u) (a : V → S'), EdgeLaw F a → ∀ x, target x → a x = a root

theorem targetForced_iff_connected (F : Frame V W) (target : V → Prop) (root : V) :
    TargetForced F target root ↔ ∀ x, target x → Connected F root x := by
  constructor
  · intro h x hx
    exact (component_equal_iff F root x).mp
      ((h (Quotient (componentSetoid F)) (component F) (component_edgeLaw F) x hx).symm)
  · intro h S' a law
    exact target_constancy law target root h

theorem source_unique_of_covered_connected {F : Frame V W} {a : V → S}
    (law : EdgeLaw F a) (target : V → Prop) (relevant : S → Prop) (root : V)
    (paths : ∀ x, target x → Connected F root x)
    (covered : ∀ s, relevant s → ∃ x, target x ∧ a x = s) :
    ∀ s, relevant s → s = a root := by
  intro s hs
  obtain ⟨x, hx, hxs⟩ := covered s hs
  exact hxs.symm.trans (target_constancy law target root paths x hx)

/-- Optional two-color separator. Classical decidability is explicit in its proof. -/
theorem disconnected_bool_separator {F : Frame V W} {x y : V}
    (h : ¬ Connected F x y) :
    ∃ a : V → Bool, EdgeLaw F a ∧ a x ≠ a y := by
  classical
  let a : V → Bool := fun z => if Connected F x z then true else false
  have law : EdgeLaw F a := by
    intro z p q hz he
    have edge : Connected F p q := .edge ⟨z, hz, Or.inl he⟩
    by_cases hp : Connected F x p
    · have hq : Connected F x q := .trans hp edge
      simp only [a, if_pos hp, if_pos hq]
    · have hq : ¬ Connected F x q := fun hq => hp (.trans hq (.symm edge))
      simp only [a, if_neg hp, if_neg hq]
  refine ⟨a, law, ?_⟩
  simp only [a, if_pos (Connected.refl x), if_neg h]
  decide

end ModalUnion
