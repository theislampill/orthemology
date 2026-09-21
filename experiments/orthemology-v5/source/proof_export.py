"""Actual strict bytes -> checked source -> finite Lean Cert exporter.

The output asks Lean to recompute the finite checker and prove its result matches
BOTH program and type reported by Python. Producing text is not certification.
GeneratedExamples.lean is a mandatory build target. The Python runtime does not
silently treat exported/uncompiled text as accepted Lean evidence.
"""
import hashlib,re
import reference as r
from boundaries import Rejection,load_json
MAX_EXPORT_BYTES=1048576
MAX_EXPORT_CERT_NODES=512

def _ty(a):
 a=tuple(a)
 if a[0]=='v':return '(TypeCode.var '+str(a[1])+')'
 if a[0]=='bottom':return 'TypeCode.bottom'
 if a[0]=='arr':return '(TypeCode.arrow '+_ty(a[1])+' '+_ty(a[2])+')'
 if a[0]=='all':return '(TypeCode.all '+_ty(a[1])+')'
 raise Rejection('export: unexpected type after checker')

def _term(t):
 if t[0]=='app':return '(Term.app '+_term(t[1])+' '+_term(t[2])+')'
 return {'i':'Term.i','k':'Term.k','s':'Term.s','zero':'Term.zero','one':'Term.one'}[t[0]]

def _cert(p,budget):
 budget[0]-=1
 if budget[0]<0:raise Rejection('export: certificate constructor budget')
 tag=p['rule']
 if tag in ('i','k','s'):
  fields={'i':['A'],'k':['A','B'],'s':['A','B','C']}[tag]
  return '(Cert.'+tag+' '+' '.join(_ty(p[k]) for k in fields)+')'
 if tag=='app':return '(Cert.app '+_cert(p['function'],budget)+' '+_cert(p['argument'],budget)+')'
 if tag=='all_i':return '(Cert.allI '+_cert(p['body'],budget)+')'
 if tag=='all_e':return '(Cert.allE '+_cert(p['polymorphic'],budget)+' '+_ty(p['type'])+')'
 if tag=='reduce':
  n=len(p['trace'])-1;budget[0]-=n
  if budget[0]<0:raise Rejection('export: reduction constructor budget')
  c=_cert(p['proof'],budget)
  return '(Cert.step '*n+c+')'*n
 raise Rejection('export: unexpected proof after checker')

def export(name:str,raw:bytes)->str:
 if type(name) is not str or not re.fullmatch('[a-zA-Z][a-zA-Z0-9_]{0,79}',name):raise Rejection('export: bounded identifier required')
 proof=load_json(raw);term,ty=r.check(proof)
 cert=_cert(proof,[MAX_EXPORT_CERT_NODES]);t=_term(term);a=_ty(ty)
 result=f'''-- Source JSON SHA256: {hashlib.sha256(raw).hexdigest()}
def {name}Certificate : Cert := {cert}
def {name}Checked : Checked := (check 0 {name}Certificate).get (by decide)
theorem {name}_erasure : {name}Checked.term = {t} := by decide
theorem {name}_type : {name}Checked.ty = {a} := by decide
theorem {name}_sound (rho : Nat → Code) : (interpret {a} rho).accepts {t} := by
  have h := checked_sound {name}Checked rho
  rw [{name}_type, {name}_erasure] at h
  exact h
'''
 if len(result.encode())>MAX_EXPORT_BYTES:raise Rejection('export: source byte budget')
 return result

def module(examples):
 if type(examples) not in (list,tuple) or not 1<=len(examples)<=16:raise Rejection('export: example count')
 names=set();blocks=[]
 for name,raw in examples:
  block=export(name,raw)
  if name in names:raise Rejection('export: duplicate identifier')
  names.add(name);blocks.append(block)
 text='''/- Generated from actual checked JSON by proof_export.py.
UNCOMPILED: text generation supplies no Lean acceptance credit. -/
import FiniteBridge
namespace OrthemologyV4Exports
open OrthemologyV2 OrthemologyV3
'''+ '\n'.join(blocks)+'\nend OrthemologyV4Exports\n'
 if len(text.encode())>MAX_EXPORT_BYTES:raise Rejection('export: module byte budget')
 return text
