import Std

/-!
General exact-reset continuation theorem. No finite-instance enumeration is used.
Every state is a complete Boolean valuation. `coords` is any exhaustive finite list.
-/
namespace ResetContinuation

universe u v w s

abbrev State (I : Type u) := I → Bool

def Essential {I : Type u} {O : Type v} (f : State I → O) (i : I) : Prop :=
  ∃ x y, (∀ j, j ≠ i → x j = y j) ∧ f x ≠ f y

inductive Closure {I : Type u} {O : Type v} {A : Type w}
    (h : State I → O) (T : A → State I → State I) : I → Prop where
  | output {i} : Essential h i → Closure h T i
  | dependency {i j} (a : A) : Closure h T j →
      Essential (fun x => T a x j) i → Closure h T i

inductive Action (I : Type u) (A : Type w) where
  | reset : I → Bool → Action I A
  | coupled : A → Action I A

def reset {I : Type u} [DecidableEq I] (i : I) (b : Bool) (x : State I) : State I :=
  fun j => if j = i then b else x j

def step {I : Type u} [DecidableEq I] {A : Type w}
    (T : A → State I → State I) : Action I A → State I → State I
  | .reset i b, x => reset i b x
  | .coupled a, x => T a x

def run {I : Type u} [DecidableEq I] {A : Type w}
    (T : A → State I → State I) : List (Action I A) → State I → State I
  | [], x => x
  | a :: as, x => run T as (step T a x)

def ContinuationEq {I : Type u} [DecidableEq I] {O : Type v} {A : Type w}
    (h : State I → O) (T : A → State I → State I) (x y : State I) : Prop :=
  ∀ word, h (run T word x) = h (run T word y)

def Agree {I : Type u} (P : I → Prop) (x y : State I) : Prop :=
  ∀ i, P i → x i = y i

theorem run_append {I : Type u} [DecidableEq I] {A : Type w}
    (T : A → State I → State I) (p q : List (Action I A)) (x : State I) :
    run T (p ++ q) x = run T q (run T p x) := by
  induction p generalizing x with
  | nil => rfl
  | cons a p ih => exact ih (step T a x)

theorem determined_aux {I : Type u} [DecidableEq I] {O : Type v}
    (f : State I → O) (l : List I) {x y : State I}
    (hdiff : ∀ j, x j ≠ y j → j ∈ l)
    (hess : Agree (Essential f) x y) : f x = f y := by
  classical
  induction l generalizing x with
  | nil =>
      have hxy : x = y := by
        funext j
        apply Classical.byContradiction
        intro hne
        exact List.not_mem_nil (hdiff j hne)
      rw [hxy]
  | cons i l ih =>
      let z := reset i (y i) x
      have hxz : f x = f z := by
        by_cases hi : Essential f i
        · have eqxz : x = z := by
            funext j
            by_cases hji : j = i
            · subst j
              simpa [z, reset] using hess i hi
            · simp [z, reset, hji]
          rw [eqxz]
        · apply Classical.byContradiction
          intro hne
          apply hi
          refine ⟨x, z, ?_, hne⟩
          intro j hji
          simp [z, reset, hji]
      apply hxz.trans
      apply ih
      · intro j hne
        have hji : j ≠ i := by
          intro e
          subst j
          exact hne (by simp [z, reset])
        have hxy : x j ≠ y j := by simpa [z, reset, hji] using hne
        exact (List.mem_cons.mp (hdiff j hxy)).resolve_left hji
      · intro j hj
        by_cases hji : j = i
        · subst j
          simp [z, reset]
        · simpa [z, reset, hji] using hess j hj

theorem essential_determines {I : Type u} [DecidableEq I] {O : Type v}
    (coords : List I) (covers : ∀ i, i ∈ coords) (f : State I → O)
    {x y : State I} (hess : Agree (Essential f) x y) : f x = f y :=
  determined_aux f coords (fun j _ => covers j) hess

/-- A concrete common word resets all listed coordinates except the exposed one. -/
def contextWord {I : Type u} [DecidableEq I] {A : Type w}
    (i : I) (u : State I) : List I → List (Action I A)
  | [] => []
  | j :: js => if j = i then contextWord i u js
      else Action.reset j (u j) :: contextWord i u js

