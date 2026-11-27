# CapacityBridge

An independent fulfilment-centre capacity and D0 promise-planning study. It translates forecast parcel demand into staffing by FC, wave and processing stage, and into internal/third-party carrier reservations. Resources are frozen before demand and disruption scenarios are evaluated.

All operational inputs are simulated assumptions. This is not an operating record from an employer or logistics partner.

## Results and evidence

[Planning review](reports/planning_review.pdf) · [Excel capacity workbook](reports/capacity_plan.xlsx) · [Executed metrics](reports/metrics.json) · [Python planner](src/capacitybridge/planner.py) · [SQL review](src/capacitybridge/review.sql) · [Tests](tests/test_planner.py)

Across the defined 120 demand and disruption cases, the 12% reserve policy raises modelled overall service attainment from **86.6% to 94.8%**, with **12.3% higher operating cost** than forecast-only planning. D0 attainment stays about **99.1% under both policies**. The finding is a conditional cost/service trade-off; it does not establish actual savings or remove carrier-cutoff risk.

Both policies are run on every case, producing 240 policy evaluations. The [full results](reports/scenario_runs.csv), [segment service review](reports/service_review.csv), [demand reconciliation](reports/reconciliation.csv) and [methodology](docs/methodology.md) make the comparison inspectable.

## Run

From this directory, using Python 3.11 or later. Python 3.12 and the versions in `requirements-tested.txt` were used for the included run:

```sh
python -m pip install -e . -c requirements-tested.txt
capacitybridge
python -m unittest discover -s tests -v
```

The run regenerates CSVs, a SQLite review database and measured summaries under `reports/`. The included Excel workbook reviews the saved peak plan. Its arithmetic and cost formulas recalculate when the included rates or staffing cells change. Rerun the Python planner to reoptimise allocations after changing operational inputs; Excel does not rerun the integer solver.

## Planning decisions

- Six hypothetical FCs in three city pairs, two dispatch waves and three processing stages.
- Integer staffing and carrier booking under per-asset throughput and capacity limits.
- BAU volume and a peak-event assumption of 2.8 times BAU demand.
- D0 service requires assumed dispatch plus carrier transit time to meet a 21:00 deadline. A PM third-party route takes too long and is excluded.
- A forecast-only policy and a 12% reserve policy share the same realised demand draws.
- 120 distinct BAU/peak and disruption cases, evaluated under both policies. Fifteen seeded demand streams are reused across conditions, so these are not 120 independent empirical observations.
- Demand, shipments and missed promises reconcile by case, city, wave, promise and policy in SQL.

## Review the work

The [planning review](reports/planning_review.pdf) explains results and decision limits. The [Excel workbook](reports/capacity_plan.xlsx) contains FC and carrier resource reviews. The [SQLite database](reports/planning.sqlite) includes underlying demand and allocation records and analytical views. [Validation evidence](docs/validation.json) records the checks performed.

## Limits

Inventory is assumed available at both FCs within a city. No SKU placement, road routing, labour-law constraint, real-time travel time, queueing or stochastic transit reliability is modelled. Each four-hour processing window is approximated by its aggregate bottleneck throughput. All stages must complete before its stated dispatch time. The model does not schedule individual tasks within that window. An eligible allocated parcel is counted as meeting its promise under assumed transit times; this is not a measured customer delivery. Missed-parcel penalties are assumed planning priorities, not compensation paid. Costs exclude leases, inventory carrying and fixed corporate overhead. The reserve policy must be judged against its extra budget and remaining risks rather than represented as real savings.

## Research context

The public description of FC capacity, delivery-carrier allocation and network planning in Agarwal et al., *Faster, Smarter, Leaner: How Flipkart Optimized Its Supply Chain to Unlock Growth*, INFORMS Journal on Applied Analytics (2026), helped identify relevant decision types. The present model, code, data and results are independent and do not reproduce that company's proprietary systems or performance.

https://doi.org/10.1287/inte.2025.0282
