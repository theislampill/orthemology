import AnchoredSourceBridge
set_option linter.constructorNameAsVariable false
set_option synthInstance.maxSize 100000
set_option maxRecDepth 10000
set_option maxHeartbeats 2000000
namespace AnchoredSourceBridge.Controls

inductive S | g | h | j deriving DecidableEq, Repr
inductive E | e | f | k | z deriving DecidableEq, Repr
inductive C | a | b | d deriving DecidableEq, Repr
inductive Agent | left | right deriving DecidableEq, Repr
inductive Token | u | v deriving DecidableEq, Repr

instance sourceForall (p : S → Prop) [DecidablePred p] : Decidable (∀ s, p s) :=
  decidable_of_iff (p .g ∧ p .h ∧ p .j) ⟨
    fun h s => by cases s; exact h.1; exact h.2.1; exact h.2.2,
    fun h => ⟨h _, h _, h _⟩⟩
instance sourceExists (p : S → Prop) [DecidablePred p] : Decidable (∃ s, p s) :=
  decidable_of_iff (p .g ∨ p .h ∨ p .j) ⟨
    fun h => by cases h with | inl h => exact ⟨.g, h⟩ | inr h => cases h with | inl h => exact ⟨.h, h⟩ | inr h => exact ⟨.j, h⟩,
    fun ⟨s, h⟩ => by cases s; exact Or.inl h; exact Or.inr (Or.inl h); exact Or.inr (Or.inr h)⟩
instance occurrenceForall (p : E → Prop) [DecidablePred p] : Decidable (∀ e, p e) :=
  decidable_of_iff (p .e ∧ p .f ∧ p .k ∧ p .z) ⟨
    fun h e => by cases e; exact h.1; exact h.2.1; exact h.2.2.1; exact h.2.2.2,
    fun h => ⟨h _, h _, h _, h _⟩⟩
instance occurrenceExists (p : E → Prop) [DecidablePred p] : Decidable (∃ e, p e) :=
  decidable_of_iff (p .e ∨ p .f ∨ p .k ∨ p .z) ⟨
    fun h => by cases h with | inl h => exact ⟨.e, h⟩ | inr h => cases h with | inl h => exact ⟨.f, h⟩ | inr h => cases h with | inl h => exact ⟨.k, h⟩ | inr h => exact ⟨.z, h⟩,
    fun ⟨e, h⟩ => by cases e; exact Or.inl h; exact Or.inr (Or.inl h); exact Or.inr (Or.inr (Or.inl h)); exact Or.inr (Or.inr (Or.inr h))⟩
instance contributionForall (p : C → Prop) [DecidablePred p] : Decidable (∀ c, p c) :=
  decidable_of_iff (p .a ∧ p .b ∧ p .d) ⟨
    fun h c => by cases c; exact h.1; exact h.2.1; exact h.2.2,
    fun h => ⟨h _, h _, h _⟩⟩
instance contributionExists (p : C → Prop) [DecidablePred p] : Decidable (∃ c, p c) :=
  decidable_of_iff (p .a ∨ p .b ∨ p .d) ⟨
    fun h => by cases h with | inl h => exact ⟨.a, h⟩ | inr h => cases h with | inl h => exact ⟨.b, h⟩ | inr h => exact ⟨.d, h⟩,
    fun ⟨c, h⟩ => by cases c; exact Or.inl h; exact Or.inr (Or.inl h); exact Or.inr (Or.inr h)⟩

-- All primitive relations have independent finite truth tables. In ordinary
-- fixtures ActualOriginal/ModeRole are explicitly chosen to coincide with
-- witnessed actual use; deletions vary them independently.
def tableRep (req : E → C → Prop) (entire : S → C → Prop) (s : S) (e : E) : Prop :=
  ∃ c, req e c ∧ entire s c

