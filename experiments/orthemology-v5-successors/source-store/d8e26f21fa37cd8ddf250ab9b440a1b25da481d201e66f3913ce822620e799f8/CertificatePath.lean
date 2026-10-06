import EndComponents
import Mathlib.Data.Fintype.Card

/-!
# Explicit bounded action-witnessed paths

The executable predicate checks stored steps locally, reconstructing each source
from the previous receipt. Its proof-only completeness construction extracts an
actual walk from inherited reachability and removes repeated-state loops. The
bound is a certificate-syntax bound, not a stochastic execution-time bound.
-/
namespace OrthemicCertificate

/-- A submitted start and an explicit list of action/next-state steps. -/
structure Path (State Action : Type*) where
  start : State
  steps : List (Action × State)
  deriving DecidableEq, Repr

namespace Path

variable {State Action : Type*}

/-- Read the endpoint by following the stored receipts. -/
def endpointFrom (s : State) : List (Action × State) → State
  | [] => s
  | (_, t) :: rest => endpointFrom t rest

/-- The endpoint of the submitted syntax. -/
def endpoint (p : Path State Action) : State := endpointFrom p.start p.steps

/-- All visited states, including the start. Used in the completeness proof. -/
def visited (s : State) (steps : List (Action × State)) : List State :=
  s :: steps.map Prod.snd

/-- Local step validation. Each source is reconstructed, never independently
supplied by the certificate. This predicate does not invoke reachability. -/
def Edges (allowed : Finset (State × Action))
    (succ : (State × Action) → Finset State) (s : State) : List (Action × State) → Prop
  | [] => True
  | (a, t) :: rest => (s, a) ∈ allowed ∧ t ∈ succ (s, a) ∧ Edges allowed succ t rest

/-- Explicit executable structural recursion for local edge checks. -/
def edgesDecidable [DecidableEq State] [DecidableEq Action] (allowed : Finset (State × Action))
    (succ : (State × Action) → Finset State) (s : State) :
    (steps : List (Action × State)) → Decidable (Edges allowed succ s steps)
  | [] => isTrue trivial
  | (a, t) :: rest =>
    letI := edgesDecidable allowed succ t rest
    inferInstanceAs (Decidable ((s, a) ∈ allowed ∧ t ∈ succ (s, a) ∧ Edges allowed succ t rest))

instance instDecidableEdges [DecidableEq State] [DecidableEq Action] (allowed : Finset (State × Action))
    (succ : (State × Action) → Finset State) (s : State) (steps : List (Action × State)) :
    Decidable (Edges allowed succ s steps) := edgesDecidable allowed succ s steps

/-- Decidable bounded path checking against fixed supplied finite tables. -/
def Valid [Fintype State] (allowed : Finset (State × Action))
    (succ : (State × Action) → Finset State) (s t : State) (p : Path State Action) : Prop :=
  p.start = s ∧ p.endpoint = t ∧ Edges allowed succ p.start p.steps ∧
    p.steps.length ≤ Fintype.card State - 1

instance instDecidableValid [DecidableEq State] [DecidableEq Action] [Fintype State] (allowed : Finset (State × Action))
    (succ : (State × Action) → Finset State) (s t : State) (p : Path State Action) :
    Decidable (Valid allowed succ s t p) := by
  unfold Valid
  infer_instance

/-- Each checked action/receipt is an actual inherited edge. -/
theorem edges_sound {allowed : Finset (State × Action)}
    {succ : (State × Action) → Finset State} {s : State} {steps : List (Action × State)}
    (h : Edges allowed succ s steps) :
    HiddenParity.Reach Prod.fst succ allowed s (endpointFrom s steps) := by
  induction steps generalizing s with
  | nil => exact Relation.ReflTransGen.refl
  | cons step rest ih =>
    rcases step with ⟨a, t⟩
    exact Relation.ReflTransGen.head ⟨(s, a), h.1, rfl, h.2.1⟩ (ih h.2.2)

/-- Accepted path syntax denotes the exact inherited reflexive reachability. -/
theorem valid_sound [Fintype State] {allowed : Finset (State × Action)}
    {succ : (State × Action) → Finset State} {s t : State} {p : Path State Action}
    (h : Valid allowed succ s t p) : HiddenParity.Reach Prod.fst succ allowed s t := by
  rcases h with ⟨hs, ht, he, _⟩
  rw [← hs, ← ht]
  exact edges_sound he

theorem edges_mono {allowed enlarged : Finset (State × Action)}
    {succ : (State × Action) → Finset State} (hsub : allowed ⊆ enlarged)
    {s : State} {steps : List (Action × State)}
    (h : Edges allowed succ s steps) : Edges enlarged succ s steps := by
  induction steps generalizing s with
  | nil => trivial
  | cons step rest ih => exact ⟨hsub h.1, h.2.1, ih h.2.2⟩

/-- Old submitted paths remain valid when only the allowed pair set grows. -/
theorem valid_mono [Fintype State] {allowed enlarged : Finset (State × Action)}
    {succ : (State × Action) → Finset State} (hsub : allowed ⊆ enlarged)
    {s t : State} {p : Path State Action}
    (h : Valid allowed succ s t p) : Valid enlarged succ s t p :=
  ⟨h.1, h.2.1, edges_mono hsub h.2.2.1, h.2.2.2⟩

