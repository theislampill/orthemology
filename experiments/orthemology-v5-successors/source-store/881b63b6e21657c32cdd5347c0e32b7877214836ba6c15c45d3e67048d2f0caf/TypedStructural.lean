/- Finite syntactic context maps and derivation reindexing. -/
import TypedAlgebra

namespace P01TC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

/-- The polynomial substitution associated with a variable renaming. -/
def renSub (r : Nat → Nat) : Nat → Poly := fun n => .var (r n)

theorem renSub_lift (r : Nat → Nat) : renSub (liftRen r) = pup (renSub r) := by
  funext n
  cases n <;> rfl

/-- A finite-scope renaming preserves the actual dependent lookup types. -/
structure Renaming (Γ Δ : Tel) (r : Nat → Nat) : Prop where
  scope : ∀ n, n < Γ.length → r n < Δ.length
  lookup : ∀ {n A}, Lookup Γ n A → Lookup Δ (r n) (subst (renSub r) A)

theorem Renaming.id (Γ : Tel) : Renaming Γ Γ id := by
  refine ⟨fun _ h => h, ?_⟩
  intro n A h
  change Lookup Γ n (subst Poly.var A)
  rw [subst_id]
  exact h

theorem Renaming.lift {Γ Δ : Tel} {r : Nat → Nat} (h : Renaming Γ Δ r) (A : Ty) :
    Renaming (A :: Γ) (subst (renSub r) A :: Δ) (liftRen r) := by
  constructor
  · intro n hn
    cases n with
    | zero => exact Nat.zero_lt_succ _
    | succ n => exact Nat.succ_lt_succ (h.scope n (Nat.lt_of_succ_lt_succ hn))
  · intro n B hn
    cases hn with
    | zero =>
        simpa only [renSub_lift, subst_wk, liftRen] using
          (Lookup.zero (A := subst (renSub r) A) (Γ := Δ))
    | succ hn =>
        simpa only [renSub_lift, subst_wk, liftRen] using Lookup.succ (h.lookup hn)

theorem Renaming.weaken (Γ : Tel) (A : Ty) : Renaming Γ (A :: Γ) Nat.succ :=
  ⟨fun _ hn => Nat.succ_lt_succ hn, fun hn => Lookup.succ hn⟩

theorem subst_theta_head (A : Ty) (x : Poly) (σ : Nat → Poly) :
    subst (pup σ) (.identity (wk A) (pren Nat.succ x) (.var 0)) =
      .identity (wk (subst σ A)) (pren Nat.succ (psub σ x)) (.var 0) := by
  simp only [subst, subst_wk, P01DF.Syntactic.polynomial_shift_substitution, psub, pup]

theorem Renaming.theta {Γ Δ : Tel} {r : Nat → Nat} (h : Renaming Γ Δ r)
    (A : Ty) (x : Poly) :
    Renaming (theta Γ A x) (theta Δ (subst (renSub r) A) (psub (renSub r) x))
      (liftRen (liftRen r)) := by
  simpa only [theta, renSub_lift, subst_theta_head] using
    (h.lift A).lift (.identity (wk A) (pren Nat.succ x) (.var 0))

/-- The list fixes every source-context component; its unused tail is zero padded. -/
def images : List Poly → Nat → Poly
  | [] => fun _ => .atom .zero
  | a :: σ => cons a (images σ)

/-- A finite dependent substitution supplies a typed component for each declaration.
The declaration is instantiated by the components already supplied for its tail. -/
inductive TypedSub (Δ : Tel) : Tel → List Poly → Prop
  | nil : Ctx Δ → TypedSub Δ [] []
  | cons : TypedSub Δ Γ σ → Form Γ A → Has Δ a (subst (images σ) A) →
      TypedSub Δ (A :: Γ) (a :: σ)

theorem TypedSub.target {Δ Γ : Tel} {σ : List Poly} (h : TypedSub Δ Γ σ) : Ctx Δ := by
  induction h with
  | nil h => exact h
  | cons h hA ha ih => exact ih

theorem TypedSub.source {Δ Γ : Tel} {σ : List Poly} (h : TypedSub Δ Γ σ) : Ctx Γ := by
  induction h with
  | nil h => exact .nil
  | cons h hA ha ih => exact .ext ih hA

theorem TypedSub.length {Δ Γ : Tel} {σ : List Poly} (h : TypedSub Δ Γ σ) :
    σ.length = Γ.length := by
  induction h with
  | nil h => rfl
  | cons h hA ha ih => exact congrArg Nat.succ ih

/-- Components type at full dependent lookup types after literal substitution. -/
theorem TypedSub.lookup {Δ Γ : Tel} {σ : List Poly} (h : TypedSub Δ Γ σ)
    {n : Nat} {A : Ty} (hn : Lookup Γ n A) :
    Has Δ (images σ n) (subst (images σ) A) := by
  induction h generalizing n A with
  | nil h => cases hn
  | cons h hA ha ih =>
      cases hn with
      | zero => simpa only [images, cons, subst_wk_cancel] using ha
      | succ hn => simpa only [images, cons, subst_wk_cancel] using ih hn

