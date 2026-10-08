"""Independently written scoring and clustered descriptive inference.

No source notebook is imported or evaluated. All fitted contrasts condition on the
realised task items. Retrospective rescoring is not a behavioral intervention.
"""
from __future__ import annotations
import ast
import math
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit
from scipy.stats import norm, t


def event_bits(text: str) -> tuple[bool, bool]:
    """Safely extract two literal booleans without evaluating other AST nodes."""
    try:
        node=ast.parse(text, mode='eval').body
        if not isinstance(node,ast.Dict): raise ValueError('event must be dict')
        fields={}
        for k,v in zip(node.keys,node.values):
            if isinstance(k,ast.Constant) and k.value in ('willHappen','globalAccurate'):
                if k.value in fields:raise ValueError('repeated target key')
                fields[k.value]=ast.literal_eval(v)
        if set(fields)!= {'willHappen','globalAccurate'}:raise ValueError('missing event bits')
        if any(type(v) is not bool for v in fields.values()):raise ValueError('event bits must be bool')
        return fields['willHappen'], fields['globalAccurate']
    except (TypeError,SyntaxError,ValueError) as e:
        raise ValueError('invalid event bits') from e


def require_unique(frame,keys):
    if frame.duplicated(keys).any():raise ValueError('duplicate key: '+','.join(keys))


def score_votes(votes, truth: bool, capacity: int) -> dict:
    votes=list(votes)
    if not isinstance(capacity,(int,np.integer)) or capacity<1 or len(votes)>capacity:
        raise ValueError('invalid capacity')
    if type(truth) not in (bool,np.bool_) or any(type(v) not in (bool,np.bool_) for v in votes):
        raise ValueError('votes and truth must be booleans')
    yes=sum(votes);n=len(votes);no=n-yes
    q= float(truth) if yes>capacity/2 else float(not truth) if no>capacity/2 else math.nan
    a= float(truth) if yes>no else float(not truth) if no>yes else .5 if n else math.nan
    return {'n':n,'Q':q,'Q0':0. if math.isnan(q) else q,
            'A':a,'A0':0. if math.isnan(a) else a,
            'q_unresolved':math.isnan(q),'empty':not n,'tie':bool(n and yes==no),
            'correct_active_fails_quorum':bool(a==1 and math.isnan(q))}


def pair_correlation(a,b,min_overlap=12):
    a=np.asarray(a,float);b=np.asarray(b,float);ok=np.isfinite(a)&np.isfinite(b)
    a=a[ok];b=b[ok]
    if len(a)<min_overlap or np.ptp(a)==0 or np.ptp(b)==0:return math.nan
    return float(np.corrcoef(a,b)[0,1])


def logistic_cluster(x,y,groups):
    """Binary/fractional logit with ordinary and CR0/CR1 game sandwich covariances."""
    x=np.asarray(x,float);y=np.asarray(y,float);groups=np.asarray(groups)
    if x.ndim!=2 or len(y)!=len(x) or len(groups)!=len(y):raise ValueError('shape')
    if np.linalg.matrix_rank(x)<x.shape[1]:raise ValueError('rank-deficient design')
    if not np.isfinite(x).all() or not np.isfinite(y).all() or (y<0).any() or (y>1).any():raise ValueError('invalid data')
    def objective(b):
        eta=x@b
        return np.logaddexp(0,eta).sum()-y@eta
    def gradient(b):return x.T@(expit(x@b)-y)
    fit=minimize(objective,np.zeros(x.shape[1]),jac=gradient,method='BFGS',options={'gtol':1e-9,'maxiter':2000})
    beta=fit.x;p=expit(x@beta);bread=np.linalg.inv(x.T@((p*(1-p))[:,None]*x))
    score=x*(y-p)[:,None];ugs=np.unique(groups)
    score_by=np.array([score[groups==g].sum(0) for g in ugs])
    cr0=bread@(score_by.T@score_by)@bread
    n,k=x.shape;ng=len(ugs)
    factor=(ng/(ng-1))*((n-1)/(n-k)) if ng>1 and n>k else math.nan
    cr1=cr0*factor;se=np.sqrt(np.maximum(np.diag(cr1),0));ordinary=np.sqrt(np.diag(bread))
    converged=bool(np.max(np.abs(gradient(beta)))<1e-5)
    return {'beta':beta.tolist(),'ordinary_se':ordinary.tolist(),
       'ordinary_p':(2*norm.sf(np.abs(beta/ordinary))).tolist(),
       'cluster_se_cr1':se.tolist(),'cluster_p_t_Gminus1':(2*t.sf(np.abs(beta/se),ng-1)).tolist(),
       'cluster_ci95':np.column_stack([beta-t.ppf(.975,ng-1)*se,beta+t.ppf(.975,ng-1)*se]).tolist(),
       'cluster_cov_cr0':cr0.tolist(),'rows':n,'clusters':ng,'rank':k,
       'gradient_max':float(np.max(np.abs(gradient(beta)))),'converged':converged,'log_likelihood':float(-objective(beta))}