@[simp] theorem endpointFrom_append (s : State) (xs ys : List (Action × State)) :
    endpointFrom s (xs ++ ys) = endpointFrom (endpointFrom s xs) ys := by
  induction xs generalizing s with
  | nil => rfl
  | cons step rest ih => exact ih step.2

theorem edges_append {allowed : Finset (State × Action)}
    {succ : (State × Action) → Finset State} {s : State} {xs ys : List (Action × State)}
    (hx : Edges allowed succ s xs) (hy : Edges allowed succ (endpointFrom s xs) ys) :
    Edges allowed succ s (xs ++ ys) := by
  induction xs generalizing s with
  | nil => exact hy
  | cons step rest ih => exact ⟨hx.1, hx.2.1, ih hx.2.2 hy⟩

/-- Truncate a simple action-witnessed walk at any already visited state. All
retained edges and their action witnesses are literal prefix data. -/
theorem prefix_to_visited [DecidableEq State] {allowed : Finset (State × Action)}
    {succ : (State × Action) → Finset State} {s t : State} {steps : List (Action × State)}
    (he : Edges allowed succ s steps) (hn : (visited s steps).Nodup)
    (ht : t ∈ visited s steps) :
    ∃ pre : List (Action × State), Edges allowed succ s pre ∧
      endpointFrom s pre = t ∧ (visited s pre).Nodup ∧
      visited s pre ⊆ visited s steps := by
  induction steps generalizing s with
  | nil =>
    have hts : t = s := by simpa [visited] using ht
    subst t
    exact ⟨[], trivial, rfl, by simp [visited], fun _ hx => hx⟩
  | cons step rest ih =>
    rcases step with ⟨a, u⟩
    by_cases hts : t = s
    · subst t
      exact ⟨[], trivial, rfl, by simp [visited], by simp [visited]⟩
    · have hn' : (visited u rest).Nodup := (List.nodup_cons.mp hn).2
      have hsnot : s ∉ visited u rest := (List.nodup_cons.mp hn).1
      have ht' : t ∈ visited u rest := by
        rcases List.mem_cons.mp ht with h | h
        · exact False.elim (hts h)
        · exact h
      obtain ⟨pre, hp, hend, hpno, hpsub⟩ := ih he.2.2 hn' ht'
      refine ⟨(a, u) :: pre, ⟨he.1, he.2.1, hp⟩, hend, ?_, ?_⟩
      · exact List.nodup_cons.mpr ⟨fun h => hsnot (hpsub h), hpno⟩
      · intro x hx
        rcases List.mem_cons.mp hx with h | h
        · exact List.mem_cons.mpr (Or.inl h)
        · exact List.mem_cons.mpr (Or.inr (hpsub h))

/-- Extract action witnesses from each inherited edge and erase loops during
extension: when the next endpoint has occurred before, keep the prefix ending
there; otherwise append the witnessed edge. The result has no repeated state. -/
theorem exists_simple [DecidableEq State] {allowed : Finset (State × Action)}
    {succ : (State × Action) → Finset State} {s t : State}
    (h : HiddenParity.Reach Prod.fst succ allowed s t) :
    ∃ steps : List (Action × State), Edges allowed succ s steps ∧
      endpointFrom s steps = t ∧ (visited s steps).Nodup := by
  induction h with
  | refl => exact ⟨[], trivial, rfl, by simp [visited]⟩
  | @tail u v _ he ih =>
    obtain ⟨steps, hs, hu, hn⟩ := ih
    by_cases hv : v ∈ visited s steps
    · obtain ⟨pre, hp, hvend, hpno, _⟩ := prefix_to_visited hs hn hv
      exact ⟨pre, hp, hvend, hpno⟩
    · obtain ⟨⟨source, a⟩, ha, hsource, hnext⟩ := he
      change source = u at hsource
      subst source
      refine ⟨steps ++ [(a, v)], ?_, ?_, ?_⟩
      · apply edges_append hs
        simpa only [hu, Edges] using And.intro ha (And.intro hnext True.intro)
      · simp [hu, endpointFrom]
      · have hn' : (v :: visited s steps).Nodup := List.nodup_cons.mpr ⟨hv, hn⟩
        have happ : (visited s steps ++ [v]).Nodup := by
          simpa only [List.singleton_append] using List.nodup_append_comm.mpr hn'
        simpa only [visited, List.map_append, List.map_cons, List.map_nil,
          List.cons_append] using happ

/-- Reachability supplies bounded certificate syntax independently of any
reachable-set solver. Empty paths cover equal endpoints, including card = 1. -/
theorem exists_valid [DecidableEq State] [Fintype State] {allowed : Finset (State × Action)}
    {succ : (State × Action) → Finset State} {s t : State}
    (h : HiddenParity.Reach Prod.fst succ allowed s t) :
    ∃ p : Path State Action, Valid allowed succ s t p := by
  obtain ⟨steps, he, hend, hn⟩ := exists_simple h
  have hcard := hn.length_le_card
  have hlength : steps.length + 1 ≤ Fintype.card State := by
    simpa [visited] using hcard
  refine ⟨⟨s, steps⟩, rfl, hend, he, ?_⟩
  change steps.length ≤ Fintype.card State - 1
  omega

end Path
end OrthemicCertificate
