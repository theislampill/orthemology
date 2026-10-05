/-
Finite source-to-semantics bridge and proof-carrying checker.
STATUS: complete authored source, NOT kernel-verified in this runtime.
The Python JSON parser is outside this theorem. This checker consumes Cert,
an explicit inductive AST; it does not assume an infinitary derivation as input.
-/
import InternalPolymorphism

namespace OrthemologyV3
open OrthemologyV2

def liftRen (r : Nat → Nat) : Nat → Nat
  | 0 => 0
  | n + 1 => r n + 1

def rename (r : Nat → Nat) : TypeCode → TypeCode
  | .var n => .var (r n)
  | .bottom => .bottom
  | .arrow A B => .arrow (rename r A) (rename r B)
  | .all A => .all (rename (liftRen r) A)

theorem rename_sem (A : TypeCode) : ∀ (r : Nat → Nat) (ρ : Nat → Code),
    interpret (rename r A) ρ = interpret A (fun n => ρ (r n)) := by
  induction A with
  | var n => intro r ρ; rfl
  | bottom => intro r ρ; rfl
  | arrow A B ihA ihB =>
      intro r ρ
      change Code.arrow (interpret (rename r A) ρ) (interpret (rename r B) ρ) = _
      rw [ihA, ihB] <;> rfl
  | all A ih =>
      intro r ρ
      change Code.all (fun X => interpret (rename (liftRen r) A) (extend X ρ)) = _
      apply congrArg Code.all
      funext X
      rw [ih]
      apply congrArg (interpret A)
      funext n
      cases n <;> rfl

def upSub (σ : Nat → TypeCode) : Nat → TypeCode
  | 0 => .var 0
  | n + 1 => rename Nat.succ (σ n)

def substitute (σ : Nat → TypeCode) : TypeCode → TypeCode
  | .var n => σ n
  | .bottom => .bottom
  | .arrow A B => .arrow (substitute σ A) (substitute σ B)
  | .all A => .all (substitute (upSub σ) A)

theorem substitute_sem (A : TypeCode) : ∀ (σ : Nat → TypeCode) (ρ : Nat → Code),
    interpret (substitute σ A) ρ =
      interpret A (fun n => interpret (σ n) ρ) := by
  induction A with
  | var n => intro σ ρ; rfl
  | bottom => intro σ ρ; rfl
  | arrow A B ihA ihB =>
      intro σ ρ
      change Code.arrow (interpret (substitute σ A) ρ)
        (interpret (substitute σ B) ρ) = _
      rw [ihA, ihB] <;> rfl
  | all A ih =>
      intro σ ρ
      change Code.all (fun X => interpret (substitute (upSub σ) A) (extend X ρ)) = _
      apply congrArg Code.all
      funext X
      rw [ih]
      apply congrArg (interpret A)
      funext n
      cases n with
      | zero => rfl
      | succ n =>
          change interpret (rename Nat.succ (σ n)) (extend X ρ) = interpret (σ n) ρ
          rw [rename_sem] <;> rfl

def singleSub (A : TypeCode) : Nat → TypeCode
  | 0 => A
  | n + 1 => .var n

def instantiateType (B A : TypeCode) : TypeCode := substitute (singleSub A) B

theorem instantiate_sem (B A : TypeCode) (ρ : Nat → Code) :
    interpret (instantiateType B A) ρ =
      interpret B (extend (interpret A ρ) ρ) := by
  unfold instantiateType
  rw [substitute_sem]
  apply congrArg (interpret B)
  funext n
  cases n <;> rfl

/-- The introduction premise is ONE finite derivation, not one per semantic code.
No term-variable context is present, so there is no generalisation of a fixed
term assumption whose type depends on the newly bound type variable. -/
inductive FiniteDerives : Term → TypeCode → Prop where
  | i (A) : FiniteDerives .i (.arrow A A)
  | k (A B) : FiniteDerives .k (.arrow A (.arrow B A))
  | s (A B C) : FiniteDerives .s
      (.arrow (.arrow A (.arrow B C)) (.arrow (.arrow A B) (.arrow A C)))
  | app {f x A B} : FiniteDerives f (.arrow A B) → FiniteDerives x A →
      FiniteDerives (.app f x) B
  | allI {t B} : FiniteDerives t B → FiniteDerives t (.all B)
  | allE {t B} : FiniteDerives t (.all B) → (A : TypeCode) →
      FiniteDerives t (instantiateType B A)
  | reduce {t u A} : FiniteDerives t A → Red t u → FiniteDerives u A

