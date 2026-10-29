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


class ContinuationCopyTests(unittest.TestCase):
    """Current-copy behavior under real synthetic Git and filesystem changes."""

    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('continuation_copy_resolver', SCRIPT.with_name('resolve_t20_v6_source.py'))
        cls.resolver=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.resolver)
        spec=importlib.util.spec_from_file_location('continuation_copy_validator', SCRIPT)
        cls.legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.legacy)

    def git(self,*args):
        import subprocess
        return subprocess.check_output(['git','--no-replace-objects','-c','user.name=Fixture',
            '-c','user.email=fixture@example.invalid',*args],cwd=self.root,stderr=subprocess.DEVNULL)

    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='continuation-copy-fixture-');self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.git('init','-q')
        self.body=b'namespace Demo\ntheorem ok : True := True.intro\nend Demo\n'
        self.excluded_body=b'namespace Held\ntheorem keep : True := True.intro\nend Held\n'
        self.identity=hashlib.sha256(self.body).hexdigest()
        self.excluded=hashlib.sha256(self.excluded_body).hexdigest()
        self.original=AREA+'/source-store/'+self.identity+'.lean'
        self.retained='experiments/orthemology-v5-successors/source-store/'+self.identity+'/DifferentStorageName.lean'
        self.excluded_original=AREA+'/source-store/'+self.excluded+'.lean'
        self.source={'id':'source-a','origin':ORIGIN,'member':'src/Proof.lean',
            'original_sha256':self.identity,'original_bytes':len(self.body),'path':self.original,
            'sha256':self.identity,'bytes':len(self.body),'projection':'EXACT','derivation':None}
        excluded=dict(self.source,id='source-b',member='src/Held.lean',original_sha256=self.excluded,
            original_bytes=len(self.excluded_body),path=self.excluded_original,
            sha256=self.excluded,bytes=len(self.excluded_body))
        legacy={'sources':[self.source,excluded]}
        self.legacy_map=PROV+'/SOURCE_MAP.json'
        self.successor_map='docs/provenance/v5-successors/SOURCE_MAP.json'
        self.preservation='docs/provenance/v5-successors/PRESERVATION.json'
        put(self.root,self.legacy_map,legacy)
        for path,body in [(self.original,self.body),(self.excluded_original,self.excluded_body)]:
            target=self.root/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(body)
        self.git('add','.');self.git('commit','-qm','Synthetic original')
        legacy_commit=self.git('rev-parse','HEAD').decode().strip()
        legacy_tree=self.git('rev-parse','HEAD^{tree}').decode().strip()
        inventory=[]
        for path in [self.original,self.excluded_original,self.legacy_map]:
            body=(self.root/path).read_bytes()
            inventory.append({'path':path,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),
                'git_blob_sha1':self.git('rev-parse','HEAD:'+path).decode().strip()})
        successor=[]
        for source,name in [(self.source,'DifferentStorageName.lean'),(excluded,'Held.lean')]:
            path='experiments/orthemology-v5-successors/source-store/'+source['sha256']+'/'+name
            target=self.root/path;target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes((self.root/source['path']).read_bytes())
            successor.append({'id':'new-'+source['id'],'original_sha256':source['sha256'],
                'original_bytes':source['bytes'],'public_path':path,'public_sha256':source['sha256'],
                'public_bytes':source['bytes'],'projection':'EXACT','derivation':None})
        put(self.root,self.successor_map,{'sources':successor,'reviews':[]})
        put(self.root,self.preservation,{'schema':'orthemology-v5-preservation-v1',
            'base_commit':legacy_commit,'base_tree':legacy_tree,
            'roots':[AREA,PROV],'files':inventory})
        self.git('add','.');self.git('commit','-qm','Synthetic retained copies')
        base=self.git('rev-parse','HEAD').decode().strip()
        metadata={name:(len((self.root/name).read_bytes()),hashlib.sha256((self.root/name).read_bytes()).hexdigest())
                  for name in [self.legacy_map,self.successor_map,self.preservation]}
        self.base=base
        pins={'CONTINUATION_COPY_BASE':base,'CONTINUATION_LEGACY_BASE':legacy_commit,
              'CONTINUATION_COPY_COUNT':1,'CONTINUATION_COPY_EXCLUDED':self.excluded,
              'CONTINUATION_COPY_METADATA':metadata}
        self.copy_pins=pins
        for module in {self.resolver,getattr(self.legacy,'_source',self.resolver)}:
            for name,value in pins.items():
                context=patch.object(module,name,value,create=True);context.start();self.addCleanup(context.stop)
        self.row={'source_sha256':self.identity,'source_bytes':len(self.body),'disposition':'REUSE',
                  'repository_path':self.original,'public_sha256':self.identity,'public_bytes':len(self.body)}

    def absent(self):
        (self.root/self.original).unlink()

    def test_absent_original_returns_exact_retained_current_body(self):
        self.absent()
        try:
            body=self.resolver.source_bytes(self.root,self.row)
        except OSError as exc:
            self.fail('Qualified missing original did not resolve its exact current copy: '+type(exc).__name__)
        self.assertEqual(body,self.body)
        self.assertFalse((self.root/self.original).exists())

    def test_absent_legacy_source_keeps_original_source_id_and_bytes(self):
        self.absent()
        before=deepcopy(self.source)
        self.assertEqual(self.legacy.source_bytes(self.root,self.source),self.body)
        self.assertEqual(self.source,before)

    def test_present_corrupt_original_is_not_masked_by_retained_copy(self):
        (self.root/self.original).write_bytes(b'X'*len(self.body))
        with self.assertRaises(ValueError):self.resolver.source_bytes(self.root,self.row)

    def test_present_executable_original_is_rejected(self):
        (self.root/self.original).chmod(0o755)
        with self.assertRaises(ValueError):self.resolver.source_bytes(self.root,self.row)

    def test_missing_or_corrupt_retained_copy_is_rejected(self):
        self.absent();target=self.root/self.retained
        for replacement in [None,b'X'*len(self.body)]:
            with self.subTest(replacement=replacement is None):
                if replacement is None:target.unlink()
                else:target.write_bytes(replacement)
                with self.assertRaises((ValueError,OSError)):self.resolver.source_bytes(self.root,self.row)

    def test_symlinked_retained_file_or_parent_is_rejected(self):
        self.absent();target=self.root/self.retained
        other=self.root/'outside.lean';other.write_bytes(self.body)
        target.unlink();target.symlink_to(other)
        with self.assertRaises((ValueError,OSError)):self.resolver.source_bytes(self.root,self.row)
        target.unlink();target.write_bytes(self.body)
        directory=target.parent;replacement=self.root/'replacement';directory.rename(replacement);directory.symlink_to(replacement,target_is_directory=True)
        with self.assertRaises((ValueError,OSError)):self.resolver.source_bytes(self.root,self.row)

    def test_staged_change_cannot_hide_behind_original_absence(self):
        (self.root/self.original).write_bytes(b'X'*len(self.body));self.git('add',self.original);self.absent()
        with self.assertRaises(ValueError):self.resolver.source_bytes(self.root,self.row)

    def test_staged_retained_mode_change_is_rejected(self):
        self.absent();self.git('update-index','--chmod=+x',self.retained)
        with self.assertRaises(ValueError):self.resolver.source_bytes(self.root,self.row)

    def test_staged_deletion_of_original_is_accepted(self):
        self.absent();self.git('rm','--cached','-q','--',self.original)
        self.assertEqual(self.resolver.source_bytes(self.root,self.row),self.body)

    def test_unknown_or_excluded_original_has_no_fallback(self):
        self.absent()
        for path,body in [(AREA+'/source-store/'+'0'*64+'.lean',self.body),
                          (self.excluded_original,self.excluded_body)]:
            target=self.root/path
            if target.exists():target.unlink()
            row=dict(self.row,repository_path=path,source_sha256=hashlib.sha256(body).hexdigest(),
                     source_bytes=len(body),public_sha256=hashlib.sha256(body).hexdigest(),public_bytes=len(body))
            with self.subTest(path=path):
                with self.assertRaises((ValueError,OSError)):self.resolver.source_bytes(self.root,row)

    def test_changed_source_id_or_member_cannot_rebind_missing_original(self):
        self.absent()
        for key,value in [('id','new-id'),('member','src/Rebound.lean'),('origin','b'*64)]:
            row=dict(self.source,**{key:value})
            with self.subTest(field=key):
                with self.assertRaises(ValueError):self.legacy.source_bytes(self.root,row)

    def test_changed_frozen_metadata_rejects_absent_copy(self):
        self.absent();path=self.root/self.legacy_map
        path.write_bytes(path.read_bytes()+b' ')
        with self.assertRaises(ValueError):self.resolver.source_bytes(self.root,self.row)

    def test_same_size_corrupted_original_git_object_is_rejected(self):
        import zlib
        self.absent();blob=self.git('rev-parse','HEAD:'+self.original).decode().strip()
        loose=self.root/'.git/objects'/blob[:2]/blob[2:]
        loose.chmod(0o600)
        loose.write_bytes(zlib.compress(b'blob '+str(len(self.body)).encode()+b'\0'+b'X'*len(self.body)))
        with self.assertRaises(ValueError):self.resolver.source_bytes(self.root,self.row)

    def test_projection_metadata_cannot_change_disposition_or_identity(self):
        self.absent()
        for key,value in [('disposition','PROJECT'),('source_sha256','0'*64),('source_bytes',len(self.body)+1),
                          ('repository_revision',self.git('rev-parse','HEAD').decode().strip())]:
            with self.subTest(field=key):
                with self.assertRaises(ValueError):self.resolver.source_bytes(self.root,dict(self.row,**{key:value}))


    def owner(self, name):
        sys.path.insert(0,str(SCRIPT.parent))
        spec=importlib.util.spec_from_file_location('copy_gate_'+name,SCRIPT.with_name(name+'.py'))
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        for target in {getattr(module,'_source',self.resolver),sys.modules.get('resolve_t20_v6_source',self.resolver)}:
            for key,value in self.copy_pins.items():
                context=patch.object(target,key,value,create=True);context.start();self.addCleanup(context.stop)
        return module

    def test_t20_object_gate_consumes_the_same_current_copy(self):
        gate=self.owner('validate_t20_v6_projection');self.absent()
        self.assertEqual(gate.check_object(self.root,self.row),[])

    def test_t20_preserved_root_gate_admits_only_authenticated_deletion(self):
        gate=self.owner('validate_t20_v6_projection');self.absent()
        with patch.object(gate,'HISTORICAL_PROSE',{}),patch.object(gate,'BASE',self.base):
            self.assertEqual(gate.check_preserved_roots(self.root,{}),[])
            (self.root/self.original).write_bytes(b'X'*len(self.body));self.git('add',self.original);self.absent()
            self.assertTrue(gate.check_preserved_roots(self.root,{}))

    def test_reader_currentness_gate_keeps_staged_change_visible(self):
        gate=self.owner('check_reader_pilot');self.absent()
        self.assertEqual(gate.check_corpus_currentness(self.root,self.base),[])
        (self.root/self.original).write_bytes(b'X'*len(self.body));self.git('add',self.original);self.absent()
        self.assertTrue(gate.check_corpus_currentness(self.root,self.base))

    def test_frozen_preservation_keeps_rows_and_rejects_extra_members(self):
        gate=self.owner('validate_v5_successors');inventory=json.loads((self.root/self.preservation).read_bytes())
        metadata={'path':self.legacy_map,'sha256':hashlib.sha256((self.root/self.legacy_map).read_bytes()).hexdigest()}
        bound={'schema':'orthemology-v5-baseline-binding-v1','base_commit':inventory['base_commit'],
            'base_tree':inventory['base_tree'],'preservation_sha256':hashlib.sha256((self.root/self.preservation).read_bytes()).hexdigest(),
            'legacy_registry':metadata,'legacy_overlay':metadata}
        anchor=dict(bound,git_required=True);anchor.pop('schema')
        bundle={'baseline_binding':bound,'preservation':inventory,'registry':{
            'records':{'PRESERVATION':{'sha256':bound['preservation_sha256']}},
            'baseline_commit':bound['base_commit'],'baseline_tree':bound['base_tree']}}
        before=deepcopy(bundle);self.absent()
        try:
            preserved=gate._preservation(bundle,self.root,anchor)
        except ValueError as exc:
            self.fail('Qualified current copy did not preserve the frozen inventory: '+str(exc))
        self.assertEqual(set(preserved),{r['path'] for r in inventory['files']})
        self.assertEqual(bundle,before)
        (self.root/AREA/'source-store/extra.lean').write_bytes(b'extra')
        with self.assertRaises(ValueError):gate._preservation(bundle,self.root,anchor)

    def test_immutable_reference_resolves_only_exact_current_copy(self):
        gate=self.owner('validate_internal_references');self.absent()
        with patch.object(gate,'ROOT',str(self.root)):
            self.assertTrue(gate._resolves('preserved.md',self.original))
            (self.root/self.retained).write_bytes(b'X'*len(self.body))
            self.assertFalse(gate._resolves('preserved.md',self.original))


