import UniquenessConverse

/- Cross-type consequence of the existing SourceUniqueness theorem.
   This module changes no source judgement and assumes no inhabitant of Rigidity. -/
namespace RigidityPolymorphicTransfer
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity RigidityInitiality
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def UnitTy : Ty := .all End
def UnitEta : Ty := .pi UnitTy (.identity UnitTy (.var 0) ident)
def liftUnit (u : Poly) : Poly := .app (.atom .k) u

theorem unit_subst (σ : Nat → Poly) : subst σ UnitTy = UnitTy := by
  simp [UnitTy, End, A, arr, subst, wk]
theorem unit_twk : twk UnitTy = UnitTy := by
  simp [UnitTy, End, A, arr, twk, trename, liftRen, wk, subst]
theorem unit_form {Γ : Tel} (hc : Ctx Γ) : Form Γ UnitTy :=
  .all hc (form_arr (.param (ctx_twk hc)) (.param (ctx_twk hc)))
theorem ident_end {Γ : Tel} (hc : Ctx Γ) : Has Γ ident End :=
  .i (.param hc) (form_arr (.param hc) (.param hc))
theorem ident_unit {Γ : Tel} (hc : Ctx Γ) : Has Γ ident UnitTy :=
  .allIntro (unit_form hc) (ident_end (ctx_twk hc))
theorem unit_end {Γ : Tel} {u : Poly} (hc : Ctx Γ) (hu : Has Γ u UnitTy) :
    Has Γ u End := by
  have h : tinst End A = End := by
    simp [End, A, arr, tinst, tsubst, mixed, wk, subst, cons]
  have q := Has.allElim (unit_form hc) (show Form Γ A from .param hc)
    (h.symm ▸ form_arr (.param hc) (.param hc)) hu
  simpa only [h] using q

theorem const_has {Γ : Tel} {X Y : Ty} {a : Poly} (_hc : Ctx Γ)
    (hX : Form Γ X) (hY : Form Γ Y) (ha : Has Γ a X) :
    Has Γ (.app (.atom .k) a) (arr Y X) :=
  app_has (form_arr hX (form_arr hY hX)) (form_arr hY hX)
    (.k hX hY (form_arr hX (form_arr hY hX))) ha

/-- The encoding is original Has, including its genuine All introduction. -/
theorem liftUnit_has {Γ : Tel} {u : Poly} (hc : Ctx Γ) (hu : Has Γ u UnitTy) :
    Has Γ (liftUnit u) N := by
  have ct := ctx_twk hc
  have hut : Has (twkTel Γ) u UnitTy := unit_twk ▸ has_twk hu
  have hue := unit_end ct hut
  exact .allIntro (N_form hc)
    (const_has ct (form_arr (.param ct) (.param ct))
      (form_arr (.param ct) (.param ct)) hue)

theorem scalar_transE {Γ : Tel} {x y z e d : Poly} (hc : Ctx Γ)
    (hx : Has Γ x A) (hy : Has Γ y A) (hz : Has Γ z A)
    (he : HasE Γ e (.identity A x y)) (hd : HasE Γ d (.identity A y z)) :
    HasE Γ (jPoly e z d) (.identity A x z) := by
  let P : Ty := .identity A (pren Nat.succ x) (.var 0)
  have cA := Ctx.ext hc (show Form Γ A from .param hc)
  have hx1 : Has (A :: Γ) (pren Nat.succ x) A := has_wk hx hc (show Form Γ A from .param hc)
  have hP : Form (A :: Γ) P := .identity (.param cA) hx1 (.var (.param cA) .zero)
  have at_eq (v : Poly) : inst P v = .identity A x v := by
    simp [P, inst, A, subst, pren, psub, psub_comp, cons, psub_id]
  have h := transport_source hc (.param hc) hP hy hz hd ((at_eq y).symm ▸ he)
  simpa only [at_eq] using h

