import TypedObservations
import FamilyObstructions

/- These are explicitly conditional candidate-model laws. The source typing
results are separate. No whole-source model or naturality law is assumed. -/
namespace TypedObserverFamilyContract
open TypeIndexedFamilyObstructions
universe u v w q

/-- Q is a proposed carrier for All(twk B) at a fixed outer environment and
D is the fixed interpretation of B. Type-weakening must identify twk B under
(i :: rho) with this same D, preserving the valuation of the weakened telescope.

`reintroAt r x` interprets the actual fixed_reabstract route: eliminate x at r,
weaken that result, then introduce All. The assembly law is compositional;
`erased_cycle` is derivation independence for the exact same source judgement.
Neither law is a generic graph/naturality axiom. -/
structure FixedAllContract (U : Type u) (D : Type v) (Q : Type q) where
  decode : Q → U → D
  reintroAt : U → Q → Q
  assembly : ∀ r x i, decode (reintroAt r x) i = decode x r
  erased_cycle : ∀ r x, reintroAt r x = x

theorem fixed_result_constant {U : Type u} {D : Type v} {Q : Type q}
    (c : FixedAllContract U D Q) (x : Q) (i j : U) :
    c.decode x i = c.decode x j := by
  have h := c.assembly j x i
  rw [c.erased_cycle] at h
  exact h

/-- Source observe_all_has requires its interpretation to assemble precisely
the typed structured body. This rejects variation only where this body sees it. -/
theorem observer_uniform {U : Type u} {D : Type v} {Q : Type q}
    (c : FixedAllContract U D Q) (X : U → Type w)
    (n : (i : U) → ((D × (X i → X i)) → (D × (X i → X i))) →
      (D × (X i → X i)) → (D × (X i → X i)))
    (f : D → D) (a : D) (result : Q)
    (body_assembly : ∀ i, c.decode result i = structuredObservation X n f a i)
    (i j : U) :
    structuredObservation X n f a i = structuredObservation X n f a j :=
  (body_assembly i).symm.trans
    ((fixed_result_constant c result i j).trans (body_assembly j))

/-- With a != b in the FIXED typed carrier B, typed K b gives the constant
update. Therefore zero at one structured instance and one at another cannot be
coordinates of one admitted n under the stated coherent family contract. -/
theorem no_zero_one_assembly {U : Type u} {D : Type v} {Q : Type q}
    (c : FixedAllContract U D Q) (X : U → Type w)
    (n : (i : U) → ((D × (X i → X i)) → (D × (X i → X i))) →
      (D × (X i → X i)) → (D × (X i → X i)))
    (a b : D) (hne : a ≠ b) (i j : U)
    (zero_at : ∀ step seed, n i step seed = seed)
    (one_at : ∀ step seed, n j step seed = step seed) :
    ¬ ∃ result : Q, ∀ k,
      c.decode result k = structuredObservation X n (fun _ => b) a k := by
  rintro ⟨result, assembly⟩
  have h := observer_uniform c X n (fun _ => b) a result assembly i j
  have hi : structuredObservation X n (fun _ => b) a i = a := by
    simp only [structuredObservation, zero_at]
  have hj : structuredObservation X n (fun _ => b) a j = b := by
    simp only [structuredObservation, one_at]
  exact hne (hi.symm.trans (h.trans hj))

/-- A nontrivial local fixed-body family contract exists. This makes clear
that the rejection is of incompatible n/assembly choices, not of all models. -/
def constant_contract (U : Type u) (D : Type v) : FixedAllContract U D D where
  decode x _ := x
  reintroAt _ x := x
  assembly _ _ _ := rfl
  erased_cycle _ _ := rfl

/-- D=Bool can be used without requiring ANY nontrivial Raw carrier. This is
only a local set-control, not a finite model of the full source calculus. -/
def testX : Bool → Type
  | false => Unit
  | true => Bool

def varying (i : Bool) (step : (Bool × (testX i → testX i)) →
    (Bool × (testX i → testX i))) (seed : Bool × (testX i → testX i)) :=
  if i then step seed else seed

theorem collapsed_raw_does_not_remove_this_test :
    Subsingleton Unit ∧ ¬ ∃ result : Bool, ∀ i,
      (constant_contract Bool Bool).decode result i =
        structuredObservation testX varying (fun _ => true) false i := by
  refine ⟨inferInstance, ?_⟩
  exact no_zero_one_assembly (constant_contract Bool Bool) testX varying
    false true (by decide) false true (fun _ _ => rfl) (fun _ _ => rfl)

#print axioms fixed_result_constant
#print axioms observer_uniform
#print axioms no_zero_one_assembly
#print axioms collapsed_raw_does_not_remove_this_test
end TypedObserverFamilyContract
