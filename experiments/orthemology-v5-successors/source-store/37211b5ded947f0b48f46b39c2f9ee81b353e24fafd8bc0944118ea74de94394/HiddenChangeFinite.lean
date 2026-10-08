import CertificateData
import CertificatePath
import RegionAlgorithm

/-! Exact finite two-layer criterion for one hidden irreversible change.
No stochastic-law or winning-policy predicate occurs in this module. Both
layers use the same explicitly declared full-support menu. -/
namespace HiddenChange
open HiddenParity

abbrev Mode := Fin 2
abbrev State (n : ℕ) := Fin n
abbrev Action (k : ℕ) := Fin k
abbrev Pair (n k : ℕ) := OrthemicCertificate.Pair n k
abbrev Input (n k : ℕ) := OrthemicCertificate.Input 2 n k
abbrev Region (n : ℕ) := Finset (State n)
abbrev PairSet (n k : ℕ) := Finset (Pair n k)
abbrev PhysicalPath (n k : ℕ) := OrthemicCertificate.Path (State n) (Action k)
variable {n k : ℕ}

def commonMenu (I : Input n k) (s : State n) : Finset (Action k) :=
  I.menu Finset.univ s

def Admissible (I : Input n k) : Prop :=
  I.Valid ∧ ∀ s, (commonMenu I s).Nonempty
instance (I : Input n k) : Decidable (Admissible I) := by
  unfold Admissible OrthemicCertificate.Input.Valid
  infer_instance

def succ (I : Input n k) (θ : Mode) (e : Pair n k) : Region n :=
  Finset.univ.filter (fun y => 0 < I.row θ e y)

def internalSucc (I : Input n k) (θ : Mode) (e : Pair n k) : Region n :=
  Finset.univ.filter (fun y => 0 < I.row θ e y ∧ 0 < I.row 0 e y)

def EvenMinimum (I : Input n k) (σ : Mode) (E : PairSet n k) : Prop :=
  ∃ e ∈ E, I.priority σ e % 2 = 0 ∧ ∀ f ∈ E, I.priority σ e ≤ I.priority σ f
instance (I : Input n k) (σ : Mode) (E : PairSet n k) :
    Decidable (EvenMinimum I σ E) := by unfold EvenMinimum; infer_instance

theorem evenMinimum_iff (I : Input n k) (σ : Mode) (E : PairSet n k) :
    EvenMinimum I σ E ↔ ∃ d, IsMinimum (I.priority σ) E d ∧ d % 2 = 0 := by
  constructor
  · rintro ⟨e, he, hp, hmin⟩
    exact ⟨I.priority σ e, ⟨⟨e, he, rfl⟩, hmin⟩, hp⟩
  · rintro ⟨d, ⟨⟨e, he, hd⟩, hmin⟩, hp⟩
    exact ⟨e, he, hd.symm ▸ hp, hd.symm ▸ hmin⟩

def KnownGood (I : Input n k) (E : PairSet n k) : Prop :=
  IsEndComponent Prod.fst (succ I 1) E ∧ EvenMinimum I 1 E
instance (I : Input n k) (E : PairSet n k) : Decidable (KnownGood I E) := by
  unfold KnownGood; infer_instance

def UncertainGood (I : Input n k) (θ : Mode) (E : PairSet n k) : Prop :=
  IsEndComponent Prod.fst (succ I θ) E ∧
  (∀ e ∈ E, ∀ y, 0 < I.row θ e y → 0 < I.row 0 e y) ∧
  (∀ σ : Mode, Match I.row θ σ E → EvenMinimum I σ E)
instance (I : Input n k) (θ : Mode) (E : PairSet n k) : Decidable (UncertainGood I θ E) := by
  unfold UncertainGood; infer_instance

def knownAllowed (I : Input n k) (K : Region n) : PairSet n k :=
  Finset.univ.filter (fun e => e.1 ∈ K ∧ e.2 ∈ commonMenu I e.1 ∧
    ∀ y, 0 < I.row 1 e y → y ∈ K)