/-- Every term admitted by the finite typing rules is scoped. -/
theorem has_scoped {Γ : Tel} {p : Poly} {A : Ty} (h : Has Γ p A) :
    Scoped Γ.length p := by
  induction h using Has.rec
    (motive_1 := fun _ _ => True)
    (motive_2 := fun _ _ _ => True) with
  | nil => trivial
  | ext => trivial
  | param => trivial
  | bottom => trivial
  | allFinite => trivial
  | raw => trivial
  | pi => trivial
  | sigma => trivial
  | identity => trivial
  | var hA hn ih => exact lookup_lt hn
  | i => trivial
  | k => trivial
  | s => trivial
  | finite => trivial
  | rawAtom => trivial
  | rawApp hF hf ha iF ihf iha => exact ⟨ihf, iha⟩
  | piIntro hF hb hs iF ihb => exact hs
  | piElim hF hI hf ha iF iI ihf iha => exact ⟨ihf, iha⟩
  | sigmaIntro hF hI ha hb iF iI iha ihb => exact scoped_pair iha ihb
  | sigmaFst hA hF hz iA iF ihz => exact scoped_fst ihz
  | sigmaSnd hF hI hz iF iI ihz => exact scoped_snd ihz
  | identityIntro => trivial
  | proofErase hR hI hp iR iI ihp => exact ihp
  | j hA hB hI hD hE hx hy he hd iA iB iI iD iE ihx ihy ihe ihd =>
      exact scoped_j ihd ihy ihe
  | conv hA hp hc hs iA ihp => exact hs

theorem lookup_exists (Γ : Tel) {n : Nat} (hn : n < Γ.length) : ∃ A, Lookup Γ n A := by
  induction Γ generalizing n with
  | nil => exact False.elim (Nat.not_lt_zero _ hn)
  | cons A Γ ih =>
      cases n with
      | zero => exact ⟨wk A, .zero⟩
      | succ n =>
          obtain ⟨B, hb⟩ := ih (Nat.lt_of_succ_lt_succ hn)
          exact ⟨wk B, .succ hb⟩

theorem TypedSub.scope {Δ Γ : Tel} {σ : List Poly} (h : TypedSub Δ Γ σ) :
    ScopedSub Γ.length Δ.length (images σ) := by
  intro n hn
  obtain ⟨A, hA⟩ := lookup_exists Γ hn
  exact has_scoped (h.lookup hA)

theorem renSub_comp (r s : Nat → Nat) :
    (fun n => psub (renSub s) (renSub r n)) = renSub (fun n => s (r n)) := rfl

theorem Renaming.comp {Γ Δ Ξ : Tel} {r s : Nat → Nat}
    (hr : Renaming Γ Δ r) (hs : Renaming Δ Ξ s) : Renaming Γ Ξ (fun n => s (r n)) := by
  refine ⟨fun n hn => hs.scope _ (hr.scope n hn), ?_⟩
  intro n A h
  simpa only [subst_comp, renSub_comp] using hs.lookup (hr.lookup h)

theorem subst_ren_shift (A : Ty) (r : Nat → Nat) :
    subst (renSub (fun n => r n + 1)) A = wk (subst (renSub r) A) := by
  rw [wk, subst_comp]
  rfl

theorem psub_ren_shift (p : Poly) (r : Nat → Nat) :
    psub (renSub (fun n => r n + 1)) p = pren Nat.succ (psub (renSub r) p) := by
  rw [pren, psub_comp]
  rfl

theorem form_pi_domain {Γ : Tel} {A B : Ty} (h : Form Γ (.pi A B)) : Form Γ A := by
  cases h with
  | pi hA hB => exact hA

