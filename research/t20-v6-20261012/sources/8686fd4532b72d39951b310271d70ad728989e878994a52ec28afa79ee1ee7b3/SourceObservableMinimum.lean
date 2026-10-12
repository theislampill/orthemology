import SourceSidecarController
import Mathlib.Data.Fintype.Card

namespace FiniteSidecar
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC
open P01F (cons)
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open JointCompletion (HasJ FormJ CtxJ)
open P01AC.Intensional.Plus (PolyConvPlus)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Observed ordinary natural counts agree with the existing actual Joint extractor. -/
theorem extracted_eq_observed {p : Poly} {k : Nat} (hp : HasJ [] p N)
    (ho : NatObs (eval p zeroEnv) k) :
    (JointCompletion.EffectiveNumerals.extractIteration p hp).val = k := by
  have hc := (JointCompletion.EffectiveNumerals.extractIteration p hp).property
  have hu := ClosedChurchIdentity.observation_uniform (JointCompletion.Structural.has_scoped hp) hc
  exact marker_conv_injective ((hu .zero .one).symm.trans (ho .zero .one))

/-- Existing typed identity cannot merge different externally checked source counts. -/
theorem identity_observed_eq {p q e : Poly} {j k : Nat}
    (hp : HasJ [] p N) (hq : HasJ [] q N)
    (op : NatObs (eval p zeroEnv) j) (oq : NatObs (eval q zeroEnv) k)
    (he : HasJ [] e (.identity N p q)) : j = k := by
  have h := JointCompletion.DependentExtraction.identity_implies_count_eq hp hq
    (JointCompletion.EffectiveNumerals.extractIteration p hp).property
    (JointCompletion.EffectiveNumerals.extractIteration q hq).property he
  simpa only [extracted_eq_observed hp op, extracted_eq_observed hq oq] using h

/-- This is a closed-typed-natural consequence only, not source compiler completeness. -/
theorem identity_at_observed {p : Poly} {k : Nat} (hp : HasJ [] p N)
    (ho : NatObs (eval p zeroEnv) k) :
    HasJ [] (.atom .i) (.identity N p (inputNumeral k)) := by
  have h := JointCompletion.DependentExtraction.extracted_identity p hp
  simpa only [extracted_eq_observed hp ho] using h

abbrev oldJ {Γ p A} (hp : Has Γ p A) : HasJ Γ p A :=
  .hasBase (P01AC.ExtensionalRepair.has_inclusion hp)
abbrev oldFormJ {Γ A} (hp : Form Γ A) : FormJ Γ A :=
  .formBase (P01AC.ExtensionalRepair.form_inclusion hp)

theorem observer_identity_counts {x y observer e : Poly} {j k : Nat}
    (hx : HasJ [] x State) (hy : HasJ [] y State)
    (ho : HasJ [] observer (arr State N))
    (ox : NatObs (eval (.app observer x) zeroEnv) j)
    (oy : NatObs (eval (.app observer y) zeroEnv) k)
    (he : HasJ [] e (.identity State x y)) : j = k := by
  have hs := oldFormJ (state_form Ctx.nil)
  have hn := oldFormJ (N_form Ctx.nil)
  have hf := JointCompletion.InductionComputation.form_arr hs hn
  exact identity_observed_eq
    (JointCompletion.InductionComputation.app_has hf hn ho hx)
    (JointCompletion.InductionComputation.app_has hf hn ho hy) ox oy
    (JointCompletion.RecursorUniqueness.arrow_congr .nil hs hn ho hx hy he)

def coarseObserver : Poly := abstract (coarsePoly (.var 0))
def tagObserver : Poly := abstract (tagPoly (.var 0))

theorem coarseObserver_has : Has [] coarseObserver (arr State N) := by
  have hc : Ctx [State] := .ext .nil (state_form .nil)
  have hv : Has [State] (.var 0) State := .var (state_form hc) .zero
  exact .piIntro (form_arr (state_form .nil) (N_form .nil)) (coarse_has hc hv)
    (scoped_abstract (has_scoped (coarse_has hc hv)))
theorem tagObserver_has : Has [] tagObserver (arr State N) := by
  have hc : Ctx [State] := .ext .nil (state_form .nil)
  have hv : Has [State] (.var 0) State := .var (state_form hc) .zero
  exact .piIntro (form_arr (state_form .nil) (N_form .nil)) (tag_has hc hv)
    (scoped_abstract (has_scoped (tag_has hc hv)))
