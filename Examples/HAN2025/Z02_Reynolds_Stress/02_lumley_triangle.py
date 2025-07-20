''' 
=========================
= Author:   HAN Zexu    =
= Version:  1.0         =
= Date:     2025/04/10  =
=========================
'''

import matplotlib.pyplot as plt
import numpy as np

from pivdataprocessor.L01_base import PIVDataProcessorBase as pBase
from pivdataprocessor.A01_toolbox import nanmean_filter2d
from G01_reynolds_stress import ReynoldsStress as RS

from pivdataprocessor.A02_pltcfg import quickset, getplotpath, myaxconfig, mycolors, generatefiglist

cases = ['Case01', 'Case02', 'Case03', 'Case04', 'Case05', 'Case06']

# -------------------------------------------------------------------------
# region
fig_path = getplotpath()
pBase.rm_and_create_directory(fig_path)
quickset()
cm_to_inch = lambda cm: cm / 2.54
figsize_inch = (cm_to_inch(14), cm_to_inch(6))
# -------------------------------------------------------------------------
# endregion

fig_number = 1
figs, axess = generatefiglist(fig_number, 1, 1, figsize_inch)

xlables = [r'$\xi$']
ylables = [r'$\eta$']
figtitles = ['lumley_triangle']
figformat = '.eps'
xlims = [(-0.2,0.4)]
ylims = [(-0.05,0.4)]

markers = ['o', '^']
markersize = [5,4,5]
case_titles = ['Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5', 'Case 6']

for axes_number in range(len(axess)):
    ax = axess[axes_number][0]
    axconfig = myaxconfig(ax = ax)
    # axconfig.title = cases[case_number]
    axconfig.xlable = xlables[axes_number]
    axconfig.ylable = ylables[axes_number]
    axconfig.ylim = ylims[axes_number]
    axconfig.xlim = xlims[axes_number]
    axconfig.apply()
    # ax.set_aspect('equal', adjustable='box')

for case_number in range(len(cases)):
    rs = RS(cases[case_number])
    rs.load()
    invariant_xi = nanmean_filter2d(rs.invariant_xi,kernel_size=8)
    invariant_eta = nanmean_filter2d(rs.invariant_eta,kernel_size=8)

    central_x, central_y = pBase.CaseInfo.Central_Position_Flow
    left,right = pBase.CaseInfo.Effective_Range[0]
    bottom,up = pBase.CaseInfo.Effective_Range[1]

    fig_id = 0
    ax = axess[fig_id][0]

    if case_number == 0:
        ax.plot([0,-1/6],[0,1/6], linestyle = '-', linewidth = 0.5, color = 'k')
        ax.plot([0,1/3],[0,1/3], linestyle = '-', linewidth = 0.5, color = 'k')
        x_2c = np.linspace(-1/6,1/3,100)
        y_2c = np.sqrt(1/27 + 2* (x_2c**3))
        ax.plot(x_2c,y_2c, linestyle = '-', linewidth = 0.5, color = 'k')
        ax.text(0.1/6,-0.02,'iso')
        ax.text(-1/6,1/12,'axi')
        ax.text(0.8/6,1/12,'axi')
        ax.text(1/3,1/3,'1C')
        ax.text(1/12,1.3/6,'2C')

    plotted_x = np.array([0,  30]) + pBase.X[0][central_x,central_y]
    plotted_y = np.array([0,  0 ]) + pBase.X[1][central_x,central_y]
    plotted_x, plotted_y = pBase.pos_mm_to_index_list(plotted_x,plotted_y)
    for loc_ID in range(len(plotted_x)):
        ax.plot(
            invariant_xi[plotted_x[loc_ID], central_y],
            invariant_eta[plotted_x[loc_ID], central_y],
            linestyle='None',
            marker=markers[loc_ID],
            markersize=markersize[loc_ID],  # 建议用 5–7 更清晰
            markerfacecolor='none',  # 中空
            markeredgecolor=mycolors[case_number],  # 用颜色区分 case
            label = case_titles[case_number]
        )


       

from matplotlib.lines import Line2D

# === 构造标题 legend ===
title_handles_col1 = []
title_labels_col1 = []
title_handles_col2 = []
title_labels_col2 = []

title_handle_empty = Line2D([], [], linestyle='None')

# 这里你给了三行标题（3个标头）
title_texts_col1 = [r'$x = x_c$']
title_texts_col2 = [r'$x = x_c + 30~\mathrm{mm}$']

for t1, t2 in zip(title_texts_col1, title_texts_col2):
    title_handles_col1.append(title_handle_empty)
    title_labels_col1.append(t1)
    title_handles_col2.append(title_handle_empty)
    title_labels_col2.append(t2)

# === 构造内容 legend ===
handles_col1 = []
handles_col2 = []
labels_col1 = []
labels_col2 = []

for i, case in enumerate(case_titles):
    color = mycolors[i]

    handle1 = Line2D([], [], color=color,
                     marker=markers[0],
                     linestyle='None',
                     markersize=markersize[0],
                     markerfacecolor='none',
                     markeredgecolor=color)

    handle2 = Line2D([], [], color=color,
                     marker=markers[1],
                     linestyle='None',
                     markersize=markersize[1],
                     markerfacecolor='none',
                     markeredgecolor=color)

    handles_col1.append(handle1)
    handles_col2.append(handle2)
    labels_col1.append(case)
    labels_col2.append(case)

# 合并列（列优先）
legend_handles = handles_col1 + handles_col2
legend_labels = labels_col1 + labels_col2

# 合并标题列
title_handles = title_handles_col1 + title_handles_col2
title_labels = title_labels_col1 + title_labels_col2


# === 绘图部分 ===
for fig_number in range(len(figs)):
    fig = figs[fig_number]
    label_size = 12
    # 先画标题 legend，ncol=2，紧凑排列，位置灵活
    legend_title = fig.legend(
        title_handles,
        title_labels,
        loc='center left',
        bbox_to_anchor=(0.49, 0.85),  # 可以调节这里Y值控制上下位置
        ncol=2,
        fontsize=label_size,
        frameon=False,
        columnspacing=0.8,
        handletextpad=0.3,
        handleheight=1.0
    )
    # 加粗标题文字
    for text in legend_title.get_texts():
        text.set_fontweight('bold')

    # 再画主体 legend
    legend_content = fig.legend(
        legend_handles,
        legend_labels,
        loc='center left',
        bbox_to_anchor=(0.5, 0.5),
        ncol=2,
        fontsize=label_size,
        frameon=False,
        columnspacing=1,
        handletextpad=0.5
    )

    # 必须把标题 legend 添加到图中，否则会被覆盖
    fig.add_artist(legend_title)

    # 调整子图和右边留白
    fig.subplots_adjust(right=0.5, bottom=0.17,left=0.1, top=0.98)
    fig.subplots_adjust(wspace=0.4)

    fig.savefig(fig_path + '/' + figtitles[0] + figformat, format=figformat[1:])

plt.close(fig)