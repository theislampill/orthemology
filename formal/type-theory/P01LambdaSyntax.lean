/- Exact untyped computational target for the Curry System-F judgment.
   Atom κ is the source bottom tag at the type level; inert markers are untyped.
   New attempt-0003 source: uncompiled, no kernel credit. -/
import P01TypeAlgebra
import P01SNReflection
namespace P01F
open OrthemologyV2 OrthemologyV3
inductive LTerm where
  | var : Nat → LTerm
  | zero | one
  | app : LTerm → LTerm → LTerm
  | lam : LTerm → LTerm
  deriving DecidableEq, Repr

def ren (r : Nat → Nat) : LTerm → LTerm
  | .var n => .var (r n)
  | .zero => .zero
  | .one => .one
  | .app f a => .app (ren r f) (ren r a)
  | .lam b => .lam (ren (liftRen r) b)

def up (σ : Nat → LTerm) : Nat → LTerm
  | 0 => .var 0
  | n+1 => ren Nat.succ (σ n)

def sub (σ : Nat → LTerm) : LTerm → LTerm
  | .var n => σ n
  | .zero => .zero
  | .one => .one
  | .app f a => .app (sub σ f) (sub σ a)
  | .lam b => .lam (sub (up σ) b)

def single (a : LTerm) : Nat → LTerm
  | 0 => a
  | n+1 => .var n

def inst (b a : LTerm) := sub (single a) b

@[simp] theorem ren_id (t : LTerm) : ren id t = t := by
  induction t with
  | var n => rfl
  | zero => rfl
  | one => rfl
  | app f a hf ha => simp only [ren, hf, ha]
  | lam b ih =>
      have e : liftRen id = id := by funext n; cases n <;> rfl
      simp only [ren, e, ih]

theorem ren_comp (t : LTerm) (r s : Nat → Nat) :
    ren s (ren r t) = ren (fun n => s (r n)) t := by
  induction t generalizing r s with
  | var n => rfl
  | zero => rfl
  | one => rfl
  | app f a hf ha => simp only [ren, hf, ha]
  | lam b ih =>
      apply congrArg LTerm.lam
      rw [ih]
      apply congrArg (fun q => ren q b)
      funext n; cases n <;> rfl

@[simp] theorem sub_id (t : LTerm) : sub LTerm.var t = t := by
  induction t with
  | var n => rfl
  | zero => rfl
  | one => rfl
  | app f a hf ha => simp only [sub, hf, ha]
  | lam b ih =>
      have e : up LTerm.var = LTerm.var := by funext n; cases n <;> rfl
      simp only [sub, e, ih]

theorem sub_ren (t : LTerm) (σ : Nat → LTerm) (r : Nat → Nat) :
    sub σ (ren r t) = sub (fun n => σ (r n)) t := by
  induction t generalizing σ r with
  | var n => rfl
  | zero => rfl
  | one => rfl
  | app f a hf ha => simp only [ren, sub, hf, ha]
  | lam b ih =>
      apply congrArg LTerm.lam
      rw [ih]
      apply congrArg (fun q => sub q b)
      funext n; cases n <;> rfl

theorem ren_sub (t : LTerm) (σ : Nat → LTerm) (r : Nat → Nat) :
    ren r (sub σ t) = sub (fun n => ren r (σ n)) t := by
  induction t generalizing σ r with
  | var n => rfl
  | zero => rfl
  | one => rfl
  | app f a hf ha => simp only [ren, sub, hf, ha]
  | lam b ih =>
      apply congrArg LTerm.lam
      rw [ih]
      apply congrArg (fun q => sub q b)
      funext n
      cases n with
      | zero => rfl
      | succ n => simp only [up]; rw [ren_comp, ren_comp]; rfl

theorem sub_comp (t : LTerm) (σ τ : Nat → LTerm) :
    sub τ (sub σ t) = sub (fun n => sub τ (σ n)) t := by
  induction t generalizing σ τ with
  | var n => rfl
  | zero => rfl
  | one => rfl
  | app f a hf ha => simp only [sub, hf, ha]
  | lam b ih =>
      apply congrArg LTerm.lam
      rw [ih]
      apply congrArg (fun q => sub q b)
      funext n
      cases n with
      | zero => rfl
      | succ n =>
          simp only [up]
          rw [sub_ren]
          exact (ren_sub (σ n) τ Nat.succ).symm

@[simp] theorem sub_up_shift (t : LTerm) (σ : Nat → LTerm) :
    sub (up σ) (ren Nat.succ t) = ren Nat.succ (sub σ t) := by
  rw [sub_ren, ren_sub]; rfl

@[simp] theorem inst_shift (t a : LTerm) : inst (ren Nat.succ t) a = t := by
  unfold inst; rw [sub_ren]; exact sub_id t

theorem sub_inst (b a : LTerm) (σ : Nat → LTerm) :
    sub σ (inst b a) = inst (sub (up σ) b) (sub σ a) := by
  unfold inst
  rw [sub_comp, sub_comp]
  apply congrArg (fun q => sub q b)
  funext n
  cases n with
  | zero => rfl
  | succ n => exact (inst_shift (σ n) (sub σ a)).symm

inductive Beta : LTerm → LTerm → Prop where
  | root (b a) : Beta (.app (.lam b) a) (inst b a)
  | left {f g} : Beta f g → (a : LTerm) → Beta (.app f a) (.app g a)
  | right (f) {a b} : Beta a b → Beta (.app f a) (.app f b)
  | under {a b} : Beta a b → Beta (.lam a) (.lam b)

abbrev BStar := P01SNReflection.Star Beta
abbrev BPositive := P01SNReflection.Positive Beta

theorem beta_sub {t u} (h : Beta t u) (σ : Nat → LTerm) :
    Beta (sub σ t) (sub σ u) := by
  induction h generalizing σ with
  | root b a => simpa only [sub, sub_inst] using Beta.root (sub (up σ) b) (sub σ a)
  | left h a ih => exact .left (ih σ) _
  | right f h ih => exact .right _ (ih σ)
  | under h ih => exact .under (ih (up σ))

theorem bstar_trans {t u v} (h : BStar t u) (k : BStar u v) : BStar t v := by
  induction h with
  | refl => exact k
  | tail h hs ih => exact .tail h (ih k)

theorem bstar_left {t u} (h : BStar t u) (a) : BStar (.app t a) (.app u a) := by
  induction h with
  | refl => exact .refl _
  | tail h hs ih => exact .tail (.left h a) ih

theorem bstar_right (f) {t u} (h : BStar t u) : BStar (.app f t) (.app f u) := by
  induction h with
  | refl => exact .refl _
  | tail h hs ih => exact .tail (.right f h) ih

inductive BConv : LTerm → LTerm → Prop where
  | refl (t) : BConv t t
  | step {t u} : Beta t u → BConv t u
  | symm {t u} : BConv t u → BConv u t
  | trans {t u v} : BConv t u → BConv u v → BConv t v

theorem bstar_conv {t u} (h : BStar t u) : BConv t u := by
  induction h with
  | refl => exact .refl _
  | tail h hs ih => exact .trans (.step h) ih
end P01F
