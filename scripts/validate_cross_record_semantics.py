#!/usr/bin/env python3
"""Cross-record semantic validator (R3 7.2, extended R4 7.4). Deterministic, offline.

Checks that JSON Schema cannot express, over every example file's parts and any
bundle handed to `collect_issues(parts)`.

R3 checks (all preserved):
  - episode.analysis == each meta-token.analysis (id and version);
  - episode.occurrence == each meta-token.anchor (identity and version);
  - unique evidence/token/claim ids within a record;
  - verdict record: pathway_state recomputes exactly from statuses over
    required_path; every not-applicable status on the required path has a
    recorded na_reason; per_token_v3c token ids resolve against the episode's
    meta-tokens (when both records are present in one example); the V3c
    aggregate matches per-token statuses; required_path respects the shipped
    governance derivation for the episode's shape (GOV_TOKEN_ADEQUATE required
    iff tokens exist; ROUTE_ADMISSIBLE iff a route was selected);
  - binder and executor remain distinct ROLES;
  - handoff state_claims carry valid_for_version (anti-transport rule);
  - closure floor: no closure claim over an unresolved residual unless the
    bundle's verdict record convicts it.

R4 additions (the reference-model semantic contract the schemas cannot carry):
  - id uniqueness ACROSS a bundle (episodes, packets, standalone tokens, claim
    and burden ids per episode, analysis editions);
  - reference resolution: claim ids, token ids, evidence ids, handoff episode
    ids, rel_spec/perturb_spec keys, analysis inheritance;
  - analysis/version compatibility across episode, ledger claims and the verdict
    record's objectivity index;
  - occurrence/version anchoring across orthemma parts, episodes and handoff
    subjects;
  - metaorthemma scope vs the claims that actually depend on the token;
  - single-typing of of_type (plural MetaInst is an unimplemented extension);
  - claim dependency cycle detection over depends_on_claims;
  - residual conditional-field completeness per disposition;
  - required-path status completeness stated as its own finding;
  - na_reasons for EVERY not-applicable status anywhere, not only on the
    required path;
  - claim-level AND episode-level pathway recomputation: claim_reasoning_paths
    must recompute from the statuses of their own req_reason projection, and
    that projection must sit inside ReqPath (B2);
  - RelSpec declared_at must precede any recorded result time (pre-outcome
    declaration);
  - PerturbSpec invariants must not appear in varied_fields.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def aggregate(statuses, path):
    """Four-valued conjunction over a verdict path. MALFORMED is not a state of
    the world: it means the record cannot be read as making a claim at all."""
    if not path:
        return "MALFORMED"
    if any(statuses.get(v) in (None, "not-applicable") for v in path):
        return "MALFORMED"
    if any(statuses[v] == "fail" for v in path):
        return "defective"
    if any(statuses[v] == "undetermined" for v in path):
        return "undetermined"
    return "adequate"


def recompute_pathway(inst):
    return aggregate(inst["statuses"], inst["required_path"])


def dups(seq):
    seen, out = set(), []
    for x in seq:
        if x in seen and x not in out:
            out.append(x)
        seen.add(x)
    return out


def _time_of(episode):
    """Start of an episode's time interval ('a/b' -> 'a')."""
    return (episode.get("time") or "").split("/")[0]


