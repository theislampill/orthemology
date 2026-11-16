#!/usr/bin/env python3
"""Current decision authority, independent of retired topology reconstruction."""
import ast
import json
import contextlib
import copy
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import unittest

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load_validator():
    spec = importlib.util.spec_from_file_location(
        'candidate_authority_probe', ROOT / 'scripts/validate_candidate_state.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture():
    return {'decisions': {
        '0001': {'status': 'adopted-merged', 'title': 'Existing adopted decision'},
        '0020': {'status': 'proposed-candidate', 'pr': 8, 'title': 'Observed candidate'},
        '0041': {'status': 'proposed-candidate', 'stage': 'local-preparation',
                 'title': 'Local preparation, not an invented pull request'},
    }}


class CandidateAuthorityTests(unittest.TestCase):
    def run_case(self, registry=None, source_changes=None):
        module = load_validator()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            decisions = root / 'docs/decisions'
            decisions.mkdir(parents=True)
            (root / 'docs/decision-status.yaml').write_text(
                yaml.safe_dump(fixture() if registry is None else registry))
            files = {'0001-adopted.md': '# Existing adopted decision\n',
                     '0020-observed.md': '# CANDIDATE decision\n',
                     '0041-local.md': '# CANDIDATE local preparation\n'}
            files.update(source_changes or {})
            for name, body in files.items():
                if body is not None:
                    (decisions / name).write_text(body)
            module.ROOT = str(root)
            module.FAILS.clear()
            output = io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                try:
                    code = module.main()
                except Exception as exc:
                    code = 99
                    output.write('UNHANDLED: '+repr(exc))
            self.assertNotIn('UNHANDLED:', output.getvalue(), output.getvalue())
            return code, output.getvalue()

    def assert_rejected(self, registry=None, changes=None, fragment=None):
        code, out = self.run_case(registry, changes)
        self.assertEqual(1, code, out)
        if fragment:
            self.assertIn(fragment, out)

    def test_current_positive_requires_no_history_or_topology(self):
        code, out = self.run_case()
        self.assertEqual(0, code, out)

    def test_candidate_promotion_is_rejected(self):
        for decision in ('0020', '0041'):
            with self.subTest(decision=decision):
                data = fixture();data['decisions'][decision]['status'] = 'adopted-merged'
                self.assert_rejected(data)

    def test_removing_pr_and_promoting_cannot_evade_boundary(self):
        data=fixture();data['decisions']['0020'].pop('pr')
        data['decisions']['0020']['status']='adopted-merged'
        self.assert_rejected(data)

    def test_historical_candidate_pr_is_not_invented_or_dropped(self):
        data=fixture();data['decisions']['0020'].pop('pr')
        self.assert_rejected(data)

    def test_local_candidate_requires_explicit_preparation(self):
        data=fixture();data['decisions']['0041'].pop('stage')
        self.assert_rejected(data)

    def test_previous_decision_without_candidate_origin_is_rejected(self):
        data=fixture();data['decisions']['0001']['status']='proposed-candidate'
        self.assert_rejected(data)

    def test_candidate_source_label_is_required(self):
        self.assert_rejected(changes={'0020-observed.md':'# A decision\n'})

    def test_missing_candidate_source_is_rejected(self):
        self.assert_rejected(changes={'0041-local.md':None})

    def test_ambiguous_candidate_source_is_rejected(self):
        self.assert_rejected(changes={'0041-other.md':'# CANDIDATE ambiguous source\n'})

    def test_malformed_registry_is_rejected_without_traceback(self):
        for data in ({}, {'decisions': []}, {'decisions': {}}, {'decisions': {'bad':{}}},
                     {'decisions': {'0041':None}}, {'decisions': {'0041': {'status': []}}}):
            with self.subTest(data=data):
                self.assert_rejected(data)

    def test_unknown_status_is_rejected(self):
        data=fixture();data['decisions']['0001']['status']='verified-by-implementation'
        self.assert_rejected(data)

    def test_guard_is_live_after_repair(self):
        data=fixture();data['decisions']['0041']['status']='adopted-merged'
        self.assert_rejected(data)
        data['decisions']['0041']['status']='proposed-candidate'
        self.assertEqual(0,self.run_case(data)[0])


def source_tree(relative):
    return ast.parse((ROOT / relative).read_text(encoding='utf-8'))


def production_history_guard():
    tree = source_tree('scripts/validate_review_state.py')
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef)
             and node.name == 'candidate_history_issues']
    if len(nodes) != 1:
        raise AssertionError('existing review owner must expose the transferred history guard')
    namespace = {}
    exec(compile(ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[])),
                 '<actual review-owner history predicate>', 'exec'), namespace)
    return namespace['candidate_history_issues']


