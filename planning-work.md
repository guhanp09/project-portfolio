# Supply chain and business planning

Working planning models and commercial analyses, with runnable code, Excel reviews, reconciled data and explicit assumptions.

## CapacityBridge — FC capacity and same-day planning

[Project and runnable source](projects/capacitybridge) · [Planning review](projects/capacitybridge/reports/planning_review.pdf) · [Excel capacity workbook](projects/capacitybridge/reports/capacity_plan.xlsx) · [Full metrics](projects/capacitybridge/reports/metrics.json) · [SQL](projects/capacitybridge/src/capacitybridge/review.sql) · [Tests](projects/capacitybridge/tests/test_planner.py)

**Decision:** How much staffing and carrier capacity should be reserved before demand arrives, and which service risks remain after adding capacity?

The model translates BAU and peak-event volume forecasts into staffing by FC, wave and picking/packing/sorting stage. Six hypothetical FCs form three city pairs. Integer optimisation allocates internal and third-party carrier capacity, with explicit dispatch and transit assumptions for D0 same-day promises. The resulting resources are frozen before actual demand draws and disruptions are evaluated.

| Defined simulation result | Forecast only | 12% planning reserve |
| --- | ---: | ---: |
| Overall service attainment | 86.6% | 94.8% |
| D0 service attainment | 99.1% | 99.1% |
| Mean operating cost per case, INR | 252,037 | 283,042 |

The reserve policy improves overall service by 8.3 percentage points with 12.3% higher operating cost. It does not materially improve D0 attainment in this comparison. Peak internal-carrier loss still reduces modelled D0 attainment to 96.7%, identifying a constraint that general reserve alone does not solve.

**Evidence:** 120 BAU/peak and disruption cases, 240 policy runs and 15 shared seeded demand streams. SQL reconciles demand, shipments and missed promises in 2,880 groups with zero parcel differences. Thirteen tests cover cutoffs, capacities, conservation, frozen resources, outages and invalid inputs. The Excel workbook contains staffing, bottleneck-throughput and carrier-cost formulas; input-change recalculation was checked in a native spreadsheet engine.

**Decision limits:** All operational inputs are simulated. Inventory is assumed available at both same-city FCs, and processing is represented by aggregate wave capacity rather than detailed queues or individual task schedules. No actual network results, savings, partner contracts or team-management experience are inferred. See the [methodology](projects/capacitybridge/docs/methodology.md) and [validation record](projects/capacitybridge/docs/validation.json).

## PartsGraph — Inventory availability and supplier risk

[Source](https://github.com/guhanp09/partsgraph) · [Scenario review](https://github.com/guhanp09/partsgraph/blob/main/reports/analysis.md) · [Excel model](https://github.com/guhanp09/partsgraph/blob/main/reports/scenario_review.xlsx)

Traces shared-component shortages through four product variants and 14 components, then allocates inventory under demand and margin assumptions. In the simulated seal-outage scenario, buildable units fall from 36 to two; compatible spare inventory restores 14 units. A nominally approved 12V fan is rejected against a 24V requirement. The analysis compares mitigation cost with recoverable contribution without double-counting shared stock. Demand, inventory, suppliers and compatibility properties are scenario assumptions.

## Revenue Anatomy — Retail performance and cost review

[Source](https://github.com/guhanp09/revenue-anatomy) · [Analysis](https://github.com/guhanp09/revenue-anatomy/blob/main/reports/analysis.md) · [Excel management model](https://github.com/guhanp09/revenue-anatomy/blob/main/reports/commercial_review.xlsx) · [Management presentation](https://github.com/guhanp09/revenue-anatomy/blob/main/reports/management_review.pptx)

Analyses all 541,909 public UCI Online Retail transaction rows with Python and SQL. Sales, credits, quarantined adjustments and duplicate flags remain inspectable. The October–November 2011 review explains GBP 391,051.58 of net revenue movement through a volume–mix–price bridge. An eight-tab Excel model and five-slide management review translate findings into account, operations and finance recommendations. Missing product costs remain explicit assumptions; the historical revenue movement is not revenue created for an employer.

## CashCycle — Financial forecasts and liquidity risk

[Source](https://github.com/guhanp09/cashcycle) · [Analysis](https://github.com/guhanp09/cashcycle/blob/main/reports/analysis.md) · [Excel cash plan](https://github.com/guhanp09/cashcycle/blob/main/reports/cash_plan.xlsx)

Reconciles 3,916 synthetic invoices, receipts and credits into a thirteen-week cash forecast, with backtests at twelve historical cutoffs. A modelled INR 3.54 lakh minimum cash shortfall highlights an equipment-payment commitment despite positive trading cash generation. The workbook separates editable assumptions, cash roll-forward calculations and zero-difference controls. The work is a simulated planning study rather than an actual cash-release result.

[All portfolio areas](README.md) · [Analytics portfolio](analytics-work.md) · [Public repositories](https://github.com/guhanp09?tab=repositories)
