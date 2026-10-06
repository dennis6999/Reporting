# Instructions for AI Assistants — Daily Operations HTML & PDF Report Generation

This document outlines the mandatory standard operating procedure (SOP), rules, and technical guidelines for AI assistants generating daily operations progress reports (HTML web pages and PDF documents) in this repository.

---

## 1. Project Locations & Domain Rules

The reporting workflow covers four primary sites. Ensure tasks, updates, and assets are strictly categorized under their correct location:

1. **Mucheru World of Golf**
   - **Activities:** Dam excavation (Dam 1, Dam 2), earthmoving & haulage, green trenching, material deliveries (hardcore rocks, red topsoil, ballast stone), green foundation laying, irrigation system setup (PVC pipes, fittings, sprinklers), gate fitting, and boundary fence asset transfers.
   - **Heavy Equipment Rule:** The **Front Loader** and **Backhoe** refer to the same vehicle on site (**Backhoe Loader**). NEVER list them as two distinct machines or create duplicate rows in the machinery log. Always consolidate its operational hours and billing under a single Backhoe Loader entry (e.g., 8.0 hrs @ 6,500/hr = KES 52,000).
   - **Supervisors:** Ken, Mr. Gichuhi, Kinoti, Kamandau.
   - **Visual Theme:** Golf Green (`#15803d`).
   - **Mandatory Daily Greens & Teeboxes Status Ledger Rule (Effective From September 16th, 2026 Onwards):**
     - Every daily report from September 16th onwards MUST include the comprehensive **Course Engineering & Agronomy Status Audit** ledger modeled strictly on `September 2026/Course Status Greens and Tees/Mucheru_Golf_Greens_and_Tees_Status_Report.pdf` (and its reference implementation in `September 2026/Course Status Greens and Tees/index.html`).
     - **Required Structure:**
       1. **Putting Greens Status Table (Greens 1 – 18):** Columns: `Green` (`col-id`), `Current Technical & Agronomic State` (`col-status`), and `Milestone Status` (`col-tag`). Use color-coded badge classes (`.tag-ready`, `.tag-sand`, `.tag-trenched`, `.tag-neutral`, `.tag-pending`).
       2. **Championship Teeboxes Status Table (Tees 1 – 18):** Columns: `Teebox` (`col-id`), `Current Technical & Earthwork State` (`col-status`), and `Platform Status` (`col-tag`). Use color-coded badge classes (`.tag-ready`, `.tag-trenched`, `.tag-neutral`).
       3. **Operations Synthesis Callout:** A dedicated summary card (`.summary-card`) synthesizing total course completion rates (e.g., % of greens trenched, sub-base pumice coverage, teebox alignment).
     - **Day-to-Day Incremental State Continuity Rule:**
       - **Only update what changed:** On each reporting day, update solely the technical description, milestone tag, and date marker (e.g., `(Sep 16)`) for the specific greens and teeboxes that underwent construction, trenching, earthwork, or shaping on that day.
       - **Unchanged Greens and Tees:** If there was no work or change on certain greens or tees on that day, **leave their description and status tag exactly as they were on the preceding day's report**. Continuity is strictly preserved day-to-day from the preceding daily report's ledger.
     - **Latest Activity & Single Date Rule (Putting Greens Status Audit):**
       - In the `Current Technical & Agronomic State` column, **only state what was done last**.
       - **NEVER** give status for more than 1 previous date or accumulate historical progression lists.
       - Use **just the latest date** a green was worked on (e.g., `Surplus red soil spread around outer surrounds and leveled (Sep 30)`).
     - **Simple Vocabulary Rule (No Heavy Technical Terms):**
       - Keep vocabulary simple, direct, and straightforward.
       - Strictly avoid unnecessary use of heavy technical jargon (e.g., replace "agronomic profile feathering" or "fractured hardcore foundation matrix" with clear, simple terms like "red soil spread to level surrounds").
     - **Visual Indicator for Changed Greens & Tees (`.row-changed` & `.badge-today`):**
       - To make daily changes instantly identifiable while maintaining executive subtlety:
         1. Apply the class `class="row-changed"` to the table row (`<tr>`) of any green or tee modified on that reporting day.
         2. The first cell (`td:first-child`) receives a subtle 3.5px solid golf-green left accent border (`border-left: 3.5px solid #15803d;`) and an ultra-soft tinted row background (`#f0fdf4`).
         3. Place a compact green micro-badge next to the ID: `<span class="badge-today">Today</span>` (e.g., `<td class="col-id">Green 1 <span class="badge-today">Today</span></td>`).
         4. Unchanged rows remain neutral with standard styling and no badge.


