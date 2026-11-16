/- Curry System F, including unrestricted term contexts with the correct
   type-variable lifting at universal introduction. No reduction rule is added
   to typing. Subject reduction is proved from substitution and lambda generation.
   New attempt-0003 authored source; UNCOMPILED, no kernel claim. -/
import P01LambdaSyntax
namespace P01F
open OrthemologyV2 OrthemologyV3
abbrev Context := Nat → Ty

def shiftContext (Γ : Context) : Context := fun n => rename Nat.succ (Γ n)
def subContext (σ : Nat → Ty) (Γ : Context) : Context := fun n => substitute σ (Γ n)

inductive Has : Context → LTerm → Ty → Prop where
  | var (Γ) (n) : Has Γ (.var n) (Γ n)
  | lam {Γ b A B} : Has (cons A Γ) b B → Has Γ (.lam b) (.arrow A B)
  | app {Γ f a A B} : Has Γ f (.arrow A B) → Has Γ a A → Has Γ (.app f a) B
  | allI {Γ t B} : Has (shiftContext Γ) t B → Has Γ t (.all B)
  | allE {Γ t B} : Has Γ t (.all B) → (A : Ty) → Has Γ t (instantiateType B A)

@[simp] theorem subContext_cons (σ) (A) (Γ) :
    subContext σ (cons A Γ) = cons (substitute σ A) (subContext σ Γ) := by
  funext n; cases n <;> rfl

@[simp] theorem subContext_up (σ) (Γ) :
    subContext (upSub σ) (shiftContext Γ) = shiftContext (subContext σ Γ) := by
  funext n; exact ty_sub_up_shift (Γ n) σ

@[simp] theorem subContext_single_shift (A) (Γ) :
    subContext (singleSub A) (shiftContext Γ) = Γ := by
  funext n; exact ty_inst_shift (Γ n) A

/-- Type substitution changes both assumptions and the conclusion; runtime syntax
    is unchanged. No term assumption is held fixed across a type binder. -/
theorem type_substitution {Γ t A} (h : Has Γ t A) (σ : Nat → Ty) :
    Has (subContext σ Γ) t (substitute σ A) := by
  induction h generalizing σ with
  | var Γ n => exact .var _ n
  | lam h ih =>
      apply Has.lam
      simpa only [subContext_cons] using ih σ
  | app hf ha ihf iha => exact .app (ihf σ) (iha σ)
  | allI h ih =>
      apply Has.allI
      simpa only [subContext_up] using ih (upSub σ)
  | allE h A ih =>
      rw [ty_sub_inst]
      exact .allE (ih σ) (substitute σ A)

theorem type_renaming {Γ t A} (h : Has Γ t A) (r : Nat → Nat) :
    Has (fun n => rename r (Γ n)) t (rename r A) := by
  have hs := type_substitution h (fun n => TypeCode.var (r n))
  have e : subContext (fun n => TypeCode.var (r n)) Γ = (fun n => rename r (Γ n)) := by
    funext n
    exact ty_sub_vars (Γ n) r
  rw [e, ty_sub_vars] at hs
  exact hs

theorem term_renaming {Γ t A} (h : Has Γ t A) :
    ∀ (Δ : Context) (r : Nat → Nat), (∀ n, Γ n = Δ (r n)) →
      Has Δ (ren r t) A := by
  induction h with
  | var Γ n =>
      intro Δ r e
      rw [e n]
      exact .var Δ (r n)
  | lam h ih =>
      intro Δ r e
      apply Has.lam
      apply ih (cons _ Δ) (liftRen r)
      intro n; cases n with
      | zero => rfl
      | succ n => exact e n
  | app hf ha ihf iha =>
      intro Δ r e
      exact .app (ihf Δ r e) (iha Δ r e)
  | allI h ih =>
      intro Δ r e
      apply Has.allI
      apply ih (shiftContext Δ) r
      intro n; exact congrArg (rename Nat.succ) (e n)
  | allE h X ih =>
      intro Δ r e
      exact .allE (ih Δ r e) X

theorem term_weakening {Γ t A} (h : Has Γ t A) (B : Ty) :
    Has (cons B Γ) (ren Nat.succ t) A :=
  term_renaming h (cons B Γ) Nat.succ (fun _ => rfl)

