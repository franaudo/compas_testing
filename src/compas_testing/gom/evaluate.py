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


__all__ = ['find_max_displacement',
           ]


# ******************************************************************************
#   Evaluate
# ******************************************************************************

def find_max_displacement(displ_history):

    """
    Find the absolute maximum displacement value and corresponding key among all the points.

    Parameters
    ----------
    points_history : dict
        key: str - point key
        value : list - list of floats

    Returns
    -------  
    max_key : str - key of the point corresponding to maximum displacement
    max_stage: int - stage number where the maximum displamcent occurs
    max_val : float - absolute maximum value in the points history

    """
    
    max_key = max(displ_history)
    max_val = max(displ_history[max_key])
    max_stage = displ_history[max_key].index(max_val)

    # for key, value in points_history.items():
    #     intermediate_max = max(dic[key])
    #     if intermediate_max > max_val:
    #         max_val = intermediate_max
    #         max_key = key
    return max_key, max_stage, max_val





# def get_test_key(dict):

#     """
#     Get a key to test a function.

#     Parameters
#     ----------
#     dict : dictionary

#     Returns
#     -------
#     key : variable - a key in the dictionary
        
#     """

#     i=0
#     for key, value in dict.items():
#         while i<1:
#             tkey = key
#             i += 1
#     return tkey


# def point_history(points_history):

#     """
#     Create a dictionary describing the displacement of a point through successive stages, measured from its initial position

#     Parameters
#     ----------
#     points_history : dictionary 
#         key: string - the coordinates of a point in initial stage
#         value : sequence - a sequence of tuples describing locations of a given point in three-dimensional space 
#         * tuple : distance to reference point, XYZ coordinates of the point, Stage of the point

#     Returns
#     -------
#     points_history_disp : dictionary 
#         key: string - the coordinates of a point in initial stage
#         value : list - a list of distances between the reference point and its location in three-dimensional space throughout the stages  

#     """

#     points_history_disp = {}
#     for key, value in points_history.items():
#         ref_point = key_to_listcoord(key)
#         points_history_disp[key] = []
#         for v in value :
#             dist = distance_point_point(ref_point, v)
#             points_history_disp[key].append(dist)
#     return points_history_disp


def scaled_val_dic(factor, dic):

    """
    Create a dictionary in which all values are scaled by a given factor

    Parameters
    ----------
    factor : float - scalar used to scale values
    dic : dictionary 
        key: -
        value : list - a list of scalars

    Returns
    -------
    scaled_dic : dictionary 
        key: -
        value : list - a list of scalars obtained by dividing the input values by the set factor
    
    """
    scaled_dic = {}
    for key, value in dic.items():
        scaled_dic[key] = [v/factor for v in value]
    return scaled_dic


# ******************************************************************************
#   Main
# ******************************************************************************

if __name__ == "__main__":

    import os

    import compas_testing
    import compas_testing.gom as gom
    from compas_testing.helpers import read_json

    HERE = os.path.dirname(__file__)

    HOME = os.path.abspath(os.path.join(HERE, "../../../"))
    DATA = os.path.abspath(os.path.join(HOME, "data"))
    DOCS = os.path.abspath(os.path.join(HOME, "docs"))
    TEMP = os.path.abspath(os.path.join(HOME, "temp"))

    # set point coordinates json files location and read the data
    coordinates_file = DATA + '/GOM_output/points_history_c0_dist.json'
    coordinates_data = read_json(coordinates_file)

    max_key, max_stage, max_val = gom.find_max_displacement(coordinates_data)
    print(str(max_key), str(max_stage), str(max_val))

