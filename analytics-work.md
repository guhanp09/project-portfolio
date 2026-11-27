# Product and commercial analytics

Working analyses with inspectable SQL, input provenance, report outputs and explicit limits on what the data can establish.

## CapacityBridge — FC capacity and D0 planning

[Source and results](projects/capacitybridge) · [Planning review](projects/capacitybridge/reports/planning_review.pdf) · [Excel workbook](projects/capacitybridge/reports/capacity_plan.xlsx) · [SQL reconciliation](projects/capacitybridge/src/capacitybridge/review.sql) · [Planning portfolio](planning-work.md)

Converts BAU and peak-event parcel forecasts into staffing for six hypothetical fulfilment centres and internal/third-party carrier reservations. Integer optimisation enforces picking, packing, sorting and carrier capacities. Dispatch and transit assumptions exclude routes that miss the D0 same-day cutoff. Resources are frozen before realised demand is evaluated.

Across 120 synthetic demand and disruption cases evaluated under two policies, a 12% reserve increases modelled overall service attainment from 86.6% to 94.8%, with 12.3% higher operating cost. D0 attainment remains about 99.1% under both policies. SQL reconciles demand to shipments and misses across all 2,880 case/policy/city/wave/promise groups. Thirteen correctness tests and a formula-driven Excel review accompany the results.

These are conditional simulation outcomes, not real FC-network performance, actual savings or partner agreements. The [methodology](projects/capacitybridge/docs/methodology.md) defines the aggregate wave model, shared seed streams and inventory assumptions.

## SlotLedger — Publisher yield review

[Source and SQL](https://github.com/guhanp09/slot-ledger) · [Interactive review](https://guhanp09.github.io/slot-ledger/) · [Decision memo](https://github.com/guhanp09/slot-ledger/blob/main/reports/decision.md) · [Reporting workflow research](https://github.com/guhanp09/slot-ledger/blob/main/docs/landscape.md)

The question is whether publisher yield improved or traffic shifted toward higher-priced markets. The pipeline reconciles 504,310 synthetic event deliveries into 140,000 request facts, retaining unfilled opportunities and handling retries, visible revisions and malformed event chains. SQL uses CTEs, window functions, CUBE, percentile aggregates, calendar spines and an exact sequential mix bridge.

In the generated fixture, request RPM rises from $1.168 to $1.724, while current yield at baseline traffic weights is $1.021. Market/device/ad-unit analysis exposes a modeled India/mobile delivery problem. The report proposes investigation and a controlled test; it does not claim a real publisher result or causal lift.

The responsive review has shareable filters, SQL-derived percentiles, CSV export and metric definitions. A sourced comparison of Google Ad Manager, Prebid and Kevel reporting workflows informs scope. Proposed stakeholder perspectives are documented as proposals, not actual team meetings. Initial implementation: November 2026.

## Revenue Anatomy — Commercial performance review

[Source](https://github.com/guhanp09/revenue-anatomy) · [Analysis](https://github.com/guhanp09/revenue-anatomy/blob/main/reports/analysis.md) · [Reconciliation](https://github.com/guhanp09/revenue-anatomy/blob/main/reports/reconciliation.json)

Analyzes all 541,909 public UCI Online Retail rows with SQLite/Python. Monthly, customer and product views reconcile to the classified ledger; duplicate flags, unknown-customer revenue, credits and quarantined rows stay visible. The October–November 2011 review explains £391,051.58 of net movement through a volume–mix–price bridge with new/discontinued products and separate credit/adjustment movements.

Outputs include a formula-driven Excel model, a PDF commercial review, five-slide management presentation and interactive charts. Missing product costs and actual collections are not invented: cost scenarios are assumptions. This is historical public retail analysis, not a claim of employer revenue growth.

## FirstMile — Experiment decisions

[Source](https://github.com/guhanp09/firstmile) · [Decision](https://github.com/guhanp09/firstmile/blob/main/reports/healthy/decision.md)

Builds seven-day activation funnels from assignment/event exports, preserving all mature assigned users in the denominator. Confidence intervals, sample-ratio checks, a planned horizon and error guardrails lead to three distinct recommendations: eligible for review, stop or blocked.

The examples are synthetic. Their activation difference is a generated condition, not measured customer growth. The tool documents the gap between an interesting metric and a defensible release decision.

## Related work

- [MarketLane](https://github.com/guhanp09/marketlane): marketplace matching, pricing and unit-economics scenarios across 268 simulations.
- [SignalDesk](https://github.com/guhanp09/signaldesk): support-intent classification, independent test evaluation and validation-selected review thresholds.
- [Indian Consumer Academy](case-studies/indian-consumer-academy.md): consumer research, public explanations and documented production decisions; 6,120 followers in the November 2026 snapshot.
- [ByteSized Careers](https://github.com/guhanp09/bytesized-careers) and [early access](https://github.com/guhanp09/bytesized-careers-waitlist): a pre-launch marketplace and deployed registration workflows.

[All portfolio areas](README.md) · [All public repositories](https://github.com/guhanp09?tab=repositories)
