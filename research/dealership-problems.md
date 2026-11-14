# Dealership Operational Workflows, Friction Analysis & Problem Mapping

**Document Classification:** Phase 1 Master Research Deliverable  
**Project:** Tekion Tek-Qubit Hackathon 2026  
**Standards Compliance:** `.cursor/rules/research-standards.mdc` & `.cursor/rules/tekion-context.mdc`  
**Reference Benchmark:** `references/tekion-themes.pdf` (All 18 Official Hackathon Use Cases Verified)  
**Sources Referenced:** `research/source-register.md` (SRC-IND-01 through SRC-IND-05, SRC-TEK-01 through SRC-TEK-11, SRC-COMP-01 through SRC-COMP-10)  
**Last Updated:** 2026-11-13  

---

## 1. Dealership Economic Context & Operational Structure

Franchised automotive dealerships operate under a bifurcated business model balancing high-volume, low-margin retail transactions against high-margin customer retention and repair services:

* **Variable Operations (New & Used Vehicle Sales, F&I):**
  * *Top-Line Revenue Contribution:* Generates **85% to 88%** of total dealership revenue.
  * *Gross Profit Margin:* Highly compressed on the front end (new car front-end gross margins average **2.0% to 4.5%**, or roughly $1,500–$2,200 per vehicle). Net profitability is predominantly generated through back-end Finance & Insurance (F&I) products (service contracts, GAP insurance, finance reserve).
  * *Economic Sensitivity:* Exposed to high carrying costs, floorplan interest rates (inventory financing), and rapid depreciation on aging used inventory.
* **Fixed Operations (Service, Parts, and Collision):**
  * *Top-Line Revenue Contribution:* Accounts for only **12% to 15%** of total dealership revenue.
  * *Gross Profit Margin:* Exceptionally lucrative. Customer-pay service labor gross margins target **70% to 75%**; parts sales gross margins target **40% to 45%**.
  * *Total Gross Profit Contribution:* Fixed Operations consistently generates **48% to 55%+ of a dealership's total gross profit** (NADA Dealership Financial Profile benchmark, 2024).
  * *Service Absorption Rate:* The primary metric of dealership financial resilience, calculating the percentage of a dealership’s total fixed operating overhead (rent, mortgage, corporate salaries, utilities) covered solely by Fixed Operations gross profit. The U.S. industry average hovers between **60% and 68%**, while high-performing benchmark dealerships target **100%+** (enabling all variable sales gross profits to flow straight to net operating income).

The underlying operational vulnerability of modern dealerships is **software fragmentation**. Dealerships routinely operate between 10 and 18 distinct software point solutions loosely stitched together via batch file syncs or brittle APIs, creating severe operational friction across 12 core workflows.

---

## 2. Exhaustive Workflow Mapping & Operational Problem Discovery

Below is the detailed examination of all 12 core dealership workflows, detailing process mechanics, stakeholders, operational challenges, quantifiable business consequences, existing software support, and Tekion’s verified coverage.

---

### Workflow 1: Vehicle Acquisition and Inventory Management

#### Process Description
Vehicle acquisition feeds both used and new vehicle inventory. Vehicles are sourced via customer trade-ins during sales transactions, street purchases, off-lease returns, wholesale dealer auto auctions (Manheim, ACV, OPENLANE), and OEM factory new-vehicle allocations. Sourced vehicles must be appraised, titled, stocked into inventory, mechanically reconditioned, cosmetically detailed, photographed, priced against local market supply/demand, and syndicated across digital marketplaces.

#### Key Stakeholders
* **Internal:** Used Car Manager, General Sales Manager (GSM), Acquisition Specialist, Lot Attendant/Porter, Inventory Merchandiser, Service Advisor (Internal RO).
* **External:** Wholesale Auction Representatives, OEM Distribution Allocators, Transport Carriers.

#### Operational Challenges & Failure Modes
1. **Reconditioning Latency ("Days to Frontline" - DTF):** Sourced used vehicles sit in mechanical and cosmetic recon backlogs. Service departments routinely deprioritize internal recon repair orders (ROs) in favor of high-paying customer-pay work.
2. **Appraisal Inaccuracy & Valuation Risk:** Used car appraisers rely heavily on historical auction averages and visual inspections, frequently misjudging mechanical repair costs, hidden structural damage, or specialized equipment (such as EV battery health).
3. **Physical Lot Inventory Blindspots:** Lot attendants waste hours searching for vehicles across large multi-acre storage lots due to lost keys, outdated lot location records, and unrecorded vehicle moves.

#### Quantified Business Consequences
* **Floorplan Holding Costs:** According to NADA and NCM Associates benchmarks, while the recommended frontline target is 3 days, the national average Days to Frontline (DTF) spans **10 to 12.2 days**. Daily holding costs (floorplan interest, insurance, lot storage, and vehicle depreciation) average **$35 to $55 per vehicle per day**. For a mid-sized store processing 75 used units monthly, recon latency burns **$35,000 to $45,000 in lost gross profit every month**.
* **Missed Retail Turn Windows:** A vehicle that takes 12 days to reach the frontline enters the market at the tail end of its highest retail pricing window, forcing immediate price discounting.

#### Existing Software Support
* Inventory Management Systems (vAuto ProfitTime GPS, MAX Digital), Digital Auction Portals (Manheim Simulcast, ACV Auctions), Merchandising Tools (Impel, Dealer Specialties).

