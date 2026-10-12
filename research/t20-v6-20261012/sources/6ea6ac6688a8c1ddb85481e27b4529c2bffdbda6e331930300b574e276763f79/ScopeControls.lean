import P01CanonicalCarrierProjection
namespace IndependentCarrierAudit
open OrthemologyV2 OrthemologyV3 P01D P01R P01DF
open P01F (cons)

-- Projection is genuinely lossy even when the two unary Codes are equal.
theorem same_carrier_different_relations :
    carrierCode totalPER = carrierCode rawPER ∧ totalPER ≠ rawPER := by
  constructor
  · apply carrier_code_ext
    intro t
    exact ⟨fun _ => Conv.refl t, fun _ => True.intro⟩
  · intro e
    have h : totalPER.rel .i skk := True.intro
    rw [e] at h
    exact P01Source.I_SKK_not_convertible h

-- Directly challenges generalising the raw Pi square, without using the
-- author's arbitrary_arrow_reverse_projection_fails theorem.
theorem pi_domain_restriction_necessary :
    (dependentPi (carrierCode totalPER)
      (carrierFamily (fun _ => rawPER) (fun _ => rfl))).accepts .i ∧
    ¬ (carrierCode (PiPER totalPER (fun _ => rawPER) (fun _ => rfl))).accepts .i := by
  constructor
  · intro x hx; exact Conv.refl _
  · intro h
    have he := h .i skk True.intro
    exact P01Source.I_SKK_not_convertible
      ((Conv.step (.i .i)).symm.trans (he.trans (Conv.step (.i skk))))

-- A distinct direct counterexample, using totalPER instead of the author's
-- polymorphic identity PER, challenges unrestricted identity equality.
theorem identity_domain_restriction_necessary :
    (carrierCode (IdPER totalPER .i skk)).accepts .i ∧
    ¬ (equalityCode (carrierCode totalPER) .i skk).accepts .i := by
  constructor
  · exact ⟨True.intro,.refl _,.refl _⟩
  · intro h; exact P01Source.I_SKK_not_convertible h.2.2.1

theorem raw_identity_rejects_nonconvertible_endpoints (p : Term) :
    ¬ (carrierCode (IdPER rawPER .i skk)).accepts p := by
  intro h; exact P01Source.I_SKK_not_convertible h.1

theorem canonical_identity_checks_proof_code :
    ¬ (equalityCode Code.top .i .i).accepts skk := by
  intro h; exact P01Source.I_SKK_not_convertible h.2.2.2.symm

-- Inspecting syntax is not globally conversion coherent, even if coherence
-- under the empty domain PER is vacuous. The second Sigma premise is real.
theorem per_coherence_does_not_supply_global_coherence :
    (∀ {x y}, botPER.rel x y → inspectedFibre x = inspectedFibre y) ∧
    ¬ (∀ {x y}, Conv x y → inspectedFibre x = inspectedFibre y) := by
  constructor
  · intro x y h; exact False.elim h
  · intro h
    have he := h (Conv.step (.i .i))
    have hn : Term.app .i .i ≠ Term.i := by decide
    simp only [inspectedFibre,if_neg hn,if_pos rfl] at he
    exact same_carrier_different_relations.2 he

theorem nonconstant_projected_family (ρ : OEnv) (η : Env) :
    ((projectedBody ρ η anchoredIdentity).fibre .i).accepts .i ∧
    (∀ p, ¬ ((projectedBody ρ η anchoredIdentity).fibre skk).accepts p) := by
  constructor
  · exact ⟨.refl _,.refl _,.refl _⟩
  · intro p h; exact P01Source.I_SKK_not_convertible h.1.symm

-- A concrete source derivation has the same evaluated SKI polynomial in the
-- actual canonical sum. No replacement witness or semantic validity premise.
theorem compiled_pair_admitted_without_replacement (ρ : OEnv) (η : Env) :
    (dependentSigma Code.top (projectedBody ρ η anchoredIdentity)).accepts
      (eval (pairPoly (.atom .i) (.atom .i)) η) := by
  apply canonical_sigma_admission
  apply Has.sigmaIntro
  change Has (.atom .i) (.identity (.atom .i) (.atom .i))
  exact .identityIntro (.refl _)

theorem canonical_nonconstant_sigma_rejects_wrong_index (ρ : OEnv) (η : Env) :
    ¬ (dependentSigma Code.top (projectedBody ρ η anchoredIdentity)).accepts
      (pairTerm skk .i) := by
  intro h
  have hx : Conv (firstTerm (pairTerm skk .i)) .i := (sigma_projections h).2.1
  exact P01Source.I_SKK_not_convertible ((pair_first skk .i).symm.trans hx).symm

theorem raw_pi_empty_fibre_rejects_every_term (f : Term) :
    ¬ (dependentPi (carrierCode rawPER)
      (carrierFamily (fun _ => botPER) (fun _ => rfl))).accepts f := by
  intro h; exact h .i (Conv.refl .i)

theorem raw_sigma_empty_fibre_rejects_every_term (z : Term) :
    ¬ (dependentSigma (carrierCode rawPER)
      (carrierFamily (fun _ => botPER) (fun _ => rfl))).accepts z := by
  rintro ⟨x,y,hx,hy,hz⟩; exact hy

-- Definitional contracts guard against accidental constructor/name changes.
theorem carrier_is_exact_domain (P : PER) (t : Term) :
    (carrierCode P).accepts t ↔ P.rel t t := Iff.rfl

theorem represented_sigma_not_ambient_product (P : PER) (B : Term → PER)
    (hp : ∀ {x y}, P.rel x y → B x = B y) (z : Term) :
    (carrierCode (SigmaPER P B hp)).accepts z → Represented z := fun h => h.1

end IndependentCarrierAudit
