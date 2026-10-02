import UniformVarintPrimrec
import UniformComputabilityExprConstructors

namespace P02.Codec.UniformComputability
open P02.Codec P02A2.ObserverCore

variable {A B C : Type} [Primcodable A] [Primcodable B] [Primcodable C]

def mapParser (read : A → List ℕ → Option (B × List ℕ)) (f : A → B → C)
    (a : A) (bs : List ℕ) : Option (C × List ℕ) := do
  let (b,rest) ← read a bs
  return (f a b,rest)

def bindParser (read : A → List ℕ → Option (B × List ℕ))
    (next : A × B → List ℕ → Option (C × List ℕ))
    (a : A) (bs : List ℕ) : Option (C × List ℕ) := do
  let (b,rest) ← read a bs
  next (a,b) rest

theorem mapParser_primrec (read : A → List ℕ → Option (B × List ℕ)) (f : A → B → C)
    (hr : Primrec₂ read) (hf : Primrec₂ f) : Primrec₂ (mapParser read f) := by
  have hg : Primrec₂ (fun (input : A × List ℕ) (p : B × List ℕ) => (f input.1 p.1,p.2)) :=
    ((hf.comp (Primrec.fst.comp Primrec.fst) (Primrec.fst.comp Primrec.snd)).pair (Primrec.snd.comp Primrec.snd)).to₂
  apply (Primrec.option_map hr hg).to₂.of_eq
  intro a bs
  unfold mapParser
  cases read a bs <;> rfl

theorem bindParser_primrec (read : A → List ℕ → Option (B × List ℕ))
    (next : A × B → List ℕ → Option (C × List ℕ))
    (hr : Primrec₂ read) (hn : Primrec₂ next) : Primrec₂ (bindParser read next) := by
  have hg : Primrec₂ (fun (input : A × List ℕ) (p : B × List ℕ) => next (input.1,p.1) p.2) :=
    (hn.comp ((Primrec.fst.comp Primrec.fst).pair (Primrec.fst.comp Primrec.snd))
      (Primrec.snd.comp Primrec.snd)).to₂
  exact (Primrec.option_bind hr hg).to₂

theorem readBinary_primrec (read : A → List ℕ → Option (Expr × List ℕ))
    (op : Expr → Expr → Expr) (hr : Primrec₂ read) (hop : Primrec₂ op) :
    Primrec₂ (fun a bs => readBinary (read a) op bs) := by
  have hr' : Primrec₂ (fun (p : A × Expr) bs => read p.1 bs) :=
    (hr.comp (Primrec.fst.comp Primrec.fst) Primrec.snd).to₂
  have hf : Primrec₂ (fun (p : A × Expr) b => op p.2 b) :=
    (hop.comp (Primrec.snd.comp Primrec.fst) Primrec.snd).to₂
  exact bindParser_primrec read _ hr (mapParser_primrec _ _ hr' hf)

/-- List drop is implemented by a bounded iterate of the actual tail function. -/
theorem list_drop_primrec {α : Type} [Primcodable α] : Primrec₂ (@List.drop α) := by
  have h : Primrec (fun p : ℕ × List α => List.tail^[p.1] p.2) :=
    Primrec.nat_iterate Primrec.fst Primrec.snd ((Primrec.list_tail.comp Primrec.snd).to₂)
  apply h.to₂.of_eq
  intro n bs
  induction n with
  | zero => rfl
  | succ n ih => rw [Function.iterate_succ_apply', ih, List.tail_drop]

theorem list_replicate_primrec {α : Type} [Primcodable α] : Primrec₂ (@List.replicate α) := by
  have h : Primrec₂ (fun (a : α) (n : ℕ) => n.rec (motive := fun _ => List α) [] (fun _ xs => a::xs)) :=
    Primrec.nat_rec (Primrec.const [])
      ((Primrec.list_cons.comp Primrec.fst (Primrec.snd.comp Primrec.snd)).to₂)
  apply h.swap.of_eq
  intro n a
  induction n with
  | zero => rfl
  | succ n ih => simpa [List.replicate_succ, ih]

end P02.Codec.UniformComputability
