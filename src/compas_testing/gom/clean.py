
__author__     = 'Francesco Ranaudo'
__copyright__  = 'Copyright 2020, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'ranaudo@arch.ethz.ch'


__all__ = ['find_corrupted_stages',
           'find_corrupted_points',
           'remove_points_from_results',
           'split_results',
           ]

def _key_to_coordinates(key):

    """
    Converts point keys into XYZ coordinates

    Parameters
    ----------
    key: string - the coordinates of a point in initial stage

    Returns
    -------
    coord : tuple - XYZ coordinates of a point in 3D space
        
    """
    stripkey = key.strip("(").strip(")").split(", ")
    point_coordinates = tuple(float(elem) for elem in stripkey)
    return point_coordinates


# ******************************************************************************
#   Clean results
# ******************************************************************************

def find_corrupted_stages(coordinates_data, val=[0.0, 0.0, 0.0]):
    """
    Find the index of the stages with blank points and add them to a list.

    Parameters
    ----------
    points_history : dictionary 
        key: string - the coordinates of a point in initial stage
        value : sequence - a sequence of tuples describing locations of a given point in three-dimensional space 
        * tuple : distance to reference point, XYZ coordinates of the point, Stage of the point
    val: any marker used to identify missing points

    Returns
    -------
    index_list : list - a list with the indexes of the stages containing blank points
        
    """
    index_list = []
    for key, value in coordinates_data.items():
        for i, e in enumerate(value):
            if e == val:
                index_list.append(i)
    # remove duplicates (dict cannot have duplicate kwys!)
    index_list = list(dict.fromkeys(index_list))
    return index_list


def find_corrupted_points(coordinates_data, val=[0.0, 0.0, 0.0]):
    """
    Find the keys of the points containing at least one corrupted configuration in their location history.

    Parameters
    ----------
    points_history : dictionary 
        key: string - the coordinates of a point in initial stage
        value : sequence - a sequence of tuples describing locations of a given point in three-dimensional space 
        * tuple : distance to reference point, XYZ coordinates of the point, Stage of the point

    Returns
    -------
    key_list : list - a list of the keys of the points containing blank coordinates in their location history
        
    """

    corrupted_points_keys = []
    for key, value in coordinates_data.items():
        try:
            value.index(val)
            corrupted_points_keys.append(key)
        except ValueError:
            pass
    
    return corrupted_points_keys


def remove_points_from_results(point_keys, points_history):
    """
    Remove a list of points form the results. This deletes the entire history 
    of that point.

    Parameters
    ----------
    point_key : list - list of the keys of the points to be removed

    point_histories : dict - points results

    Returns
    -------
    points_history : dict - clean results

    """

    for k in point_keys:
        del points_history[k]
    return points_history


def split_results(points_history, chunks):
    """
    Splits the results in chunks. Useful to split continuous measurements into
    test cycles.

    Parameters
    ----------
    points_history : dict 
        key: str - point
        value : list - point history
    
    chunks : dict - the index of the value at the begining of the slice
        key: str - chunck name
        value : list of int - [start, stop]

    Returns
    -------
    cycles : dict of dict 

    """
    cycles = {}
    for c, ends in chunks.items():
        new_history={}
        for point, history in points_history.items():
                new_history[point] = history[ends[0]:ends[-1]]
        cycles.update({c: new_history})
    return cycles


# ******************************************************************************
#   Main results
# ******************************************************************************

if __name__ == "__main__":

    import os

    import compas_testing
    import compas_testing.gom as gom
    from compas_testing.helpers import read_json
    from compas_testing.gom import history_to_json

    HERE = os.path.dirname(__file__)

    HOME = os.path.abspath(os.path.join(HERE, "../../../"))
    DATA = os.path.abspath(os.path.join(HOME, "data"))
    DOCS = os.path.abspath(os.path.join(HOME, "docs"))
    TEMP = os.path.abspath(os.path.join(HOME, "temp"))

    # set point coordinates json files location and read the data
    file_path = DATA + '/GOM_output/points_history_coordinates.json'
    coordinates_data = read_json(file_path)
    
    file_path = DATA + '/GOM_output/points_history_distances.json'
    distances_data = read_json(file_path)

    # clean the data from unwanted points
    corrupted_stages = gom.find_corrupted_stages(coordinates_data)
    corrupted_points = gom.find_corrupted_points(coordinates_data)
    clean_coord_history = gom.remove_points_from_results(corrupted_points, coordinates_data)
    clean_dist_history = gom.remove_points_from_results(corrupted_points, distances_data)

    # divide the results in cycles
    cycles_length = {'c0':[0,10], 'c1':[20,40]}
    cycles_coord = gom.split_results(clean_coord_history, cycles_length)
    cycles_dist = gom.split_results(clean_dist_history, cycles_length)    

    # let's focus only on one cycle
    cycle_coord = cycles_coord['c0']
    history_to_json(cycle_coord, DATA + '/GOM_output', names=['c0_coord'])
    cycle_dist = cycles_dist['c0']
    history_to_json(cycle_dist, DATA + '/GOM_output', names=['c0_dist'])