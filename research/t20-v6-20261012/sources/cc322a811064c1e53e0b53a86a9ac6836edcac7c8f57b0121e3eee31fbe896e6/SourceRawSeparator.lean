import JointNumeralExtraction
import NonstandardRejection

namespace OriginalRawSeparator
open P01AC P01D
open P01AC.Intensional.Plus (PolyConvPlus)
open OpenTermStandardness (T Conv pair q delta z0)
open ImportedOpenTermTransport (interp embed)
open FullPER.Application (originalP originalQ)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- A three-argument constant-one function and a two-argument constant pair. -/
def tailT : T := .k ⬝ (.k ⬝ (.k ⬝ .one))
def probeT : T := .k ⬝ (.k ⬝ pair .zero tailT)
def contextT (t : T) : T := t ⬝ probeT ⬝ .i ⬝ .i ⬝ .k

def tailP : Poly := .app (.atom .k) (.app (.atom .k) (.app (.atom .k) (.atom .one)))
def probeP : Poly := .app (.atom .k) (.app (.atom .k) (pairPoly (.atom .zero) tailP))
def contextPoly (p : Poly) : Poly :=
  .app (.app (.app (.app p probeP) (.atom .i)) (.atom .i)) (.atom .k)

theorem tail_interp (η : FullPER.Env) : interp tailP η = tailT := rfl
theorem probe_interp (η : FullPER.Env) : interp probeP η = probeT := rfl
theorem context_interp (p : Poly) (η : FullPER.Env) :
    interp (contextPoly p) η = contextT (interp p η) := rfl

theorem probe_twoargs (f a : T) : Conv (probeT ⬝ f ⬝ a) (pair .zero tailT) :=
  (Conv.app (.k (.k ⬝ pair .zero tailT) f) (.refl a)).trans (.k _ a)

theorem tail_threeargs (a b c : T) : Conv (tailT ⬝ a ⬝ b ⬝ c) .one :=
  (Conv.app (Conv.app (.k (.k ⬝ (.k ⬝ .one)) a) (.refl b)) (.refl c)).trans
    ((Conv.app (.k (.k ⬝ .one) b) (.refl c)).trans (.k .one c))

theorem q_probe : Conv (q ⬝ probeT) tailT :=
  (OpenTermStandardness.q_application probeT).trans
    ((OpenTermStandardness.snd_congr (probe_twoargs delta z0)).trans
      (OpenTermStandardness.snd_pair .zero tailT))

theorem left_context : Conv (contextT .i) .zero :=
  (Conv.app (Conv.app (Conv.app (.i probeT) (.refl .i)) (.refl .i)) (.refl .k)).trans
    ((Conv.app (probe_twoargs .i .i) (.refl .k)).trans
      (OpenTermStandardness.fst_pair .zero tailT))

theorem right_context : Conv (contextT q) .one :=
  (Conv.app (Conv.app (Conv.app q_probe (.refl .i)) (.refl .i)) (.refl .k)).trans
    (tail_threeargs .i .i .k)

/-- The original frozen endpoints, not replacements chosen up to typed equality. -/
theorem original_left (η : FullPER.Env) :
    Conv (contextT (interp originalP η)) .zero := by
  rw [FullPER.Application.originalP_eval]
  exact left_context

theorem original_right (η : FullPER.Env) :
    Conv (contextT (interp originalQ η)) .one := by
  rw [FullPER.Application.originalQ_eval]
  exact right_context

/-- Source conversion certificates for the exact literal one-hole context. -/
theorem source_left : PolyConvPlus (contextPoly originalP) (.atom .zero) :=
  ClosedScalarInstances.generic_conversion_reflect (original_left T.var)

theorem source_right : PolyConvPlus (contextPoly originalQ) (.atom .one) :=
  ClosedScalarInstances.generic_conversion_reflect (original_right T.var)

/-- A minimal fragment required of an applicative, conversion-saturated Raw
relation with the unchanged source atoms. No full semantic model is postulated. -/
structure CompatibleRaw (R : T → T → Prop) : Prop where
  saturated : ∀ {x y x' y'}, Conv x x' → Conv y y' → R x y → R x' y'
  application : ∀ {f g a b}, R f g → R a b → R (f ⬝ a) (g ⬝ b)
  i : R .i .i
  k : R .k .k
  s : R .s .s
  zero : R .zero .zero
  one : R .one .one

theorem CompatibleRaw.tail {R} (h : CompatibleRaw R) : R tailT tailT :=
  h.application h.k (h.application h.k (h.application h.k h.one))

theorem CompatibleRaw.pair {R} (h : CompatibleRaw R) {a b}
    (ha : R a a) (hb : R b b) : R (pair a b) (pair a b) :=
  h.application (h.application h.s
    (h.application (h.application h.s h.i) (h.application h.k ha))) (h.application h.k hb)

theorem CompatibleRaw.probe {R} (h : CompatibleRaw R) : R probeT probeT :=
  h.application h.k (h.application h.k (h.pair h.zero h.tail))

theorem CompatibleRaw.context {R} (h : CompatibleRaw R) {p q}
    (hpq : R p q) : R (contextT p) (contextT q) :=
  h.application (h.application (h.application (h.application hpq h.probe) h.i) h.i) h.k

/-- The proposed relation cannot identify these endpoints while separating the
inert constants. This obstruction already uses a tiny Raw fragment. -/
theorem endpoint_identification_collapses_constants {R} (h : CompatibleRaw R)
    (η : FullPER.Env) (hpq : R (interp originalP η) (interp originalQ η)) :
    R .zero .one :=
  h.saturated (original_left η) (original_right η) (h.context hpq)

theorem no_discriminating_raw_identification {R} (h : CompatibleRaw R)
    (hne : ¬ R .zero .one) (η : FullPER.Env) :
    ¬ R (interp originalP η) (interp originalQ η) :=
  fun hpq => hne (endpoint_identification_collapses_constants h η hpq)

/-- The discriminator's probe is a Raw test, not a Church-typed iterator input. -/
theorem probe_not_church : ¬ OpenTermStandardness.Church probeT := by
  intro hp
  obtain ⟨k,hk⟩ := OpenTermStandardness.church_standard _ hp
  have hn : OpenDevelopments.Normal (pair .zero tailT) :=
    OpenDevelopments.redexFree_normal (NonstandardRejection.normalB_sound (by rfl))
  have he := OpenDevelopments.normal_unique hn (OpenDevelopments.iter_normal k)
    ((probe_twoargs (.var 1) (.var 0)).symm.trans (hk (.var 1) (.var 0)))
  have hr := OpenDevelopments.readIteration_iter k
  rw [← he] at hr
  contradiction

theorem probe_not_N : ¬ JointCompletion.HasJ [] probeP P01AC.EffectiveCompleteness.N :=
  fun h => probe_not_church (JointCompletion.EffectiveNumerals.closed_church h)

#print axioms source_left
#print axioms source_right
#print axioms endpoint_identification_collapses_constants
#print axioms no_discriminating_raw_identification
#print axioms probe_not_church
#print axioms probe_not_N
end OriginalRawSeparator
