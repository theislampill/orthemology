import hashlib, io, json, os, pathlib, shutil, stat, subprocess, sys, tempfile, unittest, zipfile
SCRIPT=pathlib.Path(__file__).resolve().parent/'verify.py'
def digest(b): return hashlib.sha256(b).hexdigest()
class CollectionTests(unittest.TestCase):
    def setUp(self): self.tmp=tempfile.TemporaryDirectory(); self.root=pathlib.Path(self.tmp.name)/'collection'; self.root.mkdir(); self.out=pathlib.Path(self.tmp.name)/'out'
    def tearDown(self): self.tmp.cleanup()
    def build(self, members=None):
        if members is None: members=[('wrapper/a.txt',b'accepted bytes')]
        zpath=self.root/'part.zip'
        with zipfile.ZipFile(zpath,'w') as z:
            for name,data in members: z.writestr(name,data)
        with zipfile.ZipFile(zpath) as z:
            entries=[{'path':i.filename,'bytes':i.file_size,'sha256':digest(z.read(i)),'directory':i.is_dir()} for i in z.infolist()]
        manifest={'schema':'orthemology.seventh.collection.v1','files':[{'path':'part.zip','bytes':zpath.stat().st_size,'sha256':digest(zpath.read_bytes())}], 'components':[{'id':'part','path':'part.zip','strip_prefix':'wrapper/','entries':entries,'verify_commands':[],'replay':None}]}
        (self.root/'MANIFEST.json').write_text(json.dumps(manifest))
        return manifest
    def runcheck(self,*args): return subprocess.run([sys.executable,*(['-O'] if sys.flags.optimize else []),str(SCRIPT),'--root',str(self.root),*args],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    def reject(self,needle,*args):
        p=self.runcheck(*args); self.assertNotEqual(p.returncode,0,p.stdout); self.assertIn(needle,p.stdout); self.assertFalse(self.out.exists())
    def test_valid_inventory(self): self.build(); p=self.runcheck(); self.assertEqual(p.returncode,0,p.stdout); self.assertIn('VERIFIED',p.stdout)
    def test_fresh_extraction(self):
        self.build(); p=self.runcheck('--extract-to',str(self.out)); self.assertEqual(p.returncode,0,p.stdout); self.assertEqual((self.out/'part/a.txt').read_bytes(),b'accepted bytes')
    def test_archive_digest_corruption(self): self.build(); p=self.root/'part.zip'; p.write_bytes(p.read_bytes()+b'corrupt'); self.reject('hash/size')
    def test_member_hash_corruption(self):
        m=self.build(); m['components'][0]['entries'][0]['sha256']='0'*64; (self.root/'MANIFEST.json').write_text(json.dumps(m)); self.reject('member hash/size')
    def test_crc_corruption_with_rebound_archive_hash(self):
        m=self.build(); p=self.root/'part.zip'; data=p.read_bytes().replace(b'accepted bytes',b'damaged! bytes'); p.write_bytes(data)
        m['files'][0].update(bytes=len(data),sha256=digest(data)); (self.root/'MANIFEST.json').write_text(json.dumps(m)); self.reject('Bad CRC-32')
    def test_duplicate_zip_member(self):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore'); self.build([('wrapper/a',b'a'),('wrapper/a',b'a')])
        self.reject('duplicate member')
    def test_destination_full_path_length(self):
        self.build([('wrapper/'+'a'*200,b'x')]); self.out=pathlib.Path(self.tmp.name)/('b'*80); self.reject('full path length','--extract-to',str(self.out))
    def test_failed_replay_receipt_records_terminal_component_failure(self):
        m=self.build(); m['components'][0]['replay_commands']=[{'argv':['{python}','-c','raise SystemExit(2)']}]
        (self.root/'MANIFEST.json').write_text(json.dumps(m)); output=pathlib.Path(self.tmp.name)/'replay'
        p=self.runcheck('--extract-to',str(self.out),'--replay','part','--out',str(output))
        self.assertNotEqual(p.returncode,0); receipt=json.loads((output/'COLLECTION_REPLAY.json').read_text())
        self.assertEqual(receipt['status'],'FAILED_OR_INCOMPLETE'); self.assertEqual(receipt['components'][0]['status'],'FAILED')
    def test_replay_can_reference_sibling_extraction_root(self):
        m=self.build(); m['components'][0]['replay_commands']=[{'argv':['{python}','-c','import sys; print(sys.argv[1])','{extracted}']}]
        (self.root/'MANIFEST.json').write_text(json.dumps(m)); output=pathlib.Path(self.tmp.name)/'replay'
        p=self.runcheck('--extract-to',str(self.out),'--replay','part','--out',str(output)); self.assertEqual(p.returncode,0,p.stdout)
        self.assertEqual((output/'part/logs/00.log').read_text().strip(),str(self.out))
    def test_exit_zero_with_blocked_terminal_status_is_failure(self):
        program = "import pathlib,sys,json; p=pathlib.Path(sys.argv[1]); p.mkdir(); (p/'RESULT.json').write_text(json.dumps(dict(status='POSITIVE_CLOSURE_BLOCKED')))"
        m=self.build(); m['components'][0]['replay_commands']=[{'argv':['{python}','-c',program,'{out}'],'expect_json':[{'path':'{out}/RESULT.json','field':'status','equals':'COMPLETED_BOUNDED_REPLAY'}]}]
        (self.root/'MANIFEST.json').write_text(json.dumps(m)); output=pathlib.Path(self.tmp.name)/'replay'
        p=self.runcheck('--extract-to',str(self.out),'--replay','part','--out',str(output)); self.assertNotEqual(p.returncode,0,p.stdout); self.assertIn('terminal evidence mismatch',p.stdout)
    def test_terminal_json_success_is_checked(self):
        program = "import pathlib,sys,json; p=pathlib.Path(sys.argv[1]); p.mkdir(); (p/'RESULT.json').write_text(json.dumps(dict(status='COMPLETED_BOUNDED_REPLAY')))"
        m=self.build(); m['components'][0]['replay_commands']=[{'argv':['{python}','-c',program,'{out}'],'expect_json':[{'path':'{out}/RESULT.json','field':'status','equals':'COMPLETED_BOUNDED_REPLAY'}]}]
        (self.root/'MANIFEST.json').write_text(json.dumps(m)); output=pathlib.Path(self.tmp.name)/'replay'
        p=self.runcheck('--extract-to',str(self.out),'--replay','part','--out',str(output)); self.assertEqual(p.returncode,0,p.stdout)
        r=json.loads((output/'COLLECTION_REPLAY.json').read_text()); self.assertEqual(r['components'][0]['commands'][0].get('terminal_evidence',[{}])[0].get('status'),'MATCH')
    def test_optional_archive_argument_is_forwarded_when_supplied(self):
        m=self.build(); m['components'][0]['replay_commands']=[{'argv':['{python}','-c','import sys; print(sys.argv[1:])'],'optional_args':{'mathlib_archive':['--archive','{mathlib_archive}']}}]
        (self.root/'MANIFEST.json').write_text(json.dumps(m)); output=pathlib.Path(self.tmp.name)/'replay'; archive=pathlib.Path(self.tmp.name)/'official.tar.gz'
        p=self.runcheck('--extract-to',str(self.out),'--replay','part','--out',str(output),'--mathlib-archive',str(archive)); self.assertEqual(p.returncode,0,p.stdout)
        self.assertEqual((output/'part/logs/00.log').read_text().strip(),repr(['--archive',str(archive)]))
    def test_optional_archive_argument_is_omitted_when_absent(self):
        m=self.build(); m['components'][0]['replay_commands']=[{'argv':['{python}','-c','import sys; print(sys.argv[1:])'],'optional_args':{'mathlib_archive':['--archive','{mathlib_archive}']}}]
        (self.root/'MANIFEST.json').write_text(json.dumps(m)); output=pathlib.Path(self.tmp.name)/'replay'
        p=self.runcheck('--extract-to',str(self.out),'--replay','part','--out',str(output)); self.assertEqual(p.returncode,0,p.stdout)
        self.assertEqual((output/'part/logs/00.log').read_text().strip(),'[]')
    def test_terminal_json_array_count_and_last_row(self):
        program = "import pathlib,sys,json; p=pathlib.Path(sys.argv[1]); p.mkdir(); (p/'RESULT.json').write_text(json.dumps(dict(runs=[1,dict(id='final',exit_code=1,resource_inconclusive=True)])))"
        m=self.build(); m['components'][0]['replay_commands']=[{'argv':['{python}','-c',program,'{out}'],'expect_json':[{'path':'{out}/RESULT.json','field':'runs.length','equals':2},{'path':'{out}/RESULT.json','field':'runs.-1.id','equals':'final'},{'path':'{out}/RESULT.json','field':'runs.-1.exit_code','equals':1},{'path':'{out}/RESULT.json','field':'runs.-1.resource_inconclusive','equals':True}]}]
        (self.root/'MANIFEST.json').write_text(json.dumps(m)); output=pathlib.Path(self.tmp.name)/'replay'
        p=self.runcheck('--extract-to',str(self.out),'--replay','part','--out',str(output)); self.assertEqual(p.returncode,0,p.stdout)
    def test_existing_replay_output_is_preserved(self):
        m=self.build(); m['components'][0]['replay_commands']=[{'argv':['{python}','-c','raise SystemExit(0)']}]
        (self.root/'MANIFEST.json').write_text(json.dumps(m)); output=pathlib.Path(self.tmp.name)/'replay'; output.mkdir(); (output/'RESULT.json').write_text('existing sentinel')
        p=self.runcheck('--extract-to',str(self.out),'--replay','part','--out',str(output)); self.assertNotEqual(p.returncode,0); self.assertIn('already exists',p.stdout)
        self.assertEqual((output/'RESULT.json').read_text(),'existing sentinel'); self.assertFalse((output/'COLLECTION_REPLAY.json').exists())
    def test_extra_empty_directory_is_rejected(self):
        self.build(); (self.root/'unexpected-empty-directory').mkdir(); self.reject('inventory mismatch')
    def replay_case(self, commands, members=None, copy=False, sibling=False, timeout=4):
        m=self.build(members); m['components'][0]['replay_commands']=commands; m['components'][0]['replay_workspace_copy']=copy
        if sibling:
            import copy as copying
            shutil.copyfile(self.root/'part.zip',self.root/'other.zip'); f=dict(m['files'][0]); f['path']='other.zip'; m['files'].append(f)
            c=copying.deepcopy(m['components'][0]); c.update(id='other',path='other.zip',replay_commands=[]); m['components'].append(c)
        (self.root/'MANIFEST.json').write_text(json.dumps(m)); output=pathlib.Path(self.tmp.name)/'replay'
        try:
            p=subprocess.run([sys.executable,*(['-O'] if sys.flags.optimize else []),str(SCRIPT),'--root',str(self.root),'--extract-to',str(self.out),'--replay','part','--out',str(output)],capture_output=True,text=True,timeout=timeout)
        except subprocess.TimeoutExpired:
            self.fail('terminal evidence handling blocked instead of rejecting')
        return p,output
    def test_replay_rejects_mutated_extracted_input(self):
        p,_=self.replay_case([{'argv':['{python}','-c',"from pathlib import Path; Path('a.txt').write_text('modified')"]}]); self.assertNotEqual(p.returncode,0); self.assertIn('extracted input',p.stderr)
    def test_replay_rejects_mutated_unselected_sibling(self):
        p,_=self.replay_case([{'argv':['{python}','-c',"from pathlib import Path; import sys; Path(sys.argv[1]).write_text('modified')",'{extracted}/other/a.txt']}],sibling=True); self.assertNotEqual(p.returncode,0); self.assertIn('extracted input',p.stderr)
    def test_copied_terminal_receipt_cannot_substitute_for_new_run(self):
        p,_=self.replay_case([{'argv':['{python}','-c','pass'],'expect_json':[{'path':'{build}/proof.json','field':'status','equals':'PASS'}]}],members=[('wrapper/a.txt',b'original'),('wrapper/proof.json',b'{"status":"PASS"}')],copy=True)
        self.assertNotEqual(p.returncode,0); self.assertIn('terminal evidence',p.stderr)
    def test_strip_prefix_cannot_strip_a_file_to_empty(self):
        m=self.build();m['components'][0]['strip_prefix']='wrapper/a.txt';(self.root/'MANIFEST.json').write_text(json.dumps(m));self.reject('strip prefix')
    @unittest.skipUnless(hasattr(os,'mkfifo'),'POSIX named-pipe control')
    def test_fifo_terminal_evidence_rejected_without_blocking(self):
        p,_=self.replay_case([{'argv':['{python}','-c',"from pathlib import Path; import sys,os; p=Path(sys.argv[1]); p.mkdir(); os.mkfifo(p/'proof.json')",'{out}'],'expect_json':[{'path':'{out}/proof.json','field':'status','equals':'PASS'}]}],timeout=2)
        self.assertNotEqual(p.returncode,0); self.assertIn('regular',p.stderr)
    def test_terminal_parent_symlink_cannot_redirect_to_inputs(self):
        p,_=self.replay_case([{'argv':['{python}','-c',"from pathlib import Path; import sys; Path(sys.argv[1]).symlink_to(Path.cwd(),target_is_directory=True)",'{out}'],'expect_json':[{'path':'{out}/proof.json','field':'status','equals':'PASS'}]}],members=[('wrapper/a.txt',b'original'),('wrapper/proof.json',b'{"status":"PASS"}')])
        self.assertNotEqual(p.returncode,0); self.assertIn('symlink',p.stderr); self.assertEqual((self.out/'part/proof.json').read_bytes(),b'{"status":"PASS"}')
    def test_timeout_keeps_partial_diagnostics_and_failed_command_record(self):
        p,output=self.replay_case([{'argv':['{python}','-c',"import time; print('before-timeout-marker',flush=True); time.sleep(10)"],'timeout_seconds':0.2}])
        self.assertNotEqual(p.returncode,0); log=output/'part/logs/00.log'; self.assertTrue(log.is_file()); self.assertIn('before-timeout-marker',log.read_text())
        receipt=json.loads((output/'COLLECTION_REPLAY.json').read_text()); command=receipt['components'][0]['commands'][0]
        self.assertEqual(command['status'],'TIMEOUT');self.assertEqual(command['log_sha256'],digest(log.read_bytes()));self.assertTrue(command['resource_inconclusive'])
    def test_staging_path_length_is_checked_too(self):
        self.out=pathlib.Path(self.tmp.name)/'z'
        available=240-len(str(self.out/'part'))-1
        self.build([('wrapper/'+'a'*available,b'x')]);self.reject('staging path length','--extract-to',str(self.out))
    def test_missing_file(self): self.build(); (self.root/'part.zip').unlink(); self.reject('inventory mismatch')
    def test_extra_file(self): self.build(); (self.root/'extra.txt').write_text('extra'); self.reject('inventory mismatch')
    def test_symlink_file(self): self.build(); (self.root/'part.zip').unlink(); (self.root/'part.zip').symlink_to('/tmp/anywhere'); self.reject('symlink')
    def test_traversal_member(self): self.build([('../escape',b'x')]); self.reject('unsafe path','--extract-to',str(self.out))
    def test_absolute_member(self): self.build([('/escape',b'x')]); self.reject('unsafe path')
    def test_backslash_member(self): self.build([('wrapper\\escape',b'x')]); self.reject('unsafe path')
    def test_drive_member(self): self.build([('C:/escape',b'x')]); self.reject('unsafe path')
    def test_reserved_member(self): self.build([('wrapper/CON.txt',b'x')]); self.reject('Windows reserved')
    def test_trailing_dot_member(self): self.build([('wrapper/name.',b'x')]); self.reject('unsafe path')
    def test_casefold_file_collision(self): self.build([('wrapper/A.txt',b'a'),('wrapper/a.txt',b'b')]); self.reject('casefold collision')
    def test_casefold_directory_collision(self): self.build([('wrapper/A/one.txt',b'a'),('wrapper/a/two.txt',b'b')]); self.reject('casefold collision')
    def test_file_directory_conflict(self): self.build([('wrapper/a',b'a'),('wrapper/a/b',b'b')]); self.reject('file/directory conflict')
    def test_zip_symlink(self):
        info=zipfile.ZipInfo('wrapper/link'); info.create_system=3; info.external_attr=(stat.S_IFLNK|0o777)<<16; self.build([(info,b'../outside')]); self.reject('symlink')
    def test_zip_device(self):
        info=zipfile.ZipInfo('wrapper/device'); info.create_system=3; info.external_attr=(stat.S_IFCHR|0o600)<<16; self.build([(info,b'')]); self.reject('nonregular')
    def test_long_windows_relative_path(self): self.build([('wrapper/'+'a'*241,b'x')]); self.reject('path length')
    def test_existing_destination_not_overwritten(self):
        self.build(); self.out.mkdir(); (self.out/'keep').write_text('keep'); p=self.runcheck('--extract-to',str(self.out)); self.assertNotEqual(p.returncode,0); self.assertIn('already exists',p.stdout); self.assertEqual((self.out/'keep').read_text(),'keep')
    def test_manifest_digest_rejection(self): self.build(); self.reject('manifest digest','--manifest-sha256','0'*64)
    def test_wrong_component_inventory(self):
        m=self.build(); m['components'][0]['entries']=[]; (self.root/'MANIFEST.json').write_text(json.dumps(m)); self.reject('member inventory')
    def test_strip_prefix_mismatch(self): self.build([('other/a.txt',b'x')]); self.reject('strip prefix')
    def test_manifest_traversal(self):
        m=self.build(); m['files'][0]['path']='../part.zip'; (self.root/'MANIFEST.json').write_text(json.dumps(m)); self.reject('unsafe path')
if __name__=='__main__': unittest.main(verbosity=2)