def fixture (field : E → Prop) (req : E → C → Prop) (entire : S → C → Prop)
    (actual : S → E → Prop) (role : S → E → Prop) (defect : S → E → Prop) : Account S E C where
  Field := field
  ActualOccurrence := fun _ => True
  Req := req
  Operative := req
  EntireOrig := entire
  ActualOriginal := actual
  ModeRole := role
  Qualified := fun s => s = .g
  ModeDefect := defect

def faithful (field : E → Prop) (req : E → C → Prop) (entire : S → C → Prop)
    (defect : S → E → Prop := fun _ _ => False) : Account S E C :=
  fixture field req entire (tableRep req entire) (tableRep req entire) defect

def singleton : E → Prop := fun e => e = .e
def pairField : E → Prop := fun e => e = .e ∨ e = .f
def mixedField : E → Prop := fun e => e ≠ .z

def splitReq : E → C → Prop := fun e c => e = .e ∧ (c = .a ∨ c = .b)
def splitEntire : S → C → Prop := fun s c => (s = .g ∧ c = .a) ∨ (s = .h ∧ c = .b)
def split : Account S E C := faithful singleton splitReq splitEntire

-- Before richer fixtures, kernel checks that finite quantifier instances work.
theorem finite_quantifiers : (∀ s : S, s = .g ∨ s = .h ∨ s = .j) ∧
    (∃ c : C, c = .a) := by decide

theorem split_signature : CND split ∧ ¬ GlobalCoverage split .g := by
  simp only [CND, GlobalCoverage, Complete, split, faithful, fixture, singleton, splitReq, splitEntire]
  decide


def oneReq : E → C → Prop := fun e c => e = .e ∧ c = .a
def duplicateEntire : S → C → Prop := fun s c => (s = .g ∨ s = .h) ∧ c = .a
def duplicate : Account S E C := faithful singleton oneReq duplicateEntire

def unanchoredEntire : S → C → Prop := fun s c => (s = .h ∧ c = .a) ∨ (s = .j ∧ c = .b)
def unanchored : Account S E C := faithful singleton splitReq unanchoredEntire

def separateReq : E → C → Prop := fun e c => (e = .e ∧ c = .a) ∨ (e = .f ∧ c = .b)
def separated : Account S E C := faithful pairField separateReq splitEntire

def chainReq : E → C → Prop := fun e c => (e = .e ∧ c = .a) ∨ (e = .f ∧ (c = .a ∨ c = .b))
def shortRole : S → E → Prop := fun s e => (s = .g ∧ e = .e) ∨ (s = .h ∧ e = .f)
def missingUse : Account S E C := fixture pairField chainReq splitEntire shortRole shortRole (fun _ _ => False)
def missingRole : Account S E C := fixture pairField chainReq splitEntire (tableRep chainReq splitEntire) shortRole (fun _ _ => False)

def onlyG : S → C → Prop := fun s c => s = .g ∧ c = .a
def hiddenActual : S → E → Prop := fun s e => (s = .g ∨ s = .h) ∧ e = .e
def hidden : Account S E C := fixture singleton oneReq onlyG hiddenActual (tableRep oneReq onlyG) (fun _ _ => False)

def mixedReq : E → C → Prop := fun e c =>
  (e = .e ∧ c = .a) ∨ (e = .f ∧ c = .b) ∨ (e = .k ∧ (c = .a ∨ c = .b)) ∨ (e = .z ∧ c = .d)
def fullEntire : S → C → Prop := fun s c => (s = .g ∧ (c = .a ∨ c = .b)) ∨ (s = .h ∧ c = .d)
def full : Account S E C := faithful mixedField mixedReq fullEntire

def outsideDuplicateEntire : S → C → Prop := fun s c =>
  (s = .g ∧ (c = .a ∨ c = .b)) ∨ ((s = .h ∨ s = .j) ∧ c = .d)
def outsideDuplicate : Account S E C := faithful mixedField mixedReq outsideDuplicateEntire

