#!/usr/bin/env python3
"""Read-only exact-byte verification of this scoped review receipt."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
receipt = json.loads((root / "REVIEW_RECEIPT.json").read_text())
verified = []
for group in ["author_payloads", "review_artifacts", "directly_read_ancestry"]:
    for row in receipt[group]:
        data = (root / row["path"]).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        assert digest == row["sha256"], (group, row["path"], digest)
        assert len(data) == row["bytes"], (group, row["path"], len(data))
        verified.append({"group": group, "path": row["path"], "sha256": digest})
print(json.dumps({"status": "PASS", "count": len(verified), "verified": verified,
                  "scope": "Exact reviewed bindings; no self-hash and no future packaging coverage."}, indent=2))