def collect_issues(parts):
    """Return a list of semantic-issue strings for one bundle of parts."""
    issues = []

    def inst_of(s):
        return [p["instance"] for p in parts if p["schema"] == s]

    episodes = inst_of("orthing-episode.schema.json")
    verdicts = inst_of("verdict-record.schema.json")
    ledgers = inst_of("claim-ledger.schema.json")
    analyses = inst_of("analysis.schema.json")
    orthemmas = inst_of("orthemma.schema.json")
    standalone_token_recs = inst_of("metaorthemma.schema.json")
    standalone_tokens = {t["token_id"] for t in standalone_token_recs}
    standalone_handoffs = inst_of("handoff.schema.json")

    all_token_recs = list(standalone_token_recs)
    for ep in episodes:
        all_token_recs += list(ep.get("meta_tokens", []))
    all_token_ids = {t["token_id"] for t in all_token_recs}

    all_handoffs = list(standalone_handoffs)
    for ep in episodes:
        all_handoffs += (ep.get("handoffs_in") or []) + (ep.get("handoffs_out") or [])

    episode_by_id = {e.get("episode_id"): e for e in episodes}
    ledger_by_episode = {}
    for led in ledgers:
        ledger_by_episode.setdefault(led.get("episode_id"), []).append(led)
    analysis_by_id = {}
    for a in analyses:
        analysis_by_id.setdefault(a.get("analysis_id"), set()).add(a.get("version"))
    orthemma_versions = {}
    for o in orthemmas:
        orthemma_versions.setdefault(o.get("identity_key"), set()).add(o.get("version"))

    # ---- token identity rule (R4 independent review, D3): token_id is GLOBALLY
    # unique across the bundle. A standalone record may redeclare an embedded
    # token (same id) only when of_type and anchor agree — that is one token
    # recorded twice, not two tokens. Every token has one owning episode; a
    # standalone token names it via owning_episode or declares an explicit
    # external scope (D4/D6).
    owner_of = {}
    embedded_by_id = {}
    for ep in episodes:
        for tok in ep.get("meta_tokens", []):
            tid = tok["token_id"]
            if tid in owner_of:
                issues.append("token %s: embedded in more than one episode (%s and %s) — "
                              "token_id must be globally unique across the bundle"
                              % (tid, owner_of[tid], ep.get("episode_id")))
            owner_of[tid] = ep.get("episode_id")
            embedded_by_id[tid] = tok
    known_episode_ids = (set(episode_by_id) | set(ledger_by_episode)
                         | {v.get("episode_id") for v in verdicts})
    for t in standalone_token_recs:
        tid = t["token_id"]
        if tid in embedded_by_id:
            emb = embedded_by_id[tid]
            if (emb.get("of_type"), emb.get("anchor")) != (t.get("of_type"), t.get("anchor")):
                issues.append("token %s: standalone record conflicts with the embedded "
                              "declaration (of_type/anchor differ) — same id must mean "
                              "the same token" % tid)
            continue
        own = t.get("owning_episode")
        ext = (t.get("scope") or {}).get("external_scope")
        if own:
            owner_of[tid] = own
            if own not in known_episode_ids:
                issues.append("token %s: owning_episode %s names no episode, ledger, or "
                              "verdict record in the bundle" % (tid, own))
        elif not ext:
            issues.append("token %s: standalone record names no owning_episode and "
                          "declares no external scope — its claim scope is uncheckable"
                          % tid)

    # ------------------------------------------------- 1. id uniqueness (bundle)
    for label, seq in (
            ("episode", [e.get("episode_id") for e in episodes]),
            ("handoff packet", [h.get("packet_id") for h in all_handoffs]),
            ("standalone metaorthemma token", [t["token_id"] for t in standalone_token_recs]),
            ("analysis edition", ["%s@%s" % (a.get("analysis_id"), a.get("version"))
                                  for a in analyses])):
        d = dups(seq)
        if d:
            issues.append("bundle: duplicate %s id(s) %s" % (label, d))
    for eid, leds in sorted(ledger_by_episode.items(), key=lambda kv: str(kv[0])):
        cids = [c["claim_id"] for led in leds for c in led.get("claims", [])]
        bids = [r["burden_id"] for led in leds for r in led.get("residuals", [])]
        if dups(cids):
            issues.append("%s: duplicate claim id(s) %s across the episode's ledger(s)"
                          % (eid, dups(cids)))
        if dups(bids):
            issues.append("%s: duplicate burden id(s) %s across the episode's ledger(s)"
                          % (eid, dups(bids)))

    # -------------------------------------------------- 2. analysis inheritance
    for a in analyses:
        par = a.get("inherits_from")
        if par and par.get("version") not in analysis_by_id.get(par.get("analysis_id"), set()):
            issues.append("analysis %s: inherits_from %s@%s does not resolve in the bundle"
                          % (a.get("analysis_id"), par.get("analysis_id"), par.get("version")))

    # ---------------------------------------------------------------- 3. episodes
    for ep in episodes:
        eid = ep.get("episode_id", "?")
        ean, eoc = ep.get("analysis", {}), ep.get("occurrence", {})

        known = analysis_by_id.get(ean.get("analysis_id"))
        if known and ean.get("version") not in known:
            issues.append("%s: episode analysis %s@%s is not a declared edition (declared: %s)"
                          % (eid, ean.get("analysis_id"), ean.get("version"), sorted(known)))
        kv = orthemma_versions.get(eoc.get("identity_key"))
        if kv and eoc.get("version") not in kv:
            issues.append("%s: episode occurrence %s@%s is not a declared version (declared: %s)"
                          % (eid, eoc.get("identity_key"), eoc.get("version"), sorted(kv)))

        for tok in ep.get("meta_tokens", []):
            tan, tanc = tok.get("analysis", {}), tok.get("anchor", {})
            if (tan.get("analysis_id"), tan.get("version")) != (ean.get("analysis_id"), ean.get("version")):
                issues.append("%s: meta-token %s analysis mismatch (%s vs %s)"
                              % (eid, tok.get("token_id"), tan, ean))
            if (tanc.get("identity_key"), tanc.get("version")) != (eoc.get("identity_key"), eoc.get("version")):
                issues.append("%s: meta-token %s anchored to a different occurrence (%s vs %s)"
                              % (eid, tok.get("token_id"), tanc, eoc))
            if not tok.get("binder", {}).get("actor"):
                issues.append("%s: meta-token %s lacks an independent binder role"
                              % (eid, tok.get("token_id")))

        ev_ids = [e["evidence_id"] for e in ep.get("evidence", [])]
        if len(ev_ids) != len(set(ev_ids)):
            issues.append("%s: duplicate evidence ids %s"
                          % (eid, sorted({i for i in ev_ids if ev_ids.count(i) > 1})))
        tok_ids = [t["token_id"] for t in ep.get("meta_tokens", [])]
        if len(tok_ids) != len(set(tok_ids)):
            issues.append("%s: duplicate token ids" % eid)

        for h in (ep.get("handoffs_in") or []) + (ep.get("handoffs_out") or []):
            for c in h.get("state_claims", []):
                if not c.get("valid_for_version"):
                    issues.append("%s: handoff claim %s lacks valid_for_version"
                                  % (eid, c.get("claim_id")))

    # ----------------------------------------- 4. metaorthemma typing and binder
    for tok in all_token_recs:
        tid = tok.get("token_id", "?")
        oft = tok.get("of_type")
        if not isinstance(oft, dict) or set(oft) != {"mu_id", "mu_version"}:
            issues.append("token %s: of_type must be exactly ONE metaortheme reference "
                          "(single-typing is the R4 rule; plural MetaInst is an unimplemented "
                          "future extension)" % tid)
        if not tok.get("binder", {}).get("binding_warrant"):
            issues.append("token %s: binder records no binding warrant" % tid)
        if not tok.get("binding"):
            issues.append("token %s: empty binding — a metaorthemma exists only where material "
                          "binding exists (M1 zero-burden rule)" % tid)

    # ---------------------------------------------------------------- 5. handoffs
    for h in all_handoffs:
        pid = h.get("packet_id", "?")
        for role in ("sender_episode", "receiver_episode"):
            ref = h.get(role)
            if episodes and ref not in episode_by_id:
                issues.append("handoff %s: %s %r resolves to no episode in the bundle"
                              % (pid, role, ref))
        subj = h.get("subject", {})
        for role in ("sender_episode", "receiver_episode"):
            ep = episode_by_id.get(h.get(role))
            if ep is None:
                continue
            occ = ep.get("occurrence", {})
            if (occ.get("identity_key"), occ.get("version")) != \
                    (subj.get("identity_key"), subj.get("version")):
                issues.append("handoff %s: subject %s@%s is not the %s's occurrence %s@%s — a "
                              "packet whose subject version drifts from its endpoint's is exactly "
                              "how stale state propagates"
                              % (pid, subj.get("identity_key"), subj.get("version"), role,
                                 occ.get("identity_key"), occ.get("version")))

    # ----------------------------------------------------------------- 6. ledgers
    for led in ledgers:
        eid = led.get("episode_id", "?")
        ep = episode_by_id.get(eid)
        claim_ids = {c["claim_id"] for c in led.get("claims", [])}
        ep_evidence = {e["evidence_id"] for e in ep.get("evidence", [])} if ep else None
        ep_an = ep.get("analysis", {}) if ep else None

        for c in led.get("claims", []):
            cid = c["claim_id"]
            can = c.get("analysis", {})
            known = analysis_by_id.get(can.get("analysis_id"))
            if known and can.get("version") not in known:
                issues.append("%s: claim %s cites analysis %s@%s, not a declared edition"
                              % (eid, cid, can.get("analysis_id"), can.get("version")))
            if ep_an and (can.get("analysis_id"), can.get("version")) != \
                    (ep_an.get("analysis_id"), ep_an.get("version")):
                issues.append("%s: claim %s is indexed to %s but its episode runs under %s"
                              % (eid, cid, can, ep_an))
            if ep_evidence is not None:
                miss = [e for e in c.get("evidence_ids", []) if e not in ep_evidence]
                if miss:
                    issues.append("%s: claim %s cites evidence %s absent from the episode"
                                  % (eid, cid, miss))
            if all_token_ids:
                miss = [t for t in c.get("depends_on_tokens", []) if t not in all_token_ids]
                if miss:
                    issues.append("%s: claim %s depends on token(s) %s that exist nowhere in the "
                                  "bundle" % (eid, cid, miss))
            miss = [q for q in c.get("depends_on_claims", []) if q not in claim_ids]
            if miss:
                issues.append("%s: claim %s depends on claim(s) %s absent from the ledger"
                              % (eid, cid, miss))

        # claim dependency cycles over depends_on_claims
        graph = {c["claim_id"]: [q for q in c.get("depends_on_claims", []) if q in claim_ids]
                 for c in led.get("claims", [])}
        state, reported = {}, set()

        def walk(node, stack):
            if state.get(node) == "done":
                return
            if state.get(node) == "open":
                cyc = stack[stack.index(node):]
                key = tuple(sorted(set(cyc)))
                if key not in reported:
                    reported.add(key)
                    issues.append("%s: claim dependency cycle %s" % (eid, " -> ".join(cyc)))
                return
            state[node] = "open"
            for nxt in graph.get(node, []):
                walk(nxt, stack + [nxt])
            state[node] = "done"

        for node in sorted(graph):
            walk(node, [node])

        # residual conditional completeness (mirrors the schema if/then, and also
        # catches records that never reach the schema layer)
        need = {
            "unresolved": [("responsible_queue",), ("next_review_condition",)],
            "deferred": [("trigger", "review_date")],
            "transferred": [("receiver",), ("transfer_record",)],
            "owner-assigned": [("owner",), ("acceptance_state",)],
            "risk-accepted": [("risk_owner",), ("rationale",), ("scope",), ("review_trigger",)],
            "validated-resolved": [("evidence_refs", "verdict_refs")],
        }
        for r in led.get("residuals", []):
            for group in need.get(r.get("disposition"), []):
                if not any(r.get(f) for f in group):
                    issues.append("%s: residual %s disposed %r without %s"
                                  % (eid, r.get("burden_id"), r.get("disposition"),
                                     " or ".join(group)))

        # closure floor (R3, Definition 13): a closure claim over an unresolved
        # residual is ill-formed UNLESS the bundle's verdict record convicts it
        # (CLOSURE_TRUTHFUL fail/undetermined), in which case the record is a
        # legitimate REPRESENTATION of a false closure (the O3 case, F6).
        if led.get("closure_claim") is not None:
            bad = [r["burden_id"] for r in led.get("residuals", [])
                   if r["disposition"] == "unresolved"]
            if bad:
                vr = next((v for v in verdicts if v.get("episode_id") == eid), None)
                convicted = vr is not None and vr.get("statuses", {}).get(
                    "CLOSURE_TRUTHFUL") in ("fail", "undetermined")
                if not convicted:
                    issues.append("%s: closure claim asserted over unresolved residual(s) %s "
                                  "(false closure)" % (eid, bad))

    # ------------------------------------------- 7. token scope vs dependent claims
    scope_of = {}
    for tok in all_token_recs:
        scope_of.setdefault(tok["token_id"], set()).update(
            (tok.get("scope") or {}).get("claims") or [])
    for led in ledgers:
        eid = led.get("episode_id", "?")
        claim_ids = {c["claim_id"] for c in led.get("claims", [])}
        for c in led.get("claims", []):
            for t in c.get("depends_on_tokens", []):
                if t in scope_of and c["claim_id"] not in scope_of[t]:
                    issues.append("%s: claim %s depends on token %s but no record of that token "
                                  "scopes it (declared scope: %s)"
                                  % (eid, c["claim_id"], t, sorted(scope_of[t])))
    # R4 independent review (D4): a token's claim scope is checked ONLY against
    # its OWNING episode's ledger(s). The pre-repair loop compared every token
    # against every ledger, so any two legitimate episodes with claim-scoped
    # tokens produced reciprocal false positives
    # (examples/shared-upstream-corroboration-failure.json is the regression).
    for tid, scoped in sorted(scope_of.items()):
        own = owner_of.get(tid)
        if own is None or own not in ledger_by_episode:
            continue  # unattributable standalone tokens are flagged above (D3/D6)
        own_claims = {c["claim_id"] for led in ledger_by_episode[own]
                      for c in led.get("claims", [])}
        miss = sorted(q for q in scoped if q not in own_claims)
        if miss:
            issues.append("%s: token %s scopes claim(s) %s absent from its owning "
                          "episode's ledger(s)" % (own, tid, miss))

    # --------------------------------------------------------- 8. verdict records
    for vr in verdicts:
        vid = vr.get("episode_id", "?")
        statuses, req = vr["statuses"], vr["required_path"]

        missing = [v for v in req if v not in statuses]
        if missing:
            issues.append("%s: required verdict(s) %s carry no status at all" % (vid, missing))

        state = recompute_pathway(vr)
        if state != vr.get("pathway_state"):
            issues.append("%s: pathway_state %r does not recompute (computed %r)"
                          % (vid, vr.get("pathway_state"), state))

        # na_reasons for EVERY not-applicable status, not only on the required path
        for v, s in sorted(statuses.items()):
            if s == "not-applicable" and v not in vr.get("na_reasons", {}):
                issues.append("%s: %s not-applicable without a recorded reason" % (vid, v))

        ep = episode_by_id.get(vid)
        idx = vr.get("index", {})
        if ep is not None:
            ean = ep.get("analysis", {})
            if (idx.get("analysis_id"), idx.get("analysis_version")) != \
                    (ean.get("analysis_id"), ean.get("version")):
                issues.append("%s: verdict index cites %s@%s but the episode runs under %s@%s"
                              % (vid, idx.get("analysis_id"), idx.get("analysis_version"),
                                 ean.get("analysis_id"), ean.get("version")))
            has_tokens = bool(ep.get("meta_tokens"))
            if has_tokens != ("GOV_TOKEN_ADEQUATE" in req):
                issues.append("%s: GOV_TOKEN_ADEQUATE requirement does not match token presence "
                              "(zero-burden rule)" % vid)
            if ep.get("route") is not None and "ROUTE_ADMISSIBLE" not in req:
                issues.append("%s: route selected but ROUTE_ADMISSIBLE not required" % vid)
            tok_ids = {t["token_id"] for t in ep.get("meta_tokens", [])} | standalone_tokens
            for pt in vr.get("per_token_v3c", []):
                if pt["token_id"] not in tok_ids:
                    issues.append("%s: per_token_v3c references unknown token %s"
                                  % (vid, pt["token_id"]))
            if vr.get("per_token_v3c") and "GOV_TOKEN_ADEQUATE" in statuses:
                agg = ("fail" if any(pt["status"] == "fail" for pt in vr["per_token_v3c"])
                       else "undetermined" if any(pt["status"] == "undetermined"
                                                  for pt in vr["per_token_v3c"])
                       else "pass")
                if agg != statuses["GOV_TOKEN_ADEQUATE"]:
                    issues.append("%s: V3c aggregate %r does not match per-token statuses "
                                  "(computed %r)" % (vid, statuses["GOV_TOKEN_ADEQUATE"], agg))
        else:
            for pt in vr.get("per_token_v3c", []):
                if pt["token_id"] not in standalone_tokens:
                    issues.append("%s: per_token_v3c token %s has no episode or standalone token "
                                  "record to resolve against" % (vid, pt["token_id"]))

        # claim references
        led_claims = {c["claim_id"] for led in ledger_by_episode.get(vid, [])
                      for c in led.get("claims", [])}
        for label, ids in (
                ("claim_verdicts", [c["claim_id"] for c in vr.get("claim_verdicts", [])]),
                ("claim_reasoning_paths",
                 [c["claim_id"] for c in vr.get("claim_reasoning_paths", [])]),
                ("rel_spec", sorted(vr.get("rel_spec", {}))),
                ("perturb_spec", sorted(vr.get("perturb_spec", {})))):
            if led_claims:
                miss = [c for c in ids if c not in led_claims]
                if miss:
                    issues.append("%s: %s references claim(s) %s absent from the ledger"
                                  % (vid, label, miss))
            if dups(ids):
                issues.append("%s: %s carries duplicate claim id(s) %s" % (vid, label, dups(ids)))

        # claim-relative reasoning paths (B2): recomputed over their OWN projection
        for crp in vr.get("claim_reasoning_paths", []):
            cid, rr = crp["claim_id"], crp["req_reason"]
            outside = [v for v in rr if v not in req]
            if outside:
                issues.append("%s: claim %s reasoning path cites %s outside ReqPath — ReqReason_q "
                              "is a PROJECTION of ReqPath, never an extension" % (vid, cid, outside))
            recomputed = aggregate(statuses, rr)
            if recomputed != crp["reasoning_path_adequate"]:
                issues.append("%s: claim %s reasoning_path_adequate %r does not recompute over its "
                              "own req_reason (computed %r)"
                              % (vid, cid, crp["reasoning_path_adequate"], recomputed))

        # RelSpec: pre-outcome declaration
        result_times = [t for t in (idx.get("decision_time"),
                                    _time_of(ep) if ep is not None else None) if t]
        for cid, rs in sorted(vr.get("rel_spec", {}).items()):
            if not isinstance(rs, dict):
                issues.append("%s: rel_spec[%s] is a free-form value, not a typed RelSpec"
                              % (vid, cid))
                continue
            dat = rs.get("declared_at")
            for rt in result_times:
                if dat is not None and dat >= rt:
                    issues.append("%s: RelSpec for claim %s declared at %s, not before the recorded "
                                  "result time %s — a reliability figure declared at or after the "
                                  "outcome is not a pre-outcome declaration" % (vid, cid, dat, rt))
                    break

        # PerturbSpec: invariants and varied fields are disjoint
        for cid, ps in sorted(vr.get("perturb_spec", {}).items()):
            if not isinstance(ps, dict):
                issues.append("%s: perturb_spec[%s] is a free-form value, not a typed PerturbSpec"
                              % (vid, cid))
                continue
            both = sorted(set(ps.get("invariants", [])) & set(ps.get("varied_fields", [])))
            if both:
                issues.append("%s: PerturbSpec for claim %s declares %s as BOTH invariant and "
                              "varied — the neighborhood is incoherent" % (vid, cid, both))

    return issues


def main():
    edir = os.path.join(ROOT, "examples")
    total = 0
    for fn in sorted(os.listdir(edir)):
        if not fn.endswith(".json"):
            continue
        ex = json.load(open(os.path.join(edir, fn), encoding="utf-8"))
        issues = collect_issues(ex.get("parts", []))
        total += 1
        check("example %s cross-record semantics" % fn, not issues, "; ".join(issues[:3]))
    check("examples scanned", total >= 7, str(total))
    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
