import FiniteChainLaw

noncomputable section
namespace HiddenParity.Cost.FiniteChainHitting
open HiddenParity.FiniteReachability
variable {Q : Type*} [Fintype Q] [DecidableEq Q]

namespace Path

omit [Fintype Q] [DecidableEq Q] in
lemma tail {edge : Q → Q → Prop} {s t u : Q} {n : ℕ}
    (path : Path edge s t n) (he : edge t u) : Path edge s u (n+1) := by
  induction path with
  | nil s => exact Path.cons he (Path.nil u)
  | cons hs _ ih => exact Path.cons hs (ih he)

omit [Fintype Q] [DecidableEq Q] in
/-- A finite directed path has a concrete finite walk, represented by a total
sequence whose values beyond its horizon are irrelevant. -/
lemma exists_walk {edge : Q → Q → Prop} {s t : Q} {n : ℕ}
    (path : Path edge s t n) :
    ∃ w : ℕ → Q, w 0=s ∧ w n=t ∧ ∀ i, i<n → edge (w i) (w (i+1)) := by
  induction path with
  | nil s => exact ⟨fun _ => s,rfl,rfl,by intro i hi; omega⟩
  | @cons s u t n he hpath ih =>
      obtain ⟨w,hw0,hwn,hwe⟩ := ih
      let v : ℕ → Q := fun k => match k with | 0 => s | k+1 => w k
      refine ⟨v,rfl,hwn,?_⟩
      intro i hi
      cases i with
      | zero => simpa only [v,hw0] using he
      | succ i => exact hwe i (by omega)

end Path

/-- A bounded-fuel saturation supplies a path of bounded length, retaining the
actual directed edge relation. -/
theorem saturate_has_bounded_path (edge : Q → Q → Prop) [DecidableRel edge]
    (s : Q) (n : ℕ) (R : Finset Q) (k : ℕ)
    (hR : ∀ t ∈ R, ∃ l, l ≤ k ∧ Path edge s t l) :
    ∀ t ∈ saturate edge n R, ∃ l, l ≤ k+n ∧ Path edge s t l := by
  induction n generalizing R k with
  | zero => simpa only [saturate,Nat.add_zero] using hR
  | succ n ih =>
      have hGrow : ∀ t ∈ grow edge R, ∃ l, l ≤ k+1 ∧ Path edge s t l := by
        intro t ht
        rcases (mem_grow edge).mp ht with ht | ⟨u,hu,he⟩
        · obtain ⟨l,hl,path⟩ := hR t ht
          exact ⟨l,by omega,path⟩
        · obtain ⟨l,hl,path⟩ := hR u hu
          exact ⟨l+1,by omega,path.tail he⟩
      have hh := ih (grow edge R) (k+1) hGrow
      simpa only [saturate,Nat.add_assoc,Nat.add_left_comm,Nat.add_comm] using hh

/-- Reachability admits at most |Q|-1 edges. This is derived from the accepted
finite saturation/cardinality theorem, rather than assumed as a graph premise. -/
theorem reachable_short_path (edge : Q → Q → Prop) [DecidableRel edge]
    (s t : Q) (hreach : Relation.ReflTransGen edge s t) :
    ∃ n, n ≤ Fintype.card Q - 1 ∧ Path edge s t n := by
  let R := saturate edge (Fintype.card Q-1) {s}
  have hstable : grow edge R = R :=
    saturate_stable edge (Fintype.card Q-1) {s} (by simp)
  have hstart : s ∈ R := subset_saturate edge _ _ (Finset.mem_singleton_self s)
  have hclosed : ∀ u ∈ R, ∀ v, edge u v → v ∈ R := by
    intro u hu v huv
    rw [← hstable]
    exact (mem_grow edge).mpr (Or.inr ⟨u,hu,huv⟩)
  have ht : t ∈ R := by
    induction hreach with
    | refl => exact hstart
    | tail _ he ih => exact hclosed _ ih _ he
  have hh := saturate_has_bounded_path edge s (Fintype.card Q-1) {s} 0 (by
    intro u hu
    have he : u = s := Finset.mem_singleton.mp hu
    subst u
    exact ⟨0,le_rfl,Path.nil s⟩) t ht
  simpa only [Nat.zero_add] using hh

variable [MeasurableSpace Q] [MeasurableSingletonClass Q]

/-- Actual finite-chain geometric survival probability from unbounded directed
reachability, with the explicit finite cardinality bound derived internally. -/
theorem absorbedLaw_geometric_of_reachable (P : Rows Q) (goal : Q → Prop) [DecidablePred goal]
    (p : ℝ) (hp : 0 ≤ p) (hp1 : p ≤ 1)
    (hmin : ∀ s t, 0 < P.row s t → p ≤ P.row s t)
    (hreach : ∀ s, ∃ t, goal t ∧ Relation.ReflTransGen (fun u v => 0 < P.row u v) s t)
    (k : ℕ) (s : Q) :
    (absorbedLaw P goal (k*(Fintype.card Q-1)) s).toMeasure {t | ¬ goal t} ≤
      ENNReal.ofReal ((1-p^(Fintype.card Q-1))^k) := by
  classical
  apply absorbedLaw_geometric_survival P goal p hp hp1 hmin (Fintype.card Q-1) ?_ k s
  intro u
  obtain ⟨t,ht,hut⟩ := hreach u
  obtain ⟨n,hn,path⟩ := reachable_short_path (fun u v => 0 < P.row u v) u t hut
  exact ⟨t,n,ht,hn,path⟩

end HiddenParity.Cost.FiniteChainHitting
