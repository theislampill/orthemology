"""Execute POSTHOC_BATCH_SENSITIVITY_SPEC_v1; original primary results unchanged."""
import json,numpy as np,pandas as pd
from analysis_core import block_contrast
from run_reanalysis import HERE,load,clean_json

def main():
 d,_=load();g=pd.read_csv(HERE/'private-source'/'derived_game_metrics_v2.csv').set_index('gameId')
 g=g.join(d.groupby('gameId').batchId.first())
 # Design support is based only on treatment metadata, never outcome values.
 counts=g[g['size']>1].groupby(['batchId','size','incentive']).size().unstack('incentive',fill_value=0)
 paired=counts[(counts[0]>0)&(counts[1]>0)]
 mixed_ids=sorted(set(paired.xs(3,level='size').index)&set(paired.xs(7,level='size').index))
 fifteen_ids=sorted(paired.xs(15,level='size').index)
 if len(mixed_ids)!=6 or len(fifteen_ids)!=2:raise ValueError('unexpected matched blocks')
 outcomes=['R','A_E0','A_E0_R_known','B_E0','Q_E0','matched_active_minus_recorded','local_follow_flags','individual_accuracy_flags','pair_error_corr_flags']
 results={}
 for outcome in outcomes:
  means=g.groupby(['batchId','size','incentive'])[outcome].mean().unstack('incentive')
  n=g.groupby(['batchId','size','incentive'])[outcome].count().unstack('incentive')
  dif=means[1]-means[0]
  mixed=np.array([[dif.loc[(b,s)] for s in [3,7]] for b in mixed_ids])
  large=np.array([dif.loc[(b,15)] for b in fifteen_ids])
  res=block_contrast(mixed,large)
  weighted=[];available_game_equal=[];available_arm_counts={}
  for size,ids in [(3,mixed_ids),(7,mixed_ids),(15,fifteen_ids)]:
   weights=np.array([paired.loc[(b,size),0] for b in ids])
   weighted.append(float(np.average([dif.loc[(b,size)] for b in ids],weights=weights)))
   subset=g[(g['size']==size)&g.batchId.isin(ids)]
   arms=[subset.loc[subset.incentive.eq(i),outcome].dropna() for i in [0,1]]
   available_game_equal.append(float(arms[1].mean()-arms[0].mean()))
   available_arm_counts[str(size)]={'individual':len(arms[0]),'collective':len(arms[1])}
  res['design_count_weighted_batch_difference_size_points']=weighted;res['design_count_weighted_batch_difference_standardized_point']=float(np.mean(weighted))
  res['available_game_equal_size_points']=available_game_equal;res['available_game_equal_standardized_point']=float(np.mean(available_game_equal));res['available_arm_game_counts']=available_arm_counts
  res['paired15_difference_range']=[float(large.min()),float(large.max())]
  res['size3_difference_range']=[float(mixed[:,0].min()),float(mixed[:,0].max())]
  res['size7_difference_range']=[float(mixed[:,1].min()),float(mixed[:,1].max())]
  res['missing_contributing_games']=int(sum(paired.loc[(b,s),i]-n.loc[(b,s),i] for s,ids in [(3,mixed_ids),(7,mixed_ids),(15,fifteen_ids)] for b in ids for i in [0,1]))
  results[outcome]=res
 out={'specification':'Posthoc matched-batch sensitivity implemented in source.','review_erratum':'Secondary weighting labels and per-size leave-one-out corrected after independent review.','posthoc':True,'matched_games':46,'unpaired_size15_collective_games_excluded':1,
      'qualification':'Equal-batch sensitivity is posthoc, not certified randomization inference; inspect computed block counts and the accompanying report.',
      'contrasts':results}
 (HERE/'verification'/'batch_sensitivity_results_v2.json').write_text(json.dumps(clean_json(out),indent=2));print(json.dumps(clean_json(out),indent=2))
if __name__=='__main__':main()
