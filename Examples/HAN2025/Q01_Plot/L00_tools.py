'''
=====================================================
Scientific Figure Utilities for PIV / Turbulence Work
Author:    ChatGPT (supervisor: Zexu HAN)
Version:   1.0
Date:      2025/12/05
=====================================================
'''
import os,shutil
import numpy as np
import inspect
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def quickset():
    """
    Final paper-style settings matching the example figure:
    - Matplotlib built-in fonts only (no findfont issues)
    - Serif + math fully consistent
    - Font sizes and line widths matched to the example wide figure
    """
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        # ---------------------------
        # DPI (match the example image)
        # ---------------------------
        "figure.dpi": 300,
        "savefig.dpi": 300,
        'text.usetex': True,
        # ---------------------------
        # Fonts (built-in, fully safe)
        # ---------------------------
        "font.family": "STIXGeneral",
        "mathtext.fontset": "stix",
        "text.latex.preamble": r"""
            \usepackage{newtxtext}
            \usepackage{newtxmath}
        """,
        # ---------------------------
        # Font sizes (visually matched to your example)
        # ---------------------------
        "font.size": 18,        # base
        "axes.labelsize": 18,   # axis labels
        "xtick.labelsize": 18,
        "ytick.labelsize": 18,
        "legend.fontsize": 18,

        # ---------------------------
        # Lines and spines
        # ---------------------------
        "lines.linewidth": 1.2,
        "lines.markersize": 3,
        "axes.linewidth": 0.8,

        # ---------------------------
        # Ticks (thickness + length)
        # ---------------------------
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "xtick.major.size": 6,
        "ytick.major.size": 6,

        "xtick.minor.width": 0.8,
        "ytick.minor.width": 0.8,
        "xtick.minor.size": 3.5,
        "ytick.minor.size": 3.5,

        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.top": True,
        "ytick.right": True,
        "xtick.minor.visible": True,
        "ytick.minor.visible": True,
        "xtick.major.pad": 8.0,
        "ytick.major.pad": 8.0,
        "xtick.minor.pad": 8.0,
        "ytick.minor.pad": 8.0,
        # ---------------------------
        # Legend / formatter
        # ---------------------------
        "legend.frameon": False,
        "legend.handlelength": 2.5,
        "legend.handletextpad": 0.6,
        "axes.formatter.use_mathtext": True,

        # ---------------------------
        # PDF / PS embedding (journal-safe)
        # ---------------------------
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def getplotpath(plot_foldername = '/S02_Plots') -> str:
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    current_file_path = os.path.abspath(module.__file__)
    c_file_path, c_file_name = os.path.split(current_file_path) 

    cwd = os.getcwd()
    c_relative_path = os.path.relpath(c_file_path, start=cwd)
    
    plot_path = cwd + plot_foldername + '/' + c_relative_path + '/' + c_file_name[:-3]
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)
    return plot_path

def rm_and_create_directory(path_to_directory:str, ifcreate = True) -> None:
    if os.path.exists(path_to_directory):
        shutil.rmtree(path_to_directory)
    if ifcreate == True:
        os.makedirs(path_to_directory)  