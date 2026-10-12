/- Reuse of the retained actual-all-rule tagged model, not a new model.
   The R boundary is a concrete admissible instance of the new full-E interface. -/
import FullESigmaElimination
import Boundary
namespace SigmaCompletion.FullE.BoundaryControls
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

abbrev S := SigmaTagBoundary.SigmaRaw
abbrev R := SourceRigidity.Rigidity
abbrev Γ : Tel := [S, R]

theorem context_actual : CtxE Γ := by
  have hR := RigidityInitiality.FullE.rigidity_formed CtxE.nil
  have cr := CtxE.ext CtxE.nil hR
  exact .ext cr (.sigma (.raw cr) (.raw (.ext cr (.raw cr))))

theorem A_actual : FormE Γ .raw := .raw context_actual

theorem B_actual : FormE (.raw :: Γ) .raw := .raw (.ext context_actual A_actual)

theorem input_actual : HasE Γ (.var 0) S :=
  .var (.sigma A_actual B_actual) .zero

/-- Rigidity is an actual available hypothesis in the very same telescope. -/
theorem rigidity_actual : HasE Γ (.var 1) R := by
  have hl : Lookup Γ 1 (wk (wk R)) := .succ .zero
  have hl' : Lookup Γ 1 R := by simpa only [R, wk, SourceRigidity.rigidity_subst] using hl
  exact .var (RigidityInitiality.FullE.rigidity_formed context_actual) hl' 

theorem eta_at_unavailable : ¬ EtaAt Γ .raw .raw (.var 0) := by
  rintro ⟨e,he⟩
  exact SigmaTagBoundary.no_eta_under_rigidity e he

theorem weak_elimination_at_unavailable : ¬ WeakEliminationAt Γ .raw .raw (.var 0) := by
  intro h
  exact eta_at_unavailable ((eta_iff_weak_elimination_at context_actual A_actual B_actual input_actual).mpr h)

theorem strong_elimination_at_unavailable : ¬ EliminationAt Γ .raw .raw (.var 0) := by
  intro h
  exact eta_at_unavailable ((eta_iff_elimination_at context_actual A_actual B_actual input_actual).mpr h)

theorem eta_schema_unavailable : ¬ EtaSchema := by
  intro h
  exact eta_at_unavailable (h Γ .raw .raw (.var 0) context_actual A_actual B_actual input_actual)

theorem weak_schema_unavailable : ¬ WeakEliminationSchema :=
  fun h => eta_schema_unavailable (weak_elimination_implies_eta h)

theorem strong_schema_unavailable : ¬ EliminationSchema :=
  fun h => eta_schema_unavailable (elimination_implies_eta h)

/-- Exact inherited relative-independence statement, exposed without claiming
    a new model or identifying external schemas with a single source type. -/
theorem inherited_eta_relative_independence :
    (¬ ∃ p, HasE [] p (arr R SigmaTagBoundary.Eta)) ∧
    (¬ ∃ p, HasE [] p (arr R (arr SigmaTagBoundary.Eta .bottom))) :=
  SigmaTagBoundary.relative_independence

#print axioms rigidity_actual
#print axioms weak_elimination_at_unavailable
#print axioms eta_schema_unavailable
#print axioms strong_schema_unavailable
#print axioms inherited_eta_relative_independence
end SigmaCompletion.FullE.BoundaryControls
