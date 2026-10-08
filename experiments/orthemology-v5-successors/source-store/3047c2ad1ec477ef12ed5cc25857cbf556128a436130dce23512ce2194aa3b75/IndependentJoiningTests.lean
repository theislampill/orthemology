import JointFiniteInterpretation
open JointFinite
namespace IndependentJoining
set_option maxRecDepth 16000
set_option maxHeartbeats 8000000
set_option synthInstance.maxSize 300000

-- Independent simplification list: no candidate finite_check macro or candidate
-- certificate is used for the new finite table judgments below.
macro "table_check" : tactic => `(tactic| (simp only [
  framework, account, speech, live, receivedBeing, contributionBearer,
  contributionResource, originalResourceUsed, producedAt, directSupport,
  supportAncestor, occursAt, tokenOccurrence, tokenBearer, modeExercise,
  derivedAct, derivedUses, mediateUse, productivelySupportsToken,
  Orthemology.Tranche20.OriginalBearerBridge.ActualOriginalResource,
  Orthemology.Tranche20.OriginalBearerBridge.ActualWholeOriginal,
  Orthemology.Tranche20.OriginalBearerBridge.OriginalWitness,
  Orthemology.Tranche20.OriginalBearerBridge.EssentialNonreceipt,
  Orthemology.Tranche3.SourceIdentity.Necessary,
  AnchoredSourceBridge.Complete, AnchoredSourceBridge.GlobalCoverage,
  AnchoredSourceBridge.ActualAnchor, AnchoredSourceBridge.FieldCND,
  AnchoredSourceBridge.ActualUnique, AnchoredSourceBridge.Overlap,
  AnchoredSourceBridge.Admissible, AnchoredSourceBridge.RequisiteSound,
  AnchoredSourceBridge.RequisiteExhaustive, AnchoredSourceBridge.Classification,
  AnchoredSourceBridge.Conformance, AnchoredSourceBridge.UseSound,
  AnchoredSourceBridge.RoleApplicable, AnchoredSourceBridge.Visible,
  AnchoredSourceBridge.RepresentedParticipation,
  VeracityBoundary.K, VeracityBoundary.A, VeracityBoundary.C,
  VeracityBoundary.D, VeracityBoundary.N, VeracityBoundary.P,
  VeracityBoundary.Package, VeracityBoundary.ExerciseBridge,
  VeracityBoundary.Counterfeit, VeracityBoundary.Veracity,
  VeracityBoundary.Factive] <;> decide))

theorem canonical_witness_exact : ∀ q s,
    Orthemology.Tranche20.OriginalBearerBridge.OriginalWitness framework .x q s ↔
    q = .rg ∧ s = .g := by table_check

theorem all_original_witnesses_exact : ∀ t q s,
    Orthemology.Tranche20.OriginalBearerBridge.OriginalWitness framework t q s ↔
    ((t = .x ∨ t = .l ∨ t = .r ∨ t = .m) ∧ q = .rg ∧ s = .g) ∨
    (t = .z ∧ q = .rh ∧ s = .h) := by table_check

theorem resources_are_not_provider_relabels :
    contributionBearer .cx = B.x ∧ contributionResource .cx = R.rx ∧
    originalResourceUsed .rg .cx ∧ ¬ originalResourceUsed .rx .cx ∧
    framework.intrinsic .g .rg ∧ framework.intrinsic .x .rx ∧
    ¬ framework.intrinsic .g .rx ∧ ¬ framework.intrinsic .x .rg := by table_check

-- Permute only the account's source interpretation. Every account proof can
-- still be true at h while the ABC and veracity interpretations remain at g.
def swapSource : B → B | .g => .h | .h => .g | other => other
def switched : AnchoredSourceBridge.Account B E C :=
  { account with
    EntireOrig := fun s c => account.EntireOrig (swapSource s) c
    ActualOriginal := fun s e => account.ActualOriginal (swapSource s) e
    ModeRole := fun s e => account.ModeRole (swapSource s) e
    Qualified := fun s => account.Qualified (swapSource s)
    ModeDefect := fun s e => account.ModeDefect (swapSource s) e }

theorem detached_component_witnesses_do_not_join :
    AnchoredSourceBridge.GlobalCoverage switched .h ∧
    switched.Qualified .h ∧ AnchoredSourceBridge.Classification switched .h ∧
    AnchoredSourceBridge.Conformance switched .h ∧
    AnchoredSourceBridge.UseSound switched ∧ AnchoredSourceBridge.RoleApplicable switched .h ∧
    AnchoredSourceBridge.Visible switched ∧ AnchoredSourceBridge.FieldCND switched ∧
    AnchoredSourceBridge.ActualAnchor switched .h .a ∧
    Orthemology.Tranche20.OriginalBearerBridge.OriginalWitness framework .x .rg .g ∧
    VeracityBoundary.Package speech .g ∧
    ¬ AnchoredSourceBridge.GlobalCoverage switched .g ∧
    ¬ (∀ s c, switched.EntireOrig s c ↔ ∃ q,
       Orthemology.Tranche20.OriginalBearerBridge.ActualOriginalResource framework q ∧
       framework.intrinsic s q ∧ originalResourceUsed q c) := by
  simp only [switched, swapSource]
  table_check

theorem switched_is_connected : AnchoredSourceBridge.ConnectedFrom switched .a := by
  have transport : ∀ first last, AnchoredSourceBridge.Path account first last →
      AnchoredSourceBridge.Path switched first last := by
    intro first last path
    induction path with
    | refl he => exact AnchoredSourceBridge.Path.refl he
    | step he hf overlap _ ih => exact AnchoredSourceBridge.Path.step he hf overlap ih
  intro e field
  exact transport .a e (JointFinite.field_connected e field)

-- Add a real productive h -> m edge, without modifying any component account.
def incomingSupport (s t : B) : Prop := directSupport s t ∨ (s = .h ∧ t = .m)
inductive IncomingReach : B → B → Prop where
  | edge {s t} : incomingSupport s t → IncomingReach s t
  | trans {s t u} : IncomingReach s t → IncomingReach t u → IncomingReach s u

theorem omitted_h_edge_is_live : IncomingReach .h .m :=
  IncomingReach.edge (Or.inr ⟨rfl, rfl⟩)

theorem omitted_h_breaks_stored_reachability :
    IncomingReach .h .m ∧ ¬ supportAncestor .h .m := by
  exact ⟨omitted_h_edge_is_live, by table_check⟩

theorem omitted_h_breaks_joining_inventory :
    ¬ (∀ e, account.Field e → ∀ t, producedAt t e → ∀ y,
      IncomingReach y t → y ≠ .g → ∃ c, account.Req e c ∧ contributionBearer c = y) := by
  intro inventory
  have hidden := inventory .k (by table_check) .m (by table_check) .h omitted_h_edge_is_live (by decide)
  have absent : ¬ (∃ c, account.Req .k c ∧ contributionBearer c = B.h) := by table_check
  exact absent hidden

theorem original_h_has_no_positive_path_inside :
    ∀ e t, account.Field e → producedAt t e → ¬ PositiveReach .h t := by
  intro e t he ht reach
  have absent : ∀ e t, account.Field e → producedAt t e → ¬ supportAncestor .h t := by table_check
  exact absent e t he ht (JointFinite.reach_is_ancestor reach)

-- Enlarging the domain is a new application. Here CND survives, but the
-- selected component's connectedness, coverage and actual uniqueness do not.
def enlarged : AnchoredSourceBridge.Account B E C := { account with Field := fun _ => True }

theorem enlarged_basic_guards_survive :
    AnchoredSourceBridge.Admissible enlarged ∧
    AnchoredSourceBridge.RequisiteSound enlarged ∧
    AnchoredSourceBridge.RequisiteExhaustive enlarged ∧
    AnchoredSourceBridge.FieldCND enlarged ∧
    AnchoredSourceBridge.Classification enlarged .g ∧
    AnchoredSourceBridge.Conformance enlarged .g ∧
    AnchoredSourceBridge.UseSound enlarged ∧
    AnchoredSourceBridge.RoleApplicable enlarged .g ∧
    AnchoredSourceBridge.Visible enlarged ∧
    AnchoredSourceBridge.ActualAnchor enlarged .g .a := by
  simp only [enlarged]; table_check

theorem enlarged_outside_partition : ∀ e f,
    AnchoredSourceBridge.Overlap enlarged e f → (e = .o ↔ f = .o) := by
  simp only [enlarged]; table_check

theorem enlarged_paths_preserve_partition {e f : E}
    (p : AnchoredSourceBridge.Path enlarged e f) : e = .o ↔ f = .o := by
  induction p with
  | refl _ => rfl
  | step _ _ overlap _ ih => exact (enlarged_outside_partition _ _ overlap).trans ih

theorem enlarged_is_not_connected : ¬ AnchoredSourceBridge.ConnectedFrom enlarged .a := by
  intro h
  have impossible := (enlarged_paths_preserve_partition (h .o trivial)).mpr rfl
  cases impossible

theorem enlarged_has_no_common_provider :
    ¬ AnchoredSourceBridge.GlobalCoverage enlarged .g ∧
    ¬ AnchoredSourceBridge.ActualUnique enlarged .g ∧
    ¬ (∃ s, AnchoredSourceBridge.GlobalCoverage enlarged s) := by
  simp only [enlarged]; table_check

theorem contextual_truth_does_not_create_ownership :
    speech.trueAt .w2 .absent ∧ ¬ framework.existsAt .w2 .l ∧
    (∀ s t q, ¬ speech.asserts .w2 s t q) ∧
    speech.asserts .w0 .x .v .absent ∧ ¬ speech.trueAt .w0 .absent ∧
    (∀ w q, ¬ speech.asserts w .g .v q) ∧
    (∀ w q, ¬ speech.asserts w .x .u q) := by table_check

theorem every_owned_assertion_has_existing_owner_and_token_event :
    ∀ w s t q, speech.asserts w s t q →
    framework.existsAt w s ∧ occursAt w (tokenOccurrence t) ∧
    framework.existsAt w (tokenBearer t) := by table_check

theorem absent_creatures_have_no_world_indexed_activity :
    (∀ t, receivedBeing t → ¬ framework.existsAt .w2 t ∧ ¬ framework.wholeReceived .w2 t) ∧
    (∀ s t, ¬ framework.dep .w2 s t) ∧
    (∀ e, ¬ occursAt .w2 e) ∧
    (∀ s e, ¬ speech.actual .w2 s e ∧ ¬ speech.fitting .w2 s e ∧ ¬ speech.shortcoming .w2 s e) ∧
    (∀ s t q, ¬ speech.aware .w2 s t q) ∧
    (∀ s t, ¬ speech.deliberate .w2 s t) ∧
    framework.existsAt .w2 .g ∧ framework.existsAt .w2 .h := by table_check

theorem static_production_is_properly_world_gated :
    (∀ w t e, producedAt t e → (occursAt w e ↔ framework.existsAt w t)) ∧
    (∀ w s e, speech.actual w s e → framework.existsAt w s) ∧
    (∀ s t, directSupport s t → framework.existsAt .w0 s ∧ framework.existsAt .w0 t) ∧
    (∀ e, account.ActualOccurrence e ↔ occursAt .w0 e) := by table_check

theorem received_capacity_and_false_exercise_do_not_transfer :
    derivedAct .x .k ∧ speech.actual .w0 .x .actX ∧ speech.fitting .w0 .x .actX ∧
    speech.actual .w0 .g .provideK ∧ speech.fitting .w0 .g .provideK ∧
    speech.shortcoming .w0 .x .sayX ∧ ¬ speech.shortcoming .w0 .g .provideK ∧
    productivelySupportsToken .g .v ∧ ¬ speech.asserts .w0 .g .v .absent := by table_check

-- Literal same-source consistency does not supply a new ABC -> normative bridge.
def unqualified : AnchoredSourceBridge.Account B E C := { account with Qualified := fun _ => False }
def nonconforming : VeracityBoundary.Model B W Token Content Exercise :=
  { speech with fitting := fun _ _ _ => False }
theorem abc_does_not_force_added_premises :
    Orthemology.Tranche20.OriginalBearerBridge.FullPremises framework ∧
    ¬ unqualified.Qualified .g ∧ ¬ VeracityBoundary.Package nonconforming .g := by
  refine ⟨JointFinite.abc_full, ?_⟩
  simp only [unqualified, nonconforming]
  table_check

end IndependentJoining
