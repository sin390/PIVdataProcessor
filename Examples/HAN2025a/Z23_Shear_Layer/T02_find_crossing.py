import numpy as np

def _root_quadratic_three_points(x0, y0, x1, y1, x2, y2, thr, x_lo, x_hi):
    y0 -= thr
    y1 -= thr
    y2 -= thr

    d0 = (x0 - x1) * (x0 - x2)
    d1 = (x1 - x0) * (x1 - x2)
    d2 = (x2 - x0) * (x2 - x1)

    A = y0/d0 + y1/d1 + y2/d2

    B = -y0*(x1 + x2)/d0 - y1*(x0 + x2)/d1 - y2*(x0 + x1)/d2

    C = y0*(x1*x2)/d0 + y1*(x0*x2)/d1 + y2*(x0*x1)/d2

    r = np.roots([A, B, C])
    r = r[np.isreal(r)].real
    r = r[(r >= x_lo) & (r <= x_hi)]

    x_star = r[0]
    y_star = (A*x_star**2 + B*x_star + C) + thr

    print("interpolated y =", y_star)

    return x_star


def _crossing_left_quadratic(x, y, k, thr):
    x_lo, x_hi = min(x[k], x[k+1]), max(x[k], x[k+1])
    return _root_quadratic_three_points(
        x[k],   y[k],
        x[k+1], y[k+1],
        x[k+2], y[k+2],
        thr, x_lo, x_hi
    )

def _crossing_right_quadratic(x, y, k, thr):
    x_lo, x_hi = min(x[k-1], x[k]), max(x[k-1], x[k])
    return _root_quadratic_three_points(
        x[k-2], y[k-2],
        x[k-1], y[k-1],
        x[k],   y[k],
        thr, x_lo, x_hi
    )

def find_threshold_crossings_quadratic_minimal(x, y, ic, thr):
    n = len(y)

    kL = None
    for k in range(ic-1, -1, -1):
        if y[k] < thr:
            kL = k
            break

    kR = None
    for k in range(ic+1, n):
        if y[k] < thr:
            kR = k
            break

    xL = _crossing_left_quadratic(x, y, kL, thr)
    xR = _crossing_right_quadratic(x, y, kR, thr)
    return xR - xL
    # return x[kR]-x[kL]