theorem coarseObserver_observes {p : Term} {z k : Nat} (hp : Represents p z k) :
    NatObs (.app (eval coarseObserver zeroEnv) p) z :=
  NatObs.of_conv (P01Source.red_conv (abstraction_beta (coarsePoly (.var 0)) zeroEnv p)) hp.1
theorem tagObserver_observes {p : Term} {z k : Nat} (hp : Represents p z k) :
    NatObs (.app (eval tagObserver zeroEnv) p) k :=
  NatObs.of_conv (P01Source.red_conv (abstraction_beta (tagPoly (.var 0)) zeroEnv p)) hp.2

/-- Exact source identity separation of the joint retained record, including label reuse. -/
theorem encoded_identity_iff (z k z' k' : Nat) :
    (∃ e, HasJ [] e (.identity State (encodeState z k) (encodeState z' k'))) ↔
      z = z' ∧ k = k' := by
  constructor
  · rintro ⟨e, he⟩
    have hp := oldJ (encodeState_has z k)
    have hq := oldJ (encodeState_has z' k')
    exact ⟨observer_identity_counts hp hq (oldJ coarseObserver_has)
      (coarseObserver_observes (encoded_represents z k))
      (coarseObserver_observes (encoded_represents z' k')) he,
      observer_identity_counts hp hq (oldJ tagObserver_has)
      (tagObserver_observes (encoded_represents z k))
      (tagObserver_observes (encoded_represents z' k')) he⟩
  · rintro ⟨rfl,rfl⟩
    have hp := oldJ (encodeState_has z k)
    exact ⟨.atom .i, .identityIntro (.identity (oldFormJ (state_form .nil)) hp hp) hp hp (.refl _)⟩

/-- Explicit evidence-parametric packer: ordinary data is fixed, proof slot remains typed. -/
def proofPacker (z k : Nat) : Poly :=
  abstract (pack (inputNumeral z) (inputNumeral k) (.var 0))
def withEvidence (z k : Nat) (e : Poly) : Poly := .app (proofPacker z k) e

theorem proofPacker_has (z k : Nat) : Has [] (proofPacker z k) (arr Evidence State) := by
  have hc : Ctx [Evidence] := .ext .nil (evidence_form .nil)
  have hz := closed_has (inputNumeral_has z) N_subst hc
  have hk := closed_has (inputNumeral_has k) N_subst hc
  have he : Has [Evidence] (.var 0) Evidence := .var (evidence_form hc) .zero
  have hb := pack_has hc hz hk he
  exact .piIntro (form_arr (evidence_form .nil) (state_form .nil)) hb
    (scoped_abstract (has_scoped hb))

theorem withEvidence_has {e : Poly} (z k : Nat) (he : HasJ [] e Evidence) :
    HasJ [] (withEvidence z k e) State :=
  JointCompletion.InductionComputation.app_has
    (oldFormJ (form_arr (evidence_form .nil) (state_form .nil)))
    (oldFormJ (state_form .nil)) (oldJ (proofPacker_has z k)) he

/-- Different proofs cannot supply a hidden extra tag when coarse and ordinary tag agree. -/
theorem proof_slot_cannot_separate (z k : Nat) {e f : Poly}
    (he : HasJ [] e Evidence) (hf : HasJ [] f Evidence) :
    HasJ [] (.atom .i) (.identity State (withEvidence z k e) (withEvidence z k f)) :=
  JointCompletion.RecursorUniqueness.arrow_congr .nil
    (oldFormJ (evidence_form .nil)) (oldFormJ (state_form .nil))
    (oldJ (proofPacker_has z k)) he hf
    (JointCompletion.ProofUniqueness.identity_proof_unique .nil he hf)

/-- A required distinction has an actual typed source observer and distinct numeric outputs. -/
def ObservablyDifferent (x y : Poly) : Prop :=
  ∃ observer j k, HasJ [] observer (arr State N) ∧
    NatObs (eval (.app observer x) zeroEnv) j ∧
    NatObs (eval (.app observer y) zeroEnv) k ∧ j ≠ k

/-- Source-level pigeonhole bound: even arbitrarily varying identity proofs cannot help. -/
theorem finite_fibre_lower_bound {n M : Nat} (z : Nat) (tag : Fin n → Fin M)
    (evidence : Fin n → Poly)
    (he : ∀ i, HasJ [] (evidence i) Evidence)
    (required : ∀ i j, i ≠ j → ObservablyDifferent
      (withEvidence z (tag i).val (evidence i))
      (withEvidence z (tag j).val (evidence j))) : n ≤ M := by
  have hi : Function.Injective tag := by
    intro i j eqtag
    by_contra ne
    obtain ⟨observer, a, b, ho, oa, ob, hab⟩ := required i j ne
    apply hab
    have hs := proof_slot_cannot_separate z (tag i).val (he i) (he j)
    rw [eqtag] at hs
    exact observer_identity_counts
      (withEvidence_has z (tag i).val (he i))
      (withEvidence_has z (tag j).val (he j)) ho oa ob
      (by simpa only [eqtag] using hs)
  simpa only [Fintype.card_fin] using Fintype.card_le_of_injective tag hi

