# Phase 4 Legal and Statutory Rule Catalogue: CA-NV-AZ Corridor

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `research/phase4-legal-rule-scope.md`  
**Stage:** Phase 4 – Final Concept Selection & Scope Freeze  
**Standard:** Compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, `references/tekion-themes.pdf`, and Phase 3.2 Authoritative Corrections  
**Author:** Chief Product Strategist & Automotive Legal Systems Architect  
**Purpose:** Comprehensive, transaction-specific statutory rule specification for the California – Nevada – Arizona (CA-NV-AZ) interstate corridor, providing full legal provenance, statutory citations, applicability logic, exceptions, and human-review thresholds.

---

## 1. Governance Principles & Methodological Boundaries

1. **Administrative Pre-Audit Assistant Only:** CrossBorder TitleGuard is an administrative workflow tool designed to catch documentation defects prior to state submission. **It is NOT a legal authority, does not provide legal advice, and does not certify legal compliance or indemnify against DMV rejections.**
2. **Jurisdiction-Specific Execution Logic:** Transfer rules are non-fungible across state lines. The system enforces a strict four-way separation of legal concerns:
   * *Origin-State Title Execution Rules:* Requirements of the jurisdiction that issued the title certificate.
   * *Receiving-State Dealer Transaction Rules:* Requirements of the state where the vehicle is being registered or sold.
   * *Supporting Instrument Rules:* Statutory requirements governing Powers of Attorney and Bills of Sale.
   * *Federal Mandates:* Uniform federal odometer disclosure regulations under 49 CFR Part 580.
3. **No Blanket Notarization Rules:** Notarization requirements are strictly transaction-specific. Inked rubber stamps are audited visually; colorless raised dry embossments require manual title clerk tactile verification.
4. **Deterministic Versioning:** All rules are defined in declarative Abstract Syntax Trees (AST) with versioned metadata, effective dates, and review timestamps. Any rule with ambiguity is assigned an `UNKNOWN` status and routed to mandatory human review.

---

## 2. Federal Odometer Disclosure Rules (Uniform Nationwide Application)

### Rule FED-ODO-01: 20-Year Rolling Odometer Exemption Threshold
* **Governing Statute / Regulation:** **49 CFR Part 580 (Odometer Disclosure Requirements), § 580.17(a)(1)**; NHTSA Final Rule (84 FR 52676, amended 85 FR 69265; `SRC-P3-13`).
* **Source URL:** https://www.nhtsa.gov/laws-regulations/odometer-fraud
* **Effective Date:** January 1, 2021 (In effect through 2026).
* **Last Reviewed Date:** November 2026.
* **Transaction & Document Type:** Applicable to ALL motor vehicle ownership transfers involving a Certificate of Title, Secure Power of Attorney, or State Odometer Disclosure Form.
* **Statutory Logic & Condition:** 
  $$\text{Exemption Status} = \begin{cases} \text{EXEMPT} & \text{if } \text{Model Year} \le 2010 \\ \text{REQUIRED} & \text{if } \text{Model Year} \ge 2011 \text{ and } (\text{Transaction Year} - \text{Model Year}) < 20 \\ \text{EXEMPT} & \text{if } (\text{Transaction Year} - \text{Model Year}) \ge 20 \end{cases}$$
  *Under this federal rule, model year 2010 and older vehicles remain permanently exempt under the legacy 10-year rule. Model year 2011 and newer vehicles are subject to the 20-year rolling window (e.g., a 2011 model vehicle remains subject to mandatory odometer disclosure until 2031).*
* **Failure Mode Detected:** Seller checks "Exempt" box on a 2014 model year trade-in vehicle.
* **Exceptions:** Vehicles with Gross Vehicle Weight Rating (GVWR) $> 16,000\text{ lbs}$; vehicles not equipped with odometers at manufacture; vehicles model year 2010 or older.
* **Confidence Level:** **HIGH (100% Deterministic Rule).**
* **Mandatory Human Review:** No, unless OCR extraction confidence on numerical mileage is $< 85\%$.

