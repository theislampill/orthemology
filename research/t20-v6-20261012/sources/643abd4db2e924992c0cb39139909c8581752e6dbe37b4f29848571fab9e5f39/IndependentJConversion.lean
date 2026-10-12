import IndependentMixedControls
namespace HasEMixedReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.Structural
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def sourceCtx : Tel := [.param 0]
theorem source_ctx : CtxE sourceCtx := .ext .nil (.param .nil)
theorem source_x : HasE sourceCtx (.var 0) (.param 0) :=
  .var (.param source_ctx) .zero

theorem j_input : HasE sourceCtx (jPoly (.var 0) (.var 0) (.atom .i)) (.param 0) := by
  have ha : FormE sourceCtx (.param 0) := .param source_ctx
  have hid := FormE.identity ha source_x source_x
  have he := HasE.identityIntro hid source_x source_x (Intensional.Plus.PolyConvPlus.refl _)
  exact .j ha (B := .param 0) (.param (ctx_theta source_ctx ha source_x))
    hid ha ha source_x source_x he source_x

def paddedJ : Poly := .app (.app (.atom .k) (jPoly (.var 0) (.var 0) (.atom .i))) (.atom .i)
theorem conv_j_input : HasE sourceCtx paddedJ (.param 0) :=
  .conv (.param source_ctx) j_input
    (Intensional.Plus.PolyConvPlus.k _ _).symm
    ⟨⟨trivial, has_scoped j_input⟩, trivial⟩

theorem nonrenaming_mixed_map : Structural.MixedSubstitution sourceCtx rawCtx
    (fun _ => .atom .i) (fun _ => depImage) := by
  constructor
  · exact fun _ => dep_image_formed
  · intro n A hn
    cases hn with
    | zero =>
      have hv : HasE rawCtx (.var 0) .raw := .var (.raw raw_ctx) .zero
      exact .identityIntro dep_image_formed hv hv (.refl _)
    | succ h => cases h

theorem mixed_j_conversion : HasE rawCtx
    (.app (.app (.atom .k) (jPoly (.atom .i) (.atom .i) (.atom .i))) (.atom .i))
    depImage := by
  exact has_mixed conv_j_input raw_ctx nonrenaming_mixed_map

#print axioms mixed_j_conversion
end HasEMixedReview
