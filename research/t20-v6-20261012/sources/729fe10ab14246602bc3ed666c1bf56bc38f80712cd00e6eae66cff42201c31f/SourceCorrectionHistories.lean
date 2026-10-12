import SourceObservableMinimum

namespace FiniteSidecar
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Literal source polynomials after each correction; no decoder is inserted between steps. -/
def runSource : List Tables → Poly → List Poly × Poly
  | [], p => ([], p)
  | action :: actions, p =>
      let reply := Poly.app (controller action) p
      let rest := runSource actions (sndPoly reply)
      (fstPoly reply :: rest.1, rest.2)

def runCodes : List Tables → Nat → Nat → List Nat × (Nat × Nat)
  | [], z, k => ([], (z,k))
  | action :: actions, z, k =>
      let rest := runCodes actions (tableValue action.nextCoarse 0 z k)
        (tableValue action.nextTag 0 z k)
      (tableValue action.branch 0 z k :: rest.1, rest.2)

theorem runSource_typed (actions : List Tables) {p : Poly} (hp : Has [] p State) :
    (∀ b ∈ (runSource actions p).1, Has [] b N) ∧
    Has [] (runSource actions p).2 State := by
  induction actions generalizing p with
  | nil => exact ⟨by simp [runSource], hp⟩
  | cons action actions ih =>
    have hr := app_has (form_arr (state_form .nil) (reply_form .nil))
      (reply_form .nil) (controller_has action) hp
    have hb := Has.sigmaFst (N_form .nil) (reply_form .nil) hr
    have hs : Has [] (sndPoly (.app (controller action) p)) State :=
      .sigmaSnd (reply_form .nil) (state_form .nil) hr
    have ihs := ih hs
    refine ⟨?_, ihs.2⟩
    intro b h
    simp only [runSource, List.mem_cons] at h
    rcases h with rfl | h
    · exact hb
    · exact ihs.1 b h

/-- Every finite branch history and final retained state is preserved together. -/
theorem runSource_observes (actions : List Tables) {p : Poly} {z k : Nat}
    (hp : Represents (eval p zeroEnv) z k) :
    List.Forall₂ (fun b n => NatObs (eval b zeroEnv) n)
      (runSource actions p).1 (runCodes actions z k).1 ∧
    Represents (eval (runSource actions p).2 zeroEnv)
      (runCodes actions z k).2.1 (runCodes actions z k).2.2 := by
  induction actions generalizing p z k with
  | nil => exact ⟨.nil, hp⟩
  | cons action actions ih =>
    have h := controller_observes action hp
    have hs : Represents (eval (sndPoly (.app (controller action) p)) zeroEnv)
        (tableValue action.nextCoarse 0 z k) (tableValue action.nextTag 0 z k) := h.2
    have hi := ih hs
    exact ⟨.cons h.1 hi.1, hi.2⟩

/-- Each returned branch is also identified with its exact numeral in actual HasJ. -/
theorem runSource_branch_identities (actions : List Tables) {p : Poly} {z k : Nat}
    (typed : Has [] p State) (hp : Represents (eval p zeroEnv) z k) :
    List.Forall₂ (fun b n => JointCompletion.HasJ [] (.atom .i)
      (.identity N b (inputNumeral n)))
      (runSource actions p).1 (runCodes actions z k).1 := by
  have ht := (runSource_typed actions typed).1
  have ho := (runSource_observes actions hp).1
  generalize hbs : (runSource actions p).1 = bs at ht ho ⊢
  generalize hns : (runCodes actions z k).1 = ns at ho ⊢
  clear hbs hns
  induction ho with
  | nil => exact .nil
  | @cons b n bs ns hbn htail ih =>
    exact .cons (identity_at_observed (oldJ (ht b (by simp))) hbn)
      (ih (fun b hb => ht b (by simp [hb])))

/-- Finite code bounds are an application premise, not enforced by the N carrier. -/
def ClosedRectangle (Z M : Nat) (action : Tables) : Prop :=
  ∀ z k, z < Z → k < M →
    tableValue action.nextCoarse 0 z k < Z ∧ tableValue action.nextTag 0 z k < M

theorem runCodes_bounded {Z M z k : Nat} (actions : List Tables)
    (closed : ∀ action ∈ actions, ClosedRectangle Z M action)
    (hz : z < Z) (hk : k < M) :
    (runCodes actions z k).2.1 < Z ∧ (runCodes actions z k).2.2 < M := by
  induction actions generalizing z k with
  | nil => exact ⟨hz,hk⟩
  | cons action actions ih =>
    have step := closed action (by simp) z k hz hk
    exact ih (fun a ha => closed a (by simp [ha])) step.1 step.2

#print axioms runSource_typed
#print axioms runSource_observes
#print axioms runSource_branch_identities
end FiniteSidecar
