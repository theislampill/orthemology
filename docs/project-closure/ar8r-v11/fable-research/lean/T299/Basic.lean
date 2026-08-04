import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic.DeriveFintype
import Mathlib.Logic.Function.Basic

/-!
AR8R-T299 — matched-intervention burden-landing certification.

Machine-checked formalization of the characterization recorded in
  docs/project-closure/ar8r-v11/theorems/ar8r-t299-matched-intervention-burden-landing.md

Every `DEFECT (Ax)` / `AMBIGUITY (Ax)` comment marks a place where the informal
packet does not determine the formal content. Those are the deliverable: the
formalization is valuable here because it exposes specification defects, not
because the mathematics is deep (it is the quotient factorization lemma).

No axiom beyond Lean's own is introduced. Classical choice is used once, in the
right-to-left direction of the main characterization.
-/

namespace AR8R.T299

/-! ## §1. The abstract characterization

The packet's sentence:
  "For any declared profile map `P`, causal landing is profile-certifiable
   exactly when `L_b` is constant on every fibre of `P`."

AMBIGUITY (A7): the packet declares the setting "finite and deterministic", but
neither finiteness nor determinism is used below. The characterization is true
for arbitrary types. Finiteness buys only decidability and a *computable*
certificate. The packet conflates "the theorem needs finiteness" with "the
certificate is effectively constructible".
-/

section Abstract
variable {Bg Prof : Type*}

/-- An exact profile-level certificate exists. -/
def Certifiable (P : Bg → Prof) (l : Bg → Bool) : Prop :=
  ∃ c : Prof → Bool, ∀ b, c (P b) = l b

/-- The label is constant on every fibre of the profile map. -/
def FibreConst (P : Bg → Prof) (l : Bg → Bool) : Prop :=
  ∀ b b', P b = P b' → l b = l b'

/-- The packet's second phrasing: "two backgrounds with the same profile never
receive different causal-landing values". Recorded separately so that the
packet's word "Equivalently" is proved, not assumed. -/
def NoDisagreeingPair (P : Bg → Prof) (l : Bg → Bool) : Prop :=
  ¬ ∃ b b', P b = P b' ∧ l b ≠ l b'