def uncertainAllowed (I : Input n k) (K W : Region n) : PairSet n k :=
  Finset.univ.filter (fun e => e.1 ∈ W ∧ e.2 ∈ commonMenu I e.1 ∧
    (∀ y, 0 < I.row 0 e y → y ∈ W) ∧
    (∀ y, 0 < I.row 1 e y → I.row 0 e y = 0 → y ∈ K))

@[simp] theorem mem_knownAllowed (I : Input n k) (K : Region n) (e : Pair n k) :
    e ∈ knownAllowed I K ↔ e.1 ∈ K ∧ e.2 ∈ commonMenu I e.1 ∧
      ∀ y, 0 < I.row 1 e y → y ∈ K := by simp [knownAllowed]
@[simp] theorem mem_uncertainAllowed (I : Input n k) (K W : Region n) (e : Pair n k) :
    e ∈ uncertainAllowed I K W ↔ e.1 ∈ W ∧ e.2 ∈ commonMenu I e.1 ∧
      (∀ y, 0 < I.row 0 e y → y ∈ W) ∧
      (∀ y, 0 < I.row 1 e y → I.row 0 e y = 0 → y ∈ K) := by simp [uncertainAllowed]

def KnownProgress (I : Input n k) (D : PairSet n k) (s : State n) : Prop :=
  ∃ E ∈ D.powerset, KnownGood I E ∧
    ∃ t ∈ usedStates Prod.fst E, Reach Prod.fst (succ I 1) D s t
instance (I : Input n k) (D : PairSet n k) (s : State n) : Decidable (KnownProgress I D s) := by
  unfold KnownProgress; infer_instance

def UncertainProgress (I : Input n k) (K : Region n)
    (D : PairSet n k) (θ : Mode) (s : State n) : Prop :=
  (∃ E ∈ D.powerset, UncertainGood I θ E ∧
    ∃ t ∈ usedStates Prod.fst E, Reach Prod.fst (internalSucc I θ) D s t) ∨
  (∃ e ∈ D, ∃ y ∈ K, Reach Prod.fst (internalSucc I θ) D s e.1 ∧
    0 < I.row θ e y ∧ I.row 0 e y = 0)
instance (I : Input n k) (K : Region n) (D : PairSet n k) (θ : Mode) (s : State n) :
    Decidable (UncertainProgress I K D θ s) := by unfold UncertainProgress; infer_instance

def F1 (I : Input n k) (K : Region n) : Region n :=
  K.filter (KnownProgress I (knownAllowed I K))
def F (I : Input n k) (K W : Region n) : Region n :=
  W.filter (fun s => ∀ θ : Mode, UncertainProgress I K (uncertainAllowed I K W) θ s)

@[simp] theorem mem_F1 (I : Input n k) (K : Region n) (s : State n) :
    s ∈ F1 I K ↔ s ∈ K ∧ KnownProgress I (knownAllowed I K) s := Finset.mem_filter
@[simp] theorem mem_F (I : Input n k) (K W : Region n) (s : State n) :
    s ∈ F I K W ↔ s ∈ W ∧ ∀ θ : Mode, UncertainProgress I K (uncertainAllowed I K W) θ s :=
  Finset.mem_filter

