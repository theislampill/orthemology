import ActionDisclosure

namespace Orthemology.ActionDisclosure

def twoRootMenu (i : Fin 2) : Fin 3 := ⟨i.val, by omega⟩

theorem twoRootMenu_safe : safeDecoder twoRootMenu 1 := by
  apply injective_menu_suffices
  · intro x y h
    apply Fin.ext
    simpa [twoRootMenu] using congrArg (fun z : Fin 3 => z.val) h
  · decide

theorem duplicate_labels_not_safe :
    ¬ safeDecoder (fun _ : Fin 2 => (0 : Fin 3)) 1 := by
  intro h
  obtain ⟨m, hm⟩ := h {0} (by decide)
  exact hm (by simp)

theorem equal_size_menu_not_safe :
    ¬ safeDecoder twoRootMenu 2 := by
  intro h
  have hh := safeDecoder_message_lower_bound twoRootMenu 2 h
  simp at hh

theorem two_root_supports_not_safe :
    ¬ safeSupportCode (fun _ : Fin 2 => ({0,1} : Set (Fin 3))) 1 := by
  intro h
  obtain ⟨m, hm⟩ := h {0} (by decide)
  exact hm 0 (by simp) (by simp)

#print axioms twoRootMenu_safe
#print axioms duplicate_labels_not_safe
#print axioms equal_size_menu_not_safe
#print axioms two_root_supports_not_safe
end Orthemology.ActionDisclosure
