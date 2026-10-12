import MembershipHeavyBridge

/-! Independent semantic controls for the unchanged finite membership matrix. -/
namespace MatrixIndependentAudit
open P02.Codec P02.Codec.UniformComputability P02A2.ObserverCore AtomicMembership

/-- Complete enumeration has exactly 2^N entries; there is one empty word. -/
theorem allWords_length (N : ℕ) : (allWords N).length = 2^N := by
  induction N with
  | zero => rfl
  | succ n ih => simp [allWords, ih, pow_succ, Nat.mul_two]

theorem allWords_zero : allWords 0 = [[]] := rfl
theorem allWords_two : allWords 2 =
    [[false,false],[false,true],[true,false],[true,true]] := rfl

theorem output_length (e : ℕ) (v : List Bool) : (outputList e v).length = v.length := by
  simp [outputList]

theorem count_zero_depth (e : ℕ) : wordCount e 0 [] = 1 := by
  simp [wordCount,allWords,outputList]

theorem heavy_zero_depth (e k : ℕ) : heavyCount e k 0 = 1 := by
  have h : 1 ≤ 2^k := by
    have hp : 0 < 2^k := by positivity
    omega
  simp [heavyCount, allWords, count_zero_depth, h]

theorem matrix_zero_depth (e i k : ℕ) : membershipMatrix e i k 0 := by
  rw [membershipMatrix_integer_iff, heavy_zero_depth]
  simp only [pow_zero, Nat.mul_one]
  omega

theorem zero_denominator_all (e a k N : ℕ) : membershipMatrix e (Nat.pair a 0) k N := by
  rw [membershipMatrix_integer_iff]
  simp

theorem zero_numerator_all (e d k N : ℕ) : membershipMatrix e (Nat.pair 0 d) k N := by
  rw [membershipMatrix_integer_iff]
  simp

theorem rational_at_least_one (e a d k N : ℕ) (h : d ≤ a) :
    membershipMatrix e (Nat.pair a d) k N := by
  rw [membershipMatrix_integer_iff]
  simp [h]

/-- The boundary follows equality, rather than a strict comparison. -/
theorem exact_integer_tie (e a d k N : ℕ)
    (h : a * 2^N = d * heavyCount e k N) : membershipMatrix e (Nat.pair a d) k N := by
  rw [membershipMatrix_integer_iff]
  simpa using (Or.inr (Or.inr h.le) : d=0 ∨ d≤a ∨ a*2^N≤d*heavyCount e k N)

/-- Multiplying numerator and denominator by the same positive factor does not
change the original matrix, including zero denominators and vacuous rationals. -/
theorem redundant_fraction (e a d c k N : ℕ) (hc : 0<c) :
    membershipMatrix e (Nat.pair (c*a) (c*d)) k N ↔ membershipMatrix e (Nat.pair a d) k N := by
  simp only [membershipMatrix_integer_iff, Nat.unpair_pair]
  have hz : c*d=0 ↔ d=0 := by simp [Nat.mul_eq_zero, Nat.ne_of_gt hc]
  have hv : c*d≤c*a ↔ d≤a := Nat.mul_le_mul_left_iff hc
  have ht : c*a*2^N≤c*d*heavyCount e k N ↔ a*2^N≤d*heavyCount e k N := by
    simpa only [Nat.mul_assoc] using
      (Nat.mul_le_mul_left_iff hc : c*(a*2^N)≤c*(d*heavyCount e k N) ↔ a*2^N≤d*heavyCount e k N)
  rw [hz,hv,ht]

def echoProgram : PackedProgram := ⟨2,1,.skip⟩
theorem echo_value (n word : ℕ) : evaluateIndex (programIndex echoProgram) n word = word%2 := by
  rw [evaluateIndex,decodeIndex_programIndex]
  simp [echoProgram,exec,binaryStore]

/-- At depth two: output fibers have sizes 1,1,2,0. -/
def mixedProgram : PackedProgram :=
  ⟨2,2,.set 2 (.mul (.mod (.reg 1) (.constant 2)) (.le (.reg 1) (.constant 5)))⟩

theorem mixed_value (n word : ℕ) :
    evaluateIndex (programIndex mixedProgram) n word =
      (word%2 * (if word≤5 then 1 else 0))%2 := by
  rw [evaluateIndex,decodeIndex_programIndex]
  simp [mixedProgram,exec,evalExpr,binaryStore]

