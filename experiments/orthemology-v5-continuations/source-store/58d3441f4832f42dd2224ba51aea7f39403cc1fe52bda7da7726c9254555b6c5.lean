import CodecStmt
import Mathlib.Computability.Primrec

/-! The sealed sequential stream parser `readMany` is primitive recursive
uniformly in count, bytes, and any effectively supplied parser parameter.
The proof uses a strict forward accumulator and preserves `none` failures. -/
namespace P02.Codec.UniformComputability

variable {A B : Type} [Primcodable A] [Primcodable B]

/-- Accumulator carries reverse output and the exact unread suffix. -/
def readManyStep (read : A → List ℕ → Option (B × List ℕ)) (a : A)
    (state : Option (List B × List ℕ)) : Option (List B × List ℕ) :=
  state.bind (fun p => (read a p.2).map (fun q => (q.1::p.1,q.2)))

theorem readManyStep_primrec (read : A → List ℕ → Option (B × List ℕ))
    (hread : Primrec₂ read) : Primrec₂ (readManyStep read) := by
  exact Primrec.option_bind Primrec.snd
    ((Primrec.option_map
      (hread.comp (Primrec.fst.comp Primrec.fst) (Primrec.snd.comp Primrec.snd))
      ((Primrec.list_cons.comp (Primrec.fst.comp Primrec.snd)
          (Primrec.fst.comp (Primrec.snd.comp Primrec.fst))).pair
        (Primrec.snd.comp Primrec.snd)).to₂).to₂)

private theorem readManyStep_none (read : A → List ℕ → Option (B × List ℕ))
    (a : A) (n : ℕ) : (readManyStep read a)^[n] none = none := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [Function.iterate_succ_apply, readManyStep] using ih

/-- Exact invariant relating the forward implementation to original recursion. -/
theorem readManyStep_correct (read : A → List ℕ → Option (B × List ℕ))
    (a : A) (n : ℕ) (bs : List ℕ) (rev : List B) :
    (readManyStep read a)^[n] (some (rev,bs)) =
      (readMany (read a) n bs).map (fun p => (p.1.reverse ++ rev,p.2)) := by
  induction n generalizing bs rev with
  | zero => simp [readMany]
  | succ n ih =>
      rw [Function.iterate_succ_apply]
      cases h : read a bs with
      | none => simp [readManyStep, readMany, h, readManyStep_none]
      | some bRest =>
          rcases bRest with ⟨b,rest⟩
          simp only [readManyStep, Option.some_bind, h, Option.map_some']
          rw [ih]
          cases hr : readMany (read a) n rest with
          | none => simp [readMany, h, hr]
          | some outRest =>
              rcases outRest with ⟨out,last⟩
              simp [readMany, h, hr, List.reverse_cons, List.append_assoc]

/-- Generic uniform closure, on `(parameter,count,bytes)` using nested pairs. -/
theorem readMany_primrec (read : A → List ℕ → Option (B × List ℕ))
    (hread : Primrec₂ read) :
    Primrec (fun input : A × ℕ × List ℕ => readMany (read input.1) input.2.1 input.2.2) := by
  have hs : Primrec (fun input : A × ℕ × List ℕ =>
      (readManyStep read input.1)^[input.2.1] (some ([],input.2.2))) :=
    Primrec.nat_iterate (Primrec.fst.comp Primrec.snd)
      (Primrec.option_some.comp ((Primrec.const []).pair (Primrec.snd.comp Primrec.snd)))
      ((readManyStep_primrec read hread).comp (Primrec.fst.comp Primrec.fst) Primrec.snd).to₂
  have ho : Primrec (fun input : A × ℕ × List ℕ =>
      ((readManyStep read input.1)^[input.2.1] (some ([],input.2.2))).map
        (fun p => (p.1.reverse,p.2))) :=
    Primrec.option_map hs
      ((Primrec.list_reverse.comp (Primrec.fst.comp Primrec.snd)).pair
        (Primrec.snd.comp Primrec.snd)).to₂
  apply ho.of_eq
  intro input
  rw [readManyStep_correct]
  cases readMany (read input.1) input.2.1 input.2.2 <;> simp

#print axioms readManyStep_correct
#print axioms readMany_primrec
end P02.Codec.UniformComputability
