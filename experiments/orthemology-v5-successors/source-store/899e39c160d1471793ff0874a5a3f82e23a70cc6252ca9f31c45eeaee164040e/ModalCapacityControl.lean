import GroundExtensionControls

namespace T20.GroundExtension.Controls

/-!
A nonvacuous interpretation of standing capacity. The ground actually exercises
productive power at another modal index, on a new effect. It does not productively
cause the old actual field, even by productive ancestry. No unrestricted perfection
schema or metaphysical possibility is certified by this finite interpretation.
-/

inductive ModalNode where
  | ground | holder | effect | extra
  deriving DecidableEq

open ModalNode

def modalE (w : Bool) : ModalNode → Prop
  | ground => True
  | holder => True
  | effect => w = false
  | extra => w = true

def modalP (w : Bool) (a b : ModalNode) : Prop :=
  (w = false ∧ a = holder ∧ b = effect) ∨
  (w = true ∧ a = ground ∧ b = extra)

def modalG (_ : Bool) (a b : ModalNode) : Prop := a = ground ∧ b = holder
def modalS (w : Bool) (a b : ModalNode) : Prop := modalG w a b ∨ modalP w a b
def modalAble (a : ModalNode) : Prop := ∃ w b, modalP w a b

def embedOld : Bool → ModalNode
  | false => holder
  | true => effect

theorem modal_ground_root (w : Bool) : Root modalE modalS w ground := by
  constructor
  · exact True.intro
  · intro a h
    cases h with
    | inl h => cases h.2
    | inr h =>
      cases h with
      | inl h => cases h.2.2
      | inr h => cases h.2.2

theorem modal_actual_root_iff (a : ModalNode) :
    Root modalE modalS false a ↔ a = ground := by
  constructor
  · intro h
    cases a with
    | ground => rfl
    | holder => exact False.elim (h.2 ground (Or.inl ⟨rfl, rfl⟩))
    | effect =>
      exact False.elim (h.2 holder (Or.inr (Or.inl ⟨rfl, rfl, rfl⟩)))
    | extra => cases h.1
  · intro h
    subst a
    exact modal_ground_root false

theorem modal_actual_coverage : Coverage modalE modalS false := by
  intro a ha
  refine ⟨ground, modal_ground_root false, ?_⟩
  cases a with
  | ground => exact Path.refl ground
  | holder => exact Path.tail (Path.refl ground) (Or.inl ⟨rfl, rfl⟩)
  | effect =>
    have first : Path (modalS false) ground holder :=
      Path.tail (Path.refl ground) (Or.inl ⟨rfl, rfl⟩)
    exact Path.tail first (Or.inr (Or.inl ⟨rfl, rfl, rfl⟩))
  | extra => cases ha

theorem modal_ground_necessitates : GroundNecessitates modalE modalG := by
  intro w a b hab v _
  have hb : b = holder := hab.2
  subst b
  exact True.intro

theorem modal_ground_capable : modalAble ground := by
  exact ⟨true, extra, Or.inr ⟨rfl, rfl, rfl⟩⟩

theorem modal_ground_not_actual_producer : ¬ ∃ b, modalP false ground b := by
  intro h
  obtain ⟨b, h⟩ := h
  cases h with
  | inl h => cases h.2.1
  | inr h => cases h.1

theorem modal_actual_productive_path_stays_ground {a : ModalNode}
    (h : Path (modalP false) ground a) : a = ground := by
  induction h with
  | refl => rfl
  | @tail b c h e ih =>
    subst b
    exact False.elim (modal_ground_not_actual_producer ⟨c, e⟩)

theorem modal_no_productive_ancestry_to_field :
    ¬ Path (modalP false) ground effect := by
  intro h
  have hbad := modal_actual_productive_path_stays_ground h
  cases hbad

theorem modal_old_existence_exact (w a : Bool) :
    modalE w (embedOld a) ↔ finiteE w a := by
  cases w <;> cases a <;> simp [modalE, embedOld, finiteE]

theorem modal_old_productive_exact (w a b : Bool) :
    modalP w (embedOld a) (embedOld b) ↔ finiteS w a b := by
  cases w <;> cases a <;> cases b <;> simp [modalP, embedOld, finiteS]

theorem modal_old_support_exact (w a b : Bool) :
    modalS w (embedOld a) (embedOld b) ↔ finiteS w a b := by
  cases w <;> cases a <;> cases b <;>
    simp [modalS, modalG, modalP, embedOld, finiteS]

theorem modal_old_capacity_exact (a : Bool) : modalAble (embedOld a) ↔ finiteH a := by
  cases a with
  | false =>
    constructor
    · intro _; rfl
    · intro _; exact ⟨false, effect, Or.inl ⟨rfl, rfl, rfl⟩⟩
  | true =>
    constructor
    · intro h
      obtain ⟨w, b, h⟩ := h
      cases h with
      | inl h => cases h.2.1
      | inr h => cases h.2.1
    · intro h
      cases h

theorem modal_nonvacuous_separation :
    Necessary modalE ground ∧
    (∀ w, Root modalE modalS w ground) ∧ modalAble ground ∧
    (∃ a b, modalP false a b) ∧
    ¬ ∃ a, Root modalE modalS false a ∧ ∃ b, modalP false a b := by
  refine ⟨(fun _ => True.intro), modal_ground_root, modal_ground_capable,
    ⟨holder, effect, Or.inl ⟨rfl, rfl, rfl⟩⟩, ?_⟩
  intro h
  obtain ⟨a, hr, hp⟩ := h
  have ha := (modal_actual_root_iff a).mp hr
  subst a
  exact modal_ground_not_actual_producer hp

end T20.GroundExtension.Controls