#### Tekion Coverage Status & Theme Alignment
* **Tekion Product:** ARC Inventory Management, Internal Service RO integration.
* **Documented Capability:** Full vehicle stocking, internal RO generation, rule-based pricing, and syndication feeds (**FULLY DOCUMENTED**). Hands-free mobile voice lot logging is **NOT ESTABLISHED**.
* **Official Hackathon Use Case Alignment:**
  * *Voice First Lot Walk Assistant (Theme 1):* Mobile voice tool for lot porters to update vehicle location and condition hands-free directly into the inventory system.
  * *Days to Sell Anomaly Explainer (Theme 2):* Analytical explainer identifying why a vehicle is aging beyond predicted days to sell based on merchandising completeness, photo quality, or market position rather than setting price.

---

### Workflow 2: Vehicle Sales and Digital Retail

#### Process Description
The lead-to-sale journey begins online or in the showroom. Digital shoppers configure vehicles, calculate financing/lease payments, value their trade-in, and submit credit pre-qualification applications via dealer websites. In-store, sales consultants verify vehicle availability, pull physical keys, conduct customer discovery, facilitate vehicle walkarounds and test drives, and transition to deal negotiation ("desking").

#### Key Stakeholders
* **Internal:** Sales Consultant, Desk Manager / Sales Manager, BDC Representative, General Sales Manager (GSM).
* **External:** Vehicle Shoppers / Car Buyers.

#### Operational Challenges & Failure Modes
1. **Online-to-In-Store Disconnect:** Digital retail shopping carts built by consumers online frequently fail to ingest cleanly into the in-store desking software. Showroom sales reps force customers to restart the interview and recalculate payments from scratch.
2. **The "Desking" Friction Loop:** Sales consultants gather customer payment expectations, walk physically to the elevated sales desk, wait for a desk manager to print a paper proposal ("the pencil" or "four-square"), and walk back to negotiate. This cycle repeats 2 to 4 times per transaction.
3. **Inventory Reservation Conflicts:** Lack of real-time inventory locking allows two sales consultants or an online buyer to place simultaneous reservations on the same vehicle.

#### Quantified Business Consequences
* **Customer Dwell Time Churn:** Per Cox Automotive's Car Buyer Journey study, buying a car takes **2.5 to 3.5 hours**, with **30% to 40% of that time spent completely idle** waiting for desking calculations and paperwork. Customer Net Promoter Scores (NPS) collapse by over 50% when transaction time exceeds 90 minutes.
* **Showroom Walkout Rate:** 10% to 15% of prospective buyers abandon in-store negotiations due to perceived negotiation opacity and extended wait times.

#### Existing Software Support
* Digital Retailing Widgets (Roadster, CarNow, Darwin Online), In-Store Desking Engines (CDK Desking, Reynolds ERA Desking), Automotive CRM platforms.

#### Tekion Coverage Status & Theme Alignment
* **Tekion Product:** ARC Digital Retail, ARC Desking, ARC CRM.
* **Documented Capability:** Unified online-to-in-store deal continuity, multi-option desking matrices on mobile tablets, real-time inventory locking (**FULLY DOCUMENTED**).
* **Official Hackathon Use Case Alignment:**
  * *Accessible Showroom Kiosk Experience (Theme 3):* Self-serve showroom kiosk experience supporting screen readers, multilingual real-time translation, and simplified navigation for inclusive browsing and test-drive booking.

---

### Workflow 3: Customer Relationship Management (CRM) & BDC

#### Process Description
The Business Development Center (BDC) and internet sales department manage inbound lead flow from third-party aggregators (TrueCar, Autotrader, Cars.com), OEM leads, social media, and dealer website chat forms. Leads must be ingested, checked for duplicate records, scored based on purchase intent, and routed to agents for immediate outreach via phone, SMS, or email to schedule in-store showroom appointments.

#### Key Stakeholders
* **Internal:** BDC Representative, BDC Director, Internet Sales Manager, Sales Consultant.
* **External:** Inbound Lead Prospects.

#### Operational Challenges & Failure Modes
1. **Speed-to-Lead Degradation:** Leads arriving after dealership operating hours sit uncontacted for 10 to 14 hours. Industry studies confirm that lead conversion rates plummet by 8x if initial contact is not established within 15 minutes.
2. **Data Duplication & Record Fragmentation:** Disconnected CRM and DMS databases create duplicate customer profiles, resulting in sold customers continuing to receive aggressive marketing calls to buy the vehicle they already purchased.
3. **High BDC Staff Turnover:** Automotive dealership consulting benchmarks indicate that BDC agent turnover frequently exceeds **100% annually** due to repetitive, high-stress cold dialing and tedious manual CRM task logging.

#### Quantified Business Consequences
* **Lead Conversion Loss:** Average automotive digital lead conversion hovers at a dismal **8% to 12%**. Improving speed-to-lead and 24/7 responsiveness can lift appointment show rates by 15% to 25%, directly driving vehicle unit sales.
* **Recruitment & Training Waste:** According to dealership HR operational models, constantly recruiting and training replacement BDC staff costs dealerships an estimated **$8,000 to $12,000 per seat annually**.

#### Existing Software Support
* Automotive CRMs (VinSolutions Connect, CDK Elead, DealerSocket, DriveCentric), Inbound Call Tracking (CallRevu, Marchex).

#### Tekion Coverage Status & Theme Alignment
* **Tekion Product:** ARC CRM, Salesperson AI.
* **Documented Capability:** Single customer "One View" profile, automated lead routing, generative email/SMS summaries (**FULLY DOCUMENTED**). 24/7 autonomous Salesperson AI lead agent announced June 2026 (**ANNOUNCED**).
* **Official Hackathon Use Case Alignment:**
  * *AI Co-Pilot for First Time Buyers (Theme 3):* Conversational guide explaining financing and leasing terms in plain language, personalized to credit profile and stated goals.

