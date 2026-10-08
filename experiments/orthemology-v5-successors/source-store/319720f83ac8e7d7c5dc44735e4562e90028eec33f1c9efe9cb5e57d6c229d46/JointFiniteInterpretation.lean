import OriginalBearerBridge
import AnchoredSourceBridge
import VeracityBoundary

/-! One finite selected-fragment interpretation. All source identities are literal.
No metaphysical possibility, full source-profile or general refinement claim. -/
namespace JointFinite

set_option synthInstance.maxSize 200000
set_option maxRecDepth 12000
set_option maxHeartbeats 4000000
set_option linter.constructorNameAsVariable false

inductive W | w0 | w1 | w2 deriving DecidableEq, Repr
inductive B | g | h | x | l | r | m | z deriving DecidableEq, Repr
inductive R | rg | rh | rx | rl | rr | rm | rz deriving DecidableEq, Repr
inductive E | a | b | k | o deriving DecidableEq, Repr
inductive C | cx | cl | cr | cm | cz deriving DecidableEq, Repr
inductive Token | u | v deriving DecidableEq, Repr
inductive Content | present | absent deriving DecidableEq, Repr
inductive Exercise | sayG | sayX | provideA | provideB | provideK | provideO | actX
  deriving DecidableEq, Repr

instance : Fintype W := ⟨{.w0, .w1, .w2}, by intro w; cases w <;> simp⟩
instance : Fintype B := ⟨{.g, .h, .x, .l, .r, .m, .z}, by intro b; cases b <;> simp⟩
instance : Fintype R := ⟨{.rg, .rh, .rx, .rl, .rr, .rm, .rz}, by intro r; cases r <;> simp⟩
instance : Fintype E := ⟨{.a, .b, .k, .o}, by intro e; cases e <;> simp⟩
instance : Fintype C := ⟨{.cx, .cl, .cr, .cm, .cz}, by intro c; cases c <;> simp⟩
instance : Fintype Token := ⟨{.u, .v}, by intro t; cases t <;> simp⟩
instance : Fintype Content := ⟨{.present, .absent}, by intro q; cases q <;> simp⟩
instance : Fintype Exercise :=
  ⟨{.sayG, .sayX, .provideA, .provideB, .provideK, .provideO, .actX}, by intro e; cases e <;> simp⟩

def live (w : W) : Prop := w = .w0 ∨ w = .w1
def receivedBeing (b : B) : Prop := b = .x ∨ b = .l ∨ b = .r ∨ b = .m ∨ b = .z

def framework : Orthemology.Tranche20.OriginalBearerBridge.Framework W B R B where
  actual := .w0
  existsAt := fun w b => b = .g ∨ b = .h ∨ (live w ∧ receivedBeing b)
  wholeReceived := fun w b => live w ∧ receivedBeing b
  dep := fun w s b => live w ∧
    ((s = .g ∧ (b = .x ∨ b = .l ∨ b = .r ∨ b = .m)) ∨ (s = .h ∧ b = .z))
  resourceActual := fun _ => True
  resourceReceived := fun q => q = .rx ∨ q = .rl ∨ q = .rr ∨ q = .rm ∨ q = .rz
  intrinsic := fun b q => (b = .g ∧ q = .rg) ∨ (b = .h ∧ q = .rh) ∨
    (b = .x ∧ q = .rx) ∨ (b = .l ∧ q = .rl) ∨ (b = .r ∧ q = .rr) ∨
    (b = .m ∧ q = .rm) ∨ (b = .z ∧ q = .rz)
  targetReceived := receivedBeing
  relevant := fun q t => (q = .rg ∧ (t = .x ∨ t = .l ∨ t = .r ∨ t = .m)) ∨
    (q = .rh ∧ t = .z) ∨ ((q = .rx ∨ q = .rl ∨ q = .rr) ∧ t = .m)

