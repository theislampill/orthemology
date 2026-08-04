# AR8R-T299 — matched-intervention burden-landing certification

## Custody and status

- Historical identity: `AR8R-T299`
- Canonical repaired-payload SHA-256: `c2b70f73a3b490ae12311802615c788df07fd1734d725686fc8b912faea304c7`
- Preserved pre-repair SHA-256: `4b64280cbf8fe51324cb2d55836eca396f47f4adbd757f648f40448bdf0ce12d`
- Formal status: `VALIDATED_SCOPED_CENTRAL_ARCHITECTURE_CHARACTERIZATION`
- Frontier status: `MENISCUS_PRESSURE`; `FRONTIER_NOT_SECURELY_LOCATED`
- No general mathematical novelty is claimed.

## Declared finite setting

Let an episode-transition model be finite and deterministic. Let `A` be the
declared operation coordinate and let `term(a,b)` be the terminal state under
operation value `a` and background coordinate `b`. Let:

- `Q` be the declared target predicate;
- `D_b` be the burden-disposition field;
- `R_b` be the whole-field reread result; and
- `C` be the custody check.

For a matched background `b`, causal landing `L_b` requires all of:

1. `Q(term(1,b)) = 1`;
2. `Q(term(0,b)) = 0`;
3. `D_b(term(1,b)) = LANDED`;
4. the declared whole-field reread passes;
5. `D_b(term(0,b)) != LANDED`; and
6. custody passes.

This is the declared matched operation/no-operation comparison.

## Characterization

For any declared profile map `P`, causal landing is profile-certifiable exactly when
`L_b` is constant on every fibre of `P`. Equivalently, an exact profile-level
certificate exists precisely when two backgrounds with the same profile never
receive different causal-landing values.

The proof is the finite factorization criterion: if a profile certificate exists,
equal-profile backgrounds must have equal labels; conversely, constancy on each
fibre defines the certificate unambiguously on the attained profile image.

## Scope firewall

- A before/after actual-state delta is insufficient without the matched
  no-operation contrast and the remaining disposition, reread, and custody guards.
- The complete matched intervention profile is sufficient by construction.
- witnessed landing is not causally attributed landing.
- This is not a complete theory of actual causation.
- It makes no general claim about human, noetic, theological, or metaphysical
  restoration.
- It does not establish the truth or completeness of any real-world profile.

The theorem is retained as a bounded historical AR8R result. Repository inclusion
records custody and scope; it does not create a new independent theorem origin.

## Exact repaired causal/spontaneous twin

The repaired historical payload supplies two models that must remain distinct.

- In `M_cause`, `Q(S_term^(a))=a`, and `D_b(S_term^(a))=LANDED` iff `a=1`.
- In `M_spont`, `Q(S_term^(a))=1` and `D_b(S_term^(a))=LANDED` for both `a=0,1`, because an independent background event lands the burden.
- Under `A=1`, the before/after observations match across the models.
- Nevertheless, `L_b(M_cause,u)=1` while `L_b(M_spont,u)=0`.

The matched profile is

`B*(M,u)=(C(M,u), Q(S_term^(0)), Q(S_term^(1)), D_b(S_term^(0)), D_b(S_term^(1)), R_b(S_term^(1)))`.

Version custody remains split: the repaired exact payload is 5,217 bytes with
SHA-256 `c2b70f73a3b490ae12311802615c788df07fd1734d725686fc8b912faea304c7`;
the pre-repair payload is 4,631 bytes with SHA-256
`4b64280cbf8fe51324cb2d55836eca396f47f4adbd757f648f40448bdf0ce12d`.
The summary does not merge or overwrite those historical versions.
