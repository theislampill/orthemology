import FiniteTable

/-! Constructive ordered enumeration. No equality decision on trees, quotient
representative selection, or classical choice is used by these definitions. -/
namespace GuardedTree.Witness

/-- Explicit input order; duplicates are harmless. The completeness proof is erased. -/
structure RuleList (R : Type*) where
  rules : List R
  complete : ∀ r, r ∈ rules

/-- Cartesian powers retain every premise occurrence and its position.
The zero-th power has one empty tuple even when the input list is empty. -/
def tuples {A : Type*} (xs : List A) : (n : ℕ) → List (Fin n → A)
  | 0 => []
  | n+1 => xs.flatMap fun a => (tuples xs n).map (Fin.cons a)

theorem mem_tuples {A : Type*} (xs : List A) (n : ℕ) (f : Fin n → A) :
    f ∈ tuples xs n ↔ ∀ i, f i ∈ xs := by
  induction n with
  | zero =>
    have hf : f = Fin.elim0 := by funext i; exact Fin.elim0 i
    simp [tuples, hf]
  | succ n ih =>
    simp only [tuples, List.mem_flatMap, List.mem_map]
    constructor
    · rintro ⟨a, ha, g, hg, rfl⟩ i
      refine Fin.cases ?_ (fun j => ?_) i
      · simpa using ha
      · simpa using (ih g).mp hg j
    · intro hf
      refine ⟨f 0, hf 0, Fin.tail f, (ih _).mpr (fun i => hf i.succ), ?_⟩
      exact Fin.cons_self_tail f

variable {J E R : Type*} (G : Grammar J E R)

/-- The finite syntax family at height h, constructed as an ordered list. -/
def shapes (rs : RuleList R) : (h : ℕ) → List (Shape G h)
  | 0 => []
  | h+1 => rs.rules.flatMap fun r =>
      (tuples (shapes rs h) (G.arity r)).map (Sigma.mk r)

theorem mem_shapes (rs : RuleList R) (h : ℕ) (s : Shape G h) :
    s ∈ shapes G rs h := by
  induction h with
  | zero => exact PEmpty.elim s
  | succ h ih =>
    rcases s with ⟨r, cs⟩
    exact List.mem_flatMap.mpr ⟨r, rs.complete r,
      List.mem_map.mpr ⟨cs, (mem_tuples _ _ _).mpr (fun i => ih (cs i)), rfl⟩⟩

/-- A list of actual finite occurrence trees. It deliberately does not deduplicate. -/
def trees (rs : RuleList R) (h : ℕ) : List (Tree G) :=
  (shapes G rs h).map (decode G h)

theorem mem_trees (rs : RuleList R) (h : ℕ) (t : Tree G) :
    t ∈ trees G rs h ↔ Bounded G h t := by
  constructor
  · intro ht
    obtain ⟨s, _, rfl⟩ := List.mem_map.mp ht
    exact decode_bounded G h s
  · intro hb
    obtain ⟨s, hs⟩ := bounded_has_shape G hb
    exact List.mem_map.mpr ⟨s, mem_shapes G rs h s, hs⟩

#print axioms mem_trees
end GuardedTree.Witness
