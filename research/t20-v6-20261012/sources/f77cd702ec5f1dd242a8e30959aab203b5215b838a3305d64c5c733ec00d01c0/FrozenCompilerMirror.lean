import OpenTermStandardness

/- Isolated open-term interpretation of the pinned compiler formulas.
   No HasE source import, target proof, or full soundness theorem is claimed.
   The binder is the exact whole-subterm K-priority algorithm, not eta reduction. -/
namespace OpenTermStandardness
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

inductive P where
  | var : Nat → P
  | atom : T → P
  | app : P → P → P
  deriving DecidableEq, Repr

def cons (a : T) (η : Nat → T) : Nat → T
  | 0 => a
  | n+1 => η n

def eval : P → (Nat → T) → T
  | .var n, η => η n
  | .atom t, _ => t
  | .app f a, η => eval f η ⬝ eval a η

def psub (σ : Nat → P) : P → P
  | .var n => σ n
  | .atom t => .atom t
  | .app f a => .app (psub σ f) (psub σ a)

def pren (r : Nat → Nat) : P → P := psub (fun n => .var (r n))
def freeZero : P → Bool
  | .var n => n == 0
  | .atom _ => false
  | .app f x => freeZero f || freeZero x
def drop : P → P := pren Nat.pred
def abstract (p : P) : P :=
  if freeZero p then match p with
    | .var _ => .atom .i
    | .atom a => .app (.atom .k) (.atom a)
    | .app f x => .app (.app (.atom .s) (abstract f)) (abstract x)
  else .app (.atom .k) (drop p)
termination_by p

theorem eval_absent (p : P) (h : freeZero p = false) (η) (a) :
    eval p (cons a η) = eval (drop p) η := by
  induction p with
  | var n => cases n <;> simp_all [freeZero, eval, drop, pren, psub, cons]
  | atom t => rfl
  | app f x hf hx =>
      have hs : freeZero f = false ∧ freeZero x = false := by
        simpa only [freeZero, Bool.or_eq_false_iff] using h
      change (eval f (cons a η)).app (eval x (cons a η)) =
        (eval (drop f) η).app (eval (drop x) η)
      rw [hf hs.1, hx hs.2]

