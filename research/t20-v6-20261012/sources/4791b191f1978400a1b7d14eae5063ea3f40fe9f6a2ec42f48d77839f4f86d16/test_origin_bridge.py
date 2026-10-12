"""Modal interpretations of the SAME retained productive interpreter.
Numerical identity is explicit extra structure; no metaphysical possibility claim.
"""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, sys, unittest
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
sys.path.insert(0, str(BASE / 'provision-identity/src'))
from provision_semantics import IntendedAct, execute_intentions
from preservation_modes import preserve

@dataclass(frozen=True)
class OriginEvent:
    token: str
    original_roots: frozenset

@dataclass(frozen=True)
class NumericalEffect:
    token: str
    role: str
    origin: OriginEvent

O_AB = OriginEvent('the-same-initial-episode', frozenset({'A','B'}))
O_A = OriginEvent('alternative-initial-episode', frozenset({'A'}))
Q = NumericalEffect('q', 'e', O_AB)
Q_OTHER = NumericalEffect('q-prime', 'e', O_A)
A = IntendedAct('A', 'alpha', frozenset({'e'}))
B = IntendedAct('B', 'beta', frozenset({'e'}))


def endpoint(acts):
    events, supports, rules, exact = execute_intentions(acts)
    return {'events': events, 'supports': {k: sorted(v) for k,v in supports.items()},
            'exact_profile_intention': exact,
            'A_own_end': frozenset(k for k,state in events) == A.exact_created_target
                and all('A' in supports[e] for e in A.exact_created_target)}


def preserving_world(schedule):
    # The retained temporal interpreter is unchanged. An immutable historical
    # origin event and numerical bearer are added, shared between late branches.
    assert schedule[0] == (True, True)
    r = preserve(schedule)
    return {'roots_exist_each_stage': [{'A': True, 'B': True} for _ in schedule],
            'other_activity_unchanged': [('A-background', 'B-background') for _ in schedule],
            'origin_event': O_AB, 'numerical_bearer': Q,
            'scheduled_q_directed_exercises': [[(g, f'{g}-exercise-{t}', Q.token) for g,active in zip(('A','B'),phase) if active] for t,phase in enumerate(schedule)],
            'stage_facts': r['stage_facts'],
            'current_support': r['explanatory_proof_records'],
            'receives_intrinsic_resource': []}


