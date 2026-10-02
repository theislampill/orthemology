import MembershipWords

set_option maxHeartbeats 400000

/-! Actual uniform Mathlib Computable certificates for the list presentations
of finite observer tables. Evaluator-dependent functions are not claimed PR. -/
namespace P02.Codec.UniformComputability
open P02A2.ObserverCore

/-- Computable map on an initial segment; recursion accumulates its exact list. -/
theorem computable_range_map {A B : Type} [Primcodable A] [Primcodable B]
    (n : A → ℕ) (f : A → ℕ → B) (hn : Computable n) (hf : Computable₂ f) :
    Computable (fun a => (List.range (n a)).map (f a)) := by
  have hs : Computable₂ (fun a (p : ℕ × List B) => p.2 ++ [f a p.1]) :=
    (Computable.list_concat.comp (Computable.snd.comp Computable.snd)
      (hf.comp Computable.fst (Computable.fst.comp Computable.snd))).to₂
  apply (Computable.nat_rec hn (Computable.const []) hs).of_eq
  intro a
  induction n a with
  | zero => rfl
  | succ k ih => simp [List.range_succ, ih]

private theorem range_getD {B : Type} (bs : List B) (default : B) :
    (List.range bs.length).map (fun i => bs.getD i default) = bs := by
  apply List.ext_getElem (by simp)
  intro i hi hj
  simp only [List.getElem_map, List.getElem_range]
  exact List.getD_eq_getElem _ _ hj

/-- General list-map closure, using a harmless default only outside the range. -/
theorem computable_list_map {A B C : Type} [Primcodable A] [Primcodable B] [Primcodable C]
    (default : B) (xs : A → List B) (f : A → B → C)
    (hxs : Computable xs) (hf : Computable₂ f) :
    Computable (fun a => (xs a).map (f a)) := by
  have hget : Computable₂ (fun a i => (xs a).getD i default) :=
    ((Primrec.list_getD default).to_comp.comp (hxs.comp Computable.fst) Computable.snd).to₂
  have hm := computable_range_map (fun a => (xs a).length)
    (fun a i => f a ((xs a).getD i default)) (Computable.list_length.comp hxs)
    (hf.comp₂ Computable.fst hget)
  apply hm.of_eq
  intro a
  simpa only [List.map_map, Function.comp_def] using
    congrArg (List.map (f a)) (range_getD (xs a) default)

/-- Primitive-recursive enumeration of all fixed-length Boolean words. -/
theorem allWords_primrec : Primrec allWords := by
  have hm (b : Bool) : Primrec (fun ws : List (List Bool) => ws.map (b::·)) :=
    Primrec.list_map Primrec.id ((Primrec.list_cons.comp (Primrec.const b) Primrec.snd).to₂)
  have hs : Primrec₂ (fun (_ : ℕ) (ws : List (List Bool)) =>
      ws.map (false::·) ++ ws.map (true::·)) :=
    (Primrec.list_append.comp ((hm false).comp Primrec.snd) ((hm true).comp Primrec.snd)).to₂
  apply (Primrec.nat_rec₁ ([[]] : List (List Bool)) hs).of_eq
  intro n
  induction n with
  | zero => rfl
  | succ n ih => simp [allWords, ih]

/-- Exact source-word sentinel coding. -/
theorem sentinel_primrec : Primrec sentinel := by
  have hbit : Primrec (fun p : List Bool × ℕ × Bool => if p.2.2 then 1 else 0) :=
    by
      apply (Primrec.cond (Primrec.snd.comp Primrec.snd) (Primrec.const 1) (Primrec.const 0)).of_eq
      intro p
      cases p.2.2 <;> rfl
  have hs : Primrec₂ (fun (_ : List Bool) (p : ℕ × Bool) => 2*p.1 + if p.2 then 1 else 0) :=
    (Primrec.nat_add.comp (Primrec.nat_mul.comp (Primrec.const 2)
      (Primrec.fst.comp Primrec.snd)) hbit).to₂
  exact Primrec.list_foldl Primrec.id (Primrec.const 1) hs

/-- Variable-length take, preserving the exact list function. -/
theorem list_take_primrec {B : Type} [Primcodable B] : Primrec₂ (@List.take B) := by
  have h : Primrec (fun p : ℕ × List B => (p.2.reverse.drop (p.2.length-p.1)).reverse) :=
    Primrec.list_reverse.comp
    (list_drop_primrec.comp
      (Primrec.nat_sub.comp (Primrec.list_length.comp Primrec.snd) Primrec.fst)
      (Primrec.list_reverse.comp Primrec.snd))
  apply h.to₂.of_eq
  intro n bs
  rw [← List.reverse_take, List.reverse_reverse]

