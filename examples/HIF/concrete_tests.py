from compas_testing import DATA
from compas_testing.hif import parse_material_results
from compas_testing.hif import plot_material_results

input_file = DATA + '/cubes_results/Compressive_Strength.txt'
[my_info, my_data, my_pd_data, my_test_summary] = parse_material_results(input_file, type='compression')

plot_material_results(my_pd_data)