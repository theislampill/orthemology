import Mathlib

/-!
# Exact source-identity implications for Orthemology tranche 3

These theorems check implication structure. They do not assert that the declared
relations correctly describe concrete actuality. The actual-root necessity core
is prior canonical h-modal Theorem 1. The generic-reception premise has the
Principle of Metaphysical Insufficiency as philosophical ancestry (Rydéhn).
-/

namespace Orthemology.Tranche3.SourceIdentity

variable {W D : Type*}

def Received (dep : W → D → D → Prop) (w : W) (x : D) : Prop :=
  ∃ y, dep w y x

def Root (ex : W → D → Prop) (dep : W → D → D → Prop)
    (w : W) (x : D) : Prop :=
  ex w x ∧ ¬ Received dep w x

def Necessary (ex : W → D → Prop) (x : D) : Prop := ∀ w, ex w x

def UniformRoot (ex : W → D → Prop) (dep : W → D → D → Prop) (x : D) : Prop :=
  ∀ w, Root ex dep w x

/-- Efficient-existential counterpart of Rydéhn's PoMI. Applicability of this
counterpart, rather than just the formal implication, is substantive. -/
def GenericReception (ex : W → D → Prop) (dep : W → D → D → Prop) : Prop :=
  ∀ x, (∃ w, Received dep w x) → ∀ v, ex v x → Received dep v x

/-- Preservation only for individuals actually received at `actual`.
This is too weak to constrain an actually underived individual. -/
def ActualReceptionPreservation (ex : W → D → Prop)
    (dep : W → D → D → Prop) (actual : W) : Prop :=
  ∀ x, Received dep actual x → ∀ w, ex w x → Received dep w x

/-- The prior actual-root inference, included to expose every premise in the
composed theorem, not claimed as a new deduction. -/
theorem necessary_of_actual_root
    (ex : W → D → Prop) (dep : W → D → D → Prop) (actual : W) (x : D)
    (root : Root ex dep actual x)
    (contingent_receives : ∀ y, ex actual y → ¬ Necessary ex y → Received dep actual y) :
    Necessary ex x := by
  classical
  by_contra hn
  exact root.2 (contingent_receives x root.1 hn)

/-- The new application: an established actual necessary root and generic
reception imply uniform underivability of that same individual. -/
theorem uniform_of_necessary_actual_root
    (ex : W → D → Prop) (dep : W → D → D → Prop) (actual : W) (x : D)
    (root : Root ex dep actual x) (necessary : Necessary ex x)
    (reception : GenericReception ex dep) : UniformRoot ex dep x := by
  intro w
  refine ⟨necessary w, ?_⟩
  intro hw
  exact root.2 (reception x ⟨w, hw⟩ actual root.1)

theorem uniform_of_contingent_reception
    (ex : W → D → Prop) (dep : W → D → D → Prop) (actual : W) (x : D)
    (root : Root ex dep actual x)
    (contingent_receives : ∀ y, ex actual y → ¬ Necessary ex y → Received dep actual y)
    (reception : GenericReception ex dep) : UniformRoot ex dep x :=
  uniform_of_necessary_actual_root ex dep actual x root
    (necessary_of_actual_root ex dep actual x root contingent_receives) reception

/-- Honesty check: after actual roothood and necessary existence are fixed,
the object-specific backward-transfer clause is equivalent to the desired
uniform conclusion. Its explanatory warrant must therefore come from an
independently defended generic doctrine, not merely from this reformulation. -/
theorem local_transfer_iff_uniform
    (ex : W → D → Prop) (dep : W → D → D → Prop) (actual : W) (x : D)
    (root : Root ex dep actual x) (necessary : Necessary ex x) :
    (∀ w, ex w x → Received dep w x → Received dep actual x) ↔
      UniformRoot ex dep x := by
  constructor
  · intro transfer w
    exact ⟨necessary w, fun h => root.2 (transfer w (necessary w) h)⟩
  · intro uniform w _ h
    exact False.elim ((uniform w).2 h)

