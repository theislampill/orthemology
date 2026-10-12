from dataclasses import dataclass
class Refusal(ValueError):pass
@dataclass(frozen=True)
class Result:
    status:str
    reason:str=''
    ty:object=None
    term:object=None
    context:object=()
    type_depth:int=0

def check(*args,**kwargs):return Result('REFUSED','NOT_IMPLEMENTED')
def instantiate_term(*a,**k):raise Refusal('NOT_IMPLEMENTED')
def instantiate_type(*a,**k):raise Refusal('NOT_IMPLEMENTED')
def rename_type(*a,**k):raise Refusal('NOT_IMPLEMENTED')
def rename_term(*a,**k):raise Refusal('NOT_IMPLEMENTED')
def step_at(*a,**k):raise Refusal('NOT_IMPLEMENTED')
def prove_conversion(*a,**k):raise Refusal('NOT_IMPLEMENTED')
def compile_poly(*a,**k):raise Refusal('NOT_IMPLEMENTED')
def normalise(*a,**k):raise Refusal('NOT_IMPLEMENTED')
def export_finite(*a,**k):return {'status':'NOT_IMPLEMENTED','kernel_verified':False}
