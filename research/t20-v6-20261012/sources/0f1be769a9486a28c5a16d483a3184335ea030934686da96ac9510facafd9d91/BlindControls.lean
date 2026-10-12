import BlindGuessSharpness
open MeasureTheory Set Filter
open scoped Topology
namespace BlindAudit
open Orthemology.Tranche2 Orthemology.Tranche2.FiniteQuery

def success (a : ℝ) (e : ℕ → ℝ) : Set (ℝ × Oracle) :=
  {z | ∀ᶠ n in atTop,
    blindAsk (run blindAsk blindNext z.2 z.1 n).1 = false ∧
    BinaryGood a (e n) (1/2+(run blindAsk blindNext z.2 z.1 n).1*e n)}

theorem dirac_wrong_guess_zero (a guess : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (hne : guess ≠ a) (o : Oracle) (e : ℕ → ℝ)
    (he0 : ∀ n, 0 < e n) (he1 : ∀ n, e n ≤ 1/4)
    (he : Tendsto e atTop (𝓝 0)) :
    Measure.dirac (guess,o) (success a e) = 0 := by
  have h := blind_causal_success_mass a ha0 ha1 e he0 he1 he
    (Measure.dirac guess) (Measure.dirac (guess,o)) (Measure.map_dirac measurable_fst (guess,o))
  simpa [success, Measure.dirac_apply', hne] using h

theorem dirac_correct_guess_one (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1)
    (o : Oracle) (e : ℕ → ℝ)
    (he0 : ∀ n, 0 < e n) (he1 : ∀ n, e n ≤ 1/4)
    (he : Tendsto e atTop (𝓝 0)) :
    Measure.dirac (a,o) (success a e) = 1 := by
  have h := blind_causal_success_mass a ha0 ha1 e he0 he1 he
    (Measure.dirac a) (Measure.dirac (a,o)) (Measure.map_dirac measurable_fst (a,o))
  simpa [success] using h

end BlindAudit
#print axioms BlindAudit.dirac_wrong_guess_zero
#print axioms BlindAudit.dirac_correct_guess_one
