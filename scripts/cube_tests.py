# scripts to post-process the results form the cube/cylinder concrete tests
import os
import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

import csv

HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


def parse_results(input_file, type):
    '''
    parse the .txt result file and format it
    '''
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
                if i<4:
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

def plot_results():
    pdf = my_pd_data[0]
    pdf.plot(x ='Extern [mm]', y='Force [kN]', kind = 'scatter')
    plt.show()
    pass

def double_pounch(Ncr, D, h, p=37.5):
    fct = 4*10**3*Ncr / (math.pi*(2.4*D*h-p**2))
    return fct


if __name__ == "__main__":
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
    fig, ax = plt.subplots()
    pdf.plot(x ='Extern [mm]', y='Force [kN]', ax=ax, kind = 'line')
    pdf.plot(x ='Def. 2A [mm]', y='Force [kN]', ax=ax, kind = 'line')
    pdf.plot(x ='Def. 2B [mm]', y='Force [kN]', ax=ax, kind = 'line')    
    pdf.plot(x ='Def. 2C [mm]', y='Force [kN]', ax=ax, kind = 'line')
    ax.set_title = ("Deformation [mm]")
    # with sns.axes_style('white'):
    #     sns.kdeplot(data=pdf['Force [kN]'], shade=True)
    plt.show()