### Rule FED-ODO-02: Odometer Brand & Sequence Discrepancy Signal
* **Governing Statute / Regulation:** **49 CFR § 580.5(e)**.
* **Source URL:** https://www.nhtsa.gov/laws-regulations/odometer-fraud
* **Effective Date:** Active federal regulation.
* **Last Reviewed Date:** November 2026.
* **Required Condition:** Mileage reading on assignment line should be greater than or equal to the mileage printed on the face of the prior title. If disclosed mileage is lower, the system flags an **Odometer Sequence Anomaly**.
* **Important Operational Distinction:** A negative mileage delta is treated as an **Anomaly Signal**, NOT an automatic legal defect. Possible legitimate causes include clerical transposition errors (e.g., 64,200 vs 64,020) or mechanical replacement of an odometer cluster supported by a sworn state affidavit of repair. If uncertified, the seller must explicitly certify the brand as `WARNING_ODOMETER_DISCREPANCY` or `EXCEEDS_MECHANICAL_LIMITS`.
* **Failure Mode Detected:** Previous title face shows 64,210 miles; seller writes 46,210 miles without discrepancy brand.
* **Exceptions:** Replacement odometer certified with state affidavit attached.
* **Confidence Level:** **HIGH (Deterministic Anomaly Signal).**
* **Mandatory Human Review:** **MANDATORY.** Any negative delta routes to human title clerk investigation.

---

## 3. Arizona Statutory Transfer Rules (Origin & Transaction Specifics)

### Rule AZ-TITLE-01: Individual Seller Assignment on Physical Arizona Title
* **Governing Statute:** **Arizona Revised Statutes (A.R.S.) § 28-2058(A)** (Transfer of Title).
* **Administrative Reference:** Arizona Department of Transportation (ADOT) MVD Title and Registration Guidelines § 2.1.
* **Source URL:** https://www.azleg.gov/ars/28/02058.htm
* **Effective Date:** In effect for 2026 transactions.
* **Last Reviewed Date:** November 2026.
* **Transaction Type:** Private individual transferring an Arizona Certificate of Title.
* **Required Condition:** Seller must sign the assignment section on the title certificate. If the title is an older Arizona certificate format with a pre-printed notary acknowledgment block, the signature must be notarized or witnessed by an authorized MVD/ATP agent. If modern Arizona certificate format, signature assignment is valid without separate notary jurat when processed directly through MVD/ATP systems with identity verification.
* **Failure Mode Detected:** Seller signature block left blank or signed by unauthorized third party.
* **Exceptions:** Electronic transfers executed via AZ MVD Now portal.
* **Confidence Level:** **HIGH.**
* **Mandatory Human Review:** Yes, if older certificate format is detected.

### Rule AZ-BOS-02: ADOT Bill of Sale Notarization / Witnessing Mandate
* **Governing Statute:** **A.R.S. § 28-2058**; **A.R.S. § 28-370** (Oaths, Acknowledgments & Witnessing); ADOT Form 48-2004 / 38-1306.
* **Administrative Reference:** ADOT MVD Dealer Licensing & Title Manual, "Bill of Sale Requirements".
* **Source URL:** https://azdot.gov/mvd/services/vehicle-services/vehicle-title-and-registration
* **Effective Date:** Active policy current through 2026.
* **Last Reviewed Date:** November 2026.
* **Transaction & Document Type:** Transfer of ownership executed using an official **Arizona Bill of Sale (Form 48-2004 / 38-1306)**.
* **Required Condition:** Under official ADOT guidelines, when a Bill of Sale is utilized to transfer ownership or establish purchase price, the **seller's signature must be acknowledged before a Notary Public OR witnessed by an authorized ADOT MVD / Authorized Third Party (ATP) agent**.
* **Failure Mode Detected:** Trade-in jacket contains an un-notarized Arizona Bill of Sale signed by the private seller without an authorized MVD witness stamp.
* **Exceptions:** Transfers processed directly between licensed Arizona dealers via electronic dealer exchange.
* **Confidence Level:** **HIGH (Verified ADOT Policy).**
* **Mandatory Human Review:** Yes, if seal impression is illegible or dry-embossed.

### Rule AZ-POA-03: Vehicle Power of Attorney Notarization & Witness Exception
* **Governing Statute:** **A.R.S. § 28-370**; ADOT Form 48-1001 (Power of Attorney) & Form 48-7104 (Secure POA with Odometer Disclosure).
* **Administrative Reference:** ADOT MVD Title Manual, "Power of Attorney Execution".
* **Source URL:** https://www.azleg.gov/ars/28/00370.htm
* **Effective Date:** Active statute.
* **Last Reviewed Date:** November 2026.
* **Transaction & Document Type:** Vehicle ownership transfer or title replacement executed via Power of Attorney.
* **Required Condition:** The appointing owner's signature **must be notarized** IF executed remotely or by a non-agent third party. **Pursuant to A.R.S. § 28-370, notarization is EXEMPT if the signature is directly witnessed by an authorized ADOT MVD employee or an Authorized Third Party (ATP) agent.**
* **Failure Mode Detected:** POA Form 48-1001 executed remotely without a notary jurat or authorized agent witness signature.
* **Exceptions:** In-person witnessing at MVD/ATP counter pursuant to A.R.S. § 28-370.
* **Confidence Level:** **HIGH.**
* **Mandatory Human Review:** Yes, to verify whether witness signature belongs to a certified MVD/ATP representative.

