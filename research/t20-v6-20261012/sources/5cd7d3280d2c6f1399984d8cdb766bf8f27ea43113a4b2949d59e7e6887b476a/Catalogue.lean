import Bound
import Mathlib.Data.Fintype.Pi
import Mathlib.Data.Fintype.Sigma

/-! Explicit finite bounded tree families. The finite catalogue is constructed
from finite rule labels, not supplied as an admission or attainment premise. -/
namespace GuardedTree
universe u v w
variable {J : Type u} {E : Type v} {R : Type w} (G : Grammar J E R)
open Tree

/-- Height is branch length, counting each rule occurrence. -/
def Bounded (h : ℕ) (t : Tree G) : Prop :=
  ∀ p, Branch G t p → p.length ≤ h

/-- A finite recursive syntax code for trees of height at most h. Nullary rules
already have a code at height one, since their child function has empty domain. -/
def Shape : ℕ → Type w
  | 0 => PEmpty
  | h + 1 => (r : R) × (Fin (G.arity r) → Shape h)

instance shapeFintype [Fintype R] : (h : ℕ) → Fintype (Shape G h)
  | 0 => inferInstanceAs (Fintype PEmpty.{w+1})
  | h + 1 => by
    change Fintype ((r : R) × (Fin (G.arity r) → Shape G h))
    letI := shapeFintype h
    infer_instance

/-- Decode a shape as an actual occurrence tree. -/
def decode : (h : ℕ) → Shape G h → Tree G
  | 0, s => PEmpty.elim s
  | h + 1, ⟨r, child⟩ => .node r (fun i => decode h (child i))

theorem decode_bounded (h : ℕ) (s : Shape G h) : Bounded G h (decode G h s) := by
  induction h with
  | zero => exact PEmpty.elim s
  | succ h ih =>
    rcases s with ⟨r, child⟩
    intro p hp
    cases hp with
    | root => simp
    | down _ _ i p hp =>
      exact Nat.succ_le_succ (ih (child i) p hp)

/-- Every branch-bounded tree has a code; no validity assumption is used. -/
theorem bounded_has_shape {h : ℕ} {t : Tree G} (hb : Bounded G h t) :
    ∃ s : Shape G h, decode G h s = t := by
  classical
  induction h generalizing t with
  | zero =>
    have hfalse := hb [t] (.root t)
    simp at hfalse
  | succ h ih =>
    cases t with
    | node r child =>
      have hc : ∀ i, Bounded G h (child i) := by
        intro i p hp
        exact Nat.le_of_succ_le_succ (hb (.node r child :: p) (.down r child i p hp))
      choose codes heq using (fun i => ih (hc i))
      refine ⟨⟨r, codes⟩, ?_⟩
      simp only [decode]
      exact congrArg (Tree.node r) (funext heq)

/-- All bounded trees, computed at the level of finite syntax codes. Classical
deduplication is allowed; effective enumeration is a separate obligation. -/
noncomputable def boundedCatalogue [Fintype R] (h : ℕ) : Finset (Tree G) := by
  classical
  exact Finset.univ.image (decode G h)

theorem mem_boundedCatalogue_iff [Fintype R] (h : ℕ) (t : Tree G) :
    t ∈ boundedCatalogue G h ↔ Bounded G h t := by
  classical
  constructor
  · intro ht
    obtain ⟨s, _, rfl⟩ := Finset.mem_image.mp ht
    exact decode_bounded G h s
  · intro ht
    obtain ⟨s, hs⟩ := bounded_has_shape G ht
    exact Finset.mem_image.mpr ⟨s, Finset.mem_univ _, hs⟩

variable [DecidableEq E]

/-- Filtering checks the actual grammar validity and exact state. -/
noncomputable def exactCatalogue [Fintype R] (h : ℕ) (q : J) (S : Finset E) :
    Finset (Tree G) := by
  classical
  exact (boundedCatalogue G h).filter (fun t =>
    Valid G t ∧ judgement G t = q ∧ support G t = S)

theorem mem_exactCatalogue_iff [Fintype R] (h : ℕ) (q : J) (S : Finset E) (t : Tree G) :
    t ∈ exactCatalogue G h q S ↔
      Bounded G h t ∧ Valid G t ∧ judgement G t = q ∧ support G t = S := by
  classical
  simp only [exactCatalogue, Finset.mem_filter, mem_boundedCatalogue_iff]

#print axioms bounded_has_shape
#print axioms mem_boundedCatalogue_iff
end GuardedTree
