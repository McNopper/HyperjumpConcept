"""Transverse Dirac zero-mode localization on the sigma-model kink.

Background (the simplest 1D representative of the paper's phi_0(r) profile
when one dimension is singled out as transverse to the brane):

    phi_0(r) = v * tanh(sqrt(2 lambda) v r)              [kink]
    V(phi_0) = lambda (phi_0^2 - v^2)^2

Add a 5D Dirac fermion with Yukawa coupling  m_Psi(r) = h * phi_0(r)
(Rubakov-Shaposhnikov 1983).  The transverse zero-mode equation is

    [d/dr + h * phi_0(r)] psi_L(r) = 0

with normalizable solution

    psi_L(r) = N * exp(-h * integral_0^r phi_0(r') dr')
             = N * (cosh(sqrt(2 lambda) v r))^(-h / (sqrt(2 lambda) v))

This is the 4D SM fermion zero-mode profile.  Cross-check it numerically.

Run:  python localization.py
"""
from __future__ import annotations

import os
import numpy as np
from scipy.integrate import cumulative_trapezoid
import matplotlib.pyplot as plt


def main() -> None:
    lam = 1.0
    v = 1.0
    h_values = [0.5, 1.0, 2.0, 4.0]

    k = np.sqrt(2.0 * lam) * v  # inverse wall thickness
    r = np.linspace(-8.0, 8.0, 4001)
    phi0 = v * np.tanh(k * r)
    print(f"kink width 1/k = {1.0 / k:.3f}")
    print(f"barrier V(0) = lambda v^4 = {lam * v ** 4:.3f}")

    out_dir = os.path.join(os.path.dirname(__file__), "figures")
    os.makedirs(out_dir, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

    ax1.plot(r, phi0 / v, color="k", label=r"$\phi_0(r)/v$ (kink)")
    ax1.plot(r, (lam * (phi0 ** 2 - v ** 2) ** 2) / (lam * v ** 4),
             color="C3", label=r"$V(\phi_0)/(\lambda v^4)$")
    ax1.set_xlabel(r"$r$ (in units of $1/(\sqrt{\lambda}v)$)")
    ax1.set_title("Brane background profile")
    ax1.grid(alpha=0.3)
    ax1.legend()

    for h in h_values:
        integ = np.concatenate([[0.0], cumulative_trapezoid(h * phi0, r)])
        psi_num = np.exp(-integ)
        psi_ana = np.cosh(k * r) ** (-h / k)
        psi_num /= psi_num.max()
        psi_ana /= psi_ana.max()

        err = np.max(np.abs(psi_num - psi_ana))
        print(f"  h={h}: max|numeric - analytic| = {err:.2e}; "
              f"localization width ~ {k / h:.3f} (units of 1/(sqrt(lambda)v))")

        ax2.plot(r, psi_num, label=fr"$h={h}$")

    ax2.set_xlabel(r"$r$")
    ax2.set_ylabel(r"$\psi_L(r)$ (peak-normalized)")
    ax2.set_title("Transverse Dirac zero mode")
    ax2.grid(alpha=0.3)
    ax2.legend()

    fig.tight_layout()
    out = os.path.join(out_dir, "localization.png")
    fig.savefig(out, dpi=140)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
