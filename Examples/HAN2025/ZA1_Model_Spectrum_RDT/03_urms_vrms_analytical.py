import numpy as np
from Q01_Plot.L01_piv_plot import PlotFigure
from Q01_Plot.L00_tools import getplotpath, quickset
from Z08_StructureFunctionTransport.G01_StructureFunctionTransport import StructureFunctionTransport as SFT

quickset()

fig = PlotFigure(
    nrows=1,
    ncols=1,
    figsize=(31, 8),      # cm, physical size is sacred
    figsize_unit="cm",
    panel_fontsize= 20,
    panel_offset=(-0.12,1.05),
    right_legend=False,     # reserve legend column
    left=0.35,
    right=0.65,
    bottom=0.2,
    top=0.95,
    dpi=600,
    wspace=0.35
)

def R_0_to_1(c):
    # 0 < c < 1  ->  b = c^-3 - 1 > 0
    b = c**-3 - 1
    phi = np.arctan(np.sqrt(b)) / np.sqrt(b)
    num = 2*(b+1) * ((1-b)*phi - 1)
    den = (1-b) - (b+1)**2 * phi
    return num/den

def R_gt_1(c):
    # c > 1  ->  k = 1 - c^-3 in (0,1), 用 artanh
    k = 1 - c**-3
    psi = np.arctanh(np.sqrt(k)) / np.sqrt(k)
    num = 2*(1-k) * ((1+k)*psi - 1)
    den = (1+k) - (1-k)**2 * psi
    return num/den

c1 = np.linspace(1.01, 10, 50)   # c > 1
c2 = np.linspace(0.01, 0.99, 50)    # 0 < c < 1
R1 = R_gt_1(c1)
R2 = R_0_to_1(c2)
c_all = np.concatenate((c2, c1))
R_all = np.concatenate((R2, R1))
fig.plot(0, c_all, R_all,  color='k')
fig.set_axis(0, xlim=(0,4), ylim=(0,2.4))
fig.set_label(0, xlabel=r'$c$', ylabel=r'$g(c)$')
fig.save(getplotpath()+"/urms_vrms_analytical.pdf")