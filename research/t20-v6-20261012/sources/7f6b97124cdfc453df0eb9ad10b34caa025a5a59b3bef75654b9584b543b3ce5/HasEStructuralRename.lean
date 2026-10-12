/- Full actual-HasE renaming, including every piExt and allExt premise. -/
import HasEStructuralBase
namespace P01AC.ExtensionalRepair.Structural
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)
open P01AC.Intensional.Plus (PolyConvPlus)
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

/-- Literal polynomial substitution preserves all eight source conversion rules. -/
theorem polyConvPlus_subst {p q : Poly} (h : PolyConvPlus p q) (σ : Nat → Poly) :
    PolyConvPlus (psub σ p) (psub σ q) := by
  induction h with
  | refl => exact .refl _
  | symm h ih => exact ih.symm
  | trans h k ih ik => exact ih.trans ik
  | app h k ih ik => exact .app ih ik
  | i p => exact .i _
  | k p q => exact .k _ _
  | s p q r => exact .s _ _ _
  | bridge r t => exact .bridge r t

theorem form_rename {Γ : Tel} {A : Ty} (h : FormE Γ A) :
    ∀ {Δ : Tel} {r : Nat → Nat}, CtxE Δ → Renaming Γ Δ r → FormE Δ (subst (renSub r) A) := by
  induction h using FormE.rec
    (motive_1 := fun _ _ => True)
    (motive_3 := fun Γ p A _ => ∀ {Δ : Tel} {r : Nat → Nat},
      CtxE Δ → Renaming Γ Δ r → HasE Δ (psub (renSub r) p) (subst (renSub r) A)) with
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
        simpa only [subst, renSub_lift] using FormE.pi hA' hB'
    | sigma hA hB iA iB =>
        intro Δ r hΔ hr
        have hA' := iA hΔ hr
        have hB' := iB (.ext hΔ hA') (hr.lift _)
        simpa only [subst, renSub_lift] using FormE.sigma hA' hB'
    | identity hA hp hq iA ip iq =>
        intro Δ r hΔ hr
        exact .identity (iA hΔ hr) (ip hΔ hr) (iq hΔ hr)
    | var hA hn iA =>
        rename_i Δ r hΔ hr
        exact .var (iA hΔ hr) (hr.lookup hn)
    | i hA hF iA iF =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_arr] using
          HasE.i (iA hΔ hr)
            (by simpa only [subst_arr] using iF hΔ hr)
    | k hA hB hF iA iB iF =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_arr] using
          HasE.k (iA hΔ hr) (iB hΔ hr)
            (by simpa only [subst_arr] using iF hΔ hr)
    | s hA hB hC hF iA iB iC iF =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_arr] using
          HasE.s (iA hΔ hr) (iB hΔ hr) (iC hΔ hr)
            (by simpa only [subst_arr] using iF hΔ hr)
    | @finite C Γ t υ hlen hυ hF ht iυ iF =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_finite_instance] using
          HasE.finite (υ.map (subst (renSub r)))
            (by simpa only [List.length_map] using hlen)
            (fun n hn => by simpa only [typeImages_subst] using iυ n (by simpa only [List.length_map] using hn) hΔ hr)
            (by simpa only [subst_finite_instance] using iF hΔ hr) ht
    | allIntro hF hp iF ip =>
        rename_i Δ r hΔ hr
        exact .allIntro (iF hΔ hr) (ip (ctx_twk hΔ) hr.twk)
    | allElim hF hA hI hp iF iA iI ip =>
        rename_i Δ r hΔ hr
        simpa only [subst_tinst] using HasE.allElim (iF hΔ hr) (iA hΔ hr)
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
        change FormE Δ (.pi (subst (renSub r) A) (subst (pup (renSub r)) B)) at hF'
        cases hF' with
        | pi hA' hB' =>
            have hb' := ib (.ext hΔ hA') (hr.lift A)
            have hs' := scoped_subst (σ := renSub r) (m := Δ.length) hs
              (fun n hn => hr.scope n hn)
            have ht : HasE Δ (abstract (psub (pup (renSub r)) b))
                (.pi (subst (renSub r) A) (subst (pup (renSub r)) B)) :=
              HasE.piIntro (FormE.pi hA' hB')
                (by simpa only [renSub_lift] using hb')
                (by simpa only [abstraction_naturality] using hs')
            rw [abstraction_naturality] at ht
            exact ht
    | piElim hF hI hf ha iF iI iFterm ia =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_inst, subst] using
          HasE.piElim (iF hΔ hr)
            (by simpa only [subst_inst] using iI hΔ hr)
            (iFterm hΔ hr) (ia hΔ hr)
    | sigmaIntro hF hI ha hb iF iI ia ib =>
        rename_i Δ r hΔ hr
        simpa only [P01DF.Syntactic.polynomial_pair, subst] using
          HasE.sigmaIntro (iF hΔ hr)
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
          HasE.sigmaSnd (iF hΔ hr)
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
        have hΔA : CtxE (subst (renSub r) A :: Δ) := .ext hΔ hA'
        have hwA : FormE (subst (renSub r) A :: Δ) (wk (subst (renSub r) A)) := by
          simpa only [subst_ren_shift] using
            iA hΔA (hr.comp (Renaming.weaken Δ (subst (renSub r) A)))
        have hwx : HasE (subst (renSub r) A :: Δ)
            (pren Nat.succ (psub (renSub r) x)) (wk (subst (renSub r) A)) := by
          simpa only [subst_ren_shift, psub_ren_shift] using
            ix hΔA (hr.comp (Renaming.weaken Δ (subst (renSub r) A)))
        have hθ : CtxE (theta Δ (subst (renSub r) A) (psub (renSub r) x)) :=
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
          HasE.j hA' hB' hI' hD' hE' hx' hy' he' hd'
    | conv hA hp hc hs iA ip =>
        rename_i Δ r hΔ hr
        exact .conv (iA hΔ hr) (ip hΔ hr)
          (polyConvPlus_subst hc _) (scoped_subst hs (fun n hn => hr.scope n hn))

    | @piExt Γ A B p q h hA hB hPi hp hq hBody hFam hh hId sp sq sh sa sb iA iB iPi ip iq iBody iFam ih iId =>
        rename_i Δ r hΔ hr
        have hA' := iA hΔ hr
        have hΔA := CtxE.ext hΔ hA'
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

theorem has_rename {Γ : Tel} {p : Poly} {A : Ty} (h : HasE Γ p A)
    {Δ : Tel} {r : Nat → Nat} (hΔ : CtxE Δ) (hr : Renaming Γ Δ r) :
      HasE Δ (psub (renSub r) p) (subst (renSub r) A) := by
  have hi := form_rename (FormE.identity (ClosedProofCanonicalisation.formed h) h h) hΔ hr
  cases hi with
  | identity _ hp _ => exact hp

theorem form_wk {Γ : Tel} {A B : Ty} (h : FormE Γ A) (hΓ : CtxE Γ) (hB : FormE Γ B) :
    FormE (B :: Γ) (wk A) := form_rename h (.ext hΓ hB) (Renaming.weaken Γ B)

theorem has_wk {Γ : Tel} {p : Poly} {A B : Ty}
    (h : HasE Γ p A) (hΓ : CtxE Γ) (hB : FormE Γ B) :
    HasE (B :: Γ) (pren Nat.succ p) (wk A) :=
  has_rename h (.ext hΓ hB) (Renaming.weaken Γ B)


#print axioms form_rename
#print axioms has_rename
#print axioms has_wk
end P01AC.ExtensionalRepair.Structural
