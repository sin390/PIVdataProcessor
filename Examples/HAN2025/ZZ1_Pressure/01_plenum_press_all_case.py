import matplotlib.pyplot as plt

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.L03_sensor_handler import press_sensor_PSE540 as ps
from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist

data_folder = './ZZ1_Pressure/01/'
cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']
files = ['20241221_125452_973.CSV',
         '20250215_203716_752.CSV',
         '20250227_181320_623.CSV',
         '20250325_203741_250.CSV',
         '20250319_174844_261.CSV',
         '20250316_152845_627.CSV']

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(33), cm_to_inch(19))
# -------------------------------------------------------------------------
# endregion

fig_number = 1
figs, axess = generatefiglist(fig_number, 2, 3, figsize_inch)
env_press = 102

xlables = [r'$t$ (s)']
ylables = [r'$p$ (kPa)']
figtitles = ['plenum_pressure']
xlims = [(-0.5,10)]
ylims = [(100,400)]
figformat = '.jpg'

for i in range(2):
    for j in range(3):
        case_number = i*3+j
        for axes_number in range(len(axess)):
            ax = axess[axes_number][case_number]
            axconfig = myaxconfig(ax = ax)
            axconfig.title = cases[case_number]
            axconfig.xlable = xlables[axes_number]
            axconfig.ylable = ylables[axes_number]
            axconfig.xlim = xlims[axes_number]
            axconfig.ylim = ylims[axes_number]
            axconfig.apply()
        left = ps(data_folder+cases[case_number]+'/'+ files[case_number],col = 2) 
        right = ps(data_folder+cases[case_number]+'/'+ files[case_number],col = 1) 
        axess[0][case_number].plot(left.time, left.press+ env_press, linestyle = '-', color = mycolors[0], label = fr'left side')
        axess[0][case_number].plot(right.time, right.press+ env_press, linestyle = '-', color = mycolors[1], label = fr'right side')
        axess[0][case_number].axhline(y=285, color='k', linestyle='--', linewidth=0.5)
        axess[0][case_number].axhline(y=315, color='k', linestyle='--', linewidth=0.5)
        axess[0][case_number].axhline(y=151.2, color='k', linestyle='-', linewidth=0.5)


for fig_id in range(fig_number):
    for ax in axess[fig_id]:
        ax.legend()
    fig = figs[fig_id]
    fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_id] + figformat, format='jpg')
plt.clf() 