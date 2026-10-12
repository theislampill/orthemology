import Std

/-!
Conditional mathematics for the provision/identity frontier. Theorems validate
no historical or metaphysical premise. In particular no source-owned act is
identified with a created effect, and no conservation axiom is postulated.
-/
namespace ProvisionIdentity

inductive Root where | a | b deriving DecidableEq, Repr
inductive Policy where | coalesce | redundant | priorityA | priorityB
  deriving DecidableEq, Repr

-- Intrinsic event inputs. The sole created event is represented by occurrence.
-- Shared occurrence variables do NOT prove transworld numerical identity.
def created (_ : Policy) (a b : Bool) : Bool := a || b

-- Positive derivation support, calculated from the operational rules.
def rootsA (p : Policy) (a b : Bool) : Bool :=
  match p with
  | .coalesce => a
  | .redundant => a
  | .priorityA => a
  | .priorityB => a && !b

def rootsB (p : Policy) (a b : Bool) : Bool :=
  match p with
  | .coalesce => b
  | .redundant => b
  | .priorityA => b && !a
  | .priorityB => b

def entireA (p : Policy) (a b : Bool) : Bool := rootsA p a b && !rootsB p a b
def entireB (p : Policy) (a b : Bool) : Bool := rootsB p a b && !rootsA p a b

theorem same_created_table (p q : Policy) : created p = created q := rfl

theorem actual_provision_differs :
    entireA .priorityA true true = true ∧ entireA .coalesce true true = false := by decide

theorem whole_effect_cnd (p : Policy) (a b : Bool) :
    ¬ (entireA p a b = true ∧ entireB p a b = true) := by
  cases p <;> cases a <;> cases b <;> decide

theorem nonempty_whole_effect_provision : entireA .coalesce true false = true := by decide

theorem coalescence_fixed_act_solo :
    created .coalesce true true = true ∧ created .coalesce true false = true := by decide

-- The direct-event construction generalizes beyond a single Boolean target:
-- any event-indexed target predicate can be issued by either same bearer.
-- This does NOT say all metaphysical products are event-indexed sets.
def eventProduction {E : Type} (a b : E → Prop) : E → Prop := fun e => a e ∨ b e

theorem every_event_target_solo {E : Type} (q : E → Prop) :
    ∀ e, eventProduction q (fun _ => False) e ↔ q e := by
  intro e
  simp [eventProduction]

theorem every_event_target_double {E : Type} (q : E → Prop) :
    ∀ e, eventProduction q q e ↔ q e := by
  intro e
  simp [eventProduction]


-- No decoder from the COMPLETE chosen extensional table can recover actual
-- entire-A provision for both operational factorizations.
theorem no_extensional_provision_decoder :
    ¬ ∃ decode : (Bool → Bool → Bool) → Bool,
      decode (created .coalesce) = entireA .coalesce true true ∧
      decode (created .priorityA) = entireA .priorityA true true := by
  intro ⟨decode, hc, hp⟩
  have h : entireA .coalesce true true = entireA .priorityA true true := hc.symm.trans hp
  cases h

-- Individually different act tokens need not have different outputs. Any
-- inference from act inequality to output inequality needs a map condition.
theorem distinct_acts_can_have_same_created_effect :
    ∃ f : Root → Unit, Root.a ≠ Root.b ∧ f .a = f .b := by
  exact ⟨fun _ => (), by decide, rfl⟩

theorem act_distinction_transports_under_injectivity
    {Act Effect : Type} (f : Act → Effect)
    (inj : ∀ ⦃x y⦄, f x = f y → x = y) (a b : Act) (hne : a ≠ b) : f a ≠ f b := by
  intro eq
  exact hne (inj eq)

-- Positive created-output accounting, when independently justified, proves
-- nonabsorption without assuming that provenance fixes numerical identity.
theorem positive_accounting_excludes_unchanged_joint
    {Effect : Type} (measure : Effect → Nat) (solo joint : Effect)
    (amountA amountB : Nat)
    (solo_account : measure solo = amountA)
    (joint_account : measure joint = amountA + amountB)
    (genuine_extra : 0 < amountB) : joint ≠ solo := by
  intro eq
  rw [eq] at joint_account
  omega

