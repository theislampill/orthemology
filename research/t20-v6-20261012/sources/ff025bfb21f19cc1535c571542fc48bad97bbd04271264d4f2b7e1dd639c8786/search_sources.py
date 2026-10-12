#!/usr/bin/env python3
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser(description="Search unchanged selected source reports")
p.add_argument("term");p.add_argument("--limit",type=int,default=30);a=p.parse_args()
root=Path(__file__).resolve().parents[1]
rows=json.loads((root/"inventory/SOURCE_REPORTS.json").read_text())
n=0
for r in rows:
    text=(root/r["path"]).read_text(encoding="utf-8-sig")
    for i,line in enumerate(text.splitlines(),1):
        if a.term.casefold() in line.casefold():
            print(f'{r["source_id"]}:{i}: {line[:600]}')
            print("  "+r["bindings"][0]["archive_name"]+" :: "+r["bindings"][0]["member"])
            n+=1
            if n>=a.limit:raise SystemExit(0)