2. **Chaka Farms**
   - **Activities:** Livestock & dairy production (milking yield logs: morning/evening), canine unit care (kennel sanitation, dog bathing & grooming, manners training, afternoon off-leash walking, goat socialization), farm plumbing maintenance (unblocking drainage, sink repairs), paddock rain hose irrigation, compound & garden cleanliness.
   - **Milk Units & Reconciliation Rule (Effective October 1st, 2026 Onwards):**
     - **Units:** Milk volume MUST ALWAYS be recorded and displayed in **Litres** (or 'L'), NEVER in Kilograms (KG/kg).
     - **Field Log vs Commercial Sales Ground Truth:** The morning and evening figures recorded by Kamandau in his daily log represent the volume of milk **sold/dispatched** for commercial sale (`Commercial Sales`).
     - **Internal Farm Allocations:** Routine disbursements (e.g., 1.0L Goat Kids Ration [0.5L morning + 0.5L evening], 0.5L Gladys staff allocation, 0.5L Maasai security allocation = 2.0L total) are distributed directly on-farm in addition to commercial sales.
     - **Gross Cow Milk Harvest Formula:** Total milk produced is calculated by adding commercial sales to internal farm allocations:
       $$\text{Total Gross Milk Harvested} = \text{Morning Sold} + \text{Evening Sold} + \text{Internal Farm Allocations}$$
       *(Example: 2.5L morning sold + 2.5L evening sold + 2.0L internal allocations = **7.0L Total Gross Milk Harvested**).*
     - **Ledger Structure:** Daily Dairy Milking tables must clearly distinguish:
       1. **Commercial Milk Sales (Dispatched):** Morning session, evening session, and daily sales total.
       2. **Internal Farm Allocations:** Goat kids, Gladys, Maasai allocations.
       3. **Total Gross Milk Harvested:** Total sales + total farm allocations (100% accounted for, zero discrepancy).
   - **Supervisors:** Willy (Canine & Plumbing), Kamandau (Milking), Margaret & Monica (Gardens & Compound).
   - **Visual Theme:** Farm Amber (`#d97706`).

3. **Kabete Residence**
   - **Activities:** Building construction & painting (main house roof tile painting, carpark canopy painting, generator & lawnmower house roof painting), outdoor fireplace excavation & clearance, main water storage tank foundation slab rebar, cold room ventilation installation, veranda clearance, and domestic pet care.
   - **Resident Pets Rule:** Domestic pets—specifically **Ajabu the Golden Retriever** and **resident cats (Reo, Mocha & Aiko)**—belong strictly to **Kabete Residence**, NOT Chaka Farms.
   - **Operational Oversight & Updates:** Operations are overseen and shared by **Njoki** (she oversees daily operations and shares field updates on what has been accomplished; she is NOT a site supervisor. NEVER refer to her as a supervisor or write "under the supervision of Njoki").
   - **Visual Theme:** Residence Purple (`#6d28d9`).

4. **Amani Cottage**
   - **Activities:** Front lawn fertilization (Calcium Ammonium Nitrate - CAN fertilizer application), sprinkler irrigation, garden litter collection, and interior housekeeping (dusting, cleaning, furniture arrangement).
   - **Supervisors:** Edwin (Grounds & Lawn), Domestic Housekeeper (Interior Housekeeping).
   - **Visual Theme:** Cottage Teal (`#0d9488`).

---

## 2. Strict Factual Accuracy & Simple Plain Language

- **Never Assume or Invent Unmentioned Activities:** AI assistants MUST NEVER hallucinate, assume, fabricate, or insert routine activities, maintenance tasks, cleanings, or logs that were not explicitly provided in the user's prompt or daily field notes.
- **Strict Grounding:** If an activity (e.g. cowshed/goat shed wash, garden sweeping, plumbing repair) is not mentioned in the daily brief, **DO NOT add it or assume it took place**. Every bullet point, narrative log, and activity card must be strictly grounded in verified user updates, uploaded media, or explicit daily instructions.
- **Simple & Clear Vocabulary Rule (No Unnecessary Heavy Technical Terms):**
  - Use simple, straightforward language across the entire report (narratives, status ledgers, photo captions, and summaries).
  - Strictly avoid unnecessary, pretentious, or heavy technical jargon (e.g., replace "agronomic profile feathering" with "spreading red soil to level surrounds", replace "geomembrane polyethylene anchor trench backfill" with "tucking dam liner into anchor trench and covering with soil").
  - Plain, clear, professional English communicates progress far more effectively than complicated technical terms.

