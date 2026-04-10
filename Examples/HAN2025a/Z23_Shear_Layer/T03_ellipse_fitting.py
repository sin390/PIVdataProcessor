import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path

def extract_center_contour(X, Y, Z, level, ic, jc):
    xc, yc = X[ic, jc], Y[ic, jc]

    fig, ax = plt.subplots()
    cs = ax.contour(X, Y, Z, levels=[level])
    plt.close(fig)

    # cs.allsegs[level_index] -> list of contour segments
    segs = cs.allsegs[0]

    best = None
    min_dist = np.inf

    for seg in segs:
        if len(seg) < 10:
            continue

        # seg shape (N,2)
        if Path(seg).contains_point((xc, yc)):
            return seg

        d2 = np.min((seg[:,0]-xc)**2 + (seg[:,1]-yc)**2)
        if d2 < min_dist:
            min_dist = d2
            best = seg

    return best


def fit_axis_aligned_ellipse_with_fixed_center(X, Y, Z, ic, jc, level=0.1):
    """
    在非均匀网格 (X,Y) 上，对标量场 Z 的 level 等值线做拟合：
    - 椭圆中心固定在 (X[ic,jc], Y[ic,jc])
    - 椭圆长轴/短轴与 x/y 轴对齐
    返回:
        xc, yc, a, b, contour_points
    """
    xc, yc = X[ic, jc], Y[ic, jc]

    verts = extract_center_contour(X, Y, Z, level, ic, jc)
    if verts is None:
        raise ValueError("未找到合适的等值线")

    x = verts[:, 0]
    y = verts[:, 1]

    u = x - xc
    v = y - yc

    # 线性最小二乘拟合 alpha*u^2 + beta*v^2 = 1
    A = np.column_stack([u**2, v**2])
    rhs = np.ones(len(u))

    coeff, _, _, _ = np.linalg.lstsq(A, rhs, rcond=None)
    alpha, beta = coeff

    if alpha <= 0 or beta <= 0:
        raise ValueError("拟合失败：得到非正的 alpha/beta，说明该等值线不适合此椭圆模型")

    a = 1.0 / np.sqrt(alpha)
    b = 1.0 / np.sqrt(beta)

    # 按你的约束，长轴应在水平方向
    if a < b:
        # 若出现 a < b，说明数据本身更像竖直长轴椭圆
        # 这里可以报错，也可以交换
        print("警告：拟合结果出现 a < b，数据未必符合“水平长轴”假设。现已交换使 a >= b。")
        a, b = b, a

    return xc, yc, a, b, verts