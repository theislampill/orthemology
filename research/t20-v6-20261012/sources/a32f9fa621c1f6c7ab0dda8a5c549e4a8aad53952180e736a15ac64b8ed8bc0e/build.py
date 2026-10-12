#!/usr/bin/env python3
import pathlib,json,subprocess,os,datetime,hashlib,sys
root=pathlib.Path(__file__).resolve().parent
packet=root.parent/'shadow-packet'
project=root/'project'; artifacts=root/'artifacts'
lib=pathlib.Path('private-locator:41bd9f979012c8bbc235')
paths=[artifacts,lib/'.lake/build/lib/lean']+[p/'.lake/build/lib/lean' for p in (lib/'.lake/packages').iterdir()]
env=dict(os.environ);env['LEAN_PATH']=':'.join(map(str,paths))
lean='private-locator:4211d241978f643cb623'
order=json.loads((packet/'formal/SOURCE_INVENTORY.json').read_text())['build_order']
if len(sys.argv)>1: order=sys.argv[1:]
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S')
log=root/'logs'/stamp;log.mkdir()
for module in order:
 src=packet/'formal'/(module+'.lean')
 if not src.exists():src=packet/'formal/vendor'/(module+'.lean')
 (project/src.name).write_bytes(src.read_bytes())
 p=subprocess.run([lean,'-j1','-o',str(artifacts/(module+'.olean')),src.name],cwd=project,env=env,capture_output=True,text=True,timeout=90)
 (log/(module+'.stdout')).write_text(p.stdout);(log/(module+'.stderr')).write_text(p.stderr)
 (log/(module+'.json')).write_text(json.dumps({'module':module,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'returncode':p.returncode,'command':[lean,'-j1','-o',str(artifacts/(module+'.olean')),src.name]},indent=2))
 print(module,p.returncode,flush=True)
 if p.returncode:print(p.stdout,p.stderr,flush=True);sys.exit(p.returncode)
print('ALL_SELECTED_MODULES_ELABORATED',len(order))
