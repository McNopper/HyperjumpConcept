# Hyperjump via the Fourth Spatial Dimension

**Author:** Norbert Nopper

---

## Abstract

Within the Quaternion-Hypersphere Theory of Spacetime [Nopper 2025a], the spatial universe is a closed three-sphere $S^3$ of radius $R(\tau)$, parameterized by quaternions $q = \xi + x\mathbf{i} + y\mathbf{j} + z\mathbf{k}$ with $|q| = R$. This note examines whether two points of $S^3$ separated by an angular distance $\theta$ can be connected by a trajectory that leaves the hypersurface, traverses the interior of the four-dimensional Euclidean embedding $\mathbb{R}^4$ as a straight chord, and re-enters at the destination. The chord is strictly shorter than any geodesic arc on $S^3$; in operational terms — for an observer confined to $S^3$ — the traveller arrives sooner than a light signal travelling along $S^3$ would, so the trajectory is superluminal in $S^3$ projection while remaining timelike in the bulk metric. As a candidate dynamical skeleton we propose a quaternionic linear sigma model in which $|q|$ is a dynamical degree of freedom and the vacuum manifold $\{|q| = R\}$ confines ordinary matter to $S^3$. The resulting field equations are globally smooth on $\mathbb{R}_\tau \times \mathbb{R}^4$, including at $|q| = 0$, and the chord-traversal becomes either a classical over-the-barrier trajectory or a quantum-tunnelling process. Several substantial pieces remain to be supplied — coupling to gravity, dynamical $R(\tau)$, Standard-Model matter content, the Goldstone-mode mass problem, a fixed value for the single coupling $\lambda$, and a UV completion of the (non-renormalizable) quartic interaction. These open subproblems are listed explicitly. The note is therefore best read as a *programme* rather than a finished theory; it makes no empirical predictions, and there is no experimental evidence for macroscopic traversal of extra dimensions.

---

## The Geometric Argument

A point on the spatial hypersphere satisfies $|q| = R$. Two points $q_1, q_2 \in S^3_R$ separated by angular distance $\theta$ admit two path types: a geodesic *arc* of length $R\theta$ that stays on $S^3$, and a straight-line *chord* through the embedding $\mathbb{R}^4$ of length $2R\sin(\theta/2)$. The two-dimensional analogue ($S^1 \subset \mathbb{R}^2$) is shown below.

![Chord vs arc on a hypersphere](figures/chord-vs-arc.svg)

| Path | Parameterization | Length |
|------|-----------------|--------|
| Geodesic on $S^3$ (normal travel) | $\text{slerp}(q_1, q_2,\, t)$, $\lVert q(t) \rVert = R$ | $R\theta$ |
| Chord through $\mathbb{R}^4$ bulk (hyperjump) | $(1-t)\,q_1 + t\,q_2$, $\lVert q(t) \rVert \leq R$ | $2R\sin(\theta/2)$ |

Since $\sin(\theta/2)/(\theta/2) \leq 1$ for all $\theta \in (0, \pi]$, the chord is never longer than the arc. The maximum shortcut occurs at the antipodal point ($\theta = \pi$): chord $= 2R$ versus arc $= \pi R$ — a reduction of approximately 36 %. At bulk speed $v \leq c$ the crossing time is $\Delta\tau = 2R\sin(\theta/2)/v$, strictly finite and timelike with respect to the bulk metric.

It must be acknowledged that *from the perspective of an $S^3$-confined observer* the chord traverser arrives sooner than a light signal travelling along $S^3$ between the same endpoints. The effective $S^3$-projected speed for an antipodal chord at bulk speed $c$ is $\pi c / 2 \approx 1.57\,c$. The trajectory is therefore operationally superluminal in $S^3$ projection. This is consistent with the bulk light-cone but in tension with the FTL prohibition in [Nopper 2025a, §Light-Speed Bound], which is formulated *intrinsically* on $S^3$. Resolving this tension — either by extending [Nopper 2025a]'s causal-cone definition to the bulk, or by introducing a chronology-protection mechanism — is one of the open subproblems below.

For an antipodal jump the chord passes through $|q| = 0$ at its midpoint; for non-antipodal jumps it passes through a minimum norm $R\cos(\theta/2) > 0$. The bulk origin $|q| = 0$ is a point of the auxiliary embedding $\mathbb{R}^4$ at the present cosmic time $\tau$; it is *not* the FLRW initial singularity at $\tau = 0$, although both share the property that $|q| = 0$.

---

## A Candidate Dynamical Skeleton: Quaternionic Linear Sigma Model

