/- Current-Has observer and canonical-input templates. No calculus extension is used. -/
import EffectiveStandardness
import AllNucleusSyntax
namespace P01AC.EffectiveCompleteness
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC

def C : Ty := arr N .raw
def rawStep (g : Term) : Poly := abstract (.app (.atom g) (.var 0))
def testerBody (g o c : Term) : Poly :=
  .app (.atom o) (.app (.app (.var 0) (rawStep g)) (.atom c))
def tester (g o c : Term) : Poly := abstract (testerBody g o c)
def constantRaw (c : Term) : Poly := abstract (.atom c)

theorem N_form {Γ : Tel} (hΓ : Ctx Γ) : Form Γ N := by
  apply Form.all hΓ
  exact form_arr (form_arr (.param (ctx_twk hΓ)) (.param (ctx_twk hΓ)))
    (form_arr (.param (ctx_twk hΓ)) (.param (ctx_twk hΓ)))

theorem C_form {Γ : Tel} (hΓ : Ctx Γ) : Form Γ C :=
  form_arr (N_form hΓ) (.raw hΓ)

theorem rawStep_scoped (g : Term) (n : Nat) : Scoped n (rawStep g) :=
  scoped_abstract ⟨trivial, Nat.zero_lt_succ n⟩

theorem rawStep_has {Γ : Tel} (hΓ : Ctx Γ) (g : Term) :
    Has Γ (rawStep g) (arr .raw .raw) := by
  have hΓ' := Ctx.ext hΓ (Form.raw hΓ)
  exact .piIntro (form_arr (.raw hΓ) (.raw hΓ))
    (.rawApp (.raw hΓ') (.rawAtom (.raw hΓ'))
      (.var (.raw hΓ') (.zero))) (rawStep_scoped g Γ.length)

theorem app_has {Γ : Tel} {A B : Ty} {p q : Poly}
    (hf : Form Γ (arr A B)) (hb : Form Γ B)
    (hp : Has Γ p (arr A B)) (hq : Has Γ q A) : Has Γ (.app p q) B := by
  have h := Has.piElim hf (show Form Γ (inst (wk B) q) by simpa using hb) hp hq
  simpa only [inst_wk] using h

theorem tester_has (g o c : Term) : Has [] (tester g o c) C := by
  have hΓ : Ctx [N] := .ext .nil (N_form .nil)
  have hn : Has [N] (.var 0) N :=
    .var (N_form hΓ) (by simpa only [N, NBody, arr, wk, subst] using (Lookup.zero (A := N) (Γ := [])))
  have hr : Form [N] .raw := .raw hΓ
  have hrr := form_arr hr hr
  have hinst : tinst NBody .raw = arr (arr .raw .raw) (arr .raw .raw) := rfl
  have ht : Has [N] (.var 0) (arr (arr .raw .raw) (arr .raw .raw)) := by
    rw [← hinst]
    exact .allElim (N_form hΓ) hr (by rw [hinst]; exact form_arr hrr hrr) hn
  have hi := app_has (form_arr hrr hrr) hrr ht (rawStep_has hΓ g)
  have hc := app_has hrr hr hi (Has.rawAtom hr (t := c))
  have hb : Has [N] (testerBody g o c) .raw := .rawApp hr (.rawAtom hr) hc
  exact .piIntro (C_form .nil) hb
    (scoped_abstract ⟨trivial, ⟨⟨Nat.zero_lt_succ 0, rawStep_scoped g 1⟩, trivial⟩⟩)

theorem constantRaw_has (c : Term) : Has [] (constantRaw c) C := by
  exact .piIntro (C_form .nil) (.rawAtom (.raw (.ext .nil (N_form .nil))))
    (scoped_abstract trivial)

end P01AC.EffectiveCompleteness


namespace P01AC.EffectiveCompleteness
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC

def iterationPoly : Nat → Poly
  | 0 => .var 0
  | n+1 => .app (.var 1) (iterationPoly n)
def inputNumeral (n : Nat) : Poly := abstract (abstract (iterationPoly n))

theorem iteration_scoped (n : Nat) : Scoped 2 (iterationPoly n) := by
  induction n with
  | zero => exact Nat.zero_lt_succ 1
  | succ n ih => exact ⟨Nat.lt_succ_self 1, ih⟩

theorem inputNumeral_has (n : Nat) : Has [] (inputNumeral n) N := by
  let A : Ty := .param 0
  have hf : Form [] (arr A A) := form_arr (.param .nil) (.param .nil)
  have hΓ : Ctx [arr A A] := .ext .nil hf
  have hΔ : Ctx [A,arr A A] := .ext hΓ (.param hΓ)
  have hb : ∀ k, Has [A,arr A A] (iterationPoly k) A := by
    intro k
    induction k with
    | zero => exact .var (.param hΔ) .zero
    | succ k ih =>
      exact app_has (form_arr (.param hΔ) (.param hΔ)) (.param hΔ)
        (.var (form_arr (.param hΔ) (.param hΔ)) (.succ .zero)) ih
  have hi : Has [arr A A] (abstract (iterationPoly n)) (arr A A) :=
    .piIntro (form_arr (.param hΓ) (.param hΓ)) (hb n)
      (scoped_abstract (iteration_scoped n))
  have ho : Has [] (inputNumeral n) NBody :=
    .piIntro (form_arr hf hf) hi (scoped_abstract (scoped_abstract (iteration_scoped n)))
  exact .allIntro (N_form .nil) ho

theorem eval_iteration (n : Nat) (f x : Term) (η : Env) :
    eval (iterationPoly n) (P01F.cons x (P01F.cons f η)) = iterateTerm f n x := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [iterationPoly, eval, P01F.cons, iterateTerm, ih]

theorem inputNumeral_applied (n : Nat) (f x : Term) (η : Env) :
    Conv (.app (.app (eval (inputNumeral n) η) f) x) (iterateTerm f n x) := by
  have h1 := Conv.left (P01Source.red_conv (abstraction_beta (abstract (iterationPoly n)) η f)) x
  have h2 := P01Source.red_conv (abstraction_beta (iterationPoly n) (P01F.cons f η) x)
  exact h1.trans ((eval_iteration n f x η) ▸ h2)

def stepTerm (g : Term) : Term := eval (rawStep g) zeroEnv

theorem rawStep_application (g x : Term) : Conv (.app (stepTerm g) x) (.app g x) :=
  P01Source.red_conv (abstraction_beta (.app (.atom g) (.var 0)) zeroEnv x)

theorem eval_rawStep (g : Term) (η : Env) : eval (rawStep g) η = stepTerm g := by
  simp [rawStep, stepTerm, abstract, freeZero, eval, drop, pren, psub]

theorem tester_application (g o c t : Term) :
    Conv (.app (eval (tester g o c) zeroEnv) t)
      (.app o (.app (.app t (stepTerm g)) c)) := by
  have h := P01Source.red_conv (abstraction_beta (testerBody g o c) zeroEnv t)
  simpa only [testerBody, eval, P01F.cons, eval_rawStep] using h

theorem constantRaw_application (c t : Term) :
    Conv (.app (eval (constantRaw c) zeroEnv) t) c :=
  P01Source.red_conv (abstraction_beta (.atom c) zeroEnv t)

end P01AC.EffectiveCompleteness
