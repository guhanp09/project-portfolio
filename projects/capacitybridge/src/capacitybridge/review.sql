DROP VIEW IF EXISTS demand_reconciliation;
CREATE VIEW demand_reconciliation AS
WITH delivered AS (
 SELECT case_id, policy, city, wave, promise, SUM(parcels) AS served
 FROM shipments GROUP BY case_id, policy, city, wave, promise
), policies AS (SELECT DISTINCT policy FROM scenario_runs)
SELECT d.case_id, p.policy, d.city, d.wave, d.promise, d.parcels AS demand,
       COALESCE(s.served, 0) AS served, COALESCE(m.parcels, 0) AS missed,
       d.parcels - COALESCE(s.served, 0) - COALESCE(m.parcels, 0) AS difference
FROM demand d CROSS JOIN policies p
LEFT JOIN delivered s ON d.case_id=s.case_id AND p.policy=s.policy
 AND d.city=s.city AND d.wave=s.wave AND d.promise=s.promise
LEFT JOIN misses m ON d.case_id=m.case_id AND p.policy=m.policy
 AND d.city=m.city AND d.wave=m.wave AND d.promise=m.promise;

DROP VIEW IF EXISTS service_review;
CREATE VIEW service_review AS
SELECT d.regime, d.risk, r.policy, r.city, r.wave, r.promise,
       SUM(r.demand) AS demand, SUM(r.served) AS served, SUM(r.missed) AS missed,
       1.0*SUM(r.served)/NULLIF(SUM(r.demand),0) AS service_attainment
FROM demand_reconciliation r
JOIN (SELECT DISTINCT case_id, regime, risk FROM demand) d USING(case_id)
GROUP BY d.regime, d.risk, r.policy, r.city, r.wave, r.promise;
