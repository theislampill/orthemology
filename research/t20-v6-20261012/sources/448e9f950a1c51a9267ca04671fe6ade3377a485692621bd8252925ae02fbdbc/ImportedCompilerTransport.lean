import UArrowAndCompilerControls
import PERInterface

/- Additive imported-source transport. The original definitions are imported,
   never copied into this namespace or modified. This proves no HasE soundness. -/
namespace ImportedOpenTermTransport
open OpenTermStandardness
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def embed : OrthemologyV2.Term → T
  | .i => .i
  | .k => .k
  | .s => .s
  | .zero => .zero
  | .one => .one
  | .app f a => .app (embed f) (embed a)

/-- A retraction to the inherited raw carrier, sending fresh generators to zero. -/
def erase : T → OrthemologyV2.Term
  | .var _ => .zero
  | .i => .i
  | .k => .k
  | .s => .s
  | .zero => .zero
  | .one => .one
  | .app f a => .app (erase f) (erase a)

theorem erase_embed (t : OrthemologyV2.Term) : erase (embed t) = t := by
  induction t with
  | i | k | s | zero | one => rfl
  | app f a ihf iha => simp only [embed, erase, ihf, iha]

theorem embed_injective : Function.Injective embed := by
  intro t u h
  have h' := congrArg erase h
  simpa only [erase_embed] using h'

def poly : P01D.Poly → P
  | .var n => .var n
  | .atom t => .atom (embed t)
  | .app f a => .app (poly f) (poly a)

theorem map_psub (p : P01D.Poly) (σ : Nat → P01D.Poly) :
    poly (P01D.psub σ p) = psub (fun n => poly (σ n)) (poly p) := by
  induction p with
  | var n => rfl
  | atom t => rfl
  | app f a ihf iha => simp only [P01D.psub, poly, psub, ihf, iha]

theorem map_freeZero (p : P01D.Poly) : freeZero (poly p) = P01D.freeZero p := by
  induction p with
  | var n => rfl
  | atom t => rfl
  | app f a ihf iha => simp only [poly, freeZero, P01D.freeZero, ihf, iha]

theorem map_drop (p : P01D.Poly) : poly (P01D.drop p) = drop (poly p) := by
  exact map_psub p (fun n => .var (Nat.pred n))

