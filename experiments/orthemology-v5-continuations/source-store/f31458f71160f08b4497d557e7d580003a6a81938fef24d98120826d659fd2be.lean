import EmpiricalGateSource
set_option maxHeartbeats 2000000

namespace Orthemology.RuntimeBridge.PhaseUpdate
open P02A2.ObserverCore P02A2.PRProgram
open Orthemology.Tranche2.PolicyEmbedding
open HiddenParity HiddenParity.Sufficiency
open scoped BigOperators

/-- Eight literal pair/receipt coordinates, with an executable fixed order. -/
def coordPair (j : Fin 8) : Bool × Bool := (decide (4 ≤ j.val),decide (2 ≤ j.val % 4))
def coordReceipt (j : Fin 8) : Bool := decide (j.val % 2 = 1)

def coordIndex (e : Bool × Bool) (y : Bool) : Fin 8 :=
  ⟨2*pairCode e+bitNat y,by rcases e with ⟨s,a⟩; cases s <;> cases a <;> cases y <;> decide⟩

theorem coord_pair_inverse (e : Bool × Bool) (y : Bool) : coordPair (coordIndex e y) = e := by
  rcases e with ⟨s,a⟩
  cases s <;> cases a <;> cases y <;> rfl

theorem coord_receipt_inverse (e : Bool × Bool) (y : Bool) : coordReceipt (coordIndex e y) = y := by
  rcases e with ⟨s,a⟩
  cases s <;> cases a <;> cases y <;> rfl

def statisticInputs (k : ℕ) (h : History (Bool × Bool) Bool) : Fin 13 → ℕ :=
  ![k,actionCount (false,false) h,actionCount (false,true) h,
    actionCount (true,false) h,actionCount (true,true) h,
    RationalGate.symbolCount (false,false) false h,RationalGate.symbolCount (false,false) true h,
    RationalGate.symbolCount (false,true) false h,RationalGate.symbolCount (false,true) true h,
    RationalGate.symbolCount (true,false) false h,RationalGate.symbolCount (true,false) true h,
    RationalGate.symbolCount (true,true) false h,RationalGate.symbolCount (true,true) true h]

theorem statistic_input_coordinate (k : ℕ) (h : History (Bool × Bool) Bool) (j : Fin 8) :
    P02A2.LoopPrimrec.extend (statisticInputs k h) 0 = k ∧
    P02A2.LoopPrimrec.extend (statisticInputs k h) (1+j.val/2) = actionCount (coordPair j) h ∧
    P02A2.LoopPrimrec.extend (statisticInputs k h) (5+j.val) =
      RationalGate.symbolCount (coordPair j) (coordReceipt j) h := by
  fin_cases j <;> simp [P02A2.LoopPrimrec.extend,statisticInputs,coordPair,coordReceipt]

def coordinateExpr (t d u v : ℕ) (j : Fin 8) : Expr :=
  let n := Expr.reg (1+j.val/2)
  let m := Expr.reg (5+j.val)
  let mv := Expr.mul m (.constant v)
  let un := Expr.mul (.constant u) n
  .mul (.sub (.constant 1) (.le n (.reg 0)))
    (.le (.mul (.constant t) (.mul n (.constant v)))
      (.mul (.constant d) (.add (.sub mv un) (.sub un mv))))

theorem coordinate_expr_value (t d u v : ℕ) (hd : 0 < d) (hv : 0 < v) (j : Fin 8) (τ : Store) :
    evalExpr (coordinateExpr t d u v j) τ =
      bitNat (decide (τ 0 < τ (1+j.val/2) ∧
        (t : ℚ)/d ≤ |(τ (5+j.val) : ℚ)/τ (1+j.val/2)-(u : ℚ)/v|)) := by
  simpa [denote,gateProgram,gateExpr,deviationExpr,coordinateExpr,exec,evalExpr,P02A2.LoopPrimrec.extend]
    using gate_source_exact t d u v hd hv (τ 0) (τ (1+j.val/2)) (τ (5+j.val))

def sumExpr : List Expr → Expr
  | [] => .constant 0
  | e::es => .add e (sumExpr es)

theorem sum_expr_value (es : List Expr) (τ : Store) :
    evalExpr (sumExpr es) τ = (es.map (fun e => evalExpr e τ)).sum := by
  induction es with
  | nil => rfl
  | cons e es ih => simpa [sumExpr,evalExpr] using congrArg (evalExpr e τ + ·) ih

/-- A complete finite empirical test. No real arithmetic or counter lookup
oracle is an instruction: all eight comparisons are literal P02 expressions. -/
def empiricalProgram (t d v : ℕ) (u : Bool → (Bool × Bool) → Bool → ℕ) (θ : Bool) : Program 13 :=
  ⟨.set 13 (.le (.constant 1) (sumExpr (List.ofFn (fun j : Fin 8 =>
    coordinateExpr t d (u θ (coordPair j) (coordReceipt j)) v j)))),13⟩