/-- n tags suffice at one fixed coarse value, witnessed by a real source projection. -/
theorem finite_fibre_attains (n z : Nat) (i j : Fin n) (hij : i ≠ j) :
    ObservablyDifferent (encodeState z i.val) (encodeState z j.val) := by
  refine ⟨tagObserver, i.val, j.val, oldJ tagObserver_has,
    tagObserver_observes (encoded_represents z i.val),
    tagObserver_observes (encoded_represents z j.val), ?_⟩
  intro h
  exact hij (Fin.ext h)

/-- The ordinary projections ignore even a computationally different proof realizer. -/
theorem withEvidence_represents (z k : Nat) (e : Poly) :
    Represents (eval (withEvidence z k e) zeroEnv) z k := by
  have hb : Conv (eval (withEvidence z k e) zeroEnv)
      (pairTerm (P01AC.IdentityComplexity.canonical z)
        (pairTerm (P01AC.IdentityComplexity.canonical k) (eval e zeroEnv))) := by
    have h := P01Source.red_conv (abstraction_beta
      (pack (inputNumeral z) (inputNumeral k) (.var 0)) zeroEnv (eval e zeroEnv))
    simpa only [withEvidence, proofPacker, pack, eval_pair, eval, cons,
      eval_closed (has_scoped (inputNumeral_has z)) (P01F.cons (eval e zeroEnv) zeroEnv) zeroEnv,
      eval_closed (has_scoped (inputNumeral_has k)) (P01F.cons (eval e zeroEnv) zeroEnv) zeroEnv,
      P01AC.IdentityComplexity.canonical] using h
  exact ⟨NatObs.of_conv ((hb.left .k).trans (pair_first _ _)) (canonical_obs z),
    NatObs.of_conv ((((hb.left (.app .k .i)).trans (pair_second _ _)).left .k).trans
      (pair_first _ _)) (canonical_obs k)⟩

/-- D2's per-fibre reuse is realizable with actual source data and observers. -/
theorem common_alphabet_attains {Z M : Nat} (counts : Fin Z → Nat)
    (bound : ∀ z, counts z ≤ M) :
    ∃ tags : (z : Fin Z) → Fin (counts z) → Fin M,
      ∀ z i j, i ≠ j → ObservablyDifferent
        (withEvidence z.val (tags z i).val (.atom .i))
        (withEvidence z.val (tags z j).val (.atom .i)) := by
  refine ⟨fun z i => ⟨i.val, Nat.lt_of_lt_of_le i.isLt (bound z)⟩, ?_⟩
  intro z i j hij
  refine ⟨tagObserver, i.val, j.val, oldJ tagObserver_has,
    tagObserver_observes (withEvidence_represents z.val i.val (.atom .i)),
    tagObserver_observes (withEvidence_represents z.val j.val (.atom .i)), ?_⟩
  intro h
  exact hij (Fin.ext h)

/-- This minimum is explicitly relative to source-observable required classes. -/
theorem common_alphabet_exact {Z M : Nat} (counts : Fin Z → Nat) :
    (∃ tags : (z : Fin Z) → Fin (counts z) → Fin M,
      ∃ evidence : (z : Fin Z) → Fin (counts z) → Poly,
      (∀ z i, HasJ [] (evidence z i) Evidence) ∧
      (∀ z i j, i ≠ j → ObservablyDifferent
        (withEvidence z.val (tags z i).val (evidence z i))
        (withEvidence z.val (tags z j).val (evidence z j)))) ↔
      ∀ z, counts z ≤ M := by
  constructor
  · rintro ⟨tags, evidence, he, required⟩ z
    exact finite_fibre_lower_bound z.val (tags z) (evidence z) (he z) (required z)
  · intro bound
    obtain ⟨tags, required⟩ := common_alphabet_attains counts bound
    exact ⟨tags, fun _ _ => .atom .i, fun _ _ => oldJ (evidence_has .nil), required⟩

#print axioms encoded_identity_iff
#print axioms proof_slot_cannot_separate
#print axioms finite_fibre_lower_bound
#print axioms finite_fibre_attains
end FiniteSidecar
