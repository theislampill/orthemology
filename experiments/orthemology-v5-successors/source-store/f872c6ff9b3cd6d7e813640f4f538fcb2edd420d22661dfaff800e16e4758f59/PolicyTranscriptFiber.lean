import PolicyRowEvaluator

noncomputable section
namespace Orthemology.Tranche2.PolicyEmbedding
variable {R A Y : Type*} [DecidableEq A] [Inhabited Y]

def outsideCount (U : Finset A) (h : History A Y) : ℕ := h.countP (fun ay => ay.1 ∉ U)

def feedback (U : Finset A) (X : Stack A Y) (oracle : ℕ → A → Y) (a : A) (h : History A Y) : Y :=
  if a ∉ U then oracle (outsideCount U h) a else X a (actionCount a h)

def observedHistory (U : Finset A) (π : R → History A Y → A) (oracle : ℕ → A → Y)
    (seed : R) (X : Stack A Y) : ℕ → History A Y
  | 0 => []
  | n+1 => let h := observedHistory U π oracle seed X n
           let a := π seed h
           (a,feedback U X oracle a h)::h

omit [Inhabited Y] in
lemma observedHistory_length (U : Finset A) (π : R → History A Y → A) (oracle : ℕ → A → Y)
    (seed : R) (X : Stack A Y) (n : ℕ) : (observedHistory U π oracle seed X n).length = n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [observedHistory,ih]

/-- Exact source-evaluator correspondence, including the actual observed
history, preserved seed/stack, and outside-action query counter. -/
theorem policyRun_eq_observedHistory (U : Finset A) (π : R → History A Y → A) (oracle : ℕ → A → Y)
    (seed : R) (X : Stack A Y) (n : ℕ) :
    policyRun U π oracle seed X n =
      ((seed,(X,observedHistory U π oracle seed X n)),
        outsideCount U (observedHistory U π oracle seed X n)) := by
  induction n with
  | zero => simp [policyRun,FiniteAlphabetQuery.run,observedHistory,outsideCount]
  | succ n ih =>
    change FiniteAlphabetQuery.advance (query U π) (step U π) oracle (policyRun U π oracle seed X n) = _
    rw [ih]
    by_cases h : π seed (observedHistory U π oracle seed X n) ∉ U
    · simp [FiniteAlphabetQuery.advance,query,selected,step,observedHistory,feedback,h,outsideCount]
    · simp [FiniteAlphabetQuery.advance,query,selected,step,observedHistory,feedback,h,outsideCount]

def ActionCompatible (π : R → History A Y → A) (seed : R) : History A Y → Prop
  | [] => True
  | (a,_)::h => ActionCompatible π seed h ∧ π seed h = a

def FeedbackCompatible (U : Finset A) (X : Stack A Y) (oracle : ℕ → A → Y) : History A Y → Prop
  | [] => True
  | (a,y)::h => FeedbackCompatible U X oracle h ∧ feedback U X oracle a h = y

omit [Inhabited Y] in
/-- Finite transcript consistency separates private-policy seed constraints
from feedback-stack/oracle constraints. This is a deterministic fiber identity;
its probability factorization is a separate measure-theoretic obligation. -/
theorem observedHistory_fiber (U : Finset A) (π : R → History A Y → A) (oracle : ℕ → A → Y)
    (seed : R) (X : Stack A Y) (h : History A Y) :
    observedHistory U π oracle seed X h.length = h ↔
      ActionCompatible π seed h ∧ FeedbackCompatible U X oracle h := by
  induction h with
  | nil => simp [observedHistory,ActionCompatible,FeedbackCompatible]
  | cons ay h ih =>
    rcases ay with ⟨a,y⟩
    constructor
    · intro heq
      have ht : observedHistory U π oracle seed X h.length = h := by
        simpa only [List.length_cons,observedHistory,List.tail_cons] using congrArg List.tail heq
      have hp : (π seed h,feedback U X oracle (π seed h) h) = (a,y) := by
        simpa only [List.length_cons,observedHistory,ht,List.cons.injEq,and_true] using heq
      have ha : π seed h = a := congrArg Prod.fst hp
      have hy : feedback U X oracle a h = y := by simpa only [ha] using congrArg Prod.snd hp
      obtain ⟨hA,hF⟩ := ih.mp ht
      exact ⟨⟨hA,ha⟩,⟨hF,hy⟩⟩
    · rintro ⟨⟨hA,ha⟩,⟨hF,hy⟩⟩
      have ht := ih.mpr ⟨hA,hF⟩
      simp only [List.length_cons,observedHistory,ht,ha,hy]

theorem policyRun_transcript_fiber (U : Finset A) (π : R → History A Y → A) (oracle : ℕ → A → Y)
    (seed : R) (X : Stack A Y) (h : History A Y) :
    (policyRun U π oracle seed X h.length).1.2.2 = h ↔
      ActionCompatible π seed h ∧ FeedbackCompatible U X oracle h := by
  rw [policyRun_eq_observedHistory]
  exact observedHistory_fiber U π oracle seed X h

end Orthemology.Tranche2.PolicyEmbedding
