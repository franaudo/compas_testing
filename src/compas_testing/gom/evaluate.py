import os
import csv
import json
import itertools
import numpy as np



__author__     = 'Francesco Ranaudo'
__copyright__  = 'Copyright 2020, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'ranaudo@arch.ethz.ch'


__all__ = ['find_abs_max_displacement',
           'evaluate_displacements',
           ]


# ******************************************************************************
#   Evaluate
# ******************************************************************************

def find_abs_max_displacement(disp_history):

    """
    Find the absolute maximum displacement value and corresponding key among all the points.

    Parameters
    ----------
    disp_history : dict
        key: str - point key
        value : list - list of floats

    Returns
    -------
    max_key : str - key of the point corresponding to maximum displacement
    max_stage: int - stage number where the maximum displacement occurs
    max_val : float - absolute maximum value in the points history

    """

    max_key = max(disp_history)
    max_val = max(disp_history[max_key])
    max_stage = disp_history[max_key].index(max_val)

    return max_key, max_stage, max_val


def evaluate_displacements(points_history):
    """
    Create a dictionary describing the displacement of a point through successive stages,
    measured from its initial position, using compas distance_point_point function.
    Use this function if you want to validate the distance results from the compas
    point_in_cloud function.

    Parameters
    ----------
    points_history : dictionary
        key: str - the coordinates of a point in initial stage
        value : sequence - a sequence of tuples describing locations of a given point in three-dimensional space
        * tuple : distance to reference point, XYZ coordinates of the point, Stage of the point

    Returns
    -------
    points_history_disp : dictionary
        key: str - the coordinates of a point in initial stage
        value : list - a list of distances between the reference point and its location for every stage.

    """

    from compas_testing.helpers import key_to_coordinates
    from compas.geometry import distance_point_point

    points_history_disp = {}
    for key, value in points_history.items():
        ref_point = key_to_coordinates(key)
        points_history_disp[key] = []
        for v in value :
            points_history_disp[key].append(distance_point_point(ref_point, v))
    return points_history_disp


# def evaluate_trajectory(point_key, points_history_coord):
#     """
#     Create a dictionary describing the displacement of a point through successive stages,
#     measured from its initial position, using compas distance_point_point function.
#     Use this function if you want to validate the distance results from the compas
#     point_in_cloud function.

#     Parameters
#     ----------
#     points_history : dictionary
#         key: str - the coordinates of a point in initial stage
#         value : sequence - a sequence of tuples describing locations of a given point in three-dimensional space
#         * tuple : distance to reference point, XYZ coordinates of the point, Stage of the point

#     Returns
#     -------
#     points_history_disp : dictionary
#         key: str - the coordinates of a point in initial stage
#         value : list - a list of distances between the reference point and its location for every stage.

#     """


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
    input_file = DATA + '/GOM_output/points_history_c0_coord.json'
    coordinates_data = read_json(input_file)

    input_file = DATA + '/GOM_output/points_history_c0_dist.json'
    distances_data = read_json(input_file)

    max_key, max_stage, max_val = gom.find_abs_max_displacement(distances_data)
    print('from compas_point_cloud: ', str(max_key), str(max_stage), str(max_val))

    displacements = gom.evaluate_displacements(coordinates_data)
    max_key, max_stage, max_val = gom.find_abs_max_displacement(displacements)
    print('from compas_point_distance: ', str(max_key), str(max_stage), str(max_val))
    # NOTE: probably it is different because one starts from stage 0 and the other from stage 1.
    # TODO: fix dictionaries key to use stage 0 coordinates values
