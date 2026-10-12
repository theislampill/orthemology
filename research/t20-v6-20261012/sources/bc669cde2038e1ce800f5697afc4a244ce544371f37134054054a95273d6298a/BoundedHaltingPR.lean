import EffectivePrimitiveRecursion
import Mathlib.Computability.Halting

/- A checked bridge from Mathlib's actual finite-arity primitive-recursion
   evidence to the retained P01AC compiler input syntax. -/
namespace P01AC.BooleanPrimitive

open List.Vector
open Denumerable Encodable

/-- Restrict an infinite environment to its first `r` entries. -/
def envVec (r : Nat) (v : Nat → Nat) : List.Vector Nat r :=
  List.Vector.ofFn (fun i => v i.val)

@[simp] theorem envVec_get (r : Nat) (v : Nat → Nat) (i : Fin r) :
    (envVec r v).get i = v i.val := by simp [envVec]

@[simp] theorem envVec_head (r : Nat) (v : Nat → Nat) :
    (envVec (r+1) v).head = v 0 := by rw [← List.Vector.get_zero]; exact envVec_get _ _ 0

@[simp] theorem envVec_tail (r : Nat) (v : Nat → Nat) :
    (envVec (r+1) v).tail = envVec r (fun i => v (i+1)) := by
  apply List.Vector.ext
  intro i
  simp [envVec, List.Vector.get_tail]

@[simp] theorem envVec_cons (r : Nat) (x : Nat) (v : Nat → Nat) :
    envVec (r+1) (P01F.cons x v) = x ::ᵥ envVec r v := by
  apply List.Vector.ext
  intro i
  refine Fin.cases ?_ (fun i => ?_) i <;> simp [envVec, P01F.cons]

/-- Existence is enough: this theorem never extracts data from `Prop` into `Type`.
    Both recursion constructors use the same counter/accumulator/parameter order. -/
theorem primrec'_represented {r : Nat} {f : List.Vector Nat r → Nat}
    (hf : Nat.Primrec' f) : ∃ p : PR r, ∀ v, p.denote v = f (envVec r v) := by
  induction hf with
  | zero => exact ⟨.zero 0, fun _ => rfl⟩
  | succ => exact ⟨.succ, fun v => by simp [PR.denote]⟩
  | get i => exact ⟨.proj i, fun v => by simp [PR.denote]⟩
  | @comp m n f gs hf hgs ihf ihgs =>
    classical
    obtain ⟨p, hp⟩ := ihf
    let ps : Fin n → PR m := fun i => Classical.choose (ihgs i)
    have hps : ∀ i v, (ps i).denote v = gs i (envVec m v) :=
      fun i => Classical.choose_spec (ihgs i)
    refine ⟨.comp p ps, fun v => ?_⟩
    rw [PR.denote, hp]
    congr 1
    apply List.Vector.ext
    intro i
    simp [envVec, hps, i.isLt]
  | @prec n f g hf hg ihf ihg =>
    obtain ⟨p, hp⟩ := ihf
    obtain ⟨q, hq⟩ := ihg
    refine ⟨.prec p q, fun v => ?_⟩
    simp only [PR.denote, envVec_head, envVec_tail]
    congr 1
    · exact hp _
    · funext k a
      rw [hq]
      simp only [envVec_cons]

/-- A natural-number indexed enumeration of actual Mathlib partial-recursive codes. -/
def machineCode (e : Nat) : Nat.Partrec.Code := ofNat Nat.Partrec.Code e

/-- The enumeration and inverse index map are primitive recursive. -/
theorem machineCode_prim : Primrec machineCode := Primrec.ofNat _

theorem machineCode_index_prim : Primrec (@encode Nat.Partrec.Code _) := Primrec.encode

@[simp] theorem machineCode_encode (c : Nat.Partrec.Code) : machineCode (encode c) = c :=
  Denumerable.ofNat_encode c

@[simp] theorem encode_machineCode (e : Nat) : encode (machineCode e) = e :=
  Denumerable.encode_ofNat e

theorem machineCode_surjective : Function.Surjective machineCode :=
  fun c => ⟨encode c, machineCode_encode c⟩

/-- Zero exactly when the bounded evaluator has not returned any result. -/
def boundedHaltBit (bound e : Nat) : Nat :=
  match Nat.Partrec.Code.evaln bound (machineCode e) 0 with
  | none => 0
  | some _ => 1

theorem boundedHaltBit_prim : Primrec₂ boundedHaltBit := by
  have hEval : Primrec (fun p : Nat × Nat =>
      Nat.Partrec.Code.evaln p.1 (machineCode p.2) 0) :=
    Nat.Partrec.Code.evaln_prim.comp
      ((Primrec.fst.pair ((Primrec.ofNat Nat.Partrec.Code).comp Primrec.snd)).pair
        (Primrec.const 0))
  change Primrec (fun p : Nat × Nat => boundedHaltBit p.1 p.2)
  refine (Primrec.option_casesOn hEval (Primrec.const 0) (Primrec.const 1).to₂).of_eq ?_
  intro p
  cases h : Nat.Partrec.Code.evaln p.1 (machineCode p.2) 0 <;> simp [boundedHaltBit, h]

/-- One fixed binary project PR program implements actual bounded halting. -/
theorem boundedHaltBit_represented :
    ∃ p : PR 2, ∀ v, p.denote v = boundedHaltBit (v 0) (v 1) := by
  obtain ⟨p, hp⟩ := primrec'_represented (Nat.Primrec'.prim_iff₂.mpr boundedHaltBit_prim)
  refine ⟨p, fun v => ?_⟩
  simpa only [envVec_head, envVec_tail] using hp v

