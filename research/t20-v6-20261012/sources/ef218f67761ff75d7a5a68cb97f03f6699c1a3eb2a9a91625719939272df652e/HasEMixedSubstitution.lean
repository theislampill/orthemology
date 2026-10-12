/- Actual-E port of the retained AllStructural mixed-substitution proof.
   Uses the unchanged syntax, actual mutual FormE/HasE recursor, and both
   extensionality rules; type images may depend on target term variables. -/
import DependentBranchApplication
namespace P01AC.ExtensionalRepair.Structural
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Actual-E formation controls every polynomial in a replacement type. -/
theorem form_scoped {Γ : Tel} {A : Ty} (h : FormE Γ A) : TyScoped Γ.length A := by
  induction h using FormE.rec
    (motive_1 := fun _ _ => True) (motive_3 := fun _ _ _ _ => True) with
  | all _ _ _ ih => simpa only [twkTel, List.length_map] using ih
  | pi _ _ ia ib => exact ⟨ia, ib⟩
  | sigma _ _ ia ib => exact ⟨ia, ib⟩
  | identity _ hp hq ia _ _ => exact ⟨ia, has_scoped hp, has_scoped hq⟩
  | _ => trivial

/-- A total-function interface for finite derivation induction. Type images
are actual-E formed; term images satisfy the actual dependent lookup types.
Finite type lists can supply the first field using inherited Bottom padding. -/
structure MixedSubstitution (Γ Δ : Tel) (σ : Nat → Poly) (τ : Nat → Ty) : Prop where
  types : ∀ n, FormE Δ (τ n)
  lookup : ∀ {n A}, Lookup Γ n A → HasE Δ (σ n) (mixed σ τ A)

theorem MixedSubstitution.scope {Γ Δ : Tel} {σ : Nat → Poly} {τ : Nat → Ty}
    (h : MixedSubstitution Γ Δ σ τ) : ScopedSub Γ.length Δ.length σ := by
  intro n hn
  obtain ⟨A, ha⟩ := lookup_exists Γ hn
  exact has_scoped (h.lookup ha)

theorem MixedSubstitution.lift {Γ Δ : Tel} {σ : Nat → Poly} {τ : Nat → Ty} {A : Ty}
    (h : MixedSubstitution Γ Δ σ τ) (hΔ : CtxE Δ) (hA : FormE Δ (mixed σ τ A)) :
    MixedSubstitution (A :: Γ) (mixed σ τ A :: Δ) (pup σ) (fun n => wk (τ n)) := by
  refine ⟨fun n => form_wk (h.types n) hΔ hA, ?_⟩
  intro n B hn
  cases hn with
  | zero =>
      simpa only [mixed_wk, pup] using HasE.var (form_wk hA hΔ hA)
        (Lookup.zero (A := mixed σ τ A) (Γ := Δ))
  | succ hn => simpa only [mixed_wk, pup] using has_wk (h.lookup hn) hΔ hA

theorem MixedSubstitution.twk {Γ Δ : Tel} {σ : Nat → Poly} {τ : Nat → Ty}
    (h : MixedSubstitution Γ Δ σ τ) (hΔ : CtxE Δ) :
    MixedSubstitution (twkTel Γ) (twkTel Δ) σ (tup τ) := by
  refine ⟨?_, ?_⟩
  · intro n
    cases n with
    | zero => exact .param (ctx_twk hΔ)
    | succ n => exact form_twk (h.types n)
  · intro n B hb
    obtain ⟨A, ha, rfl⟩ := lookup_trename_inv hb
    change HasE (twkTel Δ) (σ n) (mixed σ (tup τ) (P01AC.twk A))
    rw [mixed_twk]
    exact has_twk (h.lookup ha)

theorem mixed_theta_head (A : Ty) (x : Poly) (σ : Nat → Poly) (τ : Nat → Ty) :
    mixed (pup σ) (fun n => wk (τ n)) (.identity (wk A) (pren Nat.succ x) (.var 0)) =
      .identity (wk (mixed σ τ A)) (pren Nat.succ (psub σ x)) (.var 0) := by
  simp only [mixed, mixed_wk, P01DF.Syntactic.polynomial_shift_substitution, psub, pup]