### Rule AZ-DEALER-04: Licensed Motor Vehicle Dealer Reassignment Exemption
* **Governing Statute:** **A.R.S. § 28-4409** (Consignment Sales & Dealer Reassignments); A.R.S. § 28-2058.
* **Administrative Reference:** ADOT Dealer Licensing Guidelines.
* **Source URL:** https://www.azleg.gov/ars/28/04409.htm
* **Effective Date:** Active statute.
* **Last Reviewed Date:** November 2026.
* **Transaction & Document Type:** Licensed motor vehicle dealer reassigning a trade-in to another licensed dealer or retail buyer.
* **Required Condition:** Licensed Arizona dealers executing reassignment spaces on an Arizona title or secure reassignment document do **NOT** require a notary public jurat, provided the dealer license number and authorized representative signature are recorded.
* **Failure Mode Detected:** System flagging a licensed dealer reassignment endorsement as "defective" for lacking a notary stamp.
* **Exceptions:** None (Dealer exemption is established).
* **Confidence Level:** **HIGH.**
* **Mandatory Human Review:** No.

### Rule AZ-TIME-05: 15-Day Application Window & Statutory Late Penalty
* **Governing Statute:** **A.R.S. § 28-2051(A), (C)** (Application for Certificate of Title; Penalty).
* **Administrative Reference:** ADOT MVD Title Manual § 2.1.
* **Source URL:** https://www.azleg.gov/ars/28/02051.htm
* **Effective Date:** Active statute current through 2026.
* **Last Reviewed Date:** November 2026.
* **Transaction & Document Type:** Application for title transfer following purchase or acquisition.
* **Required Condition:** Transferee must apply for title within 15 days of vehicle acquisition.
* **Important Legal Distinction:** Exceeding 15 days does NOT void the title transfer or make the assignment legally invalid. Instead, pursuant to A.R.S. § 28-2051(C), an administrative penalty fee is assessed ($8.00 if filed between days 16 and 30; $100.00 if filed after 30 days).
* **System Action:** Flags deal with an **Amber Fee Advisory** ("Statutory 15-Day Window Exceeded — Late Transfer Fee Applicable"), prompting accounting adjustment rather than a deal rejection.
* **Confidence Level:** **HIGH (Deterministic Date Arithmetic).**
* **Mandatory Human Review:** No (Calculated from signature date to intake date).

---

## 4. California Statutory Transfer Rules (Origin & Receiving State)

### Rule CA-SMOG-01: Smog Certification Mandate on California Retail Resale & Registration
* **Governing Statute:** **California Vehicle Code (CVC) § 24007(b)(2)** (Dealer Responsibility upon Retail Sale); **CVC § 4000.1(a)** & **CVC § 4000.2** (Out-of-State Registration).
* **Administrative Reference:** California DMV Dealer Handbook Chapter 24 (Out-of-State Vehicles) & Chapter 8.
* **Source URL:** https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=VEH&sectionNum=4000.1
* **Effective Date:** Active statute current through 2026.
* **Last Reviewed Date:** November 2026.
* **Transaction & Document Type:** Out-of-state trade-in vehicle being prepared for retail sale and registration to a California consumer.
* **Important Legal Distinction (Trade Intake vs Retail Sale):** 
  * *Trade-In Intake:* A California dealer is legally authorized to take an out-of-state vehicle in trade without an existing smog certificate. The absence of smog does NOT invalidate the trade-in title acquisition.
  * *Retail Resale Mandate:* Under CVC § 24007(b)(2), prior to delivering the vehicle to a retail consumer, the dealer MUST obtain a valid California Smog Inspection Certificate issued within 90 days.
  * *Wholesale Exemption:* Under CVC § 24007(a)(1), sales from dealer-to-dealer, wholesale auction transfers, or sales to auto dismantlers are EXEMPT from smog certification.
