import os

import compas_testing.gom as gom
from compas_testing.helpers import read_json
from compas_testing.helpers import normalise_dict
from compas_testing.helpers import combine_dict_in_json

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

max_key, max_stage, max_val = gom.find_abs_max_displacement(distances_data)
print('from compas_point_cloud: ', str(max_key), str(max_stage), str(max_val))

displacements = gom.evaluate_displacements(coordinates_data)
max_key, max_stage, max_val = gom.find_abs_max_displacement(displacements)
print('from compas_point_distance: ', str(max_key), str(max_stage), str(max_val))
# NOTE: probably it is different because one starts from stage 0 and the other from stage 1.
# TODO: fix dictionaries key to use stage 0 coordinates values

disp_ratio = normalise_dict(distances_data, 'max')

color_map = gom.evaluate_color_map(disp_ratio)
combine_dict_in_json([distances_data, disp_ratio, color_map], DATA + '/GOM_output', 'combined')
