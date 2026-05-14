# Numerics — companion calculations for `hyperjump.pdf`

This folder turns three of the paper's qualitative claims into runnable code.
Everything here is plain NumPy/SciPy (no GPU, no ML framework required), but
each script is a clean drop-in target for a future PINN / surrogate-model
replacement once the parameter space gets serious.

| Script | Paper item | What it computes |
|---|---|---|
| `geometry.py` | §"Geometric argument" | Chord length `2 R sin(θ/2)` vs. arc length `R θ` on $S^3$, verifies the ~36 % antipodal shortening, dumps a plot. |
| `bounce.py` | Subproblem 7 (tunnelling rate) | O(d)-symmetric Coleman bounce action $B$ for $V(\phi)=\lambda(|\phi|^2-v^2)^2$ via shooting, in $d=5$ Euclidean. Gives $\Gamma/\mathcal V_5 \sim \mu^5 e^{-B}$. |
| `localization.py` | Subproblem 3 (SM zero modes) | Kink background $\phi_0(r)=v\tanh(\sqrt{2\lambda}\,v\,r)$ + numerical solution of the transverse Dirac zero mode with Yukawa profile $m_\Psi=h\phi_0$. Cross-checks the analytic $\mathrm{sech}^{h/(\sqrt{2\lambda}v)}$ profile. |

## Run

```bash
pip install -r requirements.txt
python geometry.py
python bounce.py
python localization.py
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
