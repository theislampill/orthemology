"""Execute locked specifications plus explicitly marked reconstruction amendment.

Group-level caches are private; only compact aggregate JSON is emitted here.
"""
import itertools,json,math
import numpy as np
import pandas as pd
from analysis_core import score_flags,pair_correlation,logistic_cluster,stratified_contrast
from run_reanalysis import HERE,load,build_rounds,clean_json


def extend_rounds(d,r):
    rows=[]
    for (game,round_),g in d.groupby(['gameId','round']):
        rows.append(dict(gameId=game,round=round_,**score_flags(g.stored_correct,int(g['size'].iloc[0]))))
    r=r.merge(pd.DataFrame(rows),on=['gameId','round'],validate='one_to_one')
    if not ((r.R==r.R_reconstructed)|(r.R.isna()&r.R_reconstructed.isna())).all():raise ValueError('reconstruction identity fails')
    r['R_half']=r.R.fillna(.5);r['R_one']=r.R.fillna(1.)
    r['A_E0_R_known']=r.A_E0.where(r.R.notna());r['A_E_R_known']=r.A_E.where(r.R.notna())
    r['score_support_minus_roster']=r.A_E0-r.B_E0
    r['matched_active_minus_recorded']=r.A_E0_R_known-r.R
    r['active_minus_roster_halftie']=r.A_E0-r.R_half
    r['roster_minus_assigned']=r.B_E0-r.Q_E0
    r['final_minus_flag_active']=r.A0-r.A_E0
    r['original_final_active_minus_assigned']=r.A0-r.Q0
    r['R_available']=r.R.notna().astype(float)
    return r


def game_metrics(d,r):
    columns=['R','R_half','R_one','R_available','A_E0','A_E0_R_known','A_E_R_known','B_E0','Q_E0','A_E',
     'A0','Q0','B0','matched_active_minus_recorded','active_minus_roster_halftie','score_support_minus_roster','roster_minus_assigned','final_minus_flag_active','original_final_active_minus_assigned']
    g=r.groupby('gameId')[columns].mean().join(r.groupby('gameId')[['size','incentive']].first())
    d['local_follow_flags']=d.local_follow.where(d.stored_correct.notna())
    person=d.groupby(['gameId','playerId'])[['stored_correct','correct','local_follow_flags','local_follow']].mean()
    person=person.groupby('gameId').mean().rename(columns={'stored_correct':'individual_accuracy_flags','correct':'individual_accuracy_final',
        'local_follow_flags':'local_follow_flags','local_follow':'local_follow_final'})
    g=g.join(person)
    pairs=[];pair_audit={'total_pairs':0,'main_eligible_pairs':0,'final_eligible_pairs':0,'main_short_pairs':0,'main_constant_pairs':0}
    for game,dg in d.groupby('gameId'):
        mats={c:dg.pivot(index='playerId',columns='round',values=c).to_numpy(float) for c in ['stored_correct','correct','local','global']}
        ps=[]
        for i,j in itertools.combinations(range(len(mats['correct'])),2):
            pair_audit['total_pairs']+=1;a,b=mats['stored_correct'][[i,j]];ok=np.isfinite(a)&np.isfinite(b)
            main=pair_correlation(a,b);final=pair_correlation(*mats['correct'][[i,j]])
            if np.isfinite(main):pair_audit['main_eligible_pairs']+=1
            elif ok.sum()<12:pair_audit['main_short_pairs']+=1
            else:pair_audit['main_constant_pairs']+=1
            if np.isfinite(final):pair_audit['final_eligible_pairs']+=1
            local=pair_correlation(mats['local'][i,ok],mats['local'][j,ok]) if np.isfinite(main) else np.nan
            global_=pair_correlation(mats['global'][i,ok],mats['global'][j,ok]) if np.isfinite(main) else np.nan
            ps.append([main,final,local,global_])
        if ps:
            arr=np.array(ps)
            means=[np.mean(v[np.isfinite(v)]) if np.isfinite(v).any() else np.nan for v in arr.T]
        else:means=[np.nan]*4
        pairs.append(dict(gameId=game,**dict(zip(['pair_error_corr_flags','pair_error_corr_final','pair_local_corr_selected','pair_global_corr_selected'],means))))
    g=g.join(pd.DataFrame(pairs).set_index('gameId'))
    return g,pair_audit


