"""Fresh U03 exporter input-shape counterexample; not a kernel result."""
import os,sys,unittest
sys.path.insert(0,os.environ['P03_SOURCE'])
import proof_export as p
from boundaries import Rejection,dump_json
class ExportRows(unittest.TestCase):
    def test_malformed_rows_refuse_in_the_declared_boundary_language(self):
        for row in [None,[],['name'],['name',b'{}','extra']]:
            with self.subTest(row=repr(row)):
                try:p.module([row])
                except Rejection:continue
                except Exception as ex:self.fail(f'P03-U03-CE02: escaped {type(ex).__name__}: {ex}')
                else:self.fail('P03-U03-CE02: malformed row accepted')
    def test_valid_row_still_emits_uncompiled_certificate(self):
        raw=dump_json({'rule':'i','A':['bottom']})
        for row in [('P03Positive',raw),['P03Positive',raw]]:
            text=p.module([row])
            self.assertIn('theorem P03Positive_erasure',text)
            self.assertIn('theorem P03Positive_type',text)
            self.assertIn('UNCOMPILED',text)
if __name__=='__main__':unittest.main(verbosity=2)