---

### Workflow 4: Financing and Insurance (F&I)

#### Process Description
Once vehicle pricing is agreed upon, the deal moves to the F&I office. The F&I Manager pulls customer credit reports, runs identity verification (OFAC / Red Flags Rule), structures loan/lease financing across captive and indirect auto lenders via RouteOne or Dealertrack, presents a menu of aftermarket protection products (extended warranties, GAP, tire/wheel), finalizes documentation, and submits the deal package for funding.

#### Key Stakeholders
* **Internal:** F&I Manager, Finance Director, Sales Manager, Dealership Compliance Officer.
* **External:** Commercial Lenders / Banks, Aftermarket Product Providers, Credit Bureaus.

#### Operational Challenges & Failure Modes
1. **The "F&I Waiting Room" Bottleneck:** Dealerships operate with fewer F&I managers than sales consultants. When 3 or 4 deals close simultaneously on a peak weekend afternoon, customers sit idle for 60 to 120 minutes waiting for an open F&I office.
2. **Contracting Errors & Lender Funding Delays (CIT):** Incomplete deal jackets, missing signatures, unmatched proof of income (stipulations), and incorrect sales tax fee calculations trigger lender kickbacks, stalling funding.
3. **Regulatory Compliance Scrutiny:** F&I product pricing and finance rate markups face intense scrutiny from the Federal Trade Commission (FTC CARS Rule, Safeguards Rule) and Consumer Financial Protection Bureau (CFPB Fair Lending).

#### Quantified Business Consequences
* **Contracts-in-Transit (CIT) Capital Lockup:** Deal funding latency averages **4 to 8 business days**. Dealerships routinely carry $2M to $5M in unfunded vehicle contracts, consuming working capital and generating thousands of dollars in unnecessary floorplan credit interest.
* **F&I Product Churn:** Exhausted customers entering the F&I office after a long wait reject high-margin aftermarket products (which generate $1,200 to $2,000 in gross profit per vehicle).

#### Existing Software Support
* Finance Clearinghouses (RouteOne, Dealertrack), Menu Selling Software (Reynolds docuPAD, Darwin Automotive, MaximTrak).

#### Tekion Coverage Status & Theme Alignment
* **Tekion Product:** ARC F&I, Deal Guard AI (F&I AI suite).
* **Documented Capability:** Dynamic digital menu presentation, bi-directional RouteOne/Dealertrack sync, native e-contracting (**FULLY DOCUMENTED**). Autonomous Deal Guard AI compliance pre-audit announced June 2026 (**ANNOUNCED**).
* **Official Hackathon Use Case Alignment:**
  * *Smart Document Extraction Agent (Theme 1):* Tool reading scanned title, registration, and insurance documents, validating fields against state DMV rules, and flagging mismatches before deal finalization.
    > [!NOTE]
    > **FUNCTIONAL DIFFERENTIATION ASSESSMENT (DEAL GUARD AI):**
    > Deal Guard AI performs baseline F&I checklist validation, driver's license ID extraction, and insurance presence checks. However, deep semantic OCR on complex titles and registrations, field-level validation against 50 state statutory DMV titling rules, and cross-document discrepancy detection across titles and contracts represent distinct capabilities not documented in Deal Guard AI. Concepts in this use case must focus on these advanced document extraction and statutory DMV validation frontiers.
  * *F&I Compliance & Fairness Auditor (Theme 2):* Analytics tool reviewing F&I product attach patterns and rate markups across customer segments to flag compliance or disparate impact risks.
  * *Paperless Deal Jacket Impact Tracker (Theme 4):* Quantifies paper, ink, and tree savings from e-contracting adoption with dealership leaderboards to drive 100% digital adoption.

---

### Workflow 5: Vehicle Delivery and Handover

#### Process Description
The final phase of vehicle sales. The sold vehicle is dispatched to the detail shop for clean-up and a full tank of gas or full electric charge. Delivery specialists pair the customer’s smartphone, configure infotainment and active safety features (ADAS), register OEM connected-car telematics apps (e.g., OnStar, FordPass), review warranty parameters, collect remaining down payment funds, and issue temporary state registration tags.

#### Key Stakeholders
* **Internal:** Sales Consultant, Delivery Specialist / Product Genius, Detailer, Lot Porter, Billing Clerk.
* **External:** Car Buyer, State DMV Portals.

#### Operational Challenges & Failure Modes
1. **Detail Bay Congestion:** Peak Saturday sales create massive backups in the detail wash bays, leaving customers waiting with finalized paperwork.
2. **Rushed Technology Onboarding:** Complex modern vehicle technologies (especially EV charging settings, one-pedal driving, and infotainment profiles) are often rushed or omitted, triggering low initial Customer Satisfaction Index (CSI) scores.
3. **Uncharged EV Deliveries:** Dealerships deliver used or new EVs with low battery charge (<30%) because charging stations were occupied or unmanaged on the lot.

#### Quantified Business Consequences
* **OEM CSI Penalties:** Vehicle manufacturers tie tens of thousands of dollars in quarterly dealer incentive bonuses directly to CSI delivery scores. A single sub-par survey can forfeit dealer allocation perks.

#### Existing Software Support
* State Electronic Vehicle Registration (EVR) portals, OEM connected-car mobile platforms, DMS delivery tracking modules.