theorem knownAllowed_mono (I : Input n k) : Monotone (knownAllowed I) := by
  intro K K' hK e he
  rcases (mem_knownAllowed I K e).mp he with ⟨hs, hm, hc⟩
  exact (mem_knownAllowed I K' e).mpr ⟨hK hs, hm, fun y hy => hK (hc y hy)⟩
theorem uncertainAllowed_mono (I : Input n k) {K K' W W' : Region n}
    (hK : K ⊆ K') (hW : W ⊆ W') : uncertainAllowed I K W ⊆ uncertainAllowed I K' W' := by
  intro e he
  rcases (mem_uncertainAllowed I K W e).mp he with ⟨hs, hm, hc, hr⟩
  exact (mem_uncertainAllowed I K' W' e).mpr
    ⟨hW hs, hm, fun y hy => hW (hc y hy), fun y hy hz => hK (hr y hy hz)⟩

theorem knownProgress_mono (I : Input n k) {D D' : PairSet n k}
    (hD : D ⊆ D') {s : State n} (h : KnownProgress I D s) : KnownProgress I D' s := by
  rcases h with ⟨E, hE, hg, t, ht, hr⟩
  exact ⟨E, Finset.mem_powerset.mpr ((Finset.mem_powerset.mp hE).trans hD),
    hg, t, ht, reach_mono hD hr⟩
theorem uncertainProgress_mono (I : Input n k) {K K' : Region n} {D D' : PairSet n k}
    (hK : K ⊆ K') (hD : D ⊆ D') {θ : Mode} {s : State n}
    (h : UncertainProgress I K D θ s) : UncertainProgress I K' D' θ s := by
  rcases h with ⟨E, hE, hg, t, ht, hr⟩ | ⟨e, he, y, hy, hr, hp, hz⟩
  · exact Or.inl ⟨E, Finset.mem_powerset.mpr ((Finset.mem_powerset.mp hE).trans hD),
      hg, t, ht, reach_mono hD hr⟩
  · exact Or.inr ⟨e, hD he, y, hK hy, reach_mono hD hr, hp, hz⟩
theorem F1_mono (I : Input n k) : Monotone (F1 I) := by
  intro K K' hK s hs
  rcases (mem_F1 I K s).mp hs with ⟨hs, hp⟩
  exact (mem_F1 I K' s).mpr ⟨hK hs, knownProgress_mono I (knownAllowed_mono I hK) hp⟩
theorem F1_subset (I : Input n k) (K : Region n) : F1 I K ⊆ K := Finset.filter_subset _ _
theorem F_mono_both (I : Input n k) {K K' W W' : Region n}
    (hK : K ⊆ K') (hW : W ⊆ W') : F I K W ⊆ F I K' W' := by
  intro s hs
  rcases (mem_F I K W s).mp hs with ⟨hs, hp⟩
  exact (mem_F I K' W' s).mpr ⟨hW hs, fun θ =>
    uncertainProgress_mono I hK (uncertainAllowed_mono I hK hW) (hp θ)⟩
theorem F_mono (I : Input n k) (K : Region n) : Monotone (F I K) :=
  fun _ _ hW => F_mono_both I (Finset.Subset.refl _) hW
theorem F_subset (I : Input n k) (K W : Region n) : F I K W ⊆ W := Finset.filter_subset _ _

def knownRegion (I : Input n k) : Region n :=
  HiddenParity.Necessity.descend (F1 I) n Finset.univ
def uncertainRegion (I : Input n k) : Region n :=
  HiddenParity.Necessity.descend (F I (knownRegion I)) n Finset.univ

theorem knownRegion_fixed (I : Input n k) : F1 I (knownRegion I) = knownRegion I :=
  HiddenParity.Necessity.descend_stable _ (F1_subset I) _ _ (by simp)
theorem knownRegion_greatest (I : Input n k) (K : Region n)
    (hK : K ⊆ F1 I K) : K ⊆ knownRegion I :=
  HiddenParity.Necessity.postfixed_subset_descend _ (F1_mono I) hK (Finset.subset_univ _) n
theorem uncertainRegion_fixed (I : Input n k) :
    F I (knownRegion I) (uncertainRegion I) = uncertainRegion I :=
  HiddenParity.Necessity.descend_stable _ (F_subset I _) _ _ (by simp)
theorem uncertainRegion_greatest (I : Input n k) (W : Region n)
    (hW : W ⊆ F I (knownRegion I) W) : W ⊆ uncertainRegion I :=
  HiddenParity.Necessity.postfixed_subset_descend _ (F_mono I _) hW (Finset.subset_univ _) n

end HiddenChange
