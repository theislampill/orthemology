"""Disclosed in-memory adaptation: omit only two excluded primary-body hashes.
All source scripts remain byte-for-byte unchanged; never claim source replay.
"""
from pathlib import Path
import ast,hashlib,json,sys
if len(sys.argv)<2:raise SystemExit('Usage: portable_predictive_adapter.py ORIGINAL_SCRIPT [original arguments]')
p=Path(sys.argv[1]).resolve();source=p.read_text()
if hashlib.sha256(p.read_bytes()).hexdigest()!='58d3138673cdd81f24cda97d5bc30c1e5ebf1846f5586d1ac7b46ec4caec6590':raise RuntimeError('Unexpected original predictive verifier identity')
tree=ast.parse(source,str(p));removed=0;marked=0
for i,node in enumerate(tree.body):
 if isinstance(node,ast.For) and isinstance(node.iter,ast.Subscript) and isinstance(node.iter.value,ast.Name) and node.iter.value.id=='bindings' and isinstance(node.iter.slice,ast.Constant) and node.iter.slice.value=='primary_sources':
  tree.body[i]=ast.copy_location(ast.Pass(),node);removed+=1
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Subscript) and isinstance(t.value,ast.Name) and t.value.id=='results' and isinstance(t.slice,ast.Constant) and t.slice.value=='input_bindings_reverified' for t in node.targets):
  node.value=ast.Constant(False);marked+=1
if removed!=1 or marked!=1:raise RuntimeError('Expected precise source-hash loop and status assignment not found')
# Insert a clear disclosure before output serialization. The inherited-input
# snapshot and original checks still execute and must succeed normally.
extra=ast.parse("results['portable_replay']={'all_mathematical_checks_active': True, 'inherited_original_and_snapshot_hashes_reverified': True, 'primary_source_body_checks_replayed': False, 'omitted_primary_hash_checks': 2, 'full_source_replay_reproduced': False, 'method': 'Exact source-body hash loop omitted in memory; original script unchanged'}").body
for i,node in enumerate(tree.body):
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Subscript) and isinstance(t.value,ast.Name) and t.value.id=='results' and isinstance(t.slice,ast.Constant) and t.slice.value=='optimization_level' for t in node.targets):
  tree.body[i+1:i+1]=extra;break
else:raise RuntimeError('Disclosure insertion point missing')
ast.fix_missing_locations(tree);sys.argv=[str(p)]+sys.argv[2:]
exec(compile(tree,str(p),'exec'),{'__name__':'__main__','__file__':str(p),'__builtins__':__builtins__})
