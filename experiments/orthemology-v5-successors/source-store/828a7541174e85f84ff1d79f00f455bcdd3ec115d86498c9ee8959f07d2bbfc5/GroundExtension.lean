import Init

/-!
Uniform addition of a nonproductive ground above the actual original roots.
Only direct support/grounding arrows are encoded here. `Path` supplies reflexive
ancestry; `Acyclic` excludes a direct edge followed by a return path.
The construction is a structural model theorem, not a metaphysical assertion.
-/

namespace T20.GroundExtension

universe u v z

inductive Path {A : Type u} (R : A → A → Prop) : A → A → Prop where
  | refl (a : A) : Path R a a
  | tail {a b c : A} : Path R a b → R b c → Path R a c

def Acyclic {A : Type u} (R : A → A → Prop) : Prop :=
  ∀ a b, R a b → ¬ Path R b a

/-- `none` is the new ground; it has no incoming arrows. -/
def addRoot {A : Type u} (R : A → A → Prop) (B : A → Prop) :
    Option A → Option A → Prop
  | none, none => False
  | none, some b => B b
  | some _, none => False
  | some a, some b => R a b

def liftExist {W : Type v} {A : Type u} (E : W → A → Prop) :
    W → Option A → Prop
  | _, none => True
  | w, some a => E w a

def liftHolder {A : Type u} (H : A → Prop) : Option A → Prop
  | none => False
  | some a => H a

/-- The new ground's standing capacity is separate from its productive edges. -/
def liftHolderWith {A : Type u} (Q : Prop) (H : A → Prop) : Option A → Prop
  | none => Q
  | some a => H a

def liftProductive {W : Type v} {A : Type u} (P : W → A → A → Prop)
    (w : W) : Option A → Option A → Prop :=
  addRoot (P w) (fun _ => False)

theorem old_productive_iff {W : Type v} {A : Type u}
    (P : W → A → A → Prop) (w : W) (a b : A) :
    liftProductive P w (some a) (some b) ↔ P w a b := Iff.rfl

theorem new_has_no_production {W : Type v} {A : Type u}
    (P : W → A → A → Prop) (w : W) (a : Option A) :
    ¬ liftProductive P w none a ∧ ¬ liftProductive P w a none := by
  cases a <;> exact ⟨fun h => h, fun h => h⟩

/-- Genuine productive agents retain their possessed powers in either variant. -/
theorem productive_power_preserved {W : Type v} {A : Type u}
    (P : W → A → A → Prop) (H : A → Prop) (Q : Prop)
    (hp : ∀ w a b, P w a b → H a) :
    ∀ w a b, liftProductive P w a b → liftHolderWith Q H a := by
  intro w a b h
  cases a with
  | none =>
    cases b <;> exact False.elim h
  | some a =>
    cases b with
    | none => exact False.elim h
    | some b => exact hp w a b h

/-- A relation on old profile arguments, with no hidden full-domain quantifier. -/
def liftProfile {W : Type v} {A : Type u} {I : Type z}
    (F : W → (I → A) → Prop) (w : W) (xs : I → Option A) : Prop :=
  ∃ ys : I → A, xs = (fun i => some (ys i)) ∧ F w ys

theorem old_profile_iff {W : Type v} {A : Type u} {I : Type z}
    (F : W → (I → A) → Prop) (w : W) (xs : I → A) :
    liftProfile F w (fun i => some (xs i)) ↔ F w xs := by
  constructor
  · intro h
    obtain ⟨ys, heq, hf⟩ := h
    have hxy : xs = ys := funext (fun i => Option.some.inj (congrFun heq i))
    exact hxy ▸ hf
  · intro hf
    exact ⟨xs, rfl, hf⟩

theorem path_lift {A : Type u} {R : A → A → Prop} {B : A → Prop}
    {a b : A} (h : Path R a b) : Path (addRoot R B) (some a) (some b) := by
  induction h with
  | refl => exact Path.refl (some a)
  | tail h e ih => exact Path.tail ih e