def account : AnchoredSourceBridge.Account B E C where
  Field := fun e => e = .a ∨ e = .b ∨ e = .k
  ActualOccurrence := fun _ => True
  Req := fun e c => (e = .a ∧ (c = .cx ∨ c = .cl)) ∨ (e = .b ∧ c = .cr) ∨
    (e = .k ∧ (c = .cx ∨ c = .cl ∨ c = .cr ∨ c = .cm)) ∨ (e = .o ∧ c = .cz)
  Operative := fun e c => (e = .a ∧ (c = .cx ∨ c = .cl)) ∨ (e = .b ∧ c = .cr) ∨
    (e = .k ∧ (c = .cx ∨ c = .cl ∨ c = .cr ∨ c = .cm)) ∨ (e = .o ∧ c = .cz)
  EntireOrig := fun s c => (s = .g ∧ (c = .cx ∨ c = .cl ∨ c = .cr ∨ c = .cm)) ∨
    (s = .h ∧ c = .cz)
  ActualOriginal := fun s e => (s = .g ∧ (e = .a ∨ e = .b ∨ e = .k)) ∨ (s = .h ∧ e = .o)
  ModeRole := fun s e => (s = .g ∧ (e = .a ∨ e = .b ∨ e = .k)) ∨ (s = .h ∧ e = .o)
  Qualified := fun s => s = .g
  ModeDefect := fun _ _ => False

def producedAt (b : B) (e : E) : Prop :=
  ((b = .x ∨ b = .l) ∧ e = .a) ∨ (b = .r ∧ e = .b) ∨
  (b = .m ∧ e = .k) ∨ (b = .z ∧ e = .o)
def occursAt (w : W) (_ : E) : Prop := live w
def contributionBearer : C → B | .cx => .x | .cl => .l | .cr => .r | .cm => .m | .cz => .z
def contributionResource : C → R | .cx => .rx | .cl => .rl | .cr => .rr | .cm => .rm | .cz => .rz
def originalResourceUsed (q : R) (c : C) : Prop :=
  (q = .rg ∧ (c = .cx ∨ c = .cl ∨ c = .cr ∨ c = .cm)) ∨ (q = .rh ∧ c = .cz)
def directSupport (s t : B) : Prop :=
  (s = .g ∧ (t = .x ∨ t = .l ∨ t = .r)) ∨
  ((s = .x ∨ s = .l ∨ s = .r) ∧ t = .m) ∨ (s = .h ∧ t = .z)
def supportAncestor (s t : B) : Prop :=
  (s = .g ∧ (t = .x ∨ t = .l ∨ t = .r ∨ t = .m)) ∨
  ((s = .x ∨ s = .l ∨ s = .r) ∧ t = .m) ∨ (s = .h ∧ t = .z)
def derivedAct (s : B) (e : E) : Prop := s = .x ∧ e = .k
def derivedUses (s : B) (e : E) (c : C) : Prop :=
  s = .x ∧ e = .k ∧ (c = .cx ∨ c = .cl ∨ c = .cr)
def mediateUse (e f : E) (c : C) : Prop :=
  (e = .a ∧ f = .k ∧ (c = .cx ∨ c = .cl)) ∨ (e = .b ∧ f = .k ∧ c = .cr)
def tokenOccurrence : Token → E | .u => .b | .v => .k
def tokenBearer : Token → B | .u => .r | .v => .m
def modeExercise : E → Exercise | .a => .provideA | .b => .provideB | .k => .provideK | .o => .provideO
def productivelySupportsToken (s : B) (_ : Token) : Prop := s = .g
def authenticated (_ : Token) : Prop := False

def speech : VeracityBoundary.Model B W Token Content Exercise where
  asserts := fun w s t q => live w ∧
    ((s = .g ∧ t = .u ∧ q = .present) ∨ (s = .x ∧ t = .v ∧ q = .absent))
  trueAt := fun w q => (live w ∧ q = .present) ∨ (w = .w2 ∧ q = .absent)
  knowsFalse := fun w s q =>
    (s = .g ∧ ((live w ∧ q = .absent) ∨ (w = .w2 ∧ q = .present))) ∨
    (s = .x ∧ live w ∧ q = .absent)
  aware := fun w s t q => live w ∧
    ((s = .g ∧ t = .u ∧ q = .present) ∨ (s = .x ∧ t = .v ∧ q = .absent))
  deliberate := fun w s t => live w ∧ ((s = .g ∧ t = .u) ∨ (s = .x ∧ t = .v))
  exercise := fun t => match t with | .u => .sayG | .v => .sayX
  actual := fun w s e => live w ∧
    ((s = .g ∧ (e = .sayG ∨ e = .provideA ∨ e = .provideB ∨ e = .provideK)) ∨
     (s = .h ∧ e = .provideO) ∨ (s = .x ∧ (e = .sayX ∨ e = .actX)))
  fitting := fun w s e => live w ∧
    ((s = .g ∧ (e = .sayG ∨ e = .provideA ∨ e = .provideB ∨ e = .provideK)) ∨
     (s = .h ∧ e = .provideO) ∨ (s = .x ∧ e = .actX))
  shortcoming := fun w s e => live w ∧ s = .x ∧ e = .sayX