theorem MixedSubstitution.theta {Γ Δ : Tel} {σ : Nat → Poly} {τ : Nat → Ty}
    {A : Ty} {x : Poly} (h : MixedSubstitution Γ Δ σ τ) (hΔ : CtxE Δ)
    (hA : FormE Δ (mixed σ τ A)) (hx : HasE Δ (psub σ x) (mixed σ τ A)) :
    MixedSubstitution (theta Γ A x) (theta Δ (mixed σ τ A) (psub σ x))
      (pup (pup σ)) (fun n => wk (wk (τ n))) := by
  have hhead : FormE (mixed σ τ A :: Δ)
      (mixed (pup σ) (fun n => wk (τ n)) (.identity (wk A) (pren Nat.succ x) (.var 0))) := by
    rw [mixed_theta_head]
    exact form_theta_head hΔ hA hx
  simpa only [theta, mixed_theta_head] using
    (h.lift hΔ hA).lift (.ext hΔ hA) hhead

theorem form_mixed {Γ : Tel} {A : Ty} (h : FormE Γ A) :
    ∀ {Δ : Tel} {σ : Nat → Poly} {τ : Nat → Ty}, CtxE Δ → MixedSubstitution Γ Δ σ τ → FormE Δ (mixed σ τ A) := by
  induction h using FormE.rec
    (motive_1 := fun _ _ => True)
    (motive_3 := fun Γ p A _ => ∀ {Δ : Tel} {σ : Nat → Poly} {τ : Nat → Ty},
      CtxE Δ → MixedSubstitution Γ Δ σ τ → HasE Δ (psub (σ) p) (mixed σ τ A)) with
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
        simpa only [mixed] using FormE.pi hA' hB'
    | sigma hA hB iA iB =>
        intro Δ σ τ hΔ hσ
        have hA' := iA hΔ hσ
        have hB' := iB (.ext hΔ hA') (hσ.lift hΔ hA')
        simpa only [mixed] using FormE.sigma hA' hB'
    | identity hA hp hq iA ip iq =>
        intro Δ σ τ hΔ hσ
        exact .identity (iA hΔ hσ) (ip hΔ hσ) (iq hΔ hσ)
    | var hA hn iA =>
        rename_i Δ σ τ hΔ hσ
        exact hσ.lookup hn
    | i hA hF iA iF =>
        rename_i Δ σ τ hΔ hσ
        simpa only [psub, mixed_arr] using
          HasE.i (iA hΔ hσ)
            (by simpa only [mixed_arr] using iF hΔ hσ)
    | k hA hB hF iA iB iF =>
        rename_i Δ σ τ hΔ hσ
        simpa only [psub, mixed_arr] using
          HasE.k (iA hΔ hσ) (iB hΔ hσ)
            (by simpa only [mixed_arr] using iF hΔ hσ)
    | s hA hB hC hF iA iB iC iF =>
        rename_i Δ σ τ hΔ hσ
        simpa only [psub, mixed_arr] using
          HasE.s (iA hΔ hσ) (iB hΔ hσ) (iC hΔ hσ)
            (by simpa only [mixed_arr] using iF hΔ hσ)
    | @finite C Γ t υ hlen hυ hF ht iυ iF =>
        rename_i Δ σ τ hΔ hσ
        simpa only [psub, mixed_finite_instance] using
          HasE.finite (υ.map (mixed σ τ))
            (by simpa only [List.length_map] using hlen)
            (fun n hn => by simpa only [typeImages_mixed] using iυ n (by simpa only [List.length_map] using hn) hΔ hσ)
            (by simpa only [mixed_finite_instance] using iF hΔ hσ) ht
    | allIntro hF hp iF ip =>
        rename_i Δ σ τ hΔ hσ
        exact .allIntro (iF hΔ hσ) (ip (ctx_twk hΔ) (hσ.twk hΔ))
    | allElim hF hA hI hp iF iA iI ip =>
        rename_i Δ σ τ hΔ hσ
        simpa only [mixed_tinst] using HasE.allElim (iF hΔ hσ) (iA hΔ hσ)
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
        change FormE Δ (.pi (mixed σ τ A) (mixed (pup σ) (fun n => wk (τ n)) B)) at hF'
        cases hF' with
        | pi hA' hB' =>
            have hb' := ib (.ext hΔ hA') (hσ.lift hΔ hA')
            have hs' := scoped_subst (σ := σ) (m := Δ.length) hs
              (fun n hn => hσ.scope n hn)
            have ht : HasE Δ (abstract (psub (pup (σ)) b))
                (.pi (mixed σ τ A) (mixed (pup σ) (fun n => wk (τ n)) B)) :=
              HasE.piIntro (FormE.pi hA' hB')
                (by simpa only [] using hb')
                (by simpa only [abstraction_naturality] using hs')
            rw [abstraction_naturality] at ht
            exact ht
    | piElim hF hI hf ha iF iI iFterm ia =>
        rename_i Δ σ τ hΔ hσ
        simpa only [psub, mixed_inst, mixed] using
          HasE.piElim (iF hΔ hσ)
            (by simpa only [mixed_inst] using iI hΔ hσ)
            (iFterm hΔ hσ) (ia hΔ hσ)
    | sigmaIntro hF hI ha hb iF iI ia ib =>
        rename_i Δ σ τ hΔ hσ
        simpa only [P01DF.Syntactic.polynomial_pair, mixed] using
          HasE.sigmaIntro (iF hΔ hσ)
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
          HasE.sigmaSnd (iF hΔ hσ)
            (by simpa only [mixed_inst, P01DF.Syntactic.polynomial_fst] using
              iI hΔ hσ) (iz hΔ hσ)
    | identityIntro hF hp hq hc iF ip iq =>
        rename_i Δ σ τ hΔ hσ
        exact .identityIntro (iF hΔ hσ) (ip hΔ hσ)
          (iq hΔ hσ) (polyConvPlus_subst hc _)
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
          HasE.j hA' hB' hI' hD' hE' hx' hy' he' hd'
    | conv hA hp hc hs iA ip =>
        rename_i Δ σ τ hΔ hσ
        exact .conv (iA hΔ hσ) (ip hΔ hσ)
          (polyConvPlus_subst hc _) (scoped_subst hs (fun n hn => hσ.scope n hn))

    | @piExt Γ A B p q h hA hB hPi hp hq hBody hFam hh hId sp sq sh sa sb iA iB iPi ip iq iBody iFam ih iId =>
        rename_i Δ σ τ hΔ hσ
        have hA' := iA hΔ hσ
        have hΔA := CtxE.ext hΔ hA'
        have hB' := iB hΔA (hσ.lift hΔ hA')
        have hBody' := iBody hΔA (hσ.lift hΔ hA')
        have hFam' := iFam hΔ hσ
        have hh' := ih hΔ hσ
        have hId' := iId hΔ hσ
        simp only [mixed, psub,
          P01DF.Syntactic.polynomial_shift_substitution] at hB' hBody' hFam' hh' hId'
        exact .piExt hA' hB' (iPi hΔ hσ) (ip hΔ hσ) (iq hΔ hσ)
          hBody' hFam' hh' hId'
          (scoped_subst sp (fun n hn => hσ.scope n hn))
          (scoped_subst sq (fun n hn => hσ.scope n hn))
          (scoped_subst sh (fun n hn => hσ.scope n hn))
          (tyScoped_mixed sa hσ.scope (fun n => form_scoped (hσ.types n)))
          (tyScoped_mixed sb (scopedSub_lift hσ.scope) (fun n => tyScoped_wk (form_scoped (hσ.types n))))
    | @allExt Γ B p q h hB hAll hp hq hBody hh hId sp sq sh sb iB iAll ip iq iBody ih iId =>
        rename_i Δ σ τ hΔ hσ
        exact .allExt (iB (ctx_twk hΔ) (hσ.twk hΔ)) (iAll hΔ hσ)
          (ip hΔ hσ) (iq hΔ hσ) (iBody (ctx_twk hΔ) (hσ.twk hΔ))
          (ih (ctx_twk hΔ) (hσ.twk hΔ)) (iId hΔ hσ)
          (scoped_subst sp (fun n hn => hσ.scope n hn))
          (scoped_subst sq (fun n hn => hσ.scope n hn))
          (scoped_subst sh (fun n hn => hσ.scope n hn))
          (tyScoped_mixed sb hσ.scope (tyScoped_tup (fun n => form_scoped (hσ.types n))))

theorem has_mixed {Γ : Tel} {p : Poly} {A : Ty} (h : HasE Γ p A)
    {Δ : Tel} {σ : Nat → Poly} {τ : Nat → Ty}
    (hΔ : CtxE Δ) (hσ : MixedSubstitution Γ Δ σ τ) :
    HasE Δ (psub σ p) (mixed σ τ A) := by
  have hi := form_mixed (FormE.identity (ClosedProofCanonicalisation.formed h) h h) hΔ hσ
  cases hi with
  | identity _ hp _ => exact hp


#print axioms form_mixed
#print axioms has_mixed
end P01AC.ExtensionalRepair.Structural
