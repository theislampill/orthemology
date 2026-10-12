"""Independent finite handoff checks using manually authored metadata/CAS fixtures."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import sysconfig
import tempfile
import unittest
sys.dont_write_bytecode = True
TOOLS = Path(__file__).resolve().parent.parent / 'final_handoff_tools'
def load(name):
    spec = importlib.util.spec_from_file_location(name, TOOLS / (name + '.py'))
    module = importlib.util.module_from_spec(spec); sys.modules[name] = module; spec.loader.exec_module(module)
    return module
v = load('verify_handoff'); b = load('prepare_handoff')
def enc(x): return (json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(',', ':')) + '\n').encode()
def digest(x): return hashlib.sha256(x).hexdigest()
def path(h): return 'authored_objects/' + h[:2] + '/' + h
class IndependentControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); self.source = self.root/'source'; self.source.mkdir(); self.out = self.root/'out'
        self.body = b'raise RuntimeError("RETAINED_SOURCE_RAN")\n'; self.h = digest(self.body)
        self.tool = (TOOLS/'verify_handoff.py').read_bytes(); self.th = digest(self.tool)
        self.missing = 'd'*64
        self.plan = {'schema':'t20-v6-explicit-selection-plan-v1','state':'PLAN_ONLY_NOT_ASSEMBLED',
            'audience':'owner_private_handoff','destination':'finite-v6','decision_reference':'independent-review',
            'input_digests':{'lookup_sha256':'a'*64,'v5_index_sha256':'b'*64,'exclusions_sha256':'c'*64},
            'baseline':{'archive_sha256':'e'*64,'policy':'separate_unchanged_owner_checkpoint','whole_archive_publication_selected':False},
            'objects':[],'views':[], 'replay_blockers':[{'consumer':self.h,'dependency':self.missing,'reason':'required_dependency_not_delivered'}],
            'source_execution_selected':False,'future_preflight':[]}
        for h, raw, view, deps in [(self.h,self.body,'packet/data.py',[self.missing]),(self.th,self.tool,'tools/verify_handoff.py',[])]:
            self.plan['objects'].append({'sha256':h,'action':'include','reviewed_digest':h,'current_path_digest':h,
                'scope_status':'source-only','exclusion_categories':[],'role':'authored_code','required_dependencies':deps,
                'eligibility_basis':'reviewed_owner_authored','bytes':len(raw),'provider':{'kind':'authored_annex_object','path':path(h)}})
            self.plan['views'].append({'path':view,'sha256':h})
            fp=self.source/path(h);fp.parent.mkdir(parents=True,exist_ok=True);fp.write_bytes(raw)
        self.plan['objects'].append({'sha256':self.missing,'action':'identity_only','reviewed_digest':self.missing,
            'current_path_digest':None,'scope_status':'unavailable','exclusion_categories':[],'availability':'exact_snapshot_unavailable'})
        self.plan['views'].sort(key=lambda r:r['path'])
        self.write_metadata(self.source)
        self.declaration = {'schema':'t20-v6-curated-entry-declaration-v1','entries':[
            {'path':'READ_ME.py','source_view':'packet/data.py','sha256':self.h},
            {'path':'tools/verify_handoff.py','source_view':'tools/verify_handoff.py','sha256':self.th}]}
    def write_metadata(self, root):
        ph=digest(enc(self.plan)); objs=sorted([o for o in self.plan['objects'] if o['action']=='include'],key=lambda o:o['sha256'])
        vm={'schema':'t20-v6-selected-source-view-map-v1','plan_sha256':ph,
            'objects':[{'sha256':o['sha256'],'bytes':o['bytes'],'path':path(o['sha256'])} for o in objs],'views':self.plan['views']}
        rec={'schema':'t20-v6-selected-source-materialisation-v1','state':'MATERIALISED_SOURCE_ONLY','plan_sha256':ph,
            'view_map_sha256':digest(enc(vm)),'object_count':len(objs),'view_count':len(vm['views']),
            'total_unique_bytes':sum(o['bytes'] for o in objs),'source_execution_selected':False}
        for name,value in [('PUBLIC_PLAN.json',self.plan),('VIEW_MAP.json',vm),('MATERIALISATION.json',rec)]: (root/name).write_bytes(enc(value))
    def snapshot(self,root):
        return {str(p.relative_to(root)):(p.stat().st_mtime_ns, p.read_bytes() if p.is_file() else None) for p in root.rglob('*')}
    def stage(self): return b.prepare(self.source,self.declaration,self.out,[self.source])
    def rebind_manifest(self):
        mf=json.loads((self.out/'PACKAGE_MANIFEST.json').read_bytes())
        for row in mf['files']:
            raw=(self.out/row['path']).read_bytes(); row.update(sha256=digest(raw),bytes=len(raw))
        for key,name in [('plan_sha256','PUBLIC_PLAN.json'),('view_map_sha256','VIEW_MAP.json'),('materialisation_sha256','MATERIALISATION.json')]:
            mf[key]=digest((self.out/name).read_bytes())
        (self.out/'PACKAGE_MANIFEST.json').write_bytes(enc(mf))
    def test_manual_fixture_cli_read_only_normal_and_optimized(self):
        src=self.snapshot(self.source); report=self.stage(); before=self.snapshot(self.out)
        self.assertEqual(report['replay_blocker_count'],1)
        for mode in ([],['-O']):
            r=subprocess.run([sys.executable,*mode,'tools/verify_handoff.py','.','--expected-manifest-sha256',report['manifest_sha256']],cwd=self.out,capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr+r.stdout); self.assertEqual(json.loads(r.stdout)['object_count'],2)
        self.assertEqual(self.snapshot(self.source),src);self.assertEqual(self.snapshot(self.out),before)
    def test_rebound_dropped_blocker_rejected(self):
        self.stage();self.plan['replay_blockers']=[];self.write_metadata(self.out);self.rebind_manifest()
        with self.assertRaisesRegex(ValueError,'replay blocker mismatch'):v.verify(self.out)
    def test_rebound_missing_dependency_disposition_rejected(self):
        self.stage();self.plan['objects']=[o for o in self.plan['objects'] if o['sha256'] != self.missing]
        self.write_metadata(self.out);self.rebind_manifest()
        with self.assertRaisesRegex(ValueError,'missing explicit dependency disposition'):v.verify(self.out)
    def test_rebound_boolean_source_size_rejected(self):
        self.stage();next(o for o in self.plan['objects'] if o['sha256']==self.h)['bytes']=True
        self.write_metadata(self.out);self.rebind_manifest()
        with self.assertRaisesRegex(ValueError,'invalid source size'):v.verify(self.out)
    def test_rebound_changed_curated_source_identity_rejected(self):
        self.stage();mf=json.loads((self.out/'PACKAGE_MANIFEST.json').read_bytes());mf['curated_entries'][0]['sha256']=self.th
        (self.out/'PACKAGE_MANIFEST.json').write_bytes(enc(mf))
        with self.assertRaisesRegex(ValueError,'curated source view identity mismatch'):v.verify(self.out)
    def test_fresh_stage_disjoint_and_byte_preserving(self):
        before=self.snapshot(self.source)
        for dest in [self.source/'new', self.root/'SOURCE'/'new']:
            with self.assertRaises(ValueError):b.prepare(self.source,self.declaration,dest,[self.source])
            self.assertFalse(dest.exists())
        self.assertEqual(before,self.snapshot(self.source))
    def test_hardlinked_source_is_copied_not_retained_as_link(self):
        extra=self.root/'preserved';os.link(self.source/path(self.h),extra);self.stage()
        self.assertNotEqual((self.out/path(self.h)).stat().st_ino, extra.stat().st_ino)
        self.assertNotEqual((self.out/'READ_ME.py').stat().st_ino, (self.out/path(self.h)).stat().st_ino)
    def test_added_shadow_modules_do_not_run(self):
        self.stage()
        for name in ['__future__','argparse','json','pathlib','re','stat','unicodedata','hashlib']:
            (self.out/'tools'/f'{name}.py').write_text('raise RuntimeError("UNTRUSTED_SHADOW_EXECUTED")\n')
        for mode in ([],['-O']):
            r=subprocess.run([sys.executable,*mode,'tools/verify_handoff.py','.'],cwd=self.out,capture_output=True,text=True)
            self.assertNotEqual(r.returncode,0);self.assertNotIn('UNTRUSTED_SHADOW_EXECUTED',r.stdout+r.stderr)
        self.assertFalse((self.out/'tools/__pycache__').exists())
    def test_builder_cli_excludes_adjacent_modules_and_preserves_inputs(self):
        helpers=self.root/'helpers';helpers.mkdir()
        for name in ['prepare_handoff.py','verify_handoff.py']:shutil.copyfile(TOOLS/name,helpers/name)
        for name in ['__future__','argparse','json','pathlib','hashlib','importlib']:
            (helpers/(name+'.py')).write_text('raise RuntimeError("UNTRUSTED_BUILDER_IMPORT_EXECUTED")\n')
        declaration=self.root/'curated.json';declaration.write_bytes(enc(self.declaration))
        before=self.snapshot(self.source);helper_before=self.snapshot(helpers)
        for i,mode in enumerate(([],['-O'])):
            output=self.root/('cli-output-'+str(i))
            r=subprocess.run([sys.executable,*mode,'prepare_handoff.py','--source-package',str(self.source),
                '--curated',str(declaration),'--destination',str(output),'--protected-root',str(self.source)],
                cwd=helpers,capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stdout+r.stderr)
            self.assertEqual(json.loads(r.stdout)['state'],'VERIFIED_SOURCE_ONLY_HANDOFF')
            self.assertEqual(v.verify(output)['object_count'],2)
        self.assertEqual(self.snapshot(self.source),before);self.assertEqual(self.snapshot(helpers),helper_before)
    def test_interpreter_prefix_package_shadow_modules_do_not_run(self):
        home=self.root/'python-home';(home/'lib').mkdir(parents=True)
        (home/'lib'/f'python{sys.version_info.major}.{sys.version_info.minor}').symlink_to(sysconfig.get_path('stdlib'),target_is_directory=True)
        pkg=home/'handoff';(pkg/'tools').mkdir(parents=True);shutil.copyfile(TOOLS/'verify_handoff.py',pkg/'tools/verify_handoff.py')
        (pkg/'tools/json.py').write_text('raise RuntimeError("UNTRUSTED_PREFIX_MODULE_EXECUTED")\n')
        env=os.environ.copy();env['PYTHONHOME']=str(home);env.pop('PYTHONPATH',None)
        for mode in ([],['-O']):
            r=subprocess.run([sys.executable,*mode,'tools/verify_handoff.py','.'],cwd=pkg,env=env,capture_output=True,text=True)
            self.assertNotEqual(r.returncode,0);self.assertNotIn('UNTRUSTED_PREFIX_MODULE_EXECUTED',r.stdout+r.stderr)
    def test_interpreter_prefix_pythonpath_shadow_modules_do_not_run(self):
        home=self.root/'python-home';(home/'lib').mkdir(parents=True)
        (home/'lib'/f'python{sys.version_info.major}.{sys.version_info.minor}').symlink_to(sysconfig.get_path('stdlib'),target_is_directory=True)
        pkg=home/'handoff';(pkg/'tools').mkdir(parents=True);shutil.copyfile(TOOLS/'verify_handoff.py',pkg/'tools/verify_handoff.py')
        (pkg/'data').mkdir();(pkg/'data/json.py').write_text('raise RuntimeError("UNTRUSTED_PYTHONPATH_MODULE_EXECUTED")\n')
        env=os.environ.copy();env['PYTHONHOME']=str(home);env['PYTHONPATH']=str(pkg/'data')
        for mode in ([],['-O']):
            r=subprocess.run([sys.executable,*mode,'tools/verify_handoff.py','.'],cwd=pkg,env=env,capture_output=True,text=True)
            self.assertNotEqual(r.returncode,0);self.assertNotIn('UNTRUSTED_PYTHONPATH_MODULE_EXECUTED',r.stdout+r.stderr)
if __name__=='__main__':unittest.main()
