#!/usr/bin/env python3
"""Exact supporting controls for the fixed-group audit theorem, not its proof."""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CHECKS: list[dict[str, object]] = []


def record(name: str, count: int = 1, detail: str = "") -> None:
    CHECKS.append({"name": name, "count": count, "status": "passed", "detail": detail})


def require(condition, detail="check failed") -> None:
    if not condition:
        raise RuntimeError(str(detail))


def zero(expr: sp.Expr) -> None:
    result = sp.factor(expr)
    require(result == 0, result)


def vec_zero(xs) -> None:
    for x in xs:
        zero(x)


def simplify_vec(xs):
    return tuple(sp.factor(x) for x in xs)


def audit(w, factors):
    z = sum(a * wi for a, wi in zip(factors, w))
    return tuple(a * wi / z for a, wi in zip(factors, w))


def push_weight_tangent(w, u, factors):
    z = sum(a * wi for a, wi in zip(factors, w))
    dz = sum(a * ui for a, ui in zip(factors, u))
    out = audit(w, factors)
    return tuple(a * ui / z - wi * dz / z for a, ui, wi in zip(factors, u, out))


w1, w2, w3 = ws = sp.symbols("w1 w2 w3", positive=True)
x1, x2, x3 = xs = sp.symbols("x1 x2 x3", real=True)
alpha, a, b = sp.symbols("alpha a b", positive=True)
E = w1 * w2 / (w1 + w2) * (x1 - x2) ** 2
DE = tuple(sp.diff(E, w) for w in ws)
DX = tuple(sp.diff(E, x) for x in xs)


def field(w, x, rate=alpha, energy=E):
    substitutions = dict(zip(ws + xs, tuple(w) + tuple(x)))
    partials = tuple(sp.diff(energy, wi).subs(substitutions, simultaneous=True) for wi in ws)
    mean = sum(wi * di for wi, di in zip(w, partials))
    fw = tuple(-rate * wi * (di - mean) for wi, di in zip(w, partials))
    fx = tuple(-sp.diff(energy, xi).subs(substitutions, simultaneous=True) / wi for wi, xi in zip(w, xs))
    return simplify_vec(fw), simplify_vec(fx)


def covariance_residual(w, x, factors, rate=alpha, energy=E):
    fw, fx = field(w, x, rate, energy)
    aw = audit(w, factors)
    afw, afx = field(aw, x, rate, energy)
    pushed = push_weight_tangent(w, fw, factors)
    return simplify_vec(afwi - p for afwi, p in zip(afw, pushed)), simplify_vec(afxi - fi for afxi, fi in zip(afx, fx))


