from pathlib import Path
import json
R=Path(__file__).resolve().parent;ss=json.loads((R/'SCHEMA.json').read_text())
minimal={'Term':'Term.i','TypeCode':'TypeCode.var 0','Poly':'Poly.var 0','Ty':'Ty.param 0','Nat':'0','Tel':'([] : Tel)','List P01AC.Ty':'([] : List Ty)','StepCert':'StepCert.i Term.i','RedCert':'RedCert.refl Term.i','FiniteCert':'FiniteCert.i (TypeCode.var 0)','PolyCert':'PolyCert.refl (Poly.var 0)','LookupCert':'LookupCert.zero [] (Ty.param 0)','Claim':'Claim.ctxJ []','Rule':'Rule.CtxJ_nil','SerialCert':'SerialCert.node Rule.CtxJ_nil SerialCertList.nil','SerialCertList':'SerialCertList.nil'}
x=['import CertificateImage','import ValidityControls','import TelescopeValidityControls','namespace CertificateCodeValidity.Controls','open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability','open OrthemologyV2 P01D P01AC AuxiliaryCertificates JointCertificates TelescopeCodeValidity','set_option maxRecDepth 16384','set_option maxHeartbeats 1000000','']
for t in ss:
 full=('AuxiliaryCertificates.' if t['sort']<11 else 'JointCertificates.')+t['type']
 x+=['example (a : '+full+') : certValid '+str(t['sort'])+' (encode a) = true := (valid_'+t['type']+' _).mpr ⟨a,rfl⟩']
x+=['''
theorem certValid_unfold (s c : Nat) : certValid s c = (certShape (s,c) &&
    (certChildren (s,c)).all (fun d => if d.2 < c then certValid d.1 d.2 else false)) := by
  rw [certValid, evaluate]
  rfl

theorem reject_shape (s c : Nat) (hs : certShape (s,c) = false) : certValid s c = false := by
  rw [certValid_unfold, hs]
  rfl

@[simp] theorem zero_lt_pack (t : Nat) (xs : List Nat) : 0 < pack t xs :=
  lt_of_le_of_lt (Nat.zero_le _) (left_lt_node _ _)
@[simp] theorem wrapped_lt_pack (t n : Nat) (xs : List Nat) (h : leaf n ∈ xs) : n < pack t xs :=
  lt_of_le_of_lt (le_leaf n) (field_lt_pack t xs h)

@[simp] theorem rejectTermZero : certValid 0 0 = false := by
  rw [certValid_unfold]
  simp [certShape, ExactSyntaxValidity.Controls.rejectTermZero]
@[simp] theorem rejectTypeZero : certValid 1 0 = false := by
  rw [certValid_unfold]
  simp [certShape, ExactSyntaxValidity.Controls.rejectTypeZero]
@[simp] theorem rejectPolyZero : certValid 2 0 = false := by
  rw [certValid_unfold]
  simp [certShape, ExactSyntaxValidity.Controls.rejectPolyZero]
@[simp] theorem rejectTyZero : certValid 3 0 = false := by
  rw [certValid_unfold]
  simp [certShape, ExactSyntaxValidity.Controls.rejectTyZero]
@[simp] theorem rejectBadTel : certValid 5 1 = false := by
  rw [certValid_unfold]
  simp [certShape, TelescopeCodeValidity.rejectTelOne]
@[simp] theorem rejectRuleZero : certValid 12 0 = false := reject_shape _ _ (by decide)
@[simp] theorem rejectSerialZero : certValid 13 0 = false := reject_shape _ _ (by decide)
@[simp] theorem rejectSerialListZero : certValid 14 0 = false := reject_shape _ _ (by decide)

-- Canonical syntax images overlap exactly where the original codec does.
example : certValid 14 (encode Term.i) = true := (valid_SerialCertList _).mpr ⟨.nil,rfl⟩
example : certValid 12 (encode Term.k) = true := (valid_Rule _).mpr ⟨.CtxJ_nil,rfl⟩
example : certValid 11 (encode (Poly.var 0)) = true := (valid_Claim _).mpr ⟨.ctxJ [],rfl⟩

-- Exact arity, terminator, wrapper, sort, and constructor-tag checks.
example : certValid 15 1 = false := reject_shape _ _ (by decide)
example : certValid 6 (pack 5 []) = false := reject_shape _ _ (by decide)
example : certValid 12 (pack 63 []) = false := reject_shape _ _ (by simp [certShape, allDescriptions, localShape, ruleDescription])
theorem rejectSerialTerminator : certValid 14 (node (leaf 0) (leaf 1)) = false :=
  reject_shape _ _ (by decide)
theorem rejectSerialWrapper : certValid 13 (pack 0 [encode Rule.CtxJ_nil, encode SerialCertList.nil]) = false :=
  reject_shape _ _ (by
    simp [certShape, allDescriptions, localShape, serialCertDescription, rebuild, rebuildField, fieldCode, List.range_succ]
    simp [pack, node, leaf, Nat.pair_eq_pair])
''']
bad=[('BadStepTerm',6,'stepCertDescription','0','[leaf 0]'),('BadFiniteType',8,'finiteCertDescription','0','[leaf 0]'),('BadPolyPayload',9,'polyCertDescription','0','[leaf 0]'),('BadClaimTel',11,'claimDescription','0','[leaf 1]'),('BadRuleTy',12,'ruleDescription','13','[leaf 0,leaf 0]'),('BadSerialRule',13,'serialCertDescription','0','[leaf 0, encode SerialCertList.nil]'),('BadSerialLeft',14,'serialCertListDescription','1','[0,encode SerialCertList.nil]'),('BadSerialRight',14,'serialCertListDescription','1','[encode (SerialCert.node Rule.CtxJ_nil SerialCertList.nil),0]')]
common='localShape, localChildren, rebuild, rebuildField, dependencies, fieldCode, List.range_succ'
for name,s,desc,tag,fields in bad:
 code='pack '+tag+' '+fields
 x+=['-- Local shape is correct; rejection genuinely depends on the child sort.','theorem shape'+name+' : localShape '+desc+' ('+code+') = true := by','  simp ['+desc+', '+common+']','theorem reject'+name+' : certValid '+str(s)+' ('+code+') = false := by','  rw [certValid_unfold]','  simp [certShape, certChildren, allDescriptions, '+desc+', '+common+']','']
vals=[]
for t in ss:
 for ct in t['ctors']:
  ctor=t['type']+'.'+ct['name']+(' '+' '.join('('+minimal[f]+')' for f in ct['fields']) if ct['fields'] else '')
  vals+=['certValid '+str(t['sort'])+' (encode ('+ctor+'))']
x+=['-- Runtime acceptance exercises every actual certificate constructor, including all 63 Rule rows.\nset_option pp.deepTerms true\nset_option pp.maxSteps 100000','#eval [\n  '+',\n  '.join(vals)+']']
x+=['#eval ['+', '.join('certValid '+str(s)+' (pack '+tag+' '+fields+')' for _,s,_,tag,fields in bad)+']','end CertificateCodeValidity.Controls']
(R/'CertificateControls.lean').write_text('\n'.join(x)+'\n')
