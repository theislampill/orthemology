import Init

/-! Representation control only, not a metaphysical possibility proof or an
attribution of complete cessation to Ibn Taymiyya. G is one stated kind of
voluntary divine act. Objects are potential labels; E alone marks present
existence. Type and capacity are predicates, never extra object constructors.
The model permits a stronger all-emergent empty state but does not identify it
with the weaker G-empty statement. Modal accessibility and actual time differ. -/
namespace T20.OntologyTypeControl

inductive Obj where
  | ground | gAct (id : Nat) | effect (id : Nat) | other (id : Nat)
  deriving DecidableEq
structure World where
  serial : Nat
  gOn : Bool
  otherOn : Bool

def E (w : World) : Obj → Prop
  | .ground => True
  | .gAct n => n = w.serial ∧ w.gOn = true
  | .effect n => n = w.serial ∧ w.gOn = true
  | .other n => n = w.serial ∧ w.otherOn = true

def Emergent : Obj → Prop | .ground => False | _ => True
def GAct : Obj → Prop | .gAct _ => True | _ => False
def Created : Obj → Prop | .effect _ | .other _ => True | _ => False
def DivineAct (a g : Obj) : Prop := GAct a ∧ g = .ground
def Inheres (a g : Obj) : Prop := DivineAct a g
def Produces : Obj → Obj → Prop
  | .gAct n, .effect m => n = m
  | _, _ => False
-- Whole receipt belongs to the independent bearer level; intrinsic acts are
-- not thereby extraneously supplied. This is an interpretation, not a theorem
-- denying every possible constitutive or intrinsic dependence of acts on God.
def ExternalReceipt (_w : World) (x : Obj) : Prop := Created x

def Power (w : World) (g : Obj) : Prop := E w g ∧ g = .ground
-- G is represented by the predicate GAct, not by another member of Obj.
def EmptyG (w : World) : Prop := ¬ ∃ x, E w x ∧ GAct x
def EmptyEmergent (w : World) : Prop := ¬ ∃ x, E w x ∧ Emergent x
def Necessary (x : Obj) : Prop := ∀ w, E w x
-- serial orders eligible fresh labels. R is an explicitly chosen modal frame,
-- not evidence that the corresponding transition occurs on the actual path.
def R (w v : World) : Prop := w.serial < v.serial
def Diamond (w : World) (P : World → Prop) : Prop := ∃ v, R w v ∧ P v
def Box (w : World) (P : World → Prop) : Prop := ∀ v, R w v → P v
def FreshG (w v : World) : Prop := ∃ n,
  w.serial < n ∧ E v (.gAct n) ∧
  (∀ past : World, past.serial ≤ w.serial → ¬ E past (.gAct n))
def PossibleFreshG (w : World) : Prop := Diamond w (FreshG w)
def PossibleCreated (w : World) : Prop := Diamond w (fun v => ∃ x, E v x ∧ Created x)
def quiet (n : Nat) : World := ⟨n, false, false⟩
def active (n : Nat) : World := ⟨n, true, false⟩
-- Repeated activity uses new identities 1,3,5,...; no old token recurs.
def actual (t : Nat) : World := ⟨t, t % 2 == 1, false⟩

theorem empty_all (n : Nat) : EmptyEmergent (quiet n) ∧ EmptyG (quiet n) := by
  constructor <;> rintro ⟨x, hx, hg⟩ <;> cases x <;> simp_all [E, quiet, Emergent, GAct]

theorem fresh_possible (w : World) : PossibleFreshG w := by
  refine ⟨active (w.serial + 1), Nat.lt_succ_self _, w.serial + 1,
    Nat.lt_succ_self _, ⟨rfl, rfl⟩, ?_⟩
  intro past hp he
  have h := he.1
  have bad : w.serial + 1 ≤ w.serial := h ▸ hp
  exact (Nat.not_succ_le_self _) bad

-- Both the requested G-scoped formula and stronger all-emergent variant are
-- explicit. Neither asserts that the genus is populated at every world/time.
theorem empty_and_renewable (w : World) :
    Diamond w EmptyG ∧ Diamond w EmptyEmergent ∧ Box w PossibleFreshG := by
  exact ⟨⟨quiet (w.serial + 1), Nat.lt_succ_self _, (empty_all _).2⟩,
    ⟨quiet (w.serial + 1), Nat.lt_succ_self _, (empty_all _).1⟩,
    fun v _ => fresh_possible v⟩

