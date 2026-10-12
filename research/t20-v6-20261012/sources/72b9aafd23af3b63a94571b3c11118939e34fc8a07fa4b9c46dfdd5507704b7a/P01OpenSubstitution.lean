/- P01 U09/U11 proposal. UNVERIFIED at Lean 4.19.0.
   A finite open-term helper; not a replacement for canonical Term.
   Constants are whole closed canonical Terms; there is no type-inspection.
   No lambda-abstraction congruence theorem is claimed (see U11 countermodel). -/
import InternalPolymorphism

namespace P01OpenSubstitution
open OrthemologyV2

inductive OpenTerm where
  | atom : Term → OpenTerm
  | var : Nat → OpenTerm
  | app : OpenTerm → OpenTerm → OpenTerm

def eval (rho : Nat → Term) : OpenTerm → Term
  | .atom t => t
  | .var n => rho n
  | .app f x => .app (eval rho f) (eval rho x)

def subst (sigma : Nat → OpenTerm) : OpenTerm → OpenTerm
  | .atom t => .atom t
  | .var n => sigma n
  | .app f x => .app (subst sigma f) (subst sigma x)

theorem eval_subst (t : OpenTerm) (sigma : Nat → OpenTerm) (rho : Nat → Term) :
    eval rho (subst sigma t) = eval (fun n => eval rho (sigma n)) t := by
  induction t with
  | atom t => rfl
  | var n => rfl
  | app f x ihf ihx =>
      simp only [subst, eval, ihf, ihx]

theorem subst_id (t : OpenTerm) : subst OpenTerm.var t = t := by
  induction t with
  | atom t => rfl
  | var n => rfl
  | app f x ihf ihx => simp only [subst, ihf, ihx]

theorem subst_comp (t : OpenTerm) (sigma tau : Nat → OpenTerm) :
    subst tau (subst sigma t) = subst (fun n => subst tau (sigma n)) t := by
  induction t with
  | atom t => rfl
  | var n => rfl
  | app f x ihf ihx => simp only [subst, ihf, ihx]

end P01OpenSubstitution