#### Tekion Coverage Status & Theme Alignment
* **Tekion Product:** ARC Delivery checklists, Digital Deal Jacket, Tekion Pay.
* **Documented Capability:** Real-time sold unit status update, digital payment clearing, and electronic deal jacket archival (**FULLY DOCUMENTED**).

---

### Workflow 6: Service Appointments and Check-In

#### Process Description
Customers schedule vehicle maintenance or repair via the dealer website, OEM mobile app, or telephone BDC. On the service date, the vehicle arrives on the service drive. The service advisor conducts an intake interview, inspects vehicle condition, scans diagnostic trouble codes (DTCs), notes customer complaints, captures pre-existing cosmetic damage, reviews factory maintenance schedules, and generates the preliminary Repair Order (RO).

#### Key Stakeholders
* **Internal:** Customer, Service Advisor (Writer), Service BDC Agent, Drive Valet/Porter.
* **External:** Vehicle Owners.

#### Operational Challenges & Failure Modes
1. **Morning Drive Congestion (The "7:30 AM Rush"):** 60% to 70% of daily service appointments arrive between 7:30 AM and 8:45 AM. Advisors typing on legacy desktop terminals cause physical vehicle queues spilling out onto public streets.
2. **Overbooking & Capacity Mismatches:** Disconnected online booking engines schedule specialized repair jobs (e.g., diesel engine overhaul, EV high-voltage diagnostics) on days when certified master technicians are unavailable or bays are full.
3. **Missed Walkaround Maintenance Discovery:** Hurried advisors skip physical walkarounds, failing to spot worn tires, damaged wiper blades, or cracked glass.

#### Quantified Business Consequences
* **Lost Service Drive Upsell:** Dealership fixed-operations consulting benchmarks indicate that thorough walkaround vehicle inspections generate an estimated **$120 to $180 in additional discovered maintenance** per repair order. Rushed check-ins forfeit this high-margin revenue.
* **Customer Wait-Time Frustration:** Long check-in lines degrade initial service customer satisfaction before the vehicle even enters the workshop bay.

#### Existing Software Support
* Service Schedulers (Cox Xtime Schedule, Dealer-FX, Tekion Service Scheduler), Automated Tire/Alignment Scanners (Hunter Quick Check, UVeye).

#### Tekion Coverage Status & Theme Alignment
* **Tekion Product:** ARC Service (Digital Service Experience / DSE).
* **Documented Capability:** Mobile iPad check-in, 360-degree walkaround photo documentation, RFID lane vehicle identification, and automated service reminders (**FULLY DOCUMENTED**). Scheduler AI announced (**ANNOUNCED**).
* **Official Hackathon Use Case Alignment:**
  * *Autonomous Appointment & Dispatch Orchestrator (Theme 1):* Multi-agent system that re-optimizes technician assignments and bay allocation in real time as parts delays, no-shows, or walk-ins occur.

---

### Workflow 7: Repair Orders and Workshop Operations

#### Process Description
Once checked in, the vehicle is moved to the shop floor. The assigned technician clocks onto the Repair Order line, performs a comprehensive Multi-Point Inspection (MPI), diagnoses customer concerns, identifies required parts, records high-definition video/photo evidence of worn components, and builds an electronic estimate. The advisor presents the estimate to the customer for digital approval, and approved repairs are executed.

#### Key Stakeholders
* **Internal:** Service Technician, Service Advisor, Shop Foreman, Parts Counterperson.
* **External:** Customer.

#### Operational Challenges & Failure Modes
1. **The Estimate Approval Bottleneck ("Phone Tag"):** Technicians complete inspections and need customer authorization for $800 in brake repairs. Advisors spend hours calling customers who do not answer their phones. The vehicle sits dismounted on a lift, blocking the technician’s productivity.
2. **Technician-to-Parts Counter Delay:** Technicians leave their bay and walk physically across the shop floor to the parts back counter to check parts availability and pricing, wasting 10 to 15 minutes per repair order.
3. **Consumer Mistrust:** Customers historically distrust verbal repair recommendations made over the phone, suspecting dealership price gouging.

#### Quantified Business Consequences
* **Lift Utilization Decay:** Technicians operate on a "flat-rate" pay system (earning hours based on completed jobs). A vehicle idling on a lift for 2 hours waiting for estimate authorization costs the technician 2 flag hours ($50–$80 in personal wages) and costs the dealership **$250 to $350 in unbilled labor gross profit**.
* **MPI Conversion Rate:** Phone-based verbal recommendations achieve a modest **35% to 42% customer approval rate**. In contrast, video-backed digital MPI estimates texted to mobile phones achieve **58% to 68% conversion rates**.

#### Existing Software Support
* Electronic MPI & Video Platforms (TruVideo, myKaarma, Xtime Inspect), Tekion DSE.

#### Tekion Coverage Status & Theme Alignment
* **Tekion Product:** ARC Service (DSE), Tekion AI Copilot for Service.
* **Documented Capability:** Integrated mobile MPI video capture, customer text-to-approve interface, automated plain-language translation of technician shorthand notes (**FULLY DOCUMENTED**).
* **Official Hackathon Use Case Alignment:**
  * *Proactive Service Status Companion (Theme 3):* Real-time, transparent repair status updates sent by text or app, including technician photos and videos, cutting down inbound status calls.
  * *Service Parts Shortage Resolver Agent (Theme 1):* Detects an RO stalled on a missing part, checks sister store and vendor stock, and proposes a resequenced schedule so the bay is not idle.

---

### Workflow 8: Technician and Service-Bay Management

