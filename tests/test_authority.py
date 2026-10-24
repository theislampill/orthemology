"""Source-owned scientific projection tests, including unsupported status changes."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from source_provider import SourceProvider
import authority

ROOT=Path(__file__).resolve().parents[1]

class ScientificAuthority(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.provider=SourceProvider(ROOT,offline=True)
        cls.works,cls.records=authority.load(ROOT)

    def test_every_original_work_claim_binding_and_avenue_preserved(self):
        result=authority.validate(self.provider,self.works,self.records,include_views=True)
        self.assertEqual(result["works"],448)
        self.assertEqual(result["bindings"],1620)
        self.assertEqual(result["claims"],34)
        self.assertEqual(result["avenues"],12)

    def test_unsupported_status_promotion_rejected(self):
        works=copy.deepcopy(self.works)
        works[0]["source_owned_status"]["catalogue_review_status"]="ACCEPTED AND FORMALLY PROVED"
        with self.assertRaises(Exception): authority.validate(self.provider,works,self.records)

    def test_empty_result_identifier_is_not_ground_for_dropping_a_work(self):
        works=copy.deepcopy(self.works)
        index=next(i for i,w in enumerate(works) if not w["original_record"].get("existing_result_ids"))
        del works[index]
        with self.assertRaises(Exception): authority.validate(self.provider,works,self.records)

    def test_derivation_converges(self):
        one=authority.generate(self.provider)
        two=authority.generate(self.provider)
        self.assertEqual(one,two)
        self.assertEqual(authority.render_views(*one),authority.render_views(*two))

    def test_changed_statement_rejected(self):
        records=copy.deepcopy(self.records)
        claim=next(x for x in records if x.get("record_type")=="source_owned_claim")
        claim["original_record"]["exact_statement"]="The opposite is proved without assumptions."
        with self.assertRaises(Exception): authority.validate(self.provider,self.works,records)

if __name__=="__main__":
    unittest.main()
