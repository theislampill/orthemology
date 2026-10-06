"""Exercise continuation effects with only the process/environment boundary doubled."""
import copy,hashlib,importlib.util,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class CoveringExecutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cc=module('covering_execution_helper',ROOT/'scripts/v5_covering_continuation.py')
        cls.a=module('covering_execution_adapter',ROOT/'scripts/replay_v5_successors.py')

    def context(self):
        self.assertTrue(callable(getattr(self.cc,'execute',None)),'Covering-only executor has not been implemented')
        p=os.environ.get('V5_COVERING_CONTINUATION_CONTEXT')
        if not p:self.skipTest('Private exact custody context not supplied')
        c=json.loads(Path(p).read_text());f=json.loads(Path(c['fragment']).read_text());c['suite']=json.loads(Path(c['suite']).read_text())
        c.update(sources={r['id']:r for r in f['sources']},reviews={r['id']:r for r in f['reviews']})
        c['plan']=self.a.validate_suite(c['suite'],c['sources'],Path(c['root']))
        c['old']=json.loads((Path(c['prior'])/'RECEIPT.json').read_text())
        return c

    def call(self,c,out):return self.cc.execute(c['suite'],c['sources'],Path(c['root']),Path(c['prior']),out,c['tools'],c['inputs'],reviews=c['reviews'],adapter=self.a)

    def fake_environment(self,c,damage=False):
        e=c['old']['replay_evidence'];fingerprints=copy.deepcopy(e['tool_fingerprints'])
        if damage:fingerprints['lean']['executable_sha256']='0'*64
        return ({k:Path(v)for k,v in c['tools'].items()if k!='mathlib'},fingerprints,copy.deepcopy(e['dependency_checks']),
                {'PATH':os.environ.get('PATH','')},{k:hashlib.sha256(Path(v).read_bytes()).hexdigest()for k,v in c['inputs'].items()})

    def test_successful_boundary_calls_only_one_audit_and_keeps_old_tree(self):
        c=self.context();calls=[];old_bytes=(Path(c['prior'])/'RECEIPT.json').read_bytes();pins=self.cc.data(self.a)
        def process(argv,cwd,env,log,timeout):
            calls.append([str(x)for x in argv]);text=''
            for row in c['plan']['targets'].values():
                n=row['name'];text+=f"V5_BEGIN {n}\n{n} : True\n'{n}' does not depend on any axioms\nV5_OWNER {n} {row['module']}\nV5_SAFE {n} 1 []\nV5_END {n}\n"
            Path(log).write_text(text);now=self.a.utc()
            return {'terminal':'COMPLETED','exit_code':0,'started_at':now,'ended_at':self.a.utc(),'log_sha256':hashlib.sha256(text.encode()).hexdigest()}
        with tempfile.TemporaryDirectory()as d,patch.object(self.a,'_verify_environment',return_value=self.fake_environment(c)),patch.object(self.a,'_ac_exec_caches',return_value=(pins['official_cache_measurements'],{})),patch.object(self.a,'run_process',side_effect=process):
            out=Path(d)/'fresh';r=self.call(c,out)
            self.assertEqual(len(calls),1);self.assertEqual(calls[0][1],'-j1');self.assertNotIn('-o',calls[0])
            self.assertTrue((out/'AUDIT_PROCESS.json').is_file());self.assertTrue((out/'RECEIPT.json').is_file())
            self.assertEqual(r['outcome'],'QUALIFIED_DECLARED_SUITE');self.assertEqual((Path(c['prior'])/'RECEIPT.json').read_bytes(),old_bytes)

    def test_precondition_environment_failure_cannot_launch_audit(self):
        c=self.context()
        with tempfile.TemporaryDirectory()as d,patch.object(self.a,'_verify_environment',return_value=self.fake_environment(c,True)),patch.object(self.a,'run_process',side_effect=AssertionError('ANY_PROCESS_FORBIDDEN'))as proc:
            out=Path(d)/'fresh'
            with self.assertRaises(ValueError):self.call(c,out)
            self.assertEqual(proc.call_count,0);self.assertTrue((out/'REFUSAL.json').is_file());self.assertFalse((out/'RECEIPT.json').exists())

    def test_foreign_cache_fails_before_audit(self):
        c=self.context();pins=self.cc.data(self.a);rows=copy.deepcopy(pins['official_cache_measurements']);rows[0]['file_count']=1
        with tempfile.TemporaryDirectory()as d,patch.object(self.a,'_verify_environment',return_value=self.fake_environment(c)),patch.object(self.a,'_ac_exec_caches',return_value=(rows,{})),patch.object(self.a,'run_process',side_effect=AssertionError('ANY_PROCESS_FORBIDDEN'))as proc:
            with self.assertRaises(ValueError):self.call(c,Path(d)/'fresh')
            self.assertEqual(proc.call_count,0)

    def test_interrupted_audit_retains_terminal_and_does_not_retry(self):
        c=self.context();pins=self.cc.data(self.a)
        def process(argv,cwd,env,log,timeout):
            Path(log).write_bytes(b'');now=self.a.utc()
            return {'terminal':'INTERRUPTED','exit_code':None,'started_at':now,'ended_at':now,'log_sha256':hashlib.sha256(b'').hexdigest()}
        with tempfile.TemporaryDirectory()as d,patch.object(self.a,'_verify_environment',return_value=self.fake_environment(c)),patch.object(self.a,'_ac_exec_caches',return_value=(pins['official_cache_measurements'],{})),patch.object(self.a,'run_process',side_effect=process)as proc:
            out=Path(d)/'fresh';r=self.call(c,out)
            self.assertEqual(proc.call_count,1);self.assertEqual(r['outcome'],'RESOURCE_INCONCLUSIVE');self.assertEqual(r['proof_scope'],'NONE')
            self.assertEqual(json.loads((out/'AUDIT_PROCESS.json').read_text())['terminal'],'INTERRUPTED')

    def test_post_audit_environment_drift_preserves_output_but_writes_no_qualified_receipt(self):
        c=self.context();pins=self.cc.data(self.a)
        def process(argv,cwd,env,log,timeout):
            Path(log).write_bytes(b'error: fixture failure');now=self.a.utc()
            return {'terminal':'COMPLETED','exit_code':1,'started_at':now,'ended_at':now,'log_sha256':hashlib.sha256(Path(log).read_bytes()).hexdigest()}
        with tempfile.TemporaryDirectory()as d,patch.object(self.a,'_verify_environment',side_effect=[self.fake_environment(c),self.fake_environment(c,True)]),patch.object(self.a,'_ac_exec_caches',return_value=(pins['official_cache_measurements'],{})),patch.object(self.a,'run_process',side_effect=process)as proc:
            out=Path(d)/'fresh'
            with self.assertRaises(ValueError):self.call(c,out)
            self.assertEqual(proc.call_count,1);self.assertTrue((out/'AUDIT_PROCESS.json').is_file());self.assertTrue((out/'logs/target-audit.log').is_file())
            refusal=json.loads((out/'REFUSAL.json').read_text());self.assertEqual(refusal['audit_process']['terminal'],'COMPLETED');self.assertEqual(refusal['audit_process']['exit_code'],1)
            self.assertFalse((out/'RECEIPT.json').exists())

if __name__=='__main__':unittest.main(verbosity=2)
