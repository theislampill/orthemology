/- A total executable Boolean decision procedure and finite positive certificates,
   proved sound and complete for the original fixed P01AC identity semantics. -/
import MaskNormalisation

namespace P01AC.RestrictedIdentityV2
open P01AC.RestrictedIdentity
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness

/-- The enumerator includes every mask, including the unique arity-zero mask. -/
theorem masks_complete {r} (s : Mask r) : s ∈ masks r := by
  induction r with
  | zero =>
    have h : s = (fun i => Fin.elim0 i) := funext fun i => Fin.elim0 i
    simp [masks, h]
  | succ r ih =>
    let tail : Mask r := fun i => s i.succ
    have ht := ih tail
    cases hs : s 0 with
    | false =>
      apply List.mem_append_left
      apply List.mem_map.mpr
      refine ⟨tail, ht, ?_⟩
      apply funext
      intro i
      refine Fin.cases ?_ (fun _ => rfl) i
      exact hs.symm
    | true =>
      apply List.mem_append_right
      apply List.mem_map.mpr
      refine ⟨tail, ht, ?_⟩
      apply funext
      intro i
      refine Fin.cases ?_ (fun _ => rfl) i
      exact hs.symm

def identityCheck {r} (e f : Expr r) : Bool :=
  (masks r).all (fun s => coeffEqual (normalise s e) (normalise s f))

theorem identityCheck_iff_normal_polynomial_eq {r} (e f : Expr r) :
    identityCheck e f = true ↔
      ∀ s : Mask r, polynomial (normalise s e) = polynomial (normalise s f) := by
  simp only [identityCheck, List.all_eq_true]
  constructor
  · intro h s
    exact (coeffEqual_iff_polynomial _ _).mp (h s (masks_complete s))
  · intro h s _
    exact (coeffEqual_iff_polynomial _ _).mpr (h s)

theorem identityCheck_iff_denote {r} (e f : Expr r) :
    identityCheck e f = true ↔ ∀ v, e.denote v = f.denote v :=
  (identityCheck_iff_normal_polynomial_eq e f).trans (denote_eq_iff_normal_polynomial_eq e f).symm

/-- Full positive semantic completeness, at every finite arity. -/
theorem identityCheck_iff_fragmentValid {r} (e f : Expr r) :
    identityCheck e f = true ↔ FragmentValid e f :=
  (identityCheck_iff_denote e f).trans (fragment_valid_iff_denote e f).symm

theorem identityCheck_iff_F_identity {r} (e f : Expr r) :
    identityCheck e f = true ↔
      ∀ ρ, F (.identity (Curried r) e.closed f.closed) ρ zeroEnv .i .i :=
  (identityCheck_iff_denote e f).trans (fragment_F_identity_iff_denote e f).symm

theorem identityCheck_iff_G_identity {r} (e f : Expr r) :
    identityCheck e f = true ↔
      ∀ R : REnv, G (.identity (Curried r) e.closed f.closed) R zeroEnv zeroEnv .i .i :=
  (identityCheck_iff_denote e f).trans (fragment_G_identity_iff_denote e f).symm

theorem identityCheck_iff_semantic_witness {r} (e f : Expr r) :
    identityCheck e f = true ↔
      ∃ w : Poly, ∀ R : REnv, G (.identity (Curried r) e.closed f.closed) R zeroEnv zeroEnv
        (eval w zeroEnv) (eval w zeroEnv) :=
  (identityCheck_iff_denote e f).trans (fragment_semantic_witness_iff_denote e f).symm

/-- Proof production is executable through a Boolean computation; no classical
    proposition-decider is used to choose the branch. -/
def fragmentIdentityDecidable {r} (e f : Expr r) : Decidable (FragmentValid e f) :=
  if h : identityCheck e f = true then
    isTrue ((identityCheck_iff_fragmentValid e f).mp h)
  else isFalse (fun hv => h ((identityCheck_iff_fragmentValid e f).mpr hv))

/-- A finite table of mask labels and proposed common coefficient maps. -/
abbrev Certificate (r : Nat) := List (Mask r × Sparse r)

def rowMatches {r} (e f : Expr r) (s : Mask r) (row : Mask r × Sparse r) : Bool :=
  decide (row.1 = s) && coeffEqual (normalise s e) row.2 && coeffEqual (normalise s f) row.2

def verifyCertificate {r} (e f : Expr r) (certificate : Certificate r) : Bool :=
  (masks r).all (fun s => certificate.any (rowMatches e f s))

def makeCertificate {r} (e : Expr r) : Certificate r :=
  (masks r).map (fun s => (s, normalise s e))

theorem verifyCertificate_sound {r} (e f : Expr r) (certificate : Certificate r)
    (h : verifyCertificate e f certificate = true) : FragmentValid e f := by
  apply (identityCheck_iff_fragmentValid e f).mp
  apply (identityCheck_iff_normal_polynomial_eq e f).mpr
  intro s
  have hs := (List.all_eq_true.mp h) s (masks_complete s)
  obtain ⟨row, _, hr⟩ := List.any_eq_true.mp hs
  simp only [rowMatches, Bool.and_eq_true, decide_eq_true_eq] at hr
  exact ((coeffEqual_iff_polynomial _ _).mp hr.1.2).trans
    ((coeffEqual_iff_polynomial _ _).mp hr.2).symm

theorem makeCertificate_complete {r} (e f : Expr r) (h : FragmentValid e f) :
    verifyCertificate e f (makeCertificate e) = true := by
  apply List.all_eq_true.mpr
  intro s hs
  apply List.any_eq_true.mpr
  refine ⟨(s, normalise s e), List.mem_map.mpr ⟨s,hs,rfl⟩, ?_⟩
  have he : coeffEqual (normalise s e) (normalise s e) = true :=
    (coeffEqual_iff_polynomial _ _).mpr rfl
  have hf : coeffEqual (normalise s f) (normalise s e) = true := by
    apply (coeffEqual_iff_polynomial _ _).mpr
    exact ((denote_eq_iff_normal_polynomial_eq e f).mp ((fragment_valid_iff_denote e f).mp h) s).symm
  simp [rowMatches, he, hf]

theorem finite_certificate_complete {r} (e f : Expr r) :
    (∃ certificate : Certificate r, verifyCertificate e f certificate = true) ↔ FragmentValid e f := by
  exact ⟨fun ⟨certificate,h⟩ => verifyCertificate_sound e f certificate h,
    fun h => ⟨makeCertificate e, makeCertificate_complete e f h⟩⟩

#print axioms identityCheck_iff_fragmentValid
#print axioms identityCheck_iff_F_identity
#print axioms identityCheck_iff_G_identity
#print axioms finite_certificate_complete
end P01AC.RestrictedIdentityV2
