import Std

/-!
# Charged versioned interlocks

Fresh Seventh question-3 formal component.  Uses only Lean 4.19.0's bundled
Std.  The ordinary proof file supplies world/applicability premises, the
explicit low-overlap adversary, and the binomial enumeration argument.

Kernel-checked here: actual finite-root counting; honest cross-intersection;
root-coupled live revocation exclusion; command authorization under a large
path; exact threshold arithmetic; uniqueness of the untainted maximal path;
abstract untested-candidate obstruction; and safe idempotent batch persistence.
No physical gate or external authorization truth is axiomatized as a theorem.
-/

namespace ChargedInterlock

def card : Nat → (Nat → Bool) → Nat
  | 0, _ => 0
  | n + 1, p => card n p + if p n then 1 else 0

theorem card_le (n : Nat) (p : Nat → Bool) : card n p ≤ n := by
  induction n with
  | zero => simp [card]
  | succ n ih =>
    cases hp : p n <;> simp [card, hp] <;> omega

theorem card_mono (n : Nat) (p q : Nat → Bool)
    (h : ∀ i, i < n → p i = true → q i = true) :
    card n p ≤ card n q := by
  induction n with
  | zero => simp [card]
  | succ n ih =>
    have hprev : ∀ i, i < n → p i = true → q i = true := by
      intro i hi hp
      exact h i (by omega) hp
    have hc := ih hprev
    have hn := h n (by omega)
    cases hp : p n <;> cases hq : q n <;>
      simp_all [card] <;> omega

theorem no_honest_overlap_count (n : Nat) (l s c : Nat → Bool)
    (h : ∀ i, i < n → l i = true → s i = true → c i = true) :
    card n l + card n s ≤ n + card n c := by
  induction n with
  | zero => simp [card]
  | succ n ih =>
    have hprev : ∀ i, i < n → l i = true → s i = true → c i = true := by
      intro i hi hl hs
      exact h i (by omega) hl hs
    have hc := ih hprev
    have hn := h n (by omega)
    cases hl : l n <;> cases hs : s n <;> cases hb : c n <;>
      simp_all [card] <;> omega

theorem honest_overlap (n b : Nat) (l s c : Nat → Bool)
    (budget : card n c ≤ b)
    (overlap : n + b < card n l + card n s) :
    ∃ i, i < n ∧ l i = true ∧ s i = true ∧ c i = false := by
  classical
  apply Classical.byContradiction
  intro noWitness
  have hsub : ∀ i, i < n → l i = true → s i = true → c i = true := by
    intro i hi hl hs
    cases hc : c i with
    | false => exact False.elim (noWitness ⟨i, hi, hl, hs, hc⟩)
    | true => rfl
  have hcount := no_honest_overlap_count n l s c hsub
  omega

theorem honest_on_large_path (n b : Nat) (l c : Nat → Bool)
    (budget : card n c ≤ b) (large : b < card n l) :
    ∃ i, i < n ∧ l i = true ∧ c i = false := by
  classical
  apply Classical.byContradiction
  intro noWitness
  have hsub : ∀ i, i < n → l i = true → c i = true := by
    intro i hi hl
    cases hc : c i with
    | false => exact False.elim (noWitness ⟨i, hi, hl, hc⟩)
    | true => rfl
  have hcount := card_mono n l c hsub
  omega

def Lands (n : Nat) (l : Nat → Bool) (gateOpen : Nat → Prop) : Prop :=
  ∀ i, i < n → l i = true → gateOpen i

theorem effective_revocation_blocks (n b : Nat) (l s c : Nat → Bool)
    (gateOpen : Nat → Prop)
    (budget : card n c ≤ b)
    (overlap : n + b < card n l + card n s)
    (durableVeto : ∀ i, i < n → s i = true → c i = false → ¬gateOpen i) :
    ¬Lands n l gateOpen := by
  obtain ⟨i, hi, hl, hs, hc⟩ := honest_overlap n b l s c budget overlap
  intro lands
  exact durableVeto i hi hs hc (lands i hi hl)

theorem charged_cancellation_blocks (n b : Nat) (l cancelSet c : Nat → Bool)
    (gateOpen : Nat → Prop)
    (budget : card n c ≤ b)
    (enoughAcknowledgers : b < card n cancelSet)
    (selectedRoots : ∀ i, i < n → cancelSet i = true → l i = true)
    (durableCancel : ∀ i, i < n → cancelSet i = true → c i = false → ¬gateOpen i) :
    ¬Lands n l gateOpen := by
  obtain ⟨i, hi, hcancel, hc⟩ :=
    honest_on_large_path n b cancelSet c budget enoughAcknowledgers
  intro lands
  exact durableCancel i hi hcancel hc (lands i hi (selectedRoots i hi hcancel))