theorem path_trans {A : Type u} {R : A → A → Prop} {a b c : A}
    (hab : Path R a b) (hbc : Path R b c) : Path R a c := by
  induction hbc with
  | refl => exact hab
  | tail h e ih => exact Path.tail ih e

theorem no_edge_to_new {A : Type u} (R : A → A → Prop) (B : A → Prop)
    (a : Option A) : ¬ addRoot R B a none := by
  intro h
  cases a <;> exact h

theorem path_to_new {A : Type u} {R : A → A → Prop} {B : A → Prop}
    {x : Option A} (h : Path (addRoot R B) x none) : x = none := by
  cases h with
  | refl => rfl
  | tail h e => exact False.elim (no_edge_to_new R B _ e)

theorem path_old_endpoints {A : Type u} {R : A → A → Prop} {B : A → Prop}
    {a : A} {y : Option A} (h : Path (addRoot R B) (some a) y) :
    ∃ b, y = some b ∧ Path R a b := by
  induction h with
  | refl => exact ⟨a, rfl, Path.refl a⟩
  | @tail b c h e ih =>
    obtain ⟨d, hd, hp⟩ := ih
    subst b
    cases c with
    | none => exact False.elim e
    | some c => exact ⟨c, rfl, Path.tail hp e⟩

/-- G2: the new ground introduces no old-to-old support path. -/
theorem old_path_iff {A : Type u} (R : A → A → Prop) (B : A → Prop)
    (a b : A) : Path (addRoot R B) (some a) (some b) ↔ Path R a b := by
  constructor
  · intro h
    obtain ⟨c, heq, hp⟩ := path_old_endpoints h
    have hbc : b = c := Option.some.inj heq
    exact hbc ▸ hp
  · exact path_lift

/-- G3: no new cycle, for an arbitrary root set B. -/
theorem acyclic_preserved {A : Type u} (R : A → A → Prop) (B : A → Prop)
    (h : Acyclic R) : Acyclic (addRoot R B) := by
  intro a b hab hback
  cases a with
  | none =>
    cases b with
    | none => exact hab
    | some b =>
      have heq := path_to_new hback
      cases heq
  | some a =>
    cases b with
    | none => exact hab
    | some b => exact h a b hab ((old_path_iff R B b a).mp hback)

theorem accessible_new {A : Type u} (R : A → A → Prop) (B : A → Prop) :
    Acc (addRoot R B) none := by
  apply Acc.intro
  intro a h
  cases a with
  | none => exact False.elim h
  | some a => exact False.elim h

theorem accessible_old {A : Type u} {R : A → A → Prop} (B : A → Prop)
    {a : A} (ha : Acc R a) : Acc (addRoot R B) (some a) := by
  induction ha with
  | intro a h ih =>
    apply Acc.intro
    intro b hb
    cases b with
    | none => exact accessible_new R B
    | some b => exact ih b hb

/-- G4: predecessors are sources, so this is ancestry well-foundedness. -/
theorem wellFounded_preserved {A : Type u} (R : A → A → Prop) (B : A → Prop)
    (h : WellFounded R) : WellFounded (addRoot R B) := by
  apply WellFounded.intro
  intro a
  cases a with
  | none => exact accessible_new R B
  | some a => exact accessible_old B (h.apply a)

def Root {W : Type v} {A : Type u} (E : W → A → Prop)
    (S : W → A → A → Prop) (w : W) (a : A) : Prop :=
  E w a ∧ ∀ b, ¬ S w b a

def Coverage {W : Type v} {A : Type u} (E : W → A → Prop)
    (S : W → A → A → Prop) (w : W) : Prop :=
  ∀ a, E w a → ∃ r, Root E S w r ∧ Path (S w) r a

def Necessary {W : Type v} {A : Type u} (E : W → A → Prop) (a : A) : Prop :=
  ∀ w, E w a

theorem old_necessary_iff {W : Type v} {A : Type u}
    (E : W → A → Prop) (a : A) :
    Necessary (liftExist E) (some a) ↔ Necessary E a := Iff.rfl

