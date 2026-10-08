/- Syntactic term reindexing, with independent All lifting. -/
import AllStructuralBase
namespace P01AC
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

theorem lookup_trename_inv {Γ : Tel} {r : Nat → Nat} {n : Nat} {B : Ty}
    (h : Lookup (trenameTel r Γ) n B) : ∃ A, Lookup Γ n A ∧ trename r A = B := by
  induction Γ generalizing n B with
  | nil => cases h
  | cons A Γ ih =>
      cases h with
      | zero => exact ⟨wk A, .zero, trename_wk A r⟩
      | succ h =>
          obtain ⟨C, hc, he⟩ := ih h
          exact ⟨wk C, .succ hc, by rw [trename_wk, he]⟩

theorem Renaming.twk {Γ Δ : Tel} {r : Nat → Nat} (h : Renaming Γ Δ r) :
    Renaming (twkTel Γ) (twkTel Δ) r := by
  refine ⟨?_, ?_⟩
  · simpa only [twkTel, List.length_map] using h.scope
  · intro n B hb
    obtain ⟨A, ha, rfl⟩ := lookup_trename_inv hb
    simpa only [subst_trename] using lookup_trename (h.lookup ha) Nat.succ

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
    | @finite C Γ t υ hlen hυ hF ht iυ iF =>
        rename_i Δ r hΔ hr
        simpa only [psub, subst_finite_instance] using
          Has.finite (υ.map (subst (renSub r)))
            (by simpa only [List.length_map] using hlen)
            (fun n hn => by simpa only [typeImages_subst] using iυ n (by simpa only [List.length_map] using hn) hΔ hr)
            (by simpa only [subst_finite_instance] using iF hΔ hr) ht
    | allIntro hF hp iF ip =>
        rename_i Δ r hΔ hr
        exact .allIntro (iF hΔ hr) (ip (ctx_twk hΔ) hr.twk)
    | allElim hF hA hI hp iF iA iI ip =>
        rename_i Δ r hΔ hr
        simpa only [subst_tinst] using Has.allElim (iF hΔ hr) (iA hΔ hr)
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

theorem has_rename {Γ : Tel} {p : Poly} {A : Ty} (h : Has Γ p A)
    {Δ : Tel} {r : Nat → Nat} (hΔ : Ctx Δ) (hr : Renaming Γ Δ r) :
      Has Δ (psub (renSub r) p) (subst (renSub r) A) := by
  have hi := form_rename (Form.identity (has_form h) h h) hΔ hr
  cases hi with
  | identity _ hp _ => exact hp

theorem form_wk {Γ : Tel} {A B : Ty} (h : Form Γ A) (hΓ : Ctx Γ) (hB : Form Γ B) :
    Form (B :: Γ) (wk A) := form_rename h (.ext hΓ hB) (Renaming.weaken Γ B)

theorem has_wk {Γ : Tel} {p : Poly} {A B : Ty}
    (h : Has Γ p A) (hΓ : Ctx Γ) (hB : Form Γ B) :
    Has (B :: Γ) (pren Nat.succ p) (wk A) :=
  has_rename h (.ext hΓ hB) (Renaming.weaken Γ B)

theorem form_theta_head {Γ : Tel} {A : Ty} {x : Poly}
    (hΓ : Ctx Γ) (hA : Form Γ A) (hx : Has Γ x A) :
    Form (A :: Γ) (.identity (wk A) (pren Nat.succ x) (.var 0)) :=
  .identity (form_wk hA hΓ hA) (has_wk hx hΓ hA)
    (.var (form_wk hA hΓ hA) .zero)

theorem ctx_theta {Γ : Tel} {A : Ty} {x : Poly}
    (hΓ : Ctx Γ) (hA : Form Γ A) (hx : Has Γ x A) : Ctx (theta Γ A x) :=
  .ext (.ext hΓ hA) (form_theta_head hΓ hA hx)


end P01AC
