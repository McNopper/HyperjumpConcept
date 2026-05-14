"""Chord vs. arc on S^3 embedded in R^4.

Verifies the paper's geometric claim:
  arc  length = R * theta
  chord length = 2 R sin(theta/2)
  antipodal (theta=pi): chord/arc = 2/pi ~ 0.6366  (i.e. ~36% shorter)

Run:  python geometry.py
"""
from __future__ import annotations

import os
import numpy as np
import matplotlib.pyplot as plt


def chord_over_arc(theta: np.ndarray) -> np.ndarray:
    """Ratio chord/arc for a great-circle separation theta on S^3.

    The radius R cancels: 2 sin(theta/2) / theta.
    """
    with np.errstate(invalid="ignore", divide="ignore"):
        r = np.where(theta == 0.0, 1.0, 2.0 * np.sin(theta / 2.0) / theta)
    return r


def main() -> None:
    theta = np.linspace(1e-6, np.pi, 400)
    ratio = chord_over_arc(theta)

    antipodal = chord_over_arc(np.array([np.pi]))[0]
    print(f"chord/arc at theta=pi (antipodal): {antipodal:.6f}")
    print(f"chord is {(1.0 - antipodal) * 100:.2f}% shorter than arc")
    print(f"chord/arc at theta=pi/2          : {chord_over_arc(np.array([np.pi/2]))[0]:.6f}")
    print(f"chord/arc at theta=pi/6          : {chord_over_arc(np.array([np.pi/6]))[0]:.6f}")

    out_dir = os.path.join(os.path.dirname(__file__), "figures")
    os.makedirs(out_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(theta, ratio, label=r"chord / arc $= 2\sin(\theta/2)/\theta$")
    ax.axhline(2 / np.pi, ls="--", color="C1",
               label=fr"antipodal $= 2/\pi \approx {2/np.pi:.4f}$")
    ax.set_xlabel(r"great-circle separation $\theta$ on $S^3$ (rad)")
    ax.set_ylabel("chord / arc")
    ax.set_xlim(0, np.pi)
    ax.set_ylim(0.6, 1.0)
    ax.set_title("Bulk chord vs. on-brane arc length (radius cancels)")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    out = os.path.join(out_dir, "chord_vs_arc.png")
    fig.savefig(out, dpi=140)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
