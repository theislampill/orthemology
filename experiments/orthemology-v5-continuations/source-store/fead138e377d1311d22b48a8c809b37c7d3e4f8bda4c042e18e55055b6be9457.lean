import AtomEnumeration

namespace Orthemology.Frontier.MealyMeasure
open Set MeasureTheory
open scoped ENNReal

variable {S T U : Type*}

/-- A target generator viewed as a Mealy machine that ignores its input. -/
def generatorMealy (G : Generator T) : Mealy T where
  next t _ := G.next t
  out t _ := G.out t

theorem generatorMealy_state (G : Generator T) (t : T) (x : Cantor) (n : ℕ) :
    state (generatorMealy G) t x n = G.position t n := by
  induction n with
  | zero => rfl
  | succ n ih => rw [state, ih]; rfl

theorem generatorMealy_output (G : Generator T) (t : T) (x : Cantor) :
    output (generatorMealy G) t x = G.stream t := by
  funext n
  change G.out (state (generatorMealy G) t x n) = _
  rw [generatorMealy_state]
  rfl

theorem generatorRel_iff_stream_eq (G : Generator T) (t u : T) :
    (generatorMealy G).infiniteRel t u ↔ G.stream t = G.stream u := by
  constructor
  · intro h
    funext n
    have he := ((generatorMealy G).approx_iff_words (n+1) t u).mp (h (n+1))
      (pref (n+1) (fun _ => false)) (pref (n+1) (fun _ => false))
      (prefix_length _ _) (prefix_length _ _)
    rw [output_prefix, output_prefix, generatorMealy_output, generatorMealy_output] at he
    exact (prefix_eq_iff _ _ _).mp he n (by omega)
  · intro h n
    apply ((generatorMealy G).approx_iff_words n t u).mpr
    intro a b ha hb
    have he_a : pref n (extend a) = a := by simpa only [ha] using prefix_extend a
    have he_b : pref n (extend b) = b := by simpa only [hb] using prefix_extend b
    rw [← he_a, ← he_b, output_prefix, output_prefix, generatorMealy_output,
      generatorMealy_output, h]

def sumGenerator (G : Generator T) (H : Generator U) : Generator (Sum T U) where
  next
    | .inl t => .inl (G.next t)
    | .inr u => .inr (H.next u)
  out
    | .inl t => G.out t
    | .inr u => H.out u

theorem sumGenerator_position_left (G : Generator T) (H : Generator U) (t : T) (n : ℕ) :
    (sumGenerator G H).position (.inl t) n = .inl (G.position t n) := by
  induction n with
  | zero => rfl
  | succ n ih => rw [Generator.position, ih]; rfl

theorem sumGenerator_position_right (G : Generator T) (H : Generator U) (u : U) (n : ℕ) :
    (sumGenerator G H).position (.inr u) n = .inr (H.position u n) := by
  induction n with
  | zero => rfl
  | succ n ih => rw [Generator.position, ih]; rfl

theorem sumGenerator_stream_left (G : Generator T) (H : Generator U) (t : T) :
    (sumGenerator G H).stream (.inl t) = G.stream t := by
  funext n
  change (sumGenerator G H).out ((sumGenerator G H).position (.inl t) n) = _
  rw [sumGenerator_position_left]
  rfl

theorem sumGenerator_stream_right (G : Generator T) (H : Generator U) (u : U) :
    (sumGenerator G H).stream (.inr u) = H.stream u := by
  funext n
  change (sumGenerator G H).out ((sumGenerator G H).position (.inr u) n) = _
  rw [sumGenerator_position_right]
  rfl

/-- Decidable equality of finite-state-generated infinite streams, via the proved finite bound. -/
def generatorsEqual [Fintype T] [Fintype U]
    (G : Generator T) (t : T) (H : Generator U) (u : U) : Bool :=
  decide (((generatorMealy (sumGenerator G H)).approx
    (2 * Fintype.card (Sum T U) - 1)).rel (.inl t) (.inr u))

theorem generatorsEqual_spec [Fintype T] [Fintype U]
    (G : Generator T) (t : T) (H : Generator U) (u : U) :
    generatorsEqual G t H u = true ↔ G.stream t = H.stream u := by
  letI : Nonempty (Sum T U) := ⟨.inl t⟩
  simp only [generatorsEqual, decide_eq_true_eq]
  have h := (generatorMealy (sumGenerator G H)).bound_iff_infinite (.inl t) (.inr u)
  rw [Nat.card_eq_fintype_card] at h
  rw [h, generatorRel_iff_stream_eq, sumGenerator_stream_left, sumGenerator_stream_right]

def atomCandidatesEqual [Fintype S] (M : Mealy S) (s : S) (u v : List Bool) : Bool :=
  generatorsEqual (drivenGenerator M (prefixDriver u)) (s,0)
    (drivenGenerator M (prefixDriver v)) (s,0)

theorem atomCandidatesEqual_spec [Fintype S] (M : Mealy S) (s : S) (u v : List Bool) :
    atomCandidatesEqual M s u v = true ↔ atomCandidate M s u = atomCandidate M s v := by
  rw [atomCandidatesEqual, generatorsEqual_spec, drivenGenerator_stream,
    drivenGenerator_stream, prefixDriver_stream, prefixDriver_stream]
  rfl

end Orthemology.Frontier.MealyMeasure
