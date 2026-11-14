import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Professional Dark Enterprise Theme
    BG_DARK = RGBColor(11, 17, 32)         # #0B1120
    PANEL_BG = RGBColor(22, 30, 50)        # #161E32
    PANEL_BORDER = RGBColor(40, 54, 85)    # #283655
    PANEL_HIGHLIGHT = RGBColor(30, 41, 68) # #1E2944
    ACCENT_CYAN = RGBColor(14, 165, 233)   # #0EA5E9
    ACCENT_TEAL = RGBColor(20, 184, 166)   # #14B8A6
    ACCENT_EMERALD = RGBColor(16, 185, 129)# #10B981
    ACCENT_AMBER = RGBColor(245, 158, 11)  # #F59E0B
    ACCENT_RED = RGBColor(239, 68, 68)     # #EF4444
    TEXT_WHITE = RGBColor(248, 250, 252)   # #F8FAFC
    TEXT_MUTED = RGBColor(148, 163, 184)   # #94A3B8
    TEXT_SUBTLE = RGBColor(100, 116, 139)  # #64748B
    BADGE_BG = RGBColor(15, 45, 75)        # #0F2D4B
    STATE_BOX_BG = RGBColor(18, 26, 44)    # #121A2C

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, badge_text, title_text, subtitle_text, slide_num):
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(5.2), Inches(0.32))
        badge.fill.solid()
        badge.fill.fore_color.rgb = BADGE_BG
        badge.line.color.rgb = ACCENT_CYAN
        badge.line.width = Pt(1)
        tf_b = badge.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
        p_b = tf_b.paragraphs[0]
        p_b.alignment = PP_ALIGN.CENTER
        run_b = p_b.add_run()
        run_b.text = badge_text.upper()
        run_b.font.size = Pt(9.0)
        run_b.font.bold = True
        run_b.font.color.rgb = ACCENT_CYAN
        run_b.font.name = "Arial"

        snum = slide.shapes.add_textbox(Inches(11.333), Inches(0.4), Inches(1.2), Inches(0.32))
        tf_s = snum.text_frame
        p_s = tf_s.paragraphs[0]
        p_s.alignment = PP_ALIGN.RIGHT
        run_s = p_s.add_run()
        run_s.text = f"SLIDE {slide_num} OF 6"
        run_s.font.size = Pt(10)
        run_s.font.bold = True
        run_s.font.color.rgb = TEXT_SUBTLE
        run_s.font.name = "Arial"

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.78), Inches(11.733), Inches(0.55))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        run_t = p_t.add_run()
        run_t.text = title_text
        run_t.font.size = Pt(22)
        run_t.font.bold = True
        run_t.font.color.rgb = TEXT_WHITE
        run_t.font.name = "Arial"

        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.35))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_right = tf_sub.margin_top = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        run_sub = p_sub.add_run()
        run_sub.text = subtitle_text
        run_sub.font.size = Pt(11.5)
        run_sub.font.color.rgb = TEXT_MUTED
        run_sub.font.name = "Arial"

    def add_bottom_banner(slide, banner_text, is_qualification=False):
        banner = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.6), Inches(11.733), Inches(0.52))
        banner.fill.solid()
        banner.fill.fore_color.rgb = PANEL_HIGHLIGHT if not is_qualification else RGBColor(28, 22, 20)
        banner.line.color.rgb = ACCENT_CYAN if not is_qualification else ACCENT_AMBER
        banner.line.width = Pt(1.2)
        tf = banner.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.08)
        tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = banner_text
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = TEXT_WHITE if not is_qualification else ACCENT_AMBER
        run.font.name = "Arial"

    # =========================================================================
    # SLIDE 1: THE PROBLEM
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)
    add_header(slide1, 
               "Tekion Tek-Qubit 2026 | Theme 1: AI & Automation | UC04", 
               "One Missing Part. An Entire Workshop at Risk.", 
               "How a single mid-repair parts shortage cascades into hoist lock, idle labor, and missed service targets.", 
               1)

    cards_s1 = [
        {
            "tag": "1. THE MID-REPAIR DISRUPTION",
            "tag_color": ACCENT_AMBER,
            "title": "Hoist Lock on Bay B4",
            "subtitle": "Ford Explorer (RO-1042) — Modeled Disruption",
            "bullets": [
                "Brake overhaul in progress at 09:45 AM (t=21).",
                "Seized caliper mounting pin discovered mid-repair.",
                "Parts counter confirms: Part is out of stock.",
                "Vehicle is partially dismantled on hoist; wheels off.",
                "Holding lot H2 is saturated; Bay B4 is immobilized."
            ],
            "stat": "STALL TYPE: MECHANICAL HOIST LOCK"
        },
        {
            "tag": "2. THE WORKSHOP CASCADE",
            "tag_color": ACCENT_RED,
            "title": "Stranded Bay & Labor",
            "subtitle": "Specialized Alignment Hoist Blocked",
            "bullets": [
                "Bay B4 is the shop's specialized alignment rack.",
                "Certified Technician K1 waits for part delivery.",
                "Vehicle cannot be moved until repair is verified safe.",
                "DMS schedule faces unexpected bay blockage.",
                "Downstream jobs queued for Bay B4 are delayed."
            ],
            "stat": "IMPACT: HOIST & TECH IMMOBILIZED"
        },
        {
            "tag": "3. THE DOWNSTREAM CONFLICT",
            "tag_color": ACCENT_CYAN,
            "title": "Missed Completion Target",
            "subtitle": "Commercial Fleet F-150 (RO-1051)",
            "bullets": [
                "Awaiting ADAS camera & alignment calibration in Bay B4.",
                "Governed by modeled commercial fleet promise (12:30 PM).",
                "Priority weight w=3.0 reflects commercial operational urgency.",
                "Cannot enter until Bay B4 is cleared, inspected, and stowed.",
                "Cascading delay threatens fleet operational turnaround target."
            ],
            "stat": "TARGET: MODELED FLEET SLA (12:30 PM)"
        }
    ]

    for i, c in enumerate(cards_s1):
        left = Inches(0.8 + i * 4.0)
        top = Inches(1.85)
        width = Inches(3.733)
        height = Inches(4.55)

        card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = PANEL_BG
        card.line.color.rgb = PANEL_BORDER
        card.line.width = Pt(1.2)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.2)

        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = c["tag"]
        r0.font.size = Pt(9.0)
        r0.font.bold = True
        r0.font.color.rgb = c["tag_color"]
        r0.font.name = "Arial"

        p1 = tf.add_paragraph()
        p1.space_before = Pt(4)
        r1 = p1.add_run()
        r1.text = c["title"]
        r1.font.size = Pt(15)
        r1.font.bold = True
        r1.font.color.rgb = TEXT_WHITE
        r1.font.name = "Arial"

        p2 = tf.add_paragraph()
        p2.space_before = Pt(2)
        r2 = p2.add_run()
        r2.text = c["subtitle"]
        r2.font.size = Pt(10.0)
        r2.font.bold = True
        r2.font.color.rgb = ACCENT_CYAN
        r2.font.name = "Arial"

        for b in c["bullets"]:
            pb = tf.add_paragraph()
            pb.space_before = Pt(6)
            rb = pb.add_run()
            rb.text = f"•  {b}"
            rb.font.size = Pt(9.5)
            rb.font.color.rgb = TEXT_MUTED
            rb.font.name = "Arial"

        ps = tf.add_paragraph()
        ps.space_before = Pt(16)
        rs = ps.add_run()
        rs.text = c["stat"]
        rs.font.size = Pt(8.5)
        rs.font.bold = True
        rs.font.color.rgb = c["tag_color"]
        rs.font.name = "Arial"

    add_bottom_banner(slide1, "CORE RECOVERY REALITY: Parts shortages are not just inventory problems. They are service-operation recovery problems.")

    # =========================================================================
    # SLIDE 2: THE MISSING DECISION LAYER
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, 
               "The Operational Coordination Gap", 
               "Finding a Part Is Not the Same as Recovering a Workshop.", 
               "Decoupled parts sourcing and bay scheduling create local cost traps and uncoordinated workshop delays.", 
               2)

    # Left Panel: Fixed-Source Baseline A2
    p_left = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(5.7), Inches(4.55))
    p_left.fill.solid()
    p_left.fill.fore_color.rgb = PANEL_BG
    p_left.line.color.rgb = ACCENT_RED
    p_left.line.width = Pt(1.2)
    tf_l = p_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = Inches(0.3)
    tf_l.margin_top = Inches(0.22)

    pl0 = tf_l.paragraphs[0]
    rl0 = pl0.add_run()
    rl0.text = "DECOUPLED SOURCING: STUDY-DEFINED BASELINE A2"
    rl0.font.size = Pt(9.5)
    rl0.font.bold = True
    rl0.font.color.rgb = ACCENT_RED

    pl1 = tf_l.add_paragraph()
    pl1.space_before = Pt(4)
    rl1 = pl1.add_run()
    rl1.text = "The Local Cost Minimization Trap"
    rl1.font.size = Pt(15)
    rl1.font.bold = True
    rl1.font.color.rgb = TEXT_WHITE

    bullets_l = [
        ("Parts Sourcing Evaluation:", "Parts counter searches catalog. Candidates: S2 Sister Store ($18 freight, usable at 12:05 PM) vs S1 Hotshot Courier ($55 freight, usable at 10:15 AM)."),
        ("Isolated Cost Selection:", "Baseline A2 selects S2 to minimize departmental freight expense ($18 vs $55), saving $37 locally."),
        ("Departmental Divide:", "Parts sourcing decision is made without visibility into bay scheduling consequences or downstream RO promise targets."),
        ("Downstream Blockage:", "Because S2 arrives at 12:05 PM, Bay B4 remains occupied until 13:15 PM (t=63). Downstream Fleet RO-1051 cannot start until 13:15 PM."),
        ("Schedule Consequence:", "Fleet RO-1051 finishes at 15:15 PM (t=87) — 165 minutes late against its modeled 12:30 PM completion target (Z1 = 99.0 ticks).")
    ]

    for title_b, desc_b in bullets_l:
        p = tf_l.add_paragraph()
        p.space_before = Pt(7)
        r_t = p.add_run()
        r_t.text = f"{title_b} "
        r_t.font.bold = True
        r_t.font.size = Pt(9.5)
        r_t.font.color.rgb = ACCENT_AMBER
        r_d = p.add_run()
        r_d.text = desc_b
        r_d.font.size = Pt(9.0)
        r_d.font.color.rgb = TEXT_MUTED

    pl_stat = tf_l.add_paragraph()
    pl_stat.space_before = Pt(14)
    rl_stat = pl_stat.add_run()
    rl_stat.text = "RESULT: SAVES $37 IN FREIGHT — BUT DELAYS BAY B4 AND DOWNSTREAM FLEET BY 110 MIN"
    rl_stat.font.size = Pt(8.5)
    rl_stat.font.bold = True
    rl_stat.font.color.rgb = ACCENT_RED

    # Right Panel: StallBreaker's Coordinated Approach
    p_right = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.833), Inches(1.85), Inches(5.7), Inches(4.55))
    p_right.fill.solid()
    p_right.fill.fore_color.rgb = PANEL_BG
    p_right.line.color.rgb = ACCENT_EMERALD
    p_right.line.width = Pt(1.2)
    tf_r = p_right.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = Inches(0.3)
    tf_r.margin_top = Inches(0.22)

    pr0 = tf_r.paragraphs[0]
    rr0 = pr0.add_run()
    rr0.text = "COORDINATED RECOVERY: STALLBREAKER JOINT POLICY P3"
    rr0.font.size = Pt(9.5)
    rr0.font.bold = True
    rr0.font.color.rgb = ACCENT_EMERALD

    pr1 = tf_r.add_paragraph()
    pr1.space_before = Pt(4)
    rr1 = pr1.add_run()
    rr1.text = "Feasibility-Gated Joint Recovery"
    rr1.font.size = Pt(15)
    rr1.font.bold = True
    rr1.font.color.rgb = TEXT_WHITE

    bullets_r = [
        ("Simultaneous Evaluation:", "Evaluates candidate parts sourcing options simultaneously with downstream workshop bay and technician scheduling."),
        ("Quantified Schedule Value:", "Recognizes that expedited Hotshot S1 ($55) arrives at 10:15 AM, enabling Bay B4 release at 11:25 AM (110 minutes earlier)."),
        ("Target Protection:", "Downstream Fleet RO-1051 starts at 11:25 AM and completes at 13:25 PM — recovering 110 minutes of downstream delay!"),
        ("Feasibility Gated:", "Models vehicle teardown states, hoist clearance, and pickup staging lot capacity before proposing the recovery plan."),
        ("Explainable Proposal:", "Presents Advisor with clear trade-off: '+$37 freight premium releases Bay B4 110 min earlier, recovering 110 min on priority fleet job.'")
    ]

    for title_b, desc_b in bullets_r:
        p = tf_r.add_paragraph()
        p.space_before = Pt(7)
        r_t = p.add_run()
        r_t.text = f"{title_b} "
        r_t.font.bold = True
        r_t.font.size = Pt(9.5)
        r_t.font.color.rgb = ACCENT_CYAN
        r_d = p.add_run()
        r_d.text = desc_b
        r_d.font.size = Pt(9.0)
        r_d.font.color.rgb = TEXT_MUTED

    pr_stat = tf_r.add_paragraph()
    pr_stat.space_before = Pt(14)
    rr_stat = pr_stat.add_run()
    rr_stat.text = "RESULT: 66.7% WEIGHTED LATENESS REDUCTION | 110 MINUTES DOWNSTREAM DELAY RECOVERED"
    rr_stat.font.size = Pt(8.5)
    rr_stat.font.bold = True
    rr_stat.font.color.rgb = ACCENT_EMERALD

    add_bottom_banner(slide2, "THE COORDINATION GAP: Parts sourcing choices directly alter downstream bay availability and completion milestones.")

    # =========================================================================
    # SLIDE 3: INTRODUCING STALLBREAKER
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, 
               "Proposed System Architecture & Decision Flow", 
               "One Recovery Decision. Multiple Operational Constraints.", 
               "Designed to integrate with Tekion DMS, subject to available API access and authorization.", 
               3)

    arch_layers = [
        ("1. INGESTION", ACCENT_CYAN, "DMS Data Feed", [
            "Planned Tekion DMS Feed",
            "Active RO & Labor Status",
            "Bay & Hoist Assignments",
            "Teardown State Data"
        ], None),
        ("2. SOURCING", ACCENT_TEAL, "Parts Logistics", [
            "Planned Parts Catalog API",
            "Sister Store Network Stock",
            "Wholesale Courier Quotes",
            "Landed Cost & Usable ETA"
        ], None),
        ("3. OPTIMIZER", ACCENT_EMERALD, "CP-SAT Engine", [
            "Lexicographic Hierarchy",
            "1: Minimize Promise Lateness",
            "2: Minimize Bay Idle Time",
            "3: Control Freight Expense"
        ], "TARGET: BENCHMARK RUNTIME"),
        ("4. GATING", ACCENT_AMBER, "Feasibility & Safety", [
            "Modeled Vehicle States",
            "SAFE_TO_MOVE Condition",
            "Bay Exclusivity Guard",
            "Pickup Staging Lot Check"
        ], None),
        ("5. COPILOT", ACCENT_CYAN, "Explainable UI", [
            "Advisor Recovery Card",
            "Trade-Off Rationale",
            "Natural-Language Context",
            "Audit Log & Cost Delta"
        ], None),
        ("6. EXECUTION", ACCENT_EMERALD, "Human Control", [
            "Mandatory Advisor Sign-Off",
            "Pre-Execution Revalidation",
            "Planned Outbox Pattern",
            "Controlled DMS Commit"
        ], None)
    ]

    for i, (layer_num, layer_color, layer_name, items, footer_tag) in enumerate(arch_layers):
        left = Inches(0.8 + i * 1.98)
        top = Inches(1.85)
        width = Inches(1.85)
        height = Inches(4.55)

        card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = PANEL_BG
        card.line.color.rgb = layer_color if i == 2 else PANEL_BORDER
        card.line.width = Pt(1.5 if i == 2 else 1)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.12)
        tf.margin_top = Inches(0.18)

        p0 = tf.paragraphs[0]
        p0.alignment = PP_ALIGN.CENTER
        r0 = p0.add_run()
        r0.text = layer_num
        r0.font.size = Pt(8.5)
        r0.font.bold = True
        r0.font.color.rgb = layer_color

        p1 = tf.add_paragraph()
        p1.alignment = PP_ALIGN.CENTER
        p1.space_before = Pt(3)
        r1 = p1.add_run()
        r1.text = layer_name
        r1.font.size = Pt(11.0)
        r1.font.bold = True
        r1.font.color.rgb = TEXT_WHITE

        p_div = tf.add_paragraph()
        p_div.alignment = PP_ALIGN.CENTER
        p_div.space_before = Pt(4)
        r_div = p_div.add_run()
        r_div.text = "─────────"
        r_div.font.size = Pt(8)
        r_div.font.color.rgb = PANEL_BORDER

        for it in items:
            pi = tf.add_paragraph()
            pi.space_before = Pt(7)
            ri = pi.add_run()
            ri.text = f"• {it}"
            ri.font.size = Pt(8.8)
            ri.font.color.rgb = TEXT_MUTED if i != 2 else TEXT_WHITE

        if footer_tag:
            ps = tf.add_paragraph()
            ps.space_before = Pt(14)
            ps.alignment = PP_ALIGN.CENTER
            rs = ps.add_run()
            rs.text = footer_tag
            rs.font.size = Pt(8.0)
            rs.font.bold = True
            rs.font.color.rgb = ACCENT_EMERALD

    add_bottom_banner(slide3, "MISSION POSITIONING: We are not building another parts-finding chatbot. We are building an operational recovery decision engine.")

    # =========================================================================
    # SLIDE 4: HOW STALLBREAKER THINKS (ENHANCED ALIGNMENT)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, 
               "Operational & Physical Feasibility", 
               "An Optimal Plan Must Also Be Physically Possible.", 
               "StallBreaker is designed to reject proposals violating physical constraints; execution requires operational verification.", 
               4)

    # Main Left Panel: Visual State Machine Diagrams
    left_w = Inches(7.9)
    top_veh = Inches(1.85)
    h_veh = Inches(2.2)

    panel_v = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_veh, left_w, h_veh)
    panel_v.fill.solid()
    panel_v.fill.fore_color.rgb = PANEL_BG
    panel_v.line.color.rgb = ACCENT_CYAN
    panel_v.line.width = Pt(1.2)
    tf_pv = panel_v.text_frame
    tf_pv.word_wrap = True
    tf_pv.margin_left = tf_pv.margin_right = Inches(0.2)
    tf_pv.margin_top = Inches(0.12)

    pv0 = tf_pv.paragraphs[0]
    rv0 = pv0.add_run()
    rv0.text = "ENTITY 1: MODELED VEHICLE PHYSICAL STATE MACHINE (ENTITY V)"
    rv0.font.size = Pt(9.5)
    rv0.font.bold = True
    rv0.font.color.rgb = ACCENT_CYAN

    # 5 visual sequential boxes for Vehicle
    v_states = [
        ("PARTIALLY\nDISMANTLED", "Unbolted on Hoist"),
        ("MECHANICALLY\nCOMPLETE", "Parts Bolted"),
        ("FINAL\nVERIFICATION", "Torque & DTC Scan"),
        ("SAFE TO MOVE\nCERTIFIED", "Tech Sign-Off"),
        ("PICKUP\nSTAGING", "Delivery Lot Stall")
    ]
    box_w = Inches(1.35)
    box_h = Inches(1.1)
    y_box_v = Inches(2.28)

    for idx, (st_name, st_sub) in enumerate(v_states):
        bx = Inches(1.0 + idx * 1.5)
        sbox = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, y_box_v, box_w, box_h)
        sbox.fill.solid()
        sbox.fill.fore_color.rgb = STATE_BOX_BG
        sbox.line.color.rgb = ACCENT_TEAL if idx == 3 else PANEL_BORDER
        sbox.line.width = Pt(1.5 if idx == 3 else 1)
        tf_sb = sbox.text_frame
        tf_sb.word_wrap = True
        tf_sb.margin_left = tf_sb.margin_right = tf_sb.margin_top = tf_sb.margin_bottom = Inches(0.05)
        
        p = tf_sb.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = st_name
        r.font.size = Pt(8.0)
        r.font.bold = True
        r.font.color.rgb = TEXT_WHITE if idx != 3 else ACCENT_TEAL
        
        p2 = tf_sb.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        p2.space_before = Pt(2)
        r2 = p2.add_run()
        r2.text = st_sub
        r2.font.size = Pt(7.0)
        r2.font.color.rgb = TEXT_MUTED

        if idx < len(v_states) - 1:
            arr = slide4.shapes.add_textbox(bx + box_w, y_box_v + Inches(0.35), Inches(0.15), Inches(0.3))
            tf_a = arr.text_frame
            tf_a.margin_left = tf_a.margin_right = tf_a.margin_top = tf_a.margin_bottom = 0
            pa = tf_a.paragraphs[0]
            ra = pa.add_run()
            ra.text = "➔"
            ra.font.size = Pt(10)
            ra.font.color.rgb = ACCENT_CYAN

    pv_foot = tf_pv.add_paragraph()
    pv_foot.space_before = Pt(82)
    rv_foot = pv_foot.add_run()
    rv_foot.text = "Key Guard: Vehicle transit is strictly locked until a certified technician logs SAFE_TO_MOVE inspection sign-off."
    rv_foot.font.size = Pt(8.5)
    rv_foot.font.color.rgb = TEXT_MUTED

    # Bottom Flow: Bay Resource State Machine
    top_bay = Inches(4.18)
    h_bay = Inches(2.22)

    panel_b = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_bay, left_w, h_bay)
    panel_b.fill.solid()
    panel_b.fill.fore_color.rgb = PANEL_BG
    panel_b.line.color.rgb = ACCENT_EMERALD
    panel_b.line.width = Pt(1.2)
    tf_pb = panel_b.text_frame
    tf_pb.word_wrap = True
    tf_pb.margin_left = tf_pb.margin_right = Inches(0.2)
    tf_pb.margin_top = Inches(0.12)

    pb0 = tf_pb.paragraphs[0]
    rb0 = pb0.add_run()
    rb0.text = "ENTITY 2: BAY RESOURCE STATE MACHINE (ENTITY B4)"
    rb0.font.size = Pt(9.5)
    rb0.font.bold = True
    rb0.font.color.rgb = ACCENT_EMERALD

    b_states = [
        ("OCCUPIED\n(Car V1 Inside)", "Labor or Verification"),
        ("CLEARANCE\nPENDING", "V1 Traversing Out"),
        ("AVAILABLE FOR\nALLOCATION", "Floor Clean & Stowed"),
        ("OCCUPIED\n(Car V2 Inside)", "Downstream Job Starts")
    ]
    box_w_b = Inches(1.65)
    box_h_b = Inches(1.1)
    y_box_b = Inches(4.62)

    for idx, (st_name, st_sub) in enumerate(b_states):
        bx = Inches(1.05 + idx * 1.88)
        sbox = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, y_box_b, box_w_b, box_h_b)
        sbox.fill.solid()
        sbox.fill.fore_color.rgb = STATE_BOX_BG
        sbox.line.color.rgb = ACCENT_EMERALD if idx == 2 else PANEL_BORDER
        sbox.line.width = Pt(1.5 if idx == 2 else 1)
        tf_sb = sbox.text_frame
        tf_sb.word_wrap = True
        tf_sb.margin_left = tf_sb.margin_right = tf_sb.margin_top = tf_sb.margin_bottom = Inches(0.05)
        
        p = tf_sb.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = st_name
        r.font.size = Pt(8.0)
        r.font.bold = True
        r.font.color.rgb = TEXT_WHITE if idx != 2 else ACCENT_EMERALD
        
        p2 = tf_sb.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        p2.space_before = Pt(2)
        r2 = p2.add_run()
        r2.text = st_sub
        r2.font.size = Pt(7.0)
        r2.font.color.rgb = TEXT_MUTED

        if idx < len(b_states) - 1:
            arr = slide4.shapes.add_textbox(bx + box_w_b, y_box_b + Inches(0.35), Inches(0.2), Inches(0.3))
            tf_a = arr.text_frame
            tf_a.margin_left = tf_a.margin_right = tf_a.margin_top = tf_a.margin_bottom = 0
            pa = tf_a.paragraphs[0]
            ra = pa.add_run()
            ra.text = "➔"
            ra.font.size = Pt(10)
            ra.font.color.rgb = ACCENT_EMERALD

    pb_foot = tf_pb.add_paragraph()
    pb_foot.space_before = Pt(82)
    rb_foot = pb_foot.add_run()
    rb_foot.text = "Key Guard: Downstream vehicle V2 cannot enter until V1 has cleared the threshold and bay housekeeping is confirmed."
    rb_foot.font.size = Pt(8.5)
    rb_foot.font.color.rgb = TEXT_MUTED

    # Right Panel: 3 Core Feasibility Invariants
    p_guards = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.95), Inches(1.85), Inches(3.583), Inches(4.55))
    p_guards.fill.solid()
    p_guards.fill.fore_color.rgb = PANEL_BG
    p_guards.line.color.rgb = ACCENT_AMBER
    p_guards.line.width = Pt(1.2)
    tf_g = p_guards.text_frame
    tf_g.word_wrap = True
    tf_g.margin_left = tf_g.margin_right = Inches(0.2)
    tf_g.margin_top = Inches(0.2)

    pg0 = tf_g.paragraphs[0]
    rg0 = pg0.add_run()
    rg0.text = "3 CORE FEASIBILITY INVARIANTS"
    rg0.font.size = Pt(10)
    rg0.font.bold = True
    rg0.font.color.rgb = ACCENT_AMBER

    guards_list = [
        ("Invariant CE-1: Zero Premature Motion", "Vehicle movement is blocked until SAFE_TO_MOVE condition is certified. If inspection checks fail, the bay remains locked for rework."),
        ("Invariant CE-3: Strict Hoist Exclusivity", "Bay occupancy is strictly bounded to 1. Downstream vehicle cannot enter until Seq 3 confirms AVAILABLE_FOR_ALLOCATION."),
        ("Invariant CE-7: Staging Lot Reservation", "Vehicle transit requires AvailableStalls(PickupLot) >= 1. Prevents workshop lot gridlock.")
    ]

    for g_title, g_desc in guards_list:
        p = tf_g.add_paragraph()
        p.space_before = Pt(10)
        rt = p.add_run()
        rt.text = f"{g_title}\n"
        rt.font.size = Pt(9.5)
        rt.font.bold = True
        rt.font.color.rgb = TEXT_WHITE
        rd = p.add_run()
        rd.text = g_desc
        rd.font.size = Pt(8.8)
        rd.font.color.rgb = TEXT_MUTED

    add_bottom_banner(slide4, "FEASIBILITY PRINCIPLE: StallBreaker is designed to reject proposals violating modeled physical states; execution requires operational verification.")

    # =========================================================================
    # SLIDE 5: WHY JOINT OPTIMIZATION MATTERS
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, 
               "Mathematical Evidence & S-MATH-01 Benchmark", 
               "Better Recovery Through Coordinated Decisions.", 
               "Independent evaluation on canonical benchmark S-MATH-01: fixed-source baseline A2 vs joint policy P3.", 
               5)

    # Comparative Table
    rows, cols = 7, 3
    left_t = Inches(0.8)
    top_t = Inches(1.85)
    width_t = Inches(7.5)
    height_t = Inches(3.2)

    table_shape = slide5.shapes.add_table(rows, cols, left_t, top_t, width_t, height_t)
    table = table_shape.table
    table.columns[0].width = Inches(3.1)
    table.columns[1].width = Inches(2.2)
    table.columns[2].width = Inches(2.2)

    table_data = [
        ("Metric / Dimension", "Baseline A2: Fixed-Source Selection", "Policy P3: Joint Optimization"),
        ("Parts Sourcing Candidate", "S2: Sister Store ($18 freight)", "S1: Hotshot Courier ($55 freight)"),
        ("Usable Part Arrival Time", "t = 49 (12:05 PM)", "t = 27 (10:15 AM) [110m Earlier]"),
        ("Bay B4 Hoist Release Time", "t = 63 (13:15 PM)", "t = 41 (11:25 AM) [110m Earlier]"),
        ("Downstream RO-1051 Completion", "t = 87 (15:15 PM)", "t = 65 (13:25 PM)"),
        ("Downstream Lateness (vs 12:30 PM)", "165 minutes late", "55 minutes late (110m Saved)"),
        ("Total Weighted Customer Lateness (Z1)", "99.0 weighted ticks", "33.0 weighted ticks (-66.7%)")
    ]

    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            cell.fill.solid()
            if r_idx == 0:
                cell.fill.fore_color.rgb = RGBColor(15, 35, 65)
            elif r_idx % 2 == 1:
                cell.fill.fore_color.rgb = PANEL_BG
            else:
                cell.fill.fore_color.rgb = PANEL_HIGHLIGHT

            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER
            run = p.runs[0]
            run.font.name = "Arial"
            if r_idx == 0:
                run.font.size = Pt(9.5)
                run.font.bold = True
                run.font.color.rgb = ACCENT_CYAN if c_idx > 0 else TEXT_WHITE
            elif r_idx == 6:
                run.font.size = Pt(10.0)
                run.font.bold = True
                run.font.color.rgb = ACCENT_EMERALD if c_idx == 2 else (ACCENT_AMBER if c_idx == 1 else TEXT_WHITE)
            else:
                run.font.size = Pt(9.0)
                run.font.color.rgb = TEXT_WHITE if c_idx == 2 else (TEXT_MUTED if c_idx == 0 else TEXT_WHITE)

    # Right Stat Card 1: 66.7%
    sc1 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(1.85), Inches(3.933), Inches(2.15))
    sc1.fill.solid()
    sc1.fill.fore_color.rgb = PANEL_BG
    sc1.line.color.rgb = ACCENT_EMERALD
    sc1.line.width = Pt(1.5)
    tf_sc1 = sc1.text_frame
    tf_sc1.word_wrap = True
    tf_sc1.margin_left = tf_sc1.margin_right = Inches(0.2)
    tf_sc1.margin_top = Inches(0.18)

    psc1_0 = tf_sc1.paragraphs[0]
    rsc1_0 = psc1_0.add_run()
    rsc1_0.text = "PRIMARY HEADLINE METRIC (S-MATH-01)"
    rsc1_0.font.size = Pt(9.0)
    rsc1_0.font.bold = True
    rsc1_0.font.color.rgb = ACCENT_EMERALD

    psc1_1 = tf_sc1.add_paragraph()
    psc1_1.space_before = Pt(2)
    rsc1_1 = psc1_1.add_run()
    rsc1_1.text = "66.7% REDUCTION"
    rsc1_1.font.size = Pt(22)
    rsc1_1.font.bold = True
    rsc1_1.font.color.rgb = TEXT_WHITE

    psc1_2 = tf_sc1.add_paragraph()
    psc1_2.space_before = Pt(4)
    rsc1_2 = psc1_2.add_run()
    rsc1_2.text = "In total weighted customer & fleet promise lateness (Z1 drops from 99.0 to 33.0 weighted ticks under Milestone 1 / Eq C25).\n* Secondary staging sensitivity variant yields 62.9% reduction."
    rsc1_2.font.size = Pt(8.8)
    rsc1_2.font.color.rgb = TEXT_MUTED

    # Right Stat Card 2: 110 Minutes Qualified
    sc2 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(4.2), Inches(3.933), Inches(2.2))
    sc2.fill.solid()
    sc2.fill.fore_color.rgb = PANEL_BG
    sc2.line.color.rgb = ACCENT_CYAN
    sc2.line.width = Pt(1.5)
    tf_sc2 = sc2.text_frame
    tf_sc2.word_wrap = True
    tf_sc2.margin_left = tf_sc2.margin_right = Inches(0.2)
    tf_sc2.margin_top = Inches(0.18)

    psc2_0 = tf_sc2.paragraphs[0]
    rsc2_0 = psc2_0.add_run()
    rsc2_0.text = "QUALIFIED DOWNSTREAM INVARIANCE"
    rsc2_0.font.size = Pt(9.0)
    rsc2_0.font.bold = True
    rsc2_0.font.color.rgb = ACCENT_CYAN

    psc2_1 = tf_sc2.add_paragraph()
    psc2_1.space_before = Pt(2)
    rsc2_1 = psc2_1.add_run()
    rsc2_1.text = "110 MIN DELAY SAVED"
    rsc2_1.font.size = Pt(22)
    rsc2_1.font.bold = True
    rsc2_1.font.color.rgb = TEXT_WHITE

    psc2_2 = tf_sc2.add_paragraph()
    psc2_2.space_before = Pt(4)
    rsc2_2 = psc2_2.add_run()
    rsc2_2.text = "The 110-minute downstream lateness difference is invariant for nonnegative common clearance durations under specified fixed-source assignments, equal downstream duration, and unchanged resources."
    rsc2_2.font.size = Pt(8.5)
    rsc2_2.font.color.rgb = TEXT_MUTED

    # Bottom Qualification
    add_bottom_banner(slide5, "EVIDENCE INTEGRITY STANDARD: Result derived from a specified synthetic mathematical fixture (S-MATH-01); not a measured real-world dealership performance improvement.", is_qualification=True)

    # =========================================================================
    # SLIDE 6: DIFFERENTIATION, MVP AND IMPACT
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, 
               "Commercial Strategy & Proposed Implementation", 
               "From Parts Shortage to Feasible Service Recovery.", 
               "Proposed technical contribution and a disciplined single-rooftop roadmap for hackathon evaluation.", 
               6)

    # Left Column: 3 Proposed Differentiators
    card_diff = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.85), Inches(5.6), Inches(4.55))
    card_diff.fill.solid()
    card_diff.fill.fore_color.rgb = PANEL_BG
    card_diff.line.color.rgb = ACCENT_CYAN
    card_diff.line.width = Pt(1.2)
    tf_d = card_diff.text_frame
    tf_d.word_wrap = True
    tf_d.margin_left = tf_d.margin_right = Inches(0.25)
    tf_d.margin_top = Inches(0.2)

    pd0 = tf_d.paragraphs[0]
    rd0 = pd0.add_run()
    rd0.text = "THREE PROPOSED DIFFERENTIATORS"
    rd0.font.size = Pt(10)
    rd0.font.bold = True
    rd0.font.color.rgb = ACCENT_CYAN

    diffs = [
        ("1. Feasibility-Gated Joint Recovery", "Evaluates multi-channel parts sourcing alongside downstream workshop scheduling, avoiding the local cost traps of study-defined fixed-source baselines."),
        ("2. Modeled Physical Feasibility Gates", "Enforces modeled vehicle teardown states, technician verification sign-offs, bay exclusivity, and staging buffer limits before proposing a plan."),
        ("3. Explainable Copilot with Human Control", "Presents transparent trade-off rationale to the Service Advisor, requiring mandatory human sign-off and pre-execution state revalidation.")
    ]

    for d_title, d_desc in diffs:
        p = tf_d.add_paragraph()
        p.space_before = Pt(12)
        rt = p.add_run()
        rt.text = f"{d_title}\n"
        rt.font.size = Pt(10.5)
        rt.font.bold = True
        rt.font.color.rgb = TEXT_WHITE
        rd = p.add_run()
        rd.text = d_desc
        rd.font.size = Pt(9.0)
        rd.font.color.rgb = TEXT_MUTED

    # Right Column: 4-Phase MVP Roadmap
    card_road = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.85), Inches(5.733), Inches(4.55))
    card_road.fill.solid()
    card_road.fill.fore_color.rgb = PANEL_BG
    card_road.line.color.rgb = ACCENT_EMERALD
    card_road.line.width = Pt(1.2)
    tf_r = card_road.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_right = Inches(0.25)
    tf_r.margin_top = Inches(0.2)

    pr0 = tf_r.paragraphs[0]
    rr0 = pr0.add_run()
    rr0.text = "DISCIPLINED 4-PHASE MVP ROADMAP (PROPOSED)"
    rr0.font.size = Pt(10)
    rr0.font.bold = True
    rr0.font.color.rgb = ACCENT_EMERALD

    phases = [
        ("Phase 1: DMS Interface & Shop Digital Twin (Planned)", "Model read-only Tekion DMS data schemas for ROs, labor clock, parts inventory, and spatial shop assets."),
        ("Phase 2: Single-Rooftop CP-SAT Engine (Target)", "Implement Google OR-Tools multi-pass recovery solver; target: benchmark single-rooftop recovery scenarios and establish a measured runtime threshold."),
        ("Phase 3: Explainable Advisor UI & Revalidation (Proposed)", "Interactive recovery card with LLM-generated rationale summary, pre-execution revalidation checks, and advisor approval workflow."),
        ("Phase 4: Synthetic Benchmarking & Validation (Proposed)", "Proposed target: evaluate solver across 200 synthetic paired disruption seeds, followed by a simulated shadow evaluation.")
    ]

    for p_title, p_desc in phases:
        p = tf_r.add_paragraph()
        p.space_before = Pt(9)
        rt = p.add_run()
        rt.text = f"{p_title}\n"
        rt.font.size = Pt(10.0)
        rt.font.bold = True
        rt.font.color.rgb = TEXT_WHITE
        rd = p.add_run()
        rd.text = p_desc
        rd.font.size = Pt(8.8)
        rd.font.color.rgb = TEXT_MUTED

    add_bottom_banner(slide6, "THE WINNING PITCH: StallBreaker does not just find another part. It finds a feasible way to get the entire workshop moving again.")

    output_path = "submission/StallBreaker_TekQubit_2026_Final_Pitch.pptx"
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    create_deck()