#### Process Description
The management of workshop throughput, technician labor allocations, and specialized bay equipment (heavy-duty lifts, wheel alignment racks, EV high-voltage safety stalls). Work is dispatched according to technician skill certifications: Master Technicians (engine/transmission rebuilds, high-voltage EV isolation), B-Technicians (brakes, suspension), and C-Technicians / Lube Techs (express oil, filter, tire rotations).

#### Key Stakeholders
* **Internal:** Shop Foreman, Service Dispatcher, Master Technicians, Flat-Rate Line Technicians, Lube Technicians, Service Director.

#### Operational Challenges & Failure Modes
1. **Manual Dispatcher Inefficiency & Favoritism:** In manual dispatch shops, foremen distribute physical paper RO folders. Human bias frequently results in preferred technicians receiving high-paying warranty "gravy" jobs while other skilled technicians get bogged down in low-paying diagnostic work.
2. **Severe Automotive Technician Shortages:** According to the TechForce Foundation Supply & Demand Report, replacement positions created by occupational separations (retirements, career changes, and turnover) outpace positions created by net industry job growth by **more than 4 to 1**, creating an acute structural labor deficit across dealership service bays. Retaining certified technicians requires maximizing their billed flat-rate hours.
3. **Specialized Equipment Contention:** Dealerships possess limited specialized bays (e.g., only 1 or 2 dedicated EV battery drop tables or heavy alignment racks). Uncoordinated dispatching creates bay gridlock.

#### Quantified Business Consequences
* **Labor Efficiency Drain:** Sub-optimal shop dispatching depresses overall technician labor efficiency to **70% to 75%** of available clocked hours. According to dealership financial operational models, optimizing bay dispatching to reach **100% to 110% efficiency** increases a modeled 20-bay shop's annual labor gross profit by an estimated **$180,000 to $250,000**.

#### Existing Software Support
* Electronic Shop Loading (ESL) tools, CDK Electronic Dispatch, Reynolds Service Dispatch.

#### Tekion Coverage Status & Theme Alignment
* **Tekion Product:** ARC Service Dispatching, Scheduler AI.
* **Documented Capability:** Technician skill-level tagging, automated rule-based job routing, flag-hour tracking (**FULLY DOCUMENTED**). Dynamic real-time autonomous multi-agent bay re-optimization is **NOT ESTABLISHED**.
* **Official Hackathon Use Case Alignment:**
  * *Autonomous Appointment & Dispatch Orchestrator (Theme 1):* Multi-agent system that dynamically re-optimizes technician assignments and bay allocation in real time as parts delays, no-shows, or walk-ins occur.

---

### Workflow 9: Parts Inventory and Procurement

#### Process Description
The dealership parts department manages tens of thousands of unique OEM and aftermarket stock keeping units (SKUs). Parts counter personnel support three distinct channels: Back Counter (supplying internal service shop repair orders), Front Counter (retail consumer walk-ins), and Wholesale (selling collision and mechanical parts to independent body shops). Workflows include parts catalog lookups, checking physical bin locations, ordering from OEM regional parts distribution centers (PDCs), and processing core returns.

#### Key Stakeholders
* **Internal:** Parts Manager, Back-Counter Personnel, Wholesale Parts Counterperson, Shipping/Receiving Clerk, Delivery Drivers.
* **External:** OEM Parts Distribution Centers (PDC), Aftermarket Distributors (Worldpac, LKQ), Independent Collision Repair Facilities.

#### Operational Challenges & Failure Modes
1. **Parts Backorders Stalling Service Bays:** Global automotive supply chain disruptions and factory backorders leave vehicles disassembled on lifts for days waiting on specialized sensors, wiring harnesses, or suspension arms.
2. **Parts Obsolescence & Carrying Capital:** Dealerships accumulate obsolete, non-moving parts inventory (items unsold for >12 months) that ties up capital and eventually must be written off as scrap.
3. **Manual Cross-Referencing of Superseded Numbers:** OEM part numbers change constantly due to engineering updates. Counter personnel waste time manually verifying superseded part numbers across separate Electronic Parts Catalogs (EPCs).

#### Quantified Business Consequences
* **Inventory Carrying Waste:** The average franchised dealership carries **$350,000 to $600,000 in parts inventory**, with **15% to 22% classified as non-moving or obsolete capital**.
* **Fixed Operations Stalls:** 15% to 20% of service bay downtime is directly attributable to missing parts discovered midway through vehicle teardown.

#### Existing Software Support
* Electronic Parts Catalogs (Snap-on EPC, Microcat), Parts Locators (OEConnection D2DLink, PartsTrader), DMS Parts Modules.

#### Tekion Coverage Status & Theme Alignment
* **Tekion Product:** ARC Parts Management, Accounts Payable AI.
* **Documented Capability:** Direct linking of parts to active RO lines, automated replenishment triggers, AP AI invoice matching (**FULLY DOCUMENTED**). Autonomous cross-network sister store shortage resolution is **NOT ESTABLISHED**.
* **Official Hackathon Use Case Alignment:**
  * *Service Parts Shortage Resolver Agent (Theme 1):* Detects an RO stalled on a missing part, automatically checks sister store and vendor stock, and proposes an adjusted shop schedule.
  * *Circular Parts Marketplace (Theme 4):* Platform matching recyclable or reconditioned OEM parts across a dealer network to reduce waste and lower customer repair costs.

---

### Workflow 10: Customer Retention and Post-Sale Engagement

