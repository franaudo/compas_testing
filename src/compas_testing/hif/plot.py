import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
sns.set_palette(sns.color_palette("husl", 8))


__author__     = 'Francesco Ranaudo'
__copyright__  = 'Copyright 2020, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'ranaudo@arch.ethz.ch'


__all__ = ['plot_material_results',
           'plot_forces',
           'plot_deformations' 
           ]


def plot_material_results(my_pd_data):
    pdf = my_pd_data[0]
    pdf.plot(x ='Extern [mm]', y='Force [kN]', kind = 'scatter')
    plt.show()
    pass


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
    fig, ax = plt.subplots()
    pdf.plot(x ='Extern [mm]', y='Force [kN]', ax=ax, kind = 'line')
    pdf.plot(x ='Def. 2A [mm]', y='Force [kN]', ax=ax, kind = 'line')
    pdf.plot(x ='Def. 2B [mm]', y='Force [kN]', ax=ax, kind = 'line')    
    pdf.plot(x ='Def. 2C [mm]', y='Force [kN]', ax=ax, kind = 'line')
    ax.set_title = ("Deformation [mm]")
    # with sns.axes_style('white'):
    #     sns.kdeplot(data=pdf['Force [kN]'], shade=True)
    plt.show()
