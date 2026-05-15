# Hyperjump via the Fourth Spatial Dimension

*by Norbert Nopper*

A programme note on chord trajectories through the bulk of a closed
three-sphere universe.

## Overview

Within the Quaternion-Hypersphere Theory of Spacetime [Nopper 2025a], the
spatial universe is a closed three-sphere $S^3$ of geometric radius
$R_{\mathrm{geom}}(\tau)$ embedded in a four-dimensional Euclidean space
with coordinates $X^A = (\xi, x, y, z)$, packaged as the quaternion
$q = \xi + x\mathbf{i} + y\mathbf{j} + z\mathbf{k}$.

This note examines whether two points of $S^3$ separated by an angular
distance $\theta$ can be connected by a trajectory that leaves the
hypersurface, traverses the interior of the embedding $\mathbb{R}^4$ as a
straight chord, and re-enters at the destination. The chord is strictly
shorter than any geodesic arc on $S^3$; in operational terms — for an
observer confined to $S^3$ — the traveller arrives sooner than a light
signal travelling along $S^3$ would, so the trajectory is superluminal in
$S^3$ projection while remaining timelike in the bulk metric.

As a candidate dynamical skeleton, a separate quaternionic linear sigma
model is proposed with order-parameter field $\phi^A(X)$ and quartic
potential $V(\phi) = \lambda(\phi^A\phi^A - v^2)^2$; the intended physical
brane is the locus near $|X| = R_{\mathrm{geom}}$ where Standard-Model zero
modes are localised by the background profile of $\phi^A$. Chord traversal
then becomes either a classical over-the-barrier excitation of the
localisation field or a quantum-tunnelling process.

**Status.** Programme note, not a finished physical theory. Eight
substantial subproblems — cosmic expansion, coupling to gravity,
Standard-Model matter content, the Goldstone-mode mass problem, fixing
$\lambda$ and $v$, reconciliation with the intrinsic light-speed bound of
[Nopper 2025a], a field-theoretic tunnelling-rate calculation, and a UV
completion of the (non-renormalizable) quartic interaction — remain open
and are addressed only by first-pass closures. There is no experimental
evidence for macroscopic traversal of extra dimensions.

## The paper

- 📄 **[hyperjump.pdf](hyperjump.pdf)** — typeset PDF
- 📝 **[hyperjump.tex](hyperjump.tex)** — LaTeX source

Rebuild with any standard LaTeX engine:

```sh
latexmk -pdf hyperjump.tex
```

## Related work

- [Nopper 2025a] *Quaternion–Hypersphere Theory of Spacetime: A Conceptual
  Synthesis of Closed FLRW Cosmology, Quaternionic $S^3$ Parameterisation,
  and Relational Time.*
  <https://github.com/McNopper/SpacetimeTheory>

## License

CC BY 4.0. See [LICENSE](LICENSE).
