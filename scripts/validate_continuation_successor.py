"""Sixth-final admission constraints layered on the existing v5 registry.

This checks source/evidence associations and scope declarations. It does not
decide mathematical truth, philosophical warrant or external peer review.
"""
import hashlib
import json
import re
import validate_research_continuations as v

NEW_RESULT_IDS = tuple(f'S6F-{n:02}' for n in range(1,27))
REPORT_IDS = (tuple(f'C{n:02}' for n in range(1,6))
              + tuple(f'F{n:02}' for n in range(1,42))
              + tuple(f'T{n:02}' for n in range(1,25))
              + tuple(f'support-{n:03}' for n in range(70,113)))
INPUT_NAMES = ('Orthemology_v5_Sixth_Research_Tranche_20261002.docx',
               'Orthemology_v5_Sixth_Foundations_Evidence_20261002.zip',
               *(f'technicalpart{n}.zip' for n in range(1,6)),
               'Orthemology_v5_Sixth_Completion_Supplement_20261002.zip')

# These are the accepted interface bounds for this particular successor, not
# universal assertions about future research. Changing them needs a new scoped
# source/review admission, rather than editing a verdict to PASS.
CLAIM_CONTRACTS = {
    'foundations':{
        'track_t':'UNCHANGED', 'r5':'UNDEFEATED_AT_DECLARED_SCOPE',
        'world_existence_coverage_unity_necessity':'SUBSTANTIVE_PREMISES',
        'necessary_being':'NOT_DERIVED', 'attribute_ascent':'PREMISE_DEPENDENT',
        'categorical_norm_authority':'NOT_ESTABLISHED',
        'school_neutral_and_athari_roles':'DISTINCT', 'seventh':'PROSPECTIVE'},
    'repair':{
        'fault_model':'STATIC_SHARED_REPORT_AND_ACTION_ROOT_BUDGET',
        'diagnosis_identifies_actuator_integrity':False,
        'copies_are_independent_roots':False, 'target':'WHOLE_RULE',
        'fail_silent':'ADEQUATE_REPAIR_OR_HARMLESS_IDENTITY',
        'future_repair_safety_required':True, 'shared_gate_in_fault_support':True},
    'disclosure':{
        'private_general':'ORDINARY_REVIEWED_WITH_EXTERNAL_PARTITION_KNESER',
        'formal_scope':'ZERO_ERROR_SUBSET', 'shared_nonzero_range':'1<=M<=b',
        'private_positive_range':'1<=M<=b', 'zero_boundary':'M>=b+1_OR_b=0',
        'sender':'TRUTHFUL_INFORMED_CONTEXT_BOUND',
        'timing_games':'FOUR_SEPARATELY_OPTIMIZED_GAMES',
        'compulsory_action':'MATHEMATICAL_PREMISE_ONLY',
        'value_complexity':'O(u)_ARITHMETIC_EVALUATIONS',
        'partition_complexity':'O(M*u^2)_ARITHMETIC_OPERATIONS'},
    'cost':{
        'model_family':'FIXED_FINITE_ADMITTED', 'policy':'ONE_UNIT_SEED_POLICY_BEFORE_TRUE_MODEL',
        'cost':'ACTUAL_LOGICAL_BAD_ACTION_COUNT_INCLUDING_ACTION_ZERO',
        'objective':'COBUCHI_WITH_INITIAL_WINNING_PREMISE',
        'separation':'ALL_MODELS_IN_INITIAL_FAMILY',
        'exponential_range':'POSITIVE_OPEN_RANGE', 'ae_finite_clause':True,
        'law_transport':'FULL_MEASURABLE_COST_INTEGRAND',
        'common_bound':'FINITE_FOR_EACH_PARAMETER',
        'tolerance_wrapper':'EXISTS_BEFORE_TRUE_MODEL',
        'old_tail_lemma':'CONDITIONAL_WITH_ACTUAL_INSTANTIATION_LINK',
        'arbitrary_policy_or_physical_time_claim':False},
    'runtime':{
        'candidate':'v8', 'models':2, 'observed_states':2, 'actions':2,
        'history_and_counters':'UNBOUNDED', 'supplied_selector_equalities':36,
        'rational_denominators':'POSITIVE', 'environment':'FIXED_ONE_THIRD_TWO_THIRDS',
        'initial_state':False, 'decoder_inputs':'COMMON_POLICY_AND_OUTPUT_ONLY',
        'canonical_history_law':'DERIVED', 'selector_extraction':'NOT_SUPPLIED',
        'fully_certified_concrete_fixture':'NOT_SUPPLIED',
        'computed_tolerance_preserves_arbitrary_old_actions':False,
        'raw_output_parity_or_defect_preserved':False, 'physical_time_bound':False}
}


def record_digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()


def check_subject_digest(row):
    """Bind the reviewed subject/association separately from its execution result."""
    return record_digest({key:row[key] for key in (
        'id','kind','source_hashes','driver_hashes','scope','result_ids',
        'kernel_receipts','execution','execution_driver_sha256')})


