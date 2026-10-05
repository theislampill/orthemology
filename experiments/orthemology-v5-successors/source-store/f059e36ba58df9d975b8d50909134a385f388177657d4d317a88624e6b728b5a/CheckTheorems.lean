/- Independent statement and assumption checks. No new axioms are declared. -/
import IntensionalIdentityTheorems

open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC P01AC.Intensional

example {Γ p A} (h : P01AC.Has Γ p A) :
    P01AC.Intensional.SemanticHas Γ p A := has_sound h

example (r : Poly) : ¬ P01AC.Has [] r separationB := separation_no_has r
example (r : Poly) : ¬ Plus.HasPlus [] r separationB := separation_no_hasPlus r

example {C : Ty} {p q : Poly}
    (hC : Plus.FormPlus [] C)
    (hp : Plus.HasPlus [] p C) (hq : Plus.HasPlus [] q C)
    (sp : Scoped 0 p) (sq : Scoped 0 q) :
    (∃ r, Plus.HasPlus [] r (.identity C p q)) ↔
      Conv (eval p zeroEnv) (eval q zeroEnv) :=
  closed_typed_identity_iff hC hp hq sp sq

example {C : Ty} {p q : Poly}
    (hC : Plus.FormPlus [] C)
    (hp : Plus.HasPlus [] p C) (hq : Plus.HasPlus [] q C)
    (sp : Scoped 0 p) (sq : Scoped 0 q) :
    Plus.HasPlus [] (.atom .i) (.identity C p q) ↔
      Conv (eval p zeroEnv) (eval q zeroEnv) :=
  closed_identity_intro_iff hC hp hq sp sq

example : P01AC.Form [] separationB := separationB_form
example : P01AC.Has [] separationP separationA := separationP_has
example : P01AC.Has [] separationQ separationA := separationQ_has
example (ρ : OEnv) (η : Env) :
    P01AC.F separationB ρ η (eval separationE η) (eval separationE η) := separation_F ρ η
example (r : REnv) (η ξ : Env) :
    P01AC.G separationB r η ξ (eval separationE η) (eval separationE ξ) := separation_G r η ξ

#check @has_sound
#check @hasPlus_sound
#check @intensional_identity_separation
#check @closed_identity_intro_iff
#check @closed_typed_identity_iff
#check @closed_typed_identity_characterisation
#check @interp_mixed
#check @interp_motiveAt
#check @finite_code_sound
#check @P01AC.Intensional.E_characterisation
#check @V_theta
#check @E_theta
#check @relational_fundamental
#check @relational_fundamental_plus
#print P01AC.Intensional.V
#print P01AC.Intensional.E
#print P01AC.Intensional.Plus.PolyConvPlus
#print P01AC.Intensional.Plus.CtxPlus
#print P01AC.Intensional.Plus.FormPlus
#print P01AC.Intensional.Plus.HasPlus

