import JointTermRename
import JointScope
namespace JointCompletion.Structural
open P01AC P01D OrthemologyV2 OrthemologyV3 P01R
open P01F (cons)
open P01AC.ExtensionalRepair.Structural
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- All source-variable images have actual HasJ typing at their simultaneously
    substituted dependent lookup types. No original Has evidence is required. -/
structure TypedSubstitution (Γ Δ : Tel) (σ : Nat → Poly) : Prop where
  lookup : ∀ {n A}, Lookup Γ n A → HasJ Δ (σ n) (subst σ A)

theorem TypedSubstitution.scope {Γ Δ : Tel} {σ : Nat → Poly}
    (h : TypedSubstitution Γ Δ σ) : ScopedSub Γ.length Δ.length σ := by
  intro n hn
  obtain ⟨A, ha⟩ := lookup_exists Γ hn
  exact has_scoped (h.lookup ha)

theorem TypedSubstitution.lift {Γ Δ : Tel} {σ : Nat → Poly} {A : Ty}
    (h : TypedSubstitution Γ Δ σ) (hΔ : CtxJ Δ) (hA : FormJ Δ (subst σ A)) :
    TypedSubstitution (A :: Γ) (subst σ A :: Δ) (pup σ) := by
  constructor
  intro n B hn
  cases hn with
  | zero =>
      simpa only [subst_wk, pup] using
        HasJ.var (form_wk hA hΔ hA) (Lookup.zero (A := subst σ A) (Γ := Δ))
  | succ hn => simpa only [subst_wk, pup] using has_wk (h.lookup hn) hΔ hA

theorem TypedSubstitution.twk {Γ Δ : Tel} {σ : Nat → Poly}
    (h : TypedSubstitution Γ Δ σ) : TypedSubstitution (twkTel Γ) (twkTel Δ) σ := by
  constructor
  intro n B hb
  obtain ⟨A, ha, rfl⟩ := lookup_trename_inv hb
  simpa only [subst_trename] using has_twk (h.lookup ha)

theorem form_theta_head {Γ : Tel} {A : Ty} {x : Poly}
    (hΓ : CtxJ Γ) (hA : FormJ Γ A) (hx : HasJ Γ x A) :
    FormJ (A :: Γ) (.identity (wk A) (pren Nat.succ x) (.var 0)) :=
  .identity (form_wk hA hΓ hA) (has_wk hx hΓ hA)
    (.var (form_wk hA hΓ hA) .zero)

theorem ctx_theta {Γ : Tel} {A : Ty} {x : Poly}
    (hΓ : CtxJ Γ) (hA : FormJ Γ A) (hx : HasJ Γ x A) : CtxJ (theta Γ A x) :=
  .ext (.ext hΓ hA) (form_theta_head hΓ hA hx)

theorem TypedSubstitution.theta {Γ Δ : Tel} {σ : Nat → Poly} {A : Ty} {x : Poly}
    (h : TypedSubstitution Γ Δ σ) (hΔ : CtxJ Δ)
    (hA : FormJ Δ (subst σ A)) (hx : HasJ Δ (psub σ x) (subst σ A)) :
    TypedSubstitution (theta Γ A x) (theta Δ (subst σ A) (psub σ x)) (pup (pup σ)) := by
  have hhead : FormJ (subst σ A :: Δ)
      (subst (pup σ) (.identity (wk A) (pren Nat.succ x) (.var 0))) := by
    rw [subst_theta_head]
    exact form_theta_head hΔ hA hx
  simpa only [theta, subst_theta_head] using
    (h.lift hΔ hA).lift (.ext hΔ hA) hhead

