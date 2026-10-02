"""Adversarial source, import-universe and evidence-boundary controls."""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import sys

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/validate_research_continuations.py'
AREA = 'experiments/orthemology-v5-continuations'
PROV = 'docs/provenance/v5-research-continuations'
ORIGIN = 'a' * 64


def put(root, name, value):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def fixture(root):
    raw = b'namespace Demo\ntheorem ok : True := True.intro\nend Demo\n'
    digest = hashlib.sha256(raw).hexdigest()
    path = AREA + '/source-store/' + digest + '.lean'
    (root/path).parent.mkdir(parents=True)
    (root/path).write_bytes(raw)
    source = {'id':'source-a', 'origin':ORIGIN, 'member':'src/Proof.lean',
              'original_sha256':digest, 'original_bytes':len(raw), 'path':path,
              'sha256':digest, 'bytes':len(raw), 'projection':'EXACT', 'derivation':None}
    pins = {'lean_version':'4.19.0', 'lean_binary_sha256':'92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023',
            'packages':[{'name':'mathlib', 'revision':'c44e0c8ee63ca166450922a373c7409c5d26b00b'}]}
    suite = {'id':'fixture-a', 'origin':ORIGIN, 'descriptor_source_id':'source-a',
             'modules':[{'module':'Proof','source_id':'source-a','imports':[]}],
             'module_order':['Proof'], 'targets':[{'name':'Demo.ok','module':'Proof'}],
             'pins':pins, 'official_imports':[], 'driver':{'source_id':'source-a','lean_argument':'EXECUTABLE'},
             'controls':'ORIGINAL_DRIVER_REQUIRED', 'classification':'CURRENT_EVIDENCE'}
    registry = {'schema':'orthemology-v5-continuations-v1', 'programme':'Orthemology v5',
                'cutoff':'sixth-tranche-checkpoint-3', 'source_map':PROV+'/SOURCE_MAP.json',
                'result_status':PROV+'/RESULT_STATUS.json', 'supersession':PROV+'/SUPERSESSION.json',
                'obligations':PROV+'/OBLIGATION_CROSSWALK.json', 'lineages':PROV+'/PACKET_LINEAGES.json',
                'evidence_bindings':PROV+'/EVIDENCE_BINDINGS.json',
                'suites':[AREA+'/suites/fixture-a.json'],
                'results':[{'id':'T5-EXAMPLE','origin':ORIGIN,'title':'Scoped example',
                            'claim':'True in the declared model.', 'limit':'No implementation claim.',
                            'source_ids':['source-a'], 'review_source_ids':['source-a'],
                            'suite_ids':['fixture-a'],'math_form':'FORMAL','implementation':'MATHEMATICAL_POLICY'}]}
    statuses = {'results':[{'id':'T5-EXAMPLE','custody':'EXACT','inherited':'RETAINED_FORMAL_REVIEW',
                            'fresh':'NOT_RUN','adoption':'CANDIDATE','receipts':[],
                            'external_warrant':{'empirical':'NOT_ESTABLISHED','normative':'NOT_ESTABLISHED',
                                                'external_peer_review':'NOT_ESTABLISHED','novelty':'NOT_ESTABLISHED'}}]}
    data = {AREA+'/registry.json':registry, PROV+'/SOURCE_MAP.json':{'sources':[source]},
            PROV+'/RESULT_STATUS.json':statuses, AREA+'/suites/fixture-a.json':suite,
            PROV+'/SUPERSESSION.json':{'edges':[]}, PROV+'/OBLIGATION_CROSSWALK.json':{'obligations':[]},
            PROV+'/PACKET_LINEAGES.json':{'archives':[{'sha256':ORIGIN,'bytes':100,'classification':'CURRENT_EVIDENCE',
                                                     'basis':'Exact source and review bound.', 'parents':[]}]}}
    row=registry['results'][0]
    statement={k:row[k] for k in ['id','origin','claim','limit','math_form','implementation']}
    identities={'source-a':{'original_sha256':digest,'public_sha256':digest}}
    data[PROV+'/EVIDENCE_BINDINGS.json']={'schema':'orthemology-v5-evidence-bindings-v1','control_contracts':[],
        'results':[{'id':row['id'],'statement_sha256':hashlib.sha256(json.dumps(statement,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),
                    'sources':identities,'reviews':identities,
                    'suite_targets':[{'suite_id':'fixture-a','targets':{'Demo.ok':'source-a'}}]}]}
    for name,value in data.items(): put(root,name,value)
    return data


class ContinuationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if SCRIPT.exists():
            spec=importlib.util.spec_from_file_location('continuations',SCRIPT)
            cls.v=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.v)

    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), 'Continuation validator is not implemented')
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.data=fixture(self.root)

    def save(self):
        for name,value in self.data.items():put(self.root,name,value)

    def reject(self):
        self.save()
        with self.assertRaises(ValueError):self.v.validate(self.root)

    def test_valid_source_is_integrity_only(self):
        summary=self.v.validate(self.root)
        self.assertEqual(summary['results'],1)
        self.assertEqual(summary['fresh_qualified_results'],0)

    def test_obligation_statement_must_belong_to_exact_owner(self):
        owner='original.md';(self.root/owner).write_text('Original obligation remains open.\n',encoding='utf-8')
        row={'id':'U08','owner_path':owner,'owner_sha256':self.v.sha(self.root/owner),'statement':'Original obligation remains open.',
             'result_ids':[],'disposition':'PRESERVED_OPEN','residual':'No general closure.'}
        self.data[PROV+'/OBLIGATION_CROSSWALK.json']['obligations']=[row];self.save();self.v.validate(self.root)
        row['statement']='A different finite theorem closes this obligation.';self.reject()

    def test_packet_member_selector_is_not_a_checkout_destination(self):
        sys.path.insert(0,str(SCRIPT.parent))
        import validate_internal_references as refs
        row=deepcopy(self.data[PROV+'/SOURCE_MAP.json']['sources'][0]);row['member']='scripts/'+'not-shipped.py'
        raw=json.dumps({'sources':[row]},indent=2)
        self.assertNotIn(row['member'],[p for p,_ in refs._citation_occurrences(PROV+'/SOURCE_MAP.json',raw)])
        row['path']=row['member'];raw=json.dumps({'sources':[row]},indent=2)
        self.assertIn(row['path'],[p for p,_ in refs._citation_occurrences(PROV+'/SOURCE_MAP.json',raw)])
        row['original_sha256']='invalid';row['path']=None;raw=json.dumps({'sources':[row]},indent=2)
        self.assertIn(row['member'],[p for p,_ in refs._citation_occurrences(PROV+'/SOURCE_MAP.json',raw)])

    def test_summarized_readback_and_fingerprint_are_bound(self):
        suite=self.data[AREA+'/suites/fixture-a.json'];source=self.data[PROV+'/SOURCE_MAP.json']['sources'][0]
        hashes={'Proof':source['sha256']}
        receipt={'status':'FRESH_KERNEL_COMPONENTS','exit_code':0,'kernel_verified':True,'suite_id':'fixture-a',
                 'suite_sha256':self.v.sha(self.root/(AREA+'/suites/fixture-a.json')),'source_hashes':hashes,'post_source_hashes':hashes,
                 'compiler_sha256':suite['pins']['lean_binary_sha256'],'pins':suite['pins'],
                 'modules':[{'module':'Proof','source_sha256':source['sha256'],'object_sha256':'d'*64,'status':'FRESH_COMPILE','exit_code':0,
                             'transitive_source_fingerprint':self.v.suite_fingerprints(suite,{'source-a':source})['Proof']}],
                 'readbacks':{'Demo.ok':{'type_sha256':hashlib.sha256(b'Demo.ok : True').hexdigest(),'axioms':[]}}}
        args=(suite,self.root/(AREA+'/suites/fixture-a.json'),{'source-a':source})
        self.v.validate_receipt(receipt,*args)
        receipt['modules'][0]['transitive_source_fingerprint']='e'*64
        with self.assertRaises(ValueError):self.v.validate_receipt(receipt,*args)

    def test_predecessor_object_requires_exact_external_receipt(self):
        suite=self.data[AREA+'/suites/fixture-a.json'];source=self.data[PROV+'/SOURCE_MAP.json']['sources'][0];hashes={'Proof':source['sha256']}
        receipt={'status':'FRESH_KERNEL_COMPONENTS','exit_code':0,'kernel_verified':True,'suite_id':'fixture-a',
                 'suite_sha256':self.v.sha(self.root/(AREA+'/suites/fixture-a.json')),'source_hashes':hashes,'post_source_hashes':hashes,
                 'compiler_sha256':suite['pins']['lean_binary_sha256'],'pins':suite['pins'],
                 'modules':[{'module':'Proof','source_sha256':source['sha256'],'object_sha256':'d'*64,'status':'QUALIFIED_PREDECESSOR','predecessor_receipt':'missing.json',
                             'predecessor_receipt_sha256':'f'*64,'transitive_source_fingerprint':'e'*64}],
                 'readbacks':{'Demo.ok':{'type':'Demo.ok : True','axioms':[]}}}
        with self.assertRaises(ValueError):self.v.validate_receipt(receipt,suite,self.root/(AREA+'/suites/fixture-a.json'),{'source-a':source})

    def test_qualified_predecessor_accepts_only_same_source_object_and_transitive_context(self):
        suite=self.data[AREA+'/suites/fixture-a.json'];source=self.data[PROV+'/SOURCE_MAP.json']['sources'][0]
        sources={'source-a':source};path=self.root/(AREA+'/suites/fixture-a.json');hashes={'Proof':source['sha256']}
        prior={'status':'FRESH_KERNEL_COMPONENTS','exit_code':0,'kernel_verified':True,'suite_id':'fixture-a',
               'suite_sha256':self.v.sha(path),'source_hashes':hashes,'post_source_hashes':hashes,
               'compiler_sha256':suite['pins']['lean_binary_sha256'],'pins':suite['pins'],
               'modules':[{'module':'Proof','source_sha256':source['sha256'],'object_sha256':'d'*64,
                           'status':'FRESH_COMPILE','exit_code':0,
                           'transitive_source_fingerprint':self.v.suite_fingerprints(suite,sources)['Proof']}],
               'readbacks':{'Demo.ok':{'type':'Demo.ok : True','axioms':[]}}}
        rel=PROV+'/predecessor.json';put(self.root,rel,prior)
        receipt=deepcopy(prior);receipt['modules'][0].pop('exit_code')
        receipt['modules'][0].update(status='QUALIFIED_PREDECESSOR',predecessor_receipt=rel,
                                     predecessor_receipt_sha256=self.v.sha(self.root/rel))
        def verify(value):
            self.v.validate_receipt(value,suite,path,sources,
                                    {'root':self.root,'suites':{'fixture-a':suite},'paths':{'fixture-a':path}})
        verify(receipt)
        for field in ['source_sha256','object_sha256','transitive_source_fingerprint','predecessor_receipt_sha256']:
            changed=deepcopy(receipt);changed['modules'][0][field]='e'*64
            with self.assertRaises(ValueError):verify(changed)
        put(self.root,rel,receipt)
        with self.assertRaises(ValueError):verify(receipt)

    def test_duplicate_result_and_source_ids_rejected(self):
        for name,key in [(AREA+'/registry.json','results'),(PROV+'/SOURCE_MAP.json','sources')]:
            original=deepcopy(self.data)
            self.data[name][key].append(deepcopy(self.data[name][key][0]));self.reject()
            self.data=original

    def test_duplicate_json_keys_rejected(self):
        (self.root/(AREA+'/registry.json')).write_text('{"schema":1,"schema":2}')
        with self.assertRaises(ValueError):self.v.validate(self.root)

    def test_missing_and_unsafe_paths_rejected(self):
        row=self.data[PROV+'/SOURCE_MAP.json']['sources'][0]
        for bad in ['../escape','/absolute','a//b','a/./b','a\\b','missing.lean']:
            row['path']=bad;self.reject()

    def test_tampered_source_rejected(self):
        row=self.data[PROV+'/SOURCE_MAP.json']['sources'][0]
        (self.root/row['path']).write_text('theorem false_claim : False := by sorry')
        with self.assertRaises(ValueError):self.v.validate(self.root)

    def test_source_origin_cannot_be_changed_to_unknown_archive(self):
        self.data[PROV+'/SOURCE_MAP.json']['sources'][0]['origin']='b'*64;self.reject()

    def test_boolean_byte_count_rejected(self):
        self.data[PROV+'/SOURCE_MAP.json']['sources'][0]['bytes']=True;self.reject()

    def test_empty_and_unknown_evidence_enums_rejected(self):
        for bad in ['',True,'PASS','NOT_RUN_BUT_VERIFIED']:
            self.data[PROV+'/RESULT_STATUS.json']['results'][0]['fresh']=bad;self.reject()

    def test_retained_review_does_not_award_fresh_kernel_credit(self):
        self.data[PROV+'/RESULT_STATUS.json']['results'][0]['fresh']='QUALIFIED';self.reject()

    def test_ordinary_result_cannot_be_promoted_to_kernel_theorem(self):
        suite=self.data[AREA+'/suites/fixture-a.json'];source=self.data[PROV+'/SOURCE_MAP.json']['sources'][0]
        hashes={'Proof':source['sha256']};rel=PROV+'/receipt.json'
        receipt={'status':'FRESH_KERNEL_COMPONENTS','exit_code':0,'kernel_verified':True,'suite_id':'fixture-a',
                 'suite_sha256':self.v.sha(self.root/(AREA+'/suites/fixture-a.json')),
                 'source_hashes':hashes,'post_source_hashes':hashes,'compiler_sha256':suite['pins']['lean_binary_sha256'],
                 'pins':suite['pins'],'original_controls':'PASS',
                 'modules':[{'module':'Proof','source_sha256':source['sha256'],'object_sha256':'d'*64,
                             'status':'FRESH_COMPILE','exit_code':0,
                             'transitive_source_fingerprint':self.v.suite_fingerprints(suite,{'source-a':source})['Proof']}],
                 'readbacks':{'Demo.ok':{'type':'Demo.ok : True','axioms':[]}}}
        receipt.update(original_driver_sha256=source['original_sha256'],original_receipt_sha256='a'*64)
        control_rel=PROV+'/controls.json'
        control={'status':'PASS','exit_code':0,'suite_id':suite['id'],'suite_sha256':receipt['suite_sha256'],'source_hashes':hashes,
                 'driver_source_id':'source-a','driver_sha256':source['original_sha256'],'original_receipt_sha256':'a'*64,
                 'review_driver_source_id':'source-a','review_driver_sha256':source['original_sha256'],'review_receipt_sha256':'b'*64,
                 'control_sources':{'source-a':source['original_sha256']},'stages':[{'stage':'positive-negative','exit_code':0,'log_sha256':'c'*64}],
                 'counts':{'positive':1,'negative':1},'scope':'Synthetic fixture only.'}
        put(self.root,control_rel,control)
        self.data[PROV+'/EVIDENCE_BINDINGS.json']['control_contracts']=[{
            'suite_id':suite['id'],'driver_source_id':'source-a','review_driver_source_id':'source-a','control_source_ids':['source-a'],
            'stages':['positive-negative'],'receipt':control_rel,'sha256':self.v.sha(self.root/control_rel)}]
        put(self.root,rel,receipt)
        self.data[PROV+'/RESULT_STATUS.json']['results'][0].update(fresh='QUALIFIED',receipts=[rel])
        self.save();self.assertEqual(self.v.validate(self.root)['fresh_qualified_results'],1)
        for form in ['ORDINARY','MIXED','CONDITIONAL','IMPLEMENTATION','PROPOSAL']:
            with self.subTest(form=form):
                row=self.data[AREA+'/registry.json']['results'][0];row['math_form']=form
                self.data[PROV+'/EVIDENCE_BINDINGS.json']['results'][0]['statement_sha256']=self.v.statement_digest(row);self.save()
                with self.assertRaisesRegex(ValueError,'Illegal promotion'):
                    self.v.validate(self.root)

    def test_external_warrant_cannot_follow_from_compilation(self):
        row=self.data[PROV+'/RESULT_STATUS.json']['results'][0]
        row['external_warrant']['empirical']='PASS';self.reject()

    def test_target_binding_cannot_be_reassigned_to_another_declaration(self):
        self.data[PROV+'/EVIDENCE_BINDINGS.json']['results'][0]['suite_targets'][0]['targets']={'Demo.other':'source-a'}
        self.reject()

    def test_cross_archive_identical_source_alias_remains_valid(self):
        source=deepcopy(self.data[PROV+'/SOURCE_MAP.json']['sources'][0]);source.update(id='source-b',origin='b'*64)
        self.data[PROV+'/SOURCE_MAP.json']['sources'].append(source)
        archive=deepcopy(self.data[PROV+'/PACKET_LINEAGES.json']['archives'][0]);archive['sha256']='b'*64
        self.data[PROV+'/PACKET_LINEAGES.json']['archives'].append(archive)
        self.data[AREA+'/suites/fixture-a.json']['modules'][0]['source_id']='source-b'
        self.save();self.assertEqual(self.v.validate(self.root)['results'],1)

    def test_stale_receipt_binding_rejected(self):
        receipt={'suite_id':'fixture-a','suite_sha256':'0'*64,'status':'FRESH_KERNEL_COMPONENTS',
                 'source_hashes':{},'kernel_verified':True}
        put(self.root,PROV+'/receipt.json',receipt)
        row=self.data[PROV+'/RESULT_STATUS.json']['results'][0]
        row.update(fresh='FRESH_COMPONENTS',receipts=[PROV+'/receipt.json']);self.reject()

    def test_unequal_module_names_require_separate_import_universes(self):
        suite=self.data[AREA+'/suites/fixture-a.json']
        other=deepcopy(suite);other['id']='fixture-b'
        original=self.data[PROV+'/SOURCE_MAP.json']['sources'][0]
        raw=b'namespace Demo\ntheorem ok : 1 = 1 := rfl\nend Demo\n'
        digest=hashlib.sha256(raw).hexdigest();row=deepcopy(original)
        row.update(id='source-b',member='other/Proof.lean',original_sha256=digest,original_bytes=len(raw),
                   path=AREA+'/source-store/'+digest+'.lean',sha256=digest,bytes=len(raw))
        (self.root/row['path']).write_bytes(raw)
        self.data[PROV+'/SOURCE_MAP.json']['sources'].append(row)
        other['modules'][0]['source_id']='source-b'
        self.data[AREA+'/suites/fixture-b.json']=other
        self.data[AREA+'/registry.json']['suites'].append(AREA+'/suites/fixture-b.json')
        self.save();self.assertEqual(self.v.validate(self.root)['suites'],2)
        suite['modules'].append(deepcopy(other['modules'][0]));self.reject()

    def test_missing_import_or_wrong_declared_imports_rejected(self):
        self.data[AREA+'/suites/fixture-a.json']['modules'][0]['imports']=['Absent'];self.reject()

    def test_dependency_names_cannot_escape_replay_paths(self):
        pins=self.data[AREA+'/suites/fixture-a.json']['pins']['packages']
        for name in ['../../escape','/absolute','nested/package','bad\\package','.']:
            with self.subTest(name=name):
                pins[:]=[pins[0],{'name':name,'revision':'a'*40}]
                self.reject()

    def test_wrong_namespace_target_rejected(self):
        self.data[AREA+'/suites/fixture-a.json']['targets'][0]['name']='Other.ok';self.reject()

    def test_unapproved_axiom_and_sorry_rejected_even_with_updated_digest(self):
        for code in ['axiom trick : False','theorem trick : False := by sorry','unsafe def trick := 1']:
            with self.assertRaises(ValueError):self.v.check_lean(code)

    def test_nested_comments_do_not_create_false_imports(self):
        self.assertEqual(self.v.lean_imports('/- outer /- import Wrong -/ -/\nimport Actual\n'),['Actual'])

    def test_constant_constructor_is_not_an_unproved_constant_declaration(self):
        self.v.check_lean('inductive Expr where\n | constant : Nat -> Expr\ndef one := Expr.constant 1')
        with self.assertRaises(ValueError):self.v.check_lean('constant unproved : False')

    def test_escaped_declaration_has_its_actual_qualified_name(self):
        self.assertEqual(self.v.declared_targets('namespace Model\ndef «variable» := 1\nend Model'),{'Model.variable'})

    def test_supersession_cycle_rejected(self):
        edges=self.data[PROV+'/SUPERSESSION.json']['edges']
        edges.append({'from':'source-a','to':'source-a','statement':'same','relation':'SUPERSEDES'})
        self.reject()

    def test_derived_bytes_require_reviewed_diff(self):
        row=self.data[PROV+'/SOURCE_MAP.json']['sources'][0]
        row['projection']='DERIVED';row['original_sha256']='b'*64;self.reject()

    def test_private_locator_in_public_prose_rejected(self):
        with self.assertRaises(ValueError):self.v.check_public_text('/'+'mnt/data/private/result.txt')

    def test_symlink_source_rejected(self):
        row=self.data[PROV+'/SOURCE_MAP.json']['sources'][0]
        source=self.root/row['path'];target=self.root/'elsewhere';target.write_bytes(source.read_bytes());source.unlink()
        try:source.symlink_to(target)
        except OSError:self.skipTest('Host does not permit symlink creation; WSL run is required')
        with self.assertRaises(ValueError):self.v.validate(self.root)