theorem scalar_symE {Γ : Tel} {x y e : Poly} (hc : Ctx Γ)
    (hx : Has Γ x A) (hy : Has Γ y A) (he : HasE Γ e (.identity A x y)) :
    HasE Γ (jPoly ident y e) (.identity A y x) := by
  let P : Ty := .identity A (.var 0) (pren Nat.succ x)
  have cA := Ctx.ext hc (show Form Γ A from .param hc)
  have hx1 : Has (A :: Γ) (pren Nat.succ x) A := has_wk hx hc (show Form Γ A from .param hc)
  have hP : Form (A :: Γ) P := .identity (.param cA) (.var (.param cA) .zero) hx1
  have at_eq (v : Poly) : inst P v = .identity A v x := by
    simp [P, inst, A, subst, pren, psub, psub_comp, cons, psub_id]
  have base : Has Γ ident (.identity A x x) := .identityIntro (.identity (.param hc) hx hx) hx hx (.refl _)
  have h := transport_source hc (.param hc) hP hx hy he ((at_eq x).symm ▸ has_inclusion base)
  simpa only [at_eq] using h

theorem constant_zero {Γ : Tel} {a : Poly} (hc : Ctx Γ) (ha : Has Γ a A) :
    Has Γ ident (RecZero a (.app (.atom .k) a)) := by
  have hk := const_has hc (.param hc) (N_form hc) ha
  have hka := app_has (form_arr (N_form hc) (.param hc)) (.param hc) hk (zero_has_N hc)
  exact .identityIntro (.identity (.param hc) hka ha) hka ha (.k _ _)

theorem constant_step {Γ : Tel} {a : Poly} (hc : Ctx Γ) (ha : Has Γ a A) :
    Has Γ (abstract ident) (RecStep ident (.app (.atom .k) a)) := by
  have cN := Ctx.ext hc (N_form hc)
  have ha1 : Has (N :: Γ) (pren Nat.succ a) A := has_wk ha hc (N_form hc)
  have hk := const_has cN (.param cN) (N_form cN) ha1
  have hn : Has (N :: Γ) (.var 0) N := .var (N_form cN) .zero
  have hsn := app_has (form_arr (N_form cN) (N_form cN)) (N_form cN) (succ_has_NT cN) hn
  have left := app_has (form_arr (N_form cN) (.param cN)) (.param cN) hk hsn
  have mid := app_has (form_arr (N_form cN) (.param cN)) (.param cN) hk hn
  have right := app_has (form_arr (.param cN) (.param cN)) (.param cN) (ident_end cN) mid
  have body : Has (N :: Γ) ident (RecStepBody ident (.app (.atom .k) a)) :=
    .identityIntro (.identity (.param cN) left right) left right
      ((P01DF.PolyConv.k _ _).trans ((P01DF.PolyConv.i _).trans (.k _ _)).symm)
  exact .piIntro (.pi (N_form hc) (has_form body)) body (scoped_abstract trivial)

/-- Existing SourceUniqueness, specialized to the constant recursor and I.
    This is the entire induction content of the unit transfer. -/
theorem nat_identity_fold {Γ : Tel} {r n a : Poly} (hc : Ctx Γ)
    (hr : HasE Γ r Rigidity) (hn : Has Γ n N) (ha : Has Γ a A) :
    ∃ e, HasE Γ e (.identity A (.app (.app n ident) a) a) := by
  have hk := const_has hc (.param hc) (N_form hc) ha
  have hkn := app_has (form_arr (N_form hc) (.param hc)) (.param hc) hk hn
  have hfold := SourceFoldContract.fold_has hc (.param hc) hn (ident_end hc) ha
  have e := recursor_unique_source hc (ident_end hc) ha hk
    (constant_zero hc ha) (constant_step hc ha) hr hn
  have rev := scalar_symE hc hkn hfold e
  have last : Has Γ ident (.identity A (.app (.app (.atom .k) a) n) a) :=
    .identityIntro (.identity (.param hc) hkn ha) hkn ha (.k _ _)
  exact ⟨_, scalar_transE hc hfold hkn ha rev (has_inclusion last)⟩

