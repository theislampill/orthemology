import UniformComputabilityStmtParser

namespace P02.Codec.UniformComputability
open P02.Codec P02A2.ObserverCore

/-- Exact one-layer statement parser closure, parameterized by the lower-fuel
statement parser and expression fuel. All four actual statement tags occur. -/
theorem stmtLayer_primrec {A : Type} [Primcodable A]
    (read : A → List ℕ → StmtResult) (hr : Primrec₂ read)
    (fuel : A → ℕ) (hf : Primrec fuel) (he : Primrec₂ readExpr) :
    Primrec₂ (fun a bs => stmtLayer (fuel a) (read a) bs) := by
  have huv : Primrec₂ (fun (_ : A) bs => uvRead bs) :=
    (uvRead_primrec.comp Primrec.snd).to₂
  have hexpr : Primrec₂ (fun a bs => readExpr (fuel a) bs) :=
    (he.comp (hf.comp Primrec.fst) Primrec.snd).to₂
  have hexprR : Primrec₂ (fun (p : A × ℕ) bs => readExpr (fuel p.1) bs) :=
    (hexpr.comp (Primrec.fst.comp Primrec.fst) Primrec.snd).to₂
  have hsetMap : Primrec₂ (fun (p : A × ℕ) e => Stmt.set p.2 e) :=
    (stmtSet_primrec.comp (Primrec.snd.comp Primrec.fst) Primrec.snd).to₂
  have hset := bindParser_primrec (fun (_ : A) bs => uvRead bs) _ huv
    (mapParser_primrec _ _ hexprR hsetMap)
  have hmany : Primrec₂ (fun (p : A × ℕ) bs => readMany (read p.1) p.2 bs) :=
    ((readMany_primrec read hr).comp ((Primrec.fst.comp Primrec.fst).pair
      ((Primrec.snd.comp Primrec.fst).pair Primrec.snd))).to₂
  have hseq := bindParser_primrec (fun (_ : A) bs => uvRead bs) _ huv
    (mapParser_primrec _ (fun (_ : A × ℕ) ss => sequenceList ss) hmany
      ((sequenceList_primrec.comp Primrec.snd).to₂))
  have hreadRE : Primrec₂ (fun (p : (A × ℕ) × Expr) bs => read p.1.1 bs) :=
    (hr.comp (Primrec.fst.comp (Primrec.fst.comp Primrec.fst)) Primrec.snd).to₂
  have hloopMap : Primrec₂ (fun (p : (A × ℕ) × Expr) s => Stmt.loop p.1.2 p.2 s) :=
    (stmtLoop_primrec.comp ((Primrec.snd.comp (Primrec.fst.comp Primrec.fst)).pair
      ((Primrec.snd.comp Primrec.fst).pair Primrec.snd))).to₂
  have hloop := bindParser_primrec (fun (_ : A) bs => uvRead bs) _ huv
    (bindParser_primrec _ _ hexprR (mapParser_primrec _ _ hreadRE hloopMap))
  have hreadE : Primrec₂ (fun (p : A × Expr) bs => read p.1 bs) :=
    (hr.comp (Primrec.fst.comp Primrec.fst) Primrec.snd).to₂
  have hreadES : Primrec₂ (fun (p : (A × Expr) × Stmt) bs => read p.1.1 bs) :=
    (hr.comp (Primrec.fst.comp (Primrec.fst.comp Primrec.fst)) Primrec.snd).to₂
  have hbranchMap : Primrec₂ (fun (p : (A × Expr) × Stmt) t => Stmt.branch p.1.2 p.2 t) :=
    (stmtBranch_primrec.comp ((Primrec.snd.comp (Primrec.fst.comp Primrec.fst)).pair
      ((Primrec.snd.comp Primrec.fst).pair Primrec.snd))).to₂
  have hbranch := bindParser_primrec _ _ hexpr
    (bindParser_primrec _ _ hreadE (mapParser_primrec _ _ hreadES hbranchMap))
  have hcons : Primrec₂ (fun (input : A × List ℕ) (p : ℕ × List ℕ) =>
      stmtLayer (fuel input.1) (read input.1) (p.1::p.2)) := by
    have ha : Primrec (fun p : (A × List ℕ) × ℕ × List ℕ => p.1.1) :=
      Primrec.fst.comp Primrec.fst
    have ht : Primrec (fun p : (A × List ℕ) × ℕ × List ℕ => p.2.1) :=
      Primrec.fst.comp Primrec.snd
    have hb : Primrec (fun p : (A × List ℕ) × ℕ × List ℕ => p.2.2) :=
      Primrec.snd.comp Primrec.snd
    exact Primrec.ite (Primrec.eq.comp ht (Primrec.const 16)) (hset.comp ha hb)
      (Primrec.ite (Primrec.eq.comp ht (Primrec.const 17)) (hseq.comp ha hb)
        (Primrec.ite (Primrec.eq.comp ht (Primrec.const 18)) (hloop.comp ha hb)
          (Primrec.ite (Primrec.eq.comp ht (Primrec.const 19)) (hbranch.comp ha hb)
            (Primrec.const none))))
  apply (Primrec.list_casesOn Primrec.snd (Primrec.const none) hcons).of_eq
  intro p
  cases p.2 <;> rfl

#print axioms stmtLayer_primrec
end P02.Codec.UniformComputability
