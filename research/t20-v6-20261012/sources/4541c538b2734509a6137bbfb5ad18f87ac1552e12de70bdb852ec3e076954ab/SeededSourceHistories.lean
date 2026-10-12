import SeededSourceLookup
namespace SeededSource
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC FiniteSidecar
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

def tabulateCube (Z M D : Nat) (f : Nat → Nat → Nat → Nat) : List (List (List Nat)) :=
  (List.range D).map (fun u => tabulate Z M (fun z k => f z k u))
theorem tabulateCube_value {Z M D z k u : Nat} (f : Nat → Nat → Nat → Nat)
    (hz : z < Z) (hk : k < M) (hu : u < D) :
    cubeValue (tabulateCube Z M D f) z k u = f z k u := by
  simp [cubeValue, tabulateCube, hu, tabulate_value _ hz hk]

def finiteCubes (Z M D : Nat) (b z' k' : Nat → Nat → Nat → Nat) : Cubes :=
  ⟨tabulateCube Z M D b, tabulateCube Z M D z', tabulateCube Z M D k'⟩
theorem finite_sampler_observes {Z M D z k u : Nat}
    (b z' k' : Nat → Nat → Nat → Nat) (hz : z < Z) (hk : k < M) (hu : u < D)
    {p : Term} (hp : RepresentsInput p z k u) :
    NatObs (firstTerm (.app (eval (sampler (finiteCubes Z M D b z' k')) zeroEnv) p)) (b z k u) ∧
    Represents (secondTerm (.app (eval (sampler (finiteCubes Z M D b z' k')) zeroEnv) p))
      (z' z k u) (k' z k u) := by
  simpa only [finiteCubes, tabulateCube_value _ hz hk hu] using
    sampler_observes (finiteCubes Z M D b z' k') hp

/-- Host supplies each explicit seed term. State is passed literally, never decoded/re-encoded. -/
def runSource : List (Cubes × Poly) → Poly → List Poly × Poly
  | [], p => ([],p)
  | (c,u) :: rest, p =>
      let reply := Poly.app (sampler c) (seeded u p)
      let tail := runSource rest (sndPoly reply)
      (reply :: tail.1, tail.2)
def runCodes : List (Cubes × Nat) → Nat → Nat → List (Nat × Nat × Nat) × (Nat × Nat)
  | [], z,k => ([],(z,k))
  | (c,u) :: rest, z,k =>
      let b := cubeValue c.branch z k u
      let z' := cubeValue c.nextCoarse z k u
      let k' := cubeValue c.nextTag z k u
      let tail := runCodes rest z' k'
      ((b,z',k') :: tail.1,tail.2)

def ReplyRepresents (p : Term) (triple : Nat × Nat × Nat) : Prop :=
  NatObs (firstTerm p) triple.1 ∧ Represents (secondTerm p) triple.2.1 triple.2.2

theorem runSource_typed (actions : List (Cubes × Poly)) {p : Poly}
    (hseeds : ∀ c u, (c,u) ∈ actions → Has [] u N) (hp : Has [] p State) :
    (∀ r ∈ (runSource actions p).1, Has [] r Reply) ∧
      Has [] (runSource actions p).2 State := by
  induction actions generalizing p with
  | nil => exact ⟨by simp [runSource], hp⟩
  | cons cu rest ih =>
    rcases cu with ⟨c,u⟩
    have hr := app_has (form_arr (input_form .nil) (reply_form .nil))
      (reply_form .nil) (sampler_has c) (seeded_has (hseeds c u (by simp)) hp)
    have hs : Has [] (sndPoly (.app (sampler c) (seeded u p))) State :=
      .sigmaSnd (reply_form .nil) (state_form .nil) hr
    have ht := ih (fun c u h => hseeds c u (by simp [h])) hs
    exact ⟨by intro r h; simp only [runSource,List.mem_cons] at h
              rcases h with rfl | h
              · exact hr
              · exact ht.1 r h, ht.2⟩

/-- Exact joint reply histories for each seed realization; this theorem assigns no seed law. -/
theorem runSource_observes (actions : List (Cubes × Nat)) {p : Poly} {z k : Nat}
    (hp : Represents (eval p zeroEnv) z k) :
    List.Forall₂ (fun r t => ReplyRepresents (eval r zeroEnv) t)
      (runSource (actions.map (fun cu => (cu.1,inputNumeral cu.2))) p).1
      (runCodes actions z k).1 ∧
    Represents (eval (runSource (actions.map (fun cu => (cu.1,inputNumeral cu.2))) p).2 zeroEnv)
      (runCodes actions z k).2.1 (runCodes actions z k).2.2 := by
  induction actions generalizing p z k with
  | nil => exact ⟨.nil,hp⟩
  | cons cu rest ih =>
    rcases cu with ⟨c,u⟩
    have hu : NatObs (eval (inputNumeral u) zeroEnv) u := canonical_obs u
    have h := sampler_observes c (seeded_represents hu hp)
    have hs : Represents (eval (sndPoly (.app (sampler c) (seeded (inputNumeral u) p))) zeroEnv)
      (cubeValue c.nextCoarse z k u) (cubeValue c.nextTag z k u) := h.2
    have hi := ih hs
    exact ⟨.cons h hi.1, hi.2⟩

/-- Bounds and branch range are external code-validity hypotheses. -/
def Closed (Z M O D : Nat) (c : Cubes) : Prop :=
  ∀ z k u, z < Z → k < M → u < D →
    cubeValue c.branch z k u < O ∧ cubeValue c.nextCoarse z k u < Z ∧
      cubeValue c.nextTag z k u < M

#print axioms finite_sampler_observes
#print axioms runSource_typed
#print axioms runSource_observes
end SeededSource