def mixedAdverse : Account S E C := faithful mixedField mixedReq splitEntire

def aggregate : Account S E C := { mixedAdverse with ActualOccurrence := pairField, Operative := separateReq }

def defectiveSplit : Account S E C := faithful singleton splitReq splitEntire (fun s e => s = .g ∧ e = .e)

def emptyActual : S → E → Prop := fun s e => s = .g ∧ e = .e
def emptyInventory : Account S E C := fixture singleton (fun _ _ => False) (fun _ _ => False)
  emptyActual emptyActual (fun _ _ => False)

/-- Standing ability and modal predicates do not constrain actual provision. -/
def StandingCan (_ : S) (_ : E) : Prop := True
def Necessary (_ : S) : Prop := True

def EndpointSufficient (s : S) (e : E) : Prop := s = .g ∧ e = .e

def DerivedAct (a : Agent) (e : E) : Prop :=
  (a = .left ∧ (e = .e ∨ e = .k)) ∨ (a = .right ∧ (e = .f ∨ e = .k))
def SourceOwns (s : S) (t : Token) : Prop := s = .g ∧ t = .u
def DerivedOwns (a : Agent) (t : Token) : Prop := a = .left ∧ t = .v
def TrueContent (t : Token) : Prop := t = .u
def TokenOccurrence : Token → E | .u => .e | .v => .k
def ProvidesToken (s : S) (t : Token) : Prop := full.ActualOriginal s (TokenOccurrence t)
def Authenticated (_ : Token) : Prop := False

/-- These record actual capacity use by the distinct derived agents. The shared
c is the earlier input contribution/respect retained in a later account, not
an identification of the earlier production with the transformed output. -/
def DerivedUses (a : Agent) (e : E) (c : C) : Prop :=
  (a = .left ∧ (e = .e ∨ e = .k) ∧ c = .a) ∨
  (a = .right ∧ (e = .f ∨ e = .k) ∧ c = .b)
def MediateUse (earlier later : E) (c : C) : Prop :=
  (earlier = .e ∧ later = .k ∧ c = .a) ∨
  (earlier = .f ∧ later = .k ∧ c = .b)

instance agentForall (p : Agent → Prop) [DecidablePred p] : Decidable (∀ a, p a) :=
  decidable_of_iff (p .left ∧ p .right) ⟨fun h a => by cases a; exact h.1; exact h.2, fun h => ⟨h _, h _⟩⟩

instance tokenForall (p : Token → Prop) [DecidablePred p] : Decidable (∀ t, p t) :=
  decidable_of_iff (p .u ∧ p .v) ⟨fun h t => by cases t; exact h.1; exact h.2, fun h => ⟨h _, h _⟩⟩

def Interpretation (A : Account S E C) : Prop :=
  Admissible A ∧ RequisiteSound A ∧ RequisiteExhaustive A ∧ UseSound A ∧ Visible A

def FixedMode (A : Account S E C) : Prop :=
  A.Qualified .g ∧ Classification A .g ∧ Conformance A .g ∧ RoleApplicable A .g

