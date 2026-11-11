# Guhan Purushothaman — Product Work

I build products and analytical tools that make a decision inspectable: what problem is being addressed, what was implemented, what the evidence supports, and what needs to happen next. My work spans a creator hiring marketplace, customer-support tools, experimentation and technical communication.

The search prototype and three analytical tools below were implemented in **November 2026**. Their results come from public data or explicitly synthetic scenarios. The repositories include runnable code, tests, product briefs, decision records and committed reports.

## Multilingual information access: OpenAtlas

**Problem:** a reader needs useful sources in a chosen language, enough context to judge them, and control over preview size.

**Built:** a responsive English, Bengali and Telugu search prototype with source links, an explicit language picker, compact/expanded previews and local retrieval over 3,931 passages from Google Research's TyDi QA data.

**Measured:** on a derived closed-corpus retrieval task with 1,222 held-out queries, validation-selected word/character ranking improved language-balanced Recall@5 from **76.5% to 86.3%**. Compact previews reduced mean paired JSON response bytes by **39.8%**, preserving ranked links.

**Decision:** move toward a moderated pilot and prioritize Telugu's remaining quality gap. Native-reader comprehension and actual mobile performance are unmeasured. These are offline retrieval and payload results, not an official TyDi QA score or production user outcomes. The project is independent and has no Google affiliation.

[Code and prototype setup](https://github.com/guhanp09/openatlas) · [Evaluation](https://github.com/guhanp09/openatlas/blob/main/reports/decision.md) · [Product brief](https://github.com/guhanp09/openatlas/blob/main/docs/product-brief.md) · [Research and launch plan](https://github.com/guhanp09/openatlas/blob/main/docs/launch-plan.md)

## A working product: ByteSized Careers

**Problem:** creative hiring involves fragmented job information, portfolios, applications and follow-up.

**Built:** a pre-launch marketplace with job posting, talent portfolios, applicant pipelines, messaging and interview coordination. An AI-assisted import turns supplied job text or supported public URLs into an editable private draft with source evidence and missing-information review. Manual posting remains available independently of AI.

**Product choice:** require review before imported information becomes a listing. The companion early-access product uses saved onboarding steps, verified email, consent-aware contact capture and protected administration.

**Evidence and status:** the waitlist is deployed; the main marketplace is pre-launch. No adoption or revenue claim is made.

[Marketplace source](https://github.com/guhanp09/bytesized-careers) · [Onboarding source](https://github.com/guhanp09/bytesized-careers-waitlist) · [Early access](https://bytesizedcareers.com/early-access)

## An ML feature with a review boundary: SignalDesk

**Problem:** support teams need useful routing suggestions without treating every model prediction as reliable.

**Built:** a 77-intent text classifier, simple keyword baseline, validation-selected routing threshold and per-intent error reports. Training overlaps and duplicates are removed; the official test split stays held out from fitting and threshold selection.

**Measured:** 87.9% overall accuracy on 3,080 BANKING77 test queries. At the selected threshold, accepted-query precision is 92.0% at 90.8% coverage. There are still **223 wrong accepted routes**.

**Decision:** retain a reviewed pilot. Handwritten challenge failures show that in-domain precision does not establish domain-boundary safety. Suggested routes never send replies or change accounts. Review-cost estimates are hypothetical assumptions, not measured savings.

[Code and setup](https://github.com/guhanp09/signaldesk) · [Evaluation and failures](https://github.com/guhanp09/signaldesk/blob/main/reports/evaluation.md) · [Product brief](https://github.com/guhanp09/signaldesk/blob/main/docs/product-brief.md) · [Checks](https://github.com/guhanp09/signaldesk/actions)

## A defensible launch decision: FirstMile

**Problem:** an onboarding experiment can look successful when event instrumentation, incomplete observation windows or increased errors make the result unreliable.

**Built:** a reusable CSV analysis tool for seven-day activation, ordered event funnels, mature-cohort denominators, confidence intervals, fixed-horizon sample planning, assignment-ratio checks and an error-rate guardrail.

**Demonstrated:** three synthetic scenarios lead to three different outcomes: eligible for review, stop for increased errors, and block for invalid allocation. The first two fixtures each contain 5,200 assigned users; their conversion difference is a generated test condition.

**Decision:** a positive primary metric cannot override a failed validity or harm check. Passing the analysis produces a recommendation for human review, not an automatic rollout.

[Code and setup](https://github.com/guhanp09/firstmile) · [Scenario results](https://github.com/guhanp09/firstmile/blob/main/reports/summary.json) · [Event contract](https://github.com/guhanp09/firstmile/blob/main/docs/event-contract.md) · [Checks](https://github.com/guhanp09/firstmile/actions)

## A simpler policy that won: MarketLane

**Problem:** a creative-services marketplace must choose launch breadth, fees and allocation rules while balancing fulfilment, seller payouts and platform contribution.

**Built:** a simulator with daily supply capacity, budgets, skills, expiring demand and a reconciled transaction ledger. Four policies are compared across 40 paired seeds, followed by 108 demand/fee sensitivity runs.

**Found in the model:** focused oldest-first matching fills 93.7% of synthetic demand; a daily matching optimizer fills 90.3%. The optimizer maximizes a daily objective but leaves some older jobs to expire. A higher fee increases modeled contribution while reducing fill.

**Decision:** prefer the simpler oldest-first policy as a pilot candidate under these assumptions. Validate demand, seller availability and willingness to pay with real research before treating the simulation as a launch plan. These are **268 simulated runs, not market observations or forecasts**.

[Code and setup](https://github.com/guhanp09/marketlane) · [Decision memo](https://github.com/guhanp09/marketlane/blob/main/reports/decision.md) · [Assumptions and choices](https://github.com/guhanp09/marketlane/blob/main/docs/decisions.md) · [Checks](https://github.com/guhanp09/marketlane/actions)

## More implementation and communication evidence

| Work | Evidence |
|---|---|
| [Casebook](https://github.com/guhanp09/casebook) | Version-aware retrieval over 1,365 public documentation and issue chunks; cited excerpts, abstention and a documented 78-question author-developed evaluation. |
| [Online Dictionary Admin](https://github.com/guhanp09/online-dictionary-admin) | Android/Kotlin client and FastAPI/MySQL service; indexed lookup, validation, audit history and automated checks. |
| [Diagonal Grid Puzzle](https://github.com/guhanp09/diagonal-grid-puzzle-2021) | Unity/C# puzzle with diagonal reachability and completion feedback; source reconstruction and independent boundary/blocker tests are documented. |
| [Over the Fence](https://github.com/guhanp09/over-the-fence) | A 121-page book explaining seven mathematical ideas with dialogue and 68 illustrations, plus a reproducible publishing workflow. |
| [Indian Finance Academy films](https://github.com/guhanp09/indian-finance-academy-films) | Research, scripts, storyboards and Remotion/React production assets for finance documentaries. |

[Browse the full portfolio](README.md)
