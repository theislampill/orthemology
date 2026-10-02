import PRProgram

namespace P02A2.PRComposition
open P02A2.ObserverCore P02A2.LoopRenaming P02A2.LoopPrimrec P02A2.PRProgram

def inputArgs (k : ℕ) : Fin k → Expr := fun i => .reg i.val
def buffer {m : ℕ} (k : ℕ) (i : Fin m) : ℕ := k+1+i.val
def start (k m : ℕ) : ℕ := k+m+1

def InputsAgree {k : ℕ} (args : Fin k → ℕ) (σ : Store) : Prop := ∀ i, σ i.val = args i

theorem inputArgs_fresh (k b : ℕ) (hk : k ≤ b) :
    ∀ i r, r ∈ exprRegs (inputArgs k i) → r < b := by
  intro i r hr
  have he : r = i.val := by simpa [inputArgs, exprRegs] using hr
  subst r
  exact lt_of_lt_of_le i.isLt hk

theorem buffer_lt_start {m : ℕ} (k : ℕ) (i : Fin m) : buffer k i < start k m := by
  unfold buffer start
  omega

theorem buffer_injective {m : ℕ} (k : ℕ) : Function.Injective (@buffer m k) := by
  intro i j he
  apply Fin.ext
  unfold buffer at he
  omega

def componentCalls {k m : ℕ} (gs : Fin m → Program k) (order : List (Fin m)) : Stmt :=
  PRProgram.sequence (order.map (fun i => call (gs i) (start k m) (inputArgs k) (buffer k i)))

theorem componentCall_inputs {k m : ℕ} (gs : Fin m → Program k) (i : Fin m)
    (args : Fin k → ℕ) (σ : Store) (hi : InputsAgree args σ) :
    InputsAgree args (exec (call (gs i) (start k m) (inputArgs k) (buffer k i)) σ) := by
  intro j
  rw [call_frame (gs i) (start k m) (inputArgs k) (buffer k i)
    (inputArgs_fresh k _ (by unfold start; omega)) j.val (by unfold start; omega)
    (by unfold buffer; omega)]
  exact hi j

theorem componentCall_value {k m : ℕ} (gs : Fin m → Program k) (i : Fin m)
    (args : Fin k → ℕ) (σ : Store) (hi : InputsAgree args σ) :
    exec (call (gs i) (start k m) (inputArgs k) (buffer k i)) σ (buffer k i) = denote (gs i) args := by
  rw [call_value (gs i) (start k m) (inputArgs k) (buffer k i)
    (inputArgs_fresh k _ (by unfold start; omega))]
  congr 1
  funext j
  exact hi j

theorem componentCall_other {k m : ℕ} (gs : Fin m → Program k) (i j : Fin m) (hji : j ≠ i)
    (σ : Store) :
    exec (call (gs i) (start k m) (inputArgs k) (buffer k i)) σ (buffer k j) = σ (buffer k j) :=
  call_frame (gs i) (start k m) (inputArgs k) (buffer k i)
    (inputArgs_fresh k _ (by unfold start; omega)) (buffer k j) (buffer_lt_start k j)
    (fun he => hji (buffer_injective k he)) σ

theorem componentCalls_correct {k m : ℕ} (gs : Fin m → Program k) (order : List (Fin m))
    (horder : order.Nodup) (args : Fin k → ℕ) (σ : Store) (hi : InputsAgree args σ) :
    InputsAgree args (exec (componentCalls gs order) σ) ∧
    ∀ i, exec (componentCalls gs order) σ (buffer k i) =
      if i ∈ order then denote (gs i) args else σ (buffer k i) := by
  induction order generalizing σ with
  | nil => exact ⟨hi, fun i => by simp [componentCalls, PRProgram.sequence, exec]⟩
  | cons j order ih =>
      let τ := exec (call (gs j) (start k m) (inputArgs k) (buffer k j)) σ
      have hτ := componentCall_inputs gs j args σ hi
      have hn := List.nodup_cons.mp horder
      have hrest := ih hn.2 τ hτ
      constructor
      · exact hrest.1
      · intro i
        change exec (componentCalls gs order) τ (buffer k i) = _
        rw [hrest.2 i]
        by_cases hij : i = j
        · subst i
          simp only [List.mem_cons, true_or, ↓reduceIte, hn.1]
          exact componentCall_value gs j args σ hi
        · dsimp only [τ]
          rw [componentCall_other gs j i hij σ]
          simp [hij]

def bufferArgs {m : ℕ} (k : ℕ) : Fin m → Expr := fun i => .reg (buffer k i)

theorem bufferArgs_fresh {m : ℕ} (k : ℕ) :
    ∀ i r, r ∈ exprRegs (bufferArgs (m := m) k i) → r < start k m := by
  intro i r hr
  have he : r = buffer k i := by simpa [bufferArgs, exprRegs] using hr
  subst r
  exact buffer_lt_start k i

def composeProgram {k m : ℕ} (f : Program m) (gs : Fin m → Program k) : Program k :=
  ⟨.seq (componentCalls gs (List.finRange m))
    (call f (start k m) (bufferArgs k) k), k⟩

theorem composeProgram_correct {k m : ℕ} (f : Program m) (gs : Fin m → Program k)
    (args : Fin k → ℕ) :
    denote (composeProgram f gs) args = denote f (fun i => denote (gs i) args) := by
  have hi : InputsAgree args (extend args) := by intro i; simp [extend, i.isLt]
  have h := componentCalls_correct gs (List.finRange m) (List.nodup_finRange m) args (extend args) hi
  change exec (call f (start k m) (bufferArgs k) k)
    (exec (componentCalls gs (List.finRange m)) (extend args)) k = _
  rw [call_value f _ _ _ (bufferArgs_fresh k)]
  congr 1
  funext i
  simpa only [bufferArgs, evalExpr, List.mem_finRange, ↓reduceIte] using h.2 i

end P02A2.PRComposition