theorem invalid_value (n word : ℕ) : evaluateIndex 0 n word = 0 := by
  simp [evaluateIndex,decodeIndex,decodeNumeric]

theorem invalid_heavy_count : heavyCount 0 0 2 = 4 := by
  unfold heavyCount wordCount outputList
  simp_rw [invalid_value]
  decide +kernel

theorem invalid_matrix_true : membershipMatrix 0 (Nat.pair 3 4) 0 2 := by
  rw [membershipMatrix_integer_iff,invalid_heavy_count]
  decide

theorem echo_below_threshold : heavyCount (programIndex echoProgram) 1 2 = 0 := by
  unfold heavyCount wordCount outputList
  simp_rw [echo_value]
  decide +kernel

theorem echo_at_threshold : heavyCount (programIndex echoProgram) 2 2 = 4 := by
  unfold heavyCount wordCount outputList
  simp_rw [echo_value]
  decide +kernel

theorem echo_matrix_false : ¬ membershipMatrix (programIndex echoProgram) (Nat.pair 1 2) 1 2 := by
  rw [membershipMatrix_integer_iff,echo_below_threshold]
  decide

theorem echo_matrix_true : membershipMatrix (programIndex echoProgram) (Nat.pair 1 2) 2 2 := by
  rw [membershipMatrix_integer_iff,echo_at_threshold]
  decide

theorem mixed_count_half : heavyCount (programIndex mixedProgram) 1 2 = 2 := by
  unfold heavyCount wordCount outputList
  simp_rw [mixed_value]
  decide +kernel

theorem mixed_count_all : heavyCount (programIndex mixedProgram) 2 2 = 4 := by
  unfold heavyCount wordCount outputList
  simp_rw [mixed_value]
  decide +kernel

theorem mixed_tied_membership : membershipMatrix (programIndex mixedProgram) (Nat.pair 1 2) 1 2 := by
  rw [membershipMatrix_integer_iff,mixed_count_half]
  decide

theorem mixed_above_half_rejected : ¬ membershipMatrix (programIndex mixedProgram) (Nat.pair 3 4) 1 2 := by
  rw [membershipMatrix_integer_iff,mixed_count_half]
  decide

theorem redundant_concrete_tie : membershipMatrix (programIndex mixedProgram) (Nat.pair 2 4) 1 2 := by
  rw [membershipMatrix_integer_iff,mixed_count_half]
  decide

theorem vacuous_one_even_zero_mass : membershipMatrix (programIndex echoProgram) (Nat.pair 1 1) 1 2 :=
  rational_at_least_one _ _ _ _ _ (by decide)

theorem vacuous_above_one_even_zero_mass : membershipMatrix (programIndex echoProgram) (Nat.pair 3 2) 1 2 :=
  rational_at_least_one _ _ _ _ _ (by decide)


theorem wrong_length_count_zero (e N : ℕ) (w : List Bool) (hw : w.length ≠ N) :
    wordCount e N w = 0 := by
  unfold wordCount
  have h : ((allWords N).filter (fun v => decide (outputList e v = w))) = [] := by
    apply List.filter_eq_nil_iff.mpr
    intro v hv heq
    have he : outputList e v = w := of_decide_eq_true heq
    have hl := congrArg List.length he
    rw [output_length, (mem_allWords N v).mp hv] at hl
    exact hw hl.symm
  rw [h]
  rfl

def wrongArityProgram : PackedProgram := ⟨1,1,.skip⟩
theorem wrong_arity_value (n word : ℕ) : evaluateIndex (programIndex wrongArityProgram) n word = 0 := by
  rw [evaluateIndex, decodeIndex_programIndex]
  simp [wrongArityProgram]

theorem wrong_arity_heavy_count : heavyCount (programIndex wrongArityProgram) 0 2 = 4 := by
  unfold heavyCount wordCount outputList
  simp_rw [wrong_arity_value]
  decide +kernel

/-- Zero scaling is excluded from the redundant-fraction equivalence for a reason. -/
theorem zero_scaling_changes_matrix :
    membershipMatrix (programIndex echoProgram) (Nat.pair 0 0) 1 2 ∧
      ¬ membershipMatrix (programIndex echoProgram) (Nat.pair 1 2) 1 2 :=
  ⟨zero_denominator_all _ _ _ _, echo_matrix_false⟩


theorem echo_prefix_stream :
    outputList (programIndex echoProgram) [true,false] = [true,false] := by
  unfold outputList
  simp_rw [echo_value]
  decide +kernel

end MatrixIndependentAudit
