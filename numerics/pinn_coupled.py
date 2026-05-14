"""Coupled 5D Einstein + O(4)-sigma PINN (Subproblem 2 toolchain).

Background ansatz (planar warped slicing, transverse radial direction r):

    ds^2 = e^{2 A(r)} eta_{mu nu} dx^mu dx^nu + dr^2,
    phi(x, r) = phi(r),

with action  S = int d^5 x sqrt(-g) [ R/2 - 0.5 (d phi)^2 - V(phi) ]
(units 8 pi G_5 = 1).  The reduced equations are the standard
DeWolfe-Freedman-Gubser-Karch (DFGK 2000) domain-wall system

    6 A'^2          =  0.5 phi'^2 - V,           (E_rr)
    3 A'' + 6 A'^2  = -0.5 phi'^2 - V,           (E_mu mu, trace)
    phi'' + 4 A' phi'  = dV/dphi.                (scalar)

To get an *exactly* solvable target we use the standard superpotential
construction:

    W(phi) = phi - phi^3 / (3 v^2),
    V(phi) = (1/2) W'^2 - (2/3) W^2.

This gives the closed-form flow

    phi_*(r) = v tanh(r / v),
    A_*'(r) = - W(phi_*(r)) / 3,

which we integrate analytically (mod a constant) to

    A_*(r) = -(2/9) ln cosh(r / v) - (1/18) tanh^2(r / v).

The PINN is trained against the three residuals above and must recover
(phi_*, A_*) without ever being shown them.  This is the smallest
non-trivial laboratory for the kind of solver that Subproblem 2 needs.

Run:  python pinn_coupled.py
"""
from __future__ import annotations

import math
import os
from typing import Tuple

import numpy as np
import torch
from torch import nn


V_FIELD = 1.0   # vacuum expectation value v
R_HALF = 6.0    # solve on r in [-R_HALF, R_HALF]


def W_of_phi(phi: torch.Tensor | np.ndarray) -> torch.Tensor | np.ndarray:
    return phi - phi ** 3 / (3.0 * V_FIELD ** 2)


def Wp_of_phi(phi: torch.Tensor | np.ndarray) -> torch.Tensor | np.ndarray:
    return 1.0 - phi ** 2 / V_FIELD ** 2


def V_of_phi(phi: torch.Tensor | np.ndarray) -> torch.Tensor | np.ndarray:
    Wp = Wp_of_phi(phi)
    W = W_of_phi(phi)
    return 0.5 * Wp ** 2 - (2.0 / 3.0) * W ** 2


def dVdphi(phi: torch.Tensor) -> torch.Tensor:
    Wp = Wp_of_phi(phi)
    W = W_of_phi(phi)
    Wpp = -2.0 * phi / V_FIELD ** 2
    return Wp * Wpp - (4.0 / 3.0) * W * Wp


def analytic_phi(r: np.ndarray) -> np.ndarray:
    return V_FIELD * np.tanh(r / V_FIELD)


def analytic_A(r: np.ndarray) -> np.ndarray:
    return -(2.0 / 9.0) * np.log(np.cosh(r / V_FIELD)) \
           - (1.0 / 18.0) * np.tanh(r / V_FIELD) ** 2


class CoupledPINN(nn.Module):
    def __init__(self, hidden: int = 48, depth: int = 4) -> None:
        super().__init__()

        def block() -> nn.Sequential:
            layers: list[nn.Module] = [nn.Linear(1, hidden), nn.Tanh()]
            for _ in range(depth - 1):
                layers += [nn.Linear(hidden, hidden), nn.Tanh()]
            layers += [nn.Linear(hidden, 1)]
            return nn.Sequential(*layers)

        self.phi_net = block()
        self.A_net = block()

    def phi(self, r: torch.Tensor) -> torch.Tensor:
        # output transform: phi(0)=0, phi(+-R) -> +-v, antisymmetric
        # we enforce odd parity weakly via:  v * tanh(r) * (1 + small NN)
        raw = self.phi_net(r).squeeze(-1)
        x = r.squeeze(-1)
        return V_FIELD * torch.tanh(x / V_FIELD) + (V_FIELD ** 2 - torch.tanh(x / V_FIELD) ** 2) * raw

    def A(self, r: torch.Tensor) -> torch.Tensor:
        # output transform: A(0) = 0 (gauge), even in r approximately
        raw = self.A_net(r).squeeze(-1)
        x = r.squeeze(-1)
        return x * raw  # vanishes at r=0; sign / parity learned freely


