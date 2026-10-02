import PolicyRowEvaluator
import CanonicalBlockPolicy

noncomputable section
open MeasureTheory ProbabilityTheory Filter Finset
open scoped BigOperators

namespace Orthemology.Tranche2.MicroPolicy
open PolicyEmbedding
variable {Θ A Y : Type*} [DecidableEq A]

/-- Replay a finite acquired history to reconstruct the unexecuted block suffix.
The selector receives the current history only when the previous block ends. -/
def queue (plan : Θ → List A) (choose : History A Y → Θ) : History A Y → List A
  | [] => plan (choose [])
  | z :: h => let rest := (queue plan choose h).tail
              if rest = [] then plan (choose (z :: h)) else rest

lemma queue_nonempty (plan : Θ → List A) (choose : History A Y → Θ)
    (hne : ∀ σ, plan σ ≠ []) (h : History A Y) : queue plan choose h ≠ [] := by
  cases h with
  | nil => exact hne _
  | cons z h =>
    simp only [queue]
    split_ifs with he
    · exact hne _
    · exact he

def policy (plan : Θ → List A) (choose : History A Y → Θ) (d : A)
    (_ : Unit) (h : History A Y) : A := (queue plan choose h).headD d

lemma queue_cons (plan : Θ → List A) (choose : History A Y → Θ)
    (h : History A Y) (a : A) (y : Y) (rest : List A)
    (hq : queue plan choose h = a :: rest) :
    queue plan choose ((a,y) :: h) =
      if rest = [] then plan (choose ((a,y) :: h)) else rest := by
  simp only [queue,hq,List.tail_cons]

/-- Acquired feedback from an action-indexed stack; no later coordinate is read. -/
def feed (X : A → ℕ → Y) : History A Y → List A → History A Y
  | h, [] => h
  | h, a :: rest => feed X ((a, X a (actionCount a h)) :: h) rest

lemma feed_length (X : A → ℕ → Y) (h : History A Y) (as : List A) :
    (feed X h as).length = h.length + as.length := by
  induction as generalizing h with
  | nil => simp [feed]
  | cons a as ih =>
    simpa [feed, Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using
      (ih ((a,X a (actionCount a h)) :: h))

lemma feed_append (X : A → ℕ → Y) (h : History A Y) (as bs : List A) :
    feed X h (as ++ bs) = feed X (feed X h as) bs := by
  induction as generalizing h with
  | nil => rfl
  | cons a as ih => exact ih _

lemma queue_feed_partial (plan : Θ → List A) (choose : History A Y → Θ)
    (X : A → ℕ → Y) (h : History A Y) (as rest : List A) (hr : rest ≠ [])
    (hq : queue plan choose h = as ++ rest) :
    queue plan choose (feed X h as) = rest := by
  induction as generalizing h with
  | nil => simpa [feed] using hq
  | cons a as ih =>
    apply ih ((a,X a (actionCount a h)) :: h)
    rw [queue_cons plan choose h a _ (as ++ rest) hq,if_neg]
    exact List.append_ne_nil_of_right_ne_nil as hr

lemma queue_feed_complete (plan : Θ → List A) (choose : History A Y → Θ)
    (X : A → ℕ → Y) (h : History A Y) (as : List A) (hne : as ≠ [])
    (hq : queue plan choose h = as) :
    queue plan choose (feed X h as) = plan (choose (feed X h as)) := by
  induction as generalizing h with
  | nil => exact (hne rfl).elim
  | cons a as ih =>
    cases as with
    | nil => simp [feed,queue_cons plan choose h a _ [] hq]
    | cons b bs =>
      apply ih ((a,X a (actionCount a h)) :: h) (by simp)
      simpa using queue_cons plan choose h a (X a (actionCount a h)) (b :: bs) hq

end Orthemology.Tranche2.MicroPolicy
