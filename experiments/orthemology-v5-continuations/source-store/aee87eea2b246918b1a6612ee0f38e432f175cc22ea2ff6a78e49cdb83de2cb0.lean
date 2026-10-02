import MicroQueue
import PolicyTranscriptFiber

noncomputable section
namespace Orthemology.Tranche2.MicroPolicy
open PolicyEmbedding
variable {Θ A Y : Type*} [DecidableEq A]

/-- Exact physical-time recursion, starting from an arbitrary acquired history. -/
def microRun (plan : Θ → List A) (choose : History A Y → Θ) (d : A)
    (X : A → ℕ → Y) (h : History A Y) : ℕ → History A Y
  | 0 => h
  | n+1 => let prev := microRun plan choose d X h n
           let a := policy plan choose d () prev
           (a,X a (actionCount a prev)) :: prev

lemma microRun_add (plan : Θ → List A) (choose : History A Y → Θ) (d : A)
    (X : A → ℕ → Y) (h : History A Y) (n m : ℕ) :
    microRun plan choose d X h (n+m) =
      microRun plan choose d X (microRun plan choose d X h n) m := by
  induction m with
  | zero => rfl
  | succ m ih =>
    change (policy plan choose d () (microRun plan choose d X h (n+m)),
      X (policy plan choose d () (microRun plan choose d X h (n+m)))
        (actionCount (policy plan choose d () (microRun plan choose d X h (n+m)))
          (microRun plan choose d X h (n+m)))) :: microRun plan choose d X h (n+m) = _
    rw [ih]
    rfl

lemma microRun_succ_start (plan : Θ → List A) (choose : History A Y → Θ) (d : A)
    (X : A → ℕ → Y) (h : History A Y) (n : ℕ) :
    microRun plan choose d X h (n+1) =
      microRun plan choose d X
        ((policy plan choose d () h, X (policy plan choose d () h)
          (actionCount (policy plan choose d () h) h)) :: h) n := by
  simpa only [microRun,Nat.one_add] using microRun_add plan choose d X h 1 n

/-- A nonempty residual plan is executed from left to right before replanning. -/
theorem microRun_eq_feed_partial (plan : Θ → List A) (choose : History A Y → Θ) (d : A)
    (X : A → ℕ → Y) (h : History A Y) (as rest : List A) (hr : rest ≠ [])
    (hq : queue plan choose h = as ++ rest) :
    microRun plan choose d X h as.length = feed X h as := by
  induction as generalizing h with
  | nil => rfl
  | cons a as ih =>
    have ha : policy plan choose d () h = a := by simp [policy,hq]
    rw [List.length_cons,microRun_succ_start,ha]
    apply ih
    rw [queue_cons plan choose h a _ (as ++ rest) hq,if_neg]
    exact List.append_ne_nil_of_right_ne_nil as hr

/-- The final action of a block is executed before the history-based reset. -/
theorem microRun_eq_feed_complete (plan : Θ → List A) (choose : History A Y → Θ) (d : A)
    (X : A → ℕ → Y) (h : History A Y) (as : List A)
    (hq : queue plan choose h = as) :
    microRun plan choose d X h as.length = feed X h as := by
  induction as generalizing h with
  | nil => rfl
  | cons a as ih =>
    have ha : policy plan choose d () h = a := by simp [policy,hq]
    rw [List.length_cons,microRun_succ_start,ha]
    cases as with
    | nil => rfl
    | cons b bs =>
      apply ih
      simpa using queue_cons plan choose h a (X a (actionCount a h)) (b :: bs) hq

/-- Full-support static-menu macro boundary histories use the same acquired
feedback as the micro recursion. -/
def macroHistory (plan : Θ → List A) (choose : History A Y → Θ)
    (X : A → ℕ → Y) : ℕ → History A Y
  | 0 => []
  | n+1 => let h := macroHistory plan choose X n
           feed X h (plan (choose h))

def macroSelected (plan : Θ → List A) (choose : History A Y → Θ)
    (X : A → ℕ → Y) (n : ℕ) : Θ := choose (macroHistory plan choose X n)

lemma macro_queue (plan : Θ → List A) (choose : History A Y → Θ)
    (hne : ∀ σ, plan σ ≠ []) (X : A → ℕ → Y) (n : ℕ) :
    queue plan choose (macroHistory plan choose X n) =
      plan (choose (macroHistory plan choose X n)) := by
  induction n with
  | zero => rfl
  | succ n ih => exact queue_feed_complete plan choose X _ _ (hne _) ih

lemma macro_history_length (plan : Θ → List A) (choose : History A Y → Θ)
    (X : A → ℕ → Y) (n : ℕ) :
    (macroHistory plan choose X (n+1)).length =
      (macroHistory plan choose X n).length +
        (plan (macroSelected plan choose X n)).length := by
  exact feed_length X _ _

/-- Exact macro-to-micro refinement at every completed block boundary. -/
theorem macro_eq_micro_boundary (plan : Θ → List A) (choose : History A Y → Θ) (d : A)
    (hne : ∀ σ, plan σ ≠ []) (X : A → ℕ → Y) (n : ℕ) :
    microRun plan choose d X [] (macroHistory plan choose X n).length =
      macroHistory plan choose X n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [macro_history_length,microRun_add,ih]
    exact microRun_eq_feed_complete plan choose d X _ _ (macro_queue plan choose hne X n)

section Evaluator
variable [Fintype A] [Inhabited Y]
omit [Inhabited Y] in
/-- The physical history recursion is the same causal source-policy evaluator
used by the necessity theorem, when all action feedback comes from iid stacks. -/
theorem observedHistory_eq_micro (plan : Θ → List A) (choose : History A Y → Θ) (d : A)
    (X : A → ℕ → Y) (oracle : ℕ → A → Y) (n : ℕ) :
    observedHistory Finset.univ (policy plan choose d) oracle () X n =
      microRun plan choose d X [] n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [observedHistory,microRun,ih,feedback]
end Evaluator
end Orthemology.Tranche2.MicroPolicy
