import CodecExpr

namespace P02.Codec
open P02A2.ObserverCore

/-- The recovered variadic Seq constructor lowered to equivalent binary syntax. -/
def sequenceList : List Stmt → Stmt
  | [] => .skip
  | [s] => s
  | s::t::ss => .seq s (sequenceList (t::ss))

/-- Generic stream parser for exactly n children. -/
def readMany {α : Type} (read : List ℕ → Option (α × List ℕ)) : ℕ → List ℕ → Option (List α × List ℕ)
  | 0, bs => some ([],bs)
  | n+1, bs => do
      let (a,bs) ← read bs
      let (as,bs) ← readMany read n bs
      return (a::as,bs)

def stmtBytes : Stmt → List ℕ
  | .skip => 17 :: uv 0
  | .set r e => 16 :: (uv r ++ exprBytes e)
  | .seq s t => 17 :: (uv 2 ++ stmtBytes s ++ stmtBytes t)
  | .loop r e s => 18 :: (uv r ++ exprBytes e ++ stmtBytes s)
  | .branch e s t => 19 :: (exprBytes e ++ stmtBytes s ++ stmtBytes t)

def stmtDepth : Stmt → ℕ
  | .skip => 1
  | .set _ e => exprDepth e + 1
  | .seq s t => max (stmtDepth s) (stmtDepth t) + 1
  | .loop _ e s => max (exprDepth e) (stmtDepth s) + 1
  | .branch e s t => max (exprDepth e) (max (stmtDepth s) (stmtDepth t)) + 1

def readStmt : ℕ → List ℕ → Option (Stmt × List ℕ)
  | 0, _ => none
  | fuel+1, [] => none
  | fuel+1, tag::bs =>
      if tag = 16 then do
        let (r,bs) ← uvRead bs
        let (e,bs) ← readExpr fuel bs
        return (.set r e,bs)
      else if tag = 17 then do
        let (n,bs) ← uvRead bs
        let (ss,bs) ← readMany (readStmt fuel) n bs
        return (sequenceList ss,bs)
      else if tag = 18 then do
        let (r,bs) ← uvRead bs
        let (e,bs) ← readExpr fuel bs
        let (s,bs) ← readStmt fuel bs
        return (.loop r e s,bs)
      else if tag = 19 then do
        let (e,bs) ← readExpr fuel bs
        let (s,bs) ← readStmt fuel bs
        let (t,bs) ← readStmt fuel bs
        return (.branch e s t,bs)
      else none

theorem readStmt_append (s : Stmt) (suffix : List ℕ) (fuel : ℕ) (h : stmtDepth s ≤ fuel) :
    readStmt fuel (stmtBytes s ++ suffix) = some (s,suffix) := by
  induction s generalizing suffix fuel with
  | skip =>
      cases fuel with
      | zero => simp [stmtDepth] at h
      | succ fuel => simp [stmtBytes, readStmt, uvRead_append, readMany, sequenceList]
  | set r e =>
      cases fuel with
      | zero => simp [stmtDepth] at h
      | succ fuel =>
          have he : exprDepth e ≤ fuel := by simp [stmtDepth] at h; omega
          simp [stmtBytes, readStmt, List.append_assoc, uvRead_append, readExpr_append e suffix fuel he]
  | seq s t ihs iht =>
      cases fuel with
      | zero => simp [stmtDepth] at h
      | succ fuel =>
          have hs : stmtDepth s ≤ fuel := by simp [stmtDepth] at h; omega
          have ht : stmtDepth t ≤ fuel := by simp [stmtDepth] at h; omega
          simp [stmtBytes, readStmt, List.append_assoc, uvRead_append, readMany, sequenceList,
            ihs (stmtBytes t ++ suffix) fuel hs, iht suffix fuel ht]
  | loop r e s ih =>
      cases fuel with
      | zero => simp [stmtDepth] at h
      | succ fuel =>
          have he : exprDepth e ≤ fuel := by simp [stmtDepth] at h; omega
          have hs : stmtDepth s ≤ fuel := by simp [stmtDepth] at h; omega
          simp [stmtBytes, readStmt, List.append_assoc, uvRead_append,
            readExpr_append e (stmtBytes s ++ suffix) fuel he, ih suffix fuel hs]
  | branch e s t ihs iht =>
      cases fuel with
      | zero => simp [stmtDepth] at h
      | succ fuel =>
          have he : exprDepth e ≤ fuel := by simp [stmtDepth] at h; omega
          have hs : stmtDepth s ≤ fuel := by simp [stmtDepth] at h; omega
          have ht : stmtDepth t ≤ fuel := by simp [stmtDepth] at h; omega
          simp [stmtBytes, readStmt, List.append_assoc,
            readExpr_append e (stmtBytes s ++ (stmtBytes t ++ suffix)) fuel he,
            ihs (stmtBytes t ++ suffix) fuel hs, iht suffix fuel ht]


theorem stmtBytes_bytes (s : Stmt) : Bytes (stmtBytes s) := by
  induction s with
  | skip => exact bytes_cons (by decide) (uv_bytes 0)
  | set r e => exact bytes_cons (by decide) (bytes_append (uv_bytes r) (exprBytes_bytes e))
  | seq s t ihs iht => exact bytes_cons (by decide) (bytes_append (bytes_append (uv_bytes 2) ihs) iht)
  | loop r e s ih => exact bytes_cons (by decide) (bytes_append (bytes_append (uv_bytes r) (exprBytes_bytes e)) ih)
  | branch e s t ihs iht => exact bytes_cons (by decide) (bytes_append (bytes_append (exprBytes_bytes e) ihs) iht)

theorem stmtDepth_le_length (s : Stmt) : stmtDepth s ≤ (stmtBytes s).length := by
  induction s with
  | skip => simp [stmtDepth, stmtBytes]
  | set r e => have he := exprDepth_le_length e; simp only [stmtDepth, stmtBytes, List.length_cons, List.length_append]; omega
  | seq s t ihs iht => simp only [stmtDepth, stmtBytes, List.length_cons, List.length_append]; omega
  | loop r e s ih => have he := exprDepth_le_length e; simp only [stmtDepth, stmtBytes, List.length_cons, List.length_append]; omega
  | branch e s t ihs iht => have he := exprDepth_le_length e; simp only [stmtDepth, stmtBytes, List.length_cons, List.length_append]; omega

theorem sequenceList_execution (ss : List Stmt) (σ : Store) :
    exec (sequenceList ss) σ = ss.foldl (fun τ s => exec s τ) σ := by
  induction ss generalizing σ with
  | nil => rfl
  | cons s ss ih =>
      cases ss with
      | nil => rfl
      | cons t ss =>
          change exec (sequenceList (t::ss)) (exec s σ) = _
          exact ih (exec s σ)

end P02.Codec