class ActualEvidenceAssociationTests(unittest.TestCase):
    """Substitute real, valid evidence for a different current research result."""
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('actual_continuations',SCRIPT)
        cls.v=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.v)
        cls.root=SCRIPT.parents[1]
        cls.registry=cls.v.read_json(cls.root/AREA/'registry.json')
        cls.statuses=cls.v.read_json(cls.root/PROV/'RESULT_STATUS.json')
        cls.receipt=cls.root/PROV/'checks/769dc45d15ba-global-parity-controller.json'

    def validate_override(self, overrides):
        original=self.v.read_json
        def read(path):
            return deepcopy(overrides[Path(path)]) if Path(path) in overrides else original(path)
        with patch.object(self.v,'read_json',side_effect=read):self.v.validate(self.root)

    def test_integer_budget_receipt_cannot_qualify_global_parity(self):
        registry=deepcopy(self.registry);statuses=deepcopy(self.statuses)
        row=next(x for x in registry['results'] if x['id']=='T5-GLOBAL')
        row['suite_ids']=['0a74eb642cc6-integer-budget-v3']
        status=next(x for x in statuses['results'] if x['id']=='T5-GLOBAL')
        status.update(fresh='FRESH_COMPONENTS',receipts=[PROV+'/checks/0a74eb642cc6-integer-budget-v3.json'])
        with self.assertRaisesRegex(ValueError,'[Aa]ssociation|[Bb]inding'):
            self.validate_override({self.root/AREA/'registry.json':registry,self.root/PROV/'RESULT_STATUS.json':statuses})

    def test_knowledge_review_cannot_qualify_global_parity(self):
        registry=deepcopy(self.registry)
        row=next(x for x in registry['results'] if x['id']=='T5-GLOBAL')
        row['review_source_ids']=next(x for x in registry['results'] if x['id']=='T6-KNOWLEDGE')['review_source_ids']
        with self.assertRaisesRegex(ValueError,'[Aa]ssociation|[Bb]inding'):
            self.validate_override({self.root/AREA/'registry.json':registry})

    def test_qualified_original_controls_require_provenance(self):
        receipt=self.v.read_json(self.receipt)
        receipt.pop('original_driver_sha256');receipt.pop('original_receipt_sha256')
        with self.assertRaisesRegex(ValueError,'[Cc]ontrol|[Dd]river'):
            self.validate_override({self.receipt:receipt})

    def test_array_receipt_has_descriptive_validation_failure(self):
        with self.assertRaisesRegex(ValueError,'[Oo]bject'):
            self.validate_override({self.receipt:[]})


if __name__=='__main__':unittest.main(verbosity=2)
