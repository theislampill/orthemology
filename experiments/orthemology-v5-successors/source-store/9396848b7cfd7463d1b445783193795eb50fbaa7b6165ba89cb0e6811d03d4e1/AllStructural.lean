/- Literal syntactic preservation by contextual maps of both independent sorts. -/
import AllStructuralRename
namespace P01AC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

/-- A total-function interface used solely for the finite syntactic induction.
Finite context maps below supply this interface using distinct zero/Bottom padding. -/
structure MixedSubstitution (Γ Δ : Tel) (σ : Nat → Poly) (τ : Nat → Ty) : Prop where
  types : ∀ n, Form Δ (τ n)
  lookup : ∀ {n A}, Lookup Γ n A → Has Δ (σ n) (mixed σ τ A)

theorem MixedSubstitution.scope {Γ Δ : Tel} {σ : Nat → Poly} {τ : Nat → Ty}
    (h : MixedSubstitution Γ Δ σ τ) : ScopedSub Γ.length Δ.length σ := by
  intro n hn
  obtain ⟨A, ha⟩ := lookup_exists Γ hn
  exact has_scoped (h.lookup ha)

theorem MixedSubstitution.lift {Γ Δ : Tel} {σ : Nat → Poly} {τ : Nat → Ty} {A : Ty}
    (h : MixedSubstitution Γ Δ σ τ) (hΔ : Ctx Δ) (hA : Form Δ (mixed σ τ A)) :
    MixedSubstitution (A :: Γ) (mixed σ τ A :: Δ) (pup σ) (fun n => wk (τ n)) := by
  refine ⟨fun n => form_wk (h.types n) hΔ hA, ?_⟩
  intro n B hn
  cases hn with
  | zero =>
      simpa only [mixed_wk, pup] using Has.var (form_wk hA hΔ hA)
        (Lookup.zero (A := mixed σ τ A) (Γ := Δ))
  | succ hn => simpa only [mixed_wk, pup] using has_wk (h.lookup hn) hΔ hA

theorem MixedSubstitution.twk {Γ Δ : Tel} {σ : Nat → Poly} {τ : Nat → Ty}
    (h : MixedSubstitution Γ Δ σ τ) (hΔ : Ctx Δ) :
    MixedSubstitution (twkTel Γ) (twkTel Δ) σ (tup τ) := by
  refine ⟨?_, ?_⟩
  · intro n
    cases n with
    | zero => exact .param (ctx_twk hΔ)
    | succ n => exact form_twk (h.types n)
  · intro n B hb
    obtain ⟨A, ha, rfl⟩ := lookup_trename_inv hb
    change Has (twkTel Δ) (σ n) (mixed σ (tup τ) (P01AC.twk A))
    rw [mixed_twk]
    exact has_twk (h.lookup ha)

theorem mixed_theta_head (A : Ty) (x : Poly) (σ : Nat → Poly) (τ : Nat → Ty) :
    mixed (pup σ) (fun n => wk (τ n)) (.identity (wk A) (pren Nat.succ x) (.var 0)) =
      .identity (wk (mixed σ τ A)) (pren Nat.succ (psub σ x)) (.var 0) := by
  simp only [mixed, mixed_wk, P01DF.Syntactic.polynomial_shift_substitution, psub, pup]

theorem MixedSubstitution.theta {Γ Δ : Tel} {σ : Nat → Poly} {τ : Nat → Ty}
    {A : Ty} {x : Poly} (h : MixedSubstitution Γ Δ σ τ) (hΔ : Ctx Δ)
    (hA : Form Δ (mixed σ τ A)) (hx : Has Δ (psub σ x) (mixed σ τ A)) :
    MixedSubstitution (theta Γ A x) (theta Δ (mixed σ τ A) (psub σ x))
      (pup (pup σ)) (fun n => wk (wk (τ n))) := by
  have hhead : Form (mixed σ τ A :: Δ)
      (mixed (pup σ) (fun n => wk (τ n)) (.identity (wk A) (pren Nat.succ x) (.var 0))) := by
    rw [mixed_theta_head]
    exact form_theta_head hΔ hA hx
  simpa only [theta, mixed_theta_head] using
    (h.lift hΔ hA).lift (.ext hΔ hA) hhead

