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


def plot_material_results(pd_data):
    """
    Plots the restults of a compression test on concrete cubes/cylinders.

    Parameters
    ----------
    pd_data: panda dataframe with the results

    Returns
    -------

    """
    i   =   0
    fig, axs = plt.subplots(1, 3, constrained_layout=True)
    fig.suptitle('Compression tests', fontsize = 16)
    for pdf in pd_data:
        pdf.plot(x ='Extern [mm]', y='Force [kN]', ax=axs[i], kind = 'line')
        pdf.plot(x ='Def. 2A [mm]', y='Force [kN]', ax=axs[i], kind = 'line')
        pdf.plot(x ='Def. 2B [mm]', y='Force [kN]', ax=axs[i], kind = 'line')    
        pdf.plot(x ='Def. 2C [mm]', y='Force [kN]', ax=axs[i], kind = 'line')
        axs[i].legend(["Extern", "A", "B", "C"])
        axs[i].set_title('Cube_'+str(i+1))
        axs[i].set_xlabel('Defromation [mm]')
        axs[i].set_ylabel('Force [kN]')
        axs[i].set_ylim(0, 1000)
        i += 1
    plt.show()


def plot_spider_results(pdf):
    """
    Plots the restults of a test on the strong beam.

    Parameters
    ----------
    pd_data: panda dataframe with the results

    Returns
    -------

    """
    fig, axs = plt.subplots(2, 1, constrained_layout=True)
    fig.suptitle('Force - Displacement', fontsize = 16)
    pdf.plot(y='Total Applied Force', x='LVDT_ne CH=7', ax=axs[1], kind = 'line')
    pdf.plot(y='Total Applied Force', x='LVDT_nw CH=8', ax=axs[1], kind = 'line')
    pdf.plot(y='Total Applied Force', x='LVDT__me CH=11', ax=axs[1], kind = 'line')
    pdf.plot(y='Total Applied Force', x='LVDT__mw CH=12', ax=axs[1], kind = 'line')
    pdf.plot(y='Total Applied Force', x='LVDT__se CH=13', ax=axs[1], kind = 'line')
    pdf.plot(y='Total Applied Force', x='LVDT__sw CH=14', ax=axs[1], kind = 'line')

    pass


def plot_forces(pdf):

    fig, axs = plt.subplots(2, 1, constrained_layout=True)
    fig.suptitle('Force vs. Time', fontsize = 16)

    pdf.plot(x ='Time  1 - default sample rate CH=1', y='Pressure CH=2', ax=axs[0], kind = 'line')
    axs[0].set_title('Applied Pressure')
    axs[0].set_xlabel('Time [s]')
    axs[0].set_ylabel('Pressure [bar]')
    axs[0].set_xlim(0, 1500)

    # pdf.plot(x ='Time  1 - default sample rate CH=1', y='Total Applied Force', ax=axs[1], kind = 'line')
    pdf.plot(x ='Time  1 - default sample rate CH=1', y='Total Ties Tension', ax=axs[1], kind = 'line')
    axs[1].set_title('Ties additional tension')
    axs[1].set_xlabel('Time [s]')
    axs[1].set_ylabel('Force [N]')
    axs[1].set_xlim(0, 1500)
    # pdf.plot(x ='Time  1 - default sample rate CH=1', y='Force_south CH=3', ax=axs[2], kind = 'line')
    # pdf.plot(x ='Time  1 - default sample rate CH=1', y='Force_north CH=4', ax=axs[2], kind = 'line')
    # pdf.plot(x ='Time  1 - default sample rate CH=1', y='TR_south CH=5', ax=axs[2], kind = 'line')
    # pdf.plot(x ='Time  1 - default sample rate CH=1', y='TR_north CH=6', ax=axs[2], kind = 'line')
    # axs[2].set_title('Individual sensors')
    # axs[2].set_xlabel('Time [s]')
    # axs[2].set_ylabel('Force [kN]')

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
    axs[0].legend(["LVDT_NE", "LVDT_NW", "LVDT__ME", "LVDT__MW", "LVDT__SE", "LVDT__SW"])
    axs[0].set_xlim(0, 1500)


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
    axs[1].legend(["LVDT_NE", "LVDT_NW", "LVDT__ME", "LVDT__MW", "LVDT__SE", "LVDT__SW"])
    

    plt.show()



# ******************************************************************************
#   Main
# ******************************************************************************

if __name__ == "__main__":
    from compas_testing import DATA
    from compas_testing.hif import parse_material_results
    from compas_testing.hif import plot_material_results

    input_file = DATA + '/cubes_results/Compressive_Strength.txt'
    [my_info, my_data, my_pd_data, my_test_summary] = parse_material_results(input_file, type='compression')
    # # input_file = DATA + '\\cubes_results\\Double_Punch.txt'
    # # [my_info, my_data, my_pd_data, my_test_summary] = parse_results(input_file, type='double punch')
    # # # print(my_pd_data)
    # # print(my_pd_data)
    # # my_fct = double_pounch(124.3, 150, 150)
    # # print(my_fct)
    # # pdf = my_pd_data[0].cumsum()
    # pdf = my_pd_data[0]
    # fig, ax = plt.subplots()
    # pdf.plot(x ='Extern [mm]', y='Force [kN]', ax=ax, kind = 'line')
    # pdf.plot(x ='Def. 2A [mm]', y='Force [kN]', ax=ax, kind = 'line')
    # pdf.plot(x ='Def. 2B [mm]', y='Force [kN]', ax=ax, kind = 'line')    
    # pdf.plot(x ='Def. 2C [mm]', y='Force [kN]', ax=ax, kind = 'line')
    # ax.set_title = ("Deformation [mm]")
    # with sns.axes_style('white'):
    #     sns.kdeplot(data=pdf['Force [kN]'], shade=True)

    plot_material_results(my_pd_data)
