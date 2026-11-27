"""Plan against forecasts, freeze resources, then evaluate unseen demand draws.

This is an aggregate two-wave model. Each wave includes sequential pick/pack/sort
processing before its stated dispatch time. Carrier lead times are assumptions.
No realized demand is available when the day-ahead plan is computed.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import sqlite3

import numpy as np
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, milp

STAGES = ("pick", "pack", "sort")
MODES = ("internal", "3pl")
WAVES = ("AM", "PM")
PROMISES = ("D0", "regular")
RATES = {"pick": 35.0, "pack": 28.0, "sort": 55.0}
WAGES = {"pick": 135.0, "pack": 130.0, "sort": 115.0}
HOURS = 4.0
UTILISATION = 0.85
DELIVERY_COST = {"internal": 18.0, "3pl": 30.0}
RESERVATION_COST = 2.0
MISSED_PENALTY = {"D0": 240.0, "regular": 90.0}


@dataclass(frozen=True)
class Asset:
    fc: str
    city: str
    wave: str
    productivity: float = 1.0
    internal_cap: int = 750
    external_cap: int = 900
    min_heads: tuple[int, int, int] = (3, 3, 2)
    max_heads: tuple[int, int, int] = (15, 17, 10)

    def throughput(self, stage: str) -> float:
        return HOURS * UTILISATION * RATES[stage] * self.productivity

    def carrier_cap(self, mode: str) -> int:
        return self.internal_cap if mode == "internal" else self.external_cap


def eligible(wave: str, promise: str, mode: str) -> bool:
    """Equality at the deadline is eligible; PM 3PL misses the assumed D0 SLA."""
    dispatch = {"AM": 12, "PM": 16}[wave]
    transit = {"internal": 4, "3pl": 6}[mode]
    deadline = 21 if promise == "D0" else 24
    return dispatch + transit <= deadline


def make_inputs(regime: str):
    if regime not in {"BAU", "peak"}:
        raise ValueError("regime must be BAU or peak")
    assets = []
    forecast = {}
    for city, daily, productivity in (("Chennai", 1500, 1.03), ("Bengaluru", 1300, 0.98), ("Hyderabad", 1150, 1.00)):
        for n in (1, 2):
            for wave in WAVES:
                assets.append(Asset(f"{city[:3].upper()}-{n}", city, wave,
                                    productivity * (1 if n == 1 else .96),
                                    750 if n == 1 else 690, 900))
        for wave, share in (("AM", .52), ("PM", .48)):
            total = round(daily * share * (2.8 if regime == "peak" else 1.0))
            d0 = round(total * (.62 if regime == "peak" else .50))
            forecast[city, wave, "D0"] = d0
            forecast[city, wave, "regular"] = total - d0
    return assets, forecast


def validate_inputs(assets: list[Asset], demand: dict):
    keys = [(a.fc, a.wave) for a in assets]
    if len(set(keys)) != len(keys):
        raise ValueError("duplicate FC/wave asset")
    expected = {(a.city, a.wave, p) for a in assets for p in PROMISES}
    if set(demand) != expected:
        raise ValueError("demand keys must cover every city, wave and promise exactly")
    for value in demand.values():
        if not np.isfinite(value) or value < 0 or int(value) != value:
            raise ValueError("demand must be non-negative integer parcels")
    for a in assets:
        if a.wave not in WAVES or a.productivity <= 0 or not np.isfinite(a.productivity):
            raise ValueError("invalid asset wave or productivity")
        if a.internal_cap < 0 or a.external_cap < 0:
            raise ValueError("carrier caps must be non-negative")
        if any(lo < 0 or hi < lo for lo, hi in zip(a.min_heads, a.max_heads)):
            raise ValueError("invalid staffing bounds")


def solve(assets: list[Asset], demand: dict, *, frozen: dict | None = None,
          packing_factor: float = 1.0, internal_factor: float = 1.0):
    validate_inputs(assets, demand)
    if not 0 <= packing_factor <= 1 or not 0 <= internal_factor <= 1:
        raise ValueError("availability factors must be between zero and one")
    costs, lower, upper, index = [], [], [], {}

    def variable(key, cost, lo=0, hi=np.inf):
        index[key] = len(costs)
        costs.append(cost); lower.append(lo); upper.append(hi)
        return index[key]

    for a in assets:
        if frozen is None:
            for j, stage in enumerate(STAGES):
                variable(("heads", a.fc, a.wave, stage), HOURS * WAGES[stage], a.min_heads[j], a.max_heads[j])
            for mode in MODES:
                variable(("booked", a.fc, a.wave, mode), RESERVATION_COST, 0, a.carrier_cap(mode))
        for promise in PROMISES:
            for mode in MODES:
                if eligible(a.wave, promise, mode):
                    variable(("flow", a.fc, a.wave, promise, mode), DELIVERY_COST[mode])
    for key in demand:
        variable(("missed", *key), MISSED_PENALTY[key[2]])
    rows, lows, highs = [], [], []

    def constrain(values, lo=-np.inf, hi=np.inf):
        row = np.zeros(len(costs))
        for key, value in values.items():
            row[index[key]] = value
        rows.append(row); lows.append(lo); highs.append(hi)

    for (city, wave, promise), amount in demand.items():
        terms = {("missed", city, wave, promise): 1}
        for a in assets:
            if a.city == city and a.wave == wave:
                for mode in MODES:
                    key = ("flow", a.fc, wave, promise, mode)
                    if key in index:
                        terms[key] = 1
        constrain(terms, amount, amount)
    for a in assets:
        flows = {key: 1 for key in index if key[0] == "flow" and key[1:3] == (a.fc, a.wave)}
        for stage in STAGES:
            terms = dict(flows)
            if frozen is None:
                terms[("heads", a.fc, a.wave, stage)] = -a.throughput(stage)
                limit = 0
            else:
                factor = packing_factor if stage == "pack" else 1.0
                limit = np.floor(frozen["heads", a.fc, a.wave, stage] * a.throughput(stage) * factor + 1e-9)
            constrain(terms, hi=limit)
        for mode in MODES:
            terms = {key: 1 for key in flows if key[-1] == mode}
            if frozen is None:
                terms[("booked", a.fc, a.wave, mode)] = -1
                limit = 0
            else:
                factor = internal_factor if mode == "internal" else 1.0
                limit = min(frozen["booked", a.fc, a.wave, mode], np.floor(a.carrier_cap(mode) * factor))
            constrain(terms, hi=limit)
    result = milp(np.array(costs), integrality=np.ones(len(costs)),
                  bounds=Bounds(lower, upper),
                  constraints=LinearConstraint(np.asarray(rows), lows, highs),
                  options={"time_limit": 30.0, "mip_rel_gap": 0.0})
    if not result.success:
        raise RuntimeError(f"planning solve failed: {result.message}")
    values = {key: int(round(result.x[n])) for key, n in index.items()}
    numeric = np.array([values[k] for k in index])
    lhs = np.asarray(rows) @ numeric
    if np.any(lhs < np.array(lows)-1e-6) or np.any(lhs > np.array(highs)+1e-6):
        raise AssertionError("rounded integer solution violates a capacity constraint")
    return values


def operating_cost(assets, solution, frozen=None):
    plan = frozen if frozen is not None else solution
    staff = sum(plan["heads", a.fc, a.wave, st] * HOURS * WAGES[st] for a in assets for st in STAGES)
    reserved = sum(plan["booked", a.fc, a.wave, m] * RESERVATION_COST for a in assets for m in MODES)
    carried = sum(v * DELIVERY_COST[key[-1]] for key, v in solution.items() if key[0] == "flow")
    return {"staff_cost_inr": staff, "reservation_cost_inr": reserved,
            "delivery_cost_inr": carried, "operating_cost_inr": staff + reserved + carried}


def metrics(assets, demand, solution, frozen=None):
    amount = sum(demand.values())
    d0 = sum(v for key, v in demand.items() if key[-1] == "D0")
    missed = sum(v for key, v in solution.items() if key[0] == "missed")
    d0_missed = sum(v for key, v in solution.items() if key[0] == "missed" and key[-1] == "D0")
    return {"demand": amount, "served": amount-missed, "missed": missed,
            "d0_demand": d0, "d0_served": d0-d0_missed,
            "service_attainment": (amount-missed)/amount if amount else None,
            "d0_attainment": (d0-d0_missed)/d0 if d0 else None,
            **operating_cost(assets, solution, frozen)}


def run(root: Path):
    output = root / "reports"; output.mkdir(parents=True, exist_ok=True)
    plans, all_runs, demands, shipments, resources, misses = {}, [], [], [], [], []
    for regime in ("BAU", "peak"):
        assets, forecast = make_inputs(regime)
        for name, reserve in (("forecast_only", 1.0), ("reserve_12pct", 1.12)):
            planned_demand = {key: int(np.ceil(v * reserve)) for key, v in forecast.items()}
            plans[regime, name] = solve(assets, planned_demand)
        for risk in ("nominal", "demand_surge", "packing_absence", "carrier_outage"):
            for seed in range(15):
                rng = np.random.default_rng(20261127 + seed)
                factor = rng.lognormal(-.5*.06**2, .06) * (1.20 if risk == "demand_surge" else 1)
                actual = {key: int(rng.poisson(v * factor)) for key, v in forecast.items()}
                case = f"{regime}-{risk}-{seed:02}"
                for key, value in actual.items():
                    demands.append({"case_id":case, "regime":regime, "risk":risk, "seed":seed,
                                    "city":key[0], "wave":key[1], "promise":key[2], "parcels":value})
                for name in ("forecast_only", "reserve_12pct"):
                    frozen = plans[regime, name]
                    realised = solve(assets, actual, frozen=frozen,
                                     packing_factor=.85 if risk == "packing_absence" else 1,
                                     internal_factor=.75 if risk == "carrier_outage" else 1)
                    all_runs.append({"case_id":case, "regime":regime, "risk":risk, "seed":seed,
                                     "policy":name, **metrics(assets, actual, realised, frozen)})
                    for key, value in realised.items():
                        if key[0] == "flow":
                            a = next(a for a in assets if (a.fc, a.wave) == key[1:3])
                            shipments.append({"case_id":case,"policy":name,"fc":key[1],"city":a.city,
                                              "wave":key[2],"promise":key[3],"carrier":key[4],"parcels":value})
                        elif key[0] == "missed":
                            misses.append({"case_id":case,"policy":name,"city":key[1],"wave":key[2],
                                           "promise":key[3],"parcels":value})
        for name in ("forecast_only", "reserve_12pct"):
            p = plans[regime,name]
            for a in assets:
                resources.append({"regime":regime,"policy":name,"fc":a.fc,"city":a.city,"wave":a.wave,
                                  "productivity":a.productivity,
                                  **{st+"_heads":p["heads",a.fc,a.wave,st] for st in STAGES},
                                  **{m+"_booked":p["booked",a.fc,a.wave,m] for m in MODES},
                                  "assigned_d0":sum(v for k,v in p.items() if k[0]=="flow" and k[1:4]==(a.fc,a.wave,"D0")),
                                  "assigned_regular":sum(v for k,v in p.items() if k[0]=="flow" and k[1:4]==(a.fc,a.wave,"regular"))})
    frames={"scenario_runs":pd.DataFrame(all_runs), "demand":pd.DataFrame(demands),
            "shipments":pd.DataFrame(shipments), "misses":pd.DataFrame(misses), "resource_plans":pd.DataFrame(resources)}
    database = output / "planning.sqlite"
    with sqlite3.connect(database) as db:
        for name, df in frames.items():
            df.to_sql(name, db, if_exists="replace", index=False)
            df.to_csv(output / f"{name}.csv", index=False)
        db.executescript((root / "src/capacitybridge/review.sql").read_text())
        reconciliations = pd.read_sql_query("SELECT * FROM demand_reconciliation", db)
        assert reconciliations["difference"].abs().max() == 0
        service = pd.read_sql_query("SELECT * FROM service_review", db)
        service.to_csv(output / "service_review.csv", index=False)
        reconciliations.to_csv(output / "reconciliation.csv", index=False)
    cases=[]
    for (regime, risk, policy), group in frames["scenario_runs"].groupby(["regime","risk","policy"]):
        cases.append({"regime":regime,"risk":risk,"policy":policy,"runs":len(group),
                      "service_attainment":float(group.served.sum()/group.demand.sum()),
                      "d0_attainment":float(group.d0_served.sum()/group.d0_demand.sum()),
                      "mean_operating_cost_inr":float(group.operating_cost_inr.mean()),
                      "p90_missed":float(group.missed.quantile(.9))})
    policy_summary=[]
    for policy, group in frames["scenario_runs"].groupby("policy"):
        policy_summary.append({"policy":policy,"runs":len(group),
                               "service_attainment":float(group.served.sum()/group.demand.sum()),
                               "d0_attainment":float(group.d0_served.sum()/group.d0_demand.sum()),
                               "mean_operating_cost_inr":float(group.operating_cost_inr.mean())})
    summary={"data_kind":"fully synthetic operational assumptions", "fulfilment_centres":6,
             "waves":2,"stages":3,"carrier_modes":2,"distinct_cases":120,"policy_runs":240,
             "seed_values":15,"regimes":["BAU","peak"],"risk_conditions":4,
             "maximum_demand_reconciliation_difference":0,"policies":policy_summary,"conditions":cases}
    (output / "metrics.json").write_text(json.dumps(summary,indent=2)+"\n")
    selected=plans["peak","reserve_12pct"]
    assets, forecast=make_inputs("peak")
    raw=[];carriers=[]
    for a in assets:
        raw.append({"fc":a.fc,"city":a.city,"wave":a.wave,"productivity":a.productivity,
                    "assigned_parcels":sum(v for k,v in selected.items() if k[0]=="flow" and k[1:3]==(a.fc,a.wave)),
                    **{st+"_heads":selected["heads",a.fc,a.wave,st] for st in STAGES}})
        for mode in MODES:
            carriers.append({"fc":a.fc,"city":a.city,"wave":a.wave,"mode":mode,
                             "booked":selected["booked",a.fc,a.wave,mode],
                             "d0":selected.get(("flow",a.fc,a.wave,"D0",mode),0),
                             "regular":selected.get(("flow",a.fc,a.wave,"regular",mode),0),
                             "d0_eligible":eligible(a.wave,"D0",mode)})
    (output / "workbook_inputs.json").write_text(json.dumps({"scenario":"Peak volume with 12% planning reserve",
        "wave_hours":HOURS,"productive_share":UTILISATION,"throughput_rates":RATES,"hourly_wages":WAGES,
        "delivery_costs":DELIVERY_COST,"reservation_cost":RESERVATION_COST,"fc_plan":raw,"carrier_plan":carriers},indent=2)+"\n")
    print(json.dumps({k:v for k,v in summary.items() if k!="conditions"},indent=2))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",type=Path,default=Path.cwd())
    args=parser.parse_args();run(args.root)


if __name__ == "__main__":
    main()
