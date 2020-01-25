"""
This example illustrates how to import the results file generate by GOM PONTOS 
and convert it to 3 json file for further post-process
"""

__author__     = 'Francesco Ranaudo'
__copyright__  = 'Copyright 2020, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'ranaudo@arch.ethz.ch'


import os

import compas_testing.gom as gom

HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))

# 1. import results file from GOM (generate with the proper template)  
input_file = DATA + '/GOM_results/gom_export.txt'

# 2. Convert results
results = gom.results_to_list(input_file)

# 3. Create pointclouds for each stage
points_clouds = gom.group_per_stage(results)

# 4. Group information per point
num_stages = len(points_clouds)
points_history = gom.find_points_from_stage(points_clouds, num_stages, tollerance=50)

# 5. Export to json
gom.history_to_json(points_history, 
                    DATA + '/GOM_output', 
                    names=['complete', 'coordinates', 'distances'],
                    from_gom=True)