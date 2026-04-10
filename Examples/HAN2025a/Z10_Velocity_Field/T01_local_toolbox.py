'''
=========================
= Author:   ChatGPT     =
= Version:  1.0         =
= Date:     2026/01/23
=========================
'''
import numpy as np
import matplotlib.patches as patches

def add_open_arc_one_arrow(ax, center, r,
                           theta1, theta2,
                           arrow_theta=None,
                           direction='ccw',
                           color='k', lw=2.0,
                           dash=(4,4),
                           arrow_size=16,
                           zorder=10):
    """
    开口虚线圆弧 + 单个箭头

    theta1, theta2 : 圆弧起止角度（度）
    arrow_theta    : 箭头所在角度（度），None -> 放在中点
    direction      : 'ccw'（逆时针）或 'cw'（顺时针）
    """

    # ---- 圆弧 ----
    arc = patches.Arc(
        center, 2*r, 2*r,
        theta1=theta1, theta2=theta2,
        linewidth=lw,
        linestyle=(0, dash),
        color=color,
        zorder=zorder
    )
    ax.add_patch(arc)

    # ---- 箭头位置 ----
    if arrow_theta is None:
        arrow_theta = 0.5 * (theta1 + theta2)

    th = np.deg2rad(arrow_theta)

    # 圆弧上的点
    x = center[0] + r*np.cos(th)
    y = center[1] + r*np.sin(th)

    # 切向方向
    if direction == 'ccw':
        tx, ty = -np.sin(th),  np.cos(th)
    elif direction == 'cw':
        tx, ty =  np.sin(th), -np.cos(th)
    else:
        raise ValueError("direction must be 'ccw' or 'cw'")

    L = 0.22 * r
    p0 = (x - 0.5*L*tx, y - 0.5*L*ty)
    p1 = (x + 0.5*L*tx, y + 0.5*L*ty)

    arrow = patches.FancyArrowPatch(
        p0, p1,
        arrowstyle='-|>',
        mutation_scale=arrow_size,
        linewidth=lw,
        color=color,
        zorder=zorder+1
    )
    ax.add_patch(arrow)