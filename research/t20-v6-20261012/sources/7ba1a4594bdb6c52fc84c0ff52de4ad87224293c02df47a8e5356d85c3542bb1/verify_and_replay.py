"""Verify preserved evidence, replay in three fresh copies, retain a receipt."""
from pathlib import Path
import argparse,datetime,hashlib,importlib.metadata,json,os,shutil,subprocess,sys,tempfile

ROOT=Path(__file__).resolve().parent
NAMES=['noetic-correction-semantics-20261009','noetic-guard-peer-review-20261009','noetic-guard-repair-peer-review-20261009']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(base):
    count=0
    for line in (base/'SHA256SUMS').read_text().splitlines():
        expected,relative=line.split('  ',1)
        p=(base/relative).resolve()
        if not p.is_relative_to(base.resolve()):raise RuntimeError('Unsafe manifest path: '+relative)
        if not p.is_file() or sha(p)!=expected:raise RuntimeError('Hash mismatch: '+str(p))
        count+=1
    return count

def main():
    if not __debug__:raise RuntimeError('Do not run this replay with Python optimization enabled')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only',action='store_true')
    parser.add_argument('--work-dir',type=Path)
    args=parser.parse_args()
    verified={'root':verify(ROOT)}
    for name in NAMES:verified[name]=verify(ROOT/'evidence'/name)
    if args.verify_only:
        print(json.dumps({'status':'PASS','mode':'verify-only','files_verified':verified,'manifest_sha256':sha(ROOT/'SHA256SUMS')},indent=2));return
    if not shutil.which('patch'):raise RuntimeError('Required executable unavailable: patch')
    version=importlib.metadata.version('jsonschema')
    if version!='4.26.0':raise RuntimeError('Replay requires the recorded jsonschema version 4.26.0; found '+version)
    if args.work_dir:
        work=args.work_dir.resolve()
        if work.exists():raise RuntimeError('Work directory already exists; select an unused path')
        if work.is_relative_to(ROOT):raise RuntimeError('Work directory must be outside the extracted packet')
        work.mkdir(parents=True)
    else:work=Path(tempfile.mkdtemp(prefix='noetic-guard-replay-'))
    logs=work/'command-logs';logs.mkdir()
    def fresh(group):
        target=work/group
        shutil.copytree(ROOT/'evidence',target)
        return target
    commands=[]
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'};env.pop('PYTHONOPTIMIZE',None)
    def run(label,script):
        command=[sys.executable,'-B',str(script)]
        p=subprocess.run(command,cwd=script.parent,capture_output=True,text=True,env=env)
        record={'label':label,'command':command,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
        dest=logs/(label+'.json');dest.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
        commands.append({'label':label,'exit_code':p.returncode,'log':str(dest)})
        if p.returncode:raise RuntimeError(label+' failed; see '+str(dest))
    author=fresh('author-replay')
    for script in ('check_boundary.py','check_full_path.py','check_candidate_repair.py'):
        run('author-'+script[:-3],author/NAMES[0]/script)
    peer=fresh('finding-review-replay');run('independent-finding',peer/NAMES[1]/'replay_peer.py')
    repair=fresh('repair-review-replay');run('independent-repair',repair/NAMES[2]/'replay_repair.py')
    result=json.loads((repair/NAMES[2]/'REPAIR_PEER_RESULTS.json').read_text())
    status=json.loads((ROOT/'STATUS.json').read_text())
    for key in ('preimage_sha256','postimage_sha256'):
        if result[key]!=status[key]:raise RuntimeError('Unexpected candidate '+key)
    if result['candidate_patch_sha256']!=status['patch_sha256']:raise RuntimeError('Unexpected patch hash')
    for name in NAMES:verify(ROOT/'evidence'/name)
    verify(ROOT)
    receipt={'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'packet_status':'T20_INTERMEDIATE_RESEARCH_RESULT','repository_integration':False,'T20_closed':False,
      'manifest_sha256':sha(ROOT/'SHA256SUMS'),'files_verified':verified,'python':sys.version,'jsonschema':version,
      'work_directory':str(work),'commands':commands,'original_archived_evidence_unchanged':True,
      'frozen_commit':status['frozen_commit'],'patch_sha256':status['patch_sha256'],
      'preimage_sha256':result['preimage_sha256'],'postimage_sha256':result['postimage_sha256'],
      'results':{'author':str(author/NAMES[0]),'finding_review':str(peer/NAMES[1]/'PEER_REVIEW_RESULTS.json'),
      'repair_review':str(repair/NAMES[2]/'REPAIR_PEER_RESULTS.json')},
      'limits':'Two-entry generated-map projection, synthetic structural tests, no whole runtime/CI/schema completeness or human-state claims'}
    (work/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
