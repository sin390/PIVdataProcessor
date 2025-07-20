import matplotlib.pyplot as plt
from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.L03_sensor_handler import temp_sensor as ts
from pivdataprocessor.A02_pltcfg import quickset, getplotpath, generatefiglist, myaxconfig, mycolors

data_folder = './ZZ2_Temperature/02/'
cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']
room_temp = [23.5, 22.5, 20, 20, 20, 22]

selected_case = 1
file_folder = data_folder + cases[selected_case] + '/'
# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(16), cm_to_inch(9))
# -------------------------------------------------------------------------
# endregion
figs, axess = generatefiglist(1, 1, 1, figsize_inch)
figformat = '.jpg'
figtitles = [cases[selected_case]]

ax = axess[0]
axconfig = myaxconfig(ax = ax)
axconfig.title = f'temp_{cases[selected_case]}'
axconfig.xlable = r'$t$ (s)'
axconfig.ylable = r'$T$ (K)'
axconfig.apply()

runs = ['WAVE0001.CSV', 'WAVE0002.CSV', 'WAVE0003.CSV']
labels = ['run01', 'run02', 'run03', 'run04', 'run05', 'run06']

styles = [['-','-','-'],['--','--','--']]

for k in range(len(runs)):
    a = ts(file_folder + runs[k], moving_avg_second=0.03,environment_temp = room_temp[selected_case])
    ax.plot(a.time,a.temp+273.15, label = labels[k], color = mycolors[k])

ax.legend()

for fig_number in range(len(figs)):
    fig = figs[fig_number]
    fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_number] + figformat, format='jpg')
plt.clf()    
