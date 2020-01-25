import os
import csv
import json
import itertools
import numpy as np

import compas
from compas.geometry import closest_point_in_cloud

from compas_testing.helpers import base_round


__author__     = 'Francesco Ranaudo'
__copyright__  = 'Copyright 2020, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'ranaudo@arch.ethz.ch'


__all__ = ['results_to_list',
           'group_per_stage',
           'group_per_gkey',
           'find_points_between_stages',
           'find_points_from_stage',
           'history_to_json',
           ]


# def parse_results(input_file):
#     results=[]
#     with open(input_file,'r') as f:
#         for line in f:
#             " ".join(line.split())
#             print(line)
#             r = csv.reader(line, delimiter='\t')
#             results.append(r)
#     print(results[0])


# def results_to_point_clouds(results):
#     formatted = [[int(elem[0]), (elem[2],elem[3],elem[4])] for elem in results]
#     point_clouds = group_per_stage(formatted)
#     return point_clouds


# ******************************************************************************
#   IN
# ******************************************************************************

def results_to_list(input_file, tollerance=50):
    """
    Converts the text results to a list and computes the geometric keys of the points within a specific tollerance.

    Parameters
    ----------
    input_file : .txt file 
        File containing the data exported from GOM PONTOS.
        Each row describes the points in successive stages as follows : 
        Stage | Stage time | ID/Name | X | Y | Z | dX | dY | dZ | d
    
    tollerance : maximum distance where to look for corresponding points

    Returns
    -------
    list : a list of lists
        each list describes a point at a given stage as follows : [Stage, time, X, Y, Z, gkey]
    """

    results = []
    with open(input_file,'r') as f:
        for line in f:
            elem = line.split()
            sl = elem[1:3] + elem[4:7]
            fl = list(float(sl[i]) for i in range(len(sl)))
            # add geometric key
            fl.append(str(base_round(fl[2],base=tollerance))+
                    str(base_round(fl[3],base=tollerance))+
                    str(base_round(fl[4],base=tollerance)))
            results.append(fl)
     
    return results
    

def group_per_stage(results_list):
    """
    Groups the results in a dictionary where the keys are the stage numbers and the values are 
    the coordinates of each point.

    Parameters
    ----------
    results_list : a list of lists 
        each list describes a point at a given stage as follows : [Stage, time, X, Y, Z, gkey]

    Returns
    -------
    dict : a dictionary where: 
        key : int - Stage number 
        value : (sequence) – A sequence of locations in three-dimensional space [X, Y, Z]
    """

    results_dict = {}
    for key, group in itertools.groupby(results_list, key=lambda element: element[0]):
        g = list(group)
        t=[]
        for e in g:
            t.append((e[2],e[3],e[4]))
        results_dict[int(key)] = t
    
    return results_dict


def group_per_gkey(results_list):
    """
    Groups the results in a dictionary where the keys are the geometric keys and the values 
    are the point coordinates at each stage.

    Parameters
    ----------
    results_list : a list of lists 
        each list describes a point at a given stage as follows : [Stage, time, X, Y, Z, gkey]

    Returns
    -------
    dict : a dictionary
        each element in the disctionary is described as follows : 
        key : int - gkey 
        value : (sequence) – A sequence of locations in three-dimensional space [X, Y, Z]
    """

    results_dict = {}
    for key, group in itertools.groupby(results_list, key=lambda element: element[5]):
        g = list(group)
        t=[]
        for e in g:
            t.append((e[2],e[3],e[4]))
        results_dict[key] = t
    
    return results_dict


