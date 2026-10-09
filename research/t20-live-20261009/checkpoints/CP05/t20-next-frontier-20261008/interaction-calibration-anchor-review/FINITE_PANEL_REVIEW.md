# Separate independent review: finite interaction panel

8 October 2026 UTC. Verdict: PASS, within the explicit positive-support promise
and certified population Cauchy-oracle contract. No mathematical blocker found.
This receipt is separately scoped from REVIEW.md. It does not assert support-
absence decidability, finite-sample exact recovery, whole-map finite-panel
recovery, a uniform precision/runtime bound, physical certification or closure.

## 1. What is being accepted

For a promised positive integer multiplicity n_S on a known support S with at
least two roots, four isolated values from a nondegenerate interior 2-by-2
command panel identify n_S. They are obtained from finitely many raw masked
endpoint probabilities, not necessarily four raw measurements. Under the stated
population approximation oracle, half-integer determinant comparisons recover n_S
with finitely many sign decisions and accuracy refinements, without testing
whether an approximated real is exactly zero.

## 2. Proof check

For each corner, the isolated value is Z_pq=(1-K a_p b_q)^n, with positive K<=1
and strictly ordered 0<a_1<a_2<1, 0<b_1<b_2<1. The fixed interior K correctly
handles interactions of order greater than two. No raw log at a unit command is
introduced; all masked Q values used as divisors are positive.

For candidate m>0, P_m(p,q)=H_(n/m)(K a_p b_q). Set c=n/m and

    e_c(z)=z H'_c(z)/H_c(z).

The author's substitution t=-log(1-z) correctly gives

    e_c(z)=c (exp(t)-1)/(exp(c t)-1),
    d log(e_c)/dt = [f(t)-f(c t)]/t,
    f(t)=t/(1-exp(-t)).

The expression for f' is correct, and exp(t)>1+t implies f'>0. Therefore e_c
strictly decreases with z for c>1 and strictly increases for c<1. The function
log H_c(K exp(s+t)) has mixed derivative of strict sign 1-c throughout the
nondegenerate rectangle of log a and log b values. Integrating the derivative
yields the same strict sign for its logarithmic cross difference. All four
entries are positive, so comparing the two diagonal products preserves that
sign. The determinant orientation in the appendix is consequently correct:

    sign Delta(m)=sign(m-n),

and zero occurs exactly at m=n. Only the explicit H_c is differentiated, not the
unknown calibrations.

An independent exact algebra check for c=2 gives the determinant identity

    det[H_2(K a_p b_q)]
      = -2 K^3 a_1 a_2 b_1 b_2 (a_2-a_1)(b_2-b_1) < 0.

This is consistent with the claimed sign and rules out reversing the cut test.

## 3. Computability and termination audit

1. Positive raw probabilities admit eventually certified positive lower bounds
   from the supplied rational approximation intervals. Finite products and
   divisions then yield certified shrinking intervals for every isolated Z.
   Unknown small denominators affect cost, not individual termination.
2. At m=k+1/2, the exponent 1/m=2/(2k+1) is a rational exponent with odd positive
   denominator. Rational bisection of the (2k+1)-st root of Z^2 supplies a Cauchy
   name for the corresponding P entry. The argument also works when an
   intermediate approximation interval touches an endpoint, by clipping to the
   promised [0,1] range and refining.
3. Standard positive interval products and subtraction enclose the determinant.
   Because n is a positive integer, a half-integer cut can never equal n. Its
   determinant is nonzero, so eventually a certified interval excludes zero.
4. Positive sign at k+1/2 is equivalent to n<=k; negative sign is equivalent to
   n>=k+1. Doubling k=1,2,4,... eventually gives an upper bound because n is
   finite. Binary search with the same cuts then terminates at the integer n.
5. Only precision is adaptively refined. The distinct raw command vectors are
   the fixed finite mask panel selected at the beginning. This does not provide
   a finite Bernoulli sample procedure or a cost bound independent of the world.
6. When n=0, all Z equal one and every determinant is zero. The accepted
   terminating procedure explicitly excludes this case. The appendix correctly
   limits itself to that observation rather than claiming a broader
   impossibility theorem for every design or additional assumption.

## 4. Calibration scope

At the true n the matrix is rank one. Ratios of rows and columns identify the
specified relative factor ratios, but reciprocal rescaling of interior a and b
values preserves their products and admits homeomorphic interpolation through
sampled nominal points. For larger supports K adds further nuisance freedom.
Even when other information determines absolute sampled values, an arbitrary
homeomorphism between unqueried commands is not fixed by a finite command panel.
The appendix does not conflate these finite-panel limitations with the main
full-function limit inverse.

## 5. Exact controls and independent Cauchy-input check

The author's panel_controls.py was copied into this review directory and
replayed. Its 548 assertions pass; the replay JSON is byte-identical to the
author JSON. The original author file was not executed in place or changed.
Its controls correctly describe their starting input as exact rational Z.

The independent_panel_controls.py program was separately written for this review.
Its recovery routine receives only certified intervals for raw masked Q values.
It propagates their uncertainty through the support-mask products and quotients,
then through rational root brackets and determinant intervals. Two oracle-name
styles are exercised. Exact rational fixtures are used to generate valid names
and to verify the final count, not passed to the recovery routine as exact Z.

Observed result: PASS.

- 40 complete recoveries: n=1,...,10; supports of size two and three; two valid
  approximation-interval styles; lower-order nuisance routes remain present.
- 320 terminating half-integer sign decisions, including both adjacent cuts.
- 36 zero-support interval checks retain zero rather than falsely deciding sign.
- Three exact c=2 determinant factorizations, including a small-rate case.
- 21,104 raw-oracle calls; the largest precision used by these particular
  controls was 32 bisection bits. These are diagnostic counts, not theorem bounds.

The full mathematical sign and computability claims follow from the proof audit;
the finite tests are supporting controls only. The SHA-bound receipt identifies
the exact appendix, author script, author output, and independent work reviewed.