class FrozenAdministrativeRecordTests(unittest.TestCase):
    """Native history and real-index controls for the four finite record roles."""
    BASE = '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
    TREE_ROWS_SHA256 = '7e65473d07162893f11ee6b2a1cc4cd33e4add3f20281d8ee4cbfecab68b5f0e'
    PREFIXES = (
        'docs/provenance/v5-research-continuations/checks/',
        'experiments/orthemology-v5-continuations/native-suites/',
        'experiments/orthemology-v5-continuations/suites/',
        'experiments/orthemology-v5-successors/suites/',
    )

    @classmethod
    def setUpClass(cls):
        import os
        import subprocess
        cls.os, cls.subprocess = os, subprocess
        cls.environment = dict(os.environ, GIT_NO_LAZY_FETCH='1', GIT_NO_REPLACE_OBJECTS='1',
                               GIT_ALLOW_PROTOCOL='', GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0')
        cls.project = globals().get('PROJECT_ROOT', Path(__file__).resolve().parents[1])
        spec = importlib.util.spec_from_file_location('administrative_continuations', SCRIPT)
        cls.validator = importlib.util.module_from_spec(spec); spec.loader.exec_module(cls.validator)
        cls.source = cls.validator._source
        raw = cls.git(cls.project, 'ls-tree', '-rz', '--full-tree', cls.BASE, '--', *cls.PREFIXES)
        if hashlib.sha256(raw).hexdigest() != cls.TREE_ROWS_SHA256:
            raise AssertionError('Independent original administrative native population differs')
        entries = {}
        for record in raw.split(b'\0'):
            if record:
                left, path = record.split(b'\t', 1); mode, kind, blob = left.decode().split()
                if mode != '100644' or kind != 'blob': raise AssertionError('Original mode/type differs')
                entries[path.decode()] = blob
        if len(entries) != 236 or set(entries) != cls.source.ADMIN_RECORD_PATHS:
            raise AssertionError('Finite original role population differs')
        cls.directory = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.directory.cleanup)
        cls.root = Path(cls.directory.name)
        cls.git(cls.root, 'init', '--quiet')
        objects = cls.git(cls.project, 'rev-parse', '--path-format=absolute', '--git-path', 'objects').decode().strip()
        cls.alternates = cls.root / '.git/objects/info/alternates'
        cls.alternates.write_text(objects + '\n')
        cls.paths = [min(path for path in entries if path.startswith(prefix)) for prefix in cls.PREFIXES]
        cls.originals = {}
        for path in cls.paths:
            blob = entries[path]; body = cls.git(cls.root, 'cat-file', 'blob', blob)
            cls.put(path, body); cls.git(cls.root, 'update-index', '--add', '--cacheinfo', '100644', blob, path)
            cls.originals[path] = body
        for path, (blob, _, _, _) in cls.source.ADMIN_GUIDES.items():
            original = cls.git(cls.root, 'cat-file', 'blob', blob)
            body = cls.source.administrative_guide_adaptation(path, original)
            cls.put(path, body)
            oid = cls.git(cls.root, 'hash-object', '-w', '--stdin', incoming=body).decode().strip()
            cls.git(cls.root, 'update-index', '--add', '--cacheinfo', '100644', oid, path)
            cls.originals[path] = body
        cls.original_index = (cls.root / '.git/index').read_bytes()
        cls.original_alternates = cls.alternates.read_bytes()

    @classmethod
    def git(cls, root, *args, incoming=None):
        result = cls.subprocess.run(['git', '--no-replace-objects', '--literal-pathspecs', *args],
            cwd=root, env=cls.environment, input=incoming, capture_output=True)
        if result.returncode:
            raise AssertionError('Required native public fixture operation unavailable: ' + args[0])
        return result.stdout

    @classmethod
    def put(cls, path, body):
        target = cls.root / path; target.parent.mkdir(parents=True, exist_ok=True)
        if target.is_symlink(): target.unlink()
        target.write_bytes(body); target.chmod(0o644)

    def tearDown(self):
        for path, body in self.originals.items(): self.put(path, body)
        (self.root / '.git/index').write_bytes(self.original_index)
        self.alternates.write_bytes(self.original_alternates)

    def test_four_roles_keep_exact_bytes_with_present_worktree_and_staged_absence(self):
        for state in ('present', 'worktree-absent', 'staged-absent'):
            if state == 'worktree-absent':
                for path in self.paths: (self.root / path).unlink()
            elif state == 'staged-absent':
                self.git(self.root, 'update-index', '--force-remove', '--', *self.paths)
            for path in self.paths:
                with self.subTest(state=state, path=path):
                    self.assertEqual(self.os.path.lexists(self.root / path), state == 'present')
                    body = self.source.administrative_record_bytes(self.root, path)
                    self.assertEqual(body, self.originals[path])
                    self.assertEqual(self.validator.read_record(self.root, path), json.loads(body))
                    self.assertEqual(self.os.path.lexists(self.root / path), state == 'present')

    def test_present_corruption_symlink_and_executable_mode_are_rejected(self):
        path = self.paths[0]; target = self.root / path
        target.write_bytes(self.originals[path] + b' ')
        with self.assertRaises(ValueError): self.source.administrative_record_bytes(self.root, path)
        self.put(path, self.originals[path]); target.chmod(0o755)
        with self.assertRaises(ValueError): self.source.administrative_record_bytes(self.root, path)
        target.chmod(0o644); target.unlink(); target.symlink_to(self.root / self.paths[1])
        with self.assertRaises(ValueError): self.source.administrative_record_bytes(self.root, path)

    def test_real_index_corruption_is_not_hidden_by_correct_present_bytes(self):
        path = self.paths[0]
        oid = self.git(self.root, 'hash-object', '-w', '--stdin', incoming=b'changed').decode().strip()
        self.git(self.root, 'update-index', '--cacheinfo', '100644', oid, path)
        with self.assertRaises(ValueError): self.source.administrative_record_bytes(self.root, path)
        (self.root / '.git/index').write_bytes(self.original_index)
        oid = self.git(self.root, 'hash-object', '--stdin', incoming=self.originals[path]).decode().strip()
        self.git(self.root, 'update-index', '--cacheinfo', '100755', oid, path)
        with self.assertRaises(ValueError): self.source.administrative_record_bytes(self.root, path)

    def test_missing_original_history_refuses_even_a_correct_present_copy(self):
        self.alternates.write_bytes(b'')
        with self.assertRaises(ValueError): self.source.administrative_record_bytes(self.root, self.paths[0])

    def test_unknown_path_and_wrong_requested_identity_are_rejected(self):
        unknown = self.PREFIXES[0] + 'unreviewed.json'
        self.put(unknown, b'{}')
        with patch.object(self.source, '_administrative_git', side_effect=AssertionError('unknown path reached Git')):
            with self.assertRaises(ValueError): self.source.administrative_record_bytes(self.root, unknown)
        (self.root / unknown).unlink()
        with self.assertRaises(ValueError): self.source.administrative_record_bytes(self.root, self.paths[0], '0' * 64)
        with self.assertRaises(ValueError): self.source.administrative_record_bytes(self.root, self.paths[0], size=1)

    def test_exact_navigation_keeps_the_prior_typed_route_and_refuses_wording_changes(self):
        for path in self.source.ADMIN_GUIDES:
            original = self.source.administrative_guide_source_bytes(self.root, path, allow_original=False)
            self.assertEqual(hashlib.sha256(original).hexdigest(), self.source.ADMIN_GUIDES[path][1])
            if path in self.source.TYPED_GUIDES:
                self.assertEqual(self.source.typed_guide_source_bytes(self.root, path), original)
        path = next(iter(self.source.ADMIN_GUIDES))
        (self.root / path).write_bytes(self.originals[path] + b'Additional claim.\n')
        with self.assertRaises(ValueError): self.source.administrative_guide_source_bytes(self.root, path)


    def projection_baseline(self):
        """Real native guide history, isolated from unrelated preserved roots."""
        try:
            for path, (blob, _, _, _) in self.source.ADMIN_GUIDES.items():
                published = self.git(self.project, 'show',
                    '4bcb6fbbefb6cf960147dfc79e17f350f5370cdf:' + path)
                self.assertEqual(self.originals[path], published)
                self.git(self.root, 'update-index', '--cacheinfo', '100644', blob, path)
            return self.git(self.root, 'write-tree').decode().strip()
        finally:
            (self.root / '.git/index').write_bytes(self.original_index)

    def projection_errors(self, baseline):
        import validate_t20_v6_projection as projection
        index = (self.root / '.git/index').read_bytes()
        with patch.object(projection, 'BASE', baseline), \
             patch.object(projection, 'HISTORICAL_PROSE', {}):
            errors = projection.check_preserved_roots(self.root, {})
        self.assertEqual((self.root / '.git/index').read_bytes(), index)
        return errors

    def test_projection_accepts_exact_published_administrative_navigation(self):
        baseline = self.projection_baseline()
        self.assertEqual(self.projection_errors(baseline), [])

    def test_projection_rejects_each_changed_guide_and_hidden_staged_tamper(self):
        baseline = self.projection_baseline()
        self.assertEqual(self.projection_errors(baseline), [])
        bad = self.git(self.root, 'hash-object', '-w', '--stdin',
                       incoming=b'Unqualified administrative wording.\n').decode().strip()
        for path in self.source.ADMIN_GUIDES:
            with self.subTest(path=path, state='changed-worktree'):
                (self.root / path).write_bytes(self.originals[path] + b'Additional claim.\n')
                self.assertTrue(self.projection_errors(baseline))
                self.put(path, self.originals[path])
                self.assertEqual(self.projection_errors(baseline), [])
            with self.subTest(path=path, state='changed-index-correct-worktree'):
                self.git(self.root, 'update-index', '--cacheinfo', '100644', bad, path)
                self.assertTrue(self.projection_errors(baseline))
                (self.root / '.git/index').write_bytes(self.original_index)
                self.assertEqual(self.projection_errors(baseline), [])

    def test_projection_rejects_guide_removal_type_mode_and_missing_history(self):
        baseline = self.projection_baseline()
        self.assertEqual(self.projection_errors(baseline), [])
        path = next(iter(self.source.ADMIN_GUIDES)); target = self.root / path
        for state in ('worktree-absent', 'staged-absent', 'symlink', 'executable'):
            with self.subTest(state=state):
                if state == 'executable':
                    target.chmod(0o755)
                else:
                    target.unlink()
                    if state == 'staged-absent':
                        self.git(self.root, 'update-index', '--force-remove', '--', path)
                    elif state == 'symlink':
                        target.symlink_to(self.root / self.paths[0])
                self.assertTrue(self.projection_errors(baseline))
                self.put(path, self.originals[path])
                (self.root / '.git/index').write_bytes(self.original_index)
                self.assertEqual(self.projection_errors(baseline), [])
        self.alternates.write_bytes(b'')
        self.assertTrue(self.projection_errors(baseline))
        self.alternates.write_bytes(self.original_alternates)
        self.assertEqual(self.projection_errors(baseline), [])


