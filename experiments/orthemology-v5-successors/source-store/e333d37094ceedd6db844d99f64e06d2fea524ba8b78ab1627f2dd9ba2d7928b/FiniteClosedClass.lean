import FinitePathBound

noncomputable section
namespace HiddenParity.Cost.FiniteChainHitting
open HiddenParity.FiniteReachability
variable {Q : Type*} [Fintype Q] [DecidableEq Q]

/-- A nonempty forward-closed strongly connected set of finite graph vertices. -/
def ClosedClass (edge : Q → Q → Prop) (C : Finset Q) : Prop :=
  C.Nonempty ∧ (∀ s ∈ C, ∀ t, edge s t → t ∈ C) ∧
    ∀ s ∈ C, ∀ t ∈ C, Relation.ReflTransGen edge s t

/-- Minimize a finite reachable-set cardinality to find a closed strongly
connected class. This works for directed graphs and needs no probabilistic
recurrence theorem or assumed fair run. -/
theorem exists_reachable_closed_class (edge : Q → Q → Prop) [DecidableRel edge] (s : Q) :
    ∃ C : Finset Q, ClosedClass edge C ∧ ∀ t ∈ C, Relation.ReflTransGen edge s t := by
  have hs : s ∈ reachable edge s := (reachable_iff edge s s).mpr Relation.ReflTransGen.refl
  obtain ⟨v,hv,hmin⟩ := Finset.exists_min_image (reachable edge s) (fun t => (reachable edge t).card) ⟨s,hs⟩
  let C := reachable edge v
  have hvC : v ∈ C := (reachable_iff edge v v).mpr Relation.ReflTransGen.refl
  have hsC : ∀ t ∈ C, Relation.ReflTransGen edge s t := by
    intro t ht
    exact ((reachable_iff edge s v).mp hv).trans ((reachable_iff edge v t).mp ht)
  have hclosed : ∀ u ∈ C, ∀ t, edge u t → t ∈ C := by
    intro u hu t hut
    exact (reachable_iff edge v t).mpr (((reachable_iff edge v u).mp hu).tail hut)
  refine ⟨C,⟨⟨v,hvC⟩,hclosed,?_⟩,hsC⟩
  intro u hu t ht
  have hsub : reachable edge u ⊆ C := by
    intro x hx
    exact (reachable_iff edge v x).mpr
      (((reachable_iff edge v u).mp hu).trans ((reachable_iff edge u x).mp hx))
  have hcard : C.card ≤ (reachable edge u).card := hmin u ((reachable_iff edge s u).mpr (hsC u hu))
  have heq : reachable edge u = C := Finset.eq_of_subset_of_card_le hsub hcard
  exact (reachable_iff edge u t).mp (heq.symm ▸ ht)

/-- Excluding every nonempty closed class disjoint from the goal derives
positive-path reachability from every vertex. This is the finite graph bridge
used by dangerous navigation and mismatching operation. -/
theorem reaches_goal_of_no_avoiding_class (edge : Q → Q → Prop) [DecidableRel edge]
    (goal : Q → Prop)
    (hclasses : ∀ C, ClosedClass edge C → ∃ t ∈ C, goal t) :
    ∀ s, ∃ t, goal t ∧ Relation.ReflTransGen edge s t := by
  intro s
  obtain ⟨C,hC,hReach⟩ := exists_reachable_closed_class edge s
  obtain ⟨t,ht,hGoal⟩ := hclasses C hC
  exact ⟨t,hGoal,hReach t ht⟩

variable [MeasurableSpace Q] [MeasurableSingletonClass Q]

/-- A complete finite PMF geometric-tail theorem from row normalization,
minimum positive edge weight, and the closed-class graph criterion. -/
theorem absorbedLaw_geometric_of_closed_classes
    (P : Rows Q) (goal : Q → Prop) [DecidablePred goal]
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hmin : ∀ s t, 0 < P.row s t → p ≤ P.row s t)
    (hclasses : ∀ C, ClosedClass (fun s t => 0 < P.row s t) C → ∃ t ∈ C, goal t)
    (k : ℕ) (s : Q) :
    (absorbedLaw P goal (k*(Fintype.card Q-1)) s).toMeasure {t | ¬ goal t} ≤
      ENNReal.ofReal ((1-p^(Fintype.card Q-1))^k) := by
  classical
  exact absorbedLaw_geometric_of_reachable P goal p hp hp1 hmin
    (reaches_goal_of_no_avoiding_class _ goal hclasses) k s

end HiddenParity.Cost.FiniteChainHitting
