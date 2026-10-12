#!/usr/bin/env python3
"""Portable exact custody check and isolated, additive Lean replay only."""
from pathlib import Path
import argparse, hashlib, importlib, json, os, re, shutil, subprocess, sys
sys.dont_write_bytecode = True

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for data in iter(lambda: f.read(1024 * 1024), b''):
            h.update(data)
    return h.hexdigest()

def need(condition, message):
    if not condition:
        raise ValueError(message)

def check(path, row):
    need(path.is_file() and not path.is_symlink(), 'Missing or symlink: ' + str(path))
    need(path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], 'Mismatch: ' + str(path))

def verify(root, pin):
    need(sha(root / 'MANIFEST.json') == pin, 'Manifest external pin mismatch')
    rows = json.loads((root / 'MANIFEST.json').read_text())['files']
    names = [r['path'] for r in rows]
    need(len(names) == len(set(names)), 'Duplicate manifest path')
    actual = []
    for p in root.rglob('*'):
        need(not p.is_symlink(), 'Symlink in packet')
        if p.is_file():
            actual.append(p.relative_to(root).as_posix())
    need(set(actual) == set(names) | {'MANIFEST.json'}, 'Exact packet inventory mismatch')
    for r in rows:
        p = root / r['path']
        need(p.resolve().is_relative_to(root), 'Escaping packet path')
        check(p, r)
    c = json.loads((root / 'REUSE_CONTRACT.json').read_text())
    for r in c['copied_originals'] + c['final_receipt_bindings'] + c['modules']:
        check(root / r['path'], r)
    for r in c['review_source_bindings']:
        need(sha(root / r['author']) == sha(root / r['review']), 'Author/reviewer source mismatch')
    return c

def dependencies(w, c):
    for p in c.get('required_absent_paths', []):
        need(not (w / p).exists(), 'Quarantined stray log returned to old destination: '+p)
    for r in c['source_originals']:
        check(w / r['path'], r)
    for r in c['dependency_roots']:
        base = w / r['path']
        actual = sorted(p.relative_to(base).as_posix() for p in base.rglob('*.olean') if p.is_file())
        need(actual == sorted(r['olean_inventory']), 'Dependency-root inventory changed: ' + r['path'])
    for r in c['retained_dependency_files']:
        p = w / r['path']
        if 'symlink_target' in r:
            need(p.is_symlink() and os.readlink(p) == r['symlink_target'], 'Retained symlink changed')
            need(p.resolve().is_relative_to(w), 'Retained symlink escapes workspace')
            check(p.resolve(), r)
        else:
            check(p, r)

def python_runtime(root):
    r = json.loads((root / 'RUNTIME_PINS.json').read_text())
    need(sys.version == r['python_version'], 'Python version changed')
    need(sha(Path(sys.executable)) == r['python_executable_sha256'], 'Python executable changed')
    counts = {}
    for package in r['packages']:
        module = importlib.import_module(package['name'])
        need(module.__version__ == package['version'], 'Python package version changed')
        base = Path(module.__file__).parent
        actual = sorted(p.relative_to(base).as_posix() for p in base.rglob('*.py') if '__pycache__' not in p.parts)
        need(actual == sorted(p['path'] for p in package['python_source_files']), 'Python package inventory changed')
        for f in package['python_source_files']: check(base / f['path'], f)
        counts[package['name']] = len(actual)
    return counts

