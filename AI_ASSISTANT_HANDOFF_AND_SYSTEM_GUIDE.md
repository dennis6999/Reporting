# 🤖 AI Assistant Handoff & Automated Reporting System Guide

> **Document Purpose**: This file serves as the definitive reference for future AI assistants working with Dennis on the automated Daily Operations Reporting pipeline. Read this before making modifications or assisting with reporting tasks.

---

## 📌 1. Project Overview & Objective

Dennis manages multiple high-value agricultural, commercial, and residential projects in Kenya. Field supervisors send daily operational logs, milking metrics, machinery hours, and on-site photos over **WhatsApp**.

The objective of this system is to **fully automate the ingestion, AI visual inspection, SOP business logic calculation, HTML report generation, PDF compilation, and WhatsApp report delivery**.

```
[Supervisors send photos/text on WhatsApp]
                   ⬇️
[Local Baileys WhatsApp Bridge (bridge.js)]
   • Auto-saves photos to n8n-reports/Report [Date]
   • Filters out newsletter channels & status stories
   • Supports Dennis Self-Chat (@lid) & instant triggers
                   ⬇️
[n8n Cloud + Google Gemini AI Multimodal Vision]
   • Visually inspects image pixels (e.g. dogs -> Chaka Farms, earthworks -> Golf)
   • Enforces SOP rules (Litres only, Backhoe consolidation)
   • Generates Plus Jakarta Sans HTML report
                   ⬇️
[Microsoft Edge Headless PDF Compiler]
   • Compiles pixel-perfect A4 PDF in ~2 seconds
                   ⬇️
[Direct Delivery back to Dennis on WhatsApp]
```

---

## 🗺️ 2. Site & Supervisor Ground Truth Roster

| Project Site | Primary Supervisors | Key Operations & Assets | Ground Truth Rules |
| :--- | :--- | :--- | :--- |
| ⛳ **Mucheru World of Golf** | **Ken & Mgr Gichuhi** *(Kinoti)* | • Championship Greens (Nos. 10, 11, 14, 15, 16)<br>• Teeboxes (Nos. 4, 18)<br>• Earthmoving, spoil spreading, drainage trenches<br>• Hardcore rock deliveries from Kiganjo quarry<br>• Honi river property, stilt cabin structural assessment | • **Merge Ken & Mgr Gichuhi**: Both report on Golf; their updates must be merged into one cohesive section.<br>• **Deduplication**: Never repeat tasks or double-count hours.<br>• **Property Walk**: Property walk with Prof Ciira (DeKUT) was conducted by **Mr. Joe**, not Dennis. |
| 🚜 **Chaka Farms** | **Willy, Kamandau & Kinoti** | • Dairy cow herd production<br>• Farm canine unit (kennel manners, paddock grazing)<br>• Goat herd socialization<br>• Poultry/Goose egg hatchery<br>• Farm plumbing & compound Wi-Fi AP | • **Dairy Milk Yield**: MUST ALWAYS be formatted strictly in **Litres (L)**, NEVER in kg.<br>• **Calculation**: $\text{Gross} = \text{Morning} + \text{Evening}$; $\text{Deductions} = \text{Kids} + \text{Gladys}$; $\text{Net} = \text{Gross} - \text{Deductions}$.<br>• **Canine Unit**: Farm working dogs belong here. |
| 🏡 **Kabete Residence** | **Maggie Njoki** *(Oversees operations & shares updates; not a site supervisor)* | • Outdoor sunken fireplace deep excavation<br>• Stormwater river drainage masonry<br>• Cold room heavy-duty steel shelving<br>• Pergola terrace scrubbing & lounge furniture<br>• Kitchen mahogany cooker plinth<br>• Water storage tank anti-corrosion painting | • **Domestic Pets**: Ajabu dog and cats belong strictly to Kabete Residence, NOT Chaka Farms.<br>• **Role**: Njoki oversees daily operations and shares updates; she is NOT a supervisor. |
| 🌿 **Amani Cottage** | **Edwin** | • Front lawn oscillating sprinkler irrigation<br>• Selective weed killer herbicide spraying<br>• Two-story interior dusting & housekeeping | • Keep reporting clean and concise. |

---

## 🧮 3. Standard Operating Procedure (SOP) Math & Rules

1. **Dairy Cow Milking Production**:
   * **Gross Yield** = Morning Yield + Evening Yield (e.g. $5.5\text{L} + 2.0\text{L} = 7.5\text{L}$).
   * **Deductions** = Goat Kids Ration ($1.0\text{L}$) + Gladys Allocation ($0.5\text{L}$) = $1.5\text{L}$.
   * **Net Available Farm Balance** = $\text{Gross} - \text{Deductions} = 6.0\text{L Net Available}$.
   * **Unit Rule**: Strictly Litres (L).
