def ensure_word_closed():
    import subprocess
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'WINWORD.EXE'], capture_output=True)
    except Exception:
        pass

import os
import sys
import shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

# Paths setup
base_dir = r"c:\Users\denni\Downloads\Reporting"
sep_dir = os.path.join(base_dir, "September 2026")
report_dir = os.path.join(sep_dir, "Monthly Report September 2026")
os.makedirs(report_dir, exist_ok=True)

docx_path = os.path.join(report_dir, "Monthly_Operations_Summary_Report_September_2026.docx")
alt_docx_path = os.path.join(sep_dir, "Monthly_Operations_Summary_Report_September_2026.docx")

# ==============================================================================
# XML FORMATTING HELPERS
# ==============================================================================
def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, border_color="CBD5E1"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
        f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="{border_color}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def make_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def make_row_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

def add_callout(doc, title, text, border_color="15803D", bg_color="F0FDF4"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.9)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=160)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
        f'<w:top w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    run_t = p.add_run(title + "\n")
    run_t.bold = True
    run_t.font.name = 'Calibri'
    run_t.font.size = Pt(10.5)
    run_t.font.color.rgb = RGBColor.from_string(border_color)
    
    run_b = p.add_run(text)
    run_b.font.name = 'Calibri'
    run_b.font.size = Pt(9.5)
    run_b.font.color.rgb = RGBColor(51, 65, 85)
    
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(4)

def add_heading_1(doc, text):
    p = doc.add_heading(text, level=1)
    p.paragraph_format.space_before = Pt(22)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    run = p.runs[0]
    run.font.name = 'Calibri'
    run.font.size = Pt(16.5)
    run.bold = True
    run.font.color.rgb = RGBColor(15, 23, 42)
    return p

def add_heading_2(doc, text, color_rgb=(30, 58, 138)):
    p = doc.add_heading(text, level=2)
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.runs[0]
    run.font.name = 'Calibri'
    run.font.size = Pt(13)
    run.bold = True
    run.font.color.rgb = RGBColor(*color_rgb)
    return p

def add_toc_heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(16.5)
    run.bold = True
    run.font.color.rgb = RGBColor(15, 23, 42)
    return p

