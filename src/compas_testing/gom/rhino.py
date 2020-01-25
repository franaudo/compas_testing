import itertools

import compas
from compas.geometry import closest_point_in_cloud, distance_point_point
from compas.geometry import Point

from compas_rhino.artists import PointArtist


__author__     = 'Francesco Ranaudo'
__copyright__  = 'Copyright 2020, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'ranaudo@arch.ethz.ch'


__all__ = ['find_corrupted_stages',
           'find_corrupted_points',
           'split_results',
           'find_max_val',
           'scaled_val_dic',
           'x_rgb',
           'draw_stages_colour',
           'draw_stages',
           'remove_points_from_results',
           'point_trajectory',
           'find_rhpoint_key', 
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


def x_rgb(x_ratio):

    """
    Convert a number between 0 and 1 into an rgb color

    Parameters
    ----------
    x_ratio : float - scalar number between 0 and 1

    Returns
    -------
    rgb : tuple - rgb color 
    
    """
    b = 0
    if round(x_ratio, 1) == 0.5:
        r = 255
        g = 255
    elif x_ratio < 0.5:
        r = int(x_ratio * 2 * 255.0)
        g = 255
    else:
        r = 255
        g = int((1.0 - x_ratio) * 2 * 255.0)
    rgb = (r, g, b)

    return rgb


def draw_stages_colour(points_history_coord, scaled_displ, STAGE_a, STAGE_b):

    """
    Draw point clouds for chosen stages - in Rhino, 
    Point color is defined by its displacement from initial postion

    Parameters
    ----------
    points_history_coord : dictionary 
        key: *
        value : list - a list of locations of a given point in three-dimensional space (XYZ coordinates of the point)
    
    scaled_displ : dictionary 
        key: *
        value : list - a list of scalars between 0 and 1

    STAGE_ : the stages to be drawn

    * condition : keys must be identical in points_history_coord and scaled_displ

    """

    for key, value in points_history_coord.items():
        i=0
        for j in range(len(value)):
            if i==STAGE_a or i==STAGE_b:
                point = Point(value[j][0],value[j][1],value[j][2])
                deformation = scaled_displ[key][j]
                rgb = x_rgb(deformation)
                p = PointArtist(point, name=key.strip("()"), color=rgb, layer='Stage_'+str(i))
                p.draw()
                i+=1
            else:
                i+=1
    return p 


def draw_stages(points_history_coord, scaled_displ, start, stop):

    '''draw the point cloud for input stages'''

    """
    Draw point clouds for a sequence of stages - in Rhino, 
    Point color is defined by its displacement from initial postion

    Parameters
    ----------
    points_history_coord : dictionary 
        key: *
        value : list - a list of locations of a given point in three-dimensional space (XYZ coordinates of the point)
    
    scaled_displ : dictionary 
        key: *
        value : list - a list of scalars between 0 and 1

    start : the first stage to be drawn

    stop : the last stage to be drawn

    * condition : keys must be identical in points_history_coord and scaled_displ

    """

    for key, value in points_history_coord.items():
        for j in range(start, stop):
            point = Point(value[j][0],value[j][1],value[j][2])
            deformation = scaled_displ[key][j]
            rgb = x_rgb(deformation)
            p = PointArtist(point, name=key.strip("()"), color=rgb, layer='Stage8_'+str(j))
            p.draw()

    return p 


def point_trajectory(points_history, key, rgb=(255, 255, 255)):


    """
    Draw the locations in space of a point throughout the successive stages 

    Parameters
    ----------
    points_history : dictionary 
        key: string - the coordinates of a point in initial stage
        value : sequence - a sequence of tuples describing locations of a given point in three-dimensional space 
        * tuple : distance to reference point, XYZ coordinates of the point, Stage of the point

    key : - key of the point that you want to draw

    color : the chosen color
        
    """

    values = points_history[key]
    for v in values:
        point = Point(v[0],v[1],v[2])
        p = PointArtist(point, name=key, color=rgb, layer=key.strip("()"))
        p.draw()
    return p


def find_rhpoint_key():

    """
    Select a point on rhino and get its key in the points_history dictionary
    """

    points = select_points("select one point")
    coordinates = get_point_coordinates(points)
    name = get_object_names(points)

    parse = str(name[0])
    split = parse.split(",")
    key = '(' + split[0] + ',' + split[1] + ',' + split[2] + ')'
    return key


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
    coordinates_file = DATA + '/GOM_output/points_history_coordinates.json'
    coordinates_data = read_json(coordinates_file)

    # #import point coordinates from json files
    # coordinates_file = '/Users/fentons/Desktop/hilo/post-process/points_history_1.json'

    # #convert json file to coordinates dictionary
    # coordinates_data = read_json(coordinates_file)

    # #remove points with blank coordintes in their history from dictionary
    # keylist_0 = find_0_points(coordinates_data)
    # point_coordinates_cleaned = del_key_in_dict(coordinates_data, keylist_0)

    # #remove faulty point from dictionnary 
    # #this point has the highest displacement currently since it was mis-mapped in gom
    # displacements_all = displ_dic(point_coordinates_cleaned)
    # max_displ, max_key = find_max_val(displacements_all)
    # point_coordinates = del_key_in_dict(point_coordinates_cleaned, [max_key])

    # #compute the displacements of each point through the stages
    # displacements = displ_dic(point_coordinates)

    # #create a displacement color gradient 
    # # find the max point displacement, use it as a scaler to convert displacements into values ranging between 0 and 1, convert these values into rgb colors
    # scaler, sc_key = find_max_val(displacements)
    # displ_color = scaled_val_dic(scaler, displacements)

    # #draw point clouds of chosen stages with associated colors
    # stages = draw_stages(point_coordinates, displ_color, 110, 127)

    # # FIND POINT TRAJECTORY

    # # #import point coordinates from json files
    # # filepath = '/Users/fentons/Desktop/hilo/post-process/points_history_1.json'

    # # #convert json file to coordinates dictionary
    # # input_data = read_json(filepath)

    # # #find the key of the selected point int the point_hitory dictionary
    # # key = find_rhpoint_key()

    # # #Draw the locations in space of a point throughout the successive stages
    # # #the points will be drawn in a new layer
    # # trajectory = point_trajectory(input_data, key, (0, 255, 255))
