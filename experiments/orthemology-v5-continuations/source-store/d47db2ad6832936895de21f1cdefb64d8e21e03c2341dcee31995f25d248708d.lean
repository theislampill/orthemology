import MembershipComputableCore

set_option maxHeartbeats 400000
namespace P02.Codec.UniformComputability
open P02A2.ObserverCore
attribute [local irreducible] Computable Primrec evaluateIndex outputList wordCount heavyCount

private def heavyGate (p : ℕ × ℕ × ℕ) : ℕ :=
  if p.1 ≤ p.2.1*p.2.2 then p.2.1 else 0

private theorem heavyGate_primrec : Primrec heavyGate :=
  Primrec.ite (Primrec.nat_le.comp Primrec.fst
    (Primrec.nat_mul.comp (Primrec.fst.comp Primrec.snd) (Primrec.snd.comp Primrec.snd)))
    (Primrec.fst.comp Primrec.snd) (Primrec.const 0)

/-- Uniform effective integer numerator for the actual heavy-cylinder mass. -/
theorem heavyCount_computable :
    Computable (fun p : ℕ × ℕ × ℕ => heavyCount p.1 p.2.1 p.2.2) := by
  unfold heavyCount
  have hwords : Computable (fun p : ℕ × ℕ × ℕ => allWords p.2.2) :=
    allWords_primrec.to_comp.comp (Computable.snd.comp Computable.snd)
  have he : Computable (fun p : (ℕ × ℕ × ℕ) × List Bool => p.1.1) :=
    Computable.fst.comp Computable.fst
  have hk : Computable (fun p : (ℕ × ℕ × ℕ) × List Bool => p.1.2.1) :=
    Computable.fst.comp (Computable.snd.comp Computable.fst)
  have hn : Computable (fun p : (ℕ × ℕ × ℕ) × List Bool => p.1.2.2) :=
    Computable.snd.comp (Computable.snd.comp Computable.fst)
  have hw : Computable (fun p : (ℕ × ℕ × ℕ) × List Bool => p.2) := Computable.snd
  have hci : Computable (fun p : (ℕ × ℕ × ℕ) × List Bool => (p.1.1,p.1.2.2,p.2)) :=
    he.pair (hn.pair hw)
  have hc : Computable (fun p : (ℕ × ℕ × ℕ) × List Bool => wordCount p.1.1 p.1.2.2 p.2) :=
    Computable.comp wordCount_computable hci
  have hprimPow : Primrec₂ (fun a b : ℕ => a^b) := Primrec₂.unpaired'.mp Nat.Primrec.pow
  have hcompPow : Computable₂ (fun a b : ℕ => a^b) := Primrec₂.to_comp hprimPow
  have hp2 : Computable (fun n : ℕ => 2^n) :=
    Computable₂.comp hcompPow (Computable.const 2) (Computable.id : Computable (@id ℕ))
  have hpowN : Computable (fun p : (ℕ × ℕ × ℕ) × List Bool => 2^p.1.2.2) := hp2.comp hn
  have hpowK : Computable (fun p : (ℕ × ℕ × ℕ) × List Bool => 2^p.1.2.1) := hp2.comp hk
  have hgi : Computable (fun p : (ℕ × ℕ × ℕ) × List Bool =>
      (2^p.1.2.2,wordCount p.1.1 p.1.2.2 p.2,2^p.1.2.1)) := hpowN.pair (hc.pair hpowK)
  have hgate : Computable (fun p : (ℕ × ℕ × ℕ) × List Bool =>
      heavyGate (2^p.1.2.2,wordCount p.1.1 p.1.2.2 p.2,2^p.1.2.1)) :=
    Computable.comp heavyGate_primrec.to_comp hgi
  have hvalue : Computable₂ (fun (p : ℕ × ℕ × ℕ) w =>
      if 2^p.2.2 ≤ wordCount p.1 p.2.2 w * 2^p.2.1 then wordCount p.1 p.2.2 w else 0) := hgate.to₂
  have hm : Computable (fun p : ℕ × ℕ × ℕ =>
      (allWords p.2.2).map (fun w =>
        if 2^p.2.2 ≤ wordCount p.1 p.2.2 w * 2^p.2.1 then wordCount p.1 p.2.2 w else 0)) :=
    computable_list_map ([] : List Bool)
      (fun p : ℕ × ℕ × ℕ => allWords p.2.2)
      (fun p w => if 2^p.2.2 ≤ wordCount p.1 p.2.2 w * 2^p.2.1 then wordCount p.1 p.2.2 w else 0)
      hwords hvalue
  exact membershipNatSum_primrec.to_comp.comp hm

/-- Plain natural-number endpoint with a fixed ordinary pairing convention. -/
theorem heavyCount_nat_computable : Computable (fun n : ℕ =>
    heavyCount n.unpair.1 n.unpair.2.unpair.1 n.unpair.2.unpair.2) :=
  Computable.comp heavyCount_computable ((Computable.fst.comp Computable.unpair).pair
    (Computable.unpair.comp (Computable.snd.comp Computable.unpair)))

#print axioms allWords_primrec
#print axioms sentinel_primrec
#print axioms outputList_computable
#print axioms wordCount_computable
#print axioms heavyCount_computable
#print axioms heavyCount_nat_computable
end P02.Codec.UniformComputability