theorem fibreConst_iff_noDisagreeingPair (P : Bg → Prof) (l : Bg → Bool) :
    FibreConst P l ↔ NoDisagreeingPair P l := by
  constructor
  · rintro h ⟨b, b', hp, hne⟩
    exact hne (h b b' hp)
  · intro h b b' hp
    by_contra hne
    exact h ⟨b, b', hp, hne⟩

/-- **MAIN CHARACTERIZATION (AR8R-T299).** -/
theorem certifiable_iff_fibreConst (P : Bg → Prof) (l : Bg → Bool) :
    Certifiable P l ↔ FibreConst P l := by
  constructor
  · rintro ⟨c, hc⟩ b b' hbb'
    rw [← hc b, ← hc b', hbb']
  · intro h
    classical
    refine ⟨fun p => if hp : ∃ b, P b = p then l hp.choose else false, ?_⟩
    intro b
    have hex : ∃ b', P b' = P b := ⟨b, rfl⟩
    show (if hp : ∃ b', P b' = P b then l hp.choose else false) = l b
    rw [dif_pos hex]
    exact h _ _ hex.choose_spec

/-- The packet's remark that "the complete matched intervention profile is
sufficient by construction" is a *consequence*, not the theorem. -/
theorem certifiable_of_injective (P : Bg → Prof) (l : Bg → Bool)
    (hP : Function.Injective P) : Certifiable P l := by
  rw [certifiable_iff_fibreConst]
  intro b b' hbb'
  rw [hP hbb']

/-- Any label certified by a profile map is certified by any refinement of it. -/
theorem certifiable_mono {Prof' : Type*} (P : Bg → Prof) (P' : Bg → Prof')
    (l : Bg → Bool) (hrefine : ∀ b b', P' b = P' b' → P b = P b')
    (h : Certifiable P l) : Certifiable P' l := by
  rw [certifiable_iff_fibreConst] at *
  exact fun b b' hb => h b b' (hrefine b b' hb)

end Abstract

/-! ## §2. Where finiteness actually earns its keep -/

section Finite
variable {Bg Prof : Type*} [Fintype Bg] [DecidableEq Prof]

/-- Fibre constancy is *decidable* under finiteness + decidable profile equality.
This, and not the characterization of §1, is what the packet's word "finite"
buys. -/
instance decFibreConst (P : Bg → Prof) (l : Bg → Bool) :
    Decidable (FibreConst P l) := by
  unfold FibreConst; infer_instance

end Finite

/-! ## §3. DEFECT (A4) — "requires" is not a definition

The packet states: causal landing `L_b` **requires** all of clauses 1-6.

Read literally that supplies only necessary conditions, leaving `L_b`
underdetermined. The abstract characterization of §1 is unaffected — it holds for
an arbitrary label. What is NOT established under the literal reading is the
packet's separate claim that the matched profile `B*` is sufficient "by
construction": a merely-necessary clause set does not determine the label, so
`B*`-fibre-constancy of the clauses does not certify it.

The generic shape is `A4_requires_reading_is_insufficient` below. The
T299-specific witness, using the packet's own `Model`/`matchedProfile`/`L`
machinery, is `A4_matchedProfile_insufficient_under_requires_reading` in §4b. -/

theorem A4_requires_reading_is_insufficient :
    ∃ (Bg Prof : Type) (P : Bg → Prof) (clauses lbl : Bg → Bool),
      (∀ b, lbl b = true → clauses b = true) ∧   -- "landing requires the clauses"
      FibreConst P clauses ∧                      -- the clauses are fibre-constant
      ¬ FibreConst P lbl := by                    -- yet the label is not certifiable
  refine ⟨Bool, Unit, fun _ => (), fun _ => true, id, ?_, ?_, ?_⟩
  · intro b _; rfl
  · intro b b' _; rfl
  · intro h
    have hc : id true = id false := h true false rfl
    exact Bool.noConfusion hc

/-! ## §4. The declared setting, and DEFECT (A14)

AMBIGUITY (A9): the operation coordinate is never said to be binary; the packet
writes only `1` and `0` and calls it a "matched operation/no-operation"
comparison. We are forced to fix `Op := Bool`. With three or more values, clauses
2 and 5 become ill-posed (baseline value, or all `a` distinct from 1? —
inequivalent readings).

A14 (WITHDRAWN as a packet defect): round 1 originally claimed the declared model
shape "cannot express its own twin" and that a background-indexed `Q` was forced.
Independent review found the forcing comes from this encoding's own choice of
`term := fun a _ => ...`, which discards the background argument the packet
supplies via `term(a,b)`; with distinct per-background terminal states an
unindexed `Q` suffices. The background index on `Q` below is retained as a
convenience of this encoding only.

DEFECT (A10): the packet declares only `term(a,b)` — there is no "before" state
anywhere in the setting — yet the twin asserts that "before/after observations
match". That sentence is unstatable in the declared vocabulary. We are forced to
add `init` and an observation channel `obs`, neither of which the packet
declares. The twin claim is therefore *channel-relative*, and the channel is
unfixed: a channel exposing the background coordinate would falsify it. -/

abbrev Op := Bool

/-- AMBIGUITY (A13): only `LANDED` is ever named; whether "not landed" is one
value or many is unspecified. Three values keep the theorem honest about that
insensitivity. -/
inductive Disp | landed | notLanded | indeterminate
  deriving DecidableEq, Repr, Fintype

/-- The declared model. `init` is forced by the twin (A10); the background index
on `Q` is a convenience of this encoding (A14, withdrawn as a packet defect). -/
structure Model (Bg St : Type*) where
  term : Op → Bg → St
  Q    : Bg → St → Bool     -- background-indexed: encoding convenience (A14 withdrawn)
  D    : Bg → St → Disp
  R    : Bg → St → Bool
  C    : Bg → Bool
  init : Bg → St            -- forced by DEFECT (A10)

/-- Causal landing, under the *definitional* reading forced by DEFECT (A4).

AMBIGUITY (A11): clause 4 ("the declared whole-field reread passes") supplies no
argument, unlike clauses 1,2,3,5. We read it at the operation branch, because the
packet's own profile `B*` lists exactly `R_b(S_term^(1))`. Under the alternative
"whole-field" reading (both branches), the packet's own `B*` would be an
incomplete profile and its "sufficient by construction" claim would be FALSE.
Two sections of the packet silently constrain each other. -/
def L {Bg St : Type*} (M : Model Bg St) (b : Bg) : Bool :=
  M.Q b (M.term true b)                            -- 1
  && !(M.Q b (M.term false b))                     -- 2
  && (M.D b (M.term true b) == Disp.landed)        -- 3
  && M.R b (M.term true b)                         -- 4  [A11]
  && !(M.D b (M.term false b) == Disp.landed)      -- 5
  && M.C b                                         -- 6  [A5]

/-- The packet's matched intervention profile `B*`. -/
def matchedProfile {Bg St : Type*} (M : Model Bg St) (b : Bg) :
    Bool × Bool × Bool × Disp × Disp × Bool :=
  (M.C b,
   M.Q b (M.term false b), M.Q b (M.term true b),
   M.D b (M.term false b), M.D b (M.term true b),
   M.R b (M.term true b))

/-- "The complete matched intervention profile is sufficient by construction" —
now an actual lemma, and true for *every* model, with no finiteness. Note this
is exactly what fixes AMBIGUITY (A11): under the alternative reading of clause 4
this statement is false. -/
theorem certifiable_matchedProfile {Bg St : Type*} (M : Model Bg St) :
    Certifiable (matchedProfile M) (L M) := by
  rw [certifiable_iff_fibreConst]
  intro b b' h
  simp only [matchedProfile, Prod.mk.injEq] at h
  obtain ⟨hC, hQ0, hQ1, hD0, hD1, hR⟩ := h
  simp only [L, hC, hQ0, hQ1, hD0, hD1, hR]

/-! ## §4b. The T299-specific A4 witness

Added in the post-review correction. Unlike `A4_requires_reading_is_insufficient`
(which proves only the generic truism at `Bool`/`Unit`), this witness instantiates
the packet's own machinery: an actual model on which every six-clause conjunct
holds on both backgrounds — so the packet's matched profiles agree — while a label
satisfying the merely-necessary ("requires") reading still differs across them.
Hence `B*` does not certify a merely-necessary label, which is exactly the D1
consequence: the casualty of the literal reading is `B*` sufficiency, not the
abstract characterization. -/

/-- Two indistinguishable backgrounds, each landing causally: every clause holds
on both, so `L` is constantly `true` and the matched profiles coincide. States are
`Bool` (`true` = the operation branch's terminal state). -/
def constCause : Model Bool Bool where
  term := fun a _ => a
  Q := fun _ s => s
  D := fun _ s => if s then Disp.landed else Disp.notLanded
  R := fun _ _ => true
  C := fun _ => true
  init := fun _ => false

/-- **T299-specific A4 witness.** There is a label satisfying the "requires"
reading (it implies the six-clause conjunction `L`) that the packet's own matched
profile `B*` fails to separate. Axiom-free. -/
theorem A4_matchedProfile_insufficient_under_requires_reading :
    ∃ lbl : Bool → Bool,
      (∀ b, lbl b = true → L constCause b = true) ∧   -- the "requires" reading
      matchedProfile constCause true = matchedProfile constCause false ∧
      ¬ FibreConst (matchedProfile constCause) lbl := by
  refine ⟨id, ?_, ?_, ?_⟩
  · intro b _
    cases b <;> decide
  · decide
  · intro h
    have hc : id true = id false := h true false (by decide)
    exact Bool.noConfusion hc

/-- Restated with the packet's own word: such a label is not `B*`-certifiable. -/
theorem A4_matchedProfile_not_certifiable_under_requires_reading :
    ∃ lbl : Bool → Bool,
      (∀ b, lbl b = true → L constCause b = true) ∧
      ¬ Certifiable (matchedProfile constCause) lbl := by
  obtain ⟨lbl, hreq, _, hnc⟩ := A4_matchedProfile_insufficient_under_requires_reading
  exact ⟨lbl, hreq, fun hc => hnc ((certifiable_iff_fibreConst _ _).mp hc)⟩

/-! ## §5. The causal/spontaneous twin

DEFECT (A1): the characterization quantifies over backgrounds of ONE model; the
twin's profile `B*(M,u)` ranges over model-unit pairs across TWO models. As the
packet is written, the twin is not an instance of its own theorem. We resolve it
by reading the background coordinate as absorbing the model — the only reading
under which the twin is expressible. -/

inductive Twin | cause | spont
  deriving DecidableEq, Repr, Fintype

inductive TState | pre | term0 | term1
  deriving DecidableEq, Repr, Fintype

/-- The observation channel required by DEFECT (A10) but never declared. -/
abbrev Obs := Bool × Disp

def twin : Model Twin TState where
  term := fun a _ => if a then TState.term1 else TState.term0
  Q := fun b s => match b, s with
    | Twin.cause, TState.term1 => true
    | Twin.cause, TState.term0 => false
    | Twin.cause, TState.pre   => false
    | Twin.spont, TState.term1 => true
    | Twin.spont, TState.term0 => true      -- an independent background event lands it
    | Twin.spont, TState.pre   => false
  D := fun b s => match b, s with
    | Twin.cause, TState.term1 => Disp.landed
    | Twin.cause, TState.term0 => Disp.notLanded
    | Twin.cause, TState.pre   => Disp.notLanded
    | Twin.spont, TState.term1 => Disp.landed
    | Twin.spont, TState.term0 => Disp.landed
    | Twin.spont, TState.pre   => Disp.notLanded
  R := fun _ _ => true
  C := fun _ => true
  init := fun _ => TState.pre

def obs (b : Twin) (s : TState) : Obs := (twin.Q b s, twin.D b s)

/-- The before observation agrees across the twin. -/
theorem twin_before_agree :
    obs Twin.cause (twin.init Twin.cause) = obs Twin.spont (twin.init Twin.spont) := by
  decide

/-- Under `A = 1` the after observation agrees across the twin. -/
theorem twin_after_agree :
    obs Twin.cause (twin.term true Twin.cause)
      = obs Twin.spont (twin.term true Twin.spont) := by
  decide

/-- Nevertheless the causal-landing labels differ.
`M_spont` fails clauses 2 and 5 — two clauses, not one. -/
theorem twin_L_differs : L twin Twin.cause = true ∧ L twin Twin.spont = false := by
  constructor <;> decide

/-- The before/after observation profile under the operation branch. -/
def beforeAfterProfile (b : Twin) : Obs × Obs :=
  (obs b (twin.init b), obs b (twin.term true b))

/-- The packet's scope-firewall claim, machine-checked: a before/after delta is
insufficient. This is the right-to-left direction of the main theorem failing. -/
theorem beforeAfter_not_certifiable : ¬ Certifiable beforeAfterProfile (L twin) := by
  rw [certifiable_iff_fibreConst]
  intro h
  have hc : L twin Twin.cause = L twin Twin.spont := h Twin.cause Twin.spont (by decide)
  rw [twin_L_differs.1, twin_L_differs.2] at hc
  exact Bool.noConfusion hc

/-- The matched profile separates the twin, hence certifies it. -/
theorem matched_separates_twin :
    matchedProfile twin Twin.cause ≠ matchedProfile twin Twin.spont := by
  decide

theorem matched_certifies_twin : Certifiable (matchedProfile twin) (L twin) :=
  certifiable_matchedProfile twin

end AR8R.T299
