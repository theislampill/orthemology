import Mathlib.Data.Finset.Card
import Mathlib.Data.Finset.BooleanAlgebra

namespace T20Grounded

variable {Root Claim : Type}

/-- Finite grounded proofs; the surrounding rule graph may be cyclic. -/
inductive Derivable (base : Root → Claim → Prop)
    (rule : Finset Claim → Claim → Prop) (available : Finset Root) : Claim → Prop
  | root {r c} : r ∈ available → base r c → Derivable base rule available c
  | step {premises c} : rule premises c →
      (∀ p ∈ premises, Derivable base rule available p) →
      Derivable base rule available c

 theorem derivable_mono {base : Root → Claim → Prop}
    {rule : Finset Claim → Claim → Prop} {A B : Finset Root}
    (hAB : A ⊆ B) {c : Claim} (h : Derivable base rule A c) :
    Derivable base rule B c := by
  induction h with
  | root hm hb => exact .root (hAB hm) hb
  | step hr hp ih => exact .step hr (fun p hm => ih p hm)

/-- Adding licensed inference rules preserves existing finite derivations. -/
 theorem derivable_rules_mono {base : Root → Claim → Prop}
    {rule₁ rule₂ : Finset Claim → Claim → Prop} {A : Finset Root}
    (hr : ∀ P c, rule₁ P c → rule₂ P c) {c : Claim}
    (h : Derivable base rule₁ A c) : Derivable base rule₂ A c := by
  induction h with
  | root hm hb => exact .root hm hb
  | step hstep hp ih => exact .step (hr _ _ hstep) (fun p hm => ih p hm)

/-- Semantic truth is conditional on true roots and truth-preserving rules. -/
 theorem derivable_sound {base : Root → Claim → Prop}
    {rule : Finset Claim → Claim → Prop} {A : Finset Root}
    (meaning : Claim → Prop)
    (roots_sound : ∀ r ∈ A, ∀ c, base r c → meaning c)
    (rules_sound : ∀ P c, rule P c → (∀ p ∈ P, meaning p) → meaning c)
    {c : Claim} (h : Derivable base rule A c) : meaning c := by
  induction h with
  | root hm hb => exact roots_sound _ hm _ hb
  | step hr hp ih => exact rules_sound _ _ hr (fun p hm => ih p hm)

/-- Inclusion minimality, not minimum cardinality. -/
def MinimalFor (P : Finset Root → Prop) (S : Finset Root) : Prop :=
  P S ∧ ∀ T, T ⊆ S → P T → S ⊆ T

 theorem exists_minimal_subset (P : Finset Root → Prop) (A : Finset Root)
    (hPA : P A) : ∃ S, S ⊆ A ∧ MinimalFor P S := by
  classical
  revert hPA
  refine Finset.strongInductionOn A ?_
  intro A ih hPA
  by_cases hmin : ∀ T, T ⊆ A → P T → A ⊆ T
  · exact ⟨A, Finset.Subset.refl A, hPA, hmin⟩
  · push_neg at hmin
    obtain ⟨T, hTA, hPT, hnAT⟩ := hmin
    have hstrict : T ⊂ A := by
      apply Finset.ssubset_iff_subset_ne.mpr
      refine ⟨hTA, ?_⟩
      intro heq
      apply hnAT
      rw [heq]
    obtain ⟨S, hST, hS⟩ := ih T hstrict hPT
    exact ⟨S, Finset.Subset.trans hST hTA, hS⟩


variable [DecidableEq Root]

/-- Exact retraction for every finite original universe and removal set. -/
 theorem derivable_after_retraction_iff {base : Root → Claim → Prop}
    {rule : Finset Claim → Claim → Prop} (U removed : Finset Root) (c : Claim) :
    Derivable base rule (U \ removed) c ↔
      ∃ S, S ⊆ U ∧ MinimalFor (fun T => Derivable base rule T c) S ∧
        Disjoint S removed := by
  constructor
  · intro h
    obtain ⟨S, hSU, hmin⟩ := exists_minimal_subset
      (fun T => Derivable base rule T c) (U \ removed) h
    refine ⟨S, ?_, hmin, ?_⟩
    · intro r hr
      exact (Finset.mem_sdiff.mp (hSU hr)).1
    · apply Finset.disjoint_left.mpr
      intro r hr hm
      exact (Finset.mem_sdiff.mp (hSU hr)).2 hm
  · rintro ⟨S, hSU, hmin, hdisj⟩
    apply derivable_mono (A := S) (B := U \ removed) _ hmin.1
    intro r hr
    apply Finset.mem_sdiff.mpr
    exact ⟨hSU hr, fun hm => Finset.disjoint_left.mp hdisj hr hm⟩

/-- A fixed grounded proof survives removals outside its genuine support. -/
 theorem survives_disjoint_support {base : Root → Claim → Prop}
    {rule : Finset Claim → Claim → Prop} {U S removed : Finset Root} {c : Claim}
    (h : Derivable base rule S c) (hSU : S ⊆ U) (hd : Disjoint S removed) :
    Derivable base rule (U \ removed) c := by
  apply derivable_mono (A := S) (B := U \ removed) _ h
  intro r hr
  exact Finset.mem_sdiff.mpr ⟨hSU hr, fun hm => Finset.disjoint_left.mp hd hr hm⟩

end T20Grounded
