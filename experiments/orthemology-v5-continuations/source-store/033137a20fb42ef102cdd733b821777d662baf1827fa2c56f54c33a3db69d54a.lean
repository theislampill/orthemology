import UniformComputabilitySyntax

/-! Primitive-recursive constructors for the unchanged, explicitly coded Expr. -/
namespace P02.Codec.UniformComputability
open P02A2.ObserverCore

private theorem unary_ctor_primrec (tag : ℕ) (f : ℕ → Expr)
    (h : ∀ n, exprEncode (f n) = 10*n+tag) : Primrec f := by
  apply Primrec.encode_iff.mp
  apply (Primrec.nat_add.comp
    (Primrec.nat_mul.comp (Primrec.const 10) Primrec.id) (Primrec.const tag)).of_eq
  intro n
  simp [h]

private theorem binary_ctor_primrec (tag : ℕ) (f : Expr → Expr → Expr)
    (h : ∀ a b, exprEncode (f a b) = 10*Nat.pair (exprEncode a) (exprEncode b)+tag) :
    Primrec₂ f := by
  apply Primrec.encode_iff.mp
  have hp := Primrec₂.natPair.comp (Primrec.encode.comp (Primrec.fst : Primrec (@Prod.fst Expr Expr)))
    (Primrec.encode.comp Primrec.snd)
  apply (Primrec.nat_add.comp (Primrec.nat_mul.comp (Primrec.const 10) hp)
    (Primrec.const tag)).of_eq
  intro p
  simp [h]

theorem expr_constant_primrec : Primrec Expr.constant := by
  exact unary_ctor_primrec 0 _ (by intro n; simp [exprEncode])

theorem expr_reg_primrec : Primrec Expr.reg := by
  exact unary_ctor_primrec 1 _ (by intro n; rfl)

theorem expr_add_primrec : Primrec₂ Expr.add := binary_ctor_primrec 2 _ (fun _ _ => rfl)
theorem expr_sub_primrec : Primrec₂ Expr.sub := binary_ctor_primrec 3 _ (fun _ _ => rfl)
theorem expr_mul_primrec : Primrec₂ Expr.mul := binary_ctor_primrec 4 _ (fun _ _ => rfl)
theorem expr_div_primrec : Primrec₂ Expr.div := binary_ctor_primrec 5 _ (fun _ _ => rfl)
theorem expr_mod_primrec : Primrec₂ Expr.mod := binary_ctor_primrec 6 _ (fun _ _ => rfl)
theorem expr_le_primrec : Primrec₂ Expr.le := binary_ctor_primrec 7 _ (fun _ _ => rfl)
theorem expr_eq_primrec : Primrec₂ Expr.eq := binary_ctor_primrec 8 _ (fun _ _ => rfl)

theorem expr_pow2_primrec : Primrec Expr.pow2 := by
  apply Primrec.encode_iff.mp
  exact (Primrec.nat_add.comp
    (Primrec.nat_mul.comp (Primrec.const 10) Primrec.encode) (Primrec.const 9)).of_eq
    (fun _ => rfl)

#print axioms exprDenumerable
#print axioms readRegs_primrec
#print axioms evalRegs_primrec
#print axioms expr_add_primrec
#print axioms expr_pow2_primrec
end P02.Codec.UniformComputability
