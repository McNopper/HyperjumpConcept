# Hyperjump via the Fourth Spatial Dimension

**Author:** Norbert Nopper

This repository contains a *programme note* exploring whether two points of a
closed three-sphere universe ($S^3$) can be connected by a straight chord
through the embedding $\mathbb{R}^4$ instead of along a geodesic arc on $S^3$.
The chord is strictly shorter than the arc, so for an observer confined to
$S^3$ the traveller arrives sooner than a light signal travelling along $S^3$
would, while the trajectory remains timelike with respect to the bulk metric.
A quaternionic linear sigma model is proposed as a candidate dynamical
skeleton, and eight open subproblems are listed with first-pass closures.

The full paper is available as a PDF:

- 📄 **[hyperjump.pdf](hyperjump.pdf)** — rendered paper
- 📝 **[hyperjump.tex](hyperjump.tex)** — LaTeX source

## At a glance

- **Setting.** Quaternion-Hypersphere Theory of Spacetime [Nopper 2025a]: the
  spatial universe is a closed $S^3$ of geometric radius $R_{\mathrm{geom}}(\tau)$
  embedded in $\mathbb{R}^4$.
- **Geometric claim.** Chord length $2R_{\mathrm{geom}}\sin(\theta/2)$ vs.
  arc length $R_{\mathrm{geom}}\theta$; the antipodal chord is $\sim$36 %
  shorter than the antipodal arc.
- **Dynamical skeleton.** A Lorentz-invariant $O(4)$ linear sigma model on the
  bulk $\mathcal{B}=\mathbb{R}_\tau\times\mathbb{R}^4$ with order-parameter
  field $\phi^A$ and quartic potential
  $V(\phi)=\lambda(\phi^A\phi^A-v^2)^2$. Standard-Model zero modes are
  localized near $|X|=R_{\mathrm{geom}}$ by the background profile of $\phi^A$.
- **Status.** Programme note, not a finished theory. Eight substantial
  subproblems (cosmic expansion, coupling to gravity, Standard-Model matter
  content, Goldstone-mode masses, fixing $\lambda$ and $v$, the intrinsic vs.
  bulk light-cone, the tunnelling rate, and a UV completion) remain open and
  are addressed only by first-pass closures.

## Status and limitations

This document is a *programme note*, not a finished physical theory. It
assumes a closed $S^3$ spatial topology (a premise of [Nopper 2025a], not
established by observation), it does not construct a self-consistent 5D
gravity + Standard-Model-localization solution, and it does not contain a
chronology-protection proof that the bulk-light-cone reformulation is free
of closed timelike curves. The "first-pass closures" given for the eight
open subproblems are pointers to the appropriate textbook tools, *not*
completed calculations for this specific setup. Treat all "in-principle
possible" statements as conditional on those three items.

## Building the PDF

```bash
pdflatex hyperjump.tex
pdflatex hyperjump.tex   # second pass for cross-references
```

Requires a TeX distribution with the standard `amsmath`, `tikz`, `tabularx`,
`booktabs`, `float`, `enumitem`, and `hyperref` packages.

## Related work

- [Nopper 2025a] Nopper, N. *Quaternion–Hypersphere Theory of Spacetime: A
  Conceptual Synthesis of Closed FLRW Cosmology, Quaternionic $S^3$
  Parameterization, and Relational Time*. 2025.
  <https://github.com/McNopper/SpacetimeTheory/blob/main/SpacetimeTheory.pdf>
- [Nopper 2025b] Nopper, N. *Interval Numbers: A Formal Algebraic Framework
  for Indeterminate Forms*. 2025.
  <https://github.com/McNopper/ZeroInfinity/blob/main/paper.pdf>

A full reference list (braneworld models, sigma-model and tunnelling
literature, sub-mm gravity tests, and inspirational science-fiction sources)
is provided in the [paper](hyperjump.pdf).