The SpacetimeTheory designates $\mathbb{R}^4$ as an *auxiliary* embedding space and defines matter only on $S^3$ [Nopper 2025a, §Foundations]. To make the hyperjump a physical process, the kinematic constraint $|q| = R$ must be replaced by dynamics: an action principle that admits both $S^3$-confined ground states and chord-like excited trajectories.

We propose, as the simplest candidate skeleton, a Lorentz-invariant linear sigma model with $O(4)$ symmetry on the bulk $\mathcal{B} = \mathbb{R}_\tau \times \mathbb{R}^4$:

$$\mathcal{L} \;=\; -\tfrac{1}{2}\,\eta^{\mu\nu}\,\partial_\mu q^*\,\partial_\nu q \;-\; \lambda\bigl(|q|^2 - R^2\bigr)^2$$

with $\eta = \mathrm{diag}(-c^2, +1, +1, +1, +1)$. Structurally this is the Higgs sector with the vacuum manifold reinterpreted geometrically as the spatial universe of [Nopper 2025a].

The skeleton does three things:

| Feature | Mechanism |
|---------|-----------|
| Field $q$ becomes dynamical | $\lvert q \rvert$ is no longer a kinematic constraint |
| Equations of motion are globally smooth | $\Box q = 4\lambda(\lvert q \rvert^2 - R^2)\,q$ is well-posed everywhere on $\mathcal{B}$, including at $\lvert q \rvert = 0$ |
| The bulk origin is non-singular | $V(0) = \lambda R^4$ is finite; the chord encounters a finite barrier, not a divergence |

Excitations with energy above the central barrier $E_\star = \lambda R^4$ classically traverse the bulk along chord trajectories; excitations below the barrier tunnel quantum-mechanically (rate calculable via the Coleman bounce, not the 1D-WKB formula sometimes used heuristically). The single coupling $\lambda$ controls the *brane thickness* $\ell_\perp \sim 1/(\sqrt{\lambda}\,R)$, the *barrier energy density* $\rho_\star = \lambda R^4$, and via the product $\rho_\star V_{\text{cargo}} c\Delta\tau$ the *energy cost* of transporting an object through the bulk.

This much is a clean kinematic skeleton. It is **not yet a complete physical theory**.

---

## Open Subproblems

The skeleton above leaves eight substantial pieces unsupplied. Each is an explicit open problem; the model becomes a candidate physical theory only when all are addressed. For six of them (items 1, 2, 3, 4, 5, 7) a textbook-level *first-pass closure* is sketched inline; these are starting points, not final solutions. Items 6 and 8 remain genuinely open.

