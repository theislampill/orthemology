import UnitTransfer
import HasEClosedWeakening

namespace RigidityPolymorphicTransfer
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.CompilerBodyControl
open SourceRigidity RigidityInitiality InternalRecursorPrinciple
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def ZeroY (Y : Ty) (a u : Poly) : Ty := .identity Y (.app u zero) a
def StepY (Y : Ty) (g u : Poly) : Ty := .pi N (.identity (wk Y)
  (.app (pren Nat.succ u) (.app succPoly (.var 0)))
  (.app (pren Nat.succ g) (.app (pren Nat.succ u) (.var 0))))
def UniqueY (Y : Ty) (g a u : Poly) : Ty := .pi N (.identity (wk Y)
  (.app (pren Nat.succ u) (.var 0))
  (.app (.app (.var 0) (pren Nat.succ g)) (pren Nat.succ a)))

theorem appE {Γ : Tel} {X Y : Ty} {f a : Poly}
    (hX : Form Γ X) (hY : Form Γ Y)
    (hf : HasE Γ f (arr X Y)) (ha : HasE Γ a X) : HasE Γ (.app f a) Y := by
  have q := HasE.piElim (form_inclusion (form_arr hX hY))
    (form_inclusion ((inst_wk Y a).symm ▸ hY)) hf ha
  simpa only [inst_wk] using q

theorem uniqueness_from_rigidity {Γ : Tel} {r : Poly} (hc : Ctx Γ)
    (hr : HasE Γ r Rigidity) :
    HasE Γ (.app (abstract uniqueUniformProof) r) Uniqueness :=
  appE (rigidity_formed hc) (uniqueness_formed hc)
    (Structural.has_closed rigidity_implies_internal_uniqueness (ctx_inclusion hc)) hr