---

## 3. Image Analysis & Placement Protocol

1. **Always Visually Inspect Images (`view_file`)**
   - **DO NOT rely solely on filenames.** Filenames provided in raw uploads can be misleading, ambiguous, or mislabeled.
   - Always use multimodal tools (`view_file`) to visually inspect every single image before placing it into a report.

2. **Context-Aware Report Placement**
   - Analyze the visual contents (e.g., excavator excavating soil vs. painter on ladder vs. dog inside kennel stall vs. fertilizer bucket).
   - Assign each image to its exact section, card component, and activity.

3. **Rich & Descriptive Captions**
   - Provide clear, factual titles (`<h4>`) and descriptive visual captions (`<p>`).
   - Describe specific visual evidence (e.g., equipment model, terrain condition, progress stage, materials depicted, animal behavior).

4. **No Image Grouping Rule (Continuous Straight Photo Flow)**
   - **Stop putting images into groups.** AI assistants MUST NEVER divide a site's photos into separate thematic cards, sub-groups, or multiple fragmented gallery cards with custom thematic headings (e.g., dividing photos into distinct cards like "Fairway Clearing" vs "Green Foundation", or "Structural Works" vs "Fireplace Excavation").
   - All photographic field evidence for a given project site must be presented in **one single continuous photo gallery card** titled `📸 Photographic Field Evidence — [Site Name]`.
   - Within this unified gallery card, all verified site images must follow each other straight, flowing sequentially one after another in the standard 2-column grid layout (`grid-template-columns: repeat(2, 1fr)`).

5. **Minimal Cropping Rule for Images in Cards (Preserve Main Subject)**
   - When putting images in cards, there must be **minimal cropping** of the image.
   - Images do not serve their purpose when the main subject (workers, heavy machinery, pets, construction elements, roofs, gates) is cropped off.
   - Always display card images so the entire photograph is visible without slicing off the subject. Use `object-fit: contain; background-color: #f8fafc;` (or flexible containers) in both screen and print CSS.
   - Never apply aggressive fixed-height `object-fit: cover` that chops off workers' heads, machine booms, animals, or building features.

---

## 4. HTML Structure & Design System

Every report must be crafted with high aesthetic standards:

- **Typography:** Modern typography via Google Fonts (`Plus Jakarta Sans` or `Inter`).
- **Color Palette:**
  - Header: Sleek Dark (`#0f172a`) with contrasting date badge (clean aesthetic, no gradient bottom bar).
  - Cards: White background, subtle border (`#e2e8f0`), shadow (`0 1px 2px 0 rgb(0 0 0 / 0.05)`).
- **KPI Summary Bar:** Top section highlighting 3–4 key metrics (e.g., Dam Haulage Trips, Milk Yield in Litres, Key Accomplishments, Active Site Count).
- **Section Badges:** Display supervisor names (`Overseen by: [Name]`) prominently on each card/section.
- **Data Tables:** Use structured HTML tables for quantitative logs (e.g., Dairy Milking Yield tables in Litres, Material Delivery breakdowns).
- **Course Engineering & Agronomy Status Tables (`.status-table`):** Structured 3-column audit tables for 18 Putting Greens and 18 Championship Teeboxes under Mucheru World of Golf. Features subtle borders (`#e2e8f0`), alternating row shading (`#fafbfd`), fixed-width ID and tag columns (`col-id`, `col-tag`), and standardized color-coded status badges (`.tag-ready`, `.tag-sand`, `.tag-trenched`, `.tag-neutral`, `.tag-pending`). Accompanied by a `.summary-card` synthesizing course-wide progress.
- **Key Accomplishment Highlight Callouts:** Use green callout boxes (`.success-box`) to celebrate key accomplishments and completed objectives (e.g., 100% main house roof painting complete).
- **Responsive Photo Galleries:** Display images in a grid layout (`grid-template-columns: repeat(auto-fit, minmax(240px, 1fr))`).
- **Video Cards & Action Buttons:** Present each video in a dedicated `.video-card` component with an embedded 16:9 `<video>` element for browser playback, descriptive title and summary, and an elegant styled action button linking directly to Google Drive (`.video-drive-btn`). Never group multiple unrelated videos inside a single video player or stack raw hyperlink text.
- **Footer Signature:** Every report MUST always end with the signature block: `<h3>Compiled by Dennis</h3>`. Do NOT invent, assume, or append any job titles or designations (e.g., "Operations Lead", "Reporting Coordinator", etc.) below the name.

