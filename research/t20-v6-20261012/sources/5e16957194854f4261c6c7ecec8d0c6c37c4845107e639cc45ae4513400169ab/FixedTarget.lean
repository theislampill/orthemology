import Std

/-!
Fixed numerical-target, fixed-command controls for the resumed T20 cooperation study.
These are conditional mathematical results. No metaphysical premise is certified.
No declaration imports the historical source-mode conclusion as an antecedent.
-/
namespace FixedTarget

-- e is a fixed rigid token. Values below describe its source-neutral state.
inductive Agent where | a | b deriving DecidableEq, Repr
inductive EffectToken where | e deriving DecidableEq, Repr
inductive Coordinate where | left | right deriving DecidableEq, Repr
inductive Emission where | x0 | x1 | x2 | x3 deriving DecidableEq, Repr

-- Interventions vary peer output while retaining the first actual command.
def FixedSoloA {A B O : Type} (f : A → B → O) (a : A) (idleB : B) (q : O) : Prop :=
  f a idleB = q

def IndispensableB {A B O : Type} (f : A → B → O) (a : A) (b idleB : B) (q : O) : Prop :=
  f a b = q ∧ f a idleB ≠ q

theorem fixed_solo_excludes_indispensable_peer {A B O : Type}
    (f : A → B → O) (a : A) (b idleB : B) (q : O)
    (solo : FixedSoloA f a idleB q) : ¬ IndispensableB f a b idleB q := by
  intro h
  exact h.2 solo

-- This is a compositional/indispensability theorem, not the complete metaphysics of agency.
theorem joint_and_solo_exact_additive (a b q : Nat)
    (joint : a + b = q) (solo : a = q) : b = 0 := by omega

theorem two_fixed_solos_exact_additive (a b q : Nat)
    (joint : a + b = q) (soloA : a = q) (soloB : b = q) : q = 0 := by omega

-- Both agents can construct every vector in the declared finite range.
structure Vec where
  left : Nat
  right : Nat
  deriving DecidableEq, Repr

def add (a b : Vec) : Vec := ⟨a.left + b.left, a.right + b.right⟩
def zero : Vec := ⟨0,0⟩
def target : Vec := ⟨2,2⟩
def partialCommand : Vec := ⟨1,1⟩
def inCapacity (v : Vec) : Prop := v.left ≤ 2 ∧ v.right ≤ 2

def capacity (_g : Agent) (v : Vec) : Prop := inCapacity v

structure Will where
  token : EffectToken
  targetState : Vec
  command : Vec
  deriving DecidableEq, Repr

def actualWill (_ : Agent) : Will := ⟨.e, target, partialCommand⟩

-- Standing ability is witnessed by the command itself; no standingPower=True label.
theorem every_eligible_target_has_command (g : Agent) (q : Vec) (h : inCapacity q) :
    ∃ command, capacity g command ∧ add command zero = q := by
  refine ⟨q, h, ?_⟩
  cases q
  rfl

-- Parametric constructive extension beyond the finite search bound: all Nat² states.
-- This is unrestricted within the additive-vector family, not all metaphysical effects.
theorem every_nat_vector_constructive (q : Vec) : ∃ command : Vec, add command zero = q := by
  refine ⟨q, ?_⟩
  cases q
  rfl

-- A joint command can be concentrated, not merely set-unioned. The witness is
-- available to either same rigid bearer under this unbounded command interpreter.
def unboundedIssue (_g : Agent) (command : Vec) : Vec := command

theorem concentrate_additive_power_for_same_bearer (g : Agent) (a b : Vec) :
    ∃ command : Vec, add (unboundedIssue g command) zero = add a b := by
  refine ⟨add a b, ?_⟩
  cases a
  cases b
  rfl

theorem equal_capacities (v : Vec) : capacity .a v ↔ capacity .b v := Iff.rfl

theorem actual_additive_joint : add (actualWill .a).command (actualWill .b).command = target := by decide

theorem actual_additive_fixed_solo_failure :
    add (actualWill .a).command zero ≠ target ∧
    add zero (actualWill .b).command ≠ target := by decide

theorem actual_additive_positive_commands :
    (actualWill .a).command.left > 0 ∧ (actualWill .b).command.left > 0 := by decide

-- B5's union is an abstract capacity profile, not a new third actual bearer.
def profileUnion (v : Vec) : Prop := capacity .a v ∨ capacity .b v

theorem each_already_has_profile_union (g : Agent) (v : Vec) :
    profileUnion v → capacity g v := by
  intro h
  rcases h with h | h <;> exact h

theorem no_missing_union_capacity (g : Agent) :
    ¬ ∃ v, profileUnion v ∧ ¬ capacity g v := by
  rintro ⟨v, hv, hn⟩
  exact hn (each_already_has_profile_union g v hv)

-- Independent control has its quantifier order exposed: exists own command, for all rivals.
def ControlsA {A B O : Type} (f : A → B → O) (q : O) : Prop :=
  ∃ a, ∀ b, f a b = q

