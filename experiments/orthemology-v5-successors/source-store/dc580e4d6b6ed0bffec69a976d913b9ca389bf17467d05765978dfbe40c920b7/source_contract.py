#!/usr/bin/env python3
"""Exact source/AST identity verifier; NOT a Python semantics proof or extractor."""
from pathlib import Path
import ast,hashlib,json,sys
ROOT=Path(__file__).resolve().parent
EXPECTED_SOURCE='dd79f63f5af91bbe1c3695fa401a41a726b224fa5e3d80aa9c589de95949da6c'
sha=lambda b:hashlib.sha256(b).hexdigest()
def validate(source:str)->dict:
    pins=json.loads((ROOT/'spec/SOURCE_AST_PINS.json').read_text())
    if pins['source_sha256']!=EXPECTED_SOURCE: raise ValueError('Source contract pin drift')
    actual_source=sha(source.encode())
    if actual_source!=EXPECTED_SOURCE: raise ValueError('Pinned source changed')
    try:tree=ast.parse(source)
    except SyntaxError as exc:raise ValueError('Python parse failed') from exc
    nodes={n.name:n for n in tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef))}
    seen={}
    for name,pin in pins['nodes'].items():
        if name not in nodes:raise ValueError('Missing pinned node: '+name)
        node=nodes[name];actual=sha(ast.dump(node,annotate_fields=True,include_attributes=False).encode())
        if actual!=pin['sha256']:raise ValueError('AST shape changed: '+name)
        if node.lineno!=pin['start_line'] or node.end_lineno!=pin['end_line']:raise ValueError('Source range changed: '+name)
        seen[name]={'sha256':actual,'start_line':node.lineno,'end_line':node.end_lineno}
    return {'status':'PASS_EXACT_SOURCE_SHAPE','source_sha256':actual_source,'nodes':seen,
            'semantic_extraction_verified':False,'cp_python_verified':False,
            'scope':'Identity and source drift detection only; see SOURCE_CORRESPONDENCE.md'}
if __name__=='__main__':
    source=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'source/prcodec.py'
    print(json.dumps(validate(source.read_text()),indent=2))