/-- Simultaneous, capture-avoiding term substitution, including the allI case. -/
theorem term_substitution {Γ t A} (h : Has Γ t A) :
    ∀ (Δ : Context) (σ : Nat → LTerm), (∀ n, Has Δ (σ n) (Γ n)) →
      Has Δ (sub σ t) A := by
  induction h with
  | var Γ n => intro Δ σ hs; exact hs n
  | lam h ih =>
      intro Δ σ hs
      apply Has.lam
      apply ih (cons _ Δ) (up σ)
      intro n
      cases n with
      | zero => exact .var _ 0
      | succ n => exact term_weakening (hs n) _
  | app hf ha ihf iha =>
      intro Δ σ hs
      exact .app (ihf Δ σ hs) (iha Δ σ hs)
  | allI h ih =>
      intro Δ σ hs
      apply Has.allI
      apply ih (shiftContext Δ) σ
      intro n
      exact type_renaming (hs n) Nat.succ
  | allE h X ih =>
      intro Δ σ hs
      exact .allE (ih Δ σ hs) X

theorem instantiate_term {Γ b a A B}
    (hb : Has (cons A Γ) b B) (ha : Has Γ a A) : Has Γ (inst b a) B := by
  apply term_substitution hb Γ (single a)
  intro n
  cases n with
  | zero => exact ha
  | succ n => exact .var Γ n

/-- Lambda-headed typing without an allE constructor. This is an auxiliary view
    derived below, not an alternative assumption about Curry typing. -/
inductive LamView : Context → LTerm → Ty → Prop where
  | arrow {Γ b A B} : Has (cons A Γ) b B → LamView Γ b (.arrow A B)
  | all {Γ b B} : LamView (shiftContext Γ) b B → LamView Γ b (.all B)

theorem lamView_substitution {Γ b A} (h : LamView Γ b A) (σ : Nat → Ty) :
    LamView (subContext σ Γ) b (substitute σ A) := by
  induction h generalizing σ with
  | arrow h =>
      apply LamView.arrow
      simpa only [subContext_cons] using type_substitution h σ
  | all h ih =>
      apply LamView.all
      simpa only [subContext_up] using ih (upSub σ)

theorem lamView_instantiation {Γ b B} (h : LamView Γ b (.all B)) (A : Ty) :
    LamView Γ b (instantiateType B A) := by
  cases h with
  | all h =>
      simpa only [subContext_single_shift] using
        lamView_substitution h (singleSub A)

/-- The difficult Curry inversion step: universal introduction/elimination
    surrounding a lambda is eliminated by actual type substitution. -/
theorem lambda_view {Γ t A} (h : Has Γ t A) :
    ∀ b, t = .lam b → LamView Γ b A := by
  induction h with
  | var Γ n => intro b e; cases e
  | lam h ih => intro b e; cases e; exact .arrow h
  | app hf ha ihf iha => intro b e; cases e
  | allI h ih => intro b e; exact .all (ih b e)
  | allE h X ih => intro b e; exact lamView_instantiation (ih b e) X

theorem lambda_generation {Γ b A B} (h : Has Γ (.lam b) (.arrow A B)) :
    Has (cons A Γ) b B := by
  have hv := lambda_view h b rfl
  cases hv with
  | arrow hb => exact hb

/-- Standard compatible beta subject reduction. Reduction is NOT a typing rule. -/
theorem subject_reduction {Γ t A} (h : Has Γ t A) :
    ∀ {u}, Beta t u → Has Γ u A := by
  induction h with
  | var Γ n => intro u r; cases r
  | lam hb ih =>
      intro u r
      cases r with
      | under r => exact .lam (ih r)
  | app hf ha ihf iha =>
      intro u r
      cases r with
      | root b a => exact instantiate_term (lambda_generation hf) ha
      | left r a => exact .app (ihf r) ha
      | right f r => exact .app hf (iha r)
  | allI h ih => intro u r; exact .allI (ih r)
  | allE h X ih => intro u r; exact .allE (ih r) X

theorem subject_reduction_star {Γ t u A} (h : Has Γ t A) (r : BStar t u) :
    Has Γ u A := by
  induction r with
  | refl => exact h
  | tail s r ih => exact ih (subject_reduction h s)
end P01F
