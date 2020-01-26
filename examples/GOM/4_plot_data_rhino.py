""" 
Script to draw the point clouds in Rhino. The colour of the points is
representative of the relative displacement.
"""

import os
from compas.rpc import Proxy
import compas_testing.rhino as rhino_gom
from compas_testing.helpers import read_json

HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))

# set point coordinates json files location and read the data
input_file = DATA + '/GOM_output/points_history_c1_coord.json'
coordinates_data = read_json(input_file)

input_file = DATA + '/GOM_output/points_history_c1_dist.json'
distances_data = read_json(input_file)

with Proxy('compas_testing.helpers') as helpers:
     disp_ratio = helpers.normalise_dict(distances_data, 'max')
     
with Proxy('compas_testing.gom') as gom:
     color_map = gom.evaluate_color_map(disp_ratio)

for i in range(55):
    rhino_gom.draw_point_cloud_color(coordinates_data, color_map, i)