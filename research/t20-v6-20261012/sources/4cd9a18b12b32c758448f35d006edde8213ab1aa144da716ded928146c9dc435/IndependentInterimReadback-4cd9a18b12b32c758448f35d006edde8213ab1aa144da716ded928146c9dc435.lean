import AllSyntax
import AllTermAlgebra
import AllMixedAlgebra
import AllPredicates
import AllRawSubstitution
import AllRawRenaming
import AllBaseLaws
import AllPiLaws
import AllSigmaLaws
import AllTermLemmas
import AllBinderLaws
import AllConstants
import AllFiniteComparison
import AllSemanticSubstitution
import AllInstantiation
import AllSoundness
import AllBoundaryResults
import AuditSupport

#print P01AC.Ty
#print axioms P01AC.Ty
#ortho_audit P01AC.Ty
#print P01AC.subst
#print axioms P01AC.subst
#ortho_audit P01AC.subst
#print P01AC.wk
#print axioms P01AC.wk
#ortho_audit P01AC.wk
#print P01AC.inst
#print axioms P01AC.inst
#ortho_audit P01AC.inst
#print P01AC.motiveAt
#print axioms P01AC.motiveAt
#ortho_audit P01AC.motiveAt
#print P01AC.arr
#print axioms P01AC.arr
#ortho_audit P01AC.arr
#print P01AC.fin
#print axioms P01AC.fin
#ortho_audit P01AC.fin
#print P01AC.trename
#print axioms P01AC.trename
#ortho_audit P01AC.trename
#print P01AC.twk
#print axioms P01AC.twk
#ortho_audit P01AC.twk
#print P01AC.tup
#print axioms P01AC.tup
#ortho_audit P01AC.tup
#print P01AC.mixed
#print axioms P01AC.mixed
#ortho_audit P01AC.mixed
#print P01AC.tsubst
#print axioms P01AC.tsubst
#ortho_audit P01AC.tsubst
#print P01AC.tinst
#print axioms P01AC.tinst
#ortho_audit P01AC.tinst
#print P01AC.finSupport
#print axioms P01AC.finSupport
#ortho_audit P01AC.finSupport
#print P01AC.typeImages
#print axioms P01AC.typeImages
#ortho_audit P01AC.typeImages
#print P01AC.Tel
#print axioms P01AC.Tel
#ortho_audit P01AC.Tel
#print P01AC.Scoped
#print axioms P01AC.Scoped
#ortho_audit P01AC.Scoped
#print P01AC.TyScoped
#print axioms P01AC.TyScoped
#ortho_audit P01AC.TyScoped
#print P01AC.Lookup
#print axioms P01AC.Lookup
#ortho_audit P01AC.Lookup
#print P01AC.twkTel
#print axioms P01AC.twkTel
#ortho_audit P01AC.twkTel
#print P01AC.theta
#print axioms P01AC.theta
#ortho_audit P01AC.theta
#print P01AC.Ctx
#print axioms P01AC.Ctx
#ortho_audit P01AC.Ctx
#print P01AC.Form
#print axioms P01AC.Form
#ortho_audit P01AC.Form
#print P01AC.Has
#print axioms P01AC.Has
#ortho_audit P01AC.Has
#check P01AC.subst_id
#print axioms P01AC.subst_id
#ortho_audit P01AC.subst_id
#check P01AC.subst_comp
#print axioms P01AC.subst_comp
#ortho_audit P01AC.subst_comp
#check P01AC.subst_wk
#print axioms P01AC.subst_wk
#ortho_audit P01AC.subst_wk
#check P01AC.subst_wk_cancel
#print axioms P01AC.subst_wk_cancel
#ortho_audit P01AC.subst_wk_cancel
#check P01AC.inst_wk
#print axioms P01AC.inst_wk
#ortho_audit P01AC.inst_wk
#check P01AC.subst_inst
#print axioms P01AC.subst_inst
#ortho_audit P01AC.subst_inst
#check P01AC.subst_motiveAt
#print axioms P01AC.subst_motiveAt
#ortho_audit P01AC.subst_motiveAt
#check P01AC.motiveAt_inst
#print axioms P01AC.motiveAt_inst
#ortho_audit P01AC.motiveAt_inst
#check P01AC.motiveAt_wk_wk
#print axioms P01AC.motiveAt_wk_wk
#ortho_audit P01AC.motiveAt_wk_wk
#check P01AC.subst_arr
#print axioms P01AC.subst_arr
#ortho_audit P01AC.subst_arr
#check P01AC.subst_fin
#print axioms P01AC.subst_fin
#ortho_audit P01AC.subst_fin
#check P01AC.wk_fin
#print axioms P01AC.wk_fin
#ortho_audit P01AC.wk_fin
#check P01AC.inst_fin
#print axioms P01AC.inst_fin
#ortho_audit P01AC.inst_fin
#check P01AC.motiveAt_fin
#print axioms P01AC.motiveAt_fin
#ortho_audit P01AC.motiveAt_fin
#print P01AC.ScopedSub
#print axioms P01AC.ScopedSub
#ortho_audit P01AC.ScopedSub
#check P01AC.scoped_mono
#print axioms P01AC.scoped_mono
#ortho_audit P01AC.scoped_mono
#check P01AC.scoped_subst
#print axioms P01AC.scoped_subst
#ortho_audit P01AC.scoped_subst
#check P01AC.scoped_rename
#print axioms P01AC.scoped_rename
#ortho_audit P01AC.scoped_rename
#check P01AC.scoped_wk
#print axioms P01AC.scoped_wk
#ortho_audit P01AC.scoped_wk
#check P01AC.scopedSub_lift
#print axioms P01AC.scopedSub_lift
#ortho_audit P01AC.scopedSub_lift
#check P01AC.scopedSub_id
#print axioms P01AC.scopedSub_id
#ortho_audit P01AC.scopedSub_id
#check P01AC.scopedSub_comp
#print axioms P01AC.scopedSub_comp
#ortho_audit P01AC.scopedSub_comp
#check P01AC.scopedSub_cons
#print axioms P01AC.scopedSub_cons
#ortho_audit P01AC.scopedSub_cons
#check P01AC.scoped_pair
#print axioms P01AC.scoped_pair
#ortho_audit P01AC.scoped_pair
#check P01AC.scoped_fst
#print axioms P01AC.scoped_fst
#ortho_audit P01AC.scoped_fst
#check P01AC.scoped_snd
#print axioms P01AC.scoped_snd
#ortho_audit P01AC.scoped_snd
#check P01AC.scoped_j
#print axioms P01AC.scoped_j
#ortho_audit P01AC.scoped_j
#check P01AC.scoped_drop_absent
#print axioms P01AC.scoped_drop_absent
#ortho_audit P01AC.scoped_drop_absent
#check P01AC.scoped_abstract
#print axioms P01AC.scoped_abstract
#ortho_audit P01AC.scoped_abstract
#check P01AC.tyScoped_mono
#print axioms P01AC.tyScoped_mono
#ortho_audit P01AC.tyScoped_mono
#check P01AC.tyScoped_subst
#print axioms P01AC.tyScoped_subst
#ortho_audit P01AC.tyScoped_subst
#check P01AC.tyScoped_wk
#print axioms P01AC.tyScoped_wk
#ortho_audit P01AC.tyScoped_wk
#check P01AC.tyScoped_inst
#print axioms P01AC.tyScoped_inst
#ortho_audit P01AC.tyScoped_inst
#check P01AC.tyScoped_motiveAt
#print axioms P01AC.tyScoped_motiveAt
#ortho_audit P01AC.tyScoped_motiveAt
#check P01AC.tyScoped_fin
#print axioms P01AC.tyScoped_fin
#ortho_audit P01AC.tyScoped_fin
#check P01AC.lookup_lt
#print axioms P01AC.lookup_lt
#ortho_audit P01AC.lookup_lt
#check P01AC.polyConv_subst
#print axioms P01AC.polyConv_subst
#ortho_audit P01AC.polyConv_subst
#check P01AC.trename_id
#print axioms P01AC.trename_id
#ortho_audit P01AC.trename_id
#check P01AC.trename_comp
#print axioms P01AC.trename_comp
#ortho_audit P01AC.trename_comp
#check P01AC.subst_trename
#print axioms P01AC.subst_trename
#ortho_audit P01AC.subst_trename
#check P01AC.trename_wk
#print axioms P01AC.trename_wk
#ortho_audit P01AC.trename_wk
#check P01AC.subst_twk
#print axioms P01AC.subst_twk
#ortho_audit P01AC.subst_twk
#check P01AC.twk_wk
#print axioms P01AC.twk_wk
#ortho_audit P01AC.twk_wk
#check P01AC.trename_twk
#print axioms P01AC.trename_twk
#ortho_audit P01AC.trename_twk
#check P01AC.tup_wk
#print axioms P01AC.tup_wk
#ortho_audit P01AC.tup_wk
#check P01AC.tup_subst
#print axioms P01AC.tup_subst
#ortho_audit P01AC.tup_subst
#check P01AC.tup_param
#print axioms P01AC.tup_param
#ortho_audit P01AC.tup_param
#check P01AC.mixed_param
#print axioms P01AC.mixed_param
#ortho_audit P01AC.mixed_param
#check P01AC.mixed_id
#print axioms P01AC.mixed_id
#ortho_audit P01AC.mixed_id
#check P01AC.mixed_trename
#print axioms P01AC.mixed_trename
#ortho_audit P01AC.mixed_trename
#check P01AC.trename_mixed
#print axioms P01AC.trename_mixed
#ortho_audit P01AC.trename_mixed
#check P01AC.mixed_subst
#print axioms P01AC.mixed_subst
#ortho_audit P01AC.mixed_subst
#check P01AC.subst_mixed
#print axioms P01AC.subst_mixed
#ortho_audit P01AC.subst_mixed
#check P01AC.mixed_wk
#print axioms P01AC.mixed_wk
#ortho_audit P01AC.mixed_wk
#check P01AC.mixed_twk
#print axioms P01AC.mixed_twk
#ortho_audit P01AC.mixed_twk
#check P01AC.mixed_term_lift_comp
#print axioms P01AC.mixed_term_lift_comp
#ortho_audit P01AC.mixed_term_lift_comp
#check P01AC.mixed_type_lift_comp
#print axioms P01AC.mixed_type_lift_comp
#ortho_audit P01AC.mixed_type_lift_comp
#check P01AC.mixed_comp
#print axioms P01AC.mixed_comp
#ortho_audit P01AC.mixed_comp
#check P01AC.tsubst_id
#print axioms P01AC.tsubst_id
#ortho_audit P01AC.tsubst_id
#check P01AC.tsubst_comp
#print axioms P01AC.tsubst_comp
#ortho_audit P01AC.tsubst_comp
#check P01AC.subst_tsubst
#print axioms P01AC.subst_tsubst
#ortho_audit P01AC.subst_tsubst
#check P01AC.tinst_twk
#print axioms P01AC.tinst_twk
#ortho_audit P01AC.tinst_twk
#check P01AC.mixed_twk_cancel
#print axioms P01AC.mixed_twk_cancel
#ortho_audit P01AC.mixed_twk_cancel
#check P01AC.mixed_wk_wk
#print axioms P01AC.mixed_wk_wk
#ortho_audit P01AC.mixed_wk_wk
#check P01AC.tup_wk_wk
#print axioms P01AC.tup_wk_wk
#ortho_audit P01AC.tup_wk_wk
#check P01AC.mixed_inst
#print axioms P01AC.mixed_inst
#ortho_audit P01AC.mixed_inst
#check P01AC.mixed_motiveAt
#print axioms P01AC.mixed_motiveAt
#ortho_audit P01AC.mixed_motiveAt
#check P01AC.mixed_arr
#print axioms P01AC.mixed_arr
#ortho_audit P01AC.mixed_arr
#check P01AC.mixed_tsubst
#print axioms P01AC.mixed_tsubst
#ortho_audit P01AC.mixed_tsubst
#check P01AC.mixed_tinst
#print axioms P01AC.mixed_tinst
#ortho_audit P01AC.mixed_tinst
#check P01AC.subst_tinst
#print axioms P01AC.subst_tinst
#ortho_audit P01AC.subst_tinst
#check P01AC.trename_inst
#print axioms P01AC.trename_inst
#ortho_audit P01AC.trename_inst
#check P01AC.trename_motiveAt
#print axioms P01AC.trename_motiveAt
#ortho_audit P01AC.trename_motiveAt
#check P01AC.trename_arr
#print axioms P01AC.trename_arr
#ortho_audit P01AC.trename_arr
#check P01AC.trename_tinst
#print axioms P01AC.trename_tinst
#ortho_audit P01AC.trename_tinst
#check P01AC.tsubst_wk
#print axioms P01AC.tsubst_wk
#ortho_audit P01AC.tsubst_wk
#check P01AC.tinst_wk
#print axioms P01AC.tinst_wk
#ortho_audit P01AC.tinst_wk
#check P01AC.mixed_term_type_lifts
#print axioms P01AC.mixed_term_type_lifts
#ortho_audit P01AC.mixed_term_type_lifts
#check P01AC.mixed_double_term_type_lifts
#print axioms P01AC.mixed_double_term_type_lifts
#ortho_audit P01AC.mixed_double_term_type_lifts
#check P01AC.mixed_twk_wk
#print axioms P01AC.mixed_twk_wk
#ortho_audit P01AC.mixed_twk_wk
#check P01AC.tsubst_trename
#print axioms P01AC.tsubst_trename
#ortho_audit P01AC.tsubst_trename
#check P01AC.trename_tsubst
#print axioms P01AC.trename_tsubst
#ortho_audit P01AC.trename_tsubst
#check P01AC.tsubst_twk
#print axioms P01AC.tsubst_twk
#ortho_audit P01AC.tsubst_twk
#check P01AC.tsubst_arr
#print axioms P01AC.tsubst_arr
#ortho_audit P01AC.tsubst_arr
#check P01AC.tyScoped_trename
#print axioms P01AC.tyScoped_trename
#ortho_audit P01AC.tyScoped_trename
#check P01AC.tyScoped_twk
#print axioms P01AC.tyScoped_twk
#ortho_audit P01AC.tyScoped_twk
#check P01AC.tyScoped_tup
#print axioms P01AC.tyScoped_tup
#ortho_audit P01AC.tyScoped_tup
#check P01AC.tyScoped_mixed
#print axioms P01AC.tyScoped_mixed
#ortho_audit P01AC.tyScoped_mixed
#check P01AC.capture_both_sorts
#print axioms P01AC.capture_both_sorts
#ortho_audit P01AC.capture_both_sorts
#check P01AC.capture_term_under_all_pi
#print axioms P01AC.capture_term_under_all_pi
#ortho_audit P01AC.capture_term_under_all_pi
#check P01AC.capture_both_sorts_double_term
#print axioms P01AC.capture_both_sorts_double_term
#ortho_audit P01AC.capture_both_sorts_double_term
#check P01AC.capture_term_then_type
#print axioms P01AC.capture_term_then_type
#ortho_audit P01AC.capture_term_then_type
#check P01AC.capture_bound_type_retained
#print axioms P01AC.capture_bound_type_retained
#ortho_audit P01AC.capture_bound_type_retained
#check P01AC.capture_term_not_zero
#print axioms P01AC.capture_term_not_zero
#ortho_audit P01AC.capture_term_not_zero
#check P01AC.capture_type_not_zero
#print axioms P01AC.capture_type_not_zero
#ortho_audit P01AC.capture_type_not_zero
#print P01AC.Unary
#print axioms P01AC.Unary
#ortho_audit P01AC.Unary
#print P01AC.Hetero
#print axioms P01AC.Hetero
#ortho_audit P01AC.Hetero
#print P01AC.predicates
#print axioms P01AC.predicates
#ortho_audit P01AC.predicates
#print P01AC.F
#print axioms P01AC.F
#ortho_audit P01AC.F
#print P01AC.G
#print axioms P01AC.G
#ortho_audit P01AC.G
#check P01AC.F_param
#print axioms P01AC.F_param
#ortho_audit P01AC.F_param
#check P01AC.F_bottom
#print axioms P01AC.F_bottom
#ortho_audit P01AC.F_bottom
#check P01AC.F_raw
#print axioms P01AC.F_raw
#ortho_audit P01AC.F_raw
#check P01AC.F_pi
#print axioms P01AC.F_pi
#ortho_audit P01AC.F_pi
#check P01AC.F_sigma
#print axioms P01AC.F_sigma
#ortho_audit P01AC.F_sigma
#check P01AC.F_identity
#print axioms P01AC.F_identity
#ortho_audit P01AC.F_identity
#check P01AC.G_param
#print axioms P01AC.G_param
#ortho_audit P01AC.G_param
#check P01AC.G_bottom
#print axioms P01AC.G_bottom
#ortho_audit P01AC.G_bottom
#check P01AC.G_raw
#print axioms P01AC.G_raw
#ortho_audit P01AC.G_raw
#check P01AC.G_pi
#print axioms P01AC.G_pi
#ortho_audit P01AC.G_pi
#check P01AC.G_sigma
#print axioms P01AC.G_sigma
#ortho_audit P01AC.G_sigma
#check P01AC.G_identity
#print axioms P01AC.G_identity
#ortho_audit P01AC.G_identity
#check P01AC.F_all
#print axioms P01AC.F_all
#ortho_audit P01AC.F_all
#check P01AC.G_all
#print axioms P01AC.G_all
#ortho_audit P01AC.G_all
#print P01AC.zeroEnv
#print axioms P01AC.zeroEnv
#ortho_audit P01AC.zeroEnv
#print P01AC.tail
#print axioms P01AC.tail
#ortho_audit P01AC.tail
#print P01AC.D
#print axioms P01AC.D
#ortho_audit P01AC.D
#print P01AC.E
#print axioms P01AC.E
#ortho_audit P01AC.E
#print P01AC.H
#print axioms P01AC.H
#ortho_audit P01AC.H
#check P01AC.tail_cons
#print axioms P01AC.tail_cons
#ortho_audit P01AC.tail_cons
#check P01AC.cons_head_tail
#print axioms P01AC.cons_head_tail
#ortho_audit P01AC.cons_head_tail
#check P01AC.eval_pup_env
#print axioms P01AC.eval_pup_env
#ortho_audit P01AC.eval_pup_env
#check P01AC.eval_cons_poly
#print axioms P01AC.eval_cons_poly
#ortho_audit P01AC.eval_cons_poly
#check P01AC.FG_subst
#print axioms P01AC.FG_subst
#ortho_audit P01AC.FG_subst
#check P01AC.F_subst
#print axioms P01AC.F_subst
#ortho_audit P01AC.F_subst
#check P01AC.G_subst
#print axioms P01AC.G_subst
#ortho_audit P01AC.G_subst
#check P01AC.F_wk
#print axioms P01AC.F_wk
#ortho_audit P01AC.F_wk
#check P01AC.G_wk
#print axioms P01AC.G_wk
#ortho_audit P01AC.G_wk
#check P01AC.F_inst
#print axioms P01AC.F_inst
#ortho_audit P01AC.F_inst
#check P01AC.G_inst
#print axioms P01AC.G_inst
#ortho_audit P01AC.G_inst
#check P01AC.F_motiveAt
#print axioms P01AC.F_motiveAt
#ortho_audit P01AC.F_motiveAt
#check P01AC.G_motiveAt
#print axioms P01AC.G_motiveAt
#ortho_audit P01AC.G_motiveAt
#print P01AC.renvMap
#print axioms P01AC.renvMap
#ortho_audit P01AC.renvMap
#check P01AC.renvMap_diag
#print axioms P01AC.renvMap_diag
#ortho_audit P01AC.renvMap_diag
#check P01AC.cons_liftRen
#print axioms P01AC.cons_liftRen
#ortho_audit P01AC.cons_liftRen
#check P01AC.renvMap_extend
#print axioms P01AC.renvMap_extend
#ortho_audit P01AC.renvMap_extend
#check P01AC.FG_trename
#print axioms P01AC.FG_trename
#ortho_audit P01AC.FG_trename
#check P01AC.F_trename
#print axioms P01AC.F_trename
#ortho_audit P01AC.F_trename
#check P01AC.G_trename
#print axioms P01AC.G_trename
#ortho_audit P01AC.G_trename
#check P01AC.F_twk
#print axioms P01AC.F_twk
#ortho_audit P01AC.F_twk
#check P01AC.G_twk
#print axioms P01AC.G_twk
#ortho_audit P01AC.G_twk
#check P01AC.D_twk
#print axioms P01AC.D_twk
#ortho_audit P01AC.D_twk
#check P01AC.E_twk
#print axioms P01AC.E_twk
#ortho_audit P01AC.E_twk
#check P01AC.H_twk
#print axioms P01AC.H_twk
#ortho_audit P01AC.H_twk
#print P01AC.RelLaws
#print axioms P01AC.RelLaws
#ortho_audit P01AC.RelLaws
#print P01AC.RelLaws.per
#print axioms P01AC.RelLaws.per
#ortho_audit P01AC.RelLaws.per
#check P01AC.RelLaws.left
#print axioms P01AC.RelLaws.left
#ortho_audit P01AC.RelLaws.left
#check P01AC.RelLaws.right
#print axioms P01AC.RelLaws.right
#ortho_audit P01AC.RelLaws.right
#print P01AC.perLaws
#print axioms P01AC.perLaws
#ortho_audit P01AC.perLaws
#print P01AC.ContextLaws
#print axioms P01AC.ContextLaws
#ortho_audit P01AC.ContextLaws
#print P01AC.TypeLaws
#print axioms P01AC.TypeLaws
#ortho_audit P01AC.TypeLaws
#print P01AC.Fundamental
#print axioms P01AC.Fundamental
#ortho_audit P01AC.Fundamental
#check P01AC.TypeLaws.raw
#print axioms P01AC.TypeLaws.raw
#ortho_audit P01AC.TypeLaws.raw
#check P01AC.Fundamental.unary
#print axioms P01AC.Fundamental.unary
#ortho_audit P01AC.Fundamental.unary
#check P01AC.context_nil
#print axioms P01AC.context_nil
#ortho_audit P01AC.context_nil
#check P01AC.context_ext
#print axioms P01AC.context_ext
#ortho_audit P01AC.context_ext
#check P01AC.type_model
#print axioms P01AC.type_model
#ortho_audit P01AC.type_model
#check P01AC.type_param
#print axioms P01AC.type_param
#ortho_audit P01AC.type_param
#check P01AC.type_bottom
#print axioms P01AC.type_bottom
#ortho_audit P01AC.type_bottom
#check P01AC.type_raw
#print axioms P01AC.type_raw
#ortho_audit P01AC.type_raw
#check P01AC.type_identity
#print axioms P01AC.type_identity
#ortho_audit P01AC.type_identity
#check P01AC.type_pi
#print axioms P01AC.type_pi
#ortho_audit P01AC.type_pi
#check P01AC.type_sigma
#print axioms P01AC.type_sigma
#ortho_audit P01AC.type_sigma
#check P01AC.fundamental_var
#print axioms P01AC.fundamental_var
#ortho_audit P01AC.fundamental_var
#check P01AC.fundamental_pi_intro
#print axioms P01AC.fundamental_pi_intro
#ortho_audit P01AC.fundamental_pi_intro
#check P01AC.fundamental_pi_elim
#print axioms P01AC.fundamental_pi_elim
#ortho_audit P01AC.fundamental_pi_elim
#check P01AC.F_pair
#print axioms P01AC.F_pair
#ortho_audit P01AC.F_pair
#check P01AC.G_pair
#print axioms P01AC.G_pair
#ortho_audit P01AC.G_pair
#check P01AC.fundamental_sigma_intro
#print axioms P01AC.fundamental_sigma_intro
#ortho_audit P01AC.fundamental_sigma_intro
#check P01AC.fundamental_sigma_fst
#print axioms P01AC.fundamental_sigma_fst
#ortho_audit P01AC.fundamental_sigma_fst
#check P01AC.fundamental_sigma_snd
#print axioms P01AC.fundamental_sigma_snd
#ortho_audit P01AC.fundamental_sigma_snd
#check P01AC.fundamental_identity_intro
#print axioms P01AC.fundamental_identity_intro
#ortho_audit P01AC.fundamental_identity_intro
#check P01AC.fundamental_proof_erase
#print axioms P01AC.fundamental_proof_erase
#ortho_audit P01AC.fundamental_proof_erase
#check P01AC.fundamental_j
#print axioms P01AC.fundamental_j
#ortho_audit P01AC.fundamental_j
#print P01AC.Uniform
#print axioms P01AC.Uniform
#ortho_audit P01AC.Uniform
#check P01AC.all_uniform_transport
#print axioms P01AC.all_uniform_transport
#ortho_audit P01AC.all_uniform_transport
#check P01AC.all_per
#print axioms P01AC.all_per
#ortho_audit P01AC.all_per
#check P01AC.all_transport
#print axioms P01AC.all_transport
#ortho_audit P01AC.all_transport
#check P01AC.type_all
#print axioms P01AC.type_all
#ortho_audit P01AC.type_all
#print P01AC.objectOf
#print axioms P01AC.objectOf
#ortho_audit P01AC.objectOf
#print P01AC.linkOf
#print axioms P01AC.linkOf
#ortho_audit P01AC.linkOf
#check P01AC.F_arr
#print axioms P01AC.F_arr
#ortho_audit P01AC.F_arr
#check P01AC.G_arr
#print axioms P01AC.G_arr
#ortho_audit P01AC.G_arr
#check P01AC.fundamental_i
#print axioms P01AC.fundamental_i
#ortho_audit P01AC.fundamental_i
#check P01AC.fundamental_k
#print axioms P01AC.fundamental_k
#ortho_audit P01AC.fundamental_k
#check P01AC.fundamental_s
#print axioms P01AC.fundamental_s
#ortho_audit P01AC.fundamental_s
#check P01AC.FG_fin
#print axioms P01AC.FG_fin
#ortho_audit P01AC.FG_fin
#check P01AC.F_fin
#print axioms P01AC.F_fin
#ortho_audit P01AC.F_fin
#check P01AC.G_fin
#print axioms P01AC.G_fin
#ortho_audit P01AC.G_fin
#print P01AC.ImageMatch
#print axioms P01AC.ImageMatch
#ortho_audit P01AC.ImageMatch
#check P01AC.ImageMatch.diagonalLeft
#print axioms P01AC.ImageMatch.diagonalLeft
#ortho_audit P01AC.ImageMatch.diagonalLeft
#check P01AC.ImageMatch.diagonalRight
#print axioms P01AC.ImageMatch.diagonalRight
#ortho_audit P01AC.ImageMatch.diagonalRight
#check P01AC.ImageMatch.termLift
#print axioms P01AC.ImageMatch.termLift
#ortho_audit P01AC.ImageMatch.termLift
#check P01AC.ImageMatch.typeLift
#print axioms P01AC.ImageMatch.typeLift
#ortho_audit P01AC.ImageMatch.typeLift
#print P01AC.EvalImages
#print axioms P01AC.EvalImages
#ortho_audit P01AC.EvalImages
#check P01AC.evalImages_pup
#print axioms P01AC.evalImages_pup
#ortho_audit P01AC.evalImages_pup
#check P01AC.FG_mixed
#print axioms P01AC.FG_mixed
#ortho_audit P01AC.FG_mixed
#print P01AC.imageEnv
#print axioms P01AC.imageEnv
#ortho_audit P01AC.imageEnv
#check P01AC.imageEnv_match
#print axioms P01AC.imageEnv_match
#ortho_audit P01AC.imageEnv_match
#check P01AC.semantic_tsubst
#print axioms P01AC.semantic_tsubst
#ortho_audit P01AC.semantic_tsubst
#check P01AC.top_image_match
#print axioms P01AC.top_image_match
#ortho_audit P01AC.top_image_match
#check P01AC.G_tinst
#print axioms P01AC.G_tinst
#ortho_audit P01AC.G_tinst
#check P01AC.F_tinst
#print axioms P01AC.F_tinst
#ortho_audit P01AC.F_tinst
#check P01AC.fundamental_all_intro
#print axioms P01AC.fundamental_all_intro
#ortho_audit P01AC.fundamental_all_intro
#check P01AC.fundamental_all_elim
#print axioms P01AC.fundamental_all_elim
#ortho_audit P01AC.fundamental_all_elim
#check P01AC.typeImages_beyond
#print axioms P01AC.typeImages_beyond
#ortho_audit P01AC.typeImages_beyond
#check P01AC.finite_image_laws
#print axioms P01AC.finite_image_laws
#ortho_audit P01AC.finite_image_laws
#check P01AC.fundamental_finite
#print axioms P01AC.fundamental_finite
#ortho_audit P01AC.fundamental_finite
#print P01AC.Hereditary
#print axioms P01AC.Hereditary
#ortho_audit P01AC.Hereditary
#print P01AC.FormSound
#print axioms P01AC.FormSound
#ortho_audit P01AC.FormSound
#print P01AC.TermSound
#print axioms P01AC.TermSound
#ortho_audit P01AC.TermSound
#check P01AC.Hereditary.laws
#print axioms P01AC.Hereditary.laws
#ortho_audit P01AC.Hereditary.laws
#check P01AC.form_sound
#print axioms P01AC.form_sound
#ortho_audit P01AC.form_sound
#check P01AC.has_sound
#print axioms P01AC.has_sound
#ortho_audit P01AC.has_sound
#check P01AC.context_sound
#print axioms P01AC.context_sound
#ortho_audit P01AC.context_sound
#check P01AC.fundamental
#print axioms P01AC.fundamental
#ortho_audit P01AC.fundamental
#check P01AC.unary_fundamental
#print axioms P01AC.unary_fundamental
#ortho_audit P01AC.unary_fundamental
#check P01AC.strong_diagonal
#print axioms P01AC.strong_diagonal
#ortho_audit P01AC.strong_diagonal
#check P01AC.two_sided_invariance
#print axioms P01AC.two_sided_invariance
#ortho_audit P01AC.two_sided_invariance
#print P01AC.formedObject
#print axioms P01AC.formedObject
#ortho_audit P01AC.formedObject
#print P01AC.formedLink
#print axioms P01AC.formedLink
#ortho_audit P01AC.formedLink
#check P01AC.formedObject_rel
#print axioms P01AC.formedObject_rel
#ortho_audit P01AC.formedObject_rel
#check P01AC.formedLink_rel
#print axioms P01AC.formedLink_rel
#ortho_audit P01AC.formedLink_rel
#check P01AC.context_two_sided_invariance
#print axioms P01AC.context_two_sided_invariance
#ortho_audit P01AC.context_two_sided_invariance
#check P01AC.context_strong_diagonal
#print axioms P01AC.context_strong_diagonal
#ortho_audit P01AC.context_strong_diagonal
#print P01AC.formedFibre
#print axioms P01AC.formedFibre
#ortho_audit P01AC.formedFibre
#check P01AC.formedFibre_coherent
#print axioms P01AC.formedFibre_coherent
#ortho_audit P01AC.formedFibre_coherent
#check P01AC.formed_pi_exact
#print axioms P01AC.formed_pi_exact
#ortho_audit P01AC.formed_pi_exact
#check P01AC.formed_sigma_exact
#print axioms P01AC.formed_sigma_exact
#ortho_audit P01AC.formed_sigma_exact
#check P01AC.formed_identity_exact
#print axioms P01AC.formed_identity_exact
#ortho_audit P01AC.formed_identity_exact
#check P01AC.raw_omega_typed
#print axioms P01AC.raw_omega_typed
#ortho_audit P01AC.raw_omega_typed
#check P01AC.raw_omega_has_no_normal_reduct
#print axioms P01AC.raw_omega_has_no_normal_reduct
#ortho_audit P01AC.raw_omega_has_no_normal_reduct
#print P01AC.formedAllFamily
#print axioms P01AC.formedAllFamily
#ortho_audit P01AC.formedAllFamily
#check P01AC.formed_all_exact
#print axioms P01AC.formed_all_exact
#ortho_audit P01AC.formed_all_exact
