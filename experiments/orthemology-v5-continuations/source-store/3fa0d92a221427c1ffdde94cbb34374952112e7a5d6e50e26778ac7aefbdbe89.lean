import P02A2.ObserverCore

/-! Finite-register renaming for the actual P02-L1 LOOP grammar. Only an
injection on the finite source register set is required; no global store
bijection or assumed compiler-correctness predicate is used. -/
namespace P02A2.LoopRenaming
open P02A2.ObserverCore

 def exprRegs : Expr → Finset ℕ
  | .constant _ => ∅
  | .reg r => {r}
  | .add a b | .sub a b | .mul a b | .div a b | .mod a b | .le a b | .eq a b =>
      exprRegs a ∪ exprRegs b
  | .pow2 a => exprRegs a

def stmtRegs : Stmt → Finset ℕ
  | .skip => ∅
  | .set r e => insert r (exprRegs e)
  | .seq s t => stmtRegs s ∪ stmtRegs t
  | .loop r e s => insert r (exprRegs e ∪ stmtRegs s)
  | .branch e s t => exprRegs e ∪ (stmtRegs s ∪ stmtRegs t)

def renameExpr (ρ : ℕ → ℕ) : Expr → Expr
  | .constant n => .constant n
  | .reg r => .reg (ρ r)
  | .add a b => .add (renameExpr ρ a) (renameExpr ρ b)
  | .sub a b => .sub (renameExpr ρ a) (renameExpr ρ b)
  | .mul a b => .mul (renameExpr ρ a) (renameExpr ρ b)
  | .div a b => .div (renameExpr ρ a) (renameExpr ρ b)
  | .mod a b => .mod (renameExpr ρ a) (renameExpr ρ b)
  | .le a b => .le (renameExpr ρ a) (renameExpr ρ b)
  | .eq a b => .eq (renameExpr ρ a) (renameExpr ρ b)
  | .pow2 a => .pow2 (renameExpr ρ a)

def renameStmt (ρ : ℕ → ℕ) : Stmt → Stmt
  | .skip => .skip
  | .set r e => .set (ρ r) (renameExpr ρ e)
  | .seq s t => .seq (renameStmt ρ s) (renameStmt ρ t)
  | .loop r e s => .loop (ρ r) (renameExpr ρ e) (renameStmt ρ s)
  | .branch e s t => .branch (renameExpr ρ e) (renameStmt ρ s) (renameStmt ρ t)

def Agrees (R : Finset ℕ) (ρ : ℕ → ℕ) (σ τ : Store) : Prop :=
  ∀ r ∈ R, τ (ρ r) = σ r

theorem agrees_update {R : Finset ℕ} {ρ : ℕ → ℕ}
    (hρ : Set.InjOn ρ (↑R : Set ℕ)) {σ τ : Store} (h : Agrees R ρ σ τ)
    {r : ℕ} (hr : r ∈ R) (v : ℕ) :
    Agrees R ρ (Function.update σ r v) (Function.update τ (ρ r) v) := by
  intro j hj
  by_cases he : j = r
  · subst j
    simp
  · have hne : ρ j ≠ ρ r := fun hval => he (hρ hj hr hval)
    simp [Function.update_of_ne he, Function.update_of_ne hne, h j hj]

theorem evalExpr_rename (ρ : ℕ → ℕ) (e : Expr) (R : Finset ℕ)
    (hR : exprRegs e ⊆ R) (σ τ : Store) (h : Agrees R ρ σ τ) :
    evalExpr (renameExpr ρ e) τ = evalExpr e σ := by
  induction e with
  | constant n => rfl
  | reg r => exact h r (hR (by simp [exprRegs]))
  | add a b iha ihb | sub a b iha ihb | mul a b iha ihb | div a b iha ihb |
    mod a b iha ihb | le a b iha ihb | eq a b iha ihb =>
      have ha : exprRegs a ⊆ R := (Finset.union_subset_iff.mp hR).1
      have hb : exprRegs b ⊆ R := (Finset.union_subset_iff.mp hR).2
      simp only [renameExpr, evalExpr, iha ha, ihb hb]
  | pow2 a ih => exact congrArg (2^·) (ih hR)

