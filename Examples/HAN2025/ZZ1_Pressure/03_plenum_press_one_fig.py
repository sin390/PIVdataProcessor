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
# single column, single plot
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(8), cm_to_inch(6))


fig_number = 1
figs, axess = generatefiglist(fig_number, 1, 1, figsize_inch)

xlables = [r'$t$ (s)']
ylables = [r'$p_c$ (kPa)']
figtitles = ['plenum_pressure']
xlims = [(-0.5,10)]
ylims = [(0,500)]
xtricks = [[0,2,4,6,8,10]]
figformat = '.eps'

ax = axess[0][0]
axconfig = myaxconfig(ax = ax)
axconfig.xlable = xlables[0]
axconfig.ylable = ylables[0]
axconfig.xlim = xlims[0]
axconfig.ylim = ylims[0]
axconfig.xticks = xtricks[0]
axconfig.apply()
# -------------------------------------------------------------------------
# endregion

data_folder = './ZZ1_Pressure/01/'
cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']
files = ['20241221_125452_973.CSV',
         '20250215_203716_752.CSV',
         '20250227_181320_623.CSV',
         '20250325_203741_250.CSV',
         '20250319_174844_261.CSV',
         '20250316_152845_627.CSV']


env_press = 102
case_number = 4
left = ps(data_folder+cases[case_number]+'/'+ files[case_number],col = 2) 
right = ps(data_folder+cases[case_number]+'/'+ files[case_number],col = 1) 
axess[0][0].plot(left.time, left.press+ env_press, linestyle = '-', color = mycolors[0], label = fr'left side')
axess[0][0].plot(right.time, right.press+ env_press, linestyle = '-', color = mycolors[1], label = fr'right side')
axess[0][0].axhline(y=285, color='k', dashes=(6, 6), linewidth=0.5)
axess[0][0].axhline(y=315, color='k', dashes=(6, 6), linewidth=0.5)
axess[0][0].axhline(y=151.2, color='k', linestyle='-', linewidth=0.5)


for fig_id in range(fig_number):
    fig = figs[fig_id]
    # handles, labels = [], []
    # for line in axess[fig_id][0].get_lines():
    #     if line.get_label() != '_nolegend_' and not line.get_label().startswith('_child'): 
    #         handles.append(line)
    #         labels.append(line.get_label())
    # fig.subplots_adjust(top = 0.9, left = 0.15, right=0.65,bottom=0.2)
    # fig.subplots_adjust(wspace=0.4, hspace=0.5)
    # fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.67, 0.5), borderaxespad=0)
    fig.subplots_adjust(top = 0.9, left = 0.18, right=0.95,bottom=0.2)   
    ax = axess[fig_id][0]
    ax.legend()
    fig.savefig(fig_path + '/' + figtitles[fig_id] + figformat, format=figformat[1:])
plt.clf()       