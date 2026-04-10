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
from matplotlib.ticker import MultipleLocator, LogLocator

class PlotFigure:
    """
    Fixed-canvas-size figure manager (PIV / turbulence).

    Core rule:
        - NEVER call tight_layout / constrained_layout
        - NEVER save with bbox_inches='tight'
        - All geometry is controlled only by subplots_adjust + GridSpec params
        -> output physical size is strictly the figsize canvas.
    """

    default_colors = [
        "#e41a1c", "#377eb8", "#4daf4a", "#ff7f00",
        "#984ea3", "#f781bf", "#a65628", "#999999",
        "#dede00", "#17becf", "#324918"
    ]
    default_markers = ["o", "s", "^", "D", "v", "P", "*", "X", "<", ">"]

    def __init__(
        self,
        nrows=1,
        ncols=1,
        figsize=(7, 5),
        figsize_unit="cm",
        dpi=300,

        # GridSpec spacing
        wspace=0.25,
        hspace=0.32,

        # Outer margins (THE ONLY place to guarantee panel labels stay inside)
        left=0.14,
        right=None,
        bottom=0.14,
        top=0.96,

        # Right legend column
        right_legend=False,
        legend_col_ratio=0.15,

        # Panel labels
        panel_fontsize=12,
        panel_offset=(-0.12, 1.02),
    ):
        self.nrows = int(nrows)
        self.ncols = int(ncols)
        self.right_legend = bool(right_legend)

        self.panel_fontsize = panel_fontsize
        self.panel_offset = panel_offset
        self.dpi = int(dpi)

        # --- figsize to inches (canvas size is sacred) ---
        if figsize_unit.lower() in ("cm", "centimeter", "centimeters"):
            figsize_in = (float(figsize[0]) / 2.54, float(figsize[1]) / 2.54)
        elif figsize_unit.lower() in ("in", "inch", "inches"):
            figsize_in = (float(figsize[0]), float(figsize[1]))
        else:
            raise ValueError("figsize_unit must be 'cm' or 'inch'.")

        # IMPORTANT: disable any auto-layout
        self.fig = plt.figure(figsize=figsize_in, dpi=self.dpi, constrained_layout=False)

        # --- GridSpec ---
        total_cols = self.ncols + (1 if self.right_legend else 0)
        width_ratios = [1.0] * self.ncols + ([float(legend_col_ratio)] if self.right_legend else [])

        self.gs = gridspec.GridSpec(
            self.nrows,
            total_cols,
            width_ratios=width_ratios,
            wspace=float(wspace),
            hspace=float(hspace),
            figure=self.fig,
        )

        # --- axes grid ---
        self.axes = []
        for i in range(self.nrows):
            row = []
            for j in range(self.ncols):
                row.append(self.fig.add_subplot(self.gs[i, j]))
            self.axes.append(row)

        # --- legend axis (reserved column) ---
        if self.right_legend:
            self.ax_legend = self.fig.add_subplot(self.gs[:, -1])
            self.ax_legend.axis("off")
        else:
            self.ax_legend = None

        # --- fixed margins (do this ONCE) ---
        if right is None:
            right = 0.97 if self.right_legend else 0.98
        self.fig.subplots_adjust(left=left, right=right, bottom=bottom, top=top)

        # legend storage
        self.legend_handles = []
        self.legend_labels = []

        # style cycles
        self._ci = 0
        self._mi = 0

    # -------------------------
    # internal helpers
    # -------------------------
    def _ax(self, index: int):
        r = index // self.ncols
        c = index % self.ncols
        return self.axes[r][c]

    def _next_color(self):
        c = self.default_colors[self._ci % len(self.default_colors)]
        self._ci += 1
        return c

    def _next_marker(self):
        m = self.default_markers[self._mi % len(self.default_markers)]
        self._mi += 1
        return m

    # -------------------------
    # geometry (safe to adjust)
    # -------------------------
    def set_margins(self, left=None, right=None, bottom=None, top=None):
        cur = self.fig.subplotpars
        self.fig.subplots_adjust(
            left=cur.left if left is None else float(left),
            right=cur.right if right is None else float(right),
            bottom=cur.bottom if bottom is None else float(bottom),
            top=cur.top if top is None else float(top),
        )

    # -------------------------
    # plotting (unified)
    # -------------------------
    def plot(
        self,
        index,
        x,
        y,
        *,
        yerr=None,
        xerr=None,
        label=None,
        color=None,
        marker=None,
        ifmarker=False,
        xlog=False,
        ylog=False,

        # errorbar density control
        every=1,
        indices=None,

        # errorbar styles
        capsize=2.5,
        elinewidth=None,
        capthick=None,

        # line style
        **kw
    ):
        """
        Draw line for all points; optionally draw errorbars only at sparse indices.

        If yerr/xerr provided:
            - line: always full
            - errorbars: only at indices or every=...
        """
        ax = self._ax(index)

        x = np.asarray(x)
        y = np.asarray(y)

        color = self._next_color() if color is None else color
        marker = (self._next_marker() if marker is None else marker) if ifmarker else None

        # full line
        ln, = ax.plot(x, y, color=color, marker=marker, label=label, **kw)

        # sparse errorbars
        if (yerr is not None) or (xerr is not None):
            if indices is not None:
                idx = np.asarray(indices, dtype=int)
            else:
                every = max(int(every), 1)
                idx = np.arange(0, len(x), every)

            xe, ye = x[idx], y[idx]
            ye_err = None if yerr is None else np.asarray(yerr)[idx]
            xe_err = None if xerr is None else np.asarray(xerr)[idx]

            ax.errorbar(
                xe, ye,
                yerr=ye_err,
                xerr=xe_err,
                color=color,
                linestyle="none",
                marker=None,
                capsize=capsize,
                elinewidth=elinewidth,
                capthick=capthick,
                zorder=ln.get_zorder() - 0.1
            )

        # legend collection
        if label:
            self.legend_handles.append(ln)
            self.legend_labels.append(label)

        if xlog:
            ax.set_xscale("log")
        if ylog:
            ax.set_yscale("log")

        return ln

    def shade(
        self,
        index,
        x,
        y,
        *,
        yerr=None,
        y_low=None,
        y_high=None,
        label=None,
        color=None,
        xlog=False,
        ylog=False,
        fill_alpha=0.25,
        draw_center=True,
        center_lw=1.8,
        center_ls="-",
        draw_boundary=False,
        boundary_lw=0.8,
        boundary_ls="--",
        zorder_fill=1,
        zorder_boundary=2,
        zorder_center=3,
    ):
        ax = self._ax(index)
        x = np.asarray(x)
        y = np.asarray(y)

        color = self._next_color() if color is None else color

        if (y_low is None) ^ (y_high is None):
            raise ValueError("y_low and y_high must be both provided or both None.")
        if y_low is None:
            if yerr is None:
                raise ValueError("Provide yerr or (y_low, y_high).")
            y_low = y - np.asarray(yerr)
            y_high = y + np.asarray(yerr)
        else:
            y_low = np.asarray(y_low)
            y_high = np.asarray(y_high)

        band = ax.fill_between(
            x, y_low, y_high,
            color=color, alpha=fill_alpha, linewidth=0,
            zorder=zorder_fill
        )

        bnd_lo = bnd_hi = None
        if draw_boundary:
            bnd_lo, = ax.plot(x, y_low, color=color, lw=boundary_lw, ls=boundary_ls, zorder=zorder_boundary)
            bnd_hi, = ax.plot(x, y_high, color=color, lw=boundary_lw, ls=boundary_ls, zorder=zorder_boundary)

        ln = None
        if draw_center:
            ln, = ax.plot(x, y, color=color, lw=center_lw, ls=center_ls, zorder=zorder_center)

        if label:
            self.legend_handles.append(ln if ln is not None else band)
            self.legend_labels.append(label)

        if xlog:
            ax.set_xscale("log")
        if ylog:
            ax.set_yscale("log")

        return band, ln, (bnd_lo, bnd_hi)

    # -------------------------
    # axis configuration
    # -------------------------
    def set_axis(
        self,
        index,
        *,
        xlog=False,
        ylog=False,
        xlim=None,
        ylim=None,
        xticks=None,
        yticks=None,
        minor_xticks=None,
        minor_yticks=None,
    ):
        ax = self._ax(index)

        if xlog:
            ax.set_xscale("log")
        if ylog:
            ax.set_yscale("log")

        if xlim is not None:
            ax.set_xlim(xlim)
        if ylim is not None:
            ax.set_ylim(ylim)

        if xticks is not None:
            ax.set_xticks(xticks)
        if yticks is not None:
            ax.set_yticks(yticks)

        # minor ticks
        if minor_xticks is not None:
            if not xlog:
                ax.xaxis.set_minor_locator(MultipleLocator(minor_xticks))
            else:
                ax.xaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * 0.1))

        if minor_yticks is not None:
            if not ylog:
                ax.yaxis.set_minor_locator(MultipleLocator(minor_yticks))
            else:
                ax.yaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * 0.1))

    def set_label(
        self,
        index,
        *,
        xlabel=None,
        ylabel=None,
        fontsize=None,
        labelpad=None,
    ):
        ax = self._ax(index)

        kw = {}
        if fontsize is not None:
            kw["fontsize"] = fontsize
        if labelpad is not None:
            kw["labelpad"] = labelpad

        if xlabel is not None:
            ax.set_xlabel(xlabel, **kw)
        if ylabel is not None:
            ax.set_ylabel(ylabel, **kw)

    # -------------------------
    # panel labels
    # -------------------------
    def set_panel_label(self, index, text=None, bold=True):
        ax = self._ax(index)
        xoff, yoff = self.panel_offset

        if text is None:
            s = f"({chr(97 + index)})"
        else:
            s = f"({chr(97 + index)}){text}"

        ax.text(
            xoff, yoff, s,
            transform=ax.transAxes,
            fontsize=self.panel_fontsize,
            fontweight="bold" if bold else "normal",
            ha="left", va="bottom",
            clip_on=False  # rely on reserved margins (fixed)
        )

    # -------------------------
    # legend
    # -------------------------
    def legend(
        self,
        loc="center left",
        bbox_to_anchor=None,
        handlelength=2.5,
        handletextpad=0.6,
        labelspacing=0.4,
        fontsize=None,
    ):
        """
        Deterministic legend.

        Parameters
        ----------
        loc : str
            Legend location inside ax_legend (default: 'center left').
        bbox_to_anchor : tuple or None
            Fine control of legend position in ax_legend coordinates.
            Example: (0.0, 1.0) with loc='upper left'.
        handlelength : float
            Length of legend handles.
        handletextpad : float
            Spacing between handle and text.
        labelspacing : float
            Vertical spacing between legend entries.
        fontsize : float or None
            Legend font size.
        """
        if not self.legend_handles:
            return

        if self.right_legend and (self.ax_legend is not None):
            self.ax_legend.cla()
            self.ax_legend.axis("off")

            self.ax_legend.legend(
                self.legend_handles,
                self.legend_labels,
                loc=loc,
                bbox_to_anchor=bbox_to_anchor,
                frameon=False,
                borderaxespad=0.0,
                handlelength=handlelength,
                handletextpad=handletextpad,
                labelspacing=labelspacing,
                fontsize=fontsize,
            )

    def add_legend_inside(self, loc="best", handlelength=2.5, fontsize=9):
        for r in range(self.nrows):
            for c in range(self.ncols):
                self.axes[r][c].legend(
                    loc=loc,
                    handlelength=handlelength,
                    fontsize=fontsize,
                    frameon=False
                )

    def add_legend_bottom_rowmajor_manual(
        self,
        *,
        ncol=4,
        x=0.5,
        y=0.03,
        xpad=0.06,
        ypad=0.05,
        handlelength=0.04,
        textpad=0.01,
        linewidth=1.5,
        fontsize=9,
    ):
        """
        Manually draw a row-major legend with global (x, y) anchor
        in figure coordinates.
        """
        handles = self.legend_handles
        labels  = self.legend_labels
        n = len(handles)
        if n == 0:
            return

        fig = self.fig

        # 以 (x, y) 为“第一行中心”
        x0 = x - (ncol - 1) * xpad / 2
        y0 = y

        for i, (h, lab) in enumerate(zip(handles, labels)):
            r = i // ncol   # 行优先
            c = i % ncol

            xx = x0 + c * xpad
            yy = y0 - r * ypad

            # legend 线段
            fig.lines.append(
                h.__class__(
                    [xx - handlelength, xx],
                    [yy, yy],
                    transform=fig.transFigure,
                    color=h.get_color(),
                    linestyle=h.get_linestyle(),
                    linewidth=linewidth
                )
            )

            # legend 文本
            fig.text(
                xx + textpad, yy,
                lab,
                ha="left",
                va="center",
                fontsize=fontsize
            )

    # -------------------------
    # save/show (STRICT SIZE)
    # -------------------------
    def save(self, path, *, dpi=None):
        """
        Strict save:
            - NEVER bbox_inches='tight'
            - NEVER tight_layout()
            -> output physical size is exactly figsize canvas.
        """
        valid_exts = {'.png', '.jpg', '.jpeg', '.pdf', '.svg', '.eps', '.tif', '.tiff'}
        root, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext == "":
            ext = ".png"
            path = root + ext
        if ext not in valid_exts:
            raise ValueError(f"Unsupported extension '{ext}'. Supported: {sorted(valid_exts)}")

        folder = os.path.dirname(path)
        if folder and (not os.path.exists(folder)):
            os.makedirs(folder)

        dpi_to_use = self.dpi if dpi is None else int(dpi)

        # Vector formats ignore dpi in geometry; raster uses dpi for pixel resolution only.
        if ext in {'.png', '.jpg', '.jpeg', '.tif', '.tiff'}:
            self.fig.savefig(path, dpi=dpi_to_use)  # bbox default None -> strict
        else:
            self.fig.savefig(path)  # strict

    def show(self):
        plt.show()
