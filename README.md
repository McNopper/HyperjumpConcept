# Hyperjump via the Fourth Spatial Dimension

**Author:** Norbert Nopper

---

## Abstract

Within the Quaternion-Hypersphere Theory of Spacetime [Nopper 2025a], the spatial universe is a closed three-sphere $S^3$ of radius $R(\tau)$, parameterized by unit quaternions $q = \xi + x\mathbf{i} + y\mathbf{j} + z\mathbf{k}$ with $|q| = R$. This note proposes that if the four-dimensional Euclidean embedding space $\mathbb{R}^4$ — in which $S^3$ resides — is physically accessible, a spacecraft can reach a distant point on $S^3$ by briefly departing the hypersurface, traversing the flat interior as a straight-line chord, and re-entering at the destination. The chord is strictly shorter than any geodesic arc on $S^3$, so the maneuver requires no superluminal velocity. For an antipodal jump the chord passes exactly through the bulk origin $|q| = 0$; for non-antipodal jumps it passes through a minimum norm $R\cos(\theta/2) > 0$. Any attempt to extend $S^3$-defined densities into the bulk via $|q|$ encounters indeterminate forms of the type $0 \cdot \infty$ at $|q| = 0$. The interval-number framework [Nopper 2025b] provides a formal algebraic resolution of these forms, making it the natural mathematical companion to the geometric proposal. This note is speculative. It is grounded in two internally consistent mathematical frameworks and draws on established physics literature on extra dimensions and braneworld models. It does not constitute a new dynamical theory and makes no empirical predictions.

---

## The Geometric Argument

A point on the spatial hypersphere satisfies $|q| = R$. Two points $q_1, q_2 \in S^3_R$ separated by angular distance $\theta$ admit two path types:

| Path | Parameterization | Length |
|------|-----------------|--------|
| Geodesic on $S^3$ (normal travel) | $\text{slerp}(q_1, q_2,\, t)$, $\lVert q(t) \rVert = R$ | $R\theta$ |
| Chord through $\mathbb{R}^4$ bulk (hyperjump) | $(1-t)\,q_1 + t\,q_2$, $\lVert q(t) \rVert \leq R$ | $2R\sin(\theta/2)$ |

Since $\sin(\theta/2)/(\theta/2) \leq 1$ for all $\theta \in (0, \pi]$, the chord is never longer than the arc. The maximum shortcut occurs at the antipodal point ($\theta = \pi$): chord $= 2R$ versus arc $= \pi R$ — a reduction of approximately 36 %. At sub-light speed $v$ the crossing time is $\Delta\tau = 2R\sin(\theta/2)/v$, strictly finite and causal. No violation of the Lorentz barrier occurs.

---

## Indeterminate Forms Along the Chord

For an antipodal jump ($\theta = \pi$), the chord $q(t) = (1-2t)\,q_1$ passes through the bulk origin $|q| = 0$ at $t = \tfrac{1}{2}$. This origin is a point of the auxiliary embedding $\mathbb{R}^4$ at the present cosmic time $\tau$; it is *not* identical with the FLRW initial singularity at $\tau = 0$, although both share the property that $|q| = 0$.

The SpacetimeTheory defines matter and physical fields only on $S^3$; the bulk has no a priori physical content. A natural — but speculative — way to extend the framework is to promote $|q|$ to a local analog of the cosmological scale factor and define bulk quantities by analogy with FLRW. Under such an extension, formal expressions of the form

$$\rho_{\text{bulk}} \cdot V_{\text{bulk}} \;\sim\; |q|^{-3} \cdot |q|^{3} \;\to\; 0 \cdot \infty \quad \text{as } |q| \to 0$$

arise as indeterminate forms. Standard real arithmetic leaves them undefined. The interval-number framework of [Nopper 2025b] assigns them the foundation interval $\Omega = [0, \infty]_{\mathrm{in}}$, a first-class algebraic object encoding the full range of admissible limit values. This is a *formal* statement: the classical model does not uniquely determine the outcome at $|q| = 0$, and the interval-number calculus allows algebraic manipulations along the jump path to remain well-defined as $|q| \to 0$. It is not a physical prediction about bulk conditions.

---

## Physical Prerequisites and Open Questions

The SpacetimeTheory designates $\mathbb{R}^4$ as an *auxiliary* embedding space; physical matter is defined only on $S^3$ [Nopper 2025a, §Foundations]. Three conditions would need to be established for the hyperjump to be physically realizable:

1. **Bulk accessibility.** The constraint $|q| = R$ must become a dynamical degree of freedom rather than a fixed geometric condition. Braneworld models [Randall & Sundrum 1999] and large-extra-dimension scenarios [Arkani-Hamed, Dimopoulos & Dvali 1998] provide templates in which matter confined to a brane can in principle access the bulk, but no such mechanism is proposed here within the closed-$S^3$ cosmology.

2. **Confinement and exit mechanism.** A hyperjump drive would need to overcome the mechanism that ordinarily pins matter to $S^3$, navigate the bulk, and re-establish the $|q| = R$ condition at the destination.

3. **Metric extension.** The Lorentzian metric $ds^2 = -c^2 d\tau^2 + ds^2_{S^3_R}$ must be extended to $\mathbb{R}^4$. The natural candidate is $-c^2 d\tau^2 + d\xi^2 + dx^2 + dy^2 + dz^2$, but this is an assumption, not a derived result.

There is no experimental evidence for macroscopic traversal of extra spatial dimensions.

---

## Summary

Two mathematical frameworks combine to make the hyperjump concept precise:

| Framework | Role |
|-----------|------|
| Quaternion-Hypersphere Theory [Nopper 2025a] | Identifies $\mathbb{R}^4$ as the embedding space; provides chord-path geometry; quantifies the shortcut |
| Interval Numbers [Nopper 2025b] | Resolves the $0 \cdot \infty$ indeterminate forms encountered when extending $S^3$ quantities into the bulk along the jump path |

Neither framework alone is sufficient. Together they provide a geometrically coherent, algebraically complete, and physically honest description of the hyperjump concept.

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

### Background (Wikipedia)
- [N-sphere](https://en.wikipedia.org/wiki/N-sphere)
- [Quaternion](https://en.wikipedia.org/wiki/Quaternion)
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
