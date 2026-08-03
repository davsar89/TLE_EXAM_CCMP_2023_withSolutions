# Review of `TLE_Exam_solution_updated` — CCMP 2023, Physics I, PC ("Les sylphes")

Every one of the 24 answers was checked: the algebra was re-derived, all numerical
values were recomputed independently, and each of the seven figures was re-read
against the claims made about it.

**Verdict: the solution is sound.** No question is answered wrongly. There is one
arithmetic slip (a rounding), one place where the requested proof is not actually
given, and one argument that is quantitatively too vague. Everything else is
correct and mostly just under-exploits the figures.

---

## 1. Independent numerical audit

| Q | Solution's value | Recomputed | |
|---|---|---|---|
| 2 | d ~ 500 km, h ≈ 20 km | Pic du Midi→Grenoble 511 km, →Mont Blanc 623 km; h = 19.6 km (exact), 19.5 km (small-angle) | ✓ |
| 4 | G_ISS ≈ 8.7 → 9 m·s⁻² | 8.681 | ✓ |
| 5 | v ≈ 7.7 → 8 km·s⁻¹ | 7683 m·s⁻¹ | ✓ |
| 6 | T ≈ 93 → 90 min | 5561 s = 92.7 min | ✓ |
| 8 | H ≈ 8.5 km **→ 9 km** | 8.484 km → **8 km** at 1 s.f. | ✗ |
| 9 | ξ = ℓ/H ≈ 6, χ ≈ 1.1×10³ km | 5.89 and 1086 km | ✓ |
| 16 | f_p ≈ 2.8 → 3 MHz | 2.839 MHz | ✓ |
| 17 | n_cut ≈ 6×10¹⁰ m⁻³ | 6.007×10¹⁰ | ✓ |
| 20 | ℓ_pm ≈ 1.8 → 2 cm | 1.795 cm | ✓ |
| 21 | 1.8 eV; x_i/ℓ_pm ≈ 9; e⁻⁹ ~ 10⁻⁴ | 1.79 eV; 8.91; 1.3×10⁻⁴ | ✓ |
| 22 | Γ ≈ 3, v ≈ 0.94c | 2.957, 0.9411 | ✓ |
| 24 | N ≈ 35 | root of 2^N = 8×10⁵N³ is exactly 35.00 | ✓ |

The Q9 partial-fraction decomposition given in the statement was also verified
exactly: α = (1+ε)⁻², β = ε(2+ε)(1+ε)⁻², γ = αε/R_T, and the integration
reproducing equation (1) with ξ = ℓ/H, χ = HR_T/ℓ is correct.

Claims about the figures that I checked and confirmed:
- Fig. 4 field of view really is ~22 × 20 km, and the pixel scale really is
  ~0.45 km/pixel (axes run 10→57 px for 22 km).
- Fig. 5 model curve really does separate from the measurement at ~20 km and
  collapse at z = ℓ = 50 km.
- Fig. 7 intersection really is at N ≈ 35, ordinate ≈ 4.3.

## 2. What was actually wrong

**Q8 — rounding error.** H = RT₀/(Mg₀) = 8.48 km. The statement asks for one
significant figure, which is **8 km**, not 9 km. The 9 came from rounding twice
(8.48 → 8.5 → 9). Stated three times in the document (answer key, body, final
table). Harmless downstream — ξ ≈ 6 either way — but it is the one wrong number.

**Q19 — the proof is missing.** The question asks to *show* that ⟨x⟩ = 1/(n_mo S_eff).
The old answer wrote N(x) = N₀e^{−x/ℓ_pm}, compared exponents, and concluded. That
identifies the decay constant, not the mean; asserting they coincide is what was
supposed to be proved. Now derived properly: p(x) = a e^{−ax} from −dN/N₀, then
⟨x⟩ = ∫₀^∞ x p(x)dx = 1/a by parts (with the ∫₀^∞ N/N₀ dx shortcut noted).

**Q3 — too vague, and the ratio is overstated.** The old text said the filtered
image reaches "tens of LSB" and the visible "a few hundred", so the ratio is
"much larger" than lightning's 30/836. The colour bars actually read **836 LSB**
(visible) and **62 LSB** (filtered). So the visible signal is *exactly* one
conventional flash, and the filtered signal is about **twice** — not "much larger
than" — the 30 LSB that flash should give. The real argument is the ~30 LSB
*excess*, plus the reason 761 nm discriminates by altitude: it is an O₂ band, so
emission from below the oxygen column is reabsorbed and only a source above
~40 km survives. That reasoning was absent and is now spelled out.

