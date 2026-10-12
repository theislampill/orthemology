#!/usr/bin/env python3
from pathlib import Path
import json,os,subprocess,hashlib,re,datetime,time
R=Path(__file__).resolve().parent
q=json.loads((R/'RECEIPT.json').read_text());assert q['status']=='FRESH_BUILD_AND_EXACT_READBACK_PASS'
L=q['compiler']['path'];env=dict(os.environ,LEAN_PATH=q['lean_path'])
H=lambda b:hashlib.sha256(b).hexdigest()
ev=R/'evidence';s=R/'sources';a=R/'artifacts'
out={'schema':'independent-canonical-carrier-scope-controls-v1','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':[]}
def run(name,expected=0):
 cmd=[L,'-j1','-o',str(a/(name+'.olean')),name+'.lean'];t=time.monotonic()
 p=subprocess.run(cmd,cwd=s,env=env,capture_output=True,text=True,timeout=120)
 for stream in ['stdout','stderr']:(ev/(name+'.'+stream)).write_text(getattr(p,stream))
 row={'module':name,'command':cmd,'source_sha256':H((s/(name+'.lean')).read_bytes()),'exit_code':p.returncode,'expected_exit_code':expected,'elapsed_seconds':time.monotonic()-t,'stdout_sha256':H(p.stdout.encode()),'stderr_sha256':H(p.stderr.encode())}
 if (a/(name+'.olean')).exists():row['artifact_sha256']=H((a/(name+'.olean')).read_bytes())
 out['runs'].append(row);(ev/(name+'.json')).write_text(json.dumps(row,indent=2)+'\n')
 print(name,p.returncode,p.stdout,p.stderr,flush=True)
 assert p.returncode==expected
 assert 'sorryAx' not in p.stdout+p.stderr and 'declaration uses' not in p.stdout+p.stderr
 return p.stdout
try:
 run('ScopeControls')
 names=re.findall(r'^theorem ([A-Za-z0-9_]+)',(s/'ScopeControls.lean').read_text(),re.M)
 audit=['import ScopeControls','import Lean','set_option pp.universes true','set_option format.width 120']
 for n in names:
  n='IndependentCarrierAudit.'+n;audit.extend([f'#check {n}',f'#print axioms {n}'])
 (s/'ScopeReadback.lean').write_text('\n'.join(audit)+'\n');result=run('ScopeReadback')
 assert len(re.findall(r"depends on axioms:|does not depend on any axioms",result))==len(names)
 used=set()
 for line in re.findall(r'depends on axioms: \[([^\]]*)\]',result):used.update(x.strip() for x in line.split(','))
 assert used<={'propext','Quot.sound','Classical.choice'}
 out.update(status='PASS',proved_controls=len(names),controls=names,axiom_union=sorted(used))
 # Deliberately false generalisations must fail in independent isolated files.
 negative={
 'RejectGeneralPi':'example : carrierCode (PiPER totalPER (fun _ => rawPER) (fun _ => rfl)) = dependentPi (carrierCode totalPER) (carrierFamily (fun _ => rawPER) (fun _ => rfl)) := by\n  exact raw_pi_carrier_square (fun _ => rawPER) (fun _ => rfl)\n',
 'RejectGeneralIdentity':'example : carrierCode (IdPER totalPER .i P01DF.skk) = equalityCode (carrierCode totalPER) .i P01DF.skk := by\n  exact raw_identity_carrier_square .i P01DF.skk\n',
 'RejectRawEta':'example : Conv Term.i P01DF.skk := by\n  exact Eq.refl _\n'}
 for n,b in negative.items():
  (s/(n+'.lean')).write_text('import P01CanonicalCarrierProjection\nopen OrthemologyV2 OrthemologyV3 P01D P01R P01DF\n'+b)
  text=run(n,1);assert 'error: type mismatch' in text
  assert not (a/(n+'.olean')).exists()
 out['expected_rejected_controls']=list(negative)
except Exception as e:
 out.update(status='FAILED',failure=repr(e));raise
finally:
 out['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();out['driver_sha256']=H(Path(__file__).read_bytes());(R/'CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
