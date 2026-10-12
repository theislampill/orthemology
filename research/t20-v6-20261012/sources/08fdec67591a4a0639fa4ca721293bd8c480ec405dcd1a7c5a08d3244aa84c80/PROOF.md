# A full-polynomial strict-square-positive nonmoment functional

10 October 2026 UTC. This is a new additive research artifact. The classical
existence phenomenon, the exceptional monomial order, the seed moments and the
separating polynomial are prior art. The explicit recurrence below replaces the
classical rapidly growing diagonal choice by exact Schur completion. No claim
of field novelty, protected-source integration, or T20 closure is made.

## 1. The precise result

There is an explicitly specified real linear functional

\[
\Lambda:\mathbb R[x,y]\longrightarrow\mathbb R
\]

such that:

1. \(\Lambda(1)=1\).
2. Every monomial has a computable dyadic rational value.
3. For **every** nonzero polynomial \(p\in\mathbb R[x,y]\), with no degree bound,
   \(\Lambda(p^2)>0\).
4. The polynomial
   \[
   F=1+x^4y^2+x^2y^4-x^2y^2
   \]
   is everywhere at least \(3/4\), but \(\Lambda(F)=-1\).
5. Consequently no positive Borel measure on \(\mathbb R^2\) with finite
   polynomial moments represents \(\Lambda\).

Items 1–5 are proved below by an ordinary, fully specified infinite induction.
The implementation computes finite portions of this one functional. Finite
checks are diagnostics, not evidence substituting for the universal induction.
The accompanying Lean support checks the scalar lower bound and seed arithmetic
only; it does not yet formalize the full functional or its universal positivity.

## 2. The monomial order is a bijection

Let \(E=\mathbb N_0^2\). Define \(m:E\to\mathbb N_{>0}\) by assigning indices
1 through 10 respectively to

\[
(0,0),(2,1),(1,2),(1,1),(1,0),(0,1),(2,0),(0,2),(3,0),(0,3).
\]

These are exactly the ten pairs of total degree at most three. For \(d=a+b\ge4\),
define

\[
m(a,b)=b+1+\frac{d(d+1)}2.
\]

For each fixed \(d\ge4\), increasing \(b\) from 0 to \(d\) assigns the consecutive
indices \(T_d+1,\ldots,T_{d+1}\), where \(T_d=d(d+1)/2\). The first such block is
11 through 15. The blocks are disjoint, adjacent, and unbounded. Together with
the exceptional first ten, they establish bijectivity. Write \(e_i=m^{-1}(i)\)
and \(z_i=x^{(e_i)_1}y^{(e_i)_2}\).

## 3. Global midpoint precedence

**Lemma.** If \(p,q\in E\) are distinct and their componentwise sum is even,
then

\[
m\left(\frac{p+q}{2}\right)<\max\{m(p),m(q)\}.
\tag{MP}
\]

**Proof.** Let \(D=\max\{|p|,|q|\}\), with \(|(a,b)|=a+b\).

* If \(D\le3\), both endpoints belong to the first ten. Their parity-compatible
  unordered pairs, written as endpoint indices followed by midpoint index, are
  exactly

  \[
  (1,7;5),\ (1,8;6),\ (2,6;4),\ (2,10;3),\ (3,5;4),
  \ (3,9;2),\ (5,9;7),\ (6,10;8),\ (7,8;4).
  \]

  Each midpoint index is smaller than the larger endpoint index. This list is
  exhaustive: the parity classes of the first ten are \(\{1,7,8\}\),
  \(\{2,6,10\}\), \(\{3,5,9\}\), and \(\{4\}\), and only pairs within one
  class have an even componentwise sum.
* Suppose \(D\ge4\) and the endpoint degrees differ. The midpoint has integral
  degree \((|p|+|q|)/2<D\). If its degree is at most three, its index is at most
  10; otherwise its degree block precedes the degree-\(D\) block. In either
  case its index is below that of the degree-\(D\) endpoint, proving (MP).
* Suppose both endpoint degrees equal \(D\ge4\). Write the distinct second
  coordinates as \(b<s\). The midpoint has the same degree \(D\), and second
  coordinate \((b+s)/2<s\). Within this degree block the index increases
  strictly with that coordinate, so the midpoint index is below \(m(q)\).

These cases exhaust all pairs. This proves the global lemma, not merely its
bounded computational instances. \(\square\)

## 4. An explicit total recurrence

Set

\[
j_1=j_2=j_3=1,\qquad j_4=4,\qquad
A_4=\operatorname{diag}(1,1,1,4),\qquad
B_4=\operatorname{diag}(1,1,1,1/4).
\]

For clarity, at every stage define the intended Gram entry as

\[
g_{ik}=\begin{cases}
0,&e_i+e_k\text{ has an odd component},\\
j_{m((e_i+e_k)/2)},&\text{otherwise}.
\end{cases}
\tag{1}
\]