---

## 5. PDF Generation & Print Styling Guidelines

### Critical PDF Print CSS Rules
When converting HTML reports to PDF using headless Edge/Chrome, you **MUST** include print-specific CSS rules to ensure clean, professional output:

```css
@media print {
    @page { 
        size: A4; 
        margin: 8mm 10mm; 
    }
    
    /* 1. HIDE VIDEO PLAYER CONTROLS IN PDF OUTPUT & RENDER CLEAN CARD HEADER */
    .video-media-wrapper video, video { 
        display: none !important; 
    }
    .video-media-wrapper { 
        aspect-ratio: auto !important; 
        height: 36px !important; 
        background: #f1f5f9 !important; 
        border-bottom: 1px solid #cbd5e1 !important; 
        display: flex !important; 
        align-items: center !important; 
        padding: 0 14px !important; 
    }
    .video-media-wrapper::before { 
        content: "🎥 Video Recording" !important; 
        font-size: 0.78rem !important; 
        font-weight: 700 !important; 
        color: #334155 !important; 
        text-transform: uppercase !important; 
    }
    
    /* 2. PREVENT AWKWARD PAGE BREAKS */
    .card, .gallery-item, .video-card, footer { 
        page-break-inside: avoid; 
    }
    .section-header { 
        page-break-after: avoid; 
    }
    
    /* 3. RETAIN COLORS & STYLING IN PRINT */
    * {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
    
    /* 4. PRINT LAYOUT OPTIMIZATIONS */
    body { background-color: #ffffff; padding: 0; }
    .container { box-shadow: none; border: none; max-width: 100%; }
    .gallery-grid, .video-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
    .gallery-item img { height: 165px; object-fit: contain; background-color: #f8fafc; }

    /* 5. STATUS TABLES & CHANGED ROW INDICATORS (ANTI-COMPRESSION SIZING) */
    .status-table { width: 100% !important; }
    .status-table tr { page-break-inside: avoid !important; break-inside: avoid !important; }
    .status-table tr.row-changed { background-color: #f0fdf4 !important; }
    .status-table tr.row-changed td:first-child { border-left: 3.5px solid #15803d !important; font-weight: 800; }
    .badge-today {
        display: inline-block; font-size: 7.5px !important; font-weight: 700 !important;
        text-transform: uppercase; color: #15803d !important; background-color: #dcfce7 !important;
        border: 1px solid #86efac !important; padding: 0.5px 4px !important; border-radius: 6px; margin-left: 4px;
    }

    /* Dedicated Putting Greens Card (#greens-ledger-card) */
    #greens-ledger-card { padding: 14px 18px !important; margin-bottom: 0 !important; break-inside: avoid !important; page-break-inside: avoid !important; }
    #greens-ledger-card .card-header { font-size: 15.5px !important; margin-bottom: 6px !important; }
    #greens-ledger-card .editorial-text { font-size: 12.5px !important; line-height: 1.4 !important; margin-bottom: 6px !important; }
    #greens-ledger-card .status-table { font-size: 9.4px !important; }
    #greens-ledger-card .status-table th { padding: 4.5px 8px !important; font-size: 9px !important; }
    #greens-ledger-card .status-table td { padding: 4.2px 8px !important; font-size: 9.4px !important; line-height: 1.3 !important; }
    #greens-ledger-card .col-id { width: 74px !important; }
    #greens-ledger-card .col-tag { width: 160px !important; }
    #greens-ledger-card .tag { font-size: 8.2px !important; padding: 1.2px 4.5px !important; }

    /* Dedicated Championship Teeboxes Card (#tees-ledger-card) */
    #tees-ledger-card { padding: 16px 20px !important; margin-bottom: 0 !important; break-inside: avoid !important; page-break-inside: avoid !important; }
    #tees-ledger-card .card-header { font-size: 16px !important; margin-bottom: 8px !important; }
    #tees-ledger-card .editorial-text { font-size: 12.5px !important; line-height: 1.4 !important; margin-bottom: 8px !important; }
    #tees-ledger-card .status-table { font-size: 9.6px !important; }
    #tees-ledger-card .status-table th { padding: 5px 8px !important; font-size: 9.2px !important; }
    #tees-ledger-card .status-table td { padding: 4.5px 8px !important; font-size: 9.6px !important; line-height: 1.32 !important; }
    #tees-ledger-card .col-id { width: 72px !important; }
    #tees-ledger-card .col-tag { width: 155px !important; }
    #tees-ledger-card .tag { font-size: 8.2px !important; padding: 1.2px 4.5px !important; }
    #tees-ledger-card .summary-card { padding: 9px 12px !important; margin-top: 8px !important; margin-bottom: 0 !important; }
    #tees-ledger-card .summary-card h4 { font-size: 10.5px !important; margin-bottom: 2px !important; }
    #tees-ledger-card .summary-card p { font-size: 9.5px !important; line-height: 1.35 !important; }
}
```

