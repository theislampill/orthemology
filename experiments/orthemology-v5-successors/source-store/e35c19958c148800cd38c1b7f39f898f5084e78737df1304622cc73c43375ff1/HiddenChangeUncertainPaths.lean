import HiddenChangeActualRecurrence
import HiddenChangeRivalParity

noncomputable section
open MeasureTheory ProbabilityTheory Set Filter
open scoped BigOperators ENNReal
open Orthemology.Tranche2.PolicyEmbedding Orthemology.Tranche2.RecurrentSupport
open HiddenParity HiddenParity.Stochastic HiddenParity.ResidualSeed HiddenParity.Adaptive
open HiddenParity.ResidualSeed.Continuation

namespace HiddenChange
variable {n k : ℕ} [NeZero n] {R : Type*} [MeasurableSpace R]

omit [NeZero n] in
theorem zeroCompatible_nil (I : Input n k) : ZeroCompatible I ([] : PairHistory n k) := by
  simp [ZeroCompatible]

omit [NeZero n] in
theorem zeroCompatible_cons (I : Input n k) (e : Pair n k) (y : State n) (h : PairHistory n k) :
    ZeroCompatible I ((e,y)::h) ↔ 0 < I.row 0 e y ∧ ZeroCompatible I h := by
  simp [ZeroCompatible,Fin.forall_fin_succ]

omit [NeZero n] in
theorem coherent_compatible_prefix (I : Input n k) {H : PairTrace n k}
    (hc : CoherentTrace H) {a b : ℕ} (hab : a ≤ b) (hb : ZeroCompatible I (H b)) :
    ZeroCompatible I (H a) := by
  have he : a+(b-a)=b := by omega
  have hs := coherentTrace_take_append hc a (b-a)
  rw [he] at hs
  rw [hs,zeroCompatible_append] at hb
  exact hb.2

theorem coherent_edge_compatible_iff (I : Input n k) (s : State n) (d : Pair n k)
    {H : PairTrace n k} (hc : CoherentTrace H)
    (hs : ∀ t, (historyAction d H t).1 = currentState s (H t)) (t : ℕ) :
    ZeroCompatible I (H (t+1)) ↔
      0 < I.row 0 (historyAction d H t) (historyAction d H (t+1)).1 ∧ ZeroCompatible I (H t) := by
  obtain ⟨e,y,he⟩ := hc.2 t
  have ha : historyAction d H t = e := by simp [historyAction,he]
  have hy : (historyAction d H (t+1)).1 = y := by simpa only [he,currentState] using hs (t+1)
  rw [he,ha,hy,zeroCompatible_cons]

omit [NeZero n] in
theorem first_incompatible_after (I : Input n k) {H : PairTrace n k}
    (hc : CoherentTrace H) (L : ℕ) (hL : ZeroCompatible I (H L))
    (hbad : ¬ ∀ t, ZeroCompatible I (H t)) :
    ∃ j, L ≤ j ∧ (∀ t, t ≤ j → ZeroCompatible I (H t)) ∧ ¬ ZeroCompatible I (H (j+1)) := by
  classical
  have hEx : ∃ t, ¬ ZeroCompatible I (H t) := not_forall.mp hbad
  let q := Nat.find hEx
  have hq : ¬ ZeroCompatible I (H q) := Nat.find_spec hEx
  have hLq : L < q := by
    by_contra hh
    exact hq (coherent_compatible_prefix I hc (not_lt.mp hh) hL)
  have hqpos : 0 < q := by omega
  refine ⟨q-1,by omega,?_,?_⟩
  · intro t ht
    exact not_not.mp (Nat.find_min hEx (show t < q by omega))
  · have he : q-1+1=q := by omega
    rwa [he]

omit [NeZero n] in
/-- Finite segment extraction only needs safety and support on the segment. -/
theorem internal_segment_reachable (I : Input n k) (θ : Mode) (D : PairSet n k)
    (x : ℕ → Pair n k) (a b : ℕ) (hab : a ≤ b)
    (hsafe : ∀ t, a ≤ t → t < b → x t ∈ D)
    (hstep : ∀ t, a ≤ t → t < b →
      0 < I.row θ (x t) (x (t+1)).1 ∧ 0 < I.row 0 (x t) (x (t+1)).1) :
    Reach Prod.fst (internalSucc I θ) D (x a).1 (x b).1 := by
  induction b,hab using Nat.le_induction with
  | base => exact Relation.ReflTransGen.refl
  | succ j hj ih =>
    have hpre := ih (fun t ht hjt => hsafe t ht (by omega)) (fun t ht hjt => hstep t ht (by omega))
    exact hpre.tail ⟨x j,hsafe j hj (by omega),rfl,
      Finset.mem_filter.mpr ⟨Finset.mem_univ _,hstep j hj (by omega)⟩⟩

/-- A first actual revelation yields the finite internal-path/known-exit
alternative. The path is extracted from a supported positive-policy history. -/
theorem uncertain_exit_of_trace (I : Input n k) (hI : I.Valid) (θ : Mode)
    (K W : Region n) (s : State n) (d : Pair n k) (H : PairTrace n k) (L : ℕ)
    (hc : CoherentTrace H) (hs : ∀ t, (historyAction d H t).1 = currentState s (H t))
    (hL : ZeroCompatible I (H L))
    (hSupport : ∀ t, L ≤ t → 0 < I.row θ (historyAction d H t) (historyAction d H (t+1)).1)
    (hSafe : ∀ t, ZeroCompatible I (H t) → historyAction d H t ∈ uncertainAllowed I K W)
    (hbad : ¬ ∀ t, ZeroCompatible I (H t)) :
    UncertainProgress I K (uncertainAllowed I K W) θ (currentState s (H L)) := by
  obtain ⟨j,hLj,hcomp,hbadj⟩ := first_incompatible_after I hc L hL hbad
  let e := historyAction d H j
  let y := (historyAction d H (j+1)).1
  have he : e ∈ uncertainAllowed I K W := hSafe j (hcomp j (le_refl _))
  have hy : 0 < I.row θ e y := hSupport j hLj
  have hz : I.row 0 e y = 0 := by
    have hnot : ¬ 0 < I.row 0 e y := by
      intro hp
      exact hbadj ((coherent_edge_compatible_iff I s d hc hs j).mpr ⟨hp,hcomp j (le_refl _)⟩)
    exact le_antisymm (not_lt.mp hnot) (hI.2.2.1 0 e y)
  have hθ : θ = 1 := by
    fin_cases θ
    · change 0 < I.row 0 e y at hy
      rw [hz] at hy
      exact (lt_irrefl 0 hy).elim
    · rfl
  have hyK : y ∈ K := ((mem_uncertainAllowed I K W e).mp he).2.2.2 y (hθ ▸ hy) hz
  right
  refine ⟨e,he,y,hyK,?_,hy,hz⟩
  have hr := internal_segment_reachable I θ (uncertainAllowed I K W) (historyAction d H) L j hLj
    (fun t _ ht => hSafe t (hcomp t (by omega)))
    (fun t ht hj => ⟨hSupport t ht,
      ((coherent_edge_compatible_iff I s d hc hs t).mp (hcomp (t+1) (by omega))).1⟩)
  simpa only [hs L,e] using hr

end HiddenChange
