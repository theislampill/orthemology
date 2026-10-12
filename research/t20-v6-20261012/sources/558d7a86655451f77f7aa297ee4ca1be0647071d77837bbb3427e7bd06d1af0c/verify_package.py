from pathlib import Path
import hashlib,json
r=Path(__file__).resolve().parent
def check(p,e):
 b=p.read_bytes()
 assert len(b)==e["bytes"], f"Size mismatch: {p}"
 assert hashlib.sha256(b).hexdigest()==e["sha256"], f"Hash mismatch: {p}"
m=json.loads((r/"PACKAGE_MANIFEST.json").read_text())
expected={e["path"] for e in m["files"]}|{"PACKAGE_MANIFEST.json"}
actual={str(p.relative_to(r)) for p in r.rglob("*") if p.is_file()}
assert expected==actual, f"Membership mismatch: {expected ^ actual}"
for e in m["files"]: check(r/e["path"],e)
a=r/"attestation-response-case-20261010"
for e in json.loads((a/"MANIFEST.json").read_text())["files"]: check(a/e["path"],e)
v=json.loads((a/"VERIFICATION.json").read_text())
assert hashlib.sha256((a/"MANIFEST.json").read_bytes()).hexdigest()==v["manifest_sha256"]
b=json.loads((r/"review-attestation-response-20261010/REVIEW_BINDINGS.json").read_text())
check(r/b["target"]["path"],b["target"])
assert hashlib.sha256((r/"review-attestation-response-20261010/REVIEW.md").read_bytes()).hexdigest()==b["review_sha256"]
for e in b["authored_manifest_checks"]: check(r/e["path"],e)
for e in json.loads((a/"LOCAL_INPUT_BINDINGS.json").read_text()):
 if (r/e["path"]).exists(): check(r/e["path"],e)
print(f"PASS: {len(m['files'])} payload files, exact membership, author and review bindings, included inherited bindings. External omitted bodies and inputs are not replayed.")
