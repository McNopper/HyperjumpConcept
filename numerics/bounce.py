"""Barrier-penetration action for the sigma-model double-well, done honestly.

Potential (radial mode |phi| = rho, paper sec. 'Candidate Dynamical Skeleton'):

    V(rho) = lambda (rho^2 - v^2)^2

The two minima rho = +/- v are *degenerate*.  There is therefore **no finite-
action O(d)-symmetric Coleman bounce** in this potential -- a localized
phi(r) -> +v at infinity with phi(0) < 0 cannot be a saddle of the Euclidean
action when both vacua have the same energy density.

What actually controls the tunnelling rate flagged in Subproblem 7 is the
planar **domain-wall surface tension** sigma (the kink soliton), times the
hyper-area of the bubble/tube that the cargo carves out of the bulk in
Euclidean time as it traverses the chord.

We compute:
  1. sigma analytically and numerically for the 1D kink phi(r) = v tanh(k r),
     k = sqrt(2 lambda) v.
  2. The parametric bounce action for macroscopic cargo of cross-section A_T
     traversing a chord of length L_chord:
       B_phys  ~  sigma * (P * L_chord + 2 A_T)         (tube + caps)
     where P = perimeter of the cargo cross-section transverse to the chord.
  3. The resulting Gamma / V_5 ~ mu^5 exp(-B_phys) for a few sample numbers.

Result is, as the paper anticipates, *exponentially small* for any cargo
larger than a microscopic probe -- macroscopic hyperjumps are not free.

Run:  python bounce.py
"""
from __future__ import annotations

import os
from math import sqrt

import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt


def kink_tension_analytic(lam: float, v: float) -> float:
    """Kink surface tension sigma = (4 sqrt(2) / 3) sqrt(lambda) v^3.

    Derivation: phi(r) = v tanh(k r), k = sqrt(2 lambda) v, so
        sigma = integral dr [ 0.5 (dphi/dr)^2 + V(phi) ]
              = integral dr [ 2 V(phi) ]              (BPS / virial)
              = 2 lambda v^4 * integral sech^4(k r) dr
              = 2 lambda v^4 * 4 / (3 k)
              = (4 sqrt(2) / 3) sqrt(lambda) v^3.
    """
    return (4.0 * sqrt(2.0) / 3.0) * sqrt(lam) * v ** 3


def kink_tension_numeric(lam: float, v: float) -> float:
    k = sqrt(2.0 * lam) * v

    def integrand(r):
        phi = v * np.tanh(k * r)
        dphi = v * k / np.cosh(k * r) ** 2
        return 0.5 * dphi * dphi + lam * (phi * phi - v * v) ** 2

    val, _ = quad(integrand, -50.0 / k, 50.0 / k, limit=400)
    return val


def bounce_action_cargo(sigma: float, L_chord: float,
                        cross_section_A: float, perimeter_P: float) -> float:
    """Parametric barrier-penetration action for a tube of domain wall
    enclosing cargo of cross-section A and perimeter P traversing length L."""
    return sigma * (perimeter_P * L_chord + 2.0 * cross_section_A)