theorem contextWord_apply {I : Type u} [DecidableEq I] {A : Type w}
    (T : A → State I → State I) (i : I) (u x : State I) (l : List I) (j : I) :
    run T (contextWord (A := A) i u l) x j =
      if j ≠ i ∧ j ∈ l then u j else x j := by
  induction l generalizing x with
  | nil => simp [contextWord, run]
  | cons k l ih =>
      by_cases hki : k = i
      · subst k
        by_cases hji : j = i
        · subst j
          simp [contextWord, ih]
        · simp [contextWord, ih, hji]
      · simp only [contextWord, if_neg hki, run, step]
        rw [ih]
        by_cases hji : j = i
        · subst j
          simp [hki, Ne.symm hki, reset]
        · by_cases hjk : j = k
          · subst j
            simp [hki, reset]
          · simp [hji, hjk, reset]

theorem contextWord_realizes {I : Type u} [DecidableEq I] {A : Type w}
    (coords : List I) (covers : ∀ i, i ∈ coords)
    (T : A → State I → State I) (i : I) (u x : State I) (hi : x i = u i) :
    run T (contextWord (A := A) i u coords) x = u := by
  funext j
  rw [contextWord_apply]
  by_cases hji : j = i
  · subst j
    simpa using hi
  · simp [hji, covers j]

theorem witness_coordinate_diff {I : Type u} {O : Type v}
    (f : State I → O) {i : I} {u v : State I}
    (hother : ∀ j, j ≠ i → u j = v j) (hout : f u ≠ f v) : u i ≠ v i := by
  intro hi
  apply hout
  congr 1
  funext j
  by_cases hji : j = i
  · subst j
    exact hi
  · exact hother j hji

theorem bool_pair_match (a b c d : Bool) (hab : a ≠ b) (hcd : c ≠ d) :
    (a = c ∧ b = d) ∨ (a = d ∧ b = c) := by
  cases a <;> cases b <;> cases c <;> cases d <;> simp_all

/-- Essentiality can expose every pair differing at that coordinate by a common reset word. -/
theorem expose_essential {I : Type u} [DecidableEq I] {O : Type v} {A : Type w}
    (coords : List I) (covers : ∀ i, i ∈ coords)
    (T : A → State I → State I) (f : State I → O) {i : I}
    (he : Essential f i) {x y : State I} (hxy : x i ≠ y i) :
    ∃ word : List (Action I A), f (run T word x) ≠ f (run T word y) := by
  obtain ⟨u, v, hother, hout⟩ := he
  have huv := witness_coordinate_diff f hother hout
  have hcontext : contextWord (A := A) i u coords = contextWord i v coords := by
    clear covers
    induction coords with
    | nil => rfl
    | cons j js ih =>
        by_cases hji : j = i
        · simp [contextWord, hji, ih]
        · simp [contextWord, hji, hother j hji, ih]
  refine ⟨contextWord i u coords, ?_⟩
  rcases bool_pair_match (x i) (y i) (u i) (v i) hxy huv with h | h
  · rw [contextWord_realizes coords covers T i u x h.1]
    have hy : run T (contextWord i u coords) y = v := by
      rw [hcontext]
      exact contextWord_realizes coords covers T i v y h.2
    rw [hy]
    exact hout
  · have hx : run T (contextWord i u coords) x = v := by
      rw [hcontext]
      exact contextWord_realizes coords covers T i v x h.1
    rw [hx, contextWord_realizes coords covers T i u y h.2]
    exact Ne.symm hout

/-- The strengthened necessity statement, for arbitrary surrounding differences. -/
theorem closure_distinguishes {I : Type u} [DecidableEq I] {O : Type v} {A : Type w}
    (coords : List I) (covers : ∀ i, i ∈ coords)
    (h : State I → O) (T : A → State I → State I) {i : I}
    (hi : Closure h T i) :
    ∀ x y : State I, x i ≠ y i →
      ∃ word, h (run T word x) ≠ h (run T word y) := by
  induction hi with
  | output he =>
      intro x y hxy
      exact expose_essential coords covers T h he hxy
  | @dependency i j a hj he ih =>
      intro x y hxy
      obtain ⟨pre, hp⟩ := expose_essential coords covers T (fun z => T a z j) he hxy
      obtain ⟨suffix, hs⟩ := ih (T a (run T pre x)) (T a (run T pre y)) hp
      refine ⟨pre ++ Action.coupled a :: suffix, ?_⟩
      simpa [run_append, run, step] using hs

theorem closure_output {I : Type u} [DecidableEq I] {O : Type v} {A : Type w}
    (coords : List I) (covers : ∀ i, i ∈ coords)
    (h : State I → O) (T : A → State I → State I) {x y : State I}
    (ha : Agree (Closure h T) x y) : h x = h y :=
  essential_determines coords covers h (fun i hi => ha i (Closure.output hi))

