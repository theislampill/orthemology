/- Typed modal independence controls. No assertion of metaphysical possibility.
   Modal domain and origin-essentiality are explicit model hypotheses. -/
namespace OriginBridge

-- A general consequence of origin-essentiality, independent of finite fixtures.
theorem changed_origin_excludes_same_effect
    {W E O : Type} (occurs : W → E → Prop) (origin : W → E → O)
    (essential : ∀ w v e, occurs w e → occurs v e → origin w e = origin v e)
    {w v : W} {e : E} (actual : occurs w e)
    (changed : origin w e ≠ origin v e) : ¬ occurs v e := by
  intro other
  exact changed (essential w v e actual other)

-- The eligibility conflict is explicit, rather than an inference to incapacity.
theorem peer_essential_target_not_solo_eligible
    {W : Type} (target peerActs solo : W → Prop)
    (originCondition : ∀ w, target w → peerActs w)
    (soloCondition : ∀ w, solo w → ¬ peerActs w) :
    ¬ ∃ w, target w ∧ solo w := by
  rintro ⟨w, ht, hs⟩
  exact soloCondition w hs (originCondition w ht)

inductive Root | a | b deriving DecidableEq, Repr
inductive World | joint | laterSolo | birthSolo deriving DecidableEq, Repr
inductive Effect | q | qSolo deriving DecidableEq, Repr
inductive OriginEvent | ab | a deriving DecidableEq, Repr
inductive Phase | birth | later deriving DecidableEq, Repr

-- Both proposed original bearers exist in every world. No bearer deletion.
def rootExists (_ : World) (_ : Root) : Prop := True
-- Untargeted background activity can remain; this is not global inactivity.
def backgroundAct (_ : World) (_ : Root) : Prop := True
-- Intrinsic resources are primitives with no efficient receipt edge.
def receives (_ : World) (_ _ : Root) : Prop := False

def effectAt : World → Effect
  | .birthSolo => .qSolo
  | _ => .q

def occurs (w : World) (e : Effect) : Prop := effectAt w = e
-- Exact historical event, not merely equality of a source label.
def origin : World → Effect → OriginEvent
  | _, .q => .ab
  | _, .qSolo => .a

def support : World → Phase → Root → Prop
  | .joint, _, _ => True
  | .laterSolo, .birth, _ => True
  | .laterSolo, .later, r => r = .a
  | .birthSolo, _, r => r = .a

-- Origin and current sustaining support are different types/arguments.
def entireNow (w : World) (p : Phase) (r : Root) : Prop :=
  support w p r ∧ ∀ s, support w p s → s = r

def sameQualitativeRole (_ : Effect) : Prop := True
-- A's command and own end use a profile, not a hidden rigid reference to q.
def commandA (_ : World) : Nat := 1
def ownEndA (w : World) : Prop :=
  sameQualitativeRole (effectAt w) ∧ support w .later .a

theorem roots_remain : ∀ w r, rootExists w r := by intro w r; trivial

theorem exact_origin_essential :
    ∀ w v e, occurs w e → occurs v e → origin w e = origin v e := by
  intro w v e _ _; cases e <;> rfl

theorem no_receipt : ∀ w r s, ¬ receives w r s := by
  intro w r s h; exact h

theorem cnd_same_respect :
    ∀ w p r s, entireNow w p r → entireNow w p s → r = s := by
  intro w p r s hr hs
  exact hs.2 r hr.1

theorem changed_birth_loses_q : occurs .joint .q ∧ ¬ occurs .birthSolo .q := by
  constructor
  · rfl
  · intro h; cases h

theorem birth_suppression_preserves_qualitative_own_end :
    commandA .joint = commandA .birthSolo ∧
    ownEndA .joint ∧ ownEndA .birthSolo ∧
    (∀ r s, ¬ receives .birthSolo r s) := by
  refine ⟨rfl, ⟨?_, ?_⟩, ⟨?_, ?_⟩, ?_⟩
  · trivial
  · trivial
  · trivial
  · rfl
  · exact no_receipt .birthSolo

theorem fixed_past_later_support_countermodel :
    occurs .joint .q ∧ occurs .laterSolo .q ∧
    origin .joint .q = origin .laterSolo .q ∧
    (∀ r, support .joint .birth r ↔ support .laterSolo .birth r) ∧
    support .joint .later .b ∧ ¬ support .laterSolo .later .b ∧
    commandA .joint = commandA .laterSolo ∧
    ownEndA .joint ∧ ownEndA .laterSolo := by
  refine ⟨rfl, rfl, rfl, ?_, ?_, ?_, rfl, ⟨?_, ?_⟩, ⟨?_, ?_⟩⟩
  · intro r; exact Iff.rfl
  · trivial
  · intro h; cases h
  · trivial
  · trivial
  · trivial
  · rfl

theorem essential_origin_does_not_imply_sustaining_history_essential :
    (∀ w v e, occurs w e → occurs v e → origin w e = origin v e) ∧
    ¬ (∀ w v e, occurs w e → occurs v e →
        ∀ r, support w .later r ↔ support v .later r) := by
  refine ⟨exact_origin_essential, ?_⟩
  intro hist
  have bad : support .laterSolo .later .b :=
    (hist .joint .laterSolo .q rfl rfl .b).mp True.intro
  cases bad

-- Optional necessary concord excludes a diagnostic world without changing identity.
def concordAdmissible : World → Prop
  | .joint => True
  | _ => False

theorem identity_and_policy_obstructions_are_distinct :
    occurs .laterSolo .q ∧ ¬ concordAdmissible .laterSolo := by
  exact ⟨rfl, fun h => h⟩

#print axioms changed_origin_excludes_same_effect
#print axioms peer_essential_target_not_solo_eligible
#print axioms roots_remain
#print axioms exact_origin_essential
#print axioms no_receipt
#print axioms cnd_same_respect
#print axioms changed_birth_loses_q
#print axioms birth_suppression_preserves_qualitative_own_end
#print axioms fixed_past_later_support_countermodel
#print axioms essential_origin_does_not_imply_sustaining_history_essential
#print axioms identity_and_policy_obstructions_are_distinct
end OriginBridge
