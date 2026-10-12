import Init

/-!
A semantic discrimination, not a proof of metaphysical premise warrant.
`Available` is an assignment of actual resource instantiations. A rule says
which instantiated resources suffice for the designated consequent resource.
Rules can have infinitely many prerequisites. `Original` means nonreceived
in the fixed existential respect, not an initially occurring temporal act.
-/
namespace ExplanatoryGeneration
universe u v
variable {R : Type u} {I : Type v}

structure Supply (R : Type u) (I : Type v) where
  original : R → Prop
  needs : I → R → Prop
  output : I → R

def Enabled (s : Supply R I) (D : R → Prop) (r : R) : Prop :=
  s.original r ∨ ∃ i, s.output i = r ∧ ∀ p, s.needs i p → D p

def LocalFixed (s : Supply R I) (D : R → Prop) : Prop :=
  ∀ r, D r ↔ Enabled s D r

def Closed (s : Supply R I) (D : R → Prop) : Prop :=
  ∀ r, Enabled s D r → D r

def NoEmptyRules (s : Supply R I) : Prop := ∀ i, ∃ p, s.needs i p

inductive Generated (s : Supply R I) : R → Prop where
  | original {r} : s.original r → Generated s r
  | rule (i) : (∀ p, s.needs i p → Generated s p) → Generated s (s.output i)

-- This condition is the proposed explanatory selection; it is NOT inferred
-- from LocalFixed. It must receive independent philosophical/application warrant.
def NoUngenerated (s : Supply R I) (D : R → Prop) : Prop :=
  ∀ r, D r → Generated s r

theorem generated_closed (s : Supply R I) : Closed s (Generated s) := by
  intro r h
  rcases h with h | ⟨i, hi, hs⟩
  · exact Generated.original h
  · rw [← hi]; exact Generated.rule i hs

theorem generated_local_fixed (s : Supply R I) : LocalFixed s (Generated s) := by
  intro r
  constructor
  · intro h
    cases h with
    | original h => exact Or.inl h
    | rule i h => exact Or.inr ⟨i, rfl, h⟩
  · exact generated_closed s r

theorem generated_least (s : Supply R I) (D : R → Prop)
    (closed : Closed s D) : ∀ r, Generated s r → D r := by
  intro r h
  induction h with
  | original h => exact closed _ (Or.inl h)
  | rule i _ ih => exact closed _ (Or.inr ⟨i, rfl, ih⟩)

theorem selection_iff_least (s : Supply R I) (D : R → Prop)
    (closed : Closed s D) :
    NoUngenerated s D ↔ ∀ r, D r ↔ Generated s r := by
  constructor
  · intro h r
    exact ⟨h r, generated_least s D closed r⟩
  · intro h r hr; exact (h r).mp hr

theorem generated_has_original (s : Supply R I) (nonempty : NoEmptyRules s)
    {r} (h : Generated s r) : ∃ o, s.original o := by
  induction h with
  | original h => exact ⟨_, h⟩
  | rule i _ ih =>
    obtain ⟨p, hp⟩ := nonempty i
    exact ih p hp

theorem actual_generation_has_original (s : Supply R I) (D : R → Prop)
    (nonempty : NoEmptyRules s) (selected : NoUngenerated s D)
    (actual : ∃ r, D r) : ∃ o, s.original o := by
  obtain ⟨r, hr⟩ := actual
  exact generated_has_original s nonempty (selected r hr)

inductive SupplyPath (s : Supply R I) : R → R → Prop where
  | refl (r) : SupplyPath s r r
  | step {a p} (i) : SupplyPath s a p → s.needs i p →
      SupplyPath s a (s.output i)

theorem generated_has_relevant_original (s : Supply R I)
    (nonempty : NoEmptyRules s) {r} (h : Generated s r) :
    ∃ o, s.original o ∧ SupplyPath s o r := by
  induction h with
  | original h => exact ⟨_, h, SupplyPath.refl _⟩
  | rule i _ ih =>
    obtain ⟨p, hp⟩ := nonempty i
    obtain ⟨o, ho, path⟩ := ih p hp
    exact ⟨o, ho, SupplyPath.step i path hp⟩

theorem selected_actual_target_has_same_original_resource
    (s : Supply R I) (D : R → Prop)
    (fixed : LocalFixed s D) (nonempty : NoEmptyRules s)
    (selected : NoUngenerated s D) {r} (actual : D r) :
    ∃ o, D o ∧ s.original o ∧ SupplyPath s o r := by
  obtain ⟨o, ho, path⟩ :=
    generated_has_relevant_original s nonempty (selected r actual)
  exact ⟨o, (fixed o).mpr (Or.inl ho), ho, path⟩

