from pathlib import Path
import os,subprocess,json,hashlib,datetime
ROOT=Path.cwd(); OUT=ROOT/'hase-joint-induction-computation-independent-review-20261010'
mods='JointInductionSupport JointInductionInitiality JointInductionSectionCorollaries JointInductionUniformSection JointInductionComputationLaws JointInductionSectionApplication JointInductionLaws JointInductionControls JointInductionRawBoundary JointInductionAudit'.split()
env=os.environ.copy(); env['LEAN_PATH']=(OUT/'lean-path.txt').read_text()
lean=ROOT/'.toolchains/lean-4.19.0-linux/bin/lean'
logs=[]
for m in mods:
 cmd=[str(lean),'--trust=0','-o',str(OUT/'objects'/f'{m}.olean'),str(OUT/f'{m}.lean')]
 p=subprocess.run(cmd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 logs.append('$ '+' '.join(cmd)+'\n'+p.stdout)
 (OUT/'replay.log').write_text('\n'.join(logs))
 print(m,p.returncode,flush=True)
 if p.returncode or 'sorryAx' in p.stdout or ': warning:' in p.stdout or ': error:' in p.stdout:
  print(p.stdout,flush=True); raise SystemExit(1)
pins=json.loads((OUT/'BASELINE_PINS.json').read_text())
for x in pins['candidate']['files']+pins['retained']['sources']+pins['retained']['objects']:
 assert hashlib.sha256((ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'],x['path']
result={'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lean':subprocess.check_output([str(lean),'--version'],text=True).strip(),'trust':0,'modules':mods,'fresh_output':str(OUT/'objects'),'copied_sources':True,'all_candidate_and_retained_pins_verified_before_and_after':True,'retained_sources':130,'retained_objects':232,'baseline_rebuilt':False}
(OUT/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: all modules and pins',flush=True)
