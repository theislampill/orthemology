import SourceProofSearch
namespace ActualSourceEnumerability
open Encodable JointCertificates CertificateCodeValidity CodedRuleTemplates
set_option maxRecDepth 16384
set_option maxHeartbeats 4000000

/-- Closed Joint type inhabitation, separately projected from actual coded HasJ.
    The candidate contains both a term code and a certificate code. -/
def InhabitedTypeCode (a : Nat) : Prop :=
  ∃ A : P01AC.Ty, encode A = a ∧ ∃ p : P01D.Poly, JointCompletion.HasJ [] p A

def inhabitantCheck (a w : Nat) : Bool :=
  certValid 3 a && certValid 2 w.unpair.1 &&
    checkCanonical (hasCode 2 (encode ([] : P01AC.Tel)) w.unpair.1 a) w.unpair.2

theorem primrec_inhabitantCheck : Primrec₂ inhabitantCheck := by
  have hp : Primrec (fun s : Nat × Nat => s.2.unpair.1) :=
    Primrec.fst.comp (Primrec.unpair.comp Primrec.snd)
  have hc : Primrec (fun s : Nat × Nat => s.2.unpair.2) :=
    Primrec.snd.comp (Primrec.unpair.comp Primrec.snd)
  exact Primrec.and.comp (Primrec.and.comp
    (primrec_certValid.comp (.const 3) Primrec.fst)
    (primrec_certValid.comp (.const 2) hp))
    (primrec_checkCanonical.comp
      ((primrec_hasCode 2).comp ((Primrec.const _).pair (hp.pair Primrec.fst))) hc)

theorem inhabitantCheck_exact (A : P01AC.Ty) (p : P01D.Poly) (c : DerivationCertificate) :
    inhabitantCheck (encode A) (Nat.pair (encode p) (encodeCertificate c)) =
      check c (.hasJ [] p A) := by
  have ha : certValid 3 (encode A) = true := (valid_ty _).mpr ⟨A, rfl⟩
  have hp : certValid 2 (encode p) = true := (valid_poly _).mpr ⟨p, rfl⟩
  simp only [inhabitantCheck, Nat.unpair_pair, ha, hp, Bool.true_and, hasJCode_exact,
    checkCanonical_encode]

theorem inhabitantCheck_sound {a w : Nat} (h : inhabitantCheck a w = true) :
    InhabitedTypeCode a := by
  simp only [inhabitantCheck, Bool.and_eq_true] at h
  obtain ⟨A, rfl⟩ := (valid_ty a).mp h.1.1
  obtain ⟨p, hp⟩ := (valid_poly _).mp h.1.2
  rw [← hp, hasJCode_exact] at h
  exact ⟨A, rfl, p, (derivableCode_encode (.hasJ [] p A)).mp (checkCanonical_sound h.2)⟩

theorem inhabitedTypeCode_iff_candidate (a : Nat) :
    InhabitedTypeCode a ↔ ∃ w, inhabitantCheck a w = true := by
  constructor
  · rintro ⟨A, rfl, p, hp⟩
    obtain ⟨c, hc⟩ := complete (j := .hasJ [] p A) hp
    exact ⟨Nat.pair (encode p) (encodeCertificate c), by simpa only [inhabitantCheck_exact] using hc⟩
  · rintro ⟨w, hw⟩; exact inhabitantCheck_sound hw

theorem inhabitedTypeCode_encode (A : P01AC.Ty) :
    InhabitedTypeCode (encode A) ↔ ∃ p, JointCompletion.HasJ [] p A := by
  constructor
  · rintro ⟨B, hB, h⟩; exact Encodable.encode_injective hB ▸ h
  · intro h; exact ⟨A, rfl, h⟩

def inhabitantSearch (a : Nat) : Part Nat := Nat.rfind (fun w => inhabitantCheck a w)

theorem inhabitantSearch_partrec : Partrec inhabitantSearch :=
  Partrec.rfind primrec_inhabitantCheck.to_comp.partrec.to₂

theorem inhabitantSearch_dom (a : Nat) : (inhabitantSearch a).Dom ↔ InhabitedTypeCode a := by
  simpa only [inhabitantSearch, Nat.rfind_dom, Part.coe_some, Part.mem_some_iff,
    Part.some_dom, implies_true, and_true, eq_comm] using (inhabitedTypeCode_iff_candidate a).symm

theorem inhabitedTypeCode_re : REPred InhabitedTypeCode :=
  inhabitantSearch_partrec.dom_re.of_eq inhabitantSearch_dom

theorem inhabitantSearch_exact (A : P01AC.Ty) :
    (inhabitantSearch (encode A)).Dom ↔ ∃ p, JointCompletion.HasJ [] p A := by
  rw [inhabitantSearch_dom, inhabitedTypeCode_encode]

#print axioms primrec_inhabitantCheck
#print axioms inhabitantCheck_sound
#print axioms inhabitantSearch_partrec
#print axioms inhabitantSearch_dom
#print axioms inhabitedTypeCode_re
#print axioms inhabitantSearch_exact
end ActualSourceEnumerability