def validate_outcome(row):
    v.keys(row,{'id','status','exit_code','diagnostic_sha256'},
           {'source_sha256','derivation_sha256'})
    v.nonempty(row['id']);v.digest(row['diagnostic_sha256'])
    for field in ['source_sha256','derivation_sha256']:
        if field in row:v.digest(row[field])
    v.enum(row['status'],{'PASS','REJECTED_CONCRETE','INCONCLUSIVE'})
    if row['status']=='PASS':
        v.require(type(row['exit_code']) is int and row['exit_code']==0,'Nonterminal positive control')
    elif row['status']=='REJECTED_CONCRETE':
        v.require(type(row['exit_code']) is int and row['exit_code']==1,
                  'Concrete Lean rejection requires exit 1; timeout/kill is inconclusive')
    else:
        v.require(row['exit_code'] is None or type(row['exit_code']) is int,'Invalid inconclusive exit')


def validate_overlay(overlay,results,statuses,sources,root):
    v.keys(overlay,{'schema','predecessor','inputs','report_bindings','prior_results','new_results',
                    'claim_contracts','current_selections','checks','check_bindings','result_checks','research_avenues'})
    v.require(overlay['schema']=='orthemology-v5-sixth-final-overlay-v1','Unknown successor overlay')
    p=overlay['predecessor'];v.keys(p,{'commit','tree','registry_sha256','verification_sha256'})
    for key in ['commit','tree']:
        v.require(isinstance(p[key],str) and re.fullmatch('[0-9a-f]{40}',p[key]),'Invalid predecessor Git identity')
    for key in ['registry_sha256','verification_sha256']:v.digest(p[key])
    inputs=v.indexed(overlay['inputs'],'name')
    v.require(set(inputs)==set(INPUT_NAMES),'Missing or unexpected sixth-final input')
    for row in inputs.values():
        v.keys(row,{'name','sha256','bytes'});v.safe_relative(row['name']);v.digest(row['sha256'])
        v.require(type(row['bytes']) is int and row['bytes']>0,'Invalid input size')
    reports=v.indexed(overlay['report_bindings'],'id')
    v.require(set(reports)==set(REPORT_IDS),'Missing or unexpected report/support binding')
    for name,row in reports.items():
        v.keys(row,{'id','source_id','sha256','role'})
        v.require(row['source_id'] in sources,'Unknown report source')
        v.require(row['sha256']==sources[row['source_id']]['original_sha256'],'Report original identity mismatch')
        v.require(row['role']==('SUPPORT' if name.startswith('support-') else 'REPORT'),'Wrong report binding role')
    new=overlay['new_results']
    v.require(isinstance(new,list) and len(new)==len(set(new)) and set(new)==set(NEW_RESULT_IDS),'Wrong successor result census')
    prior=v.indexed(overlay['prior_results'],'id')
    v.require(set(prior).isdisjoint(new) and set(results)==set(prior)|set(new),'Lost or unexpected predecessor result')
    for name,row in prior.items():
        v.keys(row,{'id','statement_sha256','status_sha256','successors'})
        v.require(row['statement_sha256']==v.statement_digest(results[name]),'Rewritten predecessor statement')
        v.require(row['status_sha256']==record_digest(statuses[name]),'Rewritten predecessor evidence')
        v.require(isinstance(row['successors'],list) and len(row['successors'])==len(set(row['successors']))
                  and set(row['successors'])<=set(new),'Unknown or duplicate scoped successor')
    contracts=v.indexed(overlay['claim_contracts'],'id')
    v.require(set(contracts)==set(CLAIM_CONTRACTS),'Missing scoped claim contract')
    def reviews(ids):
        v.require(isinstance(ids,list) and bool(ids) and len(ids)==len(set(ids))
                  and all(x in sources for x in ids),'Missing source-bound scope review')
    for name,row in contracts.items():
        v.keys(row,{'id','contract','review_source_ids'});reviews(row['review_source_ids'])
        v.require(record_digest(row['contract'])==record_digest(CLAIM_CONTRACTS[name]),'Unsupported claim promotion: '+name)
    seen=set()
    for row in overlay['current_selections']:
        v.keys(row,{'prior_result','successor','scope','relation','review_source_ids'})
        v.require(row['prior_result'] in prior and row['successor'] in prior[row['prior_result']]['successors'],
                  'Unbound scoped current selection')
        v.enum(row['relation'],{'SCOPED_SUCCESSOR','CONTEXTUAL_CLARIFICATION'})
        v.nonempty(row['scope']);v.check_public_text(row['scope']);reviews(row['review_source_ids'])
        ident=(row['prior_result'],row['successor'])
        v.require(ident not in seen,'Duplicate scoped current selection');seen.add(ident)
    v.require(seen=={(name,sid) for name,row in prior.items() for sid in row['successors']},'Missing scoped current selection')
    checks=v.indexed(overlay['checks'],'id')
    bindings=v.indexed(overlay['check_bindings'],'id')
    v.require(set(bindings)==set(checks),'Missing or unassociated control binding')
    for row in checks.values():
        v.keys(row,{'id','kind','source_ids','source_hashes','driver_source_ids','driver_hashes',
                    'command_sha256','receipt_sha256','log_sha256','terminal','exit_code','status','scope','outcomes',
                    'result_ids','kernel_receipts','execution','execution_driver_sha256'})
        binding=bindings[row['id']];v.keys(binding,{'id','subject_sha256','outcomes_sha256'})
        v.require(binding['subject_sha256']==check_subject_digest(row),'Changed control subject or association')
        # This separate reviewed inventory binds every diagnostic/source identity
        # and classification, including retained retries. Exit 1 alone cannot
        # distinguish a semantic rejection from Lean heartbeat exhaustion.
        v.require(binding['outcomes_sha256']==record_digest(row['outcomes']),
                  'Changed reviewed outcome inventory or classification')
        v.require(isinstance(row['result_ids'],list) and bool(row['result_ids'])
                  and len(row['result_ids'])==len(set(row['result_ids']))
                  and set(row['result_ids'])<=set(new),'Invalid control result association')
        v.enum(row['execution'],{'PUBLIC_EXACT_FINITE_DRIVER','ORIGINAL_RUNTIME_DRIVER',
                                'SUPPLIED_CONTROLS_ON_FRESH_CLOSURE'})
        v.digest(row['execution_driver_sha256'])
        v.enum(row['kind'],{'FINITE_CONTROL','KERNEL_PROBE','SOURCE_MUTATION','RUNTIME_NATIVE'})
        if row['kind']=='SOURCE_MUTATION':
            v.require(bool(row['outcomes']),'Missing semantic outcome inventory')
        v.require(isinstance(row['kernel_receipts'],dict),'Invalid kernel dependency binding')
        if row['kind']!='FINITE_CONTROL':
            v.require(bool(row['kernel_receipts']),'Missing fresh kernel dependency')
        accepted={p for rid in row['result_ids'] for p in statuses[rid]['receipts']}
        for path,h in row['kernel_receipts'].items():
            v.require(path in accepted,'Kernel dependency belongs to an unrelated result')
            v.require(v.sha(v.path_in(root,path))==h,'Changed kernel dependency receipt')
        v.enum(row['status'],{'PASS','PASS_WITH_INCONCLUSIVE_CONTROL'})
        v.require(row['terminal']=='EXIT' and type(row['exit_code']) is int and row['exit_code']==0,
                  'Check has no successful terminal exit')
        for field in ['source_ids','driver_source_ids']:reviews(row[field])
        v.require(set(row['driver_source_ids'])<=set(row['source_ids']),'Driver is outside checked source closure')
        for names,hashes in [('source_ids','source_hashes'),('driver_source_ids','driver_hashes')]:
            v.require(row[hashes]=={sid:sources[sid]['original_sha256'] for sid in row[names]},'Check source identity mismatch')
        for field in ['command_sha256','receipt_sha256','log_sha256']:v.digest(row[field])
        v.nonempty(row['scope']);v.check_public_text(row['scope'])
        for outcome in v.indexed(row['outcomes'],'id').values():validate_outcome(outcome)
        inconclusive=any(o['status']=='INCONCLUSIVE' for o in row['outcomes'])
        v.require((row['status']=='PASS_WITH_INCONCLUSIVE_CONTROL')==inconclusive,'Inconclusive control misrepresented')
    bound=v.indexed(overlay['result_checks'],'id')
    v.require(set(bound)==set(new),'Missing successor check association')
    used=set()
    for name,row in bound.items():
        v.keys(row,{'id','check_ids'})
        v.require(isinstance(row['check_ids'],list) and len(row['check_ids'])==len(set(row['check_ids']))
                  and set(row['check_ids'])<=set(checks),'Unknown/duplicate native check association')
        v.require(set(row['check_ids'])=={cid for cid,c in checks.items() if name in c['result_ids']},
                  'Control evidence assigned to an unrelated result')
        used.update(row['check_ids'])
    v.require(used==set(checks),'Unassociated check evidence')
    avenues={}
    for row in overlay['research_avenues']:
        v.keys(row,{'id','result_ids','disposition','residual'})
        v.require(type(row['id']) is int and row['id'] not in avenues,'Invalid or duplicate research avenue')
        avenues[row['id']]=row
        v.enum(row['disposition'],{'PRESERVED_WITH_SCOPED_CONTINUATION','PRESERVED_NO_NEW_CLOSURE'})
        v.require(bool(row['result_ids']) and set(row['result_ids'])<=set(results),'Unknown avenue result')
        v.nonempty(row['residual']);v.check_public_text(row['residual'])
    v.require(set(avenues)==set(range(1,13)),'Lost avenue or unperformed Seventh research')
