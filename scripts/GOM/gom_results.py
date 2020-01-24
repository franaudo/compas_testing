import os
import csv
import json
import itertools
import numpy as np
import pandas as pd

import compas
from compas.geometry import closest_point_in_cloud


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))

# def parse_results(input_file):
#     results=[]
#     with open(input_file,'r') as f:
#         for line in f:
#             " ".join(line.split())
#             print(line)
#             r = csv.reader(line, delimiter='\t')
#             results.append(r)
#     print(results[0])

def myround(x, base):
    '''
    Custom multiple rounding function.
    '''
    return base * round(x/base)

def results_per_stage(input_file, tollerance=60):
    ''' 
    parse the input file into a list and covert to float 
    '''
    
    results = []
    with open(input_file,'r') as f:
        for line in f:
            elem = line.split()
            sl = elem[1:3] + elem[4:7]
            fl = list(float(sl[i]) for i in range(len(sl)))
            # add geometric key
            fl.append(str(myround(fl[2],base=tollerance))+
                    str(myround(fl[3],base=tollerance))+
                    str(myround(fl[4],base=tollerance)))
            results.append(fl)
    # Create pandas dataframe
    headers = ['Stage', 'Time', 'x', 'y', 'z', 'gkey']
    pd_results = pd.DataFrame(data=results, columns=headers)
     
    return results, pd_results #

# def results_to_point_clouds(results):
#     formatted = [[int(elem[0]), (elem[2],elem[3],elem[4])] for elem in results]
#     point_clouds = group_per_stage(formatted)
#     return point_clouds

def group_per_stage(results_list):
    '''
    Groups the results in a dictionary where the keys are the stage numbers
    '''

    results_dict = {}
    for key, group in itertools.groupby(results_list, key=lambda element: element[0]):
        g = list(group)
        t=[]
        for e in g:
            t.append((e[2],e[3],e[4]))
        results_dict[int(key)] = t
    
    return results_dict

def group_per_gkey(results_list):
    '''
    Groups the results in a dictionary where the keys are the geometric keys
    '''

    results_dict = {}
    for key, group in itertools.groupby(results_list, key=lambda element: element[5]):
        g = list(group)
        t=[]
        for e in g:
            t.append((e[2],e[3],e[4]))
        results_dict[key] = t
    
    return results_dict


def find_points (points_clouds, num_stages, tollerance=30):
    '''
    finds matching points in pairs of neighbouring stages. 
    When no matching point is found, blank points are added.
    '''
    
    matches=[]
    for s in range(num_stages-1):
        match = []
        for p in points_clouds[s]:
            cpc = closest_point_in_cloud(p, points_clouds[s+1])
            if cpc[0] > tollerance: # note it is in mm 
                match.append((0.0, (0.0, 0.0, 0.0), 0.0))
            else:
                match.append(cpc)
        matches.append(match)

    return matches

def find_points_0 (points_clouds, num_stages, start_stage=0, tollerance=50):
    '''
    find matching points between one stage and the others. 
    When no matching point is found, blank points are added.
    '''

    points_history={}
    for p in points_clouds[start_stage]:
        matches = []
        for s in range(num_stages-start_stage):
            if not s in points_clouds.keys():
                continue
            if not s+1 in points_clouds.keys():
                cpc = closest_point_in_cloud(p, points_clouds[start_stage+s+2]) #TODO: check
            else:
                cpc = closest_point_in_cloud(p, points_clouds[start_stage+s+1]) #TODO: check
            if cpc[0] > tollerance: # note it is in mm 
                matches.append((0.0, (0.0, 0.0, 0.0), 0.0))
            else:
                matches.append(cpc)
        points_history[str(p)] = matches

    return points_history

def split_points_history(points_history):
    points_history_coord={} # coordinates of the point per stage 
    points_history_disp={} # displacement of the point at stage
    for key, value in points_history.items():
        coord=[]
        disp=[]
        for el in value:
            coord.append(tuple(el[1]))
            disp.append(el[0])
        points_history_coord[key] = coord
        points_history_disp[key] = disp

    return (points_history, points_history_coord, points_history_disp)

def history_to_json(points_history, destination):
    i=0
    for history in points_history:
        name = "\\points_history_" + str(i)
        with open(destination + name + '.json', 'w') as fp:
            json.dump(history, fp, indent=1)
        i+=1


if __name__ == "__main__":    
    # # Step 1 : create sublist for stages
    input_file = DATA + '\\GOM_results\\export_space.txt'

    results, pdf = results_per_stage(input_file)
    
    points_clouds = group_per_stage(results)
    num_stages = len(points_clouds)
    
    points_history = find_points_0(points_clouds, num_stages, tollerance=50)
    
    histories = split_points_history(points_history)
    history_to_json(histories, DATA)

    # grouped = group_per_gkey(results)
    # print(len(grouped))
    
    
    # grouped = pdf.groupby('Stage').count()
    # print(grouped)
    # print(len(grouped))
    # for name,group in grouped:
    #     print (name, len(group))
    
    # print(grouped['1000-16040'].count())
    # stages_results = split_stages(results)
    
    # # Step 2 : find matching points in pairs of neighbouring stages
    # # points = find_points(stages_results[0], 10, 40)