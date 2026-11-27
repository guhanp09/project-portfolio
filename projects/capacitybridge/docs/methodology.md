# Capacity and promise planning methodology

## Decision timing

Day-ahead planning receives a forecast by city, dispatch wave and D0/regular promise. It chooses integer workers at each FC-stage-wave and carrier slots within assumed limits. Every forecast parcel is either allocated through an eligible FC/carrier or explicitly counted as missed. The objective combines four-hour staffing cost, slot reservation and delivery costs with assumed missed-promise penalties. D0 and regular penalties are INR 240 and INR 90 per missed parcel. They are priorities used for the optimisation, not observed financial loss.

The reserve policy multiplies each forecast segment by 1.12 and rounds up before making the same decision. The resulting resources are then frozen. Both policies see the same later demand draws. Recourse may reallocate demand between the two same-city FCs and available booked carrier slots, but cannot hire workers, add slots or borrow capacity from another city after observing demand.

## Assets and service

Each FC has picking, packing and sorting. Productive time is 85% of a four-hour window. Processing rates are 35, 28 and 55 parcels per productive worker-hour, respectively, scaled by an FC-specific assumed productivity factor. Committed staffing minima and physical staffing maxima are explicit inputs. Each allocated parcel consumes one unit of each stage, so throughput cannot exceed any stage's capacity. Two waves dispatch at 12:00 and 16:00; transit assumptions are four hours for internal delivery and six hours for a third party. D0 promises expire at 21:00, regular promises at 24:00. Consequently, PM third-party delivery is excluded for D0.

These are aggregate wave capacities. The abstraction assumes balanced processing completes before dispatch, rather than claiming that a detailed serial task schedule or queue has been simulated. There are no actual partner contracts, facility productivity observations or shipping SLAs in the data.

## Scenarios and evaluation

The 120 distinct cases are two volume regimes, four risk conditions and fifteen seeded demand streams. Peak forecasts are 2.8 times BAU volume with a larger D0 share. Actual demand is Poisson with a shared lognormal volume multiplier. Risk conditions are nominal, a further 20% demand surge, 15% lower packing productivity, or 25% lower internal-carrier availability. Seeds are reused across risk conditions and volume regimes; results are conditional, paired simulation comparisons.

Actual operating cost includes the planned workforce, fees for all reserved slots and per-parcel charges only for carried parcels. Missed-promise penalties are excluded from operating cost. Service attainment uses total allocated eligible parcels divided by all arriving parcels. D0 attainment uses all arriving D0 parcels as its denominator. Both aggregated rates use sums of matching numerators and denominators rather than averages of segment percentages. No post-arrival resources or future demand values enter day-ahead planning.

## Reconciliation and limitations

SQL independently checks demand equals shipments plus misses in every case/policy/city/wave/promise group. Optimiser outputs are also checked against the exact resource constraints after integer rounding. Tests cover cutoffs, missing demand, duplicates, integer flows, zero supply, frozen resources and complete carrier or packing outages. The supplied results do not establish operational readiness, forecast accuracy on real data, actual cost savings or experience managing a live FC network.
