import ModalUnion
namespace ModalUnion.Controls
open ModalUnion

abbrev Carrier := Fin 3
abbrev World := Fin 3

def chainFrame : Frame Carrier World where
  admissible := fun _ => True
  crossing := fun w x y => (w = 1 ∧ x = 0 ∧ y = 1) ∨ (w = 2 ∧ x = 1 ∧ y = 2)

instance (w : World) : Decidable (chainFrame.admissible w) :=
  inferInstanceAs (Decidable True)
instance (w : World) (x y : Carrier) : Decidable (chainFrame.crossing w x y) := by
  unfold chainFrame
  infer_instance

def available (w : World) (x : Carrier) : Prop :=
  w = 0 ∨ (w = 1 ∧ x ≠ 2) ∨ (w = 2 ∧ x ≠ 0)

instance (w : World) (x : Carrier) : Decidable (available w x) := by
  unfold available
  infer_instance

theorem crossing_endpoints_available :
    ∀ w x y, chainFrame.crossing w x y → available w x ∧ available w y := by decide

theorem edge01 : Connected chainFrame 0 1 :=
  .edge ⟨1, trivial, Or.inl (by decide)⟩
theorem edge12 : Connected chainFrame 1 2 :=
  .edge ⟨2, trivial, Or.inl (by decide)⟩
theorem union_connects_ends : Connected chainFrame 0 2 := .trans edge01 edge12

theorem no_common_world_for_two_edges :
    ¬ ∃ w, chainFrame.crossing w 0 1 ∧ chainFrame.crossing w 1 2 := by
  intro ⟨w, hw⟩
  have incompatible : ∀ w, ¬ (chainFrame.crossing w 0 1 ∧ chainFrame.crossing w 1 2) := by decide
  exact incompatible w hw

def constantAnchor (_ : Carrier) : Bool := false

theorem constant_anchor_edgeLaw : EdgeLaw chainFrame constantAnchor := by
  intro _ _ _ _ _
  rfl

def positiveInterpretation : FaithfulInterpretation chainFrame :=
  identityExpansion Bool constantAnchor constant_anchor_edgeLaw

theorem forced_common_source : ForcedEqual chainFrame 0 2 :=
  (forcedEqual_iff_connected chainFrame 0 2).mpr union_connects_ends

theorem unrepresented_source : ∀ x, constantAnchor x ≠ true := by decide

/-- Rigid Bool source identities; carrier 1 changes its local source in world 2. -/
def switchedAnchor (x : Carrier) : Bool := decide (x = 2)
def switchedLocal (w : World) (x : Carrier) : Bool := decide (x = 2 ∨ (w = 2 ∧ x = 1))

theorem switched_local_unity :
    ∀ w x y, chainFrame.admissible w → chainFrame.crossing w x y →
      switchedLocal w x = switchedLocal w y := by decide

theorem identity_transport_reflects :
    ∀ (_w : World) (s t : Bool), s = t → s = t := by
  intro _ _ _ h
  exact h

theorem retained_provenance_fails : switchedLocal 2 1 ≠ switchedAnchor 1 := by decide

theorem anchored_ends_differ : switchedAnchor 0 ≠ switchedAnchor 2 := by decide

theorem switched_anchor_law_fails : ¬ EdgeLaw chainFrame switchedAnchor := by
  intro h
  have different : switchedAnchor 1 ≠ switchedAnchor 2 := by decide
  exact different (h 2 1 2 trivial (by decide))

/-- The local graph lacks an end-to-end path in each individual world. -/
def singleWorld (w : World) : Frame Carrier Unit where
  admissible := fun _ => True
  crossing := fun _ x y => chainFrame.crossing w x y

theorem no_world_connects_ends : ∀ w, ¬ Connected (singleWorld w) 0 2 := by
  intro w hc
  have law : EdgeLaw (singleWorld w) (switchedLocal w) := by
    intro _ x y _ he
    exact switched_local_unity w x y trivial he
  have different : ∀ w, switchedLocal w 0 ≠ switchedLocal w 2 := by decide
  exact different w (connected_equal law hc)

/-- Distinct anchors collapse under transport; retained labels alone do not suffice. -/
def collapseFrame : Frame Bool Bool where
  admissible := fun _ => True
  crossing := fun w x y => w = true ∧ x = false ∧ y = true

instance (w : Bool) : Decidable (collapseFrame.admissible w) :=
  inferInstanceAs (Decidable True)
instance (w x y : Bool) : Decidable (collapseFrame.crossing w x y) := by
  unfold collapseFrame
  infer_instance

