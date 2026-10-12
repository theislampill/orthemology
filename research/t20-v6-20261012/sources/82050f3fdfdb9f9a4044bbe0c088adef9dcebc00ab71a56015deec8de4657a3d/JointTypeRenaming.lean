/- Type-parameter renaming for the exact frozen joint-completion grammar.
    This additive port uses actual syntactic derivations throughout. -/
import JointSyntax
import JointStructuralBasics
import JointCompletionAlgebra
import HasEStructuralBase
namespace JointCompletion.Structural
open P01AC P01D OrthemologyV2 OrthemologyV3 P01R
open P01AC.ExtensionalRepair.Structural
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

theorem form_trename {Γ : Tel} {A : Ty} (h : FormJ Γ A) :
    ∀ r : Nat → Nat, FormJ (trenameTel r Γ) (trename r A) := by
  induction h using FormJ.rec
    (motive_1 := fun Γ _ => ∀ r, CtxJ (trenameTel r Γ))
    (motive_3 := fun Γ p A _ => ∀ r, HasJ (trenameTel r Γ) p (trename r A)) with
  | ctxBase he => rename_i r; exact .ctxBase (P01AC.ExtensionalRepair.Structural.ctx_trename he r)
  | formBase he => intro r; exact .formBase (P01AC.ExtensionalRepair.Structural.form_trename he r)
  | hasBase he => rename_i r; exact .hasBase (P01AC.ExtensionalRepair.Structural.has_trename he r)
  | nil => rename_i r; exact .nil
  | ext hΓ hA iΓ iA => rename_i r; exact .ext (iΓ r) (iA r)
  | param hΓ iΓ => intro r; exact .param (iΓ r)
  | bottom hΓ iΓ => intro r; exact .bottom (iΓ r)
  | raw hΓ iΓ => intro r; exact .raw (iΓ r)
  | all hΓ hB iΓ iB =>
      intro r
      exact .all (iΓ r) (by simpa only [trenameTel_twk] using iB (liftRen r))
  | pi hA hB iA iB => intro r; exact .pi (iA r) (iB r)
  | sigma hA hB iA iB => intro r; exact .sigma (iA r) (iB r)
  | identity hA hp hq iA ip iq => intro r; exact .identity (iA r) (ip r) (iq r)
  | var hA hn iA => rename_i r; exact .var (iA r) (lookup_trename hn r)
  | i hA hF iA iF =>
      rename_i r
      simpa only [trename_arr] using HasJ.i (iA r) (by simpa only [trename_arr] using iF r)
  | k hA hB hF iA iB iF =>
      rename_i r
      simpa only [trename_arr] using HasJ.k (iA r) (iB r) (by simpa only [trename_arr] using iF r)
  | s hA hB hC hF iA iB iC iF =>
      rename_i r
      simpa only [trename_arr] using HasJ.s (iA r) (iB r) (iC r) (by simpa only [trename_arr] using iF r)
  | @finite C Γ t υ hlen hυ hF ht iυ iF =>
      rename_i r
      simpa only [trename_finite_instance] using
        HasJ.finite (υ.map (trename r)) (by simpa only [List.length_map] using hlen)
          (fun n hn => by simpa only [typeImages_trename] using iυ n (by simpa only [List.length_map] using hn) r)
          (by simpa only [trename_finite_instance] using iF r) ht
  | allIntro hF hp iF ip =>
      rename_i r
      exact .allIntro (iF r) (by simpa only [trenameTel_twk] using ip (liftRen r))
  | allElim hF hA hI hp iF iA iI ip =>
      rename_i r
      simpa only [trename_tinst] using HasJ.allElim (iF r) (iA r)
        (by simpa only [trename_tinst] using iI r) (ip r)
  | rawAtom hF iF => rename_i r; exact .rawAtom (iF r)
  | rawApp hF hf ha iF iff ia => rename_i r; exact .rawApp (iF r) (iff r) (ia r)
  | piIntro hF hb hs iF ib =>
      rename_i r
      exact .piIntro (iF r) (ib r) (by simpa only [trenameTel, List.length_map] using hs)
  | piElim hF hI hf ha iF iI iff ia =>
      rename_i r
      simpa only [trename_inst] using HasJ.piElim (iF r)
        (by simpa only [trename_inst] using iI r) (iff r) (ia r)
  | sigmaIntro hF hI ha hb iF iI ia ib =>
      rename_i r
      simpa only [trename_inst] using HasJ.sigmaIntro (iF r)
        (by simpa only [trename_inst] using iI r) (ia r)
        (by simpa only [trename_inst] using ib r)
  | sigmaFst hA hF hz iA iF iz => rename_i r; exact .sigmaFst (iA r) (iF r) (iz r)
  | sigmaSnd hF hI hz iF iI iz =>
      rename_i r
      simpa only [trename_inst] using HasJ.sigmaSnd (iF r)
        (by simpa only [trename_inst] using iI r) (iz r)
  | identityIntro hF hp hq hc iF ip iq => rename_i r; exact .identityIntro (iF r) (ip r) (iq r) hc
  | proofErase hR hI hp iR iI ip => rename_i r; exact .proofErase (iR r) (iI r) (ip r)
  | j hA hB hI hD hE hx hy he hd iA iB iI iD iE ix iy ie id =>
      rename_i r
      simpa only [trename_motiveAt] using HasJ.j (iA r)
        (by simpa only [trenameTel_theta] using iB r)
        (iI r) (by simpa only [trename_motiveAt] using iD r)
        (by simpa only [trename_motiveAt] using iE r)
        (ix r) (iy r) (ie r) (by simpa only [trename_motiveAt] using id r)
  | conv hA hp hc hs iA ip =>
      rename_i r
      exact .conv (iA r) (ip r) hc (by simpa only [trenameTel, List.length_map] using hs)

  | piExt hA hB hPi hp hq hBody hFam hh hId sp sq sh sa sb iA iB iPi ip iq iBody iFam ih iId =>
      rename_i r
      exact .piExt (iA r) (iB r) (iPi r) (ip r) (iq r)
        (iBody r) (iFam r) (ih r) (iId r)
        (by simpa only [trenameTel, List.length_map] using sp)
        (by simpa only [trenameTel, List.length_map] using sq)
        (by simpa only [trenameTel, List.length_map] using sh)
        (by simpa only [trenameTel, List.length_map] using tyScoped_trename sa r)
        (by simpa only [trenameTel, List.length_map] using tyScoped_trename sb r)
  | allExt hB hAll hp hq hBody hh hId sp sq sh sb iB iAll ip iq iBody ih iId =>
      rename_i r
      exact .allExt
        (by simpa only [trenameTel_twk] using iB (liftRen r))
        (iAll r) (ip r) (iq r)
        (by simpa only [trenameTel_twk] using iBody (liftRen r))
        (by simpa only [trenameTel_twk] using ih (liftRen r)) (iId r)
        (by simpa only [trenameTel, List.length_map] using sp)
        (by simpa only [trenameTel, List.length_map] using sq)
        (by simpa only [trenameTel, List.length_map] using sh)
        (by simpa only [trenameTel, List.length_map] using tyScoped_trename sb (liftRen r))

  | sigmaElim hc hA hB hP hd hz ic iA iB iP id iz =>
      rename_i r
      simpa only [trename_inst] using HasJ.sigmaElim (ic r) (iA r) (iB r) (iP r)
        (by simpa only [trename_branchType] using id r) (iz r)
  | natInduction hc hP hp hs ic iP ip iss =>
      rename_i r
      simpa only [trename, trename_N] using HasJ.natInduction (ic r)
        (by simpa only [trenameTel, List.map_cons, trename_N] using iP r)
        (by simpa only [trename_inst] using ip r)
        (by simpa only [trename_dependentStepType] using iss r)