The diagonal entry \(g_{ii}\) is \(j_i\). Every off-diagonal entry \(g_{ik}\)
uses a moment index strictly less than \(\max(i,k)\), by (MP). All distinct
members among the first four have distinct componentwise parity, so their
off-diagonal entries are zero. Thus the stated \(A_4\) is exactly the intended
leading Gram matrix, with no consistency condition omitted.

Assume the stages through \(n-1\) are defined, with \(n\ge5\). Define the
\((n-1)\)-vector \(v_n\) by \((v_n)_i=g_{in}\), using (1). Each value uses only
previously defined \(j\)'s. Now perform the following finite rational operations:

\[
\begin{split}
w_n&=B_{n-1}v_n,\\
q_n&=v_n^T w_n,\\
j_n&=1+q_n,\\
A_n&=\begin{pmatrix}A_{n-1}&v_n\\v_n^T&1+q_n\end{pmatrix},\\
B_n&=\begin{pmatrix}
B_{n-1}+w_nw_n^T&-w_n\\-w_n^T&1
\end{pmatrix}.
\end{split}
\tag{2}
\]

This is a total recursion using addition and multiplication only after the
initial rational \(1/4\). In particular, it has no conditional inversion step,
no numerical tolerance, and no unbounded search for a suitable diagonal.
Ordinary recursion on the natural numbers therefore defines every finite stage
and one infinite sequence \((j_n)_{n\ge1}\). All entries of every \(A_n,B_n\)
and every \(j_n\) are dyadic rationals. Computing a specified monomial moment
requires only a finite prefix. No complexity bound is asserted.

## 5. Universal invertibility and positive definiteness

We prove simultaneously for every \(n\ge4\) that \(A_n\) has the entries (1),
\(A_n\) is symmetric positive definite over \(\mathbb R\), \(B_n=A_n^{-1}\),
and \(\det A_n=4\).

The base \(n=4\) is immediate. For the induction step, write
\(A=A_{n-1}\), \(B=B_{n-1}\), \(v=v_n\), \(w=Bv\), and \(q=v^Tw\).
The indexing lemma ensures that appending \(j_n\) cannot change earlier entries:
all indices occurring in the old matrix are at most \(n-1\). Equations (1) and
(2) give exactly the desired new entries, including the new diagonal \(j_n\).
Symmetry is immediate. The induction hypothesis gives \(AB=BA=I\),
\(B^T=B\), and \(Aw=v\).

For an arbitrary real column vector \(u\) and scalar \(t\), expand to obtain

\[
\begin{pmatrix}u\\t\end{pmatrix}^{\!T}
A_n
\begin{pmatrix}u\\t\end{pmatrix}
=(u+tw)^TA(u+tw)+t^2.
\tag{3}
\]

If \(t\ne0\), the last term is strictly positive and the other is nonnegative.
If \(t=0\) and \((u,t)\ne0\), the first term is strictly positive by the
induction hypothesis. Thus \(A_n\) is positive definite over all real vectors.

The displayed \(B_n\) is the actual inverse: direct block multiplication gives

\[
\begin{pmatrix}A&v\\v^T&1+q\end{pmatrix}
\begin{pmatrix}B+ww^T&-w\\-w^T&1\end{pmatrix}
=\begin{pmatrix}I&0\\0&1\end{pmatrix}.
\]

Indeed the four blocks reduce respectively to
\(I+vw^T-vw^T\), \(-v+v\),
\(w^T+qw^T-(1+q)w^T\), and \(-q+1+q\).
Both factors are symmetric, so transposing gives the reverse product as well.
Therefore the recurrence is exactly

\[
j_n=1+v_n^T A_{n-1}^{-1}v_n,
\]

as proposed. The completed-square congruence (3) is effected by a triangular
matrix with unit diagonal; hence \(\det A_n=(\det A_{n-1})\cdot1=4\).
Equivalently, the Schur complement equals 1 at every step. This completes the
induction for all natural \(n\ge4\). The first three leading matrices are
identities and also positive definite.

No monotonicity of \(j_n\) is used or valid in general: for example
\(j_{11}=479723268580926\), whereas \(j_{12}=5/4\). The classical
entry-size/determinant estimate is not being reused for this different sequence.

## 6. One functional on the entire polynomial algebra

For every monomial set

\[
\Lambda(x^ay^b)=\begin{cases}
0,&a\text{ or }b\text{ odd},\\
j_{m(a/2,b/2)},&a,b\text{ even},
\end{cases}
\tag{4}
\]

and extend by real linearity. A polynomial has finite support, so (4) defines
a unique real number by a finite sum. There is no infinite-series convergence
condition. Every rational-coefficient polynomial has a computable rational
value; arbitrary real coefficients define a real linear functional regardless
of whether those coefficients are themselves computable.