theorem landed_command_authorized (n b : Nat) (l c : Nat → Bool)
    (gateOpen : Nat → Prop) (authorized : Prop)
    (budget : card n c ≤ b) (large : b < card n l)
    (binding : ∀ i, i < n → c i = false → gateOpen i → authorized)
    (lands : Lands n l gateOpen) : authorized := by
  obtain ⟨i, hi, hl, hc⟩ := honest_on_large_path n b l c budget large
  exact binding i hi hc (lands i hi hl)

/- Compose local binding with an actual revocation witness and the independently
warranted reservation institution.  No honest gate is assumed to possess a
fresh global-currentness oracle. -/
theorem joint_landing_authorized (n b : Nat) (l c : Nat → Bool)
    (gateOpen : Nat → Prop) (locallyBound stale authorized : Prop)
    (budget : card n c ≤ b) (large : b < card n l)
    (binding : ∀ i, i < n → c i = false → gateOpen i → locallyBound)
    (staleCertificate : stale → ∃ s : Nat → Bool,
      n + b < card n l + card n s ∧
      (∀ i, i < n → s i = true → c i = false → ¬gateOpen i))
    (institution : locallyBound → ¬stale → authorized)
    (lands : Lands n l gateOpen) : authorized := by
  have hlocal := landed_command_authorized n b l c gateOpen locallyBound
    budget large binding lands
  have current : ¬stale := by
    intro hs
    obtain ⟨s, overlap, veto⟩ := staleCertificate hs
    exact effective_revocation_blocks n b l s c gateOpen budget overlap veto lands
  exact institution hlocal current

structure ThresholdContract (n b q r : Nat) : Prop where
  overlap : n + b < q + r
  repairAvailable : q + b ≤ n
  revokeAvailable : r + b ≤ n

theorem minimum_roots {n b q r : Nat} (h : ThresholdContract n b q r) :
    3 * b + 1 ≤ n := by
  rcases h with ⟨ho, hq, hr⟩
  omega

theorem large_thresholds {n b q r : Nat} (h : ThresholdContract n b q r) :
    2 * b + 1 ≤ q ∧ 2 * b + 1 ≤ r := by
  rcases h with ⟨ho, hq, hr⟩
  omega

theorem cancellation_available {n b q r : Nat} (h : ThresholdContract n b q r) :
    b + 1 + b ≤ q := by
  obtain ⟨hq, _hr⟩ := large_thresholds h
  omega

theorem minimum_thresholds_unique {b q r : Nat}
    (h : ThresholdContract (3 * b + 1) b q r) :
    q = 2 * b + 1 ∧ r = 2 * b + 1 := by
  rcases h with ⟨ho, hq, hr⟩
  omega

theorem minimal_attainment (b : Nat) :
    ThresholdContract (3 * b + 1) b (2 * b + 1) (2 * b + 1) := by
  constructor <;> omega

theorem general_attainment (n b : Nat) (h : 3 * b < n) :
    ThresholdContract n b (n - b) (n - b) := by
  constructor <;> omega

theorem threshold_feasible_iff (n b : Nat) :
    (∃ q r, ThresholdContract n b q r) ↔ 3 * b + 1 ≤ n := by
  constructor
  · rintro ⟨q, r, h⟩
    exact minimum_roots h
  · intro h
    exact ⟨n - b, n - b, general_attainment n b (by omega)⟩

theorem card_full_pointwise (n : Nat) (p : Nat → Bool)
    (full : card n p = n) : ∀ i, i < n → p i = true := by
  induction n with
  | zero => intro i hi; omega
  | succ n ih =>
    have hb := card_le n p
    have hp : p n = true := by
      cases hn : p n with
      | false => simp [card, hn] at full; omega
      | true => rfl
    have hprev : card n p = n := by simp [card, hp] at full; omega
    intro i hi
    by_cases heq : i = n
    · simpa [heq] using hp
    · exact ih hprev i (by omega)

theorem pointwise_full_card (n : Nat) (p : Nat → Bool)
    (full : ∀ i, i < n → p i = true) : card n p = n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    have hn := full n (by omega)
    have hprev : ∀ i, i < n → p i = true := by
      intro i hi
      exact full i (by omega)
    simpa [card, hn] using ih hprev

theorem card_disjoint_union (n : Nat) (l c : Nat → Bool)
    (disjoint : ∀ i, i < n → l i = true → c i = false) :
    card n (fun i => l i || c i) = card n l + card n c := by
  induction n with
  | zero => simp [card]
  | succ n ih =>
    have hprev : ∀ i, i < n → l i = true → c i = false := by
      intro i hi hl
      exact disjoint i (by omega) hl
    have hc := ih hprev
    have hn := disjoint n (by omega)
    cases hl : l n <;> cases hb : c n <;> simp_all [card] <;> omega

