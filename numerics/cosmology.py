"""Toy cosmology for Subproblem 1: collective coordinate Phi(tau).

Equation of motion (paper, Subproblem 1):

    Phi'' + 3 H Phi' + U'(Phi) = 0

coupled to the Friedmann equation in the slow-roll spirit,

    H^2 = (8 pi G / 3) * rho_Phi,    rho_Phi = 0.5 Phi'^2 + U(Phi).

We pick the simplest chaotic-inflation potential U(Phi) = 0.5 m^2 Phi^2,
work in Planck units (8 pi G = M_Pl^{-2}, set M_Pl = 1), and integrate
forward from a slow-roll initial condition Phi_0 ~ a few, Phi'_0 set by
slow roll (Phi' = -U'/3H).

This is a textbook closure of Subproblem 1, used here only to confirm
that the brane-radius collective coordinate can sustain a quasi-de Sitter
phase followed by reheating-like oscillations, *given* a coupling to 5D
gravity (Subproblem 2) -- which provides the H term.

Run:  python cosmology.py
"""
from __future__ import annotations

import os
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


def U(phi: float, m: float) -> float:
    return 0.5 * m * m * phi * phi


def dU(phi: float, m: float) -> float:
    return m * m * phi


def rhs(t: float, y: np.ndarray, m: float) -> np.ndarray:
    phi, phidot = y
    rho = 0.5 * phidot * phidot + U(phi, m)
    H = np.sqrt(max(rho, 0.0) / 3.0)  # M_Pl = 1 -> H^2 = rho/3
    return np.array([phidot, -3.0 * H * phidot - dU(phi, m)])


def main() -> None:
    m = 1e-2          # inflaton mass in Planck units
    phi0 = 16.0       # super-Planckian -> ~64 e-folds for m^2 phi^2
    phidot0 = -dU(phi0, m) / (3.0 * np.sqrt(U(phi0, m) / 3.0))  # slow-roll IC
    t_end = 1.0e4

    sol = solve_ivp(
        lambda t, y: rhs(t, y, m),
        (0.0, t_end),
        [phi0, phidot0],
        rtol=1e-9, atol=1e-12, dense_output=True, max_step=5.0,
    )
    print(f"integration: {sol.message}, nfev={sol.nfev}")

    t = np.linspace(0.0, t_end, 4000)
    phi = sol.sol(t)[0]
    phidot = sol.sol(t)[1]
    rho = 0.5 * phidot ** 2 + U(phi, m)
    H = np.sqrt(np.maximum(rho, 0.0) / 3.0)

    # number of e-folds: N(t) = integral H dt
    N = np.concatenate([[0.0], np.cumsum(0.5 * (H[:-1] + H[1:]) * np.diff(t))])
    print(f"  total e-folds: N = {N[-1]:.2f}")
    print(f"  inflation ends roughly when Phi crosses ~1; final Phi = {phi[-1]:.3f}")
    print(f"  H at start: {H[0]:.3e}    H at end: {H[-1]:.3e}")

    out_dir = os.path.join(os.path.dirname(__file__), "figures")
    os.makedirs(out_dir, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    axes[0].plot(t, phi)
    axes[0].set_xlabel(r"cosmic time $\tau$ (Planck units)")
    axes[0].set_ylabel(r"$\Phi(\tau)$  [M_{Pl}]")
    axes[0].set_title("Collective coordinate trajectory")
    axes[0].grid(alpha=0.3)

    axes[1].semilogy(t, H)
    axes[1].set_xlabel(r"$\tau$")
    axes[1].set_ylabel("Hubble rate $H$")
    axes[1].set_title("Quasi-de Sitter then reheating-like decay")
    axes[1].grid(alpha=0.3, which="both")

    axes[2].plot(t, N)
    axes[2].set_xlabel(r"$\tau$")
    axes[2].set_ylabel(r"e-folds $N = \int H \, d\tau$")
    axes[2].set_title(f"Total e-folds: {N[-1]:.1f}")
    axes[2].grid(alpha=0.3)

    fig.tight_layout()
    out = os.path.join(out_dir, "cosmology.png")
    fig.savefig(out, dpi=140)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
