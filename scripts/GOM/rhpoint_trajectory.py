import os
import csv
import json
import itertools

import compas
from compas.geometry import closest_point_in_cloud
from compas.geometry import Point
from compas_rhino.artists import PointArtist
from compas_rhino.utilities import select_points, get_point_coordinates, get_object_names

def read_json(filepath):

    """
    Read the json file.

    Parameters
    ----------
    file : json file
        A json file with collected data.

    Returns
    -------
    data : dictionnary with data formatted into keys and values
        
    """

    with open(filepath, 'r') as fp:
        data = json.load(fp)
    return data


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

if __name__ == "__main__":

    #import point coordinates from json files
    filepath = '/Users/fentons/Desktop/hilo/post-process/points_history_1.json'

    #convert json file to coordinates dictionary
    input_data = read_json(filepath)

    #find the key of the selected point int the point_hitory dictionary
    key = find_rhpoint_key()

    #Draw the locations in space of a point throughout the successive stages
    #the points will be drawn in a new layer
    trajectory = point_trajectory(input_data, key, (0, 255, 255))







