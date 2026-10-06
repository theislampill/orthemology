/- Finite-arity primitive recursion compiled directly into unchanged P01AC Has. -/
import EffectiveBooleanCertificates
namespace P01AC.BooleanPrimitive
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC.EffectiveCompleteness P01AC.IdentityComplexity P01AC.BooleanIdentity
open P01F (cons)

def NatObs (t : Term) (n : Nat) : Prop :=
  ∀ f x, Conv (.app (.app t f) x) (iterateTerm f n x)

theorem NatObs.of_conv {left t : Term} {n : Nat} (h : Conv left t) (ht : NatObs t n) : NatObs left n :=
  fun f x => ((h.left f).left x).trans (ht f x)

theorem canonical_obs (n : Nat) : NatObs (canonical n) n :=
  fun f x => inputNumeral_applied n f x zeroEnv

theorem eval_closed {p : Poly} (hp : Scoped 0 p) (η ξ : Env) : eval p η = eval p ξ := by
  induction p with
  | var n => exact False.elim (Nat.not_lt_zero n hp)
  | atom a => rfl
  | app f a ihf iha => exact congrArg₂ Term.app (ihf hp.1) (iha hp.2)

theorem psub_closed {p : Poly} (hp : Scoped 0 p) (σ : Nat → Poly) : psub σ p = p := by
  have e := psub_scoped_congr (σ := σ) (δ := Poly.var) hp (fun n hn => False.elim (Nat.not_lt_zero n hn))
  exact e.trans (psub_id p)

theorem closed_has {p : Poly} {A : Ty} (hp : Has [] p A)
    (hA : ∀ σ, subst σ A = A) {Γ : Tel} (hΓ : Ctx Γ) : Has Γ p A := by
  have hs : MixedSubstitution [] Γ Poly.var Ty.param :=
    ⟨fun _ => .param hΓ, fun h => nomatch h⟩
  have h := has_mixed hp hΓ hs
  simpa only [mixed_param, hA, psub_id] using h

theorem N_subst (σ : Nat → Poly) : subst σ N = N := rfl
theorem B_subst (σ : Nat → Poly) : subst σ B = B := rfl

def S : Ty := .sigma N N

theorem S_form {Γ : Tel} (hΓ : Ctx Γ) : Form Γ S :=
  .sigma (N_form hΓ) (N_form (.ext hΓ (N_form hΓ)))

def succBody : Poly := .app (.var 1) (.app (.app (.var 2) (.var 1)) (.var 0))
def succPoly : Poly := abstract (abstract (abstract succBody))

theorem succ_has : Has [] succPoly (arr N N) := by
  let X : Ty := .param 0
  let FX : Ty := arr X X
  have c0 : Ctx [N] := .ext .nil (N_form .nil)
  have c1 : Ctx [FX,N] := .ext c0 (form_arr (.param c0) (.param c0))
  have c2 : Ctx [X,FX,N] := .ext c1 (.param c1)
  have nx : Has [X,FX,N] (.var 2) N := .var (N_form c2) (.succ (.succ .zero))
  have nf : Has [X,FX,N] (.var 2) (arr FX FX) := by
    exact .allElim (N_form c2) (.param c2)
      (form_arr (form_arr (.param c2) (.param c2)) (form_arr (.param c2) (.param c2))) nx
  have fx : Has [X,FX,N] (.var 1) FX :=
    .var (form_arr (.param c2) (.param c2)) (.succ .zero)
  have xx : Has [X,FX,N] (.var 0) X := .var (.param c2) .zero
  have b : Has [X,FX,N] succBody X :=
    app_has (form_arr (.param c2) (.param c2)) (.param c2) fx
      (app_has (form_arr (.param c2) (.param c2)) (.param c2)
        (app_has (form_arr (form_arr (.param c2) (.param c2))
          (form_arr (.param c2) (.param c2))) (form_arr (.param c2) (.param c2)) nf fx) xx)
  have bx : Has [FX,N] (abstract succBody) FX :=
    .piIntro (form_arr (.param c1) (.param c1)) b (scoped_abstract (has_scoped b))
  have bf : Has [N] (abstract (abstract succBody)) NBody :=
    .piIntro (form_arr (form_arr (.param c0) (.param c0))
      (form_arr (.param c0) (.param c0))) bx (scoped_abstract (has_scoped bx))
  have bn : Has [N] (abstract (abstract succBody)) N := .allIntro (N_form c0) bf
  exact .piIntro (form_arr (N_form .nil) (N_form .nil)) bn (scoped_abstract (has_scoped bn))

