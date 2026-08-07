# SANITIZED REVIEW COPY: supply owner-controlled evidence paths before execution.
#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'rereviews'/'PMR-007_DEEP_Q_DISTINCT_MATRIX_AND_LOSS_REREVIEW_RESULTS.json'
SRC=Path('EVIDENCE_ID:ASFAHANI_TRANSLATED_PRIMARY_ACCESS')
R=random.Random(20260805)

def inv(p):
    q=[0]*len(p)
    for i,v in enumerate(p): q[v]=i
    return q

def tau(ei,ej):
    ii=inv(ei)
    return [ej[ii[x]] for x in range(len(ei))]

def compose(f,g): return [f[g[x]] for x in range(len(g))]

def mat(p):
    n=len(p); M=[[0]*n for _ in range(n)]
    for x,y in enumerate(p): M[y][x]=1
    return M

def mm(A,B):
    n=len(A)
    return [[sum(A[i][k]*B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def tr(A): return [list(x) for x in zip(*A)]

def main():
    random_systems=0; matrix_law_checks=0; matrix_failures=0; predicate_checks=0; predicate_failures=0
    for n in (6,7,8):
        ident=list(range(n))
        for _ in range(3000):
            E=[ident[:]]
            for _j in range(3):
                p=ident[:]; R.shuffle(p); E.append(p)
            P=[mat(e) for e in E]
            T={(i,j):tau(E[i],E[j]) for i in range(4) for j in range(4)}
            TM={(i,j):mm(P[j],tr(P[i])) for i in range(4) for j in range(4)}
            random_systems += 1
            for i in range(4):
                for j in range(4):
                    matrix_law_checks += 1
                    if TM[(i,j)] != mat(T[(i,j)]): matrix_failures += 1
                    for k in range(4):
                        matrix_law_checks += 1
                        if mm(TM[(j,k)],TM[(i,j)]) != TM[(i,k)]: matrix_failures += 1
            for _ in range(12):
                subset={x for x in range(n) if R.getrandbits(1)}
                imgs=[{E[i][c] for c in subset} for i in range(4)]
                for i in range(4):
                    for j in range(4):
                        predicate_checks += 1
                        got={T[(i,j)][x] for x in imgs[i]}
                        if got != imgs[j]: predicate_failures += 1

    # Minimal lossy and partial controls.
    C={0,1}
    lossy={0:'x',1:'x'}
    pred={0}
    lossy_image={lossy[c] for c in pred}
    complement_image={lossy[c] for c in C-pred}
    lossy_collision = bool(lossy_image & complement_image)
    partial={0:'x'}
    partial_missing = 1 not in partial

    src=SRC.read_bytes(); h=hashlib.sha256(src).hexdigest(); text=src.decode('utf-8',errors='replace').lower()
    source_checks={
      'expected_hash':'932abd7e2d7b3702d5d6d77d2a4a95ecfb3a9ccbcfbbce7ae750b2bcf55bef7c',
      'actual_hash':h,
      'hash_match':h=='932abd7e2d7b3702d5d6d77d2a4a95ecfb3a9ccbcfbbce7ae750b2bcf55bef7c',
      'uncreated_speech_found':'speech is uncreated' in text or 'uncreated speech of allah' in text,
      'subsists_in_him_found':'speech that subsists in him' in text or 'speech subsists in him' in text,
      'translator_preface_found':"translator’s preface" in text or "translator's preface" in text,
    }
    overall=(matrix_failures==0 and predicate_failures==0 and lossy_collision and partial_missing and all(source_checks.values()))
    res={
      'identity':'PMR-007-FEAG-1',
      'method':'random permutation-matrix groupoid verification plus lossy/partial controls and direct source custody',
      'random_systems':random_systems,
      'matrix_law_checks':matrix_law_checks,
      'matrix_failures':matrix_failures,
      'predicate_transport_checks':predicate_checks,
      'predicate_transport_failures':predicate_failures,
      'lossy_control':{'predicate_collision':lossy_collision},
      'partial_control':{'missing_content':partial_missing},
      'source_checks':source_checks,
      'overall':'PASS' if overall else 'FAIL',
      'scope_notes':[
        'Finite exact bijective encodings only.',
        'Random matrix rereview does not prove absolute articulability or metaphysical possibility.',
        'Source wording remains translated-primary access and Track-N conditional.'
      ]
    }
    OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
    print(json.dumps(res,indent=2,sort_keys=True))
if __name__=='__main__': main()
