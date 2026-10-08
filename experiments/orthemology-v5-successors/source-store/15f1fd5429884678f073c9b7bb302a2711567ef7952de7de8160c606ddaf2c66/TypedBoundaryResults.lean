/- Public law packaging and preserved boundary statements. -/
import TypedNegativeControls
namespace P01TC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

def formedObject {Γ A} (hA : Form Γ A) (ρ : OEnv) (η : Env) (d : D Γ ρ η) : PER :=
  objectOf (form_sound hA).2.laws d

def formedLink {Γ A} (hA : Form Γ A) (r : REnv) (η ξ : Env) (h : H Γ r η ξ) :
    Link (formedObject hA r.left η ((form_sound hA).1.hends h).1)
      (formedObject hA r.right ξ ((form_sound hA).1.hends h).2) :=
  linkOf (form_sound hA).2.laws ((form_sound hA).1.hends h).1 ((form_sound hA).1.hends h).2

theorem formedObject_rel {Γ A} (hA : Form Γ A) (ρ : OEnv) (η : Env) (d : D Γ ρ η) (t u : Term) :
    (formedObject hA ρ η d).rel t u ↔ F A ρ η t u := Iff.rfl

theorem formedLink_rel {Γ A} (hA : Form Γ A) (r : REnv) (η ξ : Env) (h : H Γ r η ξ) (t u : Term) :
    (formedLink hA r η ξ h).rel t u ↔ G A r η ξ t u := Iff.rfl

theorem context_two_sided_invariance {Γ} (hΓ : Ctx Γ) {r η η' ξ ξ'}
    (e : E Γ r.left η η') (f : E Γ r.right ξ ξ') : H Γ r η ξ ↔ H Γ r η' ξ' :=
  ⟨(context_sound hΓ).hrespect e f,
    (context_sound hΓ).hrespect ((context_sound hΓ).sym e) ((context_sound hΓ).sym f)⟩

theorem context_strong_diagonal {Γ} (hΓ : Ctx Γ) {ρ η ξ} : H Γ (diagEnv ρ) η ξ ↔ E Γ ρ η ξ :=
  (context_sound hΓ).diagonal

noncomputable def formedFibre {Γ A B} (_hA : Form Γ A) (hB : Form (A :: Γ) B)
    (ρ : OEnv) (η : Env) (d : D Γ ρ η) (a : Term) : PER := by
  classical
  exact if h : F A ρ η a a then formedObject hB ρ (cons a η) ⟨d,h⟩ else botPER

theorem formedFibre_coherent {Γ A B} (hA : Form Γ A) (hB : Form (A :: Γ) B)
    (ρ : OEnv) (η : Env) (d : D Γ ρ η) {a b} (h : (formedObject hA ρ η d).rel a b) :
    formedFibre hA hB ρ η d a = formedFibre hA hB ρ η d b := by
  classical
  have aa : F A ρ η a a := PER.left h
  have bb : F A ρ η b b := PER.right h
  simp only [formedFibre,dif_pos aa,dif_pos bb]
  apply per_ext
  exact (form_sound hB).2.laws.transport ⟨(form_sound hA).1.refl d,h⟩

theorem formed_pi_exact {Γ A B} (hA : Form Γ A) (hB : Form (A :: Γ) B)
    (ρ : OEnv) (η : Env) (d : D Γ ρ η) :
    formedObject (.pi hA hB) ρ η d =
      PiPER (formedObject hA ρ η d) (formedFibre hA hB ρ η d)
        (formedFibre_coherent hA hB ρ η d) := by
  classical
  apply per_ext
  intro f g
  constructor
  · intro h a b ab
    have aa : F A ρ η a a := PER.left ab
    change (formedFibre hA hB ρ η d a).rel _ _
    simp only [formedFibre,dif_pos aa]
    exact h a b ab
  · intro h a b ab
    have aa : F A ρ η a a := (form_sound hA).2.laws.per d |>.left ab
    have v := h a b ab
    simpa only [formedFibre,dif_pos aa] using v

theorem formed_sigma_exact {Γ A B} (hA : Form Γ A) (hB : Form (A :: Γ) B)
    (ρ : OEnv) (η : Env) (d : D Γ ρ η) :
    formedObject (.sigma hA hB) ρ η d =
      SigmaPER (formedObject hA ρ η d) (formedFibre hA hB ρ η d)
        (formedFibre_coherent hA hB ρ η d) := by
  classical
  apply per_ext
  intro z w
  constructor
  · intro h
    refine ⟨h.1,h.2.1,h.2.2.1,?_⟩
    have aa := ((form_sound hA).2.laws.per d).left h.2.2.1
    change (formedFibre hA hB ρ η d (firstTerm z)).rel _ _
    simp only [formedFibre,dif_pos aa]
    exact h.2.2.2
  · intro h
    have aa : F A ρ η (firstTerm z) (firstTerm z) := PER.left h.2.2.1
    refine ⟨h.1,h.2.1,h.2.2.1,?_⟩
    simpa only [formedFibre,dif_pos aa] using h.2.2.2

theorem formed_identity_exact {Γ A p q} (hA : Form Γ A) (hp : Has Γ p A) (hq : Has Γ q A)
    (ρ : OEnv) (η : Env) (d : D Γ ρ η) :
    formedObject (.identity hA hp hq) ρ η d = IdPER (formedObject hA ρ η d) (eval p η) (eval q η) :=
  per_ext (fun _ _ => Iff.rfl)

theorem raw_omega_typed : Has [] (.atom omega) .raw := .rawAtom (.raw .nil)
theorem raw_omega_has_no_normal_reduct : ∀ u, Red omega u → ¬ P01Source.Normal u :=
  fun _ h => P01Source.omega_no_normal_reduct h

end P01TC