theorem runLoop_agrees {R : Finset ℕ} {ρ : ℕ → ℕ}
    (hρ : Set.InjOn ρ (↑R : Set ℕ)) (body body' : Store → Store)
    (hb : ∀ σ τ, Agrees R ρ σ τ → Agrees R ρ (body σ) (body' τ))
    {r : ℕ} (hr : r ∈ R) (k : ℕ) (σ τ : Store) (h : Agrees R ρ σ τ) :
    Agrees R ρ (runLoop body r k σ) (runLoop body' (ρ r) k τ) := by
  induction k with
  | zero => exact h
  | succ k ih => exact hb _ _ (agrees_update hρ ih hr k)

theorem exec_rename (ρ : ℕ → ℕ) (s : Stmt) (R : Finset ℕ)
    (hρ : Set.InjOn ρ (↑R : Set ℕ)) (hR : stmtRegs s ⊆ R)
    (σ τ : Store) (h : Agrees R ρ σ τ) :
    Agrees R ρ (exec s σ) (exec (renameStmt ρ s) τ) := by
  induction s generalizing σ τ with
  | skip => exact h
  | set r e =>
      have hr := (Finset.insert_subset_iff.mp hR).1
      have he := (Finset.insert_subset_iff.mp hR).2
      simp only [renameStmt, exec]
      rw [evalExpr_rename ρ e R he σ τ h]
      exact agrees_update hρ h hr _
  | seq s t ihs iht =>
      have hs := (Finset.union_subset_iff.mp hR).1
      have ht := (Finset.union_subset_iff.mp hR).2
      exact iht ht _ _ (ihs hs σ τ h)
  | loop r e s ih =>
      have hr := (Finset.insert_subset_iff.mp hR).1
      have hs := (Finset.union_subset_iff.mp (Finset.insert_subset_iff.mp hR).2).2
      have he := (Finset.union_subset_iff.mp (Finset.insert_subset_iff.mp hR).2).1
      simp only [renameStmt, exec]
      rw [evalExpr_rename ρ e R he σ τ h]
      exact runLoop_agrees hρ _ _ (fun σ τ h => ih hs σ τ h) hr _ σ τ h
  | branch e s t ihs iht =>
      have he := (Finset.union_subset_iff.mp hR).1
      have hs := (Finset.union_subset_iff.mp (Finset.union_subset_iff.mp hR).2).1
      have ht := (Finset.union_subset_iff.mp (Finset.union_subset_iff.mp hR).2).2
      simp only [renameStmt, exec]
      rw [evalExpr_rename ρ e R he σ τ h]
      split_ifs
      · exact iht ht σ τ h
      · exact ihs hs σ τ h

theorem renameExpr_id (e : Expr) : renameExpr id e = e := by
  induction e <;> simp_all [renameExpr]

theorem evalExpr_congr (e : Expr) (σ τ : Store)
    (h : ∀ r ∈ exprRegs e, τ r = σ r) : evalExpr e τ = evalExpr e σ := by
  simpa only [renameExpr_id] using evalExpr_rename id e (exprRegs e) (by rfl) σ τ h

theorem exprRegs_rename (ρ : ℕ → ℕ) (e : Expr) :
    exprRegs (renameExpr ρ e) = (exprRegs e).image ρ := by
  induction e <;> simp_all [renameExpr, exprRegs, Finset.image_union]

theorem stmtRegs_rename (ρ : ℕ → ℕ) (s : Stmt) :
    stmtRegs (renameStmt ρ s) = (stmtRegs s).image ρ := by
  induction s <;> simp_all [renameStmt, stmtRegs, exprRegs_rename,
    Finset.image_union, Finset.image_insert]

theorem runLoop_frame (body : Store → Store) (index r : ℕ) (hri : r ≠ index)
    (hbody : ∀ σ, body σ r = σ r) (k : ℕ) (σ : Store) :
    runLoop body index k σ r = σ r := by
  induction k with
  | zero => rfl
  | succ k ih => simp only [runLoop, hbody, Function.update_of_ne hri, ih]

theorem exec_frame (s : Stmt) (σ : Store) (r : ℕ) (hr : r ∉ stmtRegs s) :
    exec s σ r = σ r := by
  induction s generalizing σ with
  | skip => rfl
  | set i e =>
      have hri : r ≠ i := by intro h; subst r; exact hr (Finset.mem_insert_self _ _)
      exact Function.update_of_ne hri _ _
  | seq s t ihs iht =>
      have hs : r ∉ stmtRegs s := by intro h; exact hr (Finset.mem_union_left _ h)
      have ht : r ∉ stmtRegs t := by intro h; exact hr (Finset.mem_union_right _ h)
      rw [exec, iht _ ht, ihs _ hs]
  | loop i e s ih =>
      have hri : r ≠ i := by intro h; subst r; exact hr (Finset.mem_insert_self _ _)
      have hs : r ∉ stmtRegs s := by intro h; exact hr (Finset.mem_insert_of_mem (Finset.mem_union_right _ h))
      exact runLoop_frame (exec s) i r hri (fun σ => ih σ hs) _ σ
  | branch e s t ihs iht =>
      have hs : r ∉ stmtRegs s := by intro h; exact hr (Finset.mem_union_right _ (Finset.mem_union_left _ h))
      have ht : r ∉ stmtRegs t := by intro h; exact hr (Finset.mem_union_right _ (Finset.mem_union_right _ h))
      simp only [exec]
      split_ifs
      · exact iht σ ht
      · exact ihs σ hs

theorem renamed_frame (ρ : ℕ → ℕ) (s : Stmt) (R : Finset ℕ) (hs : stmtRegs s ⊆ R)
    (τ : Store) (r : ℕ) (hr : r ∉ R.image ρ) : exec (renameStmt ρ s) τ r = τ r := by
  apply exec_frame
  rw [stmtRegs_rename]
  exact fun h => hr (Finset.image_mono ρ hs h)

def OutsideEq (R : Finset ℕ) (ρ : ℕ → ℕ) (caller target : Store) : Prop :=
  ∀ r, r ∉ R.image ρ → target r = caller r

theorem outsideEq_update {R : Finset ℕ} {ρ : ℕ → ℕ} {caller target : Store}
    (h : OutsideEq R ρ caller target) {r : ℕ} (hr : r ∈ R) (v : ℕ) :
    OutsideEq R ρ caller (Function.update target (ρ r) v) := by
  intro j hj
  have hne : j ≠ ρ r := by intro he; subst j; exact hj (Finset.mem_image.mpr ⟨r, hr, rfl⟩)
  simpa only [Function.update_of_ne hne] using h j hj

def resetList (ρ : ℕ → ℕ) : List ℕ → Stmt
  | [] => .skip
  | r::rs => .seq (.set (ρ r) (.constant 0)) (resetList ρ rs)

theorem resetList_apply (ρ : ℕ → ℕ) (rs : List ℕ) (τ : Store) (j : ℕ) :
    exec (resetList ρ rs) τ j = if j ∈ rs.map ρ then 0 else τ j := by
  induction rs generalizing τ with
  | nil => simp [resetList, exec]
  | cons r rs ih =>
      simp only [resetList, exec, evalExpr, ih, List.map_cons, List.mem_cons]
      by_cases he : j = ρ r <;> by_cases ht : j ∈ rs.map ρ <;>
        simp [he, ht, Function.update_apply]

theorem resetList_agrees (ρ : ℕ → ℕ) (rs : List ℕ) (caller : Store) :
    Agrees rs.toFinset ρ (fun _ => 0) (exec (resetList ρ rs) caller) := by
  intro r hr
  rw [resetList_apply]
  have hm : ρ r ∈ rs.map ρ := List.mem_map.mpr ⟨r, List.mem_toFinset.mp hr, rfl⟩
  simp [hm]

theorem resetList_outside (ρ : ℕ → ℕ) (rs : List ℕ) (caller : Store) :
    OutsideEq rs.toFinset ρ caller (exec (resetList ρ rs) caller) := by
  intro j hj
  rw [resetList_apply]
  have hn : j ∉ rs.map ρ := by
    intro hm
    rcases List.mem_map.mp hm with ⟨r, hr, he⟩
    exact hj (Finset.mem_image.mpr ⟨r, List.mem_toFinset.mpr hr, he⟩)
  simp [hn]

def loadArgs (ρ : ℕ → ℕ) : List (ℕ × Expr) → Stmt
  | [] => .skip
  | (r,e)::args => .seq (.set (ρ r) e) (loadArgs ρ args)

def sourceLoad : List (ℕ × Expr) → Store → Store → Store
  | [], _, source => source
  | (r,e)::args, caller, source => sourceLoad args caller
      (Function.update source r (evalExpr e caller))

def ArgsFresh (R : Finset ℕ) (ρ : ℕ → ℕ) (args : List (ℕ × Expr)) : Prop :=
  ∀ a ∈ args, a.1 ∈ R ∧ Disjoint (exprRegs a.2) (R.image ρ)

theorem evalExpr_outside (e : Expr) (R : Finset ℕ) (ρ : ℕ → ℕ)
    (caller target : Store) (he : Disjoint (exprRegs e) (R.image ρ))
    (h : OutsideEq R ρ caller target) : evalExpr e target = evalExpr e caller := by
  apply evalExpr_congr
  intro r hr
  exact h r (fun hm => Finset.disjoint_left.mp he hr hm)

theorem loadArgs_correct (ρ : ℕ → ℕ) (args : List (ℕ × Expr)) (R : Finset ℕ)
    (hρ : Set.InjOn ρ (↑R : Set ℕ)) (ha : ArgsFresh R ρ args)
    (caller source target : Store) (hs : Agrees R ρ source target)
    (ho : OutsideEq R ρ caller target) :
    Agrees R ρ (sourceLoad args caller source) (exec (loadArgs ρ args) target) ∧
    OutsideEq R ρ caller (exec (loadArgs ρ args) target) := by
  induction args generalizing source target with
  | nil => exact ⟨hs, ho⟩
  | cons a args ih =>
      rcases a with ⟨r,e⟩
      have hhead := ha (r,e) (by simp)
      have htail : ArgsFresh R ρ args := by
        intro a ha'
        exact ha a (List.mem_cons_of_mem _ ha')
      simp only [loadArgs, sourceLoad, exec]
      rw [evalExpr_outside e R ρ caller target hhead.2 ho]
      exact ih htail _ _ (agrees_update hρ hs hhead.1 _)
        (outsideEq_update ho hhead.1 _)

def inlineCode (ρ : ℕ → ℕ) (rs : List ℕ) (args : List (ℕ × Expr))
    (body : Stmt) (output destination : ℕ) : Stmt :=
  .seq (resetList ρ rs) (.seq (loadArgs ρ args)
    (.seq (renameStmt ρ body) (.set destination (.reg (ρ output)))))

theorem inlineCode_correct (ρ : ℕ → ℕ) (rs : List ℕ) (args : List (ℕ × Expr))
    (body : Stmt) (output destination : ℕ)
    (hρ : Set.InjOn ρ (↑rs.toFinset : Set ℕ))
    (hb : stmtRegs body ⊆ rs.toFinset) (hout : output ∈ rs.toFinset)
    (ha : ArgsFresh rs.toFinset ρ args) (caller : Store) :
    exec (inlineCode ρ rs args body output destination) caller destination =
      exec body (sourceLoad args caller (fun _ => 0)) output ∧
    ∀ j, j ≠ destination → j ∉ rs.toFinset.image ρ →
      exec (inlineCode ρ rs args body output destination) caller j = caller j := by
  let reset := exec (resetList ρ rs) caller
  let loaded := exec (loadArgs ρ args) reset
  let finished := exec (renameStmt ρ body) loaded
  have hl := loadArgs_correct ρ args rs.toFinset hρ ha caller (fun _ => 0) reset
    (resetList_agrees ρ rs caller) (resetList_outside ρ rs caller)
  have hm := exec_rename ρ body rs.toFinset hρ hb
    (sourceLoad args caller (fun _ => 0)) loaded hl.1
  constructor
  · change Function.update finished destination (finished (ρ output)) destination = _
    rw [Function.update_self]
    exact hm output hout
  · intro j hj hjR
    change Function.update finished destination (finished (ρ output)) j = _
    rw [Function.update_of_ne hj]
    change exec (renameStmt ρ body) loaded j = caller j
    rw [renamed_frame ρ body rs.toFinset hb loaded j hjR]
    exact hl.2 j hjR

end P02A2.LoopRenaming
