# PartsRescue PR1.1: Existing Solutions Audit Corrections & Capability Boundaries

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `evaluation/partsrescue-pr1.1-existing-solutions-corrections.md`  
**Phase:** PR1.1 — Evidence Integrity and Financial Reconciliation Patch  
**Standard Compliance:** `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`  
**Audit Authorities:** Automotive Software Competitive Intelligence Analyst, AI Product Strategist  
**Date:** November 14, 2026  
**Audit Determination:** **BLANKET NEGATIVE CLAIMS PURGED; DOCUMENTED VS UNKNOWN CAPABILITIES PARTITIONED; SPECIFIC ORCHESTRATION WHITE SPACE GROUNDED IN EVIDENCE**

---

## 1. Executive Correction: Purging Blanket Statements

In Phase PR1 research drafts, competitor systems and existing dealership platforms were occasionally characterized with sweeping dismissals, such as:
* *"Core DMS platforms and OEC provide zero active sourcing triage."*
* *"DMS systems go completely passive during stockouts."*
* *"No existing software connects parts to service."*

Under `.cursor/rules/research-standards.mdc`, these blanket statements are **retracted and replaced**. 

Commercial dealership software platforms are highly sophisticated and possess substantial documented capabilities in inventory replenishment, inter-dealer locating, and backorder matching. To maintain technical integrity, we partition what is **verified as documented** versus what is **unverified, unknown, or genuinely unaddressed**.

---

## 2. Documented vs Unknown Capabilities of Existing Systems

```
+========================================================================================================================+
|                                    EXISTING SYSTEMS CAPABILITY BOUNDARY AUDIT                                          |
+----+----------------------+-----------------------------+-----------------------------+--------------------------------+
| #  | Software Entity      | Documented Capabilities     | Documented Operational      | Unknown / Unverified           |
|    |                      | (Verified by Evidence)      | Boundaries & Limitations    | Capabilities (Do Not Assume)   |
+----+----------------------+-----------------------------+-----------------------------+--------------------------------+
| 01 | **OEConnection**     | - Automated backorder       | - Operates strictly within  | - Extent to which OEC is       |
|    | **(OEC) D2D Express**|   routing based on time and |   OEM dealer networks for   |   piloting local aftermarket   |
|    |                      |   distance algorithms.      |   exact OEM part numbers.   |   sourcing connections.        |
|    |                      | - Electronic dealer-to-     | - Does not model service    | - Potential unpublicized       |
|    |                      |   dealer sourcing network.  |   bay holding costs or      |   dispatch software partner-   |
|    |                      | - Resolves VOR car-down     |   technician labor queues.  |   ships in development.        |
|    |                      |   backorders nationally.    | - No customer SMS module.   |                                |
+----+----------------------+-----------------------------+-----------------------------+--------------------------------+
| 02 | **Core DMS Parts**   | - Real-time on-hand (`OH`)  | - Designed primarily for    | - Unannounced internal product |
|    | **Modules** (Tekion  |   and allocated (`AL`) stock|   inventory accounting and  |   roadmaps for autonomous      |
|    | ARC, CDK, Reynolds)  | - Multi-store inventory view|   historical replenishment. |   hotshot courier dispatch.    |
|    |                      |   across dealer groups.     | - Cross-channel trade-off   | - Custom API integrations built|
|    |                      | - Automatic replenishment   |   optimization (courier fee |   by large mega-dealer groups  |
|    |                      |   (min/max & RIM programs). |   vs bay idle cost) is not  |   (e.g. AutoNation, Penske).   |
|    |                      | - Emergency VOR order entry.|   documented as native.     |                                |
+----+----------------------+-----------------------------+-----------------------------+--------------------------------+
| 03 | **Commercial After-**| - Real-time stock querying  | - Operates in isolated web  | - Degree of custom DMS write-  |
|    | **market Portals**   |   at local warehouse depots.|   browser tabs outside DMS. |   back APIs supported for      |
|    | (Nexpart, Worldpac)  | - Electronic purchase order | - Requires manual vehicle   |   independent software vendors.|
|    |                      |   transmission for parts.   |   re-keying and manual OP   |                                |
|    |                      | - Rapid hotshot courier     |   purchase order creation.  |                                |
|    |                      |   dispatch delivery.        | - Blind to shop labor state.|                                |
+----+----------------------+-----------------------------+-----------------------------+--------------------------------+
| 04 | **OEM Electronic**   | - Authoritative vehicle     | - Focuses strictly on       | - Extent of dynamic automated  |
|    | **Parts Catalogs**   |   build & VIN option decode.|   part identification.      |   hardware package suggestions |
|    | (Snap-on, Microcat)  | - Supersession text notes   | - Does not check external   |   in next-generation web EPCs. |
|    |                      |   and technical bulletins.  |   distributor stock or      |                                |
|    |                      | - Visual schematic diagrams.|   execute purchasing orders.|                                |
+========================================================================================================================+
```

---

## 3. The Verified White Space: Grounded Definition

When we strip away exaggerated claims, what is the **precise, evidenced operational white space** that PartsRescue AI addresses?

The verified white space is **not** that "dealerships have no way to find parts." They do: they can search OEC D2DLink, call sister stores, or open a Nexpart browser tab.

Rather, the unaddressed operational friction lies in **the lack of unified, cross-functional economic triage connecting parts logistics, warranty rules, and service shop floor mechanics**:

1. **The Disconnected Economic Calculation:**
   * A parts counterperson deciding whether to order a part from a sister store (2-hour courier delivery at $25 fee) versus standard PDC replenishment (free freight, 3-day arrival) currently has **no tool calculating whether that $25 fee saves $160 in dead bay labor**.
   * Incumbent DMS and locator tools optimize for *parts freight expense*, not *dealership total net operating profit*.
2. **The Compliance & Customer Bridge:**
   * When an OEM part is unavailable, no existing tool automatically checks whether the RO is factory warranty (locking out aftermarket) or customer-pay (allowing certified aftermarket), while concurrently dispatching a digital authorization card to the vehicle owner's smartphone.
3. **The Labor Resequencing Signal:**
   * When a part is confirmed delayed by 4 hours, existing DMS dispatch boards do not receive an automated ETA signal to dynamically pull forward a quick maintenance job, leaving the technician stalled on an unbillable clock.

---

## 4. Evidentiary Conclusion

PartsRescue AI does **not** replace OEC D2DLink, nor does it replace the DMS inventory master. It acts as an **orchestrated economic decision layer** that sits across the DMS, parts locator tools, warranty rulesets, and customer mobile communication to resolve in-bay bottlenecks before they destroy shop throughput.
