''' 
=========================
= Author:   Claude      =
= Supervisor: HAN Zexu  =
= Version:  1.0         =
= Date:     2026/07/22  =
=========================

Reproduces the style of Fig. in Valente & Vassilicos (2015):
    (a) Pi_u', Pi_<u> normalised by u_rms^3/L_u, vs r/L_u
    (b) Pi_v', Pi_<v> normalised by v_rms^3/L_v, vs r/L_v

Case04 only. Error bars are |even - odd|, where 'Case04_even'/'Case04_odd'
have already been computed and saved separately (via StructureFunctionTransport
on those two sub-cases) -- here we just load() + differentiate() them.

Normalisation constants (L_u, L_v, u_rms, v_rms) are NOT computed
automatically here -- set them by hand below.

Only the points whose r/L falls inside r_range_u / r_range_v are plotted
(found by index, not just an axis xlim clip).
'''

import numpy as np
from Q01_Plot.L01_piv_plot import PlotFigure
from Q01_Plot.L00_tools import getplotpath, quickset
from Z08_StructureFunctionTransport.G01_StructureFunctionTransport import StructureFunctionTransport as SFT

quickset()

# =====================================================================
# manually specified normalisation constants -- fill these in by hand
# =====================================================================
L_u = 27.62   # mm,   integral length scale for the x-direction (u)
L_v = 22.27    # mm,   integral length scale for the y-direction (v)
u_rms = 16.63     # same velocity unit as pBase.fluc_U, e.g. m/s
v_rms = 11.36    # same velocity unit as pBase.fluc_U, e.g. m/s

L_u = 28.11   # mm,   integral length scale for the x-direction (u)
L_v = 17.84    # mm,   integral length scale for the y-direction (v)
u_rms = 28.87     # same velocity unit as pBase.fluc_U, e.g. m/s
v_rms = 18.60    # same velocity unit as pBase.fluc_U, e.g. m/s
# =====================================================================

# =====================================================================
# dimensionless r/L range to actually plot, specified separately per
# direction (panel a uses r_range_u, panel b uses r_range_v)
# =====================================================================
r_range_u = (0.1, 0.9)
r_range_v = (0.1, 0.9)
# =====================================================================

case = 'Case04'

sft = SFT(case)
sft.load()
sft.differentiate()

sft_even = SFT(case + '_even')
sft_even.load()
sft_even.differentiate()

sft_odd = SFT(case + '_odd')
sft_odd.load()
sft_odd.differentiate()

# error bars defined as |even - odd|
err_uprime = np.abs(sft_even.Pi_uprime - sft_odd.Pi_uprime)
err_meanu = np.abs(sft_even.Pi_meanu - sft_odd.Pi_meanu)
err_vprime = np.abs(sft_even.Pi_vprime - sft_odd.Pi_vprime)
err_meanv = np.abs(sft_even.Pi_meanv - sft_odd.Pi_meanv)

# normalisation
norm_u = u_rms**3 / L_u
norm_v = v_rms**3 / L_v

r_over_Lu = sft.r_xdir / L_u
r_over_Lv = sft.r_ydir / L_v

Pi_uprime_n = sft.Pi_uprime / norm_u
Pi_meanu_n = sft.Pi_meanu / norm_u
err_uprime_n = err_uprime / norm_u
err_meanu_n = err_meanu / norm_u

Pi_vprime_n = sft.Pi_vprime / norm_v
Pi_meanv_n = sft.Pi_meanv / norm_v
err_vprime_n = err_vprime / norm_v
err_meanv_n = err_meanv / norm_v

# =====================================================================
# select only the points whose r/L lies inside r_range_u / r_range_v
# =====================================================================
idx_u = np.where((r_over_Lu >= r_range_u[0]) & (r_over_Lu <= r_range_u[1]))[0]
idx_v = np.where((r_over_Lv >= r_range_v[0]) & (r_over_Lv <= r_range_v[1]))[0]

r_over_Lu_plot = r_over_Lu[idx_u]
Pi_uprime_n_plot = Pi_uprime_n[idx_u]
Pi_meanu_n_plot = Pi_meanu_n[idx_u]
err_uprime_n_plot = err_uprime_n[idx_u]
err_meanu_n_plot = err_meanu_n[idx_u]

r_over_Lv_plot = r_over_Lv[idx_v]
Pi_vprime_n_plot = Pi_vprime_n[idx_v]
Pi_meanv_n_plot = Pi_meanv_n[idx_v]
err_vprime_n_plot = err_vprime_n[idx_v]
err_meanv_n_plot = err_meanv_n[idx_v]

# =====================================================================
# figure
# =====================================================================
nrows = 1
ncols = 2
fig = PlotFigure(
    nrows=1,
    ncols=2,
    figsize=(31, 9),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.12,1.05),
    right_legend=False,     # reserve legend column
    left=0.15,
    right=0.9,
    bottom=0.19,
    top=0.88,
    dpi=600,
    wspace=0.35
)


every = 2  # sparse errorbar spacing, adjust as needed
marker_size = 6
fig_id = 0
fig.plot(fig_id, r_over_Lu_plot, Pi_meanu_n_plot, yerr=err_meanu_n_plot/2, every=every,
          color='r', marker='^', ifmarker=True, markerfacecolor='white',
          markersize = marker_size, label=r"$\Pi_{\langle U \rangle}$")
fig.plot(fig_id, r_over_Lu_plot, Pi_uprime_n_plot, yerr=err_uprime_n_plot/2, every=every,
          color='b', marker='o', ifmarker=True, markerfacecolor='white',
          markersize = marker_size, label=r"$\Pi_{u}$")
fig.get_ax(fig_id).axhline(0, color='k', linewidth=0.5)

fig_id = 1
fig.plot(fig_id, r_over_Lv_plot, Pi_meanv_n_plot, yerr=err_meanv_n_plot, every=every,
          color='r', marker='^', ifmarker=True, markerfacecolor='white',
          markersize = marker_size, label=r"$\Pi_{\langle V \rangle}$")
fig.plot(fig_id, r_over_Lv_plot, Pi_vprime_n_plot, yerr=err_vprime_n_plot, every=every,
          color='b', marker='o', ifmarker=True, markerfacecolor='white',
          markersize = marker_size, label=r"$\Pi_{v}$")
fig.get_ax(fig_id).axhline(0, color='k', linewidth=0.5)

fig.set_axis(0, xlim=(0,1), ylim=(-1,2))
fig.set_axis(1, xlim=(0,1), ylim=(-1.6,1.6))
fig.set_label(0, xlabel=r'$r/L_u$', ylabel=r'$\Pi/(u_\mathrm{rms}^3L_u)$')
fig.set_label(1, xlabel=r'$r/L_v$', ylabel=r'$\Pi/(v_\mathrm{rms}^3L_v)$')
fig.add_legend_inside(handlelength=0,fontsize=18,loc='upper left')
for fig_id in range(2):
    fig.set_panel_label(fig_id)

# fig.set_margins(left=0.1,right=0.95,bottom=0.3,top=0.85)
fig.save(getplotpath()+"/structure_function_transport.pdf")