import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.L03_sensor_handler import temp_sensor as ts
from pivdataprocessor.A02_pltcfg import quickset, getplotpath, generatefiglist, myaxconfig, mycolors

data_folder = './ZZ2_Temperature/02/'
cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']
room_temp = [23.5, 22.5, 20, 20, 20, 22]
files = ['WAVE0001.CSV', 'WAVE0002.CSV', 'WAVE0003.CSV']

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
figtitles = ['temp_center']

ax = axess[0][0]
axconfig = myaxconfig(ax = ax)
axconfig.title = 'Temp-allcase-center'
axconfig.xlable = r'$t$ (s)'
axconfig.ylable = r'$T$ (K)'
axconfig.apply()


step = 0.01
start = -1
t = start + step * np.arange(1000)
# t[100] = 0, t[700] = 6

for k in range(len(cases)):
    tmp = np.zeros((1000,))
    for repeat_id in range(3):
        a = ts(data_folder + cases[k] + '/' + files[repeat_id], environment_temp = room_temp[k],moving_avg_second=0.1)
        f = interp1d(a.time, a.temp+273.15, kind='linear', bounds_error=False, fill_value='extrapolate')
        tmp = tmp + f(t)
    tmp = tmp/3
    ax.plot(t, tmp , label = cases[k], color = mycolors[k])
    mean = tmp[100:700].mean()
    ax.axhline(y = mean, linestyle = '-.' , color = mycolors[k])  
    print(f'{cases[k]},T:{mean}')  


ax.legend()

for fig_number in range(len(figs)):
    fig = figs[fig_number]
    fig.tight_layout()
    fig.savefig(fig_path + '/' + figtitles[fig_number] + figformat, format=figformat[1:])
plt.clf()    