"""Transport-integrity tests on synthetic fixtures, not mathematical checks."""
from __future__ import annotations
import hashlib,json,tempfile,unittest,warnings,zipfile
from pathlib import Path
from verify_checkpoint import verify_checkpoint

def H(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def J(x:object)->bytes:return (json.dumps(x,sort_keys=True,indent=2)+'\n').encode()
SEALS=['MANIFEST.json','RECEIPT.json','RECEIPT.json.sha256']

class CheckpointVerifierTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        payload={'INDEX.md':b'fixture\n','empty.stderr':b''}
        manifest=J({'algorithm':'sha256','excluded_seal_members':SEALS,
          'files':[{'path':n,'bytes':len(b),'sha256':H(b)} for n,b in payload.items()],
          'payload_file_count':2,'payload_bytes':sum(map(len,payload.values()))})
        receipt=J({'manifest_binding':{'path':'MANIFEST.json','bytes':len(manifest),'sha256':H(manifest)}})
        self.entries=list(payload.items())+[
          ('MANIFEST.json',manifest),('RECEIPT.json',receipt),
          ('RECEIPT.json.sha256',(H(receipt)+'  RECEIPT.json\n').encode())]
    def write(self,entries=None):
        z=self.root/'fixture.zip'
        with warnings.catch_warnings():
            warnings.simplefilter('ignore',UserWarning)
            with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
                for n,b in (self.entries if entries is None else entries):f.writestr(n,b)
        side=self.root/'fixture.zip.sha256';side.write_text(H(z.read_bytes())+'  fixture.zip\n')
        return z,side
    def check(self,entries=None):
        p,s=self.write(entries);return verify_checkpoint(p,s)
    def test_valid_complete_coverage_including_empty_stream(self):
        r=self.check();self.assertEqual(r['status'],'PASS');self.assertEqual(r['members_verified'],5)
    def test_payload_tamper_rejected_even_with_new_outer_digest(self):
        entries=[(n,b'changed' if n=='INDEX.md' else b) for n,b in self.entries]
        self.assertEqual(self.check(entries)['status'],'FAIL')
    def test_manifest_tamper_rejected(self):
        entries=[(n,b+b' ' if n=='MANIFEST.json' else b) for n,b in self.entries]
        self.assertEqual(self.check(entries)['status'],'FAIL')
    def test_receipt_tamper_rejected(self):
        entries=[(n,b+b' ' if n=='RECEIPT.json' else b) for n,b in self.entries]
        self.assertEqual(self.check(entries)['status'],'FAIL')
    def test_unexpected_member_rejected(self):
        self.assertEqual(self.check(self.entries+[('unexpected',b'x')])['status'],'FAIL')
    def test_missing_member_rejected(self):
        self.assertEqual(self.check([(n,b) for n,b in self.entries if n!='INDEX.md'])['status'],'FAIL')
    def test_duplicate_member_rejected(self):
        self.assertEqual(self.check(self.entries+[('INDEX.md',b'fixture\n')])['status'],'FAIL')
    def test_parent_traversal_rejected(self):
        self.assertEqual(self.check(self.entries+[('../escape',b'x')])['status'],'FAIL')
    def test_wrong_outer_digest_rejected(self):
        p,s=self.write();s.write_text('0'*64+'  fixture.zip\n')
        self.assertEqual(verify_checkpoint(p,s)['status'],'FAIL')
    def test_truncated_zip_rejected(self):
        p,s=self.write();p.write_bytes(p.read_bytes()[:-40]);s.write_text(H(p.read_bytes())+'  fixture.zip\n')
        self.assertEqual(verify_checkpoint(p,s)['status'],'FAIL')

if __name__=='__main__':unittest.main(verbosity=2)
