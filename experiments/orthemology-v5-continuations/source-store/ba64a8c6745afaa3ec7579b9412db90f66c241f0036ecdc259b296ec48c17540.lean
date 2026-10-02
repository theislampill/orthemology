import UniformComputabilityMachine

/-! Explicit effective encodings of the unchanged LOOP expression syntax.
The bijection is mathematical syntax coding, separate from P02 byte serialization.
All naturals decode constructively; no arbitrary choice-based encoding is used. -/
namespace P02.Codec.UniformComputability
open P02A2.ObserverCore

def exprEncode : Expr → ℕ
  | .constant n => 10*n
  | .reg n => 10*n+1
  | .add a b => 10*Nat.pair (exprEncode a) (exprEncode b)+2
  | .sub a b => 10*Nat.pair (exprEncode a) (exprEncode b)+3
  | .mul a b => 10*Nat.pair (exprEncode a) (exprEncode b)+4
  | .div a b => 10*Nat.pair (exprEncode a) (exprEncode b)+5
  | .mod a b => 10*Nat.pair (exprEncode a) (exprEncode b)+6
  | .le a b => 10*Nat.pair (exprEncode a) (exprEncode b)+7
  | .eq a b => 10*Nat.pair (exprEncode a) (exprEncode b)+8
  | .pow2 a => 10*exprEncode a+9

def exprOfNat (n : ℕ) : Expr :=
  if h0 : n % 10 = 0 then .constant (n/10)
  else if h1 : n % 10 = 1 then .reg (n/10)
  else
    let p := n/10
    have hp : p < n := Nat.div_lt_self (by omega) (by omega)
    have hl : p.unpair.1 < n := lt_of_le_of_lt p.unpair_left_le hp
    have hr : p.unpair.2 < n := lt_of_le_of_lt p.unpair_right_le hp
    match n % 10 with
    | 2 => .add (exprOfNat p.unpair.1) (exprOfNat p.unpair.2)
    | 3 => .sub (exprOfNat p.unpair.1) (exprOfNat p.unpair.2)
    | 4 => .mul (exprOfNat p.unpair.1) (exprOfNat p.unpair.2)
    | 5 => .div (exprOfNat p.unpair.1) (exprOfNat p.unpair.2)
    | 6 => .mod (exprOfNat p.unpair.1) (exprOfNat p.unpair.2)
    | 7 => .le (exprOfNat p.unpair.1) (exprOfNat p.unpair.2)
    | 8 => .eq (exprOfNat p.unpair.1) (exprOfNat p.unpair.2)
    | _ => .pow2 (exprOfNat p)
termination_by n

@[simp] theorem exprOfNat_exprEncode (e : Expr) : exprOfNat (exprEncode e) = e := by
  induction e <;> rw [exprEncode, exprOfNat] <;> simp [Nat.mul_add_div, Nat.add_mul_div_left, *]

@[simp] theorem exprEncode_exprOfNat (n : ℕ) : exprEncode (exprOfNat n) = n := by
  induction n using Nat.strong_induction_on with
  | h n ih =>
      rw [exprOfNat]
      split_ifs with h0 h1
      · simp only [exprEncode]; omega
      · simp only [exprEncode]; omega
      · have hp : n/10 < n := Nat.div_lt_self (by omega) (by omega)
        have hl : (n/10).unpair.1 < n := lt_of_le_of_lt (n/10).unpair_left_le hp
        have hr : (n/10).unpair.2 < n := lt_of_le_of_lt (n/10).unpair_right_le hp
        have hm : n%10 < 10 := Nat.mod_lt _ (by omega)
        dsimp only
        generalize ht : n%10 = t at *
        interval_cases t <;> simp_all [exprEncode, Nat.pair_unpair]
        all_goals omega

instance exprDenumerable : Denumerable Expr :=
  Denumerable.mk' ⟨exprEncode, exprOfNat, exprOfNat_exprEncode, exprEncode_exprOfNat⟩

@[simp] theorem expr_encode_eq : Encodable.encode (α := Expr) = exprEncode := rfl
@[simp] theorem expr_ofNat_eq : Denumerable.ofNat Expr = exprOfNat := rfl

/-- This is the actual finite-store read function, uniformly primitive recursive. -/
theorem readRegs_primrec : Primrec₂ readRegs := by
  have h : Primrec₂ (fun (rs : RegFile) r => (rs.lookup r).getD 0) :=
    Primrec.option_getD.comp (Primrec.listLookup.comp Primrec.snd Primrec.fst) (Primrec.const 0)
  apply h.of_eq
  intro rs r
  induction rs with
  | nil => rfl
  | cons p rs ih =>
      rcases p with ⟨j,v⟩
      by_cases hj : r = j
      · subst j; simp [readRegs, List.lookup]
      · have hb : (r == j) = false := beq_eq_false_iff_ne.mpr hj
        simp [readRegs, List.lookup, hj, hb, ih]

