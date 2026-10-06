import FixedFamilies
import UnknownRootAttribution

namespace AttributionKernel
open Finset
variable {α : Type*} [Fintype α] [DecidableEq α]

def encodeRoot (representative : α) (z : Option α) : α := z.getD representative

def representativeMap (A : Finset α) (representative i : α) : α :=
  if i ∈ A then representative else i

omit [Fintype α] in
theorem encode_rootMap (A : Finset α) (representative i : α) :
    encodeRoot representative (rootMap A i) = representativeMap A representative i := by
  by_cases h : i ∈ A <;> simp [rootMap, representativeMap, encodeRoot, h]

theorem encode_injOn_actualRoots (A : Finset α) (representative : α)
    (hr : representative ∈ A) :
    Set.InjOn (encodeRoot representative) (actualRoots A) := by
  intro x hx y hy heq
  cases x with
  | none =>
    cases y with
    | none => rfl
    | some j =>
      have hj := (some_mem_rootImage A univ j).mp hy
      have he : representative = j := heq
      exact False.elim (hj.2 (he ▸ hr))
  | some i =>
    cases y with
    | none =>
      have hi := (some_mem_rootImage A univ i).mp hx
      have he : i = representative := heq
      exact False.elim (hi.2 (he.symm ▸ hr))
    | some j =>
      have he : i = j := heq
      exact congrArg some he

omit [Fintype α] in
theorem representative_image (A P : Finset α) (representative : α) :
    P.image (representativeMap A representative) =
      (rootImage A P).image (encodeRoot representative) := by
  simp only [rootImage, image_image, Function.comp_def, encode_rootMap]

theorem representative_shared_card (A P R : Finset α) (representative : α)
    (hr : representative ∈ A) :
    ((P.image (representativeMap A representative)) ∩
      (R.image (representativeMap A representative))).card =
      (sharedRoots A P R).card := by
  have hinj := encode_injOn_actualRoots A representative hr
  rw [representative_image, representative_image,
    ← image_inter_of_injOn]
  · apply card_image_of_injOn
    exact hinj.mono (fun _ hz => rootImage_mono A (subset_univ P) (mem_inter.mp hz).1)
  · apply hinj.mono
    intro z hz
    rcases hz with hz | hz
    · exact rootImage_mono A (subset_univ P) hz
    · exact rootImage_mono A (subset_univ R) hz

def booleanLabels (m : ℕ) (p : ℕ → Bool) : Finset (Fin m) :=
  univ.filter (fun i => p i.val = true)

def natLabels (m : ℕ) (p : ℕ → Bool) : Finset ℕ :=
  (range m).filter (fun i => p i = true)

theorem natLabels_card (m : ℕ) (p : ℕ → Bool) :
    (natLabels m p).card = ChargedInterlock.card m p := by
  induction m with
  | zero => simp [natLabels, ChargedInterlock.card]
  | succ m ih =>
    simp only [natLabels, range_add_one, filter_insert]
    by_cases hp : p m = true
    · rw [if_pos hp, card_insert_of_not_mem]
      · simpa [natLabels, ChargedInterlock.card, hp] using ih
      · simp
    · rw [if_neg hp]
      simpa [natLabels, ChargedInterlock.card, hp] using ih

theorem booleanLabels_val_image (m : ℕ) (p : ℕ → Bool) :
    (booleanLabels m p).image Fin.val = natLabels m p := by
  ext i
  simp only [mem_image, booleanLabels, natLabels, mem_filter, mem_univ,
    true_and, mem_range]
  constructor
  · rintro ⟨j, hj, rfl⟩
    exact ⟨j.isLt, hj⟩
  · rintro ⟨hi, hp⟩
    exact ⟨⟨i, hi⟩, hp, rfl⟩

theorem booleanLabels_card (m : ℕ) (p : ℕ → Bool) :
    (booleanLabels m p).card = ChargedInterlock.card m p := by
  rw [← natLabels_card, ← booleanLabels_val_image, card_image_of_injective _ Fin.val_injective]

theorem booleanLabels_and (m : ℕ) (p q : ℕ → Bool) :
    booleanLabels m (fun i => p i && q i) = booleanLabels m p ∩ booleanLabels m q := by
  ext i
  simp [booleanLabels]

