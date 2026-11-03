/- Exact load-bearing type assertions. They must elaborate at the pinned compiler
   before any kernel credit. These are not assertions made by the Python runner. -/
import P01GeneratedExports
import P01ReflectionCountermodel
import P01UniverseBoundary
namespace P01TypeAssertions
open OrthemologyV2 OrthemologyV3

theorem bridge_subject_reduction : ∀ (Γ : P01F.Context) (t u : P01F.LTerm) (A : TypeCode),
    P01F.Has Γ t A → P01F.Beta t u → P01F.Has Γ u A :=
  fun _ _ _ _ h r => P01F.subject_reduction h r

theorem bridge_typing : ∀ t A, FiniteDerives t A → ∀Γ : P01F.Context,
    P01F.Has Γ (P01F.translate t) A := fun _ _ h Γ => P01F.typing_preservation h Γ

theorem bridge_nonempty : ∀t u, Step t u →
    ∃m, P01F.Beta (P01F.translate t) m ∧ P01F.BStar m (P01F.translate u) :=
  fun _ _ h => P01F.step_simulation h

theorem direct_normalisation : ∀t A, FiniteDerives t A → StronglyNormalising t :=
  fun _ _ h => P01Candidates.finite_SN h

theorem raw_source_confluence : ∀t u v, Red t u → Red t v → ∃w, Red u w ∧ Red v w :=
  fun _ _ _ h k => P01Source.confluence h k

theorem typed_conversion : ∀t u n m, Red t n → Red u m →
    P01Source.Normal n → P01Source.Normal m → (Conv t u ↔ n = m) :=
  fun _ _ _ _ ht hu hn hm => P01Source.conversion_by_normal_forms ht hu hn hm

theorem exact_nonrepresentability : ¬∃u A, FiniteDerives u A ∧ Conv omega u :=
  P01Source.omega_no_finite_representative

theorem no_target_reflection : ¬(∀t u, P01F.BConv (P01F.translate t) (P01F.translate u) → Conv t u) :=
  P01F.target_conversion_reflection_false

theorem code_bound_intrinsic_soundness : ∀(Γ : P01D.Context) (A : P01D.Ty Γ) (p : P01D.Poly),
    P01Certificate.DependentEnvelope Γ A p → ∀γ δ, Γ.eqv γ δ →
    (A.obj γ).rel (P01D.eval p (Γ.environment γ)) (P01D.eval p (Γ.environment δ)) :=
  fun _ _ _ e _ _ h => P01Certificate.dependent_envelope_sound e h

theorem all_new_identity_extension : ∀(F : P01D.ParamFamily) t u,
    (P01D.AllDiagonal F).rel t u ↔ (P01D.AllPER F).rel t u :=
  P01D.all_identity_extension

theorem j_two_coordinate_transport : ∀(P : P01D.PER) x (M : P01D.BasedMotive P x) y p d e,
    (P01D.IdPER P x y).dom p → (M.fibre x .i).rel d e →
    (M.fibre y p).rel (P01D.Jterm d y p) (P01D.Jterm e y p) :=
  fun _ _ M _ _ _ _ h hd => P01D.based_J M h hd
end P01TypeAssertions