theorem SupplyPath.trans {s : Supply R I} {a b c}
    (hab : SupplyPath s a b) (hbc : SupplyPath s b c) : SupplyPath s a c := by
  induction hbc with
  | refl => exact hab
  | step i _ hp ih => exact SupplyPath.step i ih hp

/-- This requires only one generated, actual contribution to the target.
It does not require the target, all its branches, or the whole field generated. -/
theorem one_generated_contribution_suffices (s : Supply R I) (D : R → Prop)
    (fixed : LocalFixed s D) (nonempty : NoEmptyRules s) {target}
    (anchor : ∃ q, D q ∧ Generated s q ∧ SupplyPath s q target) :
    ∃ o, D o ∧ s.original o ∧ SupplyPath s o target := by
  obtain ⟨q, _, hq, qt⟩ := anchor
  obtain ⟨o, ho, oq⟩ := generated_has_relevant_original s nonempty hq
  exact ⟨o, (fixed o).mpr (Or.inl ho), ho, SupplyPath.trans oq qt⟩

-- A fully infinite acyclic, all-received account. There is no artificial last
-- node or finite truncation; each n receives from n+1.
def regress : Supply Nat Nat where
  original := fun _ => False
  needs := fun n p => p = n + 1
  output := id

theorem regress_no_empty : NoEmptyRules regress := fun n => ⟨n+1, rfl⟩
theorem regress_local : LocalFixed regress (fun _ => True) := by
  intro n
  constructor
  · intro _; exact Or.inr ⟨n, rfl, fun _ _ => trivial⟩
  · intro _; trivial

theorem regress_has_no_generated (n : Nat) : ¬ Generated regress n := by
  intro h
  obtain ⟨o, ho⟩ := generated_has_original regress regress_no_empty h
  exact ho

theorem regress_selection_fails : ¬ NoUngenerated regress (fun _ => True) := by
  intro h; exact regress_has_no_generated 0 (h 0 trivial)

theorem regress_fixed_succ (D : Nat → Prop) (fixed : LocalFixed regress D)
    (n : Nat) : D n ↔ D (n+1) := by
  constructor
  · intro h
    rcases (fixed n).mp h with impossible | ⟨i, hi, hs⟩
    · exact False.elim impossible
    · change i = n at hi
      subst i
      exact hs (n+1) rfl
  · intro h
    apply (fixed n).mpr
    refine Or.inr ⟨n, rfl, ?_⟩
    intro p hp
    change p = n+1 at hp
    rw [hp]; exact h

/-- The observed nonempty solution is globally determinate, still seedless.
Observation is a constraint, not an original supply token. -/
theorem regress_observation_determines_profile (D : Nat → Prop)
    (fixed : LocalFixed regress D) (observed : D 0) : ∀ n, D n := by
  intro n
  induction n with
  | zero => exact observed
  | succ n ih => exact (regress_fixed_succ D fixed n).mp ih

-- Every prerequisite index strictly exceeds its output; strict natural-number
-- order is an acyclic majorant. This is not a graph with hidden self-loops.
theorem regress_strict (i p : Nat) (h : regress.needs i p) :
    regress.output i < p := by
  change p = i+1 at h
  rw [h]
  exact Nat.lt_succ_self i

-- A nonempty original component does not select the unsupported branch.
def island : Supply (Option Nat) Nat where
  original := fun r => r = none
  needs := fun n p => p = some (n+1)
  output := some

theorem island_local : LocalFixed island (fun _ => True) := by
  intro r; constructor
  · intro _; cases r with
    | none => exact Or.inl rfl
    | some n => exact Or.inr ⟨n, rfl, fun _ _ => trivial⟩
  · intro _; trivial

theorem island_generated_only_original {r} (h : Generated island r) : r = none := by
  induction h with
  | original h => exact h
  | rule i _ ih =>
    have bad := ih (some (i+1)) rfl
    cases bad

theorem island_original_but_ungenerated_branch :
    (∃ o, island.original o) ∧ ¬ NoUngenerated island (fun _ => True) := by
  refine ⟨⟨none, rfl⟩, ?_⟩
  intro h
  have bad := island_generated_only_original (h (some 0) trivial)
  cases bad

