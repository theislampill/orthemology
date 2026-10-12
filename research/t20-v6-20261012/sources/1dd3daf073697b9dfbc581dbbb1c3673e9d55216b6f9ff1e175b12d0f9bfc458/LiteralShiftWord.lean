import LiteralShiftSyntax
import Q8Compiler

/-! Numeric word bridge for the literal source expressions.  In particular,
`sentinel_suffix` proves the exact power-plus-modulo expression from Python,
not merely an independently specified list suffix. -/
namespace P02.LiteralShift
open P02A2.ObserverCore

/-- The binary payload, with no leading sentinel bit. -/
def wordPayload : List Bool → ℕ
  | [] => 0
  | b :: xs => (if b then 1 else 0) * 2^xs.length + wordPayload xs

theorem fold_word (xs : List Bool) (seed : ℕ) :
    xs.foldl (fun n b => 2*n + if b then 1 else 0) seed =
      seed * 2^xs.length + wordPayload xs := by
  induction xs generalizing seed with
  | nil => simp [wordPayload]
  | cons b xs ih =>
      simp only [List.foldl_cons, List.length_cons, ih, wordPayload, pow_succ]
      ring

theorem sentinel_payload (xs : List Bool) :
    sentinel xs = 2^xs.length + wordPayload xs := by
  simpa only [sentinel, one_mul] using fold_word xs 1

theorem wordPayload_lt (xs : List Bool) : wordPayload xs < 2^xs.length := by
  induction xs with
  | nil => simp [wordPayload]
  | cons b xs ih =>
      cases b <;> simp only [wordPayload, Bool.false_eq_true, ↓reduceIte,
        zero_mul, one_mul, zero_add, List.length_cons, pow_succ] <;> omega

theorem sentinel_append_payload (xs ys : List Bool) :
    sentinel (xs ++ ys) = sentinel xs * 2^ys.length + wordPayload ys := by
  simpa only [sentinel, List.foldl_append] using fold_word ys (sentinel xs)

theorem sentinel_append_div (xs ys : List Bool) :
    sentinel (xs ++ ys) / 2^ys.length = sentinel xs := by
  rw [sentinel_append_payload, Nat.add_comm, Nat.add_mul_div_right _ _ (by positivity),
    Nat.div_eq_of_lt (wordPayload_lt ys), zero_add]

theorem sentinel_append_mod (xs ys : List Bool) :
    sentinel (xs ++ ys) % 2^ys.length = wordPayload ys := by
  rw [sentinel_append_payload, Nat.mul_add_mod_self_right,
    Nat.mod_eq_of_lt (wordPayload_lt ys)]

theorem sentinel_mod_payload (xs : List Bool) :
    sentinel xs % 2^xs.length = wordPayload xs := by
  rw [sentinel_payload, Nat.add_mod_left, Nat.mod_eq_of_lt (wordPayload_lt xs)]

/-- Exact prefix division of an arbitrary sentinel word. -/
theorem sentinel_prefix_div (xs : List Bool) (k : ℕ) :
    sentinel xs / 2^(xs.length-k) = sentinel (xs.take k) := by
  have h := sentinel_append_div (xs.take k) (xs.drop k)
  simpa only [List.take_append_drop, List.length_drop] using h

/-- Exact numeric re-sentineling of a dropped suffix, including empty suffixes. -/
theorem sentinel_suffix (xs : List Bool) (k : ℕ) :
    2^(xs.length-k) + sentinel xs % 2^(xs.length-k) = sentinel (xs.drop k) := by
  have h := sentinel_append_mod (xs.take k) (xs.drop k)
  simp only [List.take_append_drop, List.length_drop] at h
  rw [h, sentinel_payload, List.length_drop]

def streamPrefix (x : ℕ → Bool) (k : ℕ) : List Bool :=
  List.ofFn (fun i : Fin k => x i.val)

def dropStream (k : ℕ) (x : ℕ → Bool) : ℕ → Bool := fun i => x (k+i)

@[simp] theorem streamPrefix_length (x : ℕ → Bool) (k : ℕ) :
    (streamPrefix x k).length = k := by simp [streamPrefix]

theorem streamPrefix_take (x : ℕ → Bool) (m k : ℕ) (hk : k ≤ m) :
    (streamPrefix x m).take k = streamPrefix x k := by
  apply List.ext_getElem
  · simp [streamPrefix, hk]
  · intro i hi hj
    simp [streamPrefix]

theorem streamPrefix_drop (x : ℕ → Bool) (m k : ℕ) :
    (streamPrefix x m).drop k = streamPrefix (dropStream k x) (m-k) := by
  apply List.ext_getElem
  · simp [streamPrefix]
  · intro i hi hj
    simp [streamPrefix, dropStream]

/-- The compiler's division/modulo cell is the actual source prefix payload. -/
theorem prefixValue_stream (x : ℕ → Bool) (n k : ℕ) (hk : k ≤ n+1) :
    prefixValue n (sentinel (streamPrefix x (n+1))) k =
      wordPayload (streamPrefix x k) := by
  unfold prefixValue
  have hdiv := sentinel_prefix_div (streamPrefix x (n+1)) k
  simp only [streamPrefix_length] at hdiv
  rw [hdiv, streamPrefix_take x (n+1) k hk]
  simpa only [streamPrefix_length] using sentinel_mod_payload (streamPrefix x k)

/-- The source's exact replay word encodes precisely the fresh, dropped tail. -/
theorem replayWord_stream (x : ℕ → Bool) (n k : ℕ) :
    2^(n+1-k) + sentinel (streamPrefix x (n+1)) % 2^(n+1-k) =
      sentinel (streamPrefix (dropStream k x) (n+1-k)) := by
  simpa only [streamPrefix_length, streamPrefix_drop] using
    sentinel_suffix (streamPrefix x (n+1)) k

theorem sentinel_stream_last (x : ℕ → Bool) (n : ℕ) :
    sentinel (streamPrefix x (n+1)) % 2 = if x n then 1 else 0 := by
  simpa only [streamPrefix] using P02A2.Q8Compiler.sentinel_prefix_last x n

/-- Source-independent cell classification; this is only a mathematical view
of the already defined literal selector, never a replacement compiler. -/
def streamClassify (a b : ℕ) (x : ℕ → Bool) (k : ℕ) : Option Bool :=
  let v := wordPayload (streamPrefix x k)
  if b * (v+1) ≤ a * 2^k then some false
  else if a * 2^k ≤ b*v then some true else none

theorem classify_stream (a b n k : ℕ) (x : ℕ → Bool) (hk : k ≤ n+1) :
    classify a b n (sentinel (streamPrefix x (n+1))) k =
      streamClassify a b x k := by
  unfold classify streamClassify
  rw [prefixValue_stream x n k hk]

/-- Extending the supplied finite input cannot change any already observed cell. -/
theorem classify_stage_consistent (a b n m k : ℕ) (x : ℕ → Bool)
    (hkn : k ≤ n+1) (hkm : k ≤ m+1) :
    classify a b n (sentinel (streamPrefix x (n+1))) k =
      classify a b m (sentinel (streamPrefix x (m+1))) k := by
  rw [classify_stream a b n k x hkn, classify_stream a b m k x hkm]

end P02.LiteralShift
