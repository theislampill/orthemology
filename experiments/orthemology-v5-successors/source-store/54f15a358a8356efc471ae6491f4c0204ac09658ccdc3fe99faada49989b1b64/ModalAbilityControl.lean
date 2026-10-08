import Controls
set_option synthInstance.maxSize 100000
set_option maxRecDepth 10000
set_option maxHeartbeats 2000000
namespace AnchoredSourceBridge.Controls.ModalAbility

/-- A finite declared outcome class. It is not metaphysical possibility itself. -/
inductive W | actual | alternativeA | alternativeB deriving DecidableEq, Repr
inductive Target | red | blue deriving DecidableEq, Repr
inductive Piece | first | second deriving DecidableEq, Repr

instance worldForall (p : W → Prop) [DecidablePred p] : Decidable (∀ w, p w) :=
  decidable_of_iff (p .actual ∧ p .alternativeA ∧ p .alternativeB) ⟨
    fun h w => by cases w; exact h.1; exact h.2.1; exact h.2.2,
    fun h => ⟨h _, h _, h _⟩⟩
instance worldExists (p : W → Prop) [DecidablePred p] : Decidable (∃ w, p w) :=
  decidable_of_iff (p .actual ∨ p .alternativeA ∨ p .alternativeB) ⟨
    fun h => by cases h with | inl h => exact ⟨.actual, h⟩ | inr h => cases h with | inl h => exact ⟨.alternativeA, h⟩ | inr h => exact ⟨.alternativeB, h⟩,
    fun ⟨w, h⟩ => by cases w; exact Or.inl h; exact Or.inr (Or.inl h); exact Or.inr (Or.inr h)⟩
instance targetForall (p : Target → Prop) [DecidablePred p] : Decidable (∀ t, p t) :=
  decidable_of_iff (p .red ∧ p .blue) ⟨fun h t => by cases t; exact h.1; exact h.2, fun h => ⟨h _, h _⟩⟩
instance pieceForall (p : Piece → Prop) [DecidablePred p] : Decidable (∀ r, p r) :=
  decidable_of_iff (p .first ∧ p .second) ⟨fun h r => by cases r; exact h.1; exact h.2, fun h => ⟨h _, h _⟩⟩

/-- Concrete contribution identity includes history, outcome occurrence and
productive piece. It has no provider index or built-in owner. -/
structure ContributionToken where
  history : W
  target : Target
  piece : Piece
  deriving DecidableEq, Repr

/-- Actual provision table, separately interpreted in each supplied history. -/
def supplies (w : W) (s : S) (_t : Target) (p : Piece) : Prop :=
  (w = .actual ∧ ((s = .g ∧ p = .first) ∨ (s = .h ∧ p = .second))) ∨
  (w = .alternativeA ∧ s = .g) ∨ (w = .alternativeB ∧ s = .h)
def EntireToken (s : S) (c : ContributionToken) : Prop := supplies c.history s c.target c.piece

def ActualSolo (w : W) (s : S) (t : Target) : Prop := ∀ p, supplies w s t p
/-- Ability is given genuine witnesses of actual solo production in supplied
alternatives, rather than asserted as an uninterpreted universal label. -/
def Ability (s : S) (t : Target) : Prop := ∃ w, w ≠ .actual ∧ ActualSolo w s t

def WorldCND : Prop := ∀ w s r t p, supplies w s t p → supplies w r t p → s = r

macro "ability_check" : tactic => `(tactic| (simp only [Ability, ActualSolo, WorldCND, supplies, EntireToken]; decide))

theorem both_have_interpreted_finite_ability :
    (∀ t, Ability .g t) ∧ (∀ t, Ability .h t) ∧
    (∀ t, ActualSolo .alternativeA .g t) ∧ (∀ t, ActualSolo .alternativeB .h t) := by ability_check

theorem matching_outcome_is_not_same_token :
    (ContributionToken.mk .actual .red .first ≠ ContributionToken.mk .alternativeA .red .first) ∧
    (ContributionToken.mk .alternativeA .red .first ≠ ContributionToken.mk .alternativeB .red .first) := by decide

theorem intact_finite_power_differentiated_actual_production :
    WorldCND ∧ (∀ t, Ability .g t) ∧ (∀ t, Ability .h t) ∧
    (∀ t, supplies .actual .g t .first ∧ supplies .actual .h t .second) ∧
    (∀ s t, ¬ ActualSolo .actual s t) := by ability_check

/-- Exact semantic map of the actual red occurrence into control 1/13's account. -/
theorem actual_partial_fixture_mapping :
    (∀ s, supplies .actual s .red .first ↔ split.EntireOrig s .a) ∧
    (∀ s, supplies .actual s .red .second ↔ split.EntireOrig s .b) ∧
    split.Req .e .a ∧ split.Req .e .b := by
  simp only [supplies, split, faithful, fixture, splitEntire, splitReq]
  decide

/-- This is finite relative consistency, not unrestricted omnipotence or evidence
that these histories are metaphysically possible. SourceMode still fails. -/
theorem finite_ability_does_not_supply_source_mode :
    (∀ t, Ability .g t) ∧ (∀ t, Ability .h t) ∧ CND split ∧
    ¬ ModeSatisfaction split .g ∧ ¬ GlobalCoverage split .g := by
  refine ⟨both_have_interpreted_finite_ability.1,
    both_have_interpreted_finite_ability.2.1, ?_⟩
  finite_check
end AnchoredSourceBridge.Controls.ModalAbility
