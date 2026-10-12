import Init

/-!
Independent structural controls. These certify semantic conditionals and a
precise failed implication, not a metaphysically possible perfected-original
universe or new warrant for original completion.
-/
namespace ActualProvisionReview

universe u v

inductive Path {A : Type u} (R : A → A → Prop) : A → A → Prop where
  | refl (a) : Path R a a
  | tail {a b c} : Path R a b → R b c → Path R a c

inductive StrictPath {A : Type u} (R : A → A → Prop) : A → A → Prop where
  | edge {a b} : R a b → StrictPath R a b
  | tail {a b c} : StrictPath R a b → R b c → StrictPath R a c

theorem StrictPath.toPath {A : Type u} {R : A → A → Prop} {a b}
    (h : StrictPath R a b) : Path R a b := by
  induction h with
  | edge e => exact Path.tail (Path.refl _) e
  | tail _ e ih => exact Path.tail ih e

theorem StrictPath.trans {A : Type u} {R : A → A → Prop} {a b c}
    (hab : StrictPath R a b) (hbc : StrictPath R b c) : StrictPath R a c := by
  induction hbc with
  | edge e => exact StrictPath.tail hab e
  | tail _ e ih => exact StrictPath.tail ih e

/-- Only selected route edges need certificates. A certificate may realise
an edge through multiple productive steps; it need not reclassify that edge
as a primitive efficient arrow. There is no global all-support-is-causal axiom. -/
inductive CertifiedRoute {A : Type u} (S P : A → A → Prop) : A → A → Prop where
  | edge {a b} : S a b → StrictPath P a b → CertifiedRoute S P a b
  | tail {a b c} : CertifiedRoute S P a b → S b c →
      StrictPath P b c → CertifiedRoute S P a c

theorem certified_route_is_support {A : Type u} {S P : A → A → Prop} {a b}
    (h : CertifiedRoute S P a b) : StrictPath S a b := by
  induction h with
  | edge s _ => exact StrictPath.edge s
  | tail _ s _ ih => exact StrictPath.tail ih s

theorem certified_route_is_productive {A : Type u} {S P : A → A → Prop} {a b}
    (h : CertifiedRoute S P a b) : StrictPath P a b := by
  induction h with
  | edge _ p => exact p
  | tail _ _ p ih => exact StrictPath.trans ih p

structure Bridge (R : Type u) (B : Type v) where
  actualResource : R → Prop
  receivedResource : R → Prop
  intrinsic : B → R → Prop
  actualBearer : B → Prop
  receivedBearer : B → Prop
  support : R → R → Prop
  productive : R → R → Prop

def OriginalResource {R : Type u} {B : Type v} (s : Bridge R B) (r : R) : Prop :=
  s.actualResource r ∧ ¬ s.receivedResource r

def OriginalBearer {R : Type u} {B : Type v} (s : Bridge R B) (g : B) : Prop :=
  s.actualBearer g ∧ ¬ s.receivedBearer g

def Realisation {R : Type u} {B : Type v} (s : Bridge R B) : Prop :=
  ∀ r, s.actualResource r → ∃ g, s.actualBearer g ∧ s.intrinsic g r

def ReceivedTransport {R : Type u} {B : Type v} (s : Bridge R B) : Prop :=
  ∀ g r, s.actualBearer g → s.intrinsic g r →
    s.receivedBearer g → s.receivedResource r

def Contributor {R : Type u} {B : Type v} (s : Bridge R B) (g : B) (t : R) : Prop :=
  ∃ r, s.intrinsic g r ∧ StrictPath s.productive r t

/-- The resource r is fixed outside the existential bearer conclusion.
No independently existing original producer can replace its bearer. -/
theorem same_resource_same_bearer_transfer {R : Type u} {B : Type v}
    (s : Bridge R B) (r t : R) (original : OriginalResource s r)
    (realise : Realisation s) (transport : ReceivedTransport s)
    (route : CertifiedRoute s.support s.productive r t) :
    ∃ g, s.intrinsic g r ∧ OriginalBearer s g ∧
      (∃ r', r' = r ∧ s.intrinsic g r' ∧ StrictPath s.productive r' t) := by
  obtain ⟨g, hg, hgr⟩ := realise r original.1
  refine ⟨g, hgr, ⟨hg, ?_⟩, r, rfl, hgr, certified_route_is_productive route⟩
  intro received
  exact original.2 (transport g r hg hgr received)

