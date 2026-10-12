/- Completeness is proved by actual mutual source-derivation induction.
Finite formation families become literal finite child lists; no proof object,
choice oracle, or derivability predicate is stored in a certificate. -/
import CertificateRules
namespace JointCertificates
set_option maxRecDepth 32768
set_option maxHeartbeats 32000000
set_option linter.unusedVariables false

theorem e_ctx_complete {Γ : P01AC.Tel} (h : P01AC.ExtensionalRepair.CtxE Γ) :
    Proved (.ctxE Γ) := by
  induction h using P01AC.ExtensionalRepair.CtxE.rec
    (motive_2 := fun Γ A _ => Proved (.formE Γ A))
    (motive_3 := fun Γ p A _ => Proved (.hasE Γ p A)) with
  | @nil  =>
      apply proved_rule (.CtxE_nil )
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
  | @ext Γ A pr0 pr1 ih0 ih1 =>
      apply proved_rule (.CtxE_ext Γ A)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @param Γ n pr0 ih0 =>
      apply proved_rule (.FormE_param Γ n)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @bottom Γ pr0 ih0 =>
      apply proved_rule (.FormE_bottom Γ)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @all Γ B pr0 pr1 ih0 ih1 =>
      apply proved_rule (.FormE_all Γ B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @raw Γ pr0 ih0 =>
      apply proved_rule (.FormE_raw Γ)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @pi Γ A B pr0 pr1 ih0 ih1 =>
      apply proved_rule (.FormE_pi Γ A B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @sigma Γ A B pr0 pr1 ih0 ih1 =>
      apply proved_rule (.FormE_sigma Γ A B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @identity Γ A p q pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.FormE_identity Γ A p q)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @var Γ A n pr0 pr1 ih0 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.lookup_complete pr1
      apply proved_rule (.HasE_var Γ A n aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨haux0, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @i Γ A pr0 pr1 ih0 ih1 =>
      apply proved_rule (.HasE_i Γ A)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @k Γ A B pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasE_k Γ A B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @s Γ A B C pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasE_s Γ A B C)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @finite C Γ t τ pr0 pr1 pr2 pr3 ih0 ih1 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.finite_complete pr3
      apply proved_rule (.HasE_finite C Γ t τ aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr0, haux0, True.intro⟩
      · simp only [Rule.premises, all_append, all_ofFn, All]
        exact ⟨fun i => ih0 i.val i.isLt, ⟨ih1, True.intro⟩⟩
  | @allIntro Γ B p pr0 pr1 ih0 ih1 =>
      apply proved_rule (.HasE_allIntro Γ B p)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @allElim Γ B A p pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasE_allElim Γ B A p)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @rawAtom Γ t pr0 ih0 =>
      apply proved_rule (.HasE_rawAtom Γ t)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @rawApp Γ f a pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasE_rawApp Γ f a)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @piIntro Γ A B b pr0 pr1 pr2 ih0 ih1 =>
      apply proved_rule (.HasE_piIntro Γ A B b)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr2, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @piElim Γ A B a f pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasE_piElim Γ A B a f)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @sigmaIntro Γ A B a b pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasE_sigmaIntro Γ A B a b)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @sigmaFst Γ A B z pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasE_sigmaFst Γ A B z)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @sigmaSnd Γ A B z pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasE_sigmaSnd Γ A B z)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @identityIntro Γ A p q pr0 pr1 pr2 pr3 ih0 ih1 ih2 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.poly_complete pr3
      apply proved_rule (.HasE_identityIntro Γ A p q aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨haux0, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @proofErase Γ A x y p pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasE_proofErase Γ A x y p)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @j Γ A x B y e d pr0 pr1 pr2 pr3 pr4 pr5 pr6 pr7 pr8 ih0 ih1 ih2 ih3 ih4 ih5 ih6 ih7 ih8 =>
      apply proved_rule (.HasE_j Γ A x B y e d)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, ih6, ih7, ih8, True.intro⟩
  | @conv Γ A p q pr0 pr1 pr2 pr3 ih0 ih1 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.poly_complete pr2
      apply proved_rule (.HasE_conv Γ A p q aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨haux0, pr3, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @piExt Γ A B p q h pr0 pr1 pr2 pr3 pr4 pr5 pr6 pr7 pr8 pr9 pr10 pr11 pr12 pr13 ih0 ih1 ih2 ih3 ih4 ih5 ih6 ih7 ih8 =>
      apply proved_rule (.HasE_piExt Γ A B p q h)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr9, pr10, pr11, pr12, pr13, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, ih6, ih7, ih8, True.intro⟩
  | @allExt Γ B p q h pr0 pr1 pr2 pr3 pr4 pr5 pr6 pr7 pr8 pr9 pr10 ih0 ih1 ih2 ih3 ih4 ih5 ih6 =>
      apply proved_rule (.HasE_allExt Γ B p q h)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr7, pr8, pr9, pr10, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, ih6, True.intro⟩

theorem e_form_complete {Γ : P01AC.Tel} {A : P01AC.Ty} (h : P01AC.ExtensionalRepair.FormE Γ A) :
    Proved (.formE Γ A) := by
  induction h using P01AC.ExtensionalRepair.FormE.rec
    (motive_1 := fun Γ _ => Proved (.ctxE Γ))
    (motive_3 := fun Γ p A _ => Proved (.hasE Γ p A)) with
  | @nil  =>
      apply proved_rule (.CtxE_nil )
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
  | @ext Γ A pr0 pr1 ih0 ih1 =>
      apply proved_rule (.CtxE_ext Γ A)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @param Γ n pr0 ih0 =>
      apply proved_rule (.FormE_param Γ n)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @bottom Γ pr0 ih0 =>
      apply proved_rule (.FormE_bottom Γ)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @all Γ B pr0 pr1 ih0 ih1 =>
      apply proved_rule (.FormE_all Γ B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @raw Γ pr0 ih0 =>
      apply proved_rule (.FormE_raw Γ)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @pi Γ A B pr0 pr1 ih0 ih1 =>
      apply proved_rule (.FormE_pi Γ A B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @sigma Γ A B pr0 pr1 ih0 ih1 =>
      apply proved_rule (.FormE_sigma Γ A B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @identity Γ A p q pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.FormE_identity Γ A p q)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @var Γ A n pr0 pr1 ih0 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.lookup_complete pr1
      apply proved_rule (.HasE_var Γ A n aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨haux0, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @i Γ A pr0 pr1 ih0 ih1 =>
      apply proved_rule (.HasE_i Γ A)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @k Γ A B pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasE_k Γ A B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @s Γ A B C pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasE_s Γ A B C)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @finite C Γ t τ pr0 pr1 pr2 pr3 ih0 ih1 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.finite_complete pr3
      apply proved_rule (.HasE_finite C Γ t τ aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr0, haux0, True.intro⟩
      · simp only [Rule.premises, all_append, all_ofFn, All]
        exact ⟨fun i => ih0 i.val i.isLt, ⟨ih1, True.intro⟩⟩
  | @allIntro Γ B p pr0 pr1 ih0 ih1 =>
      apply proved_rule (.HasE_allIntro Γ B p)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @allElim Γ B A p pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasE_allElim Γ B A p)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @rawAtom Γ t pr0 ih0 =>
      apply proved_rule (.HasE_rawAtom Γ t)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @rawApp Γ f a pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasE_rawApp Γ f a)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @piIntro Γ A B b pr0 pr1 pr2 ih0 ih1 =>
      apply proved_rule (.HasE_piIntro Γ A B b)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr2, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @piElim Γ A B a f pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasE_piElim Γ A B a f)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @sigmaIntro Γ A B a b pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasE_sigmaIntro Γ A B a b)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @sigmaFst Γ A B z pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasE_sigmaFst Γ A B z)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @sigmaSnd Γ A B z pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasE_sigmaSnd Γ A B z)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @identityIntro Γ A p q pr0 pr1 pr2 pr3 ih0 ih1 ih2 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.poly_complete pr3
      apply proved_rule (.HasE_identityIntro Γ A p q aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨haux0, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @proofErase Γ A x y p pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasE_proofErase Γ A x y p)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @j Γ A x B y e d pr0 pr1 pr2 pr3 pr4 pr5 pr6 pr7 pr8 ih0 ih1 ih2 ih3 ih4 ih5 ih6 ih7 ih8 =>
      apply proved_rule (.HasE_j Γ A x B y e d)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, ih6, ih7, ih8, True.intro⟩
  | @conv Γ A p q pr0 pr1 pr2 pr3 ih0 ih1 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.poly_complete pr2
      apply proved_rule (.HasE_conv Γ A p q aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨haux0, pr3, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @piExt Γ A B p q h pr0 pr1 pr2 pr3 pr4 pr5 pr6 pr7 pr8 pr9 pr10 pr11 pr12 pr13 ih0 ih1 ih2 ih3 ih4 ih5 ih6 ih7 ih8 =>
      apply proved_rule (.HasE_piExt Γ A B p q h)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr9, pr10, pr11, pr12, pr13, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, ih6, ih7, ih8, True.intro⟩
  | @allExt Γ B p q h pr0 pr1 pr2 pr3 pr4 pr5 pr6 pr7 pr8 pr9 pr10 ih0 ih1 ih2 ih3 ih4 ih5 ih6 =>
      apply proved_rule (.HasE_allExt Γ B p q h)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr7, pr8, pr9, pr10, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, ih6, True.intro⟩

theorem e_has_complete {Γ : P01AC.Tel} {p : P01D.Poly} {A : P01AC.Ty} (h : P01AC.ExtensionalRepair.HasE Γ p A) :
    Proved (.hasE Γ p A) := by
  induction h using P01AC.ExtensionalRepair.HasE.rec
    (motive_1 := fun Γ _ => Proved (.ctxE Γ))
    (motive_2 := fun Γ A _ => Proved (.formE Γ A)) with
  | @nil  =>
      apply proved_rule (.CtxE_nil )
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
  | @ext Γ A pr0 pr1 ih0 ih1 =>
      apply proved_rule (.CtxE_ext Γ A)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @param Γ n pr0 ih0 =>
      apply proved_rule (.FormE_param Γ n)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @bottom Γ pr0 ih0 =>
      apply proved_rule (.FormE_bottom Γ)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @all Γ B pr0 pr1 ih0 ih1 =>
      apply proved_rule (.FormE_all Γ B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @raw Γ pr0 ih0 =>
      apply proved_rule (.FormE_raw Γ)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @pi Γ A B pr0 pr1 ih0 ih1 =>
      apply proved_rule (.FormE_pi Γ A B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @sigma Γ A B pr0 pr1 ih0 ih1 =>
      apply proved_rule (.FormE_sigma Γ A B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @identity Γ A p q pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.FormE_identity Γ A p q)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @var Γ A n pr0 pr1 ih0 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.lookup_complete pr1
      apply proved_rule (.HasE_var Γ A n aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨haux0, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @i Γ A pr0 pr1 ih0 ih1 =>
      apply proved_rule (.HasE_i Γ A)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @k Γ A B pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasE_k Γ A B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @s Γ A B C pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasE_s Γ A B C)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @finite C Γ t τ pr0 pr1 pr2 pr3 ih0 ih1 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.finite_complete pr3
      apply proved_rule (.HasE_finite C Γ t τ aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr0, haux0, True.intro⟩
      · simp only [Rule.premises, all_append, all_ofFn, All]
        exact ⟨fun i => ih0 i.val i.isLt, ⟨ih1, True.intro⟩⟩
  | @allIntro Γ B p pr0 pr1 ih0 ih1 =>
      apply proved_rule (.HasE_allIntro Γ B p)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @allElim Γ B A p pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasE_allElim Γ B A p)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @rawAtom Γ t pr0 ih0 =>
      apply proved_rule (.HasE_rawAtom Γ t)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @rawApp Γ f a pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasE_rawApp Γ f a)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @piIntro Γ A B b pr0 pr1 pr2 ih0 ih1 =>
      apply proved_rule (.HasE_piIntro Γ A B b)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr2, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @piElim Γ A B a f pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasE_piElim Γ A B a f)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @sigmaIntro Γ A B a b pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasE_sigmaIntro Γ A B a b)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @sigmaFst Γ A B z pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasE_sigmaFst Γ A B z)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @sigmaSnd Γ A B z pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasE_sigmaSnd Γ A B z)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @identityIntro Γ A p q pr0 pr1 pr2 pr3 ih0 ih1 ih2 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.poly_complete pr3
      apply proved_rule (.HasE_identityIntro Γ A p q aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨haux0, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @proofErase Γ A x y p pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasE_proofErase Γ A x y p)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @j Γ A x B y e d pr0 pr1 pr2 pr3 pr4 pr5 pr6 pr7 pr8 ih0 ih1 ih2 ih3 ih4 ih5 ih6 ih7 ih8 =>
      apply proved_rule (.HasE_j Γ A x B y e d)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, ih6, ih7, ih8, True.intro⟩
  | @conv Γ A p q pr0 pr1 pr2 pr3 ih0 ih1 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.poly_complete pr2
      apply proved_rule (.HasE_conv Γ A p q aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨haux0, pr3, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @piExt Γ A B p q h pr0 pr1 pr2 pr3 pr4 pr5 pr6 pr7 pr8 pr9 pr10 pr11 pr12 pr13 ih0 ih1 ih2 ih3 ih4 ih5 ih6 ih7 ih8 =>
      apply proved_rule (.HasE_piExt Γ A B p q h)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr9, pr10, pr11, pr12, pr13, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, ih6, ih7, ih8, True.intro⟩
  | @allExt Γ B p q h pr0 pr1 pr2 pr3 pr4 pr5 pr6 pr7 pr8 pr9 pr10 ih0 ih1 ih2 ih3 ih4 ih5 ih6 =>
      apply proved_rule (.HasE_allExt Γ B p q h)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr7, pr8, pr9, pr10, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, ih6, True.intro⟩

theorem j_ctx_complete {Γ : P01AC.Tel} (h : JointCompletion.CtxJ Γ) :
    Proved (.ctxJ Γ) := by
  induction h using JointCompletion.CtxJ.rec
    (motive_2 := fun Γ A _ => Proved (.formJ Γ A))
    (motive_3 := fun Γ p A _ => Proved (.hasJ Γ p A)) with
  | @ctxBase Γ pr0 =>
      have base0 := e_ctx_complete pr0
      apply proved_rule (.CtxJ_ctxBase Γ)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨base0, True.intro⟩
  | @nil  =>
      apply proved_rule (.CtxJ_nil )
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
  | @ext Γ A pr0 pr1 ih0 ih1 =>
      apply proved_rule (.CtxJ_ext Γ A)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @formBase Γ A pr0 =>
      have base0 := e_form_complete pr0
      apply proved_rule (.FormJ_formBase Γ A)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨base0, True.intro⟩
  | @param Γ n pr0 ih0 =>
      apply proved_rule (.FormJ_param Γ n)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @bottom Γ pr0 ih0 =>
      apply proved_rule (.FormJ_bottom Γ)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @all Γ B pr0 pr1 ih0 ih1 =>
      apply proved_rule (.FormJ_all Γ B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @raw Γ pr0 ih0 =>
      apply proved_rule (.FormJ_raw Γ)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @pi Γ A B pr0 pr1 ih0 ih1 =>
      apply proved_rule (.FormJ_pi Γ A B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @sigma Γ A B pr0 pr1 ih0 ih1 =>
      apply proved_rule (.FormJ_sigma Γ A B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @identity Γ A p q pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.FormJ_identity Γ A p q)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @hasBase Γ p A pr0 =>
      have base0 := e_has_complete pr0
      apply proved_rule (.HasJ_hasBase Γ p A)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨base0, True.intro⟩
  | @var Γ A n pr0 pr1 ih0 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.lookup_complete pr1
      apply proved_rule (.HasJ_var Γ A n aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨haux0, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @i Γ A pr0 pr1 ih0 ih1 =>
      apply proved_rule (.HasJ_i Γ A)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @k Γ A B pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasJ_k Γ A B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @s Γ A B C pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasJ_s Γ A B C)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @finite C Γ t τ pr0 pr1 pr2 pr3 ih0 ih1 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.finite_complete pr3
      apply proved_rule (.HasJ_finite C Γ t τ aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr0, haux0, True.intro⟩
      · simp only [Rule.premises, all_append, all_ofFn, All]
        exact ⟨fun i => ih0 i.val i.isLt, ⟨ih1, True.intro⟩⟩
  | @allIntro Γ B p pr0 pr1 ih0 ih1 =>
      apply proved_rule (.HasJ_allIntro Γ B p)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @allElim Γ B A p pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasJ_allElim Γ B A p)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @rawAtom Γ t pr0 ih0 =>
      apply proved_rule (.HasJ_rawAtom Γ t)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @rawApp Γ f a pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasJ_rawApp Γ f a)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @piIntro Γ A B b pr0 pr1 pr2 ih0 ih1 =>
      apply proved_rule (.HasJ_piIntro Γ A B b)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr2, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @piElim Γ A B a f pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasJ_piElim Γ A B a f)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @sigmaIntro Γ A B a b pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasJ_sigmaIntro Γ A B a b)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @sigmaFst Γ A B z pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasJ_sigmaFst Γ A B z)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @sigmaSnd Γ A B z pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasJ_sigmaSnd Γ A B z)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @identityIntro Γ A p q pr0 pr1 pr2 pr3 ih0 ih1 ih2 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.poly_complete pr3
      apply proved_rule (.HasJ_identityIntro Γ A p q aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨haux0, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @proofErase Γ A x y p pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasJ_proofErase Γ A x y p)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @j Γ A x B y e d pr0 pr1 pr2 pr3 pr4 pr5 pr6 pr7 pr8 ih0 ih1 ih2 ih3 ih4 ih5 ih6 ih7 ih8 =>
      apply proved_rule (.HasJ_j Γ A x B y e d)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, ih6, ih7, ih8, True.intro⟩
  | @conv Γ A p q pr0 pr1 pr2 pr3 ih0 ih1 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.poly_complete pr2
      apply proved_rule (.HasJ_conv Γ A p q aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨haux0, pr3, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @piExt Γ A B p q h pr0 pr1 pr2 pr3 pr4 pr5 pr6 pr7 pr8 pr9 pr10 pr11 pr12 pr13 ih0 ih1 ih2 ih3 ih4 ih5 ih6 ih7 ih8 =>
      apply proved_rule (.HasJ_piExt Γ A B p q h)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr9, pr10, pr11, pr12, pr13, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, ih6, ih7, ih8, True.intro⟩
  | @allExt Γ B p q h pr0 pr1 pr2 pr3 pr4 pr5 pr6 pr7 pr8 pr9 pr10 ih0 ih1 ih2 ih3 ih4 ih5 ih6 =>
      apply proved_rule (.HasJ_allExt Γ B p q h)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr7, pr8, pr9, pr10, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, ih6, True.intro⟩
  | @sigmaElim Γ A B P d z pr0 pr1 pr2 pr3 pr4 pr5 ih0 ih1 ih2 ih3 ih4 ih5 =>
      apply proved_rule (.HasJ_sigmaElim Γ A B P d z)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, True.intro⟩
  | @natInduction Γ P p s pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasJ_natInduction Γ P p s)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩

theorem j_form_complete {Γ : P01AC.Tel} {A : P01AC.Ty} (h : JointCompletion.FormJ Γ A) :
    Proved (.formJ Γ A) := by
  induction h using JointCompletion.FormJ.rec
    (motive_1 := fun Γ _ => Proved (.ctxJ Γ))
    (motive_3 := fun Γ p A _ => Proved (.hasJ Γ p A)) with
  | @ctxBase Γ pr0 =>
      have base0 := e_ctx_complete pr0
      apply proved_rule (.CtxJ_ctxBase Γ)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨base0, True.intro⟩
  | @nil  =>
      apply proved_rule (.CtxJ_nil )
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
  | @ext Γ A pr0 pr1 ih0 ih1 =>
      apply proved_rule (.CtxJ_ext Γ A)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @formBase Γ A pr0 =>
      have base0 := e_form_complete pr0
      apply proved_rule (.FormJ_formBase Γ A)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨base0, True.intro⟩
  | @param Γ n pr0 ih0 =>
      apply proved_rule (.FormJ_param Γ n)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @bottom Γ pr0 ih0 =>
      apply proved_rule (.FormJ_bottom Γ)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @all Γ B pr0 pr1 ih0 ih1 =>
      apply proved_rule (.FormJ_all Γ B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @raw Γ pr0 ih0 =>
      apply proved_rule (.FormJ_raw Γ)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @pi Γ A B pr0 pr1 ih0 ih1 =>
      apply proved_rule (.FormJ_pi Γ A B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @sigma Γ A B pr0 pr1 ih0 ih1 =>
      apply proved_rule (.FormJ_sigma Γ A B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @identity Γ A p q pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.FormJ_identity Γ A p q)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @hasBase Γ p A pr0 =>
      have base0 := e_has_complete pr0
      apply proved_rule (.HasJ_hasBase Γ p A)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨base0, True.intro⟩
  | @var Γ A n pr0 pr1 ih0 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.lookup_complete pr1
      apply proved_rule (.HasJ_var Γ A n aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨haux0, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @i Γ A pr0 pr1 ih0 ih1 =>
      apply proved_rule (.HasJ_i Γ A)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @k Γ A B pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasJ_k Γ A B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @s Γ A B C pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasJ_s Γ A B C)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @finite C Γ t τ pr0 pr1 pr2 pr3 ih0 ih1 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.finite_complete pr3
      apply proved_rule (.HasJ_finite C Γ t τ aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr0, haux0, True.intro⟩
      · simp only [Rule.premises, all_append, all_ofFn, All]
        exact ⟨fun i => ih0 i.val i.isLt, ⟨ih1, True.intro⟩⟩
  | @allIntro Γ B p pr0 pr1 ih0 ih1 =>
      apply proved_rule (.HasJ_allIntro Γ B p)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @allElim Γ B A p pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasJ_allElim Γ B A p)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @rawAtom Γ t pr0 ih0 =>
      apply proved_rule (.HasJ_rawAtom Γ t)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @rawApp Γ f a pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasJ_rawApp Γ f a)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @piIntro Γ A B b pr0 pr1 pr2 ih0 ih1 =>
      apply proved_rule (.HasJ_piIntro Γ A B b)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr2, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @piElim Γ A B a f pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasJ_piElim Γ A B a f)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @sigmaIntro Γ A B a b pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasJ_sigmaIntro Γ A B a b)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @sigmaFst Γ A B z pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasJ_sigmaFst Γ A B z)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @sigmaSnd Γ A B z pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasJ_sigmaSnd Γ A B z)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @identityIntro Γ A p q pr0 pr1 pr2 pr3 ih0 ih1 ih2 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.poly_complete pr3
      apply proved_rule (.HasJ_identityIntro Γ A p q aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨haux0, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @proofErase Γ A x y p pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasJ_proofErase Γ A x y p)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @j Γ A x B y e d pr0 pr1 pr2 pr3 pr4 pr5 pr6 pr7 pr8 ih0 ih1 ih2 ih3 ih4 ih5 ih6 ih7 ih8 =>
      apply proved_rule (.HasJ_j Γ A x B y e d)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, ih6, ih7, ih8, True.intro⟩
  | @conv Γ A p q pr0 pr1 pr2 pr3 ih0 ih1 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.poly_complete pr2
      apply proved_rule (.HasJ_conv Γ A p q aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨haux0, pr3, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @piExt Γ A B p q h pr0 pr1 pr2 pr3 pr4 pr5 pr6 pr7 pr8 pr9 pr10 pr11 pr12 pr13 ih0 ih1 ih2 ih3 ih4 ih5 ih6 ih7 ih8 =>
      apply proved_rule (.HasJ_piExt Γ A B p q h)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr9, pr10, pr11, pr12, pr13, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, ih6, ih7, ih8, True.intro⟩
  | @allExt Γ B p q h pr0 pr1 pr2 pr3 pr4 pr5 pr6 pr7 pr8 pr9 pr10 ih0 ih1 ih2 ih3 ih4 ih5 ih6 =>
      apply proved_rule (.HasJ_allExt Γ B p q h)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr7, pr8, pr9, pr10, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, ih6, True.intro⟩
  | @sigmaElim Γ A B P d z pr0 pr1 pr2 pr3 pr4 pr5 ih0 ih1 ih2 ih3 ih4 ih5 =>
      apply proved_rule (.HasJ_sigmaElim Γ A B P d z)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, True.intro⟩
  | @natInduction Γ P p s pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasJ_natInduction Γ P p s)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩

