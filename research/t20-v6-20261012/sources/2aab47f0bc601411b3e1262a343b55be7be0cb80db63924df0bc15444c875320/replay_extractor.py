#!/usr/bin/env python3
"""Path-independent, exact-object-reuse replay. Does not bootstrap prerequisites."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parent
AUTHOR_NAME = 'hase-effective-instance-assessment-20261010'
REVIEW_NAME = 'hase-complete-development-review-20261010'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text())

def inside(root, name):
    rel = PurePosixPath(name)
    assert not rel.is_absolute() and '..' not in rel.parts, name
    p = root / rel
    assert not p.is_symlink() and p.resolve().is_relative_to(root.resolve()), name
    return p

def verify_index(root, expected=None):
    index = root / 'ARCHIVE_CONTENTS.json'
    if expected: assert sha(index) == expected
    rows = read(index)['files']
    assert len({r['path'] for r in rows}) == len(rows)
    for r in rows:
        p = inside(root, r['path'])
        assert p.stat().st_size == r['bytes'] and sha(p) == r['sha256'], str(p)
    return len(rows)

def archive_matches(archive, root, expected):
    assert sha(archive) == expected, str(archive)
    with zipfile.ZipFile(archive) as z:
        rows = [r for r in z.infolist() if not r.is_dir()]
        assert len({r.filename for r in rows}) == len(rows)
        for r in rows:
            path = PurePosixPath(r.filename)
            assert path.parts[0] == root.name, (path, root.name)
            target = inside(root, PurePosixPath(*path.parts[1:]).as_posix())
            assert z.read(r) == target.read_bytes(), str(target)
        return len(rows)

def verify(args):
    contract = read(ROOT / 'REUSE_CONTRACT.json')
    counts = {'addition': verify_index(ROOT)}
    for key in ['v3', 'continuation']:
        base = getattr(args, key)
        row = contract[key]
        counts[key] = verify_index(base, row['index_sha256'])
        counts[key + '_archive_entries'] = archive_matches(getattr(args, key + '_archive'), base, row['archive_sha256'])
    author = ROOT / AUTHOR_NAME
    for row in contract['final_bindings']:
        assert sha(inside(ROOT, row['path'])) == row['sha256'], row['path']
    omissions = {r['path']: r for r in contract['omitted_historical_objects']}
    for name in [AUTHOR_NAME, REVIEW_NAME]:
        for row in read(ROOT / name / 'MANIFEST.json')['files']:
            key = name + '/' + row['path']
            if key in omissions:
                assert name == REVIEW_NAME and row['path'].startswith('fresh-lib/') and row['path'].endswith('.olean')
                assert omissions[key]['sha256'] == row['sha256'] and omissions[key]['bytes'] == row['bytes']
                assert not (ROOT / key).exists()
                continue
            p = inside(ROOT / name, row['path'])
            assert sha(p) == row['sha256'], str(p)
    inp = read(author / 'INPUTS.json')
    checked = []
    for row in inp['source_and_receipt_bindings']:
        mapping = contract['source_map'][row['path']]
        if mapping['kind'] == 'historical_provenance_only': continue
        base = getattr(args, mapping['kind'])
        target = inside(base, mapping['path'])
        assert sha(target) == row['sha256'], str(target)
        checked.append({'path': row['path'], 'sha256': row['sha256'], 'mapped_to': str(target)})
    prior = read(args.v3 / contract['prerequisite_receipt'])
    assert prior['status'] == 'PASS' and len(prior['build_records']) == 89
    assert sha(args.lean) == inp['lean_binary_sha256'] == prior['lean_binary_sha256']
    version = subprocess.check_output([str(args.lean), '--version'], text=True).strip()
    assert version == prior['lean_version']
    imported = args.v3 / 'hase-imported-compiler-transport-20261010'
    acq = read(imported / 'ACQUISITION.json')
    sources = {r['module']: r for r in acq['sources']}
    assert len(sources) == 83 and acq['pin'] == prior['pin']
    pins = []
    for p in read(imported / 'EXTERNAL_PACKAGE_MANIFEST.json')['packages']:
        observed = subprocess.check_output(['git', '-C', str(args.packages / p['name']), 'rev-parse', 'HEAD'], text=True).strip()
        assert observed == p['rev'], p['name']
        pins.append({'name':p['name'], 'rev':observed})
    expected_objects = {r['module']: r['sha256'] for r in inp['reused_objects']}
    for row in prior['build_records']:
        name = row['module']
        rel = Path(*name.split('.')).with_suffix('.lean')
        assert row['trust_zero'] and row['exit_code'] == 0
        assert row['object_sha256'] == expected_objects[name]
        if name in sources:
            data = (imported / 'sources' / (name + '.lean')).read_bytes()
            assert hashlib.sha256(data).hexdigest() == sources[name]['sha256']
            assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == sources[name]['git_blob']
        elif name in {'OpenTermStandardness', 'FrozenCompilerMirror', 'PERInterface', 'ImportedCompilerTransport'}:
            data = (imported / 'proofs' / (name + '.lean')).read_bytes()
        else:
            assert name in {'Mathlib.Algebra.MvPolynomial.Polynomial','Mathlib.Algebra.MvPolynomial.Funext'}
            data = (args.packages / 'mathlib' / rel).read_bytes()
            assert data == subprocess.check_output(['git','-C',str(args.packages/'mathlib'),'show','HEAD:'+rel.as_posix()])
        assert hashlib.sha256(data).hexdigest() == row['source_sha256'], name
    model = read(args.v3 / contract['model_receipt'])
    for row in model['new_replays']:
        assert sha(args.v3 / row['source']['path']) == row['source']['sha256']
        assert row['object']['sha256'] == expected_objects[row['module']]
    objects = []
    for row in inp['reused_objects']:
        base = args.closed_objects if row['module'] in {'ClosedProofCanonicalisation','ClosedScalarInstances'} else args.prerequisite_objects
        path = base / Path(*row['module'].split('.')).with_suffix('.olean')
        assert sha(path) == row['sha256'], 'Requires exact retained object: ' + str(path)
        objects.append({'module':row['module'], 'sha256':row['sha256'], 'path':str(path)})
    assert len(objects) == 94
    return {'counts':counts,'source_bindings':checked,'objects':objects,'lean_version':version,
            'lean_binary_sha256':sha(args.lean),'pinned_packages':pins}

def clean_code(text):
    out=[]; i=0; depth=0
    while i<len(text):
        if text[i:i+2]=='/-':depth+=1;i+=2
        elif depth and text[i:i+2]=='-/':depth-=1;i+=2
        elif not depth and text[i:i+2]=='--':
            j=text.find('\n',i);i=len(text) if j<0 else j
        elif not depth and text[i]=='"':
            i+=1
            while i<len(text):
                if text[i]=='\\':i+=2
                elif text[i]=='"':i+=1;break
                else:i+=1
            out.append('""')
        else:
            if not depth:out.append(text[i])
            i+=1
    assert depth==0
    return ''.join(out)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['v3','v3-archive','continuation','continuation-archive','lean','packages','prerequisite-objects','closed-objects']:
        p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--out',type=Path)
    p.add_argument('--verify-only',action='store_true')
    args=p.parse_args()
    for name,value in vars(args).items():
        if isinstance(value,Path):setattr(args,name,value.resolve())
    before=verify(args)
    if args.verify_only:
        print(json.dumps({'status':'PASS_EXACT_REUSE_PREREQUISITES','verified_objects':94,**before['counts']},indent=2));return
    assert args.out and not args.out.exists(), 'Use an absent output directory'
    for frozen in [ROOT,args.v3,args.continuation,args.prerequisite_objects,args.closed_objects,args.packages]:
        assert not args.out.is_relative_to(frozen), 'Output must be outside frozen inputs'
    args.out.mkdir(parents=True)
    author=ROOT/AUTHOR_NAME; review=ROOT/REVIEW_NAME
    stage=args.out/'author'; stage.mkdir();(stage/'validation').mkdir()
    for f in author.iterdir():
        if f.is_file() and (f.suffix in {'.py','.lean'} or f.name=='source_ast.json'):shutil.copy2(f,stage/f.name)
    rstage=args.out/'review';rstage.mkdir();(rstage/'validation').mkdir();(rstage/'sources').mkdir()
    for f in review.iterdir():
        if f.is_file() and f.suffix in {'.py','.lean'}:shutil.copy2(f,rstage/f.name)
    for f in stage.iterdir():
        if f.is_file() and (f.suffix in {'.py','.lean'} or f.name=='source_ast.json'):shutil.copy2(f,rstage/'sources'/f.name)
    lib=args.out/'lib';lib.mkdir(); rlib=args.out/'review-lib';rlib.mkdir()
    libs=[args.packages/p['name']/'.lake/build/lib/lean' for p in before['pinned_packages']]
    libs=[x for x in libs if x.is_dir()]
    env={**os.environ,'LEAN_PATH':':'.join(map(str,[lib,args.closed_objects,args.prerequisite_objects]+libs)),'PYTHONDONTWRITEBYTECODE':'1'}
    records=[]; logpath=args.out/'REPLAY.log'
    with logpath.open('w') as log:
        def run(label,command,cwd=stage,negative=False):
            start=time.monotonic()
            result=subprocess.run(list(map(str,command)),cwd=cwd,env=env,capture_output=True,text=True,timeout=900)
            text=result.stdout+result.stderr
            log.write('$ '+' '.join(map(str,command))+'\n'+text);log.flush()
            (args.out/(label+'.log')).write_text(text)
            if negative:
                assert result.returncode != 0 and 'error:' in text and 'decide' in text, (label,text)
            else:
                assert result.returncode==0,(label,text)
                assert not any(x in text for x in ['error:','warning:','sorryAx']),(label,text)
                for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',text,re.S):
                    assert set(re.sub(r'\s+','',match).split(',')) <= {'propext','Classical.choice','Quot.sound',''},(label,match)
            records.append({'label':label,'command':list(map(str,command)),'exit_code':result.returncode,
                            'expected_negative':negative,'seconds':round(time.monotonic()-start,3),
                            'log_sha256':hashlib.sha256(text.encode()).hexdigest()})
            print(label, 'EXPECTED_REJECTION' if negative else 'PASS',flush=True)
            return result.stdout
        def compile(module,base=stage,dest=lib,label=None,negative=False):
            source=base/(module+'.lean')
            assert not re.findall(r'\b(?:sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b',clean_code(source.read_text())),module
            output=dest/(module+'.olean')
            cmd=[args.lean,'--trust=0']+([] if negative else ['-o',output])+[source]
            run(label or module,cmd,cwd=base,negative=negative)
            records[-1].update({'source_sha256':sha(source),'trust_zero':True})
            if not negative:records[-1]['object_sha256']=sha(output)
        for module in ['OpenDevelopments','DomainControls','ScalarCertificates','LiteralSourceQ','SourceExport','NonstandardRejection','NegativeCertificateControls','OpenCertificateControl']:
            compile(module)
        exported=run('literal_source_export',[args.lean,'--trust=0','--run',stage/'SourceExport.lean'])
        assert json.loads(exported)==read(author/'source_ast.json')
        run('author_python_tests',[sys.executable,'-m','unittest','-v','test_diagnostic.py'])
        run('regenerate_concrete',[sys.executable,stage/'generate_controls.py'])
        resource_code = "import diagnostic as d, json; from pathlib import Path; r={'round_zero':d.diagnose(d.SOURCE['numerals'][2],max_rounds=0),'numeral_6_200k_nodes':d.diagnose(d.SOURCE['numerals'][6],max_nodes=200000),'omega_8_rounds':d.diagnose(['atom',d.SOURCE['omega']],max_rounds=8),'normal_noniteration':d.diagnose(['atom',['zero']])}; Path('validation/REFUSAL_CONTROLS.json').write_text(json.dumps(r,indent=2)+'\\n'); print('Four fresh resource/domain diagnostic controls generated.')"
        run('regenerate_resource_controls',[sys.executable,'-c',resource_code])
        assert sha(stage/'ConcreteScalarCertificates.lean')==sha(author/'ConcreteScalarCertificates.lean')
        for f in (stage/'validation').glob('*.json'):
            assert read(f)==read(author/'validation'/f.name),f.name
        compile('ConcreteScalarCertificates');compile('DependencyAudit')
        run('review_cross_language_generate',[sys.executable,rstage/'crosscheck_implementation.py'],cwd=rstage)
        assert sha(rstage/'CrossLanguageReview.lean')==sha(review/'CrossLanguageReview.lean')
        assert sha(rstage/'validation/CROSS_LANGUAGE_CASES.json')==sha(review/'validation/CROSS_LANGUAGE_CASES.json')
        run('review_binding_attacks',[sys.executable,rstage/'test_binding_attacks.py'],cwd=rstage)
        for module in ['ChangedInputMustFail','FakeQMustFail','OpenCertificate']:
            assert sha(rstage/(module+'.lean'))==sha(review/(module+'.lean'))
        for module in ['IndependentControls','CrossLanguageReview','NonstandardControls','OpenCertificate','DependencyAudit']:
            compile(module,base=rstage,dest=rlib,label='review_'+module)
        for module in ['ChangedInputMustFail','FakeQMustFail']:
            compile(module,base=rstage,dest=rlib,label='review_'+module,negative=True)
    assert verify(args)==before, 'Prerequisites or frozen sources changed during replay'
    receipt={'status':'PASS_FRESH_EXTRACTED_ADDITION_REPLAY','strategy':'complete developments; no normal-order claim',
      'verification':before,'all_prerequisites_reverified_after':True,'reused_checked_objects':94,
      'predecessor_compilations':0,'new_successful_trust_zero_compilations':15,
      'expected_negative_trust_zero_compilations':2,'records':records,
      'source_export_rebound':True,'regenerated_certificates_byte_identical':True,
      'concrete_cases':read(stage/'validation/CONCRETE_SUMMARY.json'),
      'resource_outcomes':read(stage/'validation/REFUSAL_CONTROLS.json'),
      'review_cross_language_terms':len(read(rstage/'validation/CROSS_LANGUAGE_CASES.json')),
      'archive_source_bytes_unchanged':True,'log_sha256':sha(logpath),
      'limitations':read(ROOT/'REUSE_CONTRACT.json')['limitations']}
    (args.out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS: 94 objects rehashed/reused; 15 new accepted compilations; 2 expected rejections; no baseline rebuild.')
if __name__=='__main__':main()
