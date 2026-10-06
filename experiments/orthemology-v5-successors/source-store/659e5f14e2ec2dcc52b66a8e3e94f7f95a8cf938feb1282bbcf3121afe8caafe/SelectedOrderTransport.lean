import SourceController

namespace SharedAlias.OrderTransport
open OperationalJoin
open OperationalJoin.Typed (BoundedEnvelope interface path mem_path)
noncomputable section
open Classical

/-- A public finite selection with one coherent new ordering per support.
Orders at unselected supports are never used. -/
structure Profile (m : Nat) where
  selected : Finset (Finset (Fin m))
  order : (P : Finset (Fin m)) → {xs : List (Fin m) // xs.Nodup ∧ xs.toFinset = P}

def newLabels {m} (A : Profile m) (P : Finset (Fin m)) : List Nat :=
  (A.order P).val.map Fin.val

theorem new_perm_old {m} (A : Profile m) (P : Finset (Fin m)) :
    (newLabels A P).Perm (Progress.labelList P) := by
  have h : (A.order P).val.Perm P.toList :=
    List.perm_of_nodup_nodup_toFinset_eq (A.order P).property.1 P.nodup_toList
      (by simp only [(A.order P).property.2, Finset.toList_toFinset])
  exact h.map Fin.val

theorem command_perm_old {m} (k : BoundedEnvelope m) :
    k.val.path.Perm (Progress.labelList (path k)) := by
  apply List.perm_of_nodup_nodup_toFinset_eq k.property.1 (Progress.labelList_nodup _)
  ext j
  simp only [List.mem_toFinset, Progress.labelList, List.mem_map, Finset.mem_toList]
  constructor
  · intro member
    exact ⟨⟨j, k.property.2 j member⟩, (mem_path _ _).mpr member, rfl⟩
  · rintro ⟨i, member, rfl⟩
    exact (mem_path _ _).mp member

def swappedLabels {m} (A : Profile m) (k : BoundedEnvelope m) : List Nat :=
  if path k ∈ A.selected then
    Equiv.swap (Progress.labelList (path k)) (newLabels A (path k)) k.val.path
  else k.val.path

theorem swapped_perm {m} (A : Profile m) (k : BoundedEnvelope m) :
    (swappedLabels A k).Perm k.val.path := by
  unfold swappedLabels
  split
  · rw [Equiv.swap_apply_def]
    split_ifs with old new
    · exact (new_perm_old A (path k)).trans (command_perm_old k).symm
    · exact (command_perm_old k).symm
    · exact List.Perm.refl _
  · exact List.Perm.refl _

def selected {m} (A : Profile m) (k : BoundedEnvelope m) : BoundedEnvelope m :=
  ⟨{ k.val with path := swappedLabels A k },
    (swapped_perm A k).nodup_iff.mpr k.property.1,
    fun i member => k.property.2 i ((swapped_perm A k).mem_iff.mp member)⟩

@[simp] theorem selected_action {m} (A : Profile m) (k : BoundedEnvelope m) :
    (selected A k).val.action = k.val.action := rfl
@[simp] theorem selected_successor {m} (A : Profile m) (k : BoundedEnvelope m) :
    (selected A k).val.successor = k.val.successor := rfl
@[simp] theorem selected_nonce {m} (A : Profile m) (k : BoundedEnvelope m) :
    (selected A k).val.nonce = k.val.nonce := rfl
@[simp] theorem selected_support {m} (A : Profile m) (k : BoundedEnvelope m) :
    path (selected A k) = path k := by
  ext i
  simp only [mem_path]
  exact (swapped_perm A k).mem_iff

@[simp] theorem selected_involutive {m} (A : Profile m) :
    Function.Involutive (selected A) := by
  intro k
  have samePath : swappedLabels A (selected A k) = k.val.path := by
    unfold swappedLabels
    rw [selected_support]
    by_cases chosen : path k ∈ A.selected
    · simp only [chosen, if_true]
      change Equiv.swap _ _ (swappedLabels A k) = k.val.path
      simp only [swappedLabels, chosen, if_true, Equiv.swap_apply_self]
    · simp only [chosen, if_false]
      exact if_neg chosen
  apply Subtype.ext
  change { k.val with path := swappedLabels A (selected A k) } = k.val
  rw [samePath]

/-- Complete-command identity is renamed bijectively, never quotiented. -/
def selectedEquiv {m} (A : Profile m) : BoundedEnvelope m ≃ BoundedEnvelope m where
  toFun := selected A
  invFun := selected A
  left_inv := selected_involutive A
  right_inv := selected_involutive A

theorem selected_fixed_unselected {m} (A : Profile m) (k : BoundedEnvelope m)
    (h : path k ∉ A.selected) : selected A k = k := by
  apply Subtype.ext
  simp only [selected, swappedLabels, if_neg h]

theorem selected_fixed_other {m} (A : Profile m) (k : BoundedEnvelope m)
    (old : k.val.path ≠ Progress.labelList (path k))
    (new : k.val.path ≠ newLabels A (path k)) : selected A k = k := by
  apply Subtype.ext
  simp [selected, swappedLabels, Equiv.swap_apply_of_ne_of_ne old new]

theorem selected_fixed_identical {m} (A : Profile m) (k : BoundedEnvelope m)
    (same : Progress.labelList (path k) = newLabels A (path k)) : selected A k = k := by
  apply Subtype.ext
  simp [selected, swappedLabels, ← same, Equiv.swap_self]

theorem selected_old_to_new {m} (A : Profile m) (k : BoundedEnvelope m)
    (chosen : path k ∈ A.selected) (old : k.val.path = Progress.labelList (path k)) :
    (selected A k).val.path = newLabels A (path k) := by
  change swappedLabels A k = _
  simp only [swappedLabels, if_pos chosen, old, Equiv.swap_apply_left]

theorem selected_new_to_old {m} (A : Profile m) (k : BoundedEnvelope m)
    (chosen : path k ∈ A.selected) (new : k.val.path = newLabels A (path k)) :
    (selected A k).val.path = Progress.labelList (path k) := by
  change swappedLabels A k = _
  simp only [swappedLabels, if_pos chosen, new, Equiv.swap_apply_right]

/-- Laws needed by the accepted typed source, separately verified above. -/
structure Symmetry (m : Nat) where
  command : BoundedEnvelope m → BoundedEnvelope m
  involutive : Function.Involutive command
  action : ∀ k, (command k).val.action = k.val.action
  successor : ∀ k, (command k).val.successor = k.val.successor
  nonce : ∀ k, (command k).val.nonce = k.val.nonce
  support : ∀ k, path (command k) = path k

def profileSymmetry {m} (A : Profile m) : Symmetry m :=
  ⟨selected A, selected_involutive A, selected_action A, selected_successor A,
    selected_nonce A, selected_support A⟩

end
end SharedAlias.OrderTransport
