"""Bind selected actual source reads and exact imported implementation bytes."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
WORK=HERE.parents[1]
CAT=WORK/'t20-consolidation-20261011/catalogue/objects'
REG=json.loads((WORK/'t20-consolidation-20261011/proofs/SOURCE_REGISTRY.json').read_text())['sources']
P=Path('recovery-20261011/remaining-archives/safe-extracts/rational-kernel-additive-preservation-20261011/rational-kernel-additive-preservation-20261011/payload')
rows=[]
def add(id,path,scope,ranges=None,expected=None,role='direct controlling source'):
    path=Path(path); p=WORK/path
    data=p.read_bytes();sha=hashlib.sha256(data).hexdigest()
    if expected and sha!=expected: raise ValueError((id,'source hash mismatch'))
    reg=REG.get('sha256:'+sha,{})
    rows.append({'id':id,'path':str(path),'sha256':sha,'bytes':len(data),'lines':len(data.decode().splitlines()),'read_scope':scope,'read_ranges':ranges,'role':role,'registry_source_id':'sha256:'+sha if reg else None,'original_provenance':reg.get('original_provenance',[])})
def obj(id,sha,scope='full owner text',ranges=None): add(id,Path('t20-consolidation-20261011/catalogue/objects')/sha[:2]/sha,scope,ranges,sha)
obj('PT01_PT02','71551ae962a17ec72709b6d36cfb58ed99237a2ef776339709a43b8d3b436d28')
obj('PT03','3d8d11d73055b62913cf36138cc0b3b273d032f8f927a885ee2af11bd8eaf459')
obj('PT04','67392fef19c436aa59b00a719698d5f2ecd877b4611c1a1c57c7bb445c6eb4ec')
obj('PT06_cost','d3f215e0073d5bbae42f3fa50711ba47484a13199df5ed3b7e98059d3fd15c98','selected mathematical/contract sections',[[1,125]])
obj('PT06_overlap','be28f2455521d4d09b95dd2e129ae846af6b6e55b6bd2b190985a227b2c1b6db')
obj('PT07','2a811338df1dc4f00e5376fb07b55dc6bafeda7e753890994f56a3492e8d06fa')
obj('PT07_review','949de5dc42bb2ceb44068c90a226f8b7f70aba6ab8faeb0f0ede4920e54deab0','selected review sections',[[1,80]])
obj('ET09','8aad39f6fb030620059edd4e0639f58078537a10181836b64089f6d82dbe10f4','contract/refinement and minimum-sidecar passages',[[1,90],[103,133]])
obj('ET14','c2ca691c70c953bd5e7af3f2e0d6a86f9ef72d7cf8996cb3b369bdd9afa1e1e1','complete dependency replay and warrant-survival sections; nearby bridge read for scope only',[[389,450]])
obj('ET17','7f0d42d87119221c01358874ddbd007e39c57f9cbd9f8f918d11cfffd15c6946')
obj('ET19','fef98acb62cd651dd97bf278645807e35dc519b30f977b701db797100bb065d3','timing diagnosis, actual contract and joint-correlation control',[[1,80]])
obj('CIRS','bd83f4c2bb1a41151405872a6aa57fe9bdc352f0b63db4cfb302e0068c8b0d4a')
obj('T16_Direct_reader','10903b3260522cec902c7213a1b93a2c3280922126994c76f95755baadc2a91e','selected actual source-reader sections, not whole T16',[[1952,1995],[2028,2048],[2153,2168]])
for tag,d in [('PT19','hase-finite-sidecar-realisation-20261011'),('PT20','hase-rational-kernel-transport-20261011')]:add(tag,P/d/'RESULT.md','full owner text')
add('PT21',P/'stochastic-exact-inquiry-20261010/RESULT.md','contract, proof and applications',[[1,190]])
add('PT20_python',P/'hase-rational-kernel-transport-20261011/rational_kernel.py','full executable source; not modified or used as a policy optimizer')
add('PT28_bridge','literal-shift-kernel-refinement-20261011/SOURCE_BRIDGE.md','full source-to-kernel boundary')
add('PT29','literal-shift-probability-20261011/RESULT.md','full owner result; no fresh Lean replay')
add('PR_compiler',P/'hase-open-term-standardness-20261010/sources/EffectivePrimitiveRecursion.lean','actual PR constructors, semantics, compiler typing and computational adequacy',[[1,240],[288,307]])
add('PR_arithmetic',P/'hase-imported-compiler-transport-20261010/sources/RestrictedCompiler.lean','actual arithmetic/zero-choice descriptions and denotation proofs',[[15,92]])
add('PR_comparison',P/'hase-imported-compiler-transport-20261010/sources/PolynomialTestBoundary.lean','comparison descriptions and denotation proofs; later boundary text read for context',[[1,180]])
add('PR_lookup',P/'hase-finite-sidecar-realisation-20261011/FiniteCorrectionTable.lean','full actual finite-table source')
add('PR_record',P/'hase-finite-sidecar-realisation-20261011/SourceSidecarController.lean','record carrier, numeric projections and source observer construction',[[1,90]])
base=Path('t20-consolidation-20261011/catalogue/archive-views/T20_Guarded_Shared_Proof_Attainment_Supplement_20261009.zip--1c5155b94388/T20_Guarded_Shared_Proof_Attainment_Supplement_20261009')
copies=[]
for id,path in [('guarded_dag','guarded-shared-dag-attainment-20261009/guarded_dag.py'),('guarded_compiler','source-sensitive-proof-compilation-20261009/guarded_compiler.py'),('whole_dag_compiler','certificate-compilation-boundary-20261009/compiler.py')]:
    add(id,base/path,'full executable source; direct import via exact local copy',role='unchanged executable dependency')
    copy=HERE/'inherited'/path
    if copy.read_bytes()!=(WORK/base/path).read_bytes(): raise ValueError('Imported copy mismatch')
    copies.append({'source_id':id,'copy_path':str(copy.relative_to(HERE)),'sha256':hashlib.sha256(copy.read_bytes()).hexdigest()})
metadata=[]
for path in ('t20-consolidation-20261011/proofs/SOURCE_REGISTRY.json','t20-consolidation-20261011/proofs/PROOF_TYPE_INQUIRY_CLAIMS.json','t20-consolidation-20261011/evidence/SOURCE_MAP.json','t20-consolidation-20261011/evidence/MATERIAL_CLAIMS.json','t20-consolidation-20261011/coverage/pinned-baseline/SOURCE_MAP.json'):
    data=(WORK/path).read_bytes();metadata.append({'path':path,'sha256':hashlib.sha256(data).hexdigest(),'use':'source navigation and scope; no body-read credit inferred'})
out={'schema':'t20.proof-inquiry.source-bindings.v1','sources':rows,'unchanged_import_copies':copies,'navigation_metadata':metadata,'explicit_read_limits':['No whole-corpus read or complete originality search.','PT05 kernel correctness and PT23–27 scopes were inspected in the claim register, not freshly source-audited here.','No inherited or new Lean replay. Actual Has representability is an ordinary deduction from selected source interfaces.','Source-preservation checking does not establish real-world source authentication or substantive rule admission.']}
(HERE/'SOURCE_BINDINGS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'bound_sources':len(rows),'exact_dependency_copies':len(copies)}))
