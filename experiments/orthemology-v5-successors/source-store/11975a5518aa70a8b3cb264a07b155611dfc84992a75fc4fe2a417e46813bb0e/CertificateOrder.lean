import CertificateData
namespace OrthemicCertificate

/-- Canonical support key: cardinality first, then the increasing ambient-index
mask representation. It does not enumerate any absent support. -/
def supportKey {q : ℕ} (B : Support q) : List ℕ :=
  B.card :: (B.image Fin.val).sort (· ≤ ·)

theorem supportKey_injective {q : ℕ} : Function.Injective (@supportKey q) := by
  intro B C h
  have hl : (B.image Fin.val).sort (· ≤ ·) = (C.image Fin.val).sort (· ≤ ·) :=
    (List.cons.inj h).2
  have hi : B.image Fin.val = C.image Fin.val := by
    have := congrArg List.toFinset hl
    simpa only [Finset.sort_toFinset] using this
  ext i
  constructor <;> intro hmem
  · have hm : i.val ∈ C.image Fin.val := hi ▸ Finset.mem_image.mpr ⟨i,hmem,rfl⟩
    obtain ⟨j,hj,hji⟩ := Finset.mem_image.mp hm
    exact Fin.val_injective hji ▸ hj
  · have hm : i.val ∈ B.image Fin.val := hi.symm ▸ Finset.mem_image.mpr ⟨i,hmem,rfl⟩
    obtain ⟨j,hj,hji⟩ := Finset.mem_image.mp hm
    exact Fin.val_injective hji ▸ hj

def supportLE {q : ℕ} (B C : Support q) : Prop := supportKey B ≤ supportKey C
instance {q : ℕ} : DecidableRel (@supportLE q) := fun _ _ => inferInstanceAs (Decidable (_ ≤ _))
instance {q : ℕ} : IsTrans (Support q) supportLE := ⟨fun _ _ _ => le_trans⟩
instance {q : ℕ} : IsAntisymm (Support q) supportLE :=
  ⟨fun _ _ h₁ h₂ => supportKey_injective (le_antisymm h₁ h₂)⟩
instance {q : ℕ} : IsTotal (Support q) supportLE := ⟨fun _ _ => le_total _ _⟩

/-- Deterministic sorting reads only explicitly supplied supports. -/
def sortSupports {q : ℕ} (supports : Finset (Support q)) : List (Support q) :=
  supports.sort supportLE

@[simp] theorem mem_sortSupports {q : ℕ} (supports : Finset (Support q)) (B : Support q) :
    B ∈ sortSupports supports ↔ B ∈ supports := Finset.mem_sort _

theorem sortSupports_pairwise {q : ℕ} (supports : Finset (Support q)) :
    (sortSupports supports).Pairwise supportLE := supports.sort_sorted _

theorem sortSupports_nodup {q : ℕ} (supports : Finset (Support q)) :
    (sortSupports supports).Nodup := supports.sort_nodup _
end OrthemicCertificate
