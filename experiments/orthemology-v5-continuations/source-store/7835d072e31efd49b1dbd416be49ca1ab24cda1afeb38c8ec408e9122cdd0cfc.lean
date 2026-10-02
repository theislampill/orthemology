import LoopRenaming
import SurvivorCandidates

/-! Register-level semantics of the recovered _candidate control block.
The register layout is the first compile_sigma2 block: output 3, snapshot 5,
candidate 6, test 7, found 8, good 9, matrix result 10. -/
namespace P02A2.CandidateCompiler
open P02A2.ObserverCore P02A2.LoopRenaming P02A2.SurvivorCandidates

abbrev MatrixRelation (f : ℕ → ℕ → ℕ) := fun s t => f s t ≠ 0

def CallSpec (call : Stmt) (f : ℕ → ℕ → ℕ) : Prop :=
  (∀ σ, exec call σ 10 = f (σ 6) (σ 7)) ∧
  (∀ σ r, r < 10 → exec call σ r = σ r)

def testBody (call : Stmt) : Stmt := .seq call
  (.branch (.eq (.reg 10) (.constant 0)) (.set 9 (.constant 0)) .skip)

theorem testBody_good (call : Stmt) (f : ℕ → ℕ → ℕ) (hc : CallSpec call f) (σ : Store) :
    exec (testBody call) σ 9 = if f (σ 6) (σ 7) = 0 then 0 else σ 9 := by
  simp only [testBody, exec, evalExpr, hc.1 σ]
  split_ifs <;> simp_all [hc.2 σ 9 (by decide)]

theorem testBody_preserves (call : Stmt) (f : ℕ → ℕ → ℕ) (hc : CallSpec call f)
    (σ : Store) (r : ℕ) (hr : r < 9) : exec (testBody call) σ r = σ r := by
  have hne : r ≠ 9 := by omega
  simp only [testBody, exec, evalExpr]
  split_ifs <;> simp [Function.update_of_ne hne, hc.2 σ r (by omega)]

theorem testLoop_preserves (call : Stmt) (f : ℕ → ℕ → ℕ) (hc : CallSpec call f)
    (k : ℕ) (σ : Store) (r : ℕ) (hr : r < 9) (h7 : r ≠ 7) :
    runLoop (exec (testBody call)) 7 k σ r = σ r :=
  runLoop_frame _ 7 r h7 (fun σ => testBody_preserves call f hc σ r hr) k σ

theorem testLoop_good (call : Stmt) (f : ℕ → ℕ → ℕ) (hc : CallSpec call f)
    (k : ℕ) (σ : Store) :
    runLoop (exec (testBody call)) 7 k σ 9 =
      if (∀ t < k, f (σ 6) t ≠ 0) then σ 9 else 0 := by
  induction k with
  | zero => simp [runLoop]
  | succ k ih =>
      rw [runLoop, testBody_good call f hc]
      simp only [Function.update_of_ne (by decide : 6 ≠ 7), Function.update_self,
        Function.update_of_ne (by decide : 9 ≠ 7)]
      rw [testLoop_preserves call f hc k σ 6 (by decide) (by decide), ih]
      simp only [Nat.forall_lt_succ]
      by_cases hall : ∀ t < k, f (σ 6) t ≠ 0 <;> by_cases hzero : f (σ 6) k = 0 <;>
        simp [hall, hzero]

def tryCandidate (call : Stmt) : Stmt :=
  .seq (.set 9 (.constant 1))
    (.seq (.loop 7 (.add (.reg 5) (.constant 1)) (testBody call))
      (.branch (.reg 9) (.seq (.set 3 (.reg 6)) (.set 8 (.constant 1))) .skip))

def outerBody (call : Stmt) : Stmt :=
  .branch (.eq (.reg 8) (.constant 0)) (tryCandidate call) .skip

def searchStep (f : ℕ → ℕ → ℕ) (N s : ℕ) (p : ℕ × Bool) : ℕ × Bool :=
  if p.2 then p else if passes (MatrixRelation f) s N then (s,true) else p

def runSearch (f : ℕ → ℕ → ℕ) (N : ℕ) : ℕ → ℕ × Bool
  | 0 => (N+1,false)
  | k+1 => searchStep f N k (runSearch f N k)

def SearchMatches (N : ℕ) (p : ℕ × Bool) (σ : Store) : Prop :=
  σ 5 = N ∧ σ 3 = p.1 ∧ σ 8 = (if p.2 then 1 else 0)