theorem old_rootOf_correspondence (m representative : ℕ) (hr : representative < m)
    (a : ℕ → Bool) (i : Fin m) :
    (representativeMap (booleanLabels m a) ⟨representative, hr⟩ i).val =
      UnknownRootAttribution.rootOf a representative i.val := by
  by_cases h : a i.val = true <;>
    simp [representativeMap, booleanLabels, UnknownRootAttribution.rootOf, h]

def oldRootImage (m : ℕ) (a p : ℕ → Bool) (representative : ℕ) : Finset ℕ :=
  (booleanLabels m p).image (fun i => UnknownRootAttribution.rootOf a representative i.val)

theorem oldRootImage_as_representative (m representative : ℕ) (hr : representative < m)
    (a p : ℕ → Bool) :
    oldRootImage m a p representative =
      ((booleanLabels m p).image (representativeMap (booleanLabels m a) ⟨representative, hr⟩)).image Fin.val := by
  simp only [oldRootImage, image_image, Function.comp_def, old_rootOf_correspondence]

theorem old_shared_card_correspondence (m representative : ℕ) (hr : representative < m)
    (a p q : ℕ → Bool) (ha : a representative = true) :
    ((oldRootImage m a p representative) ∩ (oldRootImage m a q representative)).card =
      (sharedRoots (booleanLabels m a) (booleanLabels m p) (booleanLabels m q)).card := by
  rw [oldRootImage_as_representative m representative hr,
    oldRootImage_as_representative m representative hr,
    ← image_inter _ _ Fin.val_injective, card_image_of_injective _ Fin.val_injective]
  apply representative_shared_card
  simpa [booleanLabels] using ha

def setPredicate {m : ℕ} (S : Finset (Fin m)) (i : ℕ) : Bool :=
  if h : i < m then decide ((⟨i, h⟩ : Fin m) ∈ S) else false

theorem booleanLabels_setPredicate {m : ℕ} (S : Finset (Fin m)) :
    booleanLabels m (setPredicate S) = S := by
  ext i
  simp [booleanLabels, setPredicate, i.isLt]

def OldRobust (m B c : ℕ) (p q : ℕ → Bool) : Prop :=
  ∀ a : ℕ → Bool, ChargedInterlock.card m a = c →
    ∀ representative : ℕ, representative < m → a representative = true →
      B < ((oldRootImage m a p representative) ∩ (oldRootImage m a q representative)).card

theorem old_robust_iff_new (m B c : ℕ) (hc : 1 ≤ c) (p q : ℕ → Bool) :
    OldRobust m B c p q ↔ Robust B c (booleanLabels m p) (booleanLabels m q) := by
  constructor
  · intro h A hAc
    obtain ⟨r, hr⟩ := card_pos.mp (show 0 < A.card by omega)
    have hclass : ChargedInterlock.card m (setPredicate A) = c := by
      rw [← booleanLabels_card, booleanLabels_setPredicate, hAc]
    have hrA : setPredicate A r.val = true := by simp [setPredicate, r.isLt, hr]
    have ho := h (setPredicate A) hclass r.val r.isLt hrA
    rw [old_shared_card_correspondence m r.val r.isLt (setPredicate A) p q hrA,
      booleanLabels_setPredicate] at ho
    exact ho
  · intro h a hac r hr har
    rw [old_shared_card_correspondence m r hr a p q har]
    exact h (booleanLabels m a) (by simpa [booleanLabels_card] using hac)

theorem old_robust_iff (m B c : ℕ) (hB : 1 ≤ B) (hc : 1 ≤ c)
    (hcm : c ≤ m) (p q : ℕ → Bool) :
    OldRobust m B c p q ↔ B+c ≤ ChargedInterlock.card m (fun i => p i && q i) := by
  rw [old_robust_iff_new m B c hc p q,
    robust_iff B c hB hc (by simpa using hcm),
    ← booleanLabels_and, booleanLabels_card]

#print axioms old_robust_iff
#print axioms representative_shared_card
#print axioms booleanLabels_card
#print axioms old_shared_card_correspondence

end AttributionKernel
