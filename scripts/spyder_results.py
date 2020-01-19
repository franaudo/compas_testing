# scripts to post-process the results form the cube/cylinder concrete tests
import os
import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
sns.set_palette(sns.color_palette("husl", 8))

import csv

HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


def parse_results(input_file):
    '''
    parse the .txt result file and format it
    '''
    data = []
    pd_data = []
    info = []
    # Read the txt file and split it into separate tests
    with open(input_file, newline='') as f:
            r = csv.reader(f, delimiter='\t')
            for i, l in enumerate(r):
                # Get general info
                if i<37:
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

def plot_forces(pdf):
    fig, axs = plt.subplots(3, 1, constrained_layout=True)
    fig.suptitle('Force vs. Time', fontsize = 16)

    pdf.plot(x ='Time  1 - default sample rate CH=1', y='Pressure CH=2', ax=axs[0], kind = 'line')
    axs[0].set_title('Applied Pressure')
    axs[0].set_xlabel('Time [s]')
    axs[0].set_ylabel('Pressure [bar]')

    pdf.plot(x ='Time  1 - default sample rate CH=1', y='Total Applied Force', ax=axs[1], kind = 'line')
    pdf.plot(x ='Time  1 - default sample rate CH=1', y='Total Ties Tension', ax=axs[1], kind = 'line')
    axs[1].set_title('Total Forces')
    axs[1].set_xlabel('Time [s]')
    axs[1].set_ylabel('Force [kN]')

    pdf.plot(x ='Time  1 - default sample rate CH=1', y='Force_south CH=3', ax=axs[2], kind = 'line')
    pdf.plot(x ='Time  1 - default sample rate CH=1', y='Force_north CH=4', ax=axs[2], kind = 'line')
    pdf.plot(x ='Time  1 - default sample rate CH=1', y='TR_south CH=5', ax=axs[2], kind = 'line')
    pdf.plot(x ='Time  1 - default sample rate CH=1', y='TR_north CH=6', ax=axs[2], kind = 'line')
    axs[2].set_title('Individual sensors')
    axs[2].set_xlabel('Time [s]')
    axs[2].set_ylabel('Force [kN]')

    plt.show()

def plot_deformations(pdf):

    fig, axs = plt.subplots(2, 1, constrained_layout=True)
    fig.suptitle('Deformations vs. Time', fontsize = 16)

    pdf.plot(x ='Time  1 - default sample rate CH=1', y='LVDT_ne CH=7', ax=axs[0], kind = 'line')
    pdf.plot(x ='Time  1 - default sample rate CH=1', y='LVDT_nw CH=8', ax=axs[0], kind = 'line')
    pdf.plot(x ='Time  1 - default sample rate CH=1', y='LVDT__me CH=11', ax=axs[0], kind = 'line')
    pdf.plot(x ='Time  1 - default sample rate CH=1', y='LVDT__mw CH=12', ax=axs[0], kind = 'line')
    pdf.plot(x ='Time  1 - default sample rate CH=1', y='LVDT__se CH=13', ax=axs[0], kind = 'line')
    pdf.plot(x ='Time  1 - default sample rate CH=1', y='LVDT__sw CH=14', ax=axs[0], kind = 'line')
    axs[0].set_title('LVDT Response')
    axs[0].set_xlabel('Time [s]')
    axs[0].set_ylabel('Displacement [mm]')

    pdf.plot(y='Total Applied Force', x='LVDT_ne CH=7', ax=axs[1], kind = 'line')
    pdf.plot(y='Total Applied Force', x='LVDT_nw CH=8', ax=axs[1], kind = 'line')
    pdf.plot(y='Total Applied Force', x='LVDT__me CH=11', ax=axs[1], kind = 'line')
    pdf.plot(y='Total Applied Force', x='LVDT__mw CH=12', ax=axs[1], kind = 'line')
    pdf.plot(y='Total Applied Force', x='LVDT__se CH=13', ax=axs[1], kind = 'line')
    pdf.plot(y='Total Applied Force', x='LVDT__sw CH=14', ax=axs[1], kind = 'line')    
    axs[1].set_title('Force - Displacement')
    axs[1].set_xlabel('Displacements [mm]')
    axs[1].set_ylabel('Total Applied Force [kN]')
    # axs[1].set_ylim(-7,0)
    # axs[1].set_xlim(-35,0)
    axs[1].invert_xaxis()
    axs[1].invert_yaxis()
    
    plt.show()


if __name__ == "__main__":
    input_file = DATA + '\\spider_results\\cycle00_2019_12_18_16_15_36_Job1_001_002_001_001.txt'
    # input_file = DATA + '\\spider_results\\cycle01_2019_12_18_16_15_36_Job1_001_002_001_001_001.txt'

    [info, data, pdf] = parse_results(input_file)
    pdf['Total Applied Force'] = pdf['Force_south CH=3'] + pdf['Force_south CH=3']
    beam_weight = -0.79
    plates_weight = -0.11
    additional_weight = beam_weight + plates_weight
    pdf['Total Applied Force'] = pdf['Total Applied Force'].apply(lambda x: x+additional_weight)

    # pdf['TR_south CH=5'] = pdf['TR_south CH=5'].apply(lambda x: x*-0.001)
    pdf['TR_south CH=5'] = (pdf['TR_south CH=5'] + 560.91) * 0.001
    pdf['TR_north CH=6'] = (pdf['TR_north CH=6'] + 562.89) * 0.001
    pdf['Total Ties Tension'] = pdf['TR_south CH=5'] + pdf['TR_north CH=6']
    # plot_forces(pdf)
    plot_deformations(pdf)
