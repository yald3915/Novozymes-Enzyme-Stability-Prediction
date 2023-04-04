import pandas as pd
import numpy as np

# Ref: https://www.kaggle.com/code/hengck23/lb0-335-deepdgg-server-benchmark

#helper function
def read_list_from_file(list_file):
    with open(list_file) as f:
        lines  = f.readlines()
    return lines



#the results from DeepDDG server[1] 
ddg = read_list_from_file('../input/submit-novozymes-00/wildtype_structure_prediction_af2.deepddg.ddg.txt')

header = ddg[0]
data = [s.split() for s in ddg[1:]]

df = pd.DataFrame(data, columns = ['chain', 'WT', 'ResID', 'Mut', 'ddG'])
df.ddG = df.ddG.astype(np.float32)
df.ResID = df.ResID.astype(int)  
df.loc[:,'location'] = df.ResID -1  #change to 0-indexing

#test csv 
#mutation is from : https://www.kaggle.com/competitions/novozymes-enzyme-stability-prediction/discussion/354783
test_df = pd.read_csv('../input/submit-novozymes-00/test.more.csv')
test_df.location = test_df.location.fillna(-1)
test_df.location = test_df.location.astype(int)

#generate submission csv 
df.loc[:,'mut_string'] = df.WT+df.location.astype(str)+df.Mut
test_df.loc[:,'mut_string'] =  test_df.wild_type+test_df.location.astype(str)+test_df.mutation

test_df = test_df.merge(df[['ddG','mut_string']], on='mut_string',how='left')
submit_df = pd.DataFrame({
    'seq_id': test_df.seq_id.values,
    'tm': test_df.ddG.values,
})
submit_df.tm = submit_df.tm.fillna(0)
submit_df.to_csv('deepddg-ddg.csv', index=False) #lb0.335
print(submit_df)
  
print('submit_df ok!')