"""Sub-millimetre gravity bound on (lambda, v) from Subproblem 5.

The paper cites Lee et al. (2020): the new transverse length scale must
satisfy

    ell_perp  =  1 / (sqrt(lambda) v)  <  ell_exp  =  52 micron  (95% CL)

so

    sqrt(lambda) v  >  1 / ell_exp  ~  4 meV  in natural units.

This script plots the allowed region in (lambda, v) for both this 2020
bound and the older 2003 bound (ell_exp ~ 44 micron) for context.

Note: this is the *first-pass* translation flagged in Subproblem 5.  A
proper bound depends on the unsolved gravity sector (Subproblem 2).

Run:  python gravity_bound.py
"""
from __future__ import annotations

import os
import numpy as np
import matplotlib.pyplot as plt


# Convert lengths to inverse-energy (natural units, hbar = c = 1)
# 1 m = 1 / (1.973e-7 eV)  ->  1 micron = 1 / (0.1973 eV)
HBAR_C_EV_M = 1.973e-7  # eV * m


def ell_to_energy(ell_m: float) -> float:
    """Convert a length in metres to an energy in eV: E = hbar c / ell."""
    return HBAR_C_EV_M / ell_m


def main() -> None:
    bounds = {
        "Lee et al. 2020  (52 micron, 95% CL)": 52e-6,
        "Adelberger et al. 2003  (~44 micron)": 44e-6,
    }

    lam = np.logspace(-12, 2, 400)  # dimensionless coupling (in 5D it has dim^{-1}, but here we treat as dimless for visualization)
    fig, ax = plt.subplots(figsize=(7, 5))

    for label, ell in bounds.items():
        E_min = ell_to_energy(ell)  # in eV
        # bound: sqrt(lambda) v > E_min  ->  v > E_min / sqrt(lambda)
        v_min = E_min / np.sqrt(lam)
        ax.loglog(lam, v_min, label=f"{label}: $v > {E_min*1e3:.2f}\\,\\mathrm{{meV}} / \\sqrt{{\\lambda}}$")

    ax.fill_between(lam, ell_to_energy(52e-6) / np.sqrt(lam), 1e10,
                    alpha=0.15, color="C0", label="allowed by 2020 bound")

    # mark a few reference points
    ax.axhline(1.0, color="grey", lw=0.5, ls=":")
    ax.text(1e-10, 1.2, "v = 1 eV", fontsize=8, color="grey")
    ax.axhline(125e9, color="grey", lw=0.5, ls=":")
    ax.text(1e-10, 1.5e11, "v ~ EW scale (125 GeV)", fontsize=8, color="grey")

    ax.set_xlabel(r"$\lambda$ (dimensionless ratio)")
    ax.set_ylabel(r"$v$  (eV)")
    ax.set_title(r"Sub-mm gravity bound: $\sqrt{\lambda}\,v > 1/\ell_\perp$")
    ax.set_xlim(lam.min(), lam.max())
    ax.set_ylim(1e-6, 1e15)
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()

    out_dir = os.path.join(os.path.dirname(__file__), "figures")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "gravity_bound.png")
    fig.savefig(out, dpi=140)
    print(f"wrote {out}")
    print()
    print("Numerical headline (Lee et al. 2020):")
    print(f"  sqrt(lambda) v  >  {ell_to_energy(52e-6)*1e3:.3f} meV  (95% CL)")
    print(f"  Equivalent transverse length: ell_perp = 1/(sqrt(lambda) v) < 52 um.")
    print()
    print("Phenomenology: this single product is the only laboratory handle on the")
    print("sigma-model parameters at present.  Breaking the (lambda, v) degeneracy")
    print("requires an independent observable -- radial-mode mass, continuum")
    print("graviton signature, or a tunnelling-rate measurement (Subproblem 7).")


if __name__ == "__main__":
    main()
