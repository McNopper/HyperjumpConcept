# Numerics — companion calculations for `hyperjump.pdf`

This folder turns three of the paper's qualitative claims into runnable code.
Everything here is plain NumPy/SciPy (no GPU, no ML framework required), but
each script is a clean drop-in target for a future PINN / surrogate-model
replacement once the parameter space gets serious.

| Script | Paper item | What it computes |
|---|---|---|
| `geometry.py` | §"Geometric argument" | Chord length `2 R sin(θ/2)` vs. arc length `R θ` on $S^3$, verifies the ~36 % antipodal shortening, dumps a plot. |
| `bounce.py` | Subproblem 7 (tunnelling rate) | Symmetric double-well has no Coleman bounce — computes the correct saddle: kink surface tension $\sigma=(4\sqrt 2/3)\sqrt\lambda v^3$ (analytic + numeric) and the cargo-traversal action $B_{\rm phys}\sim\sigma\cdot(\text{wall worldvolume})$. |
| `localization.py` | Subproblem 3 (SM zero modes) | Kink $\phi_0(r)=v\tanh(\sqrt{2\lambda}vr)$ + numerical solution of the transverse Dirac zero mode with Yukawa profile $m_\Psi=h\phi_0$; cross-checks the analytic $\mathrm{sech}^{h/k}$ profile. |
| `hedgehog.py` | §Skeleton caveat (line ~168) | Global-monopole BVP on $\mathbb R^4$. Shows the angular gradient $1.5f^2/\rho^2$ dominates, giving energy that grows with the IR cutoff — confirming the natural defect is a centred hedgehog, not a thin shell. |
| `kk_spectrum.py` | Subproblem 3 (mass gap) | Pöschl–Teller spectrum of the squared Dirac operator on the kink: analytic levels $E_n^2 = h^2v^2 - k^2(s-n)^2$ vs. finite-difference diagonalization. Plots the KK-like tower vs. Yukawa coupling. |
| `cosmology.py` | Subproblem 1 ($\Phi(\tau)$ dynamics) | Integrates $\ddot\Phi+3H\dot\Phi+U'=0$ with self-consistent Friedmann for $U=\tfrac12 m^2\Phi^2$. Yields ~67 e-folds of quasi-de Sitter then reheating-like oscillations. |
| `gravity_bound.py` | Subproblem 5 (Lee et al. 2020) | Plots the allowed region $\sqrt\lambda\,v > 1/\ell_\perp$ in the $(\lambda,v)$ plane; recovers the 3.8 meV headline. |
| `pinn_hedgehog.py` | Subproblem 2 toolchain | PyTorch PINN for the hedgehog BVP. Boundary conditions baked in via an output transform; cross-checks against `solve_bvp` to ~1e-3 with a tiny MLP. Scaffold for the coupled $(g_{MN},\phi^A)$ problem where no closed-form ansatz works. |
| `pinn_coupled.py` | Subproblem 2 (explicit closure) | PyTorch PINN for the **coupled** 5D Einstein + sigma system in the warped ansatz, using the DeWolfe–Freedman–Gubser–Karch superpotential $W(\phi)=\phi-\phi^3/(3v^2)$. Recovers $\phi_*(r)=v\tanh(r/v)$ and the closed-form warp factor $A_*(r)$ — an explicit self-consistent 5D background of the kind the hyperjump skeleton requires. |
| `symbolic_search.py` | Subproblem 2 ansatz discovery | (i) `gplearn` rediscovers $\phi_0\propto\tanh(kr)$ from sampled kink data; (ii) `sympy` checks candidate warp factors $A(r)$ against the 5D Einstein + scalar equations; (iii) verifies the DFGK superpotential flow $\phi'=W'$, $A'=-W/3$, $V=\tfrac12 W'^2-\tfrac23 W^2$. |
| `test_numerics.py` | — | Regression tests: 13 cases covering all of the above. Run with `python test_numerics.py`. |

## Run

```bash
pip install -r requirements.txt
python geometry.py
python bounce.py
python localization.py
python hedgehog.py
python kk_spectrum.py
python cosmology.py
python gravity_bound.py
python pinn_hedgehog.py    # requires `pip install torch`
python pinn_coupled.py     # requires `pip install torch`
python symbolic_search.py  # requires `pip install gplearn sympy`
python test_numerics.py    # regression tests, 13/13 should pass
```

Each script writes a PNG to `figures/` and prints a short numerical summary.

## What this *doesn't* do

These are the "first-pass closures" the paper itself flags — they do **not**
constitute a self-consistent 5D gravity + Standard-Model-localization
solution, and they do not address chronology protection (Subproblem 6).
They are the cheapest honest numbers one can extract from the skeleton
Lagrangian, and a launchpad for the harder work (PINN solvers for the
coupled $(g_{MN},\phi^A)$ system, SBI on $\lambda, v$ against sub-mm
gravity bounds, automated theorem proving on the bulk causal structure).
