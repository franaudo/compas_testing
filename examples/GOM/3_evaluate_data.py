import os

import compas_testing
import compas_testing.gom as gom
from compas_testing.gom import history_to_json
from compas_testing.helpers import read_json
from compas_testing.helpers import normalise_dict

HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))

# set point coordinates json files location and read the data
input_file = DATA + '/GOM_output/points_history_c0_coord.json'
coordinates_data = read_json(input_file)

input_file = DATA + '/GOM_output/points_history_c0_dist.json'
distances_data = read_json(input_file)

max_key, max_stage, max_val = gom.find_abs_max_displacement(distances_data)
print('from compas_point_cloud: ', str(max_key), str(max_stage), str(max_val))

displacements = gom.evaluate_displacements(coordinates_data)
max_key, max_stage, max_val = gom.find_abs_max_displacement(displacements)
print('from compas_point_distance: ', str(max_key), str(max_stage), str(max_val))
# NOTE: probably it is different because one starts from stage 0 and the other from stage 1.
# TODO: fix dictionaries key to use stage 0 coordinates values

disp_ratio = normalise_dict(distances_data, 'max')
history_to_json(disp_ratio, DATA + '/GOM_output', names=['c0_dist_norm'])
