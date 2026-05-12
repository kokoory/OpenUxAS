#!/usr/bin/env python3
"""
OpenUxAS Technical Reference - Markdown to PDF converter
Based on generate_pdf.py. Uses fpdf2 with WenQuanYi Zen Hei font for Korean text.
"""

import re
from fpdf import FPDF, XPos, YPos

FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
INPUT_FILE = "OpenUxAS_Technical_Reference_Korean.md"
OUTPUT_FILE = "OpenUxAS_Technical_Reference_Korean.pdf"

PAGE_W = 210
MARGIN_L = 15
MARGIN_R = 15
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R


class TechRefPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(MARGIN_L, 15, MARGIN_R)
        self.add_font("Main", "", FONT_PATH)
        self.add_font("Main", "B", FONT_PATH)
        self.add_font("Main", "I", FONT_PATH)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Main", "I", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 8, "OpenUxAS 기능별 상세 기술 레퍼런스",
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
            self.set_draw_color(200, 200, 200)
            self.line(MARGIN_L, self.get_y(), PAGE_W - MARGIN_R, self.get_y())
            self.ln(3)
            self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("Main", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"- {self.page_no()} -", align="C")
        self.set_text_color(0, 0, 0)

    def write_rich_text(self, text, size=10, line_height=6, align="L"):
        self.set_font("Main", "", size)
        parts = re.split(r'(\*\*.*?\*\*|\*.*?\*|`[^`]+`)', text)
        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                self.set_font("Main", "B", size)
                self.write(line_height, part[2:-2])
                self.set_font("Main", "", size)
            elif part.startswith("*") and part.endswith("*") and not part.startswith("**"):
                self.set_font("Main", "I", size)
                self.write(line_height, part[1:-1])
                self.set_font("Main", "", size)
            elif part.startswith("`") and part.endswith("`"):
                self.set_font("Main", "", size - 1)
                self.set_text_color(180, 50, 50)
                self.write(line_height, part[1:-1])
                self.set_text_color(0, 0, 0)
                self.set_font("Main", "", size)
            else:
                self.write(line_height, part)

    def add_heading(self, level, text):
        sizes = {1: 22, 2: 17, 3: 14, 4: 12}
        size = sizes.get(level, 10)

        if level <= 2:
            self.ln(8)

        if level == 1:
            self.set_fill_color(25, 60, 120)
            self.set_text_color(255, 255, 255)
            self.set_font("Main", "B", size)
            self.ln(4)
            self.cell(CONTENT_W, 14, f"  {text}", fill=True,
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_text_color(0, 0, 0)
            self.ln(4)
        elif level == 2:
            self.set_text_color(25, 60, 120)
            self.set_font("Main", "B", size)
            self.cell(CONTENT_W, 10, text,
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_draw_color(25, 60, 120)
            self.line(MARGIN_L, self.get_y(), PAGE_W - MARGIN_R, self.get_y())
            self.set_text_color(0, 0, 0)
            self.ln(3)
        elif level == 3:
            self.set_text_color(40, 90, 160)
            self.set_font("Main", "B", size)
            self.cell(CONTENT_W, 9, text,
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_text_color(0, 0, 0)
            self.ln(2)
        else:
            self.set_font("Main", "B", size)
            self.cell(CONTENT_W, 8, text,
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.ln(2)

    def add_code_block(self, lines, language=""):
        self.set_fill_color(245, 245, 245)
        self.set_draw_color(200, 200, 200)
        self.set_font("Main", "", 7)

        estimated_height = len(lines) * 4 + 6
        if self.get_y() + min(estimated_height, 100) > self.h - 25:
            self.add_page()

        x_start = MARGIN_L
        block_w = CONTENT_W

        if language and language != "mermaid":
            self.set_font("Main", "I", 6)
            self.set_text_color(100, 100, 100)
            self.cell(block_w, 4, f"  {language}", fill=True,
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_text_color(0, 0, 0)

        self.set_font("Main", "", 7)
        for line in lines:
            if self.get_y() > self.h - 25:
                self.add_page()
                self.set_fill_color(245, 245, 245)
                self.set_font("Main", "", 7)

            self.set_x(x_start)
            display_line = line[:120] + "..." if len(line) > 120 else line
            self.cell(block_w, 4, f"  {display_line}", fill=True,
                      new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        self.ln(3)

    def add_table(self, headers, rows):
        if not headers:
            return

        num_cols = len(headers)
        col_w = CONTENT_W / num_cols
        col_widths = [col_w] * num_cols

        self.set_fill_color(25, 60, 120)
        self.set_text_color(255, 255, 255)
        self.set_font("Main", "B", 8)
        self.set_draw_color(200, 200, 200)

        for i, h in enumerate(headers):
            x_next = XPos.RIGHT if i < num_cols - 1 else XPos.LMARGIN
            y_next = YPos.TOP if i < num_cols - 1 else YPos.NEXT
            self.cell(col_widths[i], 7, f" {h.strip()}", border=1, fill=True,
                      new_x=x_next, new_y=y_next)

        self.set_text_color(0, 0, 0)
        self.set_font("Main", "", 8)
        fill = False
        for row in rows:
            if self.get_y() > self.h - 25:
                self.add_page()
                self.set_font("Main", "", 8)

            if fill:
                self.set_fill_color(240, 245, 255)
            else:
                self.set_fill_color(255, 255, 255)

            for i, cell_text in enumerate(row):
                x_next = XPos.RIGHT if i < num_cols - 1 else XPos.LMARGIN
                y_next = YPos.TOP if i < num_cols - 1 else YPos.NEXT
                display = cell_text.strip().replace("**", "")
                self.cell(col_widths[i], 7, f" {display}", border=1, fill=True,
                          new_x=x_next, new_y=y_next)
            fill = not fill

        self.ln(3)

    def add_blockquote(self, text):
        self.set_fill_color(240, 248, 255)
        self.set_draw_color(25, 60, 120)
        y = self.get_y()

        self.set_font("Main", "I", 9)
        text = text.replace("**", "").strip()
        self.set_x(MARGIN_L + 5)
        self.multi_cell(CONTENT_W - 10, 5, text, fill=True)

        y_end = self.get_y()
        self.set_line_width(0.8)
        self.line(MARGIN_L + 2, y, MARGIN_L + 2, y_end)
        self.set_line_width(0.2)
        self.ln(2)

    def add_bullet(self, text, indent=0):
        self.set_font("Main", "", 9)
        x_offset = MARGIN_L + 3 + indent * 5
        self.set_x(x_offset)
        self.cell(4, 5, "-")
        self.set_x(x_offset + 5)

        clean = text.strip()
        if clean.startswith("- "):
            clean = clean[2:]

        self.write_rich_text(clean, size=9, line_height=5)
        self.ln(5)


def parse_and_render(pdf, md_text):
    lines = md_text.split("\n")
    i = 0
    in_code_block = False
    code_lines = []
    code_lang = ""

    # Title page
    pdf.add_page()
    pdf.ln(25)
    pdf.set_font("Main", "B", 28)
    pdf.set_text_color(25, 60, 120)
    pdf.cell(CONTENT_W, 15, "OpenUxAS", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_font("Main", "B", 16)
    pdf.cell(CONTENT_W, 12, "기능별 상세 기술 레퍼런스",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(3)
    pdf.set_font("Main", "", 13)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(CONTENT_W, 10, "Technical Reference: Service-by-Service Deep Dive",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(6)
    pdf.set_font("Main", "", 11)
    pdf.cell(CONTENT_W, 8, "다수 무인 비행체 자율 시스템 프레임워크",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.cell(CONTENT_W, 8, "Multi-Vehicle Autonomous Systems Framework",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(12)

    pdf.set_draw_color(25, 60, 120)
    pdf.set_line_width(1)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.set_line_width(0.2)
    pdf.ln(12)

    pdf.set_font("Main", "", 10)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(CONTENT_W, 7, "서비스별 로직 | 입출력 분석 | 내부 알고리즘 | 데이터 구조",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(8)
    pdf.cell(CONTENT_W, 7, "Air Force Research Laboratory (AFRL)",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.cell(CONTENT_W, 7, "Aerospace Systems Directorate",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(20)

    pdf.set_font("Main", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(CONTENT_W, 8, "9 핵심 서비스 + 15 태스크 서비스 + 3 핵심 알고리즘 상세 분석",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_text_color(0, 0, 0)

    # TOC page
    pdf.add_page()
    pdf.set_font("Main", "B", 18)
    pdf.set_text_color(25, 60, 120)
    pdf.cell(CONTENT_W, 12, "목차 (Table of Contents)",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_draw_color(25, 60, 120)
    pdf.line(MARGIN_L, pdf.get_y(), PAGE_W - MARGIN_R, pdf.get_y())
    pdf.set_text_color(0, 0, 0)
    pdf.ln(6)

    toc_items = [
        ("제1장", "시스템 아키텍처 개요"),
        ("제2장", "LMCP 메시지 체계"),
        ("제3장", "임무 처리 파이프라인"),
        ("제4장", "핵심 서비스 상세 분석"),
        ("제5장", "태스크 서비스 상세 분석"),
        ("제6장", "핵심 알고리즘 상세"),
        ("제7장", "통신 레이어"),
        ("제8장", "시스템 시작 시퀀스와 설정"),
    ]
    for ch, title in toc_items:
        pdf.set_font("Main", "B", 11)
        pdf.cell(20, 8, ch)
        pdf.set_font("Main", "", 11)
        pdf.cell(0, 8, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    skip_frontmatter = True

    while i < len(lines):
        line = lines[i]

        # Code block handling
        if line.strip().startswith("```"):
            if in_code_block:
                is_mermaid = (code_lang == "mermaid")
                if is_mermaid:
                    pdf.set_font("Main", "B", 9)
                    pdf.set_text_color(100, 50, 150)
                    pdf.cell(CONTENT_W, 6,
                             "[Diagram] Mermaid Sequence Diagram",
                             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                    pdf.set_text_color(0, 0, 0)
                    pdf.add_code_block(code_lines, "mermaid")
                else:
                    pdf.add_code_block(code_lines, code_lang)
                in_code_block = False
                code_lines = []
                code_lang = ""
            else:
                in_code_block = True
                code_lang = line.strip().replace("```", "").strip()
                code_lines = []
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        stripped = line.strip()

        if skip_frontmatter:
            if stripped.startswith("# 제1장"):
                skip_frontmatter = False
            else:
                i += 1
                continue

        # Horizontal rule
        if stripped == "---":
            pdf.ln(3)
            pdf.set_draw_color(200, 200, 200)
            pdf.line(MARGIN_L, pdf.get_y(), PAGE_W - MARGIN_R, pdf.get_y())
            pdf.ln(3)
            i += 1
            continue

        # Headings
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            text = stripped.lstrip("#").strip()
            text = text.replace("*", "")

            if level == 1:
                pdf.add_page()

            pdf.add_heading(level, text)
            i += 1
            continue

        # Table
        if stripped.startswith("|") and "|" in stripped[1:]:
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1

            if len(table_lines) >= 2:
                headers = [c.strip() for c in table_lines[0].split("|") if c.strip()]
                rows = []
                for tl in table_lines[2:]:
                    cells = [c.strip() for c in tl.split("|") if c.strip()]
                    if cells and not all(set(c) <= set("-: ") for c in cells):
                        while len(cells) < len(headers):
                            cells.append("")
                        rows.append(cells[:len(headers)])
                pdf.add_table(headers, rows)
            continue

        # Blockquote
        if stripped.startswith(">"):
            quote_text = stripped.lstrip(">").strip()
            i += 1
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_text += " " + lines[i].strip().lstrip(">").strip()
                i += 1
            pdf.add_blockquote(quote_text)
            continue

        # Bullet list
        if stripped.startswith("- ") or stripped.startswith("* "):
            indent = 0
            if line.startswith("  "):
                indent = (len(line) - len(line.lstrip())) // 2
            pdf.add_bullet(stripped[2:], indent)
            i += 1
            continue

        # Empty line
        if not stripped:
            pdf.ln(2)
            i += 1
            continue

        # Normal paragraph
        pdf.set_font("Main", "", 10)
        pdf.write_rich_text(stripped, size=10, line_height=6)
        pdf.ln(6)
        i += 1


def main():
    print("Reading markdown file...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        md_text = f.read()

    print("Creating PDF...")
    pdf = TechRefPDF()
    parse_and_render(pdf, md_text)

    print(f"Saving PDF to {OUTPUT_FILE}...")
    pdf.output(OUTPUT_FILE)
    print(f"Done! {OUTPUT_FILE} created successfully.")


if __name__ == "__main__":
    main()
