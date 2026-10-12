import pathlib,re
D=pathlib.Path(__file__).resolve().parent;S=D.parent/'hase-imported-compiler-transport-20261010/sources'
s=(S/'AllStructuralBase.lean').read_text()
x=s[s.index('theorem form_ctx'):s.index('theorem form_scoped')]+s[s.index('theorem form_trename'):s.index('end P01AC')]
x=re.sub(r'\bForm\b','FormE',x);x=re.sub(r'\bHas\b','HasE',x);x=re.sub(r'\bCtx\b','CtxE',x)
x=x.replace('has_form h','ClosedProofCanonicalisation.formed h')
extra='''  | piExt hA hB hPi hp hq hBody hFam hh hId sp sq sh sa sb iA iB iPi ip iq iBody iFam ih iId =>
      first | intro r | rename_i r
      exact .piExt (iA r) (iB r) (iPi r) (ip r) (iq r)
        (iBody r) (iFam r) (ih r) (iId r)
        (by simpa only [trenameTel, List.length_map] using sp)
        (by simpa only [trenameTel, List.length_map] using sq)
        (by simpa only [trenameTel, List.length_map] using sh)
        (by simpa only [trenameTel, List.length_map] using tyScoped_trename sa r)
        (by simpa only [trenameTel, List.length_map] using tyScoped_trename sb r)
  | allExt hB hAll hp hq hBody hh hId sp sq sh sb iB iAll ip iq iBody ih iId =>
      first | intro r | rename_i r
      exact .allExt
        (by simpa only [trenameTel_twk] using iB (liftRen r))
        (iAll r) (ip r) (iq r)
        (by simpa only [trenameTel_twk] using iBody (liftRen r))
        (by simpa only [trenameTel_twk] using ih (liftRen r)) (iId r)
        (by simpa only [trenameTel, List.length_map] using sp)
        (by simpa only [trenameTel, List.length_map] using sq)
        (by simpa only [trenameTel, List.length_map] using sh)
        (by simpa only [trenameTel, List.length_map] using tyScoped_trename sb (liftRen r))

'''
x=x.replace('theorem has_trename',extra+'theorem has_trename')
out='''/- Isolated finite structural port for the actual 20-rule HasE grammar. -/
import AllStructuralRename
import ClosedProofCanonicalisation
namespace P01AC.ExtensionalRepair.Structural
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

'''+x+'''\n#print axioms form_trename
#print axioms has_trename
#print axioms ctx_twk
end P01AC.ExtensionalRepair.Structural
'''
(D/'HasEStructuralBase.lean').write_text(out)
r=(S/'AllStructuralRename.lean').read_text();y=r[r.index('theorem form_rename'):r.index('theorem form_theta_head')]
y=re.sub(r'\bForm\b','FormE',y);y=re.sub(r'\bHas\b','HasE',y);y=re.sub(r'\bCtx\b','CtxE',y)
y=y.replace('has_form h','ClosedProofCanonicalisation.formed h')
y=y.replace('polyConv_subst hc','polyConvPlus_subst hc')
extra='''    | @piExt Γ A B p q h hA hB hPi hp hq hBody hFam hh hId sp sq sh sa sb iA iB iPi ip iq iBody iFam ih iId =>
        rename_i Δ r hΔ hr
        have hA' := iA hΔ hr
        have hΔA := CtxE.ext hΔ hA'
        have hB' := iB hΔA (hr.lift A)
        have hBody' := iBody hΔA (hr.lift A)
        have hFam' := iFam hΔ hr
        have hh' := ih hΔ hr
        have hId' := iId hΔ hr
        simp only [renSub_lift, subst, psub,
          P01DF.Syntactic.polynomial_shift_substitution] at hB' hBody' hFam' hh' hId'
        exact .piExt hA' hB' (iPi hΔ hr) (ip hΔ hr) (iq hΔ hr)
          hBody' hFam' hh' hId'
          (scoped_subst sp (fun n hn => hr.scope n hn))
          (scoped_subst sq (fun n hn => hr.scope n hn))
          (scoped_subst sh (fun n hn => hr.scope n hn))
          (tyScoped_subst sa (fun n hn => hr.scope n hn))
          (tyScoped_subst sb (scopedSub_lift (fun n hn => hr.scope n hn)))
    | @allExt Γ B p q h hB hAll hp hq hBody hh hId sp sq sh sb iB iAll ip iq iBody ih iId =>
        rename_i Δ r hΔ hr
        exact .allExt (iB (ctx_twk hΔ) hr.twk) (iAll hΔ hr)
          (ip hΔ hr) (iq hΔ hr) (iBody (ctx_twk hΔ) hr.twk)
          (ih (ctx_twk hΔ) hr.twk) (iId hΔ hr)
          (scoped_subst sp (fun n hn => hr.scope n hn))
          (scoped_subst sq (fun n hn => hr.scope n hn))
          (scoped_subst sh (fun n hn => hr.scope n hn))
          (tyScoped_subst sb (fun n hn => hr.scope n hn))

'''
y=y.replace('theorem has_rename',extra+'theorem has_rename')
head='''/- Full actual-HasE renaming, including every piExt and allExt premise. -/
import HasEStructuralBase
namespace P01AC.ExtensionalRepair.Structural
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)
open P01AC.Intensional.Plus (PolyConvPlus)
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

/-- Literal polynomial substitution preserves all eight source conversion rules. -/
theorem polyConvPlus_subst {p q : Poly} (h : PolyConvPlus p q) (σ : Nat → Poly) :
    PolyConvPlus (psub σ p) (psub σ q) := by
  induction h with
  | refl => exact .refl _
  | symm h ih => exact ih.symm
  | trans h k ih ik => exact ih.trans ik
  | app h k ih ik => exact .app ih ik
  | i p => exact .i _
  | k p q => exact .k _ _
  | s p q r => exact .s _ _ _
  | bridge r t => exact .bridge r t

'''
(D/'HasEStructuralRename.lean').write_text(head+y+'''\n#print axioms form_rename
#print axioms has_rename
#print axioms has_wk
end P01AC.ExtensionalRepair.Structural
''')