def report():
    joint_acts, solo_acts = [A,B], [A]
    joint, solo = endpoint(joint_acts), endpoint(solo_acts)
    late_joint = preserving_world([(True,True)]*3)
    late_solo = preserving_world([(True,True),(True,True),(True,False)])
    stops = preserving_world([(True,True),(False,False),(True,False)])
    models = {
      'flexible_identity': {'actual_token':'q', 'birth_suppressed_token':'q',
          'exact_source_origin_essential':False, 'same_numerical_token':True},
      'origin_essential': {'actual_token':Q.token, 'birth_suppressed_token':Q_OTHER.token,
          'exact_source_origin_essential':True, 'same_numerical_token':Q == Q_OTHER,
          'same_qualitative_role':Q.role == Q_OTHER.role,
          'A_profile_end_survives':solo['A_own_end'],
          'A_rigid_q_end_survives':False},
      'counterpart': {'actual_token':Q.token, 'birth_suppressed_token':Q_OTHER.token,
          'counterpart_for_profile_comparison':Q.role == Q_OTHER.role,
          'strict_identity_claim':False,
          'actual_world_numerical_effect_count':1},
      'fixed_origin_later_suppression': {
          'roots_exist_unchanged': late_joint['roots_exist_each_stage'] == late_solo['roots_exist_each_stage'],
          'other_activity_unchanged': late_joint['other_activity_unchanged'] == late_solo['other_activity_unchanged'],
          'same_numerical_bearer':late_joint['numerical_bearer'] is late_solo['numerical_bearer'],
          'same_exact_origin_event':late_joint['origin_event'] is late_solo['origin_event'],
          'same_initial_support_record':late_joint['current_support'][0] == late_solo['current_support'][0],
          'same_entire_represented_prefix_before_probe':late_joint['current_support'][:2] == late_solo['current_support'][:2] and late_joint['scheduled_q_directed_exercises'][:2] == late_solo['scheduled_q_directed_exercises'][:2],
          'same_all_stage_existence_facts':late_joint['stage_facts'] == late_solo['stage_facts'],
          'later_support_changes':late_joint['current_support'][1:] != late_solo['current_support'][1:],
          'same_A_preserving_exercises': [[a for a in phase if a[0]=='A'] for phase in late_joint['scheduled_q_directed_exercises']] == [[a for a in phase if a[0]=='A'] for phase in late_solo['scheduled_q_directed_exercises']],
          'origin_essentiality_holds':True,
          'full_sustaining_history_essentiality_holds':False,
          'no_intrinsic_receipt':not late_solo['receives_intrinsic_resource'],
          'all_support_shutdown_breaks_persistence_without_resurrection': stops['stage_facts'] == [('e',0,'exists')],
          'under_added_necessary_concord':'Diagnostic schedule inadmissible; this is policy/modal exclusion, not numerical-identity failure.'}}
    paths=[BASE/'provision-identity/src/provision_semantics.py',BASE/'provision-identity/src/preservation_modes.py',BASE/'intrinsic-willing/src/joint_interpretation.py']
    return {'schema':'origin-identity-bridge/1','run_utc':datetime.now(timezone.utc).isoformat(),
      'source_bindings':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'role':'imported_unchanged' if p.name != 'joint_interpretation.py' else 'context_only_not_executed'} for p in paths],
      'same_operational_skeleton':{'joint':joint,'birth_suppressed':solo,
        'reuses_A_object':joint_acts[0] is solo_acts[0],'created_role_output_equal':joint['events']==solo['events'],
        'actual_support_changes':joint['supports']!=solo['supports']},
      'models':models,
      'limits':['Origin-essentiality is an additional interpretation, not inferred from numerical labels.',
        'Later-suppression fixture enriches the existing temporal interpreter with shared rigid origin and bearer; it does not establish metaphysical admissibility.',
        'Fixed background activity prevents global-inactivity and bearer-deletion readings; its independent goodness is not established.',
        'No classification of intrinsic power as perfect is derived from the finite model.',
        'Current solo preservation is not sole origination or exhaustive provision of the whole causal history.']}

class Checks(unittest.TestCase):
    def test_same_imported_operational_skeleton(self):
        r=report()['same_operational_skeleton']
        self.assertTrue(r['created_role_output_equal']);self.assertTrue(r['actual_support_changes'])
        self.assertTrue(r['joint']['A_own_end']);self.assertTrue(r['birth_suppressed']['A_own_end'])
    def test_qualitative_not_rigid_target(self):
        m=report()['models']['origin_essential']
        self.assertTrue(m['same_qualitative_role']);self.assertTrue(m['A_profile_end_survives'])
        self.assertFalse(m['same_numerical_token']);self.assertFalse(m['A_rigid_q_end_survives'])
    def test_shared_past_and_same_bearer(self):
        m=report()['models']['fixed_origin_later_suppression']
        for k in ['roots_exist_unchanged','other_activity_unchanged','same_numerical_bearer','same_exact_origin_event',
          'same_initial_support_record','same_entire_represented_prefix_before_probe','same_all_stage_existence_facts','later_support_changes',
          'same_A_preserving_exercises','origin_essentiality_holds','no_intrinsic_receipt',
          'all_support_shutdown_breaks_persistence_without_resurrection']:self.assertTrue(m[k], k)
        self.assertFalse(m['full_sustaining_history_essentiality_holds'])
    def test_counterpart_is_not_identity_or_actual_plurality(self):
        m=report()['models']['counterpart'];self.assertTrue(m['counterpart_for_profile_comparison'])
        self.assertFalse(m['strict_identity_claim']);self.assertEqual(m['actual_world_numerical_effect_count'],1)
    def test_readonly_bindings(self):
        self.assertEqual(len(report()['source_bindings']),3)

if __name__=='__main__':
    (HERE.parent/'results/MODELS.json').write_text(json.dumps(report(),indent=2)+'\n')
    unittest.main(verbosity=2)