def extSupport {W : Type v} {A : Type u} (E : W → A → Prop)
    (S : W → A → A → Prop) (w₀ : W) (w : W) : Option A → Option A → Prop :=
  addRoot (S w) (Root E S w₀)

theorem new_is_root {W : Type v} {A : Type u} (E : W → A → Prop)
    (S : W → A → A → Prop) (w₀ w : W) :
    Root (liftExist E) (extSupport E S w₀) w none := by
  constructor
  · exact True.intro
  · intro a h
    cases a with
    | none => exact h
    | some a => exact h

/-- Actual uniqueness is at w₀, not an unsupported all-world conclusion. -/
theorem no_old_actual_root {W : Type v} {A : Type u} (E : W → A → Prop)
    (S : W → A → A → Prop) (w₀ : W) (a : A) :
    ¬ Root (liftExist E) (extSupport E S w₀) w₀ (some a) := by
  intro h
  have oldRoot : Root E S w₀ a := by
    constructor
    · exact h.1
    · intro b hb
      exact h.2 (some b) hb
  exact h.2 none oldRoot

theorem actual_root_iff_new {W : Type v} {A : Type u} (E : W → A → Prop)
    (S : W → A → A → Prop) (w₀ : W) (a : Option A) :
    Root (liftExist E) (extSupport E S w₀) w₀ a ↔ a = none := by
  cases a with
  | none => exact ⟨fun _ => rfl, fun _ => new_is_root E S w₀ w₀⟩
  | some a =>
    constructor
    · intro h
      exact False.elim (no_old_actual_root E S w₀ a h)
    · intro h
      cases h

/-- G5: inherited actual coverage becomes coverage by the one new root. -/
theorem actual_coverage_preserved {W : Type v} {A : Type u}
    (E : W → A → Prop) (S : W → A → A → Prop) (w₀ : W)
    (h : Coverage E S w₀) :
    Coverage (liftExist E) (extSupport E S w₀) w₀ := by
  intro a ha
  refine ⟨none, new_is_root E S w₀ w₀, ?_⟩
  cases a with
  | none => exact Path.refl none
  | some a =>
    obtain ⟨r, hr, hp⟩ := h a ha
    have start : Path (extSupport E S w₀ w₀) none (some r) :=
      Path.tail (Path.refl none) hr
    exact path_trans start (path_lift hp)

def GroundNecessitates {W : Type v} {A : Type u}
    (E : W → A → Prop) (G : W → A → A → Prop) : Prop :=
  ∀ w a b, G w a b → ∀ v, E v a → E v b

def extGround {W : Type v} {A : Type u}
    (E : W → A → Prop) (S G : W → A → A → Prop) (w₀ : W) (w : W) :
    Option A → Option A → Prop :=
  addRoot (G w) (Root E S w₀)

/-- G6 concerns grounding, not the mixed support relation. -/
theorem ground_necessitation_preserved {W : Type v} {A : Type u}
    (E : W → A → Prop) (S G : W → A → A → Prop) (w₀ : W)
    (hg : GroundNecessitates E G)
    (hr : ∀ r, Root E S w₀ r → Necessary E r) :
    GroundNecessitates (liftExist E) (extGround E S G w₀) := by
  intro w a b hab v ha
  cases a with
  | none =>
    cases b with
    | none => exact False.elim hab
    | some b => exact hr b hab v
  | some a =>
    cases b with
    | none => exact False.elim hab
    | some b => exact hg w a b hab v ha

theorem ground_path_necessitates {W : Type v} {A : Type u}
    (E : W → A → Prop) (G : W → A → A → Prop)
    (hg : GroundNecessitates E G) {w : W} {a b : A}
    (hp : Path (G w) a b) : ∀ v, E v a → E v b := by
  induction hp with
  | refl => intro _ h; exact h
  | @tail b c hp edge ih =>
    intro v ha
    exact hg w b c edge v (ih v ha)

theorem ground_in_support_preserved {W : Type v} {A : Type u}
    (E : W → A → Prop) (S G : W → A → A → Prop) (w₀ : W)
    (h : ∀ w a b, G w a b → S w a b) :
    ∀ w a b, extGround E S G w₀ w a b → extSupport E S w₀ w a b := by
  intro w a b hab
  cases a with
  | none => cases b <;> exact hab
  | some a =>
    cases b with
    | none => exact hab
    | some b => exact h w a b hab

