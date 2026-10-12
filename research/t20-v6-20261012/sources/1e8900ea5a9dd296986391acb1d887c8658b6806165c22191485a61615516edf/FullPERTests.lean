import FullPER
import EffectivePrimitiveRecursion

namespace FullPERTests
open P01AC P01D
open P01AC.ExtensionalRepair
open P01AC.EffectiveCompleteness
open P01AC.IdentityComplexity
open P01AC.BooleanIdentity
open P01AC.BooleanPrimitive
open ImportedOpenTermTransport (interp embed)
open OpenTermStandardness (T Conv churchPER iter)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Actual source syntax: test the boolean output at the bound variable by Raw observation. -/
def testBody (p : Poly) : Poly := .app (.app (.app p (.var 0)) (.atom .zero)) (.atom .one)
def testType (p : Poly) : Ty := .pi N (.identity .raw (testBody p) (.atom .zero))

theorem testBody_has {p : Poly} (hp : Has [] p CB) : Has [N] (testBody p) .raw := by
  have hc : Ctx [N] := .ext .nil (N_form .nil)
  have hr : Form [N] .raw := .raw hc
  have hB : Form [N] B := B_form hc
  have hCB : Form [N] CB := form_arr (N_form hc) hB
  have pp : Has [N] p CB := closed_has hp (fun _ => rfl) hc
  have nn : Has [N] (.var 0) N := .var (N_form hc) .zero
  have pn : Has [N] (.app p (.var 0)) B := app_has hCB hB pp nn
  have br : Has [N] (.app p (.var 0)) (arr .raw (arr .raw .raw)) :=
    .allElim hB hr (form_arr hr (form_arr hr hr)) pn
  exact app_has (form_arr hr hr) hr
    (app_has (form_arr hr (form_arr hr hr)) (form_arr hr hr) br (.rawAtom hr)) (.rawAtom hr)

theorem testType_form {p : Poly} (hp : Has [] p CB) : Form [] (testType p) :=
  .pi (N_form .nil) (.identity (.raw (.ext .nil (N_form .nil)))
    (testBody_has hp) (.rawAtom (.raw (.ext .nil (N_form .nil)))))

theorem testType_formE {p : Poly} (hp : Has [] p CB) : FormE [] (testType p) :=
  form_inclusion (testType_form hp)

theorem interp_closed {p : Poly} (hp : Scoped 0 p) (η ξ : FullPER.Env) : interp p η = interp p ξ := by
  induction p with
  | var n => exact False.elim (Nat.not_lt_zero n hp)
  | atom a => rfl
  | app f a ihf iha => exact congrArg₂ T.app (ihf hp.1) (iha hp.2)

theorem interp_canonical (n : Nat) :
    interp (inputNumeral n) FullPER.zeroEnv = embed (canonical n) :=
  ImportedOpenTermTransport.map_eval (inputNumeral n) P01AC.zeroEnv

theorem inputNumeral_open_applied (n : Nat) (f a : T) (η : FullPER.Env) :
    Conv (interp (inputNumeral n) η ⬝ f ⬝ a) (iter f a n) := by
  have h1 := Conv.app (ImportedOpenTermTransport.interp_abstraction_beta
    (abstract (iterationPoly n)) η f) (.refl a)
  have h2 := ImportedOpenTermTransport.interp_abstraction_beta
    (iterationPoly n) (OpenTermStandardness.cons f η) a
  have he : interp (iterationPoly n) (OpenTermStandardness.cons a (OpenTermStandardness.cons f η)) =
      iter f a n := by
    clear h1 h2
    induction n with
    | zero => rfl
    | succ n ih => exact congrArg (T.app f) ih
  exact h1.trans (he ▸ h2)

theorem canonical_church (k : Nat) : churchPER.rel (embed (canonical k)) (embed (canonical k)) := by
  intro R f g fg a b ab
  have hf := inputNumeral_open_applied k f a FullPER.zeroEnv
  have hg := inputNumeral_open_applied k g b FullPER.zeroEnv
  rw [interp_canonical] at hf hg
  exact R.saturated hf.symm hg.symm (OpenTermStandardness.iter_related R fg ab k)

