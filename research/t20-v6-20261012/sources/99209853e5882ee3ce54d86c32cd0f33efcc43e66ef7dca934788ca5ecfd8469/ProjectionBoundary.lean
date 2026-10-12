import InternalGraph

namespace P01AC.ExtensionalRepair.InternalGraph
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair.CompilerBodyControl
open P01AC.Intensional.Plus (PolyConvPlus)
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

def scalarContext : Tel := [A, End, N]
def stateRun (n : Poly) : Poly := .app (.app n diagonalStep) diagonalZero
def stateTransport : Ty := .identity S
  (fstPoly (graphRun (.var 2) (.var 1) (.var 0))) (stateRun (.var 2))
def scalarTransport : Ty := .identity A
  (fstPoly (sndPoly (graphRun (.var 2) (.var 1) (.var 0))))
  (.app (.app (.var 2) (.var 1)) (.var 0))

theorem scalar_context_formed : Ctx scalarContext := ExactScalarFusion.scalar_context Ctx.nil

theorem n_has : Has scalarContext (.var 2) N :=
  .var (N_form scalar_context_formed) (.succ (.succ .zero))
theorem f_has : Has scalarContext (.var 1) End :=
  .var (form_arr (.param scalar_context_formed) (.param scalar_context_formed)) (.succ .zero)
theorem a_has : Has scalarContext (.var 0) A := .var (.param scalar_context_formed) .zero

