/- Complete authored Curry-System-F bridge for the exact canonical FiniteDerives.
   This is NEW attempt-0003 source, not recovered attempt-0002 code.
   UNCOMPILED at 4.19.0: no declaration, axiom or kernel credit. -/
import P01SystemF
import BoundaryResults
namespace P01F
open OrthemologyV2 OrthemologyV3

/-- Type translation is literal: the rigid bottom tag stays a rigid type atom. -/
def translateType (A : TypeCode) : Ty := A

def translate : Term → LTerm
  | .i => .lam (.var 0)
  | .k => .lam (.lam (.var 1))
  | .s => .lam (.lam (.lam
      (.app (.app (.var 2) (.var 0)) (.app (.var 1) (.var 0)))))
  | .zero => .zero
  | .one => .one
  | .app f a => .app (translate f) (translate a)

@[simp] theorem translate_ren (t : Term) (r : Nat → Nat) :
    ren r (translate t) = translate t := by
  induction t with
  | i => rfl
  | k => rfl
  | s => rfl
  | zero => rfl
  | one => rfl
  | app f a hf ha => simp only [translate, ren, hf, ha]

@[simp] theorem translate_sub (t : Term) (σ : Nat → LTerm) :
    sub σ (translate t) = translate t := by
  induction t with
  | i => rfl
  | k => rfl
  | s => rfl
  | zero => rfl
  | one => rfl
  | app f a hf ha => simp only [translate, sub, hf, ha]

/-- The nontrivial type-substitution square uses the *canonical* capture-avoiding
    source operation, not a new or semantic substitution. -/
theorem translate_type_substitution (A : TypeCode) (σ : Nat → TypeCode) :
    translateType (substitute σ A) = substitute (fun n => translateType (σ n))
      (translateType A) := rfl

theorem positive_left {t u} (h : BPositive t u) (a) :
    BPositive (.app t a) (.app u a) := by
  obtain ⟨v, hv, hr⟩ := h
  exact ⟨.app v a, .left hv a, bstar_left hr a⟩

theorem positive_right (f) {t u} (h : BPositive t u) :
    BPositive (.app f t) (.app f u) := by
  obtain ⟨v, hv, hr⟩ := h
  exact ⟨.app f v, .right f hv, bstar_right f hr⟩

theorem positive_to_star {t u} (h : BPositive t u) : BStar t u := by
  obtain ⟨v, hv, hr⟩ := h
  exact .tail hv hr

/-- One/two/three actual beta steps for I/K/S, not a reflexive simulation.
    The right-context case retains reduction inside discarded arguments. -/
theorem step_simulation {t u} (h : Step t u) :
    BPositive (translate t) (translate u) := by
  induction h with
  | i x =>
      refine ⟨translate x, ?_, .refl _⟩
      simpa [translate, inst, sub, single] using (Beta.root (.var 0) (translate x))
  | k x y =>
      refine ⟨.app (.lam (translate x)) (translate y), ?_, ?_⟩
      · apply Beta.left
        simpa [translate, inst, sub, single, up] using
          Beta.root (.lam (.var 1)) (translate x)
      · exact .tail (by simpa [inst] using (Beta.root (translate x) (translate y))) (.refl _)
  | s f g x =>
      let b : LTerm := .app (.app (translate f) (.var 0))
        (.app (.var 1) (.var 0))
      let c : LTerm := .app (.app (translate f) (.var 0))
        (.app (translate g) (.var 0))
      refine ⟨.app (.app (.lam (.lam b)) (translate g)) (translate x), ?_, ?_⟩
      · apply Beta.left
        apply Beta.left
        simpa [translate, b, inst, sub, single, up, ren, liftRen] using
          Beta.root (.lam (.lam (.app (.app (.var 2) (.var 0))
            (.app (.var 1) (.var 0))))) (translate f)
      · refine .tail (show Beta
          (.app (.app (.lam (.lam b)) (translate g)) (translate x))
          (.app (.lam c) (translate x)) from ?_) ?_
        · apply Beta.left
          simpa [b, c, inst, sub, single, up] using
            Beta.root (.lam b) (translate g)
        · exact .tail (by simpa [c, inst, sub, single, translate] using (Beta.root c (translate x))) (.refl _)
  | left h x ih => exact positive_left ih (translate x)
  | right f h ih => exact positive_right (translate f) ih

theorem reduction_simulation {t u} (h : Red t u) :
    BStar (translate t) (translate u) := by
  induction h with
  | refl => exact .refl _
  | tail h r ih => exact bstar_trans (positive_to_star (step_simulation h)) ih

/-- Preservation, emphatically NOT reflection, of raw source conversion. -/
theorem conversion_preservation {t u} (h : Conv t u) :
    BConv (translate t) (translate u) := by
  induction h with
  | refl => exact .refl _
  | step h => exact bstar_conv (positive_to_star (step_simulation h))
  | symm h ih => exact .symm ih
  | trans h k ih hk => exact .trans ih hk

/-- All seven actual finite-source typing constructors, including allI, allE
    and forward reduce. The source has no term-variable assumptions; therefore
    each translation is typable under EVERY target term context. -/
theorem typing_preservation {t A} (h : FiniteDerives t A) :
    ∀ Γ : Context, Has Γ (translate t) (translateType A) := by
  induction h with
  | i A => intro Γ; exact .lam (.var _ 0)
  | k A B => intro Γ; exact .lam (.lam (.var _ 1))
  | s A B C =>
      intro Γ
      exact .lam (.lam (.lam
        (.app (.app (.var _ 2) (.var _ 0)) (.app (.var _ 1) (.var _ 0)))))
  | app hf ha ihf iha => intro Γ; exact .app (ihf Γ) (iha Γ)
  | allI h ih => intro Γ; exact .allI (ih (shiftContext Γ))
  | allE h X ih => intro Γ; exact .allE (ih Γ) X
  | reduce h r ih => intro Γ; exact subject_reduction_star (ih Γ) (reduction_simulation r)

/-- The justified direction of the infinite-reduction argument. Accessibility
    reflects along *positive* simulations, including source context steps. -/
theorem target_SN_implies_source_SN (t : Term)
    (h : P01SNReflection.SN Beta (translate t)) :
    P01SNReflection.SN Step t :=
  P01SNReflection.positive_simulation_reflects_SN Step Beta translate
    (fun h => step_simulation h) h

/-- A chain-indexed version avoids silently counting an empty translation step.
    Each link of ANY source chain gives a positive target path. -/
theorem chain_simulation (ts : Nat → Term) (h : ∀ n, Step (ts n) (ts (n+1))) :
    ∀ n, BPositive (translate (ts n)) (translate (ts (n+1))) :=
  fun n => step_simulation (h n)

/-- Strong normalisation forbids a chain starting at t. This uses only Acc,
    and therefore does not assume target subject reduction or a target SN axiom. -/
theorem SN_no_chain {t : Term} (h : P01SNReflection.SN Step t) :
    ¬ ∃ ts : Nat → Term, ts 0 = t ∧ ∀ n, Step (ts n) (ts (n+1)) := by
  induction h with
  | intro t next ih =>
      rintro ⟨ts, e, hs⟩
      have s : Step t (ts 1) := by simpa only [e] using hs 0
      apply ih (ts 1) s
      exact ⟨fun n => ts (n+1), rfl, fun n => hs (n+1)⟩

end P01F
