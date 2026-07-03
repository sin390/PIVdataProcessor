'''
=====================================================
Scientific Figure Utilities for PIV / Turbulence Work
Author:    ChatGPT (supervisor: Zexu HAN)
Version:   1.0
Date:      2026/02/20
=====================================================
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def turbo_with_internal_white(p0=0.25, N=256):
    """
    在 turbo 内部插入白色（连续插值）
    
    p0 : 白色在 colormap 中的位置（0 < p0 < 1）
         例如 p0=0.25 表示前 25% 处是白色
    """
    turbo = plt.get_cmap("turbo")

    i0 = int(p0 * N)

    # turbo 原始采样
    base = turbo(np.linspace(0, 1, N))

    # turbo 起始色 & 白色
    c_start = base[0]
    white   = np.array([1.0, 1.0, 1.0, 1.0])

    # ---- 前段：turbo(0) → 白 ----
    for i in range(i0):
        t = i / max(i0 - 1, 1)
        base[i, :3] = (1 - t) * c_start[:3] + t * white[:3]

    # ---- 后段：保持 turbo 原样 ----
    return LinearSegmentedColormap.from_list(
        "turbo_internal_white",
        base
    )
white_turbo = turbo_with_internal_white()