# Operations Reporting Pipeline & Archive 📊

Automated daily and monthly operational reporting pipeline, visual AI inspection system, and document archive covering agricultural, residential, and commercial project sites in Kenya.

---

## 🗺️ Project Sites & Scope

| Site Location | Key Activities & Operations | Primary Supervisors / Leads |
| :--- | :--- | :--- |
| ⛳ **Mucheru World of Golf** | Dam excavations (Dam 1, Dam 2), green trenching, hardcore rock & red soil deliveries, sub-base laying, irrigation installation, heavy plant earthworks. | Ken, Mr. Gichuhi, Kinoti |
| 🚜 **Chaka Farms** | Livestock & dairy production (morning/evening yields in Litres), canine unit care (kennel hygiene, manners, off-leash walking), paddock irrigation, compound maintenance. | Willy, Kamandau, Margaret & Monica |
| 🏡 **Kabete Residence** | Building construction, roof tile painting, outdoor fireplace excavation, main water storage tank rebar/slab, cold room shelving, domestic pet care (**Ajabu** dog & resident cats). | Operations Overseen & Shared by: Njoki |
| 🌿 **Amani Cottage** | Front lawn fertilization (CAN fertilizer), rotary sprinkler irrigation, grounds care, interior housekeeping. | Edwin, Housekeeper |

---

## 📁 Repository Structure

```
Reporting/
├── July 2026/                          # 📁 July 2026 daily reports
│   ├── Report 30th July/
│   └── Report 31st July/
├── August 2026/                        # 📁 August 2026 reports
│   ├── Monthly Report August 2026/     # Executive monthly summary HTML & PDF
│   ├── Machinery Cost Report/          # Heavy machinery billing analysis & spreadsheets
│   └── Report 1st Aug/ ... 31st Aug/   # 31 daily operations reports
├── September 2026/                     # 📁 September 2026 daily reports
│   └── Report 1st Sep/
├── whatsapp-bridge/                    # 🤖 Local Baileys WhatsApp gateway bridge
├── n8n_daily_report_generator_*.json   # ⚙️ n8n AI multimodal workflows
├── AGENTS.md                           # 📜 Instructions & SOP rules for AI assistants
├── REPORT_GENERATION_GUIDE.md          # 📖 HTML & headless Edge PDF styling guide
└── AI_ASSISTANT_HANDOFF_AND_SYSTEM_GUIDE.md # 🤖 System architecture and operations guide
```

---

## ⚙️ Core Architecture & Automation Pipeline

1. **WhatsApp Ingestion**: Supervisors send text updates, milking yields, and site photos via WhatsApp to the local Baileys bridge (`bridge.js`).
2. **AI Multimodal Inspection**: n8n workflow processes images and field notes using Google Gemini vision models, categorizing assets by site and enforcing SOP rules.
3. **Executive Report Generation**: Modern, responsive Plus Jakarta Sans HTML report is assembled with KPI summaries, data tables, and photo galleries.
4. **Headless PDF Compilation**: Microsoft Edge headless prints pixel-perfect A4 documents with print-specific CSS rules (`@media print`).
5. **Instant Delivery**: Generated PDF reports are returned directly via WhatsApp.

---

## 📜 Key SOP Guidelines

* **Milk Measurement**: Dairy cow yields are recorded strictly in **Litres (L)**, never kilograms. Deductions (rations for goat kids, staff) are subtracted from gross yield.
* **Machinery Consolidation**: Front Loader and Backhoe refer to the same vehicle (**Backhoe Loader**); operational hours and billing are consolidated without duplicate entries.
* **Factual Grounding**: Reports strictly reflect verified supervisor updates and media assets without assumed or hallucinated tasks.
* **Video Media**: Videos are hosted and linked directly via Google Drive action buttons in report cards.

---

*Maintained by Dennis*
