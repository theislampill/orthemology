from pathlib import Path
R=Path('private-locator:f4d3d6c6fac1ac9bd43b')
# expression tuples: symbols, (fn, args)
def E(fn,*args):return (fn,*args)
def txt(e):
 if isinstance(e,str): return e
 fn,*args=e
 if fn=='and': return '('+' && '.join(txt(a) for a in args)+')'
 if fn=='eq':return f'decide ({txt(args[0])} = {txt(args[1])})'
 if fn=='child':return f'(Nat.pair ({txt(args[0])}) ({txt(args[1])}), {txt(args[2])})'
 return fn+' '+ ' '.join('('+txt(a)+')' for a in args)
def pr(e):
 if isinstance(e,str):
  if e.startswith('v') or e.startswith('a'):return f'(primrec_{e[0:2]}.comp Primrec.snd)'
  if e in ['lhs s','rhs s']:return 'primrec_'+e.split()[0]
  return '(Primrec.const _)'
 fn,*args=e
 if fn=='and':return '(Primrec.and.comp '+pr(args[0])+' '+pr(args[1])+')'
 if fn=='eq':return '(Primrec.eq.comp '+pr(args[0])+' '+pr(args[1])+')'
 if fn=='child':return '((Primrec₂.natPair.comp '+pr(args[0])+' '+pr(args[1])+').pair '+pr(args[2])+')'
 return f'(primrec_{fn}.comp '+' '.join(pr(a) for a in args)+')'
def guard(a,b):return E('and',E('eq','lhs s',a),E('eq','rhs s',b))
def apps(fn,a,*args):
 for b in args:a=E(fn,a,b)
 return a
v=[None]+[f'v{i} s.2' for i in range(1,7)]
a=[None]+[f'a{i} s.2' for i in range(1,7)]
def ifs(es):
 return '\n  '.join(('if' if i==0 else 'else if')+f' tag s.2 = {tag} then {val}' for i,(tag,val) in enumerate(es))+'\n  else false'
def prifs(es):
 out='(Primrec.const false)'
 for tag,e in reversed(es):out=f'(Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const {tag})) {pr(e)} {out})'
 return out
