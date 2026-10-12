import JointStructuralBasics
import JointTypeRenaming
import JointCompletionAlgebra
namespace JointCompletion.Structural
open P01AC P01D OrthemologyV2 OrthemologyV3 P01R
open P01F (cons)
open P01AC.ExtensionalRepair.Structural
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem base_form_rename {Γ : Tel} {A : Ty} (h : P01AC.ExtensionalRepair.FormE Γ A) :
    ∀ {Δ : Tel} {r : Nat → Nat}, CtxJ Δ → Renaming Γ Δ r → FormJ Δ (subst (renSub r) A) := by
  induction h using P01AC.ExtensionalRepair.FormE.rec
    (motive_1 := fun _ _ => True)
    (motive_3 := fun Γ p A _ => ∀ {Δ : Tel} {r : Nat → Nat},
      CtxJ Δ → Renaming Γ Δ r → HasJ Δ (psub (renSub r) p) (subst (renSub r) A)) with
    | nil => trivial
    | ext => trivial
    | param hΓ iΓ =>
        intro Δ r hΔ hr
        exact .param hΔ
    | bottom hΓ iΓ =>
        intro Δ r hΔ hr
        exact .bottom hΔ
    | all hΓ hB iΓ iB =>
        intro Δ r hΔ hr
        exact .all hΔ (iB (ctx_twk hΔ) hr.twk)
    | raw hΓ iΓ =>
        intro Δ r hΔ hr
        exact .raw hΔ
    | pi hA hB iA iB =>
        intro Δ r hΔ hr
        have hA' := iA hΔ hr
        have hB' := iB (.ext hΔ hA') (hr.lift _)
        simpa only [subst, renSub_lift] using FormJ.pi hA' hB'
    | sigma hA hB iA iB =>
        intro Δ r hΔ hr
        have hA' := iA hΔ hr
        have hB' := iB (.ext hΔ hA') (hr.lift _)
        simpa only [subst, renSub_lift] using FormJ.sigma hA' hB'
    | identity hA hp hq iA ip iq =>
        intro Δ r hΔ hr
        exact .identity (iA hΔ hr) (ip hΔ hr) (iq hΔ hr)
    | var hA hn iA =>
        rename_i Δ r hΔ hr
        exact .var (iA hΔ hr) (hr.lookup hn)
    | i hA hF iA iF =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_arr] using
          HasJ.i (iA hΔ hr)
            (by simpa only [subst_arr] using iF hΔ hr)
    | k hA hB hF iA iB iF =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_arr] using
          HasJ.k (iA hΔ hr) (iB hΔ hr)
            (by simpa only [subst_arr] using iF hΔ hr)
    | s hA hB hC hF iA iB iC iF =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_arr] using
          HasJ.s (iA hΔ hr) (iB hΔ hr) (iC hΔ hr)
            (by simpa only [subst_arr] using iF hΔ hr)
    | @finite C Γ t υ hlen hυ hF ht iυ iF =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_finite_instance] using
          HasJ.finite (υ.map (subst (renSub r)))
            (by simpa only [List.length_map] using hlen)
            (fun n hn => by simpa only [typeImages_subst] using iυ n (by simpa only [List.length_map] using hn) hΔ hr)
            (by simpa only [subst_finite_instance] using iF hΔ hr) ht
    | allIntro hF hp iF ip =>
        rename_i Δ r hΔ hr
        exact .allIntro (iF hΔ hr) (ip (ctx_twk hΔ) hr.twk)
    | allElim hF hA hI hp iF iA iI ip =>
        rename_i Δ r hΔ hr
        simpa only [subst_tinst] using HasJ.allElim (iF hΔ hr) (iA hΔ hr)
          (by simpa only [subst_tinst] using iI hΔ hr) (ip hΔ hr)
    | rawAtom hF iF =>
        rename_i Δ r hΔ hr
        exact .rawAtom (iF hΔ hr)
    | rawApp hF hf ha iF iFterm ia =>
        rename_i Δ r hΔ hr
        exact .rawApp (iF hΔ hr) (iFterm hΔ hr) (ia hΔ hr)
    | @piIntro Γ A B b hF hb hs iF ib =>
        rename_i Δ r hΔ hr
        have hF' := iF hΔ hr
        change FormJ Δ (.pi (subst (renSub r) A) (subst (pup (renSub r)) B)) at hF'
        obtain ⟨hA', hB'⟩ := form_pi_inv hF'
        have hb' := ib (.ext hΔ hA') (hr.lift A)
        have hs' := scoped_subst (σ := renSub r) (m := Δ.length) hs
          (fun n hn => hr.scope n hn)
        have ht : HasJ Δ (abstract (psub (pup (renSub r)) b))
            (.pi (subst (renSub r) A) (subst (pup (renSub r)) B)) :=
          HasJ.piIntro (FormJ.pi hA' hB')
            (by simpa only [renSub_lift] using hb')
            (by simpa only [abstraction_naturality] using hs')
        rw [abstraction_naturality] at ht
        exact ht
    | piElim hF hI hf ha iF iI iFterm ia =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_inst, subst] using
          HasJ.piElim (iF hΔ hr)
            (by simpa only [subst_inst] using iI hΔ hr)
            (iFterm hΔ hr) (ia hΔ hr)
    | sigmaIntro hF hI ha hb iF iI ia ib =>
        rename_i Δ r hΔ hr
        simpa only [P01DF.Syntactic.polynomial_pair, subst] using
          HasJ.sigmaIntro (iF hΔ hr)
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
          HasJ.sigmaSnd (iF hΔ hr)
            (by simpa only [subst_inst, P01DF.Syntactic.polynomial_fst] using
              iI hΔ hr) (iz hΔ hr)
    | identityIntro hF hp hq hc iF ip iq =>
        rename_i Δ r hΔ hr
        exact .identityIntro (iF hΔ hr) (ip hΔ hr)
          (iq hΔ hr) (polyConvPlus_subst hc _)
    | proofErase hR hI hp iR iI ip =>
        rename_i Δ r hΔ hr
        exact .proofErase (iR hΔ hr) (iI hΔ hr) (ip hΔ hr)
    | @j Γ A x B y e d hA hB hI hD hE hx hy he hd iA iB iI iD iE ix iy ie id =>
        rename_i Δ r hΔ hr
        have hA' := iA hΔ hr
        have hΔA : CtxJ (subst (renSub r) A :: Δ) := .ext hΔ hA'
        have hwA : FormJ (subst (renSub r) A :: Δ) (wk (subst (renSub r) A)) := by
          simpa only [subst_ren_shift] using
            iA hΔA (hr.comp (Renaming.weaken Δ (subst (renSub r) A)))
        have hwx : HasJ (subst (renSub r) A :: Δ)
            (pren Nat.succ (psub (renSub r) x)) (wk (subst (renSub r) A)) := by
          simpa only [subst_ren_shift, psub_ren_shift] using
            ix hΔA (hr.comp (Renaming.weaken Δ (subst (renSub r) A)))
        have hθ : CtxJ (theta Δ (subst (renSub r) A) (psub (renSub r) x)) :=
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
          HasJ.j hA' hB' hI' hD' hE' hx' hy' he' hd'
    | conv hA hp hc hs iA ip =>
        rename_i Δ r hΔ hr
        exact .conv (iA hΔ hr) (ip hΔ hr)
          (polyConvPlus_subst hc _) (scoped_subst hs (fun n hn => hr.scope n hn))

    | @piExt Γ A B p q h hA hB hPi hp hq hBody hFam hh hId sp sq sh sa sb iA iB iPi ip iq iBody iFam ih iId =>
        rename_i Δ r hΔ hr
        have hA' := iA hΔ hr
        have hΔA := CtxJ.ext hΔ hA'
        have hB' := iB hΔA (hr.lift A)
        have hBody' := iBody hΔA (hr.lift A)
        have hFam' := iFam hΔ hr
        have hh' := ih hΔ hr
        have hId' := iId hΔ hr
        simp only [renSub_lift, subst, psub,
          P01DF.Syntactic.polynomial_shift_substitution] at hB' hBody' hFam' hh' hId'
        exact .piExt hA' hB' (iPi hΔ hr) (ip hΔ hr) (iq hΔ hr)
          hBody' hFam' hh' hId'
          (scoped_subst sp (fun n hn => hr.scope n hn))
          (scoped_subst sq (fun n hn => hr.scope n hn))
          (scoped_subst sh (fun n hn => hr.scope n hn))
          (tyScoped_subst sa (fun n hn => hr.scope n hn))
          (tyScoped_subst sb (scopedSub_lift (fun n hn => hr.scope n hn)))
    | @allExt Γ B p q h hB hAll hp hq hBody hh hId sp sq sh sb iB iAll ip iq iBody ih iId =>
        rename_i Δ r hΔ hr
        exact .allExt (iB (ctx_twk hΔ) hr.twk) (iAll hΔ hr)
          (ip hΔ hr) (iq hΔ hr) (iBody (ctx_twk hΔ) hr.twk)
          (ih (ctx_twk hΔ) hr.twk) (iId hΔ hr)
          (scoped_subst sp (fun n hn => hr.scope n hn))
          (scoped_subst sq (fun n hn => hr.scope n hn))
          (scoped_subst sh (fun n hn => hr.scope n hn))
          (tyScoped_subst sb (fun n hn => hr.scope n hn))

theorem base_has_rename {Γ : Tel} {p : Poly} {A : Ty}
    (h : P01AC.ExtensionalRepair.HasE Γ p A)
    {Δ : Tel} {r : Nat → Nat} (hΔ : CtxJ Δ) (hr : Renaming Γ Δ r) :
      HasJ Δ (psub (renSub r) p) (subst (renSub r) A) := by
  have hi := base_form_rename
    (P01AC.ExtensionalRepair.FormE.identity
      (P01AC.ExtensionalRepair.ClosedProofCanonicalisation.formed h) h h) hΔ hr
  exact (form_identity_inv hi).2.1
theorem form_rename {Γ : Tel} {A : Ty} (h : FormJ Γ A) :
    ∀ {Δ : Tel} {r : Nat → Nat}, CtxJ Δ → Renaming Γ Δ r → FormJ Δ (subst (renSub r) A) := by
  induction h using FormJ.rec
    (motive_1 := fun _ _ => True)
    (motive_3 := fun Γ p A _ => ∀ {Δ : Tel} {r : Nat → Nat},
      CtxJ Δ → Renaming Γ Δ r → HasJ Δ (psub (renSub r) p) (subst (renSub r) A)) with
    | ctxBase h => trivial
    | formBase h => intro Δ r hΔ hr; exact base_form_rename h hΔ hr
    | hasBase h => rename_i Δ r hΔ hr; exact base_has_rename h hΔ hr
    | nil => trivial
    | ext => trivial
    | param hΓ iΓ =>
        intro Δ r hΔ hr
        exact .param hΔ
    | bottom hΓ iΓ =>
        intro Δ r hΔ hr
        exact .bottom hΔ
    | all hΓ hB iΓ iB =>
        intro Δ r hΔ hr
        exact .all hΔ (iB (ctx_twk hΔ) hr.twk)
    | raw hΓ iΓ =>
        intro Δ r hΔ hr
        exact .raw hΔ
    | pi hA hB iA iB =>
        intro Δ r hΔ hr
        have hA' := iA hΔ hr
        have hB' := iB (.ext hΔ hA') (hr.lift _)
        simpa only [subst, renSub_lift] using FormJ.pi hA' hB'
    | sigma hA hB iA iB =>
        intro Δ r hΔ hr
        have hA' := iA hΔ hr
        have hB' := iB (.ext hΔ hA') (hr.lift _)
        simpa only [subst, renSub_lift] using FormJ.sigma hA' hB'
    | identity hA hp hq iA ip iq =>
        intro Δ r hΔ hr
        exact .identity (iA hΔ hr) (ip hΔ hr) (iq hΔ hr)
    | var hA hn iA =>
        rename_i Δ r hΔ hr
        exact .var (iA hΔ hr) (hr.lookup hn)
    | i hA hF iA iF =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_arr] using
          HasJ.i (iA hΔ hr)
            (by simpa only [subst_arr] using iF hΔ hr)
    | k hA hB hF iA iB iF =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_arr] using
          HasJ.k (iA hΔ hr) (iB hΔ hr)
            (by simpa only [subst_arr] using iF hΔ hr)
    | s hA hB hC hF iA iB iC iF =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_arr] using
          HasJ.s (iA hΔ hr) (iB hΔ hr) (iC hΔ hr)
            (by simpa only [subst_arr] using iF hΔ hr)
    | @finite C Γ t υ hlen hυ hF ht iυ iF =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_finite_instance] using
          HasJ.finite (υ.map (subst (renSub r)))
            (by simpa only [List.length_map] using hlen)
            (fun n hn => by simpa only [typeImages_subst] using iυ n (by simpa only [List.length_map] using hn) hΔ hr)
            (by simpa only [subst_finite_instance] using iF hΔ hr) ht
    | allIntro hF hp iF ip =>
        rename_i Δ r hΔ hr
        exact .allIntro (iF hΔ hr) (ip (ctx_twk hΔ) hr.twk)
    | allElim hF hA hI hp iF iA iI ip =>
        rename_i Δ r hΔ hr
        simpa only [subst_tinst] using HasJ.allElim (iF hΔ hr) (iA hΔ hr)
          (by simpa only [subst_tinst] using iI hΔ hr) (ip hΔ hr)
    | rawAtom hF iF =>
        rename_i Δ r hΔ hr
        exact .rawAtom (iF hΔ hr)
    | rawApp hF hf ha iF iFterm ia =>
        rename_i Δ r hΔ hr
        exact .rawApp (iF hΔ hr) (iFterm hΔ hr) (ia hΔ hr)
    | @piIntro Γ A B b hF hb hs iF ib =>
        rename_i Δ r hΔ hr
        have hF' := iF hΔ hr
        change FormJ Δ (.pi (subst (renSub r) A) (subst (pup (renSub r)) B)) at hF'
        obtain ⟨hA', hB'⟩ := form_pi_inv hF'
        have hb' := ib (.ext hΔ hA') (hr.lift A)
        have hs' := scoped_subst (σ := renSub r) (m := Δ.length) hs
          (fun n hn => hr.scope n hn)
        have ht : HasJ Δ (abstract (psub (pup (renSub r)) b))
            (.pi (subst (renSub r) A) (subst (pup (renSub r)) B)) :=
          HasJ.piIntro (FormJ.pi hA' hB')
            (by simpa only [renSub_lift] using hb')
            (by simpa only [abstraction_naturality] using hs')
        rw [abstraction_naturality] at ht
        exact ht
    | piElim hF hI hf ha iF iI iFterm ia =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_inst, subst] using
          HasJ.piElim (iF hΔ hr)
            (by simpa only [subst_inst] using iI hΔ hr)
            (iFterm hΔ hr) (ia hΔ hr)
    | sigmaIntro hF hI ha hb iF iI ia ib =>
        rename_i Δ r hΔ hr
        simpa only [P01DF.Syntactic.polynomial_pair, subst] using
          HasJ.sigmaIntro (iF hΔ hr)
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
          HasJ.sigmaSnd (iF hΔ hr)
            (by simpa only [subst_inst, P01DF.Syntactic.polynomial_fst] using
              iI hΔ hr) (iz hΔ hr)
    | identityIntro hF hp hq hc iF ip iq =>
        rename_i Δ r hΔ hr
        exact .identityIntro (iF hΔ hr) (ip hΔ hr)
          (iq hΔ hr) (polyConvPlus_subst hc _)
    | proofErase hR hI hp iR iI ip =>
        rename_i Δ r hΔ hr
        exact .proofErase (iR hΔ hr) (iI hΔ hr) (ip hΔ hr)
    | @j Γ A x B y e d hA hB hI hD hE hx hy he hd iA iB iI iD iE ix iy ie id =>
        rename_i Δ r hΔ hr
        have hA' := iA hΔ hr
        have hΔA : CtxJ (subst (renSub r) A :: Δ) := .ext hΔ hA'
        have hwA : FormJ (subst (renSub r) A :: Δ) (wk (subst (renSub r) A)) := by
          simpa only [subst_ren_shift] using
            iA hΔA (hr.comp (Renaming.weaken Δ (subst (renSub r) A)))
        have hwx : HasJ (subst (renSub r) A :: Δ)
            (pren Nat.succ (psub (renSub r) x)) (wk (subst (renSub r) A)) := by
          simpa only [subst_ren_shift, psub_ren_shift] using
            ix hΔA (hr.comp (Renaming.weaken Δ (subst (renSub r) A)))
        have hθ : CtxJ (theta Δ (subst (renSub r) A) (psub (renSub r) x)) :=
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
          HasJ.j hA' hB' hI' hD' hE' hx' hy' he' hd'
    | conv hA hp hc hs iA ip =>
        rename_i Δ r hΔ hr
        exact .conv (iA hΔ hr) (ip hΔ hr)
          (polyConvPlus_subst hc _) (scoped_subst hs (fun n hn => hr.scope n hn))

    | @piExt Γ A B p q h hA hB hPi hp hq hBody hFam hh hId sp sq sh sa sb iA iB iPi ip iq iBody iFam ih iId =>
        rename_i Δ r hΔ hr
        have hA' := iA hΔ hr
        have hΔA := CtxJ.ext hΔ hA'
        have hB' := iB hΔA (hr.lift A)
        have hBody' := iBody hΔA (hr.lift A)
        have hFam' := iFam hΔ hr
        have hh' := ih hΔ hr
        have hId' := iId hΔ hr
        simp only [renSub_lift, subst, psub,
          P01DF.Syntactic.polynomial_shift_substitution] at hB' hBody' hFam' hh' hId'
        exact .piExt hA' hB' (iPi hΔ hr) (ip hΔ hr) (iq hΔ hr)
          hBody' hFam' hh' hId'
          (scoped_subst sp (fun n hn => hr.scope n hn))
          (scoped_subst sq (fun n hn => hr.scope n hn))
          (scoped_subst sh (fun n hn => hr.scope n hn))
          (tyScoped_subst sa (fun n hn => hr.scope n hn))
          (tyScoped_subst sb (scopedSub_lift (fun n hn => hr.scope n hn)))
    | @allExt Γ B p q h hB hAll hp hq hBody hh hId sp sq sh sb iB iAll ip iq iBody ih iId =>
        rename_i Δ r hΔ hr
        exact .allExt (iB (ctx_twk hΔ) hr.twk) (iAll hΔ hr)
          (ip hΔ hr) (iq hΔ hr) (iBody (ctx_twk hΔ) hr.twk)
          (ih (ctx_twk hΔ) hr.twk) (iId hΔ hr)
          (scoped_subst sp (fun n hn => hr.scope n hn))
          (scoped_subst sq (fun n hn => hr.scope n hn))
          (scoped_subst sh (fun n hn => hr.scope n hn))
          (tyScoped_subst sb (fun n hn => hr.scope n hn))

    | @sigmaElim Γ A B P d z hΓ hA hB hP hd hz iΓ iA iB iP id iz =>
        rename_i Δ r hΔ hr
        have hA' := iA hΔ hr
        have hB' := iB (.ext hΔ hA') (hr.lift A)
        simp only [renSub_lift] at hB'
        have hP' := iP (.ext hΔ (.sigma hA' hB')) (hr.lift (.sigma A B))
        have hr2 := (hr.lift A).lift B
        simp only [renSub_lift] at hr2
        have hd' := id (.ext (.ext hΔ hA') hB') hr2
        simp only [renSub_lift, branchType_subst] at hP' hd'
        simpa only [branchAt_subst, P01DF.Syntactic.polynomial_fst,
          P01DF.Syntactic.polynomial_snd, subst_inst] using
          HasJ.sigmaElim hΔ hA' hB' hP' hd' (iz hΔ hr)
    | @natInduction Γ P p s hΓ hP hp hs iΓ iP ip is =>
        rename_i Δ r hΔ hr
        have hP' := iP (.ext hΔ (form_nat hΔ)) (hr.lift P01AC.EffectiveCompleteness.N)
        simp only [renSub_lift] at hP'
        have hp' := ip hΔ hr
        have hs' := is hΔ hr
        simp only [subst_inst, zero_subst] at hp'
        simp only [dependentStepType_subst] at hs'
        simpa only [sectionPoly_subst, subst, P01AC.BooleanPrimitive.N_subst] using
          HasJ.natInduction hΔ hP' hp' hs'
