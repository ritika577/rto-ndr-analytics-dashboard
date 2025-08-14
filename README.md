# RTO / NDR Analytics Dashboard

A lightweight Streamlit dashboard to monitor Return‑to‑Origin (RTO) and Non‑Delivery Report (NDR) performance and highlight operational bottlenecks.

## What It Shows
- Core KPIs: Total RTOs, Average NDR %, Average Delivery Time, High Reattempt %, Top Failure Reason, Top Courier Partner
- Daily RTO trend
- NDR % by courier partner
- Average delivery time by product category
- Failure reasons distribution (stacked)
- Action distribution (RTO / Cancel / Review) from failure reasons
- Pincode lookup for courier & order stats

## Data (Expected Tables)
summary_daily_rto, summary_ndr_by_courier, summary_delivery_time, high_attempts_impact, failure_reasons, courier_partner_failure_reason, impact_of_delivery_attempts, top_couriers_by_pincode, rto_ndr (fact).

## Secrets Required
ACCESS_TOKEN, SERVER_HOSTNAME, HTTP_PATH (Databricks). Add them via Streamlit Secrets or environment variables.

## Usage Flow
1. Provide the required Databricks credentials.
2. Launch the Streamlit app.
3. Review KPIs.
4. Drill into charts for courier, attempts, and failure reasons.
5. Use the pincode search for localized insights.

## Customization Ideas
- Adjust action mapping (RTO / Cancel / Review).
- Add SLA breach or first‑attempt success metrics.
- Introduce weighting for average NDR %.
- Add export or alerting.

## Troubleshooting (Common)
Missing secrets → credentials error message.  
Empty tables → warnings in UI.  
Older Streamlit version → remove unsupported container border parameter.

## Intended Users
Operations, Logistics, CX, Performance / Analytics teams.


---
