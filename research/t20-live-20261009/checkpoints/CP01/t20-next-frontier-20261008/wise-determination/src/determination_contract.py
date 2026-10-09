from dataclasses import dataclass
import importlib.util,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
MODEL_PATH=ROOT/'recovery-t20/addendum/tranche20/research-frontier-continuation/sovereignty-choice-semantics/reactive-context-extension/src/reactive_context.py'
assert hashlib.sha256(MODEL_PATH.read_bytes()).hexdigest()=='f73cee9c0271dd2a80843a3994534e1119fca33386e59a483f3175d69880a6cc'
spec=importlib.util.spec_from_file_location('determination_recovered_model',MODEL_PATH)
Model=importlib.util.module_from_spec(spec);sys.modules[spec.name]=Model;spec.loader.exec_module(Model)
@dataclass(frozen=True)
class Context:
    q:int
    role_delta:int
    # role_delta is an explicitly supplied diagnostic coordination constraint,
    # not certified fittingness or an independently grounded reason.
@dataclass(frozen=True)
class Plan:
    a:int
    b:int
@dataclass(frozen=True)
class MeansCertificate:
    context:Context
    plan:Plan
    establishes_normative_eligibility:bool=False
    establishes_source_complete_will:bool=False
@dataclass(frozen=True)
class Determination:
    plan:Plan
    has_independent_justification:bool=False


def derive_means(ctx):
    """Inverse means query; permitted to consult the known production law.

    Its solution set is NOT a metaphysical admissibility domain. A unique
    solution under a supplied coordination condition is not that condition's
    normative or explanatory warrant.
    """
    if ctx.q not in range(3) or ctx.role_delta not in range(3):raise ValueError(ctx)
    c=Model.Catalogue(('e0','e1'))
    solutions=tuple(Plan(a,b) for a in range(3) for b in range(3)
                    if c.combine(a,b)==ctx.q and (a-b)%3==ctx.role_delta)
    if len(solutions)!=1:raise ValueError('Not uniquely instrumentally specified.')
    return MeansCertificate(ctx,solutions[0])


def validate_certificate(cert,claimed_plan=None):
    plan=cert.plan if claimed_plan is None else claimed_plan
    c=Model.Catalogue(('e0','e1'))
    return c.combine(plan.a,plan.b)==cert.context.q and (plan.a-plan.b)%3==cert.context.role_delta


def reason_projection(ctx):return ctx.q


def factors_through(contexts,projection,values):
    """Can these given determinations be represented using only the projection?

    Failure does not mean that NO selector using that projection exists.
    It means the particular given family cannot all be reproduced by one.
    """
    observed={}
    for ctx in contexts:
        key=projection(ctx)
        if key in observed and observed[key]!=values[ctx]:return False
        observed[key]=values[ctx]
    return True


def execute_declared(declaration,goal):
    """Execute a supplied actual declaration; do not relabel it a reason."""
    c=Model.Catalogue(('e0','e1'))
    a=Model.Original('A').issue(goal,declaration.plan.a)
    b=Model.Original('B').issue(goal,declaration.plan.b)
    return Model.execute(c,a,b)


def standing_settings(subject):return Model.Original(subject).repertoire
