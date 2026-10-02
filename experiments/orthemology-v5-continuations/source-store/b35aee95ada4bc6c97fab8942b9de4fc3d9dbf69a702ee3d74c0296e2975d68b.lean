import UniformStmtCodingStep

namespace P02.Codec.UniformComputability
open P02A2.ObserverCore

def packedEncode (p : PackedProgram) : ℕ :=
  Nat.pair p.arity (Nat.pair p.output (stmtEncode p.body))

def packedOfNat (n : ℕ) : PackedProgram :=
  ⟨n.unpair.1, n.unpair.2.unpair.1, stmtOfNat n.unpair.2.unpair.2⟩

@[simp] theorem packedOfNat_packedEncode (p : PackedProgram) : packedOfNat (packedEncode p) = p := by
  cases p
  simp [packedOfNat, packedEncode]

@[simp] theorem packedEncode_packedOfNat (n : ℕ) : packedEncode (packedOfNat n) = n := by
  simp [packedOfNat, packedEncode, Nat.pair_unpair]

instance packedDenumerable : Denumerable PackedProgram :=
  Denumerable.mk' ⟨packedEncode, packedOfNat, packedOfNat_packedEncode, packedEncode_packedOfNat⟩

@[simp] theorem packed_encode_eq : Encodable.encode (α := PackedProgram) = packedEncode := rfl
@[simp] theorem packed_ofNat_eq : Denumerable.ofNat PackedProgram = packedOfNat := rfl

theorem packedMk_primrec :
    Primrec (fun p : ℕ × ℕ × Stmt => PackedProgram.mk p.1 p.2.1 p.2.2) := by
  apply Primrec.encode_iff.mp
  change Primrec (fun p : ℕ × ℕ × Stmt => Nat.pair p.1 (Nat.pair p.2.1 (stmtEncode p.2.2)))
  exact Primrec₂.natPair.comp Primrec.fst (Primrec₂.natPair.comp
    (Primrec.fst.comp Primrec.snd) (Primrec.encode.comp (Primrec.snd.comp Primrec.snd)))

theorem packedArity_primrec : Primrec PackedProgram.arity := by
  apply (Primrec.fst.comp (Primrec.unpair.comp Primrec.encode)).of_eq
  intro p
  simp [packedEncode]

theorem packedOutput_primrec : Primrec PackedProgram.output := by
  apply (Primrec.fst.comp (Primrec.unpair.comp
    (Primrec.snd.comp (Primrec.unpair.comp Primrec.encode)))).of_eq
  intro p
  simp [packedEncode]

theorem packedBody_primrec : Primrec PackedProgram.body := by
  apply (stmtOfNat_primrec.comp (Primrec.snd.comp (Primrec.unpair.comp
    (Primrec.snd.comp (Primrec.unpair.comp Primrec.encode))))).of_eq
  intro p
  simp [packedEncode]

private def seqAccum (s : Stmt) (o : Option Stmt) : Option Stmt :=
  match o with
  | none => some s
  | some t => some (.seq s t)

private theorem seqAccum_primrec : Primrec₂ seqAccum := by
  apply (Primrec.option_casesOn Primrec.snd (Primrec.option_some.comp Primrec.fst)
    ((Primrec.option_some.comp
      (stmtSeq_primrec.comp (Primrec.fst.comp Primrec.fst) Primrec.snd)).to₂)).of_eq
  intro p
  cases p.2 <;> rfl

private theorem sequenceList_fold (ss : List Stmt) :
    sequenceList ss = (ss.foldr seqAccum none).getD .skip := by
  induction ss with
  | nil => rfl
  | cons s ss ih =>
      cases ss with
      | nil => rfl
      | cons t ts =>
          simp only [List.foldr_cons, seqAccum] at *
          cases h : ts.foldr seqAccum none <;>
            simp_all [sequenceList, seqAccum]

theorem sequenceList_primrec : Primrec sequenceList := by
  have hf : Primrec (fun ss : List Stmt => ss.foldr seqAccum none) :=
    Primrec.list_foldr Primrec.id (Primrec.const none)
      ((seqAccum_primrec.comp (Primrec.fst.comp Primrec.snd)
        (Primrec.snd.comp Primrec.snd)).to₂)
  exact (Primrec.option_getD.comp hf (Primrec.const Stmt.skip)).of_eq
    (fun ss => (sequenceList_fold ss).symm)

end P02.Codec.UniformComputability