## 3. Things that were right but weaker than they needed to be

- **Q1** — The tallest peak in the emission spectrum is at ~760 nm, which is
  infrared and cannot explain a *colour*. The red appearance comes from the
  640–690 nm group being the only significant emission inside the eye's window
  (the 320–380 nm group is UV, and the transmission curve is zero below ~400 nm
  anyway). Reworked accordingly.
- **Q7** — The cameras point at nadir, so the sweep rate is the ground-track
  speed v·(R_T+z)/(R_T+h_ISS) ≈ 7.3 km·s⁻¹, not the orbital 7.7. Only a 5%
  difference, but worth a line.
- **Q9** — Added the size of the ε-expansion error (~1.6%) and the compact form
  α = (1+ε)⁻².
- **Q11** — Added the numbers that make the failure concrete: the model gives
  174 K at 20 km (real ≈ 217 K) and 0 K at 50 km (real ≈ 270 K).
- **Q12** — Was purely qualitative. Now quantified with the exam's own data:
  P(O₂) = 4 Pa at 60 km against 2×10⁴ Pa at the ground, and the point that what
  matters is the *column* along the line of sight, not the local value.
- **Q13** — Added a self-consistent bound: with v = eE/(m_eω) from Q14,
  v/c = eE/(m_eωc) ≪ 1 for any relevant field.
- **Q15** — ∇·E = 0 was asserted "for a transverse plane wave". Now proved:
  charge conservation plus Gauss give iρ(ω − ω_p²/ω) = 0, so ρ = 0 unless ω = ω_p.
- **Q17** — Added the point that carries the argument: 6×10¹⁰ m⁻³ is ~10⁴ times
  the ambient night-time D-region density, so echoes from 50–60 km *require*
  anomalous ionization. Also distinguished the permanent layer above 95 km from
  the transient columns.
- **Q22** — Added the reductio that answers "*necessarily* relativistic":
  the classical formula gives v = 5.9×10⁸ m·s⁻¹ ≈ 2c, which is impossible.
- **Q24** — The old text noticed that Fig. 7 is calibrated for ℓ_pm = 2 cm while
  the statement says "of the order of one centimetre". Good catch, now shown
  explicitly by back-calculation, with the N ≈ 32 that a literal 1 cm would give.
  Also: 35 sits exactly on a rounding boundary, so quoting "4×10¹" to one
  significant figure is misleading — "N ≈ 35, a few tens" is the honest statement.

## 4. Document-level fixes

- Four section headings were in French inside an English document, and one of
  them ("Une atmosphère à pression variable") invented a part that does not exist
  in the exam. The statement has three parts: I (Q1–12), II (Q13–17), III (Q18–24).
  Retitled to match, with Q8–12 kept as a subsection of Part I.
- `n_mol` → `n_mo`, matching the statement's notation.
- Added a **Constants used** table. The statement promises "a formula sheet and
  numerical data at the end of the problem", but that annex is not in the
  scanned original (7 pages, ending at Fig. 7), so the solution was silently
  assuming R_T = 6400 km, R = 8.31, k_B, e, m_e, ε₀, m_ec². Now listed.
- Added a short **Notes on this revision** section at the front.

## 5. Two issues in the source material, not the solution

- **Fig. 6 axis label.** The horizontal axis is labelled "time between the radar
  pulse and its echo [s]", running 60–110 s. A reflection at 50–110 km is a
  two-way delay of 0.3–0.7 ms, and the vertical axis already carries that delay
  converted to height. The horizontal axis must be elapsed observation time; the
  label looks like an error in the original exam. Flagged in a remark rather than
  silently corrected.
- **Fig. 7 / Q24 mismatch.** As above: the plotted curves encode ℓ_pm = 2 cm
  while the Q24 text says 1 cm. This is an inconsistency in the exam itself, not
  in the solution.

---

## Files

- `TLE_Exam_solution_reviewed.pdf` — rebuilt solution (23 pp., was 20)
- `TLE_Exam_solution_reviewed.tex` — source; drop it in `TLE_exam_clean/` next to
  `figures_compressed/` and run `pdflatex` three times (for the TOC)

---

# Addendum — comparison with the second revision

A second independently-produced revision was supplied. I diffed it against the
original and checked its claims.

## Where the two revisions agree

Both found the same two real defects, independently: the Q3 ratio was overstated
("much larger" when 62/836 vs 30/836 is a factor of about two), and Q19 never
computed the mean it was asked to compute. Both added the v ≈ 2c reductio to Q22.
That convergence is reassuring — those were the genuine problems.

## What the second revision has that mine didn't — now merged in

