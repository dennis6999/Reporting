import os
import sys
import shutil
import subprocess

def ensure_word_closed():
    try:
        subprocess.run(['taskkill', '/F', '/IM', 'WINWORD.EXE'], capture_output=True)
    except Exception:
        pass

import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

base_dir = r"c:\Users\denni\Downloads\Reporting"
oct_dir = os.path.join(base_dir, "October 2026")
report_dir = os.path.join(oct_dir, "Monthly Report October 2026")
os.makedirs(report_dir, exist_ok=True)

docx_path = os.path.join(report_dir, "Monthly_Operations_Summary_Report_October_2026.docx")
pdf_path = os.path.join(report_dir, "Monthly_Operations_Summary_Report_October_2026.pdf")
alt_docx_path = os.path.join(oct_dir, "Monthly_Operations_Summary_Report_October_2026.docx")
alt_pdf_path = os.path.join(oct_dir, "Monthly_Operations_Summary_Report_October_2026.pdf")

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=130, right=130):
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
    p.paragraph_format.space_before = Pt(3)
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
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    run = p.runs[0]
    run.font.name = 'Calibri'
    run.font.size = Pt(16)
    run.bold = True
    run.font.color.rgb = RGBColor(15, 23, 42)
    return p

def add_heading_2(doc, text, color_rgb=(30, 58, 138)):
    p = doc.add_heading(text, level=2)
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.runs[0]
    run.font.name = 'Calibri'
    run.font.size = Pt(12.5)
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
    run.font.size = Pt(16)
    run.bold = True
    run.font.color.rgb = RGBColor(15, 23, 42)
    return p

