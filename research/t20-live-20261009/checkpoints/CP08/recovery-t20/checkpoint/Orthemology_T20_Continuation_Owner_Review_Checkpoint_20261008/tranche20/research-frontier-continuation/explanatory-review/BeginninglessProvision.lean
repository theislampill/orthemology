import ActualProvisionReview

/-!
A strengthened source-fidelity control: each token's actual production employs
one original standing resource AND a prior particular effect. The standing
resource is not merely co-present with an unrelated token series. All selected
edges are stipulated productive for this interpretation; there is no dormant
rule or nonproductive-grounding gap here.
-/
namespace BeginninglessProvision
open ActualProvisionReview

abbrev Resource := Option Nat

def original (r : Resource) : Prop := r = none

def needs (n : Nat) (p : Resource) : Prop := p = none ∨ p = some (n+1)

def output (n : Nat) : Resource := some n

def actual (_ : Resource) : Prop := True

def used (_ : Nat) : Prop := True

def productive (a b : Resource) : Prop :=
  ∃ n, used n ∧ needs n a ∧ output n = b

inductive Generated : Resource → Prop where
  | seed {r} : original r → Generated r
  | rule (n : Nat) : (∀ p, needs n p → Generated p) → Generated (output n)

theorem live_sound_nonempty (n : Nat) :
    used n ∧ actual (output n) ∧ (∀ p, needs n p → actual p) ∧
      (∃ p, needs n p) :=
  ⟨trivial, trivial, fun _ _ => trivial, none, Or.inl rfl⟩

theorem local_fixed (r : Resource) :
    actual r ↔ original r ∨ ∃ n, used n ∧ output n = r ∧
      ∀ p, needs n p → actual p := by
  constructor
  · intro _; cases r with
    | none => exact Or.inl rfl
    | some n => exact Or.inr ⟨n, trivial, rfl, fun _ _ => trivial⟩
  · intro _; trivial

theorem seed_no_incoming : ¬ ∃ r, productive r none := by
  intro h; obtain ⟨r, n, _, _, h⟩ := h; cases h

/-- Every token has a strict actually used contribution from THE SAME original. -/
theorem same_original_directly_supplies_every_token (n : Nat) :
    original none ∧ actual none ∧ StrictPath productive none (some n) := by
  exact ⟨rfl, trivial, StrictPath.edge ⟨n, trivial, Or.inl rfl, rfl⟩⟩

/-- This is a real second productive input, not only a chronological relation. -/
theorem prior_token_actually_supplies_next (n : Nat) :
    productive (some (n+1)) (some n) :=
  ⟨n, trivial, Or.inr rfl, rfl⟩

theorem all_generated_are_seed {r} (h : Generated r) : r = none := by
  induction h with
  | seed h => exact h
  | rule n _ ih =>
    have bad := ih (some (n+1)) (Or.inr rfl)
    cases bad

theorem all_actual_tokens_ungenerated (n : Nat) :
    actual (some n) ∧ ¬ Generated (some n) := by
  refine ⟨trivial, ?_⟩
  intro h; have bad := all_generated_are_seed h; cases bad

def Earlier (a b : Resource) : Prop := match a, b with
  | none, some _ => True
  | some m, some n => n < m
  | _, _ => False

theorem earlier_irreflexive (a : Resource) : ¬ Earlier a a := by
  cases a with
  | none => exact fun h => h
  | some n => exact Nat.lt_irrefl n

theorem earlier_transitive {a b c : Resource}
    (hab : Earlier a b) (hbc : Earlier b c) : Earlier a c := by
  cases a <;> cases b <;> cases c <;> simp_all [Earlier]
  exact Nat.lt_trans hbc hab

theorem productive_is_earlier {a b} (h : productive a b) : Earlier a b := by
  obtain ⟨n, _, ha, hb⟩ := h
  change some n = b at hb
  subst b
  rcases ha with ha | ha <;> subst a
  · trivial
  · exact Nat.lt_succ_self n

theorem productive_path_is_earlier {a b}
    (h : StrictPath productive a b) : Earlier a b := by
  induction h with
  | edge e => exact productive_is_earlier e
  | tail _ e ih => exact earlier_transitive ih (productive_is_earlier e)

theorem productive_acyclic (r : Resource) : ¬ StrictPath productive r r := by
  intro h; exact earlier_irreflexive r (productive_path_is_earlier h)

/-- A bearer/resources interface with the same original bearer at every token.
Identity is fixed by index; no sequence or law is reified as an extra bearer. -/
def bridge : Bridge Resource Resource where
  actualResource := actual
  receivedResource := fun r => r ≠ none
  intrinsic := fun b r => b = r
  actualBearer := actual
  receivedBearer := fun b => b ≠ none
  support := productive
  productive := productive

theorem bridge_realisation : Realisation bridge := by
  intro r _; exact ⟨r, trivial, rfl⟩

theorem bridge_received_transport : ReceivedTransport bridge := by
  intro b r _ hbr hrecv
  change b = r at hbr
  subst b; exact hrecv

theorem same_bearer_productive_without_token_generation (n : Nat) :
    OriginalResource bridge none ∧ OriginalBearer bridge none ∧
    bridge.intrinsic none none ∧ Contributor bridge none (some n) ∧
    ¬ Generated (some n) := by
  refine ⟨⟨trivial, fun h => h rfl⟩, ⟨trivial, fun h => h rfl⟩, rfl,
    ⟨none, rfl, (same_original_directly_supplies_every_token n).2.2⟩,
    (all_actual_tokens_ungenerated n).2⟩

/-- Broad full generated-target selection would reject every actual token
of this originally supplied history, despite actual productive coverage. -/
theorem original_productive_coverage_does_not_imply_full_generation :
    (∀ n, Contributor bridge none (some n)) ∧
    (∀ n, ∃ m, productive (some m) (some n)) ∧
    ¬ (∀ r, actual r → Generated r) := by
  refine ⟨fun n => (same_bearer_productive_without_token_generation n).2.2.2.1,
    fun n => ⟨n+1, prior_token_actually_supplies_next n⟩, ?_⟩
  intro h; exact (all_actual_tokens_ungenerated 0).2 (h (some 0) trivial)

end BeginninglessProvision
