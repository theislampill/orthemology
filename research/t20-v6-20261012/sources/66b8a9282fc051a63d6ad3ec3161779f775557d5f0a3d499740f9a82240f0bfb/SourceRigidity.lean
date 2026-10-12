import SourceFoldApplication
import RecursorUniqueness

namespace SourceRigidity
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

abbrev NT : Ty := arr N N
abbrev ident : Poly := .atom .i
abbrev zero : Poly := inputNumeral 0

def ZeroAt (u : Poly) : Ty := .identity N (.app u zero) zero

def StepAt (u : Poly) : Ty := .pi N (.identity N
  (.app (pren Nat.succ u) (.app succPoly (.var 0)))
  (.app succPoly (.app (pren Nat.succ u) (.var 0))))

def ResultAt (u : Poly) : Ty := .identity NT ident u

/-- Endomorphism rigidity of the Church zero/successor algebra. It quantifies
    over every endomorphism u, and does not mention the compiler or W. -/
def Rigidity : Ty := .pi NT
  (arr (ZeroAt (.var 0)) (arr (StepAt (.var 0)) (ResultAt (.var 0))))

theorem zero_has_N {Γ : Tel} (hc : Ctx Γ) : Has Γ zero N :=
  closed_has (inputNumeral_has 0) N_subst hc

theorem succ_has_NT {Γ : Tel} (hc : Ctx Γ) : Has Γ succPoly NT :=
  closed_has succ_has (fun _ => rfl) hc

theorem zeroAt_formed {Γ : Tel} (hc : Ctx Γ) {u : Poly} (hu : Has Γ u NT) :
    Form Γ (ZeroAt u) :=
  .identity (N_form hc)
    (app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) hu (zero_has_N hc))
    (zero_has_N hc)

theorem stepAt_formed {Γ : Tel} (hc : Ctx Γ) {u : Poly} (hu : Has Γ u NT) :
    Form Γ (StepAt u) := by
  have c1 := Ctx.ext hc (N_form hc)
  have hu1 : Has (N :: Γ) (pren Nat.succ u) NT := has_wk hu hc (N_form hc)
  have hn : Has (N :: Γ) (.var 0) N := .var (N_form c1) .zero
  have hs := succ_has_NT c1
  have sn := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hs hn
  have un := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hu1 hn
  exact .pi (N_form hc) (.identity (N_form c1)
    (app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hu1 sn)
    (app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hs un))

theorem resultAt_formed {Γ : Tel} (hc : Ctx Γ) {u : Poly} (hu : Has Γ u NT) :
    Form Γ (ResultAt u) :=
  .identity (form_arr (N_form hc) (N_form hc)) (ExactScalarFusion.i_T hc) hu

theorem rigidity_formed {Γ : Tel} (hc : Ctx Γ) : Form Γ Rigidity := by
  have hT := form_arr (N_form hc) (N_form hc)
  have c1 := Ctx.ext hc hT
  have hu : Has (NT :: Γ) (.var 0) NT :=
    .var (form_arr (N_form c1) (N_form c1)) .zero
  exact .pi hT (form_arr (zeroAt_formed c1 hu)
    (form_arr (stepAt_formed c1 hu) (resultAt_formed c1 hu)))

theorem q_beta (n : Poly) : P01DF.PolyConv
    (.app originalQ n) (sndPoly (stateRun n)) := by
  unfold originalQ
  rw [redundant_closed_exact]
  have h := poly_beta literalPairStateBody n
  have hd : Scoped 0 diagonalStep := has_scoped (delta_has Ctx.nil)
  have hz : Scoped 0 diagonalZero := has_scoped (zero_has Ctx.nil)
  simpa [literalPairStateBody, stateRun, sndPoly, psub, cons,
    P01AC.BooleanPrimitive.psub_closed hd, P01AC.BooleanPrimitive.psub_closed hz] using h

theorem zero_beta (f a : Poly) : P01DF.PolyConv (.app (.app zero f) a) a := by
  have hz : zero = .app (.atom .k) (.atom .i) := by
    simp [zero, inputNumeral, iterationPoly, abstract, freeZero, drop, pren, psub]
  rw [hz]
  exact (P01DF.PolyConv.app (.k _ _) (.refl _)).trans (.i _)

