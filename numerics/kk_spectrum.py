"""Kaluza-Klein-like mass spectrum of the transverse Dirac operator on the kink.

Background:  phi_0(r) = v tanh(k r),   k = sqrt(2 lambda) v.
Yukawa coupling m_Psi(r) = h phi_0(r).

Squaring the transverse Dirac operator (Rubakov-Shaposhnikov 1983) gives a
1D Schrodinger problem for left- and right-handed components,

    H_+- psi = E^2 psi,
    H_+- = - d^2/dr^2 + h^2 phi_0(r)^2  -+  h phi_0'(r).

With phi_0' = k v sech^2(k r) and phi_0^2 = v^2 (1 - sech^2(k r)),

    H_- = - d^2/dr^2 + h^2 v^2  -  (h^2 v^2 + h v k) sech^2(k r).

This is the exactly-solvable Poschl-Teller potential.  Its bound-state
eigenvalues are known analytically:

    E_n^2 = h^2 v^2 - (k (s - n))^2,    n = 0, 1, ..., floor(s)

where s satisfies s(s+1) = (h v / k)(h v / k + 1)  ->  s = h v / k = h/(sqrt(2 lambda) v) * v = h / sqrt(2 lambda).

Wait, in our units with v=1 and k = sqrt(2 lambda) v = sqrt(2 lambda), we have
s = h v / k = h / sqrt(2 lambda).  For lambda = v = 1, s = h / sqrt(2).

We verify the spectrum numerically by finite-difference diagonalization.
"""
from __future__ import annotations

import os
import math
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
import matplotlib.pyplot as plt


def poschl_teller_levels(h: float, lam: float = 1.0, v: float = 1.0):
    """Analytical bound-state eigenvalues E_n^2 for H_- on the kink."""
    k = math.sqrt(2.0 * lam) * v
    s = h * v / k  # depth parameter
    n_max = int(math.floor(s))  # number of bound states is floor(s) + 1 for s > 0... actually:
    levels = []
    # Standard Poschl-Teller: H = -d^2/dr^2 - U0 sech^2(k r), U0 = s(s+1) k^2
    # bound states E_b < 0: E_b = -k^2 (s - n)^2, n = 0,1,...,floor(s) if s is not integer,
    # or n = 0,1,...,s-1 if s is integer.
    # Our H_- has an additive constant h^2 v^2:
    #   E^2 = h^2 v^2 - k^2 (s - n)^2
    # but with U0 = h^2 v^2 + h v k = k^2 (s^2 + s) = k^2 s (s+1) -- consistent.
    for n in range(0, n_max + 1):
        if s - n > 0:
            levels.append(h * h * v * v - (k * (s - n)) ** 2)
    return levels


def diagonalize_kink(h: float, lam: float = 1.0, v: float = 1.0,
                     L: float = 20.0, N: int = 4001):
    k = math.sqrt(2.0 * lam) * v
    r = np.linspace(-L / k, L / k, N)
    dr = r[1] - r[0]
    phi0 = v * np.tanh(k * r)
    phi0_p = v * k / np.cosh(k * r) ** 2
    V_minus = h * h * phi0 ** 2 - h * phi0_p  # H_- potential
    # tridiagonal -d^2/dr^2 + V on Dirichlet boundary
    main = 2.0 / dr ** 2 + V_minus
    off = -1.0 / dr ** 2 * np.ones(N - 1)
    H = diags([off, main, off], offsets=[-1, 0, 1]).tocsr()
    # find low eigenvalues
    eigvals = np.sort(eigsh(H, k=8, which="SA", return_eigenvectors=False))
    return eigvals


def main() -> None:
    print("Poschl-Teller spectrum of H_- on the kink background")
    print("(units: lambda = v = 1, so k = sqrt(2), bulk gap = h^2 v^2 = h^2)")
    print()
    for h in [0.5, 1.0, 2.0, 4.0]:
        ana = poschl_teller_levels(h)
        num = diagonalize_kink(h)
        gap = h ** 2  # continuum threshold
        print(f"  h = {h:.2f}   (bulk gap E^2 = {gap:.4f})")
        print(f"    analytic bound E^2 levels: {[f'{x:+.4f}' for x in ana]}")
        print(f"    numeric  lowest 5 levels : {[f'{x:+.4f}' for x in num[:5]]}")
        if ana:
            err = abs(ana[0] - num[0])
            print(f"    zero-mode E^2 (should be 0): numeric = {num[0]:+.2e}  (analytic 0, err = {err:.2e})")
        print()

    # plot mass spectrum vs h
    hs = np.linspace(0.2, 5.0, 40)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(hs, hs ** 2, "k--", label=r"bulk threshold $E^2 = h^2 v^2$")
    for n in range(0, 6):
        e2 = []
        for h in hs:
            levels = poschl_teller_levels(h)
            if n < len(levels):
                e2.append(levels[n])
            else:
                e2.append(np.nan)
        ax.plot(hs, e2, label=f"$n={n}$ bound state")
    ax.set_xlabel(r"Yukawa coupling $h$ (units of $\sqrt{\lambda}v$)")
    ax.set_ylabel(r"$E_n^2$ (4D mass$^2$)")
    ax.set_title("KK-like tower of transverse modes on the kink")
    ax.axhline(0, color="grey", lw=0.5)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()

    out_dir = os.path.join(os.path.dirname(__file__), "figures")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "kk_spectrum.png")
    fig.savefig(out, dpi=140)
    print(f"wrote {out}")
    print()
    print("Phenomenology: the zero mode is the localized 4D SM fermion;")
    print("the bulk threshold E^2 = h^2 v^2 sets the mass gap to non-localized")
    print("(KK-like) excitations.  Stronger Yukawa coupling h pushes the gap up")
    print("but also adds more sub-threshold bound states.")


if __name__ == "__main__":
    main()
