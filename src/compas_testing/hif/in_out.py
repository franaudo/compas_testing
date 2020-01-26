import csv
import pandas as pd

__author__ = 'Francesco Ranaudo'
__copyright__ = 'Copyright 2020, BLOCK Research Group - ETH Zurich'
__license__ = 'MIT License'
__email__ = 'ranaudo@arch.ethz.ch'

__all__ = ['parse_material_results',
           'parse_spider_results',
           ]


def parse_material_results(input_file, type):
    """
    parse the .txt result file and format it
    """
    data = []
    pd_data = []
    info = []
    test_summary = []

    # Read the txt file and split it into separate tests
    with open(input_file, newline='') as f:
        r = csv.reader(f, delimiter=';')
        log = []
        for i, l in enumerate(r):
            # Get general info
            if i < 4:
                info.append(l)
                continue
            if not l:
                data.append(log)
                log = []
                continue
            log.append(l)

    # Set the headers for the panda tables
    if type == 'compression':
        headers = ['Index', 'Element', 'Markierung', 'Time [s]', 'Force [kN]', 'Extern [mm]',
                   'Def. 2A [mm]', 'Def. 2B [mm]', 'Def. 2C [mm]']
    elif type == 'double punch':
        headers = ['Index', 'Element', 'Markierung', 'Time [s]', 'Force [kN]', 'Extern [mm]']

    # Split the lists
    for t in range(len(data)):
        test_summary.append(data[t][0])
        data[t] = data[t][3:]
        for el in range(len(data[t])):
            for item in range(len(data[t][el])):
                data[t][el][item] = float(data[t][el][item])
        pd_data.append(pd.DataFrame(data=data[t], columns=headers))

    return [info, data, pd_data, test_summary]


def parse_spider_results(input_file):
    """
    parse the .txt result file and format it
    """

    data = []
    pd_data = []
    info = []
    # Read the txt file and split it into separate tests
    with open(input_file, newline='') as f:
        r = csv.reader(f, delimiter='\t')
        for i, l in enumerate(r):
            # Get general info
            if i < 37:
                if not l:
                    continue
                else:
                    info.append(l)
                    continue
            if not l:
                continue
            data.append(l)

    # Remove last empty column
    for l in range(len(data)):
        data[l].pop()
        for i in range(len(data[l])):
            data[l][i] = float(data[l][i])
    # Set the headers ad convert to pandas dataframe
    headers = info[6]
    pd_data = pd.DataFrame(data=data, columns=headers)

    return [info, data, pd_data]


# ******************************************************************************
#   Main
# ******************************************************************************

if __name__ == "__main__":
    import os

    input_file = DATA + '\\cubes_results\\Compressive_Strength.txt'
    [my_info, my_data, my_pd_data, my_test_summary] = parse_results(input_file, type='compression')
    # input_file = DATA + '\\cubes_results\\Double_Punch.txt'
    # [my_info, my_data, my_pd_data, my_test_summary] = parse_results(input_file, type='double punch')
    # # print(my_pd_data)
    # print(my_pd_data)
    # my_fct = double_pounch(124.3, 150, 150)
    # print(my_fct)
    # pdf = my_pd_data[0].cumsum()
    pdf = my_pd_data[0]