theorem closure_step {I : Type u} [DecidableEq I] {O : Type v} {A : Type w}
    (coords : List I) (covers : ∀ i, i ∈ coords)
    (h : State I → O) (T : A → State I → State I) (a : Action I A)
    {x y : State I} (ha : Agree (Closure h T) x y) :
    Agree (Closure h T) (step T a x) (step T a y) := by
  intro j hj
  cases a with
  | reset i b =>
      by_cases hji : j = i
      · simp [step, reset, hji]
      · simpa [step, reset, hji] using ha j hj
  | coupled a =>
      exact essential_determines coords covers (fun z => T a z j)
        (fun i hi => ha i (Closure.dependency a hj hi))

theorem agreement_continuation {I : Type u} [DecidableEq I] {O : Type v} {A : Type w}
    (coords : List I) (covers : ∀ i, i ∈ coords)
    (h : State I → O) (T : A → State I → State I) {x y : State I}
    (ha : Agree (Closure h T) x y) : ContinuationEq h T x y := by
  intro word
  induction word generalizing x y with
  | nil => exact closure_output coords covers h T ha
  | cons a word ih =>
      exact ih (closure_step coords covers h T a ha)

/-- Main characterization: independently defined behavioral and coordinate relations coincide. -/
theorem continuation_iff_agreement {I : Type u} [DecidableEq I] {O : Type v} {A : Type w}
    (coords : List I) (covers : ∀ i, i ∈ coords)
    (h : State I → O) (T : A → State I → State I) (x y : State I) :
    ContinuationEq h T x y ↔ Agree (Closure h T) x y := by
  constructor
  · intro hc i hi
    apply Classical.byContradiction
    intro hne
    obtain ⟨word, hw⟩ := closure_distinguishes coords covers h T hi x y hne
    exact hw (hc word)
  · exact agreement_continuation coords covers h T

/-- The stages from the source theorem, defined without using behavioral equivalence. -/
def Stage {I : Type u} {O : Type v} {A : Type w}
    (h : State I → O) (T : A → State I → State I) : Nat → I → Prop
  | 0, i => Essential h i
  | n + 1, i => Stage h T n i ∨
      ∃ a j, Stage h T n j ∧ Essential (fun x => T a x j) i

theorem stage_subset_closure {I : Type u} {O : Type v} {A : Type w}
    (h : State I → O) (T : A → State I → State I) (n : Nat) {i : I}
    (hi : Stage h T n i) : Closure h T i := by
  induction n generalizing i with
  | zero => exact Closure.output hi
  | succ n ih =>
      rcases hi with hi | ⟨a, j, hj, he⟩
      · exact ih hi
      · exact Closure.dependency a (ih hj) he

theorem closure_iff_stage {I : Type u} {O : Type v} {A : Type w}
    (h : State I → O) (T : A → State I → State I) (i : I) :
    Closure h T i ↔ ∃ n, Stage h T n i := by
  constructor
  · intro hi
    induction hi with
    | output he => exact ⟨0, he⟩
    | @dependency i j a hj he ih =>
        obtain ⟨n, hn⟩ := ih
        exact ⟨n + 1, Or.inr ⟨a, j, hn, he⟩⟩
  · rintro ⟨n, hn⟩
    exact stage_subset_closure h T n hn

theorem closure_least {I : Type u} {O : Type v} {A : Type w}
    (h : State I → O) (T : A → State I → State I) (P : I → Prop)
    (base : ∀ i, Essential h i → P i)
    (back : ∀ a i j, P j → Essential (fun x => T a x j) i → P i)
    {i : I} (hi : Closure h T i) : P i := by
  induction hi with
  | output he => exact base _ he
  | dependency a hj he ih => exact back a _ _ ih he

