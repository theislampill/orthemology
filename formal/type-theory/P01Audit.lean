/- Generated exact target readback; compiler output is mandatory. -/
import AuditSupport
import P01Candidates
import P01Certificates
import P01Confluence
import P01ContextualJ
import P01DependentCore
import P01Examples
import P01GeneratedExports
import P01LambdaSyntax
import P01Omega
import P01PER
import P01Polynomials
import P01ReflectionCountermodel
import P01SNReflection
import P01SystemF
import P01Translation
import P01TypeAlgebra
import P01TypeAssertions
import P01UniverseBoundary
set_option pp.universes true
set_option format.width 120
#eval IO.println "AUDIT_BEGIN P01Candidates.SN"
#check P01Candidates.SN
#ortho_audit P01Candidates.SN
#print axioms P01Candidates.SN
#eval IO.println "AUDIT_END P01Candidates.SN"
#eval IO.println "AUDIT_BEGIN P01Candidates.Neutral"
#check P01Candidates.Neutral
#ortho_audit P01Candidates.Neutral
#print axioms P01Candidates.Neutral
#eval IO.println "AUDIT_END P01Candidates.Neutral"
#eval IO.println "AUDIT_BEGIN P01Candidates.neutral_app"
#check P01Candidates.neutral_app
#ortho_audit P01Candidates.neutral_app
#print axioms P01Candidates.neutral_app
#eval IO.println "AUDIT_END P01Candidates.neutral_app"
#eval IO.println "AUDIT_BEGIN P01Candidates.neutral_successor"
#check P01Candidates.neutral_successor
#ortho_audit P01Candidates.neutral_successor
#print axioms P01Candidates.neutral_successor
#eval IO.println "AUDIT_END P01Candidates.neutral_successor"
#eval IO.println "AUDIT_BEGIN P01Candidates.sn_step"
#check P01Candidates.sn_step
#ortho_audit P01Candidates.sn_step
#print axioms P01Candidates.sn_step
#eval IO.println "AUDIT_END P01Candidates.sn_step"
#eval IO.println "AUDIT_BEGIN P01Candidates.sn_red"
#check P01Candidates.sn_red
#ortho_audit P01Candidates.sn_red
#print axioms P01Candidates.sn_red
#eval IO.println "AUDIT_END P01Candidates.sn_red"
#eval IO.println "AUDIT_BEGIN P01Candidates.sn_function"
#check P01Candidates.sn_function
#ortho_audit P01Candidates.sn_function
#print axioms P01Candidates.sn_function
#eval IO.println "AUDIT_END P01Candidates.sn_function"
#eval IO.println "AUDIT_BEGIN P01Candidates.Candidate"
#check P01Candidates.Candidate
#ortho_audit P01Candidates.Candidate
#print axioms P01Candidates.Candidate
#eval IO.println "AUDIT_END P01Candidates.Candidate"
#eval IO.println "AUDIT_BEGIN P01Candidates.candidate_ext"
#check P01Candidates.candidate_ext
#ortho_audit P01Candidates.candidate_ext
#print axioms P01Candidates.candidate_ext
#eval IO.println "AUDIT_END P01Candidates.candidate_ext"
#eval IO.println "AUDIT_BEGIN P01Candidates.snCandidate"
#check P01Candidates.snCandidate
#ortho_audit P01Candidates.snCandidate
#print axioms P01Candidates.snCandidate
#eval IO.println "AUDIT_END P01Candidates.snCandidate"
#eval IO.println "AUDIT_BEGIN P01Candidates.zero_mem"
#check P01Candidates.zero_mem
#ortho_audit P01Candidates.zero_mem
#print axioms P01Candidates.zero_mem
#eval IO.println "AUDIT_END P01Candidates.zero_mem"
#eval IO.println "AUDIT_BEGIN P01Candidates.descend_red"
#check P01Candidates.descend_red
#ortho_audit P01Candidates.descend_red
#print axioms P01Candidates.descend_red
#eval IO.println "AUDIT_END P01Candidates.descend_red"
#eval IO.println "AUDIT_BEGIN P01Candidates.arrow"
#check P01Candidates.arrow
#ortho_audit P01Candidates.arrow
#print axioms P01Candidates.arrow
#eval IO.println "AUDIT_END P01Candidates.arrow"
#eval IO.println "AUDIT_BEGIN P01Candidates.intersection"
#check P01Candidates.intersection
#ortho_audit P01Candidates.intersection
#print axioms P01Candidates.intersection
#eval IO.println "AUDIT_END P01Candidates.intersection"
#eval IO.println "AUDIT_BEGIN P01Candidates.i_successor"
#check P01Candidates.i_successor
#ortho_audit P01Candidates.i_successor
#print axioms P01Candidates.i_successor
#eval IO.println "AUDIT_END P01Candidates.i_successor"
#eval IO.println "AUDIT_BEGIN P01Candidates.k_successor"
#check P01Candidates.k_successor
#ortho_audit P01Candidates.k_successor
#print axioms P01Candidates.k_successor
#eval IO.println "AUDIT_END P01Candidates.k_successor"
#eval IO.println "AUDIT_BEGIN P01Candidates.s_successor"
#check P01Candidates.s_successor
#ortho_audit P01Candidates.s_successor
#print axioms P01Candidates.s_successor
#eval IO.println "AUDIT_END P01Candidates.s_successor"
#eval IO.println "AUDIT_BEGIN P01Candidates.i_expand"
#check P01Candidates.i_expand
#ortho_audit P01Candidates.i_expand
#print axioms P01Candidates.i_expand
#eval IO.println "AUDIT_END P01Candidates.i_expand"
#eval IO.println "AUDIT_BEGIN P01Candidates.k_expand"
#check P01Candidates.k_expand
#ortho_audit P01Candidates.k_expand
#print axioms P01Candidates.k_expand
#eval IO.println "AUDIT_END P01Candidates.k_expand"
#eval IO.println "AUDIT_BEGIN P01Candidates.s_expand"
#check P01Candidates.s_expand
#ortho_audit P01Candidates.s_expand
#print axioms P01Candidates.s_expand
#eval IO.println "AUDIT_END P01Candidates.s_expand"
#eval IO.println "AUDIT_BEGIN P01Candidates.i_member"
#check P01Candidates.i_member
#ortho_audit P01Candidates.i_member
#print axioms P01Candidates.i_member
#eval IO.println "AUDIT_END P01Candidates.i_member"
#eval IO.println "AUDIT_BEGIN P01Candidates.k_member"
#check P01Candidates.k_member
#ortho_audit P01Candidates.k_member
#print axioms P01Candidates.k_member
#eval IO.println "AUDIT_END P01Candidates.k_member"
#eval IO.println "AUDIT_BEGIN P01Candidates.s_member"
#check P01Candidates.s_member
#ortho_audit P01Candidates.s_member
#print axioms P01Candidates.s_member
#eval IO.println "AUDIT_END P01Candidates.s_member"
#eval IO.println "AUDIT_BEGIN P01Candidates.interpret"
#check P01Candidates.interpret
#ortho_audit P01Candidates.interpret
#print axioms P01Candidates.interpret
#eval IO.println "AUDIT_END P01Candidates.interpret"
#eval IO.println "AUDIT_BEGIN P01Candidates.rename_interpret"
#check P01Candidates.rename_interpret
#ortho_audit P01Candidates.rename_interpret
#print axioms P01Candidates.rename_interpret
#eval IO.println "AUDIT_END P01Candidates.rename_interpret"
#eval IO.println "AUDIT_BEGIN P01Candidates.substitute_interpret"
#check P01Candidates.substitute_interpret
#ortho_audit P01Candidates.substitute_interpret
#print axioms P01Candidates.substitute_interpret
#eval IO.println "AUDIT_END P01Candidates.substitute_interpret"
#eval IO.println "AUDIT_BEGIN P01Candidates.instantiate_interpret"
#check P01Candidates.instantiate_interpret
#ortho_audit P01Candidates.instantiate_interpret
#print axioms P01Candidates.instantiate_interpret
#eval IO.println "AUDIT_END P01Candidates.instantiate_interpret"
#eval IO.println "AUDIT_BEGIN P01Candidates.finite_reducibility"
#check P01Candidates.finite_reducibility
#ortho_audit P01Candidates.finite_reducibility
#print axioms P01Candidates.finite_reducibility
#eval IO.println "AUDIT_END P01Candidates.finite_reducibility"
#eval IO.println "AUDIT_BEGIN P01Candidates.finite_SN"
#check P01Candidates.finite_SN
#ortho_audit P01Candidates.finite_SN
#print axioms P01Candidates.finite_SN
#eval IO.println "AUDIT_END P01Candidates.finite_SN"
#eval IO.println "AUDIT_BEGIN P01Certificate.Direction"
#check P01Certificate.Direction
#ortho_audit P01Certificate.Direction
#print axioms P01Certificate.Direction
#eval IO.println "AUDIT_END P01Certificate.Direction"
#eval IO.println "AUDIT_BEGIN P01Certificate.Address"
#check P01Certificate.Address
#ortho_audit P01Certificate.Address
#print axioms P01Certificate.Address
#eval IO.println "AUDIT_END P01Certificate.Address"
#eval IO.println "AUDIT_BEGIN P01Certificate.root"
#check P01Certificate.root
#ortho_audit P01Certificate.root
#print axioms P01Certificate.root
#eval IO.println "AUDIT_END P01Certificate.root"
#eval IO.println "AUDIT_BEGIN P01Certificate.stepAt"
#check P01Certificate.stepAt
#ortho_audit P01Certificate.stepAt
#print axioms P01Certificate.stepAt
#eval IO.println "AUDIT_END P01Certificate.stepAt"
#eval IO.println "AUDIT_BEGIN P01Certificate.replay"
#check P01Certificate.replay
#ortho_audit P01Certificate.replay
#print axioms P01Certificate.replay
#eval IO.println "AUDIT_END P01Certificate.replay"
#eval IO.println "AUDIT_BEGIN P01Certificate.checkJoin"
#check P01Certificate.checkJoin
#ortho_audit P01Certificate.checkJoin
#print axioms P01Certificate.checkJoin
#eval IO.println "AUDIT_END P01Certificate.checkJoin"
#eval IO.println "AUDIT_BEGIN P01Certificate.replay_sound"
#check P01Certificate.replay_sound
#ortho_audit P01Certificate.replay_sound
#print axioms P01Certificate.replay_sound
#eval IO.println "AUDIT_END P01Certificate.replay_sound"
#eval IO.println "AUDIT_BEGIN P01Certificate.join_sound"
#check P01Certificate.join_sound
#ortho_audit P01Certificate.join_sound
#print axioms P01Certificate.join_sound
#eval IO.println "AUDIT_END P01Certificate.join_sound"
#eval IO.println "AUDIT_BEGIN P01Certificate.FiniteEnvelope"
#check P01Certificate.FiniteEnvelope
#ortho_audit P01Certificate.FiniteEnvelope
#print axioms P01Certificate.FiniteEnvelope
#eval IO.println "AUDIT_END P01Certificate.FiniteEnvelope"
#eval IO.println "AUDIT_BEGIN P01Certificate.finite_envelope_sound"
#check P01Certificate.finite_envelope_sound
#ortho_audit P01Certificate.finite_envelope_sound
#print axioms P01Certificate.finite_envelope_sound
#eval IO.println "AUDIT_END P01Certificate.finite_envelope_sound"
#eval IO.println "AUDIT_BEGIN P01Certificate.finite_envelope_SN"
#check P01Certificate.finite_envelope_SN
#ortho_audit P01Certificate.finite_envelope_SN
#print axioms P01Certificate.finite_envelope_SN
#eval IO.println "AUDIT_END P01Certificate.finite_envelope_SN"
#eval IO.println "AUDIT_BEGIN P01Certificate.DependentEnvelope"
#check P01Certificate.DependentEnvelope
#ortho_audit P01Certificate.DependentEnvelope
#print axioms P01Certificate.DependentEnvelope
#eval IO.println "AUDIT_END P01Certificate.DependentEnvelope"
#eval IO.println "AUDIT_BEGIN P01Certificate.dependent_envelope_sound"
#check P01Certificate.dependent_envelope_sound
#ortho_audit P01Certificate.dependent_envelope_sound
#print axioms P01Certificate.dependent_envelope_sound
#eval IO.println "AUDIT_END P01Certificate.dependent_envelope_sound"
#eval IO.println "AUDIT_BEGIN P01Certificate.ReplayResult"
#check P01Certificate.ReplayResult
#ortho_audit P01Certificate.ReplayResult
#print axioms P01Certificate.ReplayResult
#eval IO.println "AUDIT_END P01Certificate.ReplayResult"
#eval IO.println "AUDIT_BEGIN P01Certificate.acceptedProof"
#check P01Certificate.acceptedProof
#ortho_audit P01Certificate.acceptedProof
#print axioms P01Certificate.acceptedProof
#eval IO.println "AUDIT_END P01Certificate.acceptedProof"
#eval IO.println "AUDIT_BEGIN P01Certificate.refusal_preserved"
#check P01Certificate.refusal_preserved
#ortho_audit P01Certificate.refusal_preserved
#print axioms P01Certificate.refusal_preserved
#eval IO.println "AUDIT_END P01Certificate.refusal_preserved"
#eval IO.println "AUDIT_BEGIN P01Certificate.accepted_replay_sound"
#check P01Certificate.accepted_replay_sound
#ortho_audit P01Certificate.accepted_replay_sound
#print axioms P01Certificate.accepted_replay_sound
#eval IO.println "AUDIT_END P01Certificate.accepted_replay_sound"
#eval IO.println "AUDIT_BEGIN P01Certificate.TypeShape"
#check P01Certificate.TypeShape
#ortho_audit P01Certificate.TypeShape
#print axioms P01Certificate.TypeShape
#eval IO.println "AUDIT_END P01Certificate.TypeShape"
#eval IO.println "AUDIT_BEGIN P01Certificate.image"
#check P01Certificate.image
#ortho_audit P01Certificate.image
#print axioms P01Certificate.image
#eval IO.println "AUDIT_END P01Certificate.image"
#eval IO.println "AUDIT_BEGIN P01Certificate.identity_not_in_exact_target_image"
#check P01Certificate.identity_not_in_exact_target_image
#ortho_audit P01Certificate.identity_not_in_exact_target_image
#print axioms P01Certificate.identity_not_in_exact_target_image
#eval IO.println "AUDIT_END P01Certificate.identity_not_in_exact_target_image"
#eval IO.println "AUDIT_BEGIN P01Certificate.sigma_not_in_exact_target_image"
#check P01Certificate.sigma_not_in_exact_target_image
#ortho_audit P01Certificate.sigma_not_in_exact_target_image
#print axioms P01Certificate.sigma_not_in_exact_target_image
#eval IO.println "AUDIT_END P01Certificate.sigma_not_in_exact_target_image"
#eval IO.println "AUDIT_BEGIN P01Source.Par"
#check P01Source.Par
#ortho_audit P01Source.Par
#print axioms P01Source.Par
#eval IO.println "AUDIT_END P01Source.Par"
#eval IO.println "AUDIT_BEGIN P01Source.par_refl"
#check P01Source.par_refl
#ortho_audit P01Source.par_refl
#print axioms P01Source.par_refl
#eval IO.println "AUDIT_END P01Source.par_refl"
#eval IO.println "AUDIT_BEGIN P01Source.dev"
#check P01Source.dev
#ortho_audit P01Source.dev
#print axioms P01Source.dev
#eval IO.println "AUDIT_END P01Source.dev"
#eval IO.println "AUDIT_BEGIN P01Source.par_i_form"
#check P01Source.par_i_form
#ortho_audit P01Source.par_i_form
#print axioms P01Source.par_i_form
#eval IO.println "AUDIT_END P01Source.par_i_form"
#eval IO.println "AUDIT_BEGIN P01Source.par_k_form"
#check P01Source.par_k_form
#ortho_audit P01Source.par_k_form
#print axioms P01Source.par_k_form
#eval IO.println "AUDIT_END P01Source.par_k_form"
#eval IO.println "AUDIT_BEGIN P01Source.par_s1_form"
#check P01Source.par_s1_form
#ortho_audit P01Source.par_s1_form
#print axioms P01Source.par_s1_form
#eval IO.println "AUDIT_END P01Source.par_s1_form"
#eval IO.println "AUDIT_BEGIN P01Source.par_s2_form"
#check P01Source.par_s2_form
#ortho_audit P01Source.par_s2_form
#print axioms P01Source.par_s2_form
#eval IO.println "AUDIT_END P01Source.par_s2_form"
#eval IO.println "AUDIT_BEGIN P01Source.par_k_args"
#check P01Source.par_k_args
#ortho_audit P01Source.par_k_args
#print axioms P01Source.par_k_args
#eval IO.println "AUDIT_END P01Source.par_k_args"
#eval IO.println "AUDIT_BEGIN P01Source.par_s2_args"
#check P01Source.par_s2_args
#ortho_audit P01Source.par_s2_args
#print axioms P01Source.par_s2_args
#eval IO.println "AUDIT_END P01Source.par_s2_args"
#eval IO.println "AUDIT_BEGIN P01Source.dev_plain"
#check P01Source.dev_plain
#ortho_audit P01Source.dev_plain
#print axioms P01Source.dev_plain
#eval IO.println "AUDIT_END P01Source.dev_plain"
#eval IO.println "AUDIT_BEGIN P01Source.par_develop"
#check P01Source.par_develop
#ortho_audit P01Source.par_develop
#print axioms P01Source.par_develop
#eval IO.println "AUDIT_END P01Source.par_develop"
#eval IO.println "AUDIT_BEGIN P01Source.par_diamond"
#check P01Source.par_diamond
#ortho_audit P01Source.par_diamond
#print axioms P01Source.par_diamond
#eval IO.println "AUDIT_END P01Source.par_diamond"
#eval IO.println "AUDIT_BEGIN P01Source.red_trans"
#check P01Source.red_trans
#ortho_audit P01Source.red_trans
#print axioms P01Source.red_trans
#eval IO.println "AUDIT_END P01Source.red_trans"
#eval IO.println "AUDIT_BEGIN P01Source.red_right"
#check P01Source.red_right
#ortho_audit P01Source.red_right
#print axioms P01Source.red_right
#eval IO.println "AUDIT_END P01Source.red_right"
#eval IO.println "AUDIT_BEGIN P01Source.red_app"
#check P01Source.red_app
#ortho_audit P01Source.red_app
#print axioms P01Source.red_app
#eval IO.println "AUDIT_END P01Source.red_app"
#eval IO.println "AUDIT_BEGIN P01Source.par_red"
#check P01Source.par_red
#ortho_audit P01Source.par_red
#print axioms P01Source.par_red
#eval IO.println "AUDIT_END P01Source.par_red"
#eval IO.println "AUDIT_BEGIN P01Source.step_par"
#check P01Source.step_par
#ortho_audit P01Source.step_par
#print axioms P01Source.step_par
#eval IO.println "AUDIT_END P01Source.step_par"
#eval IO.println "AUDIT_BEGIN P01Source.PStar"
#check P01Source.PStar
#ortho_audit P01Source.PStar
#print axioms P01Source.PStar
#eval IO.println "AUDIT_END P01Source.PStar"
#eval IO.println "AUDIT_BEGIN P01Source.pstar_trans"
#check P01Source.pstar_trans
#ortho_audit P01Source.pstar_trans
#print axioms P01Source.pstar_trans
#eval IO.println "AUDIT_END P01Source.pstar_trans"
#eval IO.println "AUDIT_BEGIN P01Source.strip"
#check P01Source.strip
#ortho_audit P01Source.strip
#print axioms P01Source.strip
#eval IO.println "AUDIT_END P01Source.strip"
#eval IO.println "AUDIT_BEGIN P01Source.pstar_confluence"
#check P01Source.pstar_confluence
#ortho_audit P01Source.pstar_confluence
#print axioms P01Source.pstar_confluence
#eval IO.println "AUDIT_END P01Source.pstar_confluence"
#eval IO.println "AUDIT_BEGIN P01Source.red_pstar"
#check P01Source.red_pstar
#ortho_audit P01Source.red_pstar
#print axioms P01Source.red_pstar
#eval IO.println "AUDIT_END P01Source.red_pstar"
#eval IO.println "AUDIT_BEGIN P01Source.pstar_red"
#check P01Source.pstar_red
#ortho_audit P01Source.pstar_red
#print axioms P01Source.pstar_red
#eval IO.println "AUDIT_END P01Source.pstar_red"
#eval IO.println "AUDIT_BEGIN P01Source.confluence"
#check P01Source.confluence
#ortho_audit P01Source.confluence
#print axioms P01Source.confluence
#eval IO.println "AUDIT_END P01Source.confluence"
#eval IO.println "AUDIT_BEGIN P01Source.conv_join"
#check P01Source.conv_join
#ortho_audit P01Source.conv_join
#print axioms P01Source.conv_join
#eval IO.println "AUDIT_END P01Source.conv_join"
#eval IO.println "AUDIT_BEGIN P01Source.Normal"
#check P01Source.Normal
#ortho_audit P01Source.Normal
#print axioms P01Source.Normal
#eval IO.println "AUDIT_END P01Source.Normal"
#eval IO.println "AUDIT_BEGIN P01Source.normal_red"
#check P01Source.normal_red
#ortho_audit P01Source.normal_red
#print axioms P01Source.normal_red
#eval IO.println "AUDIT_END P01Source.normal_red"
#eval IO.println "AUDIT_BEGIN P01Source.normal_exists"
#check P01Source.normal_exists
#ortho_audit P01Source.normal_exists
#print axioms P01Source.normal_exists
#eval IO.println "AUDIT_END P01Source.normal_exists"
#eval IO.println "AUDIT_BEGIN P01Source.normal_unique"
#check P01Source.normal_unique
#ortho_audit P01Source.normal_unique
#print axioms P01Source.normal_unique
#eval IO.println "AUDIT_END P01Source.normal_unique"
#eval IO.println "AUDIT_BEGIN P01Source.red_conv"
#check P01Source.red_conv
#ortho_audit P01Source.red_conv
#print axioms P01Source.red_conv
#eval IO.println "AUDIT_END P01Source.red_conv"
#eval IO.println "AUDIT_BEGIN P01Source.conversion_by_normal_forms"
#check P01Source.conversion_by_normal_forms
#ortho_audit P01Source.conversion_by_normal_forms
#print axioms P01Source.conversion_by_normal_forms
#eval IO.println "AUDIT_END P01Source.conversion_by_normal_forms"
#eval IO.println "AUDIT_BEGIN P01Source.finite_normal_form"
#check P01Source.finite_normal_form
#ortho_audit P01Source.finite_normal_form
#print axioms P01Source.finite_normal_form
#eval IO.println "AUDIT_END P01Source.finite_normal_form"
#eval IO.println "AUDIT_BEGIN P01Source.I_SKK_not_convertible"
#check P01Source.I_SKK_not_convertible
#ortho_audit P01Source.I_SKK_not_convertible
#print axioms P01Source.I_SKK_not_convertible
#eval IO.println "AUDIT_END P01Source.I_SKK_not_convertible"
#eval IO.println "AUDIT_BEGIN P01D.idBody"
#check P01D.idBody
#ortho_audit P01D.idBody
#print axioms P01D.idBody
#eval IO.println "AUDIT_END P01D.idBody"
#eval IO.println "AUDIT_BEGIN P01D.idContext"
#check P01D.idContext
#ortho_audit P01D.idContext
#print axioms P01D.idContext
#eval IO.println "AUDIT_END P01D.idContext"
#eval IO.println "AUDIT_BEGIN P01D.baseProof"
#check P01D.baseProof
#ortho_audit P01D.baseProof
#print axioms P01D.baseProof
#eval IO.println "AUDIT_END P01D.baseProof"
#eval IO.println "AUDIT_BEGIN P01D.baseSub"
#check P01D.baseSub
#ortho_audit P01D.baseSub
#print axioms P01D.baseSub
#eval IO.println "AUDIT_END P01D.baseSub"
#eval IO.println "AUDIT_BEGIN P01D.pointSub"
#check P01D.pointSub
#ortho_audit P01D.pointSub
#print axioms P01D.pointSub
#eval IO.println "AUDIT_END P01D.pointSub"
#eval IO.println "AUDIT_BEGIN P01D.identity_at"
#check P01D.identity_at
#ortho_audit P01D.identity_at
#print axioms P01D.identity_at
#eval IO.println "AUDIT_END P01D.identity_at"
#eval IO.println "AUDIT_BEGIN P01D.base_point_related"
#check P01D.base_point_related
#ortho_audit P01D.base_point_related
#print axioms P01D.base_point_related
#eval IO.println "AUDIT_END P01D.base_point_related"
#eval IO.println "AUDIT_BEGIN P01D.j"
#check P01D.j
#ortho_audit P01D.j
#print axioms P01D.j
#eval IO.println "AUDIT_END P01D.j"
#eval IO.println "AUDIT_BEGIN P01D.j_computation"
#check P01D.j_computation
#ortho_audit P01D.j_computation
#print axioms P01D.j_computation
#eval IO.println "AUDIT_END P01D.j_computation"
#eval IO.println "AUDIT_BEGIN P01D.inspectProof"
#check P01D.inspectProof
#ortho_audit P01D.inspectProof
#print axioms P01D.inspectProof
#eval IO.println "AUDIT_END P01D.inspectProof"
#eval IO.println "AUDIT_BEGIN P01D.proof_inspection_not_coherent"
#check P01D.proof_inspection_not_coherent
#ortho_audit P01D.proof_inspection_not_coherent
#print axioms P01D.proof_inspection_not_coherent
#eval IO.println "AUDIT_END P01D.proof_inspection_not_coherent"
#eval IO.println "AUDIT_BEGIN P01D.Context"
#check P01D.Context
#ortho_audit P01D.Context
#print axioms P01D.Context
#eval IO.println "AUDIT_END P01D.Context"
#eval IO.println "AUDIT_BEGIN P01D.nilContext"
#check P01D.nilContext
#ortho_audit P01D.nilContext
#print axioms P01D.nilContext
#eval IO.println "AUDIT_END P01D.nilContext"
#eval IO.println "AUDIT_BEGIN P01D.Ty"
#check P01D.Ty
#ortho_audit P01D.Ty
#print axioms P01D.Ty
#eval IO.println "AUDIT_END P01D.Ty"
#eval IO.println "AUDIT_BEGIN P01D.Tm"
#check P01D.Tm
#ortho_audit P01D.Tm
#print axioms P01D.Tm
#eval IO.println "AUDIT_END P01D.Tm"
#eval IO.println "AUDIT_BEGIN P01D.tracked"
#check P01D.tracked
#ortho_audit P01D.tracked
#print axioms P01D.tracked
#eval IO.println "AUDIT_END P01D.tracked"
#eval IO.println "AUDIT_BEGIN P01D.Tm.at"
#check P01D.Tm.at
#ortho_audit P01D.Tm.at
#print axioms P01D.Tm.at
#eval IO.println "AUDIT_END P01D.Tm.at"
#eval IO.println "AUDIT_BEGIN P01D.Tm.member"
#check P01D.Tm.member
#ortho_audit P01D.Tm.member
#print axioms P01D.Tm.member
#eval IO.println "AUDIT_END P01D.Tm.member"
#eval IO.println "AUDIT_BEGIN P01D.EqTm"
#check P01D.EqTm
#ortho_audit P01D.EqTm
#print axioms P01D.EqTm
#eval IO.println "AUDIT_END P01D.EqTm"
#eval IO.println "AUDIT_BEGIN P01D.eqTm_refl"
#check P01D.eqTm_refl
#ortho_audit P01D.eqTm_refl
#print axioms P01D.eqTm_refl
#eval IO.println "AUDIT_END P01D.eqTm_refl"
#eval IO.println "AUDIT_BEGIN P01D.eqTm_sym"
#check P01D.eqTm_sym
#ortho_audit P01D.eqTm_sym
#print axioms P01D.eqTm_sym
#eval IO.println "AUDIT_END P01D.eqTm_sym"
#eval IO.println "AUDIT_BEGIN P01D.eqTm_trans"
#check P01D.eqTm_trans
#ortho_audit P01D.eqTm_trans
#print axioms P01D.eqTm_trans
#eval IO.println "AUDIT_END P01D.eqTm_trans"
#eval IO.println "AUDIT_BEGIN P01D.Sub"
#check P01D.Sub
#ortho_audit P01D.Sub
#print axioms P01D.Sub
#eval IO.println "AUDIT_END P01D.Sub"
#eval IO.println "AUDIT_BEGIN P01D.Sub.id"
#check P01D.Sub.id
#ortho_audit P01D.Sub.id
#print axioms P01D.Sub.id
#eval IO.println "AUDIT_END P01D.Sub.id"
#eval IO.println "AUDIT_BEGIN P01D.Sub.comp"
#check P01D.Sub.comp
#ortho_audit P01D.Sub.comp
#print axioms P01D.Sub.comp
#eval IO.println "AUDIT_END P01D.Sub.comp"
#eval IO.println "AUDIT_BEGIN P01D.SubEq"
#check P01D.SubEq
#ortho_audit P01D.SubEq
#print axioms P01D.SubEq
#eval IO.println "AUDIT_END P01D.SubEq"
#eval IO.println "AUDIT_BEGIN P01D.SubRel"
#check P01D.SubRel
#ortho_audit P01D.SubRel
#print axioms P01D.SubRel
#eval IO.println "AUDIT_END P01D.SubRel"
#eval IO.println "AUDIT_BEGIN P01D.subrel_refl"
#check P01D.subrel_refl
#ortho_audit P01D.subrel_refl
#print axioms P01D.subrel_refl
#eval IO.println "AUDIT_END P01D.subrel_refl"
#eval IO.println "AUDIT_BEGIN P01D.subrel_sym"
#check P01D.subrel_sym
#ortho_audit P01D.subrel_sym
#print axioms P01D.subrel_sym
#eval IO.println "AUDIT_END P01D.subrel_sym"
#eval IO.println "AUDIT_BEGIN P01D.subrel_trans"
#check P01D.subrel_trans
#ortho_audit P01D.subrel_trans
#print axioms P01D.subrel_trans
#eval IO.println "AUDIT_END P01D.subrel_trans"
#eval IO.println "AUDIT_BEGIN P01D.code_exact_substitution_implies_related"
#check P01D.code_exact_substitution_implies_related
#ortho_audit P01D.code_exact_substitution_implies_related
#print axioms P01D.code_exact_substitution_implies_related
#eval IO.println "AUDIT_END P01D.code_exact_substitution_implies_related"
#eval IO.println "AUDIT_BEGIN P01D.subrel_composition"
#check P01D.subrel_composition
#ortho_audit P01D.subrel_composition
#print axioms P01D.subrel_composition
#eval IO.println "AUDIT_END P01D.subrel_composition"
#eval IO.println "AUDIT_BEGIN P01D.sub_left_identity"
#check P01D.sub_left_identity
#ortho_audit P01D.sub_left_identity
#print axioms P01D.sub_left_identity
#eval IO.println "AUDIT_END P01D.sub_left_identity"
#eval IO.println "AUDIT_BEGIN P01D.sub_right_identity"
#check P01D.sub_right_identity
#ortho_audit P01D.sub_right_identity
#print axioms P01D.sub_right_identity
#eval IO.println "AUDIT_END P01D.sub_right_identity"
#eval IO.println "AUDIT_BEGIN P01D.sub_associative"
#check P01D.sub_associative
#ortho_audit P01D.sub_associative
#print axioms P01D.sub_associative
#eval IO.println "AUDIT_END P01D.sub_associative"
#eval IO.println "AUDIT_BEGIN P01D.Ty.pull"
#check P01D.Ty.pull
#ortho_audit P01D.Ty.pull
#print axioms P01D.Ty.pull
#eval IO.println "AUDIT_END P01D.Ty.pull"
#eval IO.println "AUDIT_BEGIN P01D.Tm.subst"
#check P01D.Tm.subst
#ortho_audit P01D.Tm.subst
#print axioms P01D.Tm.subst
#eval IO.println "AUDIT_END P01D.Tm.subst"
#eval IO.println "AUDIT_BEGIN P01D.related_substitution_fibres"
#check P01D.related_substitution_fibres
#ortho_audit P01D.related_substitution_fibres
#print axioms P01D.related_substitution_fibres
#eval IO.println "AUDIT_END P01D.related_substitution_fibres"
#eval IO.println "AUDIT_BEGIN P01D.term_substitution_related"
#check P01D.term_substitution_related
#ortho_audit P01D.term_substitution_related
#print axioms P01D.term_substitution_related
#eval IO.println "AUDIT_END P01D.term_substitution_related"
#eval IO.println "AUDIT_BEGIN P01D.typing_under_substitution"
#check P01D.typing_under_substitution
#ortho_audit P01D.typing_under_substitution
#print axioms P01D.typing_under_substitution
#eval IO.println "AUDIT_END P01D.typing_under_substitution"
#eval IO.println "AUDIT_BEGIN P01D.term_substitution_identity"
#check P01D.term_substitution_identity
#ortho_audit P01D.term_substitution_identity
#print axioms P01D.term_substitution_identity
#eval IO.println "AUDIT_END P01D.term_substitution_identity"
#eval IO.println "AUDIT_BEGIN P01D.term_substitution_composition"
#check P01D.term_substitution_composition
#ortho_audit P01D.term_substitution_composition
#print axioms P01D.term_substitution_composition
#eval IO.println "AUDIT_END P01D.term_substitution_composition"
#eval IO.println "AUDIT_BEGIN P01D.extend"
#check P01D.extend
#ortho_audit P01D.extend
#print axioms P01D.extend
#eval IO.println "AUDIT_END P01D.extend"
#eval IO.println "AUDIT_BEGIN P01D.weaken"
#check P01D.weaken
#ortho_audit P01D.weaken
#print axioms P01D.weaken
#eval IO.println "AUDIT_END P01D.weaken"
#eval IO.println "AUDIT_BEGIN P01D.variable"
#check P01D.variable
#ortho_audit P01D.variable
#print axioms P01D.variable
#eval IO.println "AUDIT_END P01D.variable"
#eval IO.println "AUDIT_BEGIN P01D.Sub.extend"
#check P01D.Sub.extend
#ortho_audit P01D.Sub.extend
#print axioms P01D.Sub.extend
#eval IO.println "AUDIT_END P01D.Sub.extend"
#eval IO.println "AUDIT_BEGIN P01D.instanceSub"
#check P01D.instanceSub
#ortho_audit P01D.instanceSub
#print axioms P01D.instanceSub
#eval IO.println "AUDIT_END P01D.instanceSub"
#eval IO.println "AUDIT_BEGIN P01D.instanceTy"
#check P01D.instanceTy
#ortho_audit P01D.instanceTy
#print axioms P01D.instanceTy
#eval IO.println "AUDIT_END P01D.instanceTy"
#eval IO.println "AUDIT_BEGIN P01D.fibre"
#check P01D.fibre
#ortho_audit P01D.fibre
#print axioms P01D.fibre
#eval IO.println "AUDIT_END P01D.fibre"
#eval IO.println "AUDIT_BEGIN P01D.fibre_cross"
#check P01D.fibre_cross
#ortho_audit P01D.fibre_cross
#print axioms P01D.fibre_cross
#eval IO.println "AUDIT_END P01D.fibre_cross"
#eval IO.println "AUDIT_BEGIN P01D.piTy"
#check P01D.piTy
#ortho_audit P01D.piTy
#print axioms P01D.piTy
#eval IO.println "AUDIT_END P01D.piTy"
#eval IO.println "AUDIT_BEGIN P01D.lam"
#check P01D.lam
#ortho_audit P01D.lam
#print axioms P01D.lam
#eval IO.println "AUDIT_END P01D.lam"
#eval IO.println "AUDIT_BEGIN P01D.app"
#check P01D.app
#ortho_audit P01D.app
#print axioms P01D.app
#eval IO.println "AUDIT_END P01D.app"
#eval IO.println "AUDIT_BEGIN P01D.abstraction_congruence"
#check P01D.abstraction_congruence
#ortho_audit P01D.abstraction_congruence
#print axioms P01D.abstraction_congruence
#eval IO.println "AUDIT_END P01D.abstraction_congruence"
#eval IO.println "AUDIT_BEGIN P01D.pi_beta"
#check P01D.pi_beta
#ortho_audit P01D.pi_beta
#print axioms P01D.pi_beta
#eval IO.println "AUDIT_END P01D.pi_beta"
#eval IO.println "AUDIT_BEGIN P01D.sigmaTy"
#check P01D.sigmaTy
#ortho_audit P01D.sigmaTy
#print axioms P01D.sigmaTy
#eval IO.println "AUDIT_END P01D.sigmaTy"
#eval IO.println "AUDIT_BEGIN P01D.pair"
#check P01D.pair
#ortho_audit P01D.pair
#print axioms P01D.pair
#eval IO.println "AUDIT_END P01D.pair"
#eval IO.println "AUDIT_BEGIN P01D.fst"
#check P01D.fst
#ortho_audit P01D.fst
#print axioms P01D.fst
#eval IO.println "AUDIT_END P01D.fst"
#eval IO.println "AUDIT_BEGIN P01D.snd"
#check P01D.snd
#ortho_audit P01D.snd
#print axioms P01D.snd
#eval IO.println "AUDIT_END P01D.snd"
#eval IO.println "AUDIT_BEGIN P01D.sigma_beta_first"
#check P01D.sigma_beta_first
#ortho_audit P01D.sigma_beta_first
#print axioms P01D.sigma_beta_first
#eval IO.println "AUDIT_END P01D.sigma_beta_first"
#eval IO.println "AUDIT_BEGIN P01D.sigma_beta_second"
#check P01D.sigma_beta_second
#ortho_audit P01D.sigma_beta_second
#print axioms P01D.sigma_beta_second
#eval IO.println "AUDIT_END P01D.sigma_beta_second"
#eval IO.println "AUDIT_BEGIN P01D.sigma_eta_context"
#check P01D.sigma_eta_context
#ortho_audit P01D.sigma_eta_context
#print axioms P01D.sigma_eta_context
#eval IO.println "AUDIT_END P01D.sigma_eta_context"
#eval IO.println "AUDIT_BEGIN P01D.identityTy"
#check P01D.identityTy
#ortho_audit P01D.identityTy
#print axioms P01D.identityTy
#eval IO.println "AUDIT_END P01D.identityTy"
#eval IO.println "AUDIT_BEGIN P01D.reflTm"
#check P01D.reflTm
#ortho_audit P01D.reflTm
#print axioms P01D.reflTm
#eval IO.println "AUDIT_END P01D.reflTm"
#eval IO.println "AUDIT_BEGIN P01D.typeExtend"
#check P01D.typeExtend
#ortho_audit P01D.typeExtend
#print axioms P01D.typeExtend
#eval IO.println "AUDIT_END P01D.typeExtend"
#eval IO.println "AUDIT_BEGIN P01D.typeWeaken"
#check P01D.typeWeaken
#ortho_audit P01D.typeWeaken
#print axioms P01D.typeWeaken
#eval IO.println "AUDIT_END P01D.typeWeaken"
#eval IO.println "AUDIT_BEGIN P01D.typeVariable"
#check P01D.typeVariable
#ortho_audit P01D.typeVariable
#print axioms P01D.typeVariable
#eval IO.println "AUDIT_END P01D.typeVariable"
#eval IO.println "AUDIT_BEGIN P01D.typeInstance"
#check P01D.typeInstance
#ortho_audit P01D.typeInstance
#print axioms P01D.typeInstance
#eval IO.println "AUDIT_END P01D.typeInstance"
#eval IO.println "AUDIT_BEGIN P01D.AllFormation"
#check P01D.AllFormation
#ortho_audit P01D.AllFormation
#print axioms P01D.AllFormation
#eval IO.println "AUDIT_END P01D.AllFormation"
#eval IO.println "AUDIT_BEGIN P01D.allTy"
#check P01D.allTy
#ortho_audit P01D.allTy
#print axioms P01D.allTy
#eval IO.println "AUDIT_END P01D.allTy"
#eval IO.println "AUDIT_BEGIN P01D.allIntro"
#check P01D.allIntro
#ortho_audit P01D.allIntro
#print axioms P01D.allIntro
#eval IO.println "AUDIT_END P01D.allIntro"
#eval IO.println "AUDIT_BEGIN P01D.allElim"
#check P01D.allElim
#ortho_audit P01D.allElim
#print axioms P01D.allElim
#eval IO.println "AUDIT_END P01D.allElim"
#eval IO.println "AUDIT_BEGIN P01D.allSelf"
#check P01D.allSelf
#ortho_audit P01D.allSelf
#print axioms P01D.allSelf
#eval IO.println "AUDIT_END P01D.allSelf"
#eval IO.println "AUDIT_BEGIN P01D.constantTy"
#check P01D.constantTy
#ortho_audit P01D.constantTy
#print axioms P01D.constantTy
#eval IO.println "AUDIT_END P01D.constantTy"
#eval IO.println "AUDIT_BEGIN P01D.identity_rel"
#check P01D.identity_rel
#ortho_audit P01D.identity_rel
#print axioms P01D.identity_rel
#eval IO.println "AUDIT_END P01D.identity_rel"
#eval IO.println "AUDIT_BEGIN P01D.identity_link"
#check P01D.identity_link
#ortho_audit P01D.identity_link
#print axioms P01D.identity_link
#eval IO.println "AUDIT_END P01D.identity_link"
#eval IO.println "AUDIT_BEGIN P01D.idParamFamily"
#check P01D.idParamFamily
#ortho_audit P01D.idParamFamily
#print axioms P01D.idParamFamily
#eval IO.println "AUDIT_END P01D.idParamFamily"
#eval IO.println "AUDIT_BEGIN P01D.idBodyTy"
#check P01D.idBodyTy
#ortho_audit P01D.idBodyTy
#print axioms P01D.idBodyTy
#eval IO.println "AUDIT_END P01D.idBodyTy"
#eval IO.println "AUDIT_BEGIN P01D.idAllFormation"
#check P01D.idAllFormation
#ortho_audit P01D.idAllFormation
#print axioms P01D.idAllFormation
#eval IO.println "AUDIT_END P01D.idAllFormation"
#eval IO.println "AUDIT_BEGIN P01D.idAllBody"
#check P01D.idAllBody
#ortho_audit P01D.idAllBody
#print axioms P01D.idAllBody
#eval IO.println "AUDIT_END P01D.idAllBody"
#eval IO.println "AUDIT_BEGIN P01D.polymorphicIdentity"
#check P01D.polymorphicIdentity
#ortho_audit P01D.polymorphicIdentity
#print axioms P01D.polymorphicIdentity
#eval IO.println "AUDIT_END P01D.polymorphicIdentity"
#eval IO.println "AUDIT_BEGIN P01D.polymorphicIdentitySelf"
#check P01D.polymorphicIdentitySelf
#ortho_audit P01D.polymorphicIdentitySelf
#print axioms P01D.polymorphicIdentitySelf
#eval IO.println "AUDIT_END P01D.polymorphicIdentitySelf"
#eval IO.println "AUDIT_BEGIN P01D.atomIdentity"
#check P01D.atomIdentity
#ortho_audit P01D.atomIdentity
#print axioms P01D.atomIdentity
#eval IO.println "AUDIT_END P01D.atomIdentity"
#eval IO.println "AUDIT_BEGIN P01D.dependentReflexivity"
#check P01D.dependentReflexivity
#ortho_audit P01D.dependentReflexivity
#print axioms P01D.dependentReflexivity
#eval IO.println "AUDIT_END P01D.dependentReflexivity"
#eval IO.println "AUDIT_BEGIN P01D.dependentReflexivityEnvelope"
#check P01D.dependentReflexivityEnvelope
#ortho_audit P01D.dependentReflexivityEnvelope
#print axioms P01D.dependentReflexivityEnvelope
#eval IO.println "AUDIT_END P01D.dependentReflexivityEnvelope"
#eval IO.println "AUDIT_BEGIN P01D.pairBody"
#check P01D.pairBody
#ortho_audit P01D.pairBody
#print axioms P01D.pairBody
#eval IO.println "AUDIT_END P01D.pairBody"
#eval IO.println "AUDIT_BEGIN P01D.representedPair"
#check P01D.representedPair
#ortho_audit P01D.representedPair
#print axioms P01D.representedPair
#eval IO.println "AUDIT_END P01D.representedPair"
#eval IO.println "AUDIT_BEGIN P01D.representedPair_eta"
#check P01D.representedPair_eta
#ortho_audit P01D.representedPair_eta
#print axioms P01D.representedPair_eta
#eval IO.println "AUDIT_END P01D.representedPair_eta"
#eval IO.println "AUDIT_BEGIN P01D.constantMotive"
#check P01D.constantMotive
#ortho_audit P01D.constantMotive
#print axioms P01D.constantMotive
#eval IO.println "AUDIT_END P01D.constantMotive"
#eval IO.println "AUDIT_BEGIN P01D.basedJExample"
#check P01D.basedJExample
#ortho_audit P01D.basedJExample
#print axioms P01D.basedJExample
#eval IO.println "AUDIT_END P01D.basedJExample"
#eval IO.println "AUDIT_BEGIN P01D.basedJExample_computes"
#check P01D.basedJExample_computes
#ortho_audit P01D.basedJExample_computes
#print axioms P01D.basedJExample_computes
#eval IO.println "AUDIT_END P01D.basedJExample_computes"
#eval IO.println "AUDIT_BEGIN P01D.polymorphicIdentity_uniform"
#check P01D.polymorphicIdentity_uniform
#ortho_audit P01D.polymorphicIdentity_uniform
#print axioms P01D.polymorphicIdentity_uniform
#eval IO.println "AUDIT_END P01D.polymorphicIdentity_uniform"
#eval IO.println "AUDIT_BEGIN P01Generated.cert_identity"
#check P01Generated.cert_identity
#ortho_audit P01Generated.cert_identity
#print axioms P01Generated.cert_identity
#eval IO.println "AUDIT_END P01Generated.cert_identity"
#eval IO.println "AUDIT_BEGIN P01Generated.checked_identity"
#check P01Generated.checked_identity
#ortho_audit P01Generated.checked_identity
#print axioms P01Generated.checked_identity
#eval IO.println "AUDIT_END P01Generated.checked_identity"
#eval IO.println "AUDIT_BEGIN P01Generated.term_identity"
#check P01Generated.term_identity
#ortho_audit P01Generated.term_identity
#print axioms P01Generated.term_identity
#eval IO.println "AUDIT_END P01Generated.term_identity"
#eval IO.println "AUDIT_BEGIN P01Generated.type_identity"
#check P01Generated.type_identity
#ortho_audit P01Generated.type_identity
#print axioms P01Generated.type_identity
#eval IO.println "AUDIT_END P01Generated.type_identity"
#eval IO.println "AUDIT_BEGIN P01Generated.envelope_identity"
#check P01Generated.envelope_identity
#ortho_audit P01Generated.envelope_identity
#print axioms P01Generated.envelope_identity
#eval IO.println "AUDIT_END P01Generated.envelope_identity"
#eval IO.println "AUDIT_BEGIN P01Generated.derives_identity"
#check P01Generated.derives_identity
#ortho_audit P01Generated.derives_identity
#print axioms P01Generated.derives_identity
#eval IO.println "AUDIT_END P01Generated.derives_identity"
#eval IO.println "AUDIT_BEGIN P01Generated.cert_polymorphic_identity"
#check P01Generated.cert_polymorphic_identity
#ortho_audit P01Generated.cert_polymorphic_identity
#print axioms P01Generated.cert_polymorphic_identity
#eval IO.println "AUDIT_END P01Generated.cert_polymorphic_identity"
#eval IO.println "AUDIT_BEGIN P01Generated.checked_polymorphic_identity"
#check P01Generated.checked_polymorphic_identity
#ortho_audit P01Generated.checked_polymorphic_identity
#print axioms P01Generated.checked_polymorphic_identity
#eval IO.println "AUDIT_END P01Generated.checked_polymorphic_identity"
#eval IO.println "AUDIT_BEGIN P01Generated.term_polymorphic_identity"
#check P01Generated.term_polymorphic_identity
#ortho_audit P01Generated.term_polymorphic_identity
#print axioms P01Generated.term_polymorphic_identity
#eval IO.println "AUDIT_END P01Generated.term_polymorphic_identity"
#eval IO.println "AUDIT_BEGIN P01Generated.type_polymorphic_identity"
#check P01Generated.type_polymorphic_identity
#ortho_audit P01Generated.type_polymorphic_identity
#print axioms P01Generated.type_polymorphic_identity
#eval IO.println "AUDIT_END P01Generated.type_polymorphic_identity"
#eval IO.println "AUDIT_BEGIN P01Generated.envelope_polymorphic_identity"
#check P01Generated.envelope_polymorphic_identity
#ortho_audit P01Generated.envelope_polymorphic_identity
#print axioms P01Generated.envelope_polymorphic_identity
#eval IO.println "AUDIT_END P01Generated.envelope_polymorphic_identity"
#eval IO.println "AUDIT_BEGIN P01Generated.derives_polymorphic_identity"
#check P01Generated.derives_polymorphic_identity
#ortho_audit P01Generated.derives_polymorphic_identity
#print axioms P01Generated.derives_polymorphic_identity
#eval IO.println "AUDIT_END P01Generated.derives_polymorphic_identity"
#eval IO.println "AUDIT_BEGIN P01Generated.cert_identity_self"
#check P01Generated.cert_identity_self
#ortho_audit P01Generated.cert_identity_self
#print axioms P01Generated.cert_identity_self
#eval IO.println "AUDIT_END P01Generated.cert_identity_self"
#eval IO.println "AUDIT_BEGIN P01Generated.checked_identity_self"
#check P01Generated.checked_identity_self
#ortho_audit P01Generated.checked_identity_self
#print axioms P01Generated.checked_identity_self
#eval IO.println "AUDIT_END P01Generated.checked_identity_self"
#eval IO.println "AUDIT_BEGIN P01Generated.term_identity_self"
#check P01Generated.term_identity_self
#ortho_audit P01Generated.term_identity_self
#print axioms P01Generated.term_identity_self
#eval IO.println "AUDIT_END P01Generated.term_identity_self"
#eval IO.println "AUDIT_BEGIN P01Generated.type_identity_self"
#check P01Generated.type_identity_self
#ortho_audit P01Generated.type_identity_self
#print axioms P01Generated.type_identity_self
#eval IO.println "AUDIT_END P01Generated.type_identity_self"
#eval IO.println "AUDIT_BEGIN P01Generated.envelope_identity_self"
#check P01Generated.envelope_identity_self
#ortho_audit P01Generated.envelope_identity_self
#print axioms P01Generated.envelope_identity_self
#eval IO.println "AUDIT_END P01Generated.envelope_identity_self"
#eval IO.println "AUDIT_BEGIN P01Generated.derives_identity_self"
#check P01Generated.derives_identity_self
#ortho_audit P01Generated.derives_identity_self
#print axioms P01Generated.derives_identity_self
#eval IO.println "AUDIT_END P01Generated.derives_identity_self"
#eval IO.println "AUDIT_BEGIN P01Generated.cert_binder_identity"
#check P01Generated.cert_binder_identity
#ortho_audit P01Generated.cert_binder_identity
#print axioms P01Generated.cert_binder_identity
#eval IO.println "AUDIT_END P01Generated.cert_binder_identity"
#eval IO.println "AUDIT_BEGIN P01Generated.checked_binder_identity"
#check P01Generated.checked_binder_identity
#ortho_audit P01Generated.checked_binder_identity
#print axioms P01Generated.checked_binder_identity
#eval IO.println "AUDIT_END P01Generated.checked_binder_identity"
#eval IO.println "AUDIT_BEGIN P01Generated.term_binder_identity"
#check P01Generated.term_binder_identity
#ortho_audit P01Generated.term_binder_identity
#print axioms P01Generated.term_binder_identity
#eval IO.println "AUDIT_END P01Generated.term_binder_identity"
#eval IO.println "AUDIT_BEGIN P01Generated.type_binder_identity"
#check P01Generated.type_binder_identity
#ortho_audit P01Generated.type_binder_identity
#print axioms P01Generated.type_binder_identity
#eval IO.println "AUDIT_END P01Generated.type_binder_identity"
#eval IO.println "AUDIT_BEGIN P01Generated.envelope_binder_identity"
#check P01Generated.envelope_binder_identity
#ortho_audit P01Generated.envelope_binder_identity
#print axioms P01Generated.envelope_binder_identity
#eval IO.println "AUDIT_END P01Generated.envelope_binder_identity"
#eval IO.println "AUDIT_BEGIN P01Generated.derives_binder_identity"
#check P01Generated.derives_binder_identity
#ortho_audit P01Generated.derives_binder_identity
#print axioms P01Generated.derives_binder_identity
#eval IO.println "AUDIT_END P01Generated.derives_binder_identity"
#eval IO.println "AUDIT_BEGIN P01Generated.cert_binder_K"
#check P01Generated.cert_binder_K
#ortho_audit P01Generated.cert_binder_K
#print axioms P01Generated.cert_binder_K
#eval IO.println "AUDIT_END P01Generated.cert_binder_K"
#eval IO.println "AUDIT_BEGIN P01Generated.checked_binder_K"
#check P01Generated.checked_binder_K
#ortho_audit P01Generated.checked_binder_K
#print axioms P01Generated.checked_binder_K
#eval IO.println "AUDIT_END P01Generated.checked_binder_K"
#eval IO.println "AUDIT_BEGIN P01Generated.term_binder_K"
#check P01Generated.term_binder_K
#ortho_audit P01Generated.term_binder_K
#print axioms P01Generated.term_binder_K
#eval IO.println "AUDIT_END P01Generated.term_binder_K"
#eval IO.println "AUDIT_BEGIN P01Generated.type_binder_K"
#check P01Generated.type_binder_K
#ortho_audit P01Generated.type_binder_K
#print axioms P01Generated.type_binder_K
#eval IO.println "AUDIT_END P01Generated.type_binder_K"
#eval IO.println "AUDIT_BEGIN P01Generated.envelope_binder_K"
#check P01Generated.envelope_binder_K
#ortho_audit P01Generated.envelope_binder_K
#print axioms P01Generated.envelope_binder_K
#eval IO.println "AUDIT_END P01Generated.envelope_binder_K"
#eval IO.println "AUDIT_BEGIN P01Generated.derives_binder_K"
#check P01Generated.derives_binder_K
#ortho_audit P01Generated.derives_binder_K
#print axioms P01Generated.derives_binder_K
#eval IO.println "AUDIT_END P01Generated.derives_binder_K"
#eval IO.println "AUDIT_BEGIN P01Generated.cert_binder_S"
#check P01Generated.cert_binder_S
#ortho_audit P01Generated.cert_binder_S
#print axioms P01Generated.cert_binder_S
#eval IO.println "AUDIT_END P01Generated.cert_binder_S"
#eval IO.println "AUDIT_BEGIN P01Generated.checked_binder_S"
#check P01Generated.checked_binder_S
#ortho_audit P01Generated.checked_binder_S
#print axioms P01Generated.checked_binder_S
#eval IO.println "AUDIT_END P01Generated.checked_binder_S"
#eval IO.println "AUDIT_BEGIN P01Generated.term_binder_S"
#check P01Generated.term_binder_S
#ortho_audit P01Generated.term_binder_S
#print axioms P01Generated.term_binder_S
#eval IO.println "AUDIT_END P01Generated.term_binder_S"
#eval IO.println "AUDIT_BEGIN P01Generated.type_binder_S"
#check P01Generated.type_binder_S
#ortho_audit P01Generated.type_binder_S
#print axioms P01Generated.type_binder_S
#eval IO.println "AUDIT_END P01Generated.type_binder_S"
#eval IO.println "AUDIT_BEGIN P01Generated.envelope_binder_S"
#check P01Generated.envelope_binder_S
#ortho_audit P01Generated.envelope_binder_S
#print axioms P01Generated.envelope_binder_S
#eval IO.println "AUDIT_END P01Generated.envelope_binder_S"
#eval IO.println "AUDIT_BEGIN P01Generated.derives_binder_S"
#check P01Generated.derives_binder_S
#ortho_audit P01Generated.derives_binder_S
#print axioms P01Generated.derives_binder_S
#eval IO.println "AUDIT_END P01Generated.derives_binder_S"
#eval IO.println "AUDIT_BEGIN P01F.LTerm"
#check P01F.LTerm
#ortho_audit P01F.LTerm
#print axioms P01F.LTerm
#eval IO.println "AUDIT_END P01F.LTerm"
#eval IO.println "AUDIT_BEGIN P01F.ren"
#check P01F.ren
#ortho_audit P01F.ren
#print axioms P01F.ren
#eval IO.println "AUDIT_END P01F.ren"
#eval IO.println "AUDIT_BEGIN P01F.up"
#check P01F.up
#ortho_audit P01F.up
#print axioms P01F.up
#eval IO.println "AUDIT_END P01F.up"
#eval IO.println "AUDIT_BEGIN P01F.sub"
#check P01F.sub
#ortho_audit P01F.sub
#print axioms P01F.sub
#eval IO.println "AUDIT_END P01F.sub"
#eval IO.println "AUDIT_BEGIN P01F.single"
#check P01F.single
#ortho_audit P01F.single
#print axioms P01F.single
#eval IO.println "AUDIT_END P01F.single"
#eval IO.println "AUDIT_BEGIN P01F.inst"
#check P01F.inst
#ortho_audit P01F.inst
#print axioms P01F.inst
#eval IO.println "AUDIT_END P01F.inst"
#eval IO.println "AUDIT_BEGIN P01F.ren_id"
#check P01F.ren_id
#ortho_audit P01F.ren_id
#print axioms P01F.ren_id
#eval IO.println "AUDIT_END P01F.ren_id"
#eval IO.println "AUDIT_BEGIN P01F.ren_comp"
#check P01F.ren_comp
#ortho_audit P01F.ren_comp
#print axioms P01F.ren_comp
#eval IO.println "AUDIT_END P01F.ren_comp"
#eval IO.println "AUDIT_BEGIN P01F.sub_id"
#check P01F.sub_id
#ortho_audit P01F.sub_id
#print axioms P01F.sub_id
#eval IO.println "AUDIT_END P01F.sub_id"
#eval IO.println "AUDIT_BEGIN P01F.sub_ren"
#check P01F.sub_ren
#ortho_audit P01F.sub_ren
#print axioms P01F.sub_ren
#eval IO.println "AUDIT_END P01F.sub_ren"
#eval IO.println "AUDIT_BEGIN P01F.ren_sub"
#check P01F.ren_sub
#ortho_audit P01F.ren_sub
#print axioms P01F.ren_sub
#eval IO.println "AUDIT_END P01F.ren_sub"
#eval IO.println "AUDIT_BEGIN P01F.sub_comp"
#check P01F.sub_comp
#ortho_audit P01F.sub_comp
#print axioms P01F.sub_comp
#eval IO.println "AUDIT_END P01F.sub_comp"
#eval IO.println "AUDIT_BEGIN P01F.sub_up_shift"
#check P01F.sub_up_shift
#ortho_audit P01F.sub_up_shift
#print axioms P01F.sub_up_shift
#eval IO.println "AUDIT_END P01F.sub_up_shift"
#eval IO.println "AUDIT_BEGIN P01F.inst_shift"
#check P01F.inst_shift
#ortho_audit P01F.inst_shift
#print axioms P01F.inst_shift
#eval IO.println "AUDIT_END P01F.inst_shift"
#eval IO.println "AUDIT_BEGIN P01F.sub_inst"
#check P01F.sub_inst
#ortho_audit P01F.sub_inst
#print axioms P01F.sub_inst
#eval IO.println "AUDIT_END P01F.sub_inst"
#eval IO.println "AUDIT_BEGIN P01F.Beta"
#check P01F.Beta
#ortho_audit P01F.Beta
#print axioms P01F.Beta
#eval IO.println "AUDIT_END P01F.Beta"
#eval IO.println "AUDIT_BEGIN P01F.BStar"
#check P01F.BStar
#ortho_audit P01F.BStar
#print axioms P01F.BStar
#eval IO.println "AUDIT_END P01F.BStar"
#eval IO.println "AUDIT_BEGIN P01F.BPositive"
#check P01F.BPositive
#ortho_audit P01F.BPositive
#print axioms P01F.BPositive
#eval IO.println "AUDIT_END P01F.BPositive"
#eval IO.println "AUDIT_BEGIN P01F.beta_sub"
#check P01F.beta_sub
#ortho_audit P01F.beta_sub
#print axioms P01F.beta_sub
#eval IO.println "AUDIT_END P01F.beta_sub"
#eval IO.println "AUDIT_BEGIN P01F.bstar_trans"
#check P01F.bstar_trans
#ortho_audit P01F.bstar_trans
#print axioms P01F.bstar_trans
#eval IO.println "AUDIT_END P01F.bstar_trans"
#eval IO.println "AUDIT_BEGIN P01F.bstar_left"
#check P01F.bstar_left
#ortho_audit P01F.bstar_left
#print axioms P01F.bstar_left
#eval IO.println "AUDIT_END P01F.bstar_left"
#eval IO.println "AUDIT_BEGIN P01F.bstar_right"
#check P01F.bstar_right
#ortho_audit P01F.bstar_right
#print axioms P01F.bstar_right
#eval IO.println "AUDIT_END P01F.bstar_right"
#eval IO.println "AUDIT_BEGIN P01F.BConv"
#check P01F.BConv
#ortho_audit P01F.BConv
#print axioms P01F.BConv
#eval IO.println "AUDIT_END P01F.BConv"
#eval IO.println "AUDIT_BEGIN P01F.bstar_conv"
#check P01F.bstar_conv
#ortho_audit P01F.bstar_conv
#print axioms P01F.bstar_conv
#eval IO.println "AUDIT_END P01F.bstar_conv"
#eval IO.println "AUDIT_BEGIN P01Source.tower"
#check P01Source.tower
#ortho_audit P01Source.tower
#print axioms P01Source.tower
#eval IO.println "AUDIT_END P01Source.tower"
#eval IO.println "AUDIT_BEGIN P01Source.omegaShape"
#check P01Source.omegaShape
#ortho_audit P01Source.omegaShape
#print axioms P01Source.omegaShape
#eval IO.println "AUDIT_END P01Source.omegaShape"
#eval IO.println "AUDIT_BEGIN P01Source.duplicator_normal"
#check P01Source.duplicator_normal
#ortho_audit P01Source.duplicator_normal
#print axioms P01Source.duplicator_normal
#eval IO.println "AUDIT_END P01Source.duplicator_normal"
#eval IO.println "AUDIT_BEGIN P01Source.tower_step"
#check P01Source.tower_step
#ortho_audit P01Source.tower_step
#print axioms P01Source.tower_step
#eval IO.println "AUDIT_END P01Source.tower_step"
#eval IO.println "AUDIT_BEGIN P01Source.shape_step"
#check P01Source.shape_step
#ortho_audit P01Source.shape_step
#print axioms P01Source.shape_step
#eval IO.println "AUDIT_END P01Source.shape_step"
#eval IO.println "AUDIT_BEGIN P01Source.shape_has_step"
#check P01Source.shape_has_step
#ortho_audit P01Source.shape_has_step
#print axioms P01Source.shape_has_step
#eval IO.println "AUDIT_END P01Source.shape_has_step"
#eval IO.println "AUDIT_BEGIN P01Source.shape_red"
#check P01Source.shape_red
#ortho_audit P01Source.shape_red
#print axioms P01Source.shape_red
#eval IO.println "AUDIT_END P01Source.shape_red"
#eval IO.println "AUDIT_BEGIN P01Source.omega_no_normal_reduct"
#check P01Source.omega_no_normal_reduct
#ortho_audit P01Source.omega_no_normal_reduct
#print axioms P01Source.omega_no_normal_reduct
#eval IO.println "AUDIT_END P01Source.omega_no_normal_reduct"
#eval IO.println "AUDIT_BEGIN P01Source.omega_no_finite_representative"
#check P01Source.omega_no_finite_representative
#ortho_audit P01Source.omega_no_finite_representative
#print axioms P01Source.omega_no_finite_representative
#eval IO.println "AUDIT_END P01Source.omega_no_finite_representative"
#eval IO.println "AUDIT_BEGIN P01Source.omega_semantic_bottom_arrow"
#check P01Source.omega_semantic_bottom_arrow
#ortho_audit P01Source.omega_semantic_bottom_arrow
#print axioms P01Source.omega_semantic_bottom_arrow
#eval IO.println "AUDIT_END P01Source.omega_semantic_bottom_arrow"
#eval IO.println "AUDIT_BEGIN P01D.PER"
#check P01D.PER
#ortho_audit P01D.PER
#print axioms P01D.PER
#eval IO.println "AUDIT_END P01D.PER"
#eval IO.println "AUDIT_BEGIN P01D.PER.dom"
#check P01D.PER.dom
#ortho_audit P01D.PER.dom
#print axioms P01D.PER.dom
#eval IO.println "AUDIT_END P01D.PER.dom"
#eval IO.println "AUDIT_BEGIN P01D.PER.left"
#check P01D.PER.left
#ortho_audit P01D.PER.left
#print axioms P01D.PER.left
#eval IO.println "AUDIT_END P01D.PER.left"
#eval IO.println "AUDIT_BEGIN P01D.PER.right"
#check P01D.PER.right
#ortho_audit P01D.PER.right
#print axioms P01D.PER.right
#eval IO.println "AUDIT_END P01D.PER.right"
#eval IO.println "AUDIT_BEGIN P01D.per_ext"
#check P01D.per_ext
#ortho_audit P01D.per_ext
#print axioms P01D.per_ext
#eval IO.println "AUDIT_END P01D.per_ext"
#eval IO.println "AUDIT_BEGIN P01D.botPER"
#check P01D.botPER
#ortho_audit P01D.botPER
#print axioms P01D.botPER
#eval IO.println "AUDIT_END P01D.botPER"
#eval IO.println "AUDIT_BEGIN P01D.rawPER"
#check P01D.rawPER
#ortho_audit P01D.rawPER
#print axioms P01D.rawPER
#eval IO.println "AUDIT_END P01D.rawPER"
#eval IO.println "AUDIT_BEGIN P01D.conv_app"
#check P01D.conv_app
#ortho_audit P01D.conv_app
#print axioms P01D.conv_app
#eval IO.println "AUDIT_END P01D.conv_app"
#eval IO.println "AUDIT_BEGIN P01D.PiPER"
#check P01D.PiPER
#ortho_audit P01D.PiPER
#print axioms P01D.PiPER
#eval IO.println "AUDIT_END P01D.PiPER"
#eval IO.println "AUDIT_BEGIN P01D.ArrPER"
#check P01D.ArrPER
#ortho_audit P01D.ArrPER
#print axioms P01D.ArrPER
#eval IO.println "AUDIT_END P01D.ArrPER"
#eval IO.println "AUDIT_BEGIN P01D.Link"
#check P01D.Link
#ortho_audit P01D.Link
#print axioms P01D.Link
#eval IO.println "AUDIT_END P01D.Link"
#eval IO.println "AUDIT_BEGIN P01D.Link.raw"
#check P01D.Link.raw
#ortho_audit P01D.Link.raw
#print axioms P01D.Link.raw
#eval IO.println "AUDIT_END P01D.Link.raw"
#eval IO.println "AUDIT_BEGIN P01D.diagonal"
#check P01D.diagonal
#ortho_audit P01D.diagonal
#print axioms P01D.diagonal
#eval IO.println "AUDIT_END P01D.diagonal"
#eval IO.println "AUDIT_BEGIN P01D.arrowLink"
#check P01D.arrowLink
#ortho_audit P01D.arrowLink
#print axioms P01D.arrowLink
#eval IO.println "AUDIT_END P01D.arrowLink"
#eval IO.println "AUDIT_BEGIN P01D.arrow_identity"
#check P01D.arrow_identity
#ortho_audit P01D.arrow_identity
#print axioms P01D.arrow_identity
#eval IO.println "AUDIT_END P01D.arrow_identity"
#eval IO.println "AUDIT_BEGIN P01D.pair_congr"
#check P01D.pair_congr
#ortho_audit P01D.pair_congr
#print axioms P01D.pair_congr
#eval IO.println "AUDIT_END P01D.pair_congr"
#eval IO.println "AUDIT_BEGIN P01D.Represented"
#check P01D.Represented
#ortho_audit P01D.Represented
#print axioms P01D.Represented
#eval IO.println "AUDIT_END P01D.Represented"
#eval IO.println "AUDIT_BEGIN P01D.pair_represented"
#check P01D.pair_represented
#ortho_audit P01D.pair_represented
#print axioms P01D.pair_represented
#eval IO.println "AUDIT_END P01D.pair_represented"
#eval IO.println "AUDIT_BEGIN P01D.represented_raw"
#check P01D.represented_raw
#ortho_audit P01D.represented_raw
#print axioms P01D.represented_raw
#eval IO.println "AUDIT_END P01D.represented_raw"
#eval IO.println "AUDIT_BEGIN P01D.SigmaPER"
#check P01D.SigmaPER
#ortho_audit P01D.SigmaPER
#print axioms P01D.SigmaPER
#eval IO.println "AUDIT_END P01D.SigmaPER"
#eval IO.println "AUDIT_BEGIN P01D.sigma_pair"
#check P01D.sigma_pair
#ortho_audit P01D.sigma_pair
#print axioms P01D.sigma_pair
#eval IO.println "AUDIT_END P01D.sigma_pair"
#eval IO.println "AUDIT_BEGIN P01D.sigma_witness_iff"
#check P01D.sigma_witness_iff
#ortho_audit P01D.sigma_witness_iff
#print axioms P01D.sigma_witness_iff
#eval IO.println "AUDIT_END P01D.sigma_witness_iff"
#eval IO.println "AUDIT_BEGIN P01D.sigma_eta"
#check P01D.sigma_eta
#ortho_audit P01D.sigma_eta
#print axioms P01D.sigma_eta
#eval IO.println "AUDIT_END P01D.sigma_eta"
#eval IO.println "AUDIT_BEGIN P01D.IdPER"
#check P01D.IdPER
#ortho_audit P01D.IdPER
#print axioms P01D.IdPER
#eval IO.println "AUDIT_END P01D.IdPER"
#eval IO.println "AUDIT_BEGIN P01D.id_intro"
#check P01D.id_intro
#ortho_audit P01D.id_intro
#print axioms P01D.id_intro
#eval IO.println "AUDIT_END P01D.id_intro"
#eval IO.println "AUDIT_BEGIN P01D.BasedMotive"
#check P01D.BasedMotive
#ortho_audit P01D.BasedMotive
#print axioms P01D.BasedMotive
#eval IO.println "AUDIT_END P01D.BasedMotive"
#eval IO.println "AUDIT_BEGIN P01D.based_transport"
#check P01D.based_transport
#ortho_audit P01D.based_transport
#print axioms P01D.based_transport
#eval IO.println "AUDIT_END P01D.based_transport"
#eval IO.println "AUDIT_BEGIN P01D.Jterm"
#check P01D.Jterm
#ortho_audit P01D.Jterm
#print axioms P01D.Jterm
#eval IO.println "AUDIT_END P01D.Jterm"
#eval IO.println "AUDIT_BEGIN P01D.J_red"
#check P01D.J_red
#ortho_audit P01D.J_red
#print axioms P01D.J_red
#eval IO.println "AUDIT_END P01D.J_red"
#eval IO.println "AUDIT_BEGIN P01D.based_J"
#check P01D.based_J
#ortho_audit P01D.based_J
#print axioms P01D.based_J
#eval IO.println "AUDIT_END P01D.based_J"
#eval IO.println "AUDIT_BEGIN P01D.ParamFamily"
#check P01D.ParamFamily
#ortho_audit P01D.ParamFamily
#print axioms P01D.ParamFamily
#eval IO.println "AUDIT_END P01D.ParamFamily"
#eval IO.println "AUDIT_BEGIN P01D.Parametric"
#check P01D.Parametric
#ortho_audit P01D.Parametric
#print axioms P01D.Parametric
#eval IO.println "AUDIT_END P01D.Parametric"
#eval IO.println "AUDIT_BEGIN P01D.AllPER"
#check P01D.AllPER
#ortho_audit P01D.AllPER
#print axioms P01D.AllPER
#eval IO.println "AUDIT_END P01D.AllPER"
#eval IO.println "AUDIT_BEGIN P01D.all_domain"
#check P01D.all_domain
#ortho_audit P01D.all_domain
#print axioms P01D.all_domain
#eval IO.println "AUDIT_END P01D.all_domain"
#eval IO.println "AUDIT_BEGIN P01D.AllDiagonal"
#check P01D.AllDiagonal
#ortho_audit P01D.AllDiagonal
#print axioms P01D.AllDiagonal
#eval IO.println "AUDIT_END P01D.AllDiagonal"
#eval IO.println "AUDIT_BEGIN P01D.all_identity_extension"
#check P01D.all_identity_extension
#ortho_audit P01D.all_identity_extension
#print axioms P01D.all_identity_extension
#eval IO.println "AUDIT_END P01D.all_identity_extension"
#eval IO.println "AUDIT_BEGIN P01D.all_eliminate"
#check P01D.all_eliminate
#ortho_audit P01D.all_eliminate
#print axioms P01D.all_eliminate
#eval IO.println "AUDIT_END P01D.all_eliminate"
#eval IO.println "AUDIT_BEGIN P01D.all_self_eliminate"
#check P01D.all_self_eliminate
#ortho_audit P01D.all_self_eliminate
#print axioms P01D.all_self_eliminate
#eval IO.println "AUDIT_END P01D.all_self_eliminate"
#eval IO.println "AUDIT_BEGIN P01D.Poly"
#check P01D.Poly
#ortho_audit P01D.Poly
#print axioms P01D.Poly
#eval IO.println "AUDIT_END P01D.Poly"
#eval IO.println "AUDIT_BEGIN P01D.Env"
#check P01D.Env
#ortho_audit P01D.Env
#print axioms P01D.Env
#eval IO.println "AUDIT_END P01D.Env"
#eval IO.println "AUDIT_BEGIN P01D.eval"
#check P01D.eval
#ortho_audit P01D.eval
#print axioms P01D.eval
#eval IO.println "AUDIT_END P01D.eval"
#eval IO.println "AUDIT_BEGIN P01D.psub"
#check P01D.psub
#ortho_audit P01D.psub
#print axioms P01D.psub
#eval IO.println "AUDIT_END P01D.psub"
#eval IO.println "AUDIT_BEGIN P01D.pren"
#check P01D.pren
#ortho_audit P01D.pren
#print axioms P01D.pren
#eval IO.println "AUDIT_END P01D.pren"
#eval IO.println "AUDIT_BEGIN P01D.pup"
#check P01D.pup
#ortho_audit P01D.pup
#print axioms P01D.pup
#eval IO.println "AUDIT_END P01D.pup"
#eval IO.println "AUDIT_BEGIN P01D.eval_sub"
#check P01D.eval_sub
#ortho_audit P01D.eval_sub
#print axioms P01D.eval_sub
#eval IO.println "AUDIT_END P01D.eval_sub"
#eval IO.println "AUDIT_BEGIN P01D.psub_id"
#check P01D.psub_id
#ortho_audit P01D.psub_id
#print axioms P01D.psub_id
#eval IO.println "AUDIT_END P01D.psub_id"
#eval IO.println "AUDIT_BEGIN P01D.psub_comp"
#check P01D.psub_comp
#ortho_audit P01D.psub_comp
#print axioms P01D.psub_comp
#eval IO.println "AUDIT_END P01D.psub_comp"
#eval IO.println "AUDIT_BEGIN P01D.eval_ren"
#check P01D.eval_ren
#ortho_audit P01D.eval_ren
#print axioms P01D.eval_ren
#eval IO.println "AUDIT_END P01D.eval_ren"
#eval IO.println "AUDIT_BEGIN P01D.freeZero"
#check P01D.freeZero
#ortho_audit P01D.freeZero
#print axioms P01D.freeZero
#eval IO.println "AUDIT_END P01D.freeZero"
#eval IO.println "AUDIT_BEGIN P01D.drop"
#check P01D.drop
#ortho_audit P01D.drop
#print axioms P01D.drop
#eval IO.println "AUDIT_END P01D.drop"
#eval IO.println "AUDIT_BEGIN P01D.abstract"
#check P01D.abstract
#ortho_audit P01D.abstract
#print axioms P01D.abstract
#eval IO.println "AUDIT_END P01D.abstract"
#eval IO.println "AUDIT_BEGIN P01D.freeZero_pren_succ"
#check P01D.freeZero_pren_succ
#ortho_audit P01D.freeZero_pren_succ
#print axioms P01D.freeZero_pren_succ
#eval IO.println "AUDIT_END P01D.freeZero_pren_succ"
#eval IO.println "AUDIT_BEGIN P01D.drop_pren_succ"
#check P01D.drop_pren_succ
#ortho_audit P01D.drop_pren_succ
#print axioms P01D.drop_pren_succ
#eval IO.println "AUDIT_END P01D.drop_pren_succ"
#eval IO.println "AUDIT_BEGIN P01D.freeZero_lifted_sub"
#check P01D.freeZero_lifted_sub
#ortho_audit P01D.freeZero_lifted_sub
#print axioms P01D.freeZero_lifted_sub
#eval IO.println "AUDIT_END P01D.freeZero_lifted_sub"
#eval IO.println "AUDIT_BEGIN P01D.drop_lifted_sub_absent"
#check P01D.drop_lifted_sub_absent
#ortho_audit P01D.drop_lifted_sub_absent
#print axioms P01D.drop_lifted_sub_absent
#eval IO.println "AUDIT_END P01D.drop_lifted_sub_absent"
#eval IO.println "AUDIT_BEGIN P01D.abstract_absent"
#check P01D.abstract_absent
#ortho_audit P01D.abstract_absent
#print axioms P01D.abstract_absent
#eval IO.println "AUDIT_END P01D.abstract_absent"
#eval IO.println "AUDIT_BEGIN P01D.abstract_present_app"
#check P01D.abstract_present_app
#ortho_audit P01D.abstract_present_app
#print axioms P01D.abstract_present_app
#eval IO.println "AUDIT_END P01D.abstract_present_app"
#eval IO.println "AUDIT_BEGIN P01D.abstraction_naturality"
#check P01D.abstraction_naturality
#ortho_audit P01D.abstraction_naturality
#print axioms P01D.abstraction_naturality
#eval IO.println "AUDIT_END P01D.abstraction_naturality"
#eval IO.println "AUDIT_BEGIN P01D.eval_absent"
#check P01D.eval_absent
#ortho_audit P01D.eval_absent
#print axioms P01D.eval_absent
#eval IO.println "AUDIT_END P01D.eval_absent"
#eval IO.println "AUDIT_BEGIN P01D.abstraction_beta"
#check P01D.abstraction_beta
#ortho_audit P01D.abstraction_beta
#print axioms P01D.abstraction_beta
#eval IO.println "AUDIT_END P01D.abstraction_beta"
#eval IO.println "AUDIT_BEGIN P01D.abstraction_substitution"
#check P01D.abstraction_substitution
#ortho_audit P01D.abstraction_substitution
#print axioms P01D.abstraction_substitution
#eval IO.println "AUDIT_END P01D.abstraction_substitution"
#eval IO.println "AUDIT_BEGIN P01D.pairPoly"
#check P01D.pairPoly
#ortho_audit P01D.pairPoly
#print axioms P01D.pairPoly
#eval IO.println "AUDIT_END P01D.pairPoly"
#eval IO.println "AUDIT_BEGIN P01D.fstPoly"
#check P01D.fstPoly
#ortho_audit P01D.fstPoly
#print axioms P01D.fstPoly
#eval IO.println "AUDIT_END P01D.fstPoly"
#eval IO.println "AUDIT_BEGIN P01D.sndPoly"
#check P01D.sndPoly
#ortho_audit P01D.sndPoly
#print axioms P01D.sndPoly
#eval IO.println "AUDIT_END P01D.sndPoly"
#eval IO.println "AUDIT_BEGIN P01D.jPoly"
#check P01D.jPoly
#ortho_audit P01D.jPoly
#print axioms P01D.jPoly
#eval IO.println "AUDIT_END P01D.jPoly"
#eval IO.println "AUDIT_BEGIN P01D.eval_pair"
#check P01D.eval_pair
#ortho_audit P01D.eval_pair
#print axioms P01D.eval_pair
#eval IO.println "AUDIT_END P01D.eval_pair"
#eval IO.println "AUDIT_BEGIN P01D.eval_fst"
#check P01D.eval_fst
#ortho_audit P01D.eval_fst
#print axioms P01D.eval_fst
#eval IO.println "AUDIT_END P01D.eval_fst"
#eval IO.println "AUDIT_BEGIN P01D.eval_snd"
#check P01D.eval_snd
#ortho_audit P01D.eval_snd
#print axioms P01D.eval_snd
#eval IO.println "AUDIT_END P01D.eval_snd"
#eval IO.println "AUDIT_BEGIN P01D.eval_j"
#check P01D.eval_j
#ortho_audit P01D.eval_j
#print axioms P01D.eval_j
#eval IO.println "AUDIT_END P01D.eval_j"
#eval IO.println "AUDIT_BEGIN P01F.bstar_under"
#check P01F.bstar_under
#ortho_audit P01F.bstar_under
#print axioms P01F.bstar_under
#eval IO.println "AUDIT_END P01F.bstar_under"
#eval IO.println "AUDIT_BEGIN P01F.SKK_beta_I"
#check P01F.SKK_beta_I
#ortho_audit P01F.SKK_beta_I
#print axioms P01F.SKK_beta_I
#eval IO.println "AUDIT_END P01F.SKK_beta_I"
#eval IO.println "AUDIT_BEGIN P01F.target_conversion_reflection_false"
#check P01F.target_conversion_reflection_false
#ortho_audit P01F.target_conversion_reflection_false
#print axioms P01F.target_conversion_reflection_false
#eval IO.println "AUDIT_END P01F.target_conversion_reflection_false"
#eval IO.println "AUDIT_BEGIN P01SNReflection.Star"
#check P01SNReflection.Star
#ortho_audit P01SNReflection.Star
#print axioms P01SNReflection.Star
#eval IO.println "AUDIT_END P01SNReflection.Star"
#eval IO.println "AUDIT_BEGIN P01SNReflection.Positive"
#check P01SNReflection.Positive
#ortho_audit P01SNReflection.Positive
#print axioms P01SNReflection.Positive
#eval IO.println "AUDIT_END P01SNReflection.Positive"
#eval IO.println "AUDIT_BEGIN P01SNReflection.SN"
#check P01SNReflection.SN
#ortho_audit P01SNReflection.SN
#print axioms P01SNReflection.SN
#eval IO.println "AUDIT_END P01SNReflection.SN"
#eval IO.println "AUDIT_BEGIN P01SNReflection.positive_simulation_reflects_SN"
#check P01SNReflection.positive_simulation_reflects_SN
#ortho_audit P01SNReflection.positive_simulation_reflects_SN
#print axioms P01SNReflection.positive_simulation_reflects_SN
#eval IO.println "AUDIT_END P01SNReflection.positive_simulation_reflects_SN"
#eval IO.println "AUDIT_BEGIN P01F.Context"
#check P01F.Context
#ortho_audit P01F.Context
#print axioms P01F.Context
#eval IO.println "AUDIT_END P01F.Context"
#eval IO.println "AUDIT_BEGIN P01F.shiftContext"
#check P01F.shiftContext
#ortho_audit P01F.shiftContext
#print axioms P01F.shiftContext
#eval IO.println "AUDIT_END P01F.shiftContext"
#eval IO.println "AUDIT_BEGIN P01F.subContext"
#check P01F.subContext
#ortho_audit P01F.subContext
#print axioms P01F.subContext
#eval IO.println "AUDIT_END P01F.subContext"
#eval IO.println "AUDIT_BEGIN P01F.Has"
#check P01F.Has
#ortho_audit P01F.Has
#print axioms P01F.Has
#eval IO.println "AUDIT_END P01F.Has"
#eval IO.println "AUDIT_BEGIN P01F.subContext_cons"
#check P01F.subContext_cons
#ortho_audit P01F.subContext_cons
#print axioms P01F.subContext_cons
#eval IO.println "AUDIT_END P01F.subContext_cons"
#eval IO.println "AUDIT_BEGIN P01F.subContext_up"
#check P01F.subContext_up
#ortho_audit P01F.subContext_up
#print axioms P01F.subContext_up
#eval IO.println "AUDIT_END P01F.subContext_up"
#eval IO.println "AUDIT_BEGIN P01F.subContext_single_shift"
#check P01F.subContext_single_shift
#ortho_audit P01F.subContext_single_shift
#print axioms P01F.subContext_single_shift
#eval IO.println "AUDIT_END P01F.subContext_single_shift"
#eval IO.println "AUDIT_BEGIN P01F.type_substitution"
#check P01F.type_substitution
#ortho_audit P01F.type_substitution
#print axioms P01F.type_substitution
#eval IO.println "AUDIT_END P01F.type_substitution"
#eval IO.println "AUDIT_BEGIN P01F.type_renaming"
#check P01F.type_renaming
#ortho_audit P01F.type_renaming
#print axioms P01F.type_renaming
#eval IO.println "AUDIT_END P01F.type_renaming"
#eval IO.println "AUDIT_BEGIN P01F.term_renaming"
#check P01F.term_renaming
#ortho_audit P01F.term_renaming
#print axioms P01F.term_renaming
#eval IO.println "AUDIT_END P01F.term_renaming"
#eval IO.println "AUDIT_BEGIN P01F.term_weakening"
#check P01F.term_weakening
#ortho_audit P01F.term_weakening
#print axioms P01F.term_weakening
#eval IO.println "AUDIT_END P01F.term_weakening"
#eval IO.println "AUDIT_BEGIN P01F.term_substitution"
#check P01F.term_substitution
#ortho_audit P01F.term_substitution
#print axioms P01F.term_substitution
#eval IO.println "AUDIT_END P01F.term_substitution"
#eval IO.println "AUDIT_BEGIN P01F.instantiate_term"
#check P01F.instantiate_term
#ortho_audit P01F.instantiate_term
#print axioms P01F.instantiate_term
#eval IO.println "AUDIT_END P01F.instantiate_term"
#eval IO.println "AUDIT_BEGIN P01F.LamView"
#check P01F.LamView
#ortho_audit P01F.LamView
#print axioms P01F.LamView
#eval IO.println "AUDIT_END P01F.LamView"
#eval IO.println "AUDIT_BEGIN P01F.lamView_substitution"
#check P01F.lamView_substitution
#ortho_audit P01F.lamView_substitution
#print axioms P01F.lamView_substitution
#eval IO.println "AUDIT_END P01F.lamView_substitution"
#eval IO.println "AUDIT_BEGIN P01F.lamView_instantiation"
#check P01F.lamView_instantiation
#ortho_audit P01F.lamView_instantiation
#print axioms P01F.lamView_instantiation
#eval IO.println "AUDIT_END P01F.lamView_instantiation"
#eval IO.println "AUDIT_BEGIN P01F.lambda_view"
#check P01F.lambda_view
#ortho_audit P01F.lambda_view
#print axioms P01F.lambda_view
#eval IO.println "AUDIT_END P01F.lambda_view"
#eval IO.println "AUDIT_BEGIN P01F.lambda_generation"
#check P01F.lambda_generation
#ortho_audit P01F.lambda_generation
#print axioms P01F.lambda_generation
#eval IO.println "AUDIT_END P01F.lambda_generation"
#eval IO.println "AUDIT_BEGIN P01F.subject_reduction"
#check P01F.subject_reduction
#ortho_audit P01F.subject_reduction
#print axioms P01F.subject_reduction
#eval IO.println "AUDIT_END P01F.subject_reduction"
#eval IO.println "AUDIT_BEGIN P01F.subject_reduction_star"
#check P01F.subject_reduction_star
#ortho_audit P01F.subject_reduction_star
#print axioms P01F.subject_reduction_star
#eval IO.println "AUDIT_END P01F.subject_reduction_star"
#eval IO.println "AUDIT_BEGIN P01F.translateType"
#check P01F.translateType
#ortho_audit P01F.translateType
#print axioms P01F.translateType
#eval IO.println "AUDIT_END P01F.translateType"
#eval IO.println "AUDIT_BEGIN P01F.translate"
#check P01F.translate
#ortho_audit P01F.translate
#print axioms P01F.translate
#eval IO.println "AUDIT_END P01F.translate"
#eval IO.println "AUDIT_BEGIN P01F.translate_ren"
#check P01F.translate_ren
#ortho_audit P01F.translate_ren
#print axioms P01F.translate_ren
#eval IO.println "AUDIT_END P01F.translate_ren"
#eval IO.println "AUDIT_BEGIN P01F.translate_sub"
#check P01F.translate_sub
#ortho_audit P01F.translate_sub
#print axioms P01F.translate_sub
#eval IO.println "AUDIT_END P01F.translate_sub"
#eval IO.println "AUDIT_BEGIN P01F.translate_type_substitution"
#check P01F.translate_type_substitution
#ortho_audit P01F.translate_type_substitution
#print axioms P01F.translate_type_substitution
#eval IO.println "AUDIT_END P01F.translate_type_substitution"
#eval IO.println "AUDIT_BEGIN P01F.positive_left"
#check P01F.positive_left
#ortho_audit P01F.positive_left
#print axioms P01F.positive_left
#eval IO.println "AUDIT_END P01F.positive_left"
#eval IO.println "AUDIT_BEGIN P01F.positive_right"
#check P01F.positive_right
#ortho_audit P01F.positive_right
#print axioms P01F.positive_right
#eval IO.println "AUDIT_END P01F.positive_right"
#eval IO.println "AUDIT_BEGIN P01F.positive_to_star"
#check P01F.positive_to_star
#ortho_audit P01F.positive_to_star
#print axioms P01F.positive_to_star
#eval IO.println "AUDIT_END P01F.positive_to_star"
#eval IO.println "AUDIT_BEGIN P01F.step_simulation"
#check P01F.step_simulation
#ortho_audit P01F.step_simulation
#print axioms P01F.step_simulation
#eval IO.println "AUDIT_END P01F.step_simulation"
#eval IO.println "AUDIT_BEGIN P01F.reduction_simulation"
#check P01F.reduction_simulation
#ortho_audit P01F.reduction_simulation
#print axioms P01F.reduction_simulation
#eval IO.println "AUDIT_END P01F.reduction_simulation"
#eval IO.println "AUDIT_BEGIN P01F.conversion_preservation"
#check P01F.conversion_preservation
#ortho_audit P01F.conversion_preservation
#print axioms P01F.conversion_preservation
#eval IO.println "AUDIT_END P01F.conversion_preservation"
#eval IO.println "AUDIT_BEGIN P01F.typing_preservation"
#check P01F.typing_preservation
#ortho_audit P01F.typing_preservation
#print axioms P01F.typing_preservation
#eval IO.println "AUDIT_END P01F.typing_preservation"
#eval IO.println "AUDIT_BEGIN P01F.target_SN_implies_source_SN"
#check P01F.target_SN_implies_source_SN
#ortho_audit P01F.target_SN_implies_source_SN
#print axioms P01F.target_SN_implies_source_SN
#eval IO.println "AUDIT_END P01F.target_SN_implies_source_SN"
#eval IO.println "AUDIT_BEGIN P01F.chain_simulation"
#check P01F.chain_simulation
#ortho_audit P01F.chain_simulation
#print axioms P01F.chain_simulation
#eval IO.println "AUDIT_END P01F.chain_simulation"
#eval IO.println "AUDIT_BEGIN P01F.SN_no_chain"
#check P01F.SN_no_chain
#ortho_audit P01F.SN_no_chain
#print axioms P01F.SN_no_chain
#eval IO.println "AUDIT_END P01F.SN_no_chain"
#eval IO.println "AUDIT_BEGIN P01F.Ty"
#check P01F.Ty
#ortho_audit P01F.Ty
#print axioms P01F.Ty
#eval IO.println "AUDIT_END P01F.Ty"
#eval IO.println "AUDIT_BEGIN P01F.cons"
#check P01F.cons
#ortho_audit P01F.cons
#print axioms P01F.cons
#eval IO.println "AUDIT_END P01F.cons"
#eval IO.println "AUDIT_BEGIN P01F.ty_rename_id"
#check P01F.ty_rename_id
#ortho_audit P01F.ty_rename_id
#print axioms P01F.ty_rename_id
#eval IO.println "AUDIT_END P01F.ty_rename_id"
#eval IO.println "AUDIT_BEGIN P01F.ty_rename_comp"
#check P01F.ty_rename_comp
#ortho_audit P01F.ty_rename_comp
#print axioms P01F.ty_rename_comp
#eval IO.println "AUDIT_END P01F.ty_rename_comp"
#eval IO.println "AUDIT_BEGIN P01F.ty_sub_id"
#check P01F.ty_sub_id
#ortho_audit P01F.ty_sub_id
#print axioms P01F.ty_sub_id
#eval IO.println "AUDIT_END P01F.ty_sub_id"
#eval IO.println "AUDIT_BEGIN P01F.ty_sub_rename"
#check P01F.ty_sub_rename
#ortho_audit P01F.ty_sub_rename
#print axioms P01F.ty_sub_rename
#eval IO.println "AUDIT_END P01F.ty_sub_rename"
#eval IO.println "AUDIT_BEGIN P01F.ty_rename_sub"
#check P01F.ty_rename_sub
#ortho_audit P01F.ty_rename_sub
#print axioms P01F.ty_rename_sub
#eval IO.println "AUDIT_END P01F.ty_rename_sub"
#eval IO.println "AUDIT_BEGIN P01F.ty_sub_comp"
#check P01F.ty_sub_comp
#ortho_audit P01F.ty_sub_comp
#print axioms P01F.ty_sub_comp
#eval IO.println "AUDIT_END P01F.ty_sub_comp"
#eval IO.println "AUDIT_BEGIN P01F.ty_sub_up_shift"
#check P01F.ty_sub_up_shift
#ortho_audit P01F.ty_sub_up_shift
#print axioms P01F.ty_sub_up_shift
#eval IO.println "AUDIT_END P01F.ty_sub_up_shift"
#eval IO.println "AUDIT_BEGIN P01F.ty_inst_shift"
#check P01F.ty_inst_shift
#ortho_audit P01F.ty_inst_shift
#print axioms P01F.ty_inst_shift
#eval IO.println "AUDIT_END P01F.ty_inst_shift"
#eval IO.println "AUDIT_BEGIN P01F.ty_sub_inst"
#check P01F.ty_sub_inst
#ortho_audit P01F.ty_sub_inst
#print axioms P01F.ty_sub_inst
#eval IO.println "AUDIT_END P01F.ty_sub_inst"
#eval IO.println "AUDIT_BEGIN P01F.ty_sub_vars"
#check P01F.ty_sub_vars
#ortho_audit P01F.ty_sub_vars
#print axioms P01F.ty_sub_vars
#eval IO.println "AUDIT_END P01F.ty_sub_vars"
#eval IO.println "AUDIT_BEGIN P01TypeAssertions.bridge_subject_reduction"
#check P01TypeAssertions.bridge_subject_reduction
#ortho_audit P01TypeAssertions.bridge_subject_reduction
#print axioms P01TypeAssertions.bridge_subject_reduction
#eval IO.println "AUDIT_END P01TypeAssertions.bridge_subject_reduction"
#eval IO.println "AUDIT_BEGIN P01TypeAssertions.bridge_typing"
#check P01TypeAssertions.bridge_typing
#ortho_audit P01TypeAssertions.bridge_typing
#print axioms P01TypeAssertions.bridge_typing
#eval IO.println "AUDIT_END P01TypeAssertions.bridge_typing"
#eval IO.println "AUDIT_BEGIN P01TypeAssertions.bridge_nonempty"
#check P01TypeAssertions.bridge_nonempty
#ortho_audit P01TypeAssertions.bridge_nonempty
#print axioms P01TypeAssertions.bridge_nonempty
#eval IO.println "AUDIT_END P01TypeAssertions.bridge_nonempty"
#eval IO.println "AUDIT_BEGIN P01TypeAssertions.direct_normalisation"
#check P01TypeAssertions.direct_normalisation
#ortho_audit P01TypeAssertions.direct_normalisation
#print axioms P01TypeAssertions.direct_normalisation
#eval IO.println "AUDIT_END P01TypeAssertions.direct_normalisation"
#eval IO.println "AUDIT_BEGIN P01TypeAssertions.raw_source_confluence"
#check P01TypeAssertions.raw_source_confluence
#ortho_audit P01TypeAssertions.raw_source_confluence
#print axioms P01TypeAssertions.raw_source_confluence
#eval IO.println "AUDIT_END P01TypeAssertions.raw_source_confluence"
#eval IO.println "AUDIT_BEGIN P01TypeAssertions.typed_conversion"
#check P01TypeAssertions.typed_conversion
#ortho_audit P01TypeAssertions.typed_conversion
#print axioms P01TypeAssertions.typed_conversion
#eval IO.println "AUDIT_END P01TypeAssertions.typed_conversion"
#eval IO.println "AUDIT_BEGIN P01TypeAssertions.exact_nonrepresentability"
#check P01TypeAssertions.exact_nonrepresentability
#ortho_audit P01TypeAssertions.exact_nonrepresentability
#print axioms P01TypeAssertions.exact_nonrepresentability
#eval IO.println "AUDIT_END P01TypeAssertions.exact_nonrepresentability"
#eval IO.println "AUDIT_BEGIN P01TypeAssertions.no_target_reflection"
#check P01TypeAssertions.no_target_reflection
#ortho_audit P01TypeAssertions.no_target_reflection
#print axioms P01TypeAssertions.no_target_reflection
#eval IO.println "AUDIT_END P01TypeAssertions.no_target_reflection"
#eval IO.println "AUDIT_BEGIN P01TypeAssertions.code_bound_intrinsic_soundness"
#check P01TypeAssertions.code_bound_intrinsic_soundness
#ortho_audit P01TypeAssertions.code_bound_intrinsic_soundness
#print axioms P01TypeAssertions.code_bound_intrinsic_soundness
#eval IO.println "AUDIT_END P01TypeAssertions.code_bound_intrinsic_soundness"
#eval IO.println "AUDIT_BEGIN P01TypeAssertions.all_new_identity_extension"
#check P01TypeAssertions.all_new_identity_extension
#ortho_audit P01TypeAssertions.all_new_identity_extension
#print axioms P01TypeAssertions.all_new_identity_extension
#eval IO.println "AUDIT_END P01TypeAssertions.all_new_identity_extension"
#eval IO.println "AUDIT_BEGIN P01TypeAssertions.j_two_coordinate_transport"
#check P01TypeAssertions.j_two_coordinate_transport
#ortho_audit P01TypeAssertions.j_two_coordinate_transport
#print axioms P01TypeAssertions.j_two_coordinate_transport
#eval IO.println "AUDIT_END P01TypeAssertions.j_two_coordinate_transport"
#eval IO.println "AUDIT_BEGIN P01D.Realiser"
#check P01D.Realiser
#ortho_audit P01D.Realiser
#print axioms P01D.Realiser
#eval IO.println "AUDIT_END P01D.Realiser"
#eval IO.println "AUDIT_BEGIN P01D.internal_all_self_instance"
#check P01D.internal_all_self_instance
#ortho_audit P01D.internal_all_self_instance
#print axioms P01D.internal_all_self_instance
#eval IO.println "AUDIT_END P01D.internal_all_self_instance"
#eval IO.println "AUDIT_BEGIN P01D.no_same_level_Girard_retraction"
#check P01D.no_same_level_Girard_retraction
#ortho_audit P01D.no_same_level_Girard_retraction
#print axioms P01D.no_same_level_Girard_retraction
#eval IO.println "AUDIT_END P01D.no_same_level_Girard_retraction"
