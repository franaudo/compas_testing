from compas_testing import DATA
from compas_testing.hif import parse_spider_results
# from compas_testing.hif import plot_spider_results
from compas_testing.hif import plot_deformations
from compas_testing.hif import plot_forces

input_file = DATA + '/spider_results/cycle00.txt'
[my_info, my_data, my_pd_data] = parse_spider_results(input_file)

my_pd_data['Total Applied Force'] = my_pd_data['Force_south CH=3'] + my_pd_data["Force_north CH=4"]
my_pd_data['Total Ties Tension'] = my_pd_data['TR_south CH=5'] + my_pd_data['TR_north CH=6']
# plot_deformations(my_pd_data)
# plot_forces(my_pd_data)
plot_deformations(my_pd_data)