/-
The Hurkens proof below is adapted from Mario Carneiro's Mathlib Girard proof:
Copyright (c) 2021 Mario Carneiro. All rights reserved.
Released under Apache 2.0; see LICENSES/Apache-2.0.txt.
Source: Counterexamples/Girard.lean at Mathlib commit
81a5d257c8e410db227a6665ed08f64fea08e997.
The adaptation replaces quantification over Type by a decoded code family,
and spells out the predicate-level proof. No novelty is claimed for the argument.
-/
import Init

namespace OrthemologyV2Boundary

universe u v

def DPred (X : Type v) : Type v := (X → Prop) → Prop

def GirardFamily {C : Type u} (decode : C → Type v) (c : C) : Type v :=
  (DPred (decode c) → decode c) → DPred (decode c)

/-- One exact family is enough: a beta-preserving retraction into its own
    decoded indexing universe is impossible. No global false axiom is added. -/
theorem no_self_product {C : Type u} (decode : C → Type v) (c : C)
    (pack : ((x : C) → GirardFamily decode x) → decode c)
    (unpack : decode c → (x : C) → GirardFamily decode x)
    (beta : ∀ (f : (x : C) → GirardFamily decode x) (x : C),
      unpack (pack f) x = f x) : False :=
  let U := decode c
  let F := GirardFamily decode
  let G (T : DPred U) (X : C) : F X :=
    fun f p => T (fun x : U => p (f (unpack x X f)))
  let τ (T : DPred U) : U := pack (G T)
  let σ (x : U) : DPred U := unpack x c τ
  have στ : ∀ (p : U → Prop) (S : DPred U),
      σ (τ S) p ↔ S (fun x => p (τ (σ x))) :=
    fun p S =>
      let e := congrArg (fun f : F c => f τ p) (beta (G S) c)
      ⟨fun h => Eq.mp e h, fun h => Eq.mpr e h⟩
  let ω : DPred U := fun p => ∀ x, σ x p → p x
  let δ (S : DPred U) : Prop := ∀ p, S p → p (τ S)
  have hω : δ ω :=
    fun p d =>
      d (τ ω) ((στ p ω).mpr
        (fun x h => d (τ (σ x)) ((στ p (σ x)).mpr h)))
  let q : U → Prop := fun y => ¬ δ (σ y)
  have hq : ω q :=
    fun x e f =>
      (f q e)
        (fun p h => f (fun y => p (τ (σ y))) ((στ p (σ x)).mp h))
  have hn : ¬ δ (σ (τ ω)) := hω q hq
  have hd : δ (σ (τ ω)) :=
    fun p h => hω (fun y => p (τ (σ y))) ((στ p ω).mp h)
  hn hd

end OrthemologyV2Boundary

#print axioms OrthemologyV2Boundary.no_self_product