* **Required Condition:** For retail delivery/registration, vehicle must have a valid California Smog Certification executed within the past 90 days.
* **System Action:** Flags trade-in as an internal **Service Reconditioning Checklist Item** ("Smog Inspection Required Prior to Retail Delivery"), rather than a fatal document rejection at trade intake.
* **Exceptions:** Dedicated Zero-Emission Vehicles (BEVs); motorcycles; diesel vehicles model year 1997 or older with GVWR $> 14,000\text{ lbs}$; gasoline vehicles 4 model years old or newer if smog transfer fee is paid under CVC § 4000.1(d)(1); wholesale transfers to other licensed dealers under CVC § 24007(a)(1).
* **Confidence Level:** **HIGH (Statutory Verification).**
* **Mandatory Human Review:** No (Can be verified electronically against Bureau of Automotive Repair / BAR database).

### Rule CA-ALTER-02: Erasure and Alteration Nullification Rule
* **Governing Statute:** **California Vehicle Code (CVC) § 5750–5753**; California DMV Vehicle Industry Services Title Manual, Reg 227.
* **Source URL:** https://www.dmv.ca.gov/portal/handbook/vehicle-industry-services-handbook/
* **Effective Date:** Active policy.
* **Last Reviewed Date:** November 2026.
* **Transaction & Document Type:** Any Certificate of Title or Reg 262 presented for transfer in California.
* **Required Condition:** The certificate of title must be free of physical erasures, strike-throughs, white-out corrections, or alterations on the seller, buyer, or odometer disclosure lines. Any alteration automatically nullifies the signature line.
* **Failure Mode Detected:** Line drawn through a mis-spelled buyer name or liquid correction fluid covering an odometer reading.
* **Exceptions:** If accompanied by an official California DMV **Statement of Error or Erasure (Form REG 101)** executed by the individual whose signature was altered.
* **Confidence Level:** **HIGH (Optical Alteration Detection).**
* **Mandatory Human Review:** **MANDATORY.** Any detected white-out or strike-through must be visually verified by a title clerk.

### Rule CA-REASSIGN-03: Wholesale Dealer Reassignment Sequence (Form REG 262)
* **Governing Statute:** **CVC § 5600** (Transfer Requirements); CVC § 5753.
* **Administrative Reference:** California DMV Dealer Handbook Chapter 8.
* **Source URL:** https://www.dmv.ca.gov/portal/handbook/vehicle-industry-services-handbook/
* **Required Condition:** All wholesale dealer-to-dealer reassignments must be executed sequentially on official California Secure Power of Attorney and Odometer Disclosure **Form REG 262**. Each intermediate dealer must record their exact Board of Equalization seller permit number and DMV occupational dealer license number.
* **Failure Mode Detected:** Dealer B sells to Dealer C, but Dealer B's endorsement is omitted, creating a reassignment break.
* **Exceptions:** Out-of-state wholesale dealer reassignment documents recognized under interstate comity.
* **Confidence Level:** **HIGH.**
* **Mandatory Human Review:** Yes, if dealer license numbers cannot be matched against DMV occupational registry.

---

## 5. Nevada Statutory Transfer Rules (Origin & Receiving State)

### Rule NV-REASSIGN-01: Sequential Dealer Reassignment Chain Continuity
* **Governing Statute:** **Nevada Revised Statutes (NRS) 482.400** & **NRS 482.431** (Delivery of Certificate; Transfer by Dealer).
* **Administrative Reference:** Nevada DMV Dealer Licensing Handbook § 4.
* **Source URL:** https://www.leg.state.nv.us/nrs/nrs-482.html#NRS482Sec400
* **Effective Date:** Active statute current through 2026.
* **Last Reviewed Date:** November 2026.
* **Transaction & Document Type:** Licensed motor vehicle dealer reassigning an out-of-state trade-in vehicle.
* **Required Condition:** Under NRS 482.431, a licensed dealer who purchases or takes a vehicle in trade must execute a direct, unbroken chain of reassignments. An intermediate dealer cannot bypass their endorsement. All intermediate dealer names, license numbers, and authorized signatures must be recorded in sequence.
* **Failure Mode Detected:** Nevada dealership takes trade-in originating from California auction; intermediate wholesale dealer skipped signing reassignment Block 2.
* **Exceptions:** None.
* **Confidence Level:** **HIGH.**
* **Mandatory Human Review:** Yes, if reassignment sequence count is discontinuous.