theorem support_endpoints_preserved {W : Type v} {A : Type u}
    (E : W → A → Prop) (S : W → A → A → Prop) (w₀ : W)
    (hs : ∀ w a b, S w a b → E w a ∧ E w b)
    (hr : ∀ r, Root E S w₀ r → Necessary E r) :
    ∀ w a b, extSupport E S w₀ w a b → liftExist E w a ∧ liftExist E w b := by
  intro w a b hab
  cases a with
  | none =>
    cases b with
    | none => exact False.elim hab
    | some b => exact ⟨True.intro, hr b hab w⟩
  | some a =>
    cases b with
    | none => exact False.elim hab
    | some b => exact hs w a b hab

/-- G7a: the new original particular exists at every modal index. -/
theorem necessary_original_particular {W : Type v} {A : Type u}
    (E : W → A → Prop) (S : W → A → A → Prop) (w₀ : W) :
    ∃ a, Root (liftExist E) (extSupport E S w₀) w₀ a ∧ Necessary (liftExist E) a := by
  exact ⟨none, new_is_root E S w₀ w₀, fun _ => True.intro⟩

/-- G7b: no actual root possesses the old productive-holder predicate. -/
theorem no_original_power_bearer {W : Type v} {A : Type u}
    (E : W → A → Prop) (S : W → A → A → Prop) (w₀ : W) (H : A → Prop) :
    ¬ ∃ a, Root (liftExist E) (extSupport E S w₀) w₀ a ∧ liftHolder H a := by
  intro h
  obtain ⟨a, hroot, hh⟩ := h
  have heq := (actual_root_iff_new E S w₀ a).mp hroot
  subst a
  exact hh

/-- The structural construction does not decide the new root's standing power. -/
theorem original_holder_iff_ground_holder {W : Type v} {A : Type u}
    (E : W → A → Prop) (S : W → A → A → Prop) (w₀ : W)
    (H : A → Prop) (Q : Prop) :
    (∃ a, Root (liftExist E) (extSupport E S w₀) w₀ a ∧ liftHolderWith Q H a)
      ↔ Q := by
  constructor
  · intro h
    obtain ⟨a, hroot, hh⟩ := h
    have heq := (actual_root_iff_new E S w₀ a).mp hroot
    subst a
    exact hh
  · intro hq
    exact ⟨none, new_is_root E S w₀ w₀, hq⟩

/-- Standing ability never silently becomes an actual productive arrow. -/
theorem no_original_actual_producer {W : Type v} {A : Type u}
    (E : W → A → Prop) (S P : W → A → A → Prop) (w₀ : W) :
    ¬ ∃ a, Root (liftExist E) (extSupport E S w₀) w₀ a ∧
      ∃ b, liftProductive P w₀ a b := by
  intro h
  obtain ⟨a, hroot, b, hp⟩ := h
  have heq := (actual_root_iff_new E S w₀ a).mp hroot
  subst a
  exact (new_has_no_production P w₀ b).1 hp

/-- A necessary, essentially original, capable ground with no actual production.
This is a structural interpretation, not an assertion of metaphysical eligibility. -/
theorem capable_ground_without_actual_production {W : Type v} {A : Type u}
    (E : W → A → Prop) (S P : W → A → A → Prop) (w₀ : W) (H : A → Prop) :
    (∃ a, Necessary (liftExist E) a ∧
      (∀ w, Root (liftExist E) (extSupport E S w₀) w a) ∧
      liftHolderWith True H a) ∧
    ¬ ∃ a, Root (liftExist E) (extSupport E S w₀) w₀ a ∧
      ∃ b, liftProductive P w₀ a b := by
  constructor
  · exact ⟨none, (fun _ => True.intro), new_is_root E S w₀, True.intro⟩
  · exact no_original_actual_producer E S P w₀

end T20.GroundExtension
