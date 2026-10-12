import AuxiliaryCodeCore
namespace CertificateCodeValidity
open Encodable SourceFamilyComputability CodedScope ExactSyntaxValidity AuxiliaryCodeComputability
set_option maxRecDepth 8192
set_option maxHeartbeats 1000000

/-- A field's first bit records the existing external-sort leaf wrapper;
    the natural number is its expected syntax sort. This is grammar data only. -/
abbrev Field := Bool × Nat
abbrev Constructor := List Field
abbrev Description := List Constructor

def iterRest (c : Nat) : Nat → Nat := Nat.rec c (fun _ r => rest r)
def slot (c i : Nat) : Nat := first (iterRest c (i+1))
def fieldCode (f : Field) (c i : Nat) : Nat := if f.1 then rest (slot c i) else slot c i
def rebuildField (f : Field) (c i : Nat) : Nat := if f.1 then leaf (fieldCode f c i) else fieldCode f c i

def dependencies (fs : Constructor) (c : Nat) : List (Nat × Nat) :=
  (List.range fs.length).map (fun i => ((fs[i]?.getD (false,0)).2, fieldCode (fs[i]?.getD (false,0)) c i))
def rebuild (fs : Constructor) (c : Nat) : List Nat :=
  (List.range fs.length).map (fun i => rebuildField (fs[i]?.getD (false,0)) c i)
def localShape (ds : Description) (c : Nat) : Bool :=
  if tag c < ds.length then decide (c = pack (tag c) (rebuild (ds[tag c]?.getD []) c)) else false
def localChildren (ds : Description) (c : Nat) : List (Nat × Nat) :=
  dependencies (ds[tag c]?.getD []) c

@[simp] theorem tag_pack (t : Nat) (xs : List Nat) : tag (pack t xs) = t := by
  simp [tag, pack, leaf]

@[simp] theorem iterRest_zero (c : Nat) : iterRest c 0 = c := rfl
@[simp] theorem iterRest_succ (c i : Nat) : iterRest c (i+1) = rest (iterRest c i) := rfl

/-- Generic PR payload packing, with the actual retained node/zero-leaf format. -/
theorem primrec_pack : Primrec₂ pack := by
  have hp : Primrec (fun xs : List Nat => xs.foldr node (leaf 0)) :=
    Primrec.list_foldr Primrec.id (Primrec.const _) (primrec_node.comp₂
      (Primrec.fst.comp₂ Primrec₂.right) (Primrec.snd.comp₂ Primrec₂.right))
  exact (primrec_node.comp (primrec_leaf.comp Primrec.fst) (hp.comp Primrec.snd)).to₂

theorem primrec_iterRest : Primrec₂ iterRest :=
  Primrec.nat_rec Primrec.id (primrec_rest.comp₂ (Primrec.snd.comp₂ Primrec₂.right))
theorem primrec_slot : Primrec₂ slot :=
  primrec_first.comp₂ (primrec_iterRest.comp₂ Primrec₂.left (Primrec.succ.comp₂ Primrec₂.right))

/-- Fully parameterized descriptor interpreter; no unproved source operation is assumed. -/
theorem primrec_fieldCode : Primrec (fun p : Field × Nat × Nat => fieldCode p.1 p.2.1 p.2.2) := by
  have hs : Primrec (fun p : Field × Nat × Nat => slot p.2.1 p.2.2) :=
    primrec_slot.comp (Primrec.fst.comp Primrec.snd) (Primrec.snd.comp Primrec.snd)
  apply (Primrec.cond (Primrec.fst.comp Primrec.fst) (primrec_rest.comp hs) hs).of_eq
  intro p
  unfold fieldCode
  cases p.1.1 <;> rfl

theorem primrec_rebuildField : Primrec (fun p : Field × Nat × Nat => rebuildField p.1 p.2.1 p.2.2) := by
  apply (Primrec.cond (Primrec.fst.comp Primrec.fst)
    (primrec_leaf.comp primrec_fieldCode) primrec_fieldCode).of_eq
  intro p
  unfold rebuildField
  cases p.1.1 <;> rfl

theorem primrec_dependencies : Primrec₂ dependencies := by
  have hf : Primrec (fun p : (Constructor × Nat) × Nat => p.1.1[p.2]?.getD (false, 0)) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp (Primrec.fst.comp Primrec.fst) Primrec.snd)
      (Primrec.const _)
  apply Primrec.list_map (Primrec.list_range.comp (Primrec.list_length.comp Primrec.fst))
  exact (Primrec.pair (Primrec.snd.comp hf) (primrec_fieldCode.comp
    (Primrec.pair hf (Primrec.pair (Primrec.snd.comp Primrec.fst) Primrec.snd)))).to₂

theorem primrec_rebuild : Primrec₂ rebuild := by
  have hf : Primrec (fun p : (Constructor × Nat) × Nat => p.1.1[p.2]?.getD (false, 0)) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp (Primrec.fst.comp Primrec.fst) Primrec.snd)
      (Primrec.const _)
  apply Primrec.list_map (Primrec.list_range.comp (Primrec.list_length.comp Primrec.fst))
  exact (primrec_rebuildField.comp
    (Primrec.pair hf (Primrec.pair (Primrec.snd.comp Primrec.fst) Primrec.snd))).to₂

theorem primrec_localShape : Primrec₂ localShape := by
  have ht : Primrec (fun p : Description × Nat => tag p.2) := primrec_tag.comp Primrec.snd
  have hf : Primrec (fun p : Description × Nat => p.1[tag p.2]?.getD []) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.fst ht) (Primrec.const [])
  exact Primrec.ite (Primrec.nat_lt.comp ht (Primrec.list_length.comp Primrec.fst))
    (Primrec.eq.comp Primrec.snd (primrec_pack.comp ht (primrec_rebuild.comp hf Primrec.snd)))
    (Primrec.const false)

theorem primrec_localChildren : Primrec₂ localChildren := by
  have ht : Primrec (fun p : Description × Nat => tag p.2) := primrec_tag.comp Primrec.snd
  have hf : Primrec (fun p : Description × Nat => p.1[tag p.2]?.getD []) :=
    Primrec.option_getD.comp (Primrec.list_getElem?.comp Primrec.fst ht) (Primrec.const [])
  exact primrec_dependencies.comp hf Primrec.snd

end CertificateCodeValidity
