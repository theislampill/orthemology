import GroundedSupport
import AliasCuts
import Mathlib.Data.Fintype.Powerset
import Mathlib.Data.Fintype.Fin

namespace T20Grounded.Controls

inductive Root
  | source | truth | pastOrder | pastStanding | grantNow | scopeNow | occasion | implementation
  deriving DecidableEq

inductive Claim
  | ownsDuty0 | veracious | issuedAt0 | standingAt0 | liveStanding | scopeNow
  | applicableNow0 | ready | duty0 | mayIssueNext | actNow
  deriving DecidableEq

def baseClaim : Root → Claim
  | .source => .ownsDuty0
  | .truth => .veracious
  | .pastOrder => .issuedAt0
  | .pastStanding => .standingAt0
  | .grantNow => .liveStanding
  | .scopeNow => .scopeNow
  | .occasion => .applicableNow0
  | .implementation => .ready

def Base (root : Root) (claim : Claim) : Prop := claim = baseClaim root

inductive Rule : Finset Claim → Claim → Prop
  | testimony : Rule {.ownsDuty0, .veracious} .duty0
  | historicalDirective : Rule {.issuedAt0, .standingAt0} .duty0
  | prospective : Rule {.liveStanding, .scopeNow} .mayIssueNext
  | implementation : Rule {.duty0, .applicableNow0, .ready} .actNow

def allRoots : Finset Root :=
  {.source, .truth, .pastOrder, .pastStanding, .grantNow, .scopeNow, .occasion, .implementation}

/-- Prospective revocation only removes the current grant root. -/
def revokeProspective (A : Finset Root) : Finset Root := A.erase .grantNow

/-- Evidence invalidation is separately parameterized; it is not prospective revocation. -/
def invalidateEvidence (A badEvidence : Finset Root) : Finset Root :=
  A \ badEvidence.erase .grantNow

 theorem testimony_needs_no_second_jurisdiction :
    Derivable Base Rule {.source, .truth} .duty0 := by
  apply Derivable.step Rule.testimony
  intro claim hc
  simp only [Finset.mem_insert, Finset.mem_singleton] at hc
  rcases hc with rfl | rfl
  · exact Derivable.root (r := Root.source) (by decide) rfl
  · exact Derivable.root (r := Root.truth) (by decide) rfl

 theorem old_duty_survives_prospective_revocation :
    Derivable Base Rule (revokeProspective allRoots) .duty0 := by
  apply derivable_mono (A := {.source, .truth}) _ testimony_needs_no_second_jurisdiction
  decide

 theorem old_duty_can_remain_currently_applicable :
    Derivable Base Rule (revokeProspective allRoots) .actNow := by
  apply Derivable.step Rule.implementation
  intro claim hc
  simp only [Finset.mem_insert, Finset.mem_singleton] at hc
  rcases hc with rfl | rfl | rfl
  · exact old_duty_survives_prospective_revocation
  · exact Derivable.root (r := Root.occasion) (by decide) rfl
  · exact Derivable.root (r := Root.implementation) (by decide) rfl

 theorem prospective_power_is_lost :
    ¬ Derivable Base Rule (revokeProspective allRoots) .mayIssueNext := by
  let V : Claim → Prop := fun c => c ≠ .liveStanding ∧ c ≠ .mayIssueNext
  have roots : ∀ r ∈ revokeProspective allRoots, ∀ c, Base r c → V c := by
    intro r hr c hc
    subst c
    cases r <;> simp_all [Base, baseClaim, V, revokeProspective]
  have rules : ∀ P c, Rule P c → (∀ p ∈ P, V p) → V c := by
    intro P c hr hp
    cases hr with
    | testimony => decide
    | historicalDirective => decide
    | prospective => exact False.elim ((hp .liveStanding (by decide)).1 rfl)
    | implementation => decide
  intro h
  exact (derivable_sound V roots rules h).2 rfl

 theorem past_duty_does_not_supply_current_applicability :
    ¬ Derivable Base Rule (allRoots.erase .occasion) .actNow := by
  let V : Claim → Prop := fun c => c ≠ .applicableNow0 ∧ c ≠ .actNow
  have roots : ∀ r ∈ allRoots.erase .occasion, ∀ c, Base r c → V c := by
    intro r hr c hc
    subst c
    cases r <;> simp_all [Base, baseClaim, V]
  have rules : ∀ P c, Rule P c → (∀ p ∈ P, V p) → V c := by
    intro P c hr hp
    cases hr with
    | testimony => decide
    | historicalDirective => decide
    | prospective => decide
    | implementation => exact False.elim ((hp .applicableNow0 (by decide)).1 rfl)
  intro h
  exact (derivable_sound V roots rules h).2 rfl

 theorem duty_still_derives_when_current_applicability_is_absent :
    Derivable Base Rule (allRoots.erase .occasion) .duty0 := by
  apply derivable_mono (A := {.source, .truth}) _ testimony_needs_no_second_jurisdiction
  decide


 theorem prospective_revocation_preserves_non_grant_roots (A : Finset Root)
    (r : Root) (hr : r ≠ .grantNow) : r ∈ revokeProspective A ↔ r ∈ A := by
  simp [revokeProspective, hr]

 theorem evidence_invalidation_preserves_current_grant (A bad : Finset Root)
    (h : Root.grantNow ∈ A) : Root.grantNow ∈ invalidateEvidence A bad := by
  simp [invalidateEvidence, h]

 theorem no_owned_truth_from_authorship_alone :
    ¬ Derivable Base Rule {.source} .duty0 := by
  let V : Claim → Prop := fun c => c = .ownsDuty0
  have roots : ∀ r ∈ ({.source} : Finset Root), ∀ c, Base r c → V c := by
    intro r hr c hc
    have heq : r = .source := Finset.mem_singleton.mp hr
    subst r
    simpa [Base, baseClaim, V] using hc
  have rules : ∀ P c, Rule P c → (∀ p ∈ P, V p) → V c := by
    intro P c hr hp
    cases hr with
    | testimony => exact False.elim (Claim.noConfusion (hp .veracious (by decide)))
    | historicalDirective => exact False.elim (Claim.noConfusion (hp .issuedAt0 (by decide)))
    | prospective => exact False.elim (Claim.noConfusion (hp .liveStanding (by decide)))
    | implementation => exact False.elim (Claim.noConfusion (hp .ready (by decide)))
  intro h
  exact Claim.noConfusion (derivable_sound V roots rules h)

inductive CycleRule : Finset Bool → Bool → Prop
  | forward : CycleRule {false} true
  | backward : CycleRule {true} false

 theorem unanchored_cycle_has_no_derivation (claim : Bool) :
    ¬ Derivable (fun (_ : Unit) (_ : Bool) => False) CycleRule ∅ claim := by
  intro h
  apply derivable_sound (fun _ => False) _ _ h
  · intro r hr
    exact False.elim (Finset.not_mem_empty r hr)
  · intro P c hr hp
    cases hr with
    | forward => exact hp false (by decide)
    | backward => exact hp true (by decide)

 theorem anchor_grounds_cycle :
    Derivable (fun (_ : Unit) (c : Bool) => c = false) CycleRule {()} true := by
  apply Derivable.step CycleRule.forward
  intro p hp
  have : p = false := Finset.mem_singleton.mp hp
  subst p
  exact Derivable.root (r := ()) (by decide) rfl

end T20Grounded.Controls
