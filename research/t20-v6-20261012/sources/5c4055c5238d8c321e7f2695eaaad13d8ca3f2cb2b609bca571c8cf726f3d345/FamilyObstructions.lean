import SourceControls
import Mathlib.Logic.Equiv.Defs

/- Ordinary set/family controls only. These are not a whole-HasE model.
The contracts are explicit; no law below is promoted to an axiom of HasE. -/
namespace TypeIndexedFamilyObstructions
universe u v w

def reabstract {U : Type u} {R : Type v} (r : U) (f : U → R) : U → R :=
  fun _ => f r

/-- Under ordinary family/projection semantics, coherence of the two literal
source routes in SourceControls forces this condition on admissible families. -/
theorem reabstract_coherent_iff {U : Type u} {R : Type v} (r : U) (f : U → R) :
    f = reabstract r f ↔ ∀ i, f i = f r := by
  constructor
  · intro h i
    exact congrFun h i
  · intro h
    funext i
    exact h i

/-- The unrestricted two-coordinate candidate fails the same-judgement control. -/
theorem full_constant_families_incoherent :
    ¬ (∀ f : Bool → Bool, f = reabstract false f) := by
  intro h
  have e := congrFun (h id) true
  have impossible : true = false := e
  cases impossible

/-- A restricted Henkin repair DOES survive this local coherence control.
It is only a constant-body fragment, not a claimed model of all constructors. -/
def ConstantFamilies (U : Type u) (R : Type v) (r : U) :=
  { f : U → R // ∀ i, f i = f r }

def constantFamiliesEquiv (U : Type u) (R : Type v) (r : U) :
    ConstantFamilies U R r ≃ R where
  toFun f := f.val r
  invFun a := ⟨fun _ => a, fun _ => rfl⟩
  left_inv f := by
    apply Subtype.ext
    funext i
    exact (f.property i).symm
  right_inv a := rfl

theorem constantFamilies_coherent {U : Type u} {R : Type v} (r : U)
    (f : ConstantFamilies U R r) : f.val = reabstract r f.val :=
  (reabstract_coherent_iff r f.val).mpr f.property

theorem constantFamilies_ext {U : Type u} {R : Type v} {r : U}
    (f g : ConstantFamilies U R r) (h : ∀ i, f.val i = g.val i) : f = g :=
  Subtype.ext (funext h)

theorem constantFamilies_nontrivial :
    (constantFamiliesEquiv Bool Bool false).symm true ≠
      (constantFamiliesEquiv Bool Bool false).symm false := by
  intro h
  have e := congrArg (constantFamiliesEquiv Bool Bool false) h
  have impossible : true = false := e
  cases impossible

/-- Set-level shape of the ACTUAL StructuredObserver source polynomial.
The operation n is supplied; this does not certify it at the full source N. -/
def structuredObservation {U : Type u} {R : Type v} (X : U → Type w)
    (n : (i : U) → ((R × (X i → X i)) → (R × (X i → X i))) →
      (R × (X i → X i)) → (R × (X i → X i)))
    (f : R → R) (a : R) (i : U) : R :=
  (n i (fun s => (f s.1, id)) (a, id)).1

/-- Explicit conditional semantic bridge: assembly must interpret the actual
source body by its displayed value. A coherent All Raw result then enforces
this restricted cross-instance equality, with no global Church claim. -/
theorem structured_observer_uniform
    {U : Type u} {R : Type v} (r : U) (X : U → Type w)
    (n : (i : U) → ((R × (X i → X i)) → (R × (X i → X i))) →
      (R × (X i → X i)) → (R × (X i → X i)))
    (f : R → R) (a : R) (result : ConstantFamilies U R r)
    (assembly : ∀ i, result.val i = structuredObservation X n f a i) :
    ∀ i j, structuredObservation X n f a i = structuredObservation X n f a j := by
  intro i j
  exact (assembly i).symm.trans
    ((result.property i).trans ((result.property j).symm.trans (assembly j)))

/-- The precise family that a self-indexed Henkin projection must omit. -/
def diagonal {D : Type u} {R : Type v} (ev : D → D → R) (flip : R → R) : D → R :=
  fun x => flip (ev x x)

theorem diagonal_not_in_image {D : Type u} {R : Type v}
    (ev : D → D → R) (flip : R → R) (noFixed : ∀ r, flip r ≠ r) :
    ∀ x, ev x ≠ diagonal ev flip := by
  intro x h
  exact noFixed (ev x x) (congrFun h x).symm

theorem self_projection_not_surjective {D : Type u} {R : Type v}
    (ev : D → D → R) (flip : R → R) (noFixed : ∀ r, flip r ≠ r) :
    ¬ Function.Surjective ev := by
  intro h
  obtain ⟨x, hx⟩ := h (diagonal ev flip)
  exact diagonal_not_in_image ev flip noFixed x hx

/-- Nontrivial classical sets admit the required fixed-point-free map. -/
theorem fixedPointFree_of_distinct {R : Type v} (a b : R) (hne : a ≠ b) :
    ∃ flip : R → R, ∀ x, flip x ≠ x := by
  classical
  refine ⟨fun x => if x = a then b else a, ?_⟩
  intro x
  by_cases h : x = a
  · simpa [h] using hne.symm
  · simpa [h] using (fun e : a = x => h e.symm)

/-- One impredicative formed discriminator code d suffices; no closure under
arbitrary type families, dependent Sigma, identity, or full-PER assumption. -/
theorem no_full_impredicative_product
    {U : Type u} (El : U → Type v) (d : U) {R : Type w}
    (a b : R) (hne : a ≠ b)
    (e : El d ≃ ((i : U) → El i → R)) : False := by
  classical
  obtain ⟨flip, noFixed⟩ := fixedPointFree_of_distinct a b hne
  let ev : El d → El d → R := fun x => e x d
  apply self_projection_not_surjective ev flip noFixed
  intro g
  let family : (i : U) → El i → R := fun i =>
    if h : i = d then fun x => g (cast (congrArg El h) x) else fun _ => a
  refine ⟨e.symm family, ?_⟩
  change e (e.symm family) d = g
  rw [e.apply_symm_apply]
  simp [family]

/-- Exact necessary restriction for EVERY set-sized Henkin representation of
this discriminator: self-instantiation cannot expose every set function. -/
theorem henkin_self_projection_proper
    {U : Type u} (El : U → Type v) (d : U) {R : Type w}
    (a b : R) (hne : a ≠ b)
    (decode : El d → (i : U) → El i → R) :
    ∃ g : El d → R, ∀ x, decode x d ≠ g := by
  obtain ⟨flip, noFixed⟩ := fixedPointFree_of_distinct a b hne
  exact ⟨diagonal (fun x => decode x d) flip,
    diagonal_not_in_image (fun x => decode x d) flip noFixed⟩

#print axioms reabstract_coherent_iff
#print axioms full_constant_families_incoherent
#print axioms constantFamilies_coherent
#print axioms constantFamilies_nontrivial
#print axioms structured_observer_uniform
#print axioms no_full_impredicative_product
#print axioms henkin_self_projection_proper
end TypeIndexedFamilyObstructions
