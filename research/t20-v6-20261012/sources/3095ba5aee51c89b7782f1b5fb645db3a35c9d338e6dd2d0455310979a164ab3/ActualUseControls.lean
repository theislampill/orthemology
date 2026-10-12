import ExplanatoryGeneration

/-!
The imported SupplyPath is CANDIDATE-rule ancestry. This file tests and repairs
that interface. A selected actual rule, instantiated endpoints, nonreflexive
exercise, and receipt completeness are distinct application obligations.
-/
namespace ActualUseControls
open ExplanatoryGeneration
universe u v
variable {R : Type u} {I : Type v}

def usedSupply (s : Supply R I) (used : I → Prop) : Supply R {i // used i} where
  original := s.original
  needs := fun i => s.needs i.1
  output := fun i => s.output i.1

def UsedReceipt (s : Supply R I) (used : I → Prop) (r : R) : Prop :=
  ∃ i, used i ∧ s.output i = r

def UsedSound (s : Supply R I) (used : I → Prop) (D : R → Prop) : Prop :=
  ∀ i, used i → D (s.output i) ∧ ∀ p, s.needs i p → D p

def SeedSound (s : Supply R I) (used : I → Prop) (D : R → Prop) : Prop :=
  ∀ r, s.original r → D r ∧ ¬ UsedReceipt s used r

-- At least one actual edge is required. Reflexive coverage is insufficient.
def PositiveUsedPath (s : Supply R I) (used : I → Prop) (a b : R) : Prop :=
  ∃ i p, used i ∧ s.needs i p ∧ s.output i = b ∧
    SupplyPath (usedSupply s used) a p

theorem positive_target_actual (s : Supply R I) (used : I → Prop) (D : R → Prop)
    (sound : UsedSound s used D) {a b} (path : PositiveUsedPath s used a b) : D b := by
  obtain ⟨i, p, hi, _, out, _⟩ := path
  rw [← out]; exact (sound i hi).1

theorem actual_anchor_original_witness (s : Supply R I) (used : I → Prop)
    (D : R → Prop) (sound : UsedSound s used D) (seeds : SeedSound s used D)
    (nonempty : NoEmptyRules (usedSupply s used)) {target}
    (anchor : ∃ q, Generated (usedSupply s used) q ∧ PositiveUsedPath s used q target) :
    D target ∧ ∃ o, D o ∧ s.original o ∧ ¬ UsedReceipt s used o ∧
      PositiveUsedPath s used o target := by
  obtain ⟨q, hq, qt⟩ := anchor
  obtain ⟨o, ho, oq⟩ := generated_has_relevant_original (usedSupply s used) nonempty hq
  obtain ⟨i, p, hi, hp, out, qp⟩ := qt
  have ot : PositiveUsedPath s used o target :=
    ⟨i, p, hi, hp, out, SupplyPath.trans oq qp⟩
  exact ⟨positive_target_actual s used D sound ot,
    o, (seeds o ho).1, ho, (seeds o ho).2, ot⟩

theorem positive_target_has_used_receipt (s : Supply R I) (used : I → Prop)
    {a b} (path : PositiveUsedPath s used a b) : UsedReceipt s used b := by
  obtain ⟨i, _, hi, _, out, _⟩ := path
  exact ⟨i, hi, out⟩

theorem positive_original_is_distinct_from_target (s : Supply R I)
    (used : I → Prop) (D : R → Prop) (seeds : SeedSound s used D)
    {o target} (original : s.original o) (path : PositiveUsedPath s used o target) :
    o ≠ target := by
  intro eq
  have rec := positive_target_has_used_receipt s used path
  rw [← eq] at rec
  exact (seeds o original).2 rec

-- Nonreceipt of graph supply is not whole-existence nonreceipt unless every
-- such receipt has been included. This is a conditional interface, not proof
-- that all grounds are productive rules.
theorem whole_nonreceipt_needs_complete_representation
    (s : Supply R I) (used : I → Prop) (wholeReceived : R → Prop)
    (complete : ∀ r, wholeReceived r → UsedReceipt s used r)
    {r} (noSupply : ¬ UsedReceipt s used r) : ¬ wholeReceived r :=
  fun h => noSupply (complete r h)

inductive Node where | seed | blocker | live (n : Nat) | target
  deriving DecidableEq, Repr
inductive Rule where | dormant | flow (n : Nat) | terminal
  deriving DecidableEq, Repr

def dormantModel : Supply Node Rule where
  original := fun r => r = .seed
  needs := fun i r => match i with
    | .dormant => r = .seed ∨ r = .blocker
    | .flow n => r = .live (n+1)
    | .terminal => r = .live 0
  output := fun i => match i with
    | .dormant => .target
    | .flow n => .live n
    | .terminal => .target

def liveAvailable : Node → Prop | .blocker => False | _ => True
def actuallyUsed : Rule → Prop | .dormant => False | _ => True

theorem dormant_local_fixed : LocalFixed dormantModel liveAvailable := by
  intro r
  cases r with
  | seed =>
    constructor
    · intro _; exact Or.inl rfl
    · intro _; trivial
  | blocker =>
    constructor
    · intro h; exact False.elim h
    · intro h
      rcases h with h | ⟨i, hi, _⟩
      · cases h
      · cases i <;> cases hi
  | live n =>
    constructor
    · intro _; exact Or.inr ⟨.flow n, rfl, by
        intro p hp; change p = .live (n+1) at hp; subst p; trivial⟩
    · intro _; trivial
  | target =>
    constructor
    · intro _; exact Or.inr ⟨.terminal, rfl, by
        intro p hp; change p = .live 0 at hp; subst p; trivial⟩
    · intro _; trivial

theorem dormant_used_sound : UsedSound dormantModel actuallyUsed liveAvailable := by
  intro i hi
  cases i with
  | dormant => exact False.elim hi
  | flow n =>
    refine ⟨trivial, ?_⟩
    intro p hp; change p = .live (n+1) at hp; subst p; trivial
  | terminal =>
    refine ⟨trivial, ?_⟩
    intro p hp; change p = .live 0 at hp; subst p; trivial

theorem dormant_seed_sound : SeedSound dormantModel actuallyUsed liveAvailable := by
  intro r hr
  change r = .seed at hr; subst r
  refine ⟨trivial, ?_⟩
  intro h; obtain ⟨i, _, out⟩ := h
  cases i <;> cases out

theorem dormant_syntactic_anchor :
    liveAvailable Node.seed ∧ liveAvailable Node.target ∧ Generated dormantModel Node.seed ∧
    SupplyPath dormantModel Node.seed Node.target := by
  exact ⟨trivial, trivial, Generated.original rfl,
    SupplyPath.step (s := dormantModel) Rule.dormant (SupplyPath.refl Node.seed) (Or.inl rfl)⟩

theorem dormant_rule_disabled :
    ¬ actuallyUsed .dormant ∧ ¬ (∀ p, dormantModel.needs .dormant p → liveAvailable p) := by
  refine ⟨id, ?_⟩
  intro h; exact h .blocker (Or.inr rfl)

theorem used_seed_path_stays_seed {r}
    (path : SupplyPath (usedSupply dormantModel actuallyUsed) .seed r) : r = .seed := by
  induction path with
  | refl => rfl
  | step i _ hp ih =>
    subst_vars
    rcases i with ⟨i, hi⟩
    cases i with
    | dormant => exact False.elim hi
    | flow n => cases hp
    | terminal => cases hp

theorem no_actual_seed_path_to_live_target :
    ¬ PositiveUsedPath dormantModel actuallyUsed .seed .target := by
  intro h
  obtain ⟨i, p, hi, hp, _, path⟩ := h
  have eq := used_seed_path_stays_seed path
  subst p
  cases i with
  | dormant => exact False.elim hi
  | flow n => cases hp
  | terminal => cases hp

-- An acyclic actual supply can enter a designated inductive seed. Thus seed
-- membership and even generated availability are not actual nonreceipt.
def overlappingSeeds : Supply Bool Unit where
  original := fun _ => True
  needs := fun _ r => r = true
  output := fun _ => false

theorem seed_can_receive_actual_supply :
    Generated overlappingSeeds false ∧ UsedReceipt overlappingSeeds (fun _ => True) false ∧
    ¬ SeedSound overlappingSeeds (fun _ => True) (fun _ => True) := by
  have receipt : UsedReceipt overlappingSeeds (fun _ => True) false := ⟨(), trivial, rfl⟩
  exact ⟨Generated.original trivial, receipt, fun h => (h false trivial).2 receipt⟩

theorem overlap_has_only_distinct_supply_endpoints :
    ∀ i p, overlappingSeeds.needs i p → p ≠ overlappingSeeds.output i := by
  intro i p hp
  change p = true at hp; subst p
  change true ≠ false
  decide

end ActualUseControls