abbrev ProjectionState {I : Type u} {O : Type v} {A : Type w}
    (h : State I → O) (T : A → State I → State I) :=
  {i : I // Closure h T i} → Bool

def project {I : Type u} {O : Type v} {A : Type w}
    (h : State I → O) (T : A → State I → State I) (x : State I) :
    ProjectionState h T := fun i => x i.val

noncomputable def fill {I : Type u} {O : Type v} {A : Type w}
    (h : State I → O) (T : A → State I → State I)
    (z : ProjectionState h T) : State I := by
  classical
  exact fun i => if hi : Closure h T i then z ⟨i, hi⟩ else false

theorem project_fill {I : Type u} {O : Type v} {A : Type w}
    (h : State I → O) (T : A → State I → State I) (z : ProjectionState h T) :
    project h T (fill h T z) = z := by
  funext i
  simp [project, fill, i.property]

theorem project_eq_iff_agree {I : Type u} {O : Type v} {A : Type w}
    (h : State I → O) (T : A → State I → State I) (x y : State I) :
    project h T x = project h T y ↔ Agree (Closure h T) x y := by
  constructor
  · intro he i hi
    exact congrFun he ⟨i, hi⟩
  · intro ha
    funext i
    exact ha i.val i.property

theorem fill_project_agrees {I : Type u} {O : Type v} {A : Type w}
    (h : State I → O) (T : A → State I → State I) (x : State I) :
    Agree (Closure h T) (fill h T (project h T x)) x := by
  apply (project_eq_iff_agree h T _ _).mp
  exact project_fill h T (project h T x)

/-- A deterministic summary must decode the present output and update under each same label. -/
structure Summary {I : Type u} [DecidableEq I] {O : Type v} {A : Type w}
    (h : State I → O) (T : A → State I → State I) (S : Type s) where
  encode : State I → S
  decode : S → O
  update : Action I A → S → S
  decode_encode : ∀ x, decode (encode x) = h x
  update_encode : ∀ a x, update a (encode x) = encode (step T a x)

/-- Explicit zero-filled implementation of the dependency projection. -/
noncomputable def projection_summary {I : Type u} [DecidableEq I]
    {O : Type v} {A : Type w}
    (coords : List I) (covers : ∀ i, i ∈ coords)
    (h : State I → O) (T : A → State I → State I) :
    Summary h T (ProjectionState h T) where
  encode := project h T
  decode := fun z => h (fill h T z)
  update := fun a z => project h T (step T a (fill h T z))
  decode_encode := fun x => closure_output coords covers h T (fill_project_agrees h T x)
  update_encode := by
    intro a x
    apply (project_eq_iff_agree h T _ _).mpr
    exact closure_step coords covers h T a (fill_project_agrees h T x)

theorem summary_eq_continuation {I : Type u} [DecidableEq I]
    {O : Type v} {A : Type w} {S : Type s}
    (h : State I → O) (T : A → State I → State I) (M : Summary h T S)
    {x y : State I} (he : M.encode x = M.encode y) : ContinuationEq h T x y := by
  intro word
  have hrun : ∀ (w : List (Action I A)) (x y : State I),
      M.encode x = M.encode y → M.encode (run T w x) = M.encode (run T w y) := by
    intro w
    induction w with
    | nil => intro x y he; exact he
    | cons a w ih =>
        intro x y he
        apply ih
        rw [← M.update_encode, ← M.update_encode, he]
  rw [← M.decode_encode, ← M.decode_encode, hrun word x y he]

/-- Coarseness: no continuation-complete deterministic summary can merge two projection states. -/
theorem every_summary_refines_projection {I : Type u} [DecidableEq I]
    {O : Type v} {A : Type w} {S : Type s}
    (coords : List I) (covers : ∀ i, i ∈ coords)
    (h : State I → O) (T : A → State I → State I) (M : Summary h T S)
    {x y : State I} (he : M.encode x = M.encode y) : project h T x = project h T y := by
  apply (project_eq_iff_agree h T x y).mpr
  apply (continuation_iff_agreement coords covers h T x y).mp
  exact summary_eq_continuation h T M he

/-- A recover function exists on the entire summary type, including unreachable summary values. -/
theorem summary_factors_projection {I : Type u} [DecidableEq I]
    {O : Type v} {A : Type w} {S : Type s}
    (coords : List I) (covers : ∀ i, i ∈ coords)
    (h : State I → O) (T : A → State I → State I) (M : Summary h T S) :
    ∃ recover : S → ProjectionState h T, ∀ x, recover (M.encode x) = project h T x := by
  classical
  let recover : S → ProjectionState h T := fun s =>
    if hs : ∃ x, M.encode x = s then project h T (Classical.choose hs) else fun _ => false
  refine ⟨recover, ?_⟩
  intro x
  have hs : ∃ y, M.encode y = M.encode x := ⟨x, rfl⟩
  simp only [recover, dif_pos hs]
  exact every_summary_refines_projection coords covers h T M (Classical.choose_spec hs)

/-- The exact original finite-dimensional product, uniformly for all natural dimensions. -/
theorem fin_continuation_iff_agreement {n : Nat} {O : Type v} {A : Type w}
    (h : State (Fin n) → O) (T : A → State (Fin n) → State (Fin n))
    (x y : State (Fin n)) :
    ContinuationEq h T x y ↔ Agree (Closure h T) x y := by
  apply continuation_iff_agreement (List.ofFn (fun i : Fin n => i))
  intro i
  exact List.mem_ofFn.mpr ⟨i, rfl⟩

#print axioms continuation_iff_agreement
#print axioms closure_iff_stage
#print axioms projection_summary
#print axioms every_summary_refines_projection
#print axioms summary_factors_projection
#print axioms fin_continuation_iff_agreement

end ResetContinuation