macro "finite_check" : tactic => `(tactic| (simp only [Admissible, RequisiteSound, RequisiteExhaustive, UseSound, RoleApplicable, Visible, Classification, Conformance, ModeSatisfaction, SourceMode, CND, FieldCND, GlobalCoverage, ActualAnchor, ActualUnique, Positive, Complete, RepresentedParticipation, Overlap, tableRep, fixture, faithful, singleton, pairField, mixedField, splitReq, splitEntire, split, oneReq, duplicateEntire, duplicate, unanchoredEntire, unanchored, separateReq, separated, chainReq, shortRole, missingUse, missingRole, onlyG, hiddenActual, hidden, mixedReq, fullEntire, full, outsideDuplicateEntire, outsideDuplicate, mixedAdverse, aggregate, defectiveSplit, emptyActual, emptyInventory, StandingCan, Necessary, EndpointSufficient, DerivedAct, SourceOwns, DerivedOwns, TrueContent, TokenOccurrence, ProvidesToken, Authenticated, DerivedUses, MediateUse, Interpretation, FixedMode] <;> decide))


/-- One-field path witnesses contain no invented causal edge. -/
theorem singleton_connected (A : Account S E C)
    (field : ∀ e, A.Field e ↔ e = .e) : ConnectedFrom A .e := by
  intro e he
  have eq := (field e).1 he
  subst e
  exact Path.refl he

/-- A concrete mixed occurrence can connect disjoint upstream branches. -/
theorem hub_connected (A : Account S E C) (a k : E)
    (fa : A.Field a) (fk : A.Field k) (edge : Overlap A a k)
    (hub : ∀ e, A.Field e → e = a ∨ Overlap A k e) : ConnectedFrom A a := by
  intro e fe
  cases hub e fe with
  | inl eq => subst e; exact Path.refl fa
  | inr overlap => exact Path.step fa fk edge (Path.step fk fe overlap (Path.refl fe))

theorem split_connected : ConnectedFrom split .e :=
  singleton_connected split (by finite_check)
theorem duplicate_connected : ConnectedFrom duplicate .e :=
  singleton_connected duplicate (by finite_check)
theorem unanchored_connected : ConnectedFrom unanchored .e :=
  singleton_connected unanchored (by finite_check)
theorem hidden_connected : ConnectedFrom hidden .e :=
  singleton_connected hidden (by finite_check)
theorem defective_connected : ConnectedFrom defectiveSplit .e :=
  singleton_connected defectiveSplit (by finite_check)
theorem empty_connected : ConnectedFrom emptyInventory .e :=
  singleton_connected emptyInventory (by finite_check)
theorem missing_use_connected : ConnectedFrom missingUse .e :=
  hub_connected missingUse .e .f (by finite_check) (by finite_check) (by finite_check) (by finite_check)
theorem missing_role_connected : ConnectedFrom missingRole .e :=
  hub_connected missingRole .e .f (by finite_check) (by finite_check) (by finite_check) (by finite_check)
theorem full_connected : ConnectedFrom full .e :=
  hub_connected full .e .k (by finite_check) (by finite_check) (by finite_check) (by finite_check)
theorem outside_duplicate_connected : ConnectedFrom outsideDuplicate .e :=
  hub_connected outsideDuplicate .e .k (by finite_check) (by finite_check) (by finite_check) (by finite_check)
theorem adverse_connected : ConnectedFrom mixedAdverse .e :=
  hub_connected mixedAdverse .e .k (by finite_check) (by finite_check) (by finite_check) (by finite_check)
theorem aggregate_connected : ConnectedFrom aggregate .e :=
  hub_connected aggregate .e .k (by finite_check) (by finite_check) (by finite_check) (by finite_check)

/-- Control 1: differentiated voluntary partial provision, CND, unrestricted
standing capacities; the additional actual source-mode implication fails. -/
theorem missing_source_mode : Interpretation split ∧ CND split ∧ ActualAnchor split .g .e ∧
    split.Qualified .g ∧ RoleApplicable split .g ∧
    (∀ s e, StandingCan s e) ∧ ¬ ModeSatisfaction split .g ∧
    ¬ SourceMode split .g ∧ ¬ (∃ s, GlobalCoverage split s) := by finite_check

/-- Control 2: double entire provision is expressible before CND. -/
theorem missing_cnd : Interpretation duplicate ∧ FixedMode duplicate ∧
    ActualAnchor duplicate .g .e ∧ GlobalCoverage duplicate .g ∧
    duplicate.EntireOrig .g .a ∧ duplicate.EntireOrig .h .a ∧
    ¬ CND duplicate ∧ ¬ ActualUnique duplicate .g ∧
    GlobalCoverage duplicate .h := by finite_check

/-- Control 3: qualification and a vacuous mode condition do not create an act. -/
theorem missing_anchor : Interpretation unanchored ∧ FixedMode unanchored ∧ CND unanchored ∧
    SourceMode unanchored .g ∧ ¬ ActualAnchor unanchored .g .e ∧
    ¬ (∃ s, GlobalCoverage unanchored s) := by finite_check

/-- Endpoint-completeness is enough to make a represented g act become e. -/
theorem separated_complete_only_at_e : ∀ o, separated.Field o → Complete separated .g o → o = .e := by finite_check

/-- Control 4 connectivity is actually false, proved without deciding Paths. -/
theorem separated_not_connected : ¬ ConnectedFrom separated .e := by
  intro connected
  have coverage := global_coverage_of_anchor separated .g .e
    (by finite_check) (by finite_check) (by finite_check) (by finite_check) connected
  have incomplete : ¬ Complete separated .g .f := by finite_check
  exact incomplete (coverage .f (by finite_check))

theorem missing_connectedness : Interpretation separated ∧ FixedMode separated ∧ CND separated ∧
    ActualAnchor separated .g .e ∧ ¬ (∃ s, GlobalCoverage separated s) := by finite_check

/-- Control 5: universal unrelated adjacency does not supply productive overlap. -/
def UnrelatedGraph (_ _ : E) : Prop := True

theorem arbitrary_graph_not_faithful : (∀ e f, UnrelatedGraph e f) ∧
    ¬ Overlap separated .e .f ∧ ¬ GlobalCoverage separated .g := by
  simp only [UnrelatedGraph]
  finite_check

/-- Control 6a: represented historical use is denied actual status only at f. -/
theorem missing_original_use : Admissible missingUse ∧ RequisiteSound missingUse ∧
    RequisiteExhaustive missingUse ∧ Visible missingUse ∧ FixedMode missingUse ∧ CND missingUse ∧
    ActualAnchor missingUse .g .e ∧ ¬ UseSound missingUse ∧
    RepresentedParticipation missingUse .g .f ∧ ¬ missingUse.ActualOriginal .g .f ∧
    ¬ GlobalCoverage missingUse .g := by finite_check

/-- Control 6b: actual contribution at f is denied mode-governed role status. -/
theorem missing_mode_role : Interpretation missingRole ∧ missingRole.Qualified .g ∧
    Classification missingRole .g ∧ Conformance missingRole .g ∧ CND missingRole ∧
    ActualAnchor missingRole .g .e ∧ ¬ RoleApplicable missingRole .g ∧
    missingRole.ActualOriginal .g .f ∧ ¬ missingRole.ModeRole .g .f ∧
    ¬ GlobalCoverage missingRole .g := by finite_check

/-- Control 7: represented-rival exclusion survives; omitted actual h survives too. -/
theorem missing_visibility : Admissible hidden ∧ RequisiteSound hidden ∧ RequisiteExhaustive hidden ∧
    UseSound hidden ∧ FixedMode hidden ∧ CND hidden ∧ ActualAnchor hidden .g .e ∧
    GlobalCoverage hidden .g ∧ (∀ s e, hidden.Field e → RepresentedParticipation hidden s e → s = .g) ∧
    ¬ Visible hidden ∧ hidden.ActualOriginal .h .e ∧ ¬ ActualUnique hidden .g := by finite_check

/-- Control 8: endpoint sufficiency tolerates additional original work. -/
theorem coarse_effect_not_full_account : EndpointSufficient .g .e ∧
    CND split ∧ split.Qualified .g ∧ ¬ split.Qualified .h ∧
    split.ActualOriginal .h .e ∧ ¬ Complete split .g .e := by finite_check

/-- Control 9: distinct actual upstream accounts need a real mixed occurrence. -/
theorem mixed_occurrence_positive : Interpretation full ∧ FixedMode full ∧ CND full ∧
    ActualAnchor full .g .e ∧ GlobalCoverage full .g ∧
    ¬ Overlap full .e .f ∧ Overlap full .e .k ∧ Overlap full .k .f ∧
    DerivedAct .left .e ∧ DerivedAct .right .f ∧ Agent.left ≠ Agent.right ∧
    ¬ DerivedAct .left .f ∧ ¬ DerivedAct .right .e := by finite_check

theorem mixed_occurrence_adverse : Interpretation mixedAdverse ∧ CND mixedAdverse ∧
    ActualAnchor mixedAdverse .g .e ∧ ¬ Complete mixedAdverse .g .k ∧
    ¬ SourceMode mixedAdverse .g ∧ ¬ Classification mixedAdverse .g := by finite_check


/-- The full model explicitly links genuine differentiated proximal actions to
actual used resources and forward mediation. Undirected graph traversal does
not reverse either MediateUse edge. -/
theorem faithful_derived_agency_and_mediation :
    (∀ a e c, DerivedUses a e c → DerivedAct a e ∧ full.Req e c) ∧
    DerivedUses .left .e .a ∧ DerivedUses .left .k .a ∧
    DerivedUses .right .f .b ∧ DerivedUses .right .k .b ∧
    MediateUse .e .k .a ∧ MediateUse .f .k .b ∧
    ¬ MediateUse .k .e .a ∧ ¬ MediateUse .k .f .b ∧
    (∀ e f c, MediateUse e f c → full.Req e c ∧ full.Req f c) ∧
    full.ActualOriginal .g .k ∧ S.g ≠ S.h := by finite_check

/-- Control 10: field-unique original g coexists with an actual outside-field h. -/
theorem outside_field_necessary_original : Interpretation full ∧ FixedMode full ∧ CND full ∧
    GlobalCoverage full .g ∧ ActualUnique full .g ∧
    Necessary .g ∧ Necessary .h ∧ S.g ≠ S.h ∧
    ¬ full.Field .z ∧ full.ActualOriginal .h .z ∧ ¬ Complete full .g .z := by finite_check

/-- Control 11: original causal provision of the false derived token v does not
confer source assertion ownership, truth of v, or authentication. -/
theorem assertion_ownership_separate : GlobalCoverage full .g ∧ ProvidesToken .g .v ∧
    DerivedAct .left .k ∧ DerivedOwns .left .v ∧ ¬ TrueContent .v ∧
    ¬ SourceOwns .g .v ∧ (∀ t, SourceOwns .g t → TrueContent t) ∧
    SourceOwns .g .u ∧ TrueContent .u ∧ ¬ Authenticated .v := by finite_check

/-- Control 12: invented aggregate membership fails independently specified
occurrence admissibility and actual-operative soundness. -/
theorem arbitrary_bundle_rejected : aggregate.Field .k ∧ ¬ aggregate.ActualOccurrence .k ∧
    ¬ Admissible aggregate ∧ ¬ RequisiteSound aggregate ∧
    Overlap aggregate .e .k ∧ Overlap aggregate .k .f ∧
    ¬ SourceMode aggregate .g := by finite_check

/-- Control 13a: classification is omitted while actual defect-free conformance
and all standing capacities remain. Completeness still fails. -/
theorem missing_classification : Interpretation split ∧ CND split ∧ ActualAnchor split .g .e ∧
    split.Qualified .g ∧ RoleApplicable split .g ∧ Conformance split .g ∧
    ¬ Classification split .g ∧ ¬ split.ModeDefect .g .e ∧
    (∀ s e, StandingCan s e) ∧ ¬ GlobalCoverage split .g := by finite_check

/-- Control 13b: the norm and defect classification hold, but its actual
conformance is omitted. An ought does not by itself provide an actual fact. -/
theorem missing_conformance : Interpretation defectiveSplit ∧ CND defectiveSplit ∧
    ActualAnchor defectiveSplit .g .e ∧ defectiveSplit.Qualified .g ∧ RoleApplicable defectiveSplit .g ∧
    Classification defectiveSplit .g ∧ ¬ Conformance defectiveSplit .g ∧
    defectiveSplit.ModeDefect .g .e ∧ (∀ s e, StandingCan s e) ∧
    ¬ GlobalCoverage defectiveSplit .g := by finite_check

/-- Extra guard: an empty inventory labels everyone Complete. The arbitrary
actual anchor cannot create positivity without its visibility bridge. -/
theorem empty_inventory_singleton : Admissible emptyInventory ∧ RequisiteSound emptyInventory ∧
    RequisiteExhaustive emptyInventory ∧ UseSound emptyInventory ∧ FixedMode emptyInventory ∧
    CND emptyInventory ∧ ActualAnchor emptyInventory .g .e ∧
    GlobalCoverage emptyInventory .g ∧ GlobalCoverage emptyInventory .h ∧
    ¬ Positive emptyInventory .e ∧ ¬ Visible emptyInventory ∧
    ActualUnique emptyInventory .g ∧ S.g ≠ S.h := by finite_check

/-- Full inhabited model verifies every premise, a real anchor, disjoint genuine
derived agency, mixed propagation, field-rival exclusion and provider uniqueness. -/
theorem full_nonvacuous_model :
    Interpretation full ∧ FixedMode full ∧ CND full ∧ ActualAnchor full .g .e ∧
    ConnectedFrom full .e ∧ GlobalCoverage full .g ∧ ActualUnique full .g ∧
    (∀ e, full.Field e → Positive full e) ∧
    (∀ e, full.Field e → ∀ s, Complete full s e → s = .g) ∧
    DerivedAct .left .e ∧ DerivedAct .right .f ∧ Agent.left ≠ Agent.right := by
  refine ⟨by finite_check, by finite_check, by finite_check, by finite_check, full_connected, ?_⟩
  finite_check


/-- Stronger global nonduplication is unnecessary: only the outside contribution
d has two entire original providers; every field-scoped conclusion still holds. -/
theorem outside_duplication_preserves_field_uniqueness :
    Interpretation outsideDuplicate ∧ FixedMode outsideDuplicate ∧ FieldCND outsideDuplicate ∧
    ActualAnchor outsideDuplicate .g .e ∧ ConnectedFrom outsideDuplicate .e ∧
    ¬ CND outsideDuplicate ∧ outsideDuplicate.EntireOrig .h .d ∧ outsideDuplicate.EntireOrig .j .d ∧
    S.h ≠ S.j ∧ ¬ outsideDuplicate.Field .z ∧
    outsideDuplicate.ActualOriginal .h .z ∧ outsideDuplicate.ActualOriginal .j .z ∧
    GlobalCoverage outsideDuplicate .g ∧ ActualUnique outsideDuplicate .g ∧
    (∀ e, outsideDuplicate.Field e → ∀ s, Complete outsideDuplicate s e → s = .g) := by
  refine ⟨by finite_check, by finite_check, by finite_check, by finite_check, outside_duplicate_connected, ?_⟩
  finite_check

/-- The weaker principal theorem actually applies to the outside-duplication
model even though its global-CND wrapper cannot apply. -/
theorem principal_application_with_outside_duplication :
    GlobalCoverage outsideDuplicate .g ∧ ActualUnique outsideDuplicate .g ∧
    (∀ e, outsideDuplicate.Field e → ∀ s, Complete outsideDuplicate s e → s = .g) := by
  have result := guarded_common_original_provider outsideDuplicate .g .e
    (by finite_check) (by finite_check) (by finite_check) (by finite_check)
    (by finite_check) (by finite_check) (by finite_check) (by finite_check) (by finite_check)
    (by finite_check) outside_duplicate_connected (by finite_check)
  exact result.2.2.2
end AnchoredSourceBridge.Controls
