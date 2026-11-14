# Phase 4 Technical Product Direction: CrossBorder TitleGuard Architecture

**Workspace:** Tekion Tek-Qubit Hackathon 2026  
**Document:** `research/phase4-technical-direction.md`  
**Stage:** Phase 4 – Final Concept Selection & Scope Freeze  
**Standard:** Compliant with `.cursor/rules/research-standards.mdc`, `.cursor/rules/tekion-context.mdc`, `references/tekion-themes.pdf`, and Phase 3.2 Authoritative Corrections  
**Author:** AI Solution Architect & Technical Review Committee  
**Purpose:** High-level system architecture, component specifications, model tradeoff analyses, failure-mode engineering, and deterministic governance without application code.

---

## 1. System Architecture Overview

CrossBorder TitleGuard avoids the fatal pitfall of using generative Large Language Models (LLMs) to make legal or compliance judgments. Instead, it utilizes a **hybrid neuro-symbolic architecture**:
1. **Perception Layer (Neuro):** Multimodal Vision-Language Models (VLMs) perform spatial OCR, cursive handwriting recognition, and unstructured layout extraction, emitting strictly typed JSON schemas with normalized bounding boxes.
2. **Reasoning Layer (Symbolic):** A deterministic Abstract Syntax Tree (AST) statutory engine evaluates versioned motor vehicle statutes, executing zero-hallucination arithmetic, string matching, and regulatory compliance logic.

```mermaid
flowchart TD
    subgraph INGESTION ["1. Ingestion & Optical Normalization Layer"]
        A[Scanned Multi-Page Deal Jacket PDF / Images] --> B[PDF Renderer: 300 DPI Rasterization]
        B --> C[OpenCV Pipeline: Deskewing, Contrast Normalization, Border Crop]
        C --> D[Document Layout Classifier: Title, BOS, POA, Smog]
    end

    subgraph EXTRACTION ["2. Multimodal VLM Extraction Engine"]
        D --> E[Multimodal Vision-Language Model<br/>Claude 3.5 Sonnet / GPT-4o Vision / Gemini 1.5 Pro]
        E --> F[Strict Pydantic JSON Schema Validation]
        F --> G1[Extracted Entity Vector: VIN, Odometer, Names]
        F --> G2[Extracted Visual Bounding Boxes: [ymin, xmin, ymax, xmax]]
        F --> G3[Extracted Confidence Scores per Field]
    end

    subgraph DETERMINISTIC ["3. Deterministic AST Statutory Rules Engine"]
        H[Declarative YAML/JSON Statutory Rulebase<br/>Versioned CA-NV-AZ Codes] --> I[AST Statutory Evaluator]
        G1 & G2 --> I
        I --> J1[Federal 20-Yr Odometer Rule Evaluator]
        I --> J2[Origin-State Seller Assignment Evaluator]
        I --> J3[AZ A.R.S. § 28-370 BOS/POA Witness Evaluator]
        I --> J4[CA CVC § 4000.1 Smog & Reg 227 Erasure Evaluator]
        I --> J5[NV NRS 482.431 Reassignment Chain Evaluator]
    end

    subgraph TRIAGE ["4. Exception Triage & Verification UI"]
        J1 & J2 & J3 & J4 & J5 & G3 --> K[Exception Severity Scorer]
        K -->|Confidence < 90% or Ambiguity| L1[Amber: Title Clerk Tactile Review Queue]
        K -->|Statutory Violation Detected| L2[Red: Non-Blocking F&I Desk Alert]
        K -->|All Rules Satisfied| L3[Green: Pre-Audit Passed - No Detected Defects]
        L1 & L2 & L3 --> M[Split-Screen React Review UI with PDF Bounding Box Overlays]
        M --> N[Proposed Tekion ARC Integration: Conceptual Deal Guard AI Payload]
    end
```

---

## 2. Component Engineering Breakdown

### 2.1 Ingestion & Optical Normalization Layer
* **Responsibility:** Ingests heterogeneous document streams (multi-page PDF deal jackets, high-resolution flatbed scans, mobile phone photos taken at sales desks) and standardizes them for visual perception.
* **Why It Is Needed:** Dealership desktop scanners generate varied resolutions, rotational skew, uneven lighting, and contrast variations that degrade OCR accuracy.
* **Candidate Technology Choices:** Python `pypdfium2` / `pdf2image` for rendering; `OpenCV` (headless) for Otsu thresholding, skew angle detection, and perspective transformation.
* **Input & Output:**
  * *Input:* Raw PDF file or multi-frame TIFF/JPEG image.
  * *Output:* Normalized, deskewed 300 DPI RGB image array per page.
* **Failure Modes:** Extremely low resolution ($<150\text{ DPI}$), severe optical glare, or truncated margins cutting off notary stamps.
* **Fallback Behavior:** Flags document as `IMAGE_QUALITY_DEGRADED`; prompts user to re-scan page with specific resolution guidelines.

