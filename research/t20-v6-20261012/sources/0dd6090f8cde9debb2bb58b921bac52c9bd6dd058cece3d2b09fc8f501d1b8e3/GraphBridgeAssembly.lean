/- Conditional assembly only: neither projection bridge is inhabited here. -/
import ProjectionBoundary
import Application

namespace P01AC.ExtensionalRepair.InternalGraph.BridgeAssembly
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair.CompilerBodyControl
open P01AC.Intensional.Plus (PolyConvPlus)
open FullPER.Application (originalQ)
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

/-- Congruence for the actual state observer. Its identity evidence is HasE,
    while the old endpoint typings suffice to form the two-coordinate motive. -/
theorem image_congr_hasE {Γ : Tel} (hc : Ctx Γ) {f a s t e : Poly}
    (hf : Has Γ f End) (ha : Has Γ a A) (hs : Has Γ s S) (ht : Has Γ t S)
    (he : HasE Γ e (.identity S s t)) :
    HasE Γ (jPoly (.atom .i) t e) (.identity A (image f a s) (image f a t)) := by
  let M : Ty := .identity A
    (image (pren (fun k => k+2) f) (pren (fun k => k+2) a) (pren (fun k => k+2) s))
    (image (pren (fun k => k+2) f) (pren (fun k => k+2) a) (.var 1))
  have hS := S_form hc
  have c1 : Ctx (S :: Γ) := .ext hc hS
  have hP := form_theta_head hc hS hs
  have ct : Ctx (theta Γ S s) := ctx_theta hc hS hs
  have hf2 : Has (theta Γ S s) (pren (fun k => k+2) f) End := by
    simpa only [wk, subst, A, End, arr, pren, psub_comp, psub] using
      (has_wk (has_wk hf hc hS) c1 hP)
  have ha2 : Has (theta Γ S s) (pren (fun k => k+2) a) A := by
    simpa only [wk, subst, A, pren, psub_comp, psub] using
      (has_wk (has_wk ha hc hS) c1 hP)
  have hs2 : Has (theta Γ S s) (pren (fun k => k+2) s) S := by
    simpa only [wk, subst, S, N, NBody, arr, pren, psub_comp, psub] using
      (has_wk (has_wk hs hc hS) c1 hP)
  have hv : Has (theta Γ S s) (.var 1) S :=
    .var (S_form ct) (.succ .zero)
  have hM : Form (theta Γ S s) M :=
    .identity (.param ct) (image_has ct hf2 ha2 hs2) (image_has ct hf2 ha2 hv)
  have at_eq (v r : Poly) : motiveAt M v r =
      .identity A (image f a s) (image f a v) := by
    simp [motiveAt, M, subst, image, sndPoly, pren, psub, psub_comp, cons]
  have his := image_has hc hf ha hs
  have hit := image_has hc hf ha ht
  have base : Form Γ (motiveAt M s (.atom .i)) := by
    rw [at_eq]; exact .identity (.param hc) his his
  have target : Form Γ (motiveAt M t e) := by
    rw [at_eq]; exact .identity (.param hc) his hit
  have d : Has Γ (.atom .i) (motiveAt M s (.atom .i)) := by
    rw [at_eq]; exact .identityIntro (.identity (.param hc) his his) his his (.refl _)
  simpa only [at_eq] using (HasE.j (form_inclusion hS) (form_inclusion hM)
    (form_inclusion (.identity hS hs ht)) (form_inclusion base) (form_inclusion target)
    (has_inclusion hs) (has_inclusion ht) he (has_inclusion d))

/-- Composition with arbitrary HasE identity proofs, not just included Has proofs. -/
theorem trans_hasE {Γ : Tel} (hc : Ctx Γ) {x y z e d : Poly}
    (hx : Has Γ x A) (hy : Has Γ y A) (hz : Has Γ z A)
    (he : HasE Γ e (.identity A x y)) (hd : HasE Γ d (.identity A y z)) :
    HasE Γ (jPoly e z d) (.identity A x z) := by
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
  have baseproof : HasE Γ e (motiveAt M y (.atom .i)) := by rw [at_eq]; exact he
  simpa only [at_eq] using
    (HasE.j (form_inclusion hA) (form_inclusion hM)
      (form_inclusion (.identity hA hy hz)) (form_inclusion base) (form_inclusion target)
      (has_inclusion hy) (has_inclusion hz) hd baseproof)

