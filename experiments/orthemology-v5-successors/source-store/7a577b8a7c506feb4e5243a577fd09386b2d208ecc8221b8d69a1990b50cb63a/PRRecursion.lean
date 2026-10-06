import PRComposition

namespace P02A2.PRRecursion
open P02A2.ObserverCore P02A2.LoopRenaming P02A2.LoopPrimrec P02A2.PRProgram P02A2.PRComposition

def loopIndex (k : ℕ) := k+2
def accumulator (k : ℕ) := k+3
def temporary (k : ℕ) := k+4
def privateStart (k : ℕ) := k+5

def appendTwo {k : ℕ} (args : Fin k → ℕ) (index value : ℕ) : Fin (k+2) → ℕ :=
  fun i => if hi : i.val < k then args ⟨i.val,hi⟩ else if i.val = k then index else value

def stepArgs (k : ℕ) : Fin (k+2) → Expr :=
  fun i => if i.val < k then .reg i.val else if i.val = k then .reg (loopIndex k) else .reg (accumulator k)

theorem stepArgs_fresh (k : ℕ) :
    ∀ i r, r ∈ exprRegs (stepArgs k i) → r < privateStart k := by
  intro i r hr
  unfold stepArgs at hr
  split_ifs at hr <;> simp only [exprRegs, Finset.mem_singleton] at hr <;>
    dsimp [loopIndex, accumulator, privateStart] at * <;> omega

def RecMatches {k : ℕ} (params : Fin k → ℕ) (acc : ℕ) (σ : Store) : Prop :=
  InputsAgree params σ ∧ σ (accumulator k) = acc

theorem stepArgs_eval {k : ℕ} (params : Fin k → ℕ) (acc index : ℕ) (σ : Store)
    (hm : RecMatches params acc σ) (hi : σ (loopIndex k) = index) :
    (fun i => evalExpr (stepArgs k i) σ) = appendTwo params index acc := by
  funext i
  by_cases h : i.val < k
  · simp only [stepArgs, appendTwo, h, ↓reduceIte, ↓reduceDIte, evalExpr]
    exact hm.1 ⟨i.val,h⟩
  · by_cases hk : i.val = k <;>
      simp [stepArgs, appendTwo, h, hk, evalExpr, hi, hm.2]

def stepBody {k : ℕ} (h : Program (k+2)) : Stmt :=
  .seq (call h (privateStart k) (stepArgs k) (temporary k))
    (.set (accumulator k) (.reg (temporary k)))

theorem stepBody_matches {k : ℕ} (h : Program (k+2)) (params : Fin k → ℕ)
    (acc index : ℕ) (σ : Store) (hm : RecMatches params acc σ) (hi : σ (loopIndex k) = index) :
    RecMatches params (denote h (appendTwo params index acc)) (exec (stepBody h) σ) := by
  let τ := exec (call h (privateStart k) (stepArgs k) (temporary k)) σ
  have hv := call_value h (privateStart k) (stepArgs k) (temporary k) (stepArgs_fresh k) σ
  rw [stepArgs_eval params acc index σ hm hi] at hv
  constructor
  · intro i
    change Function.update τ (accumulator k) (τ (temporary k)) i.val = params i
    rw [Function.update_of_ne (by unfold accumulator; omega : i.val ≠ accumulator k)]
    change exec (call h (privateStart k) (stepArgs k) (temporary k)) σ i.val = params i
    rw [call_frame h (privateStart k) (stepArgs k) (temporary k) (stepArgs_fresh k) i.val
      (by unfold privateStart; omega) (by unfold temporary; omega)]
    exact hm.1 i
  · change Function.update τ (accumulator k) (τ (temporary k)) (accumulator k) = _
    rw [Function.update_self]
    exact hv

theorem recursionLoop_matches {k : ℕ} (h : Program (k+2)) (params : Fin k → ℕ)
    (base : ℕ) (σ : Store) (hm : RecMatches params base σ) (n : ℕ) :
    RecMatches params (n.rec base (fun j value => denote h (appendTwo params j value)))
      (runLoop (exec (stepBody h)) (loopIndex k) n σ) := by
  induction n with
  | zero => exact hm
  | succ n ih =>
      simp only [runLoop, Nat.rec_add_one]
      apply stepBody_matches h params _ n
      · constructor
        · intro i
          rw [Function.update_of_ne (by unfold loopIndex; omega : i.val ≠ loopIndex k)]
          exact ih.1 i
        · rw [Function.update_of_ne (by unfold accumulator loopIndex; omega : accumulator k ≠ loopIndex k)]
          exact ih.2
      · simp

def primitiveRecProgram {k : ℕ} (g : Program k) (h : Program (k+2)) : Program (k+1) :=
  ⟨.seq (call g (privateStart k) (inputArgs k) (accumulator k))
    (.seq (.loop (loopIndex k) (.reg k) (stepBody h))
      (.set (k+1) (.reg (accumulator k)))), k+1⟩

theorem primitiveRecProgram_correct {k : ℕ} (g : Program k) (h : Program (k+2))
    (args : Fin (k+1) → ℕ) :
    denote (primitiveRecProgram g h) args =
      (args (Fin.last k)).rec (denote g (fun i => args i.castSucc))
        (fun j value => denote h (appendTwo (fun i => args i.castSucc) j value)) := by
  let params : Fin k → ℕ := fun i => args i.castSucc
  let σ := extend args
  let τ := exec (call g (privateStart k) (inputArgs k) (accumulator k)) σ
  have hf : ∀ i r, r ∈ exprRegs (inputArgs k i) → r < privateStart k :=
    inputArgs_fresh k _ (by unfold privateStart; omega)
  have hs : InputsAgree params σ := by
    intro i
    change (if hr : i.val < k+1 then args ⟨i.val,hr⟩ else 0) = args i.castSucc
    rw [dif_pos (by omega)]
    exact congrArg args (Fin.ext rfl)
  have hv := call_value g (privateStart k) (inputArgs k) (accumulator k) hf σ
  have hargs : (fun i => evalExpr (inputArgs k i) σ) = params := funext hs
  rw [hargs] at hv
  have hm : RecMatches params (denote g params) τ := by
    constructor
    · intro i
      dsimp only [τ]
      rw [call_frame g (privateStart k) (inputArgs k) (accumulator k) hf i.val
        (by unfold privateStart; omega) (by unfold accumulator; omega)]
      exact hs i
    · exact hv
  have hcount : τ k = args (Fin.last k) := by
    dsimp only [τ]
    rw [call_frame g (privateStart k) (inputArgs k) (accumulator k) hf k
      (by unfold privateStart; omega) (by unfold accumulator; omega)]
    change (if hr : k < k+1 then args ⟨k,hr⟩ else 0) = args (Fin.last k)
    rw [dif_pos (by omega)]
    exact congrArg args (Fin.ext rfl)
  have hl := recursionLoop_matches h params (denote g params) τ hm (args (Fin.last k))
  change Function.update (runLoop (exec (stepBody h)) (loopIndex k) (τ k) τ)
    (k+1) ((runLoop (exec (stepBody h)) (loopIndex k) (τ k) τ) (accumulator k)) (k+1) = _
  rw [Function.update_self, hcount]
  exact hl.2

end P02A2.PRRecursion
