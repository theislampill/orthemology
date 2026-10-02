import PhysicalFlattening

open Filter MeasureTheory

namespace Orthemology.Tranche2.PhysicalFlattening
variable {A : Type*}

def prefixActions (blocks : ℕ → List A) (N : ℕ) : List A :=
  (List.range N).flatMap blocks

@[simp] lemma prefixActions_zero (blocks : ℕ → List A) : prefixActions blocks 0 = [] := rfl

@[simp] lemma prefixActions_succ (blocks : ℕ → List A) (N : ℕ) :
    prefixActions blocks (N+1) = prefixActions blocks N ++ blocks N := by
  simp [prefixActions,List.range_succ]

@[simp] lemma prefixActions_length (blocks : ℕ → List A) (N : ℕ) :
    (prefixActions blocks N).length = prefixLength blocks N := by
  induction N with
  | zero => simp
  | succ N ih => simp [ih]

/-- Any finite concatenation already containing position t gives exactly the
least-crossing action. Unexecuted later blocks are irrelevant. -/
theorem prefix_getD_eq_flatten (blocks : ℕ → List A) (hu : Unbounded blocks)
    (d : A) (N t : ℕ) (ht : t < prefixLength blocks N) :
    (prefixActions blocks N).getD t d = flatten blocks hu t := by
  induction N with
  | zero => simp at ht
  | succ N ih =>
    rw [prefixActions_succ]
    by_cases hlt : t < prefixLength blocks N
    · rw [List.getD_append _ _ _ _ (by simpa using hlt)]
      exact ih hlt
    · have hlo : prefixLength blocks N ≤ t := le_of_not_gt hlt
      have hi : blockIndex blocks hu t = N :=
        le_antisymm (Nat.find_min' (hu t) ht) (late_index blocks hu N t hlo)
      rw [List.getD_append_right _ _ _ _ (by simpa using hlo),prefixActions_length]
      simp only [flatten,hi,List.get_eq_getElem]
      exact List.getD_eq_getElem _ _ (by
        have h := offset_lt_length blocks hu t
        simpa [hi] using h)

/-- Total finite-prefix decoder. On invalid/too-short input it returns d. -/
def decode (d : A) (blocks : ℕ → List A) (t : ℕ) : A :=
  (prefixActions blocks (t+1)).getD t d

theorem decode_eq_flatten (d : A) (blocks : ℕ → List A)
    (hne : ∀ n, blocks n ≠ []) (t : ℕ) :
    decode d blocks t = flatten blocks (unbounded_of_nonempty blocks hne) t := by
  exact prefix_getD_eq_flatten blocks _ d (t+1) t
    (lt_of_lt_of_le (Nat.lt_succ_self t) (index_le_prefixLength blocks hne (t+1)))

lemma prefixActions_congr (blocks other : ℕ → List A) (N : ℕ)
    (h : ∀ k < N, blocks k = other k) : prefixActions blocks N = prefixActions other N := by
  induction N with
  | zero => rfl
  | succ N ih =>
    rw [prefixActions_succ,prefixActions_succ,
      ih (fun k hk => h k (by omega)),h N (Nat.lt_succ_self N)]

theorem decode_prefix_local (d : A) (blocks other : ℕ → List A) (t : ℕ)
    (h : ∀ k ≤ t, blocks k = other k) : decode d blocks t = decode d other t := by
  unfold decode
  rw [prefixActions_congr blocks other (t+1) (fun k hk => h k (by omega))]

section Measurable
variable {Ω : Type*} [MeasurableSpace Ω] [MeasurableSpace A]
variable [Countable A] [MeasurableSingletonClass A]
variable [MeasurableSpace (List A)] [MeasurableSingletonClass (List A)]

/-- Measurability is obtained from a finite countable prefix, including a total
fallback for invalid paths. No almost-sure nonempty witness enters the decoder. -/
theorem decode_measurable (d : A) (blocks : ℕ → Ω → List A)
    (hb : ∀ n, Measurable (blocks n)) (t : ℕ) :
    Measurable (fun ω => decode d (fun n => blocks n ω) t) := by
  let pref : Ω → (Fin (t+1) → List A) := fun ω k => blocks k ω
  have hp : Measurable pref := measurable_pi_lambda _ (fun k => hb k)
  let finiteDecode : (Fin (t+1) → List A) → A := fun v =>
    decode d (fun n => if h : n < t+1 then v ⟨n,h⟩ else []) t
  have hf : Measurable finiteDecode := measurable_of_countable _
  have heq : (fun ω => decode d (fun n => blocks n ω) t) = finiteDecode ∘ pref := by
    funext ω
    apply decode_prefix_local
    intro k hk
    simp [finiteDecode,pref,show k < t+1 by omega]
  rw [heq]
  exact hf.comp hp

end Measurable
end Orthemology.Tranche2.PhysicalFlattening

#print axioms Orthemology.Tranche2.PhysicalFlattening.prefix_getD_eq_flatten
#print axioms Orthemology.Tranche2.PhysicalFlattening.decode_measurable