2. **Heavy Machinery Billing**:
   * Consolidate all earthmoving and tipper loading under **Backhoe Loader (XGMA)**.
   * Total Billing = Operational Hours $\times$ Hourly Rate (e.g. $9.0\text{ hrs} \times \text{KES } 6,500 = \mathbf{\text{KES } 58,500}$).
3. **Footer Signature**:
   * Official signature block: `<h3>Compiled by Dennis</h3>`.
4. **Photo Galleries (No Image Grouping / Continuous Straight Flow)**:
   * Stop putting images into groups or multiple fragmented cards with thematic headings.
   * All verified site photos must follow each other straight in a single continuous photo gallery card per project site in a 2-column grid.

---

## 🛠️ 4. System Architecture & Components

### A. WhatsApp Bridge (`bridge.js`)
* **Location**: `C:\Users\denni\Downloads\Compressed\n8n-skills-2.21.0\whatsapp-bridge\bridge.js` (and mirrored in `C:\Users\denni\Downloads\Reporting\whatsapp-bridge\bridge.js`).
* **Technology**: Node.js with `@whiskeysockets/baileys`.
* **Port**: `3000` (`http://localhost:3000`).
* **Session Auth**: `auth_info_baileys/` (persisted session, no need to re-scan QR unless logged out).
* **Protocol Filters**:
  * **Blocked**: All `@newsletter` (WhatsApp Channels), `status@broadcast` (Statuses), and broadcast IDs starting with `120363...`.
  * **Allowed**: Direct supervisor chats (`@s.whatsapp.net`), group chats (`@g.us`), and Dennis's Multi-Device self-chat (`@lid`).
  * **Self-Chat Filter**: Ignores random bookmarks, YouTube links, and personal notes unless tagged with `#report`, a site keyword, or media attached.
* **Auto-Compiler & Delivery Hook**:
  * Endpoint: `POST /api/deliver-report`.
  * Executes Microsoft Edge headless print and sends the resulting PDF directly via `waSock.sendMessage`.

### B. n8n Cloud (`dennis-n8n.app.n8n.cloud`)
* **Workflow Template**: `C:\Users\denni\Downloads\n8n_multimodal_vision_reporting_pipeline.json`.
* **AI Model**: Google Gemini (`models/gemini-3.1-flash-lite` or `gemini-1.5-flash`).
* **Multimodal Vision Role**:
  * Inspects raw image pixels.
  * Classifies scene contents (dogs $\rightarrow$ Chaka, excavator $\rightarrow$ Golf, fireplace $\rightarrow$ Kabete, lawn $\rightarrow$ Amani).
  * Writes rich `<h4>` titles and `<p>` captions.

### C. Headless PDF Compiler
* **Executable**: `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`.
* **Command Syntax**:
  ```powershell
  & "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu --run-all-compositor-stages-before-draw --print-to-pdf="output.pdf" "input.html"
  ```

---

## 📁 5. Directory & File Structure

```
c:\Users\denni\Downloads\Compressed\n8n-skills-2.21.0\
├── n8n-reports\                           # 📁 Active generated reports directory
│   ├── Report 26th Aug\                   # Daily folder
│   │   ├── index.html                     # Generated HTML report
│   │   ├── Daily_Operations_Report_26th_August.pdf
│   │   ├── daily_supervisor_logs.json     # Ingested message logs
│   │   └── *.jpeg / *.JPG                 # Downloaded WhatsApp photos
│   └── Report 27th Aug\                   # Next day folder
├── whatsapp-bridge\
│   ├── bridge.js                          # Native Baileys WhatsApp Gateway
│   ├── auth_info_baileys\                 # WhatsApp persistent credentials
│   └── package.json
└── AI_ASSISTANT_HANDOFF_AND_SYSTEM_GUIDE.md # 📄 This guide

C:\Users\denni\Downloads\Reporting\        # 🔒 Official archive folder (Reference only)
├── July 2026\                             # 📁 July reports (Report 30th July, 31st July)
├── August 2026\                           # 📁 August reports (Report 1st–31st Aug, Monthly Report, Machinery Cost)
└── September 2026\                        # 📁 September reports (Report 1st Sep...)
```

---

## 🚀 6. Common Workflows & Troubleshooting

### Q: How to start the WhatsApp Bridge?
```powershell
cd C:\Users\denni\Downloads\Reporting\whatsapp-bridge
node bridge.js
```

### Q: How to trigger an instant report generation?
* **On WhatsApp**: Send `!report` to yourself.
* **In n8n Cloud**: Click the orange **"Execute workflow"** button.

### Q: How to update a past date's report (e.g. 26th August)?
* Send a message to yourself: `!report 26th Aug: [your update text / photo]`.
* The bridge routes the update to `n8n-reports\Report 26th Aug\`, re-compiles the PDF, and sends it back to your chat.

### Q: Model name 404 error in n8n Gemini node?
* Ensure the model field is set to `models/gemini-3.1-flash-lite` or `gemini-1.5-flash` (do not double prepend `models/models/...`).