def inference(g,metric):
    d=g[g['size']>1];res=stratified_contrast(d,metric)
    cells={}
    for size in [3,7,15]:
        a=d.loc[(d['size']==size)&d.incentive.eq(0),metric].dropna().to_numpy()
        b=d.loc[(d['size']==size)&d.incentive.eq(1),metric].dropna().to_numpy()
        rng=np.random.default_rng(16052026+size)
        delta=b.mean()-a.mean() if len(a) and len(b) else np.nan
        vals=b[rng.integers(0,len(b),size=(20000,len(b)))].mean(1)-a[rng.integers(0,len(a),size=(20000,len(a)))].mean(1) if len(a) and len(b) else np.array([np.nan])
        loo=[]
        if len(a)>1:loo.extend(b.mean()-np.delete(a,j).mean() for j in range(len(a)))
        if len(b)>1:loo.extend(np.delete(b,j).mean()-a.mean() for j in range(len(b)))
        cells[str(size)]={'individual_games':len(a),'collective_games':len(b),'individual':a.mean() if len(a) else np.nan,
           'collective':b.mean() if len(b) else np.nan,'contrast':delta,'bootstrap_ci95':np.quantile(vals,[.025,.975]).tolist(),
           'leave_one_game_out_range':[min(loo),max(loo)] if loo else None}
    loo=[]
    for index in d.index:
        x=d.drop(index);vals=[]
        for size in [3,7,15]:
            a=x.loc[(x['size']==size)&x.incentive.eq(0),metric].dropna();b=x.loc[(x['size']==size)&x.incentive.eq(1),metric].dropna()
            if len(a)==0 or len(b)==0:break
            vals.append(b.mean()-a.mean())
        if len(vals)==3:loo.append(np.mean(vals))
    res['size_specific']=cells;res['leave_one_game_out_range']=[min(loo),max(loo)] if loo else None
    return res


def model_diagnostics(r):
    result={};mean=r['size'].mean();sd=r['size'].std(ddof=1)
    for pop in ['all75','multi47']:
        for metric in ['R','A_E0','B_E0','Q_E0','A0']:
            x=r if pop=='all75' else r[r['size']>1]
            x=x[x[metric].notna()];z=(x['size'].to_numpy()-mean)/sd;t=x.incentive.to_numpy()
            X=np.column_stack([np.ones(len(x)),z,t,z*t])
            fit=logistic_cluster(X,x[metric].to_numpy(),x.gameId.to_numpy())
            fit.update(response_type='fractional_half_credit_sensitivity' if metric in ['A_E0','A0'] else 'binary_score',ordinary_p_scope='working-model diagnostic; not Bernoulli-outcome likelihood inference' if metric in ['A_E0','A0'] else 'ordinary unclustered binomial diagnostic',size_mean=mean,size_sample_sd=sd,population=pop,outcome=metric,parameters=['intercept','standardized_assigned_size','collective','size_by_collective'])
            result[pop+'_'+metric]=fit
    return result


def main():
    d,author=load();r=extend_rounds(d,build_rounds(d));g,pairaudit=game_metrics(d,r)
    out={'specification':'Explicit implemented estimands; see the accompanying research report.',
      'independent_reanalysis':True,'author_code_executed':False,
      'score_identity_all_rounds_verified':True,'score_identity_rounds':len(r),
      'recorded_R_available':int(r.R.notna().sum()),'recorded_R_missing_roster_count_ties':int(r.R.isna().sum()),
      'R_known_flag_empty':int((r.R.notna()&r.flag_empty).sum()),
      'flag_active_ties':int(r.flag_tie.sum()),'flag_empty_rounds':int(r.flag_empty.sum()),
      'raw_to_author_projection':'verified exact','pair_selection':pairaudit,
      'aggregate_scores':r[['R','R_half','R_one','A_E0','B_E0','Q_E0','A0','Q0','score_support_minus_roster','roster_minus_assigned']].mean().to_dict(),
      'contrasts':{metric:inference(g,metric) for metric in g.columns if metric not in ['size','incentive']},
      'models':model_diagnostics(r),
      'qualifications':['Input provenance and publication-version limits are stated in the accompanying research report.',
        'Game bootstrap is conditional on observed task items and scoring support; inspect computed design-cell sizes and the report for sparse-cell qualifications.',
        'The score-identity audit tests the implemented reconstruction; do not infer behavioral decision or eligibility semantics from this check alone.',
        'Nonempty tie0.5 and empty0 are hypothetical expected-score/completion conventions.',
        'Contrasts and pair correlations do not establish causal mediation or individual equivalence.']}
    g.to_csv(HERE/'private-source'/'derived_game_metrics_v2.csv')
    r.to_csv(HERE/'private-source'/'derived_group_rounds_v2.csv',index=False)
    path=HERE/'verification'/'reanalysis_results_v3.json';path.write_text(json.dumps(clean_json(out),indent=2))
    print('Exact reconstruction passed:',len(r),'rounds;R known:',out['recorded_R_available'])
    print('Aggregate scores',json.dumps(out['aggregate_scores']))
    for k in ['R','A_E0','A_E0_R_known','B_E0','Q_E0','matched_active_minus_recorded','active_minus_roster_halftie','score_support_minus_roster','roster_minus_assigned','local_follow_flags','individual_accuracy_flags','pair_error_corr_flags']:
        v=out['contrasts'][k];print(k,'standardized',v['estimate'],'CI',v['ci95'],'LOO',v['leave_one_game_out_range']);print('  cells',json.dumps(v['size_specific']))
    print('Literal-formula diagnostic',json.dumps(out['models']['all75_R']))
    print('Wrote',path)
if __name__=='__main__':main()
