import PrefixObserver
import SelectorPrimrec

namespace OrthemologyTagged
open P02A2.SurvivorCandidates

variable {A : Type*} [Primcodable A]
variable (R : A → ℕ → ℕ → ℕ → Prop) [∀ a i, DecidableRel (R a i)]

/-- Joint primitive recursiveness of the actual finite-prefix family, for one
fixed jointly primitive-recursive matrix presentation. This is not a uniform
primitive-recursive evaluator of arbitrary program syntax. -/
theorem pi3PrefixValue_primrec
    (hR : PrimrecRel (fun p : (A × ℕ) × ℕ => R p.1.1 p.1.2 p.2)) :
    Primrec₂ (fun p : A × ℕ => pi3PrefixValue R p.1 p.2) := by
  let D := (A × ℕ) × ℕ
  have ha : Primrec (fun d : D => d.1.1) := Primrec.fst.comp Primrec.fst
  have hn : Primrec (fun d : D => d.1.2) := Primrec.snd.comp Primrec.fst
  have hb : Primrec (fun d : D => d.2) := Primrec.snd
  have hi := selector_primrec.comp hn hb
  have ht := Primrec.nat_sub.comp (Primrec.nat_sub.comp hn hi) (Primrec.const 1)
  have hrow : Primrec₂ (fun p : A × ℕ => innovation (R p.1 p.2)) :=
    P02A2.SurvivorPrimrec.innovation_primrec (fun p : A × ℕ => R p.1 p.2) hR
  have hflag := hrow.comp (ha.pair hi) ht
  have hbit := Primrec.nat_mod.comp hb (Primrec.const 2)
  exact (Primrec.ite (Primrec.nat_le.comp hn hi) hbit
    (Primrec.ite (Primrec.eq.comp hflag (Primrec.const true)) hbit (Primrec.const 0))).to₂

end OrthemologyTagged
#print axioms OrthemologyTagged.pi3PrefixValue_primrec
