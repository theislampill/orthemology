/- Complete canonical observations and finite negative evidence on the typed domain. -/
import EffectiveBooleanStandardness
namespace P01AC.BooleanIdentity
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC.EffectiveCompleteness P01AC.IdentityComplexity

def CB : Ty := arr N B

def BoolValid (p q : Poly) : Prop := ∀ ρ, F CB ρ zeroEnv (eval p zeroEnv) (eval q zeroEnv)
def observationAt (p : Poly) (n : Nat) : Term := observe (.app (eval p zeroEnv) (canonical n))
def BoolTests (p q : Poly) : Prop := ∀ n, Conv (observationAt p n) (observationAt q n)

theorem output_self {p : Poly} (hp : Has [] p CB) (n : Nat) (ρ : OEnv) :
    F B ρ zeroEnv (.app (eval p zeroEnv) (canonical n)) (.app (eval p zeroEnv) (canonical n)) := by
  have h := unary_fundamental hp (ρ := ρ) ⟨rfl, rfl⟩
  rw [CB, F_arr] at h
  exact h _ _ (canonical_self n ρ)

theorem bool_valid_iff_tests {p q : Poly} (hp : Has [] p CB) (hq : Has [] q CB) :
    BoolValid p q ↔ BoolTests p q := by
  constructor
  · intro h n
    have hv := h (fun _ => rawPER)
    rw [CB, F_arr] at hv
    exact boolean_observation (hv _ _ (canonical_self n _))
  · intro tests ρ
    rw [CB, F_arr]
    intro x y hxy
    have nlaws := ((form_sound (N_form Ctx.nil)).2.laws.per
      (ρ := ρ) (η := zeroEnv) (show D [] ρ zeroEnv from rfl))
    have blaws := ((form_sound (B_form Ctx.nil)).2.laws.per
      (ρ := ρ) (η := zeroEnv) (show D [] ρ zeroEnv from rfl))
    have hx := nlaws.left hxy
    obtain ⟨n, hn⟩ := semantic_church_standardness hx
    have hxc : F N ρ zeroEnv x (canonical n) :=
      same_index_related hx (canonical_self n ρ) hn (fun f a => inputNumeral_applied n f a zeroEnv)
    have hcy := nlaws.trans (nlaws.sym hxc) hxy
    have hpF := unary_fundamental hp (ρ := ρ) ⟨rfl, rfl⟩
    have hqF := unary_fundamental hq (ρ := ρ) ⟨rfl, rfl⟩
    rw [CB, F_arr] at hpF hqF
    have hm := (boolean_related_iff_observation (output_self hp n ρ) (output_self hq n ρ)).mpr (tests n)
    exact blaws.trans (hpF x (canonical n) hxc) (blaws.trans hm (hqF (canonical n) y hcy))

def Mismatch (p q : Poly) : Prop := ∃ n b c, b ≠ c ∧
  Conv (observationAt p n) (pick b .zero .one) ∧
  Conv (observationAt q n) (pick c .zero .one)

/-- A finite input plus two finite conversion certificates completely certify
    inequality within the closed current-typed endpoint domain. -/
theorem invalid_iff_mismatch {p q : Poly} (hp : Has [] p CB) (hq : Has [] q CB) :
    ¬ BoolValid p q ↔ Mismatch p q := by
  classical
  constructor
  · intro h
    have hex : ∃ n, ¬ Conv (observationAt p n) (observationAt q n) := by
      apply Classical.byContradiction
      intro hno
      apply h
      apply (bool_valid_iff_tests hp hq).mpr
      intro n
      apply Classical.byContradiction
      intro hn
      exact hno ⟨n, hn⟩
    obtain ⟨n, hn⟩ := hex
    obtain ⟨b, hb⟩ := boolean_standardness (output_self hp n (fun _ => rawPER))
    obtain ⟨c, hc⟩ := boolean_standardness (output_self hq n (fun _ => rawPER))
    refine ⟨n, b, c, ?_, hb .zero .one, hc .zero .one⟩
    intro e
    apply hn
    exact (hb .zero .one).trans (e ▸ (hc .zero .one).symm)
  · rintro ⟨n, b, c, hbc, hb, hc⟩ hv
    have ht := (bool_valid_iff_tests hp hq).mp hv n
    exact hbc (pick_conv_injective (hb.symm.trans (ht.trans hc)))


end P01AC.BooleanIdentity