### 2.2 Multimodal Vision-Language Extraction Engine
* **Responsibility:** Ingests normalized document page images and extracts printed text, cursive signatures, rubber notary stamps, checkbox marks, and table structures into a strongly typed Pydantic schema.
* **Why It Is Needed:** Physical vehicle titles feature banknote security paper, intaglio guilloche borders, anti-fraud "VOID" watermarks, and cursive signatures overlapping pre-printed lines. Traditional OCR (Tesseract, standard AWS Textract) fails on handwriting and distorted stamps over textured backgrounds. Multimodal VLMs provide superior spatial reasoning and zero-shot layout understanding.
* **Candidate Technology Comparison:**

| Model / Approach | Spatial Understanding | Cursive Handwriting | Rubber Stamp & Jurat Parsing | Processing Latency | API Cost / Page | Hackathon Suitability |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Claude 3.5 Sonnet (Vision)** | **Superior** | **State of the Art** | **Excellent (High detail)** | 3.5 – 6.0 sec | $0.008 – $0.012 | **Recommended Primary** |
| **GPT-4o (Vision)** | Excellent | Excellent | Good | 2.5 – 4.5 sec | $0.006 – $0.010 | Strong Alternative |
| **Gemini 1.5 Pro (Multimodal)** | Excellent | Good | Good | 3.0 – 5.0 sec | $0.005 – $0.008 | Strong Alternative |
| **AWS Textract (Queries/Forms)** | Moderate | Weak (Cursive fails) | Poor (Stamps ignored) | 1.5 – 2.5 sec | $0.015 – $0.025 | Inadequate for physical titles |

* **Input & Output:**
  * *Input:* 300 DPI page image + strict Pydantic JSON extraction prompt.
  * *Output:* Validated JSON payload containing exact field strings, normalized coordinates $[y_{\min}, x_{\min}, y_{\max}, x_{\max}]$, and extraction confidence scores.
* **Failure Modes:** Model hallucinating non-existent VIN characters; misreading cursive names; skipping faint rubber stamps.
* **Fallback Behavior:** Strict Pydantic schema parsing forces immediate retry on malformed JSON; any field failing validation (e.g., VIN failing 49 CFR § 565.15 modulo-11 check-digit verification at position 9) triggers immediate manual clerk escalation.

### 2.3 Deterministic AST Statutory Rules Engine
* **Responsibility:** Executes statutory transfer compliance logic deterministically against versioned motor vehicle codes (CA, NV, AZ, and Federal). **No generative AI or LLM is permitted in this layer.**
* **Why It Is Needed:** Compliance requires mathematical certainty and legal traceability. An LLM cannot be trusted to interpret statutes dynamically due to non-deterministic outputs and hallucinations.
* **Candidate Technology Choices:** Declarative YAML rule definitions compiled into a lightweight Abstract Syntax Tree (AST) evaluator using Python `jinja2` / `pyyaml` and deterministic boolean evaluation graphs.
* **Input & Output:**
  * *Input:* Extracted JSON entity payload + versioned state rulebase (e.g., `rules_az_statute_2026_v1.yaml`).
  * *Output:* Rule evaluation results vector: `[Rule_ID, Status (PASS/FAIL/UNKNOWN), Statutory_Citation, Evidence_Coordinates]`.
* **Failure Modes:** Missing statutory citation for an unexpected out-of-state title (e.g., an Oregon title in a CA dealer).
* **Fallback Behavior:** If an unknown state is detected, the engine emits `UNKNOWN_JURISDICTION_RULE` and routes to the Title Clerk's manual checklist queue.

### 2.4 Evidence-Linked Visual Annotation Layer
* **Responsibility:** Maps extracted bounding box coordinates directly onto the source document PDF, generating annotated visual overlays with color-coded triage bounding boxes (Green = Verified, Amber = Review Required, Red = Statutory Defect).
* **Why It Is Needed:** A list of text errors in a table is difficult for human clerks to verify quickly. Highlighting the defect directly on the physical document image provides instant visual validation.
* **Candidate Technology Choices:** React PDF viewer (`react-pdf` / `PDF.js`) with SVG canvas annotation overlays.
* **Input & Output:**
  * *Input:* Source document image + coordinate array $[y_{\min}, x_{\min}, y_{\max}, x_{\max}]$.
  * *Output:* Interactive visual viewport displaying annotated PDF with clickable error tags.

### 2.5 Tamper-Evident Audit Logging Layer
* **Responsibility:** Maintains an auditable, verifiable record of all document extractions, confidence scores, AST rule evaluations, and manual clerk overrides.
* **Tamper-Evidence Mechanism:** Rather than claiming unqualified "immutability", the system implements a **cryptographic SHA-256 hash-chaining protocol**. Each audit event record contains:
  $$\text{Hash}_t = \text{SHA-256}(\text{Hash}_{t-1} \,||\, \text{Timestamp} \,||\, \text{DocumentHash} \,||\, \text{RuleResults} \,||\, \text{ClerkID})$$
  Any retroactive modification to an extracted field or clerk approval breaks the cryptographic chain. Digital clerk sign-offs record the clerk's unique DMS user ID and a timestamped digital signature.
* **Upstream Sync:** Generates a signed JSON audit bundle prepared for dispatch to Tekion Deal Guard AI or archival storage.

