import compas
from compas.geometry import closest_point_in_cloud

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

# group points per stage number
num_stages = 10 # NOTE: maybe there is a better way of finding the number of stages 
stages = []
for s in range(num_stages):
    stage = []
    for l in range(len(format)):
        if format[l][0] == s:
            stage.append(format[l][1])
    stages.append(stage)

# use compas colest_point _in_cloud to find the same point in two stages
results=[]
for s in range(num_stages-1):
    result = []
    for p in stages[s]:
        a = closest_point_in_cloud(p, stages[s+1])
        if a[0] > 5: # note it is in mm 
            result.append((0.0, (0.0, 0.0, 0.0), 0.0))
        result.append(a)
    results.append(result)


for e in results:
    print(len(e))
# print(results[0][0])