theorem state_run_has {Γ : Tel} (hc : Ctx Γ) {n : Poly} (hn : Has Γ n N) :
    Has Γ (stateRun n) S := by
  have hs := S_form hc
  have he := form_arr hs hs
  have hn' : Has Γ n (arr (arr S S) (arr S S)) := by
    rw [← church_instantiate]
    exact .allElim (N_form hc) hs (by rw [church_instantiate]; exact form_arr he he) hn
  exact app_has he hs (app_has (form_arr he he) he hn' (delta_has hc)) (zero_has hc)

theorem state_transport_formed : FormE scalarContext stateTransport :=
  form_inclusion (.identity (S_form scalar_context_formed)
    (graph_state_has scalar_context_formed f_has a_has
      (graph_run_has scalar_context_formed n_has f_has a_has))
    (state_run_has scalar_context_formed n_has))

theorem scalar_transport_formed : FormE scalarContext scalarTransport :=
  form_inclusion (.identity (.param scalar_context_formed)
    (graph_scalar_has scalar_context_formed f_has a_has
      (graph_run_has scalar_context_formed n_has f_has a_has))
    (ExactScalarFusion.scalar_n_has scalar_context_formed n_has f_has a_has))

theorem literal_graph_invariant :
    HasE scalarContext (sndPoly (sndPoly (graphRun (.var 2) (.var 1) (.var 0))))
      (.identity A (fstPoly (sndPoly (graphRun (.var 2) (.var 1) (.var 0))))
        (image (.var 1) (.var 0) (fstPoly (graphRun (.var 2) (.var 1) (.var 0))))) :=
  iterated_invariant scalar_context_formed n_has f_has a_has

theorem original_scalar_computation (n f a : Poly) : P01DF.PolyConv
    (.app (.app (.app P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed n) f) a)
    (image f a (stateRun n)) := by
  rw [redundant_closed_exact]
  have h := poly_beta literalPairStateBody n
  have hd : Scoped 0 diagonalStep := has_scoped (delta_has Ctx.nil)
  have hz : Scoped 0 diagonalZero := has_scoped (zero_has Ctx.nil)
  have h' : P01DF.PolyConv (.app (abstract literalPairStateBody) n)
      (sndPoly (stateRun n)) := by
    simpa [literalPairStateBody, stateRun, sndPoly, psub, cons,
      P01AC.BooleanPrimitive.psub_closed hd, P01AC.BooleanPrimitive.psub_closed hz] using h
  exact .app (.app h' (.refl f)) (.refl a)


theorem lifted_step_beta (f a z : Poly) : P01DF.PolyConv
    (.app (liftedStep f a) z) (stepBody f a z) := by
  have h := poly_beta (stepBody (pren Nat.succ f) (pren Nat.succ a) (.var 0)) z
  simpa [liftedStep, stepBody, stepProof, image, pairPoly, fstPoly, sndPoly,
    jPoly, psub, pren, psub_comp, cons,
    P01AC.BooleanPrimitive.psub_closed (has_scoped (delta_has Ctx.nil))] using h

theorem state_step_commutes (f a z : Poly) : P01DF.PolyConv
    (fstPoly (.app (liftedStep f a) z)) (.app diagonalStep (fstPoly z)) :=
  (P01DF.PolyConv.app (lifted_step_beta f a z) (.refl _)).trans (pair_first _ _)

theorem scalar_step_commutes (f a z : Poly) : P01DF.PolyConv
    (fstPoly (sndPoly (.app (liftedStep f a) z)))
    (.app f (fstPoly (sndPoly z))) :=
  (P01DF.PolyConv.app
    ((P01DF.PolyConv.app (lifted_step_beta f a z) (.refl _)).trans (pair_second _ _))
    (.refl _)).trans (pair_first _ _)

theorem state_seed_commutes (f a : Poly) :
    P01DF.PolyConv (fstPoly (graphSeed f a)) diagonalZero := pair_first _ _

theorem image_zero (f a : Poly) : P01DF.PolyConv (image f a diagonalZero) a := by
  have hz : inputNumeral 0 = .app (.atom .k) (.atom .i) := by
    simp [inputNumeral, iterationPoly, abstract, freeZero, drop, pren, psub]
  exact (P01DF.PolyConv.app (.app (pair_second _ _) (.refl f)) (.refl a)).trans
    (hz ▸ ((P01DF.PolyConv.app (.k _ _) (.refl a)).trans (.i _)))

theorem scalar_seed_commutes (f a : Poly) :
    P01DF.PolyConv (fstPoly (sndPoly (graphSeed f a))) a :=
  ((P01DF.PolyConv.app (pair_second _ _) (.refl _)).trans (pair_first _ _)).trans
    (image_zero f a)

/-- An untyped raw valuation used only to refute a raw conversion shortcut.
    It is not claimed to inhabit the Church context. -/
def badN : Term := .app .k (.app .k .i)
def badEnv : Env := cons .i (cons .i (cons badN zeroEnv))

theorem bad_n_result (b c : Term) : Conv (.app (.app badN b) c) .i :=
  (Conv.left (.step (.k (.app .k .i) b)) c).trans (.step (.k .i c))

theorem bad_graph_result :
    Conv (eval (graphRun (.var 2) (.var 1) (.var 0)) badEnv) .i :=
  bad_n_result _ _

theorem bad_state_result : Conv (eval (stateRun (.var 2)) badEnv) .i :=
  bad_n_result _ _

theorem bad_graph_first :
    Conv (eval (fstPoly (graphRun (.var 2) (.var 1) (.var 0))) badEnv) .k :=
  (bad_graph_result.left .k).trans (.step (.i .k))

theorem k_not_i : ¬ Conv .k .i := by
  intro h
  have hnK : P01Source.Normal .k := by intro u hu; cases hu
  have hnI : P01Source.Normal .i := by intro u hu; cases hu
  cases P01Source.normal_unique hnK hnI h

/-- The first projection equation cannot be discharged by identityIntro's
    conversion premise. This is not noninhabitation of stateTransport. -/
theorem state_projection_not_conversion :
    ¬ PolyConvPlus (fstPoly (graphRun (.var 2) (.var 1) (.var 0))) (stateRun (.var 2)) := by
  intro h
  exact k_not_i (bad_graph_first.symm.trans
    ((Intensional.Plus.polyConvPlus_sound h badEnv).trans bad_state_result))


def badScalarN : Term := .app .k (.app .k .k)
def badScalarEnv : Env := cons .i (cons .i (cons badScalarN zeroEnv))

theorem bad_scalar_n_result (b c : Term) : Conv (.app (.app badScalarN b) c) .k :=
  (Conv.left (.step (.k (.app .k .k) b)) c).trans (.step (.k .k c))

theorem bad_graph_scalar_result :
    Conv (eval (fstPoly (sndPoly (graphRun (.var 2) (.var 1) (.var 0)))) badScalarEnv)
      (.app .k .i) :=
  (((bad_scalar_n_result _ _).left (.app .k .i)).left .k).trans
    (.step (.k (.app .k .i) .k))

theorem ki_not_k : ¬ Conv (.app .k .i) .k := by
  intro h
  have hnKI : P01Source.Normal (.app .k .i) := by
    intro u hu; cases hu with
    | left h _ => cases h
    | right _ h => cases h
  have hnK : P01Source.Normal .k := by intro u hu; cases hu
  cases P01Source.normal_unique hnKI hnK h

/-- The scalar projection equation has its own countervaluation; neither
    missing projection transport can be obtained by raw conversion. -/
theorem scalar_projection_not_conversion :
    ¬ PolyConvPlus (fstPoly (sndPoly (graphRun (.var 2) (.var 1) (.var 0))))
      (.app (.app (.var 2) (.var 1)) (.var 0)) := by
  intro h
  exact ki_not_k (bad_graph_scalar_result.symm.trans
    ((Intensional.Plus.polyConvPlus_sound h badScalarEnv).trans (bad_scalar_n_result _ _)))

#print axioms state_step_commutes
#print axioms scalar_step_commutes
#print axioms scalar_seed_commutes
#print axioms state_transport_formed
#print axioms scalar_transport_formed
#print axioms literal_graph_invariant
#print axioms original_scalar_computation
#print axioms state_projection_not_conversion
#print axioms scalar_projection_not_conversion
end P01AC.ExtensionalRepair.InternalGraph
