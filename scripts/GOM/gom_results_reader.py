import os
import csv
import json
import itertools
import numpy as np

import compas
from compas.geometry import closest_point_in_cloud


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


def myround(x, base):

    """Custom multiple rounding function.

    Parameters
    ----------
    x : float, number to be rounded
    base: base used to round the number

    Returns
    -------
    int : rounded number
    """

    return base * round(x/base)


def results_per_stage(input_file, tollerance=60):

    """parse the input file into a list per point and per stage and convert to float 

    Parameters
    ----------
    input_file : .txt file 
        File contains data exported from gom : analysis of displacement of points placed on an element submitted to a bending test.
        Each row describes the points in successive stages as follows : Stage|Stagetime|ID/Name| X| Y| Z| dX| dY| dZ|d

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
            fl.append(str(myround(fl[2],base=tollerance))+
                    str(myround(fl[3],base=tollerance))+
                    str(myround(fl[4],base=tollerance)))
            results.append(fl)
     
    return results


def group_per_stage(results_list):

    """
    Groups the results in a dictionary where the keys are the stage numbers and the values are the point coordinates

    Parameters
    ----------
    results_list : a list of lists 
        each list describes a point at a given stage as follows : [Stage, time, X, Y, Z, gkey]

    Returns
    -------
    dict : a dictionary
        each element in the dictionary is described as follows : 
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
    Groups the results in a dictionary where the keys are the geometric keys and the values are the point coordinates

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


def find_points (points_clouds, num_stages, tollerance=30):


    '''
    finds matching points in pairs of neighbouring stages. 
    When no matching point is found, blank points are added.
    '''
    
    """
    Create a dictionary describing the history of a point through successive stages:
    
    The browsed lists contain the coordinates of many different points at the same stage.
    Find corresponding point in pairs of neighbouring stages and group them into point_history_lists.
    Corresponding points are identified by searching for the two closest points in neighbouring stages.
    When no matching point is found, blank points are added.

    Parameters
    ----------
    points_clouds : dictionary 
        key : int - Stage number 
        value : (sequence) – A sequence of locations in three-dimensional space [X, Y, Z] - with a common stage

    num_stages : int - total number of stages

    tolerance : int - distance between two neighbouring points

    Returns
    -------
    matches : a sequence of tuples describing locations of a given point in three-dimensional space 
        tuple – (distance to reference point, XYZ coordinates of the point, Stage of the point)

    """


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
    finds matching points between one stage and the others. 
    When no matching point is found, blank points are added.
    '''

    """
    Create a dictionary describing the history of a point through successive stages:
    
    The browsed lists contain the coordinates of many different points at the same stage.
    Find corresponding points between a starting stage and following stages, and group them into point_history_lists. 
    Corresponding points are identified by searching for the closest points in different stages.
    When no matching point is found, blank points are added.

    Parameters
    ----------
    points_clouds : dictionary 
        key : int - Stage number 
        value : (sequence) – A sequence of locations in three-dimensional space [X, Y, Z] - for a common stage

    num_stages : int - total number of stages
 
    start_stage : int - stage to find matching points from

    tolerance : int - distance between two neighbouring points

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


def split_points_history(points_history):


    """
    Split the points history dictionary into two separate dictionaries describing the point coordinates and the point displacements individually.

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
    Convert the point history dictionary into a json file and save it in a folder.

    Parameters
    ----------
    points_history : dictionary 
        key: string - the coordinates of a point in initial stage
        value : sequence - a sequence of tuples describing locations of a given point in three-dimensional space 
                tuple – (distance to reference point, XYZ coordinates of the point, Stage of the point)
    destination : the path to the folder in which the file will be saved


    """

    i=0
    for history in points_history:
        name = "/points_history_" + str(i)
        with open(destination + name + '.json', 'w') as fp:
            json.dump(history, fp, indent=1)
        i+=1


if __name__ == "__main__":    

    # import table describing the locations of a series of points in 3D space, at different stages  
    input_file = '/Users/fentons/Code/Repositories/gom_postprocess/data/gom_results.txt'
    
    # create sublists per stages
    results = results_per_stage(input_file)
    
    #create a dictionnary per stage with indivuidual keys for points
    points_clouds = group_per_stage(results)
    
    #find total number of stages
    num_stages = len(points_clouds)
    
    #create a dictionnary per point describing the point locations in space throughout the stages
    points_history = find_points_0(points_clouds, num_stages, tollerance=50)
    
    #split point_history data into point coordinates and displacements
    histories = split_points_history(points_history)

    #export point coordinates and point displacements into separate json files
    history_to_json(histories, '/Users/fentons/Code/Repositories/gom_postprocess/data')

