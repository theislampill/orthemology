/- Discriminating syntax controls and reusable source certificates. -/
import SubstitutionAdmissibility
import P01CanonicalCarrierProjection

namespace P01DF.Syntactic.Controls
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

theorem abstract_atom (t : Term) : abstract (.atom t) = .app (.atom .k) (.atom t) := by
  rw [abstract_absent _ (by rfl)]
  rfl

theorem substitute_abstract_atom (t : Term) (σ : Nat → Poly) :
    psub σ (abstract (.atom t)) = abstract (.atom t) := by
  rw [abstract_atom]
  rfl

def rawShift : Nat → Poly := fun n => .var (n+1)
def openImages : Nat → Poly := fun n => .app (.var (n+1)) (.var 0)
def dependentImages : Nat → Ty := fun n => .arrow (.param n) (.identity (.var 0) (.atom .i))

 theorem raw_binder_capture_avoided :
    substIndex rawShift (.pi (.identity (.var 0) (.var 1))) =
      .pi (.identity (.var 0) (.var 2)) := rfl

 theorem unlifted_raw_binder_is_wrong :
    substIndex rawShift (.pi (.identity (.var 0) (.var 1))) ≠
      .pi (substIndex rawShift (.identity (.var 0) (.var 1))) := by decide

 theorem retained_two_sort_control :
    substType (fun _ => .arrow (.param 0) (.identity (.var 0) (.atom .i)))
      (.all (.pi (.param 1))) =
      .all (.pi (.arrow (.param 1) (.identity (.var 1) (.atom .i)))) :=
  P01DF.two_sort_substitution_control

def openTwoSort : Ty := .all (.pi (.arrow (.param 1)
  (.arrow (.identity (.var 0) (.var 1)) (.param 1))))

def insertedTwoSort : Ty := .arrow (.param 1) (.identity (.var 1) (.atom .i))

 theorem open_two_sort_typed : Has (abstract (.atom .k)) openTwoSort :=
  .allIntro (.piIntro (.k (.param 1) (.identity (.var 0) (.var 1))))

 theorem open_two_sort_index_certificate :
    Has (abstract (.atom .k))
      (.all (.pi (.arrow (.param 1)
        (.arrow (.identity (.var 0) (.app (.var 2) (.var 1))) (.param 1))))) := by
  simpa only [substitute_abstract_atom] using
    has_index_substitution open_two_sort_typed openImages

 theorem open_two_sort_type_certificate :
    Has (abstract (.atom .k))
      (.all (.pi (.arrow insertedTwoSort
        (.arrow (.identity (.var 0) (.var 1)) insertedTwoSort)))) := by
  exact has_type_substitution open_two_sort_typed dependentImages

 theorem open_two_sort_mixed_certificate :
    Has (abstract (.atom .k))
      (substType (fun n => substIndex openImages (dependentImages n))
        (substIndex openImages openTwoSort)) := by
  simpa only [substitute_abstract_atom] using
    has_mixed_substitution open_two_sort_typed openImages dependentImages

def captureImages : Nat → Ty := cons .raw (cons (.param 0) Ty.param)

 theorem earlier_image_survives_later_elimination :
    instantiateType
      (substType (liftTypes (finitePrefix 1 (fun k => captureImages (k+1))))
        (.arrow (.param 0) (.param 1)))
      (captureImages 0) = .arrow .raw (.param 0) := rfl

 theorem capture_replacement_is_not_recursive :
    substType (finitePrefix 2 captureImages) (.arrow (.param 0) (.param 1)) ≠
      .arrow .raw .raw := by decide

 theorem open_image_certificate :
    Has (.atom .k) (.arrow .raw (.arrow (.param 0) .raw)) := by
  exact has_type_substitution (Has.k (.param 0) (.param 1)) captureImages

 theorem incorrect_mixed_commutation :
    substIndex (fun _ => .atom .i)
      (substType (fun _ => .identity (.var 0) (.var 0)) (.param 0)) ≠
    substType (fun _ => .identity (.var 0) (.var 0))
      (substIndex (fun _ => .atom .i) (.param 0)) := by decide

 theorem correct_mixed_square (A : Ty) (σ : Nat → Poly) (τ : Nat → Ty) :
    substIndex σ (substType τ A) =
      substType (fun n => substIndex σ (τ n)) (substIndex σ A) :=
  index_type_interchange A σ τ

/-- All three coordinates occur in the actual motive tree. -/
def threeCoordinateMotive : Ty :=
  .arrow (.identity (.var 0) (.var 1)) (.identity (.var 2) (.var 2))
