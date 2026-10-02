import ObserverAbstraction
import P01CanonicalCarrierProjection

/-! Heterogeneous *observer-state* transport over the existing typed contextual
PER core. This does not identify different PER notions of term equality, nor
supply a new dependent type syntax or an executable observer for every term. -/
namespace Orthemology.CertifiedObserver
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open OrthemologyV2 OrthemologyV3 P01D
open Set MeasureTheory
open scoped ENNReal

/-- The runtime-state carrier may genuinely vary with the typed valuation.
The compatibility fields are local operational obligations, never a premise
of equality of complete laws. -/
structure ObserverFamily {Γ : Context} (A : P01D.Ty Γ) where
  State : Γ.Val → Type
  machine : (γ : Γ.Val) → Mealy (State γ)
  start : (γ : Γ.Val) → Term → State γ
  relates : (γ δ : Γ.Val) → State γ → State δ → Prop
  initial : ∀ {γ δ}, Γ.eqv γ δ → ∀ {x y}, (A.obj γ).rel x y →
    relates γ δ (start γ x) (start δ y)
  out_eq : ∀ {γ δ}, Γ.eqv γ δ → ∀ {s t}, relates γ δ s t →
    ∀ b, (machine γ).out s b = (machine δ).out t b
  next_rel : ∀ {γ δ}, Γ.eqv γ δ → ∀ {s t}, relates γ δ s t →
    ∀ b, relates γ δ ((machine γ).next s b) ((machine δ).next t b)

namespace ObserverFamily
variable {Γ Δ : Context} {A : P01D.Ty Γ}

def simulation (O : ObserverFamily A) {γ δ} (h : Γ.eqv γ δ) :
    Simulation (O.machine γ) (O.machine δ) where
  relates := O.relates γ δ
  out_eq := O.out_eq h
  next_rel := O.next_rel h

/-- The observed state is initialised from the *literal evaluated tracker*. -/
noncomputable def observe (O : ObserverFamily A) (t : Tm Γ A) (γ : Γ.Val) :
    Measure Cantor := law (O.machine γ) (O.start γ (eval t.code (Γ.environment γ)))

theorem observe_literal_source (O : ObserverFamily A) (t : Tm Γ A) (γ : Γ.Val) :
    O.observe t γ = law (O.machine γ) (O.start γ (t.at γ)) := rfl

/-- Semantic term equality transports complete observed laws even when the
two observer-state carriers differ. -/
theorem eqTm_observation (O : ObserverFamily A) {t u : Tm Γ A} (h : EqTm t u)
    {γ δ} (hγ : Γ.eqv γ δ) : O.observe t γ = O.observe u δ :=
  simulation_law (O.simulation hγ) (O.initial hγ (h γ δ hγ))

/-- No raw-conversion assumption is smuggled into contextual coherence. -/
theorem valuation_observation (O : ObserverFamily A) (t : Tm Γ A)
    {γ δ} (hγ : Γ.eqv γ δ) : O.observe t γ = O.observe t δ :=
  eqTm_observation O (eqTm_refl t) hγ

def pull (O : ObserverFamily A) (σ : Sub Δ Γ) : ObserverFamily (A.pull σ) where
  State γ := O.State (σ.map γ)
  machine γ := O.machine (σ.map γ)
  start γ := O.start (σ.map γ)
  relates γ δ := O.relates (σ.map γ) (σ.map δ)
  initial h := O.initial (σ.respects h)
  out_eq h := O.out_eq (σ.respects h)
  next_rel h := O.next_rel (σ.respects h)

/-- The substitution square uses the predecessor's checked code evaluation
lemma and tracker field, not an externally supplied runtime equivalence. -/
theorem substitution_square (O : ObserverFamily A) (t : Tm Γ A)
    (σ : Sub Δ Γ) (γ : Δ.Val) :
    (O.pull σ).observe (t.subst σ) γ = O.observe t (σ.map γ) := by
  unfold observe
  change law (O.machine (σ.map γ))
    (O.start (σ.map γ) (eval (psub σ.code t.code) (Δ.environment γ))) = _
  rw [eval_sub, funext (σ.tracks γ)]

/-- Related substitutions need not have equal trackers or equal valuation
maps. They nonetheless give equal observed laws under local PER compatibility. -/
theorem related_substitution_observation (O : ObserverFamily A) (t : Tm Γ A)
    {σ τ : Sub Δ Γ} (h : SubRel σ τ) {γ δ} (hγ : Δ.eqv γ δ) :
    (O.pull σ).observe (t.subst σ) γ = (O.pull τ).observe (t.subst τ) δ := by
  rw [substitution_square, substitution_square]
  exact valuation_observation O t (h γ δ hγ)

/-- A finite abstract observer may be certified for one actual evaluated
source term; the concrete observer state remains an arbitrary dependent type. -/
theorem finite_solver_transport (O : ObserverFamily A) (t : Tm Γ A) (γ : Γ.Val)
    {Q : Type*} [Fintype Q] [DecidableEq Q] [Nonempty Q] (N : Mealy Q)
    (R : Simulation (O.machine γ) N) (q : Q)
    (initial : R.relates (O.start γ (t.at γ)) q) :
    (solveDefect N q : ℝ) = P02A2.defect (O.observe t γ) :=
  certified_defect_exact R initial

/-- Two finite certificates of related substituted observations yield exactly
the same rational defect. This does not imply equality of source terms. -/
theorem related_substitution_solvers (O : ObserverFamily A) (t : Tm Γ A)
    {σ τ : Sub Δ Γ} (h : SubRel σ τ) {γ δ} (hγ : Δ.eqv γ δ)
    {Q W : Type*} [Fintype Q] [DecidableEq Q] [Nonempty Q]
    [Fintype W] [DecidableEq W] [Nonempty W] (N : Mealy Q) (L : Mealy W)
    (R : Simulation ((O.pull σ).machine γ) N)
    (U : Simulation ((O.pull τ).machine δ) L) (q : Q) (w : W)
    (hr : R.relates ((O.pull σ).start γ ((t.subst σ).at γ)) q)
    (hu : U.relates ((O.pull τ).start δ ((t.subst τ).at δ)) w) :
    solveDefect N q = solveDefect L w := by
  have he : (solveDefect N q : ℝ) = (solveDefect L w : ℝ) := by
    rw [finite_solver_transport (O.pull σ) (t.subst σ) γ N R q hr,
    finite_solver_transport (O.pull τ) (t.subst τ) δ L U w hu,
      related_substitution_observation O t h hγ]
  exact_mod_cast he

/-- Representation into P01's checked contextual core retains the original
polynomial exactly before the observer is run. -/
theorem candidate_source_observation {p B} (h : P01DF.Has p B) (ρ : P01R.OEnv)
    (O : ObserverFamily (P01DF.candidateTy ρ B)) (η : Env) :
    O.observe (P01DF.candidateTm h ρ) η =
      law (O.machine η) (O.start η (eval p η)) := rfl

end ObserverFamily
end Orthemology.CertifiedObserver
