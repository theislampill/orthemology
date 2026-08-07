#!/usr/bin/env python3
"""Distinct direct-semantic rereview of PMR-007 Round 15 V2.

This script does not import the primary Round-15 checker. It independently:
  * verifies the repaired frozen hashes;
  * canonicalizes model custody;
  * enumerates memoryless strategies;
  * computes CORE_ENTRY and co-Buchi winning regions from graph/SCC semantics;
  * computes minimax core-entry steps and bad-visit bounds;
  * tests the selected witnesses and all registered guard-deletion fixtures;
  * reruns the actual current-main daee validators.
"""
from __future__ import annotations

from copy import deepcopy
from itertools import product
from pathlib import Path
from typing import Any
import hashlib
import importlib.util
import json
import subprocess
import sys
import time

import yaml

BASE = Path(__file__).resolve().parents[1]
REPO = Path('PRIVATE_EVIDENCE_REFERENCE:orthemology-main')
MODEL = BASE / 'models/PMR007_ROUND15_TEMPORAL_RESTORATION_CERTIFICATES_V2.yaml'
RECORD = BASE / 'models/PMR007_ROUND15_SHARED_CURRENT_TRANSITION_RECORD.json'
OUTPUT = Path(__file__).with_name('PMR-007_FRONTIER_ROUND15_V2_FRESH_REREVIEW_RESULTS.json')

