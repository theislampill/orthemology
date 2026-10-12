#!/usr/bin/env python3
"""Independent controls and frozen-input replay; not a formal proof checker."""
import argparse
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

import sympy as S

BASE = Path(__file__).resolve().parent
AUTHOR = BASE / "author_snapshot"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest(base, filename):
    manifest = json.loads((base / filename).read_text())
    for name, expected in manifest["files"].items():
        assert sha(base / name) == expected, (base, name)
    digest = hashlib.sha256("".join(
        name + "\0" + value + "\n"
        for name, value in sorted(manifest["files"].items())
    ).encode()).hexdigest()
    assert digest == manifest["snapshot_digest"]
    return manifest


parser = argparse.ArgumentParser()
parser.add_argument("--output-dir", type=Path, required=True)
parser.add_argument("--original-root", type=Path)
args = parser.parse_args()
assert not args.output_dir.exists(), "Choose a fresh output directory"
author_manifest = verify_manifest(AUTHOR, "FROZEN_MANIFEST.json")
assert author_manifest["snapshot_digest"] == "eb5f5453dcc43b21b7d061ad6dbd2f4d3e8467440c771841156f2eea384649cc"
assert sha(AUTHOR / "FROZEN_MANIFEST.json") == "6241879639beda1506d1ec3772aa1403f6f2963320695d146a4ee10bed1cfcdd"
own_manifest = BASE / "REVIEW_MANIFEST.json"
if own_manifest.exists():
    verify_manifest(BASE, own_manifest.name)
args.output_dir.mkdir(parents=True)

cmd = [sys.executable, str(AUTHOR / "check_exact.py"), "--output-dir",
       str(args.output_dir / "portable-author-replay")]
subprocess.run(cmd, check=True, capture_output=True, text=True)
portable_report = args.output_dir / "portable-author-replay/EXACT_CHECKS.json"
assert portable_report.read_bytes() == (AUTHOR / "portable-author-run/EXACT_CHECKS.json").read_bytes()
original_count = 0
if args.original_root:
    subprocess.run([*cmd[:-1], str(args.output_dir / "original-author-replay"),
                    "--original-root", str(args.original_root)],
                   check=True, capture_output=True, text=True)
    assert (args.output_dir / "original-author-replay/EXACT_CHECKS.json").read_bytes() == (
        AUTHOR / "author-run/EXACT_CHECKS.json").read_bytes()
    original_author = args.original_root / "full-law-gradient-action-tail-20261010"
    verify_manifest(original_author, "FROZEN_MANIFEST.json")
    assert sha(original_author / "FROZEN_MANIFEST.json") == sha(AUTHOR / "FROZEN_MANIFEST.json")
    ancestor = args.original_root / "nonconvex-atomic-limit-classification-20261010"
    original_count = len(verify_manifest(ancestor, "FROZEN_MANIFEST.json")["files"])

checks = []


def zero(label, expression):
    reduced = S.simplify(S.expand(expression))
    assert reduced == 0, (label, reduced)
    checks.append(label)


def yes(label, condition):
    assert condition, label
    checks.append(label)


# Independently derived heavy-tail estimates, including the exact high mass.
y, z, ell, r = S.symbols("y z ell r", positive=True)
rho = 1 / (y * S.log(y)**2)
cdf = 1 - 1 / S.log(y)
zero("probability CDF derivative", S.diff(cdf, y) - rho)
yes("probability endpoints", cdf.subs(y, S.E) == 0 and S.limit(cdf, y, S.oo) == 1)
zero("low event original mass", cdf.subs(y, S.E**2) - cdf.subs(y, S.E) - S.Rational(1, 2))
zero("logarithmic energy transform", (y * rho).subs(y, S.exp(z)) * S.exp(z) - S.exp(z) / z**2)
zero("exact high event mass", 1 / ell - 1 / (ell + S.log(2)) - S.log(2) / (ell * (ell + S.log(2))))
zero("high event lower bound nonnegative remainder",
     S.log(2) / (ell * (ell + S.log(2))) - S.log(2) / (ell + S.log(2))**2
     - S.log(2)**2 / (ell * (ell + S.log(2))**2))
ss = 1 / (2 * S.E**2 * (1 + r))
zero("event separation nonnegative remainder", (1 / ss - S.E**2) - 1 / (2 * ss) - S.E**2 * r)
zero("low tilt bound premise", ss * S.E**2 - 1 / (2 * (1 + r)))
constant = S.exp(-S.Rational(5, 2)) * S.log(2) / 8
zero("explicit variance lower constant",
     (S.exp(-S.Rational(1, 2)) / 2) * (S.exp(-2) * S.log(2)) / 4 - constant)