def historical_predicate(kind, data, row=None, pr=8):
    """Execute selected actual owner statements, never import the old generator."""
    tree = source_tree('scripts/generate_candidate_state.py')
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                    and n.name == 'collect_issues')
    namespace = {'data': data, 'row': row, 'pr': pr, 'issues': []}
    for name in ('REQUIRED_REVIEW_PROVENANCE', 'EXPECTED_PROVENANCE'):
        node = next(n for n in tree.body if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))
        namespace[name] = ast.literal_eval(node.value)
    if kind == 'review':
        nodes = [n for n in function.body if isinstance(n, ast.If)
                 and 'data.get(\'review_provenance\')' in ast.unparse(n.test)]
    elif kind == 'implementation':
        loop = next(n for n in function.body if isinstance(n, ast.For)
                    and ast.unparse(n.target) == '(pr, row)')
        start = next(i for i,n in enumerate(loop.body) if isinstance(n, ast.Assign)
                     and any(isinstance(t,ast.Name) and t.id=='provenance' for t in n.targets))
        nodes = loop.body[start:start+2]
    elif kind == 'terminal':
        start = next(i for i,n in enumerate(function.body) if isinstance(n, ast.Assign)
                     and any(isinstance(t,ast.Name) and t.id=='claims' for t in n.targets))
        nodes = function.body[start:-1]
    else:
        raise AssertionError('unknown predicate')
    if not nodes:
        raise AssertionError('actual owner predicate was not selected')
    exec(compile(ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[])),
                 '<actual historical authority statements>', 'exec'), namespace)
    return namespace['issues'], namespace


class CandidateHistoryGuardTests(unittest.TestCase):
    def test_history_guard_accepts_existing_historical_shapes(self):
        rows = [{'prefix': 'docs/project-closure/r7c/', 'status': 'historical'}]
        for history in (rows, {'rules': rows}, {'entries': rows}):
            with self.subTest(history=history):
                self.assertEqual([], production_history_guard()(history))

    def test_history_guard_rejects_all_candidate_prefix_terminal_statuses(self):
        for prefix in ('r7', 'r7c/', 'r7-new-suffix/', 'r70/'):
            for status in ('merged', 'adopted', 'adopted-merged'):
                with self.subTest(prefix=prefix, status=status):
                    rows = [{'prefix':'docs/project-closure/'+prefix, 'status':status}]
                    self.assertTrue(production_history_guard()({'rules':rows}))

    def test_history_guard_does_not_promote_non_candidate_history(self):
        for status in ('merged', 'adopted', 'adopted-merged'):
            with self.subTest(status=status):
                self.assertEqual([], production_history_guard()(
                    {'rules':[{'prefix':'docs/project-closure/r6/', 'status':status}]}))

    def test_history_helper_refuses_malformed_shapes(self):
        for history in (None, 'history', {'rules':None}, {'entries':'bad'}, [None]):
            with self.subTest(history=history):
                self.assertTrue(production_history_guard()(history))

    def test_existing_review_main_calls_guard_at_its_existing_index_read(self):
        tree = source_tree('scripts/validate_review_state.py')
        main = next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
        index = next(i for i,n in enumerate(main.body) if isinstance(n,ast.Assign)
                     and any(isinstance(t,ast.Name) and t.id=='idx' for t in n.targets))
        following = main.body[index+1:index+3]
        self.assertEqual(2,len(following))
        self.assertIn('candidate_history_issues(idx)', ast.unparse(following[0]))
        self.assertEqual("check('no R7 candidate closure artifact is marked merged/adopted', not history_issues, '; '.join(history_issues))",
                         ast.unparse(following[1]))


