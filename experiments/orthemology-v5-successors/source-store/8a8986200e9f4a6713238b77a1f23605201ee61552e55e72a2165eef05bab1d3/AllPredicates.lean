/- Structural paired raw interpretation. All unary uniformity uses only its smaller body's G. -/
import AllSyntax
namespace P01AC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

abbrev Unary := OEnv → Env → Term → Term → Prop
abbrev Hetero := REnv → Env → Env → Term → Term → Prop

def predicates : Ty → Unary × Hetero
  | .param n => ⟨fun ρ _ t u => (ρ n).rel t u, fun r _ _ t u => r.rel n t u⟩
  | .bottom => ⟨fun _ _ _ _ => False, fun _ _ _ _ _ => False⟩
  | .raw => ⟨fun _ _ t u => Conv t u, fun _ _ _ t u => Conv t u⟩
  | .pi A B =>
      let a := predicates A
      let b := predicates B
      let f : Unary := fun ρ η f g => ∀ x y, a.1 ρ η x y → b.1 ρ (cons x η) (.app f x) (.app g y)
      ⟨f, fun r η ξ t u => f r.left η t t ∧ f r.right ξ u u ∧
        ∀ x y, a.2 r η ξ x y → b.2 r (cons x η) (cons y ξ) (.app t x) (.app u y)⟩
  | .sigma A B =>
      let a := predicates A
      let b := predicates B
      let f : Unary := fun ρ η z w => Represented z ∧ Represented w ∧
        a.1 ρ η (firstTerm z) (firstTerm w) ∧ b.1 ρ (cons (firstTerm z) η) (secondTerm z) (secondTerm w)
      ⟨f, fun r η ξ z w => f r.left η z z ∧ f r.right ξ w w ∧
        Represented z ∧ Represented w ∧ a.2 r η ξ (firstTerm z) (firstTerm w) ∧
        b.2 r (cons (firstTerm z) η) (cons (firstTerm w) ξ) (secondTerm z) (secondTerm w)⟩
  | .identity A p q =>
      let a := predicates A
      ⟨fun ρ η u v => a.1 ρ η (eval p η) (eval q η) ∧ Conv u .i ∧ Conv v .i,
       fun r η ξ u v => a.1 r.left η (eval p η) (eval q η) ∧
         a.1 r.right ξ (eval p ξ) (eval q ξ) ∧ Conv u .i ∧ Conv v .i⟩
  | .all B =>
      let b := predicates B
      let uniform := fun ρ η t => ∀ (P Q : PER) (R : Link P Q), b.2 (extendEnv R (diagEnv ρ)) η η t t
      let f : Unary := fun ρ η t u => uniform ρ η t ∧ uniform ρ η u ∧ ∀ P, b.1 (cons P ρ) η t u
      ⟨f, fun r η ξ t u => f r.left η t t ∧ f r.right ξ u u ∧
        ∀ (P Q : PER) (R : Link P Q), b.2 (extendEnv R r) η ξ t u⟩

def F (A : Ty) : Unary := (predicates A).1
def G (A : Ty) : Hetero := (predicates A).2

theorem F_param (n : Nat) (ρ : OEnv) (η : Env) (t u : Term) :
    F (.param n) ρ η t u =
      ((ρ n).rel t u) := rfl

theorem F_bottom  (ρ : OEnv) (η : Env) (t u : Term) :
    F (.bottom) ρ η t u =
      (False) := rfl

theorem F_raw  (ρ : OEnv) (η : Env) (t u : Term) :
    F (.raw) ρ η t u =
      (Conv t u) := rfl

theorem F_pi (A B : Ty) (ρ : OEnv) (η : Env) (f g : Term) :
    F (.pi A B) ρ η f g =
      (∀ a b, F A ρ η a b → F B ρ (cons a η) (.app f a) (.app g b)) := rfl

theorem F_sigma (A B : Ty) (ρ : OEnv) (η : Env) (z w : Term) :
    F (.sigma A B) ρ η z w =
      (Represented z ∧ Represented w ∧
      F A ρ η (firstTerm z) (firstTerm w) ∧
      F B ρ (cons (firstTerm z) η) (secondTerm z) (secondTerm w)) := rfl

theorem F_identity (A : Ty) (p q : Poly) (ρ : OEnv) (η : Env) (u v : Term) :
    F (.identity A p q) ρ η u v =
      (F A ρ η (eval p η) (eval q η) ∧ Conv u .i ∧ Conv v .i) := rfl

theorem G_param (n : Nat) (r : REnv) (η ξ : Env) (t u : Term) :
    G (.param n) r η ξ t u =
      (r.rel n t u) := rfl

theorem G_bottom  (r : REnv) (η ξ : Env) (t u : Term) :
    G (.bottom) r η ξ t u =
      (False) := rfl

theorem G_raw  (r : REnv) (η ξ : Env) (t u : Term) :
    G (.raw) r η ξ t u =
      (Conv t u) := rfl

theorem G_pi (A B : Ty) (r : REnv) (η ξ : Env) (f g : Term) :
    G (.pi A B) r η ξ f g =
      (F (.pi A B) r.left η f f ∧ F (.pi A B) r.right ξ g g ∧
      ∀ a b, G A r η ξ a b → G B r (cons a η) (cons b ξ) (.app f a) (.app g b)) := rfl

theorem G_sigma (A B : Ty) (r : REnv) (η ξ : Env) (z w : Term) :
    G (.sigma A B) r η ξ z w =
      (F (.sigma A B) r.left η z z ∧ F (.sigma A B) r.right ξ w w ∧
      Represented z ∧ Represented w ∧ G A r η ξ (firstTerm z) (firstTerm w) ∧
      G B r (cons (firstTerm z) η) (cons (firstTerm w) ξ) (secondTerm z) (secondTerm w)) := rfl

theorem G_identity (A : Ty) (p q : Poly) (r : REnv) (η ξ : Env) (u v : Term) :
    G (.identity A p q) r η ξ u v =
      (F A r.left η (eval p η) (eval q η) ∧ F A r.right ξ (eval p ξ) (eval q ξ) ∧
      Conv u .i ∧ Conv v .i) := rfl

theorem F_all (B : Ty) (ρ : OEnv) (η : Env) (t u : Term) :
    F (.all B) ρ η t u =
      ((∀ (P Q : PER) (R : Link P Q), G B (extendEnv R (diagEnv ρ)) η η t t) ∧
       (∀ (P Q : PER) (R : Link P Q), G B (extendEnv R (diagEnv ρ)) η η u u) ∧
       ∀ P, F B (cons P ρ) η t u) := rfl

theorem G_all (B : Ty) (r : REnv) (η ξ : Env) (t u : Term) :
    G (.all B) r η ξ t u =
      (F (.all B) r.left η t t ∧ F (.all B) r.right ξ u u ∧
       ∀ (P Q : PER) (R : Link P Q), G B (extendEnv R r) η ξ t u) := rfl

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


end P01AC
