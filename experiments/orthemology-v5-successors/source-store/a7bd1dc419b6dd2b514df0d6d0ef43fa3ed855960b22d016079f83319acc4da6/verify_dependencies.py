#!/usr/bin/env python3
"""Verify prepared source revisions and toolchain, without a network request."""
from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[1]
def verify(path,p):
    def git(*a):return subprocess.check_output(['git','-C',str(path),*a],text=True).strip()
    assert path.is_dir(),f"Missing dependency: {p['name']}"
    assert git('rev-parse','HEAD')==p['rev'],f"Wrong revision: {p['name']}"
    assert not git('status','--porcelain','--untracked-files=no'),f"Modified tracked sources: {p['name']}"
if __name__=='__main__':
    for p in json.loads((ROOT/'lake-manifest.json').read_text())['packages']:
        verify(ROOT/'.lake/packages'/p['name'],p)
    version=subprocess.check_output(['lean','--version'],text=True).strip()
    assert 'version 4.19.0,' in version and '6caaee842e94' in version,version
    print('DEPENDENCY_PINS_PASS: nine clean exact revisions; official-release Lean 4.19.0 commit')
