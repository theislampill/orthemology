from pathlib import Path
import json,hashlib,zipfile,subprocess,sys,platform,shutil,os
root=Path('private-locator:4c8bc74717a70d6fa8d2'); out=Path('private-locator:1dc82187dd31bb556614'); p=Path('private-locator:a516cf88ef66ba04ead5')
sha=lambda b:hashlib.sha256(b).hexdigest()
checks=[]
for name,key in [('CHECKPOINT_MANIFEST.json','files'),('RECEIPT.json','output_hashes')]:
 entries=json.loads((root/name).read_text())[key]
 for r in entries:
  b=(root/r['path']).read_bytes(); ok=len(b)==r['bytes'] and sha(b)==r['sha256']; checks.append({'kind':name,'path':r['path'],'ok':ok})
inv=json.loads((root/'SOURCE_INVENTORY.json').read_text())
for r in inv:
 b=(root/r['packet_path']).read_bytes(); blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 checks.append({'kind':'source_sha256_blob','path':r['packet_path'],'ok':len(b)==r['bytes'] and sha(b)==r['sha256'] and blob==r['git_blob'],'recorded_mode':r['git_mode'],'mode_scope':'metadata retained; checkout not claimed'})
proj=json.loads((root/'accepted-evidence/PROJECTION_BINDINGS.json').read_text())
for r in proj:
 b=(root/r['packet_path']).read_bytes(); checks.append({'kind':'accepted_projection','path':r['packet_path'],'ok':len(b)==r['bytes'] and sha(b)==r['sha256']})
for o in json.loads((root/'OBLIGATIONS.json').read_text()):
 for r in o['source_bindings']:
  b=(root/r['packet_path']).read_bytes();checks.append({'kind':'obligation_binding','id':o['id'],'path':r['packet_path'],'ok':len(b)==r['bytes'] and sha(b)==r['sha256']})
receipt_ok=sha((root/'RECEIPT.json').read_bytes())==(root/'RECEIPT.json.sha256').read_text().split()[0]
with zipfile.ZipFile(p) as z:
 crc=z.testzip(); names=z.namelist(); members=[{'path':i.filename,'bytes':i.file_size,'sha256':sha(z.read(i))} for i in z.infolist()]
r={'input_path':str(p),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'members':len(names),'uncompressed_bytes':sum(x['bytes'] for x in members),'crc_error':crc,'receipt_digest_ok':receipt_ok,'binding_checks':len(checks),'failures':[c for c in checks if not c['ok']],'source_files':len(inv),'projection_bindings':len(proj),'manifest_omissions':sorted(set(names)-{r['path'] for r in json.loads((root/'CHECKPOINT_MANIFEST.json').read_text())['files']}),'all_input_members':members,'checks':checks,'status':'PASS' if receipt_ok and crc is None and all(x['ok'] for x in checks) else 'FAIL'}
(out/'evidence/INPUT_VERIFICATION.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k not in ['all_input_members','checks']},indent=2))
env={'python':sys.version,'platform':platform.platform(),'machine':platform.machine(),'PATH':os.environ.get('PATH'),'tools':{n:shutil.which(n) for n in ['lean','lake','elan','git','curl']},'toolchain_claim':'NO_LOCAL_LEAN_LOCATED'}
(out/'evidence/ENVIRONMENT.json').write_text(json.dumps(env,indent=2)+'\n');print(json.dumps(env,indent=2))
shutil.copy2('private-locator:1c436067a8eb1eaa34ba',out/'provenance/verify_input.py')
