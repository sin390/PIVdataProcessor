'''
=====================================================
Scientific Figure Utilities for PIV / Turbulence Work
Author:    ChatGPT (supervisor: Zexu HAN)
Version:   1.0
Date:      2026/02/20
=====================================================
'''

import numpy as np
from Q01_Plot.L01_piv_plot import PlotFigure   # 假设你把类放在 plotfigure.py

# ---------------------------
# synthetic data
# ---------------------------
x = np.logspace(-2, 1, 200)
y1 = x**(-5/3)
y2 = 0.8 * x**(-5/3)
err = 0.15 * y1

# ---------------------------
# create figure (STRICT canvas)
# ---------------------------
fig = PlotFigure(
    nrows=2,
    ncols=2,
    figsize=(18, 14),      # cm, physical size is sacred
    figsize_unit="cm",
    right_legend=True,     # reserve legend column
)

# ---------------------------
# panel (a)
# ---------------------------
fig.plot(
    index=0,
    x=x,
    y=y1,
    yerr=err,
    label=r"$E_{11}$",
    xlog=True,
    ylog=True,
    every=12,              # sparse errorbars
    linewidth=2.0,
)
fig.set_label(0, ylabel=r"$E(k)$")
fig.set_panel_label(0)

# ---------------------------
# panel (b)
# ---------------------------
fig.plot(
    index=1,
    x=x,
    y=y2,
    label=r"$E_{22}$",
    xlog=True,
    ylog=True,
    linestyle="--",
    linewidth=2.0,
)
fig.set_panel_label(1)

# ---------------------------
# panel (c): shaded uncertainty
# ---------------------------
fig.shade(
    index=2,
    x=x,
    y=y1,
    yerr=0.25 * y1,
    label=r"$E_{11}\pm\sigma$",
    xlog=True,
    ylog=True,
)
fig.set_label(2, xlabel=r"$k\eta$", ylabel=r"$E(k)$")
fig.set_panel_label(2)

# ---------------------------
# panel (d): comparison
# ---------------------------
fig.plot(
    index=3,
    x=x,
    y=y1,
    label="case A",
    xlog=True,
    ylog=True,
    linewidth=1.8,
)
fig.plot(
    index=3,
    x=x,
    y=y2,
    label="case B",
    xlog=True,
    ylog=True,
    linestyle="--",
)
fig.set_label(3, xlabel=r"$k\eta$")
fig.set_panel_label(3)

# ---------------------------
# legend (ONLY in reserved column)
# ---------------------------
fig.legend()

# ---------------------------
# save & show
# ---------------------------
fig.save("demo_strict_canvas.pdf")
fig.save("demo_strict_canvas.png", dpi=300)
fig.show()
