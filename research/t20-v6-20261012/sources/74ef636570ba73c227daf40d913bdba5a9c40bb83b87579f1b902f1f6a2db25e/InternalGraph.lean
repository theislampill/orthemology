import ScalarFusionCore
import UArrowAndCompilerControls
import ExtensionalRepairSoundness

namespace P01AC.ExtensionalRepair.InternalGraph
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair.CompilerBodyControl
open P01AC.Intensional.Plus (PolyConvPlus)
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

abbrev A : Ty := .param 0
abbrev End : Ty := arr A A

def image (f a s : Poly) : Poly := .app (.app (sndPoly s) f) a
/-- The graph's independent state and scalar coordinates are connected by identity. -/
def Graph (f a : Poly) : Ty := .sigma S
  (.sigma A (.identity A (.var 0)
    (image (pren (fun k => k+2) f) (pren (fun k => k+2) a) (.var 1))))
def pack (f a s : Poly) : Poly := pairPoly s (pairPoly (image f a s) (.atom .i))

theorem image_has {Γ : Tel} (hc : Ctx Γ) {f a s : Poly}
    (hf : Has Γ f End) (ha : Has Γ a A) (hs : Has Γ s S) :
    Has Γ (image f a s) A :=
  ExactScalarFusion.scalar_n_has hc (.sigmaSnd (S_form hc) (N_form hc) hs) hf ha

theorem graph_form {Γ : Tel} (hc : Ctx Γ) {f a : Poly}
    (hf : Has Γ f End) (ha : Has Γ a A) : Form Γ (Graph f a) := by
  have c1 : Ctx (S :: Γ) := .ext hc (S_form hc)
  have c2 : Ctx (A :: S :: Γ) := .ext c1 (.param c1)
  have hf2 : Has (A :: S :: Γ) (pren (fun k => k+2) f) End := by
    simpa only [wk, subst, A, End, arr, pren, psub_comp, psub] using
      (has_wk (has_wk hf hc (S_form hc)) c1 (show Form (S :: Γ) A from .param c1))
  have ha2 : Has (A :: S :: Γ) (pren (fun k => k+2) a) A := by
    simpa only [wk, subst, A, pren, psub_comp, psub] using
      (has_wk (has_wk ha hc (S_form hc)) c1 (show Form (S :: Γ) A from .param c1))
  exact .sigma (S_form hc) (.sigma (.param c1)
    (.identity (.param c2) (.var (.param c2) .zero)
      (image_has c2 hf2 ha2 (.var (S_form c2) (.succ .zero)))))

 theorem graph_inst (f a s : Poly) :
    inst (.sigma A (.identity A (.var 0)
      (image (pren (fun k => k+2) f) (pren (fun k => k+2) a) (.var 1)))) s =
    .sigma A (.identity A (.var 0)
      (image (pren Nat.succ f) (pren Nat.succ a) (pren Nat.succ s))) := by
  simp [inst, subst, image, sndPoly, psub, pup, cons, pren, psub_comp]

 theorem graph_leaf_inst (f a s x : Poly) :
    inst (.identity A (.var 0)
      (image (pren Nat.succ f) (pren Nat.succ a) (pren Nat.succ s))) x =
    .identity A x (image f a s) := by
  simp [inst, subst, image, sndPoly, psub, cons, pren, psub_comp]