/-- Pointwise Unit identity, under arbitrary original-HasE Rigidity evidence. -/
theorem unit_point {Γ : Tel} {r u a : Poly} (hc : Ctx Γ)
    (hr : HasE Γ r Rigidity) (hu : Has Γ u UnitTy) (ha : Has Γ a A) :
    ∃ e, HasE Γ e (.identity A (.app u a) (.app ident a)) := by
  have hn := liftUnit_has hc hu
  have hua := app_has (form_arr (.param hc) (.param hc)) (.param hc) (unit_end hc hu) ha
  have hia := app_has (form_arr (.param hc) (.param hc)) (.param hc) (ident_end hc) ha
  have hfold := SourceFoldContract.fold_has hc (.param hc) hn (ident_end hc) ha
  obtain ⟨e, he⟩ := nat_identity_fold hc hr hn ha
  have first : Has Γ ident (.identity A (.app u a) (.app (.app (liftUnit u) ident) a)) :=
    .identityIntro (.identity (.param hc) hua hfold) hua hfold
      (P01DF.PolyConv.app (.k _ _) (.refl _)).symm
  have last : Has Γ ident (.identity A a (.app ident a)) :=
    .identityIntro (.identity (.param hc) ha hia) ha hia (P01DF.PolyConv.i _).symm
  exact ⟨_, scalar_transE hc hua ha hia
    (scalar_transE hc hua hfold ha (has_inclusion first) he) (has_inclusion last)⟩

/-- Extensional closure. Rigidity is an ordinary local hypothesis while
    crossing binders; no general HasE weakening is assumed here. -/
theorem unit_ext_from_original_rigidity {Γ : Tel} {r u : Poly} (hc : Ctx Γ)
    (hr : Has Γ r Rigidity) (hu : Has Γ u UnitTy) :
    HasE Γ ident (.identity UnitTy u ident) := by
  have ct := ctx_twk hc
  have hut : Has (twkTel Γ) u UnitTy := unit_twk ▸ has_twk hu
  have hrt : Has (twkTel Γ) r Rigidity := rigidity_type_closed ▸ has_twk hr
  have ca := Ctx.ext ct (show Form (twkTel Γ) A from .param ct)
  have hu1 : Has (A :: twkTel Γ) (pren Nat.succ u) UnitTy := by
    simpa only [wk, unit_subst] using has_wk hut ct (show Form (twkTel Γ) A from .param ct)
  have hr1 : Has (A :: twkTel Γ) (pren Nat.succ r) Rigidity := by
    simpa only [wk, rigidity_subst] using has_wk hrt ct (show Form (twkTel Γ) A from .param ct)
  have ha : Has (A :: twkTel Γ) (.var 0) A := .var (.param ca) .zero
  have hleft := app_has (form_arr (.param ca) (.param ca)) (.param ca) (unit_end ca hu1) ha
  have hright := app_has (form_arr (.param ca) (.param ca)) (.param ca) (ident_end ca) ha
  have hM := Form.identity (.param ca) hleft hright
  have hPM := Form.pi (show Form (twkTel Γ) A from .param ct) hM
  obtain ⟨e, he⟩ := unit_point ca (has_inclusion hr1) hu1 ha
  have hep := HasE.piIntro (form_inclusion hPM) he (scoped_abstract (hasE_scoped he))
  have hue := unit_end ct hut
  have hie := ident_end ct
  have atEnd : HasE (twkTel Γ) ident (.identity End u ident) :=
    .piExt (form_inclusion (.param ct)) (form_inclusion (.param ca))
      (form_inclusion (form_arr (.param ct) (.param ct)))
      (has_inclusion hue) (has_inclusion hie) (form_inclusion hM) (form_inclusion hPM)
      hep (form_inclusion (.identity (form_arr (.param ct) (.param ct)) hue hie))
      (has_scoped hue) trivial (scoped_abstract (hasE_scoped he))
      (form_scoped (show Form (twkTel Γ) A from .param ct))
      (form_scoped (show Form (A :: twkTel Γ) A from .param ca))
  exact .allExt (form_inclusion (form_arr (.param ct) (.param ct)))
    (form_inclusion (unit_form hc)) (has_inclusion hu) (has_inclusion (ident_unit hc))
    (form_inclusion (.identity (form_arr (.param ct) (.param ct)) hue hie)) atEnd
    (form_inclusion (.identity (unit_form hc) hu (ident_unit hc)))
    (has_scoped hu) trivial trivial (form_scoped (form_arr (.param hc) (.param hc)))

