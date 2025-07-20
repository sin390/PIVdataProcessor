import matplotlib.pyplot as plt
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.L03_sensor_handler import temp_sensor as ts
from pivdataprocessor.A02_pltcfg import quickset, getplotpath, generatefiglist, myaxconfig, mycolors

data_folder = './ZZ2_Temperature/01/'


# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(12), cm_to_inch(6))
# -------------------------------------------------------------------------
# endregion
figs, axess = generatefiglist(1, 1, 1, figsize_inch)
figformat = '.eps'
figtitles = ['temp_5point']

ax = axess[0][0]
axconfig = myaxconfig(ax = ax)
axconfig.xlable = r'$t$ (s)'
axconfig.xlim = (-0.9,10)
axconfig.xticks = [0,2,4,6,8,10]
axconfig.ylable = r'$T$ (K)'
axconfig.apply()

cases = ['WAVE0001.CSV', 'WAVE0002.CSV', 'WAVE0003.CSV', 'WAVE0004.CSV', 'WAVE0005.CSV']
labels = [r'$x = -30$~mm', r'$x = -15$~mm', r'$x = 0$~mm', r'$x = 15$~mm', r'$x = 30$~mm']

styles = [['-','-','-'],['--','--','--']]

for k in range(len(cases)):
    a = ts(data_folder + cases[k], moving_avg_second=0.1)
    ax.plot(a.time,a.temp+273.15, label = labels[k], color = mycolors[k])


for fig_id in range(len(figs)):
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