-- A target has a genuinely relevant original contributor while a second
-- actual requisite branch remains ungenerated. T17's existential witness and
-- T19's complete original coverage must therefore be assessed separately.
def mixedTarget : Supply (Option Nat) Nat where
  original := fun r => r = none
  needs := fun n p => p = some (n+1) ∨ (n = 0 ∧ p = none)
  output := some

theorem mixedTarget_local : LocalFixed mixedTarget (fun _ => True) := by
  intro r; constructor
  · intro _; cases r with
    | none => exact Or.inl rfl
    | some n => exact Or.inr ⟨n, rfl, fun _ _ => trivial⟩
  · intro _; trivial

theorem mixedTarget_only_seed_generated {r}
    (h : Generated mixedTarget r) : r = none := by
  induction h with
  | original h => exact h
  | rule i _ ih =>
    have bad := ih (some (i+1)) (Or.inl rfl)
    cases bad

theorem weaker_anchor_without_target_generation :
    (∃ q, Generated mixedTarget q ∧ SupplyPath mixedTarget q (some 0)) ∧
    ¬ Generated mixedTarget (some 0) := by
  constructor
  · refine ⟨none, Generated.original rfl, ?_⟩
    exact SupplyPath.step 0 (SupplyPath.refl none) (Or.inr ⟨rfl, rfl⟩)
  · intro h
    have bad := mixedTarget_only_seed_generated h
    cases bad

-- An infinite family of prerequisites is allowed. some n has n-step generated
-- support; the output none requires every some n. There is no finite bound on
-- the requisite derivation depths even though the output has a generated proof.
def infiniteFan : Supply (Option Nat) (Option Nat) where
  original := fun r => r = some 0
  needs := fun i p => match i with
    | some n => p = some n
    | none => ∃ n, p = some n
  output := fun i => match i with
    | some n => some (n+1)
    | none => none

theorem infiniteFan_no_empty : NoEmptyRules infiniteFan := by
  intro i; cases i with
  | none => exact ⟨some 0, 0, rfl⟩
  | some n => exact ⟨some n, rfl⟩

theorem infiniteFan_finite_generated (n : Nat) : Generated infiniteFan (some n) := by
  induction n with
  | zero => exact Generated.original rfl
  | succ n ih =>
    apply Generated.rule (some n)
    intro p hp
    change p = some n at hp
    rw [hp]; exact ih

theorem infiniteFan_limit_generated : Generated infiniteFan none := by
  apply Generated.rule none
  intro p hp
  obtain ⟨n, hn⟩ := hp
  rw [hn]; exact infiniteFan_finite_generated n

theorem infiniteFan_all_generated : NoUngenerated infiniteFan (fun _ => True) := by
  intro r _; cases r with
  | none => exact infiniteFan_limit_generated
  | some n => exact infiniteFan_finite_generated n

-- Finite-stage iteration does NOT exhaust arbitrary-arity generation.
def Stage (s : Supply R I) : Nat → R → Prop
  | 0 => fun _ => False
  | n+1 => Enabled s (Stage s n)

theorem infiniteFan_stage_bound (n : Nat) :
    ∀ r, Stage infiniteFan n r → ∃ k, r = some k ∧ k < n := by
  induction n with
  | zero => intro r h; exact False.elim h
  | succ n ih =>
    intro r h
    rcases h with horig | ⟨i, hi, hs⟩
    · exact ⟨0, horig, Nat.zero_lt_succ n⟩
    · cases i with
      | none =>
        have hn := hs (some n) ⟨n, rfl⟩
        obtain ⟨k, hk, hkn⟩ := ih (some n) hn
        have eq : n = k := Option.some.inj hk
        subst k
        exact False.elim (Nat.lt_irrefl n hkn)
      | some k =>
        have hk := hs (some k) rfl
        obtain ⟨j, hj, hjn⟩ := ih (some k) hk
        have eq : k = j := Option.some.inj hj
        subst j
        exact ⟨k+1, hi.symm, Nat.succ_lt_succ hjn⟩

theorem generated_beyond_every_finite_stage :
    Generated infiniteFan none ∧ ∀ n, ¬ Stage infiniteFan n none := by
  refine ⟨infiniteFan_limit_generated, ?_⟩
  intro n h
  obtain ⟨k, hk, _⟩ := infiniteFan_stage_bound n none h
  cases hk

inductive RegPath : Nat → Nat → Prop where
  | edge {a b} : regress.needs b a → RegPath a b
  | trans {a b c} : RegPath a b → RegPath b c → RegPath a c

