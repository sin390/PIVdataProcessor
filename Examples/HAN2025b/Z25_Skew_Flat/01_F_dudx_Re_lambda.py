''' 
=========================
= Author:   HAN Zexu    =
= Powered by ChatGPT    =
= Version:  1.0         =
= Date:     2026/02/07  =
=========================
'''
from Q01_Plot.L01_piv_plot import PlotFigure
from Q01_Plot.L00_tools import getplotpath, quickset
from Q01_Plot.C00_cfg_for_cases import colors, linewidths

import numpy as np
import pandas as pd
from Z25_Skew_Flat.G02_SkewFlat_dudx import SkewFlat as SF2
from ZZZ_Result_Manager.G01_result_manager import ResultManager as RM
from ZZZ_Result_Manager.A01_cases import cases, cases_f, cases_w
from Z11_Dissipation_Rate.G01_dissipation_rate import DissipationRate as DS

ref_dir = './Z25_Skew_Flat/ref'
refs = ['Antonia','Kerr','Kuo','Mi','Sreenivasan','Van']
ref_markers = ['o','s','^','v','x','+']
ref_colors = ['k','k','k','k','k','k']
labels = [
    'Antonia and Chambers',
    'Kerr',
    'Kuo and Corrsin',
    'Mi et al.',
    'Sreenivasan & Antonia',
    'Van Atta & Antonia'
]

class XYCSV:
    """
    Simple interface for accessing x-y data from a CSV file.

    Attributes
    ----------
    x : ndarray
        x-axis data
    y : ndarray
        y-axis data
    label : str
        label for plotting or identification
    """

    def __init__(self, csv_path, x_col=0, y_col=1, label=None):
        self.csv_path = csv_path

        df = pd.read_csv(csv_path,skiprows=-1)

        self.x = df.iloc[:, x_col].to_numpy()
        self.y = df.iloc[:, y_col].to_numpy()
        self.label = label

quickset()
nrows = 1
ncols = 1
fig = PlotFigure(nrows=nrows, ncols=ncols, figsize=(8,4), right_legend=True, hspace=0.5, wspace=0.5, panel_offset=(-0.2,1.1))
','

fig_id = 0
for ref_id, ref in enumerate(refs):
    file = ref_dir+f'/{ref}.csv'
    csv = XYCSV(file)
    fig.plot(fig_id,csv.x,csv.y, color=ref_colors[ref_id], 
             label=labels[ref_id],marker=ref_markers[ref_id],ifmarker=True,linestyle = 'None',markerfacecolor = 'none')

x=[]
y=[]
for case in cases_f+cases_w:
    sf2 = SF2(case,'gaussian',-1)
    ds = DS(case,'gaussian',-1)
    f_dudx = sf2.result_json.get(0)['avg_F_dudx']
    Re_x = ds.result_json.get(0)['Re_lambda_x']
    x.append(Re_x)
    y.append(f_dudx)
fig.plot(fig_id,x,y, color=colors[0], marker='*',ifmarker=True,linestyle = 'None',label='Present study')



fig.set_axis(0,xlim=(1,50000),ylim=(1,200),xlog=True,ylog=True)
fig.set_label(0,ylabel=r'$F_{(\partial u/\partial x)}$')
fig.set_label(0,xlabel=r'$Re_\lambda$')

fig.set_margins(right=0.85)
fig.legend(bbox_to_anchor=(0.7,0.5))
fig.save(getplotpath()+"/F_dudx_Re_lambda.png")