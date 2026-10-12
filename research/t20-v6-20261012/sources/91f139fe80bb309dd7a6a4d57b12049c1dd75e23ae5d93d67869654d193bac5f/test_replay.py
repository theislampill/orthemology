import hashlib
import json
import pathlib
import tempfile
import unittest
import replay

class ReplayBoundaryTests(unittest.TestCase):
    def test_absent_compiled_output_is_rejected(self):
        with self.assertRaises(ValueError):
            replay.verify_output("")

    def test_terminal_alone_does_not_impersonate_scenarios(self):
        with self.assertRaises(ValueError):
            replay.verify_output("SOURCE_BYTES 3013\nTERMINAL PASS\n")

    def test_failure_before_terminal_is_rejected(self):
        with self.assertRaises(ValueError):
            replay.verify_output("FAIL hidden\nTERMINAL PASS\n")

    def test_source_hash_mismatch_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=pathlib.Path(__file__).resolve().parent) as tmp:
            path = pathlib.Path(tmp)/"source"
            path.write_bytes(b"source")
            with self.assertRaises(ValueError):
                replay.verify_file(path, "0"*64, 6)

    def test_exact_source_passes_binding(self):
        with tempfile.TemporaryDirectory(dir=pathlib.Path(__file__).resolve().parent) as tmp:
            path = pathlib.Path(tmp)/"source"
            path.write_bytes(b"source")
            replay.verify_file(path, hashlib.sha256(b"source").hexdigest(), 6)


class ArtifactBoundaryTests(unittest.TestCase):
    def test_missing_compiled_state_artifacts_are_rejected(self):
        with tempfile.TemporaryDirectory(dir=pathlib.Path(__file__).resolve().parent) as tmp:
            with self.assertRaises((ValueError, FileNotFoundError)):
                replay.verify_artifacts(pathlib.Path(tmp))

    def test_full_artifact_binding_rejects_wrong_target(self):
        with tempfile.TemporaryDirectory(dir=pathlib.Path(__file__).resolve().parent) as tmp:
            build=pathlib.Path(tmp)
            source=b"source"
            before={"source":{"target":["wrong","wrong","wrong"],"content":list(source),"roots":["pinned-source"]},
                    "destination":"fixture-A","standard":"exact-source-recovery", "draft":list(source)+[10],
                    "draft_revision":8,"draft_history":[[88]],"rule":"normalizedLF","rule_version":3,
                    "rule_history":[],"unrelated":["retain-custody"]}
            installed=dict(before,rule="exact",rule_version=4,rule_history=["normalizedLF"])
            repaired=dict(installed,draft=list(source),draft_revision=9,draft_history=[[88],list(source)+[10]])
            for name,data in [("before",before),("installed",installed),("repaired",repaired)]:
                (build/f"{name}.json").write_text(json.dumps(data))
            for name in ["source.bin","preserved-source.bin","repaired-draft.bin"]:
                (build/name).write_bytes(source)
            with self.assertRaises(ValueError):
                replay.verify_artifacts(build)

if __name__ == "__main__":
    unittest.main()