theorem regress_path_strict {a b} (h : RegPath a b) : b < a := by
  induction h with
  | edge h => exact regress_strict _ _ h
  | trans _ _ h1 h2 => exact Nat.lt_trans h2 h1

theorem regress_acyclic (a : Nat) : ¬ RegPath a a := by
  intro h; exact Nat.lt_irrefl a (regress_path_strict h)

-- Empty received rules would manufacture an original-looking availability
-- without any original input. NoEmptyRules is therefore a genuine guard.
def emptyRule : Supply Unit Unit where
  original := fun _ => False
  needs := fun _ _ => False
  output := fun _ => ()

theorem empty_rule_breaks_seed_conclusion :
    Generated emptyRule () ∧ ¬ (∃ o, emptyRule.original o) ∧
    ¬ NoEmptyRules emptyRule := by
  refine ⟨Generated.rule () (fun _ h => False.elim h), ?_, ?_⟩
  · intro h; obtain ⟨_, h⟩ := h; exact h
  · intro h; obtain ⟨_, h⟩ := h (); exact h

-- A source-internal adverse control: mutually conditioned created powers can
-- derive from one common giver (Safadiyya S003 L207). Necessary co-presence must
-- not automatically become prior generative supply.
def confusedConditions : Supply (Option Bool) Bool where
  original := fun r => r = none
  needs := fun i p => p = none ∨ p = some (!i)
  output := some

def commonProvision : Supply (Option Bool) Bool where
  original := fun r => r = none
  needs := fun _ p => p = none
  output := some

def CoPresent (D : Option Bool → Prop) : Prop :=
  D (some false) ↔ D (some true)

theorem confused_local : LocalFixed confusedConditions (fun _ => True) := by
  intro r; constructor
  · intro _; cases r with
    | none => exact Or.inl rfl
    | some b => exact Or.inr ⟨b, rfl, fun _ _ => trivial⟩
  · intro _; trivial

theorem confused_generated_only_original {r}
    (h : Generated confusedConditions r) : r = none := by
  induction h with
  | original h => exact h
  | rule i _ ih =>
    have bad := ih (some (!i)) (Or.inr rfl)
    cases bad

theorem common_provision_generates_both :
    ∀ r, Generated commonProvision r := by
  intro r; cases r with
  | none => exact Generated.original rfl
  | some b =>
    apply Generated.rule b
    intro p hp
    exact Generated.original hp

theorem same_copresence_different_generativity :
    CoPresent (fun _ => True) ∧
    LocalFixed confusedConditions (fun _ => True) ∧
    (∀ r, Generated commonProvision r) ∧
    ¬ NoUngenerated confusedConditions (fun _ => True) := by
  refine ⟨Iff.rfl, confused_local, common_provision_generates_both, ?_⟩
  intro h
  have bad := confused_generated_only_original (h (some false) trivial)
  cases bad

-- Temporal action tokens are deliberately a distinct type/level from standing
-- resources. Reverse-Nat order supplies an infinite past (ending at index 0).
-- All actions have the original resource, yet there is no earliest token.
def actionEarlier (a b : Nat) : Prop := b < a

def actionOccurs (_ : Nat) : Prop := True

def standing : Supply Unit Empty where
  original := fun _ => True
  needs := fun i => nomatch i
  output := fun i => nomatch i

theorem standing_all_generated : ∀ r, Generated standing r :=
  fun _ => Generated.original trivial

theorem beginningless_actions_with_original_resource :
    (∀ n, actionOccurs n ∧ Generated standing ()) ∧
    (∀ n, ∃ m, actionOccurs m ∧ actionEarlier m n) := by
  constructor
  · intro n; exact ⟨trivial, standing_all_generated ()⟩
  · intro n; exact ⟨n+1, trivial, Nat.lt_succ_self n⟩

-- If the very same recurrence is misapplied as a resource-generation rule,
-- the original standing resource is lost and every token is ungenerated.
-- The discrepancy is a semantic typing failure, not a refutation of the source.
theorem recurrence_cannot_select_explanatory_level :
    (∀ n, ∃ m, actionEarlier m n) ∧
    LocalFixed regress actionOccurs ∧
    (∀ n, ¬ Generated regress n) := by
  exact ⟨fun n => ⟨n+1, Nat.lt_succ_self n⟩, regress_local,
    regress_has_no_generated⟩

end ExplanatoryGeneration
