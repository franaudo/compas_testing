__author__ = 'Francesco Ranaudo'
__copyright__ = 'Copyright 2020, BLOCK Research Group - ETH Zurich'
__license__ = 'MIT License'
__email__ = 'ranaudo@arch.ethz.ch'

__all__ = ['find_corrupted_stages',
           'find_corrupted_points',
           'remove_points_from_results',
           'split_results',
           ]


# ******************************************************************************
#   Clean results
# ******************************************************************************
def find_corrupted_stages(coordinates_data, val=(0.0, 0.0, 0.0)):
    """
    Find the index of the stages with blank points and add them to a list.

    Parameters
    ----------
    coordinates_data : dictionary
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
    # remove duplicates (dict cannot have duplicate keys!)
    index_list = list(dict.fromkeys(index_list))
    return index_list


def find_corrupted_points(coordinates_data, val=(0.0, 0.0, 0.0)):
    """
    Find the keys of the points containing at least one corrupted configuration in their location history.

    Parameters
    ----------
    coordinates_data : dictionary
        key: string - the coordinates of a point in initial stage
        value : sequence - a sequence of tuples describing locations of a given point in three-dimensional space
        * tuple : distance to reference point, XYZ coordinates of the point, Stage of the point
    val: any marker used to identify missing points

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
    point_keys : list - list of the keys of the points to be removed

    points_history : dict - points results

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

    chunks : dict - the index of the value at the beginning of the slice
        key: str - chunk name
        value : list of int - [start, stop]

    Returns
    -------
    cycles : dict of dict

    """
    cycles = {}
    for c, ends in chunks.items():
        new_history = {}
        for point, history in points_history.items():
            new_history[point] = history[ends[0]:ends[-1]]
        cycles.update({c: new_history})
    return cycles


# ******************************************************************************
#   Main results
# ******************************************************************************

if __name__ == "__main__":
    pass
