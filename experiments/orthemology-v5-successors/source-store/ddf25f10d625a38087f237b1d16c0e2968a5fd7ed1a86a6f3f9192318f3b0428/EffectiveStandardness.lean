/- Original F/G Church standardness, with no syntactic-input or MarkerFree premise. -/
import AllInheritedPositiveControls
namespace P01AC.EffectiveCompleteness
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC

def NBody : Ty := arr (arr (.param 0) (.param 0)) (arr (.param 0) (.param 0))
def N : Ty := .all NBody

def orbitLink (f x : Term) : Link rawPER rawPER where
  rel := fun a b => ∃ n, Conv a (iterateTerm .zero n .one) ∧ Conv b (iterateTerm f n x)
  endpoints := fun _ => ⟨.refl _, .refl _⟩
  respect := by
    intro a a' b b' ha hb h
    obtain ⟨n, hn, hm⟩ := h
    exact ⟨n, ha.symm.trans hn, hb.symm.trans hm⟩

theorem marker_normal (n : Nat) : P01Source.Normal (iterateTerm .zero n .one) := by
  induction n with
  | zero => intro u h; cases h
  | succ n ih =>
    intro u h
    cases h with
    | left h _ => cases h
    | right _ h => exact ih _ h

theorem marker_injective {m n : Nat}
    (h : iterateTerm .zero m .one = iterateTerm .zero n .one) : m = n := by
  induction m generalizing n with
  | zero => cases n with
    | zero => rfl
    | succ n => cases h
  | succ m ih => cases n with
    | zero => cases h
    | succ n => exact congrArg Nat.succ (ih (Term.app.inj h).2)

theorem marker_conv_injective {m n : Nat}
    (h : Conv (iterateTerm .zero m .one) (iterateTerm .zero n .one)) : m = n :=
  marker_injective (P01Source.normal_unique (marker_normal m) (marker_normal n) h)

theorem graph_application {t : Term} {ρ : OEnv} {η : Env}
    (ht : F N ρ η t t) (f x : Term) :
    ∃ n, Conv (.app (.app t .zero) .one) (iterateTerm .zero n .one) ∧
      Conv (.app (.app t f) x) (iterateTerm f n x) := by
  have h := ht.1 rawPER rawPER (orbitLink f x)
  change G NBody (extendEnv (orbitLink f x) (diagEnv ρ)) η η t t at h
  rw [NBody, G_arr] at h
  have hs : G (arr (.param 0) (.param 0))
      (extendEnv (orbitLink f x) (diagEnv ρ)) η η .zero f := by
    rw [G_arr]
    refine ⟨?_, ?_, ?_⟩
    · intro a b hab
      exact Conv.right .zero hab
    · intro a b hab
      exact Conv.right f hab
    · intro a b hab
      obtain ⟨n, hn, hm⟩ := hab
      exact ⟨n+1, Conv.right .zero hn, Conv.right f hm⟩
  have h1 := h.2.2 .zero f hs
  rw [G_arr] at h1
  exact h1.2.2 .one x ⟨0, .refl _, .refl _⟩

/-- No MarkerFree premise; quantification is over every raw semantic inhabitant. -/
theorem semantic_church_standardness {t : Term} {ρ : OEnv} {η : Env}
    (ht : F N ρ η t t) :
    ∃ n, ∀ f x, Conv (.app (.app t f) x) (iterateTerm f n x) := by
  obtain ⟨n, hn, _⟩ := graph_application ht .zero .one
  refine ⟨n, ?_⟩
  intro f x
  obtain ⟨m, hm, hout⟩ := graph_application ht f x
  have e : m = n := marker_conv_injective (hm.symm.trans hn)
  exact e ▸ hout

end P01AC.EffectiveCompleteness