EXPECTED = {
    'PMR-007_FRONTIER_ROUND15_DAEE_TEMPORAL_CERTIFICATE_ARCHITECTURE_V2.md': '879681edd0f28a35ba9bd87f049ad60c10ea5369474fb8bf2d092de88251299c',
    'models/PMR007_ROUND15_SHARED_CURRENT_TRANSITION_RECORD.json': 'da0b58ac75391c8ba4387332e5c7be3bdda578a4363f23c626d1f08e102d799f',
    'models/PMR007_ROUND15_TEMPORAL_RESTORATION_CERTIFICATES_V2.yaml': '1fbd97bd04fc4ab09bc8c259ff045723128da831cfacfbe18ea0ebc8cdc3ebda',
    'checks/pmr007_round15_temporal_certificate_check_v2.py': 'a281b947794c0977a217fabbdbfafb79b2d7f8854ec1e3f39e586ea73e6fbf52',
    'checks/pmr007_round15_temporal_certificate_check_v2_results.json': 'a92dcf7af41c0893d4b4996d6a54d38ee43b59867861c8675179dc920f8c9fb1',
    'audits/PMR-007_FRONTIER_ROUND15_V1_COLD_AUDIT.md': 'a52fcc7e858db20eeae966d656efc84aa58f5bf63ba7f132f002a174a3838533',
    'repairs/PMR-007_FRONTIER_ROUND15_REPAIR_LOG.md': '2c62f902709a00ef3b832ae20f07ba44df9f0ec9d7b287a7290e893c56444bb3',
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_model(cert: dict[str, Any]) -> bytes:
    action_rows = []
    for state in sorted(cert['actions']):
        for action in sorted(cert['actions'][state], key=lambda x: str(x['action_id'])):
            action_rows.append({
                'action_id': action['action_id'],
                'eligibility_epoch': action['eligibility_epoch'],
                'eligibility_ref': action['eligibility_ref'],
                'state': state,
                'successors': sorted(action['successors']),
            })
    obj = {
        'actions': action_rows,
        'model_completeness': {
            key: cert['model_completeness'][key]
            for key in sorted(cert['model_completeness'])
        },
        'safe_states': sorted(cert['safe_states']),
        'source_version_epoch': cert['source_version_epoch'],
        'states': sorted(cert['states']),
        'target_states': sorted(cert['target_states']),
    }
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def model_hash(cert: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_model(cert)).hexdigest()


def enumerate_strategies(cert: dict[str, Any]):
    states = list(cert['states'])
    menus = [cert['actions'][q] for q in states]
    for selection in product(*menus):
        yield {
            q: {
                'action_id': action['action_id'],
                'successors': frozenset(action['successors']),
            }
            for q, action in zip(states, selection)
        }


def adjacency(strategy: dict[str, dict[str, Any]]) -> dict[str, frozenset[str]]:
    return {q: action['successors'] for q, action in strategy.items()}


def reachable(adj: dict[str, frozenset[str]], start: str) -> frozenset[str]:
    seen = {start}
    todo = [start]
    while todo:
        q = todo.pop()
        for nxt in adj[q]:
            if nxt not in seen:
                seen.add(nxt)
                todo.append(nxt)
    return frozenset(seen)


def tarjan(adj: dict[str, frozenset[str]]) -> list[frozenset[str]]:
    counter = 0
    stack: list[str] = []
    on_stack: set[str] = set()
    index: dict[str, int] = {}
    low: dict[str, int] = {}
    components: list[frozenset[str]] = []

    def visit(v: str) -> None:
        nonlocal counter
        index[v] = low[v] = counter
        counter += 1
        stack.append(v)
        on_stack.add(v)
        for w in adj[v]:
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on_stack:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = set()
            while True:
                w = stack.pop()
                on_stack.remove(w)
                comp.add(w)
                if w == v:
                    break
            components.append(frozenset(comp))

    for v in adj:
        if v not in index:
            visit(v)
    return components


def cyclic_nodes(adj: dict[str, frozenset[str]]) -> set[str]:
    out: set[str] = set()
    for comp in tarjan(adj):
        if len(comp) > 1 or any(v in adj[v] for v in comp):
            out |= set(comp)
    return out


def target_invariant_winners_for_strategy(
    strategy: dict[str, dict[str, Any]],
    Target: set[str],
) -> set[str]:
    adj = adjacency(strategy)
    return {
        q for q in Target
        if reachable(adj, q) <= Target
    }


def direct_kernel(cert: dict[str, Any]) -> set[str]:
    Target = set(cert['target_states'])
    K: set[str] = set()
    for strategy in enumerate_strategies(cert):
        K |= target_invariant_winners_for_strategy(strategy, Target)
    return K


def core_winners_for_strategy(
    strategy: dict[str, dict[str, Any]],
    Safe: set[str],
    K: set[str],
) -> set[str]:
    adj = adjacency(strategy)
    cyclic = cyclic_nodes(adj)
    winners = set()
    for q in strategy:
        R = set(reachable(adj, q))
        if q not in Safe or not R <= Safe:
            continue
        if any(k in R and not adj[k] <= K for k in K):
            continue
        # Every infinite path must hit K: no reachable cycle may remain outside K.
        if (R & cyclic) - K:
            continue
        winners.add(q)
    return winners


def cob_winners_for_strategy(
    strategy: dict[str, dict[str, Any]],
    Safe: set[str],
    Target: set[str],
) -> set[str]:
    adj = adjacency(strategy)
    Bad = Safe - Target
    bad_cycle_nodes: set[str] = set()
    for comp in tarjan(adj):
        cyclic = len(comp) > 1 or any(v in adj[v] for v in comp)
        if cyclic and comp & Bad:
            bad_cycle_nodes |= set(comp & Bad)
    winners = set()
    for q in strategy:
        R = set(reachable(adj, q))
        if q in Safe and R <= Safe and not (R & bad_cycle_nodes):
            winners.add(q)
    return winners


def longest_before_kernel(adj: dict[str, frozenset[str]], start: str, K: set[str]) -> int | None:
    """Worst-case number of transitions before first K, or None if not forced."""
    memo: dict[str, int] = {}
    visiting: set[str] = set()

    def value(q: str) -> int | None:
        if q in K:
            return 0
        if q in memo:
            return memo[q]
        if q in visiting:
            return None
        visiting.add(q)
        vals = []
        for nxt in adj[q]:
            v = value(nxt)
            if v is None:
                visiting.remove(q)
                return None
            vals.append(v)
        visiting.remove(q)
        memo[q] = 1 + max(vals)
        return memo[q]

    return value(start)


def max_bad_visits(adj: dict[str, frozenset[str]], start: str, Bad: set[str]) -> int | None:
    """Maximum bad-state occurrences over paths, or None if unbounded."""
    memo: dict[str, int] = {}
    visiting: set[str] = set()

    def value(q: str) -> int | None:
        if q in memo:
            return memo[q]
        if q in visiting:
            # A target-only cycle can be traversed forever with no additional bad
            # visits. A recursion containing Bad is unbounded.
            return None if q in Bad else 0
        visiting.add(q)
        child_values = []
        for nxt in adj[q]:
            v = value(nxt)
            if v is None:
                visiting.remove(q)
                return None
            child_values.append(v)
        visiting.remove(q)
        memo[q] = (1 if q in Bad else 0) + max(child_values, default=0)
        return memo[q]

    # Use SCC semantics first; the recursive value is only run after bad cycles
    # are known absent, avoiding target-cycle recursion ambiguity.
    R = set(reachable(adj, start))
    for comp in tarjan(adj):
        cyclic = len(comp) > 1 or any(v in adj[v] for v in comp)
        if cyclic and comp & Bad and comp & R:
            return None

    # Condense target SCCs by fixed-point relaxation of finite bad-count values.
    values = {q: (1 if q in Bad else 0) for q in adj}
    for _ in range(len(adj) * len(adj) + 1):
        changed = False
        for q in adj:
            candidate = (1 if q in Bad else 0) + max(values[nxt] for nxt in adj[q])
            if candidate > values[q]:
                values[q] = candidate
                changed = True
        if not changed:
            return values[start]
    # If growth continues despite no bad SCC, something is inconsistent.
    return None


def direct_regions_and_minimax(cert: dict[str, Any]) -> dict[str, Any]:
    Safe = set(cert['safe_states'])
    Target = set(cert['target_states'])
    Bad = Safe - Target
    K = direct_kernel(cert)
    core_union: set[str] = set()
    cob_union: set[str] = set()
    core_min: dict[str, int] = {}
    cob_min_bad: dict[str, int] = {}
    strategy_count = 0
    for strategy in enumerate_strategies(cert):
        strategy_count += 1
        adj = adjacency(strategy)
        core_win = core_winners_for_strategy(strategy, Safe, K)
        cob_win = cob_winners_for_strategy(strategy, Safe, Target)
        core_union |= core_win
        cob_union |= cob_win
        for q in core_win:
            v = longest_before_kernel(adj, q, K)
            if v is not None:
                core_min[q] = min(core_min.get(q, v), v)
        for q in cob_win:
            v = max_bad_visits(adj, q, Bad)
            if v is not None:
                cob_min_bad[q] = min(cob_min_bad.get(q, v), v)
    return {
        'strategy_count': strategy_count,
        'K': K,
        'W_core': core_union,
        'W_coB': cob_union,
        'core_rank': core_min,
        'cob_outer_rank': {q: value + 1 for q, value in cob_min_bad.items()},
    }


def selected_strategy(cert: dict[str, Any]) -> dict[str, dict[str, Any]] | None:
    out = {}
    for q, action_id in cert['declared']['strategy'].items():
        matches = [a for a in cert['actions'][q] if a['action_id'] == action_id]
        if not matches:
            return None
        out[q] = {'action_id': action_id, 'successors': frozenset(matches[0]['successors'])}
    # Add arbitrary actions outside the declared region only for graph totality.
    for q in cert['states']:
        if q not in out:
            a = cert['actions'][q][0]
            out[q] = {'action_id': a['action_id'], 'successors': frozenset(a['successors'])}
    return out


def assess_certificate(cert: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        'certificate_id': cert.get('certificate_id'),
        'model_digest_match': cert.get('model_digest') == model_hash(cert),
        'epoch_consistent': all(
            action.get('eligibility_epoch') == cert.get('source_version_epoch')
            for menu in cert.get('actions', {}).values() for action in menu
        ),
        'successor_relation_declared_complete': (
            cert.get('model_completeness', {}).get('declared_successor_relation_complete_for_scope') is True
        ),
    }
    direct = direct_regions_and_minimax(cert)
    result['direct'] = {
        'strategy_count': direct['strategy_count'],
        'K': sorted(direct['K']),
        'W_core': sorted(direct['W_core']),
        'W_coB': sorted(direct['W_coB']),
        'core_rank': direct['core_rank'],
        'cob_outer_rank': direct['cob_outer_rank'],
    }
    kind = cert.get('certificate_kind')
    declared = cert.get('declared', {})
    if kind == 'CORE_ENTRY':
        result['region_match'] = (
            set(declared.get('stable_kernel', [])) == direct['K']
            and set(declared.get('winning_region', [])) == direct['W_core']
        )
        result['rank_match'] = declared.get('rank') == direct['core_rank']
    elif kind == 'CO_BUCHI_PERSISTENCE':
        result['region_match'] = set(declared.get('winning_region', [])) == direct['W_coB']
        result['rank_match'] = declared.get('rank') == direct['cob_outer_rank']
    else:
        result['region_match'] = False
        result['rank_match'] = False

    strategy = selected_strategy(cert)
    if strategy is None:
        result['selected_strategy_semantics'] = False
    else:
        Safe = set(cert['safe_states'])
        Target = set(cert['target_states'])
        if kind == 'CORE_ENTRY':
            win = core_winners_for_strategy(strategy, Safe, direct['K'])
            result['selected_strategy_semantics'] = set(declared.get('winning_region', [])) <= win
        else:
            win = cob_winners_for_strategy(strategy, Safe, Target)
            result['selected_strategy_semantics'] = set(declared.get('winning_region', [])) <= win
    result['pass'] = all([
        result['model_digest_match'],
        result['epoch_consistent'],
        result['successor_relation_declared_complete'],
        result['region_match'],
        result['rank_match'],
        result['selected_strategy_semantics'],
    ])
    return result


def apply_mutation(obj: Any, path: str, value: Any) -> None:
    parts = path.split('.')
    cur = obj
    for part in parts[:-1]:
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    last = parts[-1]
    if isinstance(cur, list):
        cur[int(last)] = value
    else:
        cur[last] = value


def independent_fixture_assessment(fixture: dict[str, Any], base: dict[str, Any]) -> dict[str, Any]:
    cert = deepcopy(base)
    for key, value in fixture['mutation'].items():
        if '.' in key:
            apply_mutation(cert, key, value)
        elif key == 'declared':
            cert['declared'] = value
        else:
            cert[key] = value
    if fixture.get('recompute_model_digest_after_mutation'):
        cert['model_digest'] = model_hash(cert)

    expected = fixture['expected_error']
    observed_guard: str | None = None
    if cert.get('model_digest') != model_hash(cert):
        observed_guard = 'model-digest-mismatch'
    elif any(
        a.get('eligibility_epoch') != cert.get('source_version_epoch')
        for menu in cert.get('actions', {}).values() for a in menu
    ):
        observed_guard = 'eligibility-epoch-mismatch'
    elif cert.get('model_completeness', {}).get('declared_successor_relation_complete_for_scope') is not True:
        observed_guard = 'successor-relation-not-declared-complete'
    else:
        # Detect ineligible action before direct graph analysis.
        for q, action_id in cert.get('declared', {}).get('strategy', {}).items():
            if not any(a['action_id'] == action_id for a in cert['actions'][q]):
                observed_guard = 'strategy-action-not-eligible'
                break
    if observed_guard is None:
        direct = direct_regions_and_minimax(cert)
        declared = cert['declared']
        if cert['certificate_kind'] == 'CORE_ENTRY':
            if set(declared.get('stable_kernel', [])) != direct['K']:
                observed_guard = 'stable-kernel-mismatch'
            elif set(declared.get('winning_region', [])) != direct['W_core']:
                observed_guard = 'winning-region-mismatch'
            elif declared.get('rank') != direct['core_rank']:
                observed_guard = 'rank-mismatch'
            else:
                strat = selected_strategy(cert)
                win = core_winners_for_strategy(strat, set(cert['safe_states']), direct['K']) if strat else set()
                if not set(declared.get('winning_region', [])) <= win:
                    observed_guard = 'strategy-rank-not-decreasing'
        else:
            if set(declared.get('winning_region', [])) != direct['W_coB']:
                observed_guard = 'winning-region-mismatch'
            elif declared.get('rank') != direct['cob_outer_rank']:
                observed_guard = 'rank-mismatch'
            else:
                strat = selected_strategy(cert)
                win = cob_winners_for_strategy(strat, set(cert['safe_states']), set(cert['target_states'])) if strat else set()
                if not set(declared.get('winning_region', [])) <= win:
                    observed_guard = 'strategy-violates-cobuchi'
    return {
        'fixture_id': fixture['fixture_id'],
        'expected_error': expected,
        'independent_observed_guard': observed_guard,
        'pass': observed_guard == expected,
    }


def run_current_validators() -> dict[str, Any]:
    out = {}
    for rel in [
        'scripts/validate_corrective_transition.py',
        'scripts/validate_semantic_operator_contract.py',
        'scripts/validate_daee_current_crosswalk.py',
        'scripts/validate_meta_noetic_memetics.py',
    ]:
        proc = subprocess.run([sys.executable, rel], cwd=REPO, text=True, capture_output=True, check=False)
        out[rel] = {
            'returncode': proc.returncode,
            'status': 'PASS' if proc.returncode == 0 else 'FAIL',
            'last_line': (proc.stdout.strip().splitlines() or [''])[-1],
        }
    return out


def load_current_validator():
    path = REPO / 'scripts/validate_corrective_transition.py'
    spec = importlib.util.spec_from_file_location('r15_current_validator', path)
    if spec is None or spec.loader is None:
        raise RuntimeError('could not load current transition validator')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    start = time.perf_counter()
    hash_checks = {
        rel: {
            'expected': expected,
            'actual': digest(BASE / rel),
            'pass': digest(BASE / rel) == expected,
        }
        for rel, expected in EXPECTED.items()
    }
    doc = yaml.safe_load(MODEL.read_text(encoding='utf-8'))
    certs = {c['certificate_id']: c for c in doc['certificates']}

    certificate_results = {cid: assess_certificate(cert) for cid, cert in certs.items()}
    fixture_results = {
        f['fixture_id']: independent_fixture_assessment(f, certs[f['base_certificate_id']])
        for f in doc['invalid_fixtures']
    }

    current_validator = load_current_validator()
    current_record = json.loads(RECORD.read_text(encoding='utf-8'))
    current_ok, current_reason = current_validator.document_ok(current_record)
    repo_validators = run_current_validators()

    # The primary result is frozen and hash-verified above. It is parsed as a
    # regression receipt rather than rerun inside this process; the direct
    # semantic checks below are the independent rereview evidence.
    primary_result = json.loads((BASE / 'checks/pmr007_round15_temporal_certificate_check_v2_results.json').read_text())

    overall = (
        all(x['pass'] for x in hash_checks.values())
        and all(x['pass'] for x in certificate_results.values())
        and all(x['pass'] for x in fixture_results.values())
        and current_ok
        and all(x['status'] == 'PASS' for x in repo_validators.values())
        and primary_result.get('overall') == 'PASS'
    )
    result = {
        'review': 'PMR-007 Round 15 V2 distinct direct-semantic fresh rereview',
        'review_relation': 'same-model procedural rereview; separate implementation; not external human or independent model-lineage review',
        'methods': [
            'independent canonical model serialization and SHA-256',
            'complete memoryless-strategy enumeration for each supplied finite model',
            'Tarjan SCC and direct temporal graph semantics',
            'minimax worst-case core-entry steps',
            'minimax worst-case bad-state occurrence counts',
            'independent negative-fixture guard assessment',
            'actual current-main validator rerun',
        ],
        'frozen_hashes': hash_checks,
        'certificate_results': certificate_results,
        'negative_fixture_results': fixture_results,
        'shared_current_transition_record': {
            'sha256': digest(RECORD),
            'current_validator_status': 'PASS' if current_ok else 'FAIL',
            'reason': current_reason,
        },
        'current_repository_validators': repo_validators,
        'primary_checker_regression': {
            'frozen_result_hash_verified': hash_checks['checks/pmr007_round15_temporal_certificate_check_v2_results.json']['pass'],
            'overall': primary_result.get('overall'),
        },
        'authority_ceiling': 'finite declared-model exactness only; external review, model completeness, source truth, target adequacy, causality, human restoration, and owner adoption remain open',
        'elapsed_seconds': time.perf_counter() - start,
        'overall': 'PASS' if overall else 'FAIL',
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
    return 0 if overall else 1


if __name__ == '__main__':
    raise SystemExit(main())
