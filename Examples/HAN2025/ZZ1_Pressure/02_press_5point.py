import matplotlib.pyplot as plt
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.L03_sensor_handler import press_sensor_PSE543 as ps
from pivdataprocessor.A02_pltcfg import quickset, getplotpath, generatefiglist, myaxconfig, mycolors

data_folder = './ZZ1_Pressure/02/'


# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(12), cm_to_inch(6))
# -------------------------------------------------------------------------
# endregion
fig_number = 1
figs, axess = generatefiglist(fig_number, 1, 1, figsize_inch)
figformat = '.eps'
figtitles = ['press_4point']

ax = axess[0][0]
axconfig = myaxconfig(ax = ax)
axconfig.xlable = r'$t$ (s)'
axconfig.ylable = r'Gauge pressure (Pa)'
axconfig.xlim = (-1,10)
axconfig.xticks = [0,2,4,6,8,10]
axconfig.apply()

cases = ['20250207_150454_070.CSV', '20250207_153525_513.CSV', '20250207_160409_049.CSV',
         '20250207_163540_728.CSV', '20250207_170715_558.CSV', '20250207_173646_341.CSV']
labels = [r'$x = 6.5$~mm', r'$x = 21.5$~mm', r'$x = 36.5$~mm', r'$x = -36.5$~mm', r'$x = -21.5$~mm', r'$x = -6.5$~mm']

zero_pos = [2.6,2.9,2.2,4.8,2.6,2.4]
env_press = 0


for k in [3,5,0,2]:
    a = ps(data_folder + cases[k],zero_pos=zero_pos[k])
    ax.plot(a.time,a.press*1000+env_press, label = labels[k], color = mycolors[k])


for fig_id in range(fig_number):
    fig = figs[fig_id]
    handles, labels = [], []
    for line in axess[fig_id][0].get_lines():
        if line.get_label() != '_nolegend_' and not line.get_label().startswith('_child'): 
            handles.append(line)
            labels.append(line.get_label())
    fig.subplots_adjust(top = 0.9, left = 0.15, right=0.65,bottom=0.2)
    fig.subplots_adjust(wspace=0.4, hspace=0.5)
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(0.67, 0.5), borderaxespad=0)
    fig = figs[fig_id]
    fig.savefig(fig_path + '/' + figtitles[fig_id] + figformat, format=figformat[1:])
plt.clf()       