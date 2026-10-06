import Mathlib

/-!
# Hidden-parity finite pruning kernel

The graph content of `ComponentFamily` is instantiated and proved separately in
`EndComponents`. Full rows are values in an arbitrary row type: equality is
never equality only after conditioning on remaining in the component.
-/
namespace HiddenParity

variable {Pair Model Row : Type*} [DecidableEq Pair]

/-- Finite nonempty components whose union is a component when they share a pair.
This is a graph theorem for end components, not a parity-preservation premise. -/
structure ComponentFamily (Pair : Type*) [DecidableEq Pair] where
  component : Finset Pair → Prop
  nonempty : ∀ {E}, component E → E.Nonempty
  union : ∀ {E D}, component E → component D →
    (∃ e, e ∈ E ∧ e ∈ D) → component (E ∪ D)

/-- Every used pair has exactly the same full row under the two models. -/
def Match (row : Model → Pair → Row) (θ σ : Model) (E : Finset Pair) : Prop :=
  ∀ e ∈ E, row σ e = row θ e

/-- The minimum is witnessed by a used pair and is a lower bound on all used pairs. -/
def IsMinimum (priority : Pair → ℕ) (E : Finset Pair) (d : ℕ) : Prop :=
  (∃ e ∈ E, priority e = d) ∧ ∀ e ∈ E, d ≤ priority e

