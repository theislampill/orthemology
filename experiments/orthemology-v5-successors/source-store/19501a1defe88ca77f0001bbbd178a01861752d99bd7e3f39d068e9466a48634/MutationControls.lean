import OccurrenceControls

namespace T20Grounded.Controls

/-- A deliberately bad extension that drops source veracity. -/
def AuthorshipOnly (P : Finset Claim) (c : Claim) : Prop :=
  Rule P c ∨ (P = {.ownsDuty0} ∧ c = .duty0)

 theorem authorship_only_mutation_creates_unsupported_duty :
    Derivable Base AuthorshipOnly {.source} .duty0 := by
  apply Derivable.step (premises := {.ownsDuty0}) (Or.inr ⟨rfl, rfl⟩)
  intro claim hclaim
  have : claim = .ownsDuty0 := Finset.mem_singleton.mp hclaim
  subst claim
  exact Derivable.root (r := Root.source) (by decide) rfl

/-- A deliberately bad extension that drops occurrence/current applicability. -/
def TimeErased (P : Finset Claim) (c : Claim) : Prop :=
  Rule P c ∨ (P = {.duty0, .ready} ∧ c = .actNow)

 theorem time_erasure_mutation_creates_unsupported_action :
    Derivable Base TimeErased (allRoots.erase .occasion) .actNow := by
  apply Derivable.step (premises := {.duty0, .ready}) (Or.inr ⟨rfl, rfl⟩)
  intro claim hclaim
  simp only [Finset.mem_insert, Finset.mem_singleton] at hclaim
  rcases hclaim with rfl | rfl
  · exact derivable_rules_mono (fun _ _ h => Or.inl h)
      duty_still_derives_when_current_applicability_is_absent
  · exact Derivable.root (r := Root.implementation) (by decide) rfl

/-- A deliberately bad extension that treats scope fit as current authority. -/
def GrantErased (P : Finset Claim) (c : Claim) : Prop :=
  Rule P c ∨ (P = {.scopeNow} ∧ c = .mayIssueNext)

 theorem grant_erasure_mutation_creates_unsupported_prospective_power :
    Derivable Base GrantErased (revokeProspective allRoots) .mayIssueNext := by
  apply Derivable.step (premises := {.scopeNow}) (Or.inr ⟨rfl, rfl⟩)
  intro claim hclaim
  have : claim = .scopeNow := Finset.mem_singleton.mp hclaim
  subst claim
  exact Derivable.root (r := Root.scopeNow) (by decide) rfl

end T20Grounded.Controls
