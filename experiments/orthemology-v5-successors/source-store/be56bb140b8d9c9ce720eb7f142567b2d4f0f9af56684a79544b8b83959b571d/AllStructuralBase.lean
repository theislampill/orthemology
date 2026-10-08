/- Syntax-only regularity and type-parameter reindexing. -/
import AllMixedAlgebra
namespace P01AC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

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
  | all => trivial
  | raw => trivial
  | pi => trivial
  | sigma => trivial
  | identity => trivial
  | var hA hn ih => exact lookup_lt hn
  | i => trivial
  | k => trivial
  | s => trivial
  | finite => trivial
  | allIntro hF hp iF ip => simpa only [twkTel, List.length_map] using ip
  | allElim hF hA hI hp iF iA iI ip => exact ip
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


/-- A derivation retains exact result formation. -/
theorem has_form {Γ : Tel} {p : Poly} {A : Ty} (h : Has Γ p A) : Form Γ A := by
  cases h <;> assumption

theorem form_ctx {Γ : Tel} {A : Ty} (h : Form Γ A) : Ctx Γ := by
  induction h using Form.rec
    (motive_1 := fun _ _ => True) (motive_3 := fun _ _ _ _ => True) with
  | param h _ => exact h
  | bottom h _ => exact h
  | raw h _ => exact h
  | all h _ _ _ => exact h
  | pi _ _ ih _ => exact ih
  | sigma _ _ ih _ => exact ih
  | identity _ _ _ ih _ _ => exact ih
  | _ => trivial

theorem form_scoped {Γ : Tel} {A : Ty} (h : Form Γ A) : TyScoped Γ.length A := by
  induction h using Form.rec
    (motive_1 := fun _ _ => True) (motive_3 := fun _ _ _ _ => True) with
  | all _ _ _ ih => simpa only [twkTel, List.length_map] using ih
  | pi _ _ ia ib => exact ⟨ia, ib⟩
  | sigma _ _ ia ib => exact ⟨ia, ib⟩
  | identity _ hp hq ia _ _ => exact ⟨ia, has_scoped hp, has_scoped hq⟩
  | _ => trivial

/-- Bottom padding is preserved by every mixed map. -/
theorem typeImages_mixed (υ : List Ty) (σ : Nat → Poly) (τ : Nat → Ty) :
    typeImages (υ.map (mixed σ τ)) = fun n => mixed σ τ (typeImages υ n) := by
  induction υ with
  | nil => rfl
  | cons A υ ih =>
      funext n
      cases n with
      | zero => rfl
      | succ n => exact congrFun ih n

theorem typeImages_trename (υ : List Ty) (r : Nat → Nat) :
    typeImages (υ.map (trename r)) = fun n => trename r (typeImages υ n) := by
  induction υ with
  | nil => rfl
  | cons A υ ih =>
      funext n
      cases n with
      | zero => rfl
      | succ n => exact congrFun ih n

theorem typeImages_subst (υ : List Ty) (σ : Nat → Poly) :
    typeImages (υ.map (subst σ)) = fun n => subst σ (typeImages υ n) := by
  simpa only [show mixed σ Ty.param = subst σ from funext (fun A => mixed_param A σ)] using typeImages_mixed υ σ Ty.param

theorem mixed_fin (C : TypeCode) (σ : Nat → Poly) (τ : Nat → Ty) :
    mixed σ τ (fin C) = tsubst τ (fin C) := by
  induction C generalizing σ τ with
  | var n => rfl
  | bottom => rfl
  | arrow A B ha hb => simp only [fin, mixed_arr, tsubst_arr, ha, hb]
  | all B ih => exact congrArg Ty.all (ih σ (tup τ))

theorem mixed_finite_instance (C : TypeCode) (υ : List Ty) (σ : Nat → Poly) (τ : Nat → Ty) :
    mixed σ τ (tsubst (typeImages υ) (fin C)) =
      tsubst (typeImages (υ.map (mixed σ τ))) (fin C) := by
  rw [mixed_tsubst, mixed_fin, typeImages_mixed]

