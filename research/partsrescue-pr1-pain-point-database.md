# PartsRescue PR1: Dealership Pain Point Database & Operational Friction Inventory

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `research/partsrescue-pr1-pain-point-database.md`  
**Phase:** PR1 — Deep Dealership Problem Discovery & Operational Validation  
**Standard Compliance:** `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`  
**Research Entity:** PartsRescue AI Innovation Research Team  
**Date:** November 14, 2026  
**Focus:** Exhaustive Inventory of Friction Points Across Service, Parts, and Shop Floor  

---

## 1. Database Architecture & Classification Schema

This database inventories real-world dealership friction points across five operational operational zones:
1. **Service Drive (Advisors & Customers):** Appointment promises, repair estimates, vehicle delivery commitments.
2. **Technician Bay (Shop Floor & Lifts):** Teardown diagnosis, billable flag-hour momentum, physical lift occupancy.
3. **Parts Counter (Counter Staff & Specialists):** Catalog lookup, supersession navigation, inventory allocations.
4. **Inventory & Procurement (Purchasing & Warehouse):** Supplier replenishment, backorder tracking, freight costs.
5. **Dealership Executive Leadership (GM, CFO, Fixed Ops Director):** Departmental margins, loaner car costs, CSI scores.

Each friction point is classified by:
* **Friction ID & Title**
* **Primary Stakeholder Impacted**
* **Trigger Event & System Failure**
* **Current Operational Workaround**
* **Financial & Throughput Severity:** Critical / High / Medium / Low
* **Frequency of Occurrence:** Daily / Weekly / Per Repair Order

---

## 2. Master Pain Point Inventory

```
+========================================================================================================================+
|                                        DEALERSHIP PARTS FRICTION POINT DATABASE                                        |
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| ID | Title & Domain       | Stakeholder        | Severity & Freq.   | Current Workaround | Core Operational Failure    |
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| P01| The "Lift Prison"    | Flat-Rate Tech,    | **CRITICAL**       | Roll car out or let| Disassembled car traps lift;|
|    | Teardown Stall       | Service Manager    | Daily (2–4/shop)   | bay sit dead.      | tech loses billable hours.  |
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| P02| Departmental Metric  | Parts Manager vs   | **HIGH**           | Uncoordinated phone| Parts saves $15 on freight; |
|    | Conflict (Silo Trap) | Service Director   | Daily (Ongoing)    | arguing at counter.| Service loses $160 in labor.|
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| P03| Ghost Backorder      | Service Advisor,   | **CRITICAL**       | Daily phone calls  | OEM issues backorder with no|
|    | Black Hole           | Customer           | Weekly (5–8/shop)  | to OEM PDC hotline.| release date; customer mad. |
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| P04| Supersession         | Parts Counter,     | **HIGH**           | Manual TSB reading | New revision ordered, but   |
|    | Incomplete Assembly  | Technician         | Weekly (3–5/shop)  | and second order.  | co-dependent bracket omitted|
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| P05| Warranty Aftermarket | Warranty Admin,    | **CRITICAL**       | Wait for OEM PDC   | Local aftermarket in stock, |
|    | Legality Trap        | Service Advisor    | Daily (Frequent)   | or risk clawback.  | but OEM warranty strictly no|
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| P06| Sister-Store Hoarding| Parts Counter,     | **MEDIUM**         | Pleading via phone;| Holding store hides part to |
|    | Friction             | Inventory Manager  | Weekly (4–6/shop)  | GM escalation.     | protect its own retail pool.|
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| P07| Customer Pay Fitment | Service Advisor,   | **HIGH**           | Advisor leaves desk| Customer won't pay $450 OEM;|
|    | Price Resistance     | Customer           | Daily (5–10/shop)  | to find aftermarket| needs fast certified alt.   |
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| P08| Accumulating Loaner  | CFO, General       | **HIGH**           | Dealer absorbs rental| Stranded warranty car burns|
|    | Vehicle Expense      | Manager            | Weekly (Ongoing)   | car cost ($45/day).| $45/day rental expense.     |
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| P09| Greasy Return &      | Parts Inventory,   | **MEDIUM**         | Parts absorbed into| Wrong part opened on bench; |
|    | Restocking Loss      | Parts Manager      | Weekly (2–4/shop)  | obsolescence bin.  | vendor rejects dirty return.|
+----+----------------------+--------------------+--------------------+--------------------+-----------------------------+
| P10| Multi-RO Stock       | Shop Dispatcher,   | **HIGH**           | First tech to grab | 1 part on shelf; 2 customer |
|    | Cannibalization      | Technicians        | Daily (1–3/shop)   | it wins the part.  | vehicles waiting in bays.   |
+========================================================================================================================+
```

---

## 3. Deep-Dive Profile of Critical Friction Points