theorem has_rename {Γ : Tel} {p : Poly} {A : Ty} (h : HasJ Γ p A) :
    ∀ {Δ : Tel} {r : Nat → Nat}, CtxJ Δ → Renaming Γ Δ r → HasJ Δ (psub (renSub r) p) (subst (renSub r) A) := by
  induction h using HasJ.rec
    (motive_1 := fun _ _ => True)
    (motive_2 := fun Γ A _ => ∀ {Δ : Tel} {r : Nat → Nat},
      CtxJ Δ → Renaming Γ Δ r → FormJ Δ (subst (renSub r) A)) with
    | ctxBase h => trivial
    | formBase h => rename_i Δ r hΔ hr; exact base_form_rename h hΔ hr
    | hasBase h => intro Δ r hΔ hr; exact base_has_rename h hΔ hr
    | nil => trivial
    | ext => trivial
    | param hΓ iΓ =>
        rename_i Δ r hΔ hr
        exact .param hΔ
    | bottom hΓ iΓ =>
        rename_i Δ r hΔ hr
        exact .bottom hΔ
    | all hΓ hB iΓ iB =>
        rename_i Δ r hΔ hr
        exact .all hΔ (iB (ctx_twk hΔ) hr.twk)
    | raw hΓ iΓ =>
        rename_i Δ r hΔ hr
        exact .raw hΔ
    | pi hA hB iA iB =>
        rename_i Δ r hΔ hr
        have hA' := iA hΔ hr
        have hB' := iB (.ext hΔ hA') (hr.lift _)
        simpa only [subst, renSub_lift] using FormJ.pi hA' hB'
    | sigma hA hB iA iB =>
        rename_i Δ r hΔ hr
        have hA' := iA hΔ hr
        have hB' := iB (.ext hΔ hA') (hr.lift _)
        simpa only [subst, renSub_lift] using FormJ.sigma hA' hB'
    | identity hA hp hq iA ip iq =>
        rename_i Δ r hΔ hr
        exact .identity (iA hΔ hr) (ip hΔ hr) (iq hΔ hr)
    | var hA hn iA =>
        intro Δ r hΔ hr
        exact .var (iA hΔ hr) (hr.lookup hn)
    | i hA hF iA iF =>
        intro Δ r hΔ hr
        simpa only [psub, subst_arr] using
          HasJ.i (iA hΔ hr)
            (by simpa only [subst_arr] using iF hΔ hr)
    | k hA hB hF iA iB iF =>
        intro Δ r hΔ hr
        simpa only [psub, subst_arr] using
          HasJ.k (iA hΔ hr) (iB hΔ hr)
            (by simpa only [subst_arr] using iF hΔ hr)
    | s hA hB hC hF iA iB iC iF =>
        intro Δ r hΔ hr
        simpa only [psub, subst_arr] using
          HasJ.s (iA hΔ hr) (iB hΔ hr) (iC hΔ hr)
            (by simpa only [subst_arr] using iF hΔ hr)
    | @finite C Γ t υ hlen hυ hF ht iυ iF =>
        intro Δ r hΔ hr
        simpa only [psub, subst_finite_instance] using
          HasJ.finite (υ.map (subst (renSub r)))
            (by simpa only [List.length_map] using hlen)
            (fun n hn => by simpa only [typeImages_subst] using iυ n (by simpa only [List.length_map] using hn) hΔ hr)
            (by simpa only [subst_finite_instance] using iF hΔ hr) ht
    | allIntro hF hp iF ip =>
        intro Δ r hΔ hr
        exact .allIntro (iF hΔ hr) (ip (ctx_twk hΔ) hr.twk)
    | allElim hF hA hI hp iF iA iI ip =>
        intro Δ r hΔ hr
        simpa only [subst_tinst] using HasJ.allElim (iF hΔ hr) (iA hΔ hr)
          (by simpa only [subst_tinst] using iI hΔ hr) (ip hΔ hr)
    | rawAtom hF iF =>
        intro Δ r hΔ hr
        exact .rawAtom (iF hΔ hr)
    | rawApp hF hf ha iF iFterm ia =>
        intro Δ r hΔ hr
        exact .rawApp (iF hΔ hr) (iFterm hΔ hr) (ia hΔ hr)
    | @piIntro Γ A B b hF hb hs iF ib =>
        intro Δ r hΔ hr
        have hF' := iF hΔ hr
        change FormJ Δ (.pi (subst (renSub r) A) (subst (pup (renSub r)) B)) at hF'
        obtain ⟨hA', hB'⟩ := form_pi_inv hF'
        have hb' := ib (.ext hΔ hA') (hr.lift A)
        have hs' := scoped_subst (σ := renSub r) (m := Δ.length) hs
          (fun n hn => hr.scope n hn)
        have ht : HasJ Δ (abstract (psub (pup (renSub r)) b))
            (.pi (subst (renSub r) A) (subst (pup (renSub r)) B)) :=
          HasJ.piIntro (FormJ.pi hA' hB')
            (by simpa only [renSub_lift] using hb')
            (by simpa only [abstraction_naturality] using hs')
        rw [abstraction_naturality] at ht
        exact ht
    | piElim hF hI hf ha iF iI iFterm ia =>
        intro Δ r hΔ hr
        simpa only [psub, subst_inst, subst] using
          HasJ.piElim (iF hΔ hr)
            (by simpa only [subst_inst] using iI hΔ hr)
            (iFterm hΔ hr) (ia hΔ hr)
    | sigmaIntro hF hI ha hb iF iI ia ib =>
        intro Δ r hΔ hr
        simpa only [P01DF.Syntactic.polynomial_pair, subst] using
          HasJ.sigmaIntro (iF hΔ hr)
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
          HasJ.sigmaSnd (iF hΔ hr)
            (by simpa only [subst_inst, P01DF.Syntactic.polynomial_fst] using
              iI hΔ hr) (iz hΔ hr)
    | identityIntro hF hp hq hc iF ip iq =>
        intro Δ r hΔ hr
        exact .identityIntro (iF hΔ hr) (ip hΔ hr)
          (iq hΔ hr) (polyConvPlus_subst hc _)
    | proofErase hR hI hp iR iI ip =>
        intro Δ r hΔ hr
        exact .proofErase (iR hΔ hr) (iI hΔ hr) (ip hΔ hr)
    | @j Γ A x B y e d hA hB hI hD hE hx hy he hd iA iB iI iD iE ix iy ie id =>
        intro Δ r hΔ hr
        have hA' := iA hΔ hr
        have hΔA : CtxJ (subst (renSub r) A :: Δ) := .ext hΔ hA'
        have hwA : FormJ (subst (renSub r) A :: Δ) (wk (subst (renSub r) A)) := by
          simpa only [subst_ren_shift] using
            iA hΔA (hr.comp (Renaming.weaken Δ (subst (renSub r) A)))
        have hwx : HasJ (subst (renSub r) A :: Δ)
            (pren Nat.succ (psub (renSub r) x)) (wk (subst (renSub r) A)) := by
          simpa only [subst_ren_shift, psub_ren_shift] using
            ix hΔA (hr.comp (Renaming.weaken Δ (subst (renSub r) A)))
        have hθ : CtxJ (theta Δ (subst (renSub r) A) (psub (renSub r) x)) :=
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
          HasJ.j hA' hB' hI' hD' hE' hx' hy' he' hd'
    | conv hA hp hc hs iA ip =>
        intro Δ r hΔ hr
        exact .conv (iA hΔ hr) (ip hΔ hr)
          (polyConvPlus_subst hc _) (scoped_subst hs (fun n hn => hr.scope n hn))

    | @piExt Γ A B p q h hA hB hPi hp hq hBody hFam hh hId sp sq sh sa sb iA iB iPi ip iq iBody iFam ih iId =>
        intro Δ r hΔ hr
        have hA' := iA hΔ hr
        have hΔA := CtxJ.ext hΔ hA'
        have hB' := iB hΔA (hr.lift A)
        have hBody' := iBody hΔA (hr.lift A)
        have hFam' := iFam hΔ hr
        have hh' := ih hΔ hr
        have hId' := iId hΔ hr
        simp only [renSub_lift, subst, psub,
          P01DF.Syntactic.polynomial_shift_substitution] at hB' hBody' hFam' hh' hId'
        exact .piExt hA' hB' (iPi hΔ hr) (ip hΔ hr) (iq hΔ hr)
          hBody' hFam' hh' hId'
          (scoped_subst sp (fun n hn => hr.scope n hn))
          (scoped_subst sq (fun n hn => hr.scope n hn))
          (scoped_subst sh (fun n hn => hr.scope n hn))
          (tyScoped_subst sa (fun n hn => hr.scope n hn))
          (tyScoped_subst sb (scopedSub_lift (fun n hn => hr.scope n hn)))
    | @allExt Γ B p q h hB hAll hp hq hBody hh hId sp sq sh sb iB iAll ip iq iBody ih iId =>
        intro Δ r hΔ hr
        exact .allExt (iB (ctx_twk hΔ) hr.twk) (iAll hΔ hr)
          (ip hΔ hr) (iq hΔ hr) (iBody (ctx_twk hΔ) hr.twk)
          (ih (ctx_twk hΔ) hr.twk) (iId hΔ hr)
          (scoped_subst sp (fun n hn => hr.scope n hn))
          (scoped_subst sq (fun n hn => hr.scope n hn))
          (scoped_subst sh (fun n hn => hr.scope n hn))
          (tyScoped_subst sb (fun n hn => hr.scope n hn))

    | @sigmaElim Γ A B P d z hΓ hA hB hP hd hz iΓ iA iB iP id iz =>
        intro Δ r hΔ hr
        have hA' := iA hΔ hr
        have hB' := iB (.ext hΔ hA') (hr.lift A)
        simp only [renSub_lift] at hB'
        have hP' := iP (.ext hΔ (.sigma hA' hB')) (hr.lift (.sigma A B))
        have hr2 := (hr.lift A).lift B
        simp only [renSub_lift] at hr2
        have hd' := id (.ext (.ext hΔ hA') hB') hr2
        simp only [renSub_lift, branchType_subst] at hP' hd'
        simpa only [branchAt_subst, P01DF.Syntactic.polynomial_fst,
          P01DF.Syntactic.polynomial_snd, subst_inst] using
          HasJ.sigmaElim hΔ hA' hB' hP' hd' (iz hΔ hr)
    | @natInduction Γ P p s hΓ hP hp hs iΓ iP ip is =>
        intro Δ r hΔ hr
        have hP' := iP (.ext hΔ (form_nat hΔ)) (hr.lift P01AC.EffectiveCompleteness.N)
        simp only [renSub_lift] at hP'
        have hp' := ip hΔ hr
        have hs' := is hΔ hr
        simp only [subst_inst, zero_subst] at hp'
        simp only [dependentStepType_subst] at hs'
        simpa only [sectionPoly_subst, subst, P01AC.BooleanPrimitive.N_subst] using
          HasJ.natInduction hΔ hP' hp' hs'

theorem form_wk {Γ : Tel} {A B : Ty} (h : FormJ Γ A) (hΓ : CtxJ Γ) (hB : FormJ Γ B) :
    FormJ (B :: Γ) (wk A) := form_rename h (.ext hΓ hB) (Renaming.weaken Γ B)

theorem has_wk {Γ : Tel} {p : Poly} {A B : Ty}
    (h : HasJ Γ p A) (hΓ : CtxJ Γ) (hB : FormJ Γ B) :
    HasJ (B :: Γ) (pren Nat.succ p) (wk A) :=
  has_rename h (.ext hΓ hB) (Renaming.weaken Γ B)

#print axioms form_rename
#print axioms has_rename
end JointCompletion.Structural
