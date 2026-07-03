'''
=====================================================
Scientific Figure Utilities for PIV / Turbulence Work
Author:    ChatGPT (supervisor: Zexu HAN)
Version:   1.0
Date:      2026/02/20
=====================================================
'''

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import AutoMinorLocator

class CloudFigure:
    """
    Fixed-canvas colormap figure manager (STRICT FIGSIZE).

    Core rule:
        - NEVER call tight_layout / constrained_layout
        - NEVER save with bbox_inches='tight'
        - All layout is controlled only by:
            * GridSpec (wspace/hspace)
            * fig.subplots_adjust (margins)
            * manually placed axes (colorbar via add_axes)
    """

    def __init__(
        self,
        nrows=1,
        ncols=1,
        figsize=(7, 5),          # cm by default
        figsize_unit="cm",
        dpi=300,
        cmap="turbo",

        # panel label
        panel_fontsize=12,
        panel_offset=(-0.12, 1.05),

        # gridspec spacing
        wspace=0.25,
        hspace=0.25,

        # fixed outer margins (IMPORTANT for panel labels staying in-canvas)
        left=0.14,
        right=0.98,
        bottom=0.14,
        top=0.96,
    ):
        self.nrows = int(nrows)
        self.ncols = int(ncols)

        # ---- figsize to inches (canvas size sacred) ----
        if figsize_unit.lower() in ("cm", "centimeter", "centimeters"):
            figsize_in = (float(figsize[0]) / 2.54, float(figsize[1]) / 2.54)
        elif figsize_unit.lower() in ("in", "inch", "inches"):
            figsize_in = (float(figsize[0]), float(figsize[1]))
        else:
            raise ValueError("figsize_unit must be 'cm' or 'inch'.")

        self.fig = plt.figure(figsize=figsize_in, dpi=int(dpi), constrained_layout=False)
        self.cmap = cmap

        self.panel_offset = panel_offset
        self.panel_fontsize = panel_fontsize

        self.gs = gridspec.GridSpec(
            self.nrows, self.ncols,
            wspace=float(wspace),
            hspace=float(hspace),
            figure=self.fig,
        )

        self.axes = [
            self.fig.add_subplot(self.gs[i, j])
            for i in range(self.nrows)
            for j in range(self.ncols)
        ]

        # store mappables (QuadMesh / AxesImage)
        self.images = [None] * (self.nrows * self.ncols)

        # fixed margins ONCE
        self.fig.subplots_adjust(left=left, right=right, bottom=bottom, top=top)

    # -----------------------------------------------------
    # Targets
    # -----------------------------------------------------
    def ax_target(self, ax_id):
        return self.axes[int(ax_id)]

    # -----------------------------------------------------
    # Outer margins + spacing (safe; does not change figsize)
    # -----------------------------------------------------
    def set_margins(self, left=None, right=None, top=None, bottom=None):
        cur = self.fig.subplotpars
        self.fig.subplots_adjust(
            left=cur.left if left is None else float(left),
            right=cur.right if right is None else float(right),
            bottom=cur.bottom if bottom is None else float(bottom),
            top=cur.top if top is None else float(top),
        )

    def set_spacing(self, wspace=None, hspace=None):
        self.gs.update(
            wspace=self.gs.wspace if wspace is None else float(wspace),
            hspace=self.gs.hspace if hspace is None else float(hspace),
        )

    # -----------------------------------------------------
    # Panel label (a)(b)(c)
    # -----------------------------------------------------
    def set_panel_label(self, index, text=None, bold=False):
        idx = int(index)
        ax = self.axes[idx]
        xoff, yoff = self.panel_offset

        if text is None:
            s = f"({chr(97 + idx)})"
        else:
            s = f"({chr(97 + idx)})" + str(text)

        ax.text(
            xoff, yoff, s,
            transform=ax.transAxes,
            fontsize=self.panel_fontsize,
            fontweight="bold" if bold else "normal",
            ha="left",
            va="bottom",
            clip_on=False,  # keep inside canvas by reserving margins
        )

    # -----------------------------------------------------
    # Axis config
    # -----------------------------------------------------
    def set_axis(
        self,
        index,
        xlim=None,
        ylim=None,
        xlabel=None,
        ylabel=None,
        xticks=None,
        yticks=None,
        subticks=None
    ):
        ax = self.axes[int(index)]
        if xlim is not None: ax.set_xlim(xlim)
        if ylim is not None: ax.set_ylim(ylim)
        if xlabel is not None: ax.set_xlabel(xlabel)
        if ylabel is not None: ax.set_ylabel(ylabel)
        if xticks is not None: ax.set_xticks(xticks)
        if yticks is not None: ax.set_yticks(yticks)
        if subticks is not None:
            ax.xaxis.set_minor_locator(AutoMinorLocator(subticks))
            ax.yaxis.set_minor_locator(AutoMinorLocator(subticks))

    def set_equal_axis(self, index):
        ax = self.axes[int(index)]
        ax.set_aspect("equal", adjustable="box")

    # -----------------------------------------------------
    # Cloud (colormap) panel
    # -----------------------------------------------------
    def add_cloud(
        self,
        index,
        X,
        Y,
        field,
        *,
        vmin=None,
        vmax=None,
        norm=None,

        method="pcolormesh",   # default: pcolormesh (nonuniform OK)
        shading="auto",
        interpolation=None,    # for imshow
        aspect="equal",

        iftran=True,
        rasterized=True,
        zorder=1,
        **kw
    ):
        """
        method:
            - "pcolormesh" (recommended): supports nonuniform grids
            - "imshow": image-like, assumes uniform mapping via extent
        """
        idx = int(index)
        ax = self.axes[idx]

        if iftran:
            X = np.asarray(X).T
            Y = np.asarray(Y).T
            field = np.asarray(field).T
        else:
            X = np.asarray(X)
            Y = np.asarray(Y)
            field = np.asarray(field)

        m = (method or "pcolormesh").lower()

        if m in ("pcolor", "pcolormesh", "mesh"):
            im = ax.pcolormesh(
                X, Y, field,
                cmap=self.cmap,
                shading=shading,
                vmin=vmin,
                vmax=vmax,
                norm=norm,
                zorder=zorder,
                **kw
            )
            if rasterized:
                try:
                    im.set_rasterized(True)
                except Exception:
                    pass

        elif m in ("imshow", "image"):
            im = ax.imshow(
                field,
                extent=[float(X.min()), float(X.max()), float(Y.min()), float(Y.max())],
                origin="lower",
                cmap=self.cmap,
                interpolation=interpolation,
                vmin=vmin,
                vmax=vmax,
                norm=norm,
                aspect="auto",
                zorder=zorder,
                **kw
            )
        else:
            raise ValueError(f"Unknown method={method!r}. Use 'pcolormesh' or 'imshow'.")

        ax.set_aspect(aspect)
        self.images[idx] = im
        return im

    # -----------------------------------------------------
    # Contour overlay
    # -----------------------------------------------------
    def add_contour(
        self,
        index,
        X,
        Y,
        field,
        *,
        levels=10,
        colors="k",
        linewidths=1.0,
        linestyles="solid",
        alpha=1.0,
        iftran=True,
        zorder=8,
        **kw
    ):
        idx = int(index)
        ax = self.axes[idx]

        if iftran:
            X = np.asarray(X).T
            Y = np.asarray(Y).T
            field = np.asarray(field).T

        cs = ax.contour(
            X, Y, field,
            levels=levels,
            colors=colors,
            linewidths=linewidths,
            linestyles=linestyles,
            alpha=alpha,
            zorder=zorder,
            **kw
        )
        return cs

    # -----------------------------------------------------
    # Quiver overlay
    # -----------------------------------------------------
    def add_quiver(
        self,
        index,
        X,
        Y,
        U,
        V,
        *,
        stride=1,
        scale=None,
        color="k",
        width=0.002,
        alpha=0.9,
        zorder=10,
        headwidth=4,
        headlength=6,
        headaxislength=5,
        iftran=True,
        **kw
    ):
        idx = int(index)
        ax = self.axes[idx]

        if iftran:
            X = np.asarray(X).T
            Y = np.asarray(Y).T
            U = np.asarray(U).T
            V = np.asarray(V).T

        if stride is None or int(stride) <= 1:
            ax.quiver(
                X, Y, U, V,
                color=color, scale=scale, width=width, alpha=alpha, zorder=zorder,
                headwidth=headwidth, headlength=headlength, headaxislength=headaxislength,
                **kw
            )
        else:
            s = int(stride)
            ax.quiver(
                X[::s, ::s], Y[::s, ::s],
                U[::s, ::s], V[::s, ::s],
                color=color, scale=scale, width=width, alpha=alpha, zorder=zorder,
                headwidth=headwidth, headlength=headlength, headaxislength=headaxislength,
                **kw
            )

    # -----------------------------------------------------
    # Colorbar (STRICT: manual cax only)
    # -----------------------------------------------------
    def add_colorbar(
        self,
        *,
        mappable_index=0,
        label="",
        orientation="horizontal",
        position=(0.2, 0.1, 0.6, 0.03),  # [left, bottom, width, height]
        fontsize=12,
        label_coords=None,
        ticks=None,
        tick_params=None,
    ):
        """
        Strict global colorbar:
            - uses fig.add_axes(position)
            - does not change GridSpec axes geometry
        """
        im = self.images[int(mappable_index)]
        if im is None:
            raise RuntimeError("No mappable found. Call add_cloud() first.")

        cax = self.fig.add_axes(list(position))
        cbar = self.fig.colorbar(im, cax=cax, orientation=orientation)

        if label:
            cbar.set_label(label, fontsize=fontsize)

        if ticks is not None:
            cbar.set_ticks(ticks)

        if tick_params is not None:
            cbar.ax.tick_params(**tick_params)

        if label_coords is not None:
            if orientation == "horizontal":
                cbar.ax.xaxis.set_label_position("bottom")
                cbar.ax.xaxis.set_label_coords(*label_coords)
            else:
                cbar.ax.yaxis.set_label_position("bottom")
                cbar.ax.yaxis.set_label_coords(*label_coords)

        cbar.ax.minorticks_off()
        return cbar

    # -----------------------------------------------------
    # Save (STRICT SIZE)
    # -----------------------------------------------------
    def save(self, path, dpi=None):
        """
        Strict save:
            - NEVER tight_layout()
            - NEVER bbox_inches='tight'
            -> output size equals figsize canvas exactly.
        """
        valid_exts = {'.png', '.jpg', '.jpeg', '.pdf', '.svg', '.eps', '.tif', '.tiff'}
        root, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext == "":
            ext = ".png"
            path = root + ext
        if ext not in valid_exts:
            raise ValueError(f"Invalid extension '{ext}'. Allowed: {sorted(valid_exts)}")

        folder = os.path.dirname(path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        if ext in {".png", ".jpg", ".jpeg", ".tif", ".tiff"}:
            self.fig.savefig(path, dpi=(self.fig.dpi if dpi is None else int(dpi)))
        else:
            self.fig.savefig(path)

        print(f"[CloudFigure] Saved (strict canvas): {path}")

    def show(self):
        plt.show()


def add_length_line(
    ax,
    x0, y0, L,
    angle_deg=0.0,
    color="w", lw=2.0, ls="-",
    label=None, label_offset=(0.0, 0.0),
    ha="center", va="bottom", zorder=20
):
    """
    Draw a line segment of length L in DATA coordinates.
    Does not affect figure canvas size.
    """
    th = np.deg2rad(angle_deg)
    x1 = x0 + L * np.cos(th)
    y1 = y0 + L * np.sin(th)

    ax.plot([x0, x1], [y0, y1], color=color, lw=lw, ls=ls, zorder=zorder)

    if label is not None:
        xm = 0.5 * (x0 + x1) + label_offset[0]
        ym = 0.5 * (y0 + y1) + label_offset[1]
        ax.text(xm, ym, label, color=color, ha=ha, va=va, zorder=zorder)

    return (x0, y0, x1, y1)