#### Process Description
Maintaining customer loyalty throughout the 3- to 7-year vehicle ownership lifecycle. Dealerships track service mileage intervals, OEM factory recall announcements, vehicle service contract expirations, and customer loan equity positions to trigger timely marketing touchpoints, service reminders, and lease-return or trade-upgrade opportunities.

#### Key Stakeholders
* **Internal:** Retention Manager, BDC Follow-up Representative, Marketing Director, Equity Mining Specialist, Service Director.
* **External:** Vehicle Owners / Customers.

#### Operational Challenges & Failure Modes
1. **Post-Warranty Customer Defection:** While dealerships retain **75% to 80%** of customer service visits during the initial factory warranty period (Years 1–3), defection rates surge to **over 60%** after year 3, as customers migrate to independent aftermarket repair shops (Jiffy Lube, Firestone, independent mechanics).
2. **Siloed Sales vs. Service Marketing:** Disconnected CRM and DMS databases send contradictory marketing messages—for example, sending a generic sales email inviting a customer to trade in their truck while the truck is currently sitting in the dealership shop undergoing an engine replacement.
3. **Equity Mining Fatigue:** Generic, unverified equity calculation mailers ("We want to buy your car for above market value!") destroy consumer trust when in-store appraisal numbers fail to honor the marketing pitch.

#### Quantified Business Consequences
* **Customer Lifetime Value (LTV) Destruction:** Retaining an existing service customer costs 5x less than acquiring a new vehicle buyer. Losing a service customer forfeits **$1,400 to $2,200 annually in customer-pay maintenance and tires**, plus the probability of their next vehicle purchase.

#### Existing Software Support
* Equity Mining Platforms (Automotive Mastermind, DealActivator, AutoAlert), Service Retention CRMs.

#### Tekion Coverage Status & Theme Alignment
* **Tekion Product:** ARC CRM, ARC Analytics.
* **Documented Capability:** Unified ownership profile, automated service reminders, vehicle equity tracking (**FULLY DOCUMENTED**). Predictive churn win-back models with dynamic personalized incentives are **NOT ESTABLISHED**.
* **Official Hackathon Use Case Alignment:**
  * *Churn & Win Back Predictor for Service Customers (Theme 2):* Model predicting which customers are at risk of skipping their next scheduled service, with triggered win-back offers at the optimal moment.
  * *Post Purchase Loyalty Journey Orchestrator (Theme 3):* Coordinates follow-up touchpoints across ownership lifecycle, service reminders, accessory upsells, and trade-in equity windows.

---

### Workflow 11: EV Servicing, Charging, and Trade-in Workflows

#### Process Description
The emergence of Battery Electric Vehicles (EVs) introduces new dealership workflows. Service departments require high-voltage safety isolation protocols (Class 0 1000V protective gear, dedicated high-voltage bays), specialized battery pack lift tables, and managed Level 2 and Level 3 DC fast-charging infrastructure. In the used car department, EV appraisals require evaluating high-voltage battery degradation (State of Health - SOH) to determine residual trade-in valuation.

#### Key Stakeholders
* **Internal:** EV Certified Master Technician, EV Specialist Service Advisor, Used Car Appraiser, Lot Attendant, Facilities/Charging Director.
* **External:** EV Owners, Commercial Electric Utilities, OEM High-Voltage Engineering Teams.

#### Operational Challenges & Failure Modes
1. **EV Battery Health Opacity during Trade-In:** Traditional vehicle valuation tools (KBB, Black Book, Manheim) rely on odometer mileage and cosmetic condition. However, an EV battery represents **30% to 40% of the vehicle’s total residual value**. A battery subjected to frequent DC fast-charging or aggressive thermal cycling may suffer 15% to 25% degradation that is invisible to traditional appraisal tools, exposing the dealership to thousands of dollars in resale losses.
2. **Dealership Lot Charging Logistical Gridlock:** Unsold EVs parked on inventory lots discharge over time. If high-voltage traction packs drop below critical charge thresholds or 12V auxiliary batteries die, vehicles become completely immobilized on the lot. Dealership Level 2 and Level 3 chargers are frequently unmanaged, blocked by finished cars, or suffer unscheduled downtime.
3. **High-Voltage Technician & Equipment Gaps:** Dealerships lack sufficient certified high-voltage technicians, resulting in EV service repair orders sitting unassigned for weeks.

#### Quantified Business Consequences
* **Trade Valuation Write-Downs:** Appraising an EV without verified battery health data creates severe valuation variance—dealerships either under-appraise by $3,000–$5,000 (losing the sale) or over-appraise and incur massive inventory losses upon resale.
* **Capital Infrastructure Drag:** Upgrading dealership transformer capacity and installing DC fast-chargers requires capital expenditures between **$150,000 and $750,000**, with dealerships lacking analytical software to optimize charger utilization or fleet energy costs.

#### Existing Software Support
* Third-Party Telematics Diagnostic Dongles (Recurrent Auto), Wholesale Auction EV Diagnostic Syndication (Cox Automotive Mobility / Spiers New Technologies ALFRED platform, syndicated into Manheim Condition Reports and MMR — though direct programmatic integration into Tekion ARC is unestablished), Charging Station Management Networks (ChargePoint, Blink), OEM proprietary vehicle flashing tools.

