import FullESigmaBoundary
import FullESigmaScopeControls
namespace IndependentSigmaReview
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.ExtensionalRepair
open P01AC.ExtensionalRepair.InternalGraph
open SigmaCompletion
abbrev F := SigmaCompletion.FullE.EtaSchema
set_option maxHeartbeats 8000000
set_option maxRecDepth 8192
example {Γ A B z} (hc : CtxE Γ) (ha : FormE Γ A) (hb : FormE (A :: Γ) B)
    (hz : HasE Γ z (.sigma A B)) :
    FullE.WeakEliminationAt Γ A B z ↔ FullE.EliminationAt Γ A B z :=
  (FullE.eta_iff_weak_elimination_at hc ha hb hz).symm.trans
    (FullE.eta_iff_elimination_at hc ha hb hz)
example : FullE.WeakEliminationSchema ↔ FullE.EliminationSchema :=
  FullE.eta_iff_weak_elimination.symm.trans FullE.eta_iff_elimination
-- Adversarial generic use: no original Ctx/Form/Has premise appears.
example {Γ A B P d z e} (hc : CtxE Γ) (ha : FormE Γ A)
    (hb : FormE (A :: Γ) B) (hp : FormE (.sigma A B :: Γ) P)
    (hd : HasE (B :: A :: Γ) d (branchType P)) (hz : HasE Γ z (.sigma A B))
    (he : HasE Γ e (.identity (.sigma A B) z (reconstruct z))) :
    HasE Γ (elim d z e) (inst P z) ∧
    P01DF.PolyConv (elim d z e) (branchAt d (fstPoly z) (sndPoly z)) :=
  ⟨FullE.elim_of_eta hc ha hb hp hd hz he, elim_erases _ _ _⟩
-- Exact inherited open target reduces definitionally, without transport to a surrogate.
example (p : Poly) :
    HasE FullE.BoundaryControls.Γ p
      (.identity (.sigma .raw .raw) (.var 0) (reconstruct (.var 0))) → False :=
  SigmaTagBoundary.no_eta_under_rigidity p
example : HasE FullE.BoundaryControls.Γ (.var 1) SourceRigidity.Rigidity :=
  FullE.BoundaryControls.rigidity_actual
example : ¬ FullE.EliminationAt FullE.BoundaryControls.Γ .raw .raw (.var 0) :=
  FullE.BoundaryControls.strong_elimination_at_unavailable
example : ¬ Ctx [FullE.ScopeControls.D] := FullE.ScopeControls.context_not_original
example : ¬ Form [FullE.ScopeControls.S] FullE.ScopeControls.motive :=
  FullE.ScopeControls.motive_not_original
example (p : Poly) : ¬ Has [.raw, .raw] p (branchType FullE.ScopeControls.motive) :=
  FullE.ScopeControls.branch_not_original p
example (p : Poly) : ¬ Has [] p FullE.ScopeControls.inputType := FullE.ScopeControls.input_not_original p
example : HasE [FullE.ScopeControls.D]
    (elim FullE.ScopeControls.ident FullE.ScopeControls.input FullE.ScopeControls.ident)
    FullE.ScopeControls.D := FullE.ScopeControls.combined_elimination
#print axioms FullE.eta_iff_elimination_at
#print axioms FullE.eta_iff_weak_elimination_at
#print axioms FullE.elim_pair_identity
#print axioms elim_erases
#print axioms elim_pair_computation
#print axioms TaggedPER.fundamental
#print axioms FullE.BoundaryControls.inherited_eta_relative_independence
#print axioms FullE.ScopeControls.combined_elimination
end IndependentSigmaReview