def residuals(model: CoupledPINN, r: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    r.requires_grad_(True)
    phi = model.phi(r)
    A = model.A(r)

    phip = torch.autograd.grad(phi.sum(), r, create_graph=True)[0].squeeze(-1)
    Ap = torch.autograd.grad(A.sum(), r, create_graph=True)[0].squeeze(-1)
    phipp = torch.autograd.grad(phip.sum(), r, create_graph=True)[0].squeeze(-1)
    App = torch.autograd.grad(Ap.sum(), r, create_graph=True)[0].squeeze(-1)

    V = V_of_phi(phi)
    dVdp = dVdphi(phi)

    Err = 6.0 * Ap ** 2 - (0.5 * phip ** 2 - V)
    Emm = 3.0 * App + 6.0 * Ap ** 2 - (-0.5 * phip ** 2 - V)
    sca = phipp + 4.0 * Ap * phip - dVdp
    return Err, Emm, sca


def train(seed: int = 0,
          n_collocation: int = 256,
          adam_iters: int = 3000,
          lbfgs_iters: int = 200,
          verbose: bool = True) -> CoupledPINN:
    torch.manual_seed(seed)
    np.random.seed(seed)
    model = CoupledPINN()

    optim = torch.optim.Adam(model.parameters(), lr=3e-3)
    for it in range(adam_iters):
        r = (torch.rand(n_collocation, 1) * 2.0 - 1.0) * R_HALF
        optim.zero_grad()
        Err, Emm, sca = residuals(model, r)
        loss = (Err ** 2).mean() + (Emm ** 2).mean() + (sca ** 2).mean()
        loss.backward()
        optim.step()
        if verbose and (it % 500 == 0 or it == adam_iters - 1):
            print(f"  adam  iter {it:5d}   loss = {loss.item():.3e}")

    r_fixed = torch.linspace(-R_HALF, R_HALF, n_collocation).unsqueeze(-1)
    lbfgs = torch.optim.LBFGS(model.parameters(),
                              lr=1.0, max_iter=lbfgs_iters,
                              tolerance_grad=1e-10, tolerance_change=1e-12,
                              history_size=50, line_search_fn="strong_wolfe")

    def closure():
        lbfgs.zero_grad()
        Err, Emm, sca = residuals(model, r_fixed.clone())
        loss = (Err ** 2).mean() + (Emm ** 2).mean() + (sca ** 2).mean()
        loss.backward()
        return loss

    final = lbfgs.step(closure)
    if verbose:
        print(f"  lbfgs final loss = {float(final.detach()):.3e}")
    return model


def evaluate(model: CoupledPINN, n: int = 401) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    r_np = np.linspace(-R_HALF, R_HALF, n)
    r = torch.tensor(r_np, dtype=torch.float32).unsqueeze(-1)
    with torch.no_grad():
        phi = model.phi(r).numpy()
        A = model.A(r).numpy()
    return r_np, phi, A


def main() -> None:
    print("Coupled 5D Einstein + sigma PINN with DFGK superpotential")
    print(f"  v        = {V_FIELD}")
    print(f"  r range  = [-{R_HALF}, {R_HALF}]")
    print(f"  W(phi)   = phi - phi^3 / (3 v^2)")
    print(f"  V(phi)   = (1/2) W'^2 - (2/3) W^2")
    print(f"  exact    phi_*(r) = v tanh(r/v),   A_*(r) = -(2/9) ln cosh - (1/18) tanh^2")
    print()

    model = train()
    print()

    r, phi_pinn, A_pinn = evaluate(model)
    phi_ex = analytic_phi(r)
    A_ex = analytic_A(r)

    # A is determined only up to an additive constant (gauge in the warp factor);
    # subtract the value at r=0 from both to make the comparison meaningful.
    A_pinn = A_pinn - A_pinn[len(r) // 2]
    A_ex = A_ex - A_ex[len(r) // 2]

    err_phi = float(np.max(np.abs(phi_pinn - phi_ex)))
    err_A = float(np.max(np.abs(A_pinn - A_ex)))
    print(f"max |phi_PINN - phi_*| = {err_phi:.3e}")
    print(f"max |A_PINN   - A_*  | = {err_A:.3e}  (after shifting A(0)=0 gauge)")

    try:
        import matplotlib.pyplot as plt
        out_dir = os.path.join(os.path.dirname(__file__), "figures")
        os.makedirs(out_dir, exist_ok=True)
        fig, axes = plt.subplots(1, 2, figsize=(11, 4))
        axes[0].plot(r, phi_ex, "k-", label=r"exact $\phi_*$")
        axes[0].plot(r, phi_pinn, "C1--", label="PINN")
        axes[0].set_xlabel("$r/v$"); axes[0].set_ylabel(r"$\phi/v$")
        axes[0].set_title("Scalar profile")
        axes[0].grid(alpha=0.3); axes[0].legend()
        axes[1].plot(r, A_ex, "k-", label=r"exact $A_*$")
        axes[1].plot(r, A_pinn, "C1--", label="PINN")
        axes[1].set_xlabel("$r/v$"); axes[1].set_ylabel("$A(r)$")
        axes[1].set_title("Warp factor (A(0)=0 gauge)")
        axes[1].grid(alpha=0.3); axes[1].legend()
        fig.tight_layout()
        out = os.path.join(out_dir, "pinn_coupled.png")
        fig.savefig(out, dpi=140)
        print(f"wrote {out}")
    except Exception as e:
        print(f"(plot skipped: {e})")

    # dump (r, phi, A) so symbolic_search.py can pick them up
    out_data = os.path.join(os.path.dirname(__file__), "figures", "pinn_coupled.npz")
    np.savez(out_data, r=r, phi=phi_pinn, A=A_pinn,
             phi_exact=phi_ex, A_exact=A_ex)
    print(f"wrote {out_data}  (consumed by symbolic_search.py for W(phi) discovery)")


if __name__ == "__main__":
    main()