def collapsingTransport (w s : Bool) : Bool := if w then false else s

theorem collapsing_local_unity :
    ∀ w x y, collapseFrame.admissible w → collapseFrame.crossing w x y →
      collapsingTransport w x = collapsingTransport w y := by decide

theorem collapsing_provenance_retained :
    ∀ w x y, collapseFrame.admissible w → collapseFrame.crossing w x y →
      collapsingTransport w x = collapsingTransport w (id x) ∧
      collapsingTransport w y = collapsingTransport w (id y) := by
  intro _ _ _ _ _
  exact ⟨rfl, rfl⟩

theorem reflection_fails :
    collapsingTransport true false = collapsingTransport true true ∧ (false : Bool) ≠ true :=
  by decide

theorem collapse_union_connected : Connected collapseFrame false true :=
  .edge ⟨true, trivial, Or.inl (by decide)⟩

theorem collapse_anchor_law_fails : ¬ EdgeLaw collapseFrame (id : Bool → Bool) := by
  intro h
  have different : (false : Bool) ≠ true := by decide
  exact different (h true false true trivial (by decide))

/-- A complete negative certificate for this exact finite declared frame. -/
def disconnectedFrame : Frame Bool Unit where
  admissible := fun _ => True
  crossing := fun _ _ _ => False

theorem twoColor_negative_certificate : EdgeLaw disconnectedFrame (id : Bool → Bool) := by
  intro _ _ _ _ h
  exact False.elim h

theorem disconnected_ends : ¬ Connected disconnectedFrame false true := by
  intro h
  have different : (false : Bool) ≠ true := by decide
  exact different (connected_equal twoColor_negative_certificate h)

theorem disconnected_not_forced : ¬ ForcedEqual disconnectedFrame false true := by
  intro h
  exact disconnected_ends ((forcedEqual_iff_connected disconnectedFrame false true).mp h)

theorem disconnected_not_expanded_forced : ¬ ExpandedForced disconnectedFrame false true := by
  intro h
  exact disconnected_ends ((expandedForced_iff_connected disconnectedFrame false true).mp h)

theorem singleton_source_always_equal : ∀ a : Bool → Unit, a false = a true := by
  intro a
  exact Subsingleton.elim _ _

theorem singleton_caveat :
    (∀ a : Bool → Unit, EdgeLaw disconnectedFrame a → a false = a true) ∧
      ¬ Connected disconnectedFrame false true := by
  exact ⟨fun a _ => singleton_source_always_equal a, disconnected_ends⟩

theorem retention_drop_countermodel :
    (∀ (_w : World) (s t : Bool), s = t → s = t) ∧
    (∀ w x y, chainFrame.admissible w → chainFrame.crossing w x y →
      switchedLocal w x = switchedLocal w y) ∧
    Connected chainFrame 0 2 ∧ switchedAnchor 0 ≠ switchedAnchor 2 ∧
    switchedLocal 2 1 ≠ switchedAnchor 1 := by
  exact ⟨identity_transport_reflects, switched_local_unity, union_connects_ends,
    anchored_ends_differ, retained_provenance_fails⟩

theorem reflection_drop_countermodel :
    (∀ w x y, collapseFrame.admissible w → collapseFrame.crossing w x y →
      collapsingTransport w x = collapsingTransport w y) ∧
    (∀ w x y, collapseFrame.admissible w → collapseFrame.crossing w x y →
      collapsingTransport w x = collapsingTransport w (id x) ∧
      collapsingTransport w y = collapsingTransport w (id y)) ∧
    Connected collapseFrame false true ∧ (false : Bool) ≠ true ∧
    ¬ (∀ w s t, collapsingTransport w s = collapsingTransport w t → s = t) := by
  refine ⟨collapsing_local_unity, collapsing_provenance_retained,
    collapse_union_connected, by decide, ?_⟩
  intro h
  exact reflection_fails.2 (h true false true reflection_fails.1)

def higherFrame : Frame (ULift.{1} Bool) Unit where
  admissible := fun _ => True
  crossing := fun _ _ _ => False

theorem higher_universe_contract (x y : ULift.{1} Bool) :
    ForcedEqual higherFrame x y ↔ Connected higherFrame x y :=
  forcedEqual_iff_connected higherFrame x y

/- Direct contract checks at the requested core declarations. -/
#check forcedEqual_iff_connected
#check expandedForced_iff_connected
#check source_unique_of_covered_connected

end ModalUnion.Controls
