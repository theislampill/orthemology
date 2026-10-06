import CertificateSyntax
import FiniteLists

namespace OrthemicCertificate.Signed
variable {q n k : Nat}

abbrev pairList (n k : Nat) : List (Pair n k) :=
  productList (List.finRange n) (List.finRange k)

@[simp] theorem mem_pairList (e : Pair n k) : e ∈ pairList n k := by simp

def pathDomain (n k : Nat) : List (Path (Fin n) (Fin k)) :=
  (List.finRange n).flatMap (fun s =>
    (boundedLists (productList (List.finRange k) (List.finRange n)) (n - 1)).map
      (fun steps => ⟨s, steps⟩))

def linkDomain (n k : Nat) : List (Link n k) :=
  (List.finRange n).flatMap (fun s => (pathDomain n k).flatMap (fun toRoot =>
    (pathDomain n k).map (fun fromRoot => ⟨s, toRoot, fromRoot⟩)))

def componentDomain (n k : Nat) : List (Component n k) :=
  (subsetList (pairList n k)).flatMap (fun pairs => (List.finRange n).flatMap (fun root =>
    (boundedLists (linkDomain n k) n).map (fun links => ⟨pairs, root, links⟩)))

def witnessDomain (n k : Nat) : List (Witness n k) :=
  ((pathDomain n k).flatMap (fun p => (pairList n k).flatMap (fun e =>
    (List.finRange n).map (fun y => .exit p e y)))) ++
  ((pathDomain n k).flatMap (fun p => (componentDomain n k).flatMap (fun c =>
    (List.finRange n).map (fun entry => .target p c entry))))

def obligationDomain (q n k : Nat) : List (Obligation q n k) :=
  (List.finRange n).flatMap (fun s => (List.finRange q).flatMap (fun θ =>
    (witnessDomain n k).map (fun w => ⟨s, θ, w⟩)))

def nodeDomain (q n k : Nat) : List (Node q n k) :=
  (subsetList (List.finRange q)).flatMap (fun support =>
    (subsetList (List.finRange n)).flatMap (fun states =>
      (subsetList (pairList n k)).flatMap (fun pairs =>
        (boundedLists (obligationDomain q n k) (n*q)).map
          (fun obligations => ⟨support, states, pairs, obligations⟩))))

/-- This over-enumerates malformed bodies and preserves every stored List order,
including unused nodes. Finsets are represented extensionally. -/
def astDomain (q n k : Nat) : List (Body q n k) :=
  boundedLists (nodeDomain q n k) (2^q - 1)

/-- The exact inherited path predicate carries this syntax bound. -/
theorem Path.length_bound {A : Finset (Pair n k)} {succ : Pair n k → Finset (Fin n)}
    {s t : Fin n} {p : Path (Fin n) (Fin k)} (h : Path.Valid A succ s t p) :
    p.steps.length ≤ n - 1 := by simpa using h.2.2.2

/-- No two link-state keys may coincide, so every accepted component has at most
n links, independently of link order or whether the query uses the component. -/
theorem Component.link_length_bound {I : Input q n k} {B : Support q} {θ : Fin q}
    {A : Finset (Pair n k)} {c : Component n k} {entry : Fin n}
    (h : c.Valid I B θ A entry) : c.links.length ≤ n := by
  have hn := h.2.2.2.2.1.length_le_card
  simpa using hn

theorem Node.obligation_length_bound {N : Node q n k} (h : N.KeysValid) :
    N.obligations.length ≤ n*q := by
  have hn := h.1.length_le_card
  simpa using hn

/-- Excluding empty support strengthens the distinct-support bound by one. -/
theorem body_length_bound {I : Input q n k} {c : Body q n k} (h : BodyValid I c) :
    c.length ≤ 2^q - 1 := by
  have hno : (c.map Node.support).Nodup := h.2.1.2
  have hempty : (∅ : Support q) ∉ c.map Node.support := by
    intro hm
    obtain ⟨N,hN,hEq⟩ := List.mem_map.mp hm
    have hn := (h.2.2 N hN).1
    simpa [hEq] using hn
  have hbound := (List.nodup_cons.mpr ⟨hempty,hno⟩).length_le_card
  have hlen : c.length + 1 ≤ 2^q := by
    simpa [Fintype.card_finset] using hbound
  omega

theorem mem_pathDomain {p : Path (Fin n) (Fin k)} (h : p.steps.length ≤ n-1) :
    p ∈ pathDomain n k := by
  rcases p with ⟨s,steps⟩
  apply List.mem_flatMap.mpr
  refine ⟨s, List.mem_finRange s, ?_⟩
  apply List.mem_map.mpr
  refine ⟨steps, (mem_boundedLists _ _ _).mpr ⟨h, ?_⟩, rfl⟩
  intro y _
  simp