def succTerm : Term := eval succPoly zeroEnv

theorem succ_application (n f x : Term) :
    Conv (.app (.app (.app succTerm n) f) x) (.app f (.app (.app n f) x)) := by
  have h1 := ((P01Source.red_conv (abstraction_beta (abstract (abstract succBody)) zeroEnv n)).left f).left x
  have h2 := (P01Source.red_conv (abstraction_beta (abstract succBody) (cons n zeroEnv) f)).left x
  have h3 := P01Source.red_conv (abstraction_beta succBody (cons f (cons n zeroEnv)) x)
  exact h1.trans (h2.trans h3)

theorem succ_obs {t : Term} {n : Nat} (h : NatObs t n) : NatObs (.app succTerm t) (n+1) := by
  intro f x
  exact (succ_application t f x).trans (Conv.right f (h f x))


def NatCtx (r : Nat) : Tel := List.replicate r N

theorem natctx_formed (r : Nat) : Ctx (NatCtx r) := by
  induction r with
  | zero => exact .nil
  | succ r ih => exact .ext ih (N_form ih)

theorem nat_lookup_eq {r i A} (h : Lookup (NatCtx r) i A) : A = N := by
  induction r generalizing i A with
  | zero => cases h
  | succ r ih =>
    cases h with
    | zero => rfl
    | succ h => exact congrArg wk (ih h)

theorem natvar {r i} (h : i < r) : Has (NatCtx r) (.var i) N := by
  have hi : i < (NatCtx r).length := by simpa [NatCtx] using h
  obtain ⟨A, ha⟩ := lookup_exists (NatCtx r) hi
  have e := nat_lookup_eq ha
  cases e
  exact .var (N_form (natctx_formed r)) ha

def recImages (i : Nat) : Poly :=
  match i with
  | 0 => fstPoly (.var 0)
  | 1 => sndPoly (.var 0)
  | j+2 => .var (j+2)
def recStepBody (h : Poly) : Poly :=
  pairPoly (.app succPoly (fstPoly (.var 0))) (psub recImages h)
def recStep (h : Poly) : Poly := abstract (recStepBody h)
def recPoly (g h : Poly) : Poly :=
  sndPoly (.app (.app (.var 0) (recStep h))
    (pairPoly (inputNumeral 0) (pren Nat.succ g)))

