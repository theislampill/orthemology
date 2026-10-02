import UniformStmtCoding

/-! Effectivity of the exact existing explicit-stack transition. -/
namespace P02.Codec.UniformComputability
open P02A2.ObserverCore

/-- A code-based presentation of the existing transition, used only to prove
its primitive recursiveness. The equality theorem below identifies both. -/
def stepByCode (c : Config) : Config :=
  let code := taskEncode (c.1.head?.getD (.stmt .skip))
  let payload := code/2
  let ts := c.1.tail
  let rs := c.2
  if c.1 = [] then c
  else if code%2 = 0 then
    if payload = 0 then (ts, rs)
    else
      let tag := (payload-1)%4
      let p := ((payload-1)/4).unpair
      if tag = 0 then (ts, writeRegs rs p.1 (evalRegs (exprOfNat p.2) rs))
      else if tag = 1 then
        (.stmt (stmtOfNat p.1) :: .stmt (stmtOfNat p.2) :: ts, rs)
      else if tag = 2 then
        (.repeat p.1 0 (evalRegs (exprOfNat p.2.unpair.1) rs)
          (stmtOfNat p.2.unpair.2) :: ts, rs)
      else
        (.stmt (if evalRegs (exprOfNat p.1) rs = 0 then stmtOfNat p.2.unpair.2
          else stmtOfNat p.2.unpair.1) :: ts, rs)
  else
    let p := payload.unpair
    let r := p.1
    let k := p.2.unpair.1
    let n := p.2.unpair.2.unpair.1
    let s := stmtOfNat p.2.unpair.2.unpair.2
    if n = 0 then (ts, rs)
    else (.stmt s :: .repeat r (k+1) (n-1) s :: ts, writeRegs rs r k)

theorem stepByCode_eq_step (c : Config) : stepByCode c = step c := by
  rcases c with ⟨ts,rs⟩
  cases ts with
  | nil => rfl
  | cons t ts =>
      cases t with
      | stmt s =>
          cases s <;>
            simp [stepByCode, step, taskEncode, stmtEncode, Nat.mul_add_div,
              Nat.add_mul_div_left]
      | «repeat» r k n s =>
          cases n <;>
            simp [stepByCode, step, taskEncode, Nat.mul_add_div, Nat.add_mul_div_left]

theorem writeRegs_primrec :
    Primrec (fun p : RegFile × ℕ × ℕ => writeRegs p.1 p.2.1 p.2.2) :=
  Primrec.list_cons.comp (Primrec.pair (Primrec.fst.comp Primrec.snd)
    (Primrec.snd.comp Primrec.snd)) Primrec.fst

