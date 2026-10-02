import SurvivorCandidates
import Mathlib.Computability.Primrec

/-! Uniform primitive-recursive bounded search for one fixed PR matrix family.
This does not posit a uniformly PR evaluator for all program syntax. -/
namespace P02A2.SurvivorPrimrec
open P02A2.SurvivorCandidates

section Bounded
variable {α : Type*} [Primcodable α]
variable (p : α → ℕ → Prop) [∀ a n, Decidable (p a n)]

def allBelow (a : α) (n : ℕ) : Bool :=
  n.rec true (fun i acc => acc && decide (p a i))

theorem allBelow_eq_decide (a : α) (n : ℕ) :
    allBelow p a n = decide (∀ i < n, p a i) := by
  induction n with
  | zero => simp [allBelow]
  | succ n ih =>
      simp only [allBelow, Nat.rec_add_one] at *
      rw [ih]
      simp [Nat.forall_lt_succ]

theorem allBelow_primrec (hp : PrimrecRel p) : Primrec₂ (allBelow p) := by
  have hg : Primrec₂ (fun (a : α) (v : ℕ × Bool) => v.2 && decide (p a v.1)) :=
    (Primrec.and.comp (Primrec.snd.comp Primrec.snd)
      (hp.comp Primrec.fst (Primrec.fst.comp Primrec.snd))).to₂
  exact Primrec.nat_rec (Primrec.const true) hg

theorem bounded_all_primrec (bound : α → ℕ) (hb : Primrec bound) (hp : PrimrecRel p) :
    PrimrecPred (fun a => ∀ i < bound a, p a i) := by
  exact ((allBelow_primrec p hp).comp Primrec.id hb).of_eq (fun a => allBelow_eq_decide p a _)
end Bounded

section Candidate
variable {α : Type*} [Primcodable α]
variable (R : α → ℕ → ℕ → Prop) [∀ a, DecidableRel (R a)]
variable (hR : PrimrecRel (fun p : α × ℕ => R p.1 p.2))

include hR in
theorem available_primrec : PrimrecRel (fun p : α × ℕ => available (R p.1) p.2) := by
  let D := (α × ℕ) × ℕ
  have he : Primrec (fun d : D => d.1.1) := Primrec.fst.comp Primrec.fst
  have hn : Primrec (fun d : D => d.1.2) := Primrec.snd.comp Primrec.fst
  have hs : Primrec (fun d : D => d.2) := Primrec.snd
  have hp : PrimrecRel (fun d : D => fun t => R d.1.1 d.2 t) :=
    hR.comp₂ ((he.pair hs).comp₂ Primrec₂.left) Primrec₂.right
  have hb := bounded_all_primrec (fun d : D => fun t => R d.1.1 d.2 t)
    (fun d => d.1.2+1) (Primrec.succ.comp hn) hp
  have ht : PrimrecPred (fun d : D => passes (R d.1.1) d.2 d.1.2) := by
    apply hb.of_eq
    intro d
    simp only [passes, Finset.mem_range]
  exact ((Primrec.nat_le.comp hs hn).and ht).or (Primrec.eq.comp hs (Primrec.succ.comp hn))

theorem candidate_graph (a : α) (n s : ℕ) :
    candidate (R a) n = s ↔ available (R a) n s ∧ ∀ j < s, ¬ available (R a) n j :=
  Nat.find_eq_iff _

include hR in
theorem candidate_primrec : Primrec₂ (fun a n => candidate (R a) n) := by
  apply Primrec.of_graph
  · exact ⟨fun p : α × ℕ => p.2+1, Primrec.succ.comp Primrec.snd,
      fun p => candidate_le_default (R p.1) p.2⟩
  · let D := (α × ℕ) × ℕ
    have hav := available_primrec R hR
    have hp : PrimrecRel (fun d : D => fun j => ¬ available (R d.1.1) d.1.2 j) :=
      PrimrecPred.not (PrimrecRel.comp₂ hav ((Primrec.fst : Primrec (fun d : D => d.1)).comp₂ Primrec₂.left) Primrec₂.right)
    have hm := bounded_all_primrec (fun d : D => fun j => ¬ available (R d.1.1) d.1.2 j)
      (fun d => d.2) Primrec.snd hp
    apply (PrimrecPred.and hav hm).of_eq
    intro d
    exact (candidate_graph R d.1.1 d.1.2 d.2).symm

include hR in
theorem previous_primrec : Primrec₂ (fun a n => previous (R a) n) := by
  have hc := candidate_primrec R hR
  exact Primrec.ite (Primrec.eq.comp Primrec.snd (Primrec.const 0)) (Primrec.const 0)
    (hc.comp Primrec.fst (Primrec.nat_sub.comp Primrec.snd (Primrec.const 1)))

include hR in
theorem innovation_primrec : Primrec₂ (fun a n => innovation (R a) n) :=
  (Primrec.eq.comp (candidate_primrec R hR) (previous_primrec R hR)).not

def prefixFunction (a : α) (n word : ℕ) : ℕ :=
  if innovation (R a) n then word % 2 else 0

include hR in
theorem prefixFunction_primrec :
    Primrec₂ (fun p : α × ℕ => prefixFunction R p.1 p.2) := by
  exact Primrec.ite
    (Primrec.eq.comp (Primrec.comp (innovation_primrec R hR) Primrec.fst) (Primrec.const true))
    (Primrec.nat_mod.comp Primrec.snd (Primrec.const 2)) (Primrec.const 0)

end Candidate
end P02A2.SurvivorPrimrec
