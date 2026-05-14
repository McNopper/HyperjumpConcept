"""Physics-Informed Neural-Network (PINN) solver for the O(4) hedgehog.

Companion to ``hedgehog.py``.  Same boundary-value problem,

    f''(rho) + (3/rho) f'(rho) - 3 f(rho)/rho^2 = 4 lambda f (f^2 - v^2),
    f(0) = 0,      f(R_max) = v,

solved with a small MLP and automatic differentiation in PyTorch instead of
``scipy.integrate.solve_bvp``.  The purpose is twofold:

  1. demonstrate the toolchain needed for the *real* targets the paper
     flags (coupled 5D Einstein + sigma system, where ``solve_bvp`` is
     no longer adequate), and
  2. give a concrete numerical cross-check against the BVP solver so
     regressions in either backend are visible.

We enforce both boundary conditions *exactly* via an output transform:

    f(rho) = (rho / R_max) * v + rho * (R_max - rho) * NN(rho),

so the PINN loss reduces to the residual of the ODE alone.

Run:  python pinn_hedgehog.py
"""
from __future__ import annotations

import math
import os
from typing import Tuple

import numpy as np
import torch
from torch import nn


LAM = 1.0
V = 1.0
K = math.sqrt(2.0 * LAM) * V


class HedgehogPINN(nn.Module):
    def __init__(self, hidden: int = 32, depth: int = 4) -> None:
        super().__init__()
        layers: list[nn.Module] = [nn.Linear(1, hidden), nn.Tanh()]
        for _ in range(depth - 1):
            layers += [nn.Linear(hidden, hidden), nn.Tanh()]
        layers += [nn.Linear(hidden, 1)]
        self.net = nn.Sequential(*layers)
        self.R_max = 20.0 / K
        self.v = V

    def raw(self, rho: torch.Tensor) -> torch.Tensor:
        return self.net(rho).squeeze(-1)

    def forward(self, rho: torch.Tensor) -> torch.Tensor:
        r = rho.squeeze(-1)
        nn_out = self.raw(rho)
        # output transform: f(0) = 0, f(R_max) = v
        return (r / self.R_max) * self.v + r * (self.R_max - r) * nn_out


def residual(model: HedgehogPINN, rho: torch.Tensor) -> torch.Tensor:
    rho.requires_grad_(True)
    f = model(rho)
    grads = torch.autograd.grad(f.sum(), rho, create_graph=True)[0].squeeze(-1)
    fp = grads
    fpp = torch.autograd.grad(fp.sum(), rho, create_graph=True)[0].squeeze(-1)
    r = rho.squeeze(-1)
    res = fpp + 3.0 * fp / r - 3.0 * f / (r * r) - 4.0 * LAM * f * (f * f - V * V)
    return res


def train(seed: int = 0,
          n_collocation: int = 512,
          adam_iters: int = 4000,
          lbfgs_iters: int = 200,
          verbose: bool = True) -> Tuple[HedgehogPINN, list[float]]:
    torch.manual_seed(seed)
    np.random.seed(seed)
    model = HedgehogPINN()
    R_max = model.R_max

    # avoid the rho=0 singularity by sampling on a small offset
    rho_eps = 1e-2 / K

    history: list[float] = []

    optim = torch.optim.Adam(model.parameters(), lr=3e-3)
    for it in range(adam_iters):
        # resample collocation points each step (helps generalisation)
        u = torch.rand(n_collocation, 1)
        rho = rho_eps + (R_max - rho_eps) * u
        optim.zero_grad()
        res = residual(model, rho)
        loss = (res * res).mean()
        loss.backward()
        optim.step()
        if verbose and (it % 500 == 0 or it == adam_iters - 1):
            history.append(float(loss.detach()))
            print(f"  adam  iter {it:5d}   loss = {loss.item():.3e}")

    # L-BFGS polish
    rho_fixed = torch.linspace(rho_eps, R_max, n_collocation).unsqueeze(-1)
    lbfgs = torch.optim.LBFGS(model.parameters(),
                              lr=1.0, max_iter=lbfgs_iters,
                              tolerance_grad=1e-9, tolerance_change=1e-12,
                              history_size=50, line_search_fn="strong_wolfe")

    def closure():
        lbfgs.zero_grad()
        res = residual(model, rho_fixed.clone())
        loss = (res * res).mean()
        loss.backward()
        return loss

    final = lbfgs.step(closure)
    if verbose:
        print(f"  lbfgs final loss = {float(final):.3e}")
    history.append(float(final))

    return model, history


def evaluate(model: HedgehogPINN, n: int = 401) -> Tuple[np.ndarray, np.ndarray]:
    rho_np = np.linspace(1e-3 / K, model.R_max, n)
    rho = torch.tensor(rho_np, dtype=torch.float32).unsqueeze(-1)
    with torch.no_grad():
        f = model(rho).numpy()
    return rho_np, f


def main() -> None:
    print("PINN solver for the O(4) hedgehog BVP")
    print(f"  lambda = {LAM},  v = {V},  k = sqrt(2 lam) v = {K:.4f}")
    print(f"  R_max  = {20.0/K:.2f} = 20/k")
    print()

    model, _ = train()
    print()

    rho, f_pinn = evaluate(model)

    # compare against solve_bvp from hedgehog.py
    from scipy.integrate import solve_bvp
    from hedgehog import ode, bc

    rho_bvp = np.linspace(1e-3 / K, 20.0 / K, 400)
    y0 = np.vstack([V * np.tanh(K * rho_bvp), V * K / np.cosh(K * rho_bvp) ** 2])
    sol = solve_bvp(ode, bc, rho_bvp, y0, tol=1e-7, max_nodes=20000)
    assert sol.success, sol.message
    f_bvp = sol.sol(rho)[0]

    err = np.max(np.abs(f_pinn - f_bvp))
    rms = float(np.sqrt(np.mean((f_pinn - f_bvp) ** 2)))
    print(f"max |f_PINN - f_BVP| = {err:.3e}")
    print(f"rms |f_PINN - f_BVP| = {rms:.3e}")
    print(f"PINN  f(R_max)      = {f_pinn[-1]:.6f}  (BC-exact, should be {V})")
    print(f"BVP   f(R_max)      = {f_bvp[-1]:.6f}")

    # plot
    try:
        import matplotlib.pyplot as plt
        out_dir = os.path.join(os.path.dirname(__file__), "figures")
        os.makedirs(out_dir, exist_ok=True)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
        ax1.plot(rho * K, f_bvp / V, "k-", label="solve_bvp")
        ax1.plot(rho * K, f_pinn / V, "C1--", label="PINN")
        ax1.set_xlabel(r"$\sqrt{2\lambda}\,v\,\rho$")
        ax1.set_ylabel(r"$f(\rho)/v$")
        ax1.set_title("Hedgehog profile: PINN vs. BVP")
        ax1.grid(alpha=0.3)
        ax1.legend()
        ax2.semilogy(rho * K, np.abs(f_pinn - f_bvp) + 1e-16, "C3-")
        ax2.set_xlabel(r"$\sqrt{2\lambda}\,v\,\rho$")
        ax2.set_ylabel("absolute pointwise error")
        ax2.set_title(f"max err = {err:.2e}")
        ax2.grid(alpha=0.3, which="both")
        fig.tight_layout()
        out = os.path.join(out_dir, "pinn_hedgehog.png")
        fig.savefig(out, dpi=140)
        print(f"wrote {out}")
    except Exception as e:
        print(f"(matplotlib output skipped: {e})")


if __name__ == "__main__":
    main()