# Attach only the additional witness to the existing current-input class.
def test_existing_early_id_local_preparation_loophole_is_not_newly_fixed(self):
    data=fixture()
    data['decisions']['0001'].update(status='proposed-candidate', stage='local-preparation')
    code,out=self.run_case(data, {'0001-adopted.md':'# CANDIDATE existing policy limitation\n'})
    self.assertEqual(0,code,out)
CandidateAuthorityTests.test_existing_early_id_local_preparation_loophole_is_not_newly_fixed = test_existing_early_id_local_preparation_loophole_is_not_newly_fixed


class ExistingHistoricalAuthorityPredicateTests(unittest.TestCase):
    def test_review_is_not_implementation_attestation(self):
        _,scope=historical_predicate('review', {})
        valid=copy.deepcopy(scope['REQUIRED_REVIEW_PROVENANCE'])
        self.assertEqual([],historical_predicate('review', {'review_provenance':valid})[0])
        for bad in (None, {'layer':'implementation','model':valid['model'], 'statement':valid['statement']},
                    scope['EXPECTED_PROVENANCE'][8]):
            with self.subTest(bad=bad):
                self.assertTrue(historical_predicate('review', {'review_provenance':bad})[0])

    def test_missing_or_fabricated_implementation_provenance_refuses(self):
        _,scope=historical_predicate('implementation', {}, row={})
        for pr,provenance in scope['EXPECTED_PROVENANCE'].items():
            with self.subTest(pr=pr):
                self.assertEqual([],historical_predicate('implementation', {}, {'provenance':provenance}, pr)[0])
                for bad in (None, {}, {'layer':'independent-review', 'model':provenance['model']},
                            {'layer':provenance['layer'], 'model':'invented-model'}):
                    self.assertTrue(historical_predicate('implementation', {}, {'provenance':bad}, pr)[0])

    def test_historical_candidate_terminal_claims_need_more_than_self_attestation(self):
        claims={'candidate_status':'proposed-candidate','merged':False,
                'independent_signoff':False,'ready_for_merge':False,
                'evidence':{'merged':[],'independent_signoff':[],'ready_for_merge':[]}}
        self.assertEqual([],historical_predicate('terminal', {'status_claims':claims})[0])
        for name in ('merged','independent_signoff','ready_for_merge'):
            for evidence in ([],['self-supplied-evidence']):
                with self.subTest(name=name,evidence=evidence):
                    changed=copy.deepcopy(claims);changed[name]=True;changed['evidence'][name]=evidence
                    issues=historical_predicate('terminal', {'status_claims':changed})[0]
                    self.assertIn('candidate topology cannot self-promote',issues)

    def test_actual_terminal_schema_refuses_malformed_claims_and_evidence(self):
        schema=json.loads((ROOT/'schemas/candidate-topology.schema.json').read_text())['$defs']['status_claims']
        validator=Draft202012Validator(schema)
        claims={'candidate_status':'proposed-candidate','merged':False,
                'independent_signoff':False,'ready_for_merge':False,
                'evidence':{'merged':[],'independent_signoff':[],'ready_for_merge':[]},
                'next_action':'Independent owner decision remains required'}
        self.assertEqual([],list(validator.iter_errors(claims)))
        wrong_evidence=copy.deepcopy(claims);wrong_evidence['evidence']='fabricated'
        wrong_boolean=copy.deepcopy(claims);wrong_boolean['merged']='false'
        for bad in ([], {}, wrong_evidence, wrong_boolean):
            with self.subTest(bad=bad):
                self.assertTrue(list(validator.iter_errors(bad)))


if __name__ == '__main__':
    unittest.main()
