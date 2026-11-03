/- Actual finite SKI polynomials and substitution. The binder is compiled without
   eta contraction or body normalisation. New source, UNCOMPILED at 4.19.0. -/
import P01Omega
namespace P01D
open OrthemologyV2 OrthemologyV3
open P01F (cons)

inductive Poly where
  | var : Nat → Poly
  | atom : Term → Poly
  | app : Poly → Poly → Poly
  deriving DecidableEq, Repr

abbrev Env := Nat → Term

def eval (p : Poly) (γ : Env) : Term := match p with
  | .var n => γ n
  | .atom a => a
  | .app f x => .app (eval f γ) (eval x γ)

def psub (σ : Nat → Poly) : Poly → Poly
  | .var n => σ n
  | .atom a => .atom a
  | .app f x => .app (psub σ f) (psub σ x)

def pren (r : Nat → Nat) : Poly → Poly := psub (fun n => .var (r n))

def pup (σ : Nat → Poly) : Nat → Poly
  | 0 => .var 0
  | n+1 => pren Nat.succ (σ n)

@[simp] theorem eval_sub (p : Poly) (σ) (γ) :
    eval (psub σ p) γ = eval p (fun n => eval (σ n) γ) := by
  induction p with
  | var n => rfl
  | atom a => rfl
  | app f x hf hx => simp only [psub, eval, hf, hx]

@[simp] theorem psub_id (p : Poly) : psub Poly.var p = p := by
  induction p with
  | var n => rfl
  | atom a => rfl
  | app f x hf hx => simp only [psub, hf, hx]

theorem psub_comp (p : Poly) (σ τ) :
    psub τ (psub σ p) = psub (fun n => psub τ (σ n)) p := by
  induction p with
  | var n => rfl
  | atom a => rfl
  | app f x hf hx => simp only [psub, hf, hx]

@[simp] theorem eval_ren (p : Poly) (r) (γ) :
    eval (pren r p) γ = eval p (fun n => γ (r n)) := by
  exact eval_sub p _ _

def freeZero : Poly → Bool
  | .var n => n == 0
  | .atom _ => false
  | .app f x => freeZero f || freeZero x

def drop : Poly → Poly := pren Nat.pred

def abstract (p : Poly) : Poly :=
  if freeZero p then match p with
    | .var _ => .atom .i
    | .atom a => .app (.atom .k) (.atom a)
    | .app f x => .app (.app (.atom .s) (abstract f)) (abstract x)
  else .app (.atom .k) (drop p)
termination_by p

/-- Capture-avoiding older-variable images cannot acquire the bound variable. -/
theorem freeZero_pren_succ (p : Poly) : freeZero (pren Nat.succ p) = false := by
  induction p with
  | var n => rfl
  | atom a => rfl
  | app f x hf hx =>
      change (freeZero (pren Nat.succ f) || freeZero (pren Nat.succ x)) = false
      rw [hf,hx]; rfl

theorem drop_pren_succ (p : Poly) : drop (pren Nat.succ p) = p := by
  induction p with
  | var n => rfl
  | atom a => rfl
  | app f x hf hx =>
      change Poly.app (drop (pren Nat.succ f)) (drop (pren Nat.succ x)) = .app f x
      rw [hf,hx]

theorem freeZero_lifted_sub (p : Poly) (σ : Nat → Poly) :
    freeZero (psub (pup σ) p) = freeZero p := by
  induction p with
  | var n =>
      cases n with
      | zero => rfl
      | succ n => exact freeZero_pren_succ (σ n)
  | atom a => rfl
  | app f x hf hx =>
      change (freeZero (psub (pup σ) f) || freeZero (psub (pup σ) x)) =
        (freeZero f || freeZero x)
      rw [hf,hx]

theorem drop_lifted_sub_absent (p : Poly) (σ : Nat → Poly) (h : freeZero p = false) :
    drop (psub (pup σ) p) = psub σ (drop p) := by
  induction p with
  | var n =>
      cases n with
      | zero => simp [freeZero] at h
      | succ n => exact drop_pren_succ (σ n)
  | atom a => rfl
  | app f x hf hx =>
      have hs : freeZero f = false ∧ freeZero x = false := by
        simpa only [freeZero,Bool.or_eq_false_iff] using h
      exact congrArg₂ Poly.app (hf hs.1) (hx hs.2)

theorem abstract_absent (p : Poly) (h : freeZero p = false) :
    abstract p = .app (.atom .k) (drop p) := by
  rw [abstract.eq_def]
  simp only [h,Bool.false_eq_true,↓reduceIte]

theorem abstract_present_app (f x : Poly) (h : freeZero (.app f x) = true) :
    abstract (.app f x) = .app (.app (.atom .s) (abstract f)) (abstract x) := by
  simp only [abstract,h,Bool.true_eq,↓reduceIte]

/-- The stronger preserved literal square, for the selected WHOLE-SUBTERM K
    priority backend and capture-avoiding lifted substitution. This is not a
    congruence law for arbitrary body conversion and not an eta shortcut. -/