theorem positive_bit_sum (f : Fin 8 → Bool) :
    1 ≤ (List.ofFn (fun j => bitNat (f j))).sum ↔ ∃ j, f j = true := by
  rw [List.sum_ofFn]
  constructor
  · intro hp
    by_contra hn
    have hz : (∑ j : Fin 8, bitNat (f j)) = 0 := by
      apply Finset.sum_eq_zero
      intro j hj
      cases he : f j
      · rfl
      · exact (hn ⟨j,he⟩).elim
    omega
  · rintro ⟨j,hj⟩
    have hb := Finset.single_le_sum (fun k (_ : k ∈ (Finset.univ : Finset (Fin 8))) => Nat.zero_le (bitNat (f k))) (Finset.mem_univ j)
    simpa [hj,bitNat] using hb

/-- Exact source equality to the retained rational/real empirical guard. The
coefficient premise states only the literal rational row representation. -/
theorem empirical_source_exact (P : RationalKernel Bool (Bool × Bool) Bool)
    (t d v : ℕ) (hd : 0 < d) (hv : 0 < v) (u : Bool → (Bool × Bool) → Bool → ℕ)
    (hu : ∀ θ e y, P.row θ e y = (u θ e y : ℚ)/v)
    (θ : Bool) (k : ℕ) (h : History (Bool × Bool) Bool) :
    denote (empiricalProgram t d v u θ) (statisticInputs k h) =
      bitNat (RationalGate.reject P ((t : ℚ)/d) θ k h) := by
  let τ := P02A2.LoopPrimrec.extend (statisticInputs k h)
  let f := fun j : Fin 8 => decide (k < actionCount (coordPair j) h ∧
    (t : ℚ)/d ≤ |RationalGate.frequency (coordPair j) (coordReceipt j) h - P.row θ (coordPair j) (coordReceipt j)|)
  have hc : ∀ j : Fin 8, evalExpr (coordinateExpr t d (u θ (coordPair j) (coordReceipt j)) v j) τ = bitNat (f j) := by
    intro j
    rw [coordinate_expr_value _ _ _ _ hd hv]
    have hi := statistic_input_coordinate k h j
    simp only [τ,hi.1,hi.2.1,hi.2.2,f,RationalGate.frequency,hu]
  have hs : evalExpr (sumExpr (List.ofFn (fun j : Fin 8 => coordinateExpr t d (u θ (coordPair j) (coordReceipt j)) v j))) τ =
      (List.ofFn (fun j : Fin 8 => bitNat (f j))).sum := by
    rw [sum_expr_value,List.map_ofFn]
    congr 2
    funext j
    exact hc j
  have hf : (∃ j : Fin 8, f j = true) ↔ RationalGate.reject P ((t : ℚ)/d) θ k h = true := by
    simp only [RationalGate.reject,decide_eq_true_eq,f]
    constructor
    · rintro ⟨j,hj⟩
      exact ⟨coordPair j,coordReceipt j,hj⟩
    · rintro ⟨e,y,he⟩
      exact ⟨coordIndex e y,by simpa only [coord_pair_inverse,coord_receipt_inverse] using he⟩
  simp only [denote,empiricalProgram,exec,Function.update_self]
  change (if 1 ≤ evalExpr (sumExpr (List.ofFn (fun j : Fin 8 => coordinateExpr t d (u θ (coordPair j) (coordReceipt j)) v j))) τ then 1 else 0) = _
  rw [hs]
  have hg := (positive_bit_sum f).trans hf
  by_cases hr : RationalGate.reject P ((t : ℚ)/d) θ k h = true
  · have hy := hg.mpr hr
    have hright : bitNat (RationalGate.reject P ((t : ℚ)/d) θ k h) = 1 := by rw [hr]; rfl
    exact (if_pos hy).trans hright.symm
  · have hn : ¬ 1 ≤ (List.ofFn (fun j => bitNat (f j))).sum := fun hsum => hr (hg.mp hsum)
    have hright : bitNat (RationalGate.reject P ((t : ℚ)/d) θ k h) = 0 := by
      cases hx : RationalGate.reject P ((t : ℚ)/d) θ k h
      · rfl
      · exact (hr hx).elim
    exact (if_neg hn).trans hright.symm

theorem empirical_source_real_exact (P : RationalKernel Bool (Bool × Bool) Bool)
    (t d v : ℕ) (hd : 0 < d) (hv : 0 < v) (u : Bool → (Bool × Bool) → Bool → ℕ)
    (hu : ∀ θ e y, P.row θ e y = (u θ e y : ℚ)/v)
    (θ : Bool) (k : ℕ) (h : History (Bool × Bool) Bool) :
    denote (empiricalProgram t d v u θ) (statisticInputs k h) =
      bitNat (empiricalReject P (((t : ℚ)/d) : ℝ) θ k h) := by
  rw [empirical_source_exact P t d v hd hv u hu θ k h,RationalGate.reject_exact]
  simp only [Rat.cast_div,Rat.cast_natCast]

end Orthemology.RuntimeBridge.PhaseUpdate
