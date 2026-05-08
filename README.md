# Hyperjump via the Fourth Spatial Dimension

**Author:** Norbert Nopper

---

## Abstract

Within the Quaternion-Hypersphere Theory of Spacetime [Nopper 2025a], the spatial universe is a closed three-sphere $S^3$ of radius $R(\tau)$, parameterized by quaternions $q = \xi + x\mathbf{i} + y\mathbf{j} + z\mathbf{k}$ with $|q| = R$. This note proposes that if the four-dimensional Euclidean embedding space $\mathbb{R}^4$ is physically accessible, a spacecraft can reach a distant point on $S^3$ by briefly departing the hypersurface, traversing the flat interior as a straight-line chord, and re-entering at the destination. The chord is strictly shorter than any geodesic arc on $S^3$, so the maneuver requires no superluminal velocity. To make the proposal a complete physical theory, the geometric picture is closed by a single dynamical assumption: that $|q|$ is a dynamical degree of freedom governed by a quaternionic linear sigma model with vacuum manifold $\{|q| = R\}$. This Lagrangian framework provides equations of motion that are globally smooth on $\mathbb{R}_\tau \times \mathbb{R}^4$, including at the bulk origin $|q| = 0$, and reproduces $S^3$-confined matter as the ground state. The resulting model is internally consistent and free of singularities; the hyperjump becomes either a classical over-the-barrier trajectory or a quantum tunneling process, depending on energy. The note remains speculative — it makes no empirical predictions and there is no experimental evidence for macroscopic traversal of extra dimensions.

---

## The Geometric Argument

A point on the spatial hypersphere satisfies $|q| = R$. Two points $q_1, q_2 \in S^3_R$ separated by angular distance $\theta$ admit two path types:

| Path | Parameterization | Length |
|------|-----------------|--------|
| Geodesic on $S^3$ (normal travel) | $\text{slerp}(q_1, q_2,\, t)$, $\lVert q(t) \rVert = R$ | $R\theta$ |
| Chord through $\mathbb{R}^4$ bulk (hyperjump) | $(1-t)\,q_1 + t\,q_2$, $\lVert q(t) \rVert \leq R$ | $2R\sin(\theta/2)$ |

Since $\sin(\theta/2)/(\theta/2) \leq 1$ for all $\theta \in (0, \pi]$, the chord is never longer than the arc. The maximum shortcut occurs at the antipodal point ($\theta = \pi$): chord $= 2R$ versus arc $= \pi R$ — a reduction of approximately 36 %. At sub-light speed $v$ the crossing time is $\Delta\tau = 2R\sin(\theta/2)/v$, strictly finite and causal. No violation of the Lorentz barrier occurs.

For an antipodal jump the chord passes through $|q| = 0$ at its midpoint; for non-antipodal jumps it passes through a minimum norm $R\cos(\theta/2) > 0$. The bulk origin $|q| = 0$ is a point of the auxiliary embedding $\mathbb{R}^4$ at the present cosmic time $\tau$; it is *not* the FLRW initial singularity at $\tau = 0$, although both share the property that $|q| = 0$.

---

## Closure of the Physical Constraints

The SpacetimeTheory designates $\mathbb{R}^4$ as an *auxiliary* embedding space and defines matter only on $S^3$ [Nopper 2025a, §Foundations]. Three conditions must therefore be supplied to make the hyperjump a physical process:

1. **Bulk accessibility.** The constraint $|q| = R$ must be promoted from a geometric condition to a dynamical degree of freedom.
2. **Bulk metric and dynamics.** A Lorentzian metric and an action functional must be specified on $\mathbb{R}_\tau \times \mathbb{R}^4$.
3. **Regularity along the chord.** The action and field equations must remain well-defined along the entire chord, including at $|q| = 0$.

All three are closed by adopting a single Lagrangian on the bulk $\mathcal{B} = \mathbb{R}_\tau \times \mathbb{R}^4$ with metric $\eta = \mathrm{diag}(-c^2, +1, +1, +1, +1)$:

$$\mathcal{L} \;=\; -\tfrac{1}{2}\,\eta^{\mu\nu}\,\partial_\mu q^*\,\partial_\nu q \;-\; \lambda\bigl(|q|^2 - R^2\bigr)^2$$

This is a Lorentz-invariant linear sigma model with $O(4)$ symmetry, structurally analogous to the Higgs sector but with the vacuum manifold reinterpreted as the spatial universe of [Nopper 2025a].

| Constraint | Resolution |
|------------|------------|
| (1) Bulk accessibility | $q$ is a four-component dynamical field; the radial mode $\lvert q \rvert$ is no longer constrained. |
| (2) Bulk metric and dynamics | Flat Lorentzian $\eta$ on $\mathbb{R}_\tau \times \mathbb{R}^4$; field equation $\Box q = 4\lambda(\lvert q \rvert^2 - R^2)\,q$ is globally well-posed. |
| (3) Regularity at $\lvert q \rvert = 0$ | The Lagrangian is finite there; $V(0) = \lambda R^4$ is a finite barrier. No singularity arises. |

