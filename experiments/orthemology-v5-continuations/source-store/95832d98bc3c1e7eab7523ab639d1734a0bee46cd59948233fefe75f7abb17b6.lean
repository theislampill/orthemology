import Mathlib

/-!
# Compatibility and independent complete outcome control

Equality propagates on the bipartite graph of compossible completed choices.
This is a formal reconstruction of one control premise, not an ontology of wills.
No statement here licenses identifying a correct controller with a knowing mind.
-/

namespace Orthemology.Tranche3.CompleteControl

variable {A B X : Type*}

/-- Outcomes separately fixed by two completed choices must agree whenever
the choices can be co-instantiated with their efficacy preserved. -/
def CompatibleOutcomes (R : A → B → Prop) (u : A → X) (v : B → X) : Prop :=
  ∀ a b, R a b → u a = v b

/-- The undirected bipartite edge relation. -/
def Edge (R : A → B → Prop) : Sum A B → Sum A B → Prop
  | .inl a, .inr b => R a b
  | .inr b, .inl a => R a b
  | _, _ => False

def Label (u : A → X) (v : B → X) : Sum A B → X := Sum.elim u v

def Reachable (R : A → B → Prop) (s t : Sum A B) : Prop :=
  Relation.ReflTransGen (Edge R) s t

def Connected (R : A → B → Prop) : Prop :=
  ∀ s t, Reachable R s t

theorem equal_on_edge (R : A → B → Prop) (u : A → X) (v : B → X)
    (h : CompatibleOutcomes R u v) {s t : Sum A B} (edge : Edge R s t) :
    Label u v s = Label u v t := by
  cases s with
  | inl a =>
    cases t with
    | inl a' => exact False.elim edge
    | inr b => exact h a b edge
  | inr b =>
    cases t with
    | inl a => exact (h a b edge).symm
    | inr b' => exact False.elim edge

theorem equal_on_path (R : A → B → Prop) (u : A → X) (v : B → X)
    (h : CompatibleOutcomes R u v) {s t : Sum A B} (path : Reachable R s t) :
    Label u v s = Label u v t := by
  induction path with
  | refl => rfl
  | tail path edge ih => exact ih.trans (equal_on_edge R u v h edge)

/-- Connected admissibility is sufficient. Full Cartesian recombination is
not assumed in this theorem. -/
theorem connected_control_is_constant (R : A → B → Prop)
    (u : A → X) (v : B → X) (h : CompatibleOutcomes R u v)
    (connected : Connected R) :
    ∀ s t, Label u v s = Label u v t := by
  intro s t
  exact equal_on_path R u v h (connected s t)

theorem nonconstant_requires_disconnected (R : A → B → Prop)
    (u : A → X) (v : B → X) (h : CompatibleOutcomes R u v)
    (variation : ∃ s t, Label u v s ≠ Label u v t) : ¬ Connected R := by
  intro connected
  obtain ⟨s, t, hne⟩ := variation
  exact hne (connected_control_is_constant R u v h connected s t)

/-- The familiar product case, without invoking graph theory. -/
theorem rectangular_control_is_constant [Nonempty B]
    (u : A → X) (v : B → X)
    (h : ∀ a b, u a = v b) : ∀ a a', u a = u a' := by
  intro a a'
  obtain ⟨b⟩ := ‹Nonempty B›
  exact (h a b).trans (h a' b).symm

/-- Direct conflict version: two unpreventable and jointly executable choices
cannot guarantee disjoint outcomes. It does not claim that all individual
possibilities are jointly executable. -/
theorem no_conflicting_guarantees (R : A → B → Prop)
    (outcome : A → B → X) (p q : X → Prop) (a : A) (b : B)
    (joint : R a b)
    (left_guarantee : ∀ b', R a b' → p (outcome a b'))
    (right_guarantee : ∀ a', R a' b → q (outcome a' b))
    (incompatible : ∀ x, p x → q x → False) : False :=
  incompatible (outcome a b) (left_guarantee b joint) (right_guarantee a joint)

namespace Controls

/-- Necessarily agreeing but nonconstant binary maps are consistent on the
diagonal admissibility relation. The missing independence is exhibited,
not disguised as a countermodel to the stronger source role. -/
theorem diagonal_harmony :
    CompatibleOutcomes (fun a b : Bool => a = b) id id ∧
    (id false : Bool) ≠ id true := by
  constructor
  · intro a b h
    exact h
  · decide

theorem diagonal_is_disconnected :
    ¬ Connected (fun a b : Bool => a = b) := by
  apply nonconstant_requires_disconnected _ id id diagonal_harmony.1
  exact ⟨.inl false, .inl true, by decide⟩

/-- Both positive inputs suffice for true under OR, but neither input can
unilaterally guarantee false. This is a weaker power profile. -/
theorem or_is_only_one_sided :
    (∀ b : Bool, (true || b) = true) ∧
    (∀ a : Bool, (a || true) = true) ∧
    (¬ ∃ a : Bool, ∀ b : Bool, (a || b) = false) ∧
    (¬ ∃ b : Bool, ∀ a : Bool, (a || b) = false) := by
  decide

/-- Three edges on a two-by-two choice space already connect all choices;
the fourth product pair is not needed. -/
def threeEdge (a b : Bool) : Prop := a = false ∨ b = true

theorem three_edges_force_constancy (u v : Bool → X)
    (h : CompatibleOutcomes threeEdge u v) :
    u false = u true ∧ v false = v true := by
  have h00 := h false false (Or.inl rfl)
  have h01 := h false true (Or.inl rfl)
  have h11 := h true true (Or.inr rfl)
  exact ⟨h01.trans h11.symm, h00.symm.trans h01⟩

theorem three_edge_not_rectangular : ¬ threeEdge true false := by
  unfold threeEdge
  decide

end Controls

#print axioms equal_on_path
#print axioms connected_control_is_constant
#print axioms nonconstant_requires_disconnected
#print axioms rectangular_control_is_constant
#print axioms no_conflicting_guarantees
#print axioms Controls.diagonal_harmony
#print axioms Controls.diagonal_is_disconnected
#print axioms Controls.or_is_only_one_sided
#print axioms Controls.three_edges_force_constancy
#print axioms Controls.three_edge_not_rectangular

end Orthemology.Tranche3.CompleteControl
