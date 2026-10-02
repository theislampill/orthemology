import UniformExprParser
import UniformParserCombinators

namespace P02.Codec.UniformComputability
open P02.Codec P02A2.ObserverCore

/-- One exact expression-parser layer is uniformly primitive recursive in
an arbitrary primitive-recursive lower-fuel parser parameter. -/
theorem exprLayer_primrec {A : Type} [Primcodable A]
    (read : A → List ℕ → ExprResult) (hr : Primrec₂ read) :
    Primrec₂ (fun a bs => exprLayer (read a) bs) := by
  have huv : Primrec₂ (fun (_ : A) bs => uvRead bs) :=
    (uvRead_primrec.comp Primrec.snd).to₂
  have hc := mapParser_primrec (fun (_ : A) bs => uvRead bs) (fun _ n => Expr.constant n)
    huv ((expr_constant_primrec.comp Primrec.snd).to₂)
  have hv := mapParser_primrec (fun (_ : A) bs => uvRead bs) (fun _ n => Expr.reg n)
    huv ((expr_reg_primrec.comp Primrec.snd).to₂)
  have hp := mapParser_primrec read (fun _ e => Expr.pow2 e)
    hr ((expr_pow2_primrec.comp Primrec.snd).to₂)
  have hcons : Primrec₂ (fun (input : A × List ℕ) (p : ℕ × List ℕ) =>
      exprLayer (read input.1) (p.1::p.2)) := by
    have ha : Primrec (fun p : (A × List ℕ) × ℕ × List ℕ => p.1.1) :=
      Primrec.fst.comp Primrec.fst
    have ht : Primrec (fun p : (A × List ℕ) × ℕ × List ℕ => p.2.1) :=
      Primrec.fst.comp Primrec.snd
    have hb : Primrec (fun p : (A × List ℕ) × ℕ × List ℕ => p.2.2) :=
      Primrec.snd.comp Primrec.snd
    exact Primrec.ite (Primrec.eq.comp ht (Primrec.const 1)) (hc.comp ha hb)
      (Primrec.ite (Primrec.eq.comp ht (Primrec.const 2)) (hv.comp ha hb)
        (Primrec.ite (Primrec.eq.comp ht (Primrec.const 3))
          ((readBinary_primrec read Expr.add hr expr_add_primrec).comp ha hb)
          (Primrec.ite (Primrec.eq.comp ht (Primrec.const 4))
            ((readBinary_primrec read Expr.sub hr expr_sub_primrec).comp ha hb)
            (Primrec.ite (Primrec.eq.comp ht (Primrec.const 5))
              ((readBinary_primrec read Expr.mul hr expr_mul_primrec).comp ha hb)
              (Primrec.ite (Primrec.eq.comp ht (Primrec.const 6))
                ((readBinary_primrec read Expr.div hr expr_div_primrec).comp ha hb)
                (Primrec.ite (Primrec.eq.comp ht (Primrec.const 7))
                  ((readBinary_primrec read Expr.mod hr expr_mod_primrec).comp ha hb)
                  (Primrec.ite (Primrec.eq.comp ht (Primrec.const 8))
                    ((readBinary_primrec read Expr.le hr expr_le_primrec).comp ha hb)
                    (Primrec.ite (Primrec.eq.comp ht (Primrec.const 9))
                      ((readBinary_primrec read Expr.eq hr expr_eq_primrec).comp ha hb)
                      (Primrec.ite (Primrec.eq.comp ht (Primrec.const 10)) (hp.comp ha hb)
                        (Primrec.const none))))))))))
  apply (Primrec.list_casesOn Primrec.snd (Primrec.const none) hcons).of_eq
  intro p
  cases p.2 <;> rfl

#print axioms exprLayer_primrec
end P02.Codec.UniformComputability