1. **Cosmic expansion.** [Nopper 2025a] has $R = R(\tau)$ (FLRW). The static $R$ in $\mathcal{L}$ is incompatible. *First-pass closure:* promote $R \to \Phi(\tau)$ with potential $U(\Phi)$ and add a kinetic term $-\tfrac{1}{2}(\partial\Phi)^2$. The homogeneous mode then satisfies $\ddot\Phi + 3H\dot\Phi + U'(\Phi) = 0$, the standard scalar-field-cosmology equation [Linde 1990]; for slow-roll choices of $U$ this reproduces de Sitter expansion. Full closure requires coupling to 5D gravity (Subproblem 2) so that $H$ is itself a solution rather than a postulate.
2. **Coupling to gravity.** The bulk is treated as flat. To recover the FLRW geometry as a *solution* rather than a postulate, the action must be coupled to 5D General Relativity, $S = \int d^5x\sqrt{-g}\,[\mathcal{R}^{(5)}/(2\kappa_5^2) + \mathcal{L}_q]$, in the spirit of Randall-Sundrum / DGP braneworlds. *First-pass closure:* in the thin-brane limit $\ell_\perp \to 0$, the energy-momentum tensor of $q$ degenerates to a delta-function source on $S^3$ and the 5D Einstein equations reduce to Israel junction conditions [Israel 1966]; the induced 4D geometry is then standard FLRW with the brane tension $\sigma = \int d\ell_\perp\,V(|q|)$ playing the role of an effective cosmological constant. A finite-$\ell_\perp$ treatment requires solving the coupled $(g_{MN}, q)$ system numerically.
3. **Standard-Model matter on the brane.** Real matter is not a quaternion sigma model. *First-pass closure:* introduce a 5D Dirac fermion $\Psi$ with Yukawa coupling $h\,\bar\Psi\Psi\,(|q|^2 - R^2)$ [Rubakov-Shaposhnikov 1983]. The transverse Dirac equation $\bigl[i\gamma^\perp\partial_\perp - h(|q|^2 - R^2)\bigr]\Psi = 0$ admits a single normalizable zero mode with profile $\Psi_0(r) \propto \exp\bigl[-h\!\int^r(|q|^2 - R^2)\,dr'\bigr]$ peaked on $S^3$ and exponentially suppressed in the bulk; this is the 4D Standard-Model fermion. Gauge bosons can be localized by analogous dilaton-type couplings [Dvali-Shifman 1997]. Recovering the full SM spectrum (chirality, generations, Higgs) within this framework is non-trivial but follows established braneworld phenomenology.
4. **Goldstone-mode mass problem.** $O(4) \to O(3)$ produces three exactly massless scalars not seen in nature. *First-pass closure:* gauge the $SO(4)$ symmetry by introducing gauge fields $A_\mu^a$ ($a = 1,\dots,6$) and replacing $\partial_\mu q \to D_\mu q = (\partial_\mu - igA_\mu^a T^a)q$, plus the Yang-Mills term $-\tfrac{1}{4}F^a_{\mu\nu}F^{a\,\mu\nu}$. After symmetry breaking, the three broken generators give three massive vector bosons with masses $m_A \sim gR$; the three Goldstones become their longitudinal components via the Higgs mechanism. The remaining $SO(3)$ gauge bosons stay massless and would need to be either confined or identified with a known sector — itself a non-trivial phenomenological constraint.
5. **Determination of $\lambda$.** The coupling is unconstrained, so the model is not predictive. *First-pass closure:* the brane-thickness relation $\ell_\perp = 1/(\sqrt\lambda\,R)$ combined with the experimental upper bound on the size of any unobserved transverse dimension, $\ell_\perp \lesssim \ell_{\exp} \approx 44\,\mu\text{m}$ [Adelberger et al. 2003], gives the lower bound $\sqrt\lambda \geq 1/(\ell_{\exp} R)$. With $R$ of order the Hubble radius, this places $\lambda$ many orders of magnitude above zero but leaves it otherwise unfixed; pinning a unique value would require an independent observable (e.g. a Kaluza-Klein-type signature, a tunnelling rate, or a cosmological constraint on $\Phi$).
6. **Operational FTL versus [Nopper 2025a]'s prohibition.** Chord traversal is timelike in the bulk but superluminal in $S^3$ projection. This must be reconciled either by extending [Nopper 2025a]'s causal cone to the bulk metric, or by adding a chronology-protection term that suppresses antipodal jumps.
7. **Tunnelling rate.** A field-theoretic Coleman–De Luccia bounce calculation should replace the 1D-WKB heuristic; this gives the actual jump amplitude as a function of $\lambda$, $R$, and cargo geometry. *First-pass closure:* the relevant process is barrier penetration, not false-vacuum decay — the system is already in the true vacuum and tunnels through the central bump $V(0) = \lambda R^4$. The Euclidean bounce action scales, in the thin-wall limit, as $B \sim \sigma \cdot \mathrm{Area}(\text{wall}) \sim \sqrt\lambda\,R^3 \cdot R^3 \sim \sqrt\lambda\,R^6$ in natural units, giving a tunnelling rate per unit volume $\Gamma/V \sim \mu^5 e^{-B/\hbar}$ with $\mu$ a characteristic mass scale. For cosmological $R$ and $\lambda$ saturating Subproblem 5's lower bound, $B$ is astronomically large and the spontaneous rate is negligible — consistent with non-observation, but also implying that *unaided* hyperjumps are exponentially suppressed and would require an external coherent source to occur on macroscopic timescales.
8. **UV completion.** The quartic interaction $\lambda(|q|^2 - R^2)^2$ is non-renormalizable in five spacetime dimensions; the Lagrangian is therefore at best an effective theory below some cutoff $\Lambda$. A UV completion (e.g. an asymptotically-safe fixed point, an embedding in a higher-symmetry theory, or a string-theoretic origin) is not supplied here.

A consistent closure of items 1–2 alone would already promote the proposal from a kinematic skeleton to a candidate dynamical theory; items 3–5 would make it phenomenologically meaningful; items 6–8 are interpretive, technical, and foundational respectively.

---

## Note on the Interval-Number Framework

Earlier formulations of this proposal invoked the interval-number algebra of [Nopper 2025b] to regularize formal expressions of the type $\rho_{\text{bulk}} \cdot V_{\text{bulk}} \sim |q|^{-3} \cdot |q|^3 \to 0 \cdot \infty$ that arise if one extends FLRW-style densities into the bulk via $|q|$. Within the sigma-model skeleton above, no such densities appear: the action is governed by the Lagrangian $\mathcal{L}$, which is finite everywhere. The interval-number framework therefore plays no role in the present formulation. It remains an independent, self-consistent algebraic system [Nopper 2025b] and may still be useful for other extensions of the theory in which genuinely indeterminate forms appear.

---

## Summary

| Framework | Role |
|-----------|------|
| Quaternion-Hypersphere Theory [Nopper 2025a] | Identifies $\mathbb{R}^4$ as the embedding space; supplies chord-path geometry and the $S^3$ vacuum structure |
| Quaternionic linear sigma model (this note) | Provides a candidate bulk Lagrangian whose vacuum manifold is $S^3$ and whose excited states traverse the bulk |

The model is **geometrically coherent and singularity-free**, but **not yet dynamically complete**: the eight open subproblems listed above must be closed before it can be considered a candidate physical theory. Six of them (cosmic expansion, gravity coupling, SM-matter localization, Goldstone masses, bound on $\lambda$, tunnelling rate) admit textbook-level first-pass closures sketched inline; the remaining two — operational FTL reconciliation and UV completion — are genuinely open and foundational. It introduces, beyond [Nopper 2025a], the $O(4)$-symmetric quartic potential $V(|q|) = \lambda(|q|^2 - R^2)^2$ with a single coupling $\lambda$. The coupling has a clean physical interpretation (barrier height $E_\star = \lambda R^4$, brane thickness $\ell_\perp = 1/(\sqrt{\lambda}\,R)$, transit-energy density $\rho_\star = \lambda R^4$) but no fixed numerical value at present. The model makes no empirical predictions, and there is no experimental evidence for macroscopic bulk traversal.

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

### Sigma models, symmetry breaking, brane localization, tunnelling
- [Gell-Mann & Lévy 1960] Gell-Mann, M. & Lévy, M. "The axial vector current in beta decay." *Il Nuovo Cimento* 16, 705–726 (1960).
- [Goldstone, Salam & Weinberg 1962] Goldstone, J., Salam, A. & Weinberg, S. "Broken symmetries." *Physical Review* 127, 965–970 (1962).
- [Linde 1990] Linde, A. *Particle Physics and Inflationary Cosmology*. Harwood Academic, 1990.
- [Coleman 1977] Coleman, S. "Fate of the false vacuum: Semiclassical theory." *Physical Review D* 15, 2929–2936 (1977).
- [Callan & Coleman 1977] Callan, C. G. & Coleman, S. "Fate of the false vacuum. II. First quantum corrections." *Physical Review D* 16, 1762–1768 (1977).
- [Israel 1966] Israel, W. "Singular hypersurfaces and thin shells in general relativity." *Il Nuovo Cimento B* 44, 1–14 (1966).
- [Rubakov & Shaposhnikov 1983] Rubakov, V. A. & Shaposhnikov, M. E. "Do we live inside a domain wall?" *Physics Letters B* 125, 136–138 (1983).
- [Dvali & Shifman 1997] Dvali, G. & Shifman, M. "Domain walls in strongly coupled theories." *Physics Letters B* 396, 64–69 (1997).
- [Adelberger et al. 2003] Adelberger, E. G., Heckel, B. R. & Nelson, A. E. "Tests of the gravitational inverse-square law." *Annual Review of Nuclear and Particle Science* 53, 77–121 (2003).

### Background (Wikipedia)
- [N-sphere](https://en.wikipedia.org/wiki/N-sphere)
- [Quaternion](https://en.wikipedia.org/wiki/Quaternion)
- [Linear sigma model](https://en.wikipedia.org/wiki/Sigma_model)
- [Brane cosmology](https://en.wikipedia.org/wiki/Brane_cosmology)
- [Kaluza–Klein theory](https://en.wikipedia.org/wiki/Kaluza%E2%80%93Klein_theory)
- [Faster-than-light](https://en.wikipedia.org/wiki/Faster-than-light)
- [Geodesic](https://en.wikipedia.org/wiki/Geodesic)

### Inspirational background (science fiction)

The motivating question of this note — whether a higher-dimensional shortcut between distant points of our spatial universe could be physically realisable — is a recurring motif in twentieth-century science fiction. The works listed below served only as *inspiration* for posing the question in the first place; they form no part of the physics or mathematics presented above, and no claim is made that the corresponding fictional devices realise the proposed mechanism.

- [Asimov 1951] Asimov, I. *Foundation*. Gnome Press, 1951. — hyperspatial jumps.
- [Herbert 1965] Herbert, F. *Dune*. Chilton Books, 1965. — foldspace navigation.
- [Roddenberry 1966] Roddenberry, G. *Star Trek* (TV series). NBC, 1966. — warp drive through subspace.
- [Lucas 1977] Lucas, G. *Star Wars: Episode IV – A New Hope*. 20th Century Fox, 1977. — hyperspace.
- [Banks 1987] Banks, I. M. *Consider Phlebas*. Macmillan, 1987. — discrete jump drives.