def add_table_caption(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(10.5)
    run.bold = True
    run.font.color.rgb = RGBColor(15, 23, 42)
    return p

def add_heading_3(doc, text):
    return add_table_caption(doc, text)

def add_bullet_point(doc, lead_bold, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    r_lead = p.add_run(lead_bold + " ")
    r_lead.bold = True
    r_lead.font.name = 'Calibri'
    r_lead.font.size = Pt(10)
    r_lead.font.color.rgb = RGBColor(15, 23, 42)
    
    r_txt = p.add_run(text)
    r_txt.font.name = 'Calibri'
    r_txt.font.size = Pt(10)
    r_txt.font.color.rgb = RGBColor(51, 65, 85)

# ==============================================================================
# MAIN BUILDER ROUTINE
# ==============================================================================
def build_report():
    doc = Document()
    
    # 1. Enable automatic field updating on open in Word
    settings = doc.settings.element
    settings.append(parse_xml(f'<w:updateFields {nsdecls("w")} w:val="true"/>'))

    # 2. Page Setup & Margins (0.8 in)
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)
        
        # Header setup
        header = s.header
        p_hdr = header.paragraphs[0]
        p_hdr.text = "MUCHERU WORLD OF GOLF & ASSOCIATED PROPERTIES   |   EXECUTIVE MONTHLY OPERATIONS AUDIT"
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_hdr.style.font.name = "Calibri"
        p_hdr.style.font.size = Pt(8.5)
        p_hdr.style.font.color.rgb = RGBColor(148, 163, 184)
        
        # Footer setup: 2-column table for dynamic pagination
        footer = s.footer
        p_ftr_old = footer.paragraphs[0]
        p_ftr_old.text = "" # clear default paragraph
        
        tbl_ftr = footer.add_table(rows=1, cols=2, width=Inches(6.9))
        tbl_ftr.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # Left footer cell
        c_left = tbl_ftr.cell(0, 0)
        c_left.width = Inches(4.5)
        p_fl = c_left.paragraphs[0]
        p_fl.paragraph_format.space_before = Pt(0)
        p_fl.paragraph_format.space_after = Pt(0)
        r_fl = p_fl.add_run("CONFIDENTIAL   •   SEPTEMBER 2026 COMPREHENSIVE REPORT   •   AUDITED & COMPILED BY DENNIS")
        r_fl.font.name = "Calibri"
        r_fl.font.size = Pt(8)
        r_fl.font.color.rgb = RGBColor(148, 163, 184)
        
        # Right footer cell (Dynamic Page X of Y)
        c_right = tbl_ftr.cell(0, 1)
        c_right.width = Inches(2.4)
        p_fr = c_right.paragraphs[0]
        p_fr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_fr.paragraph_format.space_before = Pt(0)
        p_fr.paragraph_format.space_after = Pt(0)
        
        r_p_txt = p_fr.add_run("Page ")
        r_p_txt.font.name = "Calibri"
        r_p_txt.font.size = Pt(8.5)
        r_p_txt.font.color.rgb = RGBColor(100, 116, 139)
        
        fld_page = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
        p_fr._p.append(fld_page)
        
        r_of_txt = p_fr.add_run(" of ")
        r_of_txt.font.name = "Calibri"
        r_of_txt.font.size = Pt(8.5)
        r_of_txt.font.color.rgb = RGBColor(100, 116, 139)
        
        fld_numpages = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="NUMPAGES"/>')
        p_fr._p.append(fld_numpages)

    # --------------------------------------------------------------------------
    # COVER / HEADER BLOCK
    # --------------------------------------------------------------------------
    p_kicker = doc.add_paragraph()
    p_kicker.paragraph_format.space_before = Pt(8)
    p_kicker.paragraph_format.space_after = Pt(2)
    r_k = p_kicker.add_run("EXECUTIVE PERFORMANCE BRIEFING   •   OPERATIONS AUDIT REPORT")
    r_k.bold = True
    r_k.font.name = 'Calibri'
    r_k.font.size = Pt(9.5)
    r_k.font.color.rgb = RGBColor(21, 128, 61)

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(4)
    r_t = p_title.add_run("MONTHLY OPERATIONS SUMMARY REPORT")
    r_t.bold = True
    r_t.font.name = 'Calibri'
    r_t.font.size = Pt(22)
    r_t.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(12)
    r_s = p_sub.add_run("Comprehensive Civil Engineering, Agronomic, Livestock & Capital Works Review — September 2026")
    r_s.font.name = 'Calibri'
    r_s.font.size = Pt(12)
    r_s.font.color.rgb = RGBColor(100, 116, 139)

    # Metadata Strip (Table)
    tbl_meta = doc.add_table(rows=2, cols=4)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_meta.autofit = False
    set_table_borders(tbl_meta, "E2E8F0")

    meta_headers = ["REPORTING PERIOD", "PRIMARY ASSETS", "OPERATING SITES", "AUDIT & REPORTING LEAD"]
    meta_values = ["1st – 30th September 2026", "Golf, Farms & Residences", "Nyeri & Nairobi, Kenya", "Dennis (Operations Auditing)"]

    col_w = Inches(1.72)
    for c_idx in range(4):
        c_hdr = tbl_meta.cell(0, c_idx)
        c_hdr.width = col_w
        set_cell_background(c_hdr, "F8FAFC")
        set_cell_margins(c_hdr, 70, 50, 100, 100)
        p = c_hdr.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(meta_headers[c_idx])
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(100, 116, 139)

        c_val = tbl_meta.cell(1, c_idx)
        c_val.width = col_w
        set_cell_background(c_val, "FFFFFF")
        set_cell_margins(c_val, 60, 70, 100, 100)
        p2 = c_val.paragraphs[0]
        p2.paragraph_format.space_after = Pt(0)
        r2 = p2.add_run(meta_values[c_idx])
        r2.bold = True
        r2.font.name = 'Calibri'
        r2.font.size = Pt(9)
        r2.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # --------------------------------------------------------------------------
    # SECTION 1: EXECUTIVE SUMMARY & SCORECARD
    # --------------------------------------------------------------------------
    add_heading_1(doc, "1. Executive Summary & Month-at-a-Glance Dashboard")

    p_lead = doc.add_paragraph()
    p_lead.paragraph_format.space_before = Pt(2)
    p_lead.paragraph_format.space_after = Pt(6)
    p_lead.paragraph_format.line_spacing = 1.15
    r_ld = p_lead.add_run(
        "During September 2026, operations across all four primary estate properties achieved major structural, agronomic, "
        "and operational milestones. Key heavy earthmoving and drainage infrastructure projects were completed on schedule, "
        "livestock dairy accounting was formally reconciled with zero discrepancy, and strategic capital works reached full completion."
    )
    r_ld.font.name = 'Calibri'
    r_ld.font.size = Pt(10)
    r_ld.font.color.rgb = RGBColor(51, 65, 85)

    add_bullet_point(doc, "Mucheru World of Golf:", "Subgrade excavation, polythene moisture barrier lining, and volcanic pumice aggregate sub-bases are 100% complete across all 18 championship putting greens. Clean riversand foundation beds have been applied across 6 priority greens (Greens 1, 2, 3, 4, 8, and 9), with Green 5 under mature championship turfgrass actively irrigated via overhead rotary sprinklers. The remaining greens (Greens 7, 10–18) are stabilized on compacted pumice sub-bases over drainage lines, with surplus red loam topsoil contouring their aprons and surrounds. All 18 championship teebox platforms are completely shaped and graded. Main HDPE irrigation waterline was tied into Peter's supply on Sep 29, activating automated sprinklers on Green 5.")
    add_bullet_point(doc, "Chaka Farms:", "Total gross cow milk harvested reached 215.0 Litres (daily average: 7.2 L/day). Commercial dispatched sales accounted for 160.5 Litres (74.7%), while 54.5 Litres (25.3%) went to internal farm rations (29.0L goat kids, 25.5L staff & security). Zero milk loss recorded; 100% reconciled. Herd health remained flawless under routine tick-spraying and deworming. Working Canine Unit achieved rigorous obedience, manners, and livestock socialization standards under Willy.")
    add_bullet_point(doc, "Kabete Residence:", "100% completion of main house roof tile cleaning, priming, and protective painting. Carport canopy and generator/mower house roofs fully repainted. Outdoor fireplace excavation and structural clearance finished. Main water tank foundation slab rebar assembled. Cold room shelving and ventilation fit-out completed. Domestic pets (Ajabu the Golden Retriever, cats Reo, Mocha, Aiko) in prime health. Operations overseen and shared by Njoki.")
    add_bullet_point(doc, "Amani Cottage:", "Lawn agronomy program successfully executed: Calcium Ammonium Nitrate (CAN) fertilization and automated rotary sprinkler irrigation maintained a lush emerald-green turf profile. Woodland perimeter clearing and interior housekeeping sustained immaculate guest presentation under Edwin and the domestic housekeeper.")
    add_bullet_point(doc, "Financials & Heavy Machinery:", "Consolidated Backhoe Loader deployment totaled 97.33 operating hours across 14 operational days, resulting in KES 632,645.00 expenditure (@ KES 6,500.00/hr). A 10-day standby interval (Sep 8–18) occurred following mechanical failure of the JCB 3DX, after which the original XGMA Backhoe was remobilized to finalize course contouring.")

    # Table 1: Executive Scorecard
    add_table_caption(doc, "Table 1: September 2026 Executive Performance Scorecard")

    t1 = doc.add_table(rows=5, cols=4)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1.autofit = False
    set_table_borders(t1, "CBD5E1")

    t1_headers = ["Property / Project Site", "Primary Operational Focus", "Key Quantitative Metrics", "Month-End Status"]
    t1_widths = [Inches(1.8), Inches(2.2), Inches(1.6), Inches(1.3)]

    hdr_row = t1.rows[0]
    make_row_header(hdr_row)
    make_row_cant_split(hdr_row)
    for idx, name in enumerate(t1_headers):
        c = hdr_row.cells[idx]
        c.width = t1_widths[idx]
        set_cell_background(c, "0F172A")
        set_cell_margins(c, 80, 80, 100, 100)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(name)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    scorecard_data = [
        ("Mucheru World of Golf", "Course Earthmoving, Drainage, Greens & Tees Construction, Irrigation Tie-In", "18 Greens Pumice Sub-Base (100%)\n6 Greens Riversand Applied\n18 Tees Graded (100%)\n97.33 Backhoe Hrs (KES 632k)", "Advanced (Ahead of Schedule)"),
        ("Chaka Farms", "Dairy Production & Sales, Herd Health, Canine Unit Training, Farm Upkeep", "215.0L Gross Produced\n160.5L Commercial Sales\n54.5L Farm Allocations\n7.2 L/Day Herd Average", "100% Reconciled (Zero Loss)"),
        ("Kabete Residence", "Main House Roof Painting, Fireplace Excavation, Tank Slab Rebar, Pet Care", "100% Roof Painting Done\n100% Carport & Shed Done\nCold Room Ventilated\nDaily Pet Care (Ajabu & Cats)", "Key Milestones Completed"),
        ("Amani Cottage", "Front Lawn Fertilization, Sprinkler Irrigation, Housekeeping & Presentation", "CAN Fertilizer Applied\nRotary Sprinklers Active\n100% Compound Sweeping\nInterior Staged & Sanitized", "Optimal Condition"),
    ]

    for r_idx, row_data in enumerate(scorecard_data):
        row = t1.rows[r_idx + 1]
        make_row_cant_split(row)
        bg = "FAFBFD" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx in range(4):
            c = row.cells[c_idx]
            c.width = t1_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, 70, 70, 100, 100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(row_data[c_idx])
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)
            elif c_idx == 3:
                r.bold = True
                r.font.color.rgb = RGBColor(21, 128, 61)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # --------------------------------------------------------------------------
    # TABLE OF CONTENTS (NATIVE WORD TOC FIELD)
    # --------------------------------------------------------------------------
    doc.add_page_break()
    add_toc_heading(doc, "Table of Contents")

    # Insert Native Word TOC Field (Level 1 and Level 2 headings only)
    p_native_toc = doc.add_paragraph()
    p_native_toc.paragraph_format.space_before = Pt(6)
    p_native_toc.paragraph_format.space_after = Pt(14)
    r_ntoc = p_native_toc.add_run()
    
    fldChar1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
    instrText = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> TOC \\o "1-2" \\h \\z \\u </w:instrText>')
    fldChar2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="separate"/>')
    fldChar3 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
    
    r_ntoc._r.append(fldChar1)
    r_ntoc._r.append(instrText)
    r_ntoc._r.append(fldChar2)
    r_ntoc._r.append(fldChar3)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # SECTION 3: MUCHERU WORLD OF GOLF
    # --------------------------------------------------------------------------
    add_heading_1(doc, "2. Mucheru World of Golf — Course Engineering & Agronomy")
    
    add_heading_2(doc, "2.1 Course Civil Engineering, Earthmoving & Irrigation Infrastructure", (21, 128, 61))

    p_g_lead = doc.add_paragraph()
    p_g_lead.paragraph_format.space_before = Pt(2)
    p_g_lead.paragraph_format.space_after = Pt(4)
    p_g_lead.paragraph_format.line_spacing = 1.15
    r_gl = p_g_lead.add_run(
        "Field operations at Mucheru World of Golf in September delivered comprehensive progress across putting green "
        "sub-base construction, championship teebox platform contouring, bulk haulage, and irrigation tie-ins under "
        "the supervisory coordination of Mr. Gichuhi, Ken, Kinoti, and Kamandau."
    )
    r_gl.font.name = 'Calibri'
    r_gl.font.size = Pt(10)
    r_gl.font.color.rgb = RGBColor(51, 65, 85)

    add_bullet_point(doc, "Sub-Base & Pumice Foundation Network (100%):", "All 18 championship putting greens have achieved full subgrade excavation, polythene moisture barrier installation, and volcanic pumice aggregate leveling. Clean riversand foundation beds have been placed and spread across 6 priority greens (Greens 1, 2, 3, 4, 8, and 9), with Green 5 under mature turf. Greens 7 and 10–18 remain stabilized on compacted pumice sub-bases awaiting subsequent riversand consignments.")
    add_bullet_point(doc, "Precision Teebox Platforms (100%):", "All 18 championship teeboxes were completely shaped, contour-cut, and graded to designed playing corridors using the Backhoe Loader and survey elevation controls.")
    add_bullet_point(doc, "Pressurized Irrigation Pipeline Tie-In:", "The main HDPE irrigation waterline was laid inside the perimeter boundary trench connecting from the main gate to Teebox 15. On September 29, the pipeline was officially connected to Peter's water supply, immediately energizing pop-up sprinklers across Green 5.")
    add_bullet_point(doc, "Massive Material Inflow on Sep 26:", "A coordinated logistics campaign on September 26 delivered 42+ tipper lorry loads of premium red loam topsoil directly to all 18 greens and 18 tees, with 6 dedicated lorries offloaded at Green 7.")
    add_bullet_point(doc, "Perimeter Living Fence & Boundary Berms:", "Living hedge seedlings were planted along the boundary trench from the tarmac corner to Teebox 15 and extended to Gate B, with organic farmyard manure incorporated.")

    add_callout(
        doc,
        "OPERATIONAL HIGHLIGHT: GREEN 5 WATERLINE CONNECTION & AUTOMATED SPRINKLERS ACTIVE",
        "On September 29, the dedicated course irrigation pipeline was successfully tied into Peter's pressurized water supply line. "
        "Overhead rotary sprinklers were immediately operational, delivering consistent automated irrigation across Green 5's mature "
        "turfgrass cover, securing agronomic health and demonstrating full operational viability of the primary distribution line.",
        "15803D",
        "F0FDF4"
    )

    # Table 2: Heavy Machinery Log
    add_table_caption(doc, "Table 2: Heavy Machinery (Backhoe Loader) Utilization & Cost Breakdown")

    p_mach_note = doc.add_paragraph()
    p_mach_note.paragraph_format.space_before = Pt(0)
    p_mach_note.paragraph_format.space_after = Pt(4)
    r_mn = p_mach_note.add_run("Note: In accordance with reporting directives, Front Loader and Backhoe refer to the same consolidated Backhoe Loader fleet unit billed at KES 6,500.00/hr.")
    r_mn.font.name = 'Calibri'
    r_mn.font.size = Pt(8.5)
    r_mn.font.italic = True
    r_mn.font.color.rgb = RGBColor(100, 116, 139)

    mach_rows_data = [
        ("Sep 1", "Backhoe Loader (XGMA)", "Green 17 rock spreading & backfill; Teebox 7 leveling; Teebox 9 & 18 surround grading", "8.00 hrs", "KES 6,500.00", "KES 52,000.00"),
        ("Sep 2", "Backhoe Loader (XGMA)", "Fairway 4 & Green 3 soil leveling; Teebox 14 berm formation; Green 17 red soil spreading", "9.00 hrs", "KES 6,500.00", "KES 58,500.00"),
        ("Sep 3", "Backhoe Loader (XGMA)", "Fairway 1 & 2 corridor clearing; red soil distribution (Greens 10, 11, 12, 14, 15, 16)", "9.00 hrs", "KES 6,500.00", "KES 58,500.00"),
        ("Sep 4", "Backhoe Loader (Consolidated)", "Clearing & blading fairway corridors 3, 5, 6, 13, 14, 15, 16; perimeter red soil leveling", "8.50 hrs", "KES 6,500.00", "KES 55,250.00"),
        ("Sep 5", "Backhoe Loader (Consolidated)", "Loading soil trailer; clearing Fairways 11 & 12; teebox grading; perimeter fence berms", "9.00 hrs", "KES 6,500.00", "KES 58,500.00"),
        ("Sep 7", "Backhoe Loader (JCB 3DX)", "Rough shaping of Teeboxes 11 & 13; spoil pile grading (shift curtailed by mechanical failure)", "2.83 hrs", "KES 6,500.00", "KES 18,395.00"),
        ("Sep 8–18", "Fleet Standby / Maintenance", "JCB 3DX demobilized off-site for hydraulic repairs; original XGMA remobilization in transit", "0.00 hrs", "—", "KES 0.00"),
        ("Sep 19", "Backhoe Loader (XGMA)", "Dam 1 embankment soil leveling; Teebox 15 shaping; Green 6/15 soil border formation", "4.00 hrs", "KES 6,500.00", "KES 26,000.00"),
        ("Sep 20", "Backhoe Loader (XGMA)", "Reshaping both Teebox 7 platforms; Teebox 16 shaping; Green 15/10 berm; Dam 2 soil loading", "7.50 hrs", "KES 6,500.00", "KES 48,750.00"),
        ("Sep 21", "Backhoe Loader (XGMA)", "Loading ballast stone & hardcore rocks for Green 7; Dam 2 embankment earthmoving", "6.00 hrs", "KES 6,500.00", "KES 39,000.00"),
        ("Sep 22", "Backhoe Loader (XGMA)", "Reshaping Teebox 5; forming Green 14/16 berm; trenching Dam 2 perimeter & drainage outfall", "6.00 hrs", "KES 6,500.00", "KES 39,000.00"),
        ("Sep 23", "Backhoe Loader (XGMA)", "Reshaping Teebox 4 platform; loading dumped red soil at gate; raising Green 14 berm", "7.00 hrs", "KES 6,500.00", "KES 45,500.00"),
        ("Sep 24", "Backhoe Loader (Consolidated)", "Reshaping Teeboxes 1, 2, 3; Green 4 surround leveling; Green 10 hill shaping; rock loading", "9.00 hrs", "KES 6,500.00", "KES 58,500.00"),
        ("Sep 25", "Backhoe Loader (Consolidated)", "Reshaping Teeboxes 17 & 13; Tee 16/Green 16 barrier; Green 18 mound design; palm hole digging", "8.50 hrs", "KES 6,500.00", "KES 55,250.00"),
        ("Sep 26", "Backhoe Loader (XGMA)", "Spreading excavated septic tank soil at Chaka farm; uprooting bushes; golf earthwork support", "3.00 hrs", "KES 6,500.00", "KES 19,500.00"),
    ]

    t2 = doc.add_table(rows=len(mach_rows_data) + 2, cols=6)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2.autofit = False
    set_table_borders(t2, "CBD5E1")

    t2_headers = ["Date", "Equipment Model", "Assigned Operational Scope", "Hours", "Billing Rate", "Total Spend"]
    t2_widths = [Inches(0.9), Inches(1.3), Inches(2.3), Inches(0.7), Inches(0.8), Inches(0.8)]

    hdr_r = t2.rows[0]
    make_row_header(hdr_r)
    make_row_cant_split(hdr_r)
    for idx, name in enumerate(t2_headers):
        c = hdr_r.cells[idx]
        c.width = t2_widths[idx]
        set_cell_background(c, "0F172A")
        set_cell_margins(c, 80, 80, 100, 100)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(name)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        if idx >= 3:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    for r_idx, row_data in enumerate(mach_rows_data):
        row = t2.rows[r_idx + 1]
        make_row_cant_split(row)
        bg = "FFF5F5" if "Sep 8–18" in row_data[0] else ("FAFBFD" if r_idx % 2 == 1 else "FFFFFF")
        for c_idx in range(6):
            c = row.cells[c_idx]
            c.width = t2_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, 60, 60, 100, 100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(row_data[c_idx])
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)
            elif c_idx == 5:
                r.bold = True
                r.font.color.rgb = RGBColor(185, 28, 28) if "Sep 8–18" in row_data[0] else RGBColor(15, 23, 42)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)
            if c_idx >= 3:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # Footer total row
    tot_row = t2.rows[-1]
    make_row_cant_split(tot_row)
    for c_idx in range(6):
        c = tot_row.cells[c_idx]
        c.width = t2_widths[c_idx]
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, 80, 80, 100, 100)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        if c_idx == 0:
            r = p.add_run("TOTAL")
            r.bold = True
            r.font.name = 'Calibri'
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(15, 23, 42)
        elif c_idx == 1:
            r = p.add_run("14 Active Days")
            r.bold = True
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(15, 23, 42)
        elif c_idx == 2:
            r = p.add_run("Consolidated Course Earthmoving & Shaping")
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(71, 85, 105)
        elif c_idx == 3:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r = p.add_run("97.33 hrs")
            r.bold = True
            r.font.name = 'Calibri'
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(21, 128, 61)
        elif c_idx == 4:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r = p.add_run("Avg 6.95h/d")
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(71, 85, 105)
        elif c_idx == 5:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r = p.add_run("KES 632,645.00")
            r.bold = True
            r.font.name = 'Calibri'
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(21, 128, 61)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # --------------------------------------------------------------------------
    # TABLE 3: GREENS STATUS AUDIT (18 GREENS)
    # --------------------------------------------------------------------------
    doc.add_page_break()
    add_heading_2(doc, "2.2 Comprehensive Championship Putting Greens Status Audit (Greens 1 – 18)", (21, 128, 61))
    
    p_gr_note = doc.add_paragraph()
    p_gr_note.paragraph_format.space_before = Pt(0)
    p_gr_note.paragraph_format.space_after = Pt(6)
    p_gr_note.paragraph_format.line_spacing = 1.15
    r_gn = p_gr_note.add_run(
        "In accordance with agronomic auditing standards, the table below reflects the technical and subgrade state of each "
        "putting green as of September 30, 2026. Only the latest verified activity is cited per hole using direct, plain vocabulary."
    )
    r_gn.font.name = 'Calibri'
    r_gn.font.size = Pt(9.5)
    r_gn.font.color.rgb = RGBColor(71, 85, 105)

    greens_audit_data = [
        ("Green 1", "Surplus red soil spread around outer surrounds and leveled (Sep 30). Subgrade drainage and pumice bed complete.", "Surplus Red Soil Applied"),
        ("Green 2", "Surplus red soil spread around green collar and surrounds (Sep 30). Foundation membrane and drainage intact.", "Surplus Red Soil Applied"),
        ("Green 3", "Received 1 lorry red soil; drainage outlet alignment marked (Sep 26); clean riversand layer spread across bed.", "Riversand Applied"),
        ("Green 4", "Received 1 lorry red soil; drainage outlet alignment marked (Sep 26); surrounding soils leveled with fairway.", "Surrounds Leveled"),
        ("Green 5", "Water pipeline connected from Peter's supply; overhead sprinklers running on mature grass (Sep 29).", "Turf Ready · Sprinklers Active"),
        ("Green 6", "Surplus red soil applied to raise and level surrounds (Sep 28); perimeter palm trees planted.", "Apron Raised · Palms Placed"),
        ("Green 7", "Volcanic pumice spread and leveled across green bed (Sep 28); received 6 dedicated lorries of red topsoil.", "Pumice Leveled · Soil In"),
        ("Green 8", "Received 1 lorry red soil; drainage outlet alignment marked (Sep 26); riversand applied across base.", "Riversand Applied"),
        ("Green 9", "Clean riversand application completed across surface (Sep 23); received 1 lorry red soil (Sep 26).", "Riversand Applied"),
        ("Green 10", "Surplus red soil spread around green collar and surrounds (Sep 30); stockpiled soil hill shaped.", "Surplus Red Soil Applied"),
        ("Green 11", "Surplus red soil spread and leveled around surrounds (Sep 30); pumice compacted with vibratory roller.", "Surplus Red Soil Applied"),
        ("Green 12", "Surplus red soil spread and leveled around surrounds (Sep 30); volcanic pumice foundation bed leveled.", "Surplus Red Soil Applied"),
        ("Green 13", "Surplus red soil spread around surrounds to raise and match green level (Sep 29).", "Surplus Red Soil Applied"),
        ("Green 14", "Surplus red soil spread around surrounds to build up perimeter level (Sep 29); barrier berm raised.", "Surplus Red Soil Applied"),
        ("Green 15", "Surplus red soil spread around surrounds to raise perimeter level (Sep 28); drainage connected to Dam 1.", "Apron Raised · Compacted"),
        ("Green 16", "Surplus red soil spread around surrounds to blend with fairway (Sep 29); barrier berm reinforced.", "Surplus Red Soil Applied"),
        ("Green 17", "Surplus red soil spread around surrounds to raise and align levels (Sep 29); protective barrier reshaped.", "Surplus Red Soil Applied"),
        ("Green 18", "Surplus red soil spread and leveled around collar and surrounds (Sep 30); adjacent mound reshaped.", "Surplus Red Soil Applied"),
    ]

    add_table_caption(doc, "Table 3: Championship Putting Greens Agronomic & Structural Status Audit (Greens 1 – 18)")

    t3 = doc.add_table(rows=len(greens_audit_data) + 1, cols=3)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t3.autofit = False
    set_table_borders(t3, "CBD5E1")

    t3_widths = [Inches(1.2), Inches(4.0), Inches(1.7)]
    t3_headers = ["Green ID", "Current Technical & Agronomic State (as of Sep 30)", "Milestone Status"]

    hdr_g = t3.rows[0]
    make_row_header(hdr_g)
    make_row_cant_split(hdr_g)
    for idx, name in enumerate(t3_headers):
        c = hdr_g.cells[idx]
        c.width = t3_widths[idx]
        set_cell_background(c, "0F172A")
        set_cell_margins(c, 80, 80, 100, 100)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(name)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, row_data in enumerate(greens_audit_data):
        row = t3.rows[r_idx + 1]
        make_row_cant_split(row)
        bg = "F0FDF4" if "Sep 30" in row_data[1] else ("FAFBFD" if r_idx % 2 == 1 else "FFFFFF")
        for c_idx in range(3):
            c = row.cells[c_idx]
            c.width = t3_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, 50, 50, 90, 90)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.12
            r = p.add_run(row_data[c_idx])
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(21, 128, 61)
            elif c_idx == 2:
                r.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    add_callout(
        doc,
        "OPERATIONS AGRONOMIC SYNTHESIS — PUTTING GREENS (18 HOLES)",
        "• 100% Subgrade & Pumice Sub-Bases (18 of 18 Greens): All 18 championship putting greens have achieved complete subgrade excavation, polythene moisture barrier lining, herringbone perforated PVC drainage installations, and volcanic pumice aggregate leveling.\n"
        "• Active Championship Turfgrass Cover (1 Green): Green 5 features fully established mature championship turfgrass with dedicated water supply connected to Peter's pressurized line and automated rotary pop-up sprinklers active.\n"
        "• Clean Riversand Foundation Beds Placed (6 Greens): Clean riversand has been hauled, spread, and leveled across 6 priority greens (Greens 1, 2, 3, 4, 8, and 9).\n"
        "• Compacted Pumice Beds with Apron Contouring (11 Greens): Greens 7 and 10–18 are stabilized on compacted volcanic pumice sub-bases over drainage lines, with surplus red loam topsoil spread around their collars, aprons, and surrounds (Sep 28–30) to blend with fairway grades, awaiting subsequent riversand consignments.",
        "15803D",
        "F0FDF4"
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # --------------------------------------------------------------------------
    # TABLE 4: TEEBOXES STATUS AUDIT (18 TEES)
    # --------------------------------------------------------------------------
    doc.add_page_break()
    add_heading_2(doc, "2.3 Championship Teeboxes Platform Construction Status (Tees 1 – 18)", (21, 128, 61))

    tees_audit_data = [
        ("Tee 1", "Championship launch platform completely reshaped, cut, and graded using Backhoe Loader (Sep 24); received 1 lorry red soil (Sep 26).", "Platform Reshaped"),
        ("Tee 2", "Playing launch platform completely reshaped, contoured, and graded using Backhoe Loader (Sep 24); received 1 lorry red soil (Sep 26).", "Platform Reshaped"),
        ("Tee 3", "Playing launch platform completely reshaped, contoured, and graded using Backhoe Loader (Sep 24); received 1 lorry red soil (Sep 26).", "Platform Reshaped"),
        ("Tee 4", "Championship launch platform completely reshaped, cut, and graded using Backhoe Loader (Sep 23); received 1 lorry red soil (Sep 26).", "Platform Reshaped"),
        ("Tee 5", "Main perimeter drainage pipeline backfilled and covered up to Teebox 5 (Sep 30); boundary palm trees planted.", "Drainage Backfilled"),
        ("Tee 6", "Precision leveling and compaction completed; fresh delivery of 1 lorry red loam topsoil unloaded at platform surrounds (Sep 26).", "Red Soil In · Leveled"),
        ("Tee 7", "Dual launch platforms completely reshaped and precision contour-leveled using XGMA backhoe loader (Sep 20); received 1 lorry red soil (Sep 26).", "Dual Platforms Reshaped"),
        ("Tee 8", "Graded, leveled, and contour-adjusted; fresh delivery of 1 lorry red loam topsoil unloaded directly on platform (Sep 26).", "Red Soil In · Graded"),
        ("Tee 9", "Playing platform leveled and surrounding perimeter ground graded (Sep 1); received 1 lorry red soil delivery (Sep 26).", "Platform Leveled"),
        ("Tee 10", "Graded and compacted platform serving start of back-nine playing corridor; received 1 lorry red soil delivery (Sep 26).", "Platform Compacted"),
        ("Tee 11", "Rough shaping, elevation grading, and Backhoe subsoil leveling completed (Sep 7); received 1 lorry red soil delivery (Sep 26).", "Shaped & Graded"),
        ("Tee 12", "Dual platforms established: primary championship tee resized; new forward Ladies' Tee platform constructed (Sep 5); received 1 lorry red soil.", "Dual Platforms Complete"),
        ("Tee 13", "Playing platform completely reshaped, contour-cut, and precision leveled using Backhoe Loader (Sep 25); received 1 lorry red soil (Sep 26).", "Platform Reshaped"),
        ("Tee 14", "Playing platform reshaped, elevation precision-leveled, and protective boundary embankment reinforced (Sep 16); received 1 lorry red soil (Sep 26).", "Reshaped & Leveled"),
        ("Tee 15", "Playing platform completely shaped and contour-leveled (Sep 19); received 1 lorry red soil (Sep 26); main HDPE waterline laid in trench (Sep 15).", "Shaped & Leveled"),
        ("Tee 16", "Protective earthen boundary barrier between Tee 16 and Green 16 reshaped, graded, and reinforced using Backhoe Loader (Sep 25); received 1 lorry soil.", "Barrier Berm Reworked"),
        ("Tee 17", "Championship launch platform completely reshaped, contour-cut, and precision-graded using Backhoe Loader (Sep 25); received 1 lorry soil.", "Platform Reshaped"),
        ("Tee 18", "Championship tee platform leveled; perimeter approach cleared and graded (Sep 1); received 1 lorry red soil delivery (Sep 26).", "Platform Leveled"),
    ]

    add_table_caption(doc, "Table 4: Championship Teeboxes Platform Construction Status (Tees 1 – 18)")

    t4 = doc.add_table(rows=len(tees_audit_data) + 1, cols=3)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    t4.autofit = False
    set_table_borders(t4, "CBD5E1")

    t4_widths = [Inches(1.2), Inches(4.0), Inches(1.7)]
    t4_headers = ["Teebox ID", "Current Technical & Earthwork State (as of Sep 30)", "Platform Status"]

    hdr_t = t4.rows[0]
    make_row_header(hdr_t)
    make_row_cant_split(hdr_t)
    for idx, name in enumerate(t4_headers):
        c = hdr_t.cells[idx]
        c.width = t4_widths[idx]
        set_cell_background(c, "0F172A")
        set_cell_margins(c, 80, 80, 100, 100)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(name)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, row_data in enumerate(tees_audit_data):
        row = t4.rows[r_idx + 1]
        make_row_cant_split(row)
        bg = "F0FDF4" if "Sep 30" in row_data[1] else ("FAFBFD" if r_idx % 2 == 1 else "FFFFFF")
        for c_idx in range(3):
            c = row.cells[c_idx]
            c.width = t4_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, 50, 50, 90, 90)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.12
            r = p.add_run(row_data[c_idx])
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(21, 128, 61)
            elif c_idx == 2:
                r.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Table 5: Material Deliveries
    add_table_caption(doc, "Table 5: Major Material Inflow & Course Logistics Summary")

    materials_data = [
        ("Red Loam Topsoil", "42+ Tipper Lorries (Sep 26 delivery)", "Quarry Supply", "All 18 greens & 18 tees (1 lorry each); 6 dedicated lorries offloaded on Green 7 for precision subgrade dressing."),
        ("Clean Riversand", "3 Commercial Tipper Lorries", "Commercial River Quarry", "Applied and leveled across Green 1 foundation bed; central stockpile staged for remaining green surfaces."),
        ("Volcanic Pumice Stone", "Multiple Heavy Tipper Loads", "Local Volcanic Source", "Delivered and leveled as drainage aggregate across active putting green foundation grids."),
        ("Hardcore Rocks", "Internal Borrow Pit & Hauled Stockpiles", "Internal Golf Site", "Trench stabilization, subgrade rock packing, and structural sub-base across Greens 7, 14, 15, 16, 17."),
        ("Ballast Stone", "Consignment Batches", "Commercial Quarry", "Infill placed directly atop slit PVC drainage lines inside herringbone trenches across Green 7 and surrounds."),
        ("HDPE Waterline & PVC Pipes", "Multiple Coils & Slit Batches", "Plumbing Supply & Chaka", "Main 2.5-inch HDPE distribution pipe laid to Tee 15; perforated PVC drainage lines net-wrapped and buried."),
        ("Polythene Moisture Membrane", "Heavy-Duty Rolls (1,000 gauge)", "Specialist Supplier", "Installed beneath all green foundations; deployed across Dam 1 channel basin for water containment."),
    ]

    t5 = doc.add_table(rows=len(materials_data) + 1, cols=4)
    t5.alignment = WD_TABLE_ALIGNMENT.CENTER
    t5.autofit = False
    set_table_borders(t5, "CBD5E1")

    t5_widths = [Inches(1.5), Inches(1.5), Inches(1.2), Inches(2.7)]
    t5_headers = ["Material Classification", "Quantity Received", "Supply Source", "Application Zone & Purpose"]

    hdr_m = t5.rows[0]
    make_row_header(hdr_m)
    make_row_cant_split(hdr_m)
    for idx, name in enumerate(t5_headers):
        c = hdr_m.cells[idx]
        c.width = t5_widths[idx]
        set_cell_background(c, "0F172A")
        set_cell_margins(c, 80, 80, 100, 100)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(name)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, row_data in enumerate(materials_data):
        row = t5.rows[r_idx + 1]
        make_row_cant_split(row)
        bg = "FAFBFD" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx in range(4):
            c = row.cells[c_idx]
            c.width = t5_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, 60, 60, 100, 100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.12
            r = p.add_run(row_data[c_idx])
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # --------------------------------------------------------------------------
    # SECTION 4: CHAKA FARMS
    # --------------------------------------------------------------------------
    doc.add_page_break()
    add_heading_1(doc, "3. Chaka Farms — Dairy Production, Livestock & Canine Unit")

    add_heading_2(doc, "3.1 Reconciled Dairy Production & Financial Ground Truth", (217, 119, 6))

    p_f_lead = doc.add_paragraph()
    p_f_lead.paragraph_format.space_before = Pt(2)
    p_f_lead.paragraph_format.space_after = Pt(4)
    p_f_lead.paragraph_format.line_spacing = 1.15
    r_fl = p_f_lead.add_run(
        "Agricultural and dairy production at Chaka Farms operated under the direct supervision of Kamandau (Dairy & Milking), "
        "Willy (Canine Unit & Farm Maintenance), and Margaret & Monica (Compound & Horticulture). "
        "A formal milk accounting audit completed for September established complete reconciliation between commercial field sales "
        "and internal farm nutrition rations."
    )
    r_fl.font.name = 'Calibri'
    r_fl.font.size = Pt(10)
    r_fl.font.color.rgb = RGBColor(51, 65, 85)

    add_callout(
        doc,
        "OPERATIONAL CLARIFICATION: SEPTEMBER MILK PRODUCTION RECONCILIATION",
        "In earlier daily field reporting, the morning and evening milk figures logged by Kamandau were recorded as total gross harvest. "
        "An operational audit confirmed that those daily numbers represented the milk SOLD/DISPATCHED for commercial distribution. "
        "The routine 2.0 Litres disbursed daily on-farm (1.0L to goat kids, 0.5L to Gladys, 0.5L to Maasai security) were distributed "
        "directly on-farm IN ADDITION to commercial sales.\n"
        "Ground Truth: No milk was lost or misplaced. The herd produced 215.0 Litres (54.5 Litres more than earlier paper totals), "
        "delivering 160.5 Litres in commercial revenue and 54.5 Litres in vital livestock and staff nutrition with 100% accounting fidelity.",
        "D97706",
        "FFFBEB"
    )

    # Table 6: Dairy Production Ledger
    add_table_caption(doc, "Table 6: Reconciled Monthly Dairy Production & Allocation Ledger (September 2026)")

    dairy_data = [
        ("Week 1 (Sep 1 – 7)", "46.0 L", "7.0 L", "4.0 L", "11.0 L", "57.0 L", "8.14 L/day"),
        ("Week 2 (Sep 8 – 14)", "37.0 L", "7.0 L", "6.5 L", "13.5 L", "50.5 L", "7.21 L/day"),
        ("Week 3 (Sep 15 – 21)", "34.0 L", "7.0 L", "6.0 L", "13.0 L", "47.0 L", "6.71 L/day"),
        ("Week 4 (Sep 22 – 28)", "34.0 L", "7.0 L", "6.5 L", "13.5 L", "47.5 L", "6.79 L/day"),
        ("Final Days (Sep 29 – 30)", "9.5 L", "2.0 L", "1.5 L", "3.5 L", "13.0 L", "6.50 L/day"),
    ]

    t6 = doc.add_table(rows=len(dairy_data) + 2, cols=7)
    t6.alignment = WD_TABLE_ALIGNMENT.CENTER
    t6.autofit = False
    set_table_borders(t6, "CBD5E1")

    t6_widths = [Inches(1.5), Inches(0.9), Inches(0.8), Inches(0.9), Inches(0.9), Inches(0.9), Inches(1.0)]
    t6_headers = ["Period", "Milk Sold", "Kids Ration", "Staff & Security", "Farm Total", "Gross Harvest", "Daily Avg"]

    hdr_d = t6.rows[0]
    make_row_header(hdr_d)
    make_row_cant_split(hdr_d)
    for idx, name in enumerate(t6_headers):
        c = hdr_d.cells[idx]
        c.width = t6_widths[idx]
        set_cell_background(c, "0F172A")
        set_cell_margins(c, 80, 80, 80, 80)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(name)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        if idx >= 1:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    for r_idx, row_data in enumerate(dairy_data):
        row = t6.rows[r_idx + 1]
        make_row_cant_split(row)
        bg = "FAFBFD" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx in range(7):
            c = row.cells[c_idx]
            c.width = t6_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, 60, 60, 80, 80)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(row_data[c_idx])
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)
            elif c_idx == 1:
                r.bold = True
                r.font.color.rgb = RGBColor(29, 78, 216)
            elif c_idx == 4:
                r.bold = True
                r.font.color.rgb = RGBColor(217, 119, 6)
            elif c_idx == 5:
                r.bold = True
                r.font.color.rgb = RGBColor(21, 128, 61)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)
            if c_idx >= 1:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # Footer total row
    tot_d = t6.rows[-1]
    make_row_cant_split(tot_d)
    tot_vals = ["FULL MONTH TOTAL", "160.5 L", "29.0 L", "25.5 L", "54.5 L", "215.0 L", "7.17 L/day"]
    for c_idx in range(7):
        c = tot_d.cells[c_idx]
        c.width = t6_widths[c_idx]
        set_cell_background(c, "FEF3C7")
        set_cell_margins(c, 80, 80, 80, 80)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(tot_vals[c_idx])
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(180, 83, 9) if c_idx == 4 else (RGBColor(21, 128, 61) if c_idx == 5 else RGBColor(15, 23, 42))
        if c_idx >= 1:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 4.2 Livestock Program
    add_heading_2(doc, "3.2 Livestock Census, Nutrition & Preventive Health Program", (217, 119, 6))

    add_table_caption(doc, "Table 7: Livestock Census, Nutrition & Preventive Health Log")

    livestock_data = [
        ("Dairy Cattle Herd", "Lactating cows (Thabu & herd) + heifers", "Daily Napier grass, mineral licks, concentrates; weekly acaricide knapsack spraying against ticks; zero mastitis cases."),
        ("Dorper Sheep Flock", "Breeding ewes, rams, and weaned lambs", "Rotational grazing in dedicated paddock corridors; regular flock deworming; pen bedding cleaned & refreshed."),
        ("Goat Herd & Kids", "Doe herd + nursery flock of young kids", "Receives 1.0L daily milk allocation (0.5L AM / 0.5L PM) in nursery pen; vibrant growth; zero parasite mortality."),
        ("Working Canine Unit", "Guard & estate patrol working dogs", "Daily commercial kibble + meat broth; scheduled flea/tick bathing; clean kennel housing under Willy's care."),
    ]

    t7 = doc.add_table(rows=len(livestock_data) + 1, cols=3)
    t7.alignment = WD_TABLE_ALIGNMENT.CENTER
    t7.autofit = False
    set_table_borders(t7, "CBD5E1")

    t7_widths = [Inches(1.6), Inches(1.8), Inches(3.5)]
    t7_headers = ["Livestock Category", "Flock / Herd Composition", "Nutrition, Healthcare & Management Regime"]

    hdr_l = t7.rows[0]
    make_row_header(hdr_l)
    make_row_cant_split(hdr_l)
    for idx, name in enumerate(t7_headers):
        c = hdr_l.cells[idx]
        c.width = t7_widths[idx]
        set_cell_background(c, "0F172A")
        set_cell_margins(c, 80, 80, 100, 100)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(name)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, row_data in enumerate(livestock_data):
        row = t7.rows[r_idx + 1]
        make_row_cant_split(row)
        bg = "FAFBFD" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx in range(3):
            c = row.cells[c_idx]
            c.width = t7_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, 60, 60, 100, 100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.12
            r = p.add_run(row_data[c_idx])
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 4.3 Canine Program
    add_heading_2(doc, "3.3 Working Canine Unit Care, Training & Exercise Routines", (217, 119, 6))

    add_table_caption(doc, "Table 8: Working Canine Unit Daily Routine & Training Schedule (Supervised by Willy)")

    canine_data = [
        ("06:30 – 07:30", "Morning Sanitation & Feeding", "Kennel stalls thoroughly cleaned, disinfected, and washed; fresh water provided; morning kibble rations served."),
        ("09:00 – 10:30", "Grooming & Health Checks", "Coat brushing, ear inspection, paw checks, and routine medicated tick/flea baths to maintain optimal skin health."),
        ("11:00 – 12:30", "Obedience & Manners Drills", "Structured leash training, crate manners, basic command drills (heel, sit, stay, recall) to reinforce disciplined behavior."),
        ("15:00 – 16:30", "Off-Leash Paddock Exercise", "Pack exercise and agility runs across farm paddocks and perimeter avenues to ensure physical stamina and mental stimulation."),
        ("17:00 – 18:00", "Livestock Socialization & Lock-Up", "Controlled desensitization around goat and sheep pens to prevent chasing; evening meal; secure lock-up for night guard duty."),
    ]

    t8 = doc.add_table(rows=len(canine_data) + 1, cols=3)
    t8.alignment = WD_TABLE_ALIGNMENT.CENTER
    t8.autofit = False
    set_table_borders(t8, "CBD5E1")

    t8_widths = [Inches(1.4), Inches(2.0), Inches(3.5)]
    t8_headers = ["Time Window", "Operational Protocol", "Training Scope & Veterinary Standards"]

    hdr_k = t8.rows[0]
    make_row_header(hdr_k)
    make_row_cant_split(hdr_k)
    for idx, name in enumerate(t8_headers):
        c = hdr_k.cells[idx]
        c.width = t8_widths[idx]
        set_cell_background(c, "0F172A")
        set_cell_margins(c, 80, 80, 100, 100)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(name)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, row_data in enumerate(canine_data):
        row = t8.rows[r_idx + 1]
        make_row_cant_split(row)
        bg = "FAFBFD" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx in range(3):
            c = row.cells[c_idx]
            c.width = t8_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, 60, 60, 100, 100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.12
            r = p.add_run(row_data[c_idx])
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # --------------------------------------------------------------------------
    # SECTION 5: KABETE RESIDENCE
    # --------------------------------------------------------------------------
    doc.add_page_break()
    add_heading_1(doc, "4. Kabete Residence — Infrastructure, Civil Works & Pet Care")

    add_heading_2(doc, "4.1 Structural Upgrades, Painting & Civil Renovations", (109, 40, 217))

    p_k_lead = doc.add_paragraph()
    p_k_lead.paragraph_format.space_before = Pt(2)
    p_k_lead.paragraph_format.space_after = Pt(4)
    p_k_lead.paragraph_format.line_spacing = 1.15
    r_kl = p_k_lead.add_run(
        "Field operations at Kabete Residence focused on extensive facility renovations, civil demolition, and specialized structural "
        "modifications. Operations were overseen and updates shared by Njoki, who coordinates daily field execution and communicates "
        "progress updates across all residential works."
    )
    r_kl.font.name = 'Calibri'
    r_kl.font.size = Pt(10)
    r_kl.font.color.rgb = RGBColor(51, 65, 85)

    add_bullet_point(doc, "Main House Roof Painting (100% Complete):", "The comprehensive roof restoration project was fully completed in September. Works encompassed high-pressure power washing of all concrete roof tiles, fungicidal wash treatment, primer application, and two full coats of weather-resistant protective roof paint.")
    add_bullet_point(doc, "Ancillary Roof Restorations (100%):", "Protective recoating of the main carport canopy framework and generator/mower house roof was fully executed, preventing corrosion and matching main residence aesthetics.")
    add_bullet_point(doc, "Outdoor Fireplace Excavation & Footings:", "Deep excavation of the bank embankment behind the outdoor fireplace was completed; foundational footings were widened, loose soil spoil cleared, and masonry retaining walls prepped.")
    add_bullet_point(doc, "Main Water Storage Tank Slab:", "Site clearance and foundation excavation completed; steel reinforcement starter bars (rebar) were precision-bent and arranged for the heavy concrete foundation slab.")
    add_bullet_point(doc, "Cold Room Facility Upgrades:", "Ventilation apertures were cut through exterior masonry walls to support temperature regulation; heavy-duty industrial shelving racks were assembled and installed.")

    add_callout(
        doc,
        "CAPITAL WORKS MILESTONE: 100% ROOF RENOVATION COMPLETED AT KABETE RESIDENCE",
        "The multi-stage roof rehabilitation program at Kabete Residence concluded with 100% completion across all target structures: "
        "the main residential house, the two-vehicle carport canopy, and the auxiliary generator/lawnmower utility building. "
        "All tile surfaces and structural frameworks are fully sealed against weather ingress, providing long-term structural protection.",
        "6D28D9",
        "F5F3FF"
    )

    # Table 9: Kabete Milestones
    add_table_caption(doc, "Table 9: Kabete Residence Capital Improvement & Infrastructure Milestones")

    kabete_data = [
        ("Main House Roof", "Tile cleaning, antifungal wash, primer, and double-coat protective painting", "100%", "Completed"),
        ("Carport Canopy", "Metal framework rust-treatment, timber under-ceiling prep, and recoating", "100%", "Completed"),
        ("Generator & Mower Shed", "Roof cleaning, sealing, and exterior weatherproof enamel painting", "100%", "Completed"),
        ("Outdoor Fireplace", "Embankment excavation, footing widening, rubble clearance, and retaining wall prep", "85%", "Footings Ready"),
        ("Water Tank Foundation Slab", "Sub-base excavation, leveling, and starter column rebar bending & assembly", "75%", "Rebar Assembled"),
        ("Cold Room Facility", "Exterior wall ventilation cut-outs, shelving fit-out, and access drainage clearance", "90%", "Shelves Installed"),
        ("Playground & Compound", "Red loam topsoil spreading, leveling, and safety debris clearance", "100%", "Cleared & Graded"),
    ]

    t9 = doc.add_table(rows=len(kabete_data) + 1, cols=4)
    t9.alignment = WD_TABLE_ALIGNMENT.CENTER
    t9.autofit = False
    set_table_borders(t9, "CBD5E1")

    t9_widths = [Inches(1.8), Inches(3.0), Inches(0.9), Inches(1.2)]
    t9_headers = ["Project Component", "Engineering Scope & Activity Description", "Completion", "Status"]

    hdr_kb = t9.rows[0]
    make_row_header(hdr_kb)
    make_row_cant_split(hdr_kb)
    for idx, name in enumerate(t9_headers):
        c = hdr_kb.cells[idx]
        c.width = t9_widths[idx]
        set_cell_background(c, "0F172A")
        set_cell_margins(c, 80, 80, 100, 100)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(name)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        if idx == 2:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    for r_idx, row_data in enumerate(kabete_data):
        row = t9.rows[r_idx + 1]
        make_row_cant_split(row)
        bg = "FAFBFD" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx in range(4):
            c = row.cells[c_idx]
            c.width = t9_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, 60, 60, 100, 100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.12
            r = p.add_run(row_data[c_idx])
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)
            elif c_idx == 3:
                r.bold = True
                r.font.color.rgb = RGBColor(21, 128, 61) if "Completed" in row_data[3] else RGBColor(109, 40, 217)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)
            if c_idx == 2:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 5.2 Domestic Pets Care
    add_heading_2(doc, "4.2 Domestic Pets Welfare — Ajabu the Golden Retriever & Resident Cats", (109, 40, 217))
    
    p_pet = doc.add_paragraph()
    p_pet.paragraph_format.space_before = Pt(2)
    p_pet.paragraph_format.space_after = Pt(4)
    p_pet.paragraph_format.line_spacing = 1.15
    r_pt = p_pet.add_run(
        "Domestic pets belonging strictly to Kabete Residence—specifically Ajabu the Golden Retriever and the resident feline family "
        "(Reo, Mocha & Aiko)—received attentive daily welfare and veterinary management throughout September:"
    )
    r_pt.font.name = 'Calibri'
    r_pt.font.size = Pt(10)
    r_pt.font.color.rgb = RGBColor(51, 65, 85)

    add_bullet_point(doc, "Ajabu (Golden Retriever):", "Maintained excellent energy, vibrant coat condition, and calm demeanor through regular daily walks, lawn exercise, scheduled evening nutrition, and clean bedding at the gate kennel suite.")
    add_bullet_point(doc, "Resident Cats (Reo, Mocha & Aiko):", "Received consistent daily meal disbursements, sheltered domestic sleeping quarters, and wellness observation. All three cats exhibited robust health and calm domestic bonding.")

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # --------------------------------------------------------------------------
    # SECTION 6: AMANI COTTAGE
    # --------------------------------------------------------------------------
    doc.add_page_break()
    add_heading_1(doc, "5. Amani Cottage — Turf Management & Residence Presentation")

    add_heading_2(doc, "5.1 Agronomic Lawn Care, Irrigation & Estate Housekeeping", (13, 148, 136))

    p_a_lead = doc.add_paragraph()
    p_a_lead.paragraph_format.space_before = Pt(2)
    p_a_lead.paragraph_format.space_after = Pt(4)
    p_a_lead.paragraph_format.line_spacing = 1.15
    r_al = p_a_lead.add_run(
        "Operations at Amani Cottage were executed under the supervision of Edwin (Grounds & Lawn Agronomy) and the Domestic Housekeeper. "
        "The property maintained immaculate aesthetic presentation and turf health across its expansive front lawns and woodland surrounds."
    )
    r_al.font.name = 'Calibri'
    r_al.font.size = Pt(10)
    r_al.font.color.rgb = RGBColor(51, 65, 85)

    add_bullet_point(doc, "Targeted CAN Fertilization:", "The expansive front lawn received top-dressing with Calcium Ammonium Nitrate (CAN) fertilizer, supplying essential nitrogen and calcium to promote deep root growth and vibrant emerald-green foliar color.")
    add_bullet_point(doc, "Automated Sprinkler Irrigation:", "Daily morning and evening rotary sprinkler cycles were maintained across all lawn zones, ensuring optimal moisture retention and preventing dry thatch buildup.")
    add_bullet_point(doc, "Woodland & Grounds Sanitation:", "Perimeter woodland gardens were cleared of fallen foliage, dry pine needles, and windblown debris, maintaining manicured turf borders and clean gravel walkways.")
    add_bullet_point(doc, "Interior Housekeeping Presentation:", "Interior suites, balconies, and entrance flagstones were regularly washed, polished, dusted, and dressed with fresh linens, maintaining five-star guest presentation.")

    # Table 10: Amani Cottage Cadence
    add_table_caption(doc, "Table 10: Amani Cottage Grounds & Housekeeping Operational Cadence")

    amani_data = [
        ("Front Lawn Turf", "CAN fertilizer top-dressing, mechanical mowing, and perimeter edging", "Weekly cycle", "Edwin (Grounds)"),
        ("Lawn Sprinklers", "Rotary pop-up sprinkler irrigation across front lawn zones", "Daily (AM / PM)", "Edwin (Grounds)"),
        ("Woodland Borders", "Foliage raking, deadwood clearing, and pathway sweeping", "Daily routine", "Edwin (Grounds)"),
        ("Balcony & Facade", "Balcony tile pressure-washing, stone step scrubbing, and glass wiping", "Bi-weekly", "Domestic Housekeeper"),
        ("Interior Suites", "Deep dusting, vacuuming, linen changing, and furniture staging", "Tri-weekly", "Domestic Housekeeper"),
    ]

    t10 = doc.add_table(rows=len(amani_data) + 1, cols=4)
    t10.alignment = WD_TABLE_ALIGNMENT.CENTER
    t10.autofit = False
    set_table_borders(t10, "CBD5E1")

    t10_widths = [Inches(1.6), Inches(2.8), Inches(1.1), Inches(1.4)]
    t10_headers = ["Estate Zone", "Maintenance Protocol / Scope", "Frequency", "Supervisor"]

    hdr_a = t10.rows[0]
    make_row_header(hdr_a)
    make_row_cant_split(hdr_a)
    for idx, name in enumerate(t10_headers):
        c = hdr_a.cells[idx]
        c.width = t10_widths[idx]
        set_cell_background(c, "0F172A")
        set_cell_margins(c, 80, 80, 100, 100)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(name)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, row_data in enumerate(amani_data):
        row = t10.rows[r_idx + 1]
        make_row_cant_split(row)
        bg = "FAFBFD" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx in range(4):
            c = row.cells[c_idx]
            c.width = t10_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, 60, 60, 100, 100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.12
            r = p.add_run(row_data[c_idx])
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # --------------------------------------------------------------------------
    # SECTION 7: CONSOLIDATED FINANCIALS & OUTLOOK
    # --------------------------------------------------------------------------
    doc.add_page_break()
    add_heading_1(doc, "6. Consolidated Financials & Strategic October 2026 Outlook")

    add_heading_2(doc, "6.1 Heavy Machinery Financial Reconciliation & Supervision Roster", (15, 23, 42))

    p_fin = doc.add_paragraph()
    p_fin.paragraph_format.space_before = Pt(2)
    p_fin.paragraph_format.space_after = Pt(6)
    p_fin.paragraph_format.line_spacing = 1.15
    r_fn = p_fin.add_run(
        "Consolidated machinery and capital resources deployed across September 2026 reflect disciplined budget oversight, "
        "accurate rate application (KES 6,500.00/machine hour), and zero payment during maintenance downtime intervals."
    )
    r_fn.font.name = 'Calibri'
    r_fn.font.size = Pt(10)
    r_fn.font.color.rgb = RGBColor(51, 65, 85)

    # Table 11: Consolidated Financials
    add_table_caption(doc, "Table 11: Consolidated Resource Allocation & Machinery Spend Summary")

    fin_summary_data = [
        ("Phase 1 Operations (Sep 1–5)", "Backhoe Loader (XGMA)", "43.50 hrs", "KES 6,500.00", "KES 282,750.00", "5 Active Shifts"),
        ("Phase 2 Trial (Sep 7)", "Backhoe Loader (JCB 3DX)", "2.83 hrs", "KES 6,500.00", "KES 18,395.00", "Shift Curtailed (Breakdown)"),
        ("Standby Interval (Sep 8–18)", "Off-Site Maintenance", "0.00 hrs", "KES 0.00", "KES 0.00", "Zero Charge (10 Days)"),
        ("Phase 3 Operations (Sep 19–26)", "Backhoe Loader (XGMA)", "51.00 hrs", "KES 6,500.00", "KES 331,500.00", "8 Active Shifts (Completion)"),
        ("SEPTEMBER CONSOLIDATED TOTAL", "Consolidated Fleet", "97.33 hrs", "KES 6,500.00", "KES 632,645.00", "14 Operational Shifts"),
    ]

    t11 = doc.add_table(rows=len(fin_summary_data) + 1, cols=6)
    t11.alignment = WD_TABLE_ALIGNMENT.CENTER
    t11.autofit = False
    set_table_borders(t11, "CBD5E1")

    t11_widths = [Inches(1.6), Inches(1.3), Inches(0.7), Inches(0.9), Inches(1.1), Inches(1.3)]
    t11_headers = ["Deployment Phase", "Equipment Unit", "Hours", "Billing Rate", "Total Spend", "Operational Audit"]

    hdr_f = t11.rows[0]
    make_row_header(hdr_f)
    make_row_cant_split(hdr_f)
    for idx, name in enumerate(t11_headers):
        c = hdr_f.cells[idx]
        c.width = t11_widths[idx]
        set_cell_background(c, "0F172A")
        set_cell_margins(c, 80, 80, 100, 100)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(name)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        if idx in [2, 3, 4]:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    for r_idx, row_data in enumerate(fin_summary_data):
        row = t11.rows[r_idx + 1]
        make_row_cant_split(row)
        is_tot = (r_idx == len(fin_summary_data) - 1)
        bg = "E2E8F0" if is_tot else ("FAFBFD" if r_idx % 2 == 1 else "FFFFFF")
        for c_idx in range(6):
            c = row.cells[c_idx]
            c.width = t11_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, 60, 60, 100, 100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(row_data[c_idx])
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if is_tot:
                r.bold = True
                r.font.size = Pt(9)
                r.font.color.rgb = RGBColor(21, 128, 61) if c_idx == 4 else RGBColor(15, 23, 42)
            else:
                if c_idx == 0:
                    r.bold = True
                    r.font.color.rgb = RGBColor(15, 23, 42)
                else:
                    r.font.color.rgb = RGBColor(51, 65, 85)
            if c_idx in [2, 3, 4]:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Table 12: Supervisors Directory (Dennis appropriately designated under Operations Auditing & Reporting)
    add_table_caption(doc, "Table 12: Operations Supervision & Property Management Directory")

    supervisors_data = [
        ("Mucheru World of Golf", "Ken, Mr. Gichuhi, Kinoti, Kamandau", "Earthmoving oversight, drainage surveying, material reception, contractor supervision."),
        ("Chaka Farms", "Willy (Canine & Plumbing), Kamandau (Milking), Margaret & Monica (Compound)", "Dairy herd milking, livestock nutrition, working canine unit training, compound cleaning."),
        ("Kabete Residence", "Njoki (Operational Oversight & Field Updates)", "Daily contractor coordination, building renovations, structural works, domestic pet care."),
        ("Amani Cottage", "Edwin (Grounds & Agronomy), Domestic Housekeeper (Interior)", "Front lawn CAN fertilization, automated sprinkler scheduling, grounds and interior care."),
        ("Operations Auditing & Reporting", "Dennis", "Comprehensive operational audits, daily field log verification, dairy & machinery reconciliation, and executive report compilation."),
    ]

    t12 = doc.add_table(rows=len(supervisors_data) + 1, cols=3)
    t12.alignment = WD_TABLE_ALIGNMENT.CENTER
    t12.autofit = False
    set_table_borders(t12, "CBD5E1")

    t12_widths = [Inches(1.9), Inches(2.2), Inches(2.8)]
    t12_headers = ["Project Property / Functional Domain", "Designated Lead / Supervisor(s)", "Core Operational Responsibilities"]

    hdr_s = t12.rows[0]
    make_row_header(hdr_s)
    make_row_cant_split(hdr_s)
    for idx, name in enumerate(t12_headers):
        c = hdr_s.cells[idx]
        c.width = t12_widths[idx]
        set_cell_background(c, "0F172A")
        set_cell_margins(c, 80, 80, 100, 100)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(name)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx, row_data in enumerate(supervisors_data):
        row = t12.rows[r_idx + 1]
        make_row_cant_split(row)
        bg = "FAFBFD" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx in range(3):
            c = row.cells[c_idx]
            c.width = t12_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, 60, 60, 100, 100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.12
            r = p.add_run(row_data[c_idx])
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)
            elif c_idx == 1:
                r.bold = True
                r.font.color.rgb = RGBColor(30, 58, 138)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 7.2 Strategic Next Steps
    add_heading_2(doc, "6.2 Strategic Next Steps & Priority Action Items for October 2026", (15, 23, 42))

    add_bullet_point(doc, "Mucheru World of Golf — Riversand Haulage & Grass Establishment:", "Procure, haul, and spread clean riversand across the 10 remaining greens (Greens 7 and 10–18), which currently only have volcanic pumice sub-bases and red soil aprons. With water actively flowing from Peter's supply, expand automated sprinkler lateral lines and commence stolon planting or hydroseeding across priority greens (starting with the sand-ready greens: Greens 1, 2, 3, 4, 8, 9).")
    add_bullet_point(doc, "Reservoir Liner Welding & Dam 2 Water Inflow:", "Finalize thermal welding of geomembrane dam liner sheets in Dam 1 and complete perimeter trench backfilling around Dam 2 to maximize rainwater harvesting capacity.")
    add_bullet_point(doc, "Chaka Farms — Dairy Yield Enhancement:", "Sustain high-energy silage and concentrate supplementation for lactating cows to maintain daily production above 7.5L/day; expand rotational grazing for Dorper sheep.")
    add_bullet_point(doc, "Kabete Residence — Fireplace Masonry & Tank Slab Pouring:", "Cast concrete foundation slab for the main water storage tank following rebar inspection; begin natural stone masonry lining for the outdoor fireplace.")
    add_bullet_point(doc, "Amani Cottage — Pre-Rain Lawn Conditioning:", "Apply secondary aerating and light organic dressing to the front lawn prior to expected seasonal rains to ensure deep root penetration.")

    doc.add_paragraph().paragraph_format.space_after = Pt(16)

    # SIGN-OFF BLOCK
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(14)
    p_sign.paragraph_format.space_after = Pt(2)
    p_sign.paragraph_format.keep_with_next = True
    r_so = p_sign.add_run("Compiled by Dennis")
    r_so.bold = True
    r_so.font.name = 'Calibri'
    r_so.font.size = Pt(12)
    r_so.font.color.rgb = RGBColor(15, 23, 42)

    p_sign_sub = doc.add_paragraph()
    p_sign_sub.paragraph_format.space_before = Pt(0)
    p_sign_sub.paragraph_format.space_after = Pt(6)
    r_sos = p_sign_sub.add_run("Operations Auditing & Reporting Lead")
    r_sos.font.name = 'Calibri'
    r_sos.font.size = Pt(9.5)
    r_sos.font.color.rgb = RGBColor(100, 116, 139)

    ensure_word_closed()
    doc.save(docx_path)
    print(f"Report successfully saved to: {docx_path}")
    print(f"File size: {os.path.getsize(docx_path)} bytes")

    # Use Word COM to update the Table of Contents and fields directly with Word's layout engine
    try:
        import win32com.client
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        word.DisplayAlerts = 0
        try:
            w_doc = word.Documents.Open(os.path.abspath(docx_path))
            for toc in w_doc.TablesOfContents:
                toc.Update()
            for fld in w_doc.Fields:
                fld.Update()
            w_doc.Save()
            w_doc.Close()
            print("Microsoft Word COM updated Table of Contents and dynamic pagination successfully!")
        finally:
            word.Quit()
    except Exception as e:
        print(f"Word COM update note: {e}")

    ensure_word_closed()
    shutil.copy2(docx_path, alt_docx_path)
    print(f"Report also copied to root: {alt_docx_path}")
    assert os.path.exists(alt_docx_path), "Root file does not exist!"
    assert os.path.getsize(docx_path) == os.path.getsize(alt_docx_path), "File size mismatch!"


if __name__ == "__main__":
    build_report()