### Why Hiding Videos in Print is Mandatory
HTML `<video>` controls render as blank, solid black boxes when converted to PDF. Hiding `<video>` players while styling the `.video-card` with clean header ribbons and direct Google Drive action buttons keeps the PDF document clean, functional, and print-ready.

---

## 6. Headless PDF Generation Command

To convert `index.html` to `Daily_Operations_Report_[Date].pdf`, run headless Microsoft Edge via PowerShell:

```powershell
python -c "import subprocess; subprocess.run(['C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe', '--headless', '--print-to-pdf=c:\\Users\\denni\\Downloads\\Reporting\\August 2026\\Report Xth Aug\\Daily_Operations_Report_Xth_August.pdf', 'c:\\Users\\denni\\Downloads\\Reporting\\August 2026\\Report Xth Aug\\index.html'])"
```

### Verification Checklist
After generating a report:
1. Verify `index.html` exists and opens cleanly in browser.
2. Ensure dairy milk yields are strictly recorded in Litres (never KGs).
3. Ensure no activities/tasks are assumed or hallucinated beyond user updates.
4. Verify the PDF file is created in the target directory using `list_dir`.
5. Check PDF file size (typically 5 MB – 20 MB depending on image density).
6. Ensure no video boxes appear in the generated PDF.
7. Verify all pages comply with the **Anti-Compression & Page Budgeting Standard** (Section 7).

---

## 7. Mandatory Page Budgeting, Typography & Spacing Standard (Anti-Compression Rule)

AI assistants must NEVER compress font sizes, shrink line heights, tighten bullet gaps, or jam narratives and data tables onto a single page to achieve an arbitrary page count. Every page in an executive report must feel generous, breathable, and visually balanced.

### Core Rules:
1. **Dedicated Narrative Spread**:
   - Each project site's primary narrative overview card MUST occupy its own dedicated full page.
   - **Print Typography Standard**:
     - Card padding: `20px 24px` (print) / `32px 36px` (screen).
     - Heading (`.card-heading`): `17.5px–18.5px`, bold (`800`).
     - Body text (`.editorial-text`): `14.5px–15.5px` (`0.95rem`), line-height `1.6–1.65`.
     - Bullet points (`.highlight-list li`): `14px` (`0.92rem`), line-height `1.55–1.6`, bottom margin `9px–12px`, left padding `22px–24px`.
     - Milestone callout box (`.callout-box` / `.success-box`): `11px 15px` padding, margin-top `13px`, `break-inside: avoid; page-break-inside: avoid;`.
   - The narrative card should fill **~75%–85% of the page** naturally.

2. **Dedicated Spread for Major Data Tables**:
   - Complex or multi-row data tables (e.g., *Dairy Milking Yield Ledger*, *Heavy Machinery Utilization Log*) MUST NOT be squeezed under narrative cards. Place a dedicated page break before them to grant them a dedicated page.
   - **Table Print Standard**:
     - Cell padding: `8px 12px` (print).
     - Ensure tables and accompanying clarification callouts fit completely on their dedicated page without spilling callouts onto blank overflow pages.

