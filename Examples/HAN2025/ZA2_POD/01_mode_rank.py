''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/09  =
=========================
'''

import matplotlib.pyplot as plt
import numpy as np

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.A01_toolbox import float_precsion
from G01_POD import POD

from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist

cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06','Mori465']

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(16), cm_to_inch(9))
# -------------------------------------------------------------------------
# endregion

figtitle = 'mode_rank'
figformat = '.jpg'

fig, ax = plt.subplots(1,1,figsize=figsize_inch)
axconfig = myaxconfig(ax)
axconfig.xlable = r'Mode rank'
axconfig.ylable = r'$Normalized \ \sigma^{2}$'
axconfig.xlim = (0,25)
axconfig.apply()

for case_id in range(len(cases)):
    pod = POD(cases[case_id])
    pod.PODload()

    max_rank = pod.max_rank
    sigma2 = np.zeros((max_rank,), dtype = float_precsion)
    residual = np.zeros((max_rank,), dtype = float_precsion)
        
    for i in range(max_rank):
        sigma2[i] = pod.sigma[i]**2
    sigma2 = sigma2 / np.sum(sigma2)

    ax.plot(list(range(1,max_rank+1)), sigma2, linestyle = 'None', marker = '+', color = mycolors[case_id], label = cases[case_id] )

ax.legend()
fig.savefig(fig_path + '/' + figtitle + figformat, format='jpg')