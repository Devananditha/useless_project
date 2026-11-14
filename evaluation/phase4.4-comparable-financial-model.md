# Phase 4.4 Comparable Financial Model: Unified Economic Accounting

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/phase4.4-comparable-financial-model.md`  
**Stage:** Phase 4.4 – Final Concept Integrity, Comparative Validation & Decision Gate  
**Standard Compliance:** `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`  
**Audit Authorities:** Financial Model Auditor, Automotive Dealership Operations Expert  
**Date of Audit:** November 14, 2026  
**Audit Determination:** **APPLES-TO-APPLES ACCOUNTING STRUCTURE ESTABLISHED; DEMAND ABSORPTION AND PREVENTABILITY PENALTIES MODELED**

---

## 1. Methodological Correction: Apples-to-Apples Accounting

In Phase 4.3, TitleGuard was evaluated primarily via **net cash savings** ($59.6k), while PartsRescue was evaluated via **net gross profit** ($128.4k). Comparing cash expense reduction against top-line gross profit creation was an apples-to-oranges comparison.

To establish parity, both concepts are now modeled under an identical **eight-category accounting framework**:
1. **Direct Cash Operating Savings:** Hard dollar reductions in recurring dealership expenses.
2. **Incremental Gross Profit Generated:** New gross profit earned from billable technician labor and installed parts.
3. **Recoverable Operational Capacity:** Raw capacity unlocked (idle hours or capital float).
4. **Capacity Utilization / Demand Absorption:** The percentage of recovered capacity actually monetized.
5. **Software Subscription SaaS Expense:** -$850/month (-$10,200/year) across both models.
6. **Net Annual Operating Benefit:** Direct Cash Savings + Incremental Gross Profit - Software Expense.
7. **Non-Cash Protected Margin:** Preserved vehicle gross profit from prevented contract unwinds.
8. **Unverified Addendum Benefits:** Hypothesized CSI retention bonuses or customer lifetime value gains (tracked separately as unverified assumptions).

---

## 2. Concept A: TitleGuard Comparable Financial Model

### 2.1 Audited Assumptions & Preventability Penalties
Earlier drafts assumed 100% of out-of-state trade-in delays were preventable by document pre-auditing. In reality, deals are often delayed by non-document issues (e.g., customer non-payment, uncooperative out-of-state lienholders, physical inspection hold-ups). We apply an explicit **Preventability Factor** ($70\%\text{–}90\%$):

* **Monthly Affected Trades:** Conservative = 8; Moderate = 12; Aggressive = 16.
* **Preventability Factor:** Conservative = 70% (5.6 effective deals); Moderate = 80% (9.6 effective deals); Aggressive = 90% (14.4 effective deals).
* **Average Financed Balance:** $30,000 / $35,000 / $40,000.
* **CIT Days Reduced:** 10 days / 15 days / 20 days.
* **Commercial Borrowing APR:** 8.00% / 8.50% / 9.00%.
* **Floorplan Formula:**
  $$\text{Annual Floorplan Savings} = (\text{Monthly Deals} \times \text{Preventability}) \times \text{Balance} \times \left(\frac{\text{Days}}{365}\right) \times \text{APR} \times 12$$

```
+========================================================================================================================+
|                                  TITLEGUARD UNIFIED COMPARABLE FINANCIAL TABLE                                         |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| #  | Financial Category                     | Conservative Case  | Moderate Baseline  | Aggressive Case                |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 01 | **Direct Cash Operating Savings:**     |                    |                    |                                |
|    | - Avoided Floorplan Borrowing Interest | +$4,418.63 / year  | +$14,084.38 / year | +$34,086.58 / year             |
|    | - Avoided Third-Party Expediter Fees   | +$16,200.00 / year | +$32,400.00 / year | +$48,600.00 / year             |
|    | - Avoided Unwind Direct Cash Losses    | +$4,500.00 / year  | +$7,500.00 / year  | +$12,000.00 / year             |
|    | - Avoided Title Clerk Overtime Expense | +$2,880.00 / year  | +$4,320.00 / year  | +$6,480.00 / year              |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
|    | **Subtotal Gross Cash Savings**        | **+$27,998.63 / yr**| **+$58,304.38 / yr**| **+$101,166.58 / yr**          |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 02 | **Incremental Gross Profit Generated** | **$0.00 / year**   | **$0.00 / year**   | **$0.00 / year**               |
|    | *(TitleGuard reduces expense; no labor)*| (Pure cost reduction)| (Pure cost reduction)| (Pure cost reduction)        |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 03 | **Recoverable Operational Capacity**   | $168,000 / month   | $336,000 / month   | $576,000 / month               |
|    | *(Balance Sheet Working Capital Float)*| (CIT Liquidity)    | (CIT Liquidity)    | (CIT Liquidity)                |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 04 | **Capacity Utilization / Absorption**  | **100% Cash Velocity**| **100% Cash Velocity**| **100% Cash Velocity**      |
|    | *(Immediate balance sheet relief)*     | (Zero inventory risk)| (Zero inventory risk)| (Zero inventory risk)        |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 05 | **Software SaaS Cost ($850/mo)**       | -$10,200.00 / year | -$10,200.00 / year | -$10,200.00 / year             |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 06 | **NET ANNUAL CASH BENEFIT**            | **+$17,798.63 / yr**| **+$48,104.38 / yr**| **+$90,966.58 / yr**           |
|    | *(Net Hard Operating Cash Profit)*     | **(2.75x SaaS ROI)**| **(5.72x SaaS ROI)**| **(9.92x SaaS ROI)**           |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 07 | **Non-Cash Protected Margin (Unwinds)**| +$4,800.00 / year  | +$8,000.00 / year  | +$12,800.00 / year             |
|    | *(Retained Front/Back Gross @ $3.2k)*  | (1.5 unwinds saved)| (2.5 unwinds saved)| (4.0 unwinds saved)            |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 08 | **TOTAL COMPREHENSIVE ECONOMIC VALUE** | **+$22,598.63 / yr**| **+$56,104.38 / yr**| **+$103,766.58 / yr**          |
+========================================================================================================================+
```

---

## 3. Concept B: PartsRescue AI Comparable Financial Model

### 3.1 Audited Assumptions & Demand Absorption Modeling
Earlier drafts counted 100% of recovered idle technician hours as billable revenue. In fixed operations, an unlocked bay hour is useless if the service drive has no customer appointment demand to absorb it. We apply explicit **Demand Absorption Rates** ($50\%\text{–}85\%$):

* **Benchmark Dealership:** 15 mechanical bays, 18 parts delays/week (1.2 delays/bay/week), 3.5 dead hours per delay = **63.0 stalled hours/week** (3,150 hours/year over 50 weeks).
* **Recoverable Capacity:** Conservative = 25% (787.5 hrs/yr); Moderate = 40% (1,260.0 hrs/yr); Aggressive = 60% (1,890.0 hrs/yr).
* **Demand Absorption (Monetization Rate):** Conservative = 50% (393.8 billable hrs); Moderate = 70% (882.0 billable hrs); Aggressive = 85% (1,606.5 billable hrs).
* **Customer Door Rate:** $160.00 / billable labor hour.
* **Blended Gross Profit per Hour:** $110.00 / hour (Labor margin + parts gross margin).

```
+========================================================================================================================+
|                                 PARTSRESCUE UNIFIED COMPARABLE FINANCIAL TABLE                                         |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| #  | Financial Category                     | Conservative Case  | Moderate Baseline  | Aggressive Case                |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 01 | **Direct Cash Operating Savings:**     |                    |                    |                                |
|    | - Avoided Expedited Courier Surcharges | +$2,000.00 / year  | +$4,000.00 / year  | +$6,500.00 / year              |
|    | - Avoided Duplicate Order Restock Fees | +$1,000.00 / year  | +$2,000.00 / year  | +$3,500.00 / year              |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
|    | **Subtotal Direct Cash Savings**       | **+$3,000.00 / yr**| **+$6,000.00 / yr**| **+$10,000.00 / yr**           |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 02 | **Incremental Gross Profit Generated:**|                    |                    |                                |
|    | - Realized Billable Labor & Parts Hours| 393.8 hours / year | 882.0 hours / year | 1,606.5 hours / year           |
|    | - Incremental Service Revenue ($160/hr)| $63,000.00 / year  | $141,120.00 / year | $257,040.00 / year             |
|    | - **Gross Profit Earned ($110/hr GP)** | **+$43,312.50 / yr**| **+$97,020.00 / yr**| **+$176,715.00 / yr**          |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 03 | **Recoverable Operational Capacity**   | 787.5 hours / year | 1,260.0 hours / yr | 1,890.0 hours / year           |
|    | *(Raw Unlocked Technician Lift Time)*  | (Unapplied Labor)  | (Unapplied Labor)  | (Unapplied Labor)              |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 04 | **Capacity Utilization / Absorption**  | **50.0% Absorbed** | **70.0% Absorbed** | **85.0% Absorbed**             |
|    | *(Subject to shop customer demand)*    | (Slow shop season) | (Normal metro shop)| (High backlog demand)          |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 05 | **Software SaaS Cost ($850/mo)**       | -$10,200.00 / year | -$10,200.00 / year | -$10,200.00 / year             |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 06 | **NET ANNUAL OPERATING BENEFIT**       | **+$36,112.50 / yr**| **+$92,820.00 / yr**| **+$176,515.00 / yr**          |
|    | *(Gross Profit + Cash - SaaS Expense)**| **(4.54x SaaS ROI)**| **(10.10x SaaS ROI)**| **(18.31x SaaS ROI)**         |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 07 | **Non-Cash Operational Benefits**      | Negligible ($0.00) | Negligible ($0.00) | Negligible ($0.00)             |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 08 | **Unverified Addendum Benefits (CSI):**| +$10,000.00 / year | +$20,000.00 / year | +$35,000.00 / year             |
|    | *(Hypothetical CSI bonus & retention)* | *(Assumption)*     | *(Assumption)*     | *(Assumption)*                 |
+----+----------------------------------------+--------------------+--------------------+--------------------------------+
| 09 | **TOTAL COMPREHENSIVE ECONOMIC VALUE** | **+$46,112.50 / yr**| **+$112,820.00 / yr**| **+$211,515.00 / yr**         |
+========================================================================================================================+
```

---

## 4. Head-to-Head Comparative Financial Synthesis

```
+========================================================================================================+
|                                    UNIFIED COMPARISON ACROSS FINANCIAL DOMAINS                         |
+================================+===================================+===================================+
| Financial Metric               | Concept A: TitleGuard             | Concept B: PartsRescue AI         |
+================================+===================================+===================================+
| **Economic Mechanism**         | Cost & Loss Avoidance             | Top-Line Revenue & GP Expansion   |
|                                | (Risk & Expense Mitigation)       | (Labor & Parts Billing Growth)    |
+--------------------------------+-----------------------------------+-----------------------------------+
| **Net Operating Benefit**      | **+$48,104.38 / year**            | **+$92,820.00 / year**            |
| **(Moderate Baseline)**        | (Direct Hard Cash Savings)        | (Gross Profit Generated Less SaaS)|
+--------------------------------+-----------------------------------+-----------------------------------+
| **Working Capital Velocity**   | **$336,000 / month liberated**    | Negligible ($5k–$10k holding cost)|
| **(Balance Sheet Liquidity)**  | (Major relief for credit lines)   | (No material balance sheet impact)|
+--------------------------------+-----------------------------------+-----------------------------------+
| **Absorption Volatility**      | **ZERO VOLATILITY**               | **HIGH VOLATILITY**               |
|                                | Avoided interest and fees are     | Profit depends on having customers|
|                                | 100% realized immediately.        | to buy newly unlocked hours.      |
+--------------------------------+-----------------------------------+-----------------------------------+
| **Downside Resilience**        | **Conservative: +$17,798.63 / yr**| **Conservative: +$36,112.50 / yr**|
| **(Net Operating Benefit)**    | (Always net cash positive)        | (Profitable even at 50% absorption|
+================================+===================================+===================================+
```

### Financial Verdict:
* **PartsRescue wins on net operating profit generation:** In the moderate case, it produces **$92,820.00/yr in net operating gross profit**, outperforming TitleGuard's **$48,104.38/yr in net operating cash savings** by nearly **1.93x**.
* **TitleGuard wins on capital velocity and certainty:** It liberates **$336,000/month in frozen floorplan liquidity**, and its cash recovery carries **zero demand-absorption risk**.
