"""
This example illustrates how to import the results file generate by GOM PONTOS 
and convert it to 3 json file for further post-process
"""

import os

import compas_testing.gom as gom

HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))

# import table describing the locations of a series of points in 3D space, at different stages  
input_file = DATA + '/GOM_results/gom_export.txt'

# create sublists per stages
results = gom.results_to_list(input_file)

# create a dictionnary per stage with indivuidual keys for points
points_clouds = gom.group_per_stage(results)

# find total number of stages
num_stages = len(points_clouds)

# create a dictionnary per point describing the point locations in space throughout the stages
points_history = gom.find_points_from_stage(points_clouds, num_stages, tollerance=50)

# export point coordinates and point displacements into separate json files
gom.history_to_json(points_history, DATA + '/GOM_output')