theorem church_canonical {n : T} (hn : churchPER.rel n n) :
    ∃ k, churchPER.rel n (embed (canonical k)) := by
  obtain ⟨k, hk⟩ := OpenTermStandardness.church_standard n hn
  refine ⟨k, ?_⟩
  intro R f g fg a b ab
  have hg := inputNumeral_open_applied k g b FullPER.zeroEnv
  rw [interp_canonical] at hg
  exact R.saturated (hk f a).symm hg.symm (OpenTermStandardness.iter_related R fg ab k)

/-- Raw observation is faithful conversion, through the actual full-PER Boolean type. -/
theorem boolean_observation {ρ : FullPER.REnv} {η : FullPER.Env} {u v : T}
    (h : FullPER.F B ρ η u v) : Conv (u ⬝ .zero ⬝ .one) (v ⬝ .zero ⬝ .one) := by
  let Q : OpenTermStandardness.SatPER :=
    ⟨Conv, Conv.symm, Conv.trans, fun ha hb h => ha.symm.trans (h.trans hb)⟩
  exact h Q .zero .zero (.refl _) .one .one (.refl _)

def Holds (A : Ty) : Prop :=
  ∀ ρ, FullPER.admissible ρ → ∃ t : T, FullPER.F A ρ FullPER.zeroEnv t t

def uniformWitness : T := .k ⬝ .i

theorem observations_imply_uniform {p : Poly} (hp : Has [] p CB)
    (tests : ∀ k, OrthemologyV3.Conv (observationAt p k) .zero)
    (ρ : FullPER.REnv) (r : FullPER.admissible ρ) :
    FullPER.F (testType p) ρ FullPER.zeroEnv uniformWitness uniformWitness := by
  intro n m nm
  have nn := churchPER.trans nm (churchPER.symm nm)
  obtain ⟨k, nk⟩ := church_canonical nn
  have pp := FullPER.fundamental (has_inclusion hp) ρ FullPER.zeroEnv FullPER.zeroEnv r ⟨rfl,rfl⟩
  rw [CB, FullPER.F_arr] at pp
  have obs := boolean_observation (pp n (embed (canonical k)) nk)
  have test := ImportedOpenTermTransport.source_conv_sound (tests k)
  have ep : interp p FullPER.zeroEnv = embed (P01D.eval p P01AC.zeroEnv) :=
    ImportedOpenTermTransport.map_eval p P01AC.zeroEnv
  have result : Conv (interp p FullPER.zeroEnv ⬝ n ⬝ .zero ⬝ .one) .zero := by
    apply obs.trans
    simpa only [observationAt, observe, embed, ← ep] using test
  refine ⟨?_, .k .i n, .k .i m⟩
  simpa only [testBody, FullPER.interp_app, FullPER.interp_atom, FullPER.interp_var,
    interp_closed (has_scoped hp) (FullPER.cons n FullPER.zeroEnv) FullPER.zeroEnv,
    FullPER.cons, embed] using result

theorem inhabited_iff_observations {p : Poly} (hp : Has [] p CB)
    (ρ : FullPER.REnv) (r : FullPER.admissible ρ) :
    (∃ t, FullPER.F (testType p) ρ FullPER.zeroEnv t t) ↔
      ∀ k, OrthemologyV3.Conv (observationAt p k) .zero := by
  constructor
  · rintro ⟨t, ht⟩ k
    have v := (ht (embed (canonical k)) (embed (canonical k)) (canonical_church k)).1
    have ep : interp p FullPER.zeroEnv = embed (P01D.eval p P01AC.zeroEnv) :=
      ImportedOpenTermTransport.map_eval p P01AC.zeroEnv
    have obs : Conv (embed (observationAt p k)) (embed .zero) := by
      simpa only [testBody, FullPER.interp_app, FullPER.interp_atom, FullPER.interp_var,
        interp_closed (has_scoped hp) (FullPER.cons (embed (canonical k)) FullPER.zeroEnv) FullPER.zeroEnv,
        FullPER.cons, observationAt, observe, ep, embed] using v
    exact (ImportedOpenTermTransport.embed_conversion_iff _ _).mp obs
  · intro tests
    exact ⟨uniformWitness, observations_imply_uniform hp tests ρ r⟩

#print axioms testType_formE
#print axioms inhabited_iff_observations
end FullPERTests
