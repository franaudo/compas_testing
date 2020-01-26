from compas.geometry import Point
from compas_rhino.artists import PointArtist
from compas.rpc import Proxy

__author__ = 'Francesco Ranaudo'
__copyright__ = 'Copyright 2020, BLOCK Research Group - ETH Zurich'
__license__ = 'MIT License'
__email__ = 'ranaudo@arch.ethz.ch'

__all__ = ['draw_stage_colour',
           ]


def draw_stage_colour(points_history_coord, points_history_disp_norm, stage_index):
    """
    Draws point clouds for a chosen stage - in Rhino,
    Point color is defined by its displacement from initial position

    Parameters
    ----------
    points_history_coord : dictionary
        key: str - point geometric key
        value : list - a list of locations of a given point in three-dimensional space (XYZ coordinates of the point)

    points_history_disp_norm : dictionary
        key: str - point geometric key
        value : list of floats - normalized displacement  of the point at each stage from its starting position

    stage_index : int - the stages to be drawn

    """

    for key in points_history_coord.keys():
        with Proxy('compas_testing.helpers') as helpers:
            disp_rgb = helpers.ratio_to_rgb(points_history_disp_norm[key][stage_index])

        point = Point(points_history_coord[key][stage_index][0],
                      points_history_coord[key][stage_index][1],
                      points_history_coord[key][stage_index][2]
                      )

        p = PointArtist(point, name=key.strip("()"), color=disp_rgb, layer='Stage_' + str(stage_index))
        p.draw()


# def draw_stages(points_history_coord, scaled_displ, start, stop):
#     '''draw the point cloud for input stages'''
#
#     """
#     Draw point clouds for a sequence of stages - in Rhino,
#     Point color is defined by its displacement from initial postion
#
#     Parameters
#     ----------
#     points_history_coord : dictionary
#         key: *
#         value : list - a list of locations of a given point in three-dimensional space (XYZ coordinates of the point)
#
#     scaled_displ : dictionary
#         key: *
#         value : list - a list of scalars between 0 and 1
#
#     start : the first stage to be drawn
#
#     stop : the last stage to be drawn
#
#     * condition : keys must be identical in points_history_coord and scaled_displ
#
#     """
#
#     for key, value in points_history_coord.items():
#         for j in range(start, stop):
#             point = Point(value[j][0], value[j][1], value[j][2])
#             deformation = scaled_displ[key][j]
#             rgb = ratio_to_rgb(deformation)
#             p = PointArtist(point, name=key.strip("()"), color=rgb, layer='Stage8_' + str(j))
#             p.draw()
#
#     return p
#
#
# def point_trajectory(points_history, key, rgb=(255, 255, 255)):
#     """
#     Draw the locations in space of a point throughout the successive stages
#
#     Parameters
#     ----------
#     points_history : dictionary
#         key: string - the coordinates of a point in initial stage
#         value : sequence - a sequence of tuples describing locations of a given point in three-dimensional space
#         * tuple : distance to reference point, XYZ coordinates of the point, Stage of the point
#
#     key : - key of the point that you want to draw
#
#     color : the chosen color
#
#     """
#
#     values = points_history[key]
#     for v in values:
#         point = Point(v[0], v[1], v[2])
#         p = PointArtist(point, name=key, color=rgb, layer=key.strip("()"))
#         p.draw()
#     return p
#
#
# def find_rhpoint_key():
#     """
#     Select a point on rhino and get its key in the points_history dictionary
#     """
#
#     points = select_points("select one point")
#     coordinates = get_point_coordinates(points)
#     name = get_object_names(points)
#
#     parse = str(name[0])
#     split = parse.split(",")
#     key = '(' + split[0] + ',' + split[1] + ',' + split[2] + ')'
#     return key


# ******************************************************************************
#   Main
# ******************************************************************************

if __name__ == "__main__":
    pass
    # import os
    #
    # import compas_testing
    # import compas_testing.gom as gom
    # from compas_testing.helpers import read_json
    # from compas_testing.helpers import normalise_dict
    #
    # HERE = os.path.dirname(__file__)
    #
    # HOME = os.path.abspath(os.path.join(HERE, "../../../"))
    # DATA = os.path.abspath(os.path.join(HOME, "data"))
    # DOCS = os.path.abspath(os.path.join(HOME, "docs"))
    # TEMP = os.path.abspath(os.path.join(HOME, "temp"))
    #
    # # set point coordinates json files location and read the data
    # coordinates_file = DATA + '/GOM_output/points_history_coordinates.json'
    # coordinates_data = read_json(coordinates_file)
    #
    # # #import point coordinates from json files
    # # coordinates_file = '/Users/fentons/Desktop/hilo/post-process/points_history_1.json'
    #
    # # #convert json file to coordinates dictionary
    # # coordinates_data = read_json(coordinates_file)
    #
    # # #remove points with blank coordintes in their history from dictionary
    # # keylist_0 = find_0_points(coordinates_data)
    # # point_coordinates_cleaned = del_key_in_dict(coordinates_data, keylist_0)
    #
    # # #remove faulty point from dictionnary
    # # #this point has the highest displacement currently since it was mis-mapped in gom
    # # displacements_all = displ_dic(point_coordinates_cleaned)
    # # max_displ, max_key = find_max_val(displacements_all)
    # # point_coordinates = del_key_in_dict(point_coordinates_cleaned, [max_key])
    #
    # # #compute the displacements of each point through the stages
    # # displacements = displ_dic(point_coordinates)
    #
    # # #create a displacement color gradient
    # # find the max point displacement, use it as a scaler to convert displacements into values ranging between 0 and 1, convert these values into rgb colors
    # # scaler, sc_key = find_max_val(displacements)
    # displ_color = normalise_dict(displacements, 'max')
    #
    # # #draw point clouds of chosen stages with associated colors
    # # stages = draw_stages(point_coordinates, displ_color, 110, 127)
    #
    # # # FIND POINT TRAJECTORY
    #
    # # # #import point coordinates from json files
    # # # filepath = '/Users/fentons/Desktop/hilo/post-process/points_history_1.json'
    #
    # # # #convert json file to coordinates dictionary
    # # # input_data = read_json(filepath)
    #
    # # # #find the key of the selected point int the point_hitory dictionary
    # # # key = find_rhpoint_key()
    #
    # # # #Draw the locations in space of a point throughout the successive stages
    # # # #the points will be drawn in a new layer
    # # # trajectory = point_trajectory(input_data, key, (0, 255, 255))