theorem mem_linkDomain {l : Link n k}
    (ht : l.toRoot.steps.length ≤ n-1) (hf : l.fromRoot.steps.length ≤ n-1) :
    l ∈ linkDomain n k := by
  rcases l with ⟨s,toRoot,fromRoot⟩
  exact List.mem_flatMap.mpr ⟨s,List.mem_finRange s,
    List.mem_flatMap.mpr ⟨toRoot,mem_pathDomain ht,
      List.mem_map.mpr ⟨fromRoot,mem_pathDomain hf,rfl⟩⟩⟩

theorem mem_componentDomain {I : Input q n k} {B : Support q} {θ : Fin q}
    {A : Finset (Pair n k)} {c : Component n k} {entry : Fin n}
    (h : c.Valid I B θ A entry) : c ∈ componentDomain n k := by
  have hpairs : c.pairs ∈ subsetList (pairList n k) := by
    apply (mem_subsetList _ _).mpr
    intro a _
    exact List.mem_toFinset.mpr (mem_pairList a)
  apply List.mem_flatMap.mpr
  refine ⟨c.pairs,hpairs,List.mem_flatMap.mpr ⟨c.root,List.mem_finRange c.root,?_⟩⟩
  apply List.mem_map.mpr
  refine ⟨c.links, (mem_boundedLists _ _ _).mpr ⟨Component.link_length_bound h, ?_⟩, rfl⟩
  intro l hl
  have hv := h.2.2.2.2.2.2.1 l hl
  exact mem_linkDomain (Path.length_bound hv.1) (Path.length_bound hv.2)

theorem mem_witnessDomain {I : Input q n k} {B : Support q} {θ : Fin q}
    {A : Finset (Pair n k)} {s : Fin n} {w : Witness n k}
    (h : w.Valid I B A s θ) : w ∈ witnessDomain n k := by
  cases w with
  | exit p e y =>
    apply List.mem_append_left
    exact List.mem_flatMap.mpr ⟨p,mem_pathDomain (Path.length_bound h.1),
      List.mem_flatMap.mpr ⟨e,mem_pairList e,List.mem_map.mpr ⟨y,List.mem_finRange y,rfl⟩⟩⟩
  | target p c entry =>
    apply List.mem_append_right
    exact List.mem_flatMap.mpr ⟨p,mem_pathDomain (Path.length_bound h.1),
      List.mem_flatMap.mpr ⟨c,mem_componentDomain h.2,
        List.mem_map.mpr ⟨entry,List.mem_finRange entry,rfl⟩⟩⟩

theorem mem_obligationDomain {I : Input q n k} {B : Support q}
    {A : Finset (Pair n k)} {o : Obligation q n k}
    (h : o.witness.Valid I B A o.state o.candidate) : o ∈ obligationDomain q n k := by
  exact List.mem_flatMap.mpr ⟨o.state,List.mem_finRange o.state,
    List.mem_flatMap.mpr ⟨o.candidate,List.mem_finRange o.candidate,
      List.mem_map.mpr ⟨o.witness,mem_witnessDomain h,rfl⟩⟩⟩

theorem mem_nodeDomain {I : Input q n k} {c : Body q n k} {N : Node q n k}
    (h : N.Valid I c) : N ∈ nodeDomain q n k := by
  have hpairs : N.pairs ∈ subsetList (pairList n k) := by
    apply (mem_subsetList _ _).mpr
    intro a _
    exact List.mem_toFinset.mpr (mem_pairList a)
  exact List.mem_flatMap.mpr ⟨N.support,mem_subset_finRange _ _,
    List.mem_flatMap.mpr ⟨N.states,mem_subset_finRange _ _,
      List.mem_flatMap.mpr ⟨N.pairs,hpairs,List.mem_map.mpr ⟨N.obligations,
        (mem_boundedLists _ _ _).mpr ⟨Node.obligation_length_bound h.2.1,
          fun o ho => mem_obligationDomain (h.2.2.2 o ho)⟩,rfl⟩⟩⟩⟩

theorem accepted_mem_astDomain {I : Input q n k} {c : Body q n k}
    {B : Support q} {s : Fin n} (hc : check I c B s = true) :
    c ∈ astDomain q n k := by
  have h := (check_iff I c B s).mp hc
  exact (mem_boundedLists _ _ _).mpr ⟨body_length_bound h.1,
    fun N hN => mem_nodeDomain (h.1.2.2 N hN)⟩

end OrthemicCertificate.Signed