theorem pack_has {Γ : Tel} (hc : Ctx Γ) {f a s : Poly}
    (hf : Has Γ f End) (ha : Has Γ a A) (hs : Has Γ s S) :
    Has Γ (pack f a s) (Graph f a) := by
  have him := image_has hc hf ha hs
  have c1 : Ctx (A :: Γ) := .ext hc (.param hc)
  have hi1 := has_wk him hc (show Form Γ A from .param hc)
  have hp : Form Γ (.sigma A (.identity A (.var 0)
      (image (pren Nat.succ f) (pren Nat.succ a) (pren Nat.succ s)))) := by
    apply Form.sigma (.param hc)
    apply Form.identity (.param c1) (.var (.param c1) .zero)
    simpa only [pren, psub, image, sndPoly, wk, subst] using hi1
  have hid : Form Γ (.identity A (image f a s) (image f a s)) :=
    .identity (.param hc) him him
  apply Has.sigmaIntro (graph_form hc hf ha)
  · rw [graph_inst]; exact hp
  · exact hs
  · rw [graph_inst]
    apply Has.sigmaIntro hp
    · rw [graph_leaf_inst]; exact hid
    · exact him
    · rw [graph_leaf_inst]
      exact .identityIntro hid him him (.refl _)



theorem sub_absent (p : Poly) (h : freeZero p = false) (a : Poly) :
    psub (cons a Poly.var) p = drop p := by
  induction p with
  | var n => cases n <;> simp_all [freeZero, drop, pren, psub, cons]
  | atom t => rfl
  | app f x hf hx =>
      have hs : freeZero f = false ∧ freeZero x = false := by
        simpa only [freeZero, Bool.or_eq_false_iff] using h
      exact congrArg₂ Poly.app (hf hs.1) (hx hs.2)

