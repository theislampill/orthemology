import Constructive
import Boundary
namespace IndependentEliminationReview
open P01AC P01D P01AC.ExtensionalRepair
open SigmaCompletion

-- The constructor is fixed, rather than merely an unspecified existential output.
theorem fixed_term {Γ A B P d z e} (hc : Ctx Γ) (hA : Form Γ A)
    (hB : Form (A :: Γ) B) (hP : Form (.sigma A B :: Γ) P)
    (hd : Has (B :: A :: Γ) d (branchType P)) (hz : Has Γ z (.sigma A B))
    (he : HasE Γ e (.identity (.sigma A B) z (reconstruct z))) :
    HasE Γ (elim d z e) (inst P z) ∧
      P01DF.PolyConv (elim d z e) (branchAt d (fstPoly z) (sndPoly z)) :=
  ⟨elim_of_eta hc hA hB hP hd hz he,elim_erases d z e⟩

-- Eta is not being inferred merely by proving an equivalence of schemas.
theorem schema_not_available : ¬ EtaSchema := by
  intro h
  let S := SigmaTagBoundary.SigmaRaw
  have hs : Form [] S := .sigma (.raw .nil) (.raw (.ext .nil (.raw .nil)))
  have hc : Ctx [S] := .ext .nil hs
  have hs' : Form [S] S := .sigma (.raw hc) (.raw (.ext hc (.raw hc)))
  have hz : Has [S] (.var 0) S := .var hs' .zero
  obtain ⟨e,he⟩ := h [S] .raw .raw (.var 0) hc (.raw hc) (.raw (.ext hc (.raw hc))) hz
  have sem := TaggedPER.fundamental he SigmaTagBoundary.emptyEnv
    (TaggedPER.cons OpenTermStandardness.T.i TaggedPER.zeroEnv)
    (TaggedPER.cons OpenTermStandardness.T.i TaggedPER.zeroEnv)
    SigmaTagBoundary.empty_admissible
    ⟨⟨rfl,rfl⟩,SigmaTagBoundary.ghost_member _ _⟩
  exact SigmaTagBoundary.eta_at_ghost_empty _ _ _ _ sem

theorem weak_schema_not_available : ¬ WeakEliminationSchema :=
  fun h => schema_not_available (weak_elimination_implies_eta h)

theorem strong_schema_not_available : ¬ EliminationSchema :=
  fun h => schema_not_available (elimination_implies_eta h)

-- Computation is independent of any typing, formation, or equality-of-proofs assumption.
theorem raw_computation_all_terms (d a b e : Poly) :
    P01DF.PolyConv (elim d (pairPoly a b) e) (branchAt d a b) :=
  elim_pair_computation d a b e

-- Proof arguments may vary; the same raw computation holds without identifying them.
theorem proof_variation (d a b e f : Poly) :
    P01DF.PolyConv (elim d (pairPoly a b) e) (elim d (pairPoly a b) f) :=
  (elim_pair_computation d a b e).trans (elim_pair_computation d a b f).symm

#print axioms fixed_term
#print axioms schema_not_available
#print axioms weak_schema_not_available
#print axioms raw_computation_all_terms
#print axioms proof_variation
#check SigmaCompletion.EtaSchema
#print SigmaCompletion.EtaSchema
#print SigmaCompletion.EliminationSchema
end IndependentEliminationReview
