import CodecVarint
import P02A2.ObserverCore

/-! Exact expression tags and canonical unsigned varints of recovered P02-L1.
The bounded recursive parser is given sufficient structural fuel for encoded
inputs. This is an expression-codec theorem, not a host-stack guarantee. -/
namespace P02.Codec
open P02A2.ObserverCore

def exprBytes : Expr → List ℕ
  | .constant n => 1 :: uv n
  | .reg n => 2 :: uv n
  | .add a b => 3 :: (exprBytes a ++ exprBytes b)
  | .sub a b => 4 :: (exprBytes a ++ exprBytes b)
  | .mul a b => 5 :: (exprBytes a ++ exprBytes b)
  | .div a b => 6 :: (exprBytes a ++ exprBytes b)
  | .mod a b => 7 :: (exprBytes a ++ exprBytes b)
  | .le a b => 8 :: (exprBytes a ++ exprBytes b)
  | .eq a b => 9 :: (exprBytes a ++ exprBytes b)
  | .pow2 a => 10 :: exprBytes a

def exprDepth : Expr → ℕ
  | .constant _ | .reg _ => 1
  | .add a b | .sub a b | .mul a b | .div a b | .mod a b | .le a b | .eq a b =>
      max (exprDepth a) (exprDepth b) + 1
  | .pow2 a => exprDepth a + 1

def readBinary (read : List ℕ → Option (Expr × List ℕ)) (op : Expr → Expr → Expr)
    (bs : List ℕ) : Option (Expr × List ℕ) := do
  let (a,bs) ← read bs
  let (b,bs) ← read bs
  return (op a b,bs)

def readExpr : ℕ → List ℕ → Option (Expr × List ℕ)
  | 0, _ => none
  | fuel+1, [] => none
  | fuel+1, tag::bs =>
      if tag = 1 then do let (n,rest) ← uvRead bs; return (.constant n,rest)
      else if tag = 2 then do let (n,rest) ← uvRead bs; return (.reg n,rest)
      else if tag = 3 then readBinary (readExpr fuel) .add bs
      else if tag = 4 then readBinary (readExpr fuel) .sub bs
      else if tag = 5 then readBinary (readExpr fuel) .mul bs
      else if tag = 6 then readBinary (readExpr fuel) .div bs
      else if tag = 7 then readBinary (readExpr fuel) .mod bs
      else if tag = 8 then readBinary (readExpr fuel) .le bs
      else if tag = 9 then readBinary (readExpr fuel) .eq bs
      else if tag = 10 then do let (a,rest) ← readExpr fuel bs; return (.pow2 a,rest)
      else none


theorem readExpr_append (e : Expr) (suffix : List ℕ) (fuel : ℕ) (h : exprDepth e ≤ fuel) :
    readExpr fuel (exprBytes e ++ suffix) = some (e,suffix) := by
  induction e generalizing suffix fuel with
  | constant n =>
      cases fuel with
      | zero => simp [exprDepth] at h
      | succ fuel => simp [exprBytes, readExpr, uvRead_append]
  | reg n =>
      cases fuel with
      | zero => simp [exprDepth] at h
      | succ fuel => simp [exprBytes, readExpr, uvRead_append]
  | pow2 e ih =>
      cases fuel with
      | zero => simp [exprDepth] at h
      | succ fuel =>
          have he : exprDepth e ≤ fuel := by simp [exprDepth] at h; omega
          simp [exprBytes, readExpr, ih suffix fuel he]
  | add a b iha ihb | sub a b iha ihb | mul a b iha ihb | div a b iha ihb |
    mod a b iha ihb | le a b iha ihb | eq a b iha ihb =>
      cases fuel with
      | zero => simp [exprDepth] at h
      | succ fuel =>
          have ha : exprDepth a ≤ fuel := by simp [exprDepth] at h; omega
          have hb : exprDepth b ≤ fuel := by simp [exprDepth] at h; omega
          simp [exprBytes, readExpr, readBinary, List.append_assoc,
            iha (exprBytes b ++ suffix) fuel ha, ihb suffix fuel hb]


theorem bytes_cons {b : ℕ} {xs : List ℕ} (hb : b < 256) (hxs : Bytes xs) : Bytes (b::xs) := by
  intro a ha
  rcases List.mem_cons.mp ha with he | ha
  · simpa [he] using hb
  · exact hxs a ha

theorem bytes_append {xs ys : List ℕ} (hx : Bytes xs) (hy : Bytes ys) : Bytes (xs++ys) := by
  intro a ha
  rcases List.mem_append.mp ha with ha | ha
  · exact hx a ha
  · exact hy a ha

theorem exprBytes_bytes (e : Expr) : Bytes (exprBytes e) := by
  induction e with
  | constant n => exact bytes_cons (by decide) (uv_bytes n)
  | reg n => exact bytes_cons (by decide) (uv_bytes n)
  | pow2 e ih => exact bytes_cons (by decide) ih
  | add a b iha ihb | sub a b iha ihb | mul a b iha ihb | div a b iha ihb |
    mod a b iha ihb | le a b iha ihb | eq a b iha ihb =>
      exact bytes_cons (by decide) (bytes_append iha ihb)

theorem exprDepth_le_length (e : Expr) : exprDepth e ≤ (exprBytes e).length := by
  induction e <;> simp only [exprDepth, exprBytes, List.length_cons, List.length_append] <;> omega

end P02.Codec
