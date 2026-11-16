/- New attempt-0003 source. Complete proof bodies; UNCOMPILED at Lean 4.19.0.
   Exact canonical TypeCode/rename/substitute are imported, not redefined. -/
import Mathlib.Data.Bool.Basic
import FiniteBridge
namespace P01F
open OrthemologyV2 OrthemologyV3

abbrev Ty := TypeCode

def cons {α : Type} (a : α) (ρ : Nat → α) : Nat → α
  | 0 => a
  | n+1 => ρ n

@[simp] theorem ty_rename_id (A : Ty) : rename id A = A := by
  induction A with
  | var n => rfl
  | bottom => rfl
  | arrow A B ha hb => simp only [rename, ha, hb]
  | all B ih =>
      change TypeCode.all (rename (liftRen id) B) = TypeCode.all B
      have e : liftRen id = id := by funext n; cases n <;> rfl
      rw [e, ih]

theorem ty_rename_comp (A : Ty) (r s : Nat → Nat) :
    rename s (rename r A) = rename (fun n => s (r n)) A := by
  induction A generalizing r s with
  | var n => rfl
  | bottom => rfl
  | arrow A B ha hb => simp only [rename, ha, hb]
  | all B ih =>
      apply congrArg TypeCode.all
      rw [ih]
      apply congrArg (fun q => rename q B)
      funext n; cases n <;> rfl

@[simp] theorem ty_sub_id (A : Ty) : substitute TypeCode.var A = A := by
  induction A with
  | var n => rfl
  | bottom => rfl
  | arrow A B ha hb => simp only [substitute, ha, hb]
  | all B ih =>
      change TypeCode.all (substitute (upSub TypeCode.var) B) = TypeCode.all B
      have e : upSub TypeCode.var = TypeCode.var := by
        funext n; cases n <;> rfl
      rw [e, ih]

theorem ty_sub_rename (A : Ty) (σ : Nat → Ty) (r : Nat → Nat) :
    substitute σ (rename r A) = substitute (fun n => σ (r n)) A := by
  induction A generalizing σ r with
  | var n => rfl
  | bottom => rfl
  | arrow A B ha hb => simp only [rename, substitute, ha, hb]
  | all B ih =>
      apply congrArg TypeCode.all
      rw [ih]
      apply congrArg (fun q => substitute q B)
      funext n; cases n <;> rfl

theorem ty_rename_sub (A : Ty) (σ : Nat → Ty) (r : Nat → Nat) :
    rename r (substitute σ A) = substitute (fun n => rename r (σ n)) A := by
  induction A generalizing σ r with
  | var n => rfl
  | bottom => rfl
  | arrow A B ha hb => simp only [rename, substitute, ha, hb]
  | all B ih =>
      apply congrArg TypeCode.all
      rw [ih]
      apply congrArg (fun q => substitute q B)
      funext n
      cases n with
      | zero => rfl
      | succ n =>
          simp only [upSub]
          rw [ty_rename_comp, ty_rename_comp]
          rfl

theorem ty_sub_comp (A : Ty) (σ τ : Nat → Ty) :
    substitute τ (substitute σ A) =
      substitute (fun n => substitute τ (σ n)) A := by
  induction A generalizing σ τ with
  | var n => rfl
  | bottom => rfl
  | arrow A B ha hb => simp only [substitute, ha, hb]
  | all B ih =>
      apply congrArg TypeCode.all
      rw [ih]
      apply congrArg (fun q => substitute q B)
      funext n
      cases n with
      | zero => rfl
      | succ n =>
          simp only [upSub]
          rw [ty_sub_rename]
          exact (ty_rename_sub (σ n) τ Nat.succ).symm

@[simp] theorem ty_sub_up_shift (A : Ty) (σ : Nat → Ty) :
    substitute (upSub σ) (rename Nat.succ A) =
      rename Nat.succ (substitute σ A) := by
  rw [ty_sub_rename, ty_rename_sub]
  rfl

@[simp] theorem ty_inst_shift (A X : Ty) :
    substitute (singleSub X) (rename Nat.succ A) = A := by
  rw [ty_sub_rename]
  exact ty_sub_id A

theorem ty_sub_inst (B A : Ty) (σ : Nat → Ty) :
    substitute σ (instantiateType B A) =
      instantiateType (substitute (upSub σ) B) (substitute σ A) := by
  unfold instantiateType
  rw [ty_sub_comp, ty_sub_comp]
  apply congrArg (fun q => substitute q B)
  funext n
  cases n with
  | zero => rfl
  | succ n =>
      change σ n = substitute (singleSub (substitute σ A)) (rename Nat.succ (σ n))
      exact (ty_inst_shift (σ n) (substitute σ A)).symm

theorem ty_sub_vars (A : Ty) (r : Nat → Nat) :
    substitute (fun n => TypeCode.var (r n)) A = rename r A := by
  simpa only [ty_sub_id] using (ty_rename_sub A TypeCode.var r).symm
end P01F