Take any nonzero polynomial \(p\). Since \(m\) is a bijection and the support
of \(p\) is finite, some \(N\) contains its support in \(z_1,\ldots,z_N\).
Write \(p=\sum_{i=1}^N c_i z_i\). Unique monomial expansion implies that
\(c\ne0\). Finite distributivity and (1),(4) give

\[
\Lambda(p^2)=\sum_{i,k=1}^N c_i c_k\Lambda(z_i z_k)=c^T A_N c>0.
\]

This proves strict square positivity for **every** nonzero real polynomial,
with no finite-degree or finite-prefix restriction. It also proves
nonnegativity on all finite sums of polynomial squares, with strict positivity
if at least one summand is nonzero. Finally \(\Lambda(1)=j_1=1\).

## 7. Globally positive separating polynomial and no measure

Let \(u=x^2\), \(v=y^2\), and \(s=u+v\). Then \(u,v\ge0\) and

\[
F(x,y)=1+uv(s-1).
\]

If \(s\ge1\), then \(F\ge1\). If \(s\le1\), then
\(4uv\le(u+v)^2=s^2\le1\), since \((u-v)^2\ge0\), and
\(0\le1-s\le1\). Consequently \(uv(1-s)\le1/4\), giving
\(F=1-uv(1-s)\ge3/4\). Thus \(F\ge3/4\) globally.

The four relevant moments are fixed before any completion:

\[
\Lambda(1)=j_1=1,\quad
\Lambda(x^4y^2)=j_2=1,\quad
\Lambda(x^2y^4)=j_3=1,\quad
\Lambda(x^2y^2)=j_4=4.
\]

Therefore \(\Lambda(F)=1+1+1-4=-1\).

If a positive measure \(\mu\) represented all polynomial moments, normalization
would give \(\mu(\mathbb R^2)=1\). Each of the four monomials in \(F\) is
integrable under that representation, so finite linearity gives
\(\int F\,d\mu=\Lambda(F)=-1\). Positivity and the global lower bound instead
give \(\int F\,d\mu\ge(3/4)\mu(\mathbb R^2)=3/4\), a contradiction.
In particular there is no representing probability measure, and the example
separates square positivity from positivity on all pointwise-nonnegative
polynomials even for a normalized full functional.

## 8. Exact finite verification and limits

`countermodel.py` implements (2), including the explicit inverse update.
`check_exact.py` separately enumerates degree shells and recomputes every
diagonal through index 25 using ordinary Gaussian solves. It also checks exact
LDL factorization, reconstruction, inverse identities, determinants, 80
nonzero polynomial squares and the witness value. The first twelve values are

\[
1,1,1,4,17,17,290,81515,81798,6644043123,479723268580926,5/4.
\]

All 37,588 finite assertions passed on the recorded run. Among them are all
nine exceptional pairs and 15,288 parity-compatible pairs through degree 25.
These ranges are explicit and do not purport to prove (MP) or positivity at
unexamined degrees. Sections 2–6 supply those universal proofs.

Negative controls reject replacing the Schur complement by −1, a false
monotonicity claim, and zero extension of a finite prefix. In particular,
keeping only \(j_1,\ldots,j_{10}\) and setting later values to zero gives
\(\Lambda((y^4-1)^2)=-163029\). Thus finite-prefix computation alone is not a
license to replace the genuine infinite recurrence by a zero tail.

The earlier ternary truncated Lean functional in
`lean-truncated-moment-obstruction-20261010` is a **different functional**, with
different dimension, witness and moments. Its documented higher-degree failure
is unchanged. This construction neither extends its specified truncated data
nor retroactively upgrades its Lean theorem. It independently supplies the
stronger full-algebra mathematical countermodel.

This example by itself is not a positive-time evolution satisfying a coercive
heat or diffusion equation; it supplies no counterexample to a theorem with
additional growth or dynamical assumptions. It proves neither determinate
moment reconstruction nor a moment representation algorithm. The absence of
any representing measure is the conclusion.

## 9. Prior art and source verification

Konrad Schmüdgen, *The Moment Problem* (2017), Proposition 13.4 and Proposition
13.5, printed pp. 318–319, give the polynomial family containing this witness
and an explicit positive nonmoment functional. The exceptional enumeration,
seed values and parity convention are drawn from that construction. Its later
diagonals use a factorial growth formula. Section 13.12, printed p. 355,
attributes the explicit functional to J. Friedrich, “A note on the two
dimensional moment problem.” The present work substitutes (2) for the later
diagonal choice and proves that substitution directly; it makes no novelty
claim for the phenomenon or the recurrence.

Source: https://www.imath.kiev.ua/~golub/ref2/The-Moment-Problem.pdf

The searchable PDF text was inspected at the named propositions and the
attribution. PDF screenshot requests for pages 318 and 319 failed with
“Cache miss”; no visual page verification is claimed. Bibliographic details of
the original Friedrich article were not independently checked. No exact
typographical interpretation of the book's large factorial expression is
needed by the alternative recurrence or its proof.