theorem unitEta_form {Γ : Tel} (hc : Ctx Γ) : Form Γ UnitEta := by
  have cu := Ctx.ext hc (unit_form hc)
  have hu : Has (UnitTy :: Γ) (.var 0) UnitTy := .var (unit_form cu) .zero
  exact .pi (unit_form hc) (.identity (unit_form cu) hu (ident_unit cu))

theorem unitEta_subst (σ : Nat → Poly) : subst σ UnitEta = UnitEta := by
  simp [UnitEta, unit_subst, subst, psub, pup, ident]

/-- Genuine source-internal implication in every original well-formed context.
    At Γ = [] this is the requested closed R → ∏u:Unit.Id(u,I). -/
theorem rigidity_implies_unit_eta_context {Γ : Tel} (hc : Ctx Γ) :
    HasE Γ (abstract (abstract ident)) (arr Rigidity UnitEta) := by
  have cr := Ctx.ext hc (rigidity_formed hc)
  have cu := Ctx.ext cr (unit_form cr)
  have hu : Has (UnitTy :: Rigidity :: Γ) (.var 0) UnitTy := .var (unit_form cu) .zero
  have rr : Lookup (UnitTy :: Rigidity :: Γ) 1 (wk (wk Rigidity)) := .succ .zero
  have hr0 := Has.var (lookup_form cu rr) rr
  have hr : Has (UnitTy :: Rigidity :: Γ) (.var 1) Rigidity := by
    simpa only [wk, rigidity_subst] using hr0
  have body := unit_ext_from_original_rigidity cu hr hu
  have bound : HasE (Rigidity :: Γ) (abstract ident) UnitEta :=
    .piIntro (form_inclusion (unitEta_form cr)) body (scoped_abstract trivial)
  apply HasE.piIntro (form_inclusion (form_arr (rigidity_formed hc) (unitEta_form hc)))
  · simpa only [wk, unitEta_subst] using bound
  · exact scoped_abstract (scoped_abstract trivial)

theorem rigidity_implies_unit_eta :
    HasE [] (abstract (abstract ident)) (arr Rigidity UnitEta) :=
  rigidity_implies_unit_eta_context Ctx.nil

/-- Arbitrary HasE evidence of R is admitted by elimination of the source
    implication. No arbitrary HasE weakening or family rule is postulated. -/
theorem unit_eta_from_rigidity {Γ : Tel} {r u : Poly} (hc : Ctx Γ)
    (hr : HasE Γ r Rigidity) (hu : Has Γ u UnitTy) :
    HasE Γ (.app (.app (abstract (abstract ident)) r) u) (.identity UnitTy u ident) := by
  have first := HasE.piElim
    (form_inclusion (form_arr (rigidity_formed hc) (unitEta_form hc)))
    (form_inclusion ((inst_wk UnitEta r).symm ▸ unitEta_form hc))
    (rigidity_implies_unit_eta_context hc) hr
  have first' : HasE Γ (.app (abstract (abstract ident)) r) UnitEta := by
    simpa only [inst_wk] using first
  have at_eq : inst (.identity UnitTy (.var 0) ident) u = .identity UnitTy u ident := by
    simp [inst, subst, unit_subst, ident, psub, cons]
  have h := HasE.piElim (form_inclusion (unitEta_form hc))
    (form_inclusion (at_eq.symm ▸ Form.identity (unit_form hc) hu (ident_unit hc))) first' (has_inclusion hu)
  simpa only [at_eq] using h

#print axioms nat_identity_fold
#print axioms unit_point
#print axioms rigidity_implies_unit_eta
#print axioms unit_eta_from_rigidity
end RigidityPolymorphicTransfer
