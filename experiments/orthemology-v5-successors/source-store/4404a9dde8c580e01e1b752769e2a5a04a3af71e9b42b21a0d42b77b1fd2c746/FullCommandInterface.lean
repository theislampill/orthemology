import OpaqueActions
import SourceCorrespondence
import CanonicalReplies

namespace CoveringKernel.Actions
open Finset
variable {α : Type*} [Fintype α] [DecidableEq α]

/-- The fixed repair body is bound together with its selected path and unique
attempt nonce. Authentication/authorization remain retained model premises. -/
structure FullCommand (F : Finset (Finset α)) (Body : Type*) where
  path : CoveringKernel.Path F
  nonce : ℕ
  body : Body

def commandSupport {F : Finset (Finset α)} {Body : Type*}
    (cmd : FullCommand F Body) : Finset α := cmd.path.val

omit [Fintype α] [DecidableEq α] in
theorem history_length {Action Obs : Type*} (π : Policy Action Obs)
    (reply : List (Action × Obs) → Action → Obs) (n : ℕ) :
    (history π reply n).length = n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [history, ih]

noncomputable def fullCommandPolicy (F : Finset (Finset α)) (hne : F.Nonempty)
    {Body Obs : Type*} (body : Body) : Policy (FullCommand F Body) Obs := fun h =>
  ⟨if hi : h.length < F.card then F.equivFin.symm ⟨h.length, hi⟩
    else ⟨hne.choose, hne.choose_spec⟩, h.length, body⟩

omit [Fintype α] [DecidableEq α] in
theorem fullCommand_fresh_nonce (F : Finset (Finset α)) (hne : F.Nonempty)
    {Body Obs : Type*} (body : Body)
    (reply : List (FullCommand F Body × Obs) → FullCommand F Body → Obs) (n : ℕ) :
    (fullCommandPolicy F hne body (history (fullCommandPolicy F hne body) reply n)).nonce = n := by
  simp [fullCommandPolicy, history_length]

omit [Fintype α] [DecidableEq α] in
theorem fullCommand_support_at (F : Finset (Finset α)) (hne : F.Nonempty)
    {Body Obs : Type*} (body : Body)
    (reply : List (FullCommand F Body × Obs) → FullCommand F Body → Obs) (i : Fin F.card) :
    commandSupport (fullCommandPolicy F hne body
      (history (fullCommandPolicy F hne body) reply i.val)) =
      (F.equivFin.symm i).val := by
  simp [commandSupport, fullCommandPolicy, history_length, i.isLt]

omit [Fintype α] [DecidableEq α] in
theorem fullCommand_hit (F : Finset (Finset α)) (hne : F.Nonempty)
    {Body Obs : Type*} (body : Body)
    (observe : Finset α → List (FullCommand F Body × Obs) → FullCommand F Body → Obs)
    (T : Finset α) (hhit : ∃ P ∈ F, Disjoint P T) :
    SuccessWithin commandSupport (fullCommandPolicy F hne body) observe T F.card := by
  obtain ⟨P, hP, hd⟩ := hhit
  let i : Fin F.card := F.equivFin ⟨P,hP⟩
  refine ⟨i.val, i.isLt, ?_⟩
  rw [fullCommand_support_at F hne body (observe T) i]
  simpa [i] using hd

/-- The upper-bound enumeration issues genuinely fresh full commands, preserves
one repair body, and works for all actual faults of size at most B. -/
theorem fullCommand_root_world_cap_attained (B c q : ℕ) (hB : 1 ≤ B) (hc : 1 ≤ c)
    (hcm : c ≤ Fintype.card α) (hq : q ≤ Fintype.card α)
    (hk : B+c-1 ≤ Fintype.card α-q) {Body Obs : Type*} (body : Body) :
    ∃ F : Finset (Finset α), CoveringKernel.Uniform q F ∧
      ∃ π : Policy (FullCommand F Body) Obs,
      (∀ reply n, (π (history π reply n)).nonce = n) ∧
      (∀ h, (π h).body = body) ∧
      ∀ observe : Finset α → List (FullCommand F Body × Obs) → FullCommand F Body → Obs,
      ∀ A : Finset α, A.card = c →
      ∀ S : Finset (Option α), S ⊆ AttributionKernel.actualRoots A → S.card ≤ B →
        SuccessWithin commandSupport π observe (AttributionKernel.taintedLabels A S)
          (coveringNumber α (Fintype.card α-q) (B+c-1)) := by
  obtain ⟨F, hu, ha, hsize⟩ := minimal_portfolio_attained q (B+c-1) hq hk
  have hne := available_nonempty (B+c-1) F (by omega) ha
  have hsource := (available_source_iff B c hB hc hcm (by omega) F).mpr ha
  refine ⟨F, hu, fullCommandPolicy F hne body, fullCommand_fresh_nonce F hne body,
    (fun _ => rfl), ?_⟩
  intro observe A hA S hSr hS
  obtain ⟨P, hP, hd⟩ := hsource A hA S hSr hS
  rw [← hsize]
  exact fullCommand_hit F hne body observe (AttributionKernel.taintedLabels A S)
    ⟨P, hP, (AttributionKernel.disjoint_image_iff A P S).mp hd⟩

/-- Symbolic canonical observation constructor. Every control-transcript field
can depend on the submitted complete command and complete history. -/
def canonicalObserve {Action Payload : Type*} (support : Action → Finset α)
    (control : List (Action × MacroReply Payload) → Action → Payload) (receipt : Bool)
    (T : Finset α) (h : List (Action × MacroReply Payload)) (a : Action) : MacroReply Payload :=
  ⟨control h a, if receipt then some (decide (Disjoint (support a) T)) else none⟩

def canonicalFailed {Action Payload : Type*}
    (control : List (Action × MacroReply Payload) → Action → Payload) (receipt : Bool)
    (h : List (Action × MacroReply Payload)) (a : Action) : MacroReply Payload :=
  ⟨control h a, if receipt then some false else none⟩

omit [Fintype α] in
theorem canonical_opaque {Action Payload : Type*} (support : Action → Finset α)
    (control : List (Action × MacroReply Payload) → Action → Payload) (receipt : Bool)
    (π : Policy Action (MacroReply Payload)) (k : ℕ) :
    Opaque support π (canonicalObserve support control receipt) (canonicalFailed control receipt) k := by
  intro T _ n hbad
  have hb := hbad n le_rfl
  simp [canonicalObserve, canonicalFailed, hb]

#print axioms fullCommand_fresh_nonce
#print axioms fullCommand_root_world_cap_attained
#print axioms canonical_opaque
end CoveringKernel.Actions
