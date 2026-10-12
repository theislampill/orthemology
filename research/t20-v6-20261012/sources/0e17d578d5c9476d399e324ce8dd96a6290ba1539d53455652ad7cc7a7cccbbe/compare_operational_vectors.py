import pathlib, hashlib, importlib.util, sys, ast, re, json
root=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('recovered_p02',root/'codec-source/prcodec.py')
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
r=pathlib.Path((root/'LATEST_OPERATIONAL_MACHINE_QUALIFICATION.txt').read_text().strip()).parent
s=(r/'build-UniformComputabilityControls.stdout').read_text();s=s[:s.index("\n'P02.Codec")]
expected=dict(ast.literal_eval(re.sub(r'\bsome (\d+)',r'\1',s)))
C,V,E,S,Seq,Loop,If=m.C,m.V,m.E,m.Set,m.Seq,m.Loop,m.If
programs={
'captured-count':m.Program(2,2,Seq(S(2,C(0)),Loop(3,V(0),Seq(S(0,C(0)),S(2,E('add',V(2),C(1))))))),
'overwrite-index':m.Program(2,2,Loop(3,V(0),Seq(S(2,V(3)),S(3,C(99))))),
'arithmetic':m.Program(2,2,S(2,E('add',E('mul',V(0),V(1)),E('add',E('sub',V(0),V(1)),E('add',E('div',V(1),C(0)),E('add',E('mod',V(0),C(0)),E('add',E('le',V(0),V(1)),E('add',E('eq',V(0),V(1)),E('pow2',C(2)))))))))),
'branch':m.Program(2,2,If(V(0),S(2,C(1)),S(2,C(0))))}
actual={name:[m.evaluate_index(m.encode(p),n,2 if name=='arithmetic' else 0) for n in range(6)] for name,p in programs.items()}
assert actual==expected,(actual,expected)
resource=False
try:m.evaluate_index(m.encode(m.Program(2,2,S(2,C(1)))),0,0,step_limit=0)
except m.ResourceLimit:resource=True
assert resource
out={'status':'PASS','numeric_execution_comparisons':24,'vectors':actual,'exhaustion_raises_ResourceLimit':True,'source_sha256':hashlib.sha256((root/'codec-source/prcodec.py').read_bytes()).hexdigest(),'lean_controls_source_sha256':hashlib.sha256((root/'UniformComputabilityControls.lean').read_bytes()).hexdigest(),'scope':'Bounded independent recovered-Python comparison; fuel step counts are not identified with Python Meter ticks.'}
(root/'receipts/OPERATIONAL_SOURCE_COMPARISON.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
