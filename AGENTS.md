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

2. **Chaka Farms**
   - **Activities:** Livestock & dairy production (milking yield logs: morning/evening), canine unit care (kennel sanitation, dog bathing & grooming, manners training, afternoon off-leash walking, goat socialization), farm plumbing maintenance (unblocking drainage, sink repairs), paddock rain hose irrigation, compound & garden cleanliness.
   - **Milk Units & Production vs. Allocation Rule:**
     - Milk yield units MUST ALWAYS be recorded and displayed in **Litres** (or 'L'), NEVER in Kilograms (KG/kg).
     - **Dairy Cow Milk Yield** represents the **Total Gross Milk Production** (e.g., 5.5L morning + 2.5L evening = 8.0L Total).
     - **Rations & Allocations (Goat Kids Ration, Gladys, Maasai, staff):** These are **deductions/disbursements drawn OUT OF the total milk yield**, NOT additions to it. NEVER add allocations/rations to the cow milk yield to create a higher total. Clearly distinguish Gross Production, Total Allocations Deducted, and Net Remaining Farm Balance.
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

## 2. Strict Factual Accuracy & Anti-Hallucination Rule

- **Never Assume or Invent Unmentioned Activities:** AI assistants MUST NEVER hallucinate, assume, fabricate, or insert routine activities, maintenance tasks, cleanings, or logs that were not explicitly provided in the user's prompt or daily field notes.
- **Strict Grounding:** If an activity (e.g. cowshed/goat shed wash, garden sweeping, plumbing repair) is not mentioned in the daily brief, **DO NOT add it or assume it took place**. Every bullet point, narrative log, and activity card must be strictly grounded in verified user updates, uploaded media, or explicit daily instructions.

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
    .gallery-item img { height: 155px; }
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

3. **Dedicated Spread for Canine Unit & Compound Maintenance**:
   - The Chaka Farms Canine Unit Care, Training & Routine Log and Compound Cleanliness Log MUST be given their own dedicated, spacious spread with individual supervisor badges (Willy for Canine, Margaret & Monica for Compound).

4. **High-Impact Photo Galleries (Strictly 2 Columns & Continuous Flow)**:
   - Photo galleries MUST ALWAYS display in a **spacious 2-column grid** (`grid-template-columns: repeat(2, 1fr)`).
   - NEVER compress images into 3 columns or create a 3-column class (`gallery-grid-3col`).
   - **Continuous Straight Flow (No Grouping):** Do NOT group images or split them across multiple cards with thematic sub-headings. All photos for a project site must follow each other straight in a single continuous gallery card.
   - Photo image height: `175px–185px`, object-fit `cover`.
   - Info block padding: `11px 14px`, titles `13.5px`, captions `12px` (line-height `1.4`).

5. **Page Count Integrity (Zero Artificial Compression)**:
   - There is NO arbitrary page limit. Never sacrifice visual comfort, font sizes, line heights, or image layout to meet an arbitrary page count.
   - If a daily or monthly report requires 14, 16, 18, 20+ pages to breathe properly and maintain executive presentation, let it span that full length naturally.

