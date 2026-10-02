import CanonicalInvariantSafety
import RecursiveKernelEquivalence

noncomputable section
set_option linter.unusedSectionVars false
open MeasureTheory ProbabilityTheory Filter Set Finset
open scoped BigOperators ENNReal
namespace Orthemology.Tranche3
open Orthemology.Tranche2
open Orthemology.Tranche2.PolicyEmbedding
universe u v
variable {Θ A Y : Type u} {R : Type v}
    [Fintype Θ] [Fintype A] [Fintype Y] [DecidableEq Θ] [DecidableEq A] [Inhabited Y]
    [MeasurableSpace R] [MeasurableSpace A] [MeasurableSingletonClass A]
    [MeasurableSpace Y] [MeasurableSingletonClass Y]

/-- Absence of a progress witness says exactly that true-positive observations
of recursively admissible actions preserve the entire current live support. -/
lemma no_recursive_progress_preserves_support
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)
    (B : Finset Θ) (θ : {θ // θ ∈ B})
    (hn : ¬ recursiveProgress P good menu B θ)
    (a : A) (ha : a ∈ recursiveAllowed P good menu B) (y : Y) (hy : 0 < P θ.val a y) :
    supportUpdate P B a y = B := by
  by_contra he
  exact hn ⟨a,ha,y,(supportStay_false P B a y).mpr he,hy⟩

/-- General zero-support deterministic necessity. The induction examines every
positive strict successor of every feasible same-support policy history; it does
not infer an all-branch certificate from one favorable eventual path. -/
theorem fixedSeedWinning_recursive_necessity
    (P : Θ → A → Y → ℝ) (good : Θ → Finset A) (menu : Finset Θ → Finset A)
    (hP : ∀ θ a y, 0 ≤ P θ a y) (hN : ∀ θ a, ∑ y, P θ a y = 1)
    (d : A) (B : Finset Θ) (hB : B.Nonempty) (π : R → History A Y → A) (r : R)
    (hw : FixedSeedWinning P good menu hP hN d B π r) : RecursiveWinning P good menu B := by
  classical
  induction B using Finset.strongInductionOn generalizing π r with
  | _ B ih =>
    have hadmit : ∀ h : History A Y, ActionCompatible π r h → historySupport P B h = B →
        π r h ∈ recursiveAllowed P good menu B := by
      intro h hc he
      have hn : (historySupport P B h).Nonempty := by rwa [he]
      have hmenu : π r h ∈ menu B := by simpa only [he] using hw.2.1 h hc hn
      simp only [recursiveAllowed,Finset.mem_filter]
      refine ⟨hmenu,?_⟩
      intro y hy hstrict
      have hcont := fixedSeedWinning_at_history P good menu hP hN d B π r hw h hc hn
      rw [he] at hcont
      have hstep := fixedSeedWinning_one_step P good menu hP hN d B (continuePolicy π h) r hcont y
      have heact : continuePolicy π h r [] = π r h := rfl
      rw [heact] at hstep
      exact ih (supportUpdate P B (π r h) y)
        (Finset.ssubset_iff_subset_ne.mpr ⟨supportUpdate_subset P B (π r h) y,hstrict⟩)
        hy _ r hstep
    rw [recursiveWinning_iff_stage,stageCertificate_iff_witness]
    refine ⟨hB,?_⟩
    intro θ
    by_cases hp : recursiveProgress P good menu B θ
    · exact Or.inl hp
    · right
      have hpres := no_recursive_progress_preserves_support P good menu B θ hp
      let I : History A Y → Prop := fun h => ActionCompatible π r h ∧ historySupport P B h = B
      have hi : I [] := ⟨True.intro,rfl⟩
      have hinv : ∀ h y, I h → 0 < P θ.val (π r h) y → I ((π r h,y)::h) := by
        intro h y hh hy
        refine ⟨⟨hh.1,rfl⟩,?_⟩
        simp only [historySupport,hh.2]
        exact hpres (π r h) (hadmit h hh.1 hh.2) y hy
      have hall : ∀ᵐ x ∂actionLaw π (Measure.dirac r) (P θ.val) (hP θ.val) (hN θ.val) d,
          ∀ n, x n ∈ recursiveAllowed P good menu B :=
        fixedSeed_always_of_invariant π hw.1 r (P θ.val) (hP θ.val) (hN θ.val)
          (recursiveAllowed P good menu B) I hi hinv (fun h hh => hadmit h hh.1 hh.2) d
      have hdom : ∀ η ∈ B, ∀ a ∈ recursiveAllowed P good menu B, ∀ y,
          0 < P θ.val a y → 0 < P η a y := by
        intro η hη a ha y hy
        have he := hpres a ha y hy
        have hm : η ∈ supportUpdate P B a y := by rwa [he]
        exact ((mem_supportUpdate P B a y η).mp hm).2
      obtain ⟨U,hne,hU,hgood,hsv⟩ := stable_model_self_verifying_necessity P good B
        (recursiveAllowed P good menu B) hP hN π hw.1 (Measure.dirac r) d θ.val θ.property hw.2.2 hall hdom
      refine ⟨U,hne,hU,hgood,?_⟩
      intro η hag
      exact hsv η.val η.property hag
end Orthemology.Tranche3
