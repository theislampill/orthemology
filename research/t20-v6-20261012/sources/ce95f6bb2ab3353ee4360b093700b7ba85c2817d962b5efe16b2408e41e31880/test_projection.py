import hashlib
import json
import pathlib
import tempfile
import unittest
import verify_projection

class ProjectionTests(unittest.TestCase):
    def fixture(self, root):
        data=b"scientific source\n"
        record={"original_path":"proof.lean","public_path":"proof.lean","sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data)}
        (root/"PROJECTION_MANIFEST.json").write_text(json.dumps({"retained":[record],"independent_review":[],"added":[],"excluded":[{"original_path":"PRIVATE_PLAN.md"}]}))
        return data

    def test_missing_retained_file_fails(self):
        with tempfile.TemporaryDirectory(dir=pathlib.Path(__file__).parent) as temp:
            root=pathlib.Path(temp);self.fixture(root)
            with self.assertRaises((ValueError,FileNotFoundError)):
                verify_projection.verify_tree(root)

    def test_modified_science_fails(self):
        with tempfile.TemporaryDirectory(dir=pathlib.Path(__file__).parent) as temp:
            root=pathlib.Path(temp);self.fixture(root);(root/"proof.lean").write_bytes(b"changed")
            with self.assertRaises(ValueError):verify_projection.verify_tree(root)

    def test_excluded_process_file_fails(self):
        with tempfile.TemporaryDirectory(dir=pathlib.Path(__file__).parent) as temp:
            root=pathlib.Path(temp);data=self.fixture(root);(root/"proof.lean").write_bytes(data);(root/"PRIVATE_PLAN.md").write_text("private")
            with self.assertRaises(ValueError):verify_projection.verify_tree(root)

    def test_exact_projection_passes(self):
        with tempfile.TemporaryDirectory(dir=pathlib.Path(__file__).parent) as temp:
            root=pathlib.Path(temp);data=self.fixture(root);(root/"proof.lean").write_bytes(data)
            verify_projection.verify_tree(root)

if __name__=='__main__':unittest.main()
