"""Generate deterministic *uncompiled* canonical-Cert replay fixtures."""
from pathlib import Path
import json, hashlib
from checker import check, export_finite, compile_poly, _tcstr
B=('bot',); V=lambda n:('var',n);T=lambda n:('tv',n)
I=lambda A:('I',A);Pi=lambda A,B:('pi',A,B)
App=lambda f,x:('app',f,x);Lam=lambda A,b:('lam',A,b)
poly=('allI',I(T(0)));pty=('all',Pi(T(0),T(0)))
fixtures={
 'identity':I(B),
 'polymorphic_identity':poly,
 'identity_self':App(('allE',poly,pty),poly),
 'binder_identity':Lam(B,V(0)),
 'binder_K':Lam(B,Lam(B,V(1))),
 'binder_S':Lam(Pi(B,Pi(B,B)),Lam(Pi(B,B),Lam(B,App(App(V(2),V(0)),App(V(1),V(0))))))
}

def termstr(t):
 if t[0]=='app':return f'(OrthemologyV2.Term.app {termstr(t[1])} {termstr(t[2])})'
 if t[0] in ('i','k','s','zero','one'):return 'OrthemologyV2.Term.'+t[0]
 raise ValueError('not a closed canonical term')

def main():
 root=Path(__file__).resolve().parents[1]
 lines=['/- Generated replay sources, NOT compiled results. -/','import P01Certificates',
        'namespace P01Generated','open OrthemologyV2 OrthemologyV3']
 records=[]
 for name,t in fixtures.items():
  r=check(t);e=export_finite(r)
  if r.status!='ACCEPTED' or e['status']!='EXPORTABLE_FINITE':raise RuntimeError((name,r,e))
  C=e['lean_certificate'];tm=termstr(e['compiled_term']);ty=_tcstr(e['source_typecode'])
  lines += [f'def cert_{name} : Cert := {C}',
   f'def checked_{name} : Checked := (check {e["type_depth"]} cert_{name}).get (by decide)',
   f'theorem term_{name} : checked_{name}.term = {tm} := by rfl',
   f'theorem type_{name} : checked_{name}.ty = {ty} := by rfl',
   f'def envelope_{name} : P01Certificate.FiniteEnvelope {tm} {ty} :=',
   f'  ⟨checked_{name},term_{name},type_{name}⟩',
   f'theorem derives_{name} : FiniteDerives {tm} {ty} :=',
   f'  P01Certificate.finite_envelope_sound envelope_{name}']
  records.append({'name':name,'input_term':t,'frontend_type':r.ty,'export':e,
                  'bound_theorem':'P01Generated.derives_'+name,'kernel_verified':False})
 lines.append('end P01Generated')
 source='\n'.join(lines)+'\n'
 (root/'formal/P01GeneratedExports.lean').write_text(source)
 refused=[]
 for name,t,d in [('dependent_refl',Lam(T(0),('refl',V(0))),1),
   ('represented_sigma',('pair',('sig',Pi(B,B),Pi(B,B)),I(B),I(B)),0)]:
  r=check(t,type_depth=d);e=export_finite(r)
  if r.status!='ACCEPTED' or e['status']!='REFUSED_TARGET_VOCABULARY':raise RuntimeError((r,e))
  refused.append({'name':name,'input_term':t,'frontend_type':r.ty,'compiled_poly':compile_poly(t),
                  'type_depth':d,'export':e,'not_an_untypability_claim':True})
 report={'generated_source_sha256':hashlib.sha256(source.encode()).hexdigest(),
         'accepted_finite_fixtures':records,'typed_dependent_refusals':refused,
         'kernel_runs':0,'old_attempt2_tests_reconstructed':False}
 (root/'evidence/export_fixtures.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'finite_fixtures':len(records),'typed_dependent_refusals':len(refused),
   'kernel_verified':False,'source_sha256':report['generated_source_sha256']},indent=2))
if __name__=='__main__':main()
