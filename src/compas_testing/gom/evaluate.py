
from compas_testing.helpers import key_to_coordinates
from compas_testing.helpers import ratio_to_rgb
from compas.geometry import distance_point_point


__author__     = 'Francesco Ranaudo'
__copyright__  = 'Copyright 2020, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'ranaudo@arch.ethz.ch'


__all__ = ['find_abs_max_displacement',
           'evaluate_displacements',
           'evaluate_color_map',
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
    points_history_disp = {}
    for key, value in points_history.items():
        ref_point = key_to_coordinates(key)
        points_history_disp[key] = []
        for v in value:
            points_history_disp[key].append(distance_point_point(ref_point, v))
    return points_history_disp


def evaluate_color_map(points_history_value_normalised):
    """
    Creates a color map dictionary where the keys are the points and the values are the rgb tuples associated to each
    stage. Typically used with normalised displacements.

    Parameters
    ----------
    points_history_value_normalised : dictionary
        key: str - the coordinates of a point in initial stage
        value : list - normalised values [0-1] to draw the color map

    Returns
    -------
    color_map : dictionary
        key: str - the coordinates of a point in initial stage
        value : list of tuples - a list with the rgb tuples associated to each stage.

    """
    color_map = {}
    for key in points_history_value_normalised.keys():
        disp_rgb = []
        for v in points_history_value_normalised[key]:
            disp_rgb.append(ratio_to_rgb(v))
        color_map[key] = disp_rgb
    return color_map

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
    pass
