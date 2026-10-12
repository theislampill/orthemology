import ActualProvisionReview

/-!
A depth-assumption control, not a possible plural-perfect-original universe.
Every created token has two original productive inputs and a prior jointly
supported token. The live graph is acyclic but has no first jointly supported
token and admits no finite descending derivational-depth assignment.
-/
namespace BeginninglessJointProvision
open ActualProvisionReview

abbrev Resource := Sum Bool Nat

def original : Resource → Prop
  | .inl _ => True
  | .inr _ => False

def needs (n : Nat) : Resource → Prop
  | .inl _ => True
  | .inr m => m = n+1

def productive (a b : Resource) : Prop :=
  ∃ n, needs n a ∧ b = .inr n

def actual (_ : Resource) : Prop := True

def used (_ : Nat) : Prop := True

def JointlySupported (r : Resource) : Prop :=
  StrictPath productive (.inl false) r ∧ StrictPath productive (.inl true) r

inductive Generated : Resource → Prop where
  | seed {r} : original r → Generated r
  | rule (n : Nat) : (∀ p, needs n p → Generated p) → Generated (.inr n)

theorem live_sound_nonempty (n : Nat) :
    used n ∧ actual (.inr n) ∧ (∀ p, needs n p → actual p) ∧
      (∃ p, needs n p) :=
  ⟨trivial, trivial, fun _ _ => trivial, .inl false, trivial⟩

theorem local_fixed (r : Resource) :
    actual r ↔ original r ∨ ∃ n, used n ∧ r = .inr n ∧
      ∀ p, needs n p → actual p := by
  constructor
  · intro _; cases r with
    | inl _ => exact Or.inl trivial
    | inr n => exact Or.inr ⟨n, trivial, rfl, fun _ _ => trivial⟩
  · intro _; trivial

theorem original_no_incoming (b : Bool) : ¬ ∃ r, productive r (.inl b) := by
  intro h; obtain ⟨r, n, _, h⟩ := h; cases h

theorem each_token_jointly_supported (n : Nat) : JointlySupported (.inr n) := by
  exact ⟨StrictPath.edge ⟨n, trivial, rfl⟩, StrictPath.edge ⟨n, trivial, rfl⟩⟩

theorem predecessor_productively_used (n : Nat) :
    productive (.inr (n+1)) (.inr n) := ⟨n, rfl, rfl⟩

theorem only_originals_generated {r} (h : Generated r) : original r := by
  induction h with
  | seed h => exact h
  | rule n _ ih => exact False.elim (ih (.inr (n+1)) rfl)

theorem tokens_not_generated (n : Nat) : ¬ Generated (.inr n) := by
  intro h; exact only_originals_generated h

def Earlier (a b : Resource) : Prop := match a, b with
  | .inl _, .inr _ => True
  | .inr m, .inr n => n < m
  | _, _ => False

theorem earlier_irreflexive (a : Resource) : ¬ Earlier a a := by
  cases a with
  | inl _ => exact fun h => h
  | inr n => exact Nat.lt_irrefl n

theorem earlier_transitive {a b c : Resource}
    (hab : Earlier a b) (hbc : Earlier b c) : Earlier a c := by
  cases a <;> cases b <;> cases c <;> simp_all [Earlier]
  exact Nat.lt_trans hbc hab

theorem productive_is_earlier {a b} (h : productive a b) : Earlier a b := by
  obtain ⟨n, ha, hb⟩ := h
  subst b
  cases a with
  | inl _ => trivial
  | inr m =>
    change m = n+1 at ha
    subst m; exact Nat.lt_succ_self n

theorem productive_path_is_earlier {a b}
    (h : StrictPath productive a b) : Earlier a b := by
  induction h with
  | edge e => exact productive_is_earlier e
  | tail _ e ih => exact earlier_transitive ih (productive_is_earlier e)

theorem productive_acyclic (r : Resource) : ¬ StrictPath productive r r := by
  intro h; exact earlier_irreflexive r (productive_path_is_earlier h)

theorem every_joint_token_has_prior_joint_token (n : Nat) :
    JointlySupported (.inr n) ∧
    ∃ m, JointlySupported (.inr m) ∧ productive (.inr m) (.inr n) :=
  ⟨each_token_jointly_supported n, n+1,
    each_token_jointly_supported (n+1), predecessor_productively_used n⟩

/-- Every actual jointly supported resource, not just a chosen target,
has a prior jointly supported resource. No original is spuriously counted. -/
theorem no_first_joint_resource {r} (joint : JointlySupported r) :
    ∃ p, JointlySupported p ∧ productive p r := by
  cases r with
  | inl b =>
    have bad := productive_path_is_earlier joint.1
    exact False.elim bad
  | inr n =>
    exact ⟨.inr (n+1), each_token_jointly_supported (n+1), predecessor_productively_used n⟩

theorem no_finite_derivational_depth (depth : Nat → Nat)
    (decreases : ∀ n, depth (n+1) < depth n) : False := by
  have lower : ∀ k n, k ≤ depth n := by
    intro k
    induction k with
    | zero => exact fun n => Nat.zero_le (depth n)
    | succ k ih =>
      intro n
      exact Nat.succ_le_of_lt (Nat.lt_of_le_of_lt (ih (n+1)) (decreases n))
  exact Nat.not_succ_le_self (depth 0) (lower (depth 0 + 1) 0)

/-- This meets a bare demand for an earlier joint mechanism at every token.
Its failure to admit finite depth identifies, rather than removes, the premise
used by the finite-depth first-joint-node theorem. -/
theorem acyclic_joint_history_without_first :
    (∀ r, ¬ StrictPath productive r r) ∧
    JointlySupported (.inr 0) ∧
    (∀ r, JointlySupported r → ∃ p, JointlySupported p ∧ productive p r) :=
  ⟨productive_acyclic, each_token_jointly_supported 0, fun _ h => no_first_joint_resource h⟩

end BeginninglessJointProvision