theorem recStep_has {r : Nat} {h : Poly} (hh : Has (NatCtx (r+2)) h N) :
    Has (NatCtx (r+1)) (recStep h) (arr S S) := by
  have cg := natctx_formed (r+1)
  let Δ : Tel := S :: NatCtx (r+1)
  have cd : Ctx Δ := .ext cg (S_form cg)
  have vz : Has Δ (.var 0) S := .var (S_form cd) .zero
  have vf : Has Δ (fstPoly (.var 0)) N := .sigmaFst (N_form cd) (S_form cd) vz
  have vs : Has Δ (sndPoly (.var 0)) N := .sigmaSnd (S_form cd) (N_form cd) vz
  have hm : MixedSubstitution (NatCtx (r+2)) Δ recImages Ty.param := by
    refine ⟨fun _ => .param cd, ?_⟩
    intro i A hi
    have e := nat_lookup_eq hi
    cases e
    change Has Δ (recImages i) N
    cases i with
    | zero => exact vf
    | succ i =>
      cases i with
      | zero => exact vs
      | succ i =>
        have il : i+1 < r+1 := by
          have hl := lookup_lt hi
          simp only [NatCtx, List.length_replicate] at hl
          omega
        have ht := has_wk (natvar il) cg (S_form cg)
        exact ht
  have hout : Has Δ (psub recImages h) N := by
    simpa only [mixed_param, N_subst] using has_mixed hh cd hm
  have hs : Has Δ succPoly (arr N N) :=
    closed_has succ_has (fun _ => rfl) cd
  have hf : Has Δ (.app succPoly (fstPoly (.var 0))) N :=
    app_has (form_arr (N_form cd) (N_form cd)) (N_form cd) hs vf
  have body : Has Δ (recStepBody h) S :=
    .sigmaIntro (S_form cd) (N_form cd) hf hout
  exact .piIntro (form_arr (S_form cg) (S_form cg)) body
    (scoped_abstract (has_scoped body))

theorem recPoly_has {r : Nat} {g h : Poly}
    (hg : Has (NatCtx r) g N) (hh : Has (NatCtx (r+2)) h N) :
    Has (NatCtx (r+1)) (recPoly g h) N := by
  have cg := natctx_formed (r+1)
  have hs := S_form cg
  have hss := form_arr hs hs
  have hn := natvar (show 0 < r+1 from Nat.zero_lt_succ r)
  have hni : Has (NatCtx (r+1)) (.var 0) (arr (arr S S) (arr S S)) :=
    .allElim (N_form cg) hs (form_arr hss hss) hn
  have hb0 : Has (NatCtx (r+1)) (inputNumeral 0) N :=
    closed_has (inputNumeral_has 0) N_subst cg
  have hbg : Has (NatCtx (r+1)) (pren Nat.succ g) N :=
    has_wk hg (natctx_formed r) (N_form (natctx_formed r))
  have hb : Has (NatCtx (r+1)) (pairPoly (inputNumeral 0) (pren Nat.succ g)) S :=
    .sigmaIntro hs (N_form cg) hb0 hbg
  have hi := app_has hss hs (app_has (form_arr hss hss) hss hni (recStep_has hh)) hb
  exact .sigmaSnd hs (N_form cg) hi

/-- Ordinary finite-arity primitive recursion syntax, compiled into the original
    polynomial language. It is not an alternative object-language typing calculus. -/
inductive PR : Nat → Type where
  | zero (r : Nat) : PR r
  | succ : PR 1
  | proj {r : Nat} : Fin r → PR r
  | comp {r k : Nat} : PR k → (Fin k → PR r) → PR r
  | prec {r : Nat} : PR r → PR (r+2) → PR (r+1)

def PR.denote : {r : Nat} → PR r → (Nat → Nat) → Nat
  | _, .zero _, _ => 0
  | _, .succ, v => v 0 + 1
  | _, .proj i, v => v i.val
  | _, @PR.comp r k f gs, v =>
      f.denote (fun i => if hi : i < k then (gs ⟨i,hi⟩).denote v else 0)
  | _, .prec g h, v =>
      Nat.rec (g.denote (fun i => v (i+1)))
        (fun k a => h.denote (cons k (cons a (fun i => v (i+1))))) (v 0)

def PR.compile : {r : Nat} → PR r → Poly
  | _, .zero _ => inputNumeral 0
  | _, .succ => .app succPoly (.var 0)
  | _, .proj i => .var i.val
  | _, @PR.comp r k f gs =>
      psub (fun i => if hi : i < k then (gs ⟨i,hi⟩).compile else .atom .zero) f.compile
  | _, .prec g h => recPoly g.compile h.compile

