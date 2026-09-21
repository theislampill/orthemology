/-
Exact additional results for the inherited model.
STATUS: authored proof source; NOT kernel-verified in this runtime.
No novelty claim is attached to ordinary closure, realisability or quotient laws.
-/
import FiniteBridge

namespace OrthemologyV3
open OrthemologyV2

inductive Conv : Term → Term → Prop where
  | refl (t) : Conv t t
  | step {t u} : Step t u → Conv t u
  | symm {t u} : Conv t u → Conv u t
  | trans {t u v} : Conv t u → Conv u v → Conv t v

theorem Conv.left {t u} (h : Conv t u) (x : Term) :
    Conv (.app t x) (.app u x) := by
  induction h with
  | refl => exact .refl _
  | step h => exact .step (.left h x)
  | symm h ih => exact .symm ih
  | trans h k ih ik => exact .trans ih ik

theorem Conv.right (f : Term) {t u} (h : Conv t u) :
    Conv (.app f t) (.app f u) := by
  induction h with
  | refl => exact .refl _
  | step h => exact .step (.right f h)
  | symm h ih => exact .symm ih
  | trans h k ih ik => exact .trans ih ik

theorem code_conversion (A : Code) {t u} (h : Conv t u) :
    A.accepts t ↔ A.accepts u := by
  induction h with
  | refl => exact Iff.rfl
  | step h => exact A.stable h
  | symm h ih => exact ih.symm
  | trans h k ih ik => exact ih.trans ik

def principal (x : Term) : Code where
  accepts := fun t => Conv t x
  stable := fun h =>
    ⟨fun ht => .trans (.symm (.step h)) ht,
     fun hu => .trans (.step h) hu⟩

def unionCode (A B : Code) : Code where
  accepts := fun t => A.accepts t ∨ B.accepts t
  stable := fun h =>
    ⟨fun ht => ht.elim (fun ha => Or.inl ((A.stable h).mp ha))
                       (fun hb => Or.inr ((B.stable h).mp hb)),
     fun ht => ht.elim (fun ha => Or.inl ((A.stable h).mpr ha))
                       (fun hb => Or.inr ((B.stable h).mpr hb))⟩

theorem identity_characterisation (f : Term) :
    polyId.accepts f ↔ ∀ x, Conv (.app f x) x := by
  constructor
  · intro hf x
    exact hf (principal x) x (.refl x)
  · intro hf A x hx
    exact (code_conversion A (hf x)).mpr hx

theorem boolean_conservative {f : Term} (hf : polyBool.accepts f) (x y : Term) :
    Conv (.app (.app f x) y) x ∨ Conv (.app (.app f x) y) y :=
  hf (unionCode (principal x) (principal y)) x (Or.inl (.refl x))
    y (Or.inr (.refl y))

def MarkerFree : Term → Prop
  | .zero => False
  | .one => False
  | .app f x => MarkerFree f ∧ MarkerFree x
  | _ => True

def replaceMarkers (x y : Term) : Term → Term
  | .zero => x
  | .one => y
  | .app f a => .app (replaceMarkers x y f) (replaceMarkers x y a)
  | .i => .i
  | .k => .k
  | .s => .s

theorem replace_free {t : Term} (h : MarkerFree t) (x y : Term) :
    replaceMarkers x y t = t := by
  induction t with
  | i => rfl
  | k => rfl
  | s => rfl
  | zero => exact False.elim h
  | one => exact False.elim h
  | app f a ihf iha =>
      change Term.app (replaceMarkers x y f) (replaceMarkers x y a) = Term.app f a
      exact congr (congrArg Term.app (ihf h.1)) (iha h.2)

theorem step_replace {t u} (h : Step t u) (x y : Term) :
    Step (replaceMarkers x y t) (replaceMarkers x y u) := by
  induction h with
  | i a => exact .i _
  | k a b => exact .k _ _
  | s f g a => exact .s _ _ _
  | left h a ih => exact .left ih _
  | right f h ih => exact .right _ ih

theorem conv_replace {t u} (h : Conv t u) (x y : Term) :
    Conv (replaceMarkers x y t) (replaceMarkers x y u) := by
  induction h with
  | refl => exact .refl _
  | step h => exact .step (step_replace h x y)
  | symm h ih => exact .symm ih
  | trans h k ih ik => exact .trans ih ik

/-- Unary invariant sets plus fresh symbolic markers give a UNIFORM projection
choice, not a per-input choice. Equality is conversion after two arguments. -/
theorem boolean_projection {f : Term} (free : MarkerFree f)
    (hf : polyBool.accepts f) :
    (∀ x y, Conv (.app (.app f x) y) x) ∨
    (∀ x y, Conv (.app (.app f x) y) y) := by
  have h := boolean_conservative hf .zero .one
  cases h with
  | inl h =>
      left
      intro x y
      have hs := conv_replace h x y
      simpa only [replaceMarkers, replace_free free] using hs
  | inr h =>
      right
      intro x y
      have hs := conv_replace h x y
      simpa only [replaceMarkers, replace_free free] using hs