theorem map_abstract (p : P01D.Poly) : poly (P01D.abstract p) = abstract (poly p) := by
  induction p with
  | var n => cases n <;> simp [P01D.abstract, P01D.freeZero, poly, abstract, freeZero,
      P01D.drop, P01D.pren, P01D.psub, drop, pren, psub, embed]
  | atom t => simp [P01D.abstract, P01D.freeZero, poly, abstract, freeZero,
      P01D.drop, P01D.pren, P01D.psub, drop, pren, psub, embed]
  | app f a ihf iha =>
      by_cases h : P01D.freeZero (.app f a) = true
      · have h' : freeZero (.app (poly f) (poly a)) = true := (map_freeZero _).trans h
        rw [P01D.abstract.eq_def, abstract.eq_def]
        simp only [h, h', Bool.true_eq, ↓reduceIte, poly, embed, ihf, iha]
      · have h' : ¬ freeZero (.app (poly f) (poly a)) = true := by
          change ¬ freeZero (poly (.app f a)) = true
          rw [map_freeZero]; exact h
        rw [P01D.abstract.eq_def, abstract.eq_def]
        simp only [h, h', Bool.false_eq_true, ↓reduceIte, poly, embed, map_drop]

theorem map_eval (p : P01D.Poly) (η : P01D.Env) :
    eval (poly p) (fun n => embed (η n)) = embed (P01D.eval p η) := by
  induction p with
  | var n => rfl
  | atom t => rfl
  | app f a ihf iha => simp only [poly, eval, P01D.eval, embed, ihf, iha]

def interp (p : P01D.Poly) (η : Nat → T) : T := eval (poly p) η

/-- Original K-priority abstraction interpreted at arbitrary open-term valuations. -/
theorem interp_abstraction_beta (p : P01D.Poly) (η : Nat → T) (a : T) :
    Conv (interp (P01D.abstract p) η ⬝ a) (interp p (cons a η)) := by
  unfold interp
  rw [map_abstract]
  exact abstraction_beta _ _ _

theorem source_step_sound {t u : OrthemologyV2.Term} (h : OrthemologyV2.Step t u) :
    Conv (embed t) (embed u) := by
  induction h with
  | i x => exact .i _
  | k x y => exact .k _ _
  | s f g x => exact .s _ _ _
  | left h x ih => exact .app ih (.refl _)
  | right f h ih => exact .app (.refl _) ih

theorem source_conv_sound {t u : OrthemologyV2.Term} (h : OrthemologyV3.Conv t u) :
    Conv (embed t) (embed u) := by
  induction h with
  | refl t => exact .refl _
  | step h => exact source_step_sound h
  | symm h ih => exact ih.symm
  | trans h h' ih ih' => exact ih.trans ih'

theorem erase_conv {t u : T} (h : Conv t u) :
    OrthemologyV3.Conv (erase t) (erase u) := by
  induction h with
  | refl t => exact .refl _
  | symm h ih => exact ih.symm
  | trans h h' ih ih' => exact ih.trans ih'
  | app h h' ih ih' => exact P01D.conv_app ih ih'
  | i x => exact .step (.i _)
  | k x y => exact .step (.k _ _)
  | s f g x => exact .step (.s _ _ _)

/-- Adding fresh generators changes no conversion between embedded source terms. -/
theorem embed_conversion_iff (t u : OrthemologyV2.Term) :
    Conv (embed t) (embed u) ↔ OrthemologyV3.Conv t u := by
  constructor
  · intro h
    simpa only [erase_embed] using erase_conv h
  · exact source_conv_sound

/-- All eight actual source conversion generators, including atom packing. -/
theorem source_plus_sound {p r : P01D.Poly}
    (h : P01AC.Intensional.Plus.PolyConvPlus p r) (η : Nat → T) :
    Conv (interp p η) (interp r η) := by
  induction h with
  | refl p => exact .refl _
  | symm h ih => exact ih.symm
  | trans h h' ih ih' => exact ih.trans ih'
  | app h h' ih ih' => exact .app ih ih'
  | i p => exact .i _
  | k p r => exact .k _ _
  | s p r q => exact .s _ _ _
  | bridge r t => exact .refl _

/-- This equality imports the original compiler's literal-body theorem. -/
theorem original_q_poly_exact :
    poly P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed = qPoly := by
  rw [P01AC.ExtensionalRepair.CompilerBodyControl.redundant_closed_exact, map_abstract]
  simp [P01AC.ExtensionalRepair.CompilerBodyControl.literalPairStateBody,
    P01AC.ExtensionalRepair.CompilerBodyControl.diagonalStep,
    P01AC.ExtensionalRepair.CompilerBodyControl.diagonalStepBody,
    P01AC.ExtensionalRepair.CompilerBodyControl.diagonalZero,
    P01AC.BooleanPrimitive.succPoly, P01AC.BooleanPrimitive.succBody,
    P01AC.EffectiveCompleteness.inputNumeral, P01AC.EffectiveCompleteness.iterationPoly,
    P01D.pairPoly, P01D.fstPoly, P01D.sndPoly, poly, embed, map_abstract,
    qPoly, literalPairStateBody, diagonalStep, diagonalStepBody, diagonalZero,
    pairPoly, fstPoly, sndPoly, succPoly, succBody, inputNumeral, iterationPoly]

theorem original_p_poly_exact :
    poly P01AC.UnaryIdentity.IntensionalBoundary.variableExpr.closed = .atom .i := by
  rw [P01AC.ExtensionalRepair.CompilerBodyControl.variable_closed_exact]
  rfl

theorem q_eval_independent (η : Nat → T) : eval qPoly η = q := by
  simp [q, qPoly, literalPairStateBody, diagonalStep, diagonalStepBody, diagonalZero,
    pairPoly, fstPoly, sndPoly, succPoly, succBody, inputNumeral, iterationPoly,
    abstract, freeZero, drop, pren, psub, eval]

theorem original_q_eval_exact (η : P01D.Env) :
    embed (P01D.eval P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed η) = q := by
  rw [← map_eval, original_q_poly_exact]
  exact q_eval_independent _

theorem original_p_eval_exact (η : P01D.Env) :
    embed (P01D.eval P01AC.UnaryIdentity.IntensionalBoundary.variableExpr.closed η) = .i := by
  rw [← map_eval, original_p_poly_exact]
  rfl

/-- Actual imported source endpoints, at the new reduct's exact N-to-N relation.
    This is a semantic transport theorem, not a HasE derivation. -/
theorem original_endpoints_related (η : P01D.Env) :
    (arrowPER churchPER churchPER).rel
      (embed (P01D.eval P01AC.UnaryIdentity.IntensionalBoundary.variableExpr.closed η))
      (embed (P01D.eval P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed η)) := by
  rw [original_p_eval_exact, original_q_eval_exact]
  exact identity_q_related

/-- Typed endpoint agreement does not collapse the known raw inequality. -/
theorem original_raw_endpoints_still_distinct :
    ¬ Conv
      (embed (P01D.eval P01AC.UnaryIdentity.IntensionalBoundary.variableExpr.closed P01AC.zeroEnv))
      (embed (P01D.eval P01AC.UnaryIdentity.IntensionalBoundary.redundantExpr.closed P01AC.zeroEnv)) := by
  intro h
  exact P01AC.UnaryIdentity.IntensionalBoundary.endpoints_not_convertible
    ((embed_conversion_iff _ _).mp h)

#print axioms embed_injective
#print axioms embed_conversion_iff
#print axioms original_raw_endpoints_still_distinct
#print axioms map_abstract
#print axioms source_plus_sound
#print axioms original_q_poly_exact
#print axioms original_endpoints_related
end ImportedOpenTermTransport
