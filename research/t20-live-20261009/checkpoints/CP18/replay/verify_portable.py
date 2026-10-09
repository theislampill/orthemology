#!/usr/bin/env python3
"""Portable three-file Lean4.19.0 archive qualification. No historical proof replay."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os, re, subprocess
EXPECTED = {
 "Uniqueness.lean": "29f7e5820f187957286705824a9347b41a5e889a6bc200223a2990b2efcb18e1",
 "FiniteControl.lean": "de5eefa7432a8d6fbe58f2ac9f54afa6baa14924291e4808964f8d77139d1686",
 "BooleanControl.lean": "ea375a9a0fe63016ceef74b4f64ddb462b5c414a165791c1ac9a649976966ecb"
}
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
p=argparse.ArgumentParser(description=__doc__)
p.add_argument("--lean", required=True, help="Explicit absolute path to installed Lean4.19.0 executable")
p.add_argument("--output", required=True, help="New absolute output directory; must not already exist")
a=p.parse_args()
lean=Path(a.lean)
if not lean.is_absolute() or not lean.is_file() or not os.access(lean,os.X_OK): p.error("--lean must be an executable absolute file path")
lean=lean.resolve()
out=Path(a.output)
if not out.is_absolute() or out.exists(): p.error("--output must be a new absolute directory")
root=Path(__file__).resolve().parent.parent
version=subprocess.run([str(lean),"--version"],capture_output=True,text=True,check=True).stdout.strip()
if not re.match(r"^Lean \(version 4\.19\.0,",version): p.error("Lean4.19.0 required; found: "+version)
for name,h in EXPECTED.items():
 path=root/"total-explainer-uniqueness"/name
 if digest(path)!=h: p.error("Source hash mismatch: "+name)
 if re.search(r"\b(sorry|admit|done)\b|^[ \t]*axiom[ \t]",path.read_text(),re.M): p.error("Unfinished or assumed declaration: "+name)
out.mkdir(parents=True,exist_ok=False)
checks=[]
for name,h in EXPECTED.items():
 source=root/"total-explainer-uniqueness"/name
 run=subprocess.run([str(lean),str(source)],cwd=root,capture_output=True,text=True)
 log=out/(name+".log")
 log.write_text(run.stdout+run.stderr)
 checks.append({"file":"total-explainer-uniqueness/"+name,"sha256":h,"exit_code":run.returncode,"log":str(log),"log_sha256":digest(log),"sorryAx_present":"sorryAx" in log.read_text(),"source_unchanged":digest(source)==h})
receipt={"utc":datetime.now(timezone.utc).isoformat(),"scope":"Fresh archive transport qualification of three new standalone files only. No source authentication, older-proof replay, philosophical assessment, integration or closure.","lean_executable":str(lean),"toolchain":version,"toolchain_binary_sha256":digest(lean),"checks":checks}
receipt["passed"]=all(c["exit_code"]==0 and not c["sorryAx_present"] and c["source_unchanged"] for c in checks)
(out/"QUALIFICATION.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
raise SystemExit(0 if receipt["passed"] else 1)
