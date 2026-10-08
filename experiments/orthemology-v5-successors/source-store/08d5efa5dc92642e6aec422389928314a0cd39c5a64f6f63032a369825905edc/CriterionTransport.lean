import Std

/-!
Core-only proofs for the criterion-transport investigation.

These are conditional mathematical results. No predicate below certifies its
own real-world adequacy, source authenticity, institutional legitimacy, or
runtime integrity. No metaphysical premise is encoded or concluded.
-/

namespace CriterionTransport

/- Candidate E: explicit witness-relative meaning of full-basis defeat. -/

def TokenSufficient {W : Type} (eligible authority : W → Prop) : Prop :=
  ∃ w, eligible w ∧ authority w

theorem witness_relative_exclusion {W : Type}
    (eligible defeated authority : W → Prop)
    (allDefeated : ∀ w, eligible w → defeated w)
    (adequacy : ∀ w, defeated w → ¬ authority w) :
    ¬ TokenSufficient eligible authority := by
  intro h
  obtain ⟨w, hw, ha⟩ := h
  exact adequacy w (allDefeated w hw) ha

/- false is a proper subset witness; true is the full closure. -/
def bareDef (w : Bool) : Prop := w = true
def bareAuth (w : Bool) : Prop := w = false

theorem bare_authority_adequacy : ∀ w, bareDef w → ¬ bareAuth w := by
  intro w hd ha
  cases w <;> simp [bareDef, bareAuth] at *

theorem bare_whole_defeat_with_subset_authority :
    bareDef true ∧ TokenSufficient (fun _ : Bool => True) bareAuth := by
  exact ⟨rfl, false, True.intro, rfl⟩

theorem upward_sufficiency_alternative {W : Type}
    (eligible authority : W → Prop) (whole : W)
    (upward : ∀ w, eligible w → authority w → authority whole)
    (wholeInsufficient : ¬ authority whole) :
    ¬ TokenSufficient eligible authority := by
  intro h
  obtain ⟨w, hw, ha⟩ := h
  exact wholeInsufficient (upward w hw ha)

/- Equality-sensitive standards and representation changes. -/

def AdequateAt {X : Type} (criterion : X → Prop) (target : X) : Prop :=
  ∀ x, criterion x ↔ x = target

theorem exact_criterion_adequate {X : Type} (target : X) :
    AdequateAt (fun x => x = target) target := by
  intro x
  rfl

theorem adequate_replacement_unique_extension {X : Type}
    (c d : X → Prop) (target : X)
    (hc : AdequateAt c target) (hd : AdequateAt d target) :
    ∀ x, c x ↔ d x := by
  intro x
  exact (hc x).trans (hd x).symm

theorem representation_reflects_exactness_iff_singleton_fiber
    {X Y : Type} (f : X → Y) (target : X) :
    AdequateAt (fun x => f x = f target) target ↔
      (∀ x, f x = f target → x = target) := by
  constructor
  · intro h x hx
    exact (h x).mp hx
  · intro h x
    constructor
    · exact h x
    · intro hx
      exact congrArg f hx

theorem all_targets_exact_iff_injective {X Y : Type} (f : X → Y) :
    (∀ target, AdequateAt (fun x => f x = f target) target) ↔
      (∀ x y, f x = f y → x = y) := by
  constructor
  · intro h x y hxy
    exact (h y x).mp hxy
  · intro h target x
    constructor
    · exact h x target
    · intro hx
      exact congrArg f hx

theorem collapsed_fiber_is_false_acceptance {X Y : Type}
    (f : X → Y) (target wrong : X)
    (sameImage : f wrong = f target) (different : wrong ≠ target) :
    (f wrong = f target) ∧ ¬ (wrong = target) := by
  exact ⟨sameImage, different⟩

/- Recipient evidence classes. Robust validity is not a definition of all
ordinary epistemic warrant; actual-world inclusion is a separate premise. -/

def Robust {W : Type} (evidence claim : W → Prop) : Prop :=
  ∀ w, evidence w → claim w