/-- The parity predicate is independent of pruning and applies to every matching rival. -/
def Valid (C : ComponentFamily Pair) (B : Finset Model)
    (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (E : Finset Pair) : Prop :=
  C.component E ∧ ∀ σ ∈ B, Match row θ σ E →
    ∃ d, IsMinimum (priority σ) E d ∧ d % 2 = 0

omit [DecidableEq Pair] in
theorem match_mono {row : Model → Pair → Row} {θ σ : Model}
    {E D : Finset Pair} (hED : E ⊆ D) (h : Match row θ σ D) :
    Match row θ σ E := by
  intro e he
  exact h e (hED he)

omit [DecidableEq Pair] in
theorem minimum_unique {p : Pair → ℕ} {E : Finset Pair} {d k : ℕ}
    (hd : IsMinimum p E d) (hk : IsMinimum p E k) : d = k := by
  obtain ⟨e, he, hpe⟩ := hd.1
  obtain ⟨f, hf, hpf⟩ := hk.1
  have h1 := hd.2 f hf
  have h2 := hk.2 e he
  omega

omit [DecidableEq Pair] in
theorem exists_minimum (p : Pair → ℕ) {E : Finset Pair} (hE : E.Nonempty) :
    ∃ d, IsMinimum p E d := by
  obtain ⟨e, he, hmin⟩ := E.exists_min_image p hE
  exact ⟨p e, ⟨⟨e, he, rfl⟩, hmin⟩⟩

/-- Central deletion invariant: a valid subcomponent contains no pair at an
odd minimum of any full-row-matching enclosing component. -/
theorem valid_avoids_odd_minimum
    {C : ComponentFamily Pair} {B : Finset Model}
    {row : Model → Pair → Row} {priority : Model → Pair → ℕ} {θ σ : Model}
    {E D : Finset Pair} {d : ℕ}
    (hValid : Valid C B row priority θ E) (hED : E ⊆ D)
    (hσ : σ ∈ B) (hMatch : Match row θ σ D)
    (hMin : IsMinimum (priority σ) D d) (hOdd : d % 2 = 1) :
    ∀ e ∈ E, priority σ e ≠ d := by
  intro e he hEq
  obtain ⟨k, hk, hEven⟩ := hValid.2 σ hσ (match_mono hED hMatch)
  have hSmall : IsMinimum (priority σ) E d :=
    ⟨⟨e, he, hEq⟩, fun f hf => hMin.2 f (hED hf)⟩
  have hdk := minimum_unique hSmall hk
  omega

/-- Inclusion-maximality is only graph maximality in the currently retained pairs. -/
def MaximalComponent (C : ComponentFamily Pair) (U D : Finset Pair) : Prop :=
  C.component D ∧ D ⊆ U ∧
    ∀ F, C.component F → F ⊆ U → D ⊆ F → F = D

/-- Exhaustive finite reference selector. It is not the polynomial SCC algorithm. -/
noncomputable def maximalComponents (C : ComponentFamily Pair) (U : Finset Pair) :
    Finset (Finset Pair) := by
  classical
  exact U.powerset.filter (MaximalComponent C U)

@[simp] theorem mem_maximalComponents {C : ComponentFamily Pair} {U D : Finset Pair} :
    D ∈ maximalComponents C U ↔ MaximalComponent C U D := by
  classical
  simp only [maximalComponents, Finset.mem_filter, Finset.mem_powerset]
  exact ⟨And.right, fun h => ⟨h.2.1, h⟩⟩

/-- Every component lies in a maximal one; proved by finite cardinal maximization. -/
theorem component_has_maximal {C : ComponentFamily Pair} {U E : Finset Pair}
    (hE : C.component E) (hEU : E ⊆ U) :
    ∃ D ∈ maximalComponents C U, E ⊆ D := by
  classical
  let candidates := U.powerset.filter (fun D => C.component D ∧ E ⊆ D)
  have hne : candidates.Nonempty := by
    refine ⟨E, ?_⟩
    simp [candidates, hEU, hE]
  obtain ⟨D, hD, hmax⟩ := candidates.exists_max_image Finset.card hne
  have hDU : D ⊆ U := (Finset.mem_powerset.mp (Finset.mem_filter.mp hD).1)
  have hDC : C.component D := (Finset.mem_filter.mp hD).2.1
  have hED : E ⊆ D := (Finset.mem_filter.mp hD).2.2
  refine ⟨D, mem_maximalComponents.mpr ⟨hDC, hDU, ?_⟩, hED⟩
  intro F hFC hFU hDF
  have hF : F ∈ candidates := by
    simp only [candidates, Finset.mem_filter, Finset.mem_powerset]
    exact ⟨hFU, hFC, hED.trans hDF⟩
  exact (Finset.eq_of_subset_of_card_le hDF (hmax F hF)).symm

/-- Maximality plus graph union closes the subtle global-deletion gap:
an intersecting maximal component contains the whole protected component. -/
theorem component_subset_of_intersects_maximal
    {C : ComponentFamily Pair} {U E D : Finset Pair}
    (hE : C.component E) (hEU : E ⊆ U)
    (hD : D ∈ maximalComponents C U) (hi : ∃ e, e ∈ E ∧ e ∈ D) : E ⊆ D := by
  have hm := mem_maximalComponents.mp hD
  have hc : C.component (E ∪ D) := C.union hE hm.1 hi
  have hu : E ∪ D ⊆ U := Finset.union_subset hEU hm.2.1
  have heq := hm.2.2 (E ∪ D) hc hu Finset.subset_union_right
  exact heq ▸ Finset.subset_union_left

/-- A pair is removed only at a current matching model's odd minimum layer. -/
def BadPair (C : ComponentFamily Pair) (B : Finset Model)
    (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (U : Finset Pair) (e : Pair) : Prop :=
  ∃ D ∈ maximalComponents C U, e ∈ D ∧ ∃ σ ∈ B,
    Match row θ σ D ∧ IsMinimum (priority σ) D (priority σ e) ∧
      priority σ e % 2 = 1

noncomputable def step (C : ComponentFamily Pair) (B : Finset Model)
    (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (U : Finset Pair) : Finset Pair := by
  classical
  exact ((maximalComponents C U).biUnion id).filter
    (fun e => ¬ BadPair C B row priority θ U e)

@[simp] theorem mem_step {C : ComponentFamily Pair} {B : Finset Model}
    {row : Model → Pair → Row} {priority : Model → Pair → ℕ}
    {θ : Model} {U : Finset Pair} {e : Pair} :
    e ∈ step C B row priority θ U ↔
      (∃ D ∈ maximalComponents C U, e ∈ D) ∧
        ¬ BadPair C B row priority θ U e := by
  classical
  simp [step]

theorem step_subset (C : ComponentFamily Pair) (B : Finset Model)
    (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (U : Finset Pair) : step C B row priority θ U ⊆ U := by
  intro e he
  obtain ⟨⟨D, hD, heD⟩, _⟩ := mem_step.mp he
  exact (mem_maximalComponents.mp hD).2.1 heD

/-- All valid components, not just maximal ones, survive each complete round. -/
theorem step_preserves {C : ComponentFamily Pair} {B : Finset Model}
    {row : Model → Pair → Row} {priority : Model → Pair → ℕ}
    {θ : Model} {U E : Finset Pair}
    (hV : Valid C B row priority θ E) (hEU : E ⊆ U) :
    E ⊆ step C B row priority θ U := by
  obtain ⟨D, hD, hED⟩ := component_has_maximal hV.1 hEU
  intro e he
  refine mem_step.mpr ⟨⟨D, hD, hED he⟩, ?_⟩
  rintro ⟨F, hF, heF, σ, hσ, hMatch, hMin, hOdd⟩
  have hEF := component_subset_of_intersects_maximal hV.1 hEU hF ⟨e, he, heF⟩
  exact valid_avoids_odd_minimum hV hEF hσ hMatch hMin hOdd e he rfl

/-- Every stable maximal component satisfies the independently defined parity test. -/
theorem stable_maximal_valid {C : ComponentFamily Pair} {B : Finset Model}
    {row : Model → Pair → Row} {priority : Model → Pair → ℕ}
    {θ : Model} {U D : Finset Pair}
    (hStable : step C B row priority θ U = U)
    (hD : D ∈ maximalComponents C U) : Valid C B row priority θ D := by
  have hm := mem_maximalComponents.mp hD
  refine ⟨hm.1, ?_⟩
  intro σ hσ hMatch
  obtain ⟨d, hd⟩ := exists_minimum (priority σ) (C.nonempty hm.1)
  refine ⟨d, hd, ?_⟩
  by_contra hEven
  have hOdd : d % 2 = 1 := by omega
  obtain ⟨e, he, hpe⟩ := hd.1
  have hBad : BadPair C B row priority θ U e :=
    ⟨D, hD, he, σ, hσ, hMatch, hpe ▸ hd, by omega⟩
  have heU := hm.2.1 he
  have heStep : e ∈ step C B row priority θ U := hStable.symm ▸ heU
  exact (mem_step.mp heStep).2 hBad

/-- Recompute components and matching rivals after every round. -/
noncomputable def iterate (C : ComponentFamily Pair) (B : Finset Model)
    (row : Model → Pair → Row) (priority : Model → Pair → ℕ) (θ : Model) :
    ℕ → Finset Pair → Finset Pair
  | 0, U => U
  | n + 1, U => iterate C B row priority θ n (step C B row priority θ U)

theorem iterate_subset (C : ComponentFamily Pair) (B : Finset Model)
    (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (n : ℕ) (U : Finset Pair) :
    iterate C B row priority θ n U ⊆ U := by
  induction n generalizing U with
  | zero => exact Finset.Subset.refl U
  | succ n ih => exact (ih _).trans (step_subset C B row priority θ U)

theorem iterate_preserves {C : ComponentFamily Pair} {B : Finset Model}
    {row : Model → Pair → Row} {priority : Model → Pair → ℕ}
    {θ : Model} {E U : Finset Pair}
    (hV : Valid C B row priority θ E) (hEU : E ⊆ U) (n : ℕ) :
    E ⊆ iterate C B row priority θ n U := by
  induction n generalizing U with
  | zero => exact hEU
  | succ n ih => exact ih (step_preserves hV hEU)

theorem iterate_eq_of_stable {C : ComponentFamily Pair} {B : Finset Model}
    {row : Model → Pair → Row} {priority : Model → Pair → ℕ}
    {θ : Model} {U : Finset Pair}
    (h : step C B row priority θ U = U) (n : ℕ) :
    iterate C B row priority θ n U = U := by
  induction n with
  | zero => rfl
  | succ n ih => simpa only [iterate, h] using ih

/-- The number of potentially strict rounds is bounded by retained pair count,
independent of the magnitudes of the integer priorities. -/
theorem iterate_stable (C : ComponentFamily Pair) (B : Finset Model)
    (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (n : ℕ) (U : Finset Pair) (hBound : U.card ≤ n) :
    step C B row priority θ (iterate C B row priority θ n U) =
      iterate C B row priority θ n U := by
  induction n generalizing U with
  | zero =>
      have hU : U = ∅ := Finset.card_eq_zero.mp (by omega)
      subst U
      exact Finset.eq_empty_iff_forall_not_mem.mpr (by
        intro e he
        exact Finset.not_mem_empty e (step_subset C B row priority θ ∅ he))
  | succ n ih =>
      by_cases hs : step C B row priority θ U = U
      · rw [iterate_eq_of_stable hs]
        exact hs
      · have hStrict : step C B row priority θ U ⊂ U :=
          Finset.ssubset_iff_subset_ne.mpr ⟨step_subset C B row priority θ U, hs⟩
        have hCard := Finset.card_lt_card hStrict
        exact ih (step C B row priority θ U) (by omega)

/-- The finite reference output returns whole maximal components at stability. -/
noncomputable def output (C : ComponentFamily Pair) (B : Finset Model)
    (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (U : Finset Pair) : Finset (Finset Pair) :=
  maximalComponents C (iterate C B row priority θ U.card U)

def MaximalValid (C : ComponentFamily Pair) (B : Finset Model)
    (row : Model → Pair → Row) (priority : Model → Pair → ℕ)
    (θ : Model) (U D : Finset Pair) : Prop :=
  Valid C B row priority θ D ∧ D ⊆ U ∧
    ∀ F, Valid C B row priority θ F → F ⊆ U → D ⊆ F → F = D

/-- Exact output characterization against independently defined valid components.
No preservation, target completeness, or stability assertion is an assumption. -/
theorem output_iff_maximal_valid {C : ComponentFamily Pair} {B : Finset Model}
    {row : Model → Pair → Row} {priority : Model → Pair → ℕ}
    {θ : Model} {U D : Finset Pair} :
    D ∈ output C B row priority θ U ↔ MaximalValid C B row priority θ U D := by
  let K := iterate C B row priority θ U.card U
  have hK : step C B row priority θ K = K :=
    iterate_stable C B row priority θ U.card U (le_refl _)
  have hKU : K ⊆ U := iterate_subset C B row priority θ U.card U
  change D ∈ maximalComponents C K ↔ _
  constructor
  · intro hD
    have hm := mem_maximalComponents.mp hD
    refine ⟨stable_maximal_valid hK hD, hm.2.1.trans hKU, ?_⟩
    intro F hFV hFU hDF
    have hFK : F ⊆ K := iterate_preserves hFV hFU U.card
    exact hm.2.2 F hFV.1 hFK hDF
  · intro hD
    have hDK : D ⊆ K := iterate_preserves hD.1 hD.2.1 U.card
    obtain ⟨F, hF, hDF⟩ := component_has_maximal hD.1.1 hDK
    have hFV := stable_maximal_valid hK hF
    have hFU := (mem_maximalComponents.mp hF).2.1.trans hKU
    have hFD := hD.2.2 F hFV hFU hDF
    exact hFD ▸ hF

/-- Every valid component is contained in a returned maximal valid component. -/
theorem valid_covered_by_output {C : ComponentFamily Pair} {B : Finset Model}
    {row : Model → Pair → Row} {priority : Model → Pair → ℕ}
    {θ : Model} {U E : Finset Pair}
    (hV : Valid C B row priority θ E) (hEU : E ⊆ U) :
    ∃ D ∈ output C B row priority θ U, E ⊆ D := by
  exact component_has_maximal hV.1 (iterate_preserves hV hEU U.card)

end HiddenParity