theorem PR.compile_has {r : Nat} (f : PR r) : Has (NatCtx r) f.compile N := by
  induction f with
  | zero r => exact closed_has (inputNumeral_has 0) N_subst (natctx_formed r)
  | succ =>
    have cg := natctx_formed 1
    exact app_has (form_arr (N_form cg) (N_form cg)) (N_form cg)
      (closed_has succ_has (fun _ => rfl) cg) (natvar (Nat.zero_lt_succ 0))
  | proj i => exact natvar i.isLt
  | @comp r k f gs ihf ihgs =>
    have cg := natctx_formed r
    let σ : Nat → Poly := fun i => if hi : i < k then (gs ⟨i,hi⟩).compile else .atom .zero
    have hm : MixedSubstitution (NatCtx k) (NatCtx r) σ Ty.param := by
      refine ⟨fun _ => .param cg, ?_⟩
      intro i A hi
      have e := nat_lookup_eq hi
      cases e
      have il : i < k := by simpa only [NatCtx, List.length_replicate] using lookup_lt hi
      simpa only [σ, dif_pos il, mixed_param, N_subst] using ihgs ⟨i,il⟩
    simpa only [PR.compile, mixed_param, N_subst] using has_mixed ihf cg hm
  | prec g h ihg ihh => exact recPoly_has ihg ihh

/-- The parameter vector starts after the recursion argument n. The step state
    z has its counter in fst and current value in snd, with no swapped indices. -/
theorem recStep_application (h : Poly) (η : Env) (z : Term) :
    Conv (.app (eval (recStep h) η) z)
      (pairTerm (.app succTerm (firstTerm z))
        (eval h (cons (firstTerm z) (cons (secondTerm z) (fun i => η (i+1)))))) := by
  have hb := P01Source.red_conv (abstraction_beta (recStepBody h) η z)
  have he : (fun i => eval (recImages i) (cons z η)) =
      cons (firstTerm z) (cons (secondTerm z) (fun i => η (i+1))) := by
    funext i
    cases i with
    | zero => rfl
    | succ i => cases i <;> rfl
  simpa only [recStepBody, eval_pair, eval, eval_fst, eval_sub,
    eval_closed (has_scoped succ_has) (cons z η) zeroEnv, he] using hb

def EnvNat (r : Nat) (η : Env) (v : Nat → Nat) : Prop :=
  ∀ i, i < r → NatObs (η i) (v i)

theorem recPoly_obs {r : Nat} (g h : Poly) (gv : (Nat → Nat) → Nat)
    (hv : (Nat → Nat) → Nat)
    (hg : ∀ η v, EnvNat r η v → NatObs (eval g η) (gv v))
    (hh : ∀ η v, EnvNat (r+2) η v → NatObs (eval h η) (hv v))
    (η : Env) (v : Nat → Nat) (henv : EnvNat (r+1) η v) :
    NatObs (eval (recPoly g h) η)
      (Nat.rec (gv (fun i => v (i+1)))
        (fun k a => hv (cons k (cons a (fun i => v (i+1))))) (v 0)) := by
  let ηp : Env := fun i => η (i+1)
  let vp : Nat → Nat := fun i => v (i+1)
  let value : Nat → Nat := Nat.rec (gv vp) (fun k a => hv (cons k (cons a vp)))
  let d : Term := eval (recStep h) η
  let z0 : Term := pairTerm (canonical 0) (eval g ηp)
  have hp : EnvNat r ηp vp := fun i hi => henv (i+1) (Nat.succ_lt_succ hi)
  have inv : ∀ k, NatObs (firstTerm (iterateTerm d k z0)) k ∧
      NatObs (secondTerm (iterateTerm d k z0)) (value k) := by
    intro k
    induction k with
    | zero =>
      exact ⟨NatObs.of_conv (pair_first _ _) (canonical_obs 0),
        NatObs.of_conv (pair_second _ _) (hg ηp vp hp)⟩
    | succ k ih =>
      let z := iterateTerm d k z0
      have step := recStep_application h η z
      have hf : Conv (firstTerm (.app d z)) (.app succTerm (firstTerm z)) :=
        (step.left .k).trans (pair_first _ _)
      have hs : Conv (secondTerm (.app d z))
          (eval h (cons (firstTerm z) (cons (secondTerm z) ηp))) :=
        (step.left (.app .k .i)).trans (pair_second _ _)
      have eh : EnvNat (r+2) (cons (firstTerm z) (cons (secondTerm z) ηp))
          (cons k (cons (value k) vp)) := by
        intro i hi
        cases i with
        | zero => exact ih.1
        | succ i =>
          cases i with
          | zero => exact ih.2
          | succ i => exact hp i (by omega)
      exact ⟨NatObs.of_conv hf (succ_obs ih.1), NatObs.of_conv hs (hh _ _ eh)⟩
  have hn := henv 0 (Nat.zero_lt_succ r) d z0
  have he : eval (recPoly g h) η = secondTerm (.app (.app (η 0) d) z0) := by
    simp only [recPoly, eval_snd, eval, eval_pair, eval_ren, z0, d, ηp,
      eval_closed (has_scoped (inputNumeral_has 0)) η zeroEnv, canonical]
  rw [he]
  exact NatObs.of_conv (hn.left (.app .k .i)) (inv (v 0)).2

