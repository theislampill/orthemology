import Std

/- A source-relative finite relational control. This certifies only the explicit
   predicates below. It does not make Full a genuine metaphysical explanation. -/
namespace RestrictedBridgeControl

abbrev Fact := Fin 3
abbrev Plurality := Fin 8

instance (p : Fact → Prop) [DecidablePred p] : Decidable (∃ x, p x) := by
  have h : (∃ x, p x) ↔ p 0 ∨ p 1 ∨ p 2 :=
    Fin.exists_fin_succ.trans (or_congr_right Fin.exists_fin_two)
  exact decidable_of_iff _ h.symm

def b : Fact := 0
def u : Fact := 1
def c : Fact := 2

def Mem (x : Fact) (S : Plurality) : Prop :=
  (S.val / (2 ^ x.val)) % 2 = 1

def Single (x : Fact) : Plurality :=
  if x = b then 1 else if x = u then 2 else 4

def Part (x y : Fact) : Prop := x = y ∨ y = c

def Universal (x : Fact) : Prop := x = u

def Particular (x : Fact) : Prop := x = b

def Supernatural (_x : Fact) : Prop := False

def Basic (x : Fact) : Prop := Particular x ∧ ¬ Supernatural x

-- k=true adds the permitted universal self-explanation; both controls pass.
def Full (k : Bool) (x : Fact) (S : Plurality) : Prop :=
  (x = c ∧ S = 1) ∨ (k = true ∧ x = u ∧ S = 2)

def Partial (k : Bool) (x : Fact) (S : Plurality) : Prop :=
  ∃ z : Fact, Part x z ∧ Full k z S

def Overlap (x y : Fact) : Prop :=
  ∃ z : Fact, Part z x ∧ Part z y

instance (x : Fact) (S : Plurality) : Decidable (Mem x S) :=
  inferInstanceAs (Decidable ((S.val / (2 ^ x.val)) % 2 = 1))
instance (x y : Fact) : Decidable (Part x y) :=
  inferInstanceAs (Decidable (x = y ∨ y = c))
instance (x : Fact) : Decidable (Universal x) :=
  inferInstanceAs (Decidable (x = u))
instance (x : Fact) : Decidable (Particular x) :=
  inferInstanceAs (Decidable (x = b))
instance (x : Fact) : Decidable (Supernatural x) :=
  inferInstanceAs (Decidable False)
instance (x : Fact) : Decidable (Basic x) :=
  inferInstanceAs (Decidable (Particular x ∧ ¬ Supernatural x))
instance (k : Bool) (x : Fact) (S : Plurality) : Decidable (Full k x S) :=
  inferInstanceAs (Decidable ((x = c ∧ S = 1) ∨ (k = true ∧ x = u ∧ S = 2)))
instance (k : Bool) (x : Fact) (S : Plurality) : Decidable (Partial k x S) :=
  inferInstanceAs (Decidable (∃ z : Fact, Part x z ∧ Full k z S))
instance (x y : Fact) : Decidable (Overlap x y) :=
  inferInstanceAs (Decidable (∃ z : Fact, Part z x ∧ Part z y))

set_option maxRecDepth 100000
set_option maxHeartbeats 10000000

theorem singleton_membership :
    ∀ x y, Mem y (Single x) ↔ y = x := by decide

theorem nonempty_iff_some_member :
    ∀ S, S ≠ 0 ↔ ∃ x, Mem x S := by decide

theorem part_order :
    (∀ x, Part x x) ∧
    (∀ x y z, Part x y → Part y z → Part x z) ∧
    (∀ x y, Part x y → Part y x → x = y) := by decide

theorem strong_supplementation :
    ∀ x y, ¬ Part x y → ∃ z, Part z x ∧ ¬ Overlap z y := by decide

theorem nonempty_fusion :
    ∀ S, S ≠ 0 → ∃ f : Fact,
      (∀ x, Mem x S → Part x f) ∧
      (∀ z, Overlap z f ↔ ∃ x, Mem x S ∧ Overlap z x) := by decide

theorem particular_exactly_no_universal_part :
    ∀ x, Particular x ↔ ¬ ∃ z, Universal z ∧ Part z x := by decide

theorem restricted_psr :
    ∀ k S, S ≠ 0 → (∀ x, Mem x S → Basic x) →
      ∃ y, Full k y S ∧ (∀ x, Mem x S → y ≠ x ∧ ¬ Part y x) := by decide

theorem explanatory_particularity :
    ∀ k x S, Full k x S → (∃ y, Mem y S ∧ Particular y) →
      ∃ p, Particular p ∧ Part p x := by decide

theorem no_basic_full_self_explanation :
    ∀ k x, Basic x → ¬ Full k x (Single x) := by decide

theorem complete_transitivity :
    ∀ k x S y T, Full k x S → Mem y S → Full k y T → Full k x T := by decide

theorem partial_transitivity :
    ∀ k x S y T, Partial k x S → Mem y S → Full k y T → Partial k x T := by decide

theorem distributivity :
    ∀ k x S y z, Full k x S → Mem y S → (z = y ∨ Part z y) →
      Full k x (Single z) := by decide

theorem no_extended_circles :
    ∀ k x S y, Partial k x S → Mem y S → y ≠ x → ¬ Part y x →
      ¬ Partial k y (Single x) := by decide

theorem full_implies_partial :
    ∀ k x S, Full k x S → Partial k x S := by decide

theorem partial_source_closure :
    ∀ k x y S, Part x y → Partial k y S → Partial k x S := by decide

-- Even parthood-minimal full explanations do not remove the problem.
theorem full_explainers_part_minimal :
    ∀ k x S, Full k x S → ∀ z, Part z x → z ≠ x → ¬ Full k z S := by decide

theorem basic_partially_explains_itself :
    ∀ k, Partial k b (Single b) ∧ Part b c ∧ b ≠ c ∧ Full k c (Single b) := by decide

theorem no_supernatural : ¬ ∃ x, Supernatural x := by decide

theorem unrestricted_psr_fails :
    ∀ k, ¬ ∀ S, S ≠ 0 → ∃ x, Full k x S := by decide

theorem basic_nonempty : ∃ x, Basic x := by decide

end RestrictedBridgeControl

#print axioms RestrictedBridgeControl.restricted_psr
#print axioms RestrictedBridgeControl.explanatory_particularity
#print axioms RestrictedBridgeControl.complete_transitivity
#print axioms RestrictedBridgeControl.partial_transitivity
#print axioms RestrictedBridgeControl.distributivity
#print axioms RestrictedBridgeControl.no_extended_circles
#print axioms RestrictedBridgeControl.strong_supplementation
#print axioms RestrictedBridgeControl.nonempty_fusion
#print axioms RestrictedBridgeControl.full_explainers_part_minimal
#print axioms RestrictedBridgeControl.no_supernatural