/-- Transport the first endpoint along a HasE identity. -/
theorem replace_left_hasE {Γ : Tel} (hc : Ctx Γ) {x y z e d : Poly}
    (hx : Has Γ x A) (hy : Has Γ y A) (hz : Has Γ z A)
    (he : HasE Γ e (.identity A x z)) (hd : HasE Γ d (.identity A x y)) :
    HasE Γ (jPoly e y d) (.identity A y z) := by
  let M : Ty := .identity A (.var 1) (pren (fun k => k+2) z)
  have hA : Form Γ A := .param hc
  have c1 : Ctx (A :: Γ) := .ext hc hA
  have hP := form_theta_head hc hA hx
  have ct : Ctx (theta Γ A x) := ctx_theta hc hA hx
  have hz2 : Has (theta Γ A x) (pren (fun k => k+2) z) A := by
    simpa only [wk, subst, A, pren, psub_comp, psub] using
      (has_wk (has_wk hz hc hA) c1 hP)
  have hM : Form (theta Γ A x) M :=
    .identity (.param ct) (.var (.param ct) (.succ .zero)) hz2
  have at_eq (v r : Poly) : motiveAt M v r = .identity A v z := by
    simp [motiveAt, M, subst, pren, psub, psub_comp, cons]
  have base : Form Γ (motiveAt M x (.atom .i)) := by
    rw [at_eq]; exact .identity hA hx hz
  have target : Form Γ (motiveAt M y d) := by
    rw [at_eq]; exact .identity hA hy hz
  have baseproof : HasE Γ e (motiveAt M x (.atom .i)) := by rw [at_eq]; exact he
  simpa only [at_eq] using
    (HasE.j (form_inclusion hA) (form_inclusion hM)
      (form_inclusion (.identity hA hx hy)) (form_inclusion base) (form_inclusion target)
      (has_inclusion hx) (has_inclusion hy) hd baseproof)

/-- A typed J construction followed by checked conversion, not inversion from
    a raw normal form. The supplied identity remains an indispensable premise. -/
theorem identity_i_hasE {Γ : Tel} (hc : Ctx Γ) {x y e : Poly}
    (hx : Has Γ x A) (hy : Has Γ y A)
    (he : HasE Γ e (.identity A x y)) : HasE Γ (.atom .i) (.identity A x y) := by
  have hr : Has Γ (.atom .i) (.identity A x x) :=
    .identityIntro (.identity (.param hc) hx hx) hx hx (.refl _)
  have hj := trans_hasE hc hx hx hy (has_inclusion hr) he
  exact .conv (form_inclusion (.identity (.param hc) hx hy)) hj
    (ExactScalarFusion.j_conversion (.atom .i) y e) trivial

/-- The explicit witness assembled from the two arbitrary bridge proof terms. -/
def assembledProof (stateEvidence scalarEvidence : Poly) : Poly :=
  let r := graphRun (.var 2) (.var 1) (.var 0)
  let stateImage := image (.var 1) (.var 0) (stateRun (.var 2))
  let qImage := ExactScalarFusion.scalarR originalQ
  jPoly (jPoly (jPoly (sndPoly (sndPoly r)) stateImage
    (jPoly (.atom .i) (stateRun (.var 2)) stateEvidence)) qImage (.atom .i))
    ExactScalarFusion.scalarL scalarEvidence

theorem original_q_has : Has [] originalQ ExactScalarFusion.T :=
  P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed_has