def canonical_import(path, w, fresh, aliases=()):
    p = Path(path)
    for base in [fresh, *aliases]:
        if p.is_relative_to(base):
            return 'fresh:' + p.relative_to(base).with_suffix('').as_posix().replace('/', '.')
    need(p.is_relative_to(w), 'Import escapes pinned workspace: ' + str(p))
    return 'retained:' + p.relative_to(w).as_posix()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--expected-manifest-sha256', required=True)
    ap.add_argument('--workspace', type=Path)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--replay', action='store_true')
    x = ap.parse_args()
    root, out = x.root.resolve(), x.output.resolve()
    need(not out.exists(), 'Output exists')
    need(not out.is_relative_to(root), 'Output must be outside packet')
    c = verify(root, x.expected_manifest_sha256)
    out.mkdir(parents=True)
    receipt = {'status': 'PASS_CUSTODY', 'manifest_sha256': x.expected_manifest_sha256,
               'baseline_modules_rebuilt': 0, 'new_independent_review': False,
               'source_rule_adopted': False, 'integration': False, 't20_closure': False}
    if x.replay:
        need(x.workspace is not None, 'Workspace required for exact retained dependencies')
        w = x.workspace.resolve()
        dependencies(w, c)
        prior = json.loads((root / 'PRIOR_ARCHIVES.json').read_text())
        for p, h in prior.items():
            need(sha(w / p) == h, 'Prior archive changed: ' + p)
        libs = {}
        for group in c['group_search_orders']:
            libs[group] = out / group / 'lib'
            libs[group].mkdir(parents=True)
        records = []
        for r in c['modules']:
            m, group = r['module'], r['group']
            lib = libs[group]
            source = root / r['path']
            obj = lib / (m.replace('.', '/') + '.olean')
            need(not obj.exists(), 'Fresh output object already exists')
            env = {**os.environ, 'LEAN_PATH': ':'.join([str(lib)] + [str(w / p) for p in c['group_search_orders'][group]])}
            lean = str(w / c['lean_binary'])
            dr = subprocess.run([lean, '--root='+str(root), '--deps', str(source)], env=env, capture_output=True, text=True)
            need(dr.returncode == 0, 'Import discovery failed: ' + dr.stdout + dr.stderr)
            direct = [canonical_import(p.strip(), w, lib) for p in dr.stdout.splitlines() if p.strip()]
            need(direct == r['direct_imports'], 'Direct import resolution changed: ' + m)
            opts=[lean, '--root='+str(root), '--trust=0']+r.get('lean_arguments', [])
            command = opts+['--run', str(source)] if r.get('execution_mode') == 'run' else opts+['-o', str(obj), str(source)]
            run = subprocess.run(command, env=env, capture_output=True, text=True)
            output = run.stdout + run.stderr
            log = out / (group + '-' + m + '.log')
            log.write_text(output)
            historical = (root / r['historical_log']).read_text().replace(r['historical_source_path'], str(source))
            need(output == historical, 'Exact historical diagnostic mismatch: ' + m)
            axioms = sorted({a.strip() for xs in re.findall(r'(?:depends on axioms:|axioms=)\s*\[([^\]]*)\]', output, re.S) for a in xs.split(',') if a.strip()})
            row = {'module': m, 'group': group, 'exit_code': run.returncode, 'command': command,
                   'source_sha256': sha(source), 'log_sha256': sha(log), 'direct_imports': direct, 'axioms': axioms}
            if r['expected_failure']:
                need(run.returncode != 0 and 'error:' in output and not obj.exists(), 'Expected rejection failed: ' + m)
                need('unknown identifier' not in output and 'object file' not in output, 'Invalid rejection: ' + m)
                row['status'] = 'EXPECTED_REJECTION'
            else:
                need(run.returncode == 0 and not re.search(r'warning:|error:', output), 'Replay failed: ' + m)
                need(set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'}, 'Unexpected axiom: ' + m)
                row.update(status='PASS', execution_mode=r.get('execution_mode','compile'), object_sha256=sha(obj) if obj.exists() else None)
                need(obj.exists() or r.get('execution_mode')=='run', 'Compiled output missing')
            records.append(row)
            print(group, m, row['status'], flush=True)
        closures = []
        for spec in c.get('transitive_import_manifests', []):
            imports = json.loads((root / spec['path']).read_text())
            import_log = (out / (spec['group']+'-'+spec['inspection_module']+'.log')).read_text()
            names = [line.removeprefix(spec['prefix']) for line in import_log.splitlines() if line.startswith(spec['prefix'])]
            need(names == [r['module'] for r in imports], 'Transitive imported-module sequence changed')
            fresh_imports = []
            for row in imports:
                if row['module'] in spec['fresh_modules']:
                    p = libs[spec['group']] / (row['module'].replace('.', '/')+'.olean')
                    need(p.is_file(), 'Selected import was not freshly compiled')
                    fresh_imports.append({'module':row['module'],'object_sha256':sha(p)})
                else:
                    need(sha(w/row['path']) == row['sha256'], 'Reused transitive import changed')
            closures.append({'group':spec['group'],'total_modules':len(imports),'reused_modules':len(imports)-len(fresh_imports),'fresh_selected_imports':fresh_imports})
        runtime_records=[]
        for r in c.get('runtime_replays', []):
            lib=libs[r['group']];source=root/r['path']
            env={**os.environ,'LEAN_PATH':':'.join([str(lib)]+[str(w/p) for p in c['group_search_orders'][r['group']]])}
            command=[str(w/c['lean_binary']),'--root='+str(root),'--trust=0','--run',str(source)]+r.get('arguments', [])
            run=subprocess.run(command,env=env,capture_output=True,text=True)
            output=run.stdout+run.stderr;log=out/(r['label']+'.log');log.write_text(output)
            historical=(root/r['historical_log']).read_text().replace(r['historical_source_path'],str(source))
            need(run.returncode==r['expected_exit'] and output==historical,'Runtime/CLI control mismatch: '+r['label'])
            runtime_records.append({'label':r['label'],'exit_code':run.returncode,'command':command,'log_sha256':sha(log),'status':'PASS_EXPECTED_OUTCOME'})
            print(r['label'],'PASS_EXPECTED_OUTCOME',flush=True)
        python_records = []
        if c.get('python_replays'):
            runtime_counts = python_runtime(root)
            sandbox = out / 'python-sandbox'
            shutil.copytree(root, sandbox)
            for r in c['python_replays']:
                command = [sys.executable, str(sandbox / r['script'])]
                for item in r.get('arguments', []):
                    command.append(item.replace('{sandbox}', str(sandbox)).replace('{workspace}', str(w)))
                for binding in r['expected_outputs']:
                    target = sandbox / binding['path']
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.unlink(missing_ok=True)
                run = subprocess.run(command, cwd=sandbox, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}, capture_output=True, text=True)
                log = out / (r['label'] + '.log')
                log.write_text(run.stdout + run.stderr)
                need(run.returncode == 0, 'Exact-rational replay failed: ' + r['label'])
                if r.get('stdout_output_path'):
                    (sandbox / r['stdout_output_path']).write_text(run.stdout)
                checked = []
                for binding in r['expected_outputs']:
                    output = sandbox / binding['path']
                    need(sha(output) == binding['sha256'], 'Exact-rational output changed: ' + binding['path'])
                    for key, expected in binding.get('expected_values', {}).items():
                        need(json.loads(output.read_text())[key] == expected, 'Control summary changed: ' + key)
                    checked.append({'path': binding['path'], 'sha256': sha(output)})
                python_records.append({'label': r['label'], 'command': command, 'exit_code': 0,
                                       'log_sha256': sha(log), 'outputs': checked,
                                       'evidence_level': r.get('evidence_level', 'Exact output reproduction; not an additional independent review')})
                print(r['label'], 'PASS_EXACT_OUTPUTS', flush=True)
            python_runtime(root)
        dependencies(w, c)
        verify(root, x.expected_manifest_sha256)
        for p, h in prior.items():
            need(sha(w / p) == h, 'Prior archive changed: ' + p)
        receipt.update(status='PASS_CUSTODY_AND_FRESH_REPLAY', modules=records,
                       transitive_import_closures=closures,runtime_replays=runtime_records,
                       python_replays=python_records,
                       python_runtime_source_counts=runtime_counts if c.get('python_replays') else {},
                       retained_dependencies_unchanged=True, prior_archives_verified_unchanged=len(prior),
                       trust=0, toolchain_version=subprocess.check_output([str(w / c['lean_binary']), '--version'], text=True).strip())
    (out / 'RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(receipt['status'], flush=True)

if __name__ == '__main__':
    main()
