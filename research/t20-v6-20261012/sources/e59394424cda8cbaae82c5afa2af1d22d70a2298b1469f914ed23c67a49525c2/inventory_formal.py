#!/usr/bin/env python3
"""Create an exact source/declaration inventory, never a kernel certificate."""
from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'handoff'))
from qualify_lean419 import code_only,source_lint,GateError,PIN,MATHLIB

def H(b):return hashlib.sha256(b).hexdigest()

def declarations(path):
    text=path.read_text();clean=code_only(text);scopes=[];rows=[];private=[]
    lines=text.splitlines();code=clean.splitlines()
    for i,line in enumerate(code):
        x=re.fullmatch(r'\s*(namespace|section)\s*([A-Za-z0-9_.]*)\s*',line)
        if x:scopes.append(x.groups());continue
        if re.fullmatch(r'\s*end(?:\s+[A-Za-z0-9_.]+)?\s*',line):
            if not scopes:raise GateError('unmatched end '+path.name+':'+str(i+1))
            scopes.pop();continue
        x=re.match(r'\s*(?:@\[[^]]*\]\s*)*(?:(private|protected|noncomputable)\s+)?(def|abbrev|theorem|lemma|structure|inductive)\s+([A-Za-z][A-Za-z0-9_.]*)',line)
        if not x:continue
        qualifier,kind,name=x.groups()
        full='.'.join([n for t,n in scopes if t=='namespace']+[name])
        row={'name':full,'kind':kind,'module':path.stem,'path':path.relative_to(ROOT).as_posix(),
             'line':i+1,'qualifier':qualifier,'declaration_start_text':lines[i]}
        if qualifier=='private':private.append(row)
        else:rows.append(row)
    if scopes:raise GateError('unclosed namespace/section '+path.name)
    return rows,private

new=sorted(p for p in (ROOT/'formal').glob('P01*.lean') if p.stem!='P01Audit')
modules={p.stem:p for p in new}
modules.update({p.stem:p for p in (ROOT/'formal'/'vendor').glob('*.lean')})
targets=[];privates=[];lint=[]
for p in new:
    source_lint(p.read_text())
    ts,ps=declarations(p);targets.extend(ts);privates.extend(ps)
    lint.append({'path':p.relative_to(ROOT).as_posix(),'status':'STATIC_HYGIENE_PASS','kernel_credit':False})
if len({t['name'] for t in targets})!=len(targets):raise GateError('duplicate declaration names')
deps={name:[] for name in modules}
for name,p in modules.items():
    for line in code_only(p.read_text()).splitlines():
        m=re.match(r'^import\s+(.+)',line)
        if m:
            for imp in m.group(1).split():
                if imp in modules:deps[name].append(imp)
                elif not imp.startswith(('Mathlib','Lean','Std','Init')):
                    raise GateError('unresolved local import '+name+' -> '+imp)
order=[];visiting=set();done=set()
def visit(n):
    if n in visiting:raise GateError('formal import cycle '+n)
    if n in done:return
    visiting.add(n)
    for d in deps[n]:visit(d)
    visiting.remove(n);done.add(n);order.append(n)
for n in sorted(modules):visit(n)
audit=['/- Generated exact target readback; compiler output is mandatory. -/']
for module in sorted({t['module'] for t in targets}|{'AuditSupport'}):audit.append('import '+module)
audit.extend(['set_option pp.universes true','set_option pp.width 120'])
for t in targets:
    n=t['name'];audit.extend([f'#eval IO.println "AUDIT_BEGIN {n}"',f'#check {n}',f'#ortho_audit {n}',f'#print axioms {n}',f'#eval IO.println "AUDIT_END {n}"'])
(ROOT/'formal'/'P01Audit.lean').write_text('\n'.join(audit)+'\n')
files=[]
for p in sorted((ROOT/'formal').rglob('*')):
    if not p.is_file() or not(p.suffix=='.lean' or p.name in ('lean-toolchain','lake-manifest.json')):continue
    b=p.read_bytes();kind='exact_canonical_vendor' if 'vendor' in p.parts else 'new_candidate' if p.stem.startswith('P01') else 'project_metadata'
    if p.name=='P01SNReflection.lean':kind='exact_attempt1_candidate'
    if p.name=='P01Audit.lean':kind='generated_readback_commands'
    files.append({'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':H(b),'kind':kind})
inventory={'schema':'p01-formal-source-inventory-v1','lean_pin':PIN,'mathlib_commit':MATHLIB,
           'files':files,'build_order':order,'imports':deps,'targets':targets,'private_dependencies':privates,
           'static_only':True,'kernel_credit':False,'target_policy':'Every public explicit declaration in new modules; private dependencies audited transitively. Auto-generated constructors/projections are not separate counted claims.',
           'type_authority':'Actual pinned compiler #check plus P01TypeAssertions, not this lexical inventory.'}
(ROOT/'formal'/'SOURCE_INVENTORY.json').write_text(json.dumps(inventory,indent=2)+'\n')
(ROOT/'formal'/'TARGETS.json').write_text(json.dumps({'targets':targets,'private':privates,'kernel_credit':False},indent=2)+'\n')
(ROOT/'evidence'/'formal_static_hygiene.json').write_text(json.dumps({'files':lint,'count':len(lint),'kernel_credit':False},indent=2)+'\n')
print(json.dumps({'new_modules':len(new),'public_targets':len(targets),'private_dependencies':len(privates),'all_build_modules':len(order),'source_files':len(files),'status':'STATIC_INVENTORY_AUTHORED_NOT_KERNEL_CHECKED'},indent=2))