def find_points_between_stages (points_clouds, num_stages, tollerance=30):
    """
    Finds matching points in pairs of neighbouring stages using compas point_in_cloud function. 
    When no matching point is found within the tollerance, blank points (0.0, (0.0, 0.0, 0.0), 0.0) are added.

    Parameters
    ----------
    points_clouds : dictionary 
        key : int - Stage number 
        value : (sequence) – A sequence of locations in three-dimensional space [X, Y, Z] - with a common stage

    num_stages : int - number of stages to consider

    tolerance : int - max distance between two neighbouring points

    Returns
    -------
    matches : a sequence of tuples describing locations of a given point in three-dimensional space 
    tuple – (distance to reference point, XYZ coordinates of the point, Stage of the point)

    """
    
    points_history=[]
    for s in range(num_stages-1):
        match = []
        for p in points_clouds[s]:
            cpc = closest_point_in_cloud(p, points_clouds[s+1])
            if cpc[0] > tollerance: # note it is in mm 
                match.append((0.0, (0.0, 0.0, 0.0), 0.0))
            else:
                match.append(cpc)
        points_history.append(match)

    return points_history


def find_points_from_stage (points_clouds, num_stages, start_stage=0, tollerance=50):
    """
    Finds matching points between one stage and the others using compas point_in_cloud function. 
    When no matching point is found within the tollerance, blank points (0.0, (0.0, 0.0, 0.0), 0.0) are added.

    Parameters
    ----------
    points_clouds : dictionary 
        key : int - Stage number 
        value : (sequence) – A sequence of locations in three-dimensional space [X, Y, Z] - for a common stage

    num_stages : int - number of stages to consider
 
    start_stage : int - stage to find matching points from

    tolerance : int - max distance between two neighbouring points

    Returns
    -------
    points_history : dictionary 
        key: string - the coordinates of a point in initial stage
        value : sequence - a sequence of tuples describing locations of a given point in three-dimensional space 
        tuple – (distance to reference point, XYZ coordinates of the point, Stage of the point)

    """

    points_history={}
    for p in points_clouds[start_stage]:
        matches = []
        for s in range(num_stages-start_stage):
            if not s in points_clouds.keys():
                continue
            if not s+1 in points_clouds.keys():
                cpc = closest_point_in_cloud(p, points_clouds[start_stage+s+2]) 
            else:
                cpc = closest_point_in_cloud(p, points_clouds[start_stage+s+1]) 
            if cpc[0] > tollerance and s<122: # note it is in mm 
                matches.append((0.0, (0.0, 0.0, 0.0), 0.0))
            else:
                matches.append(cpc)
        points_history[str(p)] = matches

    return points_history


# ******************************************************************************
#   OUT
# ******************************************************************************

def _split_points_history(points_history):
    """
    Splits the points history dictionary into two separate dictionaries describing 
    the point coordinates and the point displacements individually.

    Parameters
    ----------
    points_history : dictionary 
        key: string - the coordinates of a point in initial stage
        value : sequence - a sequence of tuples describing locations of a given point in three-dimensional space 
        tuple – (distance to reference point, XYZ coordinates of the point, Stage of the point)

    Returns
    -------
    points_history : dictionary 
        key: string - the coordinates of a point in initial stage
        value : sequence - a sequence of tuples describing locations of a given point in three-dimensional space 
        tuple – (distance to reference point, XYZ coordinates of the point, Stage of the point)

    points_history_coord : dictionary 
        key: string - the coordinates of a point in initial stage
        value : list - a list of locations of a given point in three-dimensional space (XYZ coordinates of the point)

    points_history_disp : dictionary 
        key: string - the coordinates of a point in initial stage
        value : list - a list of distances between the reference point and its location in three-dimensional space throughout the stages 

    """
    
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
    """
    Converts the points history dictionary into json files and saves them in local directory.

    Parameters
    ----------
    points_history : dictionary 
        key: string - the coordinates of a point in initial stage
        value : sequence - a sequence of tuples describing locations of a given point in three-dimensional space 
        tuple – (distance to reference point, XYZ coordinates of the point, Stage of the point)
    destination : the path to the folder in which the file will be saved
    """

    points_histories = _split_points_history(points_history)

    names = ['complete', 'coordinates', 'distances']
    n=0
    for history in points_histories:
        name = "/points_history_" + names[n]
        with open(destination + name + '.json', 'w') as fp:
            json.dump(history, fp, indent=1)
        n+=1


# ******************************************************************************
#   Main
# ******************************************************************************

if __name__ == "__main__":

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
    pass