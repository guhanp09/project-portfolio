# Engineering and reliability work

Mechanical design, aircraft report analysis, configuration review and electrical
verification. Each project keeps source observations separate from model predictions,
invented scenarios and work that still requires physical testing or authorized review.

## DefectReview — Aircraft reliability analysis

[GitHub](https://github.com/guhanp09/defect-review) ·
[Engineering review](https://guhanp09.github.io/defect-review/) ·
[Counting contract](https://github.com/guhanp09/defect-review/blob/main/docs/methods.md)

- Analyzed 67,649 accepted FAA service-difficulty reports across 519 make/model pairs
  using Python and DuckDB SQL; retained occurrence/submission dates and source hashes.
- Built JASC/ATA chapter, system/model and part/condition drilldowns, a date quarantine
  and source-traceable 30-day investigation candidates. Same-day findings remain distinct
  from evidence of a recurring physical defect.
- Calculated rates, MTBUR and Poisson intervals on a separate synthetic exposure case.
  Missing public fleet exposure blocks public failure-rate claims.
- Twenty-two tests and artifact checks cover cutoffs, report identities, coding,
  SQL reconciliation, export ordering and exposure boundaries.

## Effectivity Desk — Aircraft configuration and document review

[GitHub](https://github.com/guhanp09/effectivity-desk) ·
[Engineering review](https://guhanp09.github.io/effectivity-desk/) ·
[Source study](https://github.com/guhanp09/effectivity-desk/blob/main/docs/source-review.md)

- Reviewed the public FAA AD 2026-09-01 and its retained/new action scopes, reference-date
  exceptions, location-specific part-history condition and authority boundaries.
- Reviewed captured manufacturer bulletin scope in a focused Piper SB 1390 case, with serial-boundary and group-transition checks.
- Implemented model/serial/part/position rules with MATCH, NO_MATCH and UNKNOWN states.
  Nine synthetic configurations exercise missing data, incomplete inventories and
  component correlation; source/configuration changes invalidate saved reviews.
- Compared line/base windows, cost-benefit and warranty evidence in separate synthetic
  scenarios. A cheaper late window is excluded; missing quotes block selection.
- Forty-seven tests and source/artifact checks. Missing proprietary incorporated bulletin
  evidence is not replaced with invented manufacturer effectivity or due dates.

## CondenserLab — Mechanical design and CFD verification

[GitHub](https://github.com/guhanp09/condenserlab) ·
[Engineering report](https://github.com/guhanp09/condenserlab/blob/main/reports/engineering_report.md)

- Four parametric FreeCAD assemblies with STEP/STL exports, drawings, mounting interfaces
  and BOM; three accepted OpenFOAM cases across two shroud designs.
- Pressure-law benchmark: 0.062% relative error. Retained checks include mesh quality,
  mass balance, fan operating point, residuals and analytical/thermal calculations.
- Proposed water-loop rig includes a sensor layout, acquisition schema, uncertainty
  treatment and assembly plan. Full four-design ranking, mesh independence and physical
  validation remain open; predicted heat rejection is not measured efficiency.

## PackBench — Electrical data and telemetry verification

[GitHub](https://github.com/guhanp09/packbench) ·
[Measured-data reduction](https://github.com/guhanp09/packbench/blob/main/results/cell_report.md)

- Reduced public University of Maryland CALCE cell tests into Ah/Wh and evaluated a
  one-RC voltage model on a separate 6,682-sample run: 16 mV RMS and 310 mV peak error.
- Kept the capacity specimen, model specimen, fitting run and evaluation run distinct.
  Pack-screening assumptions do not imply aircraft-qualified cell performance.
- Tested C telemetry encoding with an independent Python decoder, checksum, packet-loss,
  wrap and invalid-input cases. Cortex-M0+ compilation is not a microcontroller bench run.

## Additional mechanical and controls studies

- [VibraMount](https://github.com/guhanp09/vibramount): stiffness/damping sweeps and
  parametric vibration-isolator CAD with declared load and operating assumptions.
- [Laminate Bench](https://github.com/guhanp09/laminate-bench): laminate stiffness,
  beam calculations, layup screening and coupon-fixture design; no physical coupons claimed.
- [Low Altitude Guard](https://github.com/guhanp09/low-altitude-guard): C++ clearance-control
  and fault simulation, including a retained slow-bias limitation.
- [Ground Effect Lab](https://github.com/guhanp09/ground-effect-lab): lifting-line,
  ground-effect sensitivity and mission energy/pack closure.
- [PartsGraph](https://github.com/guhanp09/partsgraph): BOM dependencies and
  inventory-constrained supply scenarios, using explicit assumed commercial inputs.

[All projects](README.md) · [Product work](product-work.md) · [Analytics work](analytics-work.md)