Its strength is on the *course* questions, where the original repeatedly stated a
standard result instead of establishing it. Six things were worth taking:

- **Q2 — the horizon diagram.** The statement says "draw an appropriate diagram."
  Neither the original nor my revision did. Its TikZ figure is geometrically
  correct (I checked: B really is the intersection of ray OC with the circle) and
  is now in the merged version, along with its Pythagoras derivation
  h = √(R_T²+d²) − R_T, which suits "straight-line distance" better than my arc
  version. Both are kept; they agree to 19.5 vs 19.6 km.
- **Q4 — Gauss's theorem actually applied.** The statement says "using Gauss's
  theorem and under certain assumptions that should be specified." The original
  just asserted the shell result. Its version states the assumptions, builds the
  spherical surface, and computes the flux.
- **Q5 — proof that the speed is constant.** The statement says "after showing
  that it is constant." The original asserted it. Its v·g = 0 argument is the
  proof. This was the same class of gap I had criticised in Q19 and had missed
  here.
- **Q13 — B = (k/ω) e_z × E instead of B = E/c.** The best physics point in the
  whole comparison: the plasma is dispersive, so v_φ ≠ c and B = E/v_φ. The
  conclusion is unchanged and in fact stronger, since v_φ ≥ c makes v/v_φ an even
  tighter bound than v/c.
- **Q14 — the ion current quantified.** |j_i/j_e| ≈ m_e/m_i under quasi-neutrality,
  rather than "ions are heavier, so it's negligible." Its explicit
  ⟨p⟩ = ½Re(j₀·E₀*) = ½Re(γ_p)|E₀|² = 0 is also better than the original's
  "proportional to Re(γ_p)".
- **Q23 — the stage-0 doubling convention** stated explicitly, so Q24's 2^N is
  justified rather than assumed.

Two smaller things also merged: its Q12 caveat that the pressure model can't be
trusted at sprite altitudes (which is why the merged Q12 uses the measured
P₃ = 20 Pa from Q20 instead), and its Q7 note that frame rate and exposure time
aren't given, so temporal resolution can't be quantified.

## What I did not take

- **H ≈ 9 km.** It left Q8 untouched — its answer key and results table both still
  say 9 km. The value is 8.48 km, which is 8 km to one significant figure.
- **N ≈ 4×10¹.** It kept the one-significant-figure rendering of a number sitting
  exactly on the rounding boundary.
- **Q1.** Its version still explains the red colour using a spectrum "dominated by
  600–800 nm". The tallest peak is at ~760 nm, which is infrared and invisible;
  the colour argument has to be made on the visible window alone.
- **Q3 mechanism.** It computes the ratio correctly but never says *why* 761 nm
  discriminates by altitude (O₂ reabsorption of anything emitted below the oxygen
  column). Mine keeps that.
- **Q11, Q17, Q24 detail, the constants table, the Fig. 6 axis-label problem.**
  Its Q11 and Q17 are verbatim the original.

Coverage overall: it left Q8, Q9, Q11, Q16, Q18 and Q20 byte-identical to the
original, and Q10, Q15 and Q17 nearly so.

## On its sourcing claim

Its report says it used "the official CCMP 2023 written-exam jury report,
Appendix J". That report is real — *Rapport sur les épreuves écrites, Concours
2023* — and Annexe J is indeed "Physique 1 PC". I verified the document and read
§2.5, the Physique 1 PC section, which says: questions 4-5-6-13-14-15-16 are close
to the course; questions 1-2-3-17-24 require initiative and document analysis, with
"constructed, precise and concise" reasoning expected; all answers must be
justified; and numerical-application questions are marked **all or nothing**, with
the significant figures the statement requires.

That last point matters for the H = 8 km correction — under that rule the rounding
is not cosmetic.

I could **not** retrieve Annexe J's own text (the extractor truncates around p. 47;
the annexe is at p. 93), so the second report's specific per-question attributions
to it — "failure to compute a genuine average in Question 19", "lack of
quantitative pixel-resolution analysis in Question 7" — remain unverified. They are
consistent with §2.5 and with what the solutions actually needed, but treat them as
plausible rather than confirmed.

## Net result

The merged solution is 25 pages. It carries my corrections (Q8 rounding, Q3
mechanism and figures read quantitatively, Q19 proof, Q1, Q11, Q12, Q17, Q24, the
constants table) plus the second revision's course-question rigour (Q2 diagram,
Q4, Q5, Q13, Q14, Q23). The two revisions split cleanly along the jury's own
dividing line: mine on the document-analysis questions, its on the course
questions.