theorem outerBody_matches (call : Stmt) (f : ℕ → ℕ → ℕ) (hc : CallSpec call f)
    (N s : ℕ) (p : ℕ × Bool) (σ : Store) (hm : SearchMatches N p σ) (hs : σ 6 = s) :
    SearchMatches N (searchStep f N s p) (exec (outerBody call) σ) := by
  rcases p with ⟨out,found⟩
  rcases hm with ⟨hN,hout,hfound⟩
  cases found
  · have hf : σ 8 = 0 := hfound
    simp only [outerBody, exec, evalExpr, hf, ↓reduceIte]
    let σi := Function.update σ 9 1
    let τ := runLoop (exec (testBody call)) 7 (N+1) σi
    have hτ5 : τ 5 = N := by
      dsimp only [τ]
      rw [testLoop_preserves call f hc (N+1) σi 5 (by decide) (by decide)]
      simpa [σi] using hN
    have hτ3 : τ 3 = out := by
      dsimp only [τ]
      rw [testLoop_preserves call f hc (N+1) σi 3 (by decide) (by decide)]
      simpa [σi] using hout
    have hτ6 : τ 6 = s := by
      dsimp only [τ]
      rw [testLoop_preserves call f hc (N+1) σi 6 (by decide) (by decide)]
      simpa [σi] using hs
    have hτ8 : τ 8 = 0 := by
      dsimp only [τ]
      rw [testLoop_preserves call f hc (N+1) σi 8 (by decide) (by decide)]
      simpa [σi] using hf
    have hτ9 : τ 9 = if passes (MatrixRelation f) s N then 1 else 0 := by
      dsimp only [τ]
      rw [testLoop_good call f hc (N+1) σi]
      simp only [σi, Function.update_of_ne (by decide : 6 ≠ 9), Function.update_self, hs]
      simp only [passes, Finset.mem_range, MatrixRelation]
    change SearchMatches N (searchStep f N s (out,false))
      (exec (.seq (.loop 7 (.add (.reg 5) (.constant 1)) (testBody call))
        (.branch (.reg 9) (.seq (.set 3 (.reg 6)) (.set 8 (.constant 1))) .skip)) σi)
    have hi5 : σi 5 = N := by simpa [σi] using hN
    simp only [exec, evalExpr, hi5]
    change SearchMatches N (searchStep f N s (out,false))
      (if τ 9 = 0 then τ else Function.update (Function.update τ 3 (τ 6)) 8 1)
    by_cases hp : passes (MatrixRelation f) s N <;>
      simp [SearchMatches, searchStep, hp, hτ9, hτ5, hτ3, hτ6, hτ8]
  · have hf : σ 8 = 1 := hfound
    simpa [outerBody, exec, evalExpr, hf, searchStep, SearchMatches] using And.intro hN (And.intro hout hf)

theorem search_before_candidate (f : ℕ → ℕ → ℕ) (N k : ℕ)
    (hk : k ≤ candidate (MatrixRelation f) N) : runSearch f N k = (N+1,false) := by
  induction k with
  | zero => rfl
  | succ k ih =>
      have hd := candidate_le_default (MatrixRelation f) N
      have hp : ¬ passes (MatrixRelation f) k N := by
        intro h
        have hm := candidate_le_passing (MatrixRelation f) (by omega : k ≤ N) h
        omega
      rw [runSearch, ih (by omega)]
      simp [searchStep, hp]

theorem search_found_stable (f : ℕ → ℕ → ℕ) (N k : ℕ)
    (hf : (runSearch f N k).2 = true) :
    ∀ j, k ≤ j → runSearch f N j = runSearch f N k := by
  intro j hj
  induction j, hj using Nat.le_induction with
  | base => rfl
  | succ j hj ih => rw [runSearch, ih]; simp [searchStep, hf]

theorem search_result (f : ℕ → ℕ → ℕ) (N : ℕ) :
    (runSearch f N (N+1)).1 = candidate (MatrixRelation f) N := by
  let c := candidate (MatrixRelation f) N
  have hc : c ≤ N+1 := candidate_le_default (MatrixRelation f) N
  by_cases hcn : c ≤ N
  · have hpass := candidate_passes (MatrixRelation f) hcn
    have hbefore := search_before_candidate f N c (le_refl _)
    have hhit : runSearch f N (c+1) = (c,true) := by
      rw [runSearch, hbefore]
      simp [searchStep, hpass, c]
    have hstable := search_found_stable f N (c+1) (by rw [hhit]) (N+1) (by omega)
    rw [hstable, hhit]
  · have he : c = N+1 := by omega
    rw [search_before_candidate f N (N+1) (by omega)]
    exact he.symm

