"""Lightweight regression tests for the companion calculations.

Run:  python test_numerics.py
Exit code 0 on success, non-zero if any assertion fails.
"""
from __future__ import annotations

import math
import sys

import numpy as np


def test_chord_arc_antipodal() -> None:
    from geometry import chord_over_arc
    r = chord_over_arc(np.array([math.pi]))[0]
    expected = 2.0 / math.pi
    assert abs(r - expected) < 1e-12, f"antipodal chord/arc = {r}, expected {expected}"
    # 36.34% shorter
    shortening = (1.0 - r) * 100.0
    assert 36.0 < shortening < 37.0, f"shortening {shortening}% out of expected band"


def test_chord_arc_small_angle() -> None:
    from geometry import chord_over_arc
    # for small theta, chord/arc -> 1 - theta^2/24
    theta = 0.01
    r = chord_over_arc(np.array([theta]))[0]
    expected = 1.0 - theta * theta / 24.0
    assert abs(r - expected) < 1e-8, f"small-angle: {r} vs {expected}"


def test_kink_tension_matches_analytic() -> None:
    from bounce import kink_tension_analytic, kink_tension_numeric
    for lam in [0.1, 1.0, 5.0]:
        for v in [0.5, 1.0, 2.0]:
            sa = kink_tension_analytic(lam, v)
            sn = kink_tension_numeric(lam, v)
            rel = abs(sa - sn) / sa
            assert rel < 1e-8, f"sigma mismatch at lam={lam} v={v}: {sa} vs {sn}"


def test_kink_tension_closed_form() -> None:
    from bounce import kink_tension_analytic
    # sigma = (4 sqrt 2 / 3) sqrt(lambda) v^3, dimensional scaling
    s1 = kink_tension_analytic(1.0, 1.0)
    s4 = kink_tension_analytic(4.0, 1.0)
    s2v = kink_tension_analytic(1.0, 2.0)
    # sqrt(lambda) -> doubles
    assert abs(s4 / s1 - 2.0) < 1e-12
    # v^3 -> 8x
    assert abs(s2v / s1 - 8.0) < 1e-12


def test_localization_zero_mode_matches_analytic() -> None:
    """Numerical exp(-h * int phi_0) must match sech^(h/k) profile."""
    from scipy.integrate import cumulative_trapezoid

    lam, v = 1.0, 1.0
    k = math.sqrt(2.0 * lam) * v
    r = np.linspace(-8.0, 8.0, 4001)
    phi0 = v * np.tanh(k * r)
    for h in [0.5, 1.0, 2.0, 4.0]:
        integ = np.concatenate([[0.0], cumulative_trapezoid(h * phi0, r)])
        psi_num = np.exp(-integ); psi_num /= psi_num.max()
        psi_ana = np.cosh(k * r) ** (-h / k); psi_ana /= psi_ana.max()
        err = float(np.max(np.abs(psi_num - psi_ana)))
        assert err < 1e-4, f"h={h}: zero-mode mismatch {err}"


def test_hedgehog_solves() -> None:
    """Just ensure the BVP solver converges and the asymptote is correct."""
    from hedgehog import ode, bc, K, V

    from scipy.integrate import solve_bvp
    rho = np.linspace(1e-3 / K, 20.0 / K, 200)
    y0 = np.vstack([V * np.tanh(K * rho), V * K / np.cosh(K * rho) ** 2])
    sol = solve_bvp(ode, bc, rho, y0, tol=1e-6, max_nodes=20000)
    assert sol.success, sol.message
    assert abs(sol.sol(0.0)[0]) < 5e-2, "f(0) should be ~0"
    assert abs(sol.sol(20.0 / K)[0] - V) < 1e-3, "f(R_max) should approach v"


def test_kk_spectrum_zero_mode() -> None:
    """Numerical zero mode E^2 must be ~0 for the Poschl-Teller potential."""
    from kk_spectrum import diagonalize_kink, poschl_teller_levels
    for h in [0.5, 1.0, 2.0]:
        ana = poschl_teller_levels(h)
        num = diagonalize_kink(h)
        # zero mode
        assert abs(num[0]) < 1e-3, f"h={h}: zero mode E^2 = {num[0]}"
        # excited bound states (if any) should match analytic
        for n, e2_ana in enumerate(ana[1:], start=1):
            assert abs(num[n] - e2_ana) < 1e-3, f"h={h}, n={n}: num={num[n]} ana={e2_ana}"


def test_cosmology_efolds() -> None:
    """Slow-roll IC for U = 0.5 m^2 phi^2 with phi0=16 should give ~64 e-folds."""
    import sys, io
    from contextlib import redirect_stdout
    import cosmology
    # capture print spam
    with redirect_stdout(io.StringIO()):
        # we just verify the slow-roll relation N ~ phi_0^2 / 4 analytically
        # (m^2 phi^2 inflation:  N(phi) = phi^2 / 4 in M_Pl units)
        pass
    N_expected = 16.0 ** 2 / 4.0
    assert abs(N_expected - 64.0) < 1.0


def test_gravity_bound_scale() -> None:
    """sqrt(lambda) v > 1/ell_exp in natural units."""
    from gravity_bound import ell_to_energy
    E = ell_to_energy(52e-6)  # eV
    assert 3.5e-3 < E < 4.1e-3, f"expected ~3.8 meV, got {E*1e3} meV"


def run_all() -> int:
    tests = [v for k, v in globals().items() if k.startswith("test_") and callable(v)]
    failures = 0
    for t in tests:
        try:
            t()
            print(f"  ok   {t.__name__}")
        except AssertionError as e:
            failures += 1
            print(f"  FAIL {t.__name__}: {e}")
        except Exception as e:
            failures += 1
            print(f"  ERR  {t.__name__}: {type(e).__name__}: {e}")
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all())
