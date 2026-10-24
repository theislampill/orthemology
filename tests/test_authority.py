"""Source-owned scientific projection tests, including unsupported status changes."""
import copy
import os
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from source_provider import SourceProvider
import authority

ROOT=Path(os.environ.get("ORTHEMOLOGY_TEST_REPO",Path(__file__).resolve().parents[1]))

class ScientificAuthority(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.provider=SourceProvider(ROOT,cache=os.environ.get("ORTHEMOLOGY_TEST_CACHE"),offline=True,git_repo=False)
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


    def test_claim_readings_include_all_nested_owned_sha_references(self):
        _, records=authority.generate(self.provider)
        claims=[r for r in records if r.get("record_type")=="source_owned_claim"]
        self.assertEqual(len(claims),34)
        def digests(obj):
            if isinstance(obj,dict):
                return ({obj["sha256"]} if "sha256" in obj else set()).union(*(digests(v) for v in obj.values()))
            if isinstance(obj,list):return set().union(*(digests(v) for v in obj))
            return set()
        for claim in claims:
            self.assertEqual({s["original_sha256"] for s in claim["sources"]},digests(claim["original_record"]))
            self.assertTrue(all(s.get("owner_pointers") for s in claim["sources"]))
        private=next(r for r in claims if r["id"]=="pure-perfection-eligibility-and-participant-sensitive-ends")
        primary=next(s for s in private["sources"] if s["role"]=="primary")
        self.assertEqual(primary["availability"],"identity_only")
        self.assertNotIn("path",primary)

    def test_selector_exact_scientific_reviews_and_church_currentness(self):
        works,_=authority.generate(self.provider)
        selector=next(w for w in works if w["compatibility"]["legacy_key"]=="successor-certified-selector")
        reviews=[s for s in selector["sources"] if s.get("review_kind")=="source_owned_scientific"]
        self.assertEqual({Path(s["path"]).name for s in reviews},{"A1_SOURCE_REVIEW.md","A2_SOURCE_REVIEW.md","A3_SOURCE_REVIEW.md"})
        self.assertTrue(all(s.get("binding_owners") for s in reviews))
        church=next(w for w in works if w["compatibility"]["legacy_key"]=="t20-church-probe")
        current=[s for s in church["sources"] if s.get("role")=="currentness"]
        self.assertEqual(len(current),2)
        self.assertIn("FullPER",str(church.get("reading_links")))
        self.assertIn("independently nonderivable",str(church.get("reading_links")))

    def test_generated_ordinary_commands_never_request_historical_all(self):
        views=authority.render_views(*authority.generate(self.provider))
        self.assertFalse(any("--role all" in line for line in views["START_HERE.md"].splitlines() if line.startswith("python ")))
        self.assertIn("--role reading",views["START_HERE.md"])
        self.assertIn("show --source",views["REPRODUCIBILITY.md"])
        self.assertIn("--work global-productive-adequacy",views["CURRENT_SCIENCE.md"])
        self.assertIn("--work pure-perfection-eligibility-and-participant-sensitive-ends --role status",views["CURRENT_SCIENCE.md"])

if __name__=="__main__":
    unittest.main()
