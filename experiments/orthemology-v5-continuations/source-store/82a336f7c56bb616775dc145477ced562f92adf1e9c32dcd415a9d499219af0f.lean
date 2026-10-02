import EncodedHistoryFoldSource

namespace Orthemology.RuntimeBridge.PhaseUpdate.HistoryFold
open P02A2.ObserverCore P02A2.PRProgram P02A2.LoopRenaming
open Orthemology.RuntimeBridge.HistoryRuntime

def buffer (k : ℕ) (i : Fin k) : ℕ := k+3+i.val
def privateStart (k : ℕ) : ℕ := 2*k+3

def collect {k l : ℕ} (ps : Fin k → Program l) (args : Fin l → Expr)
    (order : List (Fin k)) : Stmt :=
  sequence (order.map (fun i => call (ps i) (privateStart k) args (buffer k i)))

theorem collect_correct {k l : ℕ} (ps : Fin k → Program l) (args : Fin l → Expr)
    (ha : ∀ i r, r ∈ exprRegs (args i) → r < k+3)
    (order : List (Fin k)) (hn : order.Nodup) (σ : Store) :
    (∀ r, r < k+3 → exec (collect ps args order) σ r = σ r) ∧
    (∀ i, exec (collect ps args order) σ (buffer k i) =
      if i ∈ order then denote (ps i) (fun j => evalExpr (args j) σ) else σ (buffer k i)) := by
  have hf : ∀ i r, r ∈ exprRegs (args i) → r < privateStart k := by
    intro i r hr
    have := ha i r hr
    unfold privateStart
    omega
  induction order generalizing σ with
  | nil => simp [collect,P02A2.PRProgram.sequence,exec]
  | cons j order ih =>
      let τ := exec (call (ps j) (privateStart k) args (buffer k j)) σ
      have ht : ∀ r, r < k+3 → τ r = σ r := by
        intro r hr
        exact call_frame _ _ _ _ hf r (by unfold privateStart; omega)
          (by unfold buffer; omega) σ
      have hv : τ (buffer k j) = denote (ps j) (fun i => evalExpr (args i) σ) :=
        call_value _ _ _ _ hf σ
      have ho : ∀ i, i ≠ j → τ (buffer k i) = σ (buffer k i) := by
        intro i hij
        exact call_frame _ _ _ _ hf _ (by unfold buffer privateStart; omega)
          (by intro he; apply hij; apply Fin.ext; unfold buffer at he; omega) σ
      have he : (fun i => evalExpr (args i) τ) = (fun i => evalExpr (args i) σ) := by
        funext i
        apply evalExpr_congr
        intro r hr
        exact ht r (ha i r hr)
      have hn' := List.nodup_cons.mp hn
      have hh := ih hn'.2 τ
      constructor
      · intro r hr
        exact (hh.1 r hr).trans (ht r hr)
      · intro i
        change exec (collect ps args order) τ (buffer k i) = _
        rw [hh.2 i,he]
        by_cases hij : i = j
        · subst i
          simp only [List.mem_cons,true_or,↓reduceIte,hn'.1]
          exact hv
        · rw [ho i hij]
          simp [hij]

def copyBuffers (k : ℕ) (order : List (Fin k)) : Stmt :=
  sequence (order.map (fun i => .set (3+i.val) (.reg (buffer k i))))

theorem copy_buffers_correct (k : ℕ) (order : List (Fin k)) (hn : order.Nodup) (σ : Store) :
    (∀ r, r < 3 ∨ k+3 ≤ r → exec (copyBuffers k order) σ r = σ r) ∧
    (∀ i, exec (copyBuffers k order) σ (3+i.val) =
      if i ∈ order then σ (buffer k i) else σ (3+i.val)) := by
  induction order generalizing σ with
  | nil => simp [copyBuffers,P02A2.PRProgram.sequence,exec]
  | cons j order ih =>
      let τ := Function.update σ (3+j.val) (σ (buffer k j))
      have ht : ∀ r, r < 3 ∨ k+3 ≤ r → τ r = σ r := by
        intro r hr
        exact Function.update_of_ne (by rcases hr with hr|hr <;> omega) _ _
      have hn' := List.nodup_cons.mp hn
      have hh := ih hn'.2 τ
      constructor
      · intro r hr
        exact (hh.1 r hr).trans (ht r hr)
      · intro i
        change exec (copyBuffers k order) τ (3+i.val) = _
        rw [hh.2 i,ht (buffer k i) (Or.inr (by unfold buffer; omega))]
        by_cases hij : i = j
        · subst i
          simp only [List.mem_cons,true_or,↓reduceIte,hn'.1]
          exact Function.update_self _ _ _
        · have hne : 3+i.val ≠ 3+j.val := by
            intro he; apply hij; apply Fin.ext; omega
          rw [show τ (3+i.val) = σ (3+i.val) from Function.update_of_ne hne _ _]
          simp [hij]

def parallelStep {k l : ℕ} (ps : Fin k → Program l) (args : Fin l → Expr) : Stmt :=
  .seq (collect ps args (List.finRange k)) (copyBuffers k (List.finRange k))

theorem parallel_step_exact {k l : ℕ} (ps : Fin k → Program l) (args : Fin l → Expr)
    (ha : ∀ i r, r ∈ exprRegs (args i) → r < k+3) (σ : Store) :
    (∀ r, r < 3 → exec (parallelStep ps args) σ r = σ r) ∧
    (∀ i, exec (parallelStep ps args) σ (3+i.val) =
      denote (ps i) (fun j => evalExpr (args j) σ)) := by
  have hc := collect_correct ps args ha (List.finRange k) (List.nodup_finRange k) σ
  have hp := copy_buffers_correct k (List.finRange k) (List.nodup_finRange k)
    (exec (collect ps args (List.finRange k)) σ)
  constructor
  · intro r hr
    exact (hp.1 r (Or.inl hr)).trans (hc.1 r (by omega))
  · intro i
    change exec (copyBuffers k (List.finRange k)) (exec (collect ps args (List.finRange k)) σ) (3+i.val) = _
    simpa only [List.mem_finRange,↓reduceIte] using (hp.2 i).trans (by simpa using hc.2 i)

/-- Data, followed by the accepted action and receipt digits. -/
def stepArgs (k : ℕ) : Fin (k+2) → Expr := fun i =>
  if i.val < k then .reg (3+i.val)
  else if i.val = k then .mod (.div (.reg 1) (.constant 2)) (.constant 2)
  else .mod (.reg 1) (.constant 2)

def stepInputs {k : ℕ} (v : Fin k → ℕ) (e : Bool × Bool) : Fin (k+2) → ℕ := fun i =>
  if hi : i.val < k then v ⟨i.val,hi⟩
  else if i.val = k then Orthemology.RuntimeBridge.bitNat e.1
  else Orthemology.RuntimeBridge.bitNat e.2

theorem step_args_fresh (k : ℕ) :
    ∀ i r, r ∈ exprRegs (stepArgs k i) → r < k+3 := by
  intro i r hr
  unfold stepArgs at hr
  split_ifs at hr <;> simp [exprRegs] at hr <;> omega

theorem step_args_value {k : ℕ} (rep : History → Fin k → ℕ) (code : ℕ)
    (e : Bool × Bool) (remaining accumulated : History) (σ : Store)
    (hm : Matches rep code (e::remaining) accumulated σ) :
    (fun j => evalExpr (stepArgs k j) σ) = stepInputs (rep accumulated) e := by
  funext i
  unfold stepArgs stepInputs
  split_ifs with hi he
  · exact hm.2.2 ⟨i.val,hi⟩
  · simp only [evalExpr,hm.2.1,encodeHistory]
    rcases e with ⟨a,y⟩
    cases a <;> cases y <;> simp only [appendHistory,Orthemology.RuntimeBridge.bitNat,Bool.false_eq_true,↓reduceIte] <;> omega
  · simp only [evalExpr,hm.2.1,encodeHistory,append_receipt]

/-- A family of local numeric source certificates generates the complete
history-fold step; old statistics are protected until all new values exist. -/
theorem parallel_implements {k : ℕ} (ps : Fin k → Program (k+2))
    (rep : History → Fin k → ℕ)
    (hp : ∀ e h j, denote (ps j) (stepInputs (rep h) e) = rep (e::h) j) :
    StepImplements (parallelStep ps (stepArgs k)) rep := by
  intro code e remaining accumulated σ hm
  have hs := parallel_step_exact ps (stepArgs k) (step_args_fresh k) σ
  refine ⟨(hs.1 0 (by decide)).trans hm.1,(hs.1 1 (by decide)).trans hm.2.1,?_⟩
  intro j
  rw [hs.2 j,step_args_value rep code e remaining accumulated σ hm]
  exact hp e accumulated j

end Orthemology.RuntimeBridge.PhaseUpdate.HistoryFold
