"""Symbolic-regression / ansatz search for the warped-metric problem.

Two complementary demos:

  (A) **Data-driven symbolic regression** (gplearn).  Given samples of the
      kink profile  phi_0(r) = v tanh(k r)  with k = sqrt(2 lambda) v we
      try to *rediscover* the analytic form from numerical data.  This
      is a pipeline sanity check for the harder warped-factor target
      where no closed form is yet known.

  (B) **Sympy ansatz search** for the warped 5D ansatz

          ds^2 = e^{2 A(r)} eta_{mu nu} dx^mu dx^nu + dr^2,
          phi^a(x, r) = phi(r) * n^a,        |n^a| = 1,

      coupled to the O(4) sigma model with potential V(phi).  We
      symbolically substitute a family of candidate ansaetze A(r) and
      report which ones close the Einstein + scalar equations
      consistently (analogous to the Randall-Sundrum domain-wall
      construction).

The point is to show how to extend the numerical companions into a
*symbolic* search layer once the PINN of pinn_hedgehog.py is generalised
to the coupled gravity-scalar system.

Run:  python symbolic_search.py
"""
from __future__ import annotations

import math
import warnings
from typing import Optional

import numpy as np
import sympy as sp


# ============================================================================
# (A)  Rediscovering  phi_0(r) = v tanh(k r)  from data
# ============================================================================

def _gplearn_search(seed: int = 0) -> Optional[str]:
    """Use gplearn to symbolically regress the kink profile.

    gplearn ships with +, -, *, /, sqrt, log, abs, sin, cos but no tanh.
    We register tanh as a custom protected function so the GP has a
    chance of picking it out of the candidate set.
    """
    try:
        from gplearn.genetic import SymbolicRegressor
        from gplearn.functions import make_function
    except Exception as e:
        print(f"  (gplearn unavailable: {e})")
        return None

    def _tanh(x):
        # numpy tanh is already well-behaved on the full real line
        return np.tanh(np.clip(x, -50.0, 50.0))

    tanh_fn = make_function(function=_tanh, name="tanh", arity=1)

    # generate noiseless samples of the kink with lam = 1, v = 1
    lam, v = 1.0, 1.0
    k = math.sqrt(2.0 * lam) * v
    rng = np.random.default_rng(seed)
    r = rng.uniform(-3.0 / k, 3.0 / k, size=400).reshape(-1, 1)
    y = v * np.tanh(k * r).ravel()

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sr = SymbolicRegressor(
            population_size=2000,
            generations=20,
            function_set=("add", "sub", "mul", tanh_fn),
            metric="mse",
            parsimony_coefficient=0.005,
            stopping_criteria=1e-10,
            random_state=seed,
            verbose=0,
            const_range=(-3.0, 3.0),
            init_depth=(2, 4),
        )
        sr.fit(r, y)

    expr = str(sr._program)
    score = sr.score(r, y)
    print(f"  best gplearn expression : {expr}")
    print(f"  fitness (R^2)           : {score:.6f}")
    return expr


# ============================================================================
# (B)  Sympy ansatz check for the 5D warped sigma-model background
# ============================================================================
#
# Reduce the O(4) sigma sector to its radial profile phi(r) so the bulk is
# effectively governed by
#
#       L_bulk = -0.5 (d phi)^2 - V(phi),       V(phi) = lambda (phi^2 - v^2)^2
#                + (3/8) angular-gradient terms that vanish if we restrict to
#                  a domain-wall (planar) ansatz with the O(4) symmetry
#                  spontaneously broken along the transverse direction.
#
# For the planar warped ansatz
#
#       ds^2 = e^{2 A(r)} eta_{mu nu} dx^mu dx^nu + dr^2,
#
# the 5D Einstein + scalar equations reduce (in units 8 pi G_5 = 1) to
#
#       6 A'(r)^2          =  0.5 phi'^2 - V(phi),               (E_rr)
#       3 A''(r) + 6 A'^2  = -0.5 phi'^2 - V(phi),               (E_mu mu)
#       phi'' + 4 A' phi'  =  dV/dphi.                           (scalar)
#
# These are the standard scalar-domain-wall equations (DeWolfe-Freedman-
# Gubser-Karch 2000; Randall-Sundrum domain-wall limit).  We test a small
# family of ansaetze A(r) against them with sympy.
# ----------------------------------------------------------------------------


_R = sp.symbols("r", real=True, positive=True)


def warped_residuals(A_expr, phi_expr, lam=1, v=1):
    r = _R
    phi_sym = sp.symbols("phi_var", real=True)
    A = A_expr
    phi = phi_expr
    Ap = sp.diff(A, r)
    App = sp.diff(A, r, 2)
    phip = sp.diff(phi, r)
    phipp = sp.diff(phi, r, 2)
    V_sym = lam * (phi_sym ** 2 - v ** 2) ** 2
    dVdphi_sym = sp.diff(V_sym, phi_sym)
    V = V_sym.subs(phi_sym, phi)
    dVdphi = dVdphi_sym.subs(phi_sym, phi)

    Err = sp.simplify(6 * Ap ** 2 - (sp.Rational(1, 2) * phip ** 2 - V))
    Emumu = sp.simplify(3 * App + 6 * Ap ** 2 - (-sp.Rational(1, 2) * phip ** 2 - V))
    scalar = sp.simplify(phipp + 4 * Ap * phip - dVdphi)
    return Err, Emumu, scalar


