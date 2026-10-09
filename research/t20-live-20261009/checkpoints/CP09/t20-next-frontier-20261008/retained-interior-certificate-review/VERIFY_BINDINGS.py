from pathlib import Path
import hashlib,json,datetime,subprocess
BASE=Path('..').resolve()
AUTHOR=BASE/'retained-interior-certificate'
expected={'RESULT.md':'9314e6ec0c15024aeefa10e2ff222e77f66b2358b5fbf9883e4c07a267632226','RetainedInterior.lean':'85a487cd9041cc46d319a7f239ba77f911293eb922ca8dc9f97e60e98cbc170a','controls.py':'8b88ebefafedf4afdee817f73420870648b5b162ffb0ad8e6699b4a2aab9dced','verify_kernel.sh':'fa3eb5e78bcbd956962ab55889868d74906bfd11305c99b201aa3a91a24585b7','CONTROL_RESULTS.json':'a3e4120b7146789bf5f076c1a3fe1ec6d98752a1719fcc9b7f5ab36bbc62c97f'}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while data:=f.read(1048576):h.update(data)
 return h.hexdigest()
for path,d in expected.items():assert sha(AUTHOR/path)==d,path
mods=json.loads((AUTHOR/'IMPORTED_MODULE_BINDINGS.json').read_text())
assert len(mods)==1798
names=[line.removeprefix('IMPORT ') for line in Path('IMPORTS_REPLAY.log').read_text().splitlines() if line.startswith('IMPORT ')]
assert len(names)==1798 and set(names)=={x['module'] for x in mods}
files=0
for item in mods:
 for field in ['source','olean']:
  assert sha(BASE/item[field])==item[field+'_sha256'],(item['module'],field)
  files+=1
deps=json.loads((AUTHOR/'KERNEL_DEPENDENCIES.json').read_text())
for path,d in deps['files'].items():assert sha(BASE/path)==d,path
assert sha(AUTHOR/'IMPORTED_MODULE_BINDINGS.json')==deps['imported_module_manifest_sha256']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=BASE/'formal-identification/mathlib',text=True).strip()==deps['mathlib_commit']
meta=['SOURCE_AUDIT.md','NEGATIVE_CONTROLS.md','READ_FIRST.md','KERNEL_DEPENDENCIES.json','IMPORTED_MODULE_BINDINGS.json','SOURCE_BINDINGS.json','ImportInventory.lean']
bindings={**expected,**{f:sha(AUTHOR/f) for f in meta}}
result={'verdict':'PASS: final mathematical report, source-specific kernel, independent controls and dependency identities reviewed','checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'author_directory':'retained-interior-certificate','artifacts':bindings,'replayed_import_count':len(names),'individually_rehashed_import_source_and_binary_files':files,'compiler_runtime_and_metadata_files_rehashed':len(deps['files']),'scope':'Bindings verify exact local identities; not an upstream rebuild or physical/model validation.'}
Path('FINAL_ARTIFACT_BINDINGS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