Particles confined to the vacuum manifold $\{|q| = R\}$ reproduce the ordinary $S^3$ physics of [Nopper 2025a]. Excitations with energy above the central barrier $E_\star = \lambda R^4$ classically traverse the bulk along chord trajectories; excitations below the barrier tunnel quantum-mechanically with a finite, computable WKB amplitude. In both regimes all $S^3$-projected speeds remain $\leq c$, so no FTL motion is required.

---

## Status of the Interval-Number Framework

Earlier formulations of this proposal invoked the interval-number algebra of [Nopper 2025b] to regularize formal expressions of the type $\rho_{\text{bulk}} \cdot V_{\text{bulk}} \sim |q|^{-3} \cdot |q|^3 \to 0 \cdot \infty$ that arise if one extends FLRW-style densities into the bulk via $|q|$. Within the sigma-model framework above, no such densities appear: the action is governed by the Lagrangian $\mathcal{L}$, which is finite everywhere. The interval-number framework therefore plays no role in the present formulation. It remains an independent, self-consistent algebraic system [Nopper 2025b] and may still be useful for other extensions of the theory in which genuinely indeterminate forms appear.

---

## Summary

| Framework | Role |
|-----------|------|
| Quaternion-Hypersphere Theory [Nopper 2025a] | Identifies $\mathbb{R}^4$ as the embedding space; supplies chord-path geometry and the $S^3$ vacuum structure |
| Quaternionic linear sigma model (this note) | Provides the bulk Lagrangian, equations of motion, confinement mechanism, and barrier-traversal physics |

The model is geometrically coherent, dynamically complete, and free of singularities. It introduces a single new ingredient beyond [Nopper 2025a]: the $O(4)$-symmetric quartic potential $V(|q|) = \lambda(|q|^2 - R^2)^2$, parameterized by one coupling $\lambda$ (equivalently, the barrier height $E_\star = \lambda R^4$). The model makes no empirical predictions at present and there is no experimental evidence for macroscopic bulk traversal.

---

## References

### Foundations of this work
- [Nopper 2025a] Nopper, N. *Quaternion-Hypersphere Theory of Spacetime*. GitHub, 2025. <https://github.com/McNopper/SpacetimeTheory>
- [Nopper 2025b] Nopper, N. *Interval Numbers: A Formal Algebraic Framework for Indeterminate Forms*. GitHub, 2025. <https://github.com/McNopper/ZeroInfinity>

### Extra dimensions and braneworld models
- [Kaluza 1921] Kaluza, T. "Zum Unitätsproblem der Physik." *Sitzungsberichte der Preußischen Akademie der Wissenschaften* (1921) 966–972.
- [Klein 1926] Klein, O. "Quantentheorie und fünfdimensionale Relativitätstheorie." *Zeitschrift für Physik* 37, 895–906 (1926).
- [Arkani-Hamed, Dimopoulos & Dvali 1998] Arkani-Hamed, N., Dimopoulos, S. & Dvali, G. "The hierarchy problem and new dimensions at a millimeter." *Physics Letters B* 429, 263–272 (1998).
- [Randall & Sundrum 1999] Randall, L. & Sundrum, R. "A large mass hierarchy from a small extra dimension." *Physical Review Letters* 83, 3370–3373 (1999).

### Sigma models and symmetry breaking
- [Gell-Mann & Lévy 1960] Gell-Mann, M. & Lévy, M. "The axial vector current in beta decay." *Il Nuovo Cimento* 16, 705–726 (1960).
- [Goldstone, Salam & Weinberg 1962] Goldstone, J., Salam, A. & Weinberg, S. "Broken symmetries." *Physical Review* 127, 965–970 (1962).

### Background (Wikipedia)
- [N-sphere](https://en.wikipedia.org/wiki/N-sphere)
- [Quaternion](https://en.wikipedia.org/wiki/Quaternion)
- [Linear sigma model](https://en.wikipedia.org/wiki/Sigma_model)
- [Brane cosmology](https://en.wikipedia.org/wiki/Brane_cosmology)
- [Kaluza–Klein theory](https://en.wikipedia.org/wiki/Kaluza%E2%80%93Klein_theory)
- [Faster-than-light](https://en.wikipedia.org/wiki/Faster-than-light)
- [Geodesic](https://en.wikipedia.org/wiki/Geodesic)

### Science fiction
The concept of interstellar travel via a higher-dimensional shortcut is a recurring motif in science fiction, predating its mathematical formalization. Notable examples include hyperspatial jumps [Asimov 1951], foldspace navigation [Herbert 1965], subspace [Roddenberry 1966], hyperspace [Lucas 1977], and discrete jump drives [Banks 1987].

- [Asimov 1951] Asimov, I. *Foundation*. Gnome Press, 1951.
- [Herbert 1965] Herbert, F. *Dune*. Chilton Books, 1965.
- [Roddenberry 1966] Roddenberry, G. *Star Trek* (TV series). NBC, 1966.
- [Lucas 1977] Lucas, G. *Star Wars: Episode IV – A New Hope*. 20th Century Fox, 1977.
- [Banks 1987] Banks, I. M. *Consider Phlebas*. Macmillan, 1987.