theorem form_mixed {Γ : Tel} {A : Ty} (h : Form Γ A) :
    ∀ {Δ : Tel} {σ : Nat → Poly} {τ : Nat → Ty}, Ctx Δ → MixedSubstitution Γ Δ σ τ → Form Δ (mixed σ τ A) := by
  induction h using Form.rec
    (motive_1 := fun _ _ => True)
    (motive_3 := fun Γ p A _ => ∀ {Δ : Tel} {σ : Nat → Poly} {τ : Nat → Ty},
      Ctx Δ → MixedSubstitution Γ Δ σ τ → Has Δ (psub (σ) p) (mixed σ τ A)) with
    | nil => trivial
    | ext => trivial
    | param hΓ iΓ =>
        intro Δ σ τ hΔ hσ
        exact hσ.types _
    | bottom hΓ iΓ =>
        intro Δ σ τ hΔ hσ
        exact .bottom hΔ
    | all hΓ hB iΓ iB =>
        intro Δ σ τ hΔ hσ
        exact .all hΔ (iB (ctx_twk hΔ) (hσ.twk hΔ))
    | raw hΓ iΓ =>
        intro Δ σ τ hΔ hσ
        exact .raw hΔ
    | pi hA hB iA iB =>
        intro Δ σ τ hΔ hσ
        have hA' := iA hΔ hσ
        have hB' := iB (.ext hΔ hA') (hσ.lift hΔ hA')
        simpa only [mixed] using Form.pi hA' hB'
    | sigma hA hB iA iB =>
        intro Δ σ τ hΔ hσ
        have hA' := iA hΔ hσ
        have hB' := iB (.ext hΔ hA') (hσ.lift hΔ hA')
        simpa only [mixed] using Form.sigma hA' hB'
    | identity hA hp hq iA ip iq =>
        intro Δ σ τ hΔ hσ
        exact .identity (iA hΔ hσ) (ip hΔ hσ) (iq hΔ hσ)
    | var hA hn iA =>
        rename_i Δ σ τ hΔ hσ
        exact hσ.lookup hn
    | i hA hF iA iF =>
        rename_i Δ σ τ hΔ hσ
        simpa only [psub, mixed_arr] using
          Has.i (iA hΔ hσ)
            (by simpa only [mixed_arr] using iF hΔ hσ)
    | k hA hB hF iA iB iF =>
        rename_i Δ σ τ hΔ hσ
        simpa only [psub, mixed_arr] using
          Has.k (iA hΔ hσ) (iB hΔ hσ)
            (by simpa only [mixed_arr] using iF hΔ hσ)
    | s hA hB hC hF iA iB iC iF =>
        rename_i Δ σ τ hΔ hσ
        simpa only [psub, mixed_arr] using
          Has.s (iA hΔ hσ) (iB hΔ hσ) (iC hΔ hσ)
            (by simpa only [mixed_arr] using iF hΔ hσ)
    | @finite C Γ t υ hlen hυ hF ht iυ iF =>
        rename_i Δ σ τ hΔ hσ
        simpa only [psub, mixed_finite_instance] using
          Has.finite (υ.map (mixed σ τ))
            (by simpa only [List.length_map] using hlen)
            (fun n hn => by simpa only [typeImages_mixed] using iυ n (by simpa only [List.length_map] using hn) hΔ hσ)
            (by simpa only [mixed_finite_instance] using iF hΔ hσ) ht
    | allIntro hF hp iF ip =>
        rename_i Δ σ τ hΔ hσ
        exact .allIntro (iF hΔ hσ) (ip (ctx_twk hΔ) (hσ.twk hΔ))
    | allElim hF hA hI hp iF iA iI ip =>
        rename_i Δ σ τ hΔ hσ
        simpa only [mixed_tinst] using Has.allElim (iF hΔ hσ) (iA hΔ hσ)
          (by simpa only [mixed_tinst] using iI hΔ hσ) (ip hΔ hσ)
    | rawAtom hF iF =>
        rename_i Δ σ τ hΔ hσ
        exact .rawAtom (iF hΔ hσ)
    | rawApp hF hf ha iF iFterm ia =>
        rename_i Δ σ τ hΔ hσ
        exact .rawApp (iF hΔ hσ) (iFterm hΔ hσ) (ia hΔ hσ)
    | @piIntro Γ A B b hF hb hs iF ib =>
        rename_i Δ σ τ hΔ hσ
        have hF' := iF hΔ hσ
        change Form Δ (.pi (mixed σ τ A) (mixed (pup σ) (fun n => wk (τ n)) B)) at hF'
        cases hF' with
        | pi hA' hB' =>
            have hb' := ib (.ext hΔ hA') (hσ.lift hΔ hA')
            have hs' := scoped_subst (σ := σ) (m := Δ.length) hs
              (fun n hn => hσ.scope n hn)
            have ht : Has Δ (abstract (psub (pup (σ)) b))
                (.pi (mixed σ τ A) (mixed (pup σ) (fun n => wk (τ n)) B)) :=
              Has.piIntro (Form.pi hA' hB')
                (by simpa only [] using hb')
                (by simpa only [abstraction_naturality] using hs')
            rw [abstraction_naturality] at ht
            exact ht
    | piElim hF hI hf ha iF iI iFterm ia =>
        rename_i Δ σ τ hΔ hσ
        simpa only [psub, mixed_inst, mixed] using
          Has.piElim (iF hΔ hσ)
            (by simpa only [mixed_inst] using iI hΔ hσ)
            (iFterm hΔ hσ) (ia hΔ hσ)
    | sigmaIntro hF hI ha hb iF iI ia ib =>
        rename_i Δ σ τ hΔ hσ
        simpa only [P01DF.Syntactic.polynomial_pair, mixed] using
          Has.sigmaIntro (iF hΔ hσ)
            (by simpa only [mixed_inst] using iI hΔ hσ)
            (ia hΔ hσ)
            (by simpa only [mixed_inst] using ib hΔ hσ)
    | sigmaFst hA hF hz iA iF iz =>
        rename_i Δ σ τ hΔ hσ
        exact .sigmaFst (iA hΔ hσ) (iF hΔ hσ) (iz hΔ hσ)
    | sigmaSnd hF hI hz iF iI iz =>
        rename_i Δ σ τ hΔ hσ
        simpa only [P01DF.Syntactic.polynomial_snd, mixed_inst,
          P01DF.Syntactic.polynomial_fst] using
          Has.sigmaSnd (iF hΔ hσ)
            (by simpa only [mixed_inst, P01DF.Syntactic.polynomial_fst] using
              iI hΔ hσ) (iz hΔ hσ)
    | identityIntro hF hp hq hc iF ip iq =>
        rename_i Δ σ τ hΔ hσ
        exact .identityIntro (iF hΔ hσ) (ip hΔ hσ)
          (iq hΔ hσ) (polyConv_subst hc _)
    | proofErase hR hI hp iR iI ip =>
        rename_i Δ σ τ hΔ hσ
        exact .proofErase (iR hΔ hσ) (iI hΔ hσ) (ip hΔ hσ)
    | @j Γ A x B y e d hA hB hI hD hE hx hy he hd iA iB iI iD iE ix iy ie id =>
        rename_i Δ σ τ hΔ hσ
        have hA' := iA hΔ hσ
        have hx' := ix hΔ hσ
        have hθ := ctx_theta hΔ hA' hx'
        have hB' := iB hθ (hσ.theta hΔ hA' hx')
        have hI' := iI hΔ hσ
        have hD' := iD hΔ hσ
        have hE' := iE hΔ hσ
        have hy' := iy hΔ hσ
        have he' := ie hΔ hσ
        have hd' := id hΔ hσ
        simp only [mixed, mixed_motiveAt, psub] at hI' hD' hE' he' hd'
        simpa only [P01DF.Syntactic.polynomial_j, mixed_motiveAt] using
          Has.j hA' hB' hI' hD' hE' hx' hy' he' hd'
    | conv hA hp hc hs iA ip =>
        rename_i Δ σ τ hΔ hσ
        exact .conv (iA hΔ hσ) (ip hΔ hσ)
          (polyConv_subst hc _) (scoped_subst hs (fun n hn => hσ.scope n hn))


theorem has_mixed {Γ : Tel} {p : Poly} {A : Ty} (h : Has Γ p A)
    {Δ : Tel} {σ : Nat → Poly} {τ : Nat → Ty}
    (hΔ : Ctx Δ) (hσ : MixedSubstitution Γ Δ σ τ) :
    Has Δ (psub σ p) (mixed σ τ A) := by
  have hi := form_mixed (Form.identity (has_form h) h h) hΔ hσ
  cases hi with
  | identity _ hp _ => exact hp

/-- Source components have a finite list and the accepted atom-zero unused tail. -/
def images : List Poly → Nat → Poly
  | [] => fun _ => .atom .zero
  | a :: σ => cons a (images σ)

/-- Each declaration is substituted using only the already supplied tail terms.
Replacement types may mention every variable of the full target telescope. -/
inductive MixedTerms (Δ : Tel) (τ : Nat → Ty) : Tel → List Poly → Prop
  | nil : Ctx Δ → MixedTerms Δ τ [] []
  | cons : MixedTerms Δ τ Γ σ → Form Γ A → Has Δ a (mixed (images σ) τ A) →
      MixedTerms Δ τ (A :: Γ) (a :: σ)

/-- A genuinely finite contextual mixed map. Bottom padding makes the type
formation obligations finite without restricting dependencies in target images. -/
structure MixedSub (Δ Γ : Tel) (σ : List Poly) (τ : List Ty) : Prop where
  terms : MixedTerms Δ (typeImages τ) Γ σ
  types : ∀ n, n < τ.length → Form Δ (typeImages τ n)

theorem MixedTerms.target {Δ Γ : Tel} {σ : List Poly} {τ : Nat → Ty}
    (h : MixedTerms Δ τ Γ σ) : Ctx Δ := by
  induction h with
  | nil h => exact h
  | cons h hA ha ih => exact ih

theorem MixedTerms.source {Δ Γ : Tel} {σ : List Poly} {τ : Nat → Ty}
    (h : MixedTerms Δ τ Γ σ) : Ctx Γ := by
  induction h with
  | nil h => exact .nil
  | cons h hA ha ih => exact .ext ih hA

theorem MixedTerms.length {Δ Γ : Tel} {σ : List Poly} {τ : Nat → Ty}
    (h : MixedTerms Δ τ Γ σ) : σ.length = Γ.length := by
  induction h with
  | nil h => rfl
  | cons h hA ha ih => exact congrArg Nat.succ ih

theorem mixed_cons_wk (A : Ty) (a : Poly) (σ : Nat → Poly) (τ : Nat → Ty) :
    mixed (cons a σ) τ (wk A) = mixed σ τ A := by
  rw [wk, mixed_subst]
  rfl

theorem MixedTerms.lookup {Δ Γ : Tel} {σ : List Poly} {τ : Nat → Ty}
    (h : MixedTerms Δ τ Γ σ) {n : Nat} {A : Ty} (hn : Lookup Γ n A) :
    Has Δ (images σ n) (mixed (images σ) τ A) := by
  induction h generalizing n A with
  | nil h => cases hn
  | cons h hA ha ih =>
      cases hn with
      | zero => simpa only [images, cons, mixed_cons_wk] using ha
      | succ hn => simpa only [images, cons, mixed_cons_wk] using ih hn

theorem typeImages_ge (τ : List Ty) {n : Nat} (hn : τ.length ≤ n) :
    typeImages τ n = .bottom := by
  induction τ generalizing n with
  | nil => rfl
  | cons A τ ih =>
      cases n with
      | zero => exact False.elim (Nat.not_succ_le_zero _ hn)
      | succ n => exact ih (Nat.le_of_succ_le_succ hn)

theorem MixedSub.target {Δ Γ : Tel} {σ : List Poly} {τ : List Ty}
    (h : MixedSub Δ Γ σ τ) : Ctx Δ := h.terms.target

theorem MixedSub.source {Δ Γ : Tel} {σ : List Poly} {τ : List Ty}
    (h : MixedSub Δ Γ σ τ) : Ctx Γ := h.terms.source

theorem MixedSub.length {Δ Γ : Tel} {σ : List Poly} {τ : List Ty}
    (h : MixedSub Δ Γ σ τ) : σ.length = Γ.length := h.terms.length

theorem MixedSub.typeForm {Δ Γ : Tel} {σ : List Poly} {τ : List Ty}
    (h : MixedSub Δ Γ σ τ) (n : Nat) : Form Δ (typeImages τ n) := by
  by_cases hn : n < τ.length
  · exact h.types n hn
  · rw [typeImages_ge τ (Nat.le_of_not_gt hn)]
    exact .bottom h.target

theorem MixedSub.toSubstitution {Δ Γ : Tel} {σ : List Poly} {τ : List Ty}
    (h : MixedSub Δ Γ σ τ) : MixedSubstitution Γ Δ (images σ) (typeImages τ) :=
  ⟨h.typeForm, h.terms.lookup⟩

theorem MixedSub.scope {Δ Γ : Tel} {σ : List Poly} {τ : List Ty}
    (h : MixedSub Δ Γ σ τ) : ScopedSub Γ.length Δ.length (images σ) := h.toSubstitution.scope

theorem MixedSub.form {Δ Γ : Tel} {σ : List Poly} {τ : List Ty}
    (h : MixedSub Δ Γ σ τ) {A : Ty} (hA : Form Γ A) :
    Form Δ (mixed (images σ) (typeImages τ) A) := form_mixed hA h.target h.toSubstitution

theorem MixedSub.has {Δ Γ : Tel} {σ : List Poly} {τ : List Ty}
    (h : MixedSub Δ Γ σ τ) {p : Poly} {A : Ty} (hp : Has Γ p A) :
    Has Δ (psub (images σ) p) (mixed (images σ) (typeImages τ) A) :=
  has_mixed hp h.target h.toSubstitution

/-- Zero padding is stable even beyond the actual finite list. -/
theorem images_map (σ : List Poly) (δ : Nat → Poly) :
    images (σ.map (psub δ)) = fun n => psub δ (images σ n) := by
  induction σ with
  | nil => rfl
  | cons a σ ih =>
      funext n
      cases n with
      | zero => rfl
      | succ n => exact congrFun ih n

/-- Composition maps the two finite tables, keeping their separate paddings. -/
theorem MixedSub.comp {Γ Δ Ξ : Tel} {σ δ : List Poly} {τ υ : List Ty}
    (h : MixedSub Δ Γ σ τ) (g : MixedSub Ξ Δ δ υ) :
    MixedSub Ξ Γ (σ.map (psub (images δ)))
      (τ.map (mixed (images δ) (typeImages υ))) := by
  rcases h with ⟨hh, ht⟩
  constructor
  · induction hh with
    | nil hΔ => exact .nil g.target
    | cons hh hA ha ih =>
        apply MixedTerms.cons ih hA
        simpa only [mixed_comp, images_map, typeImages_mixed] using g.has ha
  · intro n hn
    simpa only [typeImages_mixed] using
      g.form (ht n (by simpa only [List.length_map] using hn))

/-- The finite term lift adds one variable, then weakens all old components. -/
def liftImages (σ : List Poly) : List Poly := .var 0 :: σ.map (pren Nat.succ)

theorem images_lift (σ : List Poly) : images (liftImages σ) = pup (images σ) := by
  funext n
  cases n with
  | zero => rfl
  | succ n => exact congrFun (images_map σ (fun k => .var (k+1))) n

/-- All adds a type coordinate only. Its finite type table remains Bottom-default. -/
def liftTypes (τ : List Ty) : List Ty := .param 0 :: τ.map twk

theorem typeImages_lift (τ : List Ty) : typeImages (liftTypes τ) = tup (typeImages τ) := by
  funext n
  cases n with
  | zero => rfl
  | succ n => exact congrFun (typeImages_trename τ Nat.succ) n

theorem typeImages_wk (τ : List Ty) :
    typeImages (τ.map wk) = fun n => wk (typeImages τ n) :=
  typeImages_subst τ (fun n => .var (n+1))

/-- Weakening the target shifts every term-dependent replacement image. -/
theorem MixedTerms.weaken {Δ Γ : Tel} {σ : List Poly} {τ : Nat → Ty}
    (h : MixedTerms Δ τ Γ σ) {B : Ty} (hB : Form Δ B) :
    MixedTerms (B :: Δ) (fun n => wk (τ n)) Γ (σ.map (pren Nat.succ)) := by
  induction h with
  | nil hΔ => exact .nil (.ext hΔ hB)
  | cons h hA ha ih =>
      apply MixedTerms.cons ih hA
      have hh := has_wk ha h.target hB
      simpa only [wk, subst_mixed, images_map, pren] using hh

theorem MixedSub.lift {Δ Γ : Tel} {σ : List Poly} {τ : List Ty}
    (h : MixedSub Δ Γ σ τ) {A : Ty} (hA : Form Γ A) :
    MixedSub (mixed (images σ) (typeImages τ) A :: Δ) (A :: Γ)
      (liftImages σ) (τ.map wk) := by
  have hf := h.form hA
  constructor
  · apply MixedTerms.cons (by simpa only [typeImages_wk] using h.terms.weaken hf) hA
    have he : mixed (images (σ.map (pren Nat.succ))) (typeImages (τ.map wk)) A =
        wk (mixed (images σ) (typeImages τ) A) := by
      simp only [typeImages_wk, wk, images_map, pren, subst_mixed]
    rw [he]
    exact .var (form_wk hf h.target hf) .zero
  · intro n hn
    simpa only [typeImages_wk] using form_wk (h.typeForm n) h.target hf

/-- Type weakening of the source changes declaration types, never term indices. -/
theorem MixedTerms.twk {Δ Γ : Tel} {σ : List Poly} {τ : Nat → Ty}
    (h : MixedTerms Δ τ Γ σ) : MixedTerms (twkTel Δ) (tup τ) (twkTel Γ) σ := by
  induction h with
  | nil hΔ => exact .nil (ctx_twk hΔ)
  | cons h hA ha ih =>
      apply MixedTerms.cons ih (form_twk hA)
      simpa only [mixed_twk] using has_twk ha

theorem MixedSub.twk {Δ Γ : Tel} {σ : List Poly} {τ : List Ty}
    (h : MixedSub Δ Γ σ τ) : MixedSub (twkTel Δ) (twkTel Γ) σ (liftTypes τ) := by
  constructor
  · simpa only [typeImages_lift] using h.terms.twk
  · intro n hn
    rw [typeImages_lift]
    cases n with
    | zero => exact .param (ctx_twk h.target)
    | succ n => exact form_twk (h.typeForm n)

theorem MixedSub.theta {Δ Γ : Tel} {σ : List Poly} {τ : List Ty}
    (h : MixedSub Δ Γ σ τ) {A : Ty} {x : Poly} (hA : Form Γ A) (hx : Has Γ x A) :
    MixedSub (theta Δ (mixed (images σ) (typeImages τ) A) (psub (images σ) x))
      (theta Γ A x) (liftImages (liftImages σ)) ((τ.map wk).map wk) := by
  have hh := (h.lift hA).lift (form_theta_head h.source hA hx)
  simpa only [P01AC.theta, images_lift, typeImages_wk, mixed_theta_head] using hh

/-- Binder-aware finite support of the free type-parameter sort. -/
def typeSupport : Ty → Nat
  | .param n => n+1
  | .bottom | .raw => 0
  | .all B => typeSupport B - 1
  | .pi A B | .sigma A B => max (typeSupport A) (typeSupport B)
  | .identity A _ _ => typeSupport A

def telTypeSupport : Tel → Nat
  | [] => 0
  | A :: Γ => max (typeSupport A) (telTypeSupport Γ)

theorem typeSupport_subst (A : Ty) (σ : Nat → Poly) :
    typeSupport (subst σ A) = typeSupport A := by
  induction A generalizing σ with
  | param n => rfl
  | bottom => rfl
  | raw => rfl
  | all B ih => simp only [subst, typeSupport, ih]
  | pi A B ia ib => simp only [subst, typeSupport, ia, ib]
  | sigma A B ia ib => simp only [subst, typeSupport, ia, ib]
  | identity A p q ia => exact ia σ

theorem typeSupport_wk (A : Ty) : typeSupport (wk A) = typeSupport A := typeSupport_subst A _

theorem psub_scoped_congr {n : Nat} {p : Poly} {σ δ : Nat → Poly}
    (h : Scoped n p) (he : ∀ k, k < n → σ k = δ k) : psub σ p = psub δ p := by
  induction p with
  | var k => exact he k h
  | atom t => rfl
  | app f a iff ia => exact congrArg₂ Poly.app (iff h.1) (ia h.2)

theorem mixed_term_congr {n : Nat} {A : Ty} {σ δ : Nat → Poly} {τ : Nat → Ty}
    (h : TyScoped n A) (he : ∀ k, k < n → σ k = δ k) :
    mixed σ τ A = mixed δ τ A := by
  induction A generalizing n σ δ τ with
  | param k => rfl
  | bottom => rfl
  | raw => rfl
  | all B ih => exact congrArg Ty.all (ih h he)
  | pi A B ia ib | sigma A B ia ib =>
      have hl : ∀ k, k < n+1 → pup σ k = pup δ k := by
        intro k hk
        cases k with
        | zero => rfl
        | succ k => exact congrArg (pren Nat.succ) (he k (Nat.lt_of_succ_lt_succ hk))
      first
      | exact congrArg₂ Ty.pi (ia h.1 he) (ib h.2 hl)
      | exact congrArg₂ Ty.sigma (ia h.1 he) (ib h.2 hl)
  | identity A p q ia =>
      simp only [mixed, ia h.1 he, psub_scoped_congr h.2.1 he, psub_scoped_congr h.2.2 he]

theorem mixed_type_congr (A : Ty) (σ : Nat → Poly) {τ υ : Nat → Ty}
    (h : ∀ k, k < typeSupport A → τ k = υ k) : mixed σ τ A = mixed σ υ A := by
  induction A generalizing σ τ υ with
  | param n => exact h n (Nat.lt_succ_self n)
  | bottom => rfl
  | raw => rfl
  | all B ih =>
      apply congrArg Ty.all
      apply ih
      intro n hn
      cases n with
      | zero => rfl
      | succ n =>
          change twk (τ n) = twk (υ n)
          rw [h n (by change n < typeSupport B - 1; omega)]
  | pi A B ia ib | sigma A B ia ib =>
      have ha : ∀ k, k < typeSupport A → τ k = υ k :=
        fun k hk => h k (Nat.lt_of_lt_of_le hk (Nat.le_max_left _ _))
      have hb : ∀ k, k < typeSupport B → wk (τ k) = wk (υ k) :=
        fun k hk => congrArg wk (h k (Nat.lt_of_lt_of_le hk (Nat.le_max_right _ _)))
      first
      | exact congrArg₂ Ty.pi (ia σ ha) (ib (pup σ) hb)
      | exact congrArg₂ Ty.sigma (ia σ ha) (ib (pup σ) hb)
  | identity A p q ia => exact congrArg (fun C => Ty.identity C (psub σ p) (psub σ q)) (ia σ h)

/-- Finite identity list. Its unused tail stays atom zero, never Poly.var. -/
def identityImages : Nat → List Poly
  | 0 => []
  | n+1 => liftImages (identityImages n)

theorem identityImages_length (n : Nat) : (identityImages n).length = n := by
  induction n with
  | zero => rfl
  | succ n ih => simpa only [identityImages, liftImages, List.length_cons, List.length_map] using congrArg Nat.succ ih

theorem identityImages_get {n k : Nat} (h : k < n) : images (identityImages n) k = .var k := by
  induction n generalizing k with
  | zero => exact False.elim (Nat.not_lt_zero _ h)
  | succ n ih =>
      rw [identityImages, images_lift]
      cases k with
      | zero => rfl
      | succ k =>
          change pren Nat.succ (images (identityImages n) k) = .var (k+1)
          rw [ih (Nat.lt_of_succ_lt_succ h)]
          rfl

theorem psub_identityImages {n : Nat} {p : Poly} (h : Scoped n p) :
    psub (images (identityImages n)) p = p := by
  rw [psub_scoped_congr h (fun _ hk => identityImages_get hk), psub_id]

theorem mixed_identityImages {n : Nat} {A : Ty} (h : TyScoped n A) (τ : Nat → Ty) :
    mixed (images (identityImages n)) τ A = tsubst τ A :=
  mixed_term_congr h (fun _ hk => identityImages_get hk)

/-- Finite free-parameter identity table, Bottom outside its indicated support. -/
def parameterImages : Nat → List Ty
  | 0 => []
  | n+1 => .param 0 :: (parameterImages n).map twk

theorem parameterImages_length (n : Nat) : (parameterImages n).length = n := by
  induction n with
  | zero => rfl
  | succ n ih => simpa only [parameterImages, List.length_cons, List.length_map] using congrArg Nat.succ ih

theorem parameterImages_get {n k : Nat} (h : k < n) : typeImages (parameterImages n) k = .param k := by
  induction n generalizing k with
  | zero => exact False.elim (Nat.not_lt_zero _ h)
  | succ n ih =>
      change typeImages (liftTypes (parameterImages n)) k = .param k
      rw [typeImages_lift]
      cases k with
      | zero => rfl
      | succ k =>
          change twk (typeImages (parameterImages n) k) = .param (k+1)
          rw [ih (Nat.lt_of_succ_lt_succ h)]
          rfl

theorem tsubst_parameterImages (A : Ty) {n : Nat} (h : typeSupport A ≤ n) :
    tsubst (typeImages (parameterImages n)) A = A := by
  change mixed Poly.var (typeImages (parameterImages n)) A = A
  rw [mixed_type_congr A Poly.var (fun k hk => parameterImages_get (Nat.lt_of_lt_of_le hk h)), mixed_id]

/-- Both finite identities cancel on their proved finite supports. -/
theorem mixed_finite_identity {m n : Nat} {A : Ty} (hm : TyScoped m A) (hn : typeSupport A ≤ n) :
    mixed (images (identityImages m)) (typeImages (parameterImages n)) A = A := by
  rw [mixed_identityImages hm, tsubst_parameterImages A hn]

theorem lookup_form {Γ : Tel} {n : Nat} {A : Ty} (hΓ : Ctx Γ) (h : Lookup Γ n A) : Form Γ A := by
  induction h with
  | zero =>
      cases hΓ with
      | ext hΓ hA => exact form_wk hA hΓ hA
  | succ h ih =>
      cases hΓ with
      | ext hΓ hB => exact form_wk (ih hΓ) hΓ hB

theorem lookup_typeSupport {Γ : Tel} {n : Nat} {A : Ty} (h : Lookup Γ n A) :
    typeSupport A ≤ telTypeSupport Γ := by
  induction h with
  | zero => simpa only [typeSupport_wk, telTypeSupport] using Nat.le_max_left (typeSupport _) (telTypeSupport _)
  | succ h ih =>
      rw [typeSupport_wk]
      exact Nat.le_trans ih (Nat.le_max_right _ _)

/-- Lookup evidence reconstructs the finite, tail-instantiated declaration tree. -/
theorem MixedTerms.ofLookup {Δ Γ : Tel} {σ : List Poly} {τ : Nat → Ty}
    (hΔ : Ctx Δ) (hΓ : Ctx Γ) (hlen : σ.length = Γ.length)
    (h : ∀ {n A}, Lookup Γ n A → Has Δ (images σ n) (mixed (images σ) τ A)) :
    MixedTerms Δ τ Γ σ := by
  induction Γ generalizing σ with
  | nil =>
      cases σ with
      | nil => exact .nil hΔ
      | cons a σ => simp only [List.length_cons, List.length_nil] at hlen; omega
  | cons A Γ ih =>
      cases σ with
      | nil => simp only [List.length_cons, List.length_nil] at hlen; omega
      | cons a σ =>
          cases hΓ with
          | ext hΓ hA =>
              apply MixedTerms.cons (ih hΓ (Nat.succ.inj hlen) ?_) hA
              · simpa only [images, cons, mixed_cons_wk] using h (Lookup.zero (A := A) (Γ := Γ))
              · intro n B hb
                simpa only [images, cons, mixed_cons_wk] using h (Lookup.succ hb)

theorem MixedSub.id {Γ : Tel} (hΓ : Ctx Γ) (n : Nat) (hn : telTypeSupport Γ ≤ n) :
    MixedSub Γ Γ (identityImages Γ.length) (parameterImages n) := by
  constructor
  · apply MixedTerms.ofLookup hΓ hΓ (identityImages_length Γ.length)
    intro k A hk
    rw [identityImages_get (lookup_lt hk), mixed_finite_identity
      (form_scoped (lookup_form hΓ hk)) (Nat.le_trans (lookup_typeSupport hk) hn)]
    exact .var (lookup_form hΓ hk) hk
  · intro k hk
    rw [parameterImages_get (by simpa only [parameterImages_length] using hk)]
    exact .param hΓ

/-- Finite All-elimination map: all term coordinates stay in the same target,
while the replacement may depend on every one of them. -/
theorem MixedSub.allElim {Γ : Tel} {A : Ty} (hΓ : Ctx Γ) (hA : Form Γ A)
    (n : Nat) (hn : telTypeSupport Γ ≤ n) :
    MixedSub Γ (twkTel Γ) (identityImages Γ.length) (A :: parameterImages n) := by
  constructor
  · apply MixedTerms.ofLookup hΓ (ctx_twk hΓ)
      (by simp only [identityImages_length, twkTel, List.length_map])
    intro k B hb
    obtain ⟨C, hc, rfl⟩ := lookup_trename_inv hb
    change Has Γ (images (identityImages Γ.length) k)
      (mixed (images (identityImages Γ.length)) (cons A (typeImages (parameterImages n))) (P01AC.twk C))
    rw [mixed_twk_cancel, identityImages_get (lookup_lt hc),
      mixed_finite_identity (form_scoped (lookup_form hΓ hc))
        (Nat.le_trans (lookup_typeSupport hc) hn)]
    exact .var (lookup_form hΓ hc) hc
  · intro k hk
    cases k with
    | zero => exact hA
    | succ k =>
        change Form Γ (typeImages (parameterImages n) k)
        rw [parameterImages_get (by simpa only [List.length_cons, parameterImages_length,
          Nat.succ_lt_succ_iff] using hk)]
        exact .param hΓ

theorem mixed_finite_instance_top {m n : Nat} {B A : Ty}
    (hm : TyScoped m B) (hn : typeSupport B ≤ n+1) :
    mixed (images (identityImages m)) (typeImages (A :: parameterImages n)) B = tinst B A := by
  rw [mixed_identityImages hm]
  apply mixed_type_congr
  intro k hk
  cases k with
  | zero => rfl
  | succ k =>
      change typeImages (parameterImages n) k = .param k
      exact parameterImages_get (by omega)

/-- Result formation at top type substitution is derived from finite syntax. -/
theorem form_tinst {Γ : Tel} {B A : Ty} (hB : Form (twkTel Γ) B) (hA : Form Γ A) :
    Form Γ (tinst B A) := by
  let n := max (telTypeSupport Γ) (typeSupport B)
  have hs := MixedSub.allElim (form_ctx hA) hA n (Nat.le_max_left _ _)
  have hb := hs.form hB
  rw [mixed_finite_instance_top (by simpa only [twkTel, List.length_map] using form_scoped hB)
    (Nat.le_trans (Nat.le_max_right _ _) (Nat.le_succ n))] at hb
  exact hb

/-- Erased top instantiation changes no polynomial at all, including open terms. -/
theorem has_tinst {Γ : Tel} {p : Poly} {B A : Ty}
    (hp : Has (twkTel Γ) p B) (hA : Form Γ A) : Has Γ p (tinst B A) := by
  let n := max (telTypeSupport Γ) (typeSupport B)
  have hs := MixedSub.allElim (form_ctx hA) hA n (Nat.le_max_left _ _)
  have hh := hs.has hp
  rw [mixed_finite_instance_top (by simpa only [twkTel, List.length_map] using form_scoped (has_form hp))
    (Nat.le_trans (Nat.le_max_right _ _) (Nat.le_succ n)),
    psub_identityImages (by simpa only [twkTel, List.length_map] using has_scoped hp)] at hh
  exact hh

/-- The inherited pure-term finite interface is the parameter-identity specialization. -/
abbrev TypedSub (Δ Γ : Tel) (σ : List Poly) : Prop := MixedTerms Δ Ty.param Γ σ

theorem TypedSub.toSubstitution {Δ Γ : Tel} {σ : List Poly} (h : TypedSub Δ Γ σ) :
    MixedSubstitution Γ Δ (images σ) Ty.param :=
  ⟨fun _ => .param h.target, h.lookup⟩

theorem TypedSub.form {Δ Γ : Tel} {σ : List Poly} (h : TypedSub Δ Γ σ)
    {A : Ty} (hA : Form Γ A) : Form Δ (subst (images σ) A) := by
  simpa only [mixed_param] using form_mixed hA h.target h.toSubstitution

theorem TypedSub.has {Δ Γ : Tel} {σ : List Poly} (h : TypedSub Δ Γ σ)
    {p : Poly} {A : Ty} (hp : Has Γ p A) : Has Δ (psub (images σ) p) (subst (images σ) A) := by
  simpa only [mixed_param] using has_mixed hp h.target h.toSubstitution

theorem TypedSub.scope {Δ Γ : Tel} {σ : List Poly} (h : TypedSub Δ Γ σ) :
    ScopedSub Γ.length Δ.length (images σ) := h.toSubstitution.scope

theorem TypedSub.comp {Γ Δ Ξ : Tel} {σ δ : List Poly}
    (h : TypedSub Δ Γ σ) (g : TypedSub Ξ Δ δ) : TypedSub Ξ Γ (σ.map (psub (images δ))) := by
  induction h with
  | nil hΔ => exact .nil g.target
  | cons h hA ha ih =>
      apply MixedTerms.cons ih hA
      simpa only [mixed_param, subst_comp, images_map] using g.has ha

theorem TypedSub.id {Γ : Tel} (hΓ : Ctx Γ) : TypedSub Γ Γ (identityImages Γ.length) := by
  apply MixedTerms.ofLookup hΓ hΓ (identityImages_length Γ.length)
  intro k A hk
  rw [identityImages_get (lookup_lt hk), mixed_identityImages (form_scoped (lookup_form hΓ hk)), tsubst_id]
  exact .var (lookup_form hΓ hk) hk

end P01AC