def add_table_caption(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(10.5)
    run.bold = True
    run.font.color.rgb = RGBColor(15, 23, 42)
    return p

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

def build_report():
    doc = Document()
    
    settings = doc.settings.element
    settings.append(parse_xml(f'<w:updateFields {nsdecls("w")} w:val="true"/>'))

    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)
        
        header = s.header
        p_hdr = header.paragraphs[0]
        p_hdr.text = "MUCHERU WORLD OF GOLF & ASSOCIATED PROPERTIES   |   MONTHLY OPERATIONS AUDIT"
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_hdr.style.font.name = "Calibri"
        p_hdr.style.font.size = Pt(8.5)
        p_hdr.style.font.color.rgb = RGBColor(148, 163, 184)
        
        footer = s.footer
        p_ftr_old = footer.paragraphs[0]
        p_ftr_old.text = ""
        
        tbl_ftr = footer.add_table(rows=1, cols=2, width=Inches(6.9))
        tbl_ftr.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        c_left = tbl_ftr.cell(0, 0)
        c_left.width = Inches(4.5)
        p_fl = c_left.paragraphs[0]
        p_fl.paragraph_format.space_before = Pt(0)
        p_fl.paragraph_format.space_after = Pt(0)
        r_fl = p_fl.add_run("OCTOBER 2026 OPERATIONS REPORT   •   AUDITED & COMPILED BY DENNIS")
        r_fl.font.name = "Calibri"
        r_fl.font.size = Pt(8)
        r_fl.font.color.rgb = RGBColor(148, 163, 184)
        
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
    # COVER PAGE (PAGE 1)
    # --------------------------------------------------------------------------
    p_kicker = doc.add_paragraph()
    p_kicker.paragraph_format.space_before = Pt(8)
    p_kicker.paragraph_format.space_after = Pt(2)
    r_k = p_kicker.add_run("MONTHLY OPERATIONS AUDIT REPORT")
    r_k.bold = True
    r_k.font.name = 'Calibri'
    r_k.font.size = Pt(9.5)
    r_k.font.color.rgb = RGBColor(21, 128, 61)

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(4)
    r_t = p_title.add_run("MONTHLY OPERATIONS REPORT")
    r_t.bold = True
    r_t.font.name = 'Calibri'
    r_t.font.size = Pt(22)
    r_t.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(12)
    r_s = p_sub.add_run("Mucheru World of Golf • Chaka Farms • Kabete Residence • Amani Cottage — October 2026")
    r_s.font.name = 'Calibri'
    r_s.font.size = Pt(12)
    r_s.font.color.rgb = RGBColor(100, 116, 139)

    tbl_meta = doc.add_table(rows=2, cols=4)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_meta.autofit = False
    set_table_borders(tbl_meta, "E2E8F0")

    meta_headers = ["REPORTING PERIOD", "PRIMARY ASSETS", "LOCATIONS", "COMPILED BY"]
    meta_values = ["1st – 31st October 2026", "Golf, Farms & Residences", "Nyeri & Nairobi, Kenya", "Dennis"]

    col_w = Inches(1.72)
    for c_idx in range(4):
        c_hdr = tbl_meta.cell(0, c_idx)
        c_hdr.width = col_w
        set_cell_background(c_hdr, "F8FAFC")
        set_cell_margins(c_hdr, 60, 40, 90, 90)
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
        set_cell_margins(c_val, 50, 60, 90, 90)
        p2 = c_val.paragraphs[0]
        p2.paragraph_format.space_after = Pt(0)
        r2 = p2.add_run(meta_values[c_idx])
        r2.bold = True
        r2.font.name = 'Calibri'
        r2.font.size = Pt(9)
        r2.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Section 1 Narrative (Fits Page 1 cleanly without table)
    add_heading_1(doc, "1. Executive Summary & Month-at-a-Glance Dashboard")

    p_lead = doc.add_paragraph()
    p_lead.paragraph_format.space_before = Pt(2)
    p_lead.paragraph_format.space_after = Pt(6)
    p_lead.paragraph_format.line_spacing = 1.15
    r_ld = p_lead.add_run(
        "During October 2026, operations across all four estate properties achieved major construction, agronomic, "
        "and maintenance milestones. The golf course reached 100% pop-up sprinkler and solenoid installation, with all 18 "
        "teeboxes ready for grass planting. Chaka Farms milk production reached 227.5 Litres with 100% accounting balance. "
        "Kabete Residence completed concrete pouring for the Staff Quarters roof slab, and Amani Cottage maintained clean grounds and home presentation."
    )
    r_ld.font.name = 'Calibri'
    r_ld.font.size = Pt(10)
    r_ld.font.color.rgb = RGBColor(51, 65, 85)

    add_bullet_point(doc, "Mucheru World of Golf:", "Pop-up sprinklers and electric solenoids are 100% installed on all 18 greens and 18 tees. All 18 teeboxes have red soil applied and leveled, ready for grass planting (with shared solenoids on Tees 1 & 10 and Tees 8 & 6). All 18 greens have clean river sand applied and leveled, leaving only apron shaping around surrounds. Green 5 was finished earlier with putting and apron grass fully grown, and currently only receives scheduled watering. Dam 1 liner edges were repaired, Dam 2 was cleaned for floor liner welding, and Dam 3 received continuous water flow.")
    add_bullet_point(doc, "Chaka Farms:", "Total gross milk harvested reached 227.5 Litres across 31 days (averaging 7.34 L/day, peaking at 9.0 L/day). 194.0 Litres was sold commercially and 33.5 Litres was distributed to staff and farm rations. Exactly 100% accounted for with zero loss. Goat kids were successfully weaned on October 6th. Farm dogs received daily manners training and exercise under Willy.")
    add_bullet_point(doc, "Kabete Residence:", "Builders tied rebar, laid electrical pipes, and poured the structural concrete roof slab for the Staff Quarters (SQ). Roof tiles and gutters were cleared of fallen leaves. Domestic pets (Ajabu the Golden Retriever and resident cats Reo, Mocha, Aiko) remained healthy under Njoki's operational oversight.")
    add_bullet_point(doc, "Amani Cottage:", "The front lawn was treated with CAN fertilizer and watered regularly with rotary sprinklers to keep it green. Paved walkways were swept clean, and the two-story cottage was dusted, aired out, and kept ready for visitors.")

    # --------------------------------------------------------------------------
    # PAGE BREAK BEFORE TABLE 1: DEDICATED PAGE FOR SCORECARD (PAGE 2)
    # --------------------------------------------------------------------------
    doc.add_page_break()
    add_heading_2(doc, "Executive Performance Scorecard", (15, 23, 42))
    add_table_caption(doc, "Table 1: October 2026 Executive Performance Scorecard Across All Project Sites")

    t1 = doc.add_table(rows=5, cols=4)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1.autofit = False
    set_table_borders(t1, "CBD5E1")

    t1_headers = ["Project Site", "Primary Operational Focus", "Key Quantitative Metrics", "Month-End Status"]
    t1_widths = [Inches(1.8), Inches(2.2), Inches(1.6), Inches(1.3)]

    hdr_row = t1.rows[0]
    make_row_header(hdr_row)
    make_row_cant_split(hdr_row)
    for idx, name in enumerate(t1_headers):
        c = hdr_row.cells[idx]
        c.width = t1_widths[idx]
        set_cell_background(c, "0F172A")
        set_cell_margins(c, 100, 100, 120, 120)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(name)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    scorecard_data = [
        ("Mucheru World of Golf", "Pop-Up Sprinklers & Solenoids, River Sand Leveling, Teebox Red Soil, Dam Liners", "18 Greens Sprinklers & Solenoids (100%)\n18 Greens River Sand Leveled (100%)\n18 Tees Red Soil Leveled (100%)\n18 Tees Ready for Grass Planting", "Major Milestones Completed (100% Ready)"),
        ("Chaka Farms", "Dairy Production & Sales Reconciliation, Cow Nutrition, Canine Unit Training", "227.5L Gross Produced\n194.0L Commercial Sales\n33.5L Farm Allocations\n7.34 L/Day Herd Average", "100% Reconciled (Zero Loss)"),
        ("Kabete Residence", "SQ Roof Slab Concrete Casting, Electrical Conduits, Roof Care, Pet Welfare", "100% SQ Slab Poured\n100% Electrical Conduits Laid\nTerracotta Roof Cleaned\nDaily Pet Care (Ajabu & Cats)", "Key Structural Milestones Met"),
        ("Amani Cottage", "Front Lawn Fertilizer, Sprinkler Watering, Grounds Sweeping, Cottage Staging", "CAN Fertilizer Active\nRotary Sprinklers Active\nWoodland Grounds Swept\nInterior Sanitized & Staged", "Optimal Condition"),
    ]

    for r_idx, row_data in enumerate(scorecard_data):
        row = t1.rows[r_idx + 1]
        make_row_cant_split(row)
        bg = "FAFBFD" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx in range(4):
            c = row.cells[c_idx]
            c.width = t1_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, 90, 90, 110, 110)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(row_data[c_idx])
            r.font.name = 'Calibri'
            r.font.size = Pt(9)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)
            elif c_idx == 3:
                r.bold = True
                r.font.color.rgb = RGBColor(21, 128, 61)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # TABLE OF CONTENTS (PAGE 3)
    doc.add_page_break()
    add_toc_heading(doc, "Table of Contents")

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

    # SECTION 2: MUCHERU GOLF NARRATIVE (PAGE 4)
    doc.add_page_break()
    add_heading_1(doc, "2. Mucheru World of Golf — Course Engineering & Agronomy")
    add_heading_2(doc, "2.1 Course Civil Engineering, Irrigation Automation & Agronomy Progress", (21, 128, 61))

    p_g_lead = doc.add_paragraph()
    p_g_lead.paragraph_format.space_before = Pt(2)
    p_g_lead.paragraph_format.space_after = Pt(4)
    p_g_lead.paragraph_format.line_spacing = 1.15
    r_gl = p_g_lead.add_run(
        "Operations at Mucheru World of Golf in October achieved major milestones in course irrigation, putting green "
        "rootzones, teebox leveling, and water reservoirs under Mr. Gichuhi, Ken, Kinoti, and Kamandau:"
    )
    r_gl.font.name = 'Calibri'
    r_gl.font.size = Pt(10)
    r_gl.font.color.rgb = RGBColor(51, 65, 85)

    add_bullet_point(doc, "Pop-Up Sprinklers & Electric Solenoids Installed (100% Complete):", "Hunter pop-up sprinklers and electric water valves are installed on all 18 greens and 18 tees. Each green has its own individual solenoid. Teeboxes have all solenoids installed (with Tees 1 & 10 sharing one solenoid, and Tees 8 & 6 sharing one solenoid). Active pressurized water spray was tested and verified on Green 2, Green 5, and surrounding fairways.")
    add_bullet_point(doc, "All 18 Teeboxes Leveled & Ready for Grass Planting (100% Complete):", "Workers hauled, spread, and leveled red soil across every teebox platform. Lateral sprinkler pipes were buried, and surfaces were smoothed to the final levels, making all 18 teeboxes ready for planting grass.")
    add_bullet_point(doc, "River Sand Applied & Leveled on All 18 Greens (100% Complete):", "Clean river sand was spread and leveled across all 18 greens on top of the volcanic pumice base. The only remaining task on greens is leveling and shaping the red soil aprons around them. Green 5 was finished earlier with putting and apron grass fully grown, and currently only receives scheduled watering.")
    add_bullet_point(doc, "Water Reservoirs & Dam Liners:", "Dam 1 liner edges were repaired and welded. Dam 2 was pumped dry of dirty rainwater so workers could inspect and heat-weld the bottom liner. Fresh water flowed continuously into Dam 3 from Peter's supply pipe.")
    add_bullet_point(doc, "Drainage Trenches & Material Haulage:", "Laborers dug perimeter drainage ditches around Green 6 and shaped the main canal so water flows naturally by gravity. The farm tractor hauled pipes, cedar posts, red soil, and manure across the course.")

    add_callout(
        doc,
        "MAJOR COURSE MILESTONE: 100% SPRINKLERS ACTIVE & TEEBOXES READY FOR PLANTING",
        "Pop-up sprinklers and electric solenoids are 100% installed on all 18 greens and 18 teeboxes. All 18 teeboxes have red "
        "soil leveled and are ready for grass planting. All 18 greens have clean river sand applied and leveled, leaving only "
        "apron shaping around surrounds as the final phase (Green 5 is already fully established and only gets watered).",
        "15803D",
        "F0FDF4"
    )

    # PUTTING GREENS TABLE (PAGE 5 - DEDICATED FULL PAGE)
    doc.add_page_break()
    add_heading_2(doc, "2.2 Putting Greens Status Audit (Greens 1 – 18)", (21, 128, 61))
    add_table_caption(doc, "Table 2: 18-Hole Championship Putting Greens Technical Audit Ledger")

    t2 = doc.add_table(rows=19, cols=3)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2.autofit = False
    set_table_borders(t2, "CBD5E1")

    t2_headers = ["Green", "Current Technical & Agronomic State", "Milestone Status"]
    t2_widths = [Inches(1.1), Inches(4.3), Inches(1.5)]

    hdr_row2 = t2.rows[0]
    make_row_header(hdr_row2)
    make_row_cant_split(hdr_row2)
    for idx, name in enumerate(t2_headers):
        c = hdr_row2.cells[idx]
        c.width = t2_widths[idx]
        set_cell_background(c, "15803D")
        set_cell_margins(c, 60, 60, 90, 90)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(name)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    greens_data = [
        ("Green 1", "Pop-up sprinklers and solenoid installed; clean river sand leveled; apron shaping in progress (Oct 31).", "Riversand Leveled & Pop-Ups Active"),
        ("Green 2", "Pop-up sprinklers and solenoid installed; active water spray confirmed; river sand leveled; apron shaping in progress (Oct 31).", "Riversand Leveled & Pop-Ups Active"),
        ("Green 3", "Pop-up sprinklers and solenoid installed; river sand leveled; apron shaping in progress (Oct 31).", "Riversand Leveled & Pop-Ups Active"),
        ("Green 4", "Pop-up sprinklers and solenoid installed; water spray verified; river sand leveled; apron shaping in progress (Oct 31).", "Riversand Leveled & Pop-Ups Active"),
        ("Green 5", "Finished green; putting surface grass and apron grass fully grown and established; currently maintained under routine pop-up sprinkler watering (Oct 31).", "Fully Grown & Watered"),
        ("Green 6", "Pop-up sprinklers and solenoid installed; perimeter drainage ditch dug; river sand leveled; apron shaping ongoing (Oct 31).", "Riversand Leveled & Pop-Ups Active"),
        ("Green 7", "Pop-up sprinklers and solenoid installed; supply trench covered; river sand leveled; apron shaping in progress (Oct 31).", "Riversand Leveled & Pop-Ups Active"),
        ("Green 8", "Pop-up sprinklers and solenoid installed; river sand leveled; apron shaping in progress (Oct 31).", "Riversand Leveled & Pop-Ups Active"),
        ("Green 9", "Pop-up sprinklers and solenoid installed; river sand leveled; apron shaping in progress (Oct 31).", "Riversand Leveled & Pop-Ups Active"),
        ("Green 10", "Pop-up sprinklers and solenoid installed; 2 lorries of river sand spread and leveled; apron shaping in progress (Oct 31).", "Riversand Leveled & Pop-Ups Active"),
        ("Green 11", "Pop-up sprinklers and solenoid installed; water spray verified; river sand leveled; apron shaping in progress (Oct 31).", "Riversand Leveled & Pop-Ups Active"),
        ("Green 12", "Pop-up sprinklers and solenoid installed; river sand spread and leveled; apron shaping ongoing (Oct 31).", "Riversand Leveled & Pop-Ups Active"),
        ("Green 13", "Pop-up sprinklers and solenoid installed; water spray verified; river sand leveled; apron shaping in progress (Oct 31).", "Riversand Leveled & Pop-Ups Active"),
        ("Green 14", "Pop-up sprinklers and solenoid installed; pipe clamps fitted and trenches backfilled; river sand leveled; apron shaping ongoing (Oct 31).", "Riversand Leveled & Pop-Ups Active"),
        ("Green 15", "Pop-up sprinklers and solenoid installed; pipe clamps fitted and trenches backfilled; river sand leveled; apron shaping ongoing (Oct 31).", "Riversand Leveled & Pop-Ups Active"),
        ("Green 16", "Pop-up sprinklers and solenoid installed; river sand spread and leveled; apron shaping in progress (Oct 31).", "Riversand Leveled & Pop-Ups Active"),
        ("Green 17", "Pop-up sprinklers and solenoid installed; sprinkler trenches covered; river sand leveled; apron shaping in progress (Oct 31).", "Riversand Leveled & Pop-Ups Active"),
        ("Green 18", "Pop-up sprinklers and solenoid installed; river sand leveled; surrounds cleared for apron shaping (Oct 31).", "Riversand Leveled & Pop-Ups Active"),
    ]

    for r_idx, row_data in enumerate(greens_data):
        row = t2.rows[r_idx + 1]
        make_row_cant_split(row)
        bg = "FAFBFD" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx in range(3):
            c = row.cells[c_idx]
            c.width = t2_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, 45, 45, 80, 80)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.1
            r = p.add_run(row_data[c_idx])
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)
            elif c_idx == 2:
                r.bold = True
                r.font.color.rgb = RGBColor(21, 128, 61)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)

    # TEEBOXES TABLE (PAGE 6 - DEDICATED FULL PAGE)
    doc.add_page_break()
    add_heading_2(doc, "2.3 Championship Teeboxes Status Audit (Tees 1 – 18)", (21, 128, 61))
    add_table_caption(doc, "Table 3: 18-Hole Championship Teeboxes Technical Audit Ledger")

    t3 = doc.add_table(rows=19, cols=3)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t3.autofit = False
    set_table_borders(t3, "CBD5E1")

    t3_headers = ["Teebox", "Current Technical & Earthwork State", "Platform Status"]
    t3_widths = [Inches(1.1), Inches(4.3), Inches(1.5)]

    hdr_row3 = t3.rows[0]
    make_row_header(hdr_row3)
    make_row_cant_split(hdr_row3)
    for idx, name in enumerate(t3_headers):
        c = hdr_row3.cells[idx]
        c.width = t3_widths[idx]
        set_cell_background(c, "15803D")
        set_cell_margins(c, 60, 60, 90, 90)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(name)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    tees_data = [
        ("Tee 1", "Red soil applied and leveled; pop-up sprinklers installed; shared solenoid with Tee 10; ready for grass planting (Oct 31).", "Ready for Planting"),
        ("Tee 2", "Red soil applied and leveled; pop-up sprinklers and solenoid installed; trenches covered; ready for grass planting (Oct 31).", "Ready for Planting"),
        ("Tee 3", "Red soil applied and leveled; pop-up sprinklers and solenoid installed; trenches covered; ready for grass planting (Oct 31).", "Ready for Planting"),
        ("Tee 4", "Red soil applied and leveled; pop-up sprinklers and solenoid installed; trenches covered; ready for grass planting (Oct 31).", "Ready for Planting"),
        ("Tee 5", "Red soil applied and leveled; pop-up sprinklers and solenoid installed; trenches covered; ready for grass planting (Oct 31).", "Ready for Planting"),
        ("Tee 6", "Red soil applied and leveled; pop-up sprinklers installed; shared solenoid with Tee 8; ready for grass planting (Oct 31).", "Ready for Planting"),
        ("Tee 7", "Red soil applied and leveled; pop-up sprinklers and solenoid installed; ready for grass planting (Oct 31).", "Ready for Planting"),
        ("Tee 8", "Red soil applied and leveled; pop-up sprinklers installed; shared solenoid with Tee 6; ready for grass planting (Oct 31).", "Ready for Planting"),
        ("Tee 9", "Red soil applied and leveled; pop-up sprinklers and solenoid installed; ready for grass planting (Oct 31).", "Ready for Planting"),
        ("Tee 10", "Red soil applied and leveled; pop-up sprinklers installed; shared solenoid with Tee 1; ready for grass planting (Oct 31).", "Ready for Planting"),
        ("Tee 11", "Red soil applied and leveled; pop-up sprinklers and solenoid installed; ready for grass planting (Oct 31).", "Ready for Planting"),
        ("Tee 12", "Red soil applied and leveled; pop-up sprinklers and solenoid installed; ready for grass planting (Oct 31).", "Ready for Planting"),
        ("Tee 13", "Red soil applied and leveled; pop-up sprinklers and solenoid installed; ready for grass planting (Oct 31).", "Ready for Planting"),
        ("Tee 14", "Red soil applied and leveled; pop-up sprinklers and solenoid installed; ready for grass planting (Oct 31).", "Ready for Planting"),
        ("Tee 15", "Red soil applied and leveled; pop-up sprinklers and solenoid installed; trenches covered; ready for grass planting (Oct 31).", "Ready for Planting"),
        ("Tee 16", "Red soil applied and leveled; pop-up sprinklers and solenoid installed; trenches covered; ready for grass planting (Oct 31).", "Ready for Planting"),
        ("Tee 17", "Red soil applied and leveled; pop-up sprinklers and solenoid installed; trenches covered; ready for grass planting (Oct 31).", "Ready for Planting"),
        ("Tee 18", "Red soil applied and leveled; pop-up sprinklers and solenoid installed; trenches covered; ready for grass planting (Oct 31).", "Ready for Planting"),
    ]

    for r_idx, row_data in enumerate(tees_data):
        row = t3.rows[r_idx + 1]
        make_row_cant_split(row)
        bg = "FAFBFD" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx in range(3):
            c = row.cells[c_idx]
            c.width = t3_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, 45, 45, 80, 80)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.1
            r = p.add_run(row_data[c_idx])
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)
            elif c_idx == 2:
                r.bold = True
                r.font.color.rgb = RGBColor(21, 128, 61)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)

    # SECTION 3: CHAKA FARMS NARRATIVE (PAGE 7)
    doc.add_page_break()
    add_heading_1(doc, "3. Chaka Farms — Dairy Production, Livestock & Canine Unit")
    add_heading_2(doc, "3.1 Dairy Operations, Livestock Health & Canine Training", (217, 119, 6))

    p_f_lead = doc.add_paragraph()
    p_f_lead.paragraph_format.space_before = Pt(2)
    p_f_lead.paragraph_format.space_after = Pt(4)
    p_f_lead.paragraph_format.line_spacing = 1.15
    r_fl = p_f_lead.add_run(
        "Chaka Farms maintained steady operations in October across livestock feeding, daily milking, canine training, "
        "and general farm maintenance under Willy, Kamandau, Margaret, and Monica:"
    )
    r_fl.font.name = 'Calibri'
    r_fl.font.size = Pt(10)
    r_fl.font.color.rgb = RGBColor(51, 65, 85)

    add_bullet_point(doc, "Balanced Dairy Milk Harvest (227.5 Litres Total):", "Morning milking produced 138.5 Litres, and evening milking produced 89.0 Litres. Commercial sales totaled 194.0 Litres. Internal farm milk was 33.5 Litres (Gladys: 14.5L, Maasai: 15.0L, Goat Kids: 3.5L, Kamau: 0.5L). Every single litre is accounted for with zero loss.")
    add_bullet_point(doc, "Dairy Herd Nutrition & Yield Increase:", "Feeding cows extra silage and good pasture boosted daily milk production from 5.5L/day at the start of October to 8.0–9.0L/day during the second half of the month. Regular tick-spraying kept the cows healthy.")
    add_bullet_point(doc, "Goat Kids Weaning & Sheep Grazing:", "Goat kids were fully weaned on October 6th and are now feeding independently on grass and solid food. The Dorper sheep grazed rotationally in irrigated paddocks.")
    add_bullet_point(doc, "Working Canine Unit Training (Under Willy):", "Farm dogs received daily kennel cleaning, obedience training, and afternoon off-leash walks across the farm. Dogs practiced socializing around the goat herd to encourage calm behavior.")
    add_bullet_point(doc, "Estate Drainage & Compound Maintenance:", "Farm plumbers repaired and cleaned the wastewater pipes at the main house and installed protective cleanout fittings. Margaret and Monica kept the compound, lawns, and gardens clean.")

    # --------------------------------------------------------------------------
    # TABLE 4: DEDICATED FULL PAGE FOR DAIRY RECONCILIATION SUMMARY (PAGE 8)
    # Generous row spacing, large 10pt/10.5pt fonts, plenty of breathing room!
    # --------------------------------------------------------------------------
    doc.add_page_break()
    add_heading_2(doc, "3.2 Monthly Dairy Reconciliation Summary Ledger", (217, 119, 6))
    add_table_caption(doc, "Table 4: October 2026 Monthly Dairy Harvest, Commercial Sales & Allocation Reconciliation")

    t4 = doc.add_table(rows=8, cols=5)
    t4.alignment = WD_TABLE_ALIGNMENT.CENTER
    t4.autofit = False
    set_table_borders(t4, "CBD5E1")

    t4_headers = ["Category / Transaction", "Morning (AM)", "Evening (PM)", "Monthly Total", "Share (%)"]
    t4_widths = [Inches(2.6), Inches(1.1), Inches(1.1), Inches(1.2), Inches(0.9)]

    hdr_row4 = t4.rows[0]
    make_row_header(hdr_row4)
    make_row_cant_split(hdr_row4)
    for idx, name in enumerate(t4_headers):
        c = hdr_row4.cells[idx]
        c.width = t4_widths[idx]
        set_cell_background(c, "D97706")
        set_cell_margins(c, 110, 110, 130, 130)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(name)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)

    dairy_summary_data = [
        ("Commercial Milk Dispatched (Sales)", "105.5 Litres", "88.5 Litres", "194.0 Litres", "85.3%"),
        ("Internal Farm Allocation — Gladys (Staff)", "14.5 Litres", "—", "14.5 Litres", "6.4%"),
        ("Internal Farm Allocation — Maasai", "15.0 Litres", "—", "15.0 Litres", "6.6%"),
        ("Internal Farm Allocation — Goat Kids (Weaned Oct 6)", "2.0 Litres", "1.5 Litres", "3.5 Litres", "1.5%"),
        ("Internal Farm Allocation — Kamau (Day 13)", "0.5 Litres", "—", "0.5 Litres", "0.2%"),
        ("Total Internal Farm Allocations", "32.0 Litres", "1.5 Litres", "33.5 Litres", "14.7%"),
        ("TOTAL GROSS COW MILK HARVESTED", "138.5 Litres", "89.0 Litres", "227.5 Litres", "100.0%"),
    ]

    for r_idx, row_data in enumerate(dairy_summary_data):
        row = t4.rows[r_idx + 1]
        make_row_cant_split(row)
        if r_idx == 6:
            bg = "FEF3C7" # Total row highlight
        elif r_idx % 2 == 1:
            bg = "FFFBEB"
        else:
            bg = "FFFFFF"
            
        for c_idx in range(5):
            c = row.cells[c_idx]
            c.width = t4_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, 100, 100, 130, 130)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(row_data[c_idx])
            r.font.name = 'Calibri'
            r.font.size = Pt(10)
            if c_idx in [0, 3] or r_idx == 6:
                r.bold = True
                r.font.color.rgb = RGBColor(180, 83, 9) if r_idx == 6 else RGBColor(15, 23, 42)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(16)

    add_callout(
        doc,
        "DAIRY GROUND TRUTH RECONCILIATION: 100% ACCOUNTED FOR (ZERO LOSS)",
        "Ground Truth Accounting Formula:\n"
        "Total Gross Cow Milk Harvested (227.5 Litres) = Commercial Sales Dispatches (194.0 Litres) + Internal Farm Allocations (33.5 Litres).\n"
        "Daily herd production averaged 7.34 Litres/day across all 31 days, rising steadily from 5.5 Litres/day in early October to 9.0 Litres/day at month-end. 100% accounted for with zero milk loss.",
        "D97706",
        "FFFBEB"
    )

    # --------------------------------------------------------------------------
    # TABLE 5: DEDICATED FULL PAGE FOR WEEKLY PROGRESSION TREND (PAGE 9)
    # Generous row spacing, large 10pt/10.5pt fonts, plenty of breathing room!
    # --------------------------------------------------------------------------
    doc.add_page_break()
    add_heading_2(doc, "3.3 Weekly Milk Production Progression & Yield Trend", (217, 119, 6))
    add_table_caption(doc, "Table 5: Weekly Milk Production, Commercial Sales & Growth Trend (October 2026)")

    t5_wk = doc.add_table(rows=7, cols=5)
    t5_wk.alignment = WD_TABLE_ALIGNMENT.CENTER
    t5_wk.autofit = False
    set_table_borders(t5_wk, "CBD5E1")

    wk_headers = ["Time Period", "Gross Harvest", "Commercial Sales", "Internal Allocations", "Daily Average"]
    wk_widths = [Inches(2.1), Inches(1.2), Inches(1.2), Inches(1.2), Inches(1.2)]

    hdr_wk = t5_wk.rows[0]
    make_row_header(hdr_wk)
    make_row_cant_split(hdr_wk)
    for idx, name in enumerate(wk_headers):
        c = hdr_wk.cells[idx]
        c.width = wk_widths[idx]
        set_cell_background(c, "0F172A")
        set_cell_margins(c, 110, 110, 130, 130)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(name)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(255, 255, 255)

    weekly_data = [
        ("Week 1 (Oct 1 – 7)", "42.5 Litres", "34.0 Litres", "8.5 Litres", "6.07 L / day"),
        ("Week 2 (Oct 8 – 14)", "44.5 Litres", "38.5 Litres", "6.0 Litres", "6.36 L / day"),
        ("Week 3 (Oct 15 – 21)", "54.5 Litres", "47.5 Litres", "7.0 Litres", "7.79 L / day"),
        ("Week 4 (Oct 22 – 28)", "59.5 Litres", "52.5 Litres", "7.0 Litres", "8.50 L / day"),
        ("Final Days (Oct 29 – 31)", "26.5 Litres", "21.5 Litres", "5.0 Litres", "8.83 L / day"),
        ("TOTAL OCTOBER 2026", "227.5 Litres", "194.0 Litres", "33.5 Litres", "7.34 L / day"),
    ]

    for r_idx, row_data in enumerate(weekly_data):
        row = t5_wk.rows[r_idx + 1]
        make_row_cant_split(row)
        if r_idx == 5:
            bg = "F0FDF4"
        elif r_idx % 2 == 1:
            bg = "FAFBFD"
        else:
            bg = "FFFFFF"
            
        for c_idx in range(5):
            c = row.cells[c_idx]
            c.width = wk_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, 100, 100, 130, 130)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(row_data[c_idx])
            r.font.name = 'Calibri'
            r.font.size = Pt(10)
            if c_idx == 0 or r_idx == 5:
                r.bold = True
                r.font.color.rgb = RGBColor(21, 128, 61) if r_idx == 5 else RGBColor(15, 23, 42)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(16)

    add_callout(
        doc,
        "PRODUCTION INSIGHT: SUSTAINED UPWARD YIELD TRAJECTORY",
        "Daily milk yield demonstrated consistent week-over-week gains throughout October:\n"
        "• Production expanded from 6.07 L/day in Week 1 to 8.50 L/day in Week 4, reaching a peak of 8.83 L/day over the final 3 days.\n"
        "• Increased production was driven by high-energy silage nutrition and optimized feeding schedules, with zero health incidents.",
        "15803D",
        "F0FDF4"
    )

    # --------------------------------------------------------------------------
    # SECTION 4: KABETE RESIDENCE (PAGE 10)
    # --------------------------------------------------------------------------
    doc.add_page_break()
    add_heading_1(doc, "4. Kabete Residence — Structural Works & Domestic Pet Care")
    add_heading_2(doc, "4.1 Staff Quarters Concrete Slab, Roof Care & Pet Welfare", (109, 40, 217))

    p_k_lead = doc.add_paragraph()
    p_k_lead.paragraph_format.space_before = Pt(2)
    p_k_lead.paragraph_format.space_after = Pt(4)
    p_k_lead.paragraph_format.line_spacing = 1.15
    r_kl = p_k_lead.add_run(
        "Kabete Residence achieved key structural milestones in October, highlighted by the concrete pouring of the Staff "
        "Quarters (SQ) roof slab. Domestic pets continued to receive attentive daily care, with all operations overseen and shared by Njoki:"
    )
    r_kl.font.name = 'Calibri'
    r_kl.font.size = Pt(10)
    r_kl.font.color.rgb = RGBColor(51, 65, 85)

    add_bullet_point(doc, "Staff Quarters (SQ) Roof Slab Poured:", "Builders assembled timber support props, tied heavy steel reinforcement cages for drop beams, and laid rebar mesh across the deck. Electricians ran heavy-duty PVC conduit pipes and central junction boxes through the rebar. Fresh concrete was poured across the entire slab and mechanically vibrated to eliminate air pockets.")
    add_bullet_point(doc, "Roofing Maintenance & Gutter Clearance:", "Workers climbed the terracotta tile roofs of the main house, carport canopy, and generator shed to clear fallen leaves and inspect gutter drainage.")
    add_bullet_point(doc, "Water Tank & Stormwater Drainage:", "Steel reinforcement bars were assembled for the main water tank foundation slab, and stone retaining walls along the forest path were reinforced.")
    add_bullet_point(doc, "Domestic Pet Care (Ajabu & Resident Cats):", "Ajabu the Golden Retriever enjoyed good health, receiving nutritious meals, grooming, and morning leashed exercise walks along the driveway and gardens. Resident cats (Reo, Mocha, and Aiko) were fed indoors and remained in prime condition. All updates were communicated by Njoki.")

    # --------------------------------------------------------------------------
    # SECTION 5: AMANI COTTAGE (PAGE 11)
    # --------------------------------------------------------------------------
    doc.add_page_break()
    add_heading_1(doc, "5. Amani Cottage — Turf Management & Estate Presentation")
    add_heading_2(doc, "5.1 Lawn Maintenance, Sprinkler Watering & Cottage Housekeeping", (13, 148, 136))

    p_a_lead = doc.add_paragraph()
    p_a_lead.paragraph_format.space_before = Pt(2)
    p_a_lead.paragraph_format.space_after = Pt(4)
    p_a_lead.paragraph_format.line_spacing = 1.15
    r_al = p_a_lead.add_run(
        "Amani Cottage remained in pristine condition throughout October, with dedicated turf care, lawn watering, "
        "and thorough two-story interior housekeeping under Edwin and the domestic housekeeper:"
    )
    r_al.font.name = 'Calibri'
    r_al.font.size = Pt(10)
    r_al.font.color.rgb = RGBColor(51, 65, 85)

    add_bullet_point(doc, "Front Lawn Fertilizer & Watering:", "Edwin applied Calcium Ammonium Nitrate (CAN) fertilizer across the front lawn and ran the rotary sprinklers on schedule to keep the grass thick, lush, and green.")
    add_bullet_point(doc, "Compound Grounds & Walkway Sweeping:", "Grounds staff swept paved walkways, cleared fallen woodland leaves, and trimmed garden borders around the cottage.")
    add_bullet_point(doc, "Interior Housekeeping & Guest Readiness:", "The two-story cottage received regular room dusting, floor cleaning, window wiping, and furniture staging, keeping the property fully prepared for executive visitors.")

    # --------------------------------------------------------------------------
    # SECTION 6: SUPERVISION & STRATEGIC OUTLOOK (PAGE 12 - CLEAN FULL PAGE)
    # --------------------------------------------------------------------------
    doc.add_page_break()
    add_heading_1(doc, "6. Supervision Roster & Strategic November 2026 Outlook")
    add_heading_2(doc, "6.1 Multi-Site Operational Supervision Roster", (15, 23, 42))

    t6 = doc.add_table(rows=5, cols=3)
    t6.alignment = WD_TABLE_ALIGNMENT.CENTER
    t6.autofit = False
    set_table_borders(t6, "CBD5E1")

    t6_headers = ["Project Site", "Key Personnel / Supervisors", "Scope of Supervisory Responsibility"]
    t6_widths = [Inches(1.8), Inches(2.2), Inches(2.9)]

    hdr_row6 = t6.rows[0]
    make_row_header(hdr_row6)
    make_row_cant_split(hdr_row6)
    for idx, name in enumerate(t6_headers):
        c = hdr_row6.cells[idx]
        c.width = t6_widths[idx]
        set_cell_background(c, "0F172A")
        set_cell_margins(c, 90, 90, 110, 110)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(name)
        r.bold = True
        r.font.name = 'Calibri'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    supervisors_data = [
        ("Mucheru Golf", "Mr. Gichuhi, Ken, Kinoti & Kamandau", "Course earthwork, pop-up sprinklers, solenoids, river sand, teebox shaping, dam liner welding, material logistics."),
        ("Chaka Farms", "Willy, Kamandau, Margaret & Monica", "Dairy milking & sales reconciliation, dog manners & walking, sheep grazing, plumbing & compound sanitation."),
        ("Kabete Residence", "Njoki (Operational Oversight)", "Staff Quarters (SQ) concrete slab works, electrical conduits, roof tile inspection, domestic pet welfare (Ajabu & cats)."),
        ("Amani Cottage", "Edwin & Domestic Housekeeper", "Front lawn CAN fertilizer, rotary sprinkler watering, woodland garden upkeep & two-story housekeeping."),
    ]

    for r_idx, row_data in enumerate(supervisors_data):
        row = t6.rows[r_idx + 1]
        make_row_cant_split(row)
        bg = "FAFBFD" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx in range(3):
            c = row.cells[c_idx]
            c.width = t6_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, 80, 80, 110, 110)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.12
            r = p.add_run(row_data[c_idx])
            r.font.name = 'Calibri'
            r.font.size = Pt(9)
            if c_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)
            elif c_idx == 1:
                r.bold = True
                r.font.color.rgb = RGBColor(30, 58, 138)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_heading_2(doc, "6.2 Strategic Priority Action Items for November 2026", (15, 23, 42))

    add_bullet_point(doc, "Plant Grass on All 18 Ready Teeboxes:", "Begin planting grass stolons across all 18 leveled teebox platforms using installed pop-up sprinklers.")
    add_bullet_point(doc, "Complete Apron Shaping Around Greens:", "Finish spreading and leveling red soil on the aprons around all 18 putting greens to complete green complexes.")
    add_bullet_point(doc, "Finalize Dam 2 Liner Welding:", "Complete heat-welding of the polythene liner in Dam 2 and backfill perimeter trenches to maximize rainwater capture.")
    add_bullet_point(doc, "Maintain High Dairy Output:", "Continue high-energy silage and mineral feeding to sustain cow milk production above 8.0 Litres per day.")
    add_bullet_point(doc, "SQ Slab Curing & Wall Masonry:", "Monitor water curing on the SQ concrete roof slab at Kabete, then start wall masonry and room partitions.")

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(10)
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
            w_doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)
            print("Microsoft Word COM updated Table of Contents and exported PDF successfully!")
            w_doc.Close()
        finally:
            word.Quit()
    except Exception as e:
        print(f"Word COM update note: {e}")

    ensure_word_closed()
    shutil.copy2(docx_path, alt_docx_path)
    if os.path.exists(pdf_path):
        shutil.copy2(pdf_path, alt_pdf_path)
    print(f"Report copies successfully placed in root of October 2026!")

if __name__ == "__main__":
    build_report()