end P02.Codec.UniformComputability

namespace P02.Codec.UniformComputability
open P02A2.ObserverCore

def exprTableValue (rs : RegFile) (table : List ℕ) : ℕ :=
  let n := table.length
  let tag := n%10
  let p := n/10
  let a := (table[p.unpair.1]?).getD 0
  let b := (table[p.unpair.2]?).getD 0
  if tag = 0 then p
  else if tag = 1 then readRegs rs p
  else if tag = 2 then a+b
  else if tag = 3 then a-b
  else if tag = 4 then a*b
  else if tag = 5 then a/b
  else if tag = 6 then a%b
  else if tag = 7 then if a ≤ b then 1 else 0
  else if tag = 8 then if a = b then 1 else 0
  else 2 ^ (table[p]?).getD 0

theorem exprTableValue_primrec : Primrec₂ exprTableValue := by
  have hn : Primrec (fun p : RegFile × List ℕ => p.2.length) :=
    Primrec.list_length.comp Primrec.snd
  have ht := Primrec.nat_mod.comp hn (Primrec.const 10)
  have hp := Primrec.nat_div.comp hn (Primrec.const 10)
  have hl := Primrec.fst.comp (Primrec.unpair.comp hp)
  have hr := Primrec.snd.comp (Primrec.unpair.comp hp)
  have ha := Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd hl) (Primrec.const 0)
  have hb := Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd hr) (Primrec.const 0)
  have hu := Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.snd hp) (Primrec.const 0)
  have hpow := (Primrec₂.unpaired'.mp Nat.Primrec.pow).comp (Primrec.const 2) hu
  exact Primrec.ite (Primrec.eq.comp ht (Primrec.const 0)) hp
    (Primrec.ite (Primrec.eq.comp ht (Primrec.const 1)) (readRegs_primrec.comp Primrec.fst hp)
      (Primrec.ite (Primrec.eq.comp ht (Primrec.const 2)) (Primrec.nat_add.comp ha hb)
        (Primrec.ite (Primrec.eq.comp ht (Primrec.const 3)) (Primrec.nat_sub.comp ha hb)
          (Primrec.ite (Primrec.eq.comp ht (Primrec.const 4)) (Primrec.nat_mul.comp ha hb)
            (Primrec.ite (Primrec.eq.comp ht (Primrec.const 5)) (Primrec.nat_div.comp ha hb)
              (Primrec.ite (Primrec.eq.comp ht (Primrec.const 6)) (Primrec.nat_mod.comp ha hb)
                (Primrec.ite (Primrec.eq.comp ht (Primrec.const 7))
                  (Primrec.ite (Primrec.nat_le.comp ha hb) (Primrec.const 1) (Primrec.const 0))
                  (Primrec.ite (Primrec.eq.comp ht (Primrec.const 8))
                    (Primrec.ite (Primrec.eq.comp ha hb) (Primrec.const 1) (Primrec.const 0))
                    hpow))))))))

theorem exprTableValue_table (rs : RegFile) (n : ℕ) :
    exprTableValue rs ((List.range n).map (fun k => evalRegs (exprOfNat k) rs)) =
      evalRegs (exprOfNat n) rs := by
  rw [exprOfNat]
  simp only [exprTableValue, List.length_map, List.length_range]
  by_cases h0 : n%10 = 0
  · simp [h0, evalRegs]
  by_cases h1 : n%10 = 1
  · simp [h0, h1, evalRegs]
  have hp : n/10 < n := Nat.div_lt_self (by omega) (by omega)
  have hl : (n/10).unpair.1 < n := lt_of_le_of_lt (n/10).unpair_left_le hp
  have hr : (n/10).unpair.2 < n := lt_of_le_of_lt (n/10).unpair_right_le hp
  simp only [h0, h1, ↓reduceIte, List.getElem?_map, List.getElem?_range hp,
    List.getElem?_range hl, List.getElem?_range hr, Option.map_some', Option.getD_some]
  have hm : n%10 < 10 := Nat.mod_lt _ (by omega)
  generalize ht : n%10 = t at *
  interval_cases t <;> simp_all [evalRegs]

/-- Uniform primitive recursion over the effective expression code; the
register contents and the expression both vary. This is not LOOP execution. -/
theorem evalRegs_primrec : Primrec₂ evalRegs := by
  have hs : Primrec₂ (fun rs n => evalRegs (exprOfNat n) rs) :=
    Primrec.nat_strong_rec _ (Primrec.option_some.comp exprTableValue_primrec).to₂
      (fun rs n => congrArg some (exprTableValue_table rs n))
  apply (hs.comp Primrec.snd (Primrec.encode.comp Primrec.fst)).of_eq
  intro p
  simp

end P02.Codec.UniformComputability