def stratified_contrast(frame,metric,replicates=20000,seed=16052026):
    """Equal-weight 3/7/15 cell contrasts, games equally weighted inside cells."""
    rng=np.random.default_rng(seed);sample=np.zeros(replicates);estimate=0.;cells={}
    for size in [3,7,15]:
        difference=0.
        for incentive,sign in [(0,-1),(1,1)]:
            values=frame.loc[(frame['size']==size)&(frame['incentive']==incentive),metric].dropna().to_numpy(float)
            if len(values)==0:return {'estimate':None,'ci95':None,'status':'empty design cell'}
            difference+=sign*float(values.mean())
            sample+=sign*values[rng.integers(0,len(values),size=(replicates,len(values)))].mean(axis=1)/3
            cells[f'{size}_{incentive}']={'games':len(values),'mean':float(values.mean())}
        estimate+=difference/3
    return {'estimate':estimate,'ci95':np.quantile(sample,[.025,.975]).tolist(),'cells':cells,
            'replicates':replicates,'seed':seed}


def score_flags(flags,assigned:int)->dict:
    """Three support boundaries; reconstructed R is an empirical archive identity."""
    flags=list(flags);m=len(flags)
    if not isinstance(assigned,(int,np.integer)) or m<1 or assigned<m:raise ValueError('invalid assigned size')
    observed=[]
    for flag in flags:
        if flag is None or (isinstance(flag,(float,np.floating)) and math.isnan(flag)):continue
        if flag not in (0,1,False,True):raise ValueError('invalid correctness flag')
        observed.append(bool(flag))
    e=len(observed);c=sum(observed)
    R=1. if c>m/2 else 0. if c<m/2 else math.nan
    A=1. if c>e/2 else 0. if c<e/2 else .5 if e else math.nan
    return {'E':e,'C':c,'R_reconstructed':R,'A_E':A,'A_E0':0. if math.isnan(A) else A,
      'B_E0':float(c>m/2),'Q_E0':float(c>assigned/2),'flag_tie':bool(e and c==e/2),'flag_empty':e==0}


def block_contrast(mixed,paired15,replicates=20000,seed=16062026):
    """Posthoc equal-batch sensitivity, retaining paired 3/7 block covariance."""
    mixed=np.asarray(mixed,float);paired15=np.asarray(paired15,float)
    if mixed.ndim!=2 or mixed.shape[1]!=2 or len(mixed)<2 or paired15.ndim!=1 or len(paired15)<2:
        raise ValueError('invalid matched block support')
    if not np.isfinite(mixed).all() or not np.isfinite(paired15).all():raise ValueError('missing block metric')
    means=np.r_[mixed.mean(0),paired15.mean()];rng=np.random.default_rng(seed)
    samples12=mixed[rng.integers(0,len(mixed),(replicates,len(mixed)))].mean(1)
    sample15=paired15[rng.integers(0,len(paired15),(replicates,len(paired15)))].mean(1)
    samples=np.column_stack([samples12,sample15]);sample=samples.mean(1)
    loo=[]
    for i in range(len(mixed)):loo.append(np.r_[np.delete(mixed,i,axis=0).mean(0),paired15.mean()].mean())
    for i in range(len(paired15)):loo.append(np.r_[mixed.mean(0),np.delete(paired15,i).mean()].mean())
    per_size_loo=[]
    for values in [mixed[:,0],mixed[:,1],paired15]:
        deletions=[np.delete(values,j).mean() for j in range(len(values))]
        per_size_loo.append([float(min(deletions)),float(max(deletions))])
    return {'estimate':float(means.mean()),'ci95':np.quantile(sample,[.025,.975]).tolist(),
       'size_specific_leave_one_block_out_ranges':per_size_loo,
       'size_specific_means':means.tolist(),'size_specific_ci95':np.quantile(samples,[.025,.975],axis=0).T.tolist(),
       'leave_one_block_out_range':[float(min(loo)),float(max(loo))],
       'replicates':replicates,'seed':seed,'mixed_blocks':len(mixed),'paired15_blocks':len(paired15)}
