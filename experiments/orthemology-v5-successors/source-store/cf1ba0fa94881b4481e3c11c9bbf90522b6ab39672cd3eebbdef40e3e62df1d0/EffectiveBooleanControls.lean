import EffectivePrimitiveRecursion
namespace P01AC.BooleanControls
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC.EffectiveCompleteness P01AC.IdentityComplexity P01AC.BooleanIdentity P01AC.BooleanPrimitive

/-- First coordinate is the recursed count; second coordinate is the base. -/
def plus : PR 2 := .prec (.proj ⟨0, by decide⟩)
  (.comp .succ (fun _ => .proj ⟨1, by decide⟩))
example : plus.denote (inputs 4 3) = 7 := rfl

/-- This control uses both distinct recursion coordinates: h(k,a,e)=k+a. -/
def trianglePlus : PR 2 := .prec (.proj ⟨0, by decide⟩)
  (.comp plus (fun i => .proj ⟨i.val, by omega⟩))
example : trianglePlus.denote (inputs 4 3) = 9 := rfl
example : Has (NatCtx 2) trianglePlus.compile N := trianglePlus.compile_has
example (η : Env) (v : Nat → Nat) (hv : EnvNat 2 η v) :
    NatObs (eval trianglePlus.compile η) (trianglePlus.denote v) :=
  trianglePlus.compile_obs η v hv

def firstInput : PR 2 := .proj ⟨0, by decide⟩

theorem always_zero_valid (e : Nat) : BoolValid (simFamily (.zero 2) e) constantChoice :=
  (sim_valid_iff_all_zero _ e).mpr (fun _ => rfl)

theorem first_input_invalid (e : Nat) : ¬ BoolValid (simFamily firstInput e) constantChoice := by
  intro h
  have bad := (sim_valid_iff_all_zero firstInput e).mp h 1
  cases bad

theorem explicit_mismatch (e : Nat) : Mismatch (simFamily firstInput e) constantChoice := by
  refine ⟨1, true, false, by decide, ?_, constantChoice_obs 1⟩
  exact simFamily_obs firstInput e 1

/-- Zero-arity composition genuinely has no input obligations. -/
def zeroArityComposition : PR 0 := .comp (.zero 0) (fun i => nomatch i)
example : zeroArityComposition.denote (fun _ => 97) = 0 := rfl
example : Has [] zeroArityComposition.compile N := zeroArityComposition.compile_has
example (η : Env) : NatObs (eval zeroArityComposition.compile η) 0 :=
  zeroArityComposition.compile_obs η (fun _ => 97) (fun i hi => False.elim (Nat.not_lt_zero i hi))

/-- Parameter-sensitive recurrence: value(0,x,y)=x and value(k+1,x,y)=y.
    h's index three must be original y, rather than the n binder or value. -/
def parameterOverwrite : PR 3 := .prec (.proj ⟨0, by decide⟩) (.proj ⟨3, by decide⟩)
example : parameterOverwrite.denote (P01F.cons 0 (P01F.cons 5 (P01F.cons 11 (fun _ => 43)))) = 5 := rfl
example : parameterOverwrite.denote (P01F.cons 4 (P01F.cons 5 (P01F.cons 11 (fun _ => 43)))) = 11 := rfl
example : Has (NatCtx 3) parameterOverwrite.compile N := parameterOverwrite.compile_has
example (η : Env) (v : Nat → Nat) (h : EnvNat 3 η v) :
    NatObs (eval parameterOverwrite.compile η) (parameterOverwrite.denote v) :=
  parameterOverwrite.compile_obs η v h


end P01AC.BooleanControls
