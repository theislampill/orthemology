#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "$0")" && pwd)
LEAN_BIN=${LEAN_BIN:-"$ROOT/../.toolchains/lean-4.19.0-linux/bin/lean"}
export LEAN_BIN
python "$ROOT/check_bindings.py"
python - "$ROOT" <<'PY'
import hashlib, json, os, pathlib, re, subprocess, sys, tempfile
root = pathlib.Path(sys.argv[1]); lean = pathlib.Path(os.environ['LEAN_BIN']).resolve()
names = ['OpenTermStandardness.lean', 'FrozenCompilerMirror.lean', 'PERInterface.lean']
version = subprocess.check_output([str(lean), '--version'], text=True).strip()
assert 'version 4.19.0' in version, version
logs = [version]; records = []
with tempfile.TemporaryDirectory(prefix='hase-orbit-replay-') as tmp:
    work = pathlib.Path(tmp)
    for name in names:
        data = (root / name).read_bytes()
        text = re.sub(r'/\-.*?\-/', '', data.decode(), flags=re.S)
        text = re.sub(r'--[^\n]*', '', text)
        bad = re.findall(r'\b(?:sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b', text)
        assert not bad, (name, bad)
        (work / name).write_bytes(data)
    for name in names:
        command = [str(lean), '-o', name[:-5] + '.olean', name]
        p = subprocess.run(command, cwd=work, env={**os.environ, 'LEAN_PATH': str(work)},
                           capture_output=True, text=True)
        output = p.stdout + p.stderr
        logs += ['$ ' + ' '.join(command), output]
        records.append({'source': name, 'sha256': hashlib.sha256((work / name).read_bytes()).hexdigest(),
                        'exit_code': p.returncode, 'command': command})
        assert p.returncode == 0, output
        assert 'sorryAx' not in output and 'warning:' not in output and 'error:' not in output, output
    for line in '\n'.join(logs).splitlines():
        if 'depends on axioms:' in line:
            axioms = line.split('[', 1)[1].split(']', 1)[0].replace(' ', '').split(',')
            assert set(axioms) <= {'propext', 'Quot.sound', ''}, line
(root / 'validation' / 'FINAL_REPLAY.log').write_text('\n'.join(logs) + '\n')
result = {'status': 'PASS', 'lean_version': version, 'fresh_temporary_directory': True,
          'sources': records, 'scope': 'Three isolated modules only. No inherited HasE import or replay.'}
(root / 'validation' / 'FINAL_REPLAY.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS: all three isolated modules kernel-checked in a fresh directory; no admitted or custom axioms.')
PY
