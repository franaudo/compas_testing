import os
import numpy as np
import pandas as pd

import compas
from compas.geometry import closest_point_in_cloud


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))

'''
Step 1 : create sublist for stages
'''

# set the location of the input file
input_file = DATA + '\\GOM_results\\export_space.txt'

# parse the input file into a list and covert to float
raw = []
with open(input_file,'r') as f:
    for line in f:
        elem = line.split()
        sl = elem[1:3] + elem[4:7]
        fl = list(float(sl[i]) for i in range(len(sl)))
        raw.append(fl)
format = [[float(elem[0]), (elem[2],elem[3],elem[4])] for elem in raw]

#num_stages = int(format[-1][0]) 

list_stages = [format[i][0] for i in range(len(format))]
unique_stages =  np.unique(list_stages)
num_stages = len(unique_stages)


#print('unique_stages:', unique_stages)
print('num_stages:',num_stages)
stages = []
for s in range(num_stages+2):
    stage = []
    for l in range(len(format)):
        if format[l][0] == s:
            stage.append(format[l][1])
    if len(stage)==0:
        continue
    stages.append(stage)

print('len_stages_list:', len(stages))

#use compas closest_point _in_cloud to find the same point in two stages

'''
Step 2 : find matching points in pairs of neighbouring stages, replace with blank points when no matching point found
Problem : the pairs dont match between each other, too many blank points inserted 
'''

results=[]
for s in range(num_stages-1):
    result = []
    for p in stages[s]:
        a = closest_point_in_cloud(p, stages[s+1])
        if a[0] > 40: # note it is in mm 
            result.append((0.0, (0.0, 0.0, 0.0), 0.0))
        else:
            result.append(a)
    results.append(result)


#check
# for e in results:
#     print(len(e))
# print('len results:', len(results))

# Problem > there are many empty tuples in the results:
#print('result[-1]:', results[-1])
#print('len result[-1]:', len(results[-1]))

#df = pd.DataFrame(results[0], columns =['dis','coord','index'])
#print(df)