theorem poly_beta (p a : Poly) :
    P01DF.PolyConv (.app (abstract p) a) (psub (cons a Poly.var) p) := by
  induction p with
  | var n =>
      cases n with
      | zero => simpa [abstract, freeZero, cons, psub] using P01DF.PolyConv.i a
      | succ n =>
        simpa [abstract, freeZero, drop, pren, psub, cons] using
          P01DF.PolyConv.k (.var n) a
  | atom t =>
      simpa [abstract, freeZero, drop, pren, psub] using P01DF.PolyConv.k (.atom t) a
  | app f x hf hx =>
      by_cases h : freeZero (.app f x) = true
      · simp only [abstract, h, Bool.true_eq, ↓reduceIte, psub]
        exact (P01DF.PolyConv.s _ _ a).trans (.app hf hx)
      · have h' : freeZero (.app f x) = false := Bool.eq_false_of_not_eq_true h
        rw [sub_absent (.app f x) h' a]
        simp only [abstract, h', Bool.false_eq_true, ↓reduceIte]
        exact .k _ a

theorem pair_apply (x y k : Poly) :
    P01DF.PolyConv (.app (pairPoly x y) k) (.app (.app k x) y) := by
  unfold pairPoly
  exact (P01DF.PolyConv.s _ _ _).trans
    (.app ((P01DF.PolyConv.s _ _ _).trans (.app (.i _) (.k _ _))) (.k _ _))

theorem pair_first (x y : Poly) : P01DF.PolyConv (fstPoly (pairPoly x y)) x :=
  (pair_apply x y (.atom .k)).trans (.k _ _)
theorem pair_second (x y : Poly) : P01DF.PolyConv (sndPoly (pairPoly x y)) y :=
  (pair_apply x y (.app (.atom .k) (.atom .i))).trans
    ((P01DF.PolyConv.app (.k _ _) (.refl _)).trans (.i _))

theorem delta_has {Γ : Tel} (hc : Ctx Γ) : Has Γ diagonalStep (arr S S) := by
  have hS := S_form hc
  have c1 : Ctx (S :: Γ) := .ext hc hS
  have hs : Has (S :: Γ) (.var 0) S := .var (S_form c1) .zero
  have hf : Has (S :: Γ) (fstPoly (.var 0)) N := .sigmaFst (N_form c1) (S_form c1) hs
  have ht : Has (S :: Γ) (sndPoly (.var 0)) N := .sigmaSnd (S_form c1) (N_form c1) hs
  have hsucc : Has (S :: Γ) succPoly (arr N N) :=
    closed_has succ_has (fun _ => rfl) c1
  have hb : Has (S :: Γ) diagonalStepBody S := .sigmaIntro (S_form c1) (N_form c1)
    (app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hsucc hf)
    (app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hsucc ht)
  exact .piIntro (form_arr hS hS) hb (scoped_abstract (has_scoped hb))

theorem zero_has {Γ : Tel} (hc : Ctx Γ) : Has Γ diagonalZero S := by
  have hz := closed_has (inputNumeral_has 0) N_subst hc
  exact .sigmaIntro (S_form hc) (N_form hc) hz hz

theorem delta_beta (s : Poly) : P01DF.PolyConv (.app diagonalStep s)
    (pairPoly (.app succPoly (fstPoly s)) (.app succPoly (sndPoly s))) := by
  have h := poly_beta diagonalStepBody s
  simpa [diagonalStep, diagonalStepBody, psub, pairPoly, fstPoly, sndPoly,
    P01AC.BooleanPrimitive.psub_closed (has_scoped succ_has), cons] using h

theorem succ_beta (n f a : Poly) : P01DF.PolyConv
    (.app (.app (.app succPoly n) f) a) (.app f (.app (.app n f) a)) := by
  have h1 := poly_beta (abstract (abstract succBody)) n
  have h2 := poly_beta (psub (pup (cons n Poly.var)) (abstract succBody)) f
  have h3 := poly_beta
    (psub (pup (cons f Poly.var)) (psub (pup (pup (cons n Poly.var))) succBody)) a
  simp only [← abstraction_naturality] at h1 h2
  have h := (P01DF.PolyConv.app (.app h1 (.refl f)) (.refl a)).trans
    ((P01DF.PolyConv.app h2 (.refl a)).trans h3)
  simpa [succPoly, ← abstraction_naturality, succBody, psub, pup, cons, pren, psub_comp] using h

theorem image_delta (f a s : Poly) : P01DF.PolyConv
    (image f a (.app diagonalStep s)) (.app f (image f a s)) := by
  exact (P01DF.PolyConv.app (.app
    ((P01DF.PolyConv.app (delta_beta s) (.refl _)).trans (pair_second _ _))
    (.refl f)) (.refl a)).trans (succ_beta _ _ _)

-- Based J gives ordinary congruence inside this grammar.
theorem congr_app_has {Γ : Tel} (hc : Ctx Γ) {f x y e : Poly}
    (hf : Has Γ f End) (hx : Has Γ x A) (hy : Has Γ y A)
    (he : Has Γ e (.identity A x y)) :
    Has Γ (jPoly (.atom .i) y e) (.identity A (.app f x) (.app f y)) := by
  let M : Ty := .identity A
    (.app (pren (fun k => k+2) f) (pren (fun k => k+2) x))
    (.app (pren (fun k => k+2) f) (.var 1))
  have hA : Form Γ A := .param hc
  have c1 : Ctx (A :: Γ) := .ext hc hA
  have hP := form_theta_head hc hA hx
  have ct : Ctx (theta Γ A x) := ctx_theta hc hA hx
  have hf2 : Has (theta Γ A x) (pren (fun k => k+2) f) End := by
    simpa only [wk, subst, A, End, arr, pren, psub_comp, psub] using
      (has_wk (has_wk hf hc hA) c1 hP)
  have hx2 : Has (theta Γ A x) (pren (fun k => k+2) x) A := by
    simpa only [wk, subst, A, pren, psub_comp, psub] using
      (has_wk (has_wk hx hc hA) c1 hP)
  have hM : Form (theta Γ A x) M := .identity (.param ct)
    (app_has (form_arr (.param ct) (.param ct)) (.param ct) hf2 hx2)
    (app_has (form_arr (.param ct) (.param ct)) (.param ct) hf2
      (.var (.param ct) (.succ .zero)))
  have at_eq (v r : Poly) : motiveAt M v r =
      .identity A (.app f x) (.app f v) := by
    simp [motiveAt, M, subst, pren, psub, psub_comp, cons]
  have hfx := app_has (form_arr hA hA) hA hf hx
  have hfy := app_has (form_arr hA hA) hA hf hy
  have base : Form Γ (motiveAt M x (.atom .i)) := by
    rw [at_eq]; exact .identity hA hfx hfx
  have target : Form Γ (motiveAt M y e) := by
    rw [at_eq]; exact .identity hA hfx hfy
  have d : Has Γ (.atom .i) (motiveAt M x (.atom .i)) := by
    rw [at_eq]; exact .identityIntro (.identity hA hfx hfx) hfx hfx (.refl _)
  simpa only [at_eq] using (Has.j hA hM (.identity hA hx hy) base target hx hy he d)

theorem trans_has {Γ : Tel} (hc : Ctx Γ) {x y z e d : Poly}
    (hx : Has Γ x A) (hy : Has Γ y A) (hz : Has Γ z A)
    (he : Has Γ e (.identity A x y)) (hd : Has Γ d (.identity A y z)) :
    Has Γ (jPoly e z d) (.identity A x z) := by
  let M : Ty := .identity A (pren (fun k => k+2) x) (.var 1)
  have hA : Form Γ A := .param hc
  have c1 : Ctx (A :: Γ) := .ext hc hA
  have hP := form_theta_head hc hA hy
  have ct : Ctx (theta Γ A y) := ctx_theta hc hA hy
  have hx2 : Has (theta Γ A y) (pren (fun k => k+2) x) A := by
    simpa only [wk, subst, A, pren, psub_comp, psub] using
      (has_wk (has_wk hx hc hA) c1 hP)
  have hM : Form (theta Γ A y) M :=
    .identity (.param ct) hx2 (.var (.param ct) (.succ .zero))
  have at_eq (v r : Poly) : motiveAt M v r = .identity A x v := by
    simp [motiveAt, M, subst, pren, psub, psub_comp, cons]
  have base : Form Γ (motiveAt M y (.atom .i)) := by
    rw [at_eq]; exact .identity hA hx hy
  have target : Form Γ (motiveAt M z d) := by
    rw [at_eq]; exact .identity hA hx hz
  have baseproof : Has Γ e (motiveAt M y (.atom .i)) := by rw [at_eq]; exact he
  simpa only [at_eq] using
    (Has.j hA hM (.identity hA hy hz) base target hy hz hd baseproof)


theorem fibre_form {Γ : Tel} (hc : Ctx Γ) {f a s : Poly}
    (hf : Has Γ f End) (ha : Has Γ a A) (hs : Has Γ s S) :
    Form Γ (.sigma A (.identity A (.var 0)
      (image (pren Nat.succ f) (pren Nat.succ a) (pren Nat.succ s)))) := by
  have c1 : Ctx (A :: Γ) := .ext hc (.param hc)
  apply Form.sigma (.param hc)
  apply Form.identity (.param c1) (.var (.param c1) .zero)
  simpa only [pren, psub, image, sndPoly, wk, subst] using
    (has_wk (image_has hc hf ha hs) hc (show Form Γ A from .param hc))

theorem graph_pair_has {Γ : Tel} (hc : Ctx Γ) {f a s x e : Poly}
    (hf : Has Γ f End) (ha : Has Γ a A) (hs : Has Γ s S)
    (hx : Has Γ x A) (he : Has Γ e (.identity A x (image f a s))) :
    Has Γ (pairPoly s (pairPoly x e)) (Graph f a) := by
  have hp := fibre_form hc hf ha hs
  have hid := Form.identity (Form.param hc) hx (image_has hc hf ha hs)
  apply Has.sigmaIntro (graph_form hc hf ha)
  · rw [graph_inst]; exact hp
  · exact hs
  · rw [graph_inst]
    apply Has.sigmaIntro hp
    · rw [graph_leaf_inst]; exact hid
    · exact hx
    · rw [graph_leaf_inst]; exact he

theorem graph_state_has {Γ : Tel} (hc : Ctx Γ) {f a z : Poly}
    (hf : Has Γ f End) (ha : Has Γ a A) (hz : Has Γ z (Graph f a)) :
    Has Γ (fstPoly z) S := .sigmaFst (S_form hc) (graph_form hc hf ha) hz

theorem graph_rest_has {Γ : Tel} (hc : Ctx Γ) {f a z : Poly}
    (hf : Has Γ f End) (ha : Has Γ a A) (hz : Has Γ z (Graph f a)) :
    Has Γ (sndPoly z) (.sigma A (.identity A (.var 0)
      (image (pren Nat.succ f) (pren Nat.succ a) (pren Nat.succ (fstPoly z))))) := by
  have hs := graph_state_has hc hf ha hz
  have hp := fibre_form hc hf ha hs
  have h := Has.sigmaSnd (graph_form hc hf ha)
    (show Form Γ (inst _ (fstPoly z)) from (graph_inst f a (fstPoly z)) ▸ hp) hz
  simpa only [graph_inst] using h

theorem graph_scalar_has {Γ : Tel} (hc : Ctx Γ) {f a z : Poly}
    (hf : Has Γ f End) (ha : Has Γ a A) (hz : Has Γ z (Graph f a)) :
    Has Γ (fstPoly (sndPoly z)) A :=
  .sigmaFst (.param hc) (fibre_form hc hf ha (graph_state_has hc hf ha hz))
    (graph_rest_has hc hf ha hz)

theorem graph_proof_has {Γ : Tel} (hc : Ctx Γ) {f a z : Poly}
    (hf : Has Γ f End) (ha : Has Γ a A) (hz : Has Γ z (Graph f a)) :
    Has Γ (sndPoly (sndPoly z))
      (.identity A (fstPoly (sndPoly z)) (image f a (fstPoly z))) := by
  have hs := graph_state_has hc hf ha hz
  have hx := graph_scalar_has hc hf ha hz
  have hp := fibre_form hc hf ha hs
  have hid := Form.identity (Form.param hc) hx (image_has hc hf ha hs)
  have h := Has.sigmaSnd hp
    (show Form Γ (inst _ (fstPoly (sndPoly z))) from
      (graph_leaf_inst f a (fstPoly z) (fstPoly (sndPoly z))) ▸ hid)
    (graph_rest_has hc hf ha hz)
  simpa only [graph_leaf_inst] using h

/-- Congruence followed by the exact original step computation. -/
def stepProof (f a z : Poly) : Poly :=
  jPoly (jPoly (.atom .i) (image f a (fstPoly z)) (sndPoly (sndPoly z)))
    (image f a (.app diagonalStep (fstPoly z))) (.atom .i)
def stepBody (f a z : Poly) : Poly :=
  pairPoly (.app diagonalStep (fstPoly z))
    (pairPoly (.app f (fstPoly (sndPoly z))) (stepProof f a z))
def liftedStep (f a : Poly) : Poly :=
  abstract (stepBody (pren Nat.succ f) (pren Nat.succ a) (.var 0))

theorem strong_step_body_has {Γ : Tel} (hc : Ctx Γ) {f a z : Poly}
    (hf : Has Γ f End) (ha : Has Γ a A) (hz : Has Γ z (Graph f a)) :
    Has Γ (stepBody f a z) (Graph f a) := by
  have hs := graph_state_has hc hf ha hz
  have hx := graph_scalar_has hc hf ha hz
  have he := graph_proof_has hc hf ha hz
  have hi := image_has hc hf ha hs
  have hd := app_has (form_arr (S_form hc) (S_form hc)) (S_form hc) (delta_has hc) hs
  have hit := image_has hc hf ha hd
  have hfx := app_has (form_arr (.param hc) (.param hc)) (.param hc) hf hx
  have hfi := app_has (form_arr (.param hc) (.param hc)) (.param hc) hf hi
  have hcongr := congr_app_has hc hf hx hi he
  have hcalc : Has Γ (.atom .i)
      (.identity A (.app f (image f a (fstPoly z)))
        (image f a (.app diagonalStep (fstPoly z)))) :=
    .identityIntro (.identity (.param hc) hfi hit) hfi hit (image_delta f a _).symm
  exact graph_pair_has hc hf ha hd hfx
    (trans_has hc hfx hfi hit hcongr hcalc)

theorem graph_wk (f a : Poly) :
    wk (Graph f a) = Graph (pren Nat.succ f) (pren Nat.succ a) := by
  simp [wk, Graph, S, N, NBody, arr, subst, image, sndPoly, pren, psub,
    pup, psub_comp]

theorem strong_step_has {Γ : Tel} (hc : Ctx Γ) {f a : Poly}
    (hf : Has Γ f End) (ha : Has Γ a A) :
    Has Γ (liftedStep f a) (arr (Graph f a) (Graph f a)) := by
  have hg := graph_form hc hf ha
  have c1 : Ctx (Graph f a :: Γ) := .ext hc hg
  have hf1 : Has (Graph f a :: Γ) (pren Nat.succ f) End := has_wk hf hc hg
  have ha1 : Has (Graph f a :: Γ) (pren Nat.succ a) A := has_wk ha hc hg
  have hv : Has (Graph f a :: Γ) (.var 0)
      (Graph (pren Nat.succ f) (pren Nat.succ a)) := by
    rw [← graph_wk]
    exact .var (form_wk hg hc hg) .zero
  have hb := strong_step_body_has c1 hf1 ha1 hv
  have hb' : Has (Graph f a :: Γ)
      (stepBody (pren Nat.succ f) (pren Nat.succ a) (.var 0)) (wk (Graph f a)) := by
    rw [graph_wk]; exact hb
  exact .piIntro (form_arr hg hg) hb' (scoped_abstract (has_scoped hb'))