theorem created_possibility_has_existent_witness (w : World) : PossibleCreated w := by
  exact ⟨active (w.serial + 1), Nat.lt_succ_self _, .effect (w.serial + 1),
    ⟨rfl, rfl⟩, True.intro⟩

theorem capacity_and_only_one_necessary :
    (∀ w, Power w .ground) ∧ (∀ x, Necessary x ↔ x = .ground) := by
  refine ⟨fun _ => ⟨True.intro, rfl⟩, ?_⟩
  intro x
  cases x with
  | ground => exact ⟨fun _ => rfl, fun _ _ => True.intro⟩
  | gAct n =>
    constructor
    · intro h; exact False.elim (Bool.noConfusion (h (quiet n)).2)
    · intro h; cases h
  | effect n =>
    constructor
    · intro h; exact False.elim (Bool.noConfusion (h (quiet n)).2)
    · intro h; cases h
  | other n =>
    constructor
    · intro h; exact False.elim (Bool.noConfusion (h (quiet n)).2)
    · intro h; cases h

-- A present new act and its product have different createdness. Emergence does
-- not logically imply createdness or external receipt in this signature.
theorem act_product_boundary :
    ¬ E (actual 0) (.gAct 1) ∧ E (actual 1) (.gAct 1) ∧
    Emergent (.gAct 1) ∧ DivineAct (.gAct 1) .ground ∧
    Produces (.gAct 1) (.effect 1) ∧ E (actual 1) (.effect 1) ∧
    Created (.effect 1) ∧ ¬ Created (.gAct 1) ∧
    ¬ ExternalReceipt (actual 1) (.gAct 1) ∧
    Inheres (.gAct 1) .ground ∧ E (actual 1) .ground := by
  simp [E, actual, Emergent, DivineAct, GAct, Produces, Created,
    ExternalReceipt, Inheres]

-- Every represented emergent token ceases after its single indexed occurrence,
-- including tokens of the auxiliary kind. This is stronger than merely showing
-- different labels on two sampled states, and is independent of gOn's pattern.
theorem each_token_ceases (t : Nat) (x : Obj)
    (present : E (actual t) x) (emergent : Emergent x) :
    ∃ u, t < u ∧ ∀ v, u ≤ v → ¬ E (actual v) x := by
  refine ⟨t + 1, Nat.lt_succ_self _, ?_⟩
  intro v hv he
  have lt : t < v := Nat.lt_of_lt_of_le (Nat.lt_succ_self _) hv
  cases x with
  | ground => exact emergent
  | gAct n => exact (Nat.ne_of_lt lt) (present.1.symm.trans he.1)
  | effect n => exact (Nat.ne_of_lt lt) (present.1.symm.trans he.1)
  | other n => exact (Nat.ne_of_lt lt) (present.1.symm.trans he.1)

theorem actual_gap_and_new_act :
    EmptyEmergent (actual 2) ∧ E (actual 3) (.gAct 3) ∧
    (.gAct 3 : Obj) ≠ .gAct 1 ∧ PossibleFreshG (actual 2) ∧
    ¬ (∀ t, ∃ x, E (actual t) x ∧ Emergent x) := by
  have gap : EmptyEmergent (actual 2) := (empty_all 2).1
  refine ⟨gap, by simp [E, actual], by decide, fresh_possible _, ?_⟩
  intro all
  exact gap (all 2)

-- G-empty is strictly weaker than all kinds empty: another emergent kind may
-- be present while G has no present token.
theorem scoped_absence_is_not_global : ∃ w, EmptyG w ∧ ¬ EmptyEmergent w := by
  refine ⟨⟨0, false, true⟩, ?_, ?_⟩
  · rintro ⟨x, hx, hg⟩
    cases x <;> simp_all [E, GAct]
  · intro h
    exact h ⟨.other 0, ⟨rfl, rfl⟩, True.intro⟩

#print axioms empty_and_renewable
#print axioms created_possibility_has_existent_witness
#print axioms capacity_and_only_one_necessary
#print axioms act_product_boundary
#print axioms each_token_ceases
#print axioms actual_gap_and_new_act
#print axioms scoped_absence_is_not_global
end T20.OntologyTypeControl
