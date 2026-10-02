import ContextualObserver
import ObserverFixtures

namespace Orthemology.CertifiedObserver.ContextFixtures
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open Orthemology.Frontier.MealyMeasure.Fixtures
open OrthemologyV2 OrthemologyV3 P01D P01DF
open ObserverFamily
open Set MeasureTheory

/-- Syntactic size is intentionally not raw-conversion invariant. It controls
only the runtime representation's auxiliary carrier, never observable output. -/
def nodes : Term → ℕ
  | .app f x => nodes f + nodes x + 1
  | _ => 1

/-- A semantic, explicitly noncomputable classifier. This fixture does not
pretend to be a parser or a total executable conversion decision procedure. -/
noncomputable def isI (t : Term) : Bool := by classical exact decide (Conv t .i)

theorem isI_transport {t u : Term} (h : Conv t u) : isI t = isI u := by
  classical
  apply Bool.eq_iff_iff.mpr
  simp only [isI, decide_eq_true_eq]
  exact ⟨fun ht => h.symm.trans ht, fun hu => h.trans hu⟩

abbrev State (η : Env) := Bool × Fin (nodes (η 0) + 1)

def machine (η : Env) : Mealy (State η) where
  next z _ := (z.1, ⟨(z.2.val+1) % (nodes (η 0)+1), Nat.mod_lt _ (by omega)⟩)
  out z b := if z.1 then false else b

noncomputable def observer : ObserverFamily candidateRaw where
  State := State
  machine := machine
  start _ t := (isI t, 0)
  relates _ _ s t := s.1 = t.1
  initial := by intro η ξ h t u htu; exact isI_transport htu
  out_eq := by intro η ξ h s t he b; simp only [machine, he]
  next_rel := by intro η ξ h s t he b; exact he

instance observerStateFintype (η : Env) : Fintype (observer.State η) := by
  change Fintype (State η)
  infer_instance

def iEnv : Env := fun _ => .i
def iiEnv : Env := fun _ => .app .i .i
def skkEnv : Env := fun _ => skk

def iSub : Sub nilContext indexContext where
  map _ := iEnv
  respects := fun _ _ => .refl _
  code _ := .atom .i
  tracks := fun _ _ => rfl

def iiSub : Sub nilContext indexContext where
  map _ := iiEnv
  respects := fun _ _ => .refl _
  code _ := .atom (.app .i .i)
  tracks := fun _ _ => rfl

theorem substitutions_related : SubRel iSub iiSub :=
  fun _ _ _ _ => (Conv.step (.i .i)).symm

def source : Tm indexContext candidateRaw := rawIndexTm (.var 0)

/-- Both tracked substitutions actually compile to different literal code. -/
theorem substitution_codes_distinct :
    (source.subst iSub).code ≠ (source.subst iiSub).code := by decide

/-- The source-derived runtime representation has four versus eight states. -/
theorem genuinely_different_state_carriers :
    Fintype.card (observer.State (iSub.map ())) = 4 ∧
    Fintype.card (observer.State (iiSub.map ())) = 8 := by
  norm_num [observer, State, iSub, iiSub, iEnv, iiEnv, nodes]

/-- The new law-transport theorem applies although both source trackers and
runtime-state cardinalities differ. -/
theorem concrete_substitution_laws :
    (observer.pull iSub).observe (source.subst iSub) () =
      (observer.pull iiSub).observe (source.subst iiSub) () :=
  observer.related_substitution_observation source substitutions_related True.intro

def zeroSimulation (η : Env) : Simulation (machine η) zeroMachine where
  relates s _ := s.1 = true
  out_eq := by intro s t h b; simp [machine, zeroMachine, h]
  next_rel := by intro s t h b; exact h

def copySimulation (η : Env) : Simulation (machine η) copyMachine where
  relates s _ := s.1 = false
  out_eq := by intro s t h b; simp [machine, copyMachine, h]
  next_rel := by intro s t h b; exact h

theorem source_I_zero : observer.observe source iEnv = law zeroMachine () := by
  apply simulation_law (zeroSimulation iEnv)
  change isI .i = true
  simp [isI, Conv.refl]

theorem source_II_zero : observer.observe source iiEnv = law zeroMachine () := by
  apply simulation_law (zeroSimulation iiEnv)
  change isI (.app .i .i) = true
  have h : Conv (.app .i .i) .i := .step (.i .i)
  simp [isI, h]

theorem source_SKK_copy : observer.observe source skkEnv = law copyMachine () := by
  apply simulation_law (copySimulation skkEnv)
  change isI skk = false
  have h : ¬ Conv skk .i := fun h => P01Source.I_SKK_not_convertible h.symm
  simp [isI, h]

/-- This family is source-sensitive: unrelated raw indices really can alter
the complete-law defect. Agreement is not built into the observer definition. -/
theorem source_sensitive_defects :
    P02A2.defect (observer.observe source iEnv) = 0 ∧
    P02A2.defect (observer.observe source skkEnv) = 1 := by
  rw [source_I_zero, source_SKK_copy]
  exact ⟨Fixtures.zero_defect, by rw [P02A2.defect, copy_atomic_mass_zero]; norm_num⟩

/-- Removing semantic compatibility makes a syntactic observer distinguish
raw-convertible terms immediately. -/
def inspectSyntax : Mealy Term where
  next z _ := z
  out z _ := decide (z = .i)

theorem raw_related_but_unlicensed_observer_distinguishes :
    Conv .i (.app .i .i) ∧
    output inspectSyntax .i ≠ output inspectSyntax (.app .i .i) := by
  refine ⟨(Conv.step (.i .i)).symm, ?_⟩
  intro h
  have he := congrFun (congrFun h (fun _ => false)) 0
  cases he

/-- A silent observer can collapse genuinely distinct source terms. A
certificate of observation equality supplies no converse source identity. -/
def silent : Mealy Term where
  next z _ := z
  out _ _ := false

def silentSimulation : Simulation silent zeroMachine where
  relates _ _ := True
  out_eq := fun _ _ => rfl
  next_rel := fun _ _ => True.intro

theorem law_equality_not_raw_identity :
    law silent .i = law silent skk ∧ ¬ Conv .i skk := by
  constructor
  · rw [simulation_law silentSimulation (s := .i) (t := ()) True.intro,
      simulation_law silentSimulation (s := skk) (t := ()) True.intro]
  · exact P01Source.I_SKK_not_convertible

end Orthemology.CertifiedObserver.ContextFixtures
