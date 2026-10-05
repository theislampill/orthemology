/- The joined arbitrary-typed/dependent/impredicative witnesses and open replacements. -/
import AllInheritedNegativeControls
import AllNucleusSyntax
namespace P01AC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

def Qbody : Ty := .pi (.param 0) (.sigma (.param 0) (.identity (.param 0) (.var 1) (.var 0)))
def Q : Ty := .all Qbody
def q : Poly := abstract (pairPoly (.var 0) (.atom .i))

theorem Qbody_form : Form [] Qbody := typed_pair_abstraction_form
theorem q_body_has : Has [] q Qbody := typed_pair_abstraction_has
theorem Q_form : Form [] Q := .all .nil Qbody_form
theorem q_has_Q : Has [] q Q := .allIntro Q_form q_body_has

theorem Q_self_exact : tinst Qbody Q = .pi Q (.sigma Q (.identity Q (.var 1) (.var 0))) := rfl

theorem q_self_has : Has [] q (.pi Q (.sigma Q (.identity Q (.var 1) (.var 0)))) := by
  rw [← Q_self_exact]
  exact .allElim Q_form Q_form (form_tinst Qbody_form Q_form) q_has_Q

theorem q_self_fundamental : Fundamental [] q (.pi Q (.sigma Q (.identity Q (.var 1) (.var 0)))) :=
  fundamental q_self_has

def polyIdentity : Ty := .all (arr (.param 0) (.param 0))

theorem polyIdentity_form {Γ} (hc : Ctx Γ) : Form Γ polyIdentity :=
  .all hc (form_arr (.param (ctx_twk hc)) (.param (ctx_twk hc)))

theorem polyIdentity_has {Γ} (hc : Ctx Γ) : Has Γ (.atom .i) polyIdentity :=
  .allIntro (polyIdentity_form hc) (.i (.param (ctx_twk hc))
    (form_arr (.param (ctx_twk hc)) (.param (ctx_twk hc))))

theorem polyIdentity_instance_exact (A : Ty) : tinst (arr (.param 0) (.param 0)) A = arr A A := by
  rw [tinst,tsubst_arr]; rfl

theorem polymorphic_identity_at {Γ A} (hA : Form Γ A) : Has Γ (.atom .i) (arr A A) := by
  rw [← polyIdentity_instance_exact A]
  have hc := form_ctx hA
  exact .allElim (polyIdentity_form hc) hA
    (form_tinst (form_arr (.param (ctx_twk hc)) (.param (ctx_twk hc))) hA) (polyIdentity_has hc)

def openIdentityReplacement : Ty := .identity alpha (.var 1) (.var 0)

theorem open_identity_replacement_form : Form [alpha,alpha] openIdentityReplacement := by
  have hc : Ctx [alpha,alpha] := .ext (.ext .nil (.param .nil)) (.param (.ext .nil (.param .nil)))
  exact .identity (.param hc) (.var (.param hc) (.succ .zero)) (.var (.param hc) .zero)

theorem open_identity_replacement_instance :
    Has [alpha,alpha] (.atom .i) (arr openIdentityReplacement openIdentityReplacement) :=
  polymorphic_identity_at open_identity_replacement_form

/-- The Sigma replacement depends on the existing outer variable and is inhabited. -/
theorem open_sigma_replacement_instance : Has [alpha] (.atom .i) (arr typedPairType typedPairType) :=
  polymorphic_identity_at typed_pair_form

theorem open_sigma_replacement_nonempty : Has [alpha] typedPair typedPairType := typed_pair_has

/-- The dependent replacement's Link can relate unequal, non-source-convertible
    outer variables, while retaining their two separate endpoint conditions. -/
theorem open_sigma_replacement_heterogeneous (ρ : OEnv) :
    G typedPairType (diagEnv (identityParameters ρ)) (cons .i zeroEnv) (cons skk zeroEnv)
      (pairTerm .i .i) (pairTerm skk .i) ∧ ¬ Conv .i skk :=
  typed_pair_I_SKK_control ρ

/-- Both kinds of binder protect the free outer term in the nonempty replacement. -/
theorem open_sigma_nested_capture :
    tsubst (cons typedPairType Ty.param) (.all (.pi .raw (.param 1))) =
      .all (.pi .raw (.sigma (.param 1) (.identity (.param 1) (.var 2) (.var 0)))) := rfl

/-- Raw specialization supplies visibly distinct nonempty dependent fibres. -/
theorem open_raw_sigma_instance : Has [.raw] (.atom .i) (arr rawFibreType rawFibreType) :=
  polymorphic_identity_at raw_fibre_form

theorem open_raw_sigma_nonempty_vary (ρ : OEnv) :
    F rawFibreType ρ (cons .i zeroEnv) (pairTerm .i .i) (pairTerm .i .i) ∧
    F rawFibreType ρ (cons skk zeroEnv) (pairTerm skk .i) (pairTerm skk .i) ∧
    ¬ F rawFibreType ρ (cons skk zeroEnv) (pairTerm .i .i) (pairTerm .i .i) :=
  raw_fibres_nonempty_and_vary ρ

end P01AC