theorem abstraction_beta (p : P) (η : Nat → T) (a : T) :
    Conv (eval (abstract p) η ⬝ a) (eval p (cons a η)) := by
  induction p with
  | var n =>
      cases n with
      | zero => simpa [abstract, freeZero, eval, cons] using Conv.i a
      | succ n => simpa [abstract, freeZero, drop, pren, psub, eval, cons]
          using Conv.k (η n) a
  | atom t => simpa [abstract, freeZero, drop, pren, psub, eval] using Conv.k t a
  | app f x hf hx =>
      by_cases h : freeZero (.app f x) = true
      · simp only [abstract, h, Bool.true_eq, ↓reduceIte, eval]
        exact (Conv.s _ _ a).trans (.app hf hx)
      · have h' : freeZero (.app f x) = false := by
          cases he : freeZero (.app f x) <;> simp_all
        rw [eval_absent (.app f x) h' η a]
        simp only [abstract, h', Bool.false_eq_true, ↓reduceIte, eval]
        exact .k _ a

def pairPoly (x y : P) : P :=
  .app (.app (.atom .s) (.app (.app (.atom .s) (.atom .i)) (.app (.atom .k) x)))
    (.app (.atom .k) y)
def fstPoly (z : P) := P.app z (.atom .k)
def sndPoly (z : P) := P.app z (.app (.atom .k) (.atom .i))
def pair (a b : T) : T := .s ⬝ (.s ⬝ .i ⬝ (.k ⬝ a)) ⬝ (.k ⬝ b)
def fst (z : T) : T := z ⬝ .k
def snd (z : T) : T := z ⬝ (.k ⬝ .i)

theorem pair_congr {a a' b b' : T} (ha : Conv a a') (hb : Conv b b') :
    Conv (pair a b) (pair a' b') :=
  .app (.app (.refl _) (.app (.refl _) (.app (.refl _) ha))) (.app (.refl _) hb)
theorem fst_congr {a b : T} (h : Conv a b) : Conv (fst a) (fst b) :=
  .app h (.refl _)
theorem snd_congr {a b : T} (h : Conv a b) : Conv (snd a) (snd b) :=
  .app h (.refl _)

theorem pair_application (a b c : T) : Conv (pair a b ⬝ c) (c ⬝ a ⬝ b) := by
  exact (Conv.s (.s ⬝ .i ⬝ (.k ⬝ a)) (.k ⬝ b) c).trans
    ((Conv.app (.s .i (.k ⬝ a) c) (.k b c)).trans
      (.app (.app (.i c) (.k a c)) (.refl b)))
theorem fst_pair (a b : T) : Conv (fst (pair a b)) a :=
  (pair_application a b .k).trans (.k a b)
theorem snd_pair (a b : T) : Conv (snd (pair a b)) b :=
  (pair_application a b (.k ⬝ .i)).trans
    ((Conv.app (.k .i a) (.refl b)).trans (.i b))

def iterationPoly : Nat → P
  | 0 => .var 0
  | n+1 => .app (.var 1) (iterationPoly n)
def inputNumeral (n : Nat) := abstract (abstract (iterationPoly n))
def succBody : P := .app (.var 1) (.app (.app (.var 2) (.var 1)) (.var 0))
def succPoly := abstract (abstract (abstract succBody))
def diagonalStepBody : P := pairPoly (.app succPoly (fstPoly (.var 0)))
  (.app succPoly (sndPoly (.var 0)))
def diagonalStep := abstract diagonalStepBody
def diagonalZero := pairPoly (inputNumeral 0) (inputNumeral 0)
def literalPairStateBody := sndPoly (.app (.app (.var 0) diagonalStep) diagonalZero)
def qPoly := abstract literalPairStateBody
def zeroEnv : Nat → T := fun _ => .i
def zeroTerm := eval (inputNumeral 0) zeroEnv
def succTerm := eval succPoly zeroEnv
def delta := eval diagonalStep zeroEnv
def z0 := pair zeroTerm zeroTerm
def q := eval qPoly zeroEnv

theorem zero_application (f a : T) : Conv (zeroTerm ⬝ f ⬝ a) a := by
  exact (Conv.app (abstraction_beta (abstract (iterationPoly 0)) zeroEnv f) (.refl a)).trans
    (abstraction_beta (iterationPoly 0) (cons f zeroEnv) a)

theorem succ_application (n f a : T) :
    Conv (succTerm ⬝ n ⬝ f ⬝ a) (f ⬝ (n ⬝ f ⬝ a)) := by
  have h₁ := Conv.app (Conv.app
    (abstraction_beta (abstract (abstract succBody)) zeroEnv n) (.refl f)) (.refl a)
  have h₂ := Conv.app (abstraction_beta (abstract succBody) (cons n zeroEnv) f) (.refl a)
  have h₃ := abstraction_beta succBody (cons f (cons n zeroEnv)) a
  exact h₁.trans (h₂.trans h₃)

theorem delta_application (z : T) :
    Conv (delta ⬝ z) (pair (succTerm ⬝ fst z) (succTerm ⬝ snd z)) := by
  simpa [delta, diagonalStep, diagonalStepBody, pairPoly, fstPoly, sndPoly, eval, pair, fst, snd,
    succTerm, succPoly, succBody, abstract, freeZero, drop, pren, psub, cons] using
    abstraction_beta diagonalStepBody zeroEnv z

theorem delta_pair (a b : T) :
    Conv (delta ⬝ pair a b) (pair (succTerm ⬝ a) (succTerm ⬝ b)) :=
  (delta_application _).trans (pair_congr
    (.app (.refl succTerm) (fst_pair a b))
    (.app (.refl succTerm) (snd_pair a b)))

theorem q_application (n : T) : Conv (q ⬝ n) (snd (n ⬝ delta ⬝ z0)) := by
  simpa [q, qPoly, literalPairStateBody, sndPoly, eval, snd, delta, diagonalStep,
    diagonalStepBody, diagonalZero, z0, zeroTerm, inputNumeral, iterationPoly,
    pair, pairPoly, fstPoly, succPoly, succBody, abstract, freeZero, drop, pren, psub, cons] using
    abstraction_beta literalPairStateBody zeroEnv n

def successorNumeral (k : Nat) := iter succTerm zeroTerm k

theorem successorNumeral_application (k : Nat) (f a : T) :
    Conv (successorNumeral k ⬝ f ⬝ a) (iter f a k) := by
  induction k with
  | zero => exact zero_application f a
  | succ k ih =>
      exact (succ_application (successorNumeral k) f a).trans (.app (.refl f) ih)

theorem state_iteration (k : Nat) :
    Conv (iter delta z0 k) (pair (successorNumeral k) (successorNumeral k)) := by
  induction k with
  | zero => exact .refl _
  | succ k ih => exact (Conv.app (.refl delta) ih).trans (delta_pair _ _)

theorem q_uniform_iteration (n : T) {k : Nat}
    (hn : ∀ f a, Conv (n ⬝ f ⬝ a) (iter f a k)) :
    Conv (q ⬝ n) (successorNumeral k) :=
  (q_application n).trans ((snd_congr ((hn delta z0).trans (state_iteration k))).trans
    (snd_pair _ _))

/-- New, kernel-checked scalar fusion for the explicit open-term FULL-PER test.
    q is the faithful compiler FORMULA MIRROR, not an imported HasE term. -/
theorem church_scalar_fusion (n : T) (hn : Church n) (f a : T) :
    Conv (n ⬝ f ⬝ a) (q ⬝ n ⬝ f ⬝ a) := by
  obtain ⟨k, hk⟩ := church_standard n hn
  have hq := Conv.app (Conv.app (q_uniform_iteration n hk) (.refl f)) (.refl a)
  exact (hk f a).trans ((hq.trans (successorNumeral_application k f a)).symm)

#print axioms abstraction_beta
#print axioms q_application
#print axioms church_scalar_fusion
end OpenTermStandardness