macro "unique_norm" : tactic => `(tactic|
  simp only [Uniqueness, ZeroLaw, StepLaw, UniqueConclusion, A, End, N, NBody,
    arr, tinst, tsubst, mixed, subst, inst, wk, tup, cons, pup, psub, pren,
    psub_comp, psub_id, liftRen, subst_comp, subst_id,
    P01AC.BooleanPrimitive.psub_closed (has_scoped succ_has),
    P01AC.BooleanPrimitive.psub_closed (has_scoped (inputNumeral_has 0))] at *)

theorem zeroY_form {Γ : Tel} {Y : Ty} {a u : Poly} (hc : Ctx Γ)
    (hY : Form Γ Y) (ha : Has Γ a Y) (hu : Has Γ u (arr N Y)) : Form Γ (ZeroY Y a u) :=
  .identity hY (app_has (form_arr (N_form hc) hY) hY hu (zero_has_N hc)) ha

theorem stepY_form {Γ : Tel} {Y : Ty} {g u : Poly} (hc : Ctx Γ)
    (hY : Form Γ Y) (hg : Has Γ g (arr Y Y)) (hu : Has Γ u (arr N Y)) : Form Γ (StepY Y g u) := by
  have cn := Ctx.ext hc (N_form hc)
  have yw := form_wk hY hc (N_form hc)
  have uw : Has (N :: Γ) (pren Nat.succ u) (arr N (wk Y)) := by
    simpa only [wk, subst_arr, N_subst] using has_wk hu hc (N_form hc)
  have gw : Has (N :: Γ) (pren Nat.succ g) (arr (wk Y) (wk Y)) := by
    simpa only [wk, subst_arr] using has_wk hg hc (N_form hc)
  have hn : Has (N :: Γ) (.var 0) N := .var (N_form cn) .zero
  have sn := app_has (form_arr (N_form cn) (N_form cn)) (N_form cn) (succ_has_NT cn) hn
  have un := app_has (form_arr (N_form cn) yw) yw uw hn
  exact .pi (N_form hc) (.identity yw
    (app_has (form_arr (N_form cn) yw) yw uw sn)
    (app_has (form_arr yw yw) yw gw un))

theorem uniqueY_form {Γ : Tel} {Y : Ty} {g a u : Poly} (hc : Ctx Γ)
    (hY : Form Γ Y) (hg : Has Γ g (arr Y Y)) (ha : Has Γ a Y)
    (hu : Has Γ u (arr N Y)) : Form Γ (UniqueY Y g a u) := by
  have cn := Ctx.ext hc (N_form hc)
  have yw := form_wk hY hc (N_form hc)
  have uw : Has (N :: Γ) (pren Nat.succ u) (arr N (wk Y)) := by
    simpa only [wk, subst_arr, N_subst] using has_wk hu hc (N_form hc)
  have gw : Has (N :: Γ) (pren Nat.succ g) (arr (wk Y) (wk Y)) := by
    simpa only [wk, subst_arr] using has_wk hg hc (N_form hc)
  have aw := has_wk ha hc (N_form hc)
  have hn : Has (N :: Γ) (.var 0) N := .var (N_form cn) .zero
  exact .pi (N_form hc) (.identity yw
    (app_has (form_arr (N_form cn) yw) yw uw hn)
    (SourceFoldContract.fold_has cn yw hn gw aw))

/-- The literal existing All uniqueness proposition admits arbitrary formed
    carriers and arbitrary HasE equation evidence by its original eliminators. -/
theorem unique_at_carrier {Γ : Tel} {Y : Ty} {w g a u z s : Poly} (hc : Ctx Γ)
    (hY : Form Γ Y) (hw : HasE Γ w Uniqueness)
    (hg : Has Γ g (arr Y Y)) (ha : Has Γ a Y) (hu : Has Γ u (arr N Y))
    (hz : HasE Γ z (ZeroY Y a u)) (hs : HasE Γ s (StepY Y g u)) :
    ∃ e, HasE Γ e (UniqueY Y g a u) := by
  have hF := form_tinst (all_body_form (uniqueness_formed hc)) hY
  have h0 := HasE.allElim (form_inclusion (uniqueness_formed hc))
    (form_inclusion hY) (form_inclusion hF) hw
  unique_norm
  obtain ⟨hF1, h1⟩ := apply_with_form hc hF ha h0
  unique_norm
  obtain ⟨hF2, h2⟩ := apply_with_form hc hF1 hg h1
  unique_norm
  obtain ⟨hF3, h3⟩ := apply_with_form hc hF2 hu h2
  unique_norm
  have h3' : HasE Γ (((w.app a).app g).app u)
      (arr (ZeroY Y a u) (arr (StepY Y g u) (UniqueY Y g a u))) := by
    simpa only [ZeroY, StepY, UniqueY, zero, N, NBody, arr, wk, subst, pren, psub,
      psub_comp, subst_comp, pup, cons,
      P01AC.BooleanPrimitive.psub_closed (has_scoped succ_has)] using h3
  have hzF := zeroY_form hc hY ha hu
  have hsF := stepY_form hc hY hg hu
  have huF := uniqueY_form hc hY hg ha hu
  exact ⟨_, appE hsF huF (appE hzF (form_arr hsF huF) h3' hz) hs⟩

theorem identity_transE {Γ : Tel} {Y : Ty} {x y z e d : Poly} (hc : Ctx Γ)
    (hY : Form Γ Y) (hx : Has Γ x Y) (hy : Has Γ y Y) (hz : Has Γ z Y)
    (he : HasE Γ e (.identity Y x y)) (hd : HasE Γ d (.identity Y y z)) :
    HasE Γ (jPoly e z d) (.identity Y x z) := by
  let P : Ty := .identity (wk Y) (pren Nat.succ x) (.var 0)
  have cy := Ctx.ext hc hY
  have yw := form_wk hY hc hY
  have xw := has_wk hx hc hY
  have hv : Has (Y :: Γ) (.var 0) (wk Y) := .var yw .zero
  have hP : Form (Y :: Γ) P := .identity yw xw hv
  have at_eq (v : Poly) : inst P v = .identity Y x v := by
    simp [P, inst, subst, subst_wk_cancel, pren, psub, psub_comp, cons, psub_id]
  have q := transport_source hc hY hP hy hz hd ((at_eq y).symm ▸ he)
  simpa only [at_eq] using q

def mappedFold (h f a : Poly) : Poly := abstract
  (.app (pren Nat.succ h) (.app (.app (.var 0) (pren Nat.succ f)) (pren Nat.succ a)))

theorem mappedFold_beta (h f a n : Poly) : P01DF.PolyConv
    (.app (mappedFold h f a) n) (.app h (.app (.app n f) a)) := by
  have q := poly_beta (.app (pren Nat.succ h)
    (.app (.app (.var 0) (pren Nat.succ f)) (pren Nat.succ a))) n
  simpa [mappedFold, psub, pren, psub_comp, cons, psub_id] using q

theorem mappedFold_ren (h f a : Poly) : pren Nat.succ (mappedFold h f a) =
    mappedFold (pren Nat.succ h) (pren Nat.succ f) (pren Nat.succ a) := by
  simp [mappedFold, pren, ← abstraction_naturality, psub, pup, psub_comp]

theorem mappedFold_has {Γ : Tel} {X Y : Ty} {h f a : Poly} (hc : Ctx Γ)
    (hX : Form Γ X) (hY : Form Γ Y) (hh : Has Γ h (arr X Y))
    (hf : Has Γ f (arr X X)) (ha : Has Γ a X) :
    Has Γ (mappedFold h f a) (arr N Y) := by
  have cn := Ctx.ext hc (N_form hc)
  have xw := form_wk hX hc (N_form hc)
  have yw := form_wk hY hc (N_form hc)
  have hw : Has (N :: Γ) (pren Nat.succ h) (arr (wk X) (wk Y)) := by
    simpa only [wk, subst_arr] using has_wk hh hc (N_form hc)
  have fw : Has (N :: Γ) (pren Nat.succ f) (arr (wk X) (wk X)) := by
    simpa only [wk, subst_arr] using has_wk hf hc (N_form hc)
  have aw := has_wk ha hc (N_form hc)
  have hn : Has (N :: Γ) (.var 0) N := .var (N_form cn) .zero
  have body := app_has (form_arr xw yw) yw hw (SourceFoldContract.fold_has cn xw hn fw aw)
  exact .piIntro (form_arr (N_form hc) hY) body (scoped_abstract (has_scoped body))

theorem mapped_zero {Γ : Tel} {X Y : Ty} {h f a : Poly} (hc : Ctx Γ)
    (hX : Form Γ X) (hY : Form Γ Y) (hh : Has Γ h (arr X Y))
    (hf : Has Γ f (arr X X)) (ha : Has Γ a X) :
    Has Γ ident (ZeroY Y (.app h a) (mappedFold h f a)) := by
  have hu := mappedFold_has hc hX hY hh hf ha
  have uz := app_has (form_arr (N_form hc) hY) hY hu (zero_has_N hc)
  have hha := app_has (form_arr hX hY) hY hh ha
  exact .identityIntro (.identity hY uz hha) uz hha
    ((mappedFold_beta _ _ _ _).trans (.app (.refl _) (zero_beta f a)))

theorem square_form {Γ : Tel} {X Y : Ty} {h f g : Poly} (hc : Ctx Γ)
    (hX : Form Γ X) (hY : Form Γ Y) (hh : Has Γ h (arr X Y))
    (hf : Has Γ f (arr X X)) (hg : Has Γ g (arr Y Y)) :
    Form (X :: Γ) (SourceFoldContract.squareType Y f g h) := by
  have cx := Ctx.ext hc hX
  have xw := form_wk hX hc hX
  have yw := form_wk hY hc hX
  have hw : Has (X :: Γ) (pren Nat.succ h) (arr (wk X) (wk Y)) := by
    simpa only [wk, subst_arr] using has_wk hh hc hX
  have fw : Has (X :: Γ) (pren Nat.succ f) (arr (wk X) (wk X)) := by
    simpa only [wk, subst_arr] using has_wk hf hc hX
  have gw : Has (X :: Γ) (pren Nat.succ g) (arr (wk Y) (wk Y)) := by
    simpa only [wk, subst_arr] using has_wk hg hc hX
  have x : Has (X :: Γ) (.var 0) (wk X) := .var xw .zero
  exact .identity yw
    (app_has (form_arr xw yw) yw hw (app_has (form_arr xw xw) xw fw x))
    (app_has (form_arr yw yw) yw gw (app_has (form_arr xw yw) yw hw x))

theorem square_at (Y : Ty) (f g h x : Poly) :
    inst (SourceFoldContract.squareType Y f g h) x =
      .identity Y (.app h (.app f x)) (.app g (.app h x)) := by
  simp [SourceFoldContract.squareType, inst, subst, subst_wk_cancel,
    pren, psub, psub_comp, psub_id, cons]

theorem square_apply {Γ : Tel} {X Y : Ty} {h f g e x : Poly} (hc : Ctx Γ)
    (hX : Form Γ X) (hY : Form Γ Y) (hh : Has Γ h (arr X Y))
    (hf : Has Γ f (arr X X)) (hg : Has Γ g (arr Y Y))
    (hs : HasE Γ e (.pi X (SourceFoldContract.squareType Y f g h)))
    (hx : Has Γ x X) :
    HasE Γ (.app e x) (.identity Y (.app h (.app f x)) (.app g (.app h x))) := by
  have hF := square_form hc hX hY hh hf hg
  have q := HasE.piElim (form_inclusion (.pi hX hF))
    (form_inclusion (form_inst_source hc hF hx)) hs (has_inclusion hx)
  simpa only [square_at] using q

theorem square_shift (X Y : Ty) (f g h : Poly) :
    wk (.pi X (SourceFoldContract.squareType Y f g h)) =
      .pi (wk X) (SourceFoldContract.squareType (wk Y)
        (pren Nat.succ f) (pren Nat.succ g) (pren Nat.succ h)) := by
  simp [SourceFoldContract.squareType, wk, subst, pren, psub, pup, subst_comp, psub_comp]

/-- Original endpoints; the square evidence may use every actual HasE rule.
    Only the separately certified HasE weakening lemma crosses the n binder. -/
theorem mapped_step {Γ : Tel} {X Y : Ty} {h f g a e : Poly} (hc : Ctx Γ)
    (hX : Form Γ X) (hY : Form Γ Y) (hh : Has Γ h (arr X Y))
    (hf : Has Γ f (arr X X)) (hg : Has Γ g (arr Y Y)) (ha : Has Γ a X)
    (hs : HasE Γ e (.pi X (SourceFoldContract.squareType Y f g h))) :
    ∃ s, HasE Γ s (StepY Y g (mappedFold h f a)) := by
  have cn := Ctx.ext hc (N_form hc)
  have xw := form_wk hX hc (N_form hc)
  have yw := form_wk hY hc (N_form hc)
  have hw : Has (N :: Γ) (pren Nat.succ h) (arr (wk X) (wk Y)) := by
    simpa only [wk, subst_arr] using has_wk hh hc (N_form hc)
  have fw : Has (N :: Γ) (pren Nat.succ f) (arr (wk X) (wk X)) := by
    simpa only [wk, subst_arr] using has_wk hf hc (N_form hc)
  have gw : Has (N :: Γ) (pren Nat.succ g) (arr (wk Y) (wk Y)) := by
    simpa only [wk, subst_arr] using has_wk hg hc (N_form hc)
  have aw := has_wk ha hc (N_form hc)
  have hn : Has (N :: Γ) (.var 0) N := .var (N_form cn) .zero
  have sn := app_has (form_arr (N_form cn) (N_form cn)) (N_form cn) (succ_has_NT cn) hn
  have sw : HasE (N :: Γ) (pren Nat.succ e)
      (.pi (wk X) (SourceFoldContract.squareType (wk Y)
        (pren Nat.succ f) (pren Nat.succ g) (pren Nat.succ h))) :=
    square_shift X Y f g h ▸ Structural.has_wk hs (ctx_inclusion hc) (form_inclusion (N_form hc))
  have fn := SourceFoldContract.fold_has cn xw hn fw aw
  have middle := square_apply cn xw yw hw fw gw sw fn
  have uw := mappedFold_has cn xw yw hw fw aw
  have un := app_has (form_arr (N_form cn) yw) yw uw hn
  have usn := app_has (form_arr (N_form cn) yw) yw uw sn
  have gun := app_has (form_arr yw yw) yw gw un
  have ffn := app_has (form_arr xw xw) xw fw fn
  have hfn := app_has (form_arr xw yw) yw hw fn
  have leftmiddle := app_has (form_arr xw yw) yw hw ffn
  have rightmiddle := app_has (form_arr yw yw) yw gw hfn
  have first : Has (N :: Γ) ident (.identity (wk Y)
      (.app (mappedFold (pren Nat.succ h) (pren Nat.succ f) (pren Nat.succ a))
        (.app succPoly (.var 0)))
      (.app (pren Nat.succ h) (.app (pren Nat.succ f)
        (.app (.app (.var 0) (pren Nat.succ f)) (pren Nat.succ a))))) :=
    .identityIntro (.identity yw usn leftmiddle) usn leftmiddle
      ((mappedFold_beta _ _ _ _).trans (.app (.refl _) (succ_beta _ _ _)))
  have last : Has (N :: Γ) ident (.identity (wk Y)
      (.app (pren Nat.succ g) (.app (pren Nat.succ h)
        (.app (.app (.var 0) (pren Nat.succ f)) (pren Nat.succ a))))
      (.app (pren Nat.succ g)
        (.app (mappedFold (pren Nat.succ h) (pren Nat.succ f) (pren Nat.succ a)) (.var 0)))) :=
    .identityIntro (.identity yw rightmiddle gun) rightmiddle gun
      (.app (.refl _) (mappedFold_beta _ _ _ _).symm)
  have body := identity_transE cn yw usn rightmiddle gun
    (identity_transE cn yw usn leftmiddle rightmiddle (has_inclusion first) middle) (has_inclusion last)
  have hu := mappedFold_has hc hX hY hh hf ha
  refine ⟨abstract _, HasE.piIntro (form_inclusion (stepY_form hc hY hg hu)) ?_
    (scoped_abstract (hasE_scoped body))⟩
  simpa only [mappedFold_ren] using body

/-- Pointwise elimination of literal internal uniqueness at any carrier. -/
theorem uniqueY_at {Γ : Tel} {Y : Ty} {g a u e n : Poly} (hc : Ctx Γ)
    (hY : Form Γ Y) (hg : Has Γ g (arr Y Y)) (ha : Has Γ a Y)
    (hu : Has Γ u (arr N Y)) (hn : Has Γ n N) (he : HasE Γ e (UniqueY Y g a u)) :
    HasE Γ (.app e n) (.identity Y (.app u n) (.app (.app n g) a)) := by
  have q := (apply_with_form hc (uniqueY_form hc hY hg ha hu) hn he).2
  simpa [UniqueY, inst, subst, subst_wk_cancel, pren, psub, psub_comp, psub_id, cons] using q

/-- Generic fold transport with an independently specified target seed.
    The rigidity, seed equation and commuting square all admit arbitrary actual
    HasE evidence. Carriers, algebra terms, map and numeral are original Has. -/
theorem fold_transport_from_rigidity {Γ : Tel} {X Y : Ty} {r n f g h a b seed square : Poly}
    (hc : Ctx Γ) (hX : Form Γ X) (hY : Form Γ Y)
    (hn : Has Γ n N) (hf : Has Γ f (arr X X)) (hg : Has Γ g (arr Y Y))
    (hh : Has Γ h (arr X Y)) (ha : Has Γ a X) (hb : Has Γ b Y)
    (hr : HasE Γ r Rigidity) (hseed : HasE Γ seed (.identity Y (.app h a) b))
    (hsquare : HasE (X :: Γ) square (SourceFoldContract.squareType Y f g h)) :
    ∃ e, HasE Γ e (.identity Y (.app h (.app (.app n f) a)) (.app (.app n g) b)) := by
  have hu := mappedFold_has hc hX hY hh hf ha
  have uz := app_has (form_arr (N_form hc) hY) hY hu (zero_has_N hc)
  have hha := app_has (form_arr hX hY) hY hh ha
  have zeroEvidence := identity_transE hc hY uz hha hb
    (has_inclusion (mapped_zero hc hX hY hh hf ha)) hseed
  have squareF := square_form hc hX hY hh hf hg
  have sq := HasE.piIntro (form_inclusion (.pi hX squareF)) hsquare
    (scoped_abstract (hasE_scoped hsquare))
  obtain ⟨s, stepEvidence⟩ := mapped_step hc hX hY hh hf hg ha sq
  have hw := uniqueness_from_rigidity hc hr
  obtain ⟨e, he⟩ := unique_at_carrier hc hY hw hg hb hu zeroEvidence stepEvidence
  have main := uniqueY_at hc hY hg hb hu hn he
  have un := app_has (form_arr (N_form hc) hY) hY hu hn
  have sourceFold := SourceFoldContract.fold_has hc hX hn hf ha
  have left := app_has (form_arr hX hY) hY hh sourceFold
  have right := SourceFoldContract.fold_has hc hY hn hg hb
  have link : Has Γ ident (.identity Y (.app h (.app (.app n f) a)) (.app (mappedFold h f a) n)) :=
    .identityIntro (.identity hY left un) left un (mappedFold_beta h f a n).symm
  exact ⟨_, identity_transE hc hY left un right (has_inclusion link) main⟩

/-- Exactly the retained SourceFoldContract conclusion and all of its original
    premises, with the one explicit additional Rigidity hypothesis. In
    particular the square is still arbitrary HasE in X::Γ, not original Has. -/
theorem source_naturality_from_rigidity {Γ : Tel} {X Y : Ty} {r n f g h a square : Poly}
    (hc : Ctx Γ) (hX : Form Γ X) (hY : Form Γ Y)
    (hn : Has Γ n N) (hf : Has Γ f (arr X X)) (hg : Has Γ g (arr Y Y))
    (hh : Has Γ h (arr X Y)) (ha : Has Γ a X)
    (hr : HasE Γ r Rigidity)
    (hsquare : HasE (X :: Γ) square (SourceFoldContract.squareType Y f g h)) :
    ∃ e, HasE Γ e (SourceFoldContract.foldType Y n f g h a) := by
  have hha := app_has (form_arr hX hY) hY hh ha
  have seed : Has Γ ident (.identity Y (.app h a) (.app h a)) :=
    .identityIntro (.identity hY hha hha) hha hha (.refl _)
  exact fold_transport_from_rigidity hc hX hY hn hf hg hh ha hha hr (has_inclusion seed) hsquare

/-- A named conditional contract preserves the exact earlier interface rather
    than redefining or asserting its premise-free SourceNaturality proposition. -/
def SourceNaturalityUnderRigidity : Prop :=
  ∀ {Γ : Tel} {X Y : Ty} {r n f g h a square : Poly},
    Ctx Γ → Form Γ X → Form Γ Y →
    Has Γ n N → Has Γ f (arr X X) → Has Γ g (arr Y Y) →
    Has Γ h (arr X Y) → Has Γ a X → HasE Γ r Rigidity →
    HasE (X :: Γ) square (SourceFoldContract.squareType Y f g h) →
    ∃ e, HasE Γ e (SourceFoldContract.foldType Y n f g h a)

theorem conditional_source_naturality : SourceNaturalityUnderRigidity :=
  source_naturality_from_rigidity

#print axioms unique_at_carrier
#print axioms mapped_step
#print axioms fold_transport_from_rigidity
#print axioms source_naturality_from_rigidity
#print axioms conditional_source_naturality
end RigidityPolymorphicTransfer