class SparsePriorHistoricalSourceTests(unittest.TestCase):
    """Real native originals and source-role controls for the incorporated notes."""
    REV = '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
    OWNER = 'docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json'
    CROSS = 'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json'
    SOURCE_MAP = 'docs/provenance/v5-research-continuations/SOURCE_MAP.json'
    NOTES = {'docs/provenance/v5-research-continuations/notes/0ba213e9f1cd5c985925864d7edcc505c3adb16fa30036338b39ad04b77ea54f.md': ('4de8b1921235006c37ae00945fad3e6e328d6336',
                                                                                                                         '0ba213e9f1cd5c985925864d7edcc505c3adb16fa30036338b39ad04b77ea54f',
                                                                                                                         1607),
 'docs/provenance/v5-research-continuations/notes/22c70614cb4a011790e348461f3e2fbea5e13b2eeb788dcd2124560fb0ef0f07.md': ('d82e2625487cf0771f96f3a883170f7edd7bd919',
                                                                                                                         '22c70614cb4a011790e348461f3e2fbea5e13b2eeb788dcd2124560fb0ef0f07',
                                                                                                                         2703),
 'docs/provenance/v5-research-continuations/notes/236f78b5ecc313f47085a765f26ef2f0482fdaff154c2aebb7393a8c01c59236.md': ('3f1ebe731980b67b94945f58689999b5b4edf55d',
                                                                                                                         '236f78b5ecc313f47085a765f26ef2f0482fdaff154c2aebb7393a8c01c59236',
                                                                                                                         4625),
 'docs/provenance/v5-research-continuations/notes/251394f394fe75f9062aaa4dea33da2b3ffa3370572e14ba60e52ceb1c68a30b.md': ('32e1bec0ba44d1f558286b0d5878d2f482b9907e',
                                                                                                                         '251394f394fe75f9062aaa4dea33da2b3ffa3370572e14ba60e52ceb1c68a30b',
                                                                                                                         8764),
 'docs/provenance/v5-research-continuations/notes/3cdf7cb6582b44a2198ce9527847416ee834aa7636999871081e1677600a9f60.md': ('ead60afbdc6f47c99c8aa17403daab4f9f602083',
                                                                                                                         '3cdf7cb6582b44a2198ce9527847416ee834aa7636999871081e1677600a9f60',
                                                                                                                         2311),
 'docs/provenance/v5-research-continuations/notes/6b796642b23d6280cfec717f7a762a55fe76a2fbc67b16f6c6b0fc1008599476.md': ('9bd1c1e0e30b46800c04c6dd189e40066b6ed4a6',
                                                                                                                         '6b796642b23d6280cfec717f7a762a55fe76a2fbc67b16f6c6b0fc1008599476',
                                                                                                                         8765),
 'docs/provenance/v5-research-continuations/notes/767be5173842b1520af940db691120091d868677754e7b452a0c7467ece4665d.md': ('b64eac11f5d5efd6618219731d6fa543d3c73487',
                                                                                                                         '767be5173842b1520af940db691120091d868677754e7b452a0c7467ece4665d',
                                                                                                                         7472),
 'docs/provenance/v5-research-continuations/notes/87cad31677966946661ca6effed55165db3505d1bca45bfa6ba2428946cca88c.md': ('40d69b1e5e377cab279f1d662cffcab0f1481378',
                                                                                                                         '87cad31677966946661ca6effed55165db3505d1bca45bfa6ba2428946cca88c',
                                                                                                                         5124),
 'docs/provenance/v5-research-continuations/notes/893aabc2774f6a31df5777a9dab8cc4de2840a2f01d95691ce913f0406ab489c.md': ('dd884420d315600cc7273536e8b70d48e5d3c3dd',
                                                                                                                         '893aabc2774f6a31df5777a9dab8cc4de2840a2f01d95691ce913f0406ab489c',
                                                                                                                         6175),
 'docs/provenance/v5-research-continuations/notes/99847d69a9a9df978a7e596cc35b75b744e7661b72dd514d29bc3cf4d897cc6c.md': ('e47ed15533018067e34c25ab30a659386a02d043',
                                                                                                                         '99847d69a9a9df978a7e596cc35b75b744e7661b72dd514d29bc3cf4d897cc6c',
                                                                                                                         4740),
 'docs/provenance/v5-research-continuations/notes/9c7508259cb9916b1ba6b0557584cff186487d256dac3918269052b4cd5626b6.md': ('db0f92e4868eb7a8df168ba69f53fce74a54f65e',
                                                                                                                         '9c7508259cb9916b1ba6b0557584cff186487d256dac3918269052b4cd5626b6',
                                                                                                                         1387),
 'docs/provenance/v5-research-continuations/notes/b0edcf2ebfe71957a789033dec063424e658fe8971ef28e1f2fe9a4956e5d18e.md': ('5f7789f7cbd38d8045e95154a00f5e2196b63134',
                                                                                                                         'b0edcf2ebfe71957a789033dec063424e658fe8971ef28e1f2fe9a4956e5d18e',
                                                                                                                         2448),
 'docs/provenance/v5-research-continuations/notes/b1a029f0cd442ff623d9783c15e09260cd6063bf976290010b3fba07ec0548bf.md': ('04a057f0604fcd9de9be11443113df5636510b19',
                                                                                                                         'b1a029f0cd442ff623d9783c15e09260cd6063bf976290010b3fba07ec0548bf',
                                                                                                                         4114),
 'docs/provenance/v5-research-continuations/notes/b3403229c91a718f3e8c61068649590ec090d208206d9922da2270f71e956658.md': ('c45b5a4f02d336ff00230e07d155b043874c4eca',
                                                                                                                         'b3403229c91a718f3e8c61068649590ec090d208206d9922da2270f71e956658',
                                                                                                                         10334),
 'docs/provenance/v5-research-continuations/notes/b545637a8dc1bdfda4a949dfe3a6084b469c5ef8639af8ae97b8e5fef683e0d3.md': ('ab2e9c125c1a65714e3a0670043f65859f299774',
                                                                                                                         'b545637a8dc1bdfda4a949dfe3a6084b469c5ef8639af8ae97b8e5fef683e0d3',
                                                                                                                         9202),
 'docs/provenance/v5-research-continuations/notes/b6a6db5048293e4de7f286689ea635448ea61aec5f9a08acff0968892e10b5bb.md': ('ab8e4a2149efeee43a943db37d0e51eb144200b3',
                                                                                                                         'b6a6db5048293e4de7f286689ea635448ea61aec5f9a08acff0968892e10b5bb',
                                                                                                                         5703),
 'docs/provenance/v5-research-continuations/notes/c079f7733904976a602adae47284062ad23141dd9c79b04652e3561e74692a50.md': ('9701a6c26c8419e2cd01db4a86a2db47af28659d',
                                                                                                                         'c079f7733904976a602adae47284062ad23141dd9c79b04652e3561e74692a50',
                                                                                                                         10353),
 'docs/provenance/v5-research-continuations/notes/cab3e124b6ef2faad2c945c20d22d50e7fc2d1455367bcd4cb6dcf633908b3b9.md': ('885d647840476099ca58a0a9b8f0ca6474033164',
                                                                                                                         'cab3e124b6ef2faad2c945c20d22d50e7fc2d1455367bcd4cb6dcf633908b3b9',
                                                                                                                         2872),
 'docs/provenance/v5-research-continuations/notes/d519d3b51e5f03f7b55db3c22c2a423bdb6cf5a702e726e4a57459e527ab8dbd.md': ('093d47e908d27ac854b722d059d2bf6ee14f2ce7',
                                                                                                                         'd519d3b51e5f03f7b55db3c22c2a423bdb6cf5a702e726e4a57459e527ab8dbd',
                                                                                                                         11197),
 'docs/provenance/v5-research-continuations/notes/daa7e92aaeee1cc9ae5601877a01ddfbb8ce2cf9cabf3f4f693ec8a7c8a0893b.md': ('05d1ee82e1cea6db4639dc96147571642a9b6f19',
                                                                                                                         'daa7e92aaeee1cc9ae5601877a01ddfbb8ce2cf9cabf3f4f693ec8a7c8a0893b',
                                                                                                                         7244),
 'docs/provenance/v5-research-continuations/notes/e2afa027d652771010f909eb34642d5512c102a34c85a0ef90ff466b9fd7e0ae.md': ('1442f0674ffe32f5a50d146993d4b3ac585e07c4',
                                                                                                                         'e2afa027d652771010f909eb34642d5512c102a34c85a0ef90ff466b9fd7e0ae',
                                                                                                                         5928),
 'docs/provenance/v5-research-continuations/notes/e2cf470975d1d6f344d3dd788410c911b5d6f9d93fa528709339322bcb4d8f6b.md': ('0639e32fb2b0d4128e64738030a546bdb1589374',
                                                                                                                         'e2cf470975d1d6f344d3dd788410c911b5d6f9d93fa528709339322bcb4d8f6b',
                                                                                                                         5715),
 'docs/provenance/v5-research-continuations/notes/e40d89c1d65f9053bafc6aea41ba93af0b510586ba188e14ba5a8f6d9a50c71f.md': ('7e33cd9283868e0bce24c38758c0d77c2a190666',
                                                                                                                         'e40d89c1d65f9053bafc6aea41ba93af0b510586ba188e14ba5a8f6d9a50c71f',
                                                                                                                         6541),
 'docs/provenance/v5-research-continuations/notes/f0fe93679a7c062a452bd3b3b2615c886dcdf8b96579af2d1ddd2c17c6df6459.md': ('a9f27e973a15d6cddc4d5ccbc20457a811e21ac9',
                                                                                                                         'f0fe93679a7c062a452bd3b3b2615c886dcdf8b96579af2d1ddd2c17c6df6459',
                                                                                                                         1437),
 'docs/provenance/v5-research-continuations/notes/f7f610f5225df88d97fb6a60f984a7ec976632697e2e3f7854f4777994601d4a.md': ('8ba4cb61febc35bffee4862c0cfa0b0ac67f3bd1',
                                                                                                                         'f7f610f5225df88d97fb6a60f984a7ec976632697e2e3f7854f4777994601d4a',
                                                                                                                         9310)}

    @classmethod
    def setUpClass(cls):
        import os, subprocess
        cls.native = subprocess
        cls.repo = SCRIPT.parents[1]
        cls.env = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
        cls.env.update(GIT_NO_LAZY_FETCH='1',GIT_ALLOW_PROTOCOL='',GIT_NO_REPLACE_OBJECTS='1',
            GIT_TERMINAL_PROMPT='0',GIT_OPTIONAL_LOCKS='0',GIT_CONFIG_NOSYSTEM='1',
            GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_SYSTEM=os.devnull)
        spec=importlib.util.spec_from_file_location('sparse_continuations',SCRIPT)
        cls.v=importlib.util.module_from_spec(spec);spec.loader.exec_module(cls.v)
        cls.resolver=cls.v._source
        common=cls.native.run(['git','rev-parse','--git-common-dir'],cwd=cls.repo,env=cls.env,
            capture_output=True,check=True).stdout.decode().strip()
        cls.object_store=(cls.repo/common/'objects').resolve()
        cls.original_owners=json.loads((cls.repo/cls.OWNER).read_bytes())
        cls.original_cross=json.loads((cls.repo/cls.CROSS).read_bytes())
        cls.current={r['path']:(cls.repo/r['path']).read_bytes() for r in cls.original_owners['source_additions']}
        rows=json.loads((cls.repo/cls.SOURCE_MAP).read_bytes())['sources']
        cls.rows=[r for r in rows if r['path'] in cls.NOTES]
        if len(cls.rows)!=35:raise AssertionError('exact historical source occurrence count differs')

    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.git('-c','init.templateDir=','init','-q')
        (self.root/'.git/objects/info/alternates').write_text(str(self.object_store)+'\n')
        self.owners=deepcopy(self.original_owners);self.cross=deepcopy(self.original_cross)
        existing={r['path'] for r in self.owners['historical_source_bindings']}
        for path,values in self.NOTES.items():
            if path not in existing:
                self.owners['historical_source_bindings'].append(dict(path=path,repository_revision=self.REV,
                    git_blob=values[0],role='historical-source',reading_source='consolidated-information-and-inquiry',basis='scientific-consolidation-review'))
        for key,row in self.cross['sources'].items():
            if row['path'] not in self.NOTES:continue
            for work in self.cross['works']:
                for form in work.get('reading_forms',[]):
                    if form.get('source')==key:form['relationship']='historical-source'
            relation=dict(from_=key)
            relation={'from':key,'to':'consolidated-information-and-inquiry',
                'kind':'logical-content-incorporated-historical-source-retained','basis':'scientific-consolidation-review'}
            if relation not in self.cross['relations']:self.cross['relations'].append(relation)
        for path,body in self.current.items():self.put(path,body)
        self.save();self.git('add','--',*self.current,self.OWNER,self.CROSS)

    def git(self,*args):
        return self.native.run(['git','--no-replace-objects','--literal-pathspecs',*args],
            cwd=self.root,env=self.env,capture_output=True,check=True).stdout

    def put(self,path,body):
        node=self.root/path;node.parent.mkdir(parents=True,exist_ok=True);node.write_bytes(body);node.chmod(0o644)

    def save(self):
        for path,value in ((self.OWNER,self.owners),(self.CROSS,self.cross)):
            self.put(path,(json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())

    def context(self):
        gate=getattr(self.resolver,'require_sparse_prior_context',None)
        self.assertTrue(callable(gate),'finite sparse-prior source context is missing')
        return gate(self.root)

    def test_exact_25_originals_and_35_occurrences_survive_absence(self):
        self.context();before=(self.root/'.git/index').read_bytes()
        for row in self.rows:
            with self.subTest(source=row['id']):
                expected=self.NOTES[row['path']]
                body=self.v.source_bytes(self.root,row)
                self.assertEqual((hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest(),
                    hashlib.sha256(body).hexdigest(),len(body)),expected)
                self.assertFalse((self.root/row['path']).exists())
        self.assertEqual((self.root/'.git/index').read_bytes(),before)

    def test_source_occurrence_identity_cannot_be_relabelled(self):
        self.context();original=self.rows[0];self.v.source_bytes(self.root,original)
        for field,bad in (('id','foreign-source'),('origin','0'*64),('member','different.md'),
            ('original_sha256','0'*64),('original_bytes',0),('sha256','0'*64),('bytes',0),
            ('projection','EXACT'),('derivation',None),('path',self.rows[-1]['path'])):
            with self.subTest(field=field):
                altered=deepcopy(original);altered[field]=bad
                with self.assertRaises(ValueError):self.v.source_bytes(self.root,altered)

    def test_corrupt_present_symlink_mode_and_staged_source_reject(self):
        self.context();row=self.rows[0];path=row['path'];body=self.v.source_bytes(self.root,row)
        node=self.root/path;self.put(path,body+b'changed')
        with self.assertRaises(ValueError):self.v.source_bytes(self.root,row)
        node.unlink();node.symlink_to('unavailable')
        with self.assertRaises(ValueError):self.v.source_bytes(self.root,row)
        node.unlink();self.put(path,body);node.chmod(0o755)
        with self.assertRaises(ValueError):self.v.source_bytes(self.root,row)
        node.unlink();wrong=self.NOTES[self.rows[-1]['path']][0]
        self.git('update-index','--add','--cacheinfo','100644,'+wrong+','+path)
        with self.assertRaises(ValueError):self.v.source_bytes(self.root,row)

    def test_incomplete_duplicate_and_foreign_historical_sets_reject(self):
        self.context();original=deepcopy(self.owners)
        for fault in ('missing','duplicate','extra','wrong-history','wrong-reading'):
            with self.subTest(fault=fault):
                self.owners=deepcopy(original);rows=self.owners['historical_source_bindings']
                item=next(r for r in rows if r['path'] in self.NOTES)
                if fault=='missing':rows.remove(item)
                elif fault=='duplicate':rows.append(deepcopy(item))
                elif fault=='extra':rows.append(dict(item,path='unadmitted-original.md'))
                elif fault=='wrong-history':item['repository_revision']='HEAD'
                else:item['reading_source']='consolidated-common-repair'
                self.save()
                with self.assertRaises(ValueError):self.context()

    def test_primary_and_support_roles_cannot_be_promoted_or_dropped(self):
        self.context();original=deepcopy(self.cross)
        for fault in ('primary-role','primary-support','support-reading','relation','source-hash','new-alias'):
            with self.subTest(fault=fault):
                self.cross=deepcopy(original)
                primary=next(w for w in self.cross['works'] if w['key']=='continuation-strict-width')
                if fault=='primary-role':primary['role']='review'
                elif fault=='primary-support':primary['supporting_source_keys']=[]
                elif fault=='support-reading':primary['reading_forms'].append({'source':'continuation-note-133','relationship':'historical-source'})
                elif fault=='relation':
                    next(r for r in self.cross['relations'] if r.get('from')=='continuation-note-145')['to']='consolidated-common-repair'
                elif fault=='source-hash':self.cross['sources']['continuation-note-145']['sha256']='0'*64
                else:self.cross['sources']['unadmitted-alias']=deepcopy(self.cross['sources']['continuation-note-145'])
                self.save()
                with self.assertRaises(ValueError):self.context()

    def test_current_science_and_review_must_match_their_native_index(self):
        self.context()
        for path in ('mathematics/information-and-inquiry.md','docs/scientific-consolidation-review.md'):
            with self.subTest(path=path):
                body=self.current[path];self.put(path,body+b'changed')
                with self.assertRaises(ValueError):self.context()
                self.put(path,body)
                wrong=self.NOTES[self.rows[0]['path']][0]
                saved=(self.root/'.git/index').read_bytes()
                self.git('update-index','--cacheinfo','100644,'+wrong+','+path)
                with self.assertRaises(ValueError):self.context()
                (self.root/'.git/index').write_bytes(saved);self.context()

    def test_unadmitted_absent_note_has_no_history_fallback(self):
        self.context();row=deepcopy(self.rows[0]);self.v.source_bytes(self.root,row)
        row['path']='docs/provenance/v5-research-continuations/notes/'+'unadmitted-original.md'
        with self.assertRaises(ValueError):self.v.source_bytes(self.root,row)


if __name__=='__main__':unittest.main(verbosity=2)