theorem subst_finite_instance (C : TypeCode) (υ : List Ty) (σ : Nat → Poly) :
    subst σ (tsubst (typeImages υ) (fin C)) =
      tsubst (typeImages (υ.map (subst σ))) (fin C) := by
  simpa only [show mixed σ Ty.param = subst σ from funext (fun A => mixed_param A σ)] using mixed_finite_instance C υ σ Ty.param

theorem trename_finite_instance (C : TypeCode) (υ : List Ty) (r : Nat → Nat) :
    trename r (tsubst (typeImages υ) (fin C)) =
      tsubst (typeImages (υ.map (trename r))) (fin C) := by
  rw [trename_tsubst, typeImages_trename]

def trenameTel (r : Nat → Nat) (Γ : Tel) : Tel := Γ.map (trename r)

theorem trenameTel_twk (r : Nat → Nat) (Γ : Tel) :
    trenameTel (liftRen r) (twkTel Γ) = twkTel (trenameTel r Γ) := by
  simp only [trenameTel, twkTel, List.map_map]
  congr 1
  funext A
  exact trename_twk A r

theorem trenameTel_theta (r : Nat → Nat) (Γ : Tel) (A : Ty) (x : Poly) :
    trenameTel r (theta Γ A x) = theta (trenameTel r Γ) (trename r A) x := by
  simp only [trenameTel, theta, List.map_cons, trename, trename_wk]

theorem lookup_trename {Γ : Tel} {n : Nat} {A : Ty} (h : Lookup Γ n A) (r : Nat → Nat) :
    Lookup (trenameTel r Γ) n (trename r A) := by
  induction h with
  | zero => simpa only [trenameTel, List.map_cons, trename_wk] using (Lookup.zero (A := trename r _) (Γ := trenameTel r _))
  | succ h ih => simpa only [trenameTel, List.map_cons, trename_wk] using Lookup.succ ih