3. **Dedicated Spreads for Greens & Teeboxes Status Ledgers (Anti-Compression & Page-Fitting Rule)**:
   - The 18-hole **Putting Greens Status (Greens 1 – 18)** table MUST occupy its own dedicated full page in print (`id="greens-ledger-card"`).
   - The 18-hole **Championship Teeboxes Status (Tees 1 – 18)** table alongside the **Operations Synthesis** callout card MUST occupy its own dedicated full page in print (`id="tees-ledger-card"`).
   - **Anti-Compression & Page-Fitting Standards to Avoid Excess Bottom Whitespace:**
     - NEVER over-compress the status tables (e.g., cell padding below `4px`, font sizes below `9px`, or line-heights below `1.25`) as this leaves an awkward, empty white void covering the bottom half of the A4 page.
     - Conversely, do NOT make the typography too large so that the 18 rows spill over onto a second page.
     - **Exact Balanced Standards for `#greens-ledger-card`:**
       - Cell padding: `4.2px 8px !important;`, font-size: `9.4px !important;`, line-height: `1.3 !important;`.
       - Header cell padding: `4.5px 8px !important;`, font-size: `9px !important;`.
       - Card padding: `14px 18px !important;`, header font-size: `15.5px !important;`, editorial text: `12.5px !important;` (line-height: `1.4 !important;`).
       - Tag width: `160px !important;`, ID width: `74px !important;`, tag font-size: `8.2px !important;`.
     - **Exact Balanced Standards for `#tees-ledger-card`:**
       - Cell padding: `4.5px 8px !important;`, font-size: `9.6px !important;`, line-height: `1.32 !important;`.
       - Header cell padding: `5px 8px !important;`, font-size: `9.2px !important;`.
       - Card padding: `16px 20px !important;`, header font-size: `16px !important;`, editorial text: `12.5px !important;` (line-height: `1.4 !important;`).
       - Operations Synthesis summary card: padding `9px 12px !important;`, font-size: `9.5px !important;` (line-height: `1.35 !important;`).
       - Tag width: `155px !important;`, ID width: `72px !important;`, tag font-size: `8.2px !important;`.
     - Both 18-row tables must fit cleanly, comfortably, and entirely onto their respective single A4 pages, filling the page naturally without awkward multi-page spilling or excessive bottom whitespace.

4. **Dedicated Spread for Canine Unit & Compound Maintenance**:
   - The Chaka Farms Canine Unit Care, Training & Routine Log and Compound Cleanliness Log MUST be given their own dedicated, spacious spread with individual supervisor badges (Willy for Canine, Margaret & Monica for Compound).

5. **High-Impact Photo Galleries (Strictly 2 Columns, Continuous Flow & Minimal Cropping)**:
   - Photo galleries MUST ALWAYS display in a **spacious 2-column grid** (`grid-template-columns: repeat(2, 1fr)`).
   - NEVER compress images into 3 columns or create a 3-column class (`gallery-grid-3col`).
   - **Continuous Straight Flow (No Grouping):** Do NOT group images or split them across multiple cards with thematic sub-headings. All photos for a project site must follow each other straight in a single continuous gallery card.
   - **Minimal Cropping Standard:** Use `object-fit: contain; background-color: #f8fafc;` with height `200px–260px` (print: `165px`) so the complete photo and its main subject (workers, equipment, pets, structural works) remain 100% visible and uncropped.
   - Info block padding: `11px 14px`, titles `13.5px`, captions `12px` (line-height `1.4`).

6. **Page Count Integrity (Zero Artificial Compression)**:
   - There is NO arbitrary page limit. Never sacrifice visual comfort, font sizes, line heights, or image layout to meet an arbitrary page count.
   - If a daily or monthly report requires 14, 16, 18, 20+ pages to breathe properly and maintain executive presentation, let it span that full length naturally.

---

## 8. Direct HTML File Authoring & Prohibited Intermediate Scripts (Single Source of Truth)

- **Direct Authoring of `index.html`:**
  - `index.html` is the sole, authoritative source of truth for every daily operations report.
  - AI assistants MUST ALWAYS create, edit, and update `index.html` directly using native file tools (`write_to_file` and surgical `replace_file_content`).
- **Strictly Prohibited: Intermediate Python / Node Generator Scripts:**
  - AI assistants MUST NEVER write intermediate generator scripts (e.g., `generate_report_[date].py`, Python template builders, or Node scripts) in scratch or workspace directories to generate or update `index.html`.
  - Creating separate generator scripts introduces duplicate sources of truth, creates synchronization lag, litters the workspace with disposable scratch code, and adds an unnecessary layer of indirection.
- **Strictly Permitted Uses of Python:**
  - Python usage is strictly restricted to:
    1. **Headless Microsoft Edge PDF Generation:** Executing `python -c "import subprocess; subprocess.run(['C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe', '--headless', '--print-to-pdf=...', '...'])"` (handles Windows file paths with spaces and commas without PowerShell quote-escaping bugs).
    2. **Read-Only Pre-Flight / Post-Flight Validation:** Quick read-only verification scripts (e.g., verifying that all local image paths exist on disk, checking generated PDF file size, or verifying total PDF page count).