def BackCover {U V : Type} (eu : U → Prop) (ev : V → Prop)
    (relation : U → V → Prop) : Prop :=
  ∀ v, ev v → ∃ u, eu u ∧ relation u v

def Preserves {U V : Type} (eu : U → Prop) (ev : V → Prop)
    (relation : U → V → Prop) (p : U → Prop) (q : V → Prop) : Prop :=
  ∀ u v, eu u → ev v → relation u v → p u → q v

theorem transport_of_robust_judgment {U V : Type}
    (eu : U → Prop) (ev : V → Prop) (relation : U → V → Prop)
    (p : U → Prop) (q : V → Prop)
    (sourceValid : Robust eu p)
    (covered : BackCover eu ev relation)
    (preserved : Preserves eu ev relation p q) : Robust ev q := by
  intro v hv
  obtain ⟨u, hu, huv⟩ := covered v hv
  exact preserved u v hu hv huv (sourceValid u hu)

theorem actual_truth_requires_evidence_soundness {W : Type}
    (evidence claim : W → Prop) (actual : W)
    (valid : Robust evidence claim) (sound : evidence actual) : claim actual := by
  exact valid actual sound

/- Exactness is uniform over ALL predicates, including the relation image.
For a fixed q, independent recipient evidence can make coverage unnecessary. -/

theorem uniform_transport_iff_back_coverage {U V : Type}
    (eu : U → Prop) (ev : V → Prop) (relation : U → V → Prop) :
    (∀ (p : U → Prop) (q : V → Prop),
      Robust eu p → Preserves eu ev relation p q → Robust ev q) ↔
    BackCover eu ev relation := by
  constructor
  · intro allClaims v hv
    let imageClaim : V → Prop := fun x => ∃ u, eu u ∧ relation u x
    have hp : Robust eu (fun _ => True) := by
      intro u hu
      exact True.intro
    have preserveImage : Preserves eu ev relation (fun _ => True) imageClaim := by
      intro u x hu hx hux hp
      exact ⟨u, hu, hux⟩
    exact allClaims (fun _ => True) imageClaim hp preserveImage v hv
  · intro covered p q hp preserves
    exact transport_of_robust_judgment eu ev relation p q hp covered preserves

def oneSource (_ : Unit) : Prop := True
def bothRecipients (_ : Bool) : Prop := True
def onlyFalseRelated (_ : Unit) (v : Bool) : Prop := v = false

theorem forward_preservation_can_miss_revoked_recipient :
    Robust oneSource (fun _ => True) ∧
    Preserves oneSource bothRecipients onlyFalseRelated (fun _ => True)
      (fun v => v = false) ∧
    ¬ Robust bothRecipients (fun v => v = false) := by
  refine ⟨?_, ?_, ?_⟩
  · intro u hu
    exact True.intro
  · intro u v hu hv hrel hp
    exact hrel
  · intro h
    have bad := h true True.intro
    cases bad

theorem coverage_not_necessary_for_independently_true_fixed_claim :
    Robust bothRecipients (fun _ => True) ∧
    ¬ BackCover oneSource bothRecipients onlyFalseRelated := by
  constructor
  · intro v hv
    exact True.intro
  · intro h
    obtain ⟨u, hu, huv⟩ := h true True.intro
    cases huv

/- One-step uniform action result. A guarded compound operation is a distinct
action/interface and must be included explicitly before applying this test. -/

theorem fixed_observation_action_iff_common_good_action
    {W O A : Type} (observe : W → O) (view : O)
    (admissible : W → Prop) (good : W → A → Prop) :
    (∃ policy : O → A, ∀ w,
      admissible w → observe w = view → good w (policy (observe w))) ↔
    (∃ action : A, ∀ w,
      admissible w → observe w = view → good w action) := by
  constructor
  · intro h
    obtain ⟨policy, hp⟩ := h
    refine ⟨policy view, ?_⟩
    intro w hw hv
    have result := hp w hw hv
    rw [hv] at result
    exact result
  · intro h
    obtain ⟨action, ha⟩ := h
    exact ⟨fun _ => action, ha⟩

