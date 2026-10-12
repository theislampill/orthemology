"""Independent exact finite controls; not a universal or formal-kernel proof."""
from pathlib import Path
import hashlib
import json
import platform
import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
checks = []

def record(label, condition):
    assert condition, label
    checks.append(label)

# Check the actual author-bound inherited sources against both snapshot and input.
bindings = json.loads((ROOT / 'fisher-endpoint-geometry-20261010/INPUT_BINDINGS.json').read_text())
source_records = []
for row in bindings['inputs']:
    raw = (ROOT / row['path']).read_bytes()
    snapshot = (ROOT / 'fisher-endpoint-geometry-20261010' / row['snapshot']).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    record('Source and snapshot equality: ' + row['path'], raw == snapshot)
    record('Source SHA-256 and size: ' + row['path'], digest == row['sha256'] and len(raw) == row['bytes'])
    source_records.append({'path': row['path'], 'sha256': digest, 'bytes': len(raw)})

# The inherited true Hessian note has a declared immutable repository blob.
hessian_source = ROOT / 'noetic-gradient-transport-20261009/INHERITED_HESSIAN_SOURCE.md'
raw = hessian_source.read_bytes()
git_blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
record('Inherited Hessian source repository blob', git_blob == '0b7f307cabd85b4d73215f024d70112a5dcd07c4')

# The opposite natural parameter sign is consequential.
v, w, qv, qw, Av, Aw = sp.symbols('v w qv qw Av Aw', real=True)
Phi_v, Phi_w, Phi_prime_w = -v*qv-Av, -w*qw-Aw, -w
Bregman_dual = sp.expand(Phi_v-Phi_w-Phi_prime_w*(qv-qw))
KL_vw = (w-v)*qv-Av+Aw
Bregman_primal_wv = Aw-Av-(-qv)*(w-v)
record('Mean dual Bregman equals forward KL', sp.simplify(Bregman_dual-KL_vw) == 0)
record('Natural Bregman reverses parameter arguments', sp.simplify(Bregman_primal_wv-KL_vw) == 0)
record('KL orientation changes on swapping law arguments', sp.expand(KL_vw-((v-w)*qw-Aw+Av)) != 0)

V = sp.Function('V')(v)
d_dq = lambda expr: -sp.diff(expr, v)/V
H = 1/V
record('Mean Hessian first derivative', sp.simplify(d_dq(H)-sp.diff(V,v)/V**3) == 0)
record('Mean Hessian second derivative', sp.simplify(d_dq(d_dq(H))-(3*sp.diff(V,v)**2-V*sp.diff(V,v,2))/V**5) == 0)
record('Mean coordinate metric transform', sp.simplify(H*(-V)**2-V) == 0)

# Finite jet controls with generic moments, independent of the author's script.
t = sp.symbols('t')
m1,m2,m3,m4 = sp.symbols('m1 m2 m3 m4')
Z = 1-m1*t+m2*t**2/2-m3*t**3/6+m4*t**4/24
A = sp.series(sp.log(Z),t,0,5).removeO().expand()
kappa2 = m2-m1**2
kappa3 = m3-3*m1*m2+2*m1**3
kappa4 = m4-4*m1*m3-3*m2**2+12*m1**2*m2-6*m1**4
record('Centered partition endpoint', A.subs(t,0) == 0)
record('Mean sign at endpoint', -sp.diff(A,t).subs(t,0) == m1)
record('Variance second cumulant', sp.simplify(sp.diff(A,t,2).subs(t,0)-kappa2) == 0)
record('Variance derivative third cumulant sign', sp.simplify(sp.diff(A,t,3).subs(t,0)+kappa3) == 0)
record('Variance second derivative fourth cumulant', sp.simplify(sp.diff(A,t,4).subs(t,0)-kappa4) == 0)
record('Lognormal endpoint variance', sp.simplify(kappa2.subs({m1:sp.exp(sp.Rational(1,2)),m2:sp.exp(2)})-(sp.exp(2)-sp.E)) == 0)
record('Lognormal variance strictly positive', (sp.exp(2)-sp.E).is_positive is True)

# Additive history normalization changes potentials but no Bregman or metric.
c = sp.symbols('c')
record('Additive gauge cancels from Bregman', sp.expand((Aw+c)-(Av+c)+qv*(w-v)-KL_vw) == 0)

result = {
    'status': 'PASS',
    'scope': 'Independent finite symbolic/source-integrity controls; ordinary universal arguments in INDEPENDENT_DERIVATION.md',
    'python': platform.python_version(),
    'sympy': sp.__version__,
    'assertions': len(checks),
    'checks': checks,
    'source_records': source_records,
    'inherited_hessian_source_git_blob_sha1': git_blob,
    'inherited_hessian_repository_pin': '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c',
}
(OUT / 'INDEPENDENT_CONTROLS.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'status':result['status'],'assertions':len(checks),'python':result['python'],'sympy':result['sympy']}))
