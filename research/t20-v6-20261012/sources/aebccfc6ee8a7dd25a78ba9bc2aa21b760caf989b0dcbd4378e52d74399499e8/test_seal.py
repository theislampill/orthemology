"""Integrity-policy mutation controls; these are NOT mathematical/kernel proofs."""
import hashlib,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'handoff'))
from verify_attempt3 import (VerificationError, check_layer, check_statuses,
                            check_test_evidence, strict_loads)

def H(b):return hashlib.sha256(b).hexdigest()
def J(o):return (json.dumps(o,sort_keys=True)+'\n').encode()
def layered(payload):
    m={'files':[{'path':n,'bytes':len(b),'sha256':H(b)} for n,b in sorted(payload.items())],
       'excluded_seal_members':['MANIFEST.json','RECEIPT.json','RECEIPT.json.sha256']}
    mb=J(m);rb=J({'manifest_binding':{'path':'MANIFEST.json','bytes':len(mb),'sha256':H(mb)}})
    return {**payload,'MANIFEST.json':mb,'RECEIPT.json':rb,
            'RECEIPT.json.sha256':(H(rb)+'  RECEIPT.json\n').encode()}

class SealPolicy(unittest.TestCase):
    def test_valid_layer(self):self.assertEqual(check_layer(layered({'x':b'a'}))['payload_members'],1)
    def test_changed_member(self):
        d=layered({'x':b'a'});d['x']=b'b'
        with self.assertRaises(VerificationError):check_layer(d)
    def test_missing_member(self):
        d=layered({'x':b'a'});del d['x']
        with self.assertRaises(VerificationError):check_layer(d)
    def test_extra_member(self):
        d=layered({'x':b'a'});d['extra']=b'bad'
        with self.assertRaises(VerificationError):check_layer(d)
    def test_receipt_change(self):
        d=layered({'x':b'a'});d['RECEIPT.json']+=b' '
        with self.assertRaises(VerificationError):check_layer(d)
    def test_duplicate_json_key(self):
        with self.assertRaises(VerificationError):strict_loads(b'{"a":1,"a":2}')
    def test_nan_json(self):
        with self.assertRaises(VerificationError):strict_loads(b'{"a":NaN}')
    def test_valid_statuses(self):
        d={u:{'terminal_status':('REFUTED_AS_STATED / REPLACEMENT_PROVED' if u=='U10' else 'PARTIAL — EXACT IRREDUCIBLE BLOCKER: exact compiler'),
            'kernel_credit':False} for u in ('U09','U10','U11')}
        self.assertEqual(check_statuses(d),3)
    def test_generic_partial_refused(self):
        d={u:{'terminal_status':'PARTIAL','kernel_credit':False} for u in ('U09','U10','U11')}
        with self.assertRaises(VerificationError):check_statuses(d)
    def test_missing_status_refused(self):
        with self.assertRaises(VerificationError):check_statuses({})
    def test_test_log_zero_exit_not_enough(self):
        stream=b'not actually unittest\n'
        row={'exit_code':0,'stdout':{'path':'out','bytes':0,'sha256':H(b'')},
             'stderr':{'path':'err','bytes':len(stream),'sha256':H(stream)},'test_count':2,
             'source_bindings':{'source.py':{'bytes':1,'sha256':H(b'x')}}}
        with self.assertRaises(VerificationError):check_test_evidence(row,{'out':b'','err':stream,'source.py':b'x'})
    def test_valid_test_log(self):
        stream=b'\nRan 2 tests in 0.001s\n\nOK\n'
        row={'exit_code':0,'stdout':{'path':'out','bytes':0,'sha256':H(b'')},
             'stderr':{'path':'err','bytes':len(stream),'sha256':H(stream)},'test_count':2,
             'source_bindings':{'source.py':{'bytes':1,'sha256':H(b'x')}}}
        self.assertEqual(check_test_evidence(row,{'out':b'','err':stream,'source.py':b'x'}),2)
    def test_test_log_hash_mismatch(self):
        stream=b'\nRan 2 tests in 0.001s\n\nOK\n'
        row={'exit_code':0,'stdout':{'path':'out','bytes':0,'sha256':H(b'')},
             'stderr':{'path':'err','bytes':len(stream),'sha256':H(stream)},'test_count':2,
             'source_bindings':{'source.py':{'bytes':1,'sha256':H(b'x')}}}
        with self.assertRaises(VerificationError):check_test_evidence(row,{'out':b'','err':stream,'source.py':b'y'})

if __name__=='__main__':unittest.main()
