import ExecutablePruning

/-!
# Full-row normalized Markov support adapter

This module fixes the relationship between numerical full rows, internal
same-support successors, zero-candidate-exit pairs, and the generic graph
pruning theorem. Allowed pairs are an explicit input: bottom-up licensing and
proper-support winning regions are not rederived here.
-/
namespace HiddenParity

variable {State Pair Model : Type*}
variable [Fintype State] [DecidableEq State] [DecidableEq Pair]

/-- Finite normalized rational transition rows, indexed by hidden model and pair. -/
structure RationalKernel (Model Pair State : Type*) [Fintype State] where
  row : Model → Pair → State → ℚ
  nonnegative : ∀ σ e y, 0 ≤ row σ e y
  normalized : ∀ σ e, ∑ y, row σ e y = 1

/-- Exact support preservation: every live model permits the successor. -/
def internalSuccessors (P : RationalKernel Model Pair State)
    (B : Finset Model) (e : Pair) : Finset State :=
  Finset.univ.filter (fun y => ∀ σ ∈ B, 0 < P.row σ e y)

omit [DecidableEq State] [DecidableEq Pair] in
@[simp] theorem mem_internalSuccessors (P : RationalKernel Model Pair State)
    (B : Finset Model) (e : Pair) (y : State) :
    y ∈ internalSuccessors P B e ↔ ∀ σ ∈ B, 0 < P.row σ e y := by
  simp [internalSuccessors]

/-- No positive candidate transition changes support. -/
def NoExit (P : RationalKernel Model Pair State) (B : Finset Model)
    (θ : Model) (e : Pair) : Prop :=
  ∀ y, 0 < P.row θ e y → y ∈ internalSuccessors P B e

instance noExitDecidable (P : RationalKernel Model Pair State) (B : Finset Model)
    (θ : Model) (e : Pair) : Decidable (NoExit P B θ e) := by
  unfold NoExit
  infer_instance

def zeroExitPairs (P : RationalKernel Model Pair State) (B : Finset Model)
    (θ : Model) (allowed : Finset Pair) : Finset Pair :=
  allowed.filter (NoExit P B θ)

omit [DecidableEq Pair] in
@[simp] theorem mem_zeroExitPairs (P : RationalKernel Model Pair State) (B : Finset Model)
    (θ : Model) (allowed : Finset Pair) (e : Pair) :
    e ∈ zeroExitPairs P B θ allowed ↔ e ∈ allowed ∧ NoExit P B θ e := by
  simp [zeroExitPairs]

omit [DecidableEq Pair] in
/-- Support-based no-exit is exactly internal mass one for normalized nonnegative rows. -/
theorem noExit_iff_internal_mass_one (P : RationalKernel Model Pair State)
    (B : Finset Model) (θ : Model) (e : Pair) :
    NoExit P B θ e ↔ ∑ y ∈ internalSuccessors P B e, P.row θ e y = 1 := by
  constructor
  · intro h
    rw [← P.normalized θ e]
    apply Finset.sum_subset (Finset.subset_univ _)
    intro y _ hNot
    have hNonpos : P.row θ e y ≤ 0 := le_of_not_gt (fun hp => hNot (h y hp))
    exact le_antisymm hNonpos (P.nonnegative θ e y)
  · intro h y hy
    by_contra hNot
    have hsum := Finset.sum_sdiff (f := P.row θ e)
      (Finset.subset_univ (internalSuccessors P B e))
    rw [P.normalized θ e, h] at hsum
    have hzero : ∑ z ∈ Finset.univ \ internalSuccessors P B e, P.row θ e z = 0 := by
      linarith
    have hall := (Finset.sum_eq_zero_iff_of_nonneg
      (fun z (_ : z ∈ Finset.univ \ internalSuccessors P B e) => P.nonnegative θ e z)).mp hzero
    have hyzero := hall y (Finset.mem_sdiff.mpr ⟨Finset.mem_univ y, hNot⟩)
    linarith

omit [DecidableEq State] [DecidableEq Pair] in
/-- A normalized zero-exit candidate has a nonempty internal successor set. -/
theorem noExit_internal_nonempty (P : RationalKernel Model Pair State)
    (B : Finset Model) (θ : Model) (e : Pair) (h : NoExit P B θ e) :
    (internalSuccessors P B e).Nonempty := by
  obtain ⟨y, _, hy⟩ := Finset.exists_ne_zero_of_sum_ne_zero
    (show (∑ y, P.row θ e y) ≠ 0 by rw [P.normalized]; norm_num)
  exact ⟨y, h y (lt_of_le_of_ne (P.nonnegative θ e y) (Ne.symm hy))⟩