end P02.Codec.UniformComputability

namespace P02.Codec.UniformComputability
open P02A2.ObserverCore

attribute [local irreducible] evaluateIndex outputList wordCount heavyCount

/-- Uniform evaluation of every output bit of the supplied source word. -/
theorem outputList_computable : Computable₂ outputList := by
  unfold outputList
  have hw : Computable (fun p : (ℕ × List Bool) × ℕ =>
      sentinel (p.1.2.take (p.2+1))) :=
    (sentinel_primrec.comp (list_take_primrec.comp (Primrec.succ.comp Primrec.snd)
      (Primrec.snd.comp Primrec.fst))).to_comp
  have hv : Computable (fun p : (ℕ × List Bool) × ℕ =>
      evaluateIndex p.1.1 p.2 (sentinel (p.1.2.take (p.2+1)))) :=
    evaluateIndex_computable.comp ((Computable.fst.comp Computable.fst).pair
      (Computable.snd.pair hw))
  have hbit : Computable₂ (fun (p : ℕ × List Bool) i =>
      decide (evaluateIndex p.1 i (sentinel (p.2.take (i+1))) % 2 = 1)) :=
    ((Primrec.eq : PrimrecRel (@Eq ℕ)).to_comp.comp
      (Primrec.nat_mod.to_comp.comp hv (Computable.const 2)) (Computable.const 1)).to₂
  exact computable_range_map (fun p : ℕ × List Bool => p.2.length) _
    (Computable.list_length.comp Computable.snd) hbit

#check outputList_computable

private theorem trueCount_primrec : Primrec (fun bs : List Bool => (bs.filter id).length) := by
  have hs : Primrec₂ (fun (_ : List Bool) (p : Bool × ℕ) => if p.1 then p.2+1 else p.2) := by
    apply (Primrec.cond (Primrec.fst.comp Primrec.snd)
      (Primrec.succ.comp (Primrec.snd.comp Primrec.snd)) (Primrec.snd.comp Primrec.snd)).of_eq
    rintro ⟨xs,b,n⟩
    cases b <;> rfl
  apply (Primrec.list_foldr Primrec.id (Primrec.const 0) hs).of_eq
  intro bs
  induction bs with
  | nil => rfl
  | cons b bs ih => cases b <;> simp_all [List.foldr_cons]

private theorem length_filter_map_id {B : Type} (xs : List B) (f : B → Bool) :
    ((xs.map f).filter id).length = (xs.filter f).length := by
  rw [← List.countP_eq_length_filter, ← List.countP_eq_length_filter, List.countP_map]
  rfl

/-- Exact fiber count over all N-bit source words, with variable program index. -/
theorem wordCount_computable :
    Computable (fun p : ℕ × ℕ × List Bool => wordCount p.1 p.2.1 p.2.2) := by
  unfold wordCount
  have hwords : Computable (fun p : ℕ × ℕ × List Bool => allWords p.2.1) :=
    allWords_primrec.to_comp.comp (Computable.fst.comp Computable.snd)
  have hpred : Computable₂ (fun (p : ℕ × ℕ × List Bool) v => decide (outputList p.1 v = p.2.2)) :=
    ((Primrec.eq : PrimrecRel (@Eq (List Bool))).to_comp.comp
      (outputList_computable.comp (Computable.fst.comp Computable.fst) Computable.snd)
      (Computable.snd.comp (Computable.snd.comp Computable.fst))).to₂
  have hm := computable_list_map ([] : List Bool) _ _ hwords hpred
  apply (trueCount_primrec.to_comp.comp hm).of_eq
  intro p
  exact length_filter_map_id _ _

#check wordCount_computable

theorem membershipNatSum_primrec : Primrec (List.sum : List ℕ → ℕ) := by
  have hs : Primrec₂ (fun (_ : List ℕ) (p : ℕ × ℕ) => p.1+p.2) :=
    (Primrec.nat_add.comp (Primrec.fst.comp Primrec.snd) (Primrec.snd.comp Primrec.snd)).to₂
  apply (Primrec.list_foldr Primrec.id (Primrec.const 0) hs).of_eq
  intro xs
  induction xs <;> simp_all


end P02.Codec.UniformComputability