theorem j_has_complete {Γ : P01AC.Tel} {p : P01D.Poly} {A : P01AC.Ty} (h : JointCompletion.HasJ Γ p A) :
    Proved (.hasJ Γ p A) := by
  induction h using JointCompletion.HasJ.rec
    (motive_1 := fun Γ _ => Proved (.ctxJ Γ))
    (motive_2 := fun Γ A _ => Proved (.formJ Γ A)) with
  | @ctxBase Γ pr0 =>
      have base0 := e_ctx_complete pr0
      apply proved_rule (.CtxJ_ctxBase Γ)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨base0, True.intro⟩
  | @nil  =>
      apply proved_rule (.CtxJ_nil )
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
  | @ext Γ A pr0 pr1 ih0 ih1 =>
      apply proved_rule (.CtxJ_ext Γ A)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @formBase Γ A pr0 =>
      have base0 := e_form_complete pr0
      apply proved_rule (.FormJ_formBase Γ A)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨base0, True.intro⟩
  | @param Γ n pr0 ih0 =>
      apply proved_rule (.FormJ_param Γ n)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @bottom Γ pr0 ih0 =>
      apply proved_rule (.FormJ_bottom Γ)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @all Γ B pr0 pr1 ih0 ih1 =>
      apply proved_rule (.FormJ_all Γ B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @raw Γ pr0 ih0 =>
      apply proved_rule (.FormJ_raw Γ)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @pi Γ A B pr0 pr1 ih0 ih1 =>
      apply proved_rule (.FormJ_pi Γ A B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @sigma Γ A B pr0 pr1 ih0 ih1 =>
      apply proved_rule (.FormJ_sigma Γ A B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @identity Γ A p q pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.FormJ_identity Γ A p q)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @hasBase Γ p A pr0 =>
      have base0 := e_has_complete pr0
      apply proved_rule (.HasJ_hasBase Γ p A)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨base0, True.intro⟩
  | @var Γ A n pr0 pr1 ih0 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.lookup_complete pr1
      apply proved_rule (.HasJ_var Γ A n aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨haux0, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @i Γ A pr0 pr1 ih0 ih1 =>
      apply proved_rule (.HasJ_i Γ A)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @k Γ A B pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasJ_k Γ A B)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @s Γ A B C pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasJ_s Γ A B C)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @finite C Γ t τ pr0 pr1 pr2 pr3 ih0 ih1 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.finite_complete pr3
      apply proved_rule (.HasJ_finite C Γ t τ aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr0, haux0, True.intro⟩
      · simp only [Rule.premises, all_append, all_ofFn, All]
        exact ⟨fun i => ih0 i.val i.isLt, ⟨ih1, True.intro⟩⟩
  | @allIntro Γ B p pr0 pr1 ih0 ih1 =>
      apply proved_rule (.HasJ_allIntro Γ B p)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @allElim Γ B A p pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasJ_allElim Γ B A p)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @rawAtom Γ t pr0 ih0 =>
      apply proved_rule (.HasJ_rawAtom Γ t)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, True.intro⟩
  | @rawApp Γ f a pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasJ_rawApp Γ f a)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @piIntro Γ A B b pr0 pr1 pr2 ih0 ih1 =>
      apply proved_rule (.HasJ_piIntro Γ A B b)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr2, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @piElim Γ A B a f pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasJ_piElim Γ A B a f)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @sigmaIntro Γ A B a b pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasJ_sigmaIntro Γ A B a b)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩
  | @sigmaFst Γ A B z pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasJ_sigmaFst Γ A B z)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @sigmaSnd Γ A B z pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasJ_sigmaSnd Γ A B z)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @identityIntro Γ A p q pr0 pr1 pr2 pr3 ih0 ih1 ih2 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.poly_complete pr3
      apply proved_rule (.HasJ_identityIntro Γ A p q aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨haux0, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @proofErase Γ A x y p pr0 pr1 pr2 ih0 ih1 ih2 =>
      apply proved_rule (.HasJ_proofErase Γ A x y p)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, True.intro⟩
  | @j Γ A x B y e d pr0 pr1 pr2 pr3 pr4 pr5 pr6 pr7 pr8 ih0 ih1 ih2 ih3 ih4 ih5 ih6 ih7 ih8 =>
      apply proved_rule (.HasJ_j Γ A x B y e d)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, ih6, ih7, ih8, True.intro⟩
  | @conv Γ A p q pr0 pr1 pr2 pr3 ih0 ih1 =>
      obtain ⟨aux0, haux0⟩ := AuxiliaryCertificates.poly_complete pr2
      apply proved_rule (.HasJ_conv Γ A p q aux0)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨haux0, pr3, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, True.intro⟩
  | @piExt Γ A B p q h pr0 pr1 pr2 pr3 pr4 pr5 pr6 pr7 pr8 pr9 pr10 pr11 pr12 pr13 ih0 ih1 ih2 ih3 ih4 ih5 ih6 ih7 ih8 =>
      apply proved_rule (.HasJ_piExt Γ A B p q h)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr9, pr10, pr11, pr12, pr13, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, ih6, ih7, ih8, True.intro⟩
  | @allExt Γ B p q h pr0 pr1 pr2 pr3 pr4 pr5 pr6 pr7 pr8 pr9 pr10 ih0 ih1 ih2 ih3 ih4 ih5 ih6 =>
      apply proved_rule (.HasJ_allExt Γ B p q h)
      · simp only [Rule.checkSide, decide_eq_true_eq]
        exact ⟨pr7, pr8, pr9, pr10, True.intro⟩
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, ih6, True.intro⟩
  | @sigmaElim Γ A B P d z pr0 pr1 pr2 pr3 pr4 pr5 ih0 ih1 ih2 ih3 ih4 ih5 =>
      apply proved_rule (.HasJ_sigmaElim Γ A B P d z)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, ih4, ih5, True.intro⟩
  | @natInduction Γ P p s pr0 pr1 pr2 pr3 ih0 ih1 ih2 ih3 =>
      apply proved_rule (.HasJ_natInduction Γ P p s)
      · simp only [Rule.checkSide, decide_eq_true_eq]
      · simp only [Rule.premises, All]
        exact ⟨ih0, ih1, ih2, ih3, True.intro⟩

/-- Every actual frozen Joint or old-E judgment has a finite accepted certificate. -/
theorem complete {j : Claim} (h : j.denote) : ∃ c : DerivationCertificate, check c j = true := by
  cases j with
  | ctxJ Γ => exact j_ctx_complete h
  | formJ Γ A => exact j_form_complete h
  | hasJ Γ p A => exact j_has_complete h
  | ctxE Γ => exact e_ctx_complete h
  | formE Γ A => exact e_form_complete h
  | hasE Γ p A => exact e_has_complete h

theorem derivable_iff_certificate (j : Claim) :
    j.denote ↔ ∃ c : DerivationCertificate, check c j = true :=
  ⟨complete, fun ⟨_,hc⟩ => check_sound hc⟩

theorem hasJ_iff_certificate (Γ : P01AC.Tel) (p : P01D.Poly) (A : P01AC.Ty) :
    JointCompletion.HasJ Γ p A ↔ ∃ c : DerivationCertificate, check c (.hasJ Γ p A) = true :=
  derivable_iff_certificate (.hasJ Γ p A)

#print axioms complete
#print axioms derivable_iff_certificate
#print axioms hasJ_iff_certificate
end JointCertificates
