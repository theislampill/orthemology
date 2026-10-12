import CertificateImage
import TelescopeValidityControls
namespace CertificateDomainReview
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability CertificateCodeValidity TelescopeCodeValidity
set_option maxRecDepth 16384
set_option maxHeartbeats 2000000
attribute [local irreducible] Nat.pair

-- The generic evaluator rejects nondecreasing dependencies instead of skipping them.
theorem equal_child_reject (s c : Nat) :
    evaluate (fun _ => true) (fun b => [b]) (s,c) = false := by
  rw [evaluate]
  simp

theorem larger_child_reject (s c : Nat) :
    evaluate (fun _ => true) (fun b => [(b.1,b.2+1)]) (s,c) = false := by
  rw [evaluate]
  simp

theorem shape_reject (s c : Nat) (h : certShape (s,c) = false) : certValid s c = false := by
  rw [certValid, evaluate, h]
  rfl

theorem child_reject (s c : Nat) (d : Nat × Nat)
    (hm : d ∈ certChildren (s,c)) (hr : certValid d.1 d.2 = false) : certValid s c = false := by
  apply Bool.eq_false_iff.mpr
  intro h
  have hc := (certValid_exact s c).mp h
  have hd := ((cert_canonical_rule (s,c)).mp hc).2 d hm
  have hv := (certValid_exact d.1 d.2).mpr hd
  rw [hr] at hv
  contradiction

theorem unsupported_sort (c : Nat) : certValid 15 c = false := by
  apply Bool.eq_false_iff.mpr
  intro h
  have hc := (certValid_exact 15 c).mp h
  simp [CertCanonical] at hc

-- The encoded languages deliberately overlap: term zero, type bottom, and Ty.raw share a natural code.
example : encode OrthemologyV2.Term.zero = encode OrthemologyV2.TypeCode.bottom := rfl
example : certValid 0 (encode OrthemologyV2.Term.zero) = true :=
  (CertificateCodeValidity.valid_term _).mpr ⟨_,rfl⟩
example : certValid 1 (encode OrthemologyV2.Term.zero) = true :=
  (CertificateCodeValidity.valid_typeCode _).mpr ⟨OrthemologyV2.TypeCode.bottom,rfl⟩
example : certValid 3 (encode OrthemologyV2.Term.zero) = true :=
  (CertificateCodeValidity.valid_ty _).mpr ⟨P01AC.Ty.raw,rfl⟩

theorem serial_cons_bad_head (h t : Nat) (hh : certValid 13 h = false) :
    certValid 14 (pack 1 [h,t]) = false := by
  apply child_reject 14 (pack 1 [h,t]) (13,h)
  · simp [certChildren, allDescriptions, localChildren, serialCertListDescription,
      dependencies, fieldCode, List.range_succ]
  · exact hh

theorem serial_cons_bad_tail (h t : Nat) (ht : certValid 14 t = false) :
    certValid 14 (pack 1 [h,t]) = false := by
  apply child_reject 14 (pack 1 [h,t]) (14,t)
  · simp [certChildren, allDescriptions, localChildren, serialCertListDescription,
      dependencies, fieldCode, List.range_succ]
  · exact ht

theorem serial_cons_shape (h t : Nat) : certShape (14,pack 1 [h,t]) = true := by
  simp [certShape, allDescriptions, localShape, serialCertListDescription,
    rebuild, rebuildField, fieldCode, List.range_succ]

-- An invalid telescope is still a perfectly formed external payload.
theorem claim_bad_tel_shape : certShape (11,pack 0 [leaf 1]) = true := by
  simp [certShape, allDescriptions, localShape, claimDescription,
    rebuild, rebuildField, fieldCode, List.range_succ]

theorem tel_one_invalid : certValid 5 1 = false := by
  apply shape_reject
  simp [certShape, rejectTelOne]

theorem claim_bad_tel_invalid : certValid 11 (pack 0 [leaf 1]) = false := by
  apply child_reject 11 (pack 0 [leaf 1]) (5,1)
  · simp [certChildren, allDescriptions, localChildren, claimDescription,
      dependencies, fieldCode, List.range_succ]
  · exact tel_one_invalid

#print axioms equal_child_reject
#print axioms larger_child_reject
#print axioms shape_reject
#print axioms child_reject
#print axioms unsupported_sort
#print axioms serial_cons_bad_head
#print axioms serial_cons_bad_tail
#print axioms serial_cons_shape
#print axioms claim_bad_tel_shape
#print axioms tel_one_invalid
#print axioms claim_bad_tel_invalid
end CertificateDomainReview