theorem boolean_projection_converse {f : Term}
    (h : (∀ x y, Conv (.app (.app f x) y) x) ∨
         (∀ x y, Conv (.app (.app f x) y) y)) : polyBool.accepts f := by
  intro A x hx y hy
  cases h with
  | inl h => exact (code_conversion A (h x y)).mpr hx
  | inr h => exact (code_conversion A (h x y)).mpr hy

theorem step_markerFree {t u} (h : Step t u) : MarkerFree t → MarkerFree u := by
  induction h with
  | i x => intro h; exact h.2
  | k x y => intro h; exact h.1.2
  | s f g x => intro h; exact ⟨⟨h.1.1.2,h.2⟩,⟨h.1.2,h.2⟩⟩
  | left h x ih => intro h; exact ⟨ih h.1,h.2⟩
  | right f h ih => intro h; exact ⟨h.1,ih h.2⟩

theorem red_markerFree {t u} (h : Red t u) : MarkerFree t → MarkerFree u := by
  induction h with
  | refl => exact fun h => h
  | tail h r ih => exact fun hf => ih (step_markerFree h hf)

theorem derives_markerFree {t A} (h : Derives t A) : MarkerFree t := by
  induction h with
  | i A => trivial
  | k A B => trivial
  | s A B C => trivial
  | app hf hx ihf ihx => exact ⟨ihf,ihx⟩
  | allIntro h ih => exact ih Code.top
  | allElim h A ih => exact ih
  | reduce h r ih => exact red_markerFree r ih

def discardedMarker : Term := .app (.app .k .i) .zero

theorem semantic_identity_with_marker : polyId.accepts discardedMarker :=
  (polyId.stable (.k .i .zero)).mpr identity.property

theorem marker_counterexample_not_derivable : ¬ Derives discardedMarker polyId := by
  intro h
  exact (derives_markerFree h).2

theorem marker_counterexample_not_finite : ¬ FiniteDerives discardedMarker identityCode := by
  intro h
  exact marker_counterexample_not_derivable
    (finite_translation h (fun _ => Code.top))

/-- A finite symbolic trace transports to all inputs. No semantic-type test is
used in this theorem; freshness and an actual reduction derivation are enough. -/
theorem red_replace {t u} (h : Red t u) (x y : Term) :
    Red (replaceMarkers x y t) (replaceMarkers x y u) := by
  induction h with
  | refl => exact .refl _
  | tail h r ih => exact .tail (step_replace h x y) ih

theorem certified_left_projection {f : Term} (free : MarkerFree f)
    (h : Red (.app (.app f .zero) .one) .zero) (x y : Term) :
    Red (.app (.app f x) y) x := by
  have hs := red_replace h x y
  simpa only [replaceMarkers, replace_free free] using hs

theorem certified_right_projection {f : Term} (free : MarkerFree f)
    (h : Red (.app (.app f .zero) .one) .one) (x y : Term) :
    Red (.app (.app f x) y) y := by
  have hs := red_replace h x y
  simpa only [replaceMarkers, replace_free free] using hs

/-- Fundamental obstruction to adding branching transitions as equations. -/
theorem branching_invariance_collapses {T : Type} (R : T → T → Prop)
    (choice : T → T → T)
    (left : ∀ x y, R (choice x y) x)
    (right : ∀ x y, R (choice x y) y)
    (P : T → Prop) (stable : ∀ {x y}, R x y → (P x ↔ P y))
    (x y : T) : P x ↔ P y :=
  (stable (left x y)).symm.trans (stable (right x y))

/-- The review's bare three-property trilemma is false: C=Unit, E(*)=Bool.
The singleton example does NOT satisfy a rich arrow-closed universe interface. -/
def singletonPack (f : Unit → Bool) : Bool := f ()
def singletonApp (b : Bool) (_ : Unit) : Bool := b

theorem singleton_full_beta (f : Unit → Bool) (u : Unit) :
    singletonApp (singletonPack f) u = f u := by cases u; rfl

/-- Correct erased-interface boundary; internal-code closure is not needed. -/
theorem no_erased_full_sections {C V R : Type} [DecidableEq C]
    (a b : C) (hab : a ≠ b) (v w : V) (hvw : v ≠ w)
    (read : R → V) (pack : (C → V) → R)
    (beta : ∀ f c, read (pack f) = f c) : False := by
  let f : C → V := fun c => if c = a then v else w
  have ha : read (pack f) = v := by simpa [f] using beta f a
  have hb : read (pack f) = w := by simpa [f, Ne.symm hab] using beta f b
  exact hvw (ha.symm.trans hb)

end OrthemologyV3

#print axioms OrthemologyV3.identity_characterisation
#print axioms OrthemologyV3.boolean_projection
#print axioms OrthemologyV3.boolean_projection_converse
#print axioms OrthemologyV3.marker_counterexample_not_finite
#print axioms OrthemologyV3.certified_left_projection
#print axioms OrthemologyV3.certified_right_projection
#print axioms OrthemologyV3.branching_invariance_collapses
#print axioms OrthemologyV3.singleton_full_beta
#print axioms OrthemologyV3.no_erased_full_sections