/-- The original scalar leaf follows conditionally from the two bridge judgements. -/
theorem scalar_leaf_from_bridges {stateEvidence scalarEvidence : Poly}
    (hs : HasE scalarContext stateEvidence stateTransport)
    (hx : HasE scalarContext scalarEvidence scalarTransport) :
    HasE scalarContext (assembledProof stateEvidence scalarEvidence)
      (ExactScalarFusion.Leaf originalQ) := by
  have hc := scalar_context_formed
  have hr := graph_run_has hc n_has f_has a_has
  have hs0 := graph_state_has hc f_has a_has hr
  have hs1 := state_run_has hc n_has
  have hx0 := graph_scalar_has hc f_has a_has hr
  have him0 := image_has hc f_has a_has hs0
  have him1 := image_has hc f_has a_has hs1
  have hl := ExactScalarFusion.scalar_n_has hc n_has f_has a_has
  have hq := ExactScalarFusion.closed_has_T original_q_has hc
  have hqn := app_has (ExactScalarFusion.T_form hc) (N_form hc) hq n_has
  have hqr := ExactScalarFusion.scalar_n_has hc hqn f_has a_has
  have him := image_congr_hasE hc f_has a_has hs0 hs1 hs
  have first := trans_hasE hc hx0 him0 him1 literal_graph_invariant him
  have comp : Has scalarContext (.atom .i)
      (.identity A (image (.var 1) (.var 0) (stateRun (.var 2)))
        (ExactScalarFusion.scalarR originalQ)) :=
    .identityIntro (.identity (.param hc) him1 hqr) him1 hqr
      (original_scalar_computation (.var 2) (.var 1) (.var 0)).symm
  have second := trans_hasE hc hx0 him1 hqr first (has_inclusion comp)
  exact replace_left_hasE hc hx0 hl hqr second hx

/-- Exact I witness for the literal leaf, obtained by typed J and conversion. -/
theorem scalar_leaf_i_from_bridges {stateEvidence scalarEvidence : Poly}
    (hs : HasE scalarContext stateEvidence stateTransport)
    (hx : HasE scalarContext scalarEvidence scalarTransport) :
    HasE scalarContext ExactScalarFusion.i (ExactScalarFusion.Leaf originalQ) := by
  have hc := scalar_context_formed
  have hl := ExactScalarFusion.scalar_n_has hc n_has f_has a_has
  have hq := ExactScalarFusion.closed_has_T original_q_has hc
  have hqn := app_has (ExactScalarFusion.T_form hc) (N_form hc) hq n_has
  have hqr := ExactScalarFusion.scalar_n_has hc hqn f_has a_has
  exact identity_i_hasE hc hl hqr (scalar_leaf_from_bridges hs hx)

/-- Conditional literal scalar-fusion assembly. The original q, W and c3 are
    unchanged, and both unproved HasE bridge judgements remain explicit premises. -/
theorem scalar_fusion_from_bridges {stateEvidence scalarEvidence : Poly}
    (hs : HasE scalarContext stateEvidence stateTransport)
    (hx : HasE scalarContext scalarEvidence scalarTransport) :
    HasE [] ExactScalarFusion.c3 (ExactScalarFusion.W originalQ) := by
  have hw := ExactScalarFusion.W_form original_q_has Ctx.nil
  have h0 : Ctx [N] := .ext .nil (N_form .nil)
  have h1 : Ctx [End, N] := .ext h0 (form_arr (.param h0) (.param h0))
  have hleaf : Form [A, End, N] (ExactScalarFusion.Leaf originalQ) :=
    ExactScalarFusion.scalar_leaf_form Ctx.nil
      (ExactScalarFusion.closed_has_T original_q_has scalar_context_formed)
  have hfam := Form.pi (show Form [End, N] A from .param h1) hleaf
  have hffam := Form.pi (form_arr (.param h0) (.param h0)) hfam
  exact .piIntro (form_inclusion hw) (.allIntro (form_inclusion (.all h0 hffam))
    (.piIntro (form_inclusion hffam)
      (.piIntro (form_inclusion hfam) (scalar_leaf_i_from_bridges hs hx)
        (scoped_abstract trivial))
      (scoped_abstract (scoped_abstract trivial)))) (ExactScalarFusion.c3_scoped 0)

#print axioms image_congr_hasE
#print axioms trans_hasE
#print axioms replace_left_hasE
#print axioms identity_i_hasE
#print axioms scalar_leaf_from_bridges
#print axioms scalar_leaf_i_from_bridges
#print axioms scalar_fusion_from_bridges
#check @scalar_fusion_from_bridges
end P01AC.ExtensionalRepair.InternalGraph.BridgeAssembly