-- Cancellation is a sufficient but stronger algebraic condition. No global
-- algebra or positivity assumption is hidden in a structure declaration.
theorem cancellation_excludes_absorption
    {M : Type} (op : M → M → M) (zero : M)
    (identity : ∀ a, op a zero = a)
    (cancel : ∀ a b c, op a b = op a c → b = c)
    (a b : M) (eq : op a b = a) : b = zero := by
  exact cancel a b zero (eq.trans (identity a).symm)

-- Completeness of a physical-accounting refinement and identity of its
-- qualitative projection are different properties.
def physical (a b : Nat) : Nat × Nat := (min 1 (a+b), (a+b)-min 1 (a+b))
theorem display_equal_with_extra_created_waste :
    (physical 1 1).1 = (physical 1 0).1 ∧ physical 1 1 ≠ physical 1 0 := by decide

-- Requiring EVERY jointly grounded event to have an earlier jointly grounded
-- mechanism is incompatible with well-founded temporal/derivational depth.
-- This is stronger than mere contingent-event efficient explanation.
theorem no_well_founded_joint_mechanism_regress
    (Joint : Nat → Prop)
    (earlier : ∀ n, Joint n → ∃ m, m < n ∧ Joint m) : ∀ n, ¬ Joint n := by
  intro n
  induction n using Nat.strongRecOn with
  | ind n ih =>
    intro hn
    obtain ⟨m, hmn, hm⟩ := earlier n hn
    exact ih m hmn hm

-- Primitive entire-provision relation is deliberately NONFUNCTIONAL.
-- CND rejects duplicate whole production; it is not encoded by a function.
def PrimitiveCND (Entire : Root → Prop) : Prop :=
  ∀ g h, Entire g → Entire h → g = h

theorem double_primitive_entire_violates_cnd :
    ¬ PrimitiveCND (fun _ => True) := by
  intro h
  have bad : Root.a = Root.b := h .a .b True.intro True.intro
  cases bad

theorem cnd_does_not_entail_entire_coverage :
    PrimitiveCND (fun _ => False) ∧ ¬ ∃ g : Root, (fun _ : Root => False) g := by
  constructor
  · intro g h hg
    exact False.elim hg
  · intro ⟨g, hg⟩
    exact hg

-- Positive reduced-signature counterexample, rather than only a failed
-- full-source model: exact output, same-act solo outcome and CND coexist
-- with no individual entire actual provider at the cooperative target.
theorem reduced_signature_provision_independence :
    created .coalesce true true = true ∧
    created .coalesce true false = true ∧
    created .coalesce false true = true ∧
    (¬ (entireA .coalesce true true = true ∧ entireB .coalesce true true = true)) ∧
    entireA .coalesce true true = false ∧ entireB .coalesce true true = false := by decide


end ProvisionIdentity

#print axioms ProvisionIdentity.same_created_table
#print axioms ProvisionIdentity.actual_provision_differs
#print axioms ProvisionIdentity.whole_effect_cnd
#print axioms ProvisionIdentity.nonempty_whole_effect_provision
#print axioms ProvisionIdentity.coalescence_fixed_act_solo
#print axioms ProvisionIdentity.no_extensional_provision_decoder
#print axioms ProvisionIdentity.distinct_acts_can_have_same_created_effect
#print axioms ProvisionIdentity.act_distinction_transports_under_injectivity
#print axioms ProvisionIdentity.positive_accounting_excludes_unchanged_joint
#print axioms ProvisionIdentity.cancellation_excludes_absorption
#print axioms ProvisionIdentity.display_equal_with_extra_created_waste
#print axioms ProvisionIdentity.no_well_founded_joint_mechanism_regress

#print axioms ProvisionIdentity.every_event_target_solo
#print axioms ProvisionIdentity.every_event_target_double

#print axioms ProvisionIdentity.double_primitive_entire_violates_cnd
#print axioms ProvisionIdentity.cnd_does_not_entail_entire_coverage
#print axioms ProvisionIdentity.reduced_signature_provision_independence
