import GenericFoldTransport
import GraphBridgeAssembly

namespace SourceFoldContract
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.InternalGraph.BridgeAssembly
open P01AC.ExtensionalRepair.CompilerBodyControl
open P01AC.Intensional.Plus (PolyConvPlus)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def squareType (B : Ty) (f g h : Poly) : Ty :=
  .identity (wk B)
    (.app (pren Nat.succ h) (.app (pren Nat.succ f) (.var 0)))
    (.app (pren Nat.succ g) (.app (pren Nat.succ h) (.var 0)))

def foldType (B : Ty) (n f g h a : Poly) : Ty :=
  .identity B (.app h (.app (.app n f) a))
    (.app (.app n g) (.app h a))

/-- The conclusion endpoints are formed in the unchanged source. -/
theorem fold_has {Γ : Tel} {X : Ty} {n f a : Poly}
    (hc : Ctx Γ) (hX : Form Γ X) (hn : Has Γ n N)
    (hf : Has Γ f (arr X X)) (ha : Has Γ a X) :
    Has Γ (.app (.app n f) a) X := by
  have he := form_arr hX hX
  have hn' : Has Γ n (arr (arr X X) (arr X X)) := by
    rw [← church_instantiate]
    exact .allElim (N_form hc) hX (by rw [church_instantiate]; exact form_arr he he) hn
  exact app_has he hX (app_has (form_arr he he) he hn' hf) ha

theorem fold_type_formed {Γ : Tel} {X Y : Ty} {n f g h a : Poly}
    (hc : Ctx Γ) (hX : Form Γ X) (hY : Form Γ Y)
    (hn : Has Γ n N) (hf : Has Γ f (arr X X)) (hg : Has Γ g (arr Y Y))
    (hh : Has Γ h (arr X Y)) (ha : Has Γ a X) :
    Form Γ (foldType Y n f g h a) :=
  .identity hY
    (app_has (form_arr hX hY) hY hh (fold_has hc hX hn hf ha))
    (fold_has hc hY hn hg (app_has (form_arr hX hY) hY hh ha))

/-- A proposed, reusable SOURCE-PROOF contract, not a new judgement or rule.
    Its antecedents and conclusion refer only to the actual unchanged syntax.
    All endpoint terms are already typed by the inherited Has fragment;
    the commuting square may have arbitrary HasE evidence. -/
def SourceNaturality : Prop :=
  ∀ {Γ : Tel} {X Y : Ty} {n f g h a square : Poly},
    Ctx Γ → Form Γ X → Form Γ Y →
    Has Γ n N → Has Γ f (arr X X) → Has Γ g (arr Y Y) →
    Has Γ h (arr X Y) → Has Γ a X →
    HasE (X :: Γ) square (squareType Y f g h) →
    ∃ e, HasE Γ e (foldType Y n f g h a)

/-- The proposed contract's conclusion has a uniform semantic I realizer in
    the inherited certified full-PER model, under its exact source premises.
    This is NOT a HasE proof and does not assert SourceNaturality. -/
theorem contract_semantically_valid {Γ : Tel} {X Y : Ty} {n f g h a square : Poly}
    (hc : Ctx Γ) (hX : Form Γ X) (hY : Form Γ Y)
    (hn : Has Γ n N) (hf : Has Γ f (arr X X)) (hg : Has Γ g (arr Y Y))
    (hh : Has Γ h (arr X Y)) (ha : Has Γ a X)
    (hsquare : HasE (X :: Γ) square (squareType Y f g h)) :
    FullPER.Fundamental Γ (.atom .i) (foldType Y n f g h a) := by
  intro ρ η ξ r e
  have c := FullPER.context_sound (ctx_inclusion hc)
  have d := (c.ends r e).1
  have ee := c.refl r d
  let XP := (FullPER.formation_per (form_inclusion hX) r d).object
  let YP := (FullPER.formation_per (form_inclusion hY) r d).object
  have nn := FullPER.fundamental (has_inclusion hn) ρ η η r ee
  have ff := FullPER.fundamental (has_inclusion hf) ρ η η r ee
  have gg := FullPER.fundamental (has_inclusion hg) ρ η η r ee
  have hhm := FullPER.fundamental (has_inclusion hh) ρ η η r ee
  have aa := FullPER.fundamental (has_inclusion ha) ρ η η r ee
  rw [FullPER.F_arr] at ff gg hhm
  have sq : GenericFoldTransport.Commutes XP YP
      (ImportedOpenTermTransport.interp f η) (ImportedOpenTermTransport.interp g η)
      (ImportedOpenTermTransport.interp h η) := by
    intro x xx
    have ex : FullPER.E (X :: Γ) ρ (FullPER.cons x η) (FullPER.cons x η) := ⟨ee,xx⟩
    have v := FullPER.fundamental hsquare ρ _ _ r ex
    change FullPER.F (wk Y) ρ (FullPER.cons x η)
      (ImportedOpenTermTransport.interp _ (FullPER.cons x η))
      (ImportedOpenTermTransport.interp _ (FullPER.cons x η)) ∧ _ at v
    simpa only [FullPER.F_wk, FullPER.interp_app, FullPER.interp_ren,
      FullPER.interp_var, FullPER.cons] using v.1
  exact ⟨GenericFoldTransport.fold_transport XP YP nn ff gg hhm aa sq,
    .refl _, .refl _⟩

/-- The ordinary encoded state observer. No graph carrier is introduced. -/
def imageMap (f a : Poly) : Poly :=
  abstract (image (pren Nat.succ f) (pren Nat.succ a) (.var 0))

theorem imageMap_beta (f a s : Poly) :
    P01DF.PolyConv (.app (imageMap f a) s) (image f a s) := by
  have v := poly_beta (image (pren Nat.succ f) (pren Nat.succ a) (.var 0)) s
  simpa [imageMap, image, sndPoly, psub, pren, psub_comp, cons] using v

theorem imageMap_has {Γ : Tel} (hc : Ctx Γ) {f a : Poly}
    (hf : Has Γ f End) (ha : Has Γ a A) : Has Γ (imageMap f a) (arr S A) := by
  have hS := S_form hc
  have c1 := Ctx.ext hc hS
  have hf1 : Has (S :: Γ) (pren Nat.succ f) End := has_wk hf hc hS
  have ha1 : Has (S :: Γ) (pren Nat.succ a) A := has_wk ha hc hS
  have hs1 : Has (S :: Γ) (.var 0) S := .var (S_form c1) .zero
  have hb := image_has c1 hf1 ha1 hs1
  exact .piIntro (form_arr hS (.param hc)) hb (scoped_abstract (has_scoped hb))

theorem imageMap_square (f a s : Poly) : P01DF.PolyConv
    (.app (imageMap f a) (.app diagonalStep s))
    (.app f (.app (imageMap f a) s)) :=
  (imageMap_beta f a _).trans ((image_delta f a s).trans
    (.app (.refl f) (imageMap_beta f a s).symm))

theorem imageMap_seed (f a : Poly) :
    P01DF.PolyConv (.app (imageMap f a) diagonalZero) a :=
  (imageMap_beta f a _).trans (image_zero f a)

/-- Every premise of the proposed square is proved in the old source. -/
theorem actual_square_has {Γ : Tel} (hc : Ctx Γ) {f a : Poly}
    (hf : Has Γ f End) (ha : Has Γ a A) :
    HasE (S :: Γ) (.atom .i) (squareType A diagonalStep f (imageMap f a)) := by
  have hS := S_form hc
  have c1 := Ctx.ext hc hS
  have hf1 : Has (S :: Γ) (pren Nat.succ f) End := has_wk hf hc hS
  have hm1 : Has (S :: Γ) (pren Nat.succ (imageMap f a)) (arr S A) :=
    has_wk (imageMap_has hc hf ha) hc hS
  have hd1 : Has (S :: Γ) (pren Nat.succ diagonalStep) (arr S S) :=
    has_wk (delta_has hc) hc hS
  have hs1 : Has (S :: Γ) (.var 0) S := .var (S_form c1) .zero
  have hd := app_has (form_arr (S_form c1) (S_form c1)) (S_form c1) hd1 hs1
  have hl := app_has (form_arr (S_form c1) (.param c1)) (.param c1) hm1 hd
  have him := app_has (form_arr (S_form c1) (.param c1)) (.param c1) hm1 hs1
  have hr := app_has (form_arr (.param c1) (.param c1)) (.param c1) hf1 him
  have hconv := imageMap_square (pren Nat.succ f) (pren Nat.succ a) (.var 0)
  have delta_closed : pren Nat.succ diagonalStep = diagonalStep :=
    ExactScalarFusion.pren_closed (has_scoped (delta_has Ctx.nil)) _
  have map_ren : pren Nat.succ (imageMap f a) =
      imageMap (pren Nat.succ f) (pren Nat.succ a) := by
    simp [imageMap, image, sndPoly, pren, ← abstraction_naturality, psub, pup, psub_comp]
  apply has_inclusion
  apply Has.identityIntro (Form.identity (.param c1) hl hr) hl hr
  simpa only [delta_closed, map_ren] using hconv

#print axioms contract_semantically_valid
#print axioms imageMap_has
#print axioms actual_square_has
#print axioms imageMap_seed
end SourceFoldContract