step=[(0,guard(apps('tmApp','encode Term.i',v[1]),v[1])),(1,guard(apps('tmApp','encode Term.k',v[1],v[2]),v[1])),(2,guard(apps('tmApp','encode Term.s',v[1],v[2],v[3]),E('tmApp',E('tmApp',v[1],v[3]),E('tmApp',v[2],v[3])))),(3,guard(E('tmApp',v[1],v[3]),E('tmApp',v[2],v[3]))),(4,guard(E('tmApp',v[1],v[2]),E('tmApp',v[1],v[3])))]
poly=[(0,guard(v[1],v[1])),(1,guard(v[2],v[1])),(2,guard(v[1],v[3])),(3,guard(E('polyApp',v[1],v[3]),E('polyApp',v[2],v[4]))),(4,guard(apps('polyApp',E('polyAtom','encode Term.i'),v[1]),v[1])),(5,guard(apps('polyApp',E('polyAtom','encode Term.k'),v[1],v[2]),v[1])),(6,guard(apps('polyApp',E('polyAtom','encode Term.s'),v[1],v[2],v[3]),E('polyApp',E('polyApp',v[1],v[3]),E('polyApp',v[2],v[3])))),(7,guard(E('polyAtom',E('tmApp',v[1],v[2])),E('polyApp',E('polyAtom',v[1]),E('polyAtom',v[2]))))]
stepChildren=[(3,[E('child',v[1],v[2],a[4])]),(4,[E('child',v[2],v[3],a[4])])]
polyChildren=[(1,[E('child',v[1],v[2],a[3])]),(2,[E('child',v[1],v[2],a[4]),E('child',v[2],v[3],a[5])]),(3,[E('child',v[1],v[2],a[5]),E('child',v[3],v[4],a[6])])]
encStep=[('i','(x : Term)', '.i x',0,['x']),('k','(x y : Term)','.k x y',1,['x','y']),('s','(f g x : Term)','.s f g x',2,['f','g','x']),('left','(f g x : Term) (c : StepCert)','.left f g x c',3,['f','g','x','!c']),('right','(f x y : Term) (c : StepCert)','.right f x y c',4,['f','x','y','!c'])]
encPoly=[('refl','(p : Poly)','.refl p',0,['p']),('symm','(p q : Poly) (c : PolyCert)','.symm p q c',1,['p','q','!c']),('trans','(p q r : Poly) (c d : PolyCert)','.trans p q r c d',2,['p','q','r','!c','!d']),('app','(f g p q : Poly) (c d : PolyCert)','.app f g p q c d',3,['f','g','p','q','!c','!d']),('i','(p : Poly)','.i p',4,['p']),('k','(p q : Poly)','.k p q',5,['p','q']),('s','(p q r : Poly)','.s p q r',6,['p','q','r']),('bridge','(r t : Term)','.bridge r t',7,['r','t'])]
for name,es,cs,encs,typ in [('Step',step,stepChildren,encStep,'StepCert'),('Poly',poly,polyChildren,encPoly,'PolyCert')]:
 n=name.lower();o='import AuxiliaryCodeCore\nnamespace AuxiliaryCodeComputability\nopen Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity\nopen AuxiliaryCertificates OrthemologyV2 P01D\nset_option maxRecDepth 8192\nset_option maxHeartbeats 8000000\n'
 for cn,bind,expr,tag,fields in encs:
  vals=', '.join('encode '+f[1:] if f.startswith('!') else 'leaf (encode '+f+')' for f in fields)
  o+=f'\n@[simp] theorem encode_{n}_{cn} {bind} : encode ({expr} : {typ}) = pack {tag} [{vals}] := rfl\n'
 o+=f'\ndef {n}Shape (s : Nat × Nat) : Bool :=\n  '+ifs([(tag,txt(e)) for tag,e in es])+'\n'
 o+=f'\ndef {n}Children (s : Nat × Nat) : List (Nat × Nat) :=\n  '+('\n  '.join(('if' if i==0 else 'else if')+f' tag s.2 = {tag} then ['+', '.join(map(txt,childs))+']' for i,(tag,childs) in enumerate(cs)))+'\n  else []\n'
 o+=f'\ndef check{name}Code (c a b : Nat) : Bool := evaluate {n}Shape {n}Children (Nat.pair a b,c)\n'
 o+=f'\ntheorem primrec_{n}Shape : Primrec {n}Shape :=\n  '+prifs(es)+'\n'
 out='(Primrec.const [])'
 for tag,childs in reversed(cs):
  cl='(Primrec.const [])'
  for child in reversed(childs):cl='(Primrec.list_cons.comp '+pr(child)+' '+cl+')'
  out=f'(Primrec.ite (Primrec.eq.comp (primrec_tag.comp Primrec.snd) (.const {tag})) {cl} {out})'
 o+=f'\ntheorem primrec_{n}Children : Primrec {n}Children :=\n  '+out+'\n'
 o+=f'\ntheorem primrec_check{name}Code : Primrec (fun p : Nat × Nat × Nat => check{name}Code p.1 p.2.1 p.2.2) :=\n  (primrec_evaluate primrec_{n}Shape primrec_{n}Children).comp\n    ((Primrec₂.natPair.comp (Primrec.fst.comp Primrec.snd) (Primrec.snd.comp Primrec.snd)).pair Primrec.fst)\n'
 o+=f'\ntheorem eval_{n} (a b c : Nat) : evaluate {n}Shape {n}Children (Nat.pair a b,c) = check{name}Code c a b := rfl\n'
 o+='\nend AuxiliaryCodeComputability\n'
 (R/f'{name}Code.lean').write_text(o)