theorem each_world_repair_does_not_give_uniform_action :
    (∀ w : Bool, ∃ a : Bool, a = w) ∧
    ¬ (∃ a : Bool, ∀ w : Bool, a = w) := by
  constructor
  · intro w
    exact ⟨w, rfl⟩
  · intro h
    obtain ⟨a, ha⟩ := h
    have bad : (false : Bool) = true := (ha false).symm.trans (ha true)
    cases bad

/- A minimal execution semantics with an explicit contextual guard.
The guard's truth is an input, not a premise generated by this code. -/

structure DraftState where
  source : List Nat
  draft : List Nat
  revision : Nat
  history : List (List Nat)
  deriving DecidableEq

def applyExact (s : DraftState) : DraftState :=
  { s with draft := s.source, revision := s.revision + 1,
           history := s.history ++ [s.draft] }

def guardedStep (s : DraftState) (allowed : Bool) (payload : List Nat) : DraftState :=
  if allowed = true ∧ payload = s.source then applyExact s else s

theorem accepted_step_repairs_and_preserves
    (s : DraftState) (payload : List Nat)
    (exactPayload : payload = s.source) :
    (guardedStep s true payload).draft = s.source ∧
    (guardedStep s true payload).source = s.source ∧
    (guardedStep s true payload).revision = s.revision + 1 ∧
    (guardedStep s true payload).history = s.history ++ [s.draft] := by
  have guard : (true : Bool) = true ∧ payload = s.source := ⟨rfl, exactPayload⟩
  unfold guardedStep
  rw [if_pos guard]
  exact ⟨rfl, rfl, rfl, rfl⟩

theorem rejected_step_is_unchanged (s : DraftState) (payload : List Nat) :
    guardedStep s false payload = s := by
  simp [guardedStep]

theorem every_guarded_step_preserves_source
    (s : DraftState) (allowed : Bool) (payload : List Nat) :
    (guardedStep s allowed payload).source = s.source := by
  unfold guardedStep
  split <;> rfl

theorem every_guarded_step_preserves_existing_repair
    (s : DraftState) (allowed : Bool) (payload : List Nat)
    (repaired : s.draft = s.source) :
    (guardedStep s allowed payload).draft =
      (guardedStep s allowed payload).source := by
  unfold guardedStep
  split
  · rfl
  · exact repaired

def runGuarded (s : DraftState) : List (Bool × List Nat) → DraftState
  | [] => s
  | (allowed, payload) :: rest =>
      runGuarded (guardedStep s allowed payload) rest

theorem mediated_persistence
    (steps : List (Bool × List Nat)) (s : DraftState)
    (repaired : s.draft = s.source) :
    (runGuarded s steps).draft = (runGuarded s steps).source := by
  induction steps generalizing s with
  | nil => exact repaired
  | cons command rest ih =>
      exact ih (guardedStep s command.1 command.2)
        (every_guarded_step_preserves_existing_repair s command.1 command.2 repaired)

theorem rejection_does_not_restore_wrong_draft
    (s : DraftState) (payload : List Nat) (wrong : s.draft ≠ s.source) :
    (guardedStep s false payload).draft ≠ s.source := by
  simpa [guardedStep] using wrong

/- Infinite recurrence alone fixes no truth value. This is only a logical
test of an equation scheme, not an account of normative authority. -/

def allTrue : Nat → Prop := fun _ => True
def allFalse : Nat → Prop := fun _ => False

theorem constant_true_satisfies_successor_recurrence :
    ∀ i : Nat, (allTrue i ↔ allTrue (i + 1)) := by
  intro i
  rfl

theorem constant_false_satisfies_successor_recurrence :
    ∀ i : Nat, (allFalse i ↔ allFalse (i + 1)) := by
  intro i
  rfl

end CriterionTransport

#print axioms CriterionTransport.witness_relative_exclusion
#print axioms CriterionTransport.uniform_transport_iff_back_coverage
#print axioms CriterionTransport.all_targets_exact_iff_injective
#print axioms CriterionTransport.accepted_step_repairs_and_preserves
#print axioms CriterionTransport.mediated_persistence
