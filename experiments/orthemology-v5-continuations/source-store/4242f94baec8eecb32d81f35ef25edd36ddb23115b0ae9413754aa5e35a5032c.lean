import SCCParity
import GlobalParityNecessity

/-! A genuine SCC-substituted support-recursive region reference. The executable
roots below call the SCC target selector, never the exhaustive reference. The
proofs refine the unchanged reference and transport its necessity certificate.
No polynomial bound for the outer support recursion is claimed. -/
namespace HiddenParity.SCCRegion
open HiddenParity.Stage
universe u v w
variable {State Action : Type u} {Model : Type w}
variable [Fintype State] [Fintype Action] [DecidableEq State] [DecidableEq Action]
variable [DecidableEq Model]

/-- Unchanged all-branch licensing and finite reachability, with an actual
SCC-based target call at every candidate. This is not an alias to regionStep. -/
def regionStep (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (lower : Finset Model → Finset State) (W : Finset State) : Finset State :=
  W.filter (fun s => ∀ θ ∈ B,
    ReachableExit P B θ (Necessity.regionAllowed P menu B lower W) s ∨
      ∃ t ∈ SCCPruning.markovTarget P Prod.fst B priority θ
        (Necessity.regionAllowed P menu B lower W),
        Reach Prod.fst (internalSuccessors P B) (Necessity.regionAllowed P menu B lower W) s t)

/-- Actual recursive computation, using this module's SCC stage at every
support depth. State descent is the unchanged bounded finite loop. -/
def computedRegion (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ) :
    ℕ → Finset Model → Finset State
  | 0, _ => ∅
  | n+1, B => if B.Nonempty then
      Necessity.descend (regionStep P menu priority B (computedRegion P menu priority n))
        (Fintype.card State) Finset.univ else ∅

/-- The SCC version at the canonical support-cardinality fuel. -/
def winningRegion (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) : Finset State := computedRegion P menu priority B.card B

/-- Selector refinement is proved, not a parameter assumed by the caller. -/
theorem regionStep_eq (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (lower : Finset Model → Finset State) (W : Finset State) :
    regionStep P menu priority B lower W = Necessity.regionStep P menu priority B lower W := by
  simp only [regionStep, Necessity.regionStep, SCCPruning.markovTarget_eq]

/-- Equality holds for every fuel, including underfuelled references; semantic
necessity uses the original cardinality condition separately. -/
theorem computedRegion_eq (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (fuel : ℕ) (B : Finset Model) :
    computedRegion P menu priority fuel B = Necessity.computedRegion P menu priority fuel B := by
  induction fuel generalizing B with
  | zero => rfl
  | succ n ih =>
      have hLower : computedRegion P menu priority n = Necessity.computedRegion P menu priority n :=
        funext ih
      simp only [computedRegion, Necessity.computedRegion, hLower]
      have hStep : regionStep P menu priority B (Necessity.computedRegion P menu priority n) =
          Necessity.regionStep P menu priority B (Necessity.computedRegion P menu priority n) :=
        funext (regionStep_eq P menu priority B _)
      rw [hStep]

theorem winningRegion_eq (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) :
    winningRegion P menu priority B = Necessity.winningRegion P menu priority B :=
  computedRegion_eq P menu priority B.card B

/-- The substitution preserves the already proved support-fuel stability. -/
theorem computedRegion_fuel_irrelevant (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (B : Finset Model) (m n : ℕ) (hm : B.card ≤ m) (hn : B.card ≤ n) :
    computedRegion P menu priority m B = computedRegion P menu priority n B := by
  rw [computedRegion_eq, computedRegion_eq]
  exact Necessity.computedRegion_fuel_irrelevant P menu priority B m n hm hn

section SemanticCertificate
variable {R : Type v} [Inhabited State]
variable [MeasurableSpace R] [MeasurableSpace State] [MeasurableSingletonClass State]
variable [MeasurableSpace Action] [MeasurableSingletonClass Action]

/-- Every actual common lawful almost-sure policy lies in the SCC result.
The policy class is the unchanged measurable private-seed/full-history class. -/
theorem winning_policy_mem_winningRegion
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (d : State × Action) (B : Finset Model) (s : State)
    (w : Necessity.WinningPolicy (R := R) P menu priority d B s) :
    s ∈ winningRegion P menu priority B := by
  rw [winningRegion_eq]
  exact Necessity.winning_policy_mem_winningRegion P menu priority d B s w

/-- A negative output of the actual SCC-substituted computation rules out any
common lawful AS policy with the chosen arbitrary measurable seed space. -/
theorem computed_losing_excludes_common_policy
    (P : RationalKernel Model (State × Action) State)
    (menu : Finset Model → State → Finset Action) (priority : Model → (State × Action) → ℕ)
    (d : State × Action) (B : Finset Model) (s : State)
    (hLose : s ∉ winningRegion P menu priority B) :
    ¬ Necessity.SemanticWinning (R := R) P menu priority d B s := by
  rw [winningRegion_eq] at hLose
  exact Necessity.computed_losing_excludes_common_policy P menu priority d B s hLose
end SemanticCertificate
end HiddenParity.SCCRegion