def graphSeed (f a : Poly) : Poly := pack f a diagonalZero
def graphRun (n f a : Poly) : Poly := .app (.app n (liftedStep f a)) (graphSeed f a)

theorem graph_seed_has {Γ : Tel} (hc : Ctx Γ) {f a : Poly}
    (hf : Has Γ f End) (ha : Has Γ a A) : Has Γ (graphSeed f a) (Graph f a) :=
  pack_has hc hf ha (zero_has hc)

theorem church_instantiate (G : Ty) : tinst NBody G = arr (arr G G) (arr G G) := by
  simp [NBody, tinst, tsubst, fin, mixed, arr, wk, subst, cons, tup, subst_comp, psub, pup, pren]

theorem graph_run_has {Γ : Tel} (hc : Ctx Γ) {n f a : Poly}
    (hn : Has Γ n N) (hf : Has Γ f End) (ha : Has Γ a A) :
    Has Γ (graphRun n f a) (Graph f a) := by
  have hg := graph_form hc hf ha
  have he := form_arr hg hg
  have hn' : Has Γ n (arr (arr (Graph f a) (Graph f a)) (arr (Graph f a) (Graph f a))) := by
    rw [← church_instantiate]
    exact .allElim (N_form hc) hg (by rw [church_instantiate]; exact form_arr he he) hn
  exact app_has he hg (app_has (form_arr he he) he hn' (strong_step_has hc hf ha))
    (graph_seed_has hc hf ha)

theorem iterated_invariant {Γ : Tel} (hc : Ctx Γ) {n f a : Poly}
    (hn : Has Γ n N) (hf : Has Γ f End) (ha : Has Γ a A) :
    HasE Γ (sndPoly (sndPoly (graphRun n f a)))
      (.identity A (fstPoly (sndPoly (graphRun n f a)))
        (image f a (fstPoly (graphRun n f a)))) :=
  has_inclusion (graph_proof_has hc hf ha (graph_run_has hc hn hf ha))

#print axioms strong_step_has
#print axioms iterated_invariant
#print axioms pack_has
#print axioms congr_app_has
#print axioms trans_has
end P01AC.ExtensionalRepair.InternalGraph