theorem form_rename {Γ : Tel} {A : Ty} (h : Form Γ A) :
    ∀ {Δ : Tel} {r : Nat → Nat}, Ctx Δ → Renaming Γ Δ r → Form Δ (subst (renSub r) A) := by
  induction h using Form.rec
    (motive_1 := fun _ _ => True)
    (motive_3 := fun Γ p A _ => ∀ {Δ : Tel} {r : Nat → Nat},
      Ctx Δ → Renaming Γ Δ r → Has Δ (psub (renSub r) p) (subst (renSub r) A)) with
    | nil => trivial
    | ext => trivial
    | param hΓ iΓ =>
        intro Δ r hΔ hr
        exact .param hΔ
    | bottom hΓ iΓ =>
        intro Δ r hΔ hr
        exact .bottom hΔ
    | allFinite hΓ iΓ =>
        intro Δ r hΔ hr
        exact .allFinite hΔ
    | raw hΓ iΓ =>
        intro Δ r hΔ hr
        exact .raw hΔ
    | pi hA hB iA iB =>
        intro Δ r hΔ hr
        have hA' := iA hΔ hr
        have hB' := iB (.ext hΔ hA') (hr.lift _)
        simpa only [subst, renSub_lift] using Form.pi hA' hB'
    | sigma hA hB iA iB =>
        intro Δ r hΔ hr
        have hA' := iA hΔ hr
        have hB' := iB (.ext hΔ hA') (hr.lift _)
        simpa only [subst, renSub_lift] using Form.sigma hA' hB'
    | identity hA hp hq iA ip iq =>
        intro Δ r hΔ hr
        exact .identity (iA hΔ hr) (ip hΔ hr) (iq hΔ hr)
    | var hA hn iA =>
        rename_i Δ r hΔ hr
        exact .var (iA hΔ hr) (hr.lookup hn)
    | i hA hF iA iF =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_arr] using
          Has.i (iA hΔ hr)
            (by simpa only [subst_arr] using iF hΔ hr)
    | k hA hB hF iA iB iF =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_arr] using
          Has.k (iA hΔ hr) (iB hΔ hr)
            (by simpa only [subst_arr] using iF hΔ hr)
    | s hA hB hC hF iA iB iC iF =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_arr] using
          Has.s (iA hΔ hr) (iB hΔ hr) (iC hΔ hr)
            (by simpa only [subst_arr] using iF hΔ hr)
    | finite hF ht iF =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_fin] using
          Has.finite (by simpa only [subst_fin] using iF hΔ hr) ht
    | rawAtom hF iF =>
        rename_i Δ r hΔ hr
        exact .rawAtom (iF hΔ hr)
    | rawApp hF hf ha iF iFterm ia =>
        rename_i Δ r hΔ hr
        exact .rawApp (iF hΔ hr) (iFterm hΔ hr) (ia hΔ hr)
    | @piIntro Γ A B b hF hb hs iF ib =>
        rename_i Δ r hΔ hr
        have hF' := iF hΔ hr
        change Form Δ (.pi (subst (renSub r) A) (subst (pup (renSub r)) B)) at hF'
        cases hF' with
        | pi hA' hB' =>
            have hb' := ib (.ext hΔ hA') (hr.lift A)
            have hs' := scoped_subst (σ := renSub r) (m := Δ.length) hs
              (fun n hn => hr.scope n hn)
            have ht : Has Δ (abstract (psub (pup (renSub r)) b))
                (.pi (subst (renSub r) A) (subst (pup (renSub r)) B)) :=
              Has.piIntro (Form.pi hA' hB')
                (by simpa only [renSub_lift] using hb')
                (by simpa only [abstraction_naturality] using hs')
            rw [abstraction_naturality] at ht
            exact ht
    | piElim hF hI hf ha iF iI iFterm ia =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_inst, subst] using
          Has.piElim (iF hΔ hr)
            (by simpa only [subst_inst] using iI hΔ hr)
            (iFterm hΔ hr) (ia hΔ hr)
    | sigmaIntro hF hI ha hb iF iI ia ib =>
        rename_i Δ r hΔ hr
        simpa only [P01DF.Syntactic.polynomial_pair, subst] using
          Has.sigmaIntro (iF hΔ hr)
            (by simpa only [subst_inst] using iI hΔ hr)
            (ia hΔ hr)
            (by simpa only [subst_inst] using ib hΔ hr)
    | sigmaFst hA hF hz iA iF iz =>
        rename_i Δ r hΔ hr
        exact .sigmaFst (iA hΔ hr) (iF hΔ hr) (iz hΔ hr)
    | sigmaSnd hF hI hz iF iI iz =>
        rename_i Δ r hΔ hr
        simpa only [P01DF.Syntactic.polynomial_snd, subst_inst,
          P01DF.Syntactic.polynomial_fst] using
          Has.sigmaSnd (iF hΔ hr)
            (by simpa only [subst_inst, P01DF.Syntactic.polynomial_fst] using
              iI hΔ hr) (iz hΔ hr)
    | identityIntro hF hp hq hc iF ip iq =>
        rename_i Δ r hΔ hr
        exact .identityIntro (iF hΔ hr) (ip hΔ hr)
          (iq hΔ hr) (polyConv_subst hc _)
    | proofErase hR hI hp iR iI ip =>
        rename_i Δ r hΔ hr
        exact .proofErase (iR hΔ hr) (iI hΔ hr) (ip hΔ hr)
    | @j Γ A x B y e d hA hB hI hD hE hx hy he hd iA iB iI iD iE ix iy ie id =>
        rename_i Δ r hΔ hr
        have hA' := iA hΔ hr
        have hΔA : Ctx (subst (renSub r) A :: Δ) := .ext hΔ hA'
        have hwA : Form (subst (renSub r) A :: Δ) (wk (subst (renSub r) A)) := by
          simpa only [subst_ren_shift] using
            iA hΔA (hr.comp (Renaming.weaken Δ (subst (renSub r) A)))
        have hwx : Has (subst (renSub r) A :: Δ)
            (pren Nat.succ (psub (renSub r) x)) (wk (subst (renSub r) A)) := by
          simpa only [subst_ren_shift, psub_ren_shift] using
            ix hΔA (hr.comp (Renaming.weaken Δ (subst (renSub r) A)))
        have hθ : Ctx (theta Δ (subst (renSub r) A) (psub (renSub r) x)) :=
          .ext hΔA (.identity hwA hwx (.var hwA .zero))
        have hB' := iB hθ (hr.theta A x)
        have hI' := iI hΔ hr
        have hD' := iD hΔ hr
        have hE' := iE hΔ hr
        have hx' := ix hΔ hr
        have hy' := iy hΔ hr
        have he' := ie hΔ hr
        have hd' := id hΔ hr
        simp only [renSub_lift] at hB'
        simp only [subst, subst_motiveAt, psub] at hI' hD' hE' he' hd'
        simpa only [P01DF.Syntactic.polynomial_j, subst_motiveAt] using
          Has.j hA' hB' hI' hD' hE' hx' hy' he' hd'
    | conv hA hp hc hs iA ip =>
        rename_i Δ r hΔ hr
        exact .conv (iA hΔ hr) (ip hΔ hr)
          (polyConv_subst hc _) (scoped_subst hs (fun n hn => hr.scope n hn))

theorem has_rename {Γ : Tel} {p : Poly} {A : Ty} (h : Has Γ p A) :
    ∀ {Δ : Tel} {r : Nat → Nat}, Ctx Δ → Renaming Γ Δ r →
      Has Δ (psub (renSub r) p) (subst (renSub r) A) := by
  induction h using Has.rec
    (motive_1 := fun _ _ => True)
    (motive_2 := fun Γ A _ => ∀ {Δ : Tel} {r : Nat → Nat},
      Ctx Δ → Renaming Γ Δ r → Form Δ (subst (renSub r) A)) with
    | nil => trivial
    | ext => trivial
    | param hΓ iΓ =>
        rename_i Δ r hΔ hr
        exact .param hΔ
    | bottom hΓ iΓ =>
        rename_i Δ r hΔ hr
        exact .bottom hΔ
    | allFinite hΓ iΓ =>
        rename_i Δ r hΔ hr
        exact .allFinite hΔ
    | raw hΓ iΓ =>
        rename_i Δ r hΔ hr
        exact .raw hΔ
    | pi hA hB iA iB =>
        rename_i Δ r hΔ hr
        have hA' := iA hΔ hr
        have hB' := iB (.ext hΔ hA') (hr.lift _)
        simpa only [subst, renSub_lift] using Form.pi hA' hB'
    | sigma hA hB iA iB =>
        rename_i Δ r hΔ hr
        have hA' := iA hΔ hr
        have hB' := iB (.ext hΔ hA') (hr.lift _)
        simpa only [subst, renSub_lift] using Form.sigma hA' hB'
    | identity hA hp hq iA ip iq =>
        rename_i Δ r hΔ hr
        exact .identity (iA hΔ hr) (ip hΔ hr) (iq hΔ hr)
    | var hA hn iA =>
        intro Δ r hΔ hr
        exact .var (iA hΔ hr) (hr.lookup hn)
    | i hA hF iA iF =>
        intro Δ r hΔ hr
        simpa only [psub, subst_arr] using
          Has.i (iA hΔ hr)
            (by simpa only [subst_arr] using iF hΔ hr)
    | k hA hB hF iA iB iF =>
        intro Δ r hΔ hr
        simpa only [psub, subst_arr] using
          Has.k (iA hΔ hr) (iB hΔ hr)
            (by simpa only [subst_arr] using iF hΔ hr)
    | s hA hB hC hF iA iB iC iF =>
        intro Δ r hΔ hr
        simpa only [psub, subst_arr] using
          Has.s (iA hΔ hr) (iB hΔ hr) (iC hΔ hr)
            (by simpa only [subst_arr] using iF hΔ hr)
    | finite hF ht iF =>
        intro Δ r hΔ hr
        simpa only [psub, subst_fin] using
          Has.finite (by simpa only [subst_fin] using iF hΔ hr) ht
    | rawAtom hF iF =>
        intro Δ r hΔ hr
        exact .rawAtom (iF hΔ hr)
    | rawApp hF hf ha iF iFterm ia =>
        intro Δ r hΔ hr
        exact .rawApp (iF hΔ hr) (iFterm hΔ hr) (ia hΔ hr)
    | @piIntro Γ A B b hF hb hs iF ib =>
        intro Δ r hΔ hr
        have hF' := iF hΔ hr
        change Form Δ (.pi (subst (renSub r) A) (subst (pup (renSub r)) B)) at hF'
        cases hF' with
        | pi hA' hB' =>
            have hb' := ib (.ext hΔ hA') (hr.lift A)
            have hs' := scoped_subst (σ := renSub r) (m := Δ.length) hs
              (fun n hn => hr.scope n hn)
            have ht : Has Δ (abstract (psub (pup (renSub r)) b))
                (.pi (subst (renSub r) A) (subst (pup (renSub r)) B)) :=
              Has.piIntro (Form.pi hA' hB')
                (by simpa only [renSub_lift] using hb')
                (by simpa only [abstraction_naturality] using hs')
            rw [abstraction_naturality] at ht
            exact ht
    | piElim hF hI hf ha iF iI iFterm ia =>
        intro Δ r hΔ hr
        simpa only [psub, subst_inst, subst] using
          Has.piElim (iF hΔ hr)
            (by simpa only [subst_inst] using iI hΔ hr)
            (iFterm hΔ hr) (ia hΔ hr)
    | sigmaIntro hF hI ha hb iF iI ia ib =>
        intro Δ r hΔ hr
        simpa only [P01DF.Syntactic.polynomial_pair, subst] using
          Has.sigmaIntro (iF hΔ hr)
            (by simpa only [subst_inst] using iI hΔ hr)
            (ia hΔ hr)
            (by simpa only [subst_inst] using ib hΔ hr)
    | sigmaFst hA hF hz iA iF iz =>
        intro Δ r hΔ hr
        exact .sigmaFst (iA hΔ hr) (iF hΔ hr) (iz hΔ hr)
    | sigmaSnd hF hI hz iF iI iz =>
        intro Δ r hΔ hr
        simpa only [P01DF.Syntactic.polynomial_snd, subst_inst,
          P01DF.Syntactic.polynomial_fst] using
          Has.sigmaSnd (iF hΔ hr)
            (by simpa only [subst_inst, P01DF.Syntactic.polynomial_fst] using
              iI hΔ hr) (iz hΔ hr)
    | identityIntro hF hp hq hc iF ip iq =>
        intro Δ r hΔ hr
        exact .identityIntro (iF hΔ hr) (ip hΔ hr)
          (iq hΔ hr) (polyConv_subst hc _)
    | proofErase hR hI hp iR iI ip =>
        intro Δ r hΔ hr
        exact .proofErase (iR hΔ hr) (iI hΔ hr) (ip hΔ hr)
    | @j Γ A x B y e d hA hB hI hD hE hx hy he hd iA iB iI iD iE ix iy ie id =>
        intro Δ r hΔ hr
        have hA' := iA hΔ hr
        have hΔA : Ctx (subst (renSub r) A :: Δ) := .ext hΔ hA'
        have hwA : Form (subst (renSub r) A :: Δ) (wk (subst (renSub r) A)) := by
          simpa only [subst_ren_shift] using
            iA hΔA (hr.comp (Renaming.weaken Δ (subst (renSub r) A)))
        have hwx : Has (subst (renSub r) A :: Δ)
            (pren Nat.succ (psub (renSub r) x)) (wk (subst (renSub r) A)) := by
          simpa only [subst_ren_shift, psub_ren_shift] using
            ix hΔA (hr.comp (Renaming.weaken Δ (subst (renSub r) A)))
        have hθ : Ctx (theta Δ (subst (renSub r) A) (psub (renSub r) x)) :=
          .ext hΔA (.identity hwA hwx (.var hwA .zero))
        have hB' := iB hθ (hr.theta A x)
        have hI' := iI hΔ hr
        have hD' := iD hΔ hr
        have hE' := iE hΔ hr
        have hx' := ix hΔ hr
        have hy' := iy hΔ hr
        have he' := ie hΔ hr
        have hd' := id hΔ hr
        simp only [renSub_lift] at hB'
        simp only [subst, subst_motiveAt, psub] at hI' hD' hE' he' hd'
        simpa only [P01DF.Syntactic.polynomial_j, subst_motiveAt] using
          Has.j hA' hB' hI' hD' hE' hx' hy' he' hd'
    | conv hA hp hc hs iA ip =>
        intro Δ r hΔ hr
        exact .conv (iA hΔ hr) (ip hΔ hr)
          (polyConv_subst hc _) (scoped_subst hs (fun n hn => hr.scope n hn))

theorem form_wk {Γ : Tel} {A B : Ty} (h : Form Γ A) (hΓ : Ctx Γ) (hB : Form Γ B) :
    Form (B :: Γ) (wk A) := form_rename h (.ext hΓ hB) (Renaming.weaken Γ B)

theorem has_wk {Γ : Tel} {p : Poly} {A B : Ty}
    (h : Has Γ p A) (hΓ : Ctx Γ) (hB : Form Γ B) :
    Has (B :: Γ) (pren Nat.succ p) (wk A) :=
  has_rename h (.ext hΓ hB) (Renaming.weaken Γ B)

/-- The lookup interface of a syntactic typed substitution. -/
structure Substitution (Γ Δ : Tel) (σ : Nat → Poly) : Prop where
  lookup : ∀ {n A}, Lookup Γ n A → Has Δ (σ n) (subst σ A)

theorem Substitution.scope {Γ Δ : Tel} {σ : Nat → Poly} (h : Substitution Γ Δ σ) :
    ScopedSub Γ.length Δ.length σ := by
  intro n hn
  obtain ⟨A, hA⟩ := lookup_exists Γ hn
  exact has_scoped (h.lookup hA)

theorem TypedSub.toSubstitution {Δ Γ : Tel} {σ : List Poly} (h : TypedSub Δ Γ σ) :
    Substitution Γ Δ (images σ) := ⟨h.lookup⟩

theorem Substitution.lift {Γ Δ : Tel} {σ : Nat → Poly} {A : Ty}
    (h : Substitution Γ Δ σ) (hΔ : Ctx Δ) (hA : Form Δ (subst σ A)) :
    Substitution (A :: Γ) (subst σ A :: Δ) (pup σ) := by
  constructor
  intro n B hn
  cases hn with
  | zero =>
      simpa only [subst_wk, pup] using
        Has.var (form_wk hA hΔ hA) (Lookup.zero (A := subst σ A) (Γ := Δ))
  | succ hn =>
      simpa only [subst_wk, pup] using has_wk (h.lookup hn) hΔ hA

theorem form_theta_head {Γ : Tel} {A : Ty} {x : Poly}
    (hΓ : Ctx Γ) (hA : Form Γ A) (hx : Has Γ x A) :
    Form (A :: Γ) (.identity (wk A) (pren Nat.succ x) (.var 0)) :=
  .identity (form_wk hA hΓ hA) (has_wk hx hΓ hA)
    (.var (form_wk hA hΓ hA) .zero)

theorem ctx_theta {Γ : Tel} {A : Ty} {x : Poly}
    (hΓ : Ctx Γ) (hA : Form Γ A) (hx : Has Γ x A) : Ctx (theta Γ A x) :=
  .ext (.ext hΓ hA) (form_theta_head hΓ hA hx)

theorem Substitution.theta {Γ Δ : Tel} {σ : Nat → Poly} {A : Ty} {x : Poly}
    (h : Substitution Γ Δ σ) (hΔ : Ctx Δ)
    (hA : Form Δ (subst σ A)) (hx : Has Δ (psub σ x) (subst σ A)) :
    Substitution (theta Γ A x) (theta Δ (subst σ A) (psub σ x)) (pup (pup σ)) := by
  have hhead : Form (subst σ A :: Δ)
      (subst (pup σ) (.identity (wk A) (pren Nat.succ x) (.var 0))) := by
    rw [subst_theta_head]
    exact form_theta_head hΔ hA hx
  simpa only [theta, subst_theta_head] using
    (h.lift hΔ hA).lift (.ext hΔ hA) hhead

theorem form_subst {Γ : Tel} {A : Ty} (h : Form Γ A) :
    ∀ {Δ : Tel} {σ : Nat → Poly}, Ctx Δ → Substitution Γ Δ σ → Form Δ (subst (σ) A) := by
  induction h using Form.rec
    (motive_1 := fun _ _ => True)
    (motive_3 := fun Γ p A _ => ∀ {Δ : Tel} {σ : Nat → Poly},
      Ctx Δ → Substitution Γ Δ σ → Has Δ (psub (σ) p) (subst (σ) A)) with
    | nil => trivial
    | ext => trivial
    | param hΓ iΓ =>
        intro Δ σ hΔ hσ
        exact .param hΔ
    | bottom hΓ iΓ =>
        intro Δ σ hΔ hσ
        exact .bottom hΔ
    | allFinite hΓ iΓ =>
        intro Δ σ hΔ hσ
        exact .allFinite hΔ
    | raw hΓ iΓ =>
        intro Δ σ hΔ hσ
        exact .raw hΔ
    | pi hA hB iA iB =>
        intro Δ σ hΔ hσ
        have hA' := iA hΔ hσ
        have hB' := iB (.ext hΔ hA') (hσ.lift hΔ hA')
        simpa only [subst] using Form.pi hA' hB'
    | sigma hA hB iA iB =>
        intro Δ σ hΔ hσ
        have hA' := iA hΔ hσ
        have hB' := iB (.ext hΔ hA') (hσ.lift hΔ hA')
        simpa only [subst] using Form.sigma hA' hB'
    | identity hA hp hq iA ip iq =>
        intro Δ σ hΔ hσ
        exact .identity (iA hΔ hσ) (ip hΔ hσ) (iq hΔ hσ)
    | var hA hn iA =>
        rename_i Δ σ hΔ hσ
        exact hσ.lookup hn
    | i hA hF iA iF =>
        rename_i Δ σ hΔ hσ
        simpa only [psub, subst_arr] using
          Has.i (iA hΔ hσ)
            (by simpa only [subst_arr] using iF hΔ hσ)
    | k hA hB hF iA iB iF =>
        rename_i Δ σ hΔ hσ
        simpa only [psub, subst_arr] using
          Has.k (iA hΔ hσ) (iB hΔ hσ)
            (by simpa only [subst_arr] using iF hΔ hσ)
    | s hA hB hC hF iA iB iC iF =>
        rename_i Δ σ hΔ hσ
        simpa only [psub, subst_arr] using
          Has.s (iA hΔ hσ) (iB hΔ hσ) (iC hΔ hσ)
            (by simpa only [subst_arr] using iF hΔ hσ)
    | finite hF ht iF =>
        rename_i Δ σ hΔ hσ
        simpa only [psub, subst_fin] using
          Has.finite (by simpa only [subst_fin] using iF hΔ hσ) ht
    | rawAtom hF iF =>
        rename_i Δ σ hΔ hσ
        exact .rawAtom (iF hΔ hσ)
    | rawApp hF hf ha iF iFterm ia =>
        rename_i Δ σ hΔ hσ
        exact .rawApp (iF hΔ hσ) (iFterm hΔ hσ) (ia hΔ hσ)
    | @piIntro Γ A B b hF hb hs iF ib =>
        rename_i Δ σ hΔ hσ
        have hF' := iF hΔ hσ
        change Form Δ (.pi (subst (σ) A) (subst (pup (σ)) B)) at hF'
        cases hF' with
        | pi hA' hB' =>
            have hb' := ib (.ext hΔ hA') (hσ.lift hΔ hA')
            have hs' := scoped_subst (σ := σ) (m := Δ.length) hs
              (fun n hn => hσ.scope n hn)
            have ht : Has Δ (abstract (psub (pup (σ)) b))
                (.pi (subst (σ) A) (subst (pup (σ)) B)) :=
              Has.piIntro (Form.pi hA' hB')
                (by simpa only [] using hb')
                (by simpa only [abstraction_naturality] using hs')
            rw [abstraction_naturality] at ht
            exact ht
    | piElim hF hI hf ha iF iI iFterm ia =>
        rename_i Δ σ hΔ hσ
        simpa only [psub, subst_inst, subst] using
          Has.piElim (iF hΔ hσ)
            (by simpa only [subst_inst] using iI hΔ hσ)
            (iFterm hΔ hσ) (ia hΔ hσ)
    | sigmaIntro hF hI ha hb iF iI ia ib =>
        rename_i Δ σ hΔ hσ
        simpa only [P01DF.Syntactic.polynomial_pair, subst] using
          Has.sigmaIntro (iF hΔ hσ)
            (by simpa only [subst_inst] using iI hΔ hσ)
            (ia hΔ hσ)
            (by simpa only [subst_inst] using ib hΔ hσ)
    | sigmaFst hA hF hz iA iF iz =>
        rename_i Δ σ hΔ hσ
        exact .sigmaFst (iA hΔ hσ) (iF hΔ hσ) (iz hΔ hσ)
    | sigmaSnd hF hI hz iF iI iz =>
        rename_i Δ σ hΔ hσ
        simpa only [P01DF.Syntactic.polynomial_snd, subst_inst,
          P01DF.Syntactic.polynomial_fst] using
          Has.sigmaSnd (iF hΔ hσ)
            (by simpa only [subst_inst, P01DF.Syntactic.polynomial_fst] using
              iI hΔ hσ) (iz hΔ hσ)
    | identityIntro hF hp hq hc iF ip iq =>
        rename_i Δ σ hΔ hσ
        exact .identityIntro (iF hΔ hσ) (ip hΔ hσ)
          (iq hΔ hσ) (polyConv_subst hc _)
    | proofErase hR hI hp iR iI ip =>
        rename_i Δ σ hΔ hσ
        exact .proofErase (iR hΔ hσ) (iI hΔ hσ) (ip hΔ hσ)
    | @j Γ A x B y e d hA hB hI hD hE hx hy he hd iA iB iI iD iE ix iy ie id =>
        rename_i Δ σ hΔ hσ
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
        simp only [subst, subst_motiveAt, psub] at hI' hD' hE' he' hd'
        simpa only [P01DF.Syntactic.polynomial_j, subst_motiveAt] using
          Has.j hA' hB' hI' hD' hE' hx' hy' he' hd'
    | conv hA hp hc hs iA ip =>
        rename_i Δ σ hΔ hσ
        exact .conv (iA hΔ hσ) (ip hΔ hσ)
          (polyConv_subst hc _) (scoped_subst hs (fun n hn => hσ.scope n hn))

theorem has_subst {Γ : Tel} {p : Poly} {A : Ty} (h : Has Γ p A) :
    ∀ {Δ : Tel} {σ : Nat → Poly}, Ctx Δ → Substitution Γ Δ σ →
      Has Δ (psub (σ) p) (subst (σ) A) := by
  induction h using Has.rec
    (motive_1 := fun _ _ => True)
    (motive_2 := fun Γ A _ => ∀ {Δ : Tel} {σ : Nat → Poly},
      Ctx Δ → Substitution Γ Δ σ → Form Δ (subst (σ) A)) with
    | nil => trivial
    | ext => trivial
    | param hΓ iΓ =>
        rename_i Δ σ hΔ hσ
        exact .param hΔ
    | bottom hΓ iΓ =>
        rename_i Δ σ hΔ hσ
        exact .bottom hΔ
    | allFinite hΓ iΓ =>
        rename_i Δ σ hΔ hσ
        exact .allFinite hΔ
    | raw hΓ iΓ =>
        rename_i Δ σ hΔ hσ
        exact .raw hΔ
    | pi hA hB iA iB =>
        rename_i Δ σ hΔ hσ
        have hA' := iA hΔ hσ
        have hB' := iB (.ext hΔ hA') (hσ.lift hΔ hA')
        simpa only [subst] using Form.pi hA' hB'
    | sigma hA hB iA iB =>
        rename_i Δ σ hΔ hσ
        have hA' := iA hΔ hσ
        have hB' := iB (.ext hΔ hA') (hσ.lift hΔ hA')
        simpa only [subst] using Form.sigma hA' hB'
    | identity hA hp hq iA ip iq =>
        rename_i Δ σ hΔ hσ
        exact .identity (iA hΔ hσ) (ip hΔ hσ) (iq hΔ hσ)
    | var hA hn iA =>
        intro Δ σ hΔ hσ
        exact hσ.lookup hn
    | i hA hF iA iF =>
        intro Δ σ hΔ hσ
        simpa only [psub, subst_arr] using
          Has.i (iA hΔ hσ)
            (by simpa only [subst_arr] using iF hΔ hσ)
    | k hA hB hF iA iB iF =>
        intro Δ σ hΔ hσ
        simpa only [psub, subst_arr] using
          Has.k (iA hΔ hσ) (iB hΔ hσ)
            (by simpa only [subst_arr] using iF hΔ hσ)
    | s hA hB hC hF iA iB iC iF =>
        intro Δ σ hΔ hσ
        simpa only [psub, subst_arr] using
          Has.s (iA hΔ hσ) (iB hΔ hσ) (iC hΔ hσ)
            (by simpa only [subst_arr] using iF hΔ hσ)
    | finite hF ht iF =>
        intro Δ σ hΔ hσ
        simpa only [psub, subst_fin] using
          Has.finite (by simpa only [subst_fin] using iF hΔ hσ) ht
    | rawAtom hF iF =>
        intro Δ σ hΔ hσ
        exact .rawAtom (iF hΔ hσ)
    | rawApp hF hf ha iF iFterm ia =>
        intro Δ σ hΔ hσ
        exact .rawApp (iF hΔ hσ) (iFterm hΔ hσ) (ia hΔ hσ)
    | @piIntro Γ A B b hF hb hs iF ib =>
        intro Δ σ hΔ hσ
        have hF' := iF hΔ hσ
        change Form Δ (.pi (subst (σ) A) (subst (pup (σ)) B)) at hF'
        cases hF' with
        | pi hA' hB' =>
            have hb' := ib (.ext hΔ hA') (hσ.lift hΔ hA')
            have hs' := scoped_subst (σ := σ) (m := Δ.length) hs
              (fun n hn => hσ.scope n hn)
            have ht : Has Δ (abstract (psub (pup (σ)) b))
                (.pi (subst (σ) A) (subst (pup (σ)) B)) :=
              Has.piIntro (Form.pi hA' hB')
                (by simpa only [] using hb')
                (by simpa only [abstraction_naturality] using hs')
            rw [abstraction_naturality] at ht
            exact ht
    | piElim hF hI hf ha iF iI iFterm ia =>
        intro Δ σ hΔ hσ
        simpa only [psub, subst_inst, subst] using
          Has.piElim (iF hΔ hσ)
            (by simpa only [subst_inst] using iI hΔ hσ)
            (iFterm hΔ hσ) (ia hΔ hσ)
    | sigmaIntro hF hI ha hb iF iI ia ib =>
        intro Δ σ hΔ hσ
        simpa only [P01DF.Syntactic.polynomial_pair, subst] using
          Has.sigmaIntro (iF hΔ hσ)
            (by simpa only [subst_inst] using iI hΔ hσ)
            (ia hΔ hσ)
            (by simpa only [subst_inst] using ib hΔ hσ)
    | sigmaFst hA hF hz iA iF iz =>
        intro Δ σ hΔ hσ
        exact .sigmaFst (iA hΔ hσ) (iF hΔ hσ) (iz hΔ hσ)
    | sigmaSnd hF hI hz iF iI iz =>
        intro Δ σ hΔ hσ
        simpa only [P01DF.Syntactic.polynomial_snd, subst_inst,
          P01DF.Syntactic.polynomial_fst] using
          Has.sigmaSnd (iF hΔ hσ)
            (by simpa only [subst_inst, P01DF.Syntactic.polynomial_fst] using
              iI hΔ hσ) (iz hΔ hσ)
    | identityIntro hF hp hq hc iF ip iq =>
        intro Δ σ hΔ hσ
        exact .identityIntro (iF hΔ hσ) (ip hΔ hσ)
          (iq hΔ hσ) (polyConv_subst hc _)
    | proofErase hR hI hp iR iI ip =>
        intro Δ σ hΔ hσ
        exact .proofErase (iR hΔ hσ) (iI hΔ hσ) (ip hΔ hσ)
    | @j Γ A x B y e d hA hB hI hD hE hx hy he hd iA iB iI iD iE ix iy ie id =>
        intro Δ σ hΔ hσ
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
        simp only [subst, subst_motiveAt, psub] at hI' hD' hE' he' hd'
        simpa only [P01DF.Syntactic.polynomial_j, subst_motiveAt] using
          Has.j hA' hB' hI' hD' hE' hx' hy' he' hd'
    | conv hA hp hc hs iA ip =>
        intro Δ σ hΔ hσ
        exact .conv (iA hΔ hσ) (ip hΔ hσ)
          (polyConv_subst hc _) (scoped_subst hs (fun n hn => hσ.scope n hn))


/-- Finite typed substitutions preserve formation with the literal substituted type. -/
theorem TypedSub.form {Δ Γ : Tel} {σ : List Poly} (h : TypedSub Δ Γ σ)
    {A : Ty} (hA : Form Γ A) : Form Δ (subst (images σ) A) :=
  form_subst hA h.target h.toSubstitution

/-- Finite typed substitutions preserve typing with the literal substituted polynomial. -/
theorem TypedSub.has {Δ Γ : Tel} {σ : List Poly} (h : TypedSub Δ Γ σ)
    {p : Poly} {A : Ty} (hp : Has Γ p A) :
    Has Δ (psub (images σ) p) (subst (images σ) A) :=
  has_subst hp h.target h.toSubstitution

/-- A typing derivation carries formation of its exact result type. -/
theorem has_form {Γ : Tel} {p : Poly} {A : Ty} (h : Has Γ p A) : Form Γ A := by
  cases h <;> assumption

theorem form_scoped {Γ : Tel} {A : Ty} (h : Form Γ A) : TyScoped Γ.length A := by
  induction h using Form.rec
    (motive_1 := fun _ _ => True)
    (motive_3 := fun _ _ _ _ => True) with
  | nil => trivial
  | ext => trivial
  | param => trivial
  | bottom => trivial
  | allFinite => trivial
  | raw => trivial
  | pi hA hB iA iB => exact ⟨iA, iB⟩
  | sigma hA hB iA iB => exact ⟨iA, iB⟩
  | identity hA hp hq iA ip iq => exact ⟨iA, has_scoped hp, has_scoped hq⟩
  | var => trivial
  | i => trivial
  | k => trivial
  | s => trivial
  | finite => trivial
  | rawAtom => trivial
  | rawApp => trivial
  | piIntro => trivial
  | piElim => trivial
  | sigmaIntro => trivial
  | sigmaFst => trivial
  | sigmaSnd => trivial
  | identityIntro => trivial
  | proofErase => trivial
  | j => trivial
  | conv => trivial

/-- Zero padding is stable under polynomial substitution, including beyond the list. -/
theorem images_map (σ : List Poly) (τ : Nat → Poly) :
    images (σ.map (psub τ)) = fun n => psub τ (images σ n) := by
  induction σ with
  | nil => rfl
  | cons a σ ih =>
      funext n
      cases n with
      | zero => rfl
      | succ n => exact congrFun ih n

/-- Composition retains the finite list and substitutes each actual component. -/
theorem TypedSub.comp {Γ Δ Ξ : Tel} {σ τ : List Poly}
    (hσ : TypedSub Δ Γ σ) (hτ : TypedSub Ξ Δ τ) :
    TypedSub Ξ Γ (σ.map (psub (images τ))) := by
  induction hσ with
  | nil hΔ => exact .nil hτ.target
  | cons hσ hA ha ih =>
      apply TypedSub.cons ih hA
      have h := hτ.has ha
      simpa only [subst_comp, images_map] using h

end P01TC