/-- Computational adequacy for ALL raw numeral observations, not only closed
    canonical syntax or a MarkerFree subset. -/
theorem PR.compile_obs {r : Nat} (f : PR r) (η : Env) (v : Nat → Nat)
    (hη : EnvNat r η v) : NatObs (eval f.compile η) (f.denote v) := by
  induction f generalizing η v with
  | zero r =>
    rw [PR.compile, eval_closed (has_scoped (inputNumeral_has 0)) η zeroEnv]
    exact canonical_obs 0
  | succ =>
    have e : eval succPoly η = succTerm := eval_closed (has_scoped succ_has) η zeroEnv
    change NatObs (.app (eval succPoly η) (η 0)) (v 0 + 1)
    rw [e]
    exact succ_obs (hη 0 (Nat.zero_lt_succ 0))
  | proj i => exact hη i.val i.isLt
  | @comp r k f gs ihf ihgs =>
    simp only [PR.compile, eval_sub, PR.denote]
    apply ihf
    intro i hi
    simp only [dif_pos hi]
    exact ihgs ⟨i,hi⟩ η v hη
  | prec g h ihg ihh =>
    exact recPoly_obs g.compile h.compile g.denote h.denote ihg ihh η v hη

def choicePoly (b : Bool) : Poly := abstract (abstract (.var (if b then 0 else 1)))
def choiceTerm (b : Bool) : Term := eval (choicePoly b) zeroEnv

theorem choice_has (b : Bool) : Has [] (choicePoly b) B := by
  let X : Ty := .param 0
  have c1 : Ctx [X] := .ext .nil (.param .nil)
  have c2 : Ctx [X,X] := .ext c1 (.param c1)
  have v : Has [X,X] (.var (if b then 0 else 1)) X := by
    cases b
    · exact .var (.param c2) (.succ .zero)
    · exact .var (.param c2) .zero
  have h1 : Has [X] (abstract (.var (if b then 0 else 1))) (arr X X) :=
    .piIntro (form_arr (.param c1) (.param c1)) v (scoped_abstract (has_scoped v))
  have h2 : Has [] (choicePoly b) (arr X (arr X X)) :=
    .piIntro (form_arr (.param .nil) (form_arr (.param .nil) (.param .nil))) h1
      (scoped_abstract (has_scoped h1))
  exact .allIntro (B_form .nil) h2

theorem choice_application (b : Bool) (x y : Term) :
    Conv (.app (.app (choiceTerm b) x) y) (pick b x y) := by
  have h1 := (P01Source.red_conv (abstraction_beta (abstract (.var (if b then 0 else 1))) zeroEnv x)).left y
  have h2 := P01Source.red_conv (abstraction_beta (.var (if b then 0 else 1)) (cons x zeroEnv) y)
  have h := h1.trans h2
  cases b <;> exact h