theorem unique_maximal_untainted_path (n : Nat) (l c : Nat → Bool)
    (disjoint : ∀ i, i < n → l i = true → c i = false)
    (sizes : card n l + card n c = n) :
    ∀ i, i < n → l i = !c i := by
  have full : card n (fun i => l i || c i) = n := by
    rw [card_disjoint_union n l c disjoint]
    exact sizes
  have cover := card_full_pointwise n (fun i => l i || c i) full
  intro i hi
  have hcov := cover i hi
  have hdis := disjoint i hi
  cases hl : l i <;> cases hc : c i <;> simp_all

theorem untested_candidate (n k : Nat) (tested : Nat → Bool)
    (cap : card n tested ≤ k) (tooSmall : k < n) :
    ∃ i, i < n ∧ tested i = false := by
  classical
  apply Classical.byContradiction
  intro noWitness
  have full : ∀ i, i < n → tested i = true := by
    intro i hi
    cases ht : tested i with
    | false => exact False.elim (noWitness ⟨i, hi, ht⟩)
    | true => rfl
  have hcount := pointwise_full_card n tested full
  omega

inductive Plant where
  | defective
  | repaired
  | damaged
  deriving DecidableEq, Repr

def safe : Plant → Prop
  | .damaged => False
  | _ => True

def trial (success : Bool) : Plant → Plant
  | .damaged => .damaged
  | state => if success then .repaired else state

def batch : List Bool → Plant → Plant
  | [], state => state
  | success :: rest, state => batch rest (trial success state)

@[simp] theorem trial_repaired (success : Bool) : trial success .repaired = .repaired := by
  cases success <;> rfl

@[simp] theorem trial_damaged (success : Bool) : trial success .damaged = .damaged := rfl

theorem trial_safe (success : Bool) (state : Plant) (h : safe state) :
    safe (trial success state) := by
  cases state <;> cases success <;> simp_all [safe, trial]

@[simp] theorem batch_repaired (results : List Bool) :
    batch results .repaired = .repaired := by
  induction results with
  | nil => rfl
  | cons hd tl ih => simpa [batch] using ih

theorem batch_safe (results : List Bool) (state : Plant) (h : safe state) :
    safe (batch results state) := by
  induction results generalizing state with
  | nil => exact h
  | cons hd tl ih => exact ih (trial hd state) (trial_safe hd state h)

theorem batch_restores (results : List Bool) (state : Plant)
    (hs : safe state) (someSuccess : true ∈ results) :
    batch results state = .repaired := by
  induction results generalizing state with
  | nil => simp at someSuccess
  | cons hd tl ih =>
    cases hd with
    | false =>
      have ht : true ∈ tl := by simpa using someSuccess
      exact ih (trial false state) (trial_safe false state hs) ht
    | true =>
      cases state <;> simp_all [safe, batch, trial]

/- Concrete matched counterexample controls.  `decide` proofs are kernel
checked computations, not calls to an external solver or a physical emulator. -/

def member (xs : List Nat) (i : Nat) : Bool := xs.contains i
def allFirst : Nat → (Nat → Bool) → Bool
  | 0, _ => true
  | n + 1, p => allFirst n p && p n

def oldPath : Nat → Bool := member [0, 1, 2]
def revokeSet : Nat → Bool := member [1, 2, 3]
def taintedOne : Nat → Bool := member [0]
def afterRevoke (s c : Nat → Bool) (i : Nat) : Bool := !(s i && !c i)
def pathOpen (n : Nat) (l gate : Nat → Bool) : Bool :=
  allFirst n (fun i => !l i || gate i)

example : card 4 oldPath = 3 ∧ card 4 revokeSet = 3 ∧ card 4 taintedOne = 1 := by decide
example : pathOpen 4 oldPath (afterRevoke revokeSet taintedOne) = false := by decide
example : pathOpen 4 oldPath (fun _ => true) = true := by decide

def tooSmallPath : Nat → Bool := member [0, 1]
def tooSmallRevoke : Nat → Bool := member [1, 2]
def sharedBad : Nat → Bool := member [1]
example : card 3 tooSmallPath = 2 ∧ card 3 tooSmallRevoke = 2 ∧ card 3 sharedBad = 1 := by decide
example : pathOpen 3 tooSmallPath (afterRevoke tooSmallRevoke sharedBad) = true := by decide

#print axioms honest_overlap
#print axioms effective_revocation_blocks
#print axioms charged_cancellation_blocks
#print axioms cancellation_available
#print axioms joint_landing_authorized
#print axioms threshold_feasible_iff
#print axioms unique_maximal_untainted_path
#print axioms untested_candidate
#print axioms batch_restores
#print axioms batch_safe

end ChargedInterlock