-- Every public theorem in the six frozen proof modules.
#print axioms P01AC.Intensional.Plus.polyConv_inclusion
#print axioms P01AC.Intensional.Plus.polyConvPlus_sound
#print axioms P01AC.Intensional.Plus.atom_app_congr
#print axioms P01AC.Intensional.Plus.raw_step_atom
#print axioms P01AC.Intensional.Plus.raw_conv_atom
#print axioms P01AC.Intensional.Plus.closed_pack
#print axioms P01AC.Intensional.Plus.closed_conversion_iff
#print axioms P01AC.Intensional.Plus.has_inclusion
#print axioms P01AC.Intensional.Plus.form_inclusion
#print axioms P01AC.Intensional.Plus.ctx_inclusion
#print axioms P01AC.Intensional.sat_saturated
#print axioms P01AC.Intensional.saturated_iff_code
#print axioms P01AC.Intensional.code_ext
#print axioms P01AC.Intensional.interp_saturated
#print axioms P01AC.Intensional.envConv_cons
#print axioms P01AC.Intensional.eval_coherent
#print axioms P01AC.Intensional.interp_coherent
#print axioms P01AC.Intensional.eval_pup
#print axioms P01AC.Intensional.interp_subst
#print axioms P01AC.Intensional.interp_wk
#print axioms P01AC.Intensional.interp_inst
#print axioms P01AC.Intensional.interp_motiveAt
#print axioms P01AC.Intensional.interp_arr
#print axioms P01AC.Intensional.interp_trename
#print axioms P01AC.Intensional.interp_twk
#print axioms P01AC.Intensional.interp_mixed
#print axioms P01AC.Intensional.interp_tsubst
#print axioms P01AC.Intensional.interp_tinst
#print axioms P01AC.Intensional.interp_fin
#print axioms P01AC.Intensional.finite_code_sound
#print axioms P01AC.Intensional.finite_mem
#print axioms P01AC.Intensional.R_refines
#print axioms P01AC.Intensional.R_symm
#print axioms P01AC.Intensional.R_trans
#print axioms P01AC.Intensional.R_domain
#print axioms P01AC.Intensional.R_saturated
#print axioms P01AC.Intensional.R_coherent
#print axioms P01AC.Intensional.E_characterisation
#print axioms P01AC.Intensional.E_refl
#print axioms P01AC.Intensional.E_symm
#print axioms P01AC.Intensional.E_trans
#print axioms P01AC.Intensional.E_twk
#print axioms P01AC.Intensional.V_theta
#print axioms P01AC.Intensional.V_theta_base
#print axioms P01AC.Intensional.E_theta
#print axioms P01AC.Intensional.semantic_relational
#print axioms P01AC.Intensional.relational_fundamental
#print axioms P01AC.Intensional.relational_fundamental_plus
#print axioms P01AC.Intensional.V_nil
#print axioms P01AC.Intensional.V_cons
#print axioms P01AC.Intensional.lookup_member
#print axioms P01AC.Intensional.V_twk
#print axioms P01AC.Intensional.fundamental_var
#print axioms P01AC.Intensional.fundamental_i
#print axioms P01AC.Intensional.fundamental_k
#print axioms P01AC.Intensional.fundamental_s
#print axioms P01AC.Intensional.fundamental_finite
#print axioms P01AC.Intensional.fundamental_all_intro
#print axioms P01AC.Intensional.fundamental_all_elim
#print axioms P01AC.Intensional.fundamental_raw_atom
#print axioms P01AC.Intensional.fundamental_raw_app
#print axioms P01AC.Intensional.fundamental_pi_intro
#print axioms P01AC.Intensional.fundamental_pi_elim
#print axioms P01AC.Intensional.fundamental_sigma_intro
#print axioms P01AC.Intensional.fundamental_sigma_fst
#print axioms P01AC.Intensional.fundamental_sigma_snd
#print axioms P01AC.Intensional.fundamental_identity_intro
#print axioms P01AC.Intensional.fundamental_proof_erase
#print axioms P01AC.Intensional.fundamental_j
#print axioms P01AC.Intensional.fundamental_conv
#print axioms P01AC.Intensional.has_sound
#print axioms P01AC.Intensional.closed_identity_conversion
#print axioms P01AC.Intensional.hasPlus_sound
#print axioms P01AC.Intensional.plus_closed_identity_conversion
#print axioms P01AC.Intensional.separation_no_has
#print axioms P01AC.Intensional.separation_no_hasPlus
#print axioms P01AC.Intensional.separationA_formPlus
#print axioms P01AC.Intensional.separationP_hasPlus
#print axioms P01AC.Intensional.separationQ_hasPlus
#print axioms P01AC.Intensional.separationB_formPlus
#print axioms P01AC.Intensional.intensional_identity_separation
#print axioms P01AC.Intensional.closed_identity_intro_iff
#print axioms P01AC.Intensional.closed_typed_identity_iff
#print axioms P01AC.Intensional.closed_typed_identity_characterisation
#print axioms P01AC.Intensional.separationA_form
#print axioms P01AC.Intensional.separationP_has
#print axioms P01AC.Intensional.separationQ_has
#print axioms P01AC.Intensional.separationB_form
#print axioms P01AC.Intensional.separationP_scoped
#print axioms P01AC.Intensional.separationQ_scoped
#print axioms P01AC.Intensional.separationE_scoped
#print axioms P01AC.Intensional.separationA_scoped
#print axioms P01AC.Intensional.separationB_scoped
#print axioms P01AC.Intensional.separationA_type_scoped
#print axioms P01AC.Intensional.separationB_type_scoped
#print axioms P01AC.Intensional.separation_endpoints_F
#print axioms P01AC.Intensional.separation_F
#print axioms P01AC.Intensional.separation_G
#print axioms P01AC.Intensional.separation_closed_positive
#print axioms P01AC.Intensional.separation_endpoints_not_convertible
#print axioms P01AC.Intensional.separation_contradiction
