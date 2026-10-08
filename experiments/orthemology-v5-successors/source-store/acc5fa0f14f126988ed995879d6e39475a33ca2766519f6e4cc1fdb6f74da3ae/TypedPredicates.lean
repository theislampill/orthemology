/- Raw syntax-indexed predicates, defined before any laws or semantic records. -/
import TypedSyntax
namespace P01TC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

def F : Ty → OEnv → Env → Term → Term → Prop
  | .param n, ρ, _, t, u => (ρ n).rel t u
  | .bottom, _, _, _, _ => False
  | .allFinite C, ρ, _, t, u => ((P01R.interpret (.all C)).obj ρ).rel t u
  | .raw, _, _, t, u => Conv t u
  | .pi A B, ρ, η, f, g => ∀ a b, F A ρ η a b → F B ρ (cons a η) (.app f a) (.app g b)
  | .sigma A B, ρ, η, z, w => Represented z ∧ Represented w ∧
      F A ρ η (firstTerm z) (firstTerm w) ∧
      F B ρ (cons (firstTerm z) η) (secondTerm z) (secondTerm w)
  | .identity A p q, ρ, η, u, v => F A ρ η (eval p η) (eval q η) ∧ Conv u .i ∧ Conv v .i

def G : Ty → REnv → Env → Env → Term → Term → Prop
  | .param n, r, _, _, t, u => r.rel n t u
  | .bottom, _, _, _, _, _ => False
  | .allFinite C, r, _, _, t, u => (P01R.interpret (.all C)).rel r t u
  | .raw, _, _, _, t, u => Conv t u
  | .pi A B, r, η, ξ, f, g => F (.pi A B) r.left η f f ∧ F (.pi A B) r.right ξ g g ∧
      ∀ a b, G A r η ξ a b → G B r (cons a η) (cons b ξ) (.app f a) (.app g b)
  | .sigma A B, r, η, ξ, z, w => F (.sigma A B) r.left η z z ∧ F (.sigma A B) r.right ξ w w ∧
      Represented z ∧ Represented w ∧ G A r η ξ (firstTerm z) (firstTerm w) ∧
      G B r (cons (firstTerm z) η) (cons (firstTerm w) ξ) (secondTerm z) (secondTerm w)
  | .identity A p q, r, η, ξ, u, v =>
      F A r.left η (eval p η) (eval q η) ∧ F A r.right ξ (eval p ξ) (eval q ξ) ∧
      Conv u .i ∧ Conv v .i

/-- Total evaluation environments are zero padded representations of finite tuples. -/
def zeroEnv : Env := fun _ => .zero
def tail (η : Env) : Env := fun n => η (n+1)

def D : Tel → OEnv → Env → Prop
  | [], _, η => η = zeroEnv
  | A :: Γ, ρ, η => D Γ ρ (tail η) ∧ F A ρ (tail η) (η 0) (η 0)

def E : Tel → OEnv → Env → Env → Prop
  | [], _, η, ξ => η = zeroEnv ∧ ξ = zeroEnv
  | A :: Γ, ρ, η, ξ => E Γ ρ (tail η) (tail ξ) ∧ F A ρ (tail η) (η 0) (ξ 0)

def H : Tel → REnv → Env → Env → Prop
  | [], _, η, ξ => η = zeroEnv ∧ ξ = zeroEnv
  | A :: Γ, r, η, ξ => H Γ r (tail η) (tail ξ) ∧ G A r (tail η) (tail ξ) (η 0) (ξ 0)

@[simp] theorem tail_cons (a : Term) (η : Env) : tail (cons a η) = η := rfl
@[simp] theorem cons_head_tail (η : Env) : cons (η 0) (tail η) = η := by
  funext n; cases n <;> rfl

@[simp] theorem eval_pup_env (σ : Nat → Poly) (η : Env) (a : Term) :
    (fun n => eval (pup σ n) (cons a η)) = cons a (fun n => eval (σ n) η) := by
  funext n; cases n <;> simp [pup, eval, eval_ren, cons]