theorem has_trename {Γ : Tel} {p : Poly} {A : Ty} (h : HasJ Γ p A) :
    ∀ r : Nat → Nat, HasJ (trenameTel r Γ) p (trename r A) := by
  induction h using HasJ.rec
    (motive_1 := fun Γ _ => ∀ r, CtxJ (trenameTel r Γ))
    (motive_2 := fun Γ A _ => ∀ r, FormJ (trenameTel r Γ) (trename r A)) with
  | ctxBase he => rename_i r; exact .ctxBase (P01AC.ExtensionalRepair.Structural.ctx_trename he r)
  | formBase he => rename_i r; exact .formBase (P01AC.ExtensionalRepair.Structural.form_trename he r)
  | hasBase he => intro r; exact .hasBase (P01AC.ExtensionalRepair.Structural.has_trename he r)
  | nil => rename_i r; exact .nil
  | ext hΓ hA iΓ iA => rename_i r; exact .ext (iΓ r) (iA r)
  | param hΓ iΓ => rename_i r; exact .param (iΓ r)
  | bottom hΓ iΓ => rename_i r; exact .bottom (iΓ r)
  | raw hΓ iΓ => rename_i r; exact .raw (iΓ r)
  | all hΓ hB iΓ iB =>
      rename_i r
      exact .all (iΓ r) (by simpa only [trenameTel_twk] using iB (liftRen r))
  | pi hA hB iA iB => rename_i r; exact .pi (iA r) (iB r)
  | sigma hA hB iA iB => rename_i r; exact .sigma (iA r) (iB r)
  | identity hA hp hq iA ip iq => rename_i r; exact .identity (iA r) (ip r) (iq r)
  | var hA hn iA => intro r; exact .var (iA r) (lookup_trename hn r)
  | i hA hF iA iF =>
      intro r
      simpa only [trename_arr] using HasJ.i (iA r) (by simpa only [trename_arr] using iF r)
  | k hA hB hF iA iB iF =>
      intro r
      simpa only [trename_arr] using HasJ.k (iA r) (iB r) (by simpa only [trename_arr] using iF r)
  | s hA hB hC hF iA iB iC iF =>
      intro r
      simpa only [trename_arr] using HasJ.s (iA r) (iB r) (iC r) (by simpa only [trename_arr] using iF r)
  | @finite C Γ t υ hlen hυ hF ht iυ iF =>
      intro r
      simpa only [trename_finite_instance] using
        HasJ.finite (υ.map (trename r)) (by simpa only [List.length_map] using hlen)
          (fun n hn => by simpa only [typeImages_trename] using iυ n (by simpa only [List.length_map] using hn) r)
          (by simpa only [trename_finite_instance] using iF r) ht
  | allIntro hF hp iF ip =>
      intro r
      exact .allIntro (iF r) (by simpa only [trenameTel_twk] using ip (liftRen r))
  | allElim hF hA hI hp iF iA iI ip =>
      intro r
      simpa only [trename_tinst] using HasJ.allElim (iF r) (iA r)
        (by simpa only [trename_tinst] using iI r) (ip r)
  | rawAtom hF iF => intro r; exact .rawAtom (iF r)
  | rawApp hF hf ha iF iff ia => intro r; exact .rawApp (iF r) (iff r) (ia r)
  | piIntro hF hb hs iF ib =>
      intro r
      exact .piIntro (iF r) (ib r) (by simpa only [trenameTel, List.length_map] using hs)
  | piElim hF hI hf ha iF iI iff ia =>
      intro r
      simpa only [trename_inst] using HasJ.piElim (iF r)
        (by simpa only [trename_inst] using iI r) (iff r) (ia r)
  | sigmaIntro hF hI ha hb iF iI ia ib =>
      intro r
      simpa only [trename_inst] using HasJ.sigmaIntro (iF r)
        (by simpa only [trename_inst] using iI r) (ia r)
        (by simpa only [trename_inst] using ib r)
  | sigmaFst hA hF hz iA iF iz => intro r; exact .sigmaFst (iA r) (iF r) (iz r)
  | sigmaSnd hF hI hz iF iI iz =>
      intro r
      simpa only [trename_inst] using HasJ.sigmaSnd (iF r)
        (by simpa only [trename_inst] using iI r) (iz r)
  | identityIntro hF hp hq hc iF ip iq => intro r; exact .identityIntro (iF r) (ip r) (iq r) hc
  | proofErase hR hI hp iR iI ip => intro r; exact .proofErase (iR r) (iI r) (ip r)
  | j hA hB hI hD hE hx hy he hd iA iB iI iD iE ix iy ie id =>
      intro r
      simpa only [trename_motiveAt] using HasJ.j (iA r)
        (by simpa only [trenameTel_theta] using iB r)
        (iI r) (by simpa only [trename_motiveAt] using iD r)
        (by simpa only [trename_motiveAt] using iE r)
        (ix r) (iy r) (ie r) (by simpa only [trename_motiveAt] using id r)
  | conv hA hp hc hs iA ip =>
      intro r
      exact .conv (iA r) (ip r) hc (by simpa only [trenameTel, List.length_map] using hs)

  | piExt hA hB hPi hp hq hBody hFam hh hId sp sq sh sa sb iA iB iPi ip iq iBody iFam ih iId =>
      intro r
      exact .piExt (iA r) (iB r) (iPi r) (ip r) (iq r)
        (iBody r) (iFam r) (ih r) (iId r)
        (by simpa only [trenameTel, List.length_map] using sp)
        (by simpa only [trenameTel, List.length_map] using sq)
        (by simpa only [trenameTel, List.length_map] using sh)
        (by simpa only [trenameTel, List.length_map] using tyScoped_trename sa r)
        (by simpa only [trenameTel, List.length_map] using tyScoped_trename sb r)
  | allExt hB hAll hp hq hBody hh hId sp sq sh sb iB iAll ip iq iBody ih iId =>
      intro r
      exact .allExt
        (by simpa only [trenameTel_twk] using iB (liftRen r))
        (iAll r) (ip r) (iq r)
        (by simpa only [trenameTel_twk] using iBody (liftRen r))
        (by simpa only [trenameTel_twk] using ih (liftRen r)) (iId r)
        (by simpa only [trenameTel, List.length_map] using sp)
        (by simpa only [trenameTel, List.length_map] using sq)
        (by simpa only [trenameTel, List.length_map] using sh)
        (by simpa only [trenameTel, List.length_map] using tyScoped_trename sb (liftRen r))

  | sigmaElim hc hA hB hP hd hz ic iA iB iP id iz =>
      intro r
      simpa only [trename_inst] using HasJ.sigmaElim (ic r) (iA r) (iB r) (iP r)
        (by simpa only [trename_branchType] using id r) (iz r)
  | natInduction hc hP hp hs ic iP ip iss =>
      intro r
      simpa only [trename, trename_N] using HasJ.natInduction (ic r)
        (by simpa only [trenameTel, List.map_cons, trename_N] using iP r)
        (by simpa only [trename_inst] using ip r)
        (by simpa only [trename_dependentStepType] using iss r)