@[simp] theorem boundedHaltBit_eq_zero (bound e : Nat) :
    boundedHaltBit bound e = 0 ↔ Nat.Partrec.Code.evaln bound (machineCode e) 0 = none := by
  simp [boundedHaltBit]
  cases Nat.Partrec.Code.evaln bound (machineCode e) 0 <;> simp

/-- All finite bounds fail exactly when the actual partial evaluator is undefined. -/
theorem all_bounds_zero_iff_nonhalting (e : Nat) :
    (∀ bound, boundedHaltBit bound e = 0) ↔
      ¬ (Nat.Partrec.Code.eval (machineCode e) 0).Dom := by
  rw [Part.dom_iff_mem]
  simp only [boundedHaltBit_eq_zero, Nat.Partrec.Code.evaln_complete]
  constructor
  · intro h ⟨x, bound, hx⟩
    simp [h bound] at hx
  · intro h bound
    cases he : Nat.Partrec.Code.evaln bound (machineCode e) 0 with
    | none => rfl
    | some x => exact False.elim (h ⟨x, bound, he⟩)

/-- The numerical index set of these actual nonhalting programs is not r.e.
    This is only the source computability obstruction, not a claim about P01AC derivability. -/
theorem machine_nonhalting_not_re :
    ¬ REPred (fun e : Nat => ¬ (Nat.Partrec.Code.eval (machineCode e) 0).Dom) := by
  intro h
  apply ComputablePred.halting_problem_not_re 0
  have hc : REPred (fun c : Nat.Partrec.Code =>
      ¬ (Nat.Partrec.Code.eval (machineCode (encode c)) 0).Dom) :=
    h.comp machineCode_index_prim.to_comp
  simpa only [machineCode_encode] using hc

/-- The requested combined machine bridge, without a surrogate halting predicate. -/
theorem exists_bounded_nonhalting_program :
    ∃ p : PR 2,
      (∀ bound e, p.denote (P01F.cons bound (P01F.cons e (fun _ => 0))) = 0 ↔
        Nat.Partrec.Code.evaln bound (machineCode e) 0 = none) ∧
      (∀ e, (∀ bound, p.denote (P01F.cons bound (P01F.cons e (fun _ => 0))) = 0) ↔
        ¬ (Nat.Partrec.Code.eval (machineCode e) 0).Dom) := by
  obtain ⟨p, hp⟩ := boundedHaltBit_represented
  refine ⟨p, ?_, ?_⟩
  · intro bound e
    simpa only [hp, P01F.cons] using boundedHaltBit_eq_zero bound e
  · intro e
    simpa only [hp, P01F.cons] using all_bounds_zero_iff_nonhalting e

#print axioms primrec'_represented
#print axioms exists_bounded_nonhalting_program
#print axioms machine_nonhalting_not_re
end P01AC.BooleanPrimitive
