"""Safe, independently authored reanalysis of hash-bound archived observations."""
from __future__ import annotations
import ast, hashlib, itertools, json, math
from pathlib import Path
import numpy as np
import pandas as pd
from analysis_core import event_bits, require_unique, score_votes, pair_correlation, logistic_cluster, stratified_contrast

HERE=Path(__file__).resolve().parent
INPUT_PATHS=None
EXPECTED={'export_3.csv':'dc49a4248a193b47df08f419f108f4070e0c0c07422fdbda31537c1d33aa6f5c',
'globalPref_LM_100.csv':'c43ba9293db5c1657f7829de1033e0985bb4dc46508ea253a669449207dbd317'}


def load():
    paths=INPUT_PATHS if INPUT_PATHS is not None else {n:HERE/'private-source'/n for n in EXPECTED}
    for n,p in paths.items():
        h=hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
        if h!=EXPECTED[n]:raise ValueError('input digest mismatch '+n)
    cs=['batchId','gameId','playerId','round.index','stage.name','round.data.ifp','player.data.roundLocalAccurate',
        'treatment.playerCount','treatment.reward','playerRound.data.value','playerRound.data.correct',
        'playerRound.data.groupCorrect','playerRound.data.groupVoteEmpty','playerRound.data.yesGroup']
    raw=pd.read_csv(paths['export_3.csv'],usecols=cs)
    key=['gameId','playerId','round.index']
    require_unique(raw,key+['stage.name'])
    if not raw.groupby(key)['stage.name'].nunique().eq(3).all():raise ValueError('incomplete stages')
    check=[c for c in cs if c not in key+['stage.name']]
    if (raw.groupby(key)[check].nunique(dropna=False)>1).any().any():raise ValueError('stage inconsistency')
    d=raw[raw['stage.name']=='response'].copy().rename(columns={'round.index':'round','treatment.playerCount':'size','treatment.reward':'reward',
       'playerRound.data.value':'forecast','playerRound.data.correct':'stored_correct','playerRound.data.groupCorrect':'R',
       'playerRound.data.groupVoteEmpty':'stored_empty','playerRound.data.yesGroup':'stored_yes'})
    memo={s:event_bits(s) for s in d['round.data.ifp'].unique()}
    d['truth']=d['round.data.ifp'].map(lambda s:memo[s][0]);d['global']=d['round.data.ifp'].map(lambda s:memo[s][1])
    loc={s:ast.literal_eval(s) for s in d['player.data.roundLocalAccurate'].unique()}
    if not all(len(v)==48 and all(type(b) is bool for b in v) for v in loc.values()):raise ValueError('local vector')
    d['local']=[loc[s][int(r)] for s,r in zip(d['player.data.roundLocalAccurate'],d['round'])]
    d['incentive']=d['reward'].map({'individual':0,'group':1})
    if d.incentive.isna().any():raise ValueError('unexpected treatment')
    if d['forecast'].dropna().eq(50).any() or not d['forecast'].dropna().between(0,100).all():raise ValueError('invalid forecasts')
    d['valid']=d['forecast'].notna();d['choice']=d['forecast']>50
    d['correct']=np.where(d.valid,(d.choice==d.truth).astype(float),np.nan)
    for c in ['stored_correct','R']:d[c]=d[c].map({True:1.,False:0.})
    d['local_follow']=np.where(d.valid & (d.local!=d['global']),d['correct']==d.local,np.nan)
    author=pd.read_csv(paths['globalPref_LM_100.csv']).rename(columns={'roundIndex':'round'})
    require_unique(d,['gameId','playerId','round']);require_unique(author,['gameId','playerId','round'])
    joined=d.merge(author,on=['gameId','playerId','round'],validate='one_to_one',suffixes=('','_author'))
    if len(joined)!=len(d) or len(author)!=len(d):raise ValueError('author key mismatch')
    checks={'forecast':'forecast_author','stored_correct':'accuracy','R':'groupAccuracy','size':'expN','global':'globalAccuracy','local':'localAccuracy','reward':'incentiveScheme'}
    for c,ac in checks.items():
        a=joined[c];b=joined[ac]
        if not ((a==b)|(a.isna()&b.isna())).all():raise ValueError('author column mismatch '+c)
    for c in ['truth','global','R','stored_empty','stored_yes','size','incentive']:
        if (d.groupby(['gameId','round'])[c].nunique(dropna=False)>1).any():raise ValueError('game-round conflict '+c)
    for c in ['size','incentive','batchId']:
        if (d.groupby('gameId')[c].nunique()>1).any():raise ValueError('game attribute conflict '+c)
    return d,author


