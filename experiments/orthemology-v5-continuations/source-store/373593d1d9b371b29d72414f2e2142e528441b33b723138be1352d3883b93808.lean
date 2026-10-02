import UniformStmtParserPrimrec
import UniformStmtCodingEvaluation

/-! Effectivity of the exact sealed P02-L1 decoder on every numeric input.
The auxiliary internal syntax encodings do not change the wire representation.
All parser rejections, trailing-byte checks and arities are preserved. -/
set_option maxHeartbeats 2000000

namespace P02.Codec.UniformComputability
open P02.Codec P02A2.ObserverCore

theorem list_take_fixed_primrec {α : Type} [Primcodable α] (n : ℕ) : Primrec (@List.take α n) := by
  induction n with
  | zero => exact Primrec.const []
  | succ n ih =>
      have h := Primrec.list_casesOn (Primrec.id : Primrec (@id (List α))) (Primrec.const [])
        ((Primrec.list_cons.comp (Primrec.fst.comp Primrec.snd) (ih.comp (Primrec.snd.comp Primrec.snd))).to₂)
      apply h.of_eq
      intro bs
      cases bs <;> rfl

theorem stripMagic_primrec : Primrec stripMagic := by
  exact Primrec.ite (Primrec.eq.comp (list_take_fixed_primrec 5) (Primrec.const magic))
    (Primrec.option_some.comp (list_drop_primrec.comp (Primrec.const 5) Primrec.id)) (Primrec.const none)

def decodeBody (input : ℕ × ℕ × List ℕ) : Option PackedProgram := do
  let (body,rest) ← readStmt input.2.2.length input.2.2
  if rest = [] then some ⟨input.1,input.2.1,body⟩ else none

theorem decodeBody_primrec : Primrec decodeBody := by
  have hb : Primrec (fun input : ℕ × ℕ × List ℕ => input.2.2) := Primrec.snd.comp Primrec.snd
  have hp := readStmt_primrec.comp (Primrec.list_length.comp hb) hb
  have hc : Primrec₂ (fun (input : ℕ × ℕ × List ℕ) (p : Stmt × List ℕ) =>
      if p.2=[] then some (PackedProgram.mk input.1 input.2.1 p.1) else none) := by
    have ha : Primrec (fun d : (ℕ × ℕ × List ℕ) × (Stmt × List ℕ) => d.1.1) := Primrec.fst.comp Primrec.fst
    have ho : Primrec (fun d : (ℕ × ℕ × List ℕ) × (Stmt × List ℕ) => d.1.2.1) := Primrec.fst.comp (Primrec.snd.comp Primrec.fst)
    have hs : Primrec (fun d : (ℕ × ℕ × List ℕ) × (Stmt × List ℕ) => d.2.1) := Primrec.fst.comp Primrec.snd
    have hr : Primrec (fun d : (ℕ × ℕ × List ℕ) × (Stmt × List ℕ) => d.2.2) := Primrec.snd.comp Primrec.snd
    exact (Primrec.ite (Primrec.eq.comp hr (Primrec.const []))
      (Primrec.option_some.comp (packedMk_primrec.comp (ha.pair (ho.pair hs)))) (Primrec.const none)).to₂
  exact Primrec.option_bind hp hc

def decodeOutput (input : ℕ × List ℕ) : Option PackedProgram := do
  let (out,rest) ← uvRead input.2
  decodeBody (input.1,out,rest)

theorem decodeOutput_primrec : Primrec decodeOutput := by
  have hn : Primrec₂ (fun (input : ℕ × List ℕ) (p : ℕ × List ℕ) => decodeBody (input.1,p.1,p.2)) :=
    (decodeBody_primrec.comp ((Primrec.fst.comp Primrec.fst).pair Primrec.snd)).to₂
  exact Primrec.option_bind (uvRead_primrec.comp Primrec.snd) hn

def decodeFields (bs : List ℕ) : Option PackedProgram := do
  let p ← uvRead bs
  decodeOutput p

theorem decodeFields_primrec : Primrec decodeFields :=
  Primrec.option_bind uvRead_primrec (decodeOutput_primrec.comp Primrec.snd).to₂

/-- Exact byte parser, not restricted to the serializer image. -/
theorem decodeBytes_primrec : Primrec decodeBytes := by
  have h := Primrec.option_bind stripMagic_primrec (decodeFields_primrec.comp Primrec.snd).to₂
  exact h

/-- Exact numeric syntax decoder, including every invalid-code branch. -/
theorem decodeIndex_primrec : Primrec decodeIndex :=
  Primrec.option_bind decodeNumeric_primrec (decodeBytes_primrec.comp Primrec.snd).to₂

theorem decodeIndex_computable : Computable decodeIndex := decodeIndex_primrec.to_comp

/-- The exact bounded numeric evaluator's effectivity premise is discharged. -/
theorem evaluateIndexFuel_primrec :
    Primrec₂ (fun input : ℕ × ℕ × ℕ => fun fuel => evaluateIndexFuel fuel input.1 input.2.1 input.2.2) :=
  evaluateIndexFuel_primrec_of_decode decodeIndex_primrec

/-- Actual universal numeric evaluation is computable. No uniform primitive
recursiveness is asserted for this unbounded evaluation. -/
theorem evaluateIndex_computable :
    Computable (fun input : ℕ × ℕ × ℕ => evaluateIndex input.1 input.2.1 input.2.2) :=
  evaluateIndex_computable_of_fuel evaluateIndexFuel_primrec.to_comp

/-- An explicit external Nat-to-Nat endpoint, using ordinary Nat.unpair twice. -/
theorem evaluateIndex_nat_computable :
    Computable (fun code : ℕ => evaluateIndex code.unpair.1 code.unpair.2.unpair.1 code.unpair.2.unpair.2) := by
  have hp : Computable (fun code : ℕ => (code.unpair.1, code.unpair.2.unpair)) :=
    ((Primrec.fst.comp Primrec.unpair).pair
      (Primrec.unpair.comp (Primrec.snd.comp Primrec.unpair))).to_comp
  exact evaluateIndex_computable.comp hp

end P02.Codec.UniformComputability
