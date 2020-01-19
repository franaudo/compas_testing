import compas
import numpy as np
from compas.geometry import closest_point_in_cloud
import pandas as pd


'''
Step 1 : create sublist for stages
'''

# set the location of the input file
input_file = '/Users/fentons/Desktop/hilo/post-process/Export2.txt'

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

print('before stages[0][0]:', stages[0][0])
print('before stages[-1][0]:', stages[-1][0])

'''
Step 2 : find matching points by comparing points in stage 0 to all other stages, replace with blank points when no matching point found, remove point from origin when matching

'''

#use compas closest_point _in_cloud to find the same point in two stages

# print('len STAGES[0]:', len(stages[0]))
# print('len STAGES[-1]:', len(stages[-1]))

results=[]

for elem in stages:
    print('before',len(elem))

for i in range(len(stages[0])):
    point_history = [0.0, stages[0][i], i]
    for s in range(1,num_stages):
        a = closest_point_in_cloud(stages[0][i], stages[s])
        if a[0] > 30: # note it is in mm 
            point_history.append((0.0, (0.0, 0.0, 0.0), 0.0))
        else:
            point_history.append(a)
            stages[s].pop(a[2])
    results.append(point_history)

'''
apply same strategy to search through remaining points in next stages
'''

# #check
# for elem in stages:
#     print('after',len(elem))

# print('after stages[0][0]:', stages[0][0])
# print('after stages[-1][0]:', stages[-1][0])
# print('len STAGES[0]:', len(stages[0]))
# print('len STAGES[-1]:', len(stages[-1]))

# print('len results:', len(results))
# print('len results[0]:', len(results[0]))
# #print('results[0]:', results[0])

# df = pd.DataFrame(results[0], columns =['dis,coord,index'])
# print(df)