theorem form_trename {Γ : Tel} {A : Ty} (h : Form Γ A) :
    ∀ r : Nat → Nat, Form (trenameTel r Γ) (trename r A) := by
  induction h using Form.rec
    (motive_1 := fun Γ _ => ∀ r, Ctx (trenameTel r Γ))
    (motive_3 := fun Γ p A _ => ∀ r, Has (trenameTel r Γ) p (trename r A)) with
  | nil => (first | intro r | rename_i r); exact .nil
  | ext hΓ hA iΓ iA => (first | intro r | rename_i r); exact .ext (iΓ r) (iA r)
  | param hΓ iΓ => (first | intro r | rename_i r); exact .param (iΓ r)
  | bottom hΓ iΓ => (first | intro r | rename_i r); exact .bottom (iΓ r)
  | raw hΓ iΓ => (first | intro r | rename_i r); exact .raw (iΓ r)
  | all hΓ hB iΓ iB =>
      first | intro r | rename_i r
      exact .all (iΓ r) (by simpa only [trenameTel_twk] using iB (liftRen r))
  | pi hA hB iA iB => (first | intro r | rename_i r); exact .pi (iA r) (iB r)
  | sigma hA hB iA iB => (first | intro r | rename_i r); exact .sigma (iA r) (iB r)
  | identity hA hp hq iA ip iq => (first | intro r | rename_i r); exact .identity (iA r) (ip r) (iq r)
  | var hA hn iA => (first | intro r | rename_i r); exact .var (iA r) (lookup_trename hn r)
  | i hA hF iA iF =>
      first | intro r | rename_i r
      simpa only [trename_arr] using Has.i (iA r) (by simpa only [trename_arr] using iF r)
  | k hA hB hF iA iB iF =>
      first | intro r | rename_i r
      simpa only [trename_arr] using Has.k (iA r) (iB r) (by simpa only [trename_arr] using iF r)
  | s hA hB hC hF iA iB iC iF =>
      first | intro r | rename_i r
      simpa only [trename_arr] using Has.s (iA r) (iB r) (iC r) (by simpa only [trename_arr] using iF r)
  | @finite C Γ t υ hlen hυ hF ht iυ iF =>
      first | intro r | rename_i r
      simpa only [trename_finite_instance] using
        Has.finite (υ.map (trename r)) (by simpa only [List.length_map] using hlen)
          (fun n hn => by simpa only [typeImages_trename] using iυ n (by simpa only [List.length_map] using hn) r)
          (by simpa only [trename_finite_instance] using iF r) ht
  | allIntro hF hp iF ip =>
      first | intro r | rename_i r
      exact .allIntro (iF r) (by simpa only [trenameTel_twk] using ip (liftRen r))
  | allElim hF hA hI hp iF iA iI ip =>
      first | intro r | rename_i r
      simpa only [trename_tinst] using Has.allElim (iF r) (iA r)
        (by simpa only [trename_tinst] using iI r) (ip r)
  | rawAtom hF iF => (first | intro r | rename_i r); exact .rawAtom (iF r)
  | rawApp hF hf ha iF iff ia => (first | intro r | rename_i r); exact .rawApp (iF r) (iff r) (ia r)
  | piIntro hF hb hs iF ib =>
      first | intro r | rename_i r
      exact .piIntro (iF r) (ib r) (by simpa only [trenameTel, List.length_map] using hs)
  | piElim hF hI hf ha iF iI iff ia =>
      first | intro r | rename_i r
      simpa only [trename_inst] using Has.piElim (iF r)
        (by simpa only [trename_inst] using iI r) (iff r) (ia r)
  | sigmaIntro hF hI ha hb iF iI ia ib =>
      first | intro r | rename_i r
      simpa only [trename_inst] using Has.sigmaIntro (iF r)
        (by simpa only [trename_inst] using iI r) (ia r)
        (by simpa only [trename_inst] using ib r)
  | sigmaFst hA hF hz iA iF iz => (first | intro r | rename_i r); exact .sigmaFst (iA r) (iF r) (iz r)
  | sigmaSnd hF hI hz iF iI iz =>
      first | intro r | rename_i r
      simpa only [trename_inst] using Has.sigmaSnd (iF r)
        (by simpa only [trename_inst] using iI r) (iz r)
  | identityIntro hF hp hq hc iF ip iq => (first | intro r | rename_i r); exact .identityIntro (iF r) (ip r) (iq r) hc
  | proofErase hR hI hp iR iI ip => (first | intro r | rename_i r); exact .proofErase (iR r) (iI r) (ip r)
  | j hA hB hI hD hE hx hy he hd iA iB iI iD iE ix iy ie id =>
      first | intro r | rename_i r
      simpa only [trename_motiveAt] using Has.j (iA r)
        (by simpa only [trenameTel_theta] using iB r)
        (iI r) (by simpa only [trename_motiveAt] using iD r)
        (by simpa only [trename_motiveAt] using iE r)
        (ix r) (iy r) (ie r) (by simpa only [trename_motiveAt] using id r)
  | conv hA hp hc hs iA ip =>
      first | intro r | rename_i r
      exact .conv (iA r) (ip r) hc (by simpa only [trenameTel, List.length_map] using hs)

theorem has_trename {Γ : Tel} {p : Poly} {A : Ty} (h : Has Γ p A) (r : Nat → Nat) :
    Has (trenameTel r Γ) p (trename r A) := by
  have hi := form_trename (Form.identity (has_form h) h h) r
  cases hi with
  | identity _ hp _ => exact hp

theorem ctx_trename {Γ : Tel} (h : Ctx Γ) (r : Nat → Nat) : Ctx (trenameTel r Γ) := by
  exact form_ctx (form_trename (Form.bottom h) r)

theorem ctx_twk {Γ : Tel} (h : Ctx Γ) : Ctx (twkTel Γ) := ctx_trename h Nat.succ

theorem form_twk {Γ : Tel} {A : Ty} (h : Form Γ A) : Form (twkTel Γ) (twk A) :=
  form_trename h Nat.succ

theorem has_twk {Γ : Tel} {p : Poly} {A : Ty} (h : Has Γ p A) : Has (twkTel Γ) p (twk A) :=
  has_trename h Nat.succ

end P01AC
