#!/usr/bin/env python3
import pathlib,json,hashlib,subprocess,datetime
ROOT=pathlib.Path(__file__).resolve().parent
WORK=ROOT.parent
MANIFEST=ROOT/'SOURCE_BOUNDARY.json'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    data=json.loads(MANIFEST.read_text())
    records=data['retained']+data['additive']
    def check():
        for row in records:
            p=WORK/row['path']
            if digest(p)!=row['sha256']: raise RuntimeError('Input changed: '+row['path'])
    check()
    p=subprocess.run(['bash',str(ROOT/'check.sh')],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (ROOT/'validation/pinned-replay.log').write_text(p.stdout)
    if p.returncode: raise RuntimeError(p.stdout)
    check()
    pinned={str((WORK/r['path']).resolve()) for r in data['retained']}
    imported=[]
    for line in p.stdout.splitlines():
        if not line.startswith('IMPORTED '): continue
        name=line.removeprefix('IMPORTED ').strip()
        if name in ['JointProofUniqueness','OriginalProofUniqueness','ProofUniquenessControls']:continue
        rel=pathlib.Path(*name.split('.')).with_suffix('.olean')
        found=next((pathlib.Path(d)/rel for d in data['lean_path'].split(':') if (pathlib.Path(d)/rel).is_file()),None)
        if found:
            if str(found.resolve()) not in pinned:raise RuntimeError('Unpinned import '+name)
            imported.append({'module':name,'object':str(found.relative_to(WORK)),'sha256':digest(found)})
        else:
            std=WORK/'.toolchains/lean-4.19.0-linux/lib/lean'/rel
            if not std.is_file():raise RuntimeError('Unresolved import '+name)
            imported.append({'module':name,'toolchain_object':str(std.relative_to(WORK)),'sha256':digest(std)})
    receipt={'status':'PASS','checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest_sha256':digest(MANIFEST),'retained_pin_count':len(data['retained']),'actual_import_closure':imported,'output':p.stdout.splitlines()[-1],'command':['bash',str(ROOT/'check.sh')]}
    (ROOT/'validation/REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('PASS: fresh trust-zero compile, input pins before/after, actual imported closure checked.')
if __name__=='__main__':main()