def ControlsB {A B O : Type} (f : A → B → O) (q : O) : Prop :=
  ∃ b, ∀ a, f a b = q

theorem rectangular_control_incompatible_targets {A B O : Type}
    (f : A → B → O) (q r : O) (neq : q ≠ r)
    (ha : ControlsA f q) (hb : ControlsB f r) : False := by
  obtain ⟨a, ha⟩ := ha
  obtain ⟨b, hb⟩ := hb
  exact neq ((ha b).symm.trans (hb a))

-- Allow explicit nonrectangular admissibility; the contradiction needs the mixed profile.
def AdmissibleControlsA {A B O : Type} (f : A → B → O) (adm : A → B → Prop) (q : O) : Prop :=
  ∃ a, (∃ b, adm a b) ∧ ∀ b, adm a b → f a b = q

def sat (a b : Bool) : Bool := a || b

def concord (a b : Bool) : Prop := a = b

theorem concordant_all_targets : ∀ q : Bool, AdmissibleControlsA sat concord q := by
  intro q
  refine ⟨q, ⟨q, rfl⟩, ?_⟩
  intro b hab
  subst b
  cases q <;> rfl

theorem saturation_cannot_force_false : ¬ ControlsA sat false := by
  rintro ⟨a, ha⟩
  have h := ha true
  cases a <;> cases h

theorem saturation_fixed_actual_determination :
    sat true true = true ∧ sat true false = true ∧ sat false true = true := by decide

theorem saturation_no_actual_indispensability :
    ¬ IndispensableB sat true true false true := by
  exact fixed_solo_excludes_indispensable_peer sat true true false true rfl

-- CND accepts arbitrary binary ownership relations. A duplicate relation is representable.
def Own : Agent → Emission → Prop
  | .a, .x0 | .a, .x1 | .b, .x2 | .b, .x3 => True
  | _, _ => False

instance (g : Agent) (c : Emission) : Decidable (Own g c) := by cases g <;> cases c <;> unfold Own <;> infer_instance

def CND (own : Agent → Emission → Prop) : Prop :=
  ∀ ag bg c, own ag c → own bg c → ag = bg

def Entire (own : Agent → Emission → Prop) (g : Agent) : Prop :=
  ∀ c, own g c

def DuplicateOwn (g : Agent) (c : Emission) : Prop := Own g c ∨ c = .x0

instance (g : Agent) (c : Emission) : Decidable (DuplicateOwn g c) := by unfold DuplicateOwn; infer_instance

theorem emitted_token_cnd : CND Own := by
  intro ag bg c ha hb
  cases ag <;> cases bg <;> cases c <;> simp_all [Own]

theorem neither_owns_entire_emission_process : ¬ Entire Own .a ∧ ¬ Entire Own .b := by
  constructor
  · intro h; exact h .x2
  · intro h; exact h .x0

theorem duplicate_ownership_rejected : ¬ CND DuplicateOwn := by
  intro h
  have bad : Agent.a = Agent.b := h .a .b .x0 (Or.inr rfl) (Or.inr rfl)
  cases bad

-- Same numerical target and full outcome-directed commands; provenance is separate.
-- This theorem is only an emission-process signature counterinterpretation.
theorem outcome_guarantee_does_not_imply_entire_emission_provenance :
    (sat true true = true ∧ sat true false = true ∧ sat false true = true) ∧
    CND Own ∧ (¬ Entire Own .a ∧ ¬ Entire Own .b) := by
  exact ⟨saturation_fixed_actual_determination, emitted_token_cnd, neither_owns_entire_emission_process⟩

-- Changing to the common whole-target respect exposes the attribution ambiguity.
def WholeSufficient (_g : Agent) (_e : EffectToken) : Prop := sat true false = true

def CNDAt {Token : Type} (own : Agent → Token → Prop) : Prop :=
  ∀ ag bg token, own ag token → own bg token → ag = bg

theorem sufficient_as_entire_breaks_whole_target_cnd : ¬ CNDAt WholeSufficient := by
  intro h
  have bad : Agent.a = Agent.b := h .a .b .e rfl rfl
  cases bad

-- If entire production is independently supplied as an extra bridge, CND has its real force.
theorem entire_same_respect_excludes_two (own : Agent → Emission → Prop)
    (cnd : CND own) (ag bg : Agent) (ha : Entire own ag) (hb : Entire own bg) : ag = bg :=
  cnd ag bg .x0 (ha .x0) (hb .x0)

#print axioms fixed_solo_excludes_indispensable_peer
#print axioms joint_and_solo_exact_additive
#print axioms two_fixed_solos_exact_additive
#print axioms every_eligible_target_has_command
#print axioms no_missing_union_capacity
#print axioms concentrate_additive_power_for_same_bearer
#print axioms rectangular_control_incompatible_targets
#print axioms concordant_all_targets
#print axioms outcome_guarantee_does_not_imply_entire_emission_provenance
#print axioms sufficient_as_entire_breaks_whole_target_cnd
#print axioms duplicate_ownership_rejected
#print axioms entire_same_respect_excludes_two
end FixedTarget