omit [DecidableEq State] [DecidableEq Pair] in
/-- Full-row matching preserves zero exit without renormalization. -/
theorem matching_noExit (P : RationalKernel Model Pair State) (B : Finset Model)
    {θ σ : Model} {E : Finset Pair} (hm : Match P.row θ σ E)
    (hNo : ∀ e ∈ E, NoExit P B θ e) : ∀ e ∈ E, NoExit P B σ e := by
  intro e he y hy
  have hrow := congrFun (hm e he) y
  apply hNo e he y
  simpa only [hrow] using hy

omit [DecidableEq State] [DecidableEq Pair] in
/-- For a live candidate, zero exit identifies the internal graph with the
candidate's actual positive-support graph, rather than merely a supplied graph. -/
theorem noExit_internal_eq_candidate_support (P : RationalKernel Model Pair State)
    (B : Finset Model) (θ : Model) (hθ : θ ∈ B) (e : Pair)
    (h : NoExit P B θ e) :
    internalSuccessors P B e = Finset.univ.filter (fun y => 0 < P.row θ e y) := by
  ext y
  constructor
  · intro hy
    exact Finset.mem_filter.mpr ⟨Finset.mem_univ y,
      (mem_internalSuccessors P B e y).mp hy θ hθ⟩
  · intro hy
    exact h y (Finset.mem_filter.mp hy).2

/-- The original qualifying target predicate for this normalized Markov input,
independent of pruning, explicitly includes allowed pairs and zero exit. -/
def MarkovQualifying (P : RationalKernel Model Pair State) (source : Pair → State)
    (B : Finset Model) (priority : Model → Pair → ℕ) (θ : Model)
    (allowed E : Finset Pair) : Prop :=
  E ⊆ allowed ∧ (∀ e ∈ E, NoExit P B θ e) ∧
    IsEndComponent source (internalSuccessors P B) E ∧
    ∀ σ ∈ B, Match P.row θ σ E → ∃ d, IsMinimum (priority σ) E d ∧ d % 2 = 0

theorem markovQualifying_iff (P : RationalKernel Model Pair State) (source : Pair → State)
    (B : Finset Model) (priority : Model → Pair → ℕ) (θ : Model)
    (allowed E : Finset Pair) :
    MarkovQualifying P source B priority θ allowed E ↔
      E ⊆ zeroExitPairs P B θ allowed ∧
        Valid (endComponentFamily source (internalSuccessors P B)) B P.row priority θ E := by
  constructor
  · rintro ⟨hA, hN, hEC, hP⟩
    exact ⟨fun e he => (mem_zeroExitPairs P B θ allowed e).mpr ⟨hA he, hN e he⟩,
      hEC, hP⟩
  · rintro ⟨hE, hEC, hP⟩
    refine ⟨?_, ?_, hEC, hP⟩
    · intro e he
      exact ((mem_zeroExitPairs P B θ allowed e).mp (hE he)).1
    · intro e he
      exact ((mem_zeroExitPairs P B θ allowed e).mp (hE he)).2

/-- Executable target-state solver on actual normalized full transition rows. -/
def markovTargetStates (P : RationalKernel Model Pair State) (source : Pair → State)
    (B : Finset Model) (priority : Model → Pair → ℕ) (θ : Model)
    (allowed : Finset Pair) : Finset State :=
  executableTargetStates source (internalSuccessors P B) B P.row priority θ
    (zeroExitPairs P B θ allowed)

/-- End-to-end normalized-row target equality. Licensing is the supplied allowed
pair set; neither MEC correctness nor row/support consistency is a hypothesis. -/
theorem markovTargetStates_exact (P : RationalKernel Model Pair State) (source : Pair → State)
    (B : Finset Model) (priority : Model → Pair → ℕ) (θ : Model)
    (allowed : Finset Pair) (s : State) :
    s ∈ markovTargetStates P source B priority θ allowed ↔
      ∃ E, MarkovQualifying P source B priority θ allowed E ∧ s ∈ usedStates source E := by
  rw [markovTargetStates, executable_targetStates_exact]
  constructor
  · rintro ⟨E, hEU, hV, hs⟩
    exact ⟨E, (markovQualifying_iff P source B priority θ allowed E).mpr ⟨hEU, hV⟩, hs⟩
  · rintro ⟨E, hE, hs⟩
    obtain ⟨hEU, hV⟩ := (markovQualifying_iff P source B priority θ allowed E).mp hE
    exact ⟨E, hEU, hV, hs⟩

end HiddenParity