theorem base_form_subst {Γ : Tel} {A : Ty} (h : P01AC.ExtensionalRepair.FormE Γ A) :
    ∀ {Δ : Tel} {σ : Nat → Poly}, CtxJ Δ → TypedSubstitution Γ Δ σ → FormJ Δ (subst (σ) A) := by
  induction h using P01AC.ExtensionalRepair.FormE.rec
    (motive_1 := fun _ _ => True)
    (motive_3 := fun Γ p A _ => ∀ {Δ : Tel} {σ : Nat → Poly},
      CtxJ Δ → TypedSubstitution Γ Δ σ → HasJ Δ (psub (σ) p) (subst (σ) A)) with
    | nil => trivial
    | ext => trivial
    | param hΓ iΓ =>
        intro Δ σ hΔ hσ
        exact .param hΔ
    | bottom hΓ iΓ =>
        intro Δ σ hΔ hσ
        exact .bottom hΔ
    | all hΓ hB iΓ iB =>
        intro Δ σ hΔ hσ
        exact .all hΔ (iB (ctx_twk hΔ) hσ.twk)
    | raw hΓ iΓ =>
        intro Δ σ hΔ hσ
        exact .raw hΔ
    | pi hA hB iA iB =>
        intro Δ σ hΔ hσ
        have hA' := iA hΔ hσ
        have hB' := iB (.ext hΔ hA') (hσ.lift hΔ hA')
        simpa only [subst] using FormJ.pi hA' hB'
    | sigma hA hB iA iB =>
        intro Δ σ hΔ hσ
        have hA' := iA hΔ hσ
        have hB' := iB (.ext hΔ hA') (hσ.lift hΔ hA')
        simpa only [subst] using FormJ.sigma hA' hB'
    | identity hA hp hq iA ip iq =>
        intro Δ σ hΔ hσ
        exact .identity (iA hΔ hσ) (ip hΔ hσ) (iq hΔ hσ)
    | var hA hn iA =>
        rename_i Δ σ hΔ hσ
        exact hσ.lookup hn
    | i hA hF iA iF =>
        rename_i Δ σ hΔ hσ
        simpa only [psub, subst_arr] using
          HasJ.i (iA hΔ hσ)
            (by simpa only [subst_arr] using iF hΔ hσ)
    | k hA hB hF iA iB iF =>
        rename_i Δ σ hΔ hσ
        simpa only [psub, subst_arr] using
          HasJ.k (iA hΔ hσ) (iB hΔ hσ)
            (by simpa only [subst_arr] using iF hΔ hσ)
    | s hA hB hC hF iA iB iC iF =>
        rename_i Δ σ hΔ hσ
        simpa only [psub, subst_arr] using
          HasJ.s (iA hΔ hσ) (iB hΔ hσ) (iC hΔ hσ)
            (by simpa only [subst_arr] using iF hΔ hσ)
    | @finite C Γ t υ hlen hυ hF ht iυ iF =>
        rename_i Δ σ hΔ hσ
        simpa only [psub, subst_finite_instance] using
          HasJ.finite (υ.map (subst (σ)))
            (by simpa only [List.length_map] using hlen)
            (fun n hn => by simpa only [typeImages_subst] using iυ n (by simpa only [List.length_map] using hn) hΔ hσ)
            (by simpa only [subst_finite_instance] using iF hΔ hσ) ht
    | allIntro hF hp iF ip =>
        rename_i Δ σ hΔ hσ
        exact .allIntro (iF hΔ hσ) (ip (ctx_twk hΔ) hσ.twk)
    | allElim hF hA hI hp iF iA iI ip =>
        rename_i Δ σ hΔ hσ
        simpa only [subst_tinst] using HasJ.allElim (iF hΔ hσ) (iA hΔ hσ)
          (by simpa only [subst_tinst] using iI hΔ hσ) (ip hΔ hσ)
    | rawAtom hF iF =>
        rename_i Δ σ hΔ hσ
        exact .rawAtom (iF hΔ hσ)
    | rawApp hF hf ha iF iFterm ia =>
        rename_i Δ σ hΔ hσ
        exact .rawApp (iF hΔ hσ) (iFterm hΔ hσ) (ia hΔ hσ)
    | @piIntro Γ A B b hF hb hs iF ib =>
        rename_i Δ σ hΔ hσ
        have hF' := iF hΔ hσ
        change FormJ Δ (.pi (subst (σ) A) (subst (pup (σ)) B)) at hF'
        obtain ⟨hA', hB'⟩ := form_pi_inv hF'
        have hb' := ib (.ext hΔ hA') (hσ.lift hΔ hA')
        have hs' := scoped_subst (σ := σ) (m := Δ.length) hs
          (fun n hn => hσ.scope n hn)
        have ht : HasJ Δ (abstract (psub (pup (σ)) b))
            (.pi (subst (σ) A) (subst (pup (σ)) B)) :=
          HasJ.piIntro (FormJ.pi hA' hB')
            (by simpa only [] using hb')
            (by simpa only [abstraction_naturality] using hs')
        rw [abstraction_naturality] at ht
        exact ht
    | piElim hF hI hf ha iF iI iFterm ia =>
        rename_i Δ σ hΔ hσ
        simpa only [psub, subst_inst, subst] using
          HasJ.piElim (iF hΔ hσ)
            (by simpa only [subst_inst] using iI hΔ hσ)
            (iFterm hΔ hσ) (ia hΔ hσ)
    | sigmaIntro hF hI ha hb iF iI ia ib =>
        rename_i Δ σ hΔ hσ
        simpa only [P01DF.Syntactic.polynomial_pair, subst] using
          HasJ.sigmaIntro (iF hΔ hσ)
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
          HasJ.sigmaSnd (iF hΔ hσ)
            (by simpa only [subst_inst, P01DF.Syntactic.polynomial_fst] using
              iI hΔ hσ) (iz hΔ hσ)
    | identityIntro hF hp hq hc iF ip iq =>
        rename_i Δ σ hΔ hσ
        exact .identityIntro (iF hΔ hσ) (ip hΔ hσ)
          (iq hΔ hσ) (polyConvPlus_subst hc _)
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
        simp only [] at hB'
        simp only [subst, subst_motiveAt, psub] at hI' hD' hE' he' hd'
        simpa only [P01DF.Syntactic.polynomial_j, subst_motiveAt] using
          HasJ.j hA' hB' hI' hD' hE' hx' hy' he' hd'
    | conv hA hp hc hs iA ip =>
        rename_i Δ σ hΔ hσ
        exact .conv (iA hΔ hσ) (ip hΔ hσ)
          (polyConvPlus_subst hc _) (scoped_subst hs (fun n hn => hσ.scope n hn))

    | @piExt Γ A B p q h hA hB hPi hp hq hBody hFam hh hId sp sq sh sa sb iA iB iPi ip iq iBody iFam ih iId =>
        rename_i Δ σ hΔ hσ
        have hA' := iA hΔ hσ
        have hΔA := CtxJ.ext hΔ hA'
        have hB' := iB hΔA (hσ.lift hΔ hA')
        have hBody' := iBody hΔA (hσ.lift hΔ hA')
        have hFam' := iFam hΔ hσ
        have hh' := ih hΔ hσ
        have hId' := iId hΔ hσ
        simp only [subst, psub,
          P01DF.Syntactic.polynomial_shift_substitution] at hB' hBody' hFam' hh' hId'
        exact .piExt hA' hB' (iPi hΔ hσ) (ip hΔ hσ) (iq hΔ hσ)
          hBody' hFam' hh' hId'
          (scoped_subst sp (fun n hn => hσ.scope n hn))
          (scoped_subst sq (fun n hn => hσ.scope n hn))
          (scoped_subst sh (fun n hn => hσ.scope n hn))
          (tyScoped_subst sa (fun n hn => hσ.scope n hn))
          (tyScoped_subst sb (scopedSub_lift (fun n hn => hσ.scope n hn)))
    | @allExt Γ B p q h hB hAll hp hq hBody hh hId sp sq sh sb iB iAll ip iq iBody ih iId =>
        rename_i Δ σ hΔ hσ
        exact .allExt (iB (ctx_twk hΔ) hσ.twk) (iAll hΔ hσ)
          (ip hΔ hσ) (iq hΔ hσ) (iBody (ctx_twk hΔ) hσ.twk)
          (ih (ctx_twk hΔ) hσ.twk) (iId hΔ hσ)
          (scoped_subst sp (fun n hn => hσ.scope n hn))
          (scoped_subst sq (fun n hn => hσ.scope n hn))
          (scoped_subst sh (fun n hn => hσ.scope n hn))
          (tyScoped_subst sb (fun n hn => hσ.scope n hn))

theorem base_has_subst {Γ : Tel} {p : Poly} {A : Ty}
    (h : P01AC.ExtensionalRepair.HasE Γ p A)
    {Δ : Tel} {σ : Nat → Poly} (hΔ : CtxJ Δ) (hσ : TypedSubstitution Γ Δ σ) :
      HasJ Δ (psub σ p) (subst σ A) := by
  have hi := base_form_subst
    (P01AC.ExtensionalRepair.FormE.identity
      (P01AC.ExtensionalRepair.ClosedProofCanonicalisation.formed h) h h) hΔ hσ
  exact (form_identity_inv hi).2.1
theorem form_subst {Γ : Tel} {A : Ty} (h : FormJ Γ A) :
    ∀ {Δ : Tel} {σ : Nat → Poly}, CtxJ Δ → TypedSubstitution Γ Δ σ → FormJ Δ (subst (σ) A) := by
  induction h using FormJ.rec
    (motive_1 := fun _ _ => True)
    (motive_3 := fun Γ p A _ => ∀ {Δ : Tel} {σ : Nat → Poly},
      CtxJ Δ → TypedSubstitution Γ Δ σ → HasJ Δ (psub (σ) p) (subst (σ) A)) with
    | ctxBase h => trivial
    | formBase h => intro Δ σ hΔ hσ; exact base_form_subst h hΔ hσ
    | hasBase h => rename_i Δ σ hΔ hσ; exact base_has_subst h hΔ hσ
    | nil => trivial
    | ext => trivial
    | param hΓ iΓ =>
        intro Δ σ hΔ hσ
        exact .param hΔ
    | bottom hΓ iΓ =>
        intro Δ σ hΔ hσ
        exact .bottom hΔ
    | all hΓ hB iΓ iB =>
        intro Δ σ hΔ hσ
        exact .all hΔ (iB (ctx_twk hΔ) hσ.twk)
    | raw hΓ iΓ =>
        intro Δ σ hΔ hσ
        exact .raw hΔ
    | pi hA hB iA iB =>
        intro Δ σ hΔ hσ
        have hA' := iA hΔ hσ
        have hB' := iB (.ext hΔ hA') (hσ.lift hΔ hA')
        simpa only [subst] using FormJ.pi hA' hB'
    | sigma hA hB iA iB =>
        intro Δ σ hΔ hσ
        have hA' := iA hΔ hσ
        have hB' := iB (.ext hΔ hA') (hσ.lift hΔ hA')
        simpa only [subst] using FormJ.sigma hA' hB'
    | identity hA hp hq iA ip iq =>
        intro Δ σ hΔ hσ
        exact .identity (iA hΔ hσ) (ip hΔ hσ) (iq hΔ hσ)
    | var hA hn iA =>
        rename_i Δ σ hΔ hσ
        exact hσ.lookup hn
    | i hA hF iA iF =>
        rename_i Δ σ hΔ hσ
        simpa only [psub, subst_arr] using
          HasJ.i (iA hΔ hσ)
            (by simpa only [subst_arr] using iF hΔ hσ)
    | k hA hB hF iA iB iF =>
        rename_i Δ σ hΔ hσ
        simpa only [psub, subst_arr] using
          HasJ.k (iA hΔ hσ) (iB hΔ hσ)
            (by simpa only [subst_arr] using iF hΔ hσ)
    | s hA hB hC hF iA iB iC iF =>
        rename_i Δ σ hΔ hσ
        simpa only [psub, subst_arr] using
          HasJ.s (iA hΔ hσ) (iB hΔ hσ) (iC hΔ hσ)
            (by simpa only [subst_arr] using iF hΔ hσ)
    | @finite C Γ t υ hlen hυ hF ht iυ iF =>
        rename_i Δ σ hΔ hσ
        simpa only [psub, subst_finite_instance] using
          HasJ.finite (υ.map (subst (σ)))
            (by simpa only [List.length_map] using hlen)
            (fun n hn => by simpa only [typeImages_subst] using iυ n (by simpa only [List.length_map] using hn) hΔ hσ)
            (by simpa only [subst_finite_instance] using iF hΔ hσ) ht
    | allIntro hF hp iF ip =>
        rename_i Δ σ hΔ hσ
        exact .allIntro (iF hΔ hσ) (ip (ctx_twk hΔ) hσ.twk)
    | allElim hF hA hI hp iF iA iI ip =>
        rename_i Δ σ hΔ hσ
        simpa only [subst_tinst] using HasJ.allElim (iF hΔ hσ) (iA hΔ hσ)
          (by simpa only [subst_tinst] using iI hΔ hσ) (ip hΔ hσ)
    | rawAtom hF iF =>
        rename_i Δ σ hΔ hσ
        exact .rawAtom (iF hΔ hσ)
    | rawApp hF hf ha iF iFterm ia =>
        rename_i Δ σ hΔ hσ
        exact .rawApp (iF hΔ hσ) (iFterm hΔ hσ) (ia hΔ hσ)
    | @piIntro Γ A B b hF hb hs iF ib =>
        rename_i Δ σ hΔ hσ
        have hF' := iF hΔ hσ
        change FormJ Δ (.pi (subst (σ) A) (subst (pup (σ)) B)) at hF'
        obtain ⟨hA', hB'⟩ := form_pi_inv hF'
        have hb' := ib (.ext hΔ hA') (hσ.lift hΔ hA')
        have hs' := scoped_subst (σ := σ) (m := Δ.length) hs
          (fun n hn => hσ.scope n hn)
        have ht : HasJ Δ (abstract (psub (pup (σ)) b))
            (.pi (subst (σ) A) (subst (pup (σ)) B)) :=
          HasJ.piIntro (FormJ.pi hA' hB')
            (by simpa only [] using hb')
            (by simpa only [abstraction_naturality] using hs')
        rw [abstraction_naturality] at ht
        exact ht
    | piElim hF hI hf ha iF iI iFterm ia =>
        rename_i Δ σ hΔ hσ
        simpa only [psub, subst_inst, subst] using
          HasJ.piElim (iF hΔ hσ)
            (by simpa only [subst_inst] using iI hΔ hσ)
            (iFterm hΔ hσ) (ia hΔ hσ)
    | sigmaIntro hF hI ha hb iF iI ia ib =>
        rename_i Δ σ hΔ hσ
        simpa only [P01DF.Syntactic.polynomial_pair, subst] using
          HasJ.sigmaIntro (iF hΔ hσ)
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
          HasJ.sigmaSnd (iF hΔ hσ)
            (by simpa only [subst_inst, P01DF.Syntactic.polynomial_fst] using
              iI hΔ hσ) (iz hΔ hσ)
    | identityIntro hF hp hq hc iF ip iq =>
        rename_i Δ σ hΔ hσ
        exact .identityIntro (iF hΔ hσ) (ip hΔ hσ)
          (iq hΔ hσ) (polyConvPlus_subst hc _)
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
        simp only [] at hB'
        simp only [subst, subst_motiveAt, psub] at hI' hD' hE' he' hd'
        simpa only [P01DF.Syntactic.polynomial_j, subst_motiveAt] using
          HasJ.j hA' hB' hI' hD' hE' hx' hy' he' hd'
    | conv hA hp hc hs iA ip =>
        rename_i Δ σ hΔ hσ
        exact .conv (iA hΔ hσ) (ip hΔ hσ)
          (polyConvPlus_subst hc _) (scoped_subst hs (fun n hn => hσ.scope n hn))

    | @piExt Γ A B p q h hA hB hPi hp hq hBody hFam hh hId sp sq sh sa sb iA iB iPi ip iq iBody iFam ih iId =>
        rename_i Δ σ hΔ hσ
        have hA' := iA hΔ hσ
        have hΔA := CtxJ.ext hΔ hA'
        have hB' := iB hΔA (hσ.lift hΔ hA')
        have hBody' := iBody hΔA (hσ.lift hΔ hA')
        have hFam' := iFam hΔ hσ
        have hh' := ih hΔ hσ
        have hId' := iId hΔ hσ
        simp only [subst, psub,
          P01DF.Syntactic.polynomial_shift_substitution] at hB' hBody' hFam' hh' hId'
        exact .piExt hA' hB' (iPi hΔ hσ) (ip hΔ hσ) (iq hΔ hσ)
          hBody' hFam' hh' hId'
          (scoped_subst sp (fun n hn => hσ.scope n hn))
          (scoped_subst sq (fun n hn => hσ.scope n hn))
          (scoped_subst sh (fun n hn => hσ.scope n hn))
          (tyScoped_subst sa (fun n hn => hσ.scope n hn))
          (tyScoped_subst sb (scopedSub_lift (fun n hn => hσ.scope n hn)))
    | @allExt Γ B p q h hB hAll hp hq hBody hh hId sp sq sh sb iB iAll ip iq iBody ih iId =>
        rename_i Δ σ hΔ hσ
        exact .allExt (iB (ctx_twk hΔ) hσ.twk) (iAll hΔ hσ)
          (ip hΔ hσ) (iq hΔ hσ) (iBody (ctx_twk hΔ) hσ.twk)
          (ih (ctx_twk hΔ) hσ.twk) (iId hΔ hσ)
          (scoped_subst sp (fun n hn => hσ.scope n hn))
          (scoped_subst sq (fun n hn => hσ.scope n hn))
          (scoped_subst sh (fun n hn => hσ.scope n hn))
          (tyScoped_subst sb (fun n hn => hσ.scope n hn))

    | @sigmaElim Γ A B P d z hΓ hA hB hP hd hz iΓ iA iB iP id iz =>
        rename_i Δ σ hΔ hσ
        have hA' := iA hΔ hσ
        have hΔA := CtxJ.ext hΔ hA'
        have sA := hσ.lift hΔ hA'
        have hB' := iB hΔA sA
        have hP' := iP (.ext hΔ (.sigma hA' hB')) (hσ.lift hΔ (.sigma hA' hB'))
        have hd' := id (.ext hΔA hB') (sA.lift hΔA hB')
        simp only [branchType_subst] at hd'
        simpa only [branchAt_subst, P01DF.Syntactic.polynomial_fst,
          P01DF.Syntactic.polynomial_snd, subst_inst] using
          HasJ.sigmaElim hΔ hA' hB' hP' hd' (iz hΔ hσ)
    | @natInduction Γ P p s hΓ hP hp hs iΓ iP ip is =>
        rename_i Δ σ hΔ hσ
        have hN : FormJ Δ (subst σ P01AC.EffectiveCompleteness.N) := by
          simpa only [P01AC.BooleanPrimitive.N_subst] using form_nat hΔ
        have hP' := iP (.ext hΔ hN) (hσ.lift hΔ hN)
        simp only [P01AC.BooleanPrimitive.N_subst] at hP'
        have hp' := ip hΔ hσ
        have hs' := is hΔ hσ
        simp only [subst_inst, zero_subst] at hp'
        simp only [dependentStepType_subst] at hs'
        simpa only [sectionPoly_subst, subst, P01AC.BooleanPrimitive.N_subst] using
          HasJ.natInduction hΔ hP' hp' hs'
theorem has_subst {Γ : Tel} {p : Poly} {A : Ty} (h : HasJ Γ p A) :
    ∀ {Δ : Tel} {σ : Nat → Poly}, CtxJ Δ → TypedSubstitution Γ Δ σ → HasJ Δ (psub σ p) (subst σ A) := by
  induction h using HasJ.rec
    (motive_1 := fun _ _ => True)
    (motive_2 := fun Γ A _ => ∀ {Δ : Tel} {σ : Nat → Poly},
      CtxJ Δ → TypedSubstitution Γ Δ σ → FormJ Δ (subst σ A)) with
    | ctxBase h => trivial
    | formBase h => rename_i Δ σ hΔ hσ; exact base_form_subst h hΔ hσ
    | hasBase h => intro Δ σ hΔ hσ; exact base_has_subst h hΔ hσ
    | nil => trivial
    | ext => trivial
    | param hΓ iΓ =>
        rename_i Δ σ hΔ hσ
        exact .param hΔ
    | bottom hΓ iΓ =>
        rename_i Δ σ hΔ hσ
        exact .bottom hΔ
    | all hΓ hB iΓ iB =>
        rename_i Δ σ hΔ hσ
        exact .all hΔ (iB (ctx_twk hΔ) hσ.twk)
    | raw hΓ iΓ =>
        rename_i Δ σ hΔ hσ
        exact .raw hΔ
    | pi hA hB iA iB =>
        rename_i Δ σ hΔ hσ
        have hA' := iA hΔ hσ
        have hB' := iB (.ext hΔ hA') (hσ.lift hΔ hA')
        simpa only [subst] using FormJ.pi hA' hB'
    | sigma hA hB iA iB =>
        rename_i Δ σ hΔ hσ
        have hA' := iA hΔ hσ
        have hB' := iB (.ext hΔ hA') (hσ.lift hΔ hA')
        simpa only [subst] using FormJ.sigma hA' hB'
    | identity hA hp hq iA ip iq =>
        rename_i Δ σ hΔ hσ
        exact .identity (iA hΔ hσ) (ip hΔ hσ) (iq hΔ hσ)
    | var hA hn iA =>
        intro Δ σ hΔ hσ
        exact hσ.lookup hn
    | i hA hF iA iF =>
        intro Δ σ hΔ hσ
        simpa only [psub, subst_arr] using
          HasJ.i (iA hΔ hσ)
            (by simpa only [subst_arr] using iF hΔ hσ)
    | k hA hB hF iA iB iF =>
        intro Δ σ hΔ hσ
        simpa only [psub, subst_arr] using
          HasJ.k (iA hΔ hσ) (iB hΔ hσ)
            (by simpa only [subst_arr] using iF hΔ hσ)
    | s hA hB hC hF iA iB iC iF =>
        intro Δ σ hΔ hσ
        simpa only [psub, subst_arr] using
          HasJ.s (iA hΔ hσ) (iB hΔ hσ) (iC hΔ hσ)
            (by simpa only [subst_arr] using iF hΔ hσ)
    | @finite C Γ t υ hlen hυ hF ht iυ iF =>
        intro Δ σ hΔ hσ
        simpa only [psub, subst_finite_instance] using
          HasJ.finite (υ.map (subst (σ)))
            (by simpa only [List.length_map] using hlen)
            (fun n hn => by simpa only [typeImages_subst] using iυ n (by simpa only [List.length_map] using hn) hΔ hσ)
            (by simpa only [subst_finite_instance] using iF hΔ hσ) ht
    | allIntro hF hp iF ip =>
        intro Δ σ hΔ hσ
        exact .allIntro (iF hΔ hσ) (ip (ctx_twk hΔ) hσ.twk)
    | allElim hF hA hI hp iF iA iI ip =>
        intro Δ σ hΔ hσ
        simpa only [subst_tinst] using HasJ.allElim (iF hΔ hσ) (iA hΔ hσ)
          (by simpa only [subst_tinst] using iI hΔ hσ) (ip hΔ hσ)
    | rawAtom hF iF =>
        intro Δ σ hΔ hσ
        exact .rawAtom (iF hΔ hσ)
    | rawApp hF hf ha iF iFterm ia =>
        intro Δ σ hΔ hσ
        exact .rawApp (iF hΔ hσ) (iFterm hΔ hσ) (ia hΔ hσ)
    | @piIntro Γ A B b hF hb hs iF ib =>
        intro Δ σ hΔ hσ
        have hF' := iF hΔ hσ
        change FormJ Δ (.pi (subst (σ) A) (subst (pup (σ)) B)) at hF'
        obtain ⟨hA', hB'⟩ := form_pi_inv hF'
        have hb' := ib (.ext hΔ hA') (hσ.lift hΔ hA')
        have hs' := scoped_subst (σ := σ) (m := Δ.length) hs
          (fun n hn => hσ.scope n hn)
        have ht : HasJ Δ (abstract (psub (pup (σ)) b))
            (.pi (subst (σ) A) (subst (pup (σ)) B)) :=
          HasJ.piIntro (FormJ.pi hA' hB')
            (by simpa only [] using hb')
            (by simpa only [abstraction_naturality] using hs')
        rw [abstraction_naturality] at ht
        exact ht
    | piElim hF hI hf ha iF iI iFterm ia =>
        intro Δ σ hΔ hσ
        simpa only [psub, subst_inst, subst] using
          HasJ.piElim (iF hΔ hσ)
            (by simpa only [subst_inst] using iI hΔ hσ)
            (iFterm hΔ hσ) (ia hΔ hσ)
    | sigmaIntro hF hI ha hb iF iI ia ib =>
        intro Δ σ hΔ hσ
        simpa only [P01DF.Syntactic.polynomial_pair, subst] using
          HasJ.sigmaIntro (iF hΔ hσ)
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
          HasJ.sigmaSnd (iF hΔ hσ)
            (by simpa only [subst_inst, P01DF.Syntactic.polynomial_fst] using
              iI hΔ hσ) (iz hΔ hσ)
    | identityIntro hF hp hq hc iF ip iq =>
        intro Δ σ hΔ hσ
        exact .identityIntro (iF hΔ hσ) (ip hΔ hσ)
          (iq hΔ hσ) (polyConvPlus_subst hc _)
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
        simp only [] at hB'
        simp only [subst, subst_motiveAt, psub] at hI' hD' hE' he' hd'
        simpa only [P01DF.Syntactic.polynomial_j, subst_motiveAt] using
          HasJ.j hA' hB' hI' hD' hE' hx' hy' he' hd'
    | conv hA hp hc hs iA ip =>
        intro Δ σ hΔ hσ
        exact .conv (iA hΔ hσ) (ip hΔ hσ)
          (polyConvPlus_subst hc _) (scoped_subst hs (fun n hn => hσ.scope n hn))

    | @piExt Γ A B p q h hA hB hPi hp hq hBody hFam hh hId sp sq sh sa sb iA iB iPi ip iq iBody iFam ih iId =>
        intro Δ σ hΔ hσ
        have hA' := iA hΔ hσ
        have hΔA := CtxJ.ext hΔ hA'
        have hB' := iB hΔA (hσ.lift hΔ hA')
        have hBody' := iBody hΔA (hσ.lift hΔ hA')
        have hFam' := iFam hΔ hσ
        have hh' := ih hΔ hσ
        have hId' := iId hΔ hσ
        simp only [subst, psub,
          P01DF.Syntactic.polynomial_shift_substitution] at hB' hBody' hFam' hh' hId'
        exact .piExt hA' hB' (iPi hΔ hσ) (ip hΔ hσ) (iq hΔ hσ)
          hBody' hFam' hh' hId'
          (scoped_subst sp (fun n hn => hσ.scope n hn))
          (scoped_subst sq (fun n hn => hσ.scope n hn))
          (scoped_subst sh (fun n hn => hσ.scope n hn))
          (tyScoped_subst sa (fun n hn => hσ.scope n hn))
          (tyScoped_subst sb (scopedSub_lift (fun n hn => hσ.scope n hn)))
    | @allExt Γ B p q h hB hAll hp hq hBody hh hId sp sq sh sb iB iAll ip iq iBody ih iId =>
        intro Δ σ hΔ hσ
        exact .allExt (iB (ctx_twk hΔ) hσ.twk) (iAll hΔ hσ)
          (ip hΔ hσ) (iq hΔ hσ) (iBody (ctx_twk hΔ) hσ.twk)
          (ih (ctx_twk hΔ) hσ.twk) (iId hΔ hσ)
          (scoped_subst sp (fun n hn => hσ.scope n hn))
          (scoped_subst sq (fun n hn => hσ.scope n hn))
          (scoped_subst sh (fun n hn => hσ.scope n hn))
          (tyScoped_subst sb (fun n hn => hσ.scope n hn))

    | @sigmaElim Γ A B P d z hΓ hA hB hP hd hz iΓ iA iB iP id iz =>
        intro Δ σ hΔ hσ
        have hA' := iA hΔ hσ
        have hΔA := CtxJ.ext hΔ hA'
        have sA := hσ.lift hΔ hA'
        have hB' := iB hΔA sA
        have hP' := iP (.ext hΔ (.sigma hA' hB')) (hσ.lift hΔ (.sigma hA' hB'))
        have hd' := id (.ext hΔA hB') (sA.lift hΔA hB')
        simp only [branchType_subst] at hd'
        simpa only [branchAt_subst, P01DF.Syntactic.polynomial_fst,
          P01DF.Syntactic.polynomial_snd, subst_inst] using
          HasJ.sigmaElim hΔ hA' hB' hP' hd' (iz hΔ hσ)
    | @natInduction Γ P p s hΓ hP hp hs iΓ iP ip is =>
        intro Δ σ hΔ hσ
        have hN : FormJ Δ (subst σ P01AC.EffectiveCompleteness.N) := by
          simpa only [P01AC.BooleanPrimitive.N_subst] using form_nat hΔ
        have hP' := iP (.ext hΔ hN) (hσ.lift hΔ hN)
        simp only [P01AC.BooleanPrimitive.N_subst] at hP'
        have hp' := ip hΔ hσ
        have hs' := is hΔ hσ
        simp only [subst_inst, zero_subst] at hp'
        simp only [dependentStepType_subst] at hs'
        simpa only [sectionPoly_subst, subst, P01AC.BooleanPrimitive.N_subst] using
          HasJ.natInduction hΔ hP' hp' hs'

#print axioms base_has_subst
#print axioms form_subst
#print axioms has_subst
end JointCompletion.Structural