def jEndpoint : Poly := .app (.atom .i) (.var 0)
def jProof : Poly := .app (.atom .i) (.atom .i)
def jBase : Poly := .app (.atom .k) (.atom .i)

 theorem three_coordinate_j_typed :
    Has (jPoly jBase jEndpoint jProof) (motiveAt threeCoordinateMotive jEndpoint jProof) := by
  apply Has.j (x := .var 0)
  · exact .conv (.identityIntro (.symm (.i (.var 0)))) (.symm (.i (.atom .i)))
  · exact .app (.k (.identity (.var 0) (.var 0)) (.identity (.atom .i) (.var 0)))
      (.identityIntro (.refl (.var 0)))

 theorem three_coordinate_j_substitution (σ : Nat → Poly) :
    Has (jPoly (psub σ jBase) (psub σ jEndpoint) (psub σ jProof))
      (motiveAt (substIndex (pup (pup σ)) threeCoordinateMotive)
        (psub σ jEndpoint) (psub σ jProof)) := by
  simpa only [polynomial_j, index_motiveAt] using
    has_index_substitution three_coordinate_j_typed σ

 theorem double_lift_retains_coordinates :
    substIndex (pup (pup openImages)) threeCoordinateMotive =
      .arrow (.identity (.var 0) (.var 1))
        (.identity (.app (.var 3) (.var 2)) (.app (.var 3) (.var 2))) := rfl

 theorem one_lift_is_wrong_for_j :
    substIndex (pup (pup openImages)) threeCoordinateMotive ≠
      substIndex (pup openImages) threeCoordinateMotive := by decide

 theorem proof_coordinate_is_not_endpoint :
    motiveAt threeCoordinateMotive jEndpoint jProof ≠
      motiveAt threeCoordinateMotive jEndpoint jEndpoint := by decide

 theorem outer_coordinate_is_not_bound_endpoint :
    substIndex (pup (pup openImages)) threeCoordinateMotive ≠
      .arrow (.identity (.var 0) (.var 1)) (.identity (.var 1) (.var 1)) := by decide

def openSigmaBody : Ty := .identity (.var 0) (.var 1)
def openSigma : Ty := .sigma openSigmaBody
def openPair : Poly := pairPoly (.var 0) (.atom .i)

 theorem open_pair_typed : Has openPair openSigma :=
  .sigmaIntro (.identityIntro (.refl (.var 0)))

 theorem source_changing_sigma_certificate (σ : Nat → Poly) :
    Has (pairPoly (σ 0) (.atom .i))
      (.sigma (.identity (.var 0) (pren Nat.succ (σ 0)))) := by
  exact has_index_substitution open_pair_typed σ

 theorem pair_source_really_changes : psub openImages openPair ≠ openPair := by decide

 theorem substituted_sigma_projection (σ : Nat → Poly) :
    Has (sndPoly (pairPoly (σ 0) (.atom .i)))
      (instantiate (.identity (.var 0) (pren Nat.succ (σ 0)))
        (fstPoly (pairPoly (σ 0) (.atom .i)))) :=
  .sigmaSnd (source_changing_sigma_certificate σ)

 theorem opaque_finite_input :
    Has (.atom P01R.skk)
      (.arrow (.arrow (.param 0) (.param 1)) (.arrow (.param 0) (.param 1))) :=
  .finite (P01R.finite_skk_identity (.arrow (.var 0) (.var 1)))

 theorem opaque_finite_dependent_certificate :
    Has (.atom P01R.skk)
      (.arrow (.arrow openSigma dependentPolyType) (.arrow openSigma dependentPolyType)) := by
  exact has_type_substitution opaque_finite_input
    (cons openSigma (cons dependentPolyType Ty.param))

 theorem opaque_atom_stays_distinct_from_polynomial_application :
    Poly.atom P01R.skk ≠ .app (.app (.atom .s) (.atom .k)) (.atom .k) := by decide

def acceptedPolymorphicProgram : Poly := abstract (.atom .k)
def constantDependentProgram : Poly := .app (.atom .k) acceptedPolymorphicProgram

def composedProgram : Poly :=
  .app (.app (.atom P01R.skk) constantDependentProgram) openPair

 theorem constant_dependent_certificate :
    Has constantDependentProgram (.arrow openSigma dependentPolyType) :=
  .app (.k dependentPolyType openSigma) dependent_polymorphic_typed

 theorem composed_certificate : Has composedProgram dependentPolyType :=
  .app (.app opaque_finite_dependent_certificate constant_dependent_certificate) open_pair_typed

 theorem composed_substituted_certificate (σ : Nat → Poly) :
    Has (psub σ composedProgram) dependentPolyType := by
  exact has_index_substitution composed_certificate σ

 theorem composed_program_really_changes :
    psub openImages composedProgram ≠ composedProgram := by
  simp only [composedProgram, constantDependentProgram, acceptedPolymorphicProgram, abstract_atom]
  decide

 theorem reused_open_all_certificate (σ : Nat → Poly) (τ : Nat → Ty) :
    Has (psub σ (abstract (.atom .k)))
      (substType (fun n => substIndex σ (τ n)) (substIndex σ openTwoSort)) :=
  has_mixed_substitution open_two_sort_typed σ τ

 theorem envelope_keeps_substituted_source (σ : Nat → Poly) (ρ : OEnv) :
    (candidateEnvelope (has_index_substitution composed_certificate σ) ρ).checked.code =
      psub σ composedProgram := rfl

 theorem sigma_reuses_scoped_canonical_admission (σ : Nat → Poly) (ρ : OEnv) (η : Env) :
    (dependentSigma Code.top
      (projectedBody ρ η (.identity (.var 0) (pren Nat.succ (σ 0))))).accepts
      (eval (pairPoly (σ 0) (.atom .i)) η) :=
  canonical_sigma_admission (source_changing_sigma_certificate σ) ρ η

end P01DF.Syntactic.Controls
