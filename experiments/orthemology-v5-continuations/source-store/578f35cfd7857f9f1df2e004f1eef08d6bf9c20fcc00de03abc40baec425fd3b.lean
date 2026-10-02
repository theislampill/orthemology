import UniformStmtCodingProgram

namespace P02.Codec.UniformComputability
open P02A2.ObserverCore

def evaluatePackedFuel (fuel : ℕ) (p : PackedProgram) (n word : ℕ) : Option ℕ :=
  if p.arity = 2 then
    (runFuel fuel [.stmt p.body] (binaryRegs n word)).map (fun rs => readRegs rs p.output % 2)
  else some 0

theorem evaluatePackedFuel_primrec :
    Primrec (fun p : ℕ × PackedProgram × ℕ × ℕ =>
      evaluatePackedFuel p.1 p.2.1 p.2.2.1 p.2.2.2) := by
  have hfuel : Primrec (fun p : ℕ × PackedProgram × ℕ × ℕ => p.1) := Primrec.fst
  have hp : Primrec (fun p : ℕ × PackedProgram × ℕ × ℕ => p.2.1) :=
    Primrec.fst.comp Primrec.snd
  have hn : Primrec (fun p : ℕ × PackedProgram × ℕ × ℕ => p.2.2.1) :=
    Primrec.fst.comp (Primrec.snd.comp Primrec.snd)
  have hw : Primrec (fun p : ℕ × PackedProgram × ℕ × ℕ => p.2.2.2) :=
    Primrec.snd.comp (Primrec.snd.comp Primrec.snd)
  have hrun := runFuel_primrec.comp hfuel (Primrec.pair
    (Primrec.list_cons.comp (taskStmt_primrec.comp (packedBody_primrec.comp hp))
      (Primrec.const [])) (binaryRegs_primrec.comp hn hw))
  have hout := packedOutput_primrec.comp hp
  have hmap := Primrec.option_map hrun
    ((Primrec.nat_mod.comp (readRegs_primrec.comp Primrec.snd (hout.comp Primrec.fst))
      (Primrec.const 2)).to₂)
  exact Primrec.ite (Primrec.eq.comp (packedArity_primrec.comp hp) (Primrec.const 2))
    hmap (Primrec.const (some 0))

/-- The bounded evaluator's only remaining external dependency is the actual
byte parser. This theorem composes it with the already-proved exact machine. -/
theorem evaluateIndexFuel_primrec_of_decode (hd : Primrec decodeIndex) :
    Primrec₂ (fun (input : ℕ × ℕ × ℕ) fuel =>
      evaluateIndexFuel fuel input.1 input.2.1 input.2.2) := by
  have hinput : Primrec (fun p : (ℕ × ℕ × ℕ) × ℕ => p.1) := Primrec.fst
  have hidx := Primrec.fst.comp hinput
  have hn := Primrec.fst.comp (Primrec.snd.comp hinput)
  have hw := Primrec.snd.comp (Primrec.snd.comp hinput)
  have hsome : Primrec₂ (fun (x : (ℕ × ℕ × ℕ) × ℕ) (p : PackedProgram) =>
      evaluatePackedFuel x.2 p x.1.2.1 x.1.2.2) :=
    (evaluatePackedFuel_primrec.comp (Primrec.pair (Primrec.snd.comp Primrec.fst)
      (Primrec.pair Primrec.snd (Primrec.pair (hn.comp Primrec.fst) (hw.comp Primrec.fst))))).to₂
  apply (Primrec.option_casesOn (hd.comp hidx) (Primrec.const (some 0)) hsome).of_eq
  intro p
  simp only [evaluateIndexFuel]
  cases decodeIndex p.1.1 <;> rfl

theorem evaluateIndexFuel_computable_of_decode (hd : Computable decodeIndex) :
    Computable₂ (fun (input : ℕ × ℕ × ℕ) fuel =>
      evaluateIndexFuel fuel input.1 input.2.1 input.2.2) := by
  have hinput : Computable (fun p : (ℕ × ℕ × ℕ) × ℕ => p.1) := Computable.fst
  have hidx := Computable.fst.comp hinput
  have hn := Computable.fst.comp (Computable.snd.comp hinput)
  have hw := Computable.snd.comp (Computable.snd.comp hinput)
  have hsome : Computable₂ (fun (x : (ℕ × ℕ × ℕ) × ℕ) (p : PackedProgram) =>
      evaluatePackedFuel x.2 p x.1.2.1 x.1.2.2) :=
    (evaluatePackedFuel_primrec.to_comp.comp (Computable.pair (Computable.snd.comp Computable.fst)
      (Computable.pair Computable.snd
        (Computable.pair (hn.comp Computable.fst) (hw.comp Computable.fst))))).to₂
  apply (Computable.option_casesOn (hd.comp hidx) (Computable.const (some 0)) hsome).of_eq
  intro p
  simp only [evaluateIndexFuel]
  cases decodeIndex p.1.1 <;> rfl

end P02.Codec.UniformComputability
