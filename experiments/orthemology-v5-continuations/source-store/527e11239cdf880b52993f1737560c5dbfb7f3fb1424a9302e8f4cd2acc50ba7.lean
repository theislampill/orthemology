import Mathlib

/-! General all-length parity counting. UNEXECUTED at Lean 4.19.0.
A mask is a list of fixed bits or free coordinates. No fixed dimension census
or hypothesis asserting the desired count occurs in the proofs. -/
namespace P02A2.AllNParity

def free : List (Option Bool) → ℕ
  | [] => 0
  | none::ms => free ms+1
  | some _::ms => free ms

def fixed : List (Option Bool) → ℕ
  | [] => 0
  | none::ms => fixed ms
  | some _::ms => fixed ms+1

def count : Bool → List (Option Bool) → ℕ
  | b, [] => if b then 0 else 1
  | b, none::ms => count b ms+count (!b) ms
  | b, some a::ms => count (Bool.xor b a) ms

def solutions : Bool → List (Option Bool) → List (List Bool)
  | b, [] => if b then [] else [[]]
  | b, none::ms => (solutions b ms).map (false::·) ++ (solutions (!b) ms).map (true::·)
  | b, some a::ms => (solutions (Bool.xor b a) ms).map (a::·)

theorem solutions_length (b : Bool) (ms : List (Option Bool)) :
    (solutions b ms).length=count b ms := by
  induction ms generalizing b with
  | nil => cases b <;> rfl
  | cons a ms ih => cases a <;> simp [solutions,count,ih]

theorem free_fixed (ms : List (Option Bool)) : free ms+fixed ms=ms.length := by
  induction ms with
  | nil => rfl
  | cons a ms ih => cases a <;> simp [free,fixed] <;> omega

theorem free_replicate (n : ℕ) : free (List.replicate n none)=n := by
  induction n with
  | zero => rfl
  | succ n ih => simpa [List.replicate_succ,free] using congrArg Nat.succ ih

theorem complementary_count (b : Bool) (ms : List (Option Bool)) :
    count b ms+count (!b) ms=2^(free ms) := by
  induction ms generalizing b with
  | nil => cases b <;> rfl
  | cons a ms ih =>
    cases a with
    | none =>
      have h := ih false
      cases b <;> simp only [count,free,Bool.not_false,Bool.not_true,pow_succ] at * <;> omega
    | some a =>
      have h0 := ih false
      have h1 := ih true
      cases a <;> cases b <;> simp_all [count,free]

theorem proper_mask_count (b : Bool) (ms : List (Option Bool)) (h : 0<free ms) :
    count b ms=2^(free ms-1) := by
  induction ms generalizing b with
  | nil => simp [free] at h
  | cons a ms ih =>
    cases a with
    | none => simpa [count,free] using complementary_count b ms
    | some a => simpa [count,free] using ih (Bool.xor b a) h

theorem full_parity_count (n : ℕ) (hn : 1≤n) (b : Bool) :
    count b (List.replicate n none)=2^(n-1) := by
  have hf : 0<free (List.replicate n none) := by rw [free_replicate]; omega
  simpa [free_replicate] using proper_mask_count b (List.replicate n none) hf

-- Ratio of exact enumerated event count to full parity-word count.
noncomputable def marginal (b : Bool) (ms : List (Option Bool)) : ℚ :=
  (count b ms : ℚ)/(count b (List.replicate ms.length none) : ℚ)

theorem proper_mask_marginal (b : Bool) (ms : List (Option Bool)) (h : 0<free ms) :
    marginal b ms=1/(2:ℚ)^(fixed ms) := by
  have hsplit := free_fixed ms
  have hlen : 1 ≤ ms.length := by omega
  have he : ms.length-1=(free ms-1)+fixed ms := by omega
  unfold marginal
  rw [proper_mask_count b ms h,full_parity_count ms.length hlen b]
  simp only [Nat.cast_pow,Nat.cast_ofNat]
  rw [he,pow_add]
  have h1 : (2:ℚ)^(free ms-1) ≠ 0 := pow_ne_zero _ (by norm_num)
  have h2 : (2:ℚ)^fixed ms ≠ 0 := pow_ne_zero _ (by norm_num)
  field_simp

theorem parity_marginals_equal (ms : List (Option Bool)) (h : 0<free ms) :
    marginal false ms=marginal true ms := by
  rw [proper_mask_marginal false ms h,proper_mask_marginal true ms h]

theorem mixture_pair_00 (a : ℚ) : (1-a)*(1/4:ℚ)+a=(1+3*a)/4 := by ring

theorem mixture_pair_other (a : ℚ) : (1-a)*(1/4:ℚ)+a*0=(1-a)/4 := by ring

theorem mixture_half_profile :
    (1-(1/2:ℚ))*(1/4)+1/2=5/8 ∧ (1-(1/2:ℚ))*(1/4)=1/8 := by norm_num

end P02A2.AllNParity
