/-
Isolated T20 helper for the fixed scalar-fusion equivalence.
Only the polynomial of an already supplied closed HasE identity proof is
canonicalised. Semantic endpoint validity is not converted into a derivation.
-/
import ExtensionalRepairSoundness
import AllTermAlgebra

namespace P01AC.ExtensionalRepair.ClosedProofCanonicalisation
open OrthemologyV2 OrthemologyV3 P01D P01R

/-- All twenty unchanged HasE constructors preserve finite term scope. -/
theorem has_scope {Γ : Tel} {p : Poly} {A : Ty} (h : HasE Γ p A) :
    Scoped Γ.length p := by
  induction h using HasE.rec
    (motive_1 := fun _ _ => True)
    (motive_2 := fun _ _ _ => True) with
  | nil => trivial
  | ext => trivial
  | param => trivial
  | bottom => trivial
  | all => trivial
  | raw => trivial
  | pi => trivial
  | sigma => trivial
  | identity => trivial
  | var hA hn ih => exact lookup_lt hn
  | i => trivial
  | k => trivial
  | s => trivial
  | finite => trivial
  | allIntro hF hp iF ip => simpa only [twkTel, List.length_map] using ip
  | allElim hF hA hI hp iF iA iI ip => exact ip
  | rawAtom => trivial
  | rawApp hF hf ha iF ihf iha => exact ⟨ihf, iha⟩
  | piIntro hF hb hs iF ihb => exact hs
  | piElim hF hI hf ha iF iI ihf iha => exact ⟨ihf, iha⟩
  | sigmaIntro hF hI ha hb iF iI iha ihb => exact scoped_pair iha ihb
  | sigmaFst hA hF hz iA iF ihz => exact scoped_fst ihz
  | sigmaSnd hF hI hz iF iI ihz => exact scoped_snd ihz
  | identityIntro => trivial
  | proofErase hR hI hp iR iI ihp => exact ihp
  | j hA hB hI hD hE hx hy he hd iA iB iI iD iE ihx ihy ihe ihd =>
      exact scoped_j ihd ihy ihe
  | conv hA hp hc hs iA ihp => exact hs
  | piExt => trivial
  | allExt => trivial

/-- Every typing constructor supplies the exact result's syntactic formation. -/
theorem formed {Γ : Tel} {p : Poly} {A : Ty} (h : HasE Γ p A) : FormE Γ A := by
  cases h <;> assumption

/-- Soundness is used solely for the supplied identity proof's Raw-I component. -/
theorem proof_raw_conversion {r : Poly} {A : Ty} {p q : Poly}
    (h : HasE [] r (.identity A p q)) : Conv (eval r zeroEnv) .i := by
  have semantic := P01AC.ExtensionalRepair.fundamental h
    (diagEnv (fun _ => rawPER)) zeroEnv zeroEnv ⟨rfl, rfl⟩
  exact semantic.2.2.1

/-- Canonical witness for an already inhabited closed identity, same endpoints/type. -/
theorem canonical_identity {r : Poly} {A : Ty} {p q : Poly}
    (h : HasE [] r (.identity A p q)) : HasE [] (.atom .i) (.identity A p q) :=
  .conv (formed h) h
    ((Intensional.Plus.closed_conversion_iff (has_scope h)
      (show Scoped 0 (.atom .i) from trivial)).mpr
      (proof_raw_conversion h)) trivial

theorem closed_identity_exists_iff {A : Ty} {p q : Poly} :
    (∃ r, HasE [] r (.identity A p q)) ↔ HasE [] (.atom .i) (.identity A p q) :=
  ⟨fun ⟨_, h⟩ => canonical_identity h, fun h => ⟨.atom .i, h⟩⟩

#print axioms has_scope
#print axioms formed
#print axioms proof_raw_conversion
#print axioms canonical_identity
#print axioms closed_identity_exists_iff

end P01AC.ExtensionalRepair.ClosedProofCanonicalisation