theorem q_preserves_zero : P01DF.PolyConv (.app originalQ zero) zero :=
  (q_beta zero).trans ((P01DF.PolyConv.app (zero_beta diagonalStep diagonalZero) (.refl _)).trans
    (P01AC.ExtensionalRepair.InternalGraph.pair_second _ _))

theorem q_preserves_succ (n : Poly) : P01DF.PolyConv
    (.app originalQ (.app succPoly n)) (.app succPoly (.app originalQ n)) :=
  (q_beta _).trans ((P01DF.PolyConv.app (succ_beta n diagonalStep diagonalZero) (.refl _)).trans
    ((P01DF.PolyConv.app (delta_beta (stateRun n)) (.refl _)).trans
      ((P01AC.ExtensionalRepair.InternalGraph.pair_second _ _).trans (.app (.refl _) (q_beta n).symm))))

theorem q_zero_evidence {Γ : Tel} (hc : Ctx Γ) : Has Γ ident (ZeroAt originalQ) := by
  have hq := ExactScalarFusion.closed_has_T original_q_has hc
  have hq0 := app_has (form_arr (N_form hc) (N_form hc)) (N_form hc) hq (zero_has_N hc)
  exact .identityIntro (zeroAt_formed hc hq) hq0 (zero_has_N hc) q_preserves_zero

theorem q_step_evidence {Γ : Tel} (hc : Ctx Γ) :
    Has Γ (abstract ident) (StepAt originalQ) := by
  have hq := ExactScalarFusion.closed_has_T original_q_has hc
  have c1 := Ctx.ext hc (N_form hc)
  have hq1 : Has (N :: Γ) (pren Nat.succ originalQ) NT := has_wk hq hc (N_form hc)
  have hn : Has (N :: Γ) (.var 0) N := .var (N_form c1) .zero
  have hs := succ_has_NT c1
  have sn := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hs hn
  have qn := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hq1 hn
  have left := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hq1 sn
  have right := app_has (form_arr (N_form c1) (N_form c1)) (N_form c1) hs qn
  apply Has.piIntro (stepAt_formed hc hq)
  · apply Has.identityIntro (.identity (N_form c1) left right) left right
    simpa only [ExactScalarFusion.pren_closed (has_scoped original_q_has)] using q_preserves_succ (.var 0)
  · exact scoped_abstract trivial

/-- A direct computation of the dependent elimination type; the proof arguments
    are ordinary identity hypotheses, not new inference constructors. -/
theorem rigidity_inst (u : Poly) :
    inst (arr (ZeroAt (.var 0)) (arr (StepAt (.var 0)) (ResultAt (.var 0)))) u =
      arr (ZeroAt u) (arr (StepAt u) (ResultAt u)) := by
  have hz := has_scoped (inputNumeral_has 0)
  have hs := has_scoped succ_has
  simp [inst, ZeroAt, StepAt, ResultAt, NT, ident, zero, N, NBody, arr, wk, subst,
    psub, pup, pren, psub_comp, cons,
    P01AC.BooleanPrimitive.psub_closed hz, P01AC.BooleanPrimitive.psub_closed hs]

/-- Actual same-calculus elimination of an internal rigidity hypothesis. -/
theorem identity_from_rigidity {Γ : Tel} (hc : Ctx Γ) {r : Poly}
    (hr : Has Γ r Rigidity) :
    Has Γ (.app (.app (.app r originalQ) ident) (abstract ident)) (ResultAt originalQ) := by
  have hq := ExactScalarFusion.closed_has_T original_q_has hc
  have hZ := zeroAt_formed hc hq
  have hS := stepAt_formed hc hq
  have hR := resultAt_formed hc hq
  have first : Has Γ (.app r originalQ) (arr (ZeroAt originalQ) (arr (StepAt originalQ) (ResultAt originalQ))) := by
    have h := Has.piElim (rigidity_formed hc)
      (show Form Γ (inst _ originalQ) from (rigidity_inst originalQ).symm ▸ form_arr hZ (form_arr hS hR)) hr hq
    simpa only [rigidity_inst] using h
  exact app_has (form_arr hS hR) hR
    (app_has (form_arr hZ (form_arr hS hR)) (form_arr hS hR) first (q_zero_evidence hc))
    (q_step_evidence hc)

