import PolicyTranscriptFiber

noncomputable section
namespace Orthemology.Tranche2.PolicyEmbedding
variable {A Y : Type*} [DecidableEq A]

abbrev FeedbackKey (A : Type*) := (A × ℕ) ⊕ ℕ

def feedbackKey (U : Finset A) (a : A) (h : History A Y) : FeedbackKey A :=
  if a ∈ U then Sum.inl (a,actionCount a h) else Sum.inr (outsideCount U h)

def feedbackKeys (U : Finset A) : History A Y → List (FeedbackKey A)
  | [] => []
  | (a,_)::h => feedbackKey U a h :: feedbackKeys U h

lemma feedbackKeys_length (U : Finset A) (h : History A Y) : (feedbackKeys U h).length = h.length := by
  induction h with
  | nil => rfl
  | cons ay h ih => rcases ay with ⟨a,y⟩; simp [feedbackKeys,ih]

lemma actionCount_cons (b a : A) (y : Y) (h : History A Y) :
    actionCount b ((a,y)::h) = actionCount b h + if a = b then 1 else 0 := by
  by_cases he : a = b <;> simp [actionCount,List.countP_cons,he]

lemma outsideCount_cons (U : Finset A) (a : A) (y : Y) (h : History A Y) :
    outsideCount U ((a,y)::h) = outsideCount U h + if a ∉ U then 1 else 0 := by
  by_cases he : a ∉ U <;> simp [outsideCount,List.countP_cons,he]

lemma inside_key_bound (U : Finset A) (h : History A Y) (a : A) (k : ℕ)
    (hk : Sum.inl (a,k) ∈ feedbackKeys U h) : k < actionCount a h := by
  induction h with
  | nil => simp [feedbackKeys] at hk
  | cons ay h ih =>
    rcases ay with ⟨b,y⟩
    rcases List.mem_cons.mp hk with heq | hm
    · by_cases hb : b ∈ U
      · simp only [feedbackKey, if_pos hb, Sum.inl.injEq, Prod.mk.injEq] at heq
        rcases heq with ⟨hab,hk⟩
        subst b
        subst k
        simp [actionCount_cons]
      · simp [feedbackKey,hb] at heq
    · have hh := ih hm
      rw [actionCount_cons]
      omega

lemma outside_key_bound (U : Finset A) (h : History A Y) (k : ℕ)
    (hk : Sum.inr k ∈ feedbackKeys U h) : k < outsideCount U h := by
  induction h with
  | nil => simp [feedbackKeys] at hk
  | cons ay h ih =>
    rcases ay with ⟨a,y⟩
    rcases List.mem_cons.mp hk with heq | hm
    · by_cases ha : a ∈ U
      · simp [feedbackKey,ha] at heq
      · simp only [feedbackKey,if_neg ha,Sum.inr.injEq] at heq
        subst k
        simp [outsideCount_cons,ha]
    · have hh := ih hm
      rw [outsideCount_cons]
      omega

/-- Each fixed transcript consults each latent sample slot at most once. This
is the exact combinatorial freshness condition needed for cylinder probability. -/
theorem feedbackKeys_nodup (U : Finset A) (h : History A Y) : (feedbackKeys U h).Nodup := by
  induction h with
  | nil => exact List.nodup_nil
  | cons ay h ih =>
    rcases ay with ⟨a,y⟩
    apply List.nodup_cons.mpr
    refine ⟨?_,ih⟩
    intro hm
    by_cases ha : a ∈ U
    · rw [feedbackKey,if_pos ha] at hm
      exact Nat.lt_irrefl _ (inside_key_bound U h a _ hm)
    · rw [feedbackKey,if_neg ha] at hm
      exact Nat.lt_irrefl _ (outside_key_bound U h _ hm)

def requestKey (U : Finset A) (h : History A Y) (i : Fin h.length) : FeedbackKey A :=
  (feedbackKeys U h)[i.val]'(by rw [feedbackKeys_length]; exact i.isLt)

lemma requestKey_zero (U : Finset A) (a : A) (y : Y) (h : History A Y) :
    requestKey U ((a,y)::h) ⟨0,by simp⟩ = feedbackKey U a h := rfl
lemma requestKey_succ (U : Finset A) (a : A) (y : Y) (h : History A Y) (i : Fin h.length) :
    requestKey U ((a,y)::h) i.succ = requestKey U h i := rfl

theorem requestKey_injective (U : Finset A) (h : History A Y) : Function.Injective (requestKey U h) := by
  intro i j hij
  apply Fin.ext
  exact (feedbackKeys_nodup U h).getElem_inj_iff.mp hij

def readFeedback (X : Stack A Y) (oracle : ℕ → A → Y) (key : FeedbackKey A) (a : A) : Y :=
  match key with
  | Sum.inl (b,n) => X b n
  | Sum.inr n => oracle n a

lemma readFeedback_key (U : Finset A) (X : Stack A Y) (oracle : ℕ → A → Y) (a : A) (h : History A Y) :
    readFeedback X oracle (feedbackKey U a h) a = feedback U X oracle a h := by
  by_cases ha : a ∈ U <;> simp [readFeedback,feedbackKey,feedback,ha]

/-- The feedback fiber is exactly a finite family of constraints on those
pairwise-distinct latent slots. No probabilistic independence is assumed here. -/
theorem feedbackCompatible_iff_requests (U : Finset A) (X : Stack A Y) (oracle : ℕ → A → Y) (h : History A Y) :
    FeedbackCompatible U X oracle h ↔
      ∀ i : Fin h.length, readFeedback X oracle (requestKey U h i) h[i].1 = h[i].2 := by
  induction h with
  | nil => simp [FeedbackCompatible]
  | cons ay h ih =>
    rcases ay with ⟨a,y⟩
    simp only [List.length_cons]
    rw [Fin.forall_fin_succ]
    change (FeedbackCompatible U X oracle h ∧ feedback U X oracle a h = y) ↔
      (readFeedback X oracle (feedbackKey U a h) a = y ∧
        ∀ i : Fin h.length, readFeedback X oracle (requestKey U h i) h[i].1 = h[i].2)
    rw [readFeedback_key, ← ih]
    exact and_comm

/-- The key tag and the recorded action agree with the U/outside-U split. -/
theorem requestKey_branch (U : Finset A) (h : History A Y) (i : Fin h.length) :
    ((∃ n, requestKey U h i = Sum.inl (h[i].1,n)) ∧ h[i].1 ∈ U) ∨
      ((∃ n, requestKey U h i = Sum.inr n) ∧ h[i].1 ∉ U) := by
  induction h with
  | nil => exact Fin.elim0 i
  | cons ay h ih =>
    rcases ay with ⟨a,y⟩
    refine Fin.cases ?_ (fun j => ?_) i
    · by_cases ha : a ∈ U
      · exact Or.inl ⟨⟨actionCount a h, by simp [requestKey,feedbackKeys,feedbackKey,ha]⟩,ha⟩
      · exact Or.inr ⟨⟨outsideCount U h, by simp [requestKey,feedbackKeys,feedbackKey,ha]⟩,ha⟩
    · exact ih j

end Orthemology.Tranche2.PolicyEmbedding
