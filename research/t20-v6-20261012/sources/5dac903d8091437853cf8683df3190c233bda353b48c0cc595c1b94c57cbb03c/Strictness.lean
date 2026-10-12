/- Independent exact-TRS strictness check; not a whole-source model. -/
namespace HomogeneousPERAdversarial

inductive Term where
  | i | k | s | nu | a0 | a1
  | app : Term → Term → Term
  deriving DecidableEq
open Term
infixl:70 " @@ " => Term.app

inductive FunWHNF : Term → Prop
  | i : FunWHNF i
  | k : FunWHNF k
  | kApp (x) : FunWHNF (k @@ x)
  | s : FunWHNF s
  | sApp (x) : FunWHNF (s @@ x)
  | sApp2 (x y) : FunWHNF (s @@ x @@ y)
  | nu : FunWHNF nu
  | nuApp (x) : FunWHNF (nu @@ x)

inductive Value : Term → Prop
  | a0 : Value a0
  | a1 : Value a1
  | fn : FunWHNF x → Value x

/-- `nuFunction` is the disjoint union of exactly the eight first-order
    rules obtained by substituting the eight FunWHNF constructors. -/
inductive Step : Term → Term → Prop
  | i (x) : Step (i @@ x) x
  | k (x y) : Step (k @@ x @@ y) x
  | s (f g x) : Step (s @@ f @@ g @@ x) ((f @@ x) @@ (g @@ x))
  | nuAtom0 (f) : Step (nu @@ f @@ a0) a0
  | nuAtom1 (f) : Step (nu @@ f @@ a1) a1
  | nuFunction (f) : FunWHNF v → Step (nu @@ f @@ v) (f @@ v)
  | left : Step f g → Step (f @@ x) (g @@ x)
  | right : Step x y → Step (f @@ x) (f @@ y)

inductive Reduces : Term → Term → Prop
  | refl (t) : Reduces t t
  | tail : Step t u → Reduces u v → Reduces t v

def FunHead (t) := ∃ v, Reduces t v ∧ FunWHNF v

theorem funHead_now {t} (h : FunWHNF t) : FunHead t := ⟨t, .refl t, h⟩
theorem funHead_back {t u} (h : Step t u) : FunHead u → FunHead t := by
  rintro ⟨v, huv, hv⟩
  exact ⟨v, .tail h huv, hv⟩

theorem value_app_left {t a} (h : Value (t @@ a)) : FunWHNF t := by
  cases h with
  | fn h =>
      cases h with
      | kApp _ => exact .k
      | sApp _ => exact .s
      | sApp2 _ _ => exact .sApp _
      | nuApp _ => exact .nu

/-- Application can reach any atom/function WHNF only if its function
    part reaches a function WHNF. No confluence or standardisation premise. -/
theorem application_strictness {z v} (h : Reduces z v) (hv : Value v) :
    ∀ t a, z = t @@ a → FunHead t := by
  induction h with
  | refl z =>
      intro t a hz
      subst z
      exact funHead_now (value_app_left hv)
  | @tail z u v hs hr ih =>
      intro t a hz
      subst z
      cases hs with
      | i _ => exact funHead_now .i
      | k x y => exact funHead_now (.kApp _)
      | s f g x => exact funHead_now (.sApp2 _ _)
      | nuAtom0 f => exact funHead_now (.nuApp _)
      | nuAtom1 f => exact funHead_now (.nuApp _)
      | nuFunction f _ => exact funHead_now (.nuApp _)
      | left h => exact funHead_back h (ih hv _ _ rfl)
      | right h => exact ih hv _ _ rfl

/-- All eight function WHNFs retain their outer function shape under
    one compatible reduction. Reductions within arbitrary arguments are fine. -/
theorem function_whnf_step {t u} (ht : FunWHNF t) (h : Step t u) : FunWHNF u := by
  cases ht with
  | i => cases h
  | k => cases h
  | s => cases h
  | nu => cases h
  | kApp x =>
      cases h with
      | left h => cases h
      | right h => exact .kApp _
  | sApp x =>
      cases h with
      | left h => cases h
      | right h => exact .sApp _
  | sApp2 x y =>
      cases h with
      | left h =>
          cases h with
          | left h => cases h
          | right h => exact .sApp2 _ _
      | right h => exact .sApp2 _ _
  | nuApp x =>
      cases h with
      | left h => cases h
      | right h => exact .nuApp _

theorem value_step {t u} (ht : Value t) (h : Step t u) : Value u := by
  cases ht with
  | a0 => cases h
  | a1 => cases h
  | fn hf => exact .fn (function_whnf_step hf h)

theorem value_reduces {t u} (ht : Value t) (h : Reduces t u) : Value u := by
  induction h with
  | refl => exact ht
  | tail hs hr ih => exact ih (value_step ht hs)

/-- A Church-Rosser join for a term/application and a value is enough.
    This isolates exactly what the remaining confluence proof must deliver. -/
theorem application_join_strictness {t a v w}
    (happ : Reduces (t @@ a) w) (hval : Reduces v w) (hv : Value v) : FunHead t :=
  application_strictness happ (value_reduces hv hval) t a rfl

#print axioms application_strictness
#print axioms function_whnf_step
#print axioms application_join_strictness
end HomogeneousPERAdversarial
