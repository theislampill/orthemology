import InternalUniqueness
namespace RigidityInitiality
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity InternalRecursorPrinciple
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

theorem all_body_form {Γ : Tel} {B : Ty} (h : Form Γ (.all B)) : Form (twkTel Γ) B := by
  cases h; assumption

theorem apply_with_form {Γ : Tel} {X B : Ty} {f a : Poly} (hc : Ctx Γ)
    (hF : Form Γ (.pi X B)) (ha : Has Γ a X) (hf : HasE Γ f (.pi X B)) :
    Form Γ (inst B a) ∧ HasE Γ (.app f a) (inst B a) := by
  have ht := form_inst_source hc (pi_body_form hF) ha
  exact ⟨ht, .piElim (form_inclusion hF) (form_inclusion ht) hf (has_inclusion ha)⟩

def NatRecResult (u : Poly) : Ty := .pi N (.identity N
  (.app (pren Nat.succ u) (.var 0)) (.app (.app (.var 0) succPoly) zero))

macro "natU_norm" : tactic => `(tactic|
  simp only [Uniqueness, ZeroLaw, StepLaw, UniqueConclusion, A, End, NT, N, NBody,
    arr, wk, tinst, tsubst, mixed, subst, inst, tup, cons, pup, psub, pren,
    psub_comp, psub_id, liftRen,
    P01AC.BooleanPrimitive.psub_closed (has_scoped succ_has),
    P01AC.BooleanPrimitive.psub_closed (has_scoped (inputNumeral_has 0))] at *)

theorem uniqueness_nat_instance {Γ : Tel} {w u z s : Poly} (hc : Ctx Γ)
    (hw : HasE Γ w Uniqueness) (hu : Has Γ u NT)
    (hz : Has Γ z (ZeroAt u)) (hs : Has Γ s (StepAt u)) :
    ∃ e, HasE Γ e (NatRecResult u) := by
  have hF := form_tinst (all_body_form (uniqueness_formed hc)) (N_form hc)
  have h0 := HasE.allElim (form_inclusion (uniqueness_formed hc))
    (form_inclusion (N_form hc)) (form_inclusion hF) hw
  have hzero := zero_has_N hc
  have hsucc := succ_has_NT hc
  natU_norm
  obtain ⟨hF1, h1⟩ := apply_with_form hc hF hzero h0
  natU_norm
  obtain ⟨hF2, h2⟩ := apply_with_form hc hF1 hsucc h1
  natU_norm
  obtain ⟨hF3, h3⟩ := apply_with_form hc hF2 hu h2
  natU_norm
  obtain ⟨hF4, h4⟩ := apply_with_form hc hF3 hz h3
  natU_norm
  obtain ⟨hF5, h5⟩ := apply_with_form hc hF4 hs h4
  refine ⟨.app (.app (.app (.app (.app w zero) succPoly) u) z) s, ?_⟩
  simpa [NatRecResult, N, NBody, arr, wk, subst, inst, psub, pup, pren, cons,
    psub_comp, psub_id, zero,
    P01AC.BooleanPrimitive.psub_closed (has_scoped succ_has),
    P01AC.BooleanPrimitive.psub_closed (has_scoped (inputNumeral_has 0))] using h5


theorem hasE_scoped {Γ : Tel} {p : Poly} {A : Ty} (h : HasE Γ p A) :
    Scoped Γ.length p := by
  induction h using HasE.rec
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
  | piExt => trivial
  | allExt => trivial


theorem nat_sym {Γ : Tel} {x y e : Poly} (hc : Ctx Γ)
    (hx : Has Γ x N) (hy : Has Γ y N) (he : HasE Γ e (.identity N x y)) :
    HasE Γ (jPoly ident y e) (.identity N y x) := by
  let P : Ty := .identity N (.var 0) (pren Nat.succ x)
  have cN := Ctx.ext hc (N_form hc)
  have hx1 : Has (N :: Γ) (pren Nat.succ x) N := has_wk hx hc (N_form hc)
  have hP : Form (N :: Γ) P := .identity (N_form cN) (.var (N_form cN) .zero) hx1
  have at_eq (v : Poly) : inst P v = .identity N v x := by
    simp [P, inst, subst, N, NBody, arr, wk, pren, psub, psub_comp, cons, psub_id]
  have base : Has Γ ident (.identity N x x) := .identityIntro (.identity (N_form hc) hx hx) hx hx (.refl _)
  have h := transport_source hc (N_form hc) hP hx hy he ((at_eq x).symm ▸ has_inclusion base)
  simpa only [at_eq] using h

theorem identity_zero {Γ : Tel} (hc : Ctx Γ) : Has Γ ident (ZeroAt ident) := by
  have hz := zero_has_N hc
  have hi : Has Γ ident NT := ExactScalarFusion.i_T hc
  have hiz := app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) hi hz
  exact .identityIntro (zeroAt_formed hc hi) hiz hz (.i zero)

theorem identity_step {Γ : Tel} (hc : Ctx Γ) : Has Γ (abstract ident) (StepAt ident) := by
  have hi : Has Γ ident NT := ExactScalarFusion.i_T hc
  have cN := Ctx.ext hc (N_form hc)
  have hn : Has (N :: Γ) (.var 0) N := .var (N_form cN) .zero
  have hs := succ_has_NT cN
  have hi1 : Has (N :: Γ) ident NT := ExactScalarFusion.i_T cN
  have isn := app_has (form_arr (N_form cN) (N_form cN)) (N_form cN) hi1
    (app_has (form_arr (N_form cN) (N_form cN)) (N_form cN) hs hn)
  have sin := app_has (form_arr (N_form cN) (N_form cN)) (N_form cN) hs
    (app_has (form_arr (N_form cN) (N_form cN)) (N_form cN) hi1 hn)
  apply Has.piIntro (stepAt_formed hc hi)
  · exact .identityIntro (.identity (N_form cN) isn sin) isn sin
      ((P01DF.PolyConv.i _).trans (.app (.refl _) (P01DF.PolyConv.i _).symm))
  · exact scoped_abstract trivial

theorem natRec_form {Γ : Tel} {u : Poly} (hc : Ctx Γ) (hu : Has Γ u NT) :
    Form Γ (NatRecResult u) := by
  have cN := Ctx.ext hc (N_form hc)
  have hu1 : Has (N :: Γ) (pren Nat.succ u) NT := has_wk hu hc (N_form hc)
  have hn : Has (N :: Γ) (.var 0) N := .var (N_form cN) .zero
  exact .pi (N_form hc) (.identity (N_form cN)
    (app_has (form_arr (N_form cN) (N_form cN)) (N_form cN) hu1 hn)
    (SourceFoldContract.fold_has cN (N_form cN) hn (succ_has_NT cN) (zero_has_N cN)))

theorem natRec_at {Γ : Tel} {u n e : Poly} (hc : Ctx Γ) (hu : Has Γ u NT)
    (hn : Has Γ n N) (he : HasE Γ e (NatRecResult u)) :
    HasE Γ (.app e n) (.identity N (.app u n) (.app (.app n succPoly) zero)) := by
  have h := (apply_with_form hc (natRec_form hc hu) hn he).2
  simpa [NatRecResult, inst, subst, N, NBody, arr, wk, pren, psub, psub_comp, cons, psub_id, zero,
    P01AC.BooleanPrimitive.psub_closed (has_scoped succ_has),
    P01AC.BooleanPrimitive.psub_closed (has_scoped (inputNumeral_has 0))] using h

theorem uniqueness_endomorphism_point {Γ : Tel} {w u z s n : Poly} (hc : Ctx Γ)
    (hw : HasE Γ w Uniqueness) (hu : Has Γ u NT)
    (hz : Has Γ z (ZeroAt u)) (hs : Has Γ s (StepAt u)) (hn : Has Γ n N) :
    ∃ e, HasE Γ e (.identity N (.app ident n) (.app u n)) := by
  have hi : Has Γ ident NT := ExactScalarFusion.i_T hc
  obtain ⟨pu, hpu⟩ := uniqueness_nat_instance hc hw hu hz hs
  obtain ⟨pi, hpi⟩ := uniqueness_nat_instance hc hw hi (identity_zero hc) (identity_step hc)
  have un := app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) hu hn
  have inn := app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) hi hn
  have foldn := SourceFoldContract.fold_has hc (N_form hc) hn (succ_has_NT hc) (zero_has_N hc)
  have p := natRec_at hc hu hn hpu
  have q := natRec_at hc hi hn hpi
  exact ⟨_, nat_identity_trans hc inn foldn un q (nat_sym hc un foldn p)⟩

theorem zeroAt_shift (u : Poly) : wk (ZeroAt u) = ZeroAt (pren Nat.succ u) := by
  simp [ZeroAt, wk, subst, N, NBody, arr, pren, psub, zero,
    P01AC.BooleanPrimitive.psub_closed (has_scoped (inputNumeral_has 0))]

theorem stepAt_shift (u : Poly) : wk (StepAt u) = StepAt (pren Nat.succ u) := by
  simp [StepAt, wk, subst, N, NBody, arr, pren, psub, pup, psub_comp,
    P01AC.BooleanPrimitive.psub_closed (has_scoped succ_has)]

/-- The generic uniqueness proposition forces every source Peano endomorphism
    to be identity, using actual source Pi extensionality. -/
theorem uniqueness_endomorphism {Γ : Tel} {w u z s : Poly} (hc : Ctx Γ)
    (hw : Has Γ w Uniqueness) (hu : Has Γ u NT)
    (hz : Has Γ z (ZeroAt u)) (hs : Has Γ s (StepAt u)) :
    HasE Γ ident (ResultAt u) := by
  have cN := Ctx.ext hc (N_form hc)
  have hw1 : Has (N :: Γ) (pren Nat.succ w) Uniqueness := by
    simpa only [wk, uniqueness_term_closed] using has_wk hw hc (N_form hc)
  have hu1 : Has (N :: Γ) (pren Nat.succ u) NT := has_wk hu hc (N_form hc)
  have hz1 := zeroAt_shift u ▸ has_wk hz hc (N_form hc)
  have hs1 := stepAt_shift u ▸ has_wk hs hc (N_form hc)
  have hn : Has (N :: Γ) (.var 0) N := .var (N_form cN) .zero
  obtain ⟨e, he⟩ := uniqueness_endomorphism_point cN (has_inclusion hw1) hu1 hz1 hs1 hn
  have hi : Has Γ ident NT := ExactScalarFusion.i_T hc
  have hi1 : Has (N :: Γ) ident NT := ExactScalarFusion.i_T cN
  have left := app_has (form_arr (N_form cN) (N_form cN)) (N_form cN) hi1 hn
  have right := app_has (form_arr (N_form cN) (N_form cN)) (N_form cN) hu1 hn
  have hM := Form.identity (N_form cN) left right
  have hPiM := Form.pi (N_form hc) hM
  have hh := HasE.piIntro (form_inclusion hPiM) he (scoped_abstract (hasE_scoped he))
  exact HasE.piExt (form_inclusion (N_form hc)) (form_inclusion (N_form cN))
    (form_inclusion (form_arr (N_form hc) (N_form hc))) (has_inclusion hi) (has_inclusion hu)
    (form_inclusion hM) (form_inclusion hPiM) hh (form_inclusion (resultAt_formed hc hu))
    (has_scoped hi) (has_scoped hu) (scoped_abstract (hasE_scoped he))
    (form_scoped (N_form hc)) (form_scoped (N_form cN))


theorem resultAt_shift (u : Poly) : wk (ResultAt u) = ResultAt (pren Nat.succ u) := by
  simp [ResultAt, NT, ident, wk, subst, N, NBody, arr, pren, psub]

/-- Closed converse at the exact original internal propositions.
    Neither proposition is asserted inhabited. -/
theorem internal_uniqueness_implies_rigidity :
    HasE [] (abstract (abstract (abstract (abstract ident)))) (arr Uniqueness Rigidity) := by
  have hU := uniqueness_formed Ctx.nil
  have cU := Ctx.ext Ctx.nil hU
  have hNT := form_arr (N_form cU) (N_form cU)
  have cT := Ctx.ext cU hNT
  have hu0 : Has [NT, Uniqueness] (.var 0) NT :=
    .var (form_arr (N_form cT) (N_form cT)) .zero
  have hZ := zeroAt_formed cT hu0
  have cZ := Ctx.ext cT hZ
  have hu1 : Has [ZeroAt (.var 0), NT, Uniqueness] (.var 1) NT :=
    .var (form_arr (N_form cZ) (N_form cZ)) (.succ .zero)
  have hS := stepAt_formed cZ hu1
  have cS := Ctx.ext cZ hS
  have hu2 : Has [StepAt (.var 1), ZeroAt (.var 0), NT, Uniqueness] (.var 2) NT :=
    .var (form_arr (N_form cS) (N_form cS)) (.succ (.succ .zero))
  have hz0 : Has [StepAt (.var 1), ZeroAt (.var 0), NT, Uniqueness] (.var 1)
      (wk (wk (ZeroAt (.var 0)))) :=
    .var (lookup_form cS (.succ .zero)) (.succ .zero)
  have hz : Has [StepAt (.var 1), ZeroAt (.var 0), NT, Uniqueness] (.var 1) (ZeroAt (.var 2)) := by
    simpa only [zeroAt_shift, pren, psub] using hz0
  have hs0 : Has [StepAt (.var 1), ZeroAt (.var 0), NT, Uniqueness] (.var 0)
      (wk (StepAt (.var 1))) := .var (form_wk hS cZ hS) .zero
  have hs : Has [StepAt (.var 1), ZeroAt (.var 0), NT, Uniqueness] (.var 0) (StepAt (.var 2)) := by
    simpa only [stepAt_shift, pren, psub] using hs0
  have rw0 : Lookup [StepAt (.var 1), ZeroAt (.var 0), NT, Uniqueness] 3
      (wk (wk (wk (wk Uniqueness)))) := .succ (.succ (.succ .zero))
  have hw0 := Has.var (lookup_form cS rw0) rw0
  have hw : Has [StepAt (.var 1), ZeroAt (.var 0), NT, Uniqueness] (.var 3) Uniqueness := by
    simpa only [wk, uniqueness_term_closed] using hw0
  have body := uniqueness_endomorphism cS hw hu2 hz hs
  have hR1 := resultAt_formed cZ hu1
  have first : HasE [ZeroAt (.var 0), NT, Uniqueness] (abstract ident)
      (arr (StepAt (.var 1)) (ResultAt (.var 1))) := by
    apply HasE.piIntro (form_inclusion (form_arr hS hR1))
    · simpa only [resultAt_shift, pren, psub] using body
    · exact scoped_abstract trivial
  have hS0 := stepAt_formed cT hu0
  have hR0 := resultAt_formed cT hu0
  have second : HasE [NT, Uniqueness] (abstract (abstract ident))
      (arr (ZeroAt (.var 0)) (arr (StepAt (.var 0)) (ResultAt (.var 0)))) := by
    apply HasE.piIntro (form_inclusion (form_arr hZ (form_arr hS0 hR0)))
    · have ew (X Y : Ty) : wk (arr X Y) = arr (wk X) (wk Y) := subst_arr X Y _
      simpa only [ew, stepAt_shift, resultAt_shift, pren, psub] using first
    · exact scoped_abstract (scoped_abstract trivial)
  have third : HasE [Uniqueness] (abstract (abstract (abstract ident))) Rigidity :=
    .piIntro (form_inclusion (rigidity_formed cU)) second
      (scoped_abstract (scoped_abstract (scoped_abstract trivial)))
  apply HasE.piIntro (form_inclusion (form_arr hU (rigidity_formed Ctx.nil)))
  · simpa only [wk, rigidity_subst] using third
  · exact scoped_abstract (scoped_abstract (scoped_abstract (scoped_abstract trivial)))

#print axioms uniqueness_nat_instance
#print axioms uniqueness_endomorphism
#print axioms internal_uniqueness_implies_rigidity
end RigidityInitiality