inductive Resource where
  | gStock | hPower | kStock | target | side
  deriving DecidableEq
inductive Bearer where
  | g | h | k | targetOwner | sideOwner
  deriving DecidableEq
inductive Rule where
  | grounding | targetProduction | sideProduction
  deriving DecidableEq
open Resource Bearer Rule

def owner : Resource → Bearer
  | gStock => g
  | hPower => h
  | kStock => k
  | target => targetOwner
  | side => sideOwner

def original (r : Resource) : Prop := r = gStock ∨ r = kStock

def needs : Rule → Resource → Prop
  | grounding, r => r = gStock
  | targetProduction, r => r = hPower ∨ r = kStock
  | sideProduction, r => r = gStock

def output : Rule → Resource
  | grounding => hPower
  | targetProduction => target
  | sideProduction => side

def Used (_ : Rule) : Prop := True

def Support (a b : Resource) : Prop := ∃ i, Used i ∧ needs i a ∧ output i = b

def Producing (i : Rule) : Prop := i = targetProduction ∨ i = sideProduction

def Productive (a b : Resource) : Prop :=
  ∃ i, Used i ∧ Producing i ∧ needs i a ∧ output i = b

inductive Generated : Resource → Prop where
  | seed {r} : original r → Generated r
  | rule (i) : Used i → (∀ p, needs i p → Generated p) → Generated (output i)

def actual (_ : Resource) : Prop := True

def control : Bridge Resource Bearer where
  actualResource := actual
  receivedResource := fun r => ¬ original r
  intrinsic := fun b r => b = owner r
  actualBearer := fun _ => True
  receivedBearer := fun b => b ≠ g ∧ b ≠ k
  support := Support
  productive := Productive

theorem all_rules_used_and_sound :
    ∀ i, Used i ∧ actual (output i) ∧ (∀ p, needs i p → actual p) := by
  intro i; exact ⟨trivial, trivial, fun _ _ => trivial⟩

theorem no_empty_rules : ∀ i, ∃ p, needs i p := by
  intro i; cases i with
  | grounding => exact ⟨gStock, rfl⟩
  | targetProduction => exact ⟨hPower, Or.inl rfl⟩
  | sideProduction => exact ⟨gStock, rfl⟩

theorem all_resources_generated : ∀ r, Generated r := by
  have hg : Generated gStock := Generated.seed (Or.inl rfl)
  have hk : Generated kStock := Generated.seed (Or.inr rfl)
  have hh : Generated hPower := Generated.rule grounding trivial (by
    intro p hp; change p = gStock at hp; subst p; exact hg)
  intro r; cases r with
  | gStock => exact hg
  | kStock => exact hk
  | hPower => exact hh
  | target =>
    exact Generated.rule targetProduction trivial (by
      intro p hp; rcases hp with hp | hp <;> subst p
      · exact hh
      · exact hk)
  | side =>
    exact Generated.rule sideProduction trivial (by
      intro p hp; change p = gStock at hp; subst p; exact hg)

theorem actual_local_equation (r : Resource) :
    actual r ↔ original r ∨ ∃ i, Used i ∧ output i = r ∧
      ∀ p, needs i p → actual p := by
  constructor
  · intro _; cases r with
    | gStock => exact Or.inl (Or.inl rfl)
    | kStock => exact Or.inl (Or.inr rfl)
    | hPower => exact Or.inr ⟨grounding, trivial, rfl, fun _ _ => trivial⟩
    | target => exact Or.inr ⟨targetProduction, trivial, rfl, fun _ _ => trivial⟩
    | side => exact Or.inr ⟨sideProduction, trivial, rfl, fun _ _ => trivial⟩
  · intro _; trivial

theorem originals_receive_no_support (r : Resource) (hr : original r) :
    ¬ ∃ a, Support a r := by
  intro h; obtain ⟨a, i, _, _, hi⟩ := h
  rcases hr with hr | hr <;> subst r <;> cases i <;> simp_all [output]

def rank : Resource → Nat
  | gStock => 0
  | kStock => 0
  | hPower => 1
  | side => 1
  | target => 2

theorem support_increases_rank {a b} (h : Support a b) : rank a < rank b := by
  obtain ⟨i, _, ha, hb⟩ := h
  cases i <;> cases a <;> cases b <;> simp_all [needs, output, rank]