/-- The same elimination accepts arbitrary original HasE hypothesis evidence. -/
theorem identity_from_rigidityE {Γ : Tel} (hc : Ctx Γ) {r : Poly}
    (hr : HasE Γ r Rigidity) :
    HasE Γ (.app (.app (.app r originalQ) ident) (abstract ident)) (ResultAt originalQ) := by
  have hq := ExactScalarFusion.closed_has_T original_q_has hc
  have hZ := zeroAt_formed hc hq
  have hS := stepAt_formed hc hq
  have hR := resultAt_formed hc hq
  have first : HasE Γ (.app r originalQ) (arr (ZeroAt originalQ) (arr (StepAt originalQ) (ResultAt originalQ))) := by
    have h := HasE.piElim (form_inclusion (rigidity_formed hc))
      (form_inclusion (show Form Γ (inst _ originalQ) from
        (rigidity_inst originalQ).symm ▸ form_arr hZ (form_arr hS hR))) hr (has_inclusion hq)
    simpa only [rigidity_inst] using h
  have second : HasE Γ (.app (.app r originalQ) ident) (arr (StepAt originalQ) (ResultAt originalQ)) := by
    have h := HasE.piElim (form_inclusion (form_arr hZ (form_arr hS hR)))
      (form_inclusion (show Form Γ (inst (wk (arr (StepAt originalQ) (ResultAt originalQ))) ident) from
        by simpa only [inst_wk] using form_arr hS hR)) first (has_inclusion (q_zero_evidence hc))
    simpa only [inst_wk] using h
  have h := HasE.piElim (form_inclusion (form_arr hS hR))
    (form_inclusion (show Form Γ (inst (wk (ResultAt originalQ)) (abstract ident)) from
      by simpa only [inst_wk] using hR)) second (has_inclusion (q_step_evidence hc))
  simpa only [inst_wk] using h

theorem result_exact : ResultAt originalQ = FullPER.Application.originalIdentity := by
  simp only [ResultAt, NT, ident, FullPER.Application.originalIdentity,
    FullPER.Application.originalP, variable_closed_exact]

/-- Rigidity and the literal target are term-closed source types. -/
theorem rigidity_subst (σ : Nat → Poly) : subst σ Rigidity = Rigidity := by
  have hz := has_scoped (inputNumeral_has 0)
  have hs := has_scoped succ_has
  simp [Rigidity, ZeroAt, StepAt, ResultAt, NT, ident, zero, N, NBody, arr, wk, subst,
    psub, pup, pren, psub_comp, cons,
    P01AC.BooleanPrimitive.psub_closed hz, P01AC.BooleanPrimitive.psub_closed hs]

theorem result_q_subst (σ : Nat → Poly) :
    subst σ (ResultAt originalQ) = ResultAt originalQ := by
  simp [ResultAt, NT, ident, N, NBody, arr, wk, subst, psub,
    P01AC.BooleanPrimitive.psub_closed (has_scoped original_q_has)]

def implicationProof : Poly :=
  abstract (.app (.app (.app (.var 0) originalQ) ident) (abstract ident))

/-- A genuine closed proof of Rigidity → Id(I,q) in the UNCHANGED source.
    Rigidity remains a hypothesis; no proof of Rigidity is asserted. -/
theorem rigidity_implies_identity :
    Has [] implicationProof (arr Rigidity (ResultAt originalQ)) := by
  have hR := rigidity_formed Ctx.nil
  have hc := Ctx.ext Ctx.nil hR
  have hv : Has [Rigidity] (.var 0) Rigidity := by
    have v : Has [Rigidity] (.var 0) (wk Rigidity) :=
      .var (form_wk hR Ctx.nil hR) .zero
    simpa only [wk, rigidity_subst] using v
  have b := identity_from_rigidity hc hv
  apply Has.piIntro (form_arr hR
    (resultAt_formed Ctx.nil original_q_has))
  · simpa only [wk, result_q_subst] using b
  · exact scoped_abstract (has_scoped b)

#print axioms identity_from_rigidityE
#print axioms result_exact
#print axioms rigidity_implies_identity
#print axioms rigidity_formed
#print axioms q_preserves_zero
#print axioms q_preserves_succ
#print axioms identity_from_rigidity
end SourceRigidity
