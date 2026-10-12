#!/usr/bin/env python3
"""Verify that retained completed replay records bind all current Lean suites."""
from pathlib import Path
import argparse,json
from portable_core import verify_manifest,verify_replay_evidence,write_json

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--receipt',type=Path);a=ap.parse_args();root=a.root.resolve();verify_manifest(root)
 entries=json.loads((root/'REPLAY_EVIDENCE_INDEX.json').read_text())['entries'];suites=json.loads((root/'SUITES.json').read_text())['suites'];result=verify_replay_evidence(root,entries,suites)
 if a.receipt:
  if a.receipt.resolve().is_relative_to(root):ap.error('Receipt must be outside immutable package')
  write_json(a.receipt,result)
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