macro "finite_check" : tactic => `(tactic| (simp only [
  framework, account, speech, live, receivedBeing, producedAt, occursAt,
  contributionBearer, contributionResource, originalResourceUsed, directSupport,
  supportAncestor, derivedAct, derivedUses, mediateUse, tokenOccurrence,
  tokenBearer, modeExercise, productivelySupportsToken, authenticated,
  Orthemology.Tranche20.OriginalBearerBridge.Completion, Orthemology.Tranche20.OriginalBearerBridge.Realisation, Orthemology.Tranche20.OriginalBearerBridge.SupportTransport, Orthemology.Tranche20.OriginalBearerBridge.ReceiptRepresentation,
  Orthemology.Tranche20.OriginalBearerBridge.ContingencyNeed, Orthemology.Tranche20.OriginalBearerBridge.ConstitutiveReception, Orthemology.Tranche20.OriginalBearerBridge.ActualOriginalResource,
  Orthemology.Tranche20.OriginalBearerBridge.ActualWholeOriginal, Orthemology.Tranche20.OriginalBearerBridge.OriginalWitness, Orthemology.Tranche20.OriginalBearerBridge.EssentialNonreceipt,
  Orthemology.Tranche3.SourceIdentity.Received, Orthemology.Tranche3.SourceIdentity.Root, Orthemology.Tranche3.SourceIdentity.Necessary, Orthemology.Tranche3.SourceIdentity.UniformRoot, Orthemology.Tranche3.SourceIdentity.GenericReception,
  AnchoredSourceBridge.Admissible, AnchoredSourceBridge.RequisiteSound, AnchoredSourceBridge.RequisiteExhaustive,
  AnchoredSourceBridge.UseSound, AnchoredSourceBridge.RoleApplicable, AnchoredSourceBridge.Visible, AnchoredSourceBridge.Classification,
  AnchoredSourceBridge.Conformance, AnchoredSourceBridge.ModeSatisfaction, AnchoredSourceBridge.SourceMode, AnchoredSourceBridge.CND,
  AnchoredSourceBridge.FieldCND, AnchoredSourceBridge.Overlap, AnchoredSourceBridge.ActualAnchor, AnchoredSourceBridge.Positive,
  AnchoredSourceBridge.ActualUnique, AnchoredSourceBridge.RepresentedParticipation, AnchoredSourceBridge.Complete,
  AnchoredSourceBridge.GlobalCoverage, VeracityBoundary.K, VeracityBoundary.A, VeracityBoundary.C, VeracityBoundary.D, VeracityBoundary.N, VeracityBoundary.P, VeracityBoundary.ExerciseBridge,
  VeracityBoundary.Factive, VeracityBoundary.Veracity, VeracityBoundary.NoCounterfeit, VeracityBoundary.Package, VeracityBoundary.Counterfeit,
  VeracityBoundary.informedOwnership] <;> decide))

theorem abc_full : Orthemology.Tranche20.OriginalBearerBridge.FullPremises framework := by
  constructor <;> finite_check

theorem J01_canonical_identity : ∀ q s,
    Orthemology.Tranche20.OriginalBearerBridge.OriginalWitness framework .x q s → q = .rg ∧ s = .g := by finite_check

/-- The original A theorem is applied at x, then its actual witnesses identified. -/
theorem canonical_original_via_component : Orthemology.Tranche20.OriginalBearerBridge.OriginalWitness framework .x .rg .g := by
  obtain ⟨q, s, witness⟩ := Orthemology.Tranche20.OriginalBearerBridge.original_bearer_of_completion framework .x
    (by finite_check) abc_full.completion abc_full.realisation abc_full.support
  obtain ⟨hq, hs⟩ := J01_canonical_identity q s witness
  subst q; subst s
  exact witness

theorem canonical_root_via_component : Orthemology.Tranche3.SourceIdentity.Root framework.existsAt framework.dep .w0 .g :=
  Orthemology.Tranche20.OriginalBearerBridge.root_to_inherited framework abc_full.representation .g
    canonical_original_via_component.2.2.2.2

theorem canonical_necessary_via_inherited : Orthemology.Tranche3.SourceIdentity.Necessary framework.existsAt .g :=
  Orthemology.Tranche3.SourceIdentity.necessary_of_actual_root framework.existsAt framework.dep .w0 .g
    canonical_root_via_component
    (Orthemology.Tranche20.OriginalBearerBridge.need_to_inherited framework abc_full.representation abc_full.need)

theorem canonical_uniform_via_inherited : Orthemology.Tranche3.SourceIdentity.UniformRoot framework.existsAt framework.dep .g :=
  Orthemology.Tranche3.SourceIdentity.uniform_of_necessary_actual_root framework.existsAt framework.dep .w0 .g
    canonical_root_via_component canonical_necessary_via_inherited
    (Orthemology.Tranche20.OriginalBearerBridge.constitution_to_inherited framework abc_full.representation abc_full.constitution)

theorem canonical_abc_same_g : Orthemology.Tranche20.OriginalBearerBridge.OriginalWitness framework .x .rg .g ∧
    Orthemology.Tranche3.SourceIdentity.Necessary framework.existsAt .g ∧ Orthemology.Tranche3.SourceIdentity.UniformRoot framework.existsAt framework.dep .g ∧
    Orthemology.Tranche20.OriginalBearerBridge.EssentialNonreceipt framework .g :=
  ⟨canonical_original_via_component, canonical_necessary_via_inherited,
   canonical_uniform_via_inherited,
   Orthemology.Tranche20.OriginalBearerBridge.essential_nonreceipt_of_actual_original framework .g
    canonical_original_via_component.2.2.2.2 abc_full.constitution⟩

theorem generic_abc_via_component : ∃ t q s, Orthemology.Tranche20.OriginalBearerBridge.OriginalWitness framework t q s ∧
    Orthemology.Tranche3.SourceIdentity.Necessary framework.existsAt s ∧ Orthemology.Tranche3.SourceIdentity.UniformRoot framework.existsAt framework.dep s ∧
    Orthemology.Tranche20.OriginalBearerBridge.EssentialNonreceipt framework s := Orthemology.Tranche20.OriginalBearerBridge.abc_same_witness framework abc_full

theorem abc_live_receipt_and_transport : framework.existsAt .w0 .x ∧
    framework.existsAt .w1 .x ∧ ¬ framework.existsAt .w2 .x ∧
    framework.wholeReceived .w0 .x ∧ framework.wholeReceived .w1 .x ∧
    framework.intrinsic .x .rx ∧ framework.resourceReceived .rx ∧
    ¬ Orthemology.Tranche3.SourceIdentity.Necessary framework.existsAt .x := by finite_check

theorem field_admissible : AnchoredSourceBridge.Admissible account := by finite_check
theorem field_req_sound : AnchoredSourceBridge.RequisiteSound account := by finite_check
theorem field_req_exhaustive : AnchoredSourceBridge.RequisiteExhaustive account := by finite_check
theorem field_qualified : account.Qualified .g := by finite_check
theorem field_classification : AnchoredSourceBridge.Classification account .g := by finite_check
theorem field_conformance : AnchoredSourceBridge.Conformance account .g := by finite_check
theorem field_use_sound : AnchoredSourceBridge.UseSound account := by finite_check
theorem field_role : AnchoredSourceBridge.RoleApplicable account .g := by finite_check
theorem field_visible : AnchoredSourceBridge.Visible account := by finite_check
theorem field_anchor : AnchoredSourceBridge.ActualAnchor account .g .a := by finite_check
theorem field_cnd : AnchoredSourceBridge.FieldCND account := by finite_check

theorem field_connected : AnchoredSourceBridge.ConnectedFrom account .a := by
  intro e he
  cases e with
  | a => exact AnchoredSourceBridge.Path.refl (by finite_check)
  | b =>
    exact AnchoredSourceBridge.Path.step (e := E.a) (f := E.k) (z := E.b)
      (by finite_check) (by finite_check)
      (show AnchoredSourceBridge.Overlap account .a .k from by finite_check)
      (AnchoredSourceBridge.Path.step (e := E.k) (f := E.b) (z := E.b)
        (by finite_check) (by finite_check)
        (show AnchoredSourceBridge.Overlap account .k .b from by finite_check) (AnchoredSourceBridge.Path.refl he))
  | k =>
    exact AnchoredSourceBridge.Path.step (e := E.a) (f := E.k) (z := E.k)
      (by finite_check) he
      (show AnchoredSourceBridge.Overlap account .a .k from by finite_check) (AnchoredSourceBridge.Path.refl he)
  | o => exact False.elim ((show ¬ account.Field .o from by finite_check) he)

theorem field_coverage_without_cnd : AnchoredSourceBridge.GlobalCoverage account .g :=
  AnchoredSourceBridge.global_coverage_of_qualified_anchor account .g .a field_qualified
    field_classification field_conformance field_use_sound field_role field_anchor field_connected

theorem field_guarded : AnchoredSourceBridge.Admissible account ∧ AnchoredSourceBridge.RequisiteSound account ∧
    AnchoredSourceBridge.RequisiteExhaustive account ∧ AnchoredSourceBridge.GlobalCoverage account .g ∧
    AnchoredSourceBridge.ActualUnique account .g ∧
    (∀ e, account.Field e → ∀ s, AnchoredSourceBridge.Complete account s e → s = .g) :=
  AnchoredSourceBridge.guarded_common_original_provider account .g .a field_admissible field_req_sound
    field_req_exhaustive field_qualified field_classification field_conformance field_use_sound
    field_role field_visible field_anchor field_connected field_cnd

theorem field_positive : ∀ e, account.Field e → AnchoredSourceBridge.Positive account e :=
  AnchoredSourceBridge.every_field_positive account .g .a field_visible field_anchor field_connected

theorem complete_provider_exists_and_unique :
    (∃ s, AnchoredSourceBridge.GlobalCoverage account s) ∧
    (∀ e, account.Field e → ∀ s, AnchoredSourceBridge.Complete account s e → s = .g) :=
  AnchoredSourceBridge.unique_complete_provider account .g .a field_coverage_without_cnd field_cnd
    field_visible field_anchor field_connected

theorem mixed_occurrence_real : account.ActualOccurrence .k ∧ .a ≠ E.k ∧ .b ≠ E.k ∧
    ¬ AnchoredSourceBridge.Overlap account .a .b ∧ AnchoredSourceBridge.Overlap account .a .k ∧
    AnchoredSourceBridge.Overlap account .k .b ∧ account.Req .k .cm ∧
    derivedAct .x .k ∧ derivedUses .x .k .cx ∧ derivedUses .x .k .cl ∧
    derivedUses .x .k .cr ∧ mediateUse .a .k .cl ∧ mediateUse .b .k .cr ∧
    ¬ mediateUse .k .a .cl ∧ ¬ mediateUse .k .b .cr := by finite_check

theorem veracity_package : VeracityBoundary.Package speech .g := by finite_check
theorem veracity_factive : VeracityBoundary.Factive speech .g := by finite_check
theorem veracity_via_component : VeracityBoundary.Veracity speech .g :=
  VeracityBoundary.veracity_of_coverage speech .g veracity_package.1 veracity_package.2.1
    veracity_package.2.2.1 veracity_package.2.2.2.1 veracity_package.2.2.2.2.1
    veracity_package.2.2.2.2.2.1 veracity_package.2.2.2.2.2.2

theorem honesty_equivalence_via_component : VeracityBoundary.Veracity speech .g ↔ VeracityBoundary.NoCounterfeit speech .g :=
  VeracityBoundary.veracity_iff_no_counterfeit speech .g veracity_package.1 veracity_package.2.1
    veracity_package.2.2.1 veracity_factive

theorem created_speaker_normative_boundary : VeracityBoundary.K speech .x ∧ VeracityBoundary.A speech .x ∧
    VeracityBoundary.C speech .x ∧ VeracityBoundary.D speech .x ∧ VeracityBoundary.N speech .x ∧ VeracityBoundary.ExerciseBridge speech .x ∧
    VeracityBoundary.Factive speech .x ∧ ¬ VeracityBoundary.P speech .x ∧ ¬ VeracityBoundary.Package speech .x ∧
    VeracityBoundary.Counterfeit speech .x .w0 .v .absent ∧ speech.shortcoming .w0 .x .sayX ∧
    ¬ speech.fitting .w0 .x .sayX := by finite_check

theorem source_live_knowledge_and_nonspeech_conformance :
    speech.knowsFalse .w0 .g .absent ∧ ¬ speech.trueAt .w0 .absent ∧
    ¬ (∃ t, speech.asserts .w0 .g t .absent) ∧
    speech.asserts .w0 .g .u .present ∧ speech.trueAt .w0 .present ∧
    speech.actual .w0 .g .provideK ∧ speech.fitting .w0 .g .provideK ∧
    (∀ t, speech.exercise t ≠ .provideK) := by finite_check

inductive PositiveReach : B → B → Prop where
  | edge {s t} : directSupport s t → PositiveReach s t
  | trans {s t u} : PositiveReach s t → PositiveReach t u → PositiveReach s u

theorem ancestor_transitive : ∀ s t u, supportAncestor s t → supportAncestor t u → supportAncestor s u := by
  finite_check
theorem direct_is_ancestor : ∀ s t, directSupport s t → supportAncestor s t := by finite_check
theorem ancestor_decomposition : ∀ s t, supportAncestor s t → directSupport s t ∨ (s = .g ∧ t = .m) := by
  finite_check

theorem reach_is_ancestor {s t : B} (h : PositiveReach s t) : supportAncestor s t := by
  induction h with
  | edge h => exact direct_is_ancestor _ _ h
  | trans _ _ ih1 ih2 => exact ancestor_transitive _ _ _ ih1 ih2

theorem ancestor_is_reach {s t : B} (h : supportAncestor s t) : PositiveReach s t := by
  cases ancestor_decomposition s t h with
  | inl hd => exact PositiveReach.edge hd
  | inr special =>
    obtain ⟨hs, ht⟩ := special
    subst s; subst t
    exact PositiveReach.trans (PositiveReach.edge (show directSupport .g .x from by finite_check))
      (PositiveReach.edge (show directSupport .x .m from by finite_check))

theorem J02_original_resource_provision : ∀ s c,
    account.EntireOrig s c ↔ ∃ q, Orthemology.Tranche20.OriginalBearerBridge.ActualOriginalResource framework q ∧
      framework.intrinsic s q ∧ originalResourceUsed q c := by finite_check

theorem J03_concrete_receipt : ∀ c,
    framework.wholeReceived .w0 (contributionBearer c) ∧
    framework.resourceReceived (contributionResource c) ∧
    framework.intrinsic (contributionBearer c) (contributionResource c) := by finite_check

theorem J04_field_target_link :
    (∀ t e, producedAt t e → framework.targetReceived t) ∧
    (∀ e, account.Field e → ∃ t, producedAt t e) ∧ producedAt .x .a := by finite_check

theorem J05_positive_reachability : ∀ s t, supportAncestor s t ↔ PositiveReach s t :=
  fun _ _ => ⟨ancestor_is_reach, reach_is_ancestor⟩

theorem J05_live_productive_support : PositiveReach .g .x ∧ PositiveReach .g .l ∧
    PositiveReach .g .r ∧ PositiveReach .g .m ∧ PositiveReach .h .z ∧
    directSupport .x .m ∧ derivedUses .x .k .cx ∧ derivedUses .x .k .cl ∧
    derivedUses .x .k .cr := by
  refine ⟨ancestor_is_reach (by finite_check), ancestor_is_reach (by finite_check),
    ancestor_is_reach (by finite_check), ancestor_is_reach (by finite_check),
    ancestor_is_reach (by finite_check), ?_⟩
  finite_check

theorem reception_and_direct_support_distinct :
    framework.dep .w0 .g .m ∧ ¬ directSupport .g .m ∧ directSupport .x .m ∧
    ¬ framework.dep .w0 .x .m ∧ PositiveReach .g .m := by
  refine ⟨?_, ?_, ?_, ?_, ancestor_is_reach (by finite_check)⟩ <;> finite_check

theorem J06_complete_incoming_inventory :
    (∀ e, account.Field e → ∀ t, producedAt t e → ∀ y,
      supportAncestor y t → y ≠ .g → ∃ c, account.Req e c ∧ contributionBearer c = y) ∧
    (∀ e c, account.Field e → account.Req e c → ∃ t, producedAt t e ∧
      (contributionBearer c = t ∨ supportAncestor (contributionBearer c) t)) := by finite_check

theorem J07_no_incoming_outside_source :
    (∀ e t, account.Field e → producedAt t e → ¬ directSupport .h t ∧ ¬ supportAncestor .h t) ∧
    (∀ e c, account.Field e → account.Req e c → ¬ account.EntireOrig .h c) ∧
    (∀ e, account.Field e → ¬ account.ActualOriginal .h e) := by finite_check

theorem J08_actual_mode_realization : ∀ s e, account.ModeRole s e →
    speech.actual .w0 s (modeExercise e) := by finite_check

theorem J09_fitting_source_realization :
    (∀ e, account.ModeRole .g e → speech.fitting .w0 .g (modeExercise e)) ∧
    ¬ speech.fitting .w0 .x .sayX := by finite_check

theorem J10_truth_grounding : ∀ w,
    (speech.trueAt w .present ↔ framework.existsAt w .l) ∧
    (speech.trueAt w .absent ↔ ¬ framework.existsAt w .l) := by finite_check

theorem J11_token_support_grounding :
    (∀ s t, productivelySupportsToken s t ↔ account.ActualOriginal s (tokenOccurrence t)) ∧
    (∀ t, producedAt (tokenBearer t) (tokenOccurrence t)) := by finite_check

theorem J12_support_not_ownership : productivelySupportsToken .g .v ∧
    speech.asserts .w0 .x .v .absent ∧ ¬ speech.trueAt .w0 .absent ∧
    ¬ speech.asserts .w0 .g .v .absent := by finite_check

theorem J13_genuine_agent_identity : B.x ≠ B.g ∧ B.x ≠ B.h ∧
    framework.existsAt .w0 .x ∧ framework.existsAt .w1 .x ∧ ¬ framework.existsAt .w2 .x ∧
    framework.intrinsic .x .rx ∧ derivedAct .x .k ∧ speech.actual .w0 .x .actX ∧
    speech.actual .w0 .x .sayX := by finite_check

theorem J14_outside_boundary : B.h ≠ B.g ∧ Orthemology.Tranche3.SourceIdentity.Necessary framework.existsAt .h ∧
    Orthemology.Tranche20.OriginalBearerBridge.EssentialNonreceipt framework .h ∧ Orthemology.Tranche3.SourceIdentity.UniformRoot framework.existsAt framework.dep .h ∧
    Orthemology.Tranche20.OriginalBearerBridge.ActualWholeOriginal framework .h ∧ framework.intrinsic .h .rh ∧
    Orthemology.Tranche20.OriginalBearerBridge.ActualOriginalResource framework .rh ∧ account.EntireOrig .h .cz ∧
    account.ActualOriginal .h .o ∧ ¬ AnchoredSourceBridge.Complete account .g .o := by finite_check

theorem J15_strong_ownership_extension : ∀ s, (s = .g ∨ s = .x) → ∀ w t q,
    (VeracityBoundary.informedOwnership speech).asserts w s t q ↔ speech.asserts w s t q := by finite_check

def selectedSupport (s : B) : Prop := s = .g ∨ s = .x ∨ s = .l ∨ s = .r ∨ s = .m
def below (s t : B) : Prop := s = t ∨ supportAncestor s t
def localCover (s t : B) : Prop := below s t ∧ ∀ y, below y t → below s y

/-- Exact finite formula compatibility only; no general Sixth refinement. -/
theorem finite_ancestry_compatibility :
    (∀ s, ¬ supportAncestor s s) ∧
    (∀ s t u, supportAncestor s t → supportAncestor t u → supportAncestor s u) ∧
    (∀ s t, selectedSupport t → supportAncestor s t → selectedSupport s) ∧
    (∀ t, selectedSupport t → localCover .g t) ∧
    (∀ t, selectedSupport t → t = .g ∨ supportAncestor .g t) ∧
    supportAncestor .g .x ∧ ¬ selectedSupport .h ∧ ¬ selectedSupport .z := by
  simp only [selectedSupport, localCover, below]
  finite_check

theorem no_source_or_created_authentication : ¬ authenticated .u ∧ ¬ authenticated .v := by finite_check

theorem good_source_antecedent_boundary :
    (∀ e, account.Field e → account.ModeRole .g e → ¬ (¬ AnchoredSourceBridge.Complete account .g e)) ∧
    (∀ w t q, speech.asserts w .g t q → ¬ (¬ speech.trueAt w q)) ∧
    (∀ w t q, ¬ VeracityBoundary.Counterfeit speech .g w t q) ∧
    (∀ w e, ¬ speech.shortcoming w .g e) := by finite_check

end JointFinite