### P01: The "Lift Prison" Teardown Stall
* **Operational Mechanism:** A customer brings in a vehicle for an oil leak or knocking noise. The technician puts the vehicle on a 2-post hydraulic lift, disassembles the front subframe, suspension, or timing cover, and discovers a damaged seal, cracked bracket, or worn guide rail. The technician walks to the parts counter. The counterperson reports: "Out of stock; 3 days out from the PDC."
* **The Failure:** The vehicle is mechanically immobilized. It cannot be steered or rolled off the lift safely without spending 1.5 unbillable hours reinstalling subframe bolts. The bay is trapped ("lift prison").
* **Impact:** 
  * Technician loses momentum and billable flag hours.
  * Dealership loses 8–16 billable hours of lift capacity ($1,200–$2,500 gross revenue potential).
  * Current workaround: Push the vehicle into the back lot using 4 lot porters and a forklift, risking shop injury and lot damage, or leave it dead on the lift.

### P02: Departmental Metric Conflict (The Silo Trap)
* **Operational Mechanism:** Dealerships evaluate departmental managers on opposing Key Performance Indicators (KPIs):
  * **Parts Manager KPI:** Evaluated on parts gross margin %, parts inventory turn rate, and minimizing freight/shipping expense.
  * **Service Manager KPI:** Evaluated on total shop labor hours billed, effective labor rate, bay efficiency, and vehicle turnaround time.
* **The Failure:** When a $40 sensor is out of stock, the parts counterperson chooses standard replenishment (arriving in 3 days with free freight) rather than ordering a $25 local hotshot courier delivery that would arrive in 45 minutes. The parts manager saves $25 in freight expenses; the service department loses $200 in idle technician billing.
* **Impact:** Dealership leadership loses total net profit because departments sub-optimize for their individual budgets.

### P03: The Ghost Backorder Black Hole
* **Operational Mechanism:** A required warranty component (e.g., an electronic power steering rack, hybrid inverter cable, or turbocharger actuator) is ordered from the OEM PDC. The OEM order status returns code `B` (Backorder) with an estimated shipping date of "TBD" (To Be Determined).
* **The Failure:** The DMS provides no automated intelligence on whether other franchised dealers nationwide possess the part on their shelves, whether alternative approved superseded part numbers exist, or whether OEM emergency buyback programs are active.
* **Impact:** The vehicle sits in the dealership back lot for 3 to 6 weeks. The customer calls the service advisor every 48 hours for updates. The service advisor spends 20 minutes on hold with the factory representative, obtaining zero new information. Customer Net Promoter Score (NPS) and CSI crater.

### P05: The Warranty Aftermarket Legality Trap
* **Operational Mechanism:** A 3-year-old vehicle under factory bumper-to-bumper warranty has a failed alternator. The factory OEM alternator is on national backorder for 14 days. A local commercial parts distributor (Worldpac or NAPA) has a certified OEM-grade Denso or Bosch alternator on the shelf 3 miles away for $220.
* **The Failure:** Dealership technicians or advisors often ask: *"Can't we just buy the local alternator and get the customer on the road?"* The Warranty Administrator must intervene: Under OEM franchise agreements, **installing an aftermarket part on a factory warranty claim results in 100% claim rejection and chargeback during factory audit**.
* **Impact:** Dealerships are legally and commercially handcuffed. Software that naively recommends "buy aftermarket" on warranty repair orders will cause thousands of dollars in warranty audit penalties.

### P07: Customer-Pay Fitment Price Resistance
* **Operational Mechanism:** An out-of-warranty customer with a 2017 vehicle is quoted $1,100 for an OEM catalytic converter or suspension control arm replacement. The customer states: "That's too expensive; I'll take the car to an independent shop."
* **The Failure:** The service advisor wants to offer an affordable, certified aftermarket alternative to save the repair, but the dealership DMS and parts counter do not display live commercial aftermarket pricing or fitment on the service drive screen. The advisor must physically walk to the back parts counter, ask for an outside quote, wait 10 minutes, and return to the customer.
* **Impact:** High customer defection rate (estimated 40%–60% of post-warranty repair estimates walk out the door to independent repair facilities).

---

## 4. Key Takeaways for Solution Design

1. **Shortages are Not Just Supply Issues—They are Coordination Failures:** The majority of dealership delays occur during the **4 to 6 hours between discovery and action**, when parts and service are misaligned on priorities.
2. **Warranty vs Customer-Pay is the Primary Fork:** A solution must treat warranty ROs (OEM only, supersession DAGs, inter-dealer transfers) completely differently from customer-pay ROs (aftermarket fitment, customer digital authorizations, price competitiveness).
3. **Physical Bay Reality Overrides Scheduling Software:** Software cannot move an engine-less car off a lift. Recovery actions must prioritize **sourcing speed** over theoretical shop resequencing when vehicles are physically immobilized.