theorem abstraction_naturality (p : Poly) (σ : Nat → Poly) :
    abstract (psub (pup σ) p) = psub σ (abstract p) := by
  induction p with
  | var n =>
      cases n with
      | zero => simp [psub, pup, abstract, freeZero]
      | succ n =>
          simp only [psub, pup]
          rw [abstract_absent (.var (n+1)) (by rfl)]
          change abstract (pren Nat.succ (σ n)) = .app (.atom .k) (σ n)
          rw [abstract_absent _ (freeZero_pren_succ _),drop_pren_succ]
  | atom a => simp [psub, abstract, freeZero, drop, pren]
  | app f x hf hx =>
      by_cases h : freeZero (.app f x) = true
      · have h' : freeZero (.app (psub (pup σ) f) (psub (pup σ) x)) = true := by
          exact (freeZero_lifted_sub (.app f x) σ).trans h
        change abstract (.app (psub (pup σ) f) (psub (pup σ) x)) =
          psub σ (abstract (.app f x))
        rw [abstract_present_app _ _ h',abstract_present_app _ _ h]
        change Poly.app (.app (.atom .s) (abstract (psub (pup σ) f)))
          (abstract (psub (pup σ) x)) =
          .app (.app (.atom .s) (psub σ (abstract f))) (psub σ (abstract x))
        rw [hf,hx]
      · have h0 : freeZero (.app f x) = false := Bool.eq_false_of_not_eq_true h
        have h' : freeZero (psub (pup σ) (.app f x)) = false :=
          (freeZero_lifted_sub (.app f x) σ).trans h0
        rw [abstract_absent _ h',abstract_absent _ h0]
        change Poly.app (.atom .k) (drop (psub (pup σ) (.app f x))) =
          .app (.atom .k) (psub σ (drop (.app f x)))
        rw [drop_lifted_sub_absent _ _ h0]

theorem eval_absent (p : Poly) (h : freeZero p = false) (γ) (a) :
    eval p (cons a γ) = eval (drop p) γ := by
  induction p with
  | var n => cases n <;> simp_all [freeZero, eval, drop, pren, psub, cons]
  | atom t => rfl
  | app f x hf hx =>
      have hs : freeZero f = false ∧ freeZero x = false := by
        simpa only [freeZero, Bool.or_eq_false_iff] using h
      exact congrArg₂ Term.app (hf hs.1) (hx hs.2)

/-- Real compatible source reduction, valid under any closing valuation. -/
theorem abstraction_beta (p : Poly) (γ : Env) (a : Term) :
    Red (.app (eval (abstract p) γ) a) (eval p (cons a γ)) := by
  induction p with
  | var n =>
      cases n with
      | zero => simpa [abstract, freeZero, eval, cons] using Red.one (.i a)
      | succ n => simpa [abstract, freeZero, drop, pren, psub, eval, cons] using Red.one (.k (γ n) a)
  | atom t => simpa [abstract, freeZero, drop, pren, psub, eval] using Red.one (.k t a)
  | app f x hf hx =>
      by_cases h : freeZero (.app f x) = true
      · simp only [abstract, h, Bool.true_eq, ↓reduceIte, eval]
        exact .tail (.s _ _ a) (P01Source.red_app hf hx)
      · have h' : freeZero (.app f x) = false := Bool.eq_false_of_not_eq_true h
        have e := eval_absent (.app f x) h' γ a
        rw [e]
        simp only [abstract, h', Bool.false_eq_true, ↓reduceIte, eval]
        exact Red.one (.k _ a)

/-- The substitution square required by dependent application/abstraction is
    proved at applications. It never asserts raw equality of un-applied trackers. -/
theorem abstraction_substitution (p : Poly) (σ : Nat → Poly) (γ : Env) (a : Term) :
    Conv (.app (eval (abstract (psub (pup σ) p)) γ) a)
      (.app (eval (abstract p) (fun n => eval (σ n) γ)) a) := by
  have l := abstraction_beta (psub (pup σ) p) γ a
  have r := abstraction_beta p (fun n => eval (σ n) γ) a
  have e : (fun n => eval (pup σ n) (cons a γ)) =
      cons a (fun n => eval (σ n) γ) := by
    funext n; cases n <;> simp [pup, eval, eval_ren, cons]
  rw [eval_sub, e] at l
  exact .trans (P01Source.red_conv l) (.symm (P01Source.red_conv r))

def pairPoly (x y : Poly) : Poly :=
  .app (.app (.atom .s) (.app (.app (.atom .s) (.atom .i)) (.app (.atom .k) x)))
    (.app (.atom .k) y)
def fstPoly (z : Poly) := Poly.app z (.atom .k)
def sndPoly (z : Poly) := Poly.app z (.app (.atom .k) (.atom .i))
def jPoly (d y p : Poly) := Poly.app (.app (.app (.atom .k) (.app (.atom .k) d)) y) p

@[simp] theorem eval_pair (x y : Poly) (γ) :
    eval (pairPoly x y) γ = pairTerm (eval x γ) (eval y γ) := rfl
@[simp] theorem eval_fst (z : Poly) (γ) : eval (fstPoly z) γ = firstTerm (eval z γ) := rfl
@[simp] theorem eval_snd (z : Poly) (γ) : eval (sndPoly z) γ = secondTerm (eval z γ) := rfl

theorem eval_j (d y p : Poly) (γ) : Red (eval (jPoly d y p) γ) (eval d γ) :=
  .tail (.left (.k (.app .k (eval d γ)) (eval y γ)) (eval p γ))
    (.tail (.k (eval d γ) (eval p γ)) (.refl _))
end P01D
