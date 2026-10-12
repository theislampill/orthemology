#!/usr/bin/env python3
"""Freeze and package a partial continuation; never infer scientific completion."""
from __future__ import annotations
import ast
from datetime import datetime, timezone
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import zipfile

if not __debug__:
    raise SystemExit("Ordinary Python is required.")

BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parent
SEALED=ROOT/"orthemology_consolidation_stage3_delivery_package"
PREFIX=ROOT/"orthemology_consolidation_stage3_delivery"
EXCLUSIONS=[]
ERRORS=[]

def h(data):
    return hashlib.sha256(data).hexdigest()

def write_json(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    if SEALED.exists():
        previous=ROOT/("orthemology_consolidation_stage3_delivery_previous_"+
                       datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f"))
        SEALED.rename(previous)
    SEALED.mkdir()
    screening=load_module("current_distribution_screen",BASE/"verification/preserve_work.py")
    # Syntax-check only authored Python, not inherited repository code.
    for path in (BASE/"verification").glob("*.py"):
        ast.parse(path.read_text(encoding="utf-8"),filename=str(path))
    for path in sorted(BASE.rglob("*")):
        if not path.is_file() and not path.is_symlink():
            continue
        rel=path.relative_to(BASE).as_posix()
        if rel=="SHA256SUMS":
            continue
        if path.is_symlink():
            EXCLUSIONS.append({"path":rel,"reason":"symlink","reading_scope_reduced":False})
            continue
        if rel.startswith("verification/") and "__pycache__" in path.relative_to(BASE).parts:
            EXCLUSIONS.append({"path":rel,"reason":"new_runtime_bytecode_cache",
                               "source_python_preserved":True,"reading_scope_reduced":False})
            continue
        if any(part==".git" or part.endswith(".git") for part in path.relative_to(BASE).parts):
            EXCLUSIONS.append({"path":rel,"reason":"opaque_git_storage",
                               "reading_scope_reduced":False})
            continue
        if "\n" in rel or "\r" in rel:
            EXCLUSIONS.append({"path_sha256":h(rel.encode()),"reason":"manifest_inexpressible_path",
                               "reading_scope_reduced":False})
            continue
        # A changing acquisition file is retained only after a stable read-copy-read.
        stable=False
        for _ in range(3):
            before=path.read_bytes()
            after=path.read_bytes()
            if before==after:
                stable=True;data=before;break
            time.sleep(0.05)
        if not stable:
            EXCLUSIONS.append({"path":rel,"reason":"file_changed_during_freeze",
                               "reading_scope_reduced":False})
            continue
        reasons=screening.screen(rel,data)
        if reasons:
            EXCLUSIONS.append({"path":rel,"sha256":h(data),"bytes":len(data),
                               "reasons":reasons,"reading_scope_reduced":False})
            continue
        dest=SEALED/rel
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(data)
        if h(dest.read_bytes())!=h(data):
            raise RuntimeError("Frozen-copy mismatch: "+rel)
    for required in ("REPORT.md","README.md","CONTINUE.md","verification/verify_package.py",
                     "verification/finite_trajectory_checks_v3.py",
                     "verification/test_finite_trajectory_checks_v3.py"):
        if not (SEALED/required).is_file():
            raise RuntimeError("Required delivery surface missing or excluded: "+required)
    write_json(SEALED/"ledgers/delivery_exclusions.json",EXCLUSIONS)
    text=(SEALED/"REPORT.md").read_text(encoding="utf-8")
    try:
        import markdown
        body=markdown.markdown(text,extensions=["tables","fenced_code","toc"])
    except ImportError:
        body="<pre class='plain-report'>"+html.escape(text)+"</pre>"
    document="""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Orthemology — stage-three continuation, not approved</title>
<style>
:root{color-scheme:light dark}
body{font-family:system-ui,sans-serif;line-height:1.65;margin:3rem auto;padding:0 1.4rem;max-width:1000px}
h1{font-size:2.1rem;line-height:1.2} h2{margin-top:2.4rem;border-bottom:1px solid #888;padding-bottom:.4rem}
h3{margin-top:1.6rem} p{margin:.8rem 0} code,pre{font-family:ui-monospace,monospace}
pre{white-space:pre-wrap;overflow-wrap:anywhere;padding:1rem;border:1px solid #888;border-radius:.3rem}
table{border-collapse:collapse;width:100%;font-size:.93rem}
th,td{text-align:left;vertical-align:top;border:1px solid #888;padding:.6rem}
a{overflow-wrap:anywhere}.status{font-weight:700;border:2px solid #888;padding:1rem;margin-bottom:2rem}
@media print{body{max-width:none;margin:0;font-size:10pt}h2,h3{break-after:avoid}pre,table{font-size:8.5pt}}
</style></head><body>
<div class="status">PARTIAL CONTINUATION — the original exhaustive-review gate remains open.</div>
"""+body+"</body></html>\n"
    (SEALED/"REPORT.html").write_text(document,encoding="utf-8")
    # The HTML is a self-contained rendering of the same text; no external scripts or fonts.
    write_json(SEALED/"ledgers/render_provenance.json",{
        "markdown_sha256":h((SEALED/"REPORT.md").read_bytes()),
        "html_sha256":h((SEALED/"REPORT.html").read_bytes()),
        "external_assets":[],
        "visual_review_claim":False,
        "source_semantic_review_claim":False
    })
    inventory=[]
    for path in sorted(SEALED.rglob("*")):
        if path.is_file():
            data=path.read_bytes()
            inventory.append({"path":path.relative_to(SEALED).as_posix(),
                              "bytes":len(data),"sha256":h(data)})
    write_json(SEALED/"ledgers/delivery_inventory.json",{
        "entries":inventory,
        "inventory_self_excluded_to_avoid_recursive_hashing":True,
        "root_manifest_is_the_full_frozen_byte_set":True,
        "overall_gate":"OPEN_NOT_APPROVED"
    })
    files=[p for p in sorted(SEALED.rglob("*")) if p.is_file()]
    manifest="".join(h(p.read_bytes())+"  "+p.relative_to(SEALED).as_posix()+"\n" for p in files)
    (SEALED/"SHA256SUMS").write_text(manifest,encoding="utf-8")
    verifier=SEALED/"verification/verify_package.py"
    command=[sys.executable,"-B",str(verifier)]
    verified=subprocess.run(command,cwd=SEALED,capture_output=True,text=True,timeout=90)
    # Save this external to the frozen root so executing verification changes no declared byte.
    verification_receipt={
        "command":command,"interpreter":sys.version,
        "verifier_sha256":h(verifier.read_bytes()),
        "exit_code":verified.returncode,"stdout":verified.stdout,"stderr":verified.stderr,
        "scope":"Frozen package bytes, not exhaustive review or mathematical/physical validation."
    }
    write_json(ROOT/(PREFIX.name+"_package_verification.json"),verification_receipt)
    if verified.returncode:
        raise RuntimeError("Frozen package verification failed; inspect the external receipt.")
    archive=ROOT/(PREFIX.name+".zip")
    with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for path in sorted(SEALED.rglob("*")):
            if path.is_file():
                z.write(path,arcname=path.relative_to(SEALED).as_posix())
    with zipfile.ZipFile(archive) as z:
        bad=z.testzip()
        if bad is not None:
            raise RuntimeError("Archive CRC failure: "+bad)
        for line in manifest.splitlines():
            expected,relative=line.split("  ",1)
            if h(z.read(relative))!=expected:
                raise RuntimeError("Archived bytes differ from manifest: "+relative)
    exports={
        "report_markdown":ROOT/(PREFIX.name+"_report.md"),
        "report_html":ROOT/(PREFIX.name+"_report.html"),
        "continuation":ROOT/(PREFIX.name+"_continue.md")
    }
    for key,source in (("report_markdown","REPORT.md"),("report_html","REPORT.html"),
                       ("continuation","CONTINUE.md")):
        shutil.copyfile(SEALED/source,exports[key])
    receipt={
        "created_utc":datetime.now(timezone.utc).isoformat(),
        "overall_gate":"OPEN_NOT_APPROVED",
        "archive":{"path":str(archive),"bytes":archive.stat().st_size,
                   "sha256":h(archive.read_bytes())},
        "exports":{key:{"path":str(p),"bytes":p.stat().st_size,"sha256":h(p.read_bytes())}
                   for key,p in exports.items()},
        "package_verification_exit":verified.returncode,
        "machine_receipt_readback_by_resumed_assistant":"NOT_ESTABLISHED",
        "fresh_source_line_credit_in_resumed_segment":0,
        "inherited_reviews":"Preserved; not reset or recredited.",
        "additional_delivery_exclusions":len(EXCLUSIONS),
        "fonts_and_possible_secret_screen":"See explicit screening code and exclusions; no semantic-review credit.",
        "model_execution_receipt":"verification/results.json inside the package",
        "independent_review":False,
        "meniscus_attainment":False,
        "repository_writes":0
    }
    write_json(ROOT/(PREFIX.name+"_receipt.json"),receipt)
    print(json.dumps(receipt,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
