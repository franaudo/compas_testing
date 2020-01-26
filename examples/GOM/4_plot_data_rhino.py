import os

import compas_testing.rhino as rhino_gom
from compas_testing.helpers import read_json


#rhino_gom = Proxy('compas_testing.rhino')

HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))

# set point coordinates json files location and read the data
input_file = DATA + '/GOM_output/points_history_c0_coord.json'
coordinates_data = read_json(input_file)

input_file = DATA + '/GOM_output/points_history_c0_dist_norm.json'
distances_data = read_json(input_file)

for i in range(5):
    rhino_gom.draw_stage_colour(coordinates_data, distances_data, i)