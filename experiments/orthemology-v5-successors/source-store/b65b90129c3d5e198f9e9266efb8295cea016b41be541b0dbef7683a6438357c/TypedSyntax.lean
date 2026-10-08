/- Finite typed telescopes over the unchanged source polynomials. -/
import SubstitutionSyntax
namespace P01TC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

inductive Ty where
  | param : Nat → Ty
  | bottom : Ty
  | allFinite : TypeCode → Ty
  | raw : Ty
  | pi : Ty → Ty → Ty
  | sigma : Ty → Ty → Ty
  | identity : Ty → Poly → Poly → Ty
  deriving DecidableEq

def subst (σ : Nat → Poly) : Ty → Ty
  | .param n => .param n
  | .bottom => .bottom
  | .allFinite C => .allFinite C
  | .raw => .raw
  | .pi A B => .pi (subst σ A) (subst (pup σ) B)
  | .sigma A B => .sigma (subst σ A) (subst (pup σ) B)
  | .identity A p q => .identity (subst σ A) (psub σ p) (psub σ q)

def wk (A : Ty) := subst (fun n => .var (n+1)) A
def inst (B : Ty) (a : Poly) := subst (cons a Poly.var) B
def motiveAt (B : Ty) (y e : Poly) := subst (cons e (cons y Poly.var)) B
def arr (A B : Ty) := Ty.pi A (wk B)

def fin : TypeCode → Ty
  | .var n => .param n
  | .bottom => .bottom
  | .arrow A B => arr (fin A) (fin B)
  | .all B => .allFinite B

abbrev Tel := List Ty

def Scoped (n : Nat) : Poly → Prop
  | .var k => k < n
  | .atom _ => True
  | .app f a => Scoped n f ∧ Scoped n a

def TyScoped (n : Nat) : Ty → Prop
  | .param _ | .bottom | .allFinite _ | .raw => True
  | .pi A B | .sigma A B => TyScoped n A ∧ TyScoped (n+1) B
  | .identity A p q => TyScoped n A ∧ Scoped n p ∧ Scoped n q

/-- Declaration types are literally weakened at every intervening binder. -/
inductive Lookup : Tel → Nat → Ty → Prop
  | zero : Lookup (A :: Γ) 0 (wk A)
  | succ : Lookup Γ n A → Lookup (B :: Γ) (n+1) (wk A)

def theta (Γ : Tel) (A : Ty) (x : Poly) : Tel :=
  Ty.identity (wk A) (pren Nat.succ x) (.var 0) :: A :: Γ

/- All premises below are finite syntax judgements or syntactic scope/conversion.
   No semantic relation, law record or arbitrary family is accepted. -/
mutual
  inductive Ctx : Tel → Prop
    | nil : Ctx []
    | ext : Ctx Γ → Form Γ A → Ctx (A :: Γ)
  inductive Form : Tel → Ty → Prop
    | param : Ctx Γ → Form Γ (.param n)
    | bottom : Ctx Γ → Form Γ .bottom
    | allFinite : Ctx Γ → Form Γ (.allFinite C)
    | raw : Ctx Γ → Form Γ .raw
    | pi : Form Γ A → Form (A :: Γ) B → Form Γ (.pi A B)
    | sigma : Form Γ A → Form (A :: Γ) B → Form Γ (.sigma A B)
    | identity : Form Γ A → Has Γ p A → Has Γ q A → Form Γ (.identity A p q)
  inductive Has : Tel → Poly → Ty → Prop
    | var : Form Γ A → Lookup Γ n A → Has Γ (.var n) A
    | i : Form Γ A → Form Γ (arr A A) → Has Γ (.atom .i) (arr A A)
    | k : Form Γ A → Form Γ B → Form Γ (arr A (arr B A)) →
        Has Γ (.atom .k) (arr A (arr B A))
    | s : Form Γ A → Form Γ B → Form Γ C →
        Form Γ (arr (arr A (arr B C)) (arr (arr A B) (arr A C))) →
        Has Γ (.atom .s) (arr (arr A (arr B C)) (arr (arr A B) (arr A C)))
    | finite : Form Γ (fin C) → FiniteDerives t C → Has Γ (.atom t) (fin C)
    | rawAtom : Form Γ .raw → Has Γ (.atom t) .raw
    | rawApp : Form Γ .raw → Has Γ f .raw → Has Γ a .raw → Has Γ (.app f a) .raw
    | piIntro : Form Γ (.pi A B) → Has (A :: Γ) b B → Scoped Γ.length (abstract b) →
        Has Γ (abstract b) (.pi A B)
    | piElim : Form Γ (.pi A B) → Form Γ (inst B a) →
        Has Γ f (.pi A B) → Has Γ a A → Has Γ (.app f a) (inst B a)
    | sigmaIntro : Form Γ (.sigma A B) → Form Γ (inst B a) →
        Has Γ a A → Has Γ b (inst B a) → Has Γ (pairPoly a b) (.sigma A B)
    | sigmaFst : Form Γ A → Form Γ (.sigma A B) → Has Γ z (.sigma A B) →
        Has Γ (fstPoly z) A
    | sigmaSnd : Form Γ (.sigma A B) → Form Γ (inst B (fstPoly z)) →
        Has Γ z (.sigma A B) → Has Γ (sndPoly z) (inst B (fstPoly z))
    | identityIntro : Form Γ (.identity A p q) → Has Γ p A → Has Γ q A →
        P01DF.PolyConv p q → Has Γ (.atom .i) (.identity A p q)
    | proofErase : Form Γ .raw → Form Γ (.identity A x y) →
        Has Γ p (.identity A x y) → Has Γ p .raw
    | j : Form Γ A → Form (theta Γ A x) B →
        Form Γ (.identity A x y) → Form Γ (motiveAt B x (.atom .i)) →
        Form Γ (motiveAt B y e) → Has Γ x A → Has Γ y A →
        Has Γ e (.identity A x y) → Has Γ d (motiveAt B x (.atom .i)) →
        Has Γ (jPoly d y e) (motiveAt B y e)
    | conv : Form Γ A → Has Γ p A → P01DF.PolyConv p q → Scoped Γ.length q → Has Γ q A
end

end P01TC