---

## 3. Categorization of System Information States

To prevent treating probabilistic machine predictions as verified facts, CrossBorder TitleGuard enforces a strict taxonomy across four distinct data states:

```
+========================================================================================================================+
|                                    INFORMATION STATE TAXONOMY & AUDIT GOVERNANCE                                       |
+================================+================================+======================================================+
| Information State              | Operational Definition         | System Treatment & UI Representation                 |
+================================+================================+======================================================+
| **1. Machine-Extracted Facts** | Raw visual characters extracted| Displayed as candidate text; accompanied by numerical|
|                                | by VLM (names, dates, VIN,     | confidence score (0%–100%); links to source bounding |
|                                | mileage, notary text).         | box coordinates.                                     |
+--------------------------------+--------------------------------+------------------------------------------------------+
| **2. Deterministically         | Facts verified via mathematical| Tagged with Green Badge. Examples: VIN check-digit   |
|    Validated Facts**           | algorithms or external databases| validated via 49 CFR § 565.15 modulo-11 checksum     |
|                                | (checksums, BAR smog records). | (North American standard); Federal odometer 20-year  |
|                                |                                | rolling window arithmetic verified.                  |
+--------------------------------+--------------------------------+------------------------------------------------------+
| **3. Inferred Visual           | Probabilistic visual defects   | Tagged with Amber/Red Warning Badge. System cites    |
|    Anomalies**                 | flagged by optical models      | exact pixel region. Examples: strike-through detected|
|                                | (alterations, rubber stamps).  | over buyer name; unnotarized Arizona Bill of Sale.   |
+--------------------------------+--------------------------------+------------------------------------------------------+
| **4. Mandatory Human-          | Legal conditions that cannot be| Tagged with Amber "Clerk Review Required" Banner.    |
|    Verification Requirements** | determined optically (raised dry| Examples: Colorless dry-emboss notary seal; estate/  |
|                                | seals, estate death certs).    | trust transfer documents; low-confidence cursive.    |
+================================+================================+======================================================+
```

---

## 4. Failure Modes, Edge Cases & Safe Degradation Architecture

A resilient enterprise product must fail safely. Under no circumstances may an uncertain document be converted into a confident approval:

1. **Failure Mode 1: Colorless Dry-Embossed Notary Seals**
   * *Mechanism:* Certain out-of-state jurisdictions allow raised crimp seals without ink. A 2D optical scan captures no pixel contrast.
   * *Safe Degradation:* The VLM identifies the printed notary jurat text and commission expiration date, but notes `seal_optical_presence: false`. The rule engine flags: `AMBER: Dry Emboss Seal Suspected — Tactile Clerk Verification Required`. The deal is NOT marked compliant until the title clerk physically touches the document and checks a confirmation toggle.
2. **Failure Mode 2: VLM Hallucination on Cursive Handwriting**
   * *Mechanism:* The model encounters heavily distorted cursive signatures or altered dates and guesses characters.
   * *Safe Degradation:* Character-level log-probabilities are thresholded. Any extracted signature block with confidence $< 88\%$ or containing unexpected character sequences triggers an immediate `CONFIDENCE_ESCALATION` alert, forcing manual clerk verification.
3. **Failure Mode 3: Banknote Anti-Copy Guilloche Interference**
   * *Mechanism:* Title security paper triggers anti-copy pantographs ("VOID" text appearing across the background), causing OCR engines to inject "VOID" into seller assignment names.
   * *Safe Degradation:* Contrast-normalization pre-processing filters uniform background micro-patterns. The extraction prompt explicitly instructs the VLM to distinguish background security pantographs from foreground ink strokes.
4. **Failure Mode 4: VLM API Timeout or Outage**
   * *Mechanism:* Third-party vision model API latency exceeds 20 seconds or returns HTTP 503/429.
   * *Safe Degradation:* The system enforces a strict 15-second API timeout. Upon timeout, it degrades gracefully to a traditional layout OCR pipeline (Tesseract/Textract) combined with a prominent UI banner: `FALLBACK OCR ENGAGED — High-Precision VLM Offline; Manual Title Clerk Review Required for All Handwritten Fields`.

---

## 5. Technical Delivery Plan for Student Hackathon Team

To deliver a working prototype without code bloat, the 2- to 4-person team will execute across four modular components:
1. **Module 1 (Perception & Schema):** Python script utilizing `Anthropic API` (Claude 3.5 Sonnet Vision) / `OpenAI API` (GPT-4o) with a standardized Pydantic schema extracting title fields from PDF deal jackets.
2. **Module 2 (Rules Core):** Declarative YAML rule engine evaluating CA, NV, and AZ transfer rules deterministically.
3. **Module 3 (Synthetic Test Dataset):** 10 curated synthetic PDF deal jackets (clean, defective, and ambiguous cases) generated using reportlab and realistic banknote background textures.
4. **Module 4 (Demonstration UI):** A lightweight `Streamlit` or `React / Vite` split-screen interface displaying the annotated PDF with SVG bounding box overlays and the interactive pre-audit compliance checklist.