theorem ctx_trename {Γ : Tel} (h : CtxJ Γ) (r : Nat → Nat) : CtxJ (trenameTel r Γ) :=
  form_ctx (form_trename (FormJ.bottom h) r)

theorem ctx_twk {Γ : Tel} (h : CtxJ Γ) : CtxJ (twkTel Γ) := ctx_trename h Nat.succ

theorem form_twk {Γ : Tel} {A : Ty} (h : FormJ Γ A) : FormJ (twkTel Γ) (twk A) :=
  form_trename h Nat.succ

theorem has_twk {Γ : Tel} {p : Poly} {A : Ty} (h : HasJ Γ p A) : HasJ (twkTel Γ) p (twk A) :=
  has_trename h Nat.succ

/-- Church naturals are syntactically formed in every actual joint context. -/
theorem form_nat {Γ : Tel} (hc : CtxJ Γ) : FormJ Γ P01AC.EffectiveCompleteness.N := by
  apply FormJ.all hc
  have cw := ctx_twk hc
  have fp : FormJ (twkTel Γ) (.param 0) := .param cw
  have fe : FormJ (twkTel Γ) (.pi (.param 0) (.param 0)) :=
    .pi fp (.param (.ext cw fp))
  have ce := CtxJ.ext cw fe
  have fpe : FormJ (.pi (.param 0) (.param 0) :: twkTel Γ) (.param 0) := .param ce
  exact .pi fe (.pi fpe (.param (.ext ce fpe)))

#print axioms form_nat
#print axioms form_trename
#print axioms has_trename
#print axioms ctx_trename
#print axioms form_twk
#print axioms has_twk
#print axioms ctx_twk
end JointCompletion.Structural
