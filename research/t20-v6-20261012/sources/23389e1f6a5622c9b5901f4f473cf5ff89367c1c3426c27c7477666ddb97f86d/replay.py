import pathlib,os,subprocess,json,hashlib,time
W=pathlib.Path(__file__).resolve().parent.parent
R=pathlib.Path(__file__).resolve().parent
L=W/'.toolchains/lean-4.19.0-linux/bin/lean'
paths=[R/'fresh-lib',W/'homogeneous-per-model-20261010',W/'review-henkin-source-model-20261010/independent-9tbc2axj',W/'hase-closed-scalar-review-20261010/fresh-lib']+[pathlib.Path(x) for x in (W/'hase-graph-bridge-assembly-20261010/lean_path.txt').read_text().strip().split(':')]
(R/'lean_path.txt').write_text(':'.join(map(str,paths)))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
modules=['GenericFoldTransport','SourceFoldContract','SourceFoldApplication','NaturalityBoundary','RecursorUniqueness','InternalRecursorPrinciple','SourceRigidity','RigidityDiscriminator','ClosedInstanceBoundary','IndependentControls','DependencyAudit']
for m in modules:
 p=R/'sources'/f'{m}.lean'; o=R/'fresh-lib'/f'{m}.olean'; cmd=[str(L),'--trust=0','-o',str(o),str(p)]
 start=time.time(); x=subprocess.run(cmd,env={**os.environ,'LEAN_PATH':':'.join(map(str,paths))},capture_output=True,text=True)
 log=R/'logs'/f'{m}.log';log.write_text(x.stdout+x.stderr)
 records.append({'module':m,'command':cmd,'exit_code':x.returncode,'seconds':time.time()-start,'source_sha256':sha(p),'log_sha256':sha(log),'object_sha256':sha(o) if o.exists() else None})
 print(m,x.returncode,flush=True)
 (R/'REPLAY.json').write_text(json.dumps(records,indent=2)+'\n')
 if x.returncode:raise SystemExit(x.returncode)