@[simp] theorem eval_cons_poly (a : Poly) (σ : Nat → Poly) (η : Env) :
    (fun n => eval (cons a σ n) η) = cons (eval a η) (fun n => eval (σ n) η) := by
  funext n; cases n <;> rfl

theorem F_subst (A : Ty) (σ : Nat → Poly) (ρ : OEnv) (η : Env) (t u : Term) :
    F (subst σ A) ρ η t u = F A ρ (fun n => eval (σ n) η) t u := by
  induction A generalizing σ η t u with
  | param n => rfl
  | bottom => rfl
  | allFinite C => rfl
  | raw => rfl
  | identity A p q ih => simp only [subst, F, ih, eval_sub]
  | pi A B ha hb =>
      simp only [subst, F, ha, hb, eval_pup_env]
  | sigma A B ha hb =>
      simp only [subst, F, ha, hb, eval_pup_env]

theorem G_subst (A : Ty) (σ : Nat → Poly) (r : REnv) (η ξ : Env) (t u : Term) :
    G (subst σ A) r η ξ t u =
      G A r (fun n => eval (σ n) η) (fun n => eval (σ n) ξ) t u := by
  induction A generalizing σ η ξ t u with
  | param n => rfl
  | bottom => rfl
  | allFinite C => rfl
  | raw => rfl
  | identity A p q ih => simp only [subst,G,F_subst,eval_sub]
  | pi A B ha hb =>
      change (F (subst σ (.pi A B)) r.left η t t ∧ F (subst σ (.pi A B)) r.right ξ u u ∧ _) = _
      simp only [F_subst,G,ha,hb,eval_pup_env]
  | sigma A B ha hb =>
      change (F (subst σ (.sigma A B)) r.left η t t ∧ F (subst σ (.sigma A B)) r.right ξ u u ∧ _) = _
      simp only [F_subst,G,ha,hb,eval_pup_env]

theorem F_wk (A : Ty) (ρ : OEnv) (η : Env) (a t u : Term) :
    F (wk A) ρ (cons a η) t u = F A ρ η t u := F_subst A _ ρ _ t u

theorem G_wk (A : Ty) (r : REnv) (η ξ : Env) (a b t u : Term) :
    G (wk A) r (cons a η) (cons b ξ) t u = G A r η ξ t u := G_subst A _ r _ _ t u

theorem F_inst (B : Ty) (a : Poly) (ρ : OEnv) (η : Env) (t u : Term) :
    F (inst B a) ρ η t u = F B ρ (cons (eval a η) η) t u := by
  simpa only [inst,eval_cons_poly,eval] using F_subst B (cons a Poly.var) ρ η t u

theorem G_inst (B : Ty) (a : Poly) (r : REnv) (η ξ : Env) (t u : Term) :
    G (inst B a) r η ξ t u = G B r (cons (eval a η) η) (cons (eval a ξ) ξ) t u :=
  by simpa only [inst,eval_cons_poly,eval] using G_subst B (cons a Poly.var) r η ξ t u

theorem F_motiveAt (B : Ty) (y e : Poly) (ρ : OEnv) (η : Env) (t u : Term) :
    F (motiveAt B y e) ρ η t u = F B ρ (cons (eval e η) (cons (eval y η) η)) t u :=
  by simpa only [motiveAt,eval_cons_poly,eval] using F_subst B (cons e (cons y Poly.var)) ρ η t u

theorem G_motiveAt (B : Ty) (y e : Poly) (r : REnv) (η ξ : Env) (t u : Term) :
    G (motiveAt B y e) r η ξ t u =
      G B r (cons (eval e η) (cons (eval y η) η)) (cons (eval e ξ) (cons (eval y ξ) ξ)) t u :=
  by simpa only [motiveAt,eval_cons_poly,eval] using G_subst B (cons e (cons y Poly.var)) r η ξ t u

end P01TC
