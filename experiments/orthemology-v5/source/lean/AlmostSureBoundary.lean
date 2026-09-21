/-
Logical core of the almost-sure intersection/atomicity criterion.
STATUS: authored source, NOT kernel-verified here.

Full is a predicate on events; atom records positive-mass points. The three
laws below are EXPLICIT theorem hypotheses. The mathematical document proves
their probability-measure interpretation and the weak-closure trilemma.
This Init-only file does NOT import Lebesgue measure, prove countability of the
atom set, or pretend to kernel-verify weak convergence or Kakutani.
-/
import Init

namespace OrthemologyV3
universe u

def CompleteFull {X : Type u} (Full : (X → Prop) → Prop) : Prop :=
  ∀ (I : Type u) (B : I → X → Prop),
    (∀ i, Full (B i)) → Full (fun x => ∀ i, B i x)

/-- Exact logical criterion. For probability, the hypotheses say that almost-
sure events are upward closed, contain every positive atom, and may exclude a
specified zero-mass singleton. No arbitrary intersection closure is assumed. -/
theorem completeFull_iff_full_atoms {X : Type u}
    (Full : (X → Prop) → Prop) (atom : X → Prop)
    (mono : ∀ P Q : X → Prop, (∀ x, P x → Q x) → Full P → Full Q)
    (positive_mem : ∀ P : X → Prop, Full P → ∀ x, atom x → P x)
    (null_complement : ∀ x, ¬ atom x → Full (fun y => y ≠ x)) :
    CompleteFull Full ↔ Full atom := by
  constructor
  · intro allFull
    let I := {x : X // ¬ atom x}
    have each : ∀ i : I, Full (fun y => y ≠ i.val) :=
      fun i => null_complement i.val i.property
    have combined := allFull I (fun i y => y ≠ i.val) each
    apply mono (fun y => ∀ i : I, y ≠ i.val) atom ?_ combined
    intro y hy
    apply Classical.byContradiction
    intro hn
    exact hy ⟨y,hn⟩ rfl
  · intro fullAtoms I B hB
    apply mono atom (fun x => ∀ i, B i x) ?_ fullAtoms
    intro x hx i
    exact positive_mem (B i) (hB i) x hx

/-- A uniform draw from a continuum is a probability instantiation of these
hypotheses: excluding EACH singleton almost surely is not excluding ALL points.
Measurability of singletons and the null-singleton fact are proved outside this
logical lemma; they are not fabricated as Lean axioms. -/
theorem no_atomless_full_intersection {X : Type u}
    (Full : (X → Prop) → Prop)
    (mono : ∀ P Q : X → Prop, (∀ x, P x → Q x) → Full P → Full Q)
    (noFalse : ¬ Full (fun _ => False))
    (omitPoint : ∀ x, Full (fun y => y ≠ x)) : ¬ CompleteFull Full := by
  intro h
  have all := h X (fun x y => y ≠ x) omitPoint
  apply noFalse
  exact mono (fun y => ∀ x, y ≠ x) (fun _ => False)
    (fun y hy => hy y rfl) all

/-- Support lifting always commutes with intersections for its declared carrier.
To identify this with probability-one membership one must separately show that
the law is concentrated on its positive atoms. -/
theorem support_lifting_intersection {T : Type u} (S : T → Prop)
    {I : Type u} (B : I → T → Prop) :
    (∀ t, S t → ∀ i, B i t) ↔ (∀ i t, S t → B i t) :=
  ⟨fun h i t ht => h t ht i, fun h t ht i => h i t ht⟩

end OrthemologyV3

#print axioms OrthemologyV3.completeFull_iff_full_atoms
#print axioms OrthemologyV3.no_atomless_full_intersection
#print axioms OrthemologyV3.support_lifting_intersection
