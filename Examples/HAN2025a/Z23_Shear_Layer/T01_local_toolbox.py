''' 
=========================
= Author:   ChatGPT     =
= Version:  1.0         =
=========================
'''
from numba import njit
import numpy as np
@njit
def compute_mask_lagrange(grid1: np.ndarray, grid2: np.ndarray, 
                          left: int, right: int, bottom: int, up: int) -> np.ndarray:
    x_read = grid1[0]
    y_read = grid1[1]
    x = grid2[0]
    y = grid2[1]
    Nx, Ny = x_read.shape
    Nx2, Ny2 = x.shape
    mask_inside = np.zeros((Nx2, Ny2), dtype=np.bool_)
    dx = x_read[1, 0] - x_read[0, 0]
    dy = y_read[0, 1] - y_read[0, 0]
    for i in range(Nx2):
        for j in range(Ny2):
            xi = x[i, j]
            yj = y[i, j]

            i_ip = int((xi - x_read[0, 0]) / dx + 1)
            j_ip = int((yj - y_read[0, 0]) / dy + 1)
            if (i_ip - 2 < left) or (i_ip + 1 >= right) or (j_ip - 2 < bottom) or (j_ip + 1 >= up):
                continue
            mask_inside[i, j] = True
    return mask_inside

@njit
def lagrange_interpolate_with_mask(grid1: np.ndarray,
                                   grid2: np.ndarray,
                                   scalar1: np.ndarray,
                                   mask_inside: np.ndarray):

    x_read = grid1[0]
    y_read = grid1[1]
    x = grid2[0]
    y = grid2[1]

    Nx, Ny = scalar1.shape
    Nx2, Ny2 = x.shape

    scalar2 = np.full((Nx2, Ny2), np.nan, dtype=np.float64)

    dx = x_read[1, 0] - x_read[0, 0]
    dy = y_read[0, 1] - y_read[0, 0]

    for i in range(Nx2):
        for j in range(Ny2):
            if not mask_inside[i, j]:
                continue
            xi = x[i, j]
            yj = y[i, j]
            i_ip = int((xi - x_read[0, 0]) / dx + 1)
            j_ip = int((yj - y_read[0, 0]) / dy + 1)

            x1 = x_read[i_ip - 2, j_ip]; x2 = x_read[i_ip - 1, j_ip]
            x3 = x_read[i_ip    , j_ip]; x4 = x_read[i_ip + 1, j_ip]

            y1 = y_read[i_ip, j_ip - 2]; y2 = y_read[i_ip, j_ip - 1]
            y3 = y_read[i_ip, j_ip    ]; y4 = y_read[i_ip, j_ip + 1]

            ax1 = ((xi - x2) * (xi - x3) * (xi - x4)) / ((x1 - x2) * (x1 - x3) * (x1 - x4))
            ax2 = ((xi - x1) * (xi - x3) * (xi - x4)) / ((x2 - x1) * (x2 - x3) * (x2 - x4))
            ax3 = ((xi - x1) * (xi - x2) * (xi - x4)) / ((x3 - x1) * (x3 - x2) * (x3 - x4))
            ax4 = ((xi - x1) * (xi - x2) * (xi - x3)) / ((x4 - x1) * (x4 - x2) * (x4 - x3))

            by1 = ((yj - y2) * (yj - y3) * (yj - y4)) / ((y1 - y2) * (y1 - y3) * (y1 - y4))
            by2 = ((yj - y1) * (yj - y3) * (yj - y4)) / ((y2 - y1) * (y2 - y3) * (y2 - y4))
            by3 = ((yj - y1) * (yj - y2) * (yj - y4)) / ((y3 - y1) * (y3 - y2) * (y3 - y4))
            by4 = ((yj - y1) * (yj - y2) * (yj - y3)) / ((y4 - y1) * (y4 - y2) * (y4 - y3))

            val = (
                by1 * (ax1 * scalar1[i_ip - 2, j_ip - 2] + ax2 * scalar1[i_ip - 1, j_ip - 2] +
                       ax3 * scalar1[i_ip    , j_ip - 2] + ax4 * scalar1[i_ip + 1, j_ip - 2]) +
                by2 * (ax1 * scalar1[i_ip - 2, j_ip - 1] + ax2 * scalar1[i_ip - 1, j_ip - 1] +
                       ax3 * scalar1[i_ip    , j_ip - 1] + ax4 * scalar1[i_ip + 1, j_ip - 1]) +
                by3 * (ax1 * scalar1[i_ip - 2, j_ip    ] + ax2 * scalar1[i_ip - 1, j_ip    ] +
                       ax3 * scalar1[i_ip    , j_ip    ] + ax4 * scalar1[i_ip + 1, j_ip    ]) +
                by4 * (ax1 * scalar1[i_ip - 2, j_ip + 1] + ax2 * scalar1[i_ip - 1, j_ip + 1] +
                       ax3 * scalar1[i_ip    , j_ip + 1] + ax4 * scalar1[i_ip + 1, j_ip + 1])
            )
            scalar2[i, j] = val
    return scalar2


def dscalar_dxdy_physical_2d(X, scalar):
    """
    非均匀二维网格上显式利用 (x,y) 坐标
    使用 5x5 局部最小二乘平面拟合
    边界两层标记为 nan

    Parameters
    ----------
    X : shape (2, nx, ny)
        X[0] = x, X[1] = y
    scalar : shape (nx, ny)

    Returns
    -------
    out : shape (2, nx, ny)
        out[0] = ds/dx
        out[1] = ds/dy
    """

    x = X[0]
    y = X[1]
    s = scalar

    nx, ny = s.shape
    out = np.full((2, nx, ny), np.nan)

    for i in range(2, nx-2):
        for j in range(2, ny-2):

            # 取 5x5 邻域
            xs = x[i-2:i+3, j-2:j+3].ravel()
            ys = y[i-2:i+3, j-2:j+3].ravel()
            ss = s[i-2:i+3, j-2:j+3].ravel()

            # 构造最小二乘矩阵
            A = np.column_stack([xs, ys, np.ones_like(xs)])

            # 解最小二乘
            coeff, *_ = np.linalg.lstsq(A, ss, rcond=None)

            # coeff = [a, b, c]
            out[0, i, j] = coeff[0]  # ds/dx
            out[1, i, j] = coeff[1]  # ds/dy

    return out