def build_rounds(d):
    rows=[]
    for (game,round_),g in d.groupby(['gameId','round']):
        f=g.iloc[0];votes=g.loc[g.valid,'choice'].tolist();q=score_votes(votes,bool(f.truth),int(f['size']))
        b=score_votes(votes,bool(f.truth),len(g))
        rows.append(dict(gameId=game,round=int(round_),size=int(f['size']),incentive=int(f.incentive),
           batchId=f.batchId,R=float(f.R),B=b['Q'],B0=b['Q0'],stored_empty=bool(f.stored_empty),
           stored_yes=bool(f.stored_yes),truth=bool(f.truth),global_correct=bool(f['global']),
           roster=len(g),yes=sum(votes),no=len(votes)-sum(votes),**q))
    return pd.DataFrame(rows)


def audit(d,r,author):
    known=d.stored_correct.notna();valid=d.valid
    event=r.groupby('round')[['truth','global_correct']].nunique()
    signatures=r.sort_values('round').groupby('gameId').apply(lambda x:tuple(zip(x.truth,x.global_correct)),include_groups=False)
    common=r.R.notna()&r.Q.notna()
    out={'raw_stage_rows':len(d)*3,'response_rows':len(d),'participants':d.playerId.nunique(),'games':d.gameId.nunique(),
       'group_rounds':len(r),'input_hashes':EXPECTED,'author_response_projection':'exact on key and seven verified fields',
       'design_cells':r.groupby(['size','incentive']).gameId.nunique().to_dict(),
       'missing_forecast':int((~valid).sum()),'missing_stored_correct':int((~known).sum()),
       'valid_forecast_missing_stored_correct':int((valid&~known).sum()),
       'stored_individual_correctness_mismatches':int((known&valid&(d.correct!=d.stored_correct)).sum()),
       'stored_individual_correctness_without_forecast':int((known&~valid).sum()),
       'distinct_truth_global_signatures':signatures.nunique(),
       'question_indices_with_between_game_truth_variation':int(event.truth.gt(1).sum()),
       'question_indices_with_between_game_global_variation':int(event.global_correct.gt(1).sum()),
       'R_missing':int(r.R.isna().sum()),'Q_unresolved':int(r.Q.isna().sum()),'A_empty':int(r.A.isna().sum()),
       'active_ties':int(r.tie.sum()),'R_vs_Q_common_mismatches':int((r.loc[common,'R']!=r.loc[common,'Q']).sum()),
       'R_present_Q_unresolved':int((r.R.notna()&r.Q.isna()).sum()),
       'R_absent_Q_resolved':int((r.R.isna()&r.Q.notna()).sum()),
       'R_equals_stored_yes_truth_mismatches':int((r.R.notna()&(r.R!=(r.stored_yes==r.truth).astype(float))).sum()),
       'stored_empty_vs_Q_unresolved_mismatches':int((r.stored_empty!=r.q_unresolved).sum()),
       'stored_yes_vs_assigned_yes_quorum_mismatches':int((r.stored_yes!=(r.yes>r['size']/2)).sum()),
       'stored_yes_vs_active_yes_majority_mismatches':int((r.stored_yes!=(r.yes>r.no)).sum())}
    out['design_cells']={f'{s}_{i}':int(v) for (s,i),v in out['design_cells'].items()}
    out['R_support_by_quorum']=r.assign(R_known=r.R.notna(),R_positive=r.R==1).groupby(['q_unresolved','stored_empty','R_known','R_positive']).size().reset_index(name='rounds').to_dict('records')
    return out


def clean_json(x):
    if isinstance(x,dict):return {str(k):clean_json(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [clean_json(v) for v in x]
    if isinstance(x,(np.integer,)):return int(x)
    if isinstance(x,(np.bool_,)):return bool(x)
    if isinstance(x,(float,np.floating)):return float(x) if np.isfinite(x) else None
    return x

if __name__=='__main__':
    d,author=load();r=build_rounds(d);out=audit(d,r,author)
    path=HERE/'verification'/'reconstruction_audit_v2.json';path.write_text(json.dumps(clean_json(out),indent=2))
    print(json.dumps(clean_json(out),indent=2))
