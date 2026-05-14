"""Global-monopole hedgehog in the O(4) sigma model on flat R^4.

The paper notes (sec. 'A Candidate Dynamical Skeleton') that the *natural*
codimension-four defect of the O(4)-symmetric Lagrangian on flat R^4 is a
hedgehog centred at |X|=0, not a thin shell at |X|=R_geom.  This script
makes that observation quantitative.

Hedgehog ansatz:
    phi^A(X) = f(rho) * X^A / rho,         rho = |X|.

Substituting into  L = 0.5 (d phi)^2 + lambda (|phi|^2 - v^2)^2  in flat
R^4 and integrating over the angles of S^3 (Omega_3 = 2 pi^2) gives the
radial equation

    f'' + (3/rho) f' - 3 f / rho^2 = 4 lambda f (f^2 - v^2)

with boundary conditions f(0) = 0 (regularity) and f(infty) = v (vacuum).

The defect energy *per global monopole* in this dimensionality is

    E_monopole = 2 pi^2 * integral_0^inf [ 0.5 f'^2 + 1.5 f^2/rho^2
                                          + lambda (f^2 - v^2)^2 ] rho^3 drho.

The 1.5 f^2/rho^2 term comes from the angular gradient and is what makes
the defect *delocalized* (the integrand falls only as 1/rho at large rho
in the absence of gauge fields, giving a logarithmically growing energy
inside a box).  This is precisely why pinning the brane at finite |X| in
the SpacetimeTheory framework requires extra dynamics (Subproblem 1, 2).

We solve the BVP with scipy.integrate.solve_bvp.

Run:  python hedgehog.py
"""
from __future__ import annotations

import os
import numpy as np
from scipy.integrate import solve_bvp, quad
import matplotlib.pyplot as plt


LAM = 1.0
V = 1.0
K = np.sqrt(2.0 * LAM) * V  # natural inverse-length scale


def ode(rho: np.ndarray, y: np.ndarray) -> np.ndarray:
    f, fp = y
    # avoid 1/rho singularity at rho=0 by regularization
    safe_rho = np.where(rho < 1e-6, 1e-6, rho)
    fpp = 4.0 * LAM * f * (f * f - V * V) + 3.0 * f / safe_rho ** 2 - 3.0 * fp / safe_rho
    return np.vstack([fp, fpp])


def bc(ya: np.ndarray, yb: np.ndarray) -> np.ndarray:
    # f(0) = 0,  f(R_max) = v
    return np.array([ya[0], yb[0] - V])


def main() -> None:
    R_max = 20.0 / K
    rho = np.linspace(1e-3 / K, R_max, 400)
    # initial guess: f = v tanh(K rho)
    y0 = np.vstack([V * np.tanh(K * rho), V * K / np.cosh(K * rho) ** 2])
    sol = solve_bvp(ode, bc, rho, y0, tol=1e-7, max_nodes=20000)
    if not sol.success:
        raise SystemExit(f"BVP failed: {sol.message}")

    print(f"Hedgehog profile solved on rho in [0, {R_max:.2f}],  status: {sol.message}")
    print(f"  f(0)               = {sol.sol(0.0)[0]:.3e}    (should be 0)")
    print(f"  f(R_max)           = {sol.sol(R_max)[0]:.6f}  (should be {V})")
    print(f"  core size 1/k      = {1.0/K:.3f}")

    # energy density and total energy inside a box of radius R
    def integrand(rho_):
        f, fp = sol.sol(rho_)
        kinetic_radial = 0.5 * fp * fp
        kinetic_angular = 1.5 * f * f / (rho_ * rho_)
        potential = LAM * (f * f - V * V) ** 2
        return (kinetic_radial + kinetic_angular + potential) * rho_ ** 3

    omega3 = 2.0 * np.pi ** 2  # surface area of unit S^3

    for R_box in [2.0 / K, 5.0 / K, 10.0 / K, 18.0 / K]:
        E, _ = quad(integrand, 1e-3 / K, R_box, limit=400)
        E *= omega3
        print(f"  E_monopole(rho<{R_box*K:.0f}/k) = {E:.4f}  (linear growth in R from angular gradient)")

    # show that the angular gradient piece dominates at large rho
    rho_grid = np.linspace(0.1 / K, R_max, 600)
    f_grid = sol.sol(rho_grid)[0]
    fp_grid = sol.sol(rho_grid)[1]
    grad_radial = 0.5 * fp_grid ** 2
    grad_angular = 1.5 * f_grid ** 2 / rho_grid ** 2
    potential = LAM * (f_grid ** 2 - V * V) ** 2

    out_dir = os.path.join(os.path.dirname(__file__), "figures")
    os.makedirs(out_dir, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    ax1.plot(rho_grid * K, f_grid / V, "k-", label=r"$f(\rho)/v$")
    ax1.axhline(1.0, ls=":", color="grey")
    ax1.set_xlabel(r"$\sqrt{2\lambda}\,v\,\rho$")
    ax1.set_ylabel(r"$f(\rho)/v$")
    ax1.set_title("Hedgehog radial profile on $\\mathbb{R}^4$")
    ax1.grid(alpha=0.3)
    ax1.legend()

    ax2.semilogy(rho_grid * K, grad_radial, label=r"$\frac{1}{2} f'^2$ (radial)")
    ax2.semilogy(rho_grid * K, grad_angular, label=r"$3 f^2/(2\rho^2)$ (angular)")
    ax2.semilogy(rho_grid * K, potential + 1e-30, label=r"$\lambda (f^2-v^2)^2$")
    ax2.set_xlabel(r"$\sqrt{2\lambda}\,v\,\rho$")
    ax2.set_ylabel("energy-density contributions")
    ax2.set_title("Angular gradient dominates at large $\\rho$")
    ax2.grid(alpha=0.3, which="both")
    ax2.legend()

    fig.tight_layout()
    out = os.path.join(out_dir, "hedgehog.png")
    fig.savefig(out, dpi=140)
    print(f"wrote {out}")
    print()
    print("Conclusion: the natural codimension-4 O(4) defect in flat R^4 is a")
    print("global-monopole hedgehog centred at |X|=0, with energy diverging linearly")
    print("in the IR cutoff R_box (from the 1.5 f^2/rho^2 angular-gradient term).")
    print("It is NOT a thin shell at |X|=R_geom.  Pinning the brane at finite radius")
    print("requires the additional dynamics of Subproblems 1 (cosmic expansion) and")
    print("2 (coupling to 5D gravity) -- consistent with the caveat in the paper.")


if __name__ == "__main__":
    main()
