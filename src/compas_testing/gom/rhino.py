import os
import csv

import itertools

import compas
from compas.geometry import closest_point_in_cloud, distance_point_point
from compas.geometry import Point
from compas_rhino.artists import PointArtist


__author__     = 'Francesco Ranaudo'
__copyright__  = 'Copyright 2020, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'ranaudo@arch.ethz.ch'


__all__ = ['find_0_stages',
           'find_0_points',
           'key_to_listcoord',
           'get_test_key',
           'displ_dic',
           'sliced_dict',
           'find_max_val',
           'scaled_val_dic',
           'x_rgb',
           'draw_stages_colour',
           'draw_stages',
           'del_key_in_dict',
           'point_trajectory',
           'find_rhpoint_key', 
           ]


def find_0_stages(data):

    """
    Find the index of stages with blank points.

    Parameters
    ----------
    points_history : dictionary 
        key: string - the coordinates of a point in initial stage
        value : sequence - a sequence of tuples describing locations of a given point in three-dimensional space 
        * tuple : distance to reference point, XYZ coordinates of the point, Stage of the point

    Returns
    -------
    index_list : list - a list of the indexes of stages containing blank points
        
    """

    for key, value in data.items():
        index_list = []
        print(len(value))
        for i in range(len(value)):
            if value[i] == [0.0, 0.0, 0.0]:
                index_list.append(i)
    return index_list


def find_0_points(data):

    """
    Find the keys of points containing blank coordinates in their location history.

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

    key_list = []
    for key, value in data.items():
        for v in value :
            if v == [0.0, 0.0, 0.0]:
                key_list.append(key)
                break
    
    return key_list


def key_to_listcoord(key):

    """
    Convert point keys into XYZ coordinates in 3D space

    Parameters
    ----------
    key: string - the coordinates of a point in initial stage

    Returns
    -------
    coord : list - XYZ coordinates of a point in 3D space
        
    """
    stripkey = key.strip("(").strip(")").split(", ")
    coord = [float(elem) for elem in stripkey]
    return coord


def get_test_key(dict):

    """
    Get a key to test a function.

    Parameters
    ----------
    dict : dictionary

    Returns
    -------
    key : variable - a key in the dictionary
        
    """

    i=0
    for key, value in dict.items():
        while i<1:
            tkey = key
            i += 1
    return tkey


def displ_dic(points_history):

    """
    Create a dictionary describing the displacement of a point through successive stages, measured from its initial position

    Parameters
    ----------
    points_history : dictionary 
        key: string - the coordinates of a point in initial stage
        value : sequence - a sequence of tuples describing locations of a given point in three-dimensional space 
        * tuple : distance to reference point, XYZ coordinates of the point, Stage of the point

    Returns
    -------
    points_history_disp : dictionary 
        key: string - the coordinates of a point in initial stage
        value : list - a list of distances between the reference point and its location in three-dimensional space throughout the stages  

    """

    points_history_disp = {}
    for key, value in points_history.items():
        ref_point = key_to_listcoord(key)
        points_history_disp[key] = []
        for v in value :
            dist = distance_point_point(ref_point, v)
            points_history_disp[key].append(dist)
    return points_history_disp


def sliced_dict(dic, start, stop):

    """
    Remove unwanted values from a dictionary:

    Create a new dictionary containing a slice of the values of the input one.

    Parameters
    ----------
    dic : dictionary 
        key: -
        value : list - length of the list should exceed 'stop'
    
    start : int - the index of the value at the begining of the slice

    stop : int - the index of the value at the end of the slice

    condition : len(values) < start < stop

    Returns
    -------
    sliced_dic : dictionary 

    """
    sliced_dict = {}
    for key, value in dic.items():
        sliced_dict[key] = value[start:stop]
    return sliced_dict


def find_max_val(dic):

    """
    Find the maximal value and corresponding key within a dictionary.

    Parameters
    ----------
    dic : dictionary 
        key: -
        value : list - list of int/float variables

    Returns
    -------
    max_val : int/float - maximal value  
    max_key : key - key corresponding to maximal value

    """
    
    max_val = 0
    for key, value in dic.items():
        intermediate_max = max(dic[key])
        if intermediate_max > max_val:
            max_val = intermediate_max
            max_key = key
    return max_val, max_key


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


def del_key_in_dict(dic, keylist):

    """
    Remove a key and its values from a dictionnary

    Parameters
    ----------
    dic : dictionary 

    keylist : list - list of keys to be removed

    * condition : keys must match in dic and keylist

    Returns
    -------
    dic : dictionary - dictionary with removed keys

    """
    for key in keylist:
        del dic[key]
    return dic


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

    #import point coordinates from json files
    coordinates_file = '/Users/fentons/Desktop/hilo/post-process/points_history_1.json'

    #convert json file to coordinates dictionary
    coordinates_data = read_json(coordinates_file)

    #remove points with blank coordintes in their history from dictionary
    keylist_0 = find_0_points(coordinates_data)
    point_coordinates_cleaned = del_key_in_dict(coordinates_data, keylist_0)

    #remove faulty point from dictionnary 
    #this point has the highest displacement currently since it was mis-mapped in gom
    displacements_all = displ_dic(point_coordinates_cleaned)
    max_displ, max_key = find_max_val(displacements_all)
    point_coordinates = del_key_in_dict(point_coordinates_cleaned, [max_key])

    #compute the displacements of each point through the stages
    displacements = displ_dic(point_coordinates)

    #create a displacement color gradient 
    # find the max point displacement, use it as a scaler to convert displacements into values ranging between 0 and 1, convert these values into rgb colors
    scaler, sc_key = find_max_val(displacements)
    displ_color = scaled_val_dic(scaler, displacements)

    #draw point clouds of chosen stages with associated colors
    stages = draw_stages(point_coordinates, displ_color, 110, 127)

    # FIND POINT TRAJECTORY

    # #import point coordinates from json files
    # filepath = '/Users/fentons/Desktop/hilo/post-process/points_history_1.json'

    # #convert json file to coordinates dictionary
    # input_data = read_json(filepath)

    # #find the key of the selected point int the point_hitory dictionary
    # key = find_rhpoint_key()

    # #Draw the locations in space of a point throughout the successive stages
    # #the points will be drawn in a new layer
    # trajectory = point_trajectory(input_data, key, (0, 255, 255))