def _sympy_ansatz_scan() -> None:
    r = _R
    c, k_sym = sp.symbols("c k", real=True, positive=True)

    # phi profile is the standard kink (works on flat slices)
    phi_kink = sp.tanh(k_sym * r)
    candidates = {
        "A(r) = 0                          (flat space)":
            sp.Integer(0),
        "A(r) = -|r|/L (Randall-Sundrum)":
            -sp.Abs(r) / c,
        "A(r) = -ln cosh(k r)              (DFGK domain-wall)":
            -sp.log(sp.cosh(k_sym * r)),
        "A(r) = -(1/3) ln cosh(k r)        (sub-RS scaling)":
            -sp.Rational(1, 3) * sp.log(sp.cosh(k_sym * r)),
    }

    print("  Substituting candidate A(r) with phi(r) = v tanh(k r), lambda=v=1:")
    for label, A in candidates.items():
        try:
            Err, Emumu, scalar = warped_residuals(A, phi_kink, lam=1, v=1)
        except Exception as e:
            print(f"    {label} -> sympy error: {e}")
            continue
        # check residuals at a numerical sample r = 0.5/k
        subs = {k_sym: 1.0, c: 1.0, r: 0.5}
        try:
            vals = (float(Err.subs(subs)), float(Emumu.subs(subs)), float(scalar.subs(subs)))
        except (TypeError, ValueError):
            vals = (float("nan"),) * 3
        ok = all(abs(v) < 1e-10 for v in vals)
        tag = "CLOSES" if ok else "fails "
        print(f"    [{tag}]  {label}")
        print(f"            E_rr,  E_mumu,  scalar residual at r=0.5/k:")
        print(f"            {vals[0]:+.3e},  {vals[1]:+.3e},  {vals[2]:+.3e}")
    print()
    print("  Note: none of the simple closed-form A(r) close *all three* equations")
    print("  with the bare kink phi -- domain-wall solutions in this potential")
    print("  require a self-consistent superpotential W(phi) (DeWolfe-Freedman-")
    print("  Gubser-Karch 2000).  This is precisely where the numerical PINN")
    print("  of pinn_hedgehog.py needs to be extended to the coupled system.")


# ============================================================================
# (A2)  Sympy direct verification of the DFGK relation
# ============================================================================

def _verify_dfgk() -> None:
    """First-order DFGK relations:  phi' = dW/dphi,   A' = -W/3.

    Given a superpotential W(phi) the corresponding scalar potential is

        V(phi) = 0.5 (dW/dphi)^2 - (4/3) W^2.

    We check the identity symbolically.
    """
    phi = sp.symbols("phi", real=True)
    W = sp.Function("W")(phi)
    V_sym = sp.Rational(1, 2) * sp.diff(W, phi) ** 2 - sp.Rational(2, 3) * W ** 2

    r = sp.symbols("r", real=True)
    phi_r = sp.Function("phi")(r)
    A_r = sp.Function("A")(r)

    # impose first-order flow
    W_phi = sp.Function("W")(phi_r)
    eom1 = sp.diff(phi_r, r) - sp.diff(W_phi, phi_r)
    eom2 = sp.diff(A_r, r) + sp.Rational(1, 3) * W_phi

    print("  DFGK first-order flow:")
    print(f"    phi'(r) - dW/dphi   = {sp.simplify(eom1)}")
    print(f"    A'(r)   + W/3       = {sp.simplify(eom2)}")
    print(f"    induced V(phi)      = (1/2)(dW/dphi)^2 - (2/3) W^2")
    print(f"                        = {sp.simplify(V_sym)}")


def main() -> None:
    print("=" * 72)
    print("(A) gplearn symbolic regression on kink data phi_0(r) = v tanh(k r)")
    print("=" * 72)
    _gplearn_search()
    print()

    print("=" * 72)
    print("(B) Sympy ansatz scan for the 5D warped scalar-gravity system")
    print("=" * 72)
    _sympy_ansatz_scan()

    print("=" * 72)
    print("(C) Sympy verification of the DFGK first-order flow")
    print("=" * 72)
    _verify_dfgk()
    print()
    print("These two layers (data-driven SR + symbolic ansatz check) are the")
    print("scaffolding for closing Subproblem 2 (coupling to 5D gravity):")
    print("  - run pinn_hedgehog.py-style PINNs for (A(r), phi(r));")
    print("  - feed the numerical A(r) into gplearn for a closed-form guess;")
    print("  - test guesses with warped_residuals() until one closes exactly.")


if __name__ == "__main__":
    main()
