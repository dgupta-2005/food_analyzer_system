"""
Calibrated build script to generate exactly 18 pages for NutriVision IEEE 830 SRS Specification.
Covers all sections, user classes table, all 6 system features with REQ-x.x, non-functional requirements,
glossary, embedded UML diagrams in Appendix B, and TBD table in Appendix C.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=70, bottom=70, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def add_header_footer(doc, project_name="NutriVision"):
    for section in doc.sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(0.95)
        section.right_margin = Inches(0.95)
        
        # Header (Right aligned italicized)
        header = section.header
        header_p = header.paragraphs[0]
        header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        header_p.text = f"Software Requirements Specification for {project_name}"
        header_p.runs[0].font.name = "Arial"
        header_p.runs[0].font.size = Pt(8.5)
        header_p.runs[0].font.italic = True
        header_p.runs[0].font.color.rgb = RGBColor(100, 100, 100)
        
        # Footer (Center aligned page number)
        footer = section.footer
        footer_p = footer.paragraphs[0]
        footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_f = footer_p.add_run("Page ")
        run_f.font.name = "Arial"
        run_f.font.size = Pt(9)
        run_f.font.color.rgb = RGBColor(100, 100, 100)
        
        fldSimple = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
        footer_p._p.append(fldSimple)

def main():
    doc = Document()
    add_header_footer(doc, "NutriVision")
    
    # Base Style Adjustments
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Arial'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = RGBColor(20, 20, 20)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(3.5)
    
    def add_p(text, bold_prefix="", italic_prefix="", space_after=3.5, bullet=False):
        p = doc.add_paragraph(style='List Bullet' if bullet else 'Normal')
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.bold = True
            r_b.font.name = 'Arial'
        if italic_prefix:
            r_i = p.add_run(italic_prefix)
            r_i.italic = True
            r_i.font.name = 'Arial'
        if text:
            r_t = p.add_run(text)
            r_t.font.name = 'Arial'
        return p

    def add_h1(text, space_before=11, space_after=4):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Arial'
        run.font.size = Pt(15)
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_h2(text, space_before=8, space_after=3):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Arial'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_h3(text, space_before=5, space_after=2):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Arial'
        run.font.size = Pt(10.5)
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    # ==========================================
    # PAGE 1: COVER PAGE
    # ==========================================
    p_top = doc.add_paragraph()
    p_top.paragraph_format.space_before = Pt(120)
    p_top.paragraph_format.space_after = Pt(16)
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_top.add_run("Software Requirements Specification")
    r_title.bold = True
    r_title.font.size = Pt(26)
    r_title.font.name = 'Arial'
    
    p_for = doc.add_paragraph()
    p_for.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_for.paragraph_format.space_after = Pt(16)
    r_for = p_for.add_run("for")
    r_for.font.size = Pt(14)
    r_for.font.name = 'Arial'

    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_proj.paragraph_format.space_after = Pt(160)
    r_proj = p_proj.add_run("NutriVision – AI-Powered Dietary Intake & Packaged Food Analyzer System")
    r_proj.bold = True
    r_proj.font.size = Pt(18)
    r_proj.font.name = 'Arial'

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = Pt(6)
    r_v = p_meta.add_run("Version 1.0 approved\n\n")
    r_v.font.size = Pt(12)
    r_prep = p_meta.add_run("Prepared by <author>\n")
    r_prep.font.size = Pt(12)
    r_org = p_meta.add_run("<organization>\n")
    r_org.font.size = Pt(12)
    r_date = p_meta.add_run("<date created>\n")
    r_date.font.size = Pt(12)

    doc.add_page_break()

    # ==========================================
    # PAGE 2: TABLE OF CONTENTS & REVISION HISTORY
    # ==========================================
    p_toc_t = doc.add_paragraph()
    p_toc_t.paragraph_format.space_before = Pt(4)
    p_toc_t.paragraph_format.space_after = Pt(6)
    r_toc = p_toc_t.add_run("Table of Contents")
    r_toc.bold = True
    r_toc.font.size = Pt(16)
    
    toc_items = [
        ("Table of Contents", "ii"),
        ("Revision History", "ii"),
        ("1. Introduction", "1"),
        ("    1.1 Purpose", "1"),
        ("    1.2 Document Conventions", "1"),
        ("    1.3 Intended Audience and Reading Suggestions", "1"),
        ("    1.4 Product Scope", "2"),
        ("    1.5 References", "2"),
        ("2. Overall Description", "3"),
        ("    2.1 Product Perspective", "3"),
        ("    2.2 Product Functions", "3"),
        ("    2.3 User Classes and Characteristics", "3"),
        ("    2.4 Operating Environment", "4"),
        ("    2.5 Design and Implementation Constraints", "4"),
        ("    2.6 User Documentation", "4"),
        ("    2.7 Assumptions and Dependencies", "4"),
        ("3. External Interface Requirements", "5"),
        ("    3.1 User Interfaces", "5"),
        ("    3.2 Hardware Interfaces", "5"),
        ("    3.3 Software Interfaces", "5"),
        ("    3.4 Communications Interfaces", "5"),
        ("4. System Features", "6"),
        ("    4.1 Multimodal AI Meal Calorie & Macro Estimator (SVC-01)", "6"),
        ("    4.2 Packaged Food Barcode Scanning & OpenFoodFacts Registry Lookup (SVC-02)", "7"),
        ("    4.3 Side-by-Side Product Comparison Engine & Healthy Substitutes (SVC-03)", "8"),
        ("    4.4 Personalized AI Diet & Macro Allocation Planner (SVC-04)", "9"),
        ("    4.5 Meal Intake Logging & Historical Nutrient Analytics (SVC-05)", "10"),
        ("    4.6 User Authentication, Biometric Profiling & Telemetry Portal (SVC-06)", "11"),
        ("5. Other Nonfunctional Requirements", "12"),
        ("    5.1 Performance Requirements", "12"),
        ("    5.2 Safety Requirements", "12"),
        ("    5.3 Security Requirements", "12"),
        ("    5.4 Software Quality Attributes", "13"),
        ("    5.5 Business Rules", "13"),
        ("6. Other Requirements (Database, Legal, Compliance)", "13"),
        ("Appendix A: Glossary", "14"),
        ("Appendix B: Analysis Models (Use Case, Sequence & State Diagrams)", "15"),
        ("Appendix C: To Be Determined (TBD) List", "18"),
    ]
    
    for item, page_num in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_after = Pt(1.8)
        p_t.paragraph_format.line_spacing = 1.05
        p_t.add_run(item)
        p_t.add_run(" " + "." * max(2, int(84 - len(item) * 1.45)) + " ")
        r_pn = p_t.add_run(page_num)
        r_pn.bold = True

    p_rev_t = doc.add_paragraph()
    p_rev_t.paragraph_format.space_before = Pt(12)
    p_rev_t.paragraph_format.space_after = Pt(4)
    r_rev = p_rev_t.add_run("Revision History")
    r_rev.bold = True
    r_rev.font.size = Pt(13)

    rev_table = doc.add_table(rows=3, cols=4)
    rev_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    rev_headers = ["Name", "Date", "Reason For Changes", "Version"]
    for i, h in enumerate(rev_headers):
        cell = rev_table.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_shading(cell, "E0E0E0")
        set_cell_margins(cell, 60, 60, 80, 80)

    rev_data = [
        ("<author>", "<date created>", "Initial draft based on approved architecture & specifications", "1.0"),
        ("<author>", "<date created>", "Integrated black & white UML analysis models & calibrated 18-page layout", "1.1")
    ]
    for row_idx, data in enumerate(rev_data, start=1):
        for col_idx, text in enumerate(data):
            cell = rev_table.cell(row_idx, col_idx)
            cell.text = text
            set_cell_margins(cell, 50, 50, 80, 80)

    doc.add_page_break()

    # ==========================================
    # PAGE 3: 1. INTRODUCTION (1.1 - 1.3)
    # ==========================================
    add_h1("1. Introduction")
    
    add_h2("1.1 Purpose")
    add_p(
        "This document specifies the software requirements for Version 1.0 of NutriVision (FoodLens), an "
        "enterprise-grade, AI-powered food analysis and dietary management platform. It encompasses the end-to-end "
        "functional and non-functional requirements for the complete system: multimodal computer-vision meal estimation "
        "via Google Gemini AI, hardware-independent optical barcode decoding using OpenCV preprocessing, real-time "
        "product nutritional lookup against global databases (OpenFoodFacts API v2), statistical side-by-side product "
        "health comparisons, personalized macro/calorie diet planning, and transactional meal intake logging with async "
        "database persistence. This SRS serves as the authoritative, contractually binding baseline for system architecture, "
        "implementation, verification, and acceptance testing."
    )
    add_p(
        "The scope covers both the reactive single-page client interface (React 18 + Vite) and the high-concurrency "
        "asynchronous backend (FastAPI, Python 3.11+, SQLAlchemy 2.0 Async, ZXing-C++, and Google GenAI SDK). It is targeted "
        "for direct evaluation by software architects, quality assurance engineers, clinical nutrition consultants, and "
        "academic assessment panels."
    )

    add_h2("1.2 Document Conventions")
    add_p(
        "This document conforms strictly to the IEEE 830-1998 Standard for Software Requirements Specifications. The following "
        "typographical and formatting conventions are maintained throughout:"
    )
    add_p("Requirement Identifiers: Every functional requirement in Section 4 is tagged uniquely using the schema REQ-<FeatureNumber>.<RequirementNumber> (e.g., REQ-1.1, REQ-2.4). Each statement is concise, verifiable, and atomic.", bullet=True)
    add_p("Priority Classifications: System features and requirements are assigned priority levels of High (critical core path), Medium (important functional feature), or Low (enhancement/secondary service). Detailed requirements inherit the priority of their parent feature unless explicitly stated.", bullet=True)
    add_p("Technical & Domain Nomenclature: Specialized terms such as Nutri-Score, Basal Metabolic Rate (BMR), Total Daily Energy Expenditure (TDEE), Macronutrients, and ZXing are italicized upon initial introduction and formally defined in Appendix A (Glossary).", bullet=True)
    add_p("Placeholders: Unresolved parameterizations or calibration benchmarks are explicitly tagged as [TBD-x] and logged in Appendix C (To Be Determined List) for traceability.", bullet=True)

    add_h2("1.3 Intended Audience and Reading Suggestions")
    add_p(
        "This document is authored for multiple stakeholder groups, each with distinct informational requirements:"
    )
    add_p("Software Development Engineers: Focus on Section 2 (System Architecture), Section 3 (External Interfaces), Section 4 (System Features with stimulus/response sequences), and Appendix B (UML Analysis Models).", bullet=True)
    add_p("Quality Assurance & Test Engineers: Focus on Section 4 (Functional Requirements) and Section 5 (Nonfunctional Requirements) to formulate automated integration tests, boundary validations, and acceptance suites.", bullet=True)
    add_p("Clinical Dietitians & Domain Specialists: Review Section 1.4 (Product Scope), Section 4.1 (AI Meal Estimation), Section 4.4 (Diet Planning), and Section 5.2 (Safety & Disclaimers) to verify clinical integrity.", bullet=True)
    add_p("Project Evaluators & Academic Reviewers: Read sequentially from Section 1 through Section 6, with particular attention to Appendix B (UML Analysis Models) for software engineering rigor.", bullet=True)

    doc.add_page_break()

    # ==========================================
    # PAGE 4: 1.4 PRODUCT SCOPE & 1.5 REFERENCES
    # ==========================================
    add_h2("1.4 Product Scope")
    add_p(
        "Dietary indiscretion, excessive consumption of ultra-processed packaged foods, and inaccurate portion estimation are "
        "leading drivers of metabolic disorders globally. While existing commercial applications require tedious manual logging, "
        "text searching, and user guessing of weights and portion sizes, NutriVision establishes a cohesive, zero-friction dietary "
        "intelligence ecosystem. The system bridges consumer behavior with clinical precision by:"
    )
    add_p("Multimodal Vision AI Portion & Macro Estimation: Allowing consumers to snap a photo or input a natural language description of any prepared meal to receive instant, itemized estimates of calories, protein, carbohydrates, fats, and dish components via Google Gemini 2.5 Flash Vision models with automated fallback mechanisms.", bullet=True)
    add_p("Decoupled Barcode Scanning & Product Registry: Enabling optical barcode acquisition from camera uploads with automated image preprocessing (contrast enhancement, border padding, noise crop) decoded through ZXing-C++, querying over 3 million verified packaged goods in the OpenFoodFacts database.", bullet=True)
    add_p("Statistical Product Comparison & Smart Substitutions: Delivering side-by-side analytical comparisons that calculate percentage calorie reductions, sugar deltas, sodium drops, and Nutri-Score differentials (Grades A through E), guiding users toward healthier packaged alternatives and saving them to personal collections.", bullet=True)
    add_p("Intelligent Personalized Diet Planning: Analyzing historical 30-day user intake telemetry alongside biometric metrics (weight, height, age, activity multiplier, dietary preferences) to automatically compute customized daily caloric deficits/surpluses and meal distribution slots.", bullet=True)
    add_p("Historical Intake Analytics & Progress Telemetry: Persisting granular meal components, timestamps, and image assets to an asynchronous relational database, feeding real-time visual progress rings and macro bars.", bullet=True)

    add_h2("1.5 References")
    references = [
        "[1] IEEE Computer Society, 'IEEE Recommended Practice for Software Requirements Specifications', IEEE Std 830-1998, 1998.",
        "[2] Google DeepMind, 'Gemini 1.5 & 2.5 Technical Report: Multimodal Reasoning and Portion Estimation Capabilities', Google AI Research, 2024.",
        "[3] OpenFoodFacts Community, 'OpenFoodFacts API v2 Documentation: JSON Schema & Nutriments Mapping', World OpenFoodFacts Organization, 2024.",
        "[4] Santé Publique France, 'Nutri-Score Scientific Rationale and Grading Algorithm: Calculation of Nutritional Quality Index', Ministry of Health, France, 2023.",
        "[5] M. D. Mifflin, S. T. St Jeor, et al., 'A new predictive equation for resting energy expenditure in healthy individuals', The American Journal of Clinical Nutrition, vol. 51, no. 2, pp. 241-247, 1990.",
        "[6] ZXing-C++ Project, 'High-Performance 1D/2D Barcode Scanning Library in Modern C++', GitHub Open Source Repository, 2024.",
        "[7] FastAPI Framework, 'FastAPI Documentation: High-performance Asynchronous Web Framework for Python', Tiangolo, 2024.",
        "[8] SQLAlchemy Project, 'SQLAlchemy 2.0 Unified Async IO and ORM Architecture', Python Software Foundation, 2024.",
        "[9] React Core Team, 'React 18 Single-Page Application Design Patterns and Context API State Management', Meta Open Source, 2023.",
        "[10] World Health Organization, 'Global Guidelines on Healthy Diet, Macronutrient Distribution and Noncommunicable Disease Prevention', WHO Guidelines Approved by the Guidelines Review Committee, Geneva, 2023.",
        "[11] Food Safety and Standards Authority of India (FSSAI), 'Food Safety and Standards (Labelling and Display) Regulations', Gazette of India, 2020.",
        "[12] U.S. Food and Drug Administration (FDA), 'Guidance for Industry: Nutrition Labeling and Serving Size Determinations', HHS, 2022.",
        "[13] Pydantic Development Team, 'Pydantic V2: Data Validation and Settings Management Using Python Type Annotations', 2024.",
        "[14] RFC 7519, 'JSON Web Token (JWT) Architecture and Security Best Practices', Internet Engineering Task Force (IETF), 2015."
    ]
    for ref in references:
        add_p(ref, space_after=2.5)

    doc.add_page_break()

    # ==========================================
    # PAGE 5: 2. OVERALL DESCRIPTION (2.1 - 2.3)
    # ==========================================
    add_h1("2. Overall Description")

    add_h2("2.1 Product Perspective")
    add_p(
        "NutriVision is an autonomous, self-contained web platform architected around a modern microservice-inspired "
        "decoupled stack. The application replaces disparate, manual nutrition calculation tools with a unified digital "
        "health suite. The core components of the system environment comprise:"
    )
    add_p("Client Single-Page Application (SPA): Implemented with React 18, Vite build tooling, and modular Vanilla CSS. Employs React Context API (AuthContext) for reactive state propagation and Axios (apiClient) for asynchronous REST communication.", bullet=True)
    add_p("High-Throughput Asynchronous REST Server: Implemented with FastAPI (Python 3.11+), utilizing ASGI uvicorn workers, Pydantic v2 schemas for bidirectional validation, and CORS middleware configured for cross-origin security.", bullet=True)
    add_p("Multimodal AI Vision Integration: Employs the google-genai SDK communicating directly with Gemini 2.5 Flash and Gemini 1.5 Flash endpoints with structured JSON schema output validation and automated fallback loops.", bullet=True)
    add_p("Optical Barcode Decoding Subsystem: Integrates OpenCV (cv2) for image border padding, noise crop, and threshold preprocessing paired with zxingcpp for low-latency barcode extraction from consumer camera captures.", bullet=True)
    add_p("Global Food Data Ingestion Gateway: Connects via asynchronous HTTP client (httpx) to the OpenFoodFacts API v2 for on-demand nutritional facts retrieval, serving size normalization, and Nutri-Score calculation.", bullet=True)
    add_p("Asynchronous Persistence Layer: Powered by SQLAlchemy 2.0 with aiosqlite / asyncpg drivers communicating with an SQLite / PostgreSQL database executing migrations via Alembic.", bullet=True)

    add_h2("2.2 Product Functions")
    add_p("At a functional level, the system empowers users and administrators to execute six primary software services:")
    add_p("SVC-01 (AI Meal Calorie & Macro Estimator): Uploads prepared meal photographs or natural language dish descriptions, invoking Gemini Vision AI with structured JSON formatting to extract total calories, proteins, carbohydrates, fats, and confidence ratings, with one-click database logging.", bullet=True)
    add_p("SVC-02 (Packaged Food Barcode Scanner & Search): Scans 1D EAN/UPC product barcodes or executes text queries against OpenFoodFacts API, retrieving verified product titles, brands, packaging images, 100g nutritional breakdowns, and Nutri-Score grades.", bullet=True)
    add_p("SVC-03 (Side-by-Side Product Comparison Engine): Generates statistical comparisons between any two packaged food items, calculating exact calorie percentage deltas, sugar reductions, and sodium differentials, with one-click saving of healthy alternatives to user collections.", bullet=True)
    add_p("SVC-04 (Personalized Diet & Macro Planner): Synthesizes historical meal intake with user biometrics (BMR/TDEE calculations via Mifflin-St Jeor formulas) to allocate target caloric distribution across breakfast, lunch, dinner, and snacks with tailored dish suggestions.", bullet=True)
    add_p("SVC-05 (Meal History & Intake Database Manager): Records complete itemized nutrient breakdowns linked to user profiles, supporting chronologically sorted queries, daily progress totals, and macro progress bars.", bullet=True)
    add_p("SVC-06 (Enterprise Telemetry & Interactive API Portal): Exposes live system health checks, connected AI model status, database metrics, and interactive OpenAPI/Swagger testing suites (/docs).", bullet=True)

    add_h2("2.3 User Classes and Characteristics")
    add_p("NutriVision serves five distinct user classes differentiated by privilege levels, goals, and technical expertise:")
    
    uc_table = doc.add_table(rows=6, cols=4)
    uc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    uc_headers = ["User Class", "Privilege Level", "Technical Expertise", "Primary Motivation & System Usage"]
    for i, h in enumerate(uc_headers):
        cell = uc_table.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        set_cell_shading(cell, "E0E0E0")
        set_cell_margins(cell, 60, 60, 80, 80)

    uc_data = [
        ("Registered Consumer (Primary User)", "Standard Authenticated (JWT)", "Low to Moderate", "Logs daily meals via photo/text, tracks calories against BMR/TDEE targets, scans packaged snacks to avoid unhealthy sugars."),
        ("Guest / Visitor", "Unauthenticated Public", "Low", "Accesses authentication portal, views feature catalog, reviews security disclaimers, and initiates self-registration."),
        ("Clinical Nutritionist / Dietitian", "Verified Specialist", "Moderate", "Inspects historical intake logs for patients, verifies macro accuracy, and formulates calibrated diet plans."),
        ("System Administrator / IT Developer", "Full Administrative", "High", "Monitors API uptime, inspects Gemini token consumption, executes database migrations, and validates OpenAPI endpoints."),
        ("Client Application (System Actor)", "API Key / Service Token", "Automated Programmatic", "Headless automated requests querying barcode resolutions or feeding meal logs via REST API.")
    ]
    for r_idx, row in enumerate(uc_data, start=1):
        for c_idx, val in enumerate(row):
            cell = uc_table.cell(r_idx, c_idx)
            cell.text = val
            set_cell_margins(cell, 45, 45, 60, 60)

    doc.add_page_break()

    # ==========================================
    # PAGE 6: 2.4 OPERATING ENV - 2.7 ASSUMPTIONS
    # ==========================================
    add_h2("2.4 Operating Environment")
    add_p(
        "NutriVision operates in a containerized and cloud-ready multi-tier web environment. The operational specifications "
        "for the respective tiers include:"
    )
    add_p("Server Operating System: Linux (Ubuntu 22.04 LTS / Debian 12) or Windows 10/11 64-bit with WSL2 support.", bullet=True)
    add_p("Backend Runtime & Libraries: Python 3.11+, FastAPI 0.110+, Uvicorn 0.28+, SQLAlchemy 2.0+ (asyncio), Pydantic v2.6+, OpenCV-Python-Headless 4.9+, zxing-cpp 2.2+, httpx 0.27+, google-genai 0.1+.", bullet=True)
    add_p("Client Operating Environment: Modern evergreen web browsers (Google Chrome 115+, Mozilla Firefox 118+, Microsoft Edge 115+, Apple Safari 16+) with ECMAScript 2022 and HTML5 Camera / Canvas API support.", bullet=True)
    add_p("Relational Database: SQLite 3.39+ with WAL (Write-Ahead Logging) enabled for development, PostgreSQL 15+ for high-concurrency production deployments.", bullet=True)
    add_p("External Network Interfaces: Outbound HTTPS (TCP Port 443) access to https://generativelanguage.googleapis.com (Gemini API) and https://world.openfoodfacts.org (OpenFoodFacts API v2).", bullet=True)

    add_h2("2.5 Design and Implementation Constraints")
    add_p("The design and implementation of NutriVision are governed by several binding architectural constraints:")
    add_p("Stateless REST Architecture: The FastAPI application server must maintain zero server-side session affinity; all user state is verified via cryptographically signed JSON Web Tokens (JWT) passed in HTTP Authorization headers.", bullet=True)
    add_p("Strict Multimodal AI Fallback Loop: Because upstream multimodal vision endpoints may experience transient rate limiting or model depreciation, the backend GeminiService must enforce a deterministic fallback hierarchy (gemini-2.5-flash -> gemini-1.5-flash -> gemini-2.0-flash) with structured Pydantic schema validation.", bullet=True)
    add_p("Optical Barcode Noise Robustness: Smartphone cameras frequently generate blurred, low-contrast, or unevenly cropped barcode images. The system must apply OpenCV preprocessing (cropping quiet noise borders and padding 40px pure white margins) prior to secondary decoding passes.", bullet=True)
    add_p("Nutrition Label Data Standardization: External databases represent nutritional data in variable formats (per portion, per 100g, per 100ml). All packaged food entities must be rigorously normalized to standard 100g metric baselines.", bullet=True)
    add_p("Zero Third-Party Image Persistence: To safeguard user privacy and comply with data minimization principles, temporary dish photos uploaded for calorie estimation are purged or strictly sandboxed within the host upload directory.", bullet=True)

    add_h2("2.6 User Documentation")
    add_p(
        "The project deliverables include comprehensive documentation packages: (1) An interactive web-based Swagger UI "
        "and ReDoc documentation suite hosted at /docs and /redoc; (2) An end-user operating manual detailing meal photo "
        "framing guidelines, barcode scanning tips, and diet profile configuration; (3) A developer deployment manual with "
        "Docker Compose instructions and environment variable configuration guides (.env.example); and (4) In-app contextual "
        "tooltips across dashboard metrics."
    )

    add_h2("2.7 Assumptions and Dependencies")
    add_p("The system requirements are formulated upon the following validated assumptions:")
    add_p("API Availability: Google Gemini API and OpenFoodFacts API maintain an operational uptime of >= 99.5%.", bullet=True)
    add_p("Image Quality: User-uploaded meal images possess adequate ambient illumination and focus to allow visual discrimination of food components by multimodal vision models.", bullet=True)
    add_p("Database Schema Stability: Relational data structures managed via Alembic database migrations preserve backward compatibility across Version 1.x releases.", bullet=True)
    add_p("Client Connectivity: End users possess an active internet connection capable of transmitting 2MB-5MB image payloads within standard HTTP request timeout thresholds (10.0 seconds).", bullet=True)

    doc.add_page_break()

    # ==========================================
    # PAGE 7: 3. EXTERNAL INTERFACE REQUIREMENTS
    # ==========================================
    add_h1("3. External Interface Requirements")

    add_h2("3.1 User Interfaces")
    add_p(
        "NutriVision features an enterprise-grade, high-contrast, responsive user interface built using modern React 18 single-page "
        "architecture. The layout conforms to strict human-computer interaction (HCI) standards with consistent typography, intuitive "
        "spatial hierarchy, and reactive feedback loops. The visual interface is partitioned into seven core screen modules:"
    )
    add_p("Global Application Shell: Incorporates a persistent top Header featuring real-time daily calorie consumption counters against calculated BMR targets, user authentication state badges, and dynamic profile trigger buttons. A collapsible left Sidebar provides instant navigation across all core application domains.", bullet=True)
    add_p("Executive Health Dashboard: Displays real-time macro progress rings (Protein, Carbohydrates, Fats), target vs. consumed energy metrics, quick-action navigation tiles, and a list of the most recent logged meals with thumbnail previews.", bullet=True)
    add_p("AI Meal Calorie Estimator Workspace: Features a drag-and-drop image dropzone with live client-side preview, an optional dish description text area, asynchronous loading animations during Gemini inference, and an itemized nutrient table displaying dish components, calories, protein, carbs, fats, and confidence scores with one-click 'Log Meal' persistence.", bullet=True)
    add_p("Packaged Food Barcode Scanning Hub: Provides dual-mode input: direct high-speed optical barcode image upload decoded via ZXing-C++, and an instant live search input querying OpenFoodFacts with 400ms debounced auto-complete dropdowns.", bullet=True)
    add_p("Side-by-Side Product Comparison Studio: Offers dual-column layout displaying high-resolution product imagery, calorie deltas, sugar percentage differences, sodium comparisons, Nutri-Score color badges (A through E), and one-click 'Save Alternative' buttons.", bullet=True)
    add_p("AI Personalized Diet Planner: Displays computed BMR/TDEE targets, primary fitness goals (Weight Loss, Muscle Gain, Maintenance), dietary preferences (Vegan, Keto, Vegetarian), and custom daily meal slots (Breakfast, Lunch, Dinner, Snack) with caloric quotas and suggested dishes.", bullet=True)
    add_p("Meal History & Analytics Explorer: Displays a chronologically indexed ledger of all historical meals, date range filters, granular component breakdowns, and total daily macronutrient summaries.", bullet=True)

    add_h2("3.2 Hardware Interfaces")
    add_p(
        "NutriVision requires no proprietary or dedicated physical hardware. It operates seamlessly across commodity consumer "
        "and server hardware: (1) Client Devices: Desktops, laptops, tablets, and smartphones equipped with standard RGB cameras "
        "(minimum 720p resolution); (2) Input Peripherals: Touchscreens, mice, keyboards, and optical barcode hand scanners; "
        "(3) Host Server: Commodity x86_64 or ARM64 multi-core processors (minimum 2 vCPUs, 4GB RAM) capable of executing asynchronous I/O."
    )

    add_h2("3.3 Software Interfaces")
    add_p("The software stack interfaces with multiple external and host-level software subsystems:")
    add_p("Google Gemini Vision API: Interfaced via google.genai.Client utilizing types.GenerateContentConfig with response_mime_type set to 'application/json' and structured Pydantic schema validation. Communicates with gemini-2.5-flash and gemini-1.5-flash.", bullet=True)
    add_p("OpenFoodFacts World Database API v2: Interfaced via asynchronous HTTP client (httpx) targeting https://world.openfoodfacts.org/api/v2/product/{barcode}.json and https://world.openfoodfacts.org/cgi/search.pl with custom User-Agent identifiers.", bullet=True)
    add_p("ZXing-C++ Optical Engine: C++ barcode scanning bindings (zxingcpp.read_barcodes) integrated into Python runtime for decoding 1D EAN-13, EAN-8, UPC-A, and UPC-E codes directly from OpenCV numpy matrices.", bullet=True)
    add_p("OpenCV Computer Vision Engine: cv2 runtime utilized for image loading, grayscale conversions, boundary crops, and copyMakeBorder padding.", bullet=True)
    add_p("SQLAlchemy 2.0 Async ORM: Communicates with SQLite database engine via async_engine with aiosqlite driver, enforcing foreign keys, cascade deletes, and relationship joins.", bullet=True)

    add_h2("3.4 Communications Interfaces")
    add_p(
        "All network communications adhere strictly to modern web and transport security protocols: (1) Transport Layer Security: "
        "Strictly encrypted using TLS 1.2 or TLS 1.3; (2) RESTful API Protocol: Endpoints communicate over HTTPS utilizing standard "
        "HTTP verbs (GET, POST, PUT, DELETE) transmitting and receiving application/json payloads; (3) Multipart Form Transmission: "
        "Meal photographs and barcode images are ingested via multipart/form-data with maximum payload limits of 10MB per upload; "
        "(4) CORS: Backend middleware enforces secure CORS headers allowing verified frontend origins."
    )

    doc.add_page_break()

    # ==========================================
    # PAGE 8: 4. SYSTEM FEATURES (4.1 SVC-01)
    # ==========================================
    add_h1("4. System Features")

    add_h2("4.1 Multimodal AI Meal Calorie & Macro Estimator (SVC-01)")
    add_h3("4.1.1 Description and Priority")
    add_p(
        "Enables users to submit prepared meal photographs and/or natural language dish descriptions to obtain an instant, "
        "accurate nutritional breakdown generated by Google Gemini Multimodal Vision AI. The service parses portion sizes, "
        "calculates total calories, estimates grams of protein, carbohydrates, and fats, extracts individual dish components, "
        "and assigns a statistical confidence score. Priority: High (Core Value Proposition)."
    )
    add_h3("4.1.2 Stimulus/Response Sequences")
    add_p("User selects or captures a dish photograph and optionally inputs portion context (e.g., '1 cup brown rice and grilled chicken') -> System displays local image preview and enables the analyze button.", bullet=True)
    add_p("User clicks 'Analyze Meal' -> Frontend transmits multipart form data to POST /api/v1/meals/estimate.", bullet=True)
    add_p("FastAPI backend validates file format, saves temporary image via StorageService, and invokes GeminiService.", bullet=True)
    add_p("GeminiService queries Gemini 2.5 Flash with structured JSON schema; if an API exception occurs, it automatically falls back to Gemini 1.5 Flash.", bullet=True)
    add_p("Backend receives structured JSON, validates it against AIStructuredMealResponse Pydantic schema, and returns HTTP 200.", bullet=True)
    add_p("Frontend renders the nutrient breakdown card, confidence badge, and itemized component table.", bullet=True)
    add_p("User clicks 'Log Meal to History' -> Frontend sends POST /api/v1/meals/log -> Backend persists meal log and linked items to SQLite -> UI displays success toast and updates daily calorie total.", bullet=True)

    add_h3("4.1.3 Functional Requirements")
    add_p("REQ-1.1: The system shall accept image uploads in JPEG, PNG, WEBP, and HEIC formats up to 10MB in size.", bullet=True)
    add_p("REQ-1.2: The system shall allow optional text descriptions to accompany image uploads or serve as standalone prompts.", bullet=True)
    add_p("REQ-1.3: The system shall query Google Gemini Multimodal models using a clinical dietitian system prompt instructing portion estimation and macro quantification.", bullet=True)
    add_p("REQ-1.4: The system shall enforce response schema conformance using Pydantic DTOs comprising dish summary, total calories, protein_g, carbs_g, fat_g, confidence score (0.0 to 1.0), and component items.", bullet=True)
    add_p("REQ-1.5: The system shall implement an automated fallback hierarchy: gemini-2.5-flash -> gemini-1.5-flash -> gemini-2.0-flash upon upstream error.", bullet=True)
    add_p("REQ-1.6: The system shall provide an endpoint POST /api/v1/meals/log to persist verified estimation results to the MealLog and MealItem database tables.", bullet=True)
    add_p("REQ-1.7: The system shall reject unsupported file types with an HTTP 400 Bad Request error.", bullet=True)
    add_p("REQ-1.8: The system shall handle upstream AI model timeouts within 15 seconds, returning an informative HTTP 504 Gateway Timeout error.", bullet=True)

    doc.add_page_break()

    # ==========================================
    # PAGE 9: 4.2 SVC-02 BARCODE SCANNER
    # ==========================================
    add_h2("4.2 Packaged Food Barcode Scanning & OpenFoodFacts Registry Lookup (SVC-02)")
    add_h3("4.2.1 Description and Priority")
    add_p(
        "Provides optical barcode scanning from user images and direct alphanumeric querying against the global OpenFoodFacts "
        "database. Retrieves comprehensive brand information, product packaging photos, standardized 100g nutritional facts, "
        "and official Nutri-Score grades (A, B, C, D, E). Priority: High."
    )
    add_h3("4.2.2 Stimulus/Response Sequences")
    add_p("User captures/uploads an image containing a product barcode -> Frontend sends file to POST /api/v1/food/scan-barcode.", bullet=True)
    add_p("Backend executes direct zxingcpp detection; if no barcode is found, it crops quiet noise and pads a 40px border using OpenCV, re-executing detection.", bullet=True)
    add_p("System extracts barcode string and queries OpenFoodFacts API v2.", bullet=True)
    add_p("System normalizes JSON nutriments into ProductNutritionSchema and returns HTTP 200.", bullet=True)
    add_p("User enters product name in search bar -> Frontend debounces query by 400ms and calls GET /api/v1/food/search -> Backend returns list of matching items with Nutri-Scores.", bullet=True)

    add_h3("4.2.3 Functional Requirements")
    add_p("REQ-2.1: The system shall decode standard 1D barcodes including EAN-13, EAN-8, UPC-A, and UPC-E from uploaded images.", bullet=True)
    add_p("REQ-2.2: The system shall apply OpenCV border padding and quiet-zone filtering as an automated fallback when initial barcode decoding yields zero results.", bullet=True)
    add_p("REQ-2.3: The system shall query OpenFoodFacts API v2 asynchronously using httpx with custom User-Agent headers.", bullet=True)
    add_p("REQ-2.4: The system shall extract and normalize product name, brand, category, front image URL, serving size, calories (kcal), protein (g), carbohydrates (g), fat (g), sugar (g), sodium (mg), and Nutri-Score grade.", bullet=True)
    add_p("REQ-2.5: The system shall provide an endpoint GET /api/v1/food/lookup/{barcode} for direct numeric barcode queries.", bullet=True)
    add_p("REQ-2.6: The system shall provide an endpoint GET /api/v1/food/search?query={text} returning up to 10 matching products.", bullet=True)
    add_p("REQ-2.7: If a product is not cataloged in OpenFoodFacts, the system shall return an HTTP 404 with an appropriate diagnostic message.", bullet=True)
    add_p("REQ-2.8: The system shall cache recently resolved barcode entities in memory/database to eliminate redundant external network requests.", bullet=True)

    doc.add_page_break()

    # ==========================================
    # PAGE 10: 4.3 SVC-03 PRODUCT COMPARISON
    # ==========================================
    add_h2("4.3 Side-by-Side Product Comparison Engine & Healthy Substitutes (SVC-03)")
    add_h3("4.3.1 Description and Priority")
    add_p(
        "Performs statistical and nutritional benchmarking between any two selected packaged food products. Computes exact "
        "percentage differences in caloric density, sugar content, protein ratio, and Nutri-Score improvements, presenting "
        "visual health verdicts and enabling users to bookmark healthier alternatives. Priority: High."
    )
    add_h3("4.3.2 Stimulus/Response Sequences")
    add_p("User selects an original product (e.g., standard potato chips) and an alternative product (e.g., baked oat chips) -> System calls POST /api/v1/food/compare.", bullet=True)
    add_p("ComparisonService calculates absolute deltas, percentage calorie reduction, and sugar delta.", bullet=True)
    add_p("System generates an automated health verdict ('Significantly Healthier Alternative: -35% Calories, -75% Sugar').", bullet=True)
    add_p("User clicks 'Save Healthy Alternative' -> System sends POST /api/v1/collections/save -> Backend saves mapping in UserCollection database.", bullet=True)

    add_h3("4.3.3 Functional Requirements")
    add_p("REQ-3.1: The system shall accept two ProductNutritionSchema payloads representing the target product and the comparison alternative.", bullet=True)
    add_p("REQ-3.2: The system shall calculate percentage calorie reduction using the formula: ((Original Calories - Alternative Calories) / Original Calories) * 100.", bullet=True)
    add_p("REQ-3.3: The system shall compute absolute deltas for protein, carbohydrates, fats, sugars, and sodium per 100g.", bullet=True)
    add_p("REQ-3.4: The system shall compare Nutri-Score alphabetical ranks (A > B > C > D > E) and flag positive nutritional transitions.", bullet=True)
    add_p("REQ-3.5: The system shall generate a synthesized summary verdict highlighting key nutritional trade-offs.", bullet=True)
    add_p("REQ-3.6: The system shall provide an endpoint POST /api/v1/collections/save allowing users to persist healthy alternative products.", bullet=True)
    add_p("REQ-3.7: The system shall provide an endpoint GET /api/v1/collections/user/{user_id} retrieving saved products with item metadata.", bullet=True)
    add_p("REQ-3.8: The system shall allow users to delete saved alternatives via DELETE /api/v1/collections/{id}.", bullet=True)

    doc.add_page_break()

    # ==========================================
    # PAGE 11: 4.4 SVC-04 DIET PLANNER
    # ==========================================
    add_h2("4.4 Personalized AI Diet & Macro Allocation Planner (SVC-04)")
    add_h3("4.4.1 Description and Priority")
    add_p(
        "Synthesizes user biometric data (age, gender, weight, height, activity level, fitness goals) and historical meal logs "
        "to calculate target Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE). Generates structured daily meal "
        "distribution slots with allocated caloric budgets and tailored dish recommendations. Priority: Medium."
    )
    add_h3("4.4.2 Stimulus/Response Sequences")
    add_p("User navigates to Diet Planner tab -> System calls GET /api/v1/recommendations/meal-plan/{user_id}.", bullet=True)
    add_p("Backend loads UserProfile and queries the last 30 historical MealLog entries via SQLAlchemy selectinload.", bullet=True)
    add_p("RecommendationService calculates daily energy targets based on user's primary goal (Weight Loss: -20% deficit, Muscle Gain: +15% surplus, Maintenance: equilibrium).", bullet=True)
    add_p("System constructs daily meal slots (Breakfast: 25%, Lunch: 35%, Dinner: 25%, Snack: 15% of total calories).", bullet=True)
    add_p("Frontend renders the interactive diet plan with macro targets and recommended meal cards.", bullet=True)

    add_h3("4.4.3 Functional Requirements")
    add_p("REQ-4.1: The system shall compute BMR using the Mifflin-St Jeor equation based on gender, weight, height, and age.", bullet=True)
    add_p("REQ-4.2: The system shall calculate TDEE by multiplying BMR with physical activity factors (Sedentary: 1.2, Moderately Active: 1.55, Extremely Active: 1.9).", bullet=True)
    add_p("REQ-4.3: The system shall adjust target daily calories based on user fitness goal: weight_loss (-500 kcal/day), muscle_gain (+350 kcal/day), maintenance (0 delta).", bullet=True)
    add_p("REQ-4.4: The system shall partition daily calories into structured meal slots: Breakfast, Lunch, Dinner, and Afternoon Snack.", bullet=True)
    add_p("REQ-4.5: The system shall compute recommended macro distributions (Protein: 25-35%, Carbs: 45-55%, Fat: 20-30% of energy intake).", bullet=True)
    add_p("REQ-4.6: The system shall inspect historical meal logs to exclude dishes that the user has historically logged with adverse or low-confidence ratings.", bullet=True)
    add_p("REQ-4.7: The system shall respect dietary preference filters including vegan, vegetarian, keto, and gluten-free.", bullet=True)
    add_p("REQ-4.8: The system shall format meal plan outputs into MealPlanResponse DTOs containing title, target calories, slots, and suggested dishes.", bullet=True)

    doc.add_page_break()

    # ==========================================
    # PAGE 12: 4.5 SVC-05 MEAL LOGS
    # ==========================================
    add_h2("4.5 Meal Intake Logging & Historical Nutrient Analytics (SVC-05)")
    add_h3("4.5.1 Description and Priority")
    add_p(
        "Persists user meal intake sessions into relational database storage with atomic integrity. Maintains granular "
        "component associations, logged timestamps, portion metadata, and image references, feeding real-time historical "
        "analytics and daily progress metrics. Priority: High."
    )
    add_h3("4.5.2 Stimulus/Response Sequences")
    add_p("User confirms estimated meal on frontend -> Frontend submits POST /api/v1/meals/log.", bullet=True)
    add_p("FastAPI opens an async transaction with the database session, creates a MealLog record, and attaches related MealItem entities.", bullet=True)
    add_p("Transaction commits atomically, and backend returns the serialized MealLogResponse.", bullet=True)
    add_p("Frontend triggers global state refresh, updating the Header daily calorie ring and history tab.", bullet=True)
    add_p("User opens Meal History tab -> Frontend calls GET /api/v1/meals/history/{user_id} -> Backend returns chronologically descending meal list.", bullet=True)

    add_h3("4.5.3 Functional Requirements")
    add_p("REQ-5.1: The system shall persist meal intake records into the MealLog table with user_id, meal_name, total_calories, total_protein, total_carbs, total_fat, confidence, and timestamp.", bullet=True)
    add_p("REQ-5.2: The system shall persist component items into the MealItem table with item_name, estimated_weight_g, calories, and macros, linked via foreign key to MealLog.", bullet=True)
    add_p("REQ-5.3: The system shall provide an endpoint GET /api/v1/meals/history/{user_id} returning the user's complete logged meal history with eager-loaded items.", bullet=True)
    add_p("REQ-5.4: The system shall provide an endpoint DELETE /api/v1/meals/log/{meal_id} allowing users to remove accidental or incorrect meal entries.", bullet=True)
    add_p("REQ-5.5: The system shall compute aggregate daily consumption totals for calories, protein, carbs, and fats.", bullet=True)
    add_p("REQ-5.6: The system shall store image file paths linking persisted meal logs to their source upload files.", bullet=True)
    add_p("REQ-5.7: Database insertions shall be atomic; if component item insertion fails, the parent meal log transaction shall be rolled back.", bullet=True)
    add_p("REQ-5.8: The system shall enforce database indexes on user_id and logged_at timestamps to maintain sub-50ms query latency under load.", bullet=True)

    doc.add_page_break()

    # ==========================================
    # PAGE 13: 4.6 SVC-06 AUTH & 5.1 - 5.2 NON-FUNCTIONAL
    # ==========================================
    add_h2("4.6 User Authentication, Biometric Profiling & Telemetry Portal (SVC-06)")
    add_h3("4.6.1 Description and Priority")
    add_p(
        "Manages user identity, registration, JWT token generation, encrypted password validation, biometric health profiles, "
        "and administrative system diagnostics. Exposes interactive OpenAPI/Swagger portals for live service inspection. Priority: High."
    )
    add_h3("4.6.2 Stimulus/Response Sequences")
    add_p("Visitor submits registration form -> Backend hashes password with bcrypt, stores user, and returns JWT token.", bullet=True)
    add_p("User logs in -> Backend verifies password hash and returns access token with 24-hour expiration.", bullet=True)
    add_p("User opens Profile Settings -> System fetches UserProfile via GET /api/v1/auth/profile/{user_id}.", bullet=True)
    add_p("User updates weight or fitness goal -> System saves updates via PUT /api/v1/auth/profile/{user_id} and recalculates macro targets.", bullet=True)
    add_p("Administrator opens Service Overview -> System displays live service uptime, Gemini engine status, and database log count.", bullet=True)

    add_h3("4.6.3 Functional Requirements")
    add_p("REQ-6.1: The system shall support user registration and authentication using cryptographically salted password hashes.", bullet=True)
    add_p("REQ-6.2: The system shall issue signed JSON Web Tokens (JWT) containing user_id, email, and expiration claims.", bullet=True)
    add_p("REQ-6.3: The system shall manage UserProfile entities storing age, gender, weight_kg, height_cm, activity_level, primary_goal, and dietary_preferences.", bullet=True)
    add_p("REQ-6.4: The system shall recalculate target daily calories and macro quotas whenever user profile metrics are updated.", bullet=True)
    add_p("REQ-6.5: The system shall host automated OpenAPI v3 documentation accessible at /docs (Swagger UI) and /redoc (ReDoc).", bullet=True)
    add_p("REQ-6.6: The system shall expose a health check endpoint GET / returning server status, project version, and service name.", bullet=True)
    add_p("REQ-6.7: The system shall enforce client session logout by clearing client-side token storage.", bullet=True)
    add_p("REQ-6.8: The system shall protect sensitive user profile endpoints via JWT bearer authorization headers.", bullet=True)

    add_h1("5. Other Nonfunctional Requirements")

    add_h2("5.1 Performance Requirements")
    add_p("AI Meal Estimation Latency: Round-trip response time for multimodal meal image estimation shall not exceed 5.0 seconds under normal network conditions (target <= 3.2s).", bullet=True)
    add_p("Optical Barcode Decoding Speed: Local OpenCV image preprocessing and ZXing-C++ barcode extraction shall execute within 450 milliseconds per image on standard server CPU hardware.", bullet=True)
    add_p("OpenFoodFacts Query Latency: Barcode lookups against OpenFoodFacts API shall complete within 1.5 seconds, with client-side timeout thresholds set to 10.0 seconds.", bullet=True)
    add_p("Database Query Execution: Standard relational database read and write operations (meal log commits, history queries, profile lookups) shall complete in less than 50 milliseconds.", bullet=True)

    add_h2("5.2 Safety Requirements")
    add_p("Clinical Decision Disclaimer: All estimations and recommendations represent informational estimates and do not constitute clinical or medical advice. The UI shall visibly display a mandatory health disclaimer on all estimation and planner screens.", bullet=True)
    add_p("Caloric Floor Safeguards: The automated diet planner shall strictly prevent calculating target daily caloric allocations below medically established minimum thresholds (1,200 kcal/day for females, 1,500 kcal/day for males).", bullet=True)

    doc.add_page_break()

    # ==========================================
    # PAGE 14: 5.3 - 5.5 NON-FUNC & 6. OTHER REQS
    # ==========================================
    add_h2("5.3 Security Requirements")
    add_p("Password Cryptography: User passwords shall never be stored in plaintext; all credentials shall be salted and hashed using bcrypt with an adaptive cost factor >= 12.", bullet=True)
    add_p("Token Authentication: All protected API endpoints shall validate JSON Web Tokens (JWT) signed with HMAC-SHA256 and verified using a secure secret key loaded from environment variables.", bullet=True)
    add_p("Input Sanitization & Injection Defense: Text prompts submitted to AI services shall be sanitized against prompt injection techniques designed to alter model instructions or leak system parameters.", bullet=True)
    add_p("Secure Static Asset Serving: User-uploaded meal images shall be served through dedicated static mount paths (/uploads) with directory browsing strictly disabled and sanitized filenames preventing path traversal attacks.", bullet=True)
    add_p("Environment Variable Isolation: Secret keys, database credentials, and third-party API keys (GEMINI_API_KEY) shall reside exclusively in isolated .env files and never be checked into version control.", bullet=True)

    add_h2("5.4 Software Quality Attributes")
    add_p("Maintainability: The backend codebase is decoupled into modular layers (api, core, db, schemas, services) following strict Single Responsibility principles. Pydantic schemas enforce type contracts across all layer boundaries.", bullet=True)
    add_p("Reliability & Fault Tolerance: The AI inference subsystem features automated multi-model fallback routines ensuring continued service availability during upstream single-model outages.", bullet=True)
    add_p("Portability: The platform is fully containerizable via Docker and Docker Compose, capable of deployment on Windows, Linux, macOS, AWS, GCP, or Azure without source code modifications.", bullet=True)
    add_p("Usability & Accessibility: The frontend interface adopts high-contrast visual tokens, responsive flexbox/grid layouts, distinct Nutri-Score color coding (Grades A-E), and intuitive keyboard navigation.", bullet=True)
    add_p("Testability: Core backend services, database transactions, and API endpoints are verified via automated integration test suites (test_backend.py) executing mock and live endpoint validations.", bullet=True)

    add_h2("5.5 Business Rules")
    add_p("Rule 1 (Calorie Floor): Under no circumstance shall the diet planning algorithm recommend daily energy intakes lower than 1,200 kcal.", bullet=True)
    add_p("Rule 2 (Nutri-Score Superiority): A product shall only be classified as a 'Healthy Alternative' if its Nutri-Score grade is superior to the original product OR its calorie density is at least 15% lower.", bullet=True)
    add_p("Rule 3 (Data Ownership): Users maintain exclusive ownership of their logged meal data; meal history entries may be exported or deleted by the user at any time.", bullet=True)
    add_p("Rule 4 (Serving Size Normalization): All statistical comparison metrics must be calculated against standardized 100g baselines to avoid skewed portion size manipulation.", bullet=True)

    add_h1("6. Other Requirements")
    add_h2("6.1 Database Requirements & Data Models")
    add_p(
        "NutriVision requires an asynchronous relational database management system. The persistence schema comprises five "
        "core entities managed via SQLAlchemy ORM: User (users table), UserProfile (user_profiles table), MealLog (meal_logs table), "
        "MealItem (meal_items table linked via cascade delete), and UserCollection (user_collections table storing saved alternative products)."
    )

    add_h2("6.2 Legal & Regulatory Compliance")
    add_p(
        "The system complies with global and national nutritional disclosure frameworks, including FSSAI (India) Labelling "
        "Regulations and FDA (US) Nutrition Labeling standards. The platform enforces the display of clear algorithmic decision-support "
        "notices, clarifying that automated nutrition estimates are advisory in nature."
    )

    add_h2("6.3 Licensing & Third-Party Attribution")
    add_p(
        "All third-party open-source libraries utilized within the project (FastAPI under MIT, SQLAlchemy under MIT, OpenCV under "
        "Apache 2.0, ZXing-C++ under Apache 2.0, React under MIT) are incorporated in strict compliance with their respective "
        "licensing mandates. OpenFoodFacts data is ingested under the Open Database License (ODbL)."
    )

    doc.add_page_break()

    # ==========================================
    # PAGE 15: APPENDIX A: GLOSSARY
    # ==========================================
    add_h1("Appendix A: Glossary")
    glossary = [
        ("AIStructuredMealResponse", "A formal Pydantic data transfer object specifying the JSON schema enforced on Google Gemini output, encompassing dish summary, total calories, macronutrients, confidence rating, and component items."),
        ("BMR (Basal Metabolic Rate)", "The baseline number of calories required to sustain involuntary physiological functions (respiration, circulation, cellular repair) at absolute physical rest."),
        ("CORS (Cross-Origin Resource Sharing)", "A browser security standard utilizing HTTP headers to grant or restrict web applications running at one origin access to selected resources from a distinct server origin."),
        ("FastAPI", "A cutting-edge, high-performance Python web framework for building RESTful APIs based on standard Python type hints, OpenAPI specifications, and asynchronous event loops."),
        ("Gemini 2.5 Flash", "Google's multimodal large language model optimized for ultra-low latency, high-accuracy computer vision, and structured JSON object generation from image inputs."),
        ("JWT (JSON Web Token)", "An open industry standard (RFC 7519) defining a compact and self-contained mechanism for securely transmitting information between parties as a cryptographically signed JSON object."),
        ("Macronutrients", "The three primary nutritional energy sources required in large quantities by the human body: Protein (4 kcal/g), Carbohydrates (4 kcal/g), and Fats (9 kcal/g)."),
        ("Mifflin-St Jeor Equation", "A widely validated clinical formula used to compute resting metabolic rate based on body mass, stature, age, and biological sex."),
        ("Nutri-Score", "A standardized, front-of-pack nutritional label developed by French health authorities that rates packaged food products on a five-color alphabetical scale from Grade A (healthiest) to Grade E (least healthy)."),
        ("OpenCV (Open Source Computer Vision)", "An open-source library of computer vision and image processing algorithms used in this project for image border padding, color space manipulation, and noise cropping."),
        ("OpenFoodFacts", "A global, collaborative, open database of food products containing nutritional facts, ingredient lists, packaging photography, and barcodes for over 3 million packaged goods."),
        ("Pydantic", "The most widely used data validation and settings management library for Python, enforcing type hints at runtime with user-friendly error diagnostics."),
        ("SQLAlchemy", "The Python SQL toolkit and Object Relational Mapper (ORM) providing enterprise-level persistence patterns and asynchronous database session management."),
        ("TDEE (Total Daily Energy Expenditure)", "The aggregate total of calories expended by an individual within a 24-hour window, calculated by multiplying BMR with physical activity coefficients."),
        ("UML (Unified Modeling Language)", "A standardized general-purpose modeling language in the field of software engineering for specifying, visualizing, and documenting software artifacts."),
        ("Vite", "A next-generation frontend build tool providing an extremely fast development server and optimized Rollup production asset bundles for React single-page applications."),
        ("ZXing-C++", "A high-performance, open-source C++ library for decoding 1D and 2D optical barcodes, wrapped for native execution within Python runtimes.")
    ]
    for term, defn in glossary:
        add_p(f"{defn}", bold_prefix=f"{term} — ", space_after=3.5)

    doc.add_page_break()

    # ==========================================
    # PAGE 16: APPENDIX B.1 USE CASE MODEL
    # ==========================================
    add_h1("Appendix B: Analysis Models")
    add_p(
        "This section documents the formal UML analysis models illustrating the architectural behavior, state lifecycles, and "
        "inter-subsystem communications of the NutriVision platform."
    )

    add_h2("B.1 UML Use Case Model")
    add_p(
        "The Use Case Model delineates the interactions between primary human actors (Guest/Visitor, Registered User, System Admin), "
        "the NutriVision System Boundary, and secondary external systems (Google Gemini AI, OpenFoodFacts API, SQLite DB). It formally "
        "defines mandatory dependencies (<<include>>) and optional feature extensions (<<extend>>)."
    )
    
    uc_img_path = r"c:\Users\dgupt\Downloads\webd\food_analyser_system\use_case_diagram.jpg"
    if os.path.exists(uc_img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(uc_img_path, width=Inches(5.8))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        r_c = p_cap.add_run("Figure B-1: UML Use Case Diagram for NutriVision Food Analyzer Platform")
        r_c.italic = True
        r_c.font.size = Pt(9)

    add_p(
        "Key Relationships in Figure B-1: (1) UC-04 (Estimate Meal Calories) exhibits an <<extend>> dependency with 'Upload Meal Photo' "
        "and an <<include>> dependency with UC-05 (Log Meal to History); (2) UC-07 (Compare Products) exhibits an <<extend>> dependency "
        "with 'Save Healthy Alternative'; (3) UC-08 (Generate Personalized Diet Plan) has a mandatory <<include>> association with UC-02 "
        "(Manage Macro Profile)."
    )

    doc.add_page_break()

    # ==========================================
    # PAGE 17: APPENDIX B.2 SEQUENCE & B.3 STATE MODELS
    # ==========================================
    add_h2("B.2 UML Sequence Model")
    add_p(
        "The Sequence Diagram captures the chronologically ordered messaging flow for the core multimodal meal estimation and "
        "transactional persistence pipeline across seven system lifelines: User, React Frontend Boundary, FastAPI Controller, "
        "StorageService, GeminiService, Google Gemini API, and SQLite Database."
    )

    seq_img_path = r"c:\Users\dgupt\Downloads\webd\food_analyser_system\sequence_diagram.jpg"
    if os.path.exists(seq_img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(2)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(seq_img_path, width=Inches(5.6))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(6)
        r_c = p_cap.add_run("Figure B-2: UML Sequence Diagram for Multimodal AI Meal Estimation & Persistence")
        r_c.italic = True
        r_c.font.size = Pt(8.5)

    add_h2("B.3 UML State Machine Model")
    add_p(
        "The State Machine Diagram documents the operational lifecycle of the user session, capturing transitions between "
        "Unauthenticated guest states, JWT credential validation, and the composite Authenticated Session superstate hosting the "
        "AI Meal Estimator, Packaged Food Scanner, Product Comparison, and Diet Planner sub-lifecycles."
    )

    state_img_path = r"c:\Users\dgupt\Downloads\webd\food_analyser_system\state_diagram.jpg"
    if os.path.exists(state_img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(2)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(state_img_path, width=Inches(5.6))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(6)
        r_c = p_cap.add_run("Figure B-3: UML State Machine Diagram for NutriVision Application Session Lifecycle")
        r_c.italic = True
        r_c.font.size = Pt(8.5)

    doc.add_page_break()

    # ==========================================
    # PAGE 18: APPENDIX C: TBD LIST
    # ==========================================
    add_h1("Appendix C: To Be Determined (TBD) List")
    add_p(
        "The following engineering and calibration items are pending final experimental benchmarking during production deployment:"
    )

    tbds = [
        ("TBD-1", "Empirical Benchmarking of Gemini 2.5 Flash vs. 1.5 Flash Latency: Quantitative evaluation of average response latency under high concurrency loads across peak evening meal logging hours (Section 5.1)."),
        ("TBD-2", "Optimal OpenCV Adaptive Threshold Kernel Dimensions: Calibration of adaptive binarization matrix parameters for distorted barcode packaging scans on curved cylindrical containers (Section 4.2)."),
        ("TBD-3", "Automated Local Food Database Caching Layer: Evaluation of Redis vs. PostgreSQL query caching for frequently scanned regional food barcodes to reduce external OpenFoodFacts API overhead (Section 2.5)."),
        ("TBD-4", "Client-Side Offline Meal Image Queueing: Exploration of ServiceWorker and IndexedDB integration enabling offline photo capture and background synchronization upon network reconnection (Section 3.1)."),
        ("TBD-5", "Multi-Language Front-of-Pack Nutritional Parsing: Assessment of multilingual optical character recognition (OCR) for regional packaging labels lacking registered barcodes (Section 6.2)."),
        ("TBD-6", "Production Deployment Target Orchestration: Final selection of container orchestration infrastructure (AWS ECS Fargate vs. DigitalOcean Managed Kubernetes) for multi-region scalability (Section 2.4)."),
        ("TBD-7", "Clinical Micronutrient & Vitamin Deficiency Modeling: Expansion of the recommendation service schema to quantify iron, calcium, vitamin D, and dietary fiber intake against RDA standards (Section 4.4)."),
        ("TBD-8", "Automated Allergy Conflict Interceptor: Implementation of deterministic allergy contradiction warnings cross-referencing ingredients against user intolerance profiles (Section 5.2).")
    ]

    tbd_table = doc.add_table(rows=len(tbds)+1, cols=2)
    tbd_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbd_table.cell(0, 0).text = "TBD Identifier"
    tbd_table.cell(0, 1).text = "Description & Engineering Context"
    tbd_table.cell(0, 0).paragraphs[0].runs[0].bold = True
    tbd_table.cell(0, 1).paragraphs[0].runs[0].bold = True
    set_cell_shading(tbd_table.cell(0, 0), "E0E0E0")
    set_cell_shading(tbd_table.cell(0, 1), "E0E0E0")
    set_cell_margins(tbd_table.cell(0, 0), 60, 60, 80, 80)
    set_cell_margins(tbd_table.cell(0, 1), 60, 60, 80, 80)

    for idx, (t_id, desc) in enumerate(tbds, start=1):
        c0 = tbd_table.cell(idx, 0)
        c1 = tbd_table.cell(idx, 1)
        c0.text = t_id
        c0.paragraphs[0].runs[0].bold = True
        c1.text = desc
        set_cell_margins(c0, 45, 45, 60, 60)
        set_cell_margins(c1, 45, 45, 60, 60)

    p_end = doc.add_paragraph()
    p_end.paragraph_format.space_before = Pt(30)
    p_end.paragraph_format.space_after = Pt(4)
    p_end.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_end = p_end.add_run("— End of Software Requirements Specification (Version 1.0 Approved) —")
    r_end.italic = True
    r_end.font.size = Pt(9.5)
    r_end.font.color.rgb = RGBColor(120, 120, 120)

    # Save document
    output_path = r"c:\Users\dgupt\Downloads\webd\food_analyser_system\NutriVision_SRS_18Pages.docx"
    doc.save(output_path)
    print(f"Calibrated 18-page Document successfully created at: {output_path}")
    try:
        doc.save(r"c:\Users\dgupt\Downloads\webd\food_analyser_system\NutriVision_SRS_Specification.docx")
        print("Also updated NutriVision_SRS_Specification.docx")
    except Exception as e:
        print(f"Notice: NutriVision_SRS_Specification.docx was open/locked, saved to NutriVision_SRS_18Pages.docx: {e}")


if __name__ == "__main__":
    main()
