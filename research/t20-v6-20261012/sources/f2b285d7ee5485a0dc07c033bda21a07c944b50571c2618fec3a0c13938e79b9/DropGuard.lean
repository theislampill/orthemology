import Attainment
import Mathlib.Data.Finset.Option

/-! A genuine synchronous update on numeric exact-support tables. The finite
candidate generator does not enumerate or inspect bounded proof trees. -/
namespace GuardedTree.Saturation
open Tree
variable {J E R : Type*} [DecidableEq E] (G : Grammar J E R) [Fintype R]

abbrev Table := J → Finset E → Option ℚ

/-- All premise supports permitted by this fixed finite grammar. -/
abbrev SupportChoice := ↥((grammarSupport G).powerset)
abbrev RuleChoice := (r : R) × (Fin (G.arity r) → SupportChoice G)

noncomputable instance : Fintype (RuleChoice G) := by
  classical
  infer_instance

/-- Every premise is read from the old numeric table; support order matters. -/
def enabled (D : Table (J := J) (E := E)) (x : RuleChoice G) : Prop :=
  (∀ i, (D (G.premise x.1 i) (x.2 i).val).isSome) ∧
    True -- deliberately mutated: guard no longer checked

def outputSupport (x : RuleChoice G) : Finset E :=
  G.localSupport x.1 ∪ Finset.univ.biUnion (fun i => (x.2 i).val)

def outputCost (D : Table (J := J) (E := E)) (x : RuleChoice G) : ℚ :=
  G.price x.1 + ∑ i, (D (G.premise x.1 i) (x.2 i).val).getD 0

/-- Old value plus all enabled root-rule candidates for exactly (q,S). -/
noncomputable def candidates (D : Table (J := J) (E := E)) (q : J) (S : Finset E) :
    Finset ℚ := by
  classical
  exact (D q S).toFinset ∪
    ((Finset.univ.filter (fun x : RuleChoice G =>
      enabled G D x ∧ G.head x.1 = q ∧ outputSupport G x = S)).image (outputCost G D))

/-- A finite-set minimum, with none representing an unreachable state. -/
noncomputable def minimum (A : Finset ℚ) : Option ℚ :=
  if h : A.Nonempty then some (A.min' h) else none

noncomputable def step (D : Table (J := J) (E := E)) : Table (J := J) (E := E) :=
  fun q S => minimum (candidates G D q S)

theorem minimum_some_iff (A : Finset ℚ) (c : ℚ) :
    minimum A = some c ↔ c ∈ A ∧ ∀ d ∈ A, c ≤ d := by
  classical
  unfold minimum
  split_ifs with h
  · constructor
    · intro hc
      have heq : A.min' h = c := Option.some.inj hc
      subst c
      exact ⟨Finset.min'_mem A h, fun d hd => Finset.min'_le A d hd⟩
    · rintro ⟨hc, hmin⟩
      congr 1
      exact le_antisymm (Finset.min'_le A c hc) (hmin _ (Finset.min'_mem A h))
  · simp only [ reduceCtorEq, false_iff]
    rintro ⟨hc, _⟩
    exact h ⟨c, hc⟩

theorem minimum_le (A : Finset ℚ) (c : ℚ) (hc : c ∈ A) :
    ∃ d, minimum A = some d ∧ d ≤ c := by
  classical
  have h : A.Nonempty := ⟨c, hc⟩
  exact ⟨A.min' h, by simp [minimum, h], Finset.min'_le A c hc⟩

/-- Declarative characterization of the actual finite candidate generator. -/
theorem mem_candidates_iff (D : Table (J := J) (E := E)) (q : J) (S : Finset E) (c : ℚ) :
    c ∈ candidates G D q S ↔
      D q S = some c ∨
      ∃ (r : R) (s : Fin (G.arity r) → Finset E) (p : Fin (G.arity r) → ℚ),
        (∀ i, s i ⊆ grammarSupport G) ∧
        (∀ i, D (G.premise r i) (s i) = some (p i)) ∧
        G.guard r s ∧ G.head r = q ∧
        G.localSupport r ∪ Finset.univ.biUnion s = S ∧
        G.price r + ∑ i, p i = c := by
  classical
  simp only [candidates, Finset.mem_union, Option.mem_toFinset, Finset.mem_image,
    Finset.mem_filter, Finset.mem_univ, true_and]
  constructor
  · rintro (hold | ⟨x, ⟨hen, hq, hs⟩, hc⟩)
    · exact Or.inl hold
    · refine Or.inr ⟨x.1, fun i => (x.2 i).val,
        fun i => (D (G.premise x.1 i) (x.2 i).val).getD 0,
        fun i => Finset.mem_powerset.mp (x.2 i).property, ?_, hen.2, hq, hs, hc⟩
      intro i
      have hi := hen.1 i
      cases hd : D (G.premise x.1 i) (x.2 i).val with
      | none => simp [hd] at hi
      | some p => simp [hd]
  · rintro (hold | ⟨r, s, p, hsub, hp, hg, hq, hs, hc⟩)
    · exact Or.inl hold
    · let x : RuleChoice G := ⟨r, fun i => ⟨s i, Finset.mem_powerset.mpr (hsub i)⟩⟩
      refine Or.inr ⟨x, ⟨⟨?_, hg⟩, hq, hs⟩, ?_⟩
      · intro i
        change (D (G.premise r i) (s i)).isSome
        simp [hp i]
      · change G.price r + ∑ i, (D (G.premise r i) (s i)).getD 0 = c
        simpa only [hp, Option.getD_some] using hc

theorem step_some_iff (D : Table (J := J) (E := E)) (q : J) (S : Finset E) (c : ℚ) :
    step G D q S = some c ↔
      c ∈ candidates G D q S ∧ ∀ d ∈ candidates G D q S, c ≤ d :=
  minimum_some_iff _ _

#print axioms mem_candidates_iff
#print axioms step_some_iff
end GuardedTree.Saturation
