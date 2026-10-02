import PrefixBits

namespace OrthemologyTagged
open P02A2.ObserverCore P02A2.Q8Measure

def scannedBits (n b : ℕ) : List Bool :=
  List.ofFn (fun j : Fin (n+1) => readBit n b j.val)

def selector (n b : ℕ) : ℕ := (scannedBits n b).findIdx Bool.not

theorem scannedBits_prefix (x : Cantor) (n : ℕ) :
    scannedBits n (sentinel (List.ofFn (fun j : Fin (n+1) => x j.val))) =
      List.ofFn (fun j : Fin (n+1) => x j.val) := by
  unfold scannedBits
  congr 1
  funext j
  exact readBit_prefix x n j.val (by have := j.isLt; omega)

theorem selector_on_tag {x : Cantor} {i n : ℕ}
    (hx : x ∈ tagEvent i) (hin : i ≤ n) :
    selector n (sentinel (List.ofFn (fun j : Fin (n+1) => x j.val))) = i := by
  rw [selector, scannedBits_prefix]
  obtain ⟨hp,hz⟩ := (tagEvent_spec i x).mp hx
  apply (List.findIdx_eq (by simp; omega)).mpr
  constructor
  · simp only [List.getElem_ofFn]
    rw [hz]
    rfl
  · intro j hj
    simp only [List.getElem_ofFn]
    rw [hp j hj]
    rfl

theorem selector_before_tag {x : Cantor} {i n : ℕ}
    (hx : x ∈ tagEvent i) (hni : n < i) :
    selector n (sentinel (List.ofFn (fun j : Fin (n+1) => x j.val))) = n+1 := by
  rw [selector, scannedBits_prefix]
  have hp := ((tagEvent_spec i x).mp hx).1
  have he : (List.ofFn (fun j : Fin (n+1) => x j.val)).findIdx Bool.not =
      (List.ofFn (fun j : Fin (n+1) => x j.val)).length := by
    apply List.findIdx_eq_length_of_false
    intro b hb
    obtain ⟨j,rfl⟩ := List.mem_ofFn.mp hb
    have hj : j.val < i := by have := j.isLt; omega
    simp [hp j.val hj]
  simpa using he

theorem selector_allTrue (n : ℕ) :
    selector n (sentinel (List.ofFn (fun j : Fin (n+1) => allTrue j.val))) = n+1 := by
  rw [selector, scannedBits_prefix]
  have he : (List.ofFn (fun j : Fin (n+1) => allTrue j.val)).findIdx Bool.not =
      (List.ofFn (fun j : Fin (n+1) => allTrue j.val)).length := by
    apply List.findIdx_eq_length_of_false
    intro b hb
    obtain ⟨j,rfl⟩ := List.mem_ofFn.mp hb
    rfl
  simpa using he

end OrthemologyTagged
#print axioms OrthemologyTagged.selector_on_tag
#print axioms OrthemologyTagged.selector_before_tag