t, Y = S.symbols("t Y", positive=True)
q = S.exp(-2 * t)
clock = (1 - q) / 2
zero("quadratic accumulated killing derivative", S.diff(clock * Y, t) - q * Y)
zero("variance clock cancellation", q / S.diff(clock, t) - 1)
M = S.Function("M")
V = S.symbols("V", positive=True)
energy_derivative = S.diff(q * M(clock), t).doit()
assert len(energy_derivative.atoms(S.Subs)) == 1
# The sole substituted derivative is M'(s) = -Var_s(Y).
energy_derivative = energy_derivative.replace(
    lambda expr: isinstance(expr, S.Subs), lambda expr: -V)
zero("full quadratic dissipation factors", energy_derivative + 2 * q * M(clock) + q**2 * V)
s = S.symbols("s", positive=True)
antiderivative = -S.log(S.log(2 / s))
zero("divergent length primitive", S.diff(antiderivative, s) - 1 / (s * S.log(2 / s)))
yes("length primitive limit", S.limit(antiderivative, s, 0, dir="+") == -S.oo)

# A three-point variance expansion independently checks the factor 1/2.
a, b, x0, x1, x2 = S.symbols("a b x0 x1 x2", real=True)
weights, values = (a, b, 1 - a - b), (x0, x1, x2)
mean = sum(w * x for w, x in zip(weights, values))
variance = sum(w * (x - mean)**2 for w, x in zip(weights, values))
pair = sum(weights[i] * weights[j] * (values[i] - values[j])**2
           for i in range(3) for j in range(3)) / 2
zero("independent pair variance factor", pair - variance)

# Exact adversarial control: deleting reaction loses every coercive bound.
x = S.symbols("x", real=True)
F = (x*x - 1)**2 / 4
w = S.Rational(1, 8)
mu = lambda f: (1-w)*f.subs(x, 1) + w*f.subs(x, 0)
G = mu(S.diff(F, x)**2)
h = mu(F)
D = G + mu((F-h)**2)
yes("gradient-only bound fails on stationary two-level law", G == 0 and h > 0 and D > 0)
zero("stationary two-level exact dissipation", D - w*(1-w)/16)
yes("convex Jensen direction is strict", S.Rational(1, 2)*4**S.Rational(3, 2) > 2**S.Rational(3, 2))

# Direct finite-atomic cometric and metric-speed comparison.
weights2, points2 = (S.Rational(2, 5), S.Rational(3, 5)), (-1, 2)
mu2 = lambda f: sum(wi * f.subs(x, xi) for wi, xi in zip(weights2, points2))
B = lambda f, g: mu2(S.diff(f, x)*S.diff(g, x)) + mu2(f*g) - mu2(f)*mu2(g)
p = x**3 + 2*x
generator = -mu2(S.diff(F, x)*S.diff(p, x)) - mu2(F*p) + mu2(F)*mu2(p)
zero("polynomial generator is minus cometric", generator + B(p, F))
yes("cometric Cauchy-Schwarz exact Gram determinant", B(p,p)*B(F,F)-B(p,F)**2 > 0)
E = mu2(F)
weight_derivatives = [-wi*(F.subs(x, xi)-E) for wi, xi in zip(weights2, points2)]
metric_speed = sum(du**2/wi for du, wi in zip(weight_derivatives, weights2)) + mu2(S.diff(F, x)**2)
zero("finite atomic metric speed equals action", metric_speed - B(F,F))
zero("constant polynomial gauge annihilation", B(S.Integer(7), F))

# Check both exponent branches and exact monomial tail lengths.
H, C, tau = S.symbols("H C tau", positive=True)
hexp = H*S.exp(-C*tau)
zero("exponential comparison ODE", S.diff(hexp, tau) + C*hexp)
for theta in (S.Rational(3,4), S.Rational(5,6), S.Rational(7,8)):
    beta = 2*theta-1
    hp = (H**(-beta)+C*beta*tau)**(-1/beta)
    zero("algebraic comparison theta="+str(theta), S.diff(hp,tau)+C*hp**(2*theta))
for m in (2,3,4):
    xp = S.symbols("xp", positive=True)
    fm = xp**(2*m)/(2*m)
    theta = S.Rational(2*m-1,2*m)
    kappa = (2*m)**theta
    zero("monomial sharp tail length m="+str(m), fm**(1-theta)/(kappa*(1-theta))-xp)

report = {"status": "all_independent_controls_passed", "check_count": len(checks),
          "python": platform.python_version(), "sympy": S.__version__, "checks": checks,
          "scope": "Supplementary exact identities and countercontrols; written mathematical review remains essential. No formal-kernel or closure authority."}
(args.output_dir / "INDEPENDENT_CONTROLS.json").write_text(json.dumps(report, indent=2)+"\n")
verify_manifest(AUTHOR, "FROZEN_MANIFEST.json")
print(json.dumps({"status": report["status"], "independent_control_count": len(checks),
                  "author_payload_count": len(author_manifest["files"]),
                  "portable_author_check_count": json.loads(portable_report.read_text())["check_count"],
                  "original_ancestor_payload_count": original_count}))