theorem support_path_increases_rank {a b} (h : StrictPath Support a b) : rank a < rank b := by
  induction h with
  | edge h => exact support_increases_rank h
  | tail _ e ih => exact Nat.lt_trans ih (support_increases_rank e)

theorem support_acyclic (r : Resource) : ¬ StrictPath Support r r := by
  intro h; exact Nat.lt_irrefl _ (support_path_increases_rank h)

theorem control_realisation : Realisation control := by
  intro r _; exact ⟨owner r, trivial, rfl⟩

theorem control_received_transport : ReceivedTransport control := by
  intro b r _ hi hb
  change b = owner r at hi
  subst b
  change ¬ original r
  intro ho
  rcases ho with ho | ho <;> subst r
  · exact hb.1 rfl
  · exact hb.2 rfl

theorem g_original_resource : OriginalResource control gStock :=
  ⟨trivial, fun h => h (Or.inl rfl)⟩

theorem g_same_original_bearer : control.intrinsic g gStock ∧ OriginalBearer control g := by
  exact ⟨rfl, trivial, fun h => h.1 rfl⟩

theorem g_strict_live_support_to_target : StrictPath Support gStock target := by
  have h : StrictPath Support gStock hPower :=
    StrictPath.edge ⟨grounding, trivial, rfl, rfl⟩
  exact StrictPath.tail h ⟨targetProduction, trivial, Or.inl rfl, rfl⟩

theorem g_actually_produces_side : Productive gStock side :=
  ⟨sideProduction, trivial, Or.inr rfl, rfl, rfl⟩

theorem k_actually_contributes_target : Contributor control k target := by
  exact ⟨kStock, rfl, StrictPath.edge
    ⟨targetProduction, trivial, Or.inl rfl, Or.inr rfl, rfl⟩⟩

theorem g_productive_path_restricted {r} (h : Path Productive gStock r) :
    r = gStock ∨ r = side := by
  induction h with
  | refl => exact Or.inl rfl
  | @tail b c _ e ih =>
    obtain ⟨i, _, hi, hn, ho⟩ := e
    rcases ih with ih | ih <;> subst b <;>
      cases i <;> simp_all [Producing, needs, output]

theorem g_has_no_productive_path_to_target : ¬ StrictPath Productive gStock target := by
  intro h
  rcases g_productive_path_restricted h.toPath with h | h <;> cases h

theorem g_is_target_noncontributor : ¬ Contributor control g target := by
  intro h; obtain ⟨r, hr, hp⟩ := h
  change g = owner r at hr
  cases r <;> simp_all [owner]
  exact g_has_no_productive_path_to_target hp

/-- Stronger than the previous capable-but-idle control: G actually produces
side; an actual original K produces into target; all selected support is live,
acyclic, least-generated, and original seeds receive no actual support. -/
theorem nonidle_same_witness_obstruction :
    OriginalResource control gStock ∧
    control.intrinsic g gStock ∧ OriginalBearer control g ∧
    StrictPath control.support gStock target ∧
    (∃ t, Contributor control g t) ∧
    (∃ b, OriginalBearer control b ∧ Contributor control b target) ∧
    ¬ Contributor control g target := by
  refine ⟨g_original_resource, g_same_original_bearer.1,
    g_same_original_bearer.2, g_strict_live_support_to_target,
    ⟨side, gStock, rfl, StrictPath.edge g_actually_produces_side⟩,
    ⟨k, ⟨trivial, fun h => h.2 rfl⟩, k_actually_contributes_target⟩,
    g_is_target_noncontributor⟩

theorem target_route_certificate_fails_for_g :
    ¬ CertifiedRoute Support Productive gStock target := by
  intro h; exact g_has_no_productive_path_to_target (certified_route_is_productive h)

/-- Positive nonvacuity: exactly the same bridge succeeds on K's actual route. -/
theorem target_route_certificate_succeeds_for_k :
    CertifiedRoute Support Productive kStock target := by
  exact CertifiedRoute.edge ⟨targetProduction, trivial, Or.inr rfl, rfl⟩
    (StrictPath.edge ⟨targetProduction, trivial, Or.inl rfl, Or.inr rfl, rfl⟩)

end ActualProvisionReview
