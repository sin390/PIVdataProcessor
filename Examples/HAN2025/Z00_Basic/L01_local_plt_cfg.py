import matplotlib.pyplot as plt

def quickset():
    plt.rcParams.update({
    'text.usetex': True,
    'font.family': 'serif',
    'font.serif': ['Computer Modern'], 
    'font.size': 12,

    'lines.linewidth': 1.0,

    'figure.dpi': 300,
    'savefig.dpi': 600,

    'axes.linewidth': 0.5,
    'axes.labelsize': 12,
    'axes.titlesize': 12,

    'xtick.labelsize': 10,
    'ytick.labelsize': 10, 
    'xtick.top': True,
    'xtick.bottom': True,
    'ytick.left': True,
    'ytick.right': True,
    'xtick.direction': 'in',
    'ytick.direction': 'in',

    'xtick.major.size': 4,
    'ytick.major.size': 4,
    'xtick.major.width': 0.5,
    'ytick.major.width': 0.5,

    'xtick.minor.visible': True,
    'ytick.minor.visible': True,
    'xtick.minor.top': True,
    'xtick.minor.bottom': True,
    'ytick.minor.left': True,
    'ytick.minor.right': True,
    'xtick.minor.size': 2,
    'ytick.minor.size': 2,
    'xtick.minor.width': 0.3,
    'ytick.minor.width': 0.3,


    'legend.fontsize': 11,
    'legend.loc': 'upper right',
    'legend.frameon': False,
    'legend.facecolor': 'none',
    'legend.edgecolor': 'none'    
    })