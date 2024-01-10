import math
import numpy as np


def run_simulation(n, r, zs):
    np.set_printoptions(threshold=np.inf)

    a_list = range(1, n+1)
    unit_roots = np.array([math.e**(2j * math.pi * m/n) for m in a_list])

    rr = r*np.ones(unit_roots.shape)

    N = int(max(0, round(4.0 + 0.5 * np.log10(r))))

    npts = 3 * N + 2

    a_list = range(1, int(npts+1))
    circ = np.array([math.e**(m * 2j* math.pi/npts) for m in a_list])

    z_list = [(unit_roots[i] + rr[i] * circ) for i in range(n)]

    z = np.concatenate(z_list)

    A = np.concatenate([np.zeros(1), -np.ones(z.shape[0])])

    b = np.concatenate([np.zeros(1), -np.log(np.abs(z-zs))])

    for i in range(n):
        B = np.concatenate([np.ones(1), np.log(np.abs(z-unit_roots[i]))])
        A = np.column_stack((A, B))
        for k in range(N):
            zck = np.power((z - unit_roots[i]), -(k+1))
            C = np.concatenate([np.zeros(1), zck.real])
            D = np.concatenate([np.zeros(1), zck.imag])
            A = np.column_stack((A, C, D))

    x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
    x = np.delete(x, (0), axis=0)
    d = x[0:: 2 * N + 1]
    x = np.delete(x, np.s_[0::2*N+1], None)

    a = x[0::2]
    b = x[1::2]

    X = np.linspace(-2.0*zs, 2.0*zs, 1000)
    Y = np.linspace(-2.0*zs, 2.0*zs, 1000)
    [xx, yy] = np.meshgrid(X, Y)

    zz = xx + 1j*yy
    uu = np.log(np.abs(zz - zs))

    for j in range(n):
        uu = uu + d[j]*np.log(np.abs(zz - unit_roots[j]))
        for k in range(N):
            zck = np.power((zz - unit_roots[j]), -(k+1))
            kk = k + j * N
            uu = uu + a[kk] * zck.real + b[kk] * zck.imag
    for j in range(n):
        uu[np.abs(zz - unit_roots[j]) <= rr[j]] = np.nan

    return xx, yy, uu