#### Tekion Coverage Status & Theme Alignment
* **Tekion Product:** ARC Service, ARC Inventory.
* **Documented Capability:** Standard vehicle repair order processing, multi-make VIN decode (**FULLY DOCUMENTED**). Standalone battery diagnostic telemetry ingestion, dealership carbon tracking, and charging route optimization are **NOT ESTABLISHED**.
* **Official Hackathon Use Case Alignment:**
  * *EV Readiness Advisor for Dealers (Theme 4):* Scores dealership readiness for EV sales and service (charging infrastructure, tech certifications, parts) and recommends an investment roadmap.
  * *EV Trade In Battery Health Estimator (Theme 4):* Estimates a trade-in EV’s battery health and remaining life from available diagnostic and service history data for fairer trade-in valuation and resale pricing.
  * *Green Delivery Route Optimizer (Theme 4):* Optimizes routing for loaner, shuttle, and delivery vehicles, favoring EVs where available to cut fleet emissions and fuel cost.

---

### Workflow 12: Dealer Reporting and Performance Management

#### Process Description
The financial administration and operational governance of the dealership. Daily deal jackets from sales and closed repair orders from service are cleared by billing clerks, posted to the general ledger (GL), and compiled into the Daily Operating Control (DOC) for executive management. Controllers reconcile floorplan loan interest statements, track factory warranty receivables, audit uncollected OEM incentive payouts, and submit the monthly standardized factory financial statement to the vehicle manufacturer by the 10th of each month.

#### Key Stakeholders
* **Internal:** Dealer Principal, General Manager (GM), Chief Financial Officer (CFO), Controller, Office Manager, Department Heads.
* **External:** OEM Financial Auditors, Commercial Floorplan Banks, Certified Public Accountants (CPA).

#### Operational Challenges & Failure Modes
1. **The Month-End Accounting Crunch (5 to 10-Day Lag):** In legacy batch-posting DMS architectures, sales and service transactions require manual end-of-day posting and journal balancing. Controllers spend days reconciling Work in Progress (WIP) labor, unmatched parts packing slips, and open deal jackets.
2. **Uncollected Factory Incentive Rebates:** Automakers distribute complex stair-step sales incentives and warranty claim allowances with strict submission deadlines. Disconnected sales and accounting systems lead to missed claims, leaving tens of thousands of dollars in OEM rebates uncollected.
3. **Cross-Store Multi-Rooftop Blindspots:** Dealer group executives managing 5 to 20 rooftops struggle to benchmark store-level operational metrics (lead response times, closing ratios, service technician efficiency) due to disparate data definitions and delayed consolidated reporting.

#### Quantified Business Consequences
* **Operational Blindness:** When financial statements take 10 days to close, GMs manage the dealership using outdated numbers, missing critical inventory liquidation windows or failing to catch ballooning department expenses.
* **Lost OEM Receivables:** Dealership accounting benchmarks estimate that stores forfeit **$15,000 to $40,000 annually** in rejected or unappealed warranty claims and missed factory volume bonuses due to clerical reconciliation lag.

#### Existing Software Support
* Core DMS Accounting Modules (CDK Drive Accounting, Reynolds ERA Financials), Business Intelligence Tools (Tableau, Microsoft PowerBI, NADA 20 Group reporting).

#### Tekion Coverage Status & Theme Alignment
* **Tekion Product:** ARC Accounting, Automotive Enterprise Cloud (AEC), Tekion Analytics.
* **Documented Capability:** Real-time continuous general ledger posting, multi-rooftop consolidated financial statements, automated trial balance generation (**FULLY DOCUMENTED**). Operational facility carbon footprint tracking is **NOT ESTABLISHED**.
* **Official Hackathon Use Case Alignment:**
  * *Cross Store Benchmarking Dashboard (Theme 2):* For multi-location dealer groups, surfaces which store-level metrics (lead response time, close rate, CSI) are outliers, and explains *why*.
  * *Carbon Footprint Tracker for Dealer Operations (Theme 4):* Tracks and visualizes emissions from dealership operations, facilities, loaner fleets, and logistics with reduction recommendations.

---

## 3. Master Mapping Matrix: 18 Official Hackathon Use Cases to Dealership Workflows

This master matrix connects every official hackathon use case from `references/tekion-themes.pdf` to its core dealership workflow, primary stakeholders, operational problem, and Tekion capability status:

| # | Official Theme | Official Use Case Title (Verbatim from PDF) | Core Dealership Workflow | Target Stakeholders | Primary Operational Problem Addressed | Tekion Coverage Status |
| :-: | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Theme 1: AI & Automation** | Autonomous Appointment & Dispatch Orchestrator | W6 (Appts) & W8 (Bay Mgmt) | Service Advisors, Foremen, Technicians | Static capacity booking causes bay idle time when parts delays or walk-ins occur. | **PARTIALLY DOCUMENTED** |
| **2** | **Theme 1: AI & Automation** | Smart Document Extraction Agent | W4 (Financing & Insurance) | F&I Managers, Title Clerks, Lenders | Stalled deal funding (CIT) due to document mismatches and state DMV rule errors. | **ANNOUNCED** (Deal Guard AI) |
| **3** | **Theme 1: AI & Automation** | Voice First Lot Walk Assistant | W1 (Acquisition & Inventory) | Lot Porters, Used Car Managers | Porters waste hours searching multi-acre lots; manual clipboards delay inventory stocking. | **NOT ESTABLISHED** |
| **4** | **Theme 1: AI & Automation** | Service Parts Shortage Resolver Agent | W7 (RO Ops) & W9 (Parts) | Technicians, Parts Counter, Foremen | Disassembled vehicles block service bays when replacement parts are out of stock. | **NOT ESTABLISHED** |
| **5** | **Theme 2: Data Analytics** | Churn & Win Back Predictor for Service Customers | W10 (Customer Retention) | Service Advisors, BDC, Marketing | Dealerships lose >60% of service customers post-warranty to independent repair shops. | **NOT ESTABLISHED** |
| **6** | **Theme 2: Data Analytics** | Cross Store Benchmarking Dashboard | W12 (Dealer Reporting) | Dealer Principals, GMs, CFOs | Multi-store dealer groups lack diagnostic visibility into *why* store KPIs lag. | **PARTIALLY DOCUMENTED** |
| **7** | **Theme 2: Data Analytics** | Days to Sell Anomaly Explainer | W1 (Acquisition & Inventory) | Used Car Managers, GSMs | Used cars age on lots; stores slash prices rather than fixing non-price listing gaps. | **PARTIALLY DOCUMENTED** |
| **8** | **Theme 2: Data Analytics** | F&I Compliance & Fairness Auditor | W4 (Financing & Insurance) | F&I Directors, Compliance Officers | F&I product pricing and markup disparities create severe regulatory and legal risks. | **NOT ESTABLISHED** |
| **9** | **Theme 3: Customer Experience** | AI Co-Pilot for First Time Buyers | W2 (Sales) & W4 (F&I) | Car Buyers, Sales Reps, F&I | First-time buyers overwhelmed by complex finance terms, leasing APRs, and disclosures. | **NOT ESTABLISHED** |
| **10** | **Theme 3: Customer Experience** | Proactive Service Status Companion | W6 (Appts) & W7 (RO Ops) | Service Customers, Advisors | Inbound "phone tag" calls asking for repair updates distract advisors from selling work. | **PARTIALLY DOCUMENTED** |
| **11** | **Theme 3: Customer Experience** | Accessible Showroom Kiosk Experience | W2 (Vehicle Sales & Retail) | Showroom Visitors, Sales Consultants | In-store browsing touchscreens lack accessibility, screen readers, or multilingual support. | **NOT ESTABLISHED** |
| **12** | **Theme 3: Customer Experience** | Post Purchase Loyalty Journey Orchestrator | W5 (Delivery) & W10 (Retention) | Vehicle Buyers, BDC, Service | Post-sale customer communication is generic, disjointed, and misses equity upgrade windows. | **PARTIALLY DOCUMENTED** |
| **13** | **Theme 4: Sustainability** | EV Readiness Advisor for Dealers | W11 (EV Servicing & Trade-In) | Dealer Principals, Facilities Mgrs | Dealerships lack capital investment roadmaps for chargers, tech training, and tooling. | **NOT ESTABLISHED** |
| **14** | **Theme 4: Sustainability** | Carbon Footprint Tracker for Dealer Operations | W12 (Dealer Reporting & Ops) | Dealer Principals, Controllers, OEMs | Zero native software tools to track operational greenhouse gas emissions across rooftops. | **NOT ESTABLISHED** |
| **15** | **Theme 4: Sustainability** | Circular Parts Marketplace | W9 (Parts Inventory) | Parts Managers, Collision Shops | Usable, certified reconditioned and core parts are scrapped instead of reused across stores. | **NOT ESTABLISHED** |
| **16** | **Theme 4: Sustainability** | Paperless Deal Jacket Impact Tracker | W4 (F&I) & W12 (Reporting) | F&I Managers, Title Clerks, GMs | Dealerships fail to quantify paper/toner savings or gamify internal e-contracting adoption. | **NOT ESTABLISHED** |
| **17** | **Theme 4: Sustainability** | EV Trade In Battery Health Estimator | W1 (Acquisition) & W11 (EV Ops) | Used Car Appraisers, EV Techs | Opacity of used EV battery degradation causes $3,000–$5,000 trade-in valuation errors. | **NOT ESTABLISHED** |
| **18** | **Theme 4: Sustainability** | Green Delivery Route Optimizer | W5 (Delivery) & W11 (EV Ops) | Parts Drivers, Shuttle Drivers | Dealership shuttles and parts vans use basic routing without carbon minimization or EV priority. | **NOT ESTABLISHED** |

---

## 4. Key Takeaways for Hackathon Research Phases

1. **Fixed Operations is the Margin Powerhouse:** While vehicle sales capture consumer headlines, Fixed Operations generates over half of dealership gross profit at 70%+ gross labor margins. Problem concepts that reclaim lost technician hours (e.g., Use Case 1 and Use Case 4) deliver disproportionately higher financial return on investment (ROI) than basic showroom chat widgets.
2. **Theme 4 Represents Significant Potential Opportunity:** While Themes 1, 2, and 3 intersect with existing commercial products (e.g., Tekion ARC CRM, DSE, Deal Guard AI), **Theme 4 (Sustainability)** represents unaddressed territory in mainstream native DMS platforms. Neither Tekion, CDK, Reynolds, nor Salesforce offers native in-store DMS tools for used EV battery degradation valuation, operational carbon footprint tracking, or circular parts re-distribution. (Note: In the adjacent mobility space, Cox Automotive operates Spiers New Technologies / ALFRED at centralized hubs, but this is not an integrated in-store DMS appraisal tool).
3. **Strict Adherence to Use Case Boundaries:** In subsequent research phases, proposed solutions must strictly observe the operational constraints established in `references/tekion-themes.pdf`. For example, *Days to Sell Anomaly Explainer* must remain an analytical explainer diagnosing listing completeness and merchandising rather than an automated pricing tool; and *Smart Document Extraction Agent* must focus on state-specific DMV titling validation rather than generic file upload checks.

---
*End of Dealership Operational Workflows & Problem Mapping.*