def discriminatorStep : Poly := .app (.atom .k) (choicePoly true)
def discriminatorBody : Poly := .app (.app (.var 0) discriminatorStep) (choicePoly false)
/-- First choice for index zero, second choice for every positive index. -/
def zeroDiscriminator : Poly := abstract discriminatorBody
def discriminatorTerm : Term := eval zeroDiscriminator zeroEnv

theorem discriminator_has : Has [] zeroDiscriminator (arr N B) := by
  have cg : Ctx [N] := .ext .nil (N_form .nil)
  have hb := B_form cg
  have hbb := form_arr hb hb
  have k : Has [N] (.atom .k) (arr B (arr B B)) := .k hb hb (form_arr hb hbb)
  have step : Has [N] discriminatorStep (arr B B) :=
    app_has (form_arr hb hbb) hbb k (closed_has (choice_has true) B_subst cg)
  have hn : Has [N] (.var 0) (arr (arr B B) (arr B B)) :=
    .allElim (N_form cg) hb (form_arr hbb hbb) (.var (N_form cg) .zero)
  have body : Has [N] discriminatorBody B :=
    app_has hbb hb (app_has (form_arr hbb hbb) hbb hn step)
      (closed_has (choice_has false) B_subst cg)
  exact .piIntro (form_arr (N_form .nil) (B_form .nil)) body (scoped_abstract (has_scoped body))

theorem discriminator_application (t : Term) :
    Conv (.app discriminatorTerm t)
      (.app (.app t (.app .k (choiceTerm true))) (choiceTerm false)) := by
  have h := P01Source.red_conv (abstraction_beta discriminatorBody zeroEnv t)
  simpa only [discriminatorBody, discriminatorStep, eval,
    eval_closed (has_scoped (choice_has true)) (cons t zeroEnv) zeroEnv,
    eval_closed (has_scoped (choice_has false)) (cons t zeroEnv) zeroEnv] using h

theorem discriminator_obs {t : Term} {n : Nat} (ht : NatObs t n) (x y : Term) :
    Conv (.app (.app (.app discriminatorTerm t) x) y) (pick (decide (n ≠ 0)) x y) := by
  have h := (discriminator_application t).trans (ht (.app .k (choiceTerm true)) (choiceTerm false))
  have hi : Conv (iterateTerm (.app .k (choiceTerm true)) n (choiceTerm false))
      (choiceTerm (decide (n ≠ 0))) := by
    cases n with
    | zero => exact .refl _
    | succ n => exact .step (.k _ _)
  exact (((h.trans hi).left x).left y).trans (choice_application _ x y)

/-- For f of arity two, x₀ is the bound and x₁ the program code. The outer
    abstraction binds the program code; the inner abstraction binds the bound. -/
def simulator (f : PR 2) : Poly := abstract (abstract (.app zeroDiscriminator f.compile))
def simFamily (f : PR 2) (e : Nat) : Poly := .app (simulator f) (inputNumeral e)
def constantChoice : Poly := abstract (choicePoly false)
def inputs (n e : Nat) : Nat → Nat := cons n (cons e (fun _ => 0))

theorem simulator_has (f : PR 2) : Has [] (simulator f) (arr N (arr N B)) := by
  have c2 := natctx_formed 2
  have body : Has (NatCtx 2) (.app zeroDiscriminator f.compile) B :=
    app_has (form_arr (N_form c2) (B_form c2)) (B_form c2)
      (closed_has discriminator_has (fun _ => rfl) c2) f.compile_has
  have inner : Has (NatCtx 1) (abstract (.app zeroDiscriminator f.compile)) (arr N B) :=
    .piIntro (form_arr (N_form (natctx_formed 1)) (B_form (natctx_formed 1))) body
      (scoped_abstract (has_scoped body))
  exact .piIntro (form_arr (N_form .nil) (form_arr (N_form .nil) (B_form .nil))) inner
    (scoped_abstract (has_scoped inner))

