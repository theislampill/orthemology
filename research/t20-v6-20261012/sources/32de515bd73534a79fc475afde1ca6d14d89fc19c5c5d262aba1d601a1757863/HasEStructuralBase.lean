/- Isolated finite structural port for the actual 20-rule HasE grammar. -/
import AllStructuralRename
import ClosedProofCanonicalisation
namespace P01AC.ExtensionalRepair.Structural
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

theorem form_ctx {Γ : Tel} {A : Ty} (h : FormE Γ A) : CtxE Γ := by
  induction h using FormE.rec
    (motive_1 := fun _ _ => True) (motive_3 := fun _ _ _ _ => True) with
  | param h _ => exact h
  | bottom h _ => exact h
  | raw h _ => exact h
  | all h _ _ _ => exact h
  | pi _ _ ih _ => exact ih
  | sigma _ _ ih _ => exact ih
  | identity _ _ _ ih _ _ => exact ih
  | _ => trivial

theorem form_trename {Γ : Tel} {A : Ty} (h : FormE Γ A) :
    ∀ r : Nat → Nat, FormE (trenameTel r Γ) (trename r A) := by
  induction h using FormE.rec
    (motive_1 := fun Γ _ => ∀ r, CtxE (trenameTel r Γ))
    (motive_3 := fun Γ p A _ => ∀ r, HasE (trenameTel r Γ) p (trename r A)) with
  | nil => (first | intro r | rename_i r); exact .nil
  | ext hΓ hA iΓ iA => (first | intro r | rename_i r); exact .ext (iΓ r) (iA r)
  | param hΓ iΓ => intro r; exact .param (iΓ r)
  | bottom hΓ iΓ => intro r; exact .bottom (iΓ r)
  | raw hΓ iΓ => intro r; exact .raw (iΓ r)
  | all hΓ hB iΓ iB =>
      intro r
      exact .all (iΓ r) (by simpa only [trenameTel_twk] using iB (liftRen r))
  | pi hA hB iA iB => intro r; exact .pi (iA r) (iB r)
  | sigma hA hB iA iB => intro r; exact .sigma (iA r) (iB r)
  | identity hA hp hq iA ip iq => intro r; exact .identity (iA r) (ip r) (iq r)
  | var hA hn iA => (first | intro r | rename_i r); exact .var (iA r) (lookup_trename hn r)
  | i hA hF iA iF =>
      first | intro r | rename_i r
      simpa only [trename_arr] using HasE.i (iA r) (by simpa only [trename_arr] using iF r)
  | k hA hB hF iA iB iF =>
      first | intro r | rename_i r
      simpa only [trename_arr] using HasE.k (iA r) (iB r) (by simpa only [trename_arr] using iF r)
  | s hA hB hC hF iA iB iC iF =>
      first | intro r | rename_i r
      simpa only [trename_arr] using HasE.s (iA r) (iB r) (iC r) (by simpa only [trename_arr] using iF r)
  | @finite C Γ t υ hlen hυ hF ht iυ iF =>
      first | intro r | rename_i r
      simpa only [trename_finite_instance] using
        HasE.finite (υ.map (trename r)) (by simpa only [List.length_map] using hlen)
          (fun n hn => by simpa only [typeImages_trename] using iυ n (by simpa only [List.length_map] using hn) r)
          (by simpa only [trename_finite_instance] using iF r) ht
  | allIntro hF hp iF ip =>
      first | intro r | rename_i r
      exact .allIntro (iF r) (by simpa only [trenameTel_twk] using ip (liftRen r))
  | allElim hF hA hI hp iF iA iI ip =>
      first | intro r | rename_i r
      simpa only [trename_tinst] using HasE.allElim (iF r) (iA r)
        (by simpa only [trename_tinst] using iI r) (ip r)
  | rawAtom hF iF => (first | intro r | rename_i r); exact .rawAtom (iF r)
  | rawApp hF hf ha iF iff ia => (first | intro r | rename_i r); exact .rawApp (iF r) (iff r) (ia r)
  | piIntro hF hb hs iF ib =>
      first | intro r | rename_i r
      exact .piIntro (iF r) (ib r) (by simpa only [trenameTel, List.length_map] using hs)
  | piElim hF hI hf ha iF iI iff ia =>
      first | intro r | rename_i r
      simpa only [trename_inst] using HasE.piElim (iF r)
        (by simpa only [trename_inst] using iI r) (iff r) (ia r)
  | sigmaIntro hF hI ha hb iF iI ia ib =>
      first | intro r | rename_i r
      simpa only [trename_inst] using HasE.sigmaIntro (iF r)
        (by simpa only [trename_inst] using iI r) (ia r)
        (by simpa only [trename_inst] using ib r)
  | sigmaFst hA hF hz iA iF iz => (first | intro r | rename_i r); exact .sigmaFst (iA r) (iF r) (iz r)
  | sigmaSnd hF hI hz iF iI iz =>
      first | intro r | rename_i r
      simpa only [trename_inst] using HasE.sigmaSnd (iF r)
        (by simpa only [trename_inst] using iI r) (iz r)
  | identityIntro hF hp hq hc iF ip iq => (first | intro r | rename_i r); exact .identityIntro (iF r) (ip r) (iq r) hc
  | proofErase hR hI hp iR iI ip => (first | intro r | rename_i r); exact .proofErase (iR r) (iI r) (ip r)
  | j hA hB hI hD hE hx hy he hd iA iB iI iD iE ix iy ie id =>
      first | intro r | rename_i r
      simpa only [trename_motiveAt] using HasE.j (iA r)
        (by simpa only [trenameTel_theta] using iB r)
        (iI r) (by simpa only [trename_motiveAt] using iD r)
        (by simpa only [trename_motiveAt] using iE r)
        (ix r) (iy r) (ie r) (by simpa only [trename_motiveAt] using id r)
  | conv hA hp hc hs iA ip =>
      first | intro r | rename_i r
      exact .conv (iA r) (ip r) hc (by simpa only [trenameTel, List.length_map] using hs)

  | piExt hA hB hPi hp hq hBody hFam hh hId sp sq sh sa sb iA iB iPi ip iq iBody iFam ih iId =>
      first | intro r | rename_i r
      exact .piExt (iA r) (iB r) (iPi r) (ip r) (iq r)
        (iBody r) (iFam r) (ih r) (iId r)
        (by simpa only [trenameTel, List.length_map] using sp)
        (by simpa only [trenameTel, List.length_map] using sq)
        (by simpa only [trenameTel, List.length_map] using sh)
        (by simpa only [trenameTel, List.length_map] using tyScoped_trename sa r)
        (by simpa only [trenameTel, List.length_map] using tyScoped_trename sb r)
  | allExt hB hAll hp hq hBody hh hId sp sq sh sb iB iAll ip iq iBody ih iId =>
      first | intro r | rename_i r
      exact .allExt
        (by simpa only [trenameTel_twk] using iB (liftRen r))
        (iAll r) (ip r) (iq r)
        (by simpa only [trenameTel_twk] using iBody (liftRen r))
        (by simpa only [trenameTel_twk] using ih (liftRen r)) (iId r)
        (by simpa only [trenameTel, List.length_map] using sp)
        (by simpa only [trenameTel, List.length_map] using sq)
        (by simpa only [trenameTel, List.length_map] using sh)
        (by simpa only [trenameTel, List.length_map] using tyScoped_trename sb (liftRen r))

theorem has_trename {Γ : Tel} {p : Poly} {A : Ty} (h : HasE Γ p A) (r : Nat → Nat) :
    HasE (trenameTel r Γ) p (trename r A) := by
  have hi := form_trename (FormE.identity (ClosedProofCanonicalisation.formed h) h h) r
  cases hi with
  | identity _ hp _ => exact hp

theorem ctx_trename {Γ : Tel} (h : CtxE Γ) (r : Nat → Nat) : CtxE (trenameTel r Γ) := by
  exact form_ctx (form_trename (FormE.bottom h) r)

theorem ctx_twk {Γ : Tel} (h : CtxE Γ) : CtxE (twkTel Γ) := ctx_trename h Nat.succ

theorem form_twk {Γ : Tel} {A : Ty} (h : FormE Γ A) : FormE (twkTel Γ) (twk A) :=
  form_trename h Nat.succ

theorem has_twk {Γ : Tel} {p : Poly} {A : Ty} (h : HasE Γ p A) : HasE (twkTel Γ) p (twk A) :=
  has_trename h Nat.succ


#print axioms form_trename
#print axioms has_trename
#print axioms ctx_twk
end P01AC.ExtensionalRepair.Structural
