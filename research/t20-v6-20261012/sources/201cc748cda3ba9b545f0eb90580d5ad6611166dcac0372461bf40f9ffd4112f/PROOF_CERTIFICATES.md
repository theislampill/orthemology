# Readable quantified inference certificates

These are the exact premises and target formulas consumed by the local checker. The JSON contains each explicit proof step; the checker computes intermediate conclusions rather than trusting claimed ones.

`world` and `entity` are distinct sorts. `Actual`, `Root`, `Dep`, `TotalGround`, and `GroundExistence` have the interpretation supplied in the manuscript; interpretation is not proved by this checker. Necessity is expanded as `FOR ALL world: Ex(world, entity)`, not treated as an uninterpreted `Necessary` atom. Concreteness and well-foundedness belong to the paper-level premises and are not established by the three inference certificates.

The code is a newly authored many-sorted classical natural-deduction checker, not Lean and not independently audited. It proves conditional inference only.

## Certificate 1: Actual root plus contingent-dependence entails a necessary actual entity

Checked nodes: 21. Rules: andI, andL, andR, existsE, existsI, forallE, hyp, impE, raa.

### Open premises

**root_exists**

```text
EXISTS x:entity: (Actual(x:entity) AND Root(x:entity))
```

**contingent_existence_requires_parent**

```text
FOR ALL x:entity: (Actual(x:entity) -> ((FOR ALL w:world: Ex(w:world, x:entity) -> FALSE) -> EXISTS y:entity: (Actual(y:entity) AND Dep(y:entity, x:entity))))
```

**root_definition**

```text
FOR ALL x:entity: (Root(x:entity) -> FOR ALL y:entity: (Dep(y:entity, x:entity) -> FALSE))
```

### Target

```text
EXISTS x:entity: (Actual(x:entity) AND FOR ALL w:world: Ex(w:world, x:entity))
```

### Step index

| Step | Rule | Earlier premises |
|---:|---|---|
| 0 | `hyp` |  |
| 1 | `hyp` |  |
| 2 | `hyp` |  |
| 3 | `hyp` |  |
| 4 | `andL` | 3 |
| 5 | `andR` | 3 |
| 6 | `forallE` | 1 |
| 7 | `impE` | 6, 4 |
| 8 | `hyp` |  |
| 9 | `impE` | 7, 8 |
| 10 | `hyp` |  |
| 11 | `andR` | 10 |
| 12 | `forallE` | 2 |
| 13 | `impE` | 12, 5 |
| 14 | `forallE` | 13 |
| 15 | `impE` | 14, 11 |
| 16 | `existsE` | 9, 15 |
| 17 | `raa` | 16 |
| 18 | `andI` | 4, 17 |
| 19 | `existsI` | 18 |
| 20 | `existsE` | 0, 19 |

## Certificate 2: A fixed indispensable bearer of a necessary condition exists necessarily

Checked nodes: 6. Rules: forallE, forallI, hyp, impE.

### Open premises

**condition_is_necessary**

```text
FOR ALL w:world: Q(w:world)
```

**same_bearer_is_required**

```text
FOR ALL w:world: (Q(w:world) -> Ex(w:world, fixed_bearer:entity[constant]))
```

### Target

```text
FOR ALL u_eigen:world: Ex(u_eigen:world, fixed_bearer:entity[constant])
```

### Step index

| Step | Rule | Earlier premises |
|---:|---|---|
| 0 | `hyp` |  |
| 1 | `hyp` |  |
| 2 | `forallE` | 0 |
| 3 | `forallE` | 1 |
| 4 | `impE` | 3, 2 |
| 5 | `forallI` | 4 |

## Certificate 3: Complete actual explanation of contingent existence is not itself contingent

Checked nodes: 18. Rules: andI, andL, andR, existsE, existsI, forallE, hyp, impE, raa.

### Open premises

**total_explanation_exists**

```text
EXISTS x:entity: (Actual(x:entity) AND TotalGround(x:entity))
```

**explanation_projects_to_contingent_members**

```text
FOR ALL x:entity: (TotalGround(x:entity) -> FOR ALL y:entity: ((Actual(y:entity) AND (FOR ALL w:world: Ex(w:world, y:entity) -> FALSE)) -> GroundExistence(x:entity, y:entity)))
```

**no_complete_self_explanation**

```text
FOR ALL x:entity: (GroundExistence(x:entity, x:entity) -> FALSE)
```

### Target

```text
EXISTS x:entity: (Actual(x:entity) AND FOR ALL w:world: Ex(w:world, x:entity))
```

### Step index

| Step | Rule | Earlier premises |
|---:|---|---|
| 0 | `hyp` |  |
| 1 | `hyp` |  |
| 2 | `hyp` |  |
| 3 | `hyp` |  |
| 4 | `andL` | 3 |
| 5 | `andR` | 3 |
| 6 | `hyp` |  |
| 7 | `andI` | 4, 6 |
| 8 | `forallE` | 1 |
| 9 | `impE` | 8, 5 |
| 10 | `forallE` | 9 |
| 11 | `impE` | 10, 7 |
| 12 | `forallE` | 2 |
| 13 | `impE` | 12, 11 |
| 14 | `raa` | 13 |
| 15 | `andI` | 4, 14 |
| 16 | `existsI` | 15 |
| 17 | `existsE` | 0, 16 |

## Rejected controls

Eleven deliberately invalid certificates cover final-target replacement, illicit generalisation, escaping existential witnesses, sort mismatch, capture, omitted assumptions, wrong modus ponens, an unlicensed oracle rule and an altered intermediate conclusion. See `proof_check_results.json` for each actual rejection. Their rejection is evidence about this checker on those cases, not a general independent soundness certification.