theorem simFamily_has (f : PR 2) (e : Nat) : Has [] (simFamily f e) CB :=
  app_has (form_arr (N_form .nil) (form_arr (N_form .nil) (B_form .nil)))
    (form_arr (N_form .nil) (B_form .nil)) (simulator_has f) (inputNumeral_has e)

theorem constantChoice_has : Has [] constantChoice CB := by
  have body := closed_has (choice_has false) B_subst (natctx_formed 1)
  exact .piIntro (form_arr (N_form .nil) (B_form .nil)) body (scoped_abstract (has_scoped body))

theorem simFamily_obs (f : PR 2) (e n : Nat) :
    Conv (observationAt (simFamily f e) n) (pick (decide (f.denote (inputs n e) ≠ 0)) .zero .one) := by
  let η : Env := cons (canonical n) (cons (canonical e) zeroEnv)
  have h1 := (P01Source.red_conv (abstraction_beta (abstract (.app zeroDiscriminator f.compile)) zeroEnv (canonical e))).left (canonical n)
  have h2 := P01Source.red_conv (abstraction_beta (.app zeroDiscriminator f.compile) (cons (canonical e) zeroEnv) (canonical n))
  have hc : Conv (.app (eval (simFamily f e) zeroEnv) (canonical n)) (.app discriminatorTerm (eval f.compile η)) := by
    have h := h1.trans h2
    change Conv (.app (eval (simFamily f e) zeroEnv) (canonical n))
      (.app (eval zeroDiscriminator η) (eval f.compile η)) at h
    rw [eval_closed (has_scoped discriminator_has) η zeroEnv] at h
    exact h
  have hn : NatObs (eval f.compile η) (f.denote (inputs n e)) := by
    apply f.compile_obs
    intro i hi
    cases i with
    | zero => exact canonical_obs n
    | succ i =>
      cases i with
      | zero => exact canonical_obs e
      | succ i => omega
  exact ((hc.left .zero).left .one).trans (discriminator_obs hn .zero .one)

theorem constantChoice_obs (n : Nat) : Conv (observationAt constantChoice n) .zero := by
  have h := P01Source.red_conv (abstraction_beta (choicePoly false) zeroEnv (canonical n))
  have hc : Conv (.app (eval constantChoice zeroEnv) (canonical n)) (choiceTerm false) := by
    simpa only [eval_closed (has_scoped (choice_has false)) (cons (canonical n) zeroEnv) zeroEnv] using h
  exact ((hc.left .zero).left .one).trans (choice_application false .zero .one)

/-- Every primitive-recursive numeric predicate yields the exact typed Boolean
    universal-zero test, with no representation premise hidden in the theorem. -/
theorem sim_valid_iff_all_zero (f : PR 2) (e : Nat) :
    BoolValid (simFamily f e) constantChoice ↔ ∀ n, f.denote (inputs n e) = 0 := by
  constructor
  · intro hv n
    have ht := (bool_valid_iff_tests (simFamily_has f e) constantChoice_has).mp hv n
    have hc : Conv (pick (decide (f.denote (inputs n e) ≠ 0)) .zero .one) (pick false .zero .one) :=
      (simFamily_obs f e n).symm.trans (ht.trans (constantChoice_obs n))
    have he := pick_conv_injective hc
    apply Classical.byContradiction
    intro hn
    exact (of_decide_eq_false he) hn
  · intro hz
    apply (bool_valid_iff_tests (simFamily_has f e) constantChoice_has).mpr
    intro n
    have h := simFamily_obs f e n
    simp only [hz n, ne_eq, not_true_eq_false, decide_false, pick, Bool.false_eq_true, ↓reduceIte] at h
    exact h.trans (constantChoice_obs n).symm

end P01AC.BooleanPrimitive
