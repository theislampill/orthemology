/- Elementary algebra applied to the reactive rival. No novelty or metaphysical claim. -/
namespace CoalescenceComposition

theorem associative_idempotent_left_surjective_is_right_projection
    {X : Type} (f : X → X → X)
    (assoc : ∀ a b c, f (f a b) c = f a (f b c))
    (idem : ∀ a, f a a = a)
    (leftSurj : ∀ a b, ∃ x, f a x = b) :
    ∀ a b, f a b = b := by
  intro a b
  obtain ⟨x, rfl⟩ := leftSurj a b
  rw [← assoc, idem]

theorem associative_idempotent_bilateral_surjective_is_subsingleton
    {X : Type} (f : X → X → X)
    (assoc : ∀ a b c, f (f a b) c = f a (f b c))
    (idem : ∀ a, f a a = a)
    (leftSurj : ∀ a b, ∃ x, f a x = b)
    (rightSurj : ∀ a b, ∃ x, f x a = b) :
    ∀ a b : X, a = b := by
  have proj := associative_idempotent_left_surjective_is_right_projection f assoc idem leftSurj
  intro a b
  obtain ⟨x, hx⟩ := rightSurj a b
  exact (proj x a).symm.trans hx

theorem associative_image
    {H Q : Type} (join : H → H → H) (f : Q → Q → Q) (p : H → Q)
    (onto : ∀ q, ∃ h, p h = q)
    (assoc : ∀ a b c, join (join a b) c = join a (join b c))
    (hom : ∀ a b, p (join a b) = f (p a) (p b)) :
    ∀ a b c, f (f a b) c = f a (f b c) := by
  intro a b c
  obtain ⟨x, rfl⟩ := onto a
  obtain ⟨y, rfl⟩ := onto b
  obtain ⟨z, rfl⟩ := onto c
  rw [← hom x y, ← hom (join x y) z, assoc, hom x (join y z), hom y z]

def tri (a b : Fin 3) : Fin 3 := ⟨(2 * (a.val + b.val)) % 3, Nat.mod_lt _ (by decide)⟩

theorem actual_three_label_nonassociative :
    tri (tri 0 0) 1 ≠ tri 0 (tri 0 1) := by decide

theorem no_associative_onto_lift
    {H : Type} (join : H → H → H) (p : H → Fin 3)
    (onto : ∀ q, ∃ h, p h = q)
    (assoc : ∀ a b c, join (join a b) c = join a (join b c)) :
    ¬ (∀ a b, p (join a b) = tri (p a) (p b)) := by
  intro hom
  exact actual_three_label_nonassociative (associative_image join tri p onto assoc hom 0 0 1)

-- Positive exact lift. The rich operation retains bracketing; it is not associative.
inductive Tree where
  | atom : Fin 3 → Tree
  | branch : Tree → Tree → Tree

def eval : Tree → Fin 3
  | .atom q => q
  | .branch a b => tri (eval a) (eval b)

theorem tree_evaluation_hom : ∀ a b, eval (.branch a b) = tri (eval a) (eval b) := by
  intro a b; rfl

theorem tree_evaluation_onto : ∀ q, ∃ h, eval h = q := by
  intro q; exact ⟨.atom q, rfl⟩

-- Existing H-style update criterion, used only to reject a particular projection.
theorem separating_continuation_blocks_update
    {H Q : Type} (p : H → Q) (step : H → H) (x y : H)
    (sameNow : p x = p y) (differentLater : p (step x) ≠ p (step y)) :
    ¬ ∃ update : Q → Q, ∀ h, update (p h) = p (step h) := by
  rintro ⟨update, commutes⟩
  apply differentLater
  calc p (step x) = update (p x) := (commutes x).symm
       _ = update (p y) := congrArg update sameNow
       _ = p (step y) := commutes y

-- A symmetry-fixed input needs a symmetry-fixed output for any equivariant decoder.
theorem fixed_input_without_fixed_output_has_no_decoder
    {G H Q : Type} (actH : G → H → H) (actQ : G → Q → Q) (h : H)
    (fixedInput : ∀ g, actH g h = h)
    (noFixedOutput : ∀ q, ∃ g, actQ g q ≠ q) :
    ¬ ∃ decode : H → Q, ∀ g x, decode (actH g x) = actQ g (decode x) := by
  rintro ⟨decode, equiv⟩
  obtain ⟨g, hg⟩ := noFixedOutput (decode h)
  apply hg
  have eq := equiv g h
  rw [fixedInput g] at eq
  exact eq.symm

#print axioms associative_idempotent_left_surjective_is_right_projection
#print axioms associative_idempotent_bilateral_surjective_is_subsingleton
#print axioms associative_image
#print axioms actual_three_label_nonassociative
#print axioms no_associative_onto_lift
#print axioms tree_evaluation_hom
#print axioms tree_evaluation_onto
#print axioms separating_continuation_blocks_update
#print axioms fixed_input_without_fixed_output_has_no_decoder
end CoalescenceComposition
