/- Independent mathematical equations for reference.py's validated tagged
   TypeCode operations. JSON decoding, host execution and resource checks are
   not supplied by this datatype. Negative native shifts are outside this
   substitution use; instantiated binders always give a natural shift. -/
import FiniteBridge
namespace P03Source
open OrthemologyV2 OrthemologyV3

def sourceScoped (d : Nat) : TypeCode → Bool
  | .var n => decide (n < d)
  | .bottom => true
  | .arrow A B => sourceScoped d A && sourceScoped d B
  | .all A => sourceScoped (d+1) A

theorem sourceScoped_eq (A : TypeCode) (d : Nat) : sourceScoped d A = wellScoped d A := by
  induction A generalizing d with
  | var n => rfl
  | bottom => rfl
  | arrow A B ihA ihB => simp [sourceScoped, wellScoped, ihA, ihB]
  | all A ih => simp [sourceScoped, wellScoped, ih]

def sourceShift (A : TypeCode) (amount cutoff : Nat) : TypeCode :=
  match A with
  | .var n => .var (if cutoff ≤ n then n + amount else n)
  | .bottom => .bottom
  | .arrow A B => .arrow (sourceShift A amount cutoff) (sourceShift B amount cutoff)
  | .all A => .all (sourceShift A amount (cutoff+1))

theorem rename_comp (A : TypeCode) (r s : Nat → Nat) :
    rename r (rename s A) = rename (fun n => r (s n)) A := by
  induction A generalizing r s with
  | var n => rfl
  | bottom => rfl
  | arrow A B ihA ihB => simp [rename, ihA, ihB]
  | all A ih =>
      simp only [rename]
      rw [ih]
      apply congrArg TypeCode.all
      apply congrArg (fun f => rename f A)
      funext n
      cases n <;> rfl

theorem sourceShift_eq (A : TypeCode) (amount cutoff : Nat) :
    sourceShift A amount cutoff = rename (fun n => if cutoff ≤ n then n + amount else n) A := by
  induction A generalizing cutoff with
  | var n => rfl
  | bottom => rfl
  | arrow A B ihA ihB => simp [sourceShift, rename, ihA, ihB]
  | all A ih =>
      simp only [sourceShift, rename]
      rw [ih]
      apply congrArg TypeCode.all
      apply congrArg (fun f => rename f A)
      funext n
      cases n with
      | zero => simp [liftRen]
      | succ n =>
          simp only [liftRen]
          split <;> split <;> omega

theorem sourceShift_zero_cutoff (A : TypeCode) (amount : Nat) :
    sourceShift A amount 0 = rename (fun n => n + amount) A := by
  rw [sourceShift_eq]
  simp

theorem sourceShift_next (A : TypeCode) (amount : Nat) :
    rename Nat.succ (sourceShift A amount 0) = sourceShift A (amount+1) 0 := by
  rw [sourceShift_zero_cutoff, sourceShift_zero_cutoff, rename_comp]
  rfl

def sourceSubMap (argument : TypeCode) (binders n : Nat) : TypeCode :=
  if n < binders then .var n
  else if n = binders then sourceShift argument binders 0
  else .var (n-1)

theorem sourceSubMap_next (argument : TypeCode) (binders : Nat) :
    sourceSubMap argument (binders+1) = upSub (sourceSubMap argument binders) := by
  funext n
  cases n with
  | zero => simp [sourceSubMap, upSub]
  | succ n =>
      simp only [upSub]
      by_cases hn : n < binders
      · simp [sourceSubMap, hn, Nat.succ_lt_succ_iff, rename]
      · by_cases he : n = binders
        · subst n
          simp [sourceSubMap, sourceShift_next]
        · have hgt : binders < n := by omega
          have hp : n - 1 + 1 = n := by omega
          simp [sourceSubMap, hn, he, show ¬n+1 < binders+1 by omega,
            show n+1 ≠ binders+1 by omega, rename, hp]

def sourceSubstitute (body argument : TypeCode) (binders : Nat := 0) : TypeCode :=
  match body with
  | .var n => sourceSubMap argument binders n
  | .bottom => .bottom
  | .arrow A B => .arrow (sourceSubstitute A argument binders) (sourceSubstitute B argument binders)
  | .all A => .all (sourceSubstitute A argument (binders+1))

theorem sourceSubstitute_eq (body argument : TypeCode) (binders : Nat) :
    sourceSubstitute body argument binders = substitute (sourceSubMap argument binders) body := by
  induction body generalizing binders with
  | var n => rfl
  | bottom => rfl
  | arrow A B ihA ihB => simp [sourceSubstitute, substitute, ihA, ihB]
  | all A ih =>
      simp only [sourceSubstitute, substitute]
      rw [ih, sourceSubMap_next]

theorem sourceInstantiate_eq (body argument : TypeCode) :
    sourceSubstitute body argument 0 = instantiateType body argument := by
  rw [sourceSubstitute_eq]
  unfold instantiateType
  apply congrArg (fun s => substitute s body)
  funext n
  cases n with
  | zero =>
      simp only [sourceSubMap, Nat.not_lt_zero, ↓reduceIte, singleSub]
      rw [sourceShift_zero_cutoff]
      change rename (fun n => n) argument = argument
      induction argument with
      | var n => rfl
      | bottom => rfl
      | arrow A B ihA ihB => simp [rename, ihA, ihB]
      | all A ih =>
          simp only [rename]
          have h : liftRen (fun n => n) = (fun n => n) := by funext n; cases n <;> rfl
          rw [h, ih]
  | succ n => simp [sourceSubMap, singleSub]

#print axioms sourceInstantiate_eq
end P03Source