theorem outerLoop_matches (call : Stmt) (f : ℕ → ℕ → ℕ) (hc : CallSpec call f)
    (N : ℕ) (σ : Store) (hinit : SearchMatches N (N+1,false) σ) (k : ℕ) :
    SearchMatches N (runSearch f N k) (runLoop (exec (outerBody call)) 6 k σ) := by
  induction k with
  | zero => exact hinit
  | succ k ih =>
      change SearchMatches N (searchStep f N k (runSearch f N k))
        (exec (outerBody call) (Function.update (runLoop (exec (outerBody call)) 6 k σ) 6 k))
      apply outerBody_matches call f hc N k
      · simpa only [SearchMatches, Function.update_of_ne (by decide : 5 ≠ 6),
          Function.update_of_ne (by decide : 3 ≠ 6), Function.update_of_ne (by decide : 8 ≠ 6)] using ih
      · simp

def candidateBlock (call : Stmt) (stage : Expr) : Stmt :=
  .seq (.set 5 stage) (.seq (.set 3 (.add (.reg 5) (.constant 1)))
    (.seq (.set 8 (.constant 0)) (.loop 6 (.add (.reg 5) (.constant 1)) (outerBody call))))

theorem candidateBlock_value (call : Stmt) (f : ℕ → ℕ → ℕ) (hc : CallSpec call f)
    (stage : Expr) (σ : Store) :
    exec (candidateBlock call stage) σ 3 = candidate (MatrixRelation f) (evalExpr stage σ) := by
  let N := evalExpr stage σ
  let initialStore := Function.update (Function.update (Function.update σ 5 N) 3 (N+1)) 8 0
  have hi : SearchMatches N (N+1,false) initialStore := by
    simp [SearchMatches, initialStore]
  have hm := outerLoop_matches call f hc N initialStore hi (N+1)
  change runLoop (exec (outerBody call)) 6 (N+1) initialStore 3 = _
  exact hm.2.1.trans (search_result f N)

def Preserves (s : Stmt) (r : ℕ) : Prop := ∀ σ, exec s σ r = σ r

theorem preserves_skip (r : ℕ) : Preserves .skip r := fun _ => rfl

theorem preserves_set (r j : ℕ) (e : Expr) (h : r ≠ j) : Preserves (.set j e) r :=
  fun σ => Function.update_of_ne h _ _

theorem preserves_seq (s t : Stmt) (r : ℕ) (hs : Preserves s r) (ht : Preserves t r) :
    Preserves (.seq s t) r := fun σ => (ht (exec s σ)).trans (hs σ)

theorem preserves_branch (e : Expr) (s t : Stmt) (r : ℕ)
    (hs : Preserves s r) (ht : Preserves t r) : Preserves (.branch e s t) r := by
  intro σ
  simp only [exec]
  split_ifs
  · exact ht σ
  · exact hs σ

theorem preserves_loop (i : ℕ) (e : Expr) (s : Stmt) (r : ℕ)
    (hr : r ≠ i) (hs : Preserves s r) : Preserves (.loop i e s) r := by
  intro σ
  exact runLoop_frame (exec s) i r hr hs _ σ

theorem tryCandidate_preserves (call : Stmt) (f : ℕ → ℕ → ℕ) (hc : CallSpec call f)
    (r : ℕ) (hr : r < 5) (h3 : r ≠ 3) : Preserves (tryCandidate call) r := by
  apply preserves_seq
  · exact preserves_set r 9 _ (by omega)
  · apply preserves_seq
    · exact preserves_loop 7 _ _ r (by omega) (fun σ => testBody_preserves call f hc σ r (by omega))
    · apply preserves_branch
      · exact preserves_seq _ _ r (preserves_set r 3 _ h3) (preserves_set r 8 _ (by omega))
      · exact preserves_skip r

theorem outerBody_preserves (call : Stmt) (f : ℕ → ℕ → ℕ) (hc : CallSpec call f)
    (r : ℕ) (hr : r < 5) (h3 : r ≠ 3) : Preserves (outerBody call) r :=
  preserves_branch _ _ _ r (tryCandidate_preserves call f hc r hr h3) (preserves_skip r)

theorem candidateBlock_preserves (call : Stmt) (f : ℕ → ℕ → ℕ) (hc : CallSpec call f)
    (stage : Expr) (r : ℕ) (hr : r < 5) (h3 : r ≠ 3) : Preserves (candidateBlock call stage) r := by
  apply preserves_seq
  · exact preserves_set r 5 _ (by omega)
  · apply preserves_seq
    · exact preserves_set r 3 _ h3
    · apply preserves_seq
      · exact preserves_set r 8 _ (by omega)
      · exact preserves_loop 6 _ _ r (by omega) (outerBody_preserves call f hc r hr h3)

end P02A2.CandidateCompiler
