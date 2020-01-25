import os

import compas_testing
import compas_testing.gom as gom
from compas_testing.helpers import read_json
from compas_testing.gom import history_to_json

HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))

# set point coordinates json files location and read the data
file_path = DATA + '/GOM_output/points_history_coordinates.json'
coordinates_data = read_json(file_path)

file_path = DATA + '/GOM_output/points_history_distances.json'
distances_data = read_json(file_path)

# clean the data from unwanted points
corrupted_stages = gom.find_corrupted_stages(coordinates_data)
corrupted_points = gom.find_corrupted_points(coordinates_data)
clean_coord_history = gom.remove_points_from_results(corrupted_points, coordinates_data)
clean_dist_history = gom.remove_points_from_results(corrupted_points, distances_data)

# divide the results in cycles
cycles_length = {'c0':[0,10], 'c1':[20,40]}
cycles_coord = gom.split_results(clean_coord_history, cycles_length)
cycles_dist = gom.split_results(clean_dist_history, cycles_length)    

# let's focus only on one cycle
cycle_coord = cycles_coord['c0']
history_to_json(cycle_coord, DATA + '/GOM_output', names=['c0_coord'])
cycle_dist = cycles_dist['c0']
history_to_json(cycle_dist, DATA + '/GOM_output', names=['c0_dist'])