def main() -> None:
    lam = 1.0
    v = 1.0

    sigma_a = kink_tension_analytic(lam, v)
    sigma_n = kink_tension_numeric(lam, v)
    print("Domain-wall (kink) surface tension for V = lambda (phi^2 - v^2)^2")
    print(f"  analytic : sigma = (4 sqrt 2 / 3) sqrt(lambda) v^3 = {sigma_a:.6f}")
    print(f"  numeric  : sigma                                  = {sigma_n:.6f}")
    print(f"  relative error                                    = {abs(sigma_a - sigma_n) / sigma_a:.2e}")
    print()

    # === Parametric tunnelling rates for sample cargos =============================
    # All quantities in natural units (hbar = c = 1).
    # Set lambda*v constrained by sub-mm gravity: 1/(sqrt(lambda) v) <~ 52 micron.
    # Pick the saturating value: ell_perp = 52e-6 m  ->  sqrt(lambda) v = 1 / ell_perp.
    print("=" * 72)
    print("Sample tunnelling-rate exponents for various cargos")
    print("(saturating laboratory bound: 1/(sqrt(lambda) v) = ell_perp = 52 um)")
    print("=" * 72)
    ell_perp = 52e-6                                  # metres
    # In natural units we work in inverse-metres ("length").
    sigma_phys = sigma_a / ell_perp ** 3              # sigma ~ 1/length^3 in d=5? actually
    # Quick dimensional check: in 5D, [phi] = mass^{3/2}, [V] = mass^5 = 1/length^5,
    # [sigma] = [V] * length = 1/length^4. With our rescaling sigma = O(1) /(ell_perp^4)
    # for the integrated planar wall in the *transverse* dimension only -- but the
    # wall has 4 worldvolume dimensions, so the Euclidean area element is length^4.
    # The action S_E is dimensionless, sigma * Area, with [Area] = length^4.
    sigma_phys = sigma_a / ell_perp ** 4              # [sigma] = 1/length^4 (correct)

    cargos = [
        ("electron-scale probe (1 fm radius, 1 fm long)",
         1e-15, np.pi * (1e-15) ** 2, 2 * np.pi * 1e-15),
        ("atom (0.1 nm radius, 0.1 nm long)",
         1e-10, np.pi * (1e-10) ** 2, 2 * np.pi * 1e-10),
        ("dust grain (1 um radius), 1 m chord",
         1.0, np.pi * (1e-6) ** 2, 2 * np.pi * 1e-6),
        ("spacecraft (1 m radius), 1 ly chord",
         9.46e15, np.pi * 1.0 ** 2, 2 * np.pi * 1.0),
    ]
    for label, L_chord, A_T, P in cargos:
        # Worldvolume "area" in 5D Euclidean: tube has 4 wv dims = (3 brane dims along
        # the spatial extent of the cargo) x (1 Euclidean-time dim along the chord).
        # We approximate the tube wall worldvolume as P_3 * L_chord, with P_3 the
        # 3-surface of the cargo transverse to the chord.  Using the simplest model
        # (cargo is a 3-ball of cross-radius R, P_3 = 4 pi R^2):
        R = sqrt(A_T / np.pi)
        wv_area = 4.0 * np.pi * R * R * L_chord     # tube
        wv_caps = 2.0 * (4.0 / 3.0 * np.pi * R ** 3)  # two end-caps (3-ball volumes)
        B = sigma_phys * (wv_area + wv_caps)
        print(f"  {label}")
        print(f"    R={R:.3e} m, L={L_chord:.3e} m")
        print(f"    worldvolume area ~ {wv_area:.3e} m^4,  S_E = {B:.3e}")
        print(f"    Gamma / V_5 ~ mu^5 exp({-B:.3e}) -> "
              + ("totally negligible" if B > 50 else "non-trivial; needs full calc"))
        print()

    # === Plot the kink profile for completeness ====================================
    out_dir = os.path.join(os.path.dirname(__file__), "figures")
    os.makedirs(out_dir, exist_ok=True)

    k = sqrt(2.0 * lam) * v
    r = np.linspace(-6 / k, 6 / k, 400)
    phi = v * np.tanh(k * r)
    energy_density = 0.5 * (v * k / np.cosh(k * r) ** 2) ** 2 + lam * (phi ** 2 - v ** 2) ** 2

    fig, ax = plt.subplots(figsize=(6, 4))
    ax2 = ax.twinx()
    ax.plot(r * k, phi / v, "C0-", label=r"$\phi(r)/v$ (kink)")
    ax2.plot(r * k, energy_density / (lam * v ** 4), "C3--",
             label=r"energy density / $\lambda v^4$")
    ax.set_xlabel(r"$\sqrt{2\lambda}\,v\,r$")
    ax.set_ylabel(r"$\phi/v$", color="C0")
    ax2.set_ylabel(r"energy density (normalized)", color="C3")
    ax.set_title(fr"Domain wall: $\sigma = (4\sqrt{{2}}/3)\,\sqrt{{\lambda}}\,v^3 = {sigma_a:.3f}$")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out = os.path.join(out_dir, "domain_wall.png")
    fig.savefig(out, dpi=140)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
