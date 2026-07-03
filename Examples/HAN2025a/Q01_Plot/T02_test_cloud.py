'''
=====================================================
Scientific Figure Utilities for PIV / Turbulence Work
Author:    ChatGPT (supervisor: Zexu HAN)
Version:   1.0
Date:      2026/02/20
=====================================================
'''

import numpy as np
from Q01_Plot.L02_cloud_plot import CloudFigure  
from matplotlib.colors import Normalize

# -------------------------------------------------
# synthetic non-uniform grid (mimic PIV window spacing)
# -------------------------------------------------
nx, ny = 120, 80

x = np.linspace(0, 1.0, nx)**1.3      # 非等距
y = np.linspace(0, 0.6, ny)**1.1
X, Y = np.meshgrid(x, y)

# -------------------------------------------------
# scalar field (e.g. filtered vorticity / |grad u|)
# -------------------------------------------------
field = (
    np.exp(-((X - 0.45)**2 + (Y - 0.30)**2) / 0.01)
    - 0.6 * np.exp(-((X - 0.65)**2 + (Y - 0.35)**2) / 0.02)
)

# vector field (velocity-like)
U =  0.4 * np.cos(2 * np.pi * Y)
V = -0.4 * np.sin(2 * np.pi * X)

# -------------------------------------------------
# colormap & normalization
# -------------------------------------------------
from Q01_Plot.L03_cmap import white_turbo

norm = Normalize(vmin=-1.0, vmax=1.0)

# -------------------------------------------------
# create CloudFigure (STRICT CANVAS)
# -------------------------------------------------
cf = CloudFigure(
    nrows=1,
    ncols=1,
    figsize=(15, 8),        # cm → 论文级物理尺寸
    figsize_unit="cm",
    cmap=white_turbo,

    # margins must be reserved manually
    left=0.14,
    right=0.96,
    bottom=0.16,
    top=0.95,
)

# -------------------------------------------------
# cloud (pcolormesh on nonuniform grid)
# -------------------------------------------------
im = cf.add_cloud(
    index=0,
    X=X,
    Y=Y,
    field=field,
    method="pcolormesh",
    norm=norm,
    shading="auto",
    rasterized=True,    # PDF size friendly
    aspect="equal",
)

# -------------------------------------------------
# contour overlay
# -------------------------------------------------
cf.add_contour(
    index=0,
    X=X,
    Y=Y,
    field=field,
    levels=np.linspace(-0.8, 0.8, 9),
    colors="k",
    linewidths=0.7,
    alpha=0.8,
)

# -------------------------------------------------
# quiver overlay (sparse)
# -------------------------------------------------
cf.add_quiver(
    index=0,
    X=X,
    Y=Y,
    U=U,
    V=V,
    stride=6,           # PIV-style decimation
    scale=15,
    color="k",
    alpha=0.85,
)

# -------------------------------------------------
# axis labels & panel label
# -------------------------------------------------
cf.set_axis(
    index=0,
    xlabel=r"$x/L$",
    ylabel=r"$y/L$",
)

cf.set_panel_label(0)

# -------------------------------------------------
# global colorbar (STRICT: manual axis)
# -------------------------------------------------
cf.add_colorbar(
    mappable_index=0,
    label=r"$\omega^\ast$",
    orientation="horizontal",
    position=(0.25, 0.08, 0.5, 0.035),  # [left, bottom, width, height]
    fontsize=12,
    label_coords=(0.5, -1.6),
)

# -------------------------------------------------
# save (canvas size is sacred)
# -------------------------------------------------
# cf.save("cloud_piv_strict.pdf")
cf.save("cloud_piv_strict.png", dpi=300)
cf.show()
