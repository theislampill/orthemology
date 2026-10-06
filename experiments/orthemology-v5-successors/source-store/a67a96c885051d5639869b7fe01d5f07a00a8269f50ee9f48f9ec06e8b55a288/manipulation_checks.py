"""Descriptive checks of recorded signal vectors and response correctness support."""
import itertools,json
import numpy as np
import pandas as pd
from analysis_core import pair_correlation
from run_reanalysis import HERE,load,clean_json

def main():
 d,_=load();gg=d.groupby(['gameId','round'])
 global_identity=bool(gg['global'].nunique().eq(1).all())
 global_count=gg['global'].first().groupby('gameId').sum()
 local_count=d.groupby(['gameId','playerId']).local.sum()
 rates={'global_game_count_distribution':{str(int(k)):int(v) for k,v in global_count.value_counts().sort_index().items()},
        'local_player_count_distribution':{str(int(k)):int(v) for k,v in local_count.value_counts().sort_index().items()},
        'rounds_per_vector':48,'global_correct_rate_game_equal':float((global_count/48).mean()),
        'local_correct_rate_participant_equal':float((local_count/48).mean()),
        'global_identical_within_every_game_round':global_identity,
        'games':len(global_count),'participants':len(local_count)}
 pairs=[];game_means=[]
 for game,g in d.groupby('gameId'):
  local=g.pivot(index='playerId',columns='round',values='local').to_numpy(float)
  global_=g.pivot(index='playerId',columns='round',values='global').to_numpy(float)
  gp=[]
  for i,j in itertools.combinations(range(len(local)),2):
   vals=[pair_correlation(local[i],local[j],48),pair_correlation(global_[i],global_[j],48)];gp.append(vals);pairs.append(vals)
  if gp:game_means.append(np.mean(gp,axis=0))
 pairs=np.array(pairs);game_means=np.array(game_means)
 corr={'roster_pairs':len(pairs),'games_with_pairs':len(game_means),
       'local_pair_weighted_mean':float(pairs[:,0].mean()),'local_game_equal_mean':float(game_means[:,0].mean()),
       'local_pair_range':[float(pairs[:,0].min()),float(pairs[:,0].max())],
       'global_pair_weighted_mean':float(pairs[:,1].mean()),'global_game_equal_mean':float(game_means[:,1].mean()),
       'global_pair_range':[float(pairs[:,1].min()),float(pairs[:,1].max())]}
 responses={}
 for label,support,col in [('recorded_score_support',d.stored_correct.notna(),'stored_correct'),('final_forecast_present',d.valid,'correct')]:
  x=d[support].copy();x['cue_agreement']=x['global']==x.local
  four=x.groupby(['global','local']).agg(responses=(col,'size'),correct=(col,'sum'),accuracy=(col,'mean')).reset_index().to_dict('records')
  agree=x.groupby('cue_agreement').agg(responses=(col,'size'),correct=(col,'sum'),accuracy=(col,'mean')).reset_index().to_dict('records')
  responses[label]={'responses':len(x),'four_signal_correctness_cells':four,'agreement_vs_conflict':agree}
 out={'specification':'Full recorded-cue checks implemented in source.','cue_vectors':rates,'full_vector_correlations':corr,'responses':responses,
      'scope':'Finite recorded vectors; no proof of stochastic independence, causal mediation, or a learning trajectory. Repeated-response weighting is descriptive.'}
 (HERE/'verification'/'manipulation_checks_v1.json').write_text(json.dumps(clean_json(out),indent=2));print(json.dumps(clean_json(out),indent=2))
if __name__=='__main__':main()