theorem finite_translation {t A} (h : FiniteDerives t A) :
    ∀ ρ, Derives t (interpret A ρ) := by
  induction h with
  | i A => intro ρ; exact .i (interpret A ρ)
  | k A B => intro ρ; exact .k (interpret A ρ) (interpret B ρ)
  | s A B C => intro ρ; exact .s (interpret A ρ) (interpret B ρ) (interpret C ρ)
  | app hf hx ihf ihx => intro ρ; exact .app (ihf ρ) (ihx ρ)
  | allI h ih =>
      intro ρ
      exact .allIntro (fun X => ih (extend X ρ))
  | allE h A ih =>
      intro ρ
      rw [instantiate_sem]
      exact .allElim (ih ρ) (interpret A ρ)
  | reduce h r ih => intro ρ; exact .reduce (ih ρ) r

theorem finite_sound {t A} (h : FiniteDerives t A) (ρ : Nat → Code) :
    (interpret A ρ).accepts t := sound (finite_translation h ρ)

def wellScoped (d : Nat) : TypeCode → Bool
  | .var n => decide (n < d)
  | .bottom => true
  | .arrow A B => wellScoped d A && wellScoped d B
  | .all A => wellScoped (d+1) A

/-- The reduction result carries the actual v2 one-step proof. -/
def certifiedHeadStep : (t : Term) → Option {u : Term // Step t u}
  | .app .i x => some ⟨x, .i x⟩
  | .app (.app .k x) y => some ⟨x, .k x y⟩
  | .app (.app (.app .s f) g) x =>
      some ⟨.app (.app f x) (.app g x), .s f g x⟩
  | .app f x =>
      match certifiedHeadStep f with
      | none => none
      | some u => some ⟨.app u.val x, .left u.property x⟩
  | _ => none

inductive Cert where
  | i : TypeCode → Cert
  | k : TypeCode → TypeCode → Cert
  | s : TypeCode → TypeCode → TypeCode → Cert
  | app : Cert → Cert → Cert
  | allI : Cert → Cert
  | allE : Cert → TypeCode → Cert
  | step : Cert → Cert
  deriving Repr

structure Checked where
  term : Term
  ty : TypeCode
  valid : FiniteDerives term ty

/-- Total elaboration of a finite certificate AST. All type operations are
computable. No proposition about semantic Code membership is a checker input. -/
def check (d : Nat) : Cert → Option Checked
  | .i A =>
      if wellScoped d A then some ⟨.i, .arrow A A, .i A⟩ else none
  | .k A B =>
      if wellScoped d A && wellScoped d B then
        some ⟨.k, .arrow A (.arrow B A), .k A B⟩ else none
  | .s A B C =>
      if wellScoped d A && wellScoped d B && wellScoped d C then
        some ⟨.s, .arrow (.arrow A (.arrow B C))
          (.arrow (.arrow A B) (.arrow A C)), .s A B C⟩ else none
  | .app p q =>
      match check d p, check d q with
      | some f, some x =>
          match hft : f.ty with
          | .arrow A B =>
              if h : A = x.ty then
                have hf : FiniteDerives f.term (.arrow A B) := hft ▸ f.valid
                have hx : FiniteDerives x.term A := h.symm ▸ x.valid
                some ⟨.app f.term x.term, B, .app hf hx⟩
              else none
          | _ => none
      | _, _ => none
  | .allI p =>
      match check (d+1) p with
      | some t => some ⟨t.term, .all t.ty, .allI t.valid⟩
      | none => none
  | .allE p A =>
      if wellScoped d A then
        match check d p with
        | some t =>
            match ht : t.ty with
            | .all B =>
                have h : FiniteDerives t.term (.all B) := ht ▸ t.valid
                some ⟨t.term, instantiateType B A, .allE h A⟩
            | _ => none
        | none => none
      else none
  | .step p =>
      match check d p with
      | some t =>
          match certifiedHeadStep t.term with
          | some u => some ⟨u.val, t.ty, .reduce t.valid (Red.one u.property)⟩
          | none => none
      | none => none

/-- Every returned object carries a finite derivation and therefore realises its
interpreted type under EVERY environment. Parser correctness is a separate task. -/
theorem checked_sound (v : Checked) (ρ : Nat → Code) :
    (interpret v.ty ρ).accepts v.term := finite_sound v.valid ρ

theorem check_cannot_return_bottom (v : Checked) (h : v.ty = .bottom) : False := by
  have hs := checked_sound v (fun _ => Code.top)
  rw [h] at hs
  exact hs

def identityCert : Cert := .allI (.i (.var 0))
def identitySelfCert : Cert := .app (.allE identityCert identityCode) identityCert

/-- Erasure of an accepted all-elimination does not construct a term node. -/
theorem finite_allE_erasure (t : Term) (B A : TypeCode) :
    (t, instantiateType B A).1 = (t, TypeCode.all B).1 := rfl

end OrthemologyV3

#print axioms OrthemologyV3.rename_sem
#print axioms OrthemologyV3.substitute_sem
#print axioms OrthemologyV3.instantiate_sem
#print axioms OrthemologyV3.finite_translation
#print axioms OrthemologyV3.finite_sound
#print axioms OrthemologyV3.checked_sound
#print axioms OrthemologyV3.check_cannot_return_bottom
