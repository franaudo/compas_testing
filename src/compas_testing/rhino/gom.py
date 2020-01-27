from compas.geometry import Point
from compas_rhino.artists import PointArtist


__author__ = 'Francesco Ranaudo'
__copyright__ = 'Copyright 2020, BLOCK Research Group - ETH Zurich'
__license__ = 'MIT License'
__email__ = 'ranaudo@arch.ethz.ch'

__all__ = ['draw_point_cloud_color',
           ]


def draw_point_cloud_color(points_history_coord, color_map, stage_index):
    """
    Draws point clouds for a chosen stage - in Rhino,
    Point color is defined by its displacement from initial position

    Parameters
    ----------
    points_history_coord : dictionary
        key: str - point geometric key
        value : list - a list of locations of a given point in three-dimensional space (XYZ coordinates of the point)

    color_map : dictionary
        key: str - point geometric key
        value : list of lists - RGB values for each point at each stage

    stage_index : int - the stages to be drawn

    """
    for key in points_history_coord.keys():
        point = Point(points_history_coord[key][stage_index][0],
                      points_history_coord[key][stage_index][1],
                      points_history_coord[key][stage_index][2]
                      )
        p = PointArtist(point, name=key.strip("()"), color=color_map[key][stage_index], layer='Stage_'+str(stage_index))
        p.draw()


def draw_delaunay_mesh(point_cloud, color_map):
    pass

# def draw_stages(points_history_coord, scaled_disp, start, stop):
#     '''draw the point cloud for input stages'''
#
#     """
#     Draw point clouds for a sequence of stages - in Rhino,
#     Point color is defined by its displacement from initial position
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
