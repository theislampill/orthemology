This is a preservation construction, not a compression result. The basis can be large or infinite across episodes; equality of referenced identifiers does not authenticate their referents. Encoding records injectively supplies no independent test of source truth, efficient computation, predictive gain, or faithful modelling of a worldly process.

## Example: one finite episode view

Consider a synthetic record with one claim $q$, two evidence items $h_1,h_2$, an actor $a$, a case-bound configuration $\bar\mu$, a route $r$, and an unresolved obligation $b$. Suppose the declaration extracts supports, assessments, and route-authorisation interactions:

$$
\begin{aligned}
\rho_A(e)=\eta_A(\xi_A(e))
&+[h_1]\otimes[q]+[h_2]\otimes[q]\\
&+[a]\otimes[h_1]\otimes[q]\\
&+[\bar\mu]\otimes[h_1]\otimes[q]\otimes[r].
\end{aligned}
$$

The role tags and occurrence IDs are suppressed only for readability. The degree profile is $\{1,2,3,4\}$. The two support edges share one typed-word component. The unresolved status of $b$ remains in the record channel; the displayed tensor does not claim $q$ true or $b$ resolved.

This is an explicit instance of finite-support actualisation, not an encoding of the entire present chat and not a submitted repository episode.

## When a compressed representation is adequate

**Theorem 4.2 — Fibre criterion for preserving a target.** Let $D$ be any set, $r:D\to Y$ a representation, and $q:D\to Z$ a declared observable. There exists a decoder $\bar q:r(D)\to Z$ with

$$q=\bar q\circ r$$

if and only if

$$r(d)=r(d')\quad\Longrightarrow\quad q(d)=q(d')$$

for all $d,d'\in D$.

*Proof.* Factorisation makes $q$ equal on every fibre of $r$. Conversely define $\bar q(y)$ to be the unique value of $q$ on $r^{-1}(\{y\})$. Each such fibre is nonempty for $y\in r(D)$, and fibre constancy makes the definition unambiguous. $\square$

For a family of required observables, apply the theorem to their product. This is an elementary set-theoretic factorisation criterion, not a new general theorem. In Orthemology it gives an exact meaning to “this representation retains the distinctions needed for this assessment”. It does not prove that the declared observable is the correct one for the world.

**Corollary 4.3 — Representation transport.** A compression $c:r(D)\to Y'$ preserves $q$ exactly when $q$ is constant on fibres of $c\circ r$. Calling $c$ a contraction, projection, summary, or neural embedding does not settle this condition.

## Change of basis and semantic composition

For linear isomorphisms $g_\tau:V_\tau\to V'_\tau$, the direct-sum map induces

$$
T(g)|_{V_w}=g_{\tau_1}\otimes\cdots\otimes g_{\tau_n}.
$$

It preserves each word type and degree. A representation change is equivariant when $\rho'_A=T(g)\rho_A$ on the admitted domain. Basis relabellings satisfy this equation for the free-basis construction. Arbitrary semantic relabellings do not become justified merely because a linear isomorphism exists.

To represent a workflow composition $e\circ f$ by tensor multiplication, one would additionally need

$$\rho_A(e\circ f)=\rho_A(e)\rho_A(f)$$

where that composition is defined, or an explicitly specified alternative intertwining law. Shared evidence, aliasing, authority constraints and duplicate obligations can prevent naive concatenation from having that meaning. The construction above makes no blanket homomorphism claim.