/-- Fixed-origin transport implies generic transport, provided source edges
have existing targets. The converse is refuted by a finite fixture below. -/
theorem generic_of_fixed_origin
    (ex : W → D → Prop) (dep : W → D → D → Prop)
    (target_exists : ∀ w y x, dep w y x → ex w x)
    (fixed : ∀ w v y x, ex w x → ex v x → dep w y x → dep v y x) :
    GenericReception ex dep := by
  rintro x ⟨w, y, hdep⟩ v hv
  exact ⟨y, fixed w v y x (target_exists w y x hdep) hv hdep⟩

namespace Controls

set_option synthInstance.maxSize 4096

/-- A root can become derived even though every *actually* received bearer
retains some origin. All individuals here exist necessarily. -/
def changingDep (w : Bool) (y x : Fin 2) : Prop :=
  w = true ∧ y = 1 ∧ x = 0

theorem actual_preservation_does_not_give_uniform :
    Root (fun (_ : Bool) (_ : Fin 2) => True) changingDep false 0 ∧
    Necessary (fun (_ : Bool) (_ : Fin 2) => True) 0 ∧
    ActualReceptionPreservation (fun (_ : Bool) (_ : Fin 2) => True)
      changingDep false ∧
    ¬ UniformRoot (fun (_ : Bool) (_ : Fin 2) => True) changingDep 0 := by
  simp only [GenericReception, ActualReceptionPreservation, UniformRoot, Necessary, Root,
    Received, changingDep] 
  decide

/-- Generic reception can hold while the particular originating individual
varies. Both alleged parents exist in both worlds. -/
def variableOrigin (w : Bool) (y x : Fin 3) : Prop :=
  x = 2 ∧ ((w = false ∧ y = 0) ∨ (w = true ∧ y = 1))

theorem generic_not_fixed_origin :
    GenericReception (fun (_ : Bool) (_ : Fin 3) => True) variableOrigin ∧
    variableOrigin false 0 2 ∧ ¬ variableOrigin true 0 2 := by
  simp only [GenericReception, ActualReceptionPreservation, UniformRoot, Necessary, Root,
    Received, variableOrigin]
  decide

/-- Every dependent bearer remains dependent, yet the modal union contains a
cycle between 1 and 2. Each individual world's graph is acyclic. -/
def switchingOrder (w : Bool) (y x : Fin 3) : Prop :=
  (w = false ∧ ((y = 0 ∧ x = 1) ∨ (y = 1 ∧ x = 2))) ∨
  (w = true ∧ ((y = 0 ∧ x = 2) ∨ (y = 2 ∧ x = 1)))

theorem generic_allows_modal_cycle :
    GenericReception (fun (_ : Bool) (_ : Fin 3) => True) switchingOrder ∧
    UniformRoot (fun (_ : Bool) (_ : Fin 3) => True) switchingOrder 0 ∧
    switchingOrder false 1 2 ∧ switchingOrder true 2 1 := by
  simp only [GenericReception, ActualReceptionPreservation, UniformRoot, Necessary, Root,
    Received, changingDep, variableOrigin, switchingOrder]
  decide

/-- Generic reception does not itself make an actually unreceived bearer
necessary: the individual may be absent at an alternative. -/
theorem reception_alone_does_not_give_necessary :
    GenericReception (fun w (_ : Unit) => w = false)
      (fun (_ : Bool) (_ _ : Unit) => False) ∧
    Root (fun w (_ : Unit) => w = false)
      (fun (_ : Bool) (_ _ : Unit) => False) false () ∧
    ¬ Necessary (fun w (_ : Unit) => w = false) () := by
  simp only [GenericReception, ActualReceptionPreservation, UniformRoot, Necessary, Root,
    Received, changingDep, variableOrigin, switchingOrder]
  decide

end Controls

#print axioms necessary_of_actual_root
#print axioms uniform_of_necessary_actual_root
#print axioms uniform_of_contingent_reception
#print axioms local_transfer_iff_uniform
#print axioms generic_of_fixed_origin
#print axioms Controls.actual_preservation_does_not_give_uniform
#print axioms Controls.generic_not_fixed_origin
#print axioms Controls.generic_allows_modal_cycle
#print axioms Controls.reception_alone_does_not_give_necessary

end Orthemology.Tranche3.SourceIdentity
