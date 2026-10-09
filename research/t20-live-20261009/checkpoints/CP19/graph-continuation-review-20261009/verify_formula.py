#!/usr/bin/env python3
"""Independent all-labelled-graphs BFS versus connected-superset formula."""
from collections import deque
from itertools import combinations
from time import perf_counter
import json

def graph_data(n, code):
    adj = [0] * n
    edges = list(combinations(range(n), 2))
    for k, (i,j) in enumerate(edges):
        if code >> k & 1:
            adj[i] |= 1 << j
            adj[j] |= 1 << i
    return adj

def bfs(adj, starts=None):
    n = len(adj)
    dist = [-1] * (1 << n)
    q = deque(starts if starts is not None else [1 << i for i in range(n)])
    for m in q: dist[m] = 0
    while q:
        m = q.popleft()
        active = m
        togglable = 0
        while active:
            b = active & -active
            active -= b
            togglable |= adj[b.bit_length()-1]
        while togglable:
            b = togglable & -togglable
            togglable -= b
            target = m ^ b
            if dist[target] < 0:
                dist[target] = dist[m] + 1
                q.append(target)
    return dist

def connected_tau(adj):
    n = len(adj)
    inf = 10**9
    tau = [inf] * (1 << n)
    for m in range(1, 1 << n):
        reached = m & -m
        wave = reached
        while wave:
            b = wave & -wave
            wave -= b
            added = adj[b.bit_length()-1] & m & ~reached
            reached |= added
            wave |= added
        if reached == m: tau[m] = m.bit_count()
    # Minimum connected superset size, computed independently of gate moves.
    for i in range(n):
        for m in range(1 << n):
            if not (m >> i & 1): tau[m] = min(tau[m], tau[m | (1 << i)])
    return tau

def main():
    start = perf_counter()
    results=[]
    for n in range(1,7):
        graphs = 1 << (n * (n-1) // 2)
        pairs = 0
        max_cost = 0
        for code in range(graphs):
            adj = graph_data(n, code)
            dist = bfs(adj)
            tau = connected_tau(adj)
            assert dist[0] == -1
            for m in range(1,1 << n):
                expected = 2*tau[m] - m.bit_count() - 1 if tau[m] < 10**9 else -1
                assert dist[m] == expected, (n, code, m, dist[m], expected)
                max_cost = max(max_cost, dist[m])
                pairs += 1
            # Check fixed-root strengthening on all n<=5.
            if n <= 5:
                for r in range(n):
                    fixed = bfs(adj,[1 << r])
                    for m in range(1,1 << n):
                        t = tau[m | (1 << r)]
                        expected = 2*t - m.bit_count() - 1 if t < 10**9 else -1
                        assert fixed[m] == expected, ('fixed',n,code,r,m,fixed[m],expected)
        record = dict(n=n, labelled_graphs=graphs, nonempty_graph_mask_pairs=pairs,
                      maximum_finite_minimum_cost=max_cost)
        results.append(record)
        print(json.dumps(record), flush=True)
    out = dict(results=results, total_graphs=sum(r['labelled_graphs'] for r in results),
               total_nonempty_graph_mask_pairs=sum(r['nonempty_graph_mask_pairs'] for r in results),
               all_passed=True, fixed_root_checked_through_n=5,
               runtime_seconds=round(perf_counter()-start,3))
    with open('[OMITTED_PRIVATE_MACHINE_PATH]','w') as f:
        json.dump(out,f,indent=2)
    print(json.dumps(out),flush=True)

if __name__=='__main__': main()
