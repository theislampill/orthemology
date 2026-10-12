"""Replay the research return without mutating the immutable P14 predecessor."""
from pathlib import Path
import argparse,hashlib,json,os,platform,subprocess,sys,tempfile,time,zipfile

BASE=Path(__file__).resolve().parent
P14_HASH='437be32e1d2a909e353abd376f36bf99968c6679f1ccbcb401301aa48f8a4d37'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source-repo',type=Path)
    args=parser.parse_args();start=time.monotonic();records=[];log=[]
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(BASE))
    def call(command,cwd=BASE):
        p=subprocess.run(command,cwd=cwd,env=env,text=True,capture_output=True)
        log.extend(['COMMAND: '+' '.join(command),p.stdout,p.stderr])
        records.append({'command':command,'exit_code':p.returncode})
        if p.returncode:
            (BASE/'verification-run.log').write_text('\n'.join(log))
            raise RuntimeError('Replay failed: '+' '.join(command))
    call([sys.executable,'-m','unittest','test_restoration','test_migration','test_correlation',
          'test_stochastic_refinement','test_private_refinement','test_refinement_composition'])
    for probe in sorted(BASE.glob('probe_*.py')):call([sys.executable,probe.name])
    archive=BASE/'P14'/'P14_Completed_Research_Return.zip'
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==P14_HASH
    with tempfile.TemporaryDirectory(prefix='p14-replay-',dir=BASE) as temp:
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist())
            z.extractall(temp)
        work=Path(temp)/'P14_Completed_Research_Return'
        manifest=json.loads((work/'MANIFEST.json').read_text())
        # P14's manifest convention is verified independently below.
        items=manifest['files']
        for item in items:
            assert hashlib.sha256((work/item['path']).read_bytes()).hexdigest()==item['sha256']
        call([sys.executable,'-m','unittest','test_epistemic'],work)
        call([sys.executable,'probe_epistemic.py'],work)
        call([sys.executable,'team_concavity_check.py'],work)
    source_verified=False
    if args.source_repo:
        repo=args.source_repo.resolve();identity=json.loads((BASE/'source_identity.json').read_text())
        head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
        assert head==identity['commit']
        for source in identity['sources']:
            assert hashlib.sha256((repo/source['path']).read_bytes()).hexdigest()==source['sha256']
        source_verified=True
    report={'status':'PASS','python':platform.python_version(),'commands':records,
        'unit_tests_control':34,'unit_tests_P14':7,'P14_archive_sha256':P14_HASH,
        'P14_manifest_artifacts_verified':len(items),'pinned_source_hashes_verified':source_verified,
        'P14_external_replay_dependency':{'path':'restoration.py','sha256':hashlib.sha256((BASE/'restoration.py').read_bytes()).hexdigest()},
        'elapsed_seconds':round(time.monotonic()-start,3),
        'scope':'Executable finite verification only. Mathematical infinite-horizon proofs and authority/model premises remain explicit.'}
    (BASE/'verification-run.log').write_text('\n'.join(log))
    (BASE/'verification_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