def main() -> None:
    bindings = json.loads((HERE / "INPUT_BINDINGS.json").read_text())
    for entry in bindings:
        for path in (HERE / entry["copy"], ROOT / entry["source"]):
            data = path.read_bytes()
            require(len(data) == entry["bytes"], str(path))
            require(hashlib.sha256(data).hexdigest() == entry["sha256"], str(path))
    record("copied and unchanged original input hashes", 2 * len(bindings))

    m, r = sp.symbols("m r", positive=True)
    dm, dr, v1, v2, v3 = sp.symbols("dm dr v1 v2 v3", real=True)
    w = (m * r, m * (1-r), 1-m)
    dw = (r * dm + m * dr, (1-r) * dm - m * dr, -dm)
    fisher_fine = sum(ui**2 / wi for ui, wi in zip(dw, w)) / alpha
    fisher_coarse = (dm**2 / (m*(1-m)) + m * dr**2 / (r*(1-r))) / alpha
    zero(fisher_fine - fisher_coarse)
    transport_fine = sum(wi * vi**2 for wi, vi in zip(w, (v1, v2, v3)))
    transport_coarse = m*(r*v1**2 + (1-r)*v2**2) + (1-m)*v3**2
    zero(transport_fine - transport_coarse)
    record("metric decomposition with conditional-simplex tangent", 2)

    fw, fx = field(w, xs)
    vec_zero(fx_i - expected for fx_i, expected in zip(fx, (2*(1-r)*(x2-x1), -2*r*(x2-x1), 0)))
    mdot = sp.factor(fw[0]+fw[1])
    rdot = sp.factor((fw[0]-r*mdot)/m)
    zero(rdot + alpha*r*(1-r)*(1-2*r)*(x2-x1)**2)
    zero(mdot + alpha*m*(1-m)*r*(1-r)*(x2-x1)**2)
    record("joint position and conditional and mass field formulas", 5)

    # The coordinates m and r encode the full normalized positive simplex.
    rw, rx = covariance_residual(w, xs, (a,a,b))
    vec_zero(rw + rx)
    record("symbolic full joint covariance for arbitrary positive group factors and alpha", 6)

    q = sp.Rational
    initial_w = (q(1,3), q(1,3), q(1,3))
    initial_x = (sp.Integer(0), sp.Integer(1), sp.Integer(2))
    original = field(initial_w, initial_x, 1)
    audited = field(audit(initial_w,(2,1,1)), initial_x, 1)
    require(original[1] == (1,-1,0))
    require(audited[1] == (q(2,3),-q(4,3),0))
    rw, rx = covariance_residual(initial_w, initial_x, (2,1,1), 1)
    require(rx == (-q(1,3),-q(1,3),0))
    require(any(e != 0 for e in rw))
    require(sp.factor(sp.diff(E,x1,x2)) == -2*w1*w2/(w1+w2))
    zero(sp.diff(E.subs({w1:m*r,w2:m*(1-r)}, simultaneous=True), r, 2)+2*m*(x1-x2)**2)
    record("singleton noncovariance and genuine two kinds of nonseparability", 6,
           "At thirds and positions (0,1,2), old velocities (1,-1,0), new (2/3,-4/3,0).")

    # Distinct rational fixtures vary relative masses, both group factors and positions.
    for k in range(1, 61):
        unnormalized = (sp.Integer(k+1), sp.Integer((k % 7)+2), sp.Integer((k % 11)+3))
        norm = sum(unnormalized)
        fixture_w = tuple(t/norm for t in unnormalized)
        fixture_x = (q(k % 5, 3), q((k % 13)+1, 4), q(-(k % 17), 5))
        factors = (q((k % 9)+1, 3),) * 2 + (q((k % 6)+1, 7),)
        rw, rx = covariance_residual(fixture_w, fixture_x, factors, q((k % 4)+1,2))
        vec_zero(rw + rx)
    record("exact rational full-field group audit fixtures", 60)

    weight_only = w1*w2/(w1+w2)
    rw, rx = covariance_residual(w, xs, (a,a,b), energy=weight_only)
    vec_zero(rw+rx)
    rw, _ = covariance_residual(initial_w,initial_x,(2,1,1),1,weight_only)
    require(any(v != 0 for v in rw))
    record("parent weight-only candidate positive and negative controls", 2)

    forbidden = (w1+w2)*w3
    fixture_w = (q(1,4),q(1,4),q(1,2))
    old, _ = field(fixture_w,initial_x,1,forbidden)
    require(old == (0,0,0))
    rw, _ = covariance_residual(fixture_w,initial_x,(2,2,1),1,forbidden)
    require(rw == (q(1,27),q(1,27),-q(2,27)))
    record("forbidden nonlinear group-mass energy is not groupcovariant", 1,
           "E=m1*m2 has zero old field and nonzero audited field (1/27,1/27,-2/27).")

    t, d0, c, s0 = sp.symbols("t d0 c s0", real=True)
    d = d0 * sp.exp(-2*t)
    path_x = (c-d/2, c+d/2, x3)
    A = sp.exp(-alpha*d0**2*(1-sp.exp(-4*t))/16)
    s = s0*A/(s0*A+1-s0)
    path_w = (s/2,s/2,1-s)
    path_fw,path_fx=field(path_w,path_x)
    vec_zero(sp.diff(yi,t)-fi for yi,fi in zip(path_x,path_fx))
    vec_zero(sp.diff(wi,t)-fi for wi,fi in zip(path_w,path_fw))
    transformed_s0=a*s0/(a*s0+b*(1-s0))
    after_audit=a*s/(a*s+b*(1-s))
    audited_from_origin=s.subs(s0,transformed_s0)
    zero(after_audit-audited_from_origin)
    record("exact moving-position trajectory and group-audit commutation", 7)

    aa,ab,ba,bb=sp.symbols("aa ab ba bb",positive=True)
    row_column=(aa*ba,aa*bb,ab*ba,ab*bb)
    zero(row_column[0]*row_column[3]-row_column[1]*row_column[2])
    p11,p12,p21,p22=sp.symbols("p11 p12 p21 p22",positive=True)
    out=audit((p11,p12,p21,p22),row_column)
    zero(out[0]*out[3]/(out[1]*out[2])-p11*p22/(p12*p21))
    require(2*1 != 1*1)
    record("row-column action odds-ratio invariant and absent singleton factor", 3)

    payload={
        "status":"passed",
        "run_utc":datetime.now(timezone.utc).isoformat(),
        "engine":f"Python / SymPy {sp.__version__}",
        "python_optimize":sys.flags.optimize,
        "checks_use_assert":False,
        "control_groups":len(CHECKS),
        "control_count":sum(int(c["count"]) for c in CHECKS),
        "checks":CHECKS,
        "scope":"Exact author controls supplement the written theorem; not independent review or formal-kernel proof.",
        "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "report_sha256":hashlib.sha256((HERE/"RESULT.md").read_bytes()).hexdigest(),
    }
    output = "EXACT_CHECKS_OPTIMIZED.json" if sys.flags.optimize else "EXACT_CHECKS.json"
    (HERE/output).write_text(json.dumps(payload,indent=2)+"\n")
    print(json.dumps(payload,indent=2))


if __name__ == "__main__":
    main()