theorem stepByCode_primrec : Primrec stepByCode := by
  have hts : Primrec (fun c : Config => c.1.tail) := Primrec.list_tail.comp Primrec.fst
  have hrs : Primrec (fun c : Config => c.2) := Primrec.snd
  have hc : Primrec (fun c : Config => taskEncode (c.1.head?.getD (.stmt .skip))) :=
    Primrec.encode.comp (Primrec.option_getD.comp (Primrec.list_head?.comp Primrec.fst)
      (Primrec.const (Task.stmt Stmt.skip)))
  have hv := Primrec.nat_div.comp hc (Primrec.const 2)
  have hq := Primrec.nat_sub.comp hv (Primrec.const 1)
  have htag := Primrec.nat_mod.comp hq (Primrec.const 4)
  have hp := Primrec.unpair.comp (Primrec.nat_div.comp hq (Primrec.const 4))
  have hl := Primrec.fst.comp hp
  have hr := Primrec.snd.comp hp
  have hrl := Primrec.fst.comp (Primrec.unpair.comp hr)
  have hrr := Primrec.snd.comp (Primrec.unpair.comp hr)
  have hevalr := evalRegs_primrec.comp ((Primrec.ofNat Expr).comp hr) hrs
  have hevall := evalRegs_primrec.comp ((Primrec.ofNat Expr).comp hl) hrs
  have hevalrl := evalRegs_primrec.comp ((Primrec.ofNat Expr).comp hrl) hrs
  have hstmtl := taskStmt_primrec.comp (stmtOfNat_primrec.comp hl)
  have hstmtr := taskStmt_primrec.comp (stmtOfNat_primrec.comp hr)
  have hskip := Primrec.pair hts hrs
  have hset := Primrec.pair hts
    (writeRegs_primrec.comp (Primrec.pair hrs (Primrec.pair hl hevalr)))
  have hseq := Primrec.pair
    (Primrec.list_cons.comp hstmtl (Primrec.list_cons.comp hstmtr hts)) hrs
  have hloop := Primrec.pair (Primrec.list_cons.comp
    (taskRepeat_primrec.comp (Primrec.pair hl (Primrec.pair (Primrec.const 0)
      (Primrec.pair hevalrl (stmtOfNat_primrec.comp hrr))))) hts) hrs
  have hbranch := Primrec.pair (Primrec.list_cons.comp
    (taskStmt_primrec.comp (Primrec.ite (Primrec.eq.comp hevall (Primrec.const 0))
      (stmtOfNat_primrec.comp hrr) (stmtOfNat_primrec.comp hrl))) hts) hrs
  have hstmt := Primrec.ite (Primrec.eq.comp hv (Primrec.const 0)) hskip
    (Primrec.ite (Primrec.eq.comp htag (Primrec.const 0)) hset
      (Primrec.ite (Primrec.eq.comp htag (Primrec.const 1)) hseq
        (Primrec.ite (Primrec.eq.comp htag (Primrec.const 2)) hloop hbranch)))
  have hrep := Primrec.unpair.comp hv
  have hrp := Primrec.fst.comp hrep
  have htail := Primrec.unpair.comp (Primrec.snd.comp hrep)
  have hkp := Primrec.fst.comp htail
  have htail₂ := Primrec.unpair.comp (Primrec.snd.comp htail)
  have hnp := Primrec.fst.comp htail₂
  have hsp := stmtOfNat_primrec.comp (Primrec.snd.comp htail₂)
  have hrepeat := Primrec.ite (Primrec.eq.comp hnp (Primrec.const 0)) hskip
    (Primrec.pair
      (Primrec.list_cons.comp (taskStmt_primrec.comp hsp)
        (Primrec.list_cons.comp
          (taskRepeat_primrec.comp (Primrec.pair hrp
            (Primrec.pair (Primrec.nat_add.comp hkp (Primrec.const 1))
              (Primrec.pair (Primrec.nat_sub.comp hnp (Primrec.const 1)) hsp)))) hts))
      (writeRegs_primrec.comp (Primrec.pair hrs (Primrec.pair hrp hkp))))
  exact Primrec.ite (Primrec.eq.comp Primrec.fst (Primrec.const [])) Primrec.id
    (Primrec.ite (Primrec.eq.comp (Primrec.nat_mod.comp hc (Primrec.const 2))
      (Primrec.const 0)) hstmt hrepeat)

/-- The actual transition from the frozen machine is primitive recursive. -/
theorem step_primrec : Primrec step := stepByCode_primrec.of_eq stepByCode_eq_step

theorem step_computable : Computable step := step_primrec.to_comp

/-- Fuel and the entire starting stack/register file vary uniformly. -/
theorem runFuel_primrec : Primrec₂ (fun fuel (c : Config) => runFuel fuel c.1 c.2) := by
  have hit : Primrec (fun p : ℕ × Config => step^[p.1] p.2) :=
    Primrec.nat_iterate Primrec.fst Primrec.snd ((step_primrec.comp Primrec.snd).to₂)
  exact Primrec.ite (Primrec.eq.comp (Primrec.fst.comp hit) (Primrec.const []))
    (Primrec.option_some.comp (Primrec.snd.comp hit)) (Primrec.const none)

theorem runFuel_computable : Computable₂ (fun fuel (c : Config) => runFuel fuel c.1 c.2) :=
  runFuel_primrec.to_comp

theorem binaryRegs_primrec : Primrec₂ binaryRegs :=
  Primrec.list_cons.comp (Primrec.pair (Primrec.const 0) Primrec.fst)
    (Primrec.list_cons.comp (Primrec.pair (Primrec.const 1) Primrec.snd) (Primrec.const []))

end P02.Codec.UniformComputability
