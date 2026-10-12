import SourceFoldContract

namespace SourceFoldContract
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.InternalGraph
open P01AC.ExtensionalRepair.InternalGraph.BridgeAssembly
open P01AC.ExtensionalRepair.CompilerBodyControl
open FullPER.Application (originalQ)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Exact original scalar leaf from a GENERIC naturality proof contract.
    The graph invariant and its two missing projection transports are unused. -/
theorem scalar_leaf_from_naturality (naturality : SourceNaturality) :
    HasE scalarContext ExactScalarFusion.i (ExactScalarFusion.Leaf originalQ) := by
  have hc := scalar_context_formed
  have hmap := imageMap_has hc f_has a_has
  have hrun := state_run_has hc n_has
  have himrun := app_has (form_arr (S_form hc) (.param hc)) (.param hc) hmap hrun
  have hseed := app_has (form_arr (S_form hc) (.param hc)) (.param hc) hmap (zero_has hc)
  have hnseed := ExactScalarFusion.scalar_n_has hc n_has f_has hseed
  have hl := ExactScalarFusion.scalar_n_has hc n_has f_has a_has
  have hq := ExactScalarFusion.closed_has_T original_q_has hc
  have hqn := app_has (ExactScalarFusion.T_form hc) (N_form hc) hq n_has
  have hqr := ExactScalarFusion.scalar_n_has hc hqn f_has a_has
  obtain ⟨e, he⟩ := naturality hc (S_form hc) (show Form scalarContext A from .param hc)
    n_has (delta_has hc) f_has hmap (zero_has hc) (actual_square_has hc f_has a_has)
  have seed_eq : Has scalarContext (.atom .i)
      (.identity A
        (.app (.app (.var 2) (.var 1)) (.app (imageMap (.var 1) (.var 0)) diagonalZero))
        ExactScalarFusion.scalarL) :=
    .identityIntro (.identity (.param hc) hnseed hl) hnseed hl
      (.app (.refl _) (imageMap_seed (.var 1) (.var 0)))
  have first := trans_hasE hc himrun hnseed hl he (has_inclusion seed_eq)
  have q_eq : Has scalarContext (.atom .i)
      (.identity A (.app (imageMap (.var 1) (.var 0)) (stateRun (.var 2)))
        (ExactScalarFusion.scalarR originalQ)) :=
    .identityIntro (.identity (.param hc) himrun hqr) himrun hqr
      ((imageMap_beta (.var 1) (.var 0) _).trans
        (original_scalar_computation (.var 2) (.var 1) (.var 0)).symm)
  have leaf := replace_left_hasE hc himrun hl hqr (has_inclusion q_eq) first
  exact identity_i_hasE hc hl hqr leaf

/-- Conditional source sufficiency, keeping the exact original q, W and c3. -/
theorem original_W_from_naturality (naturality : SourceNaturality) :
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
      (.piIntro (form_inclusion hfam) (scalar_leaf_from_naturality naturality)
        (scoped_abstract trivial))
      (scoped_abstract (scoped_abstract trivial)))) (ExactScalarFusion.c3_scoped 0)

#print axioms scalar_leaf_from_naturality
#print axioms original_W_from_naturality
end SourceFoldContract