### Rule NV-BOS-02: Nevada Bill of Sale & Odometer Statement (Form VP-104)
* **Governing Statute:** **NRS 482.400**; Nevada DMV Administrative Regulations.
* **Administrative Reference:** Nevada DMV Form VP-104 Guidelines.
* **Source URL:** https://dmv.nv.gov/forms.htm
* **Effective Date:** Active policy.
* **Last Reviewed Date:** November 2026.
* **Transaction & Document Type:** Private party vehicle transfer in Nevada without title space or as supporting transfer instrument.
* **Required Condition:** Under Nevada DMV regulations, if an official **Bill of Sale (Form VP-104)** is utilized, it must include an explicit federal odometer statement and be signed by the seller. If executed outside Nevada for registration within Nevada, signature must be notarized or witnessed by an authorized Nevada DMV representative.
* **Failure Mode Detected:** VP-104 signed without required notary jurat or missing odometer disclosure.
* **Exceptions:** Transfers processed entirely within Nevada between Nevada residents with MVD portal identity verification.
* **Confidence Level:** **HIGH.**
* **Mandatory Human Review:** Yes, if out-of-state notarization is missing.

### Rule NV-VIN-03: Out-of-State Vehicle Inspection (Form VP-015)
* **Governing Statute:** **NRS 482.220** (Application for Registration of Out-of-State Vehicle).
* **Source URL:** https://www.leg.state.nv.us/nrs/nrs-482.html#NRS482Sec220
* **Required Condition:** Any vehicle previously titled or registered outside Nevada must undergo a physical VIN verification and safety inspection executed by a Nevada DMV inspector, licensed Nevada dealer, or law enforcement officer (Form VP-015).
* **Failure Mode Detected:** Out-of-state trade-in deal jacket submitted to Nevada DMV without completed Form VP-015.
* **Exceptions:** New vehicles delivered directly by franchised OEM distributors.
* **Confidence Level:** **HIGH.**
* **Mandatory Human Review:** No (Presence check for Form VP-015).

---

## 6. Cross-Border Interaction Matrix & Precedence Logic

When an out-of-state trade-in document packet enters CrossBorder TitleGuard, the rule engine applies a deterministic precedence hierarchy:

```
+========================================================================================================================+
|                                    CROSS-BORDER JURISDICTION PRECEDENCE HIERARCHY                                      |
+================================+================================+======================================================+
| Transaction Component          | Controlling Jurisdiction       | Evaluation Logic & Precedence                        |
+================================+================================+======================================================+
| 1. Certificate of Title Face   | Origin State (Issuing State)   | Validates document security features, VIN, registered|
|                                |                                | owner names, and printed brands according to issuing |
|                                |                                | state title design standards.                        |
+--------------------------------+--------------------------------+------------------------------------------------------+
| 2. Seller Sign-Off Assignment  | Origin State Statutory Rules   | Evaluates seller release rules of issuing state      |
|                                |                                | (e.g., checks older AZ notary boxes or CA Reg 227    |
|                                |                                | erasure rules).                                      |
+--------------------------------+--------------------------------+------------------------------------------------------+
| 3. Supporting Bill of Sale     | State where BOS was Executed   | Evaluates execution state's notary/witness laws      |
|                                |                                | (e.g., ADOT Form 48-2004 requires notary or MVD ATP  |
|                                |                                | witness under A.R.S. § 28-370).                      |
+--------------------------------+--------------------------------+------------------------------------------------------+
| 4. Odometer Disclosure         | Federal Mandate (49 CFR 580)   | Overrules any conflicting state exemptions for model |
|                                |                                | years 2011 and newer (20-year rolling window).       |
+--------------------------------+--------------------------------+------------------------------------------------------+
| 5. Reassignment Chain          | Intermediate Dealer States     | Validates sequential chain continuity across all     |
|                                |                                | intermediate licensed wholesale/retail dealers.      |
+--------------------------------+--------------------------------+------------------------------------------------------+
| 6. Final Registration & Smog   | Destination State (Receiving)  | Enforces destination state entry mandates (e.g., CA  |
|                                |                                | CVC § 4000.1 smog cert within 90 days; NV VP-015).   |
+================================+================================+======================================================+
```

---

## 7. Mandatory Human-Review Escalation Thresholds

The system strictly avoids autonomous legal compliance determination. Mandatory human-in-the-loop review is triggered whenever:

1. **OCR / VLM Confidence Degradation:** Any critical field (VIN, Odometer, Seller Name) is extracted with model confidence $< 90\%$.
2. **Colorless Dry-Emboss Suspected:** System detects a notary jurat text block without an optical ink impression seal (triggers tactile paper review).
3. **Physical Alteration / Erasure Detected:** System detects pixel variance, white-out texture, or strike-through lines over signature or mileage blocks (requires Statement of Error verification).
4. **Discontinuous Reassignment Chain:** Intermediate dealer licensing records cannot be verified against state occupational licensing tables.
5. **Estate / Power of Attorney Ambiguity:** Supporting death certificates, letters testamentary, or trustee signatures require manual legal verification.
