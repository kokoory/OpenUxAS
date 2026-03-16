#!/usr/bin/env python3
"""PDF utility classes for OpenUxAS Book"""
from fpdf import FPDF

FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

class BookPDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.add_font('K', '', FONT_PATH)
        self.add_font('K', 'B', FONT_PATH)
        self.add_font('K', 'I', FONT_PATH)
        self.ch_num = 0
        self.sec_num = 0
        self.subsec_num = 0
        self.toc = []
        self.set_auto_page_break(auto=True, margin=22)

    def header(self):
        if self.page_no() > 3:
            self.set_font('K', 'I', 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 8, 'OpenUxAS \ucd08\ubcf4\uc790\ub97c \uc704\ud55c \uc644\ubcbd \uac00\uc774\ub4dc', 0, 0, 'C')
            self.ln(10)
            self.set_draw_color(200, 200, 200)
            self.line(10, 18, 200, 18)

    def footer(self):
        if self.page_no() > 2:
            self.set_y(-15)
            self.set_font('K', 'I', 8)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, f'- {self.page_no()} -', 0, 0, 'C')

    def title_page(self):
        self.add_page()
        self.ln(40)
        self.set_font('K', 'B', 36)
        self.set_text_color(0, 51, 102)
        self.cell(0, 18, 'OpenUxAS', 0, new_x='LMARGIN', new_y='NEXT', align='C')
        self.ln(8)
        self.set_font('K', 'B', 18)
        self.set_text_color(0, 102, 153)
        self.cell(0, 10, '\ucd08\ubcf4\uc790\ub97c \uc704\ud55c \uc644\ubcbd \uac00\uc774\ub4dc', 0, new_x='LMARGIN', new_y='NEXT', align='C')
        self.ln(3)
        self.set_font('K', '', 13)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, 'Complete Guide for Beginners', 0, new_x='LMARGIN', new_y='NEXT', align='C')
        self.ln(15)
        self.set_draw_color(0, 102, 153)
        self.set_line_width(1.0)
        self.line(55, self.get_y(), 155, self.get_y())
        self.ln(15)
        self.set_font('K', '', 11)
        self.set_text_color(80, 80, 80)
        info = [
            '\ub2e4\uc218 \ubb34\uc778 \ube44\ud589\uccb4 \uc790\uc728 \uc2dc\uc2a4\ud15c \ud504\ub808\uc784\uc6cc\ud06c',
            'Multi-Vehicle Autonomous Systems Framework',
            '',
            '\uc774\ub860 | \uc124\uce58 | \uc544\ud0a4\ud14d\ucc98 | \uc608\uc81c \uc2e4\uc2b5 | \uacb0\uacfc \ubd84\uc11d',
            '',
            'Air Force Research Laboratory (AFRL)',
            'Aerospace Systems Directorate',
        ]
        for line in info:
            self.cell(0, 7, line, 0, new_x='LMARGIN', new_y='NEXT', align='C')

    def add_toc_page(self):
        self.add_page()
        self.set_font('K', 'B', 22)
        self.set_text_color(0, 51, 102)
        self.cell(0, 14, '\ubaa9\ucc28 (Table of Contents)', 0, new_x='LMARGIN', new_y='NEXT')
        self.ln(6)
        for level, title, page in self.toc:
            if level == 0:
                self.set_font('K', 'B', 11)
                self.ln(2)
            elif level == 1:
                self.set_font('K', '', 10)
            else:
                self.set_font('K', '', 9)
            indent = level * 8
            self.set_x(15 + indent)
            self.set_text_color(51, 51, 51)
            w = 185 - indent - 12
            self.cell(w, 6, title, 0, 0, 'L')
            self.cell(12, 6, str(page), 0, new_x='LMARGIN', new_y='NEXT', align='R')

    def ch(self, title_ko, title_en=''):
        """Chapter title"""
        self.ch_num += 1
        self.sec_num = 0
        self.subsec_num = 0
        self.add_page()
        full = f'\uc81c{self.ch_num}\uc7a5  {title_ko}'
        self.toc.append((0, full, self.page_no()))
        # Blue banner
        y = self.get_y()
        self.set_fill_color(0, 51, 102)
        self.rect(10, y, 190, 16, 'F')
        self.set_font('K', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.set_xy(15, y + 1)
        self.cell(0, 14, f'Chapter {self.ch_num}', 0, new_x='LMARGIN', new_y='NEXT')
        self.ln(4)
        self.set_font('K', 'B', 16)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, title_ko, 0, new_x='LMARGIN', new_y='NEXT')
        if title_en:
            self.set_font('K', 'I', 10)
            self.set_text_color(120, 120, 120)
            self.cell(0, 6, title_en, 0, new_x='LMARGIN', new_y='NEXT')
        self.ln(6)
        self.set_text_color(51, 51, 51)

    def sec(self, title):
        """Section title"""
        self.sec_num += 1
        self.subsec_num = 0
        num = f'{self.ch_num}.{self.sec_num}'
        self.toc.append((1, f'  {num}  {title}', self.page_no()))
        self.ln(3)
        self.set_draw_color(0, 102, 153)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)
        self.set_font('K', 'B', 13)
        self.set_text_color(0, 102, 153)
        self.cell(0, 8, f'{num}  {title}', 0, new_x='LMARGIN', new_y='NEXT')
        self.ln(2)
        self.set_text_color(51, 51, 51)

    def subsec(self, title):
        """Subsection title"""
        self.subsec_num += 1
        num = f'{self.ch_num}.{self.sec_num}.{self.subsec_num}'
        self.toc.append((2, f'    {num}  {title}', self.page_no()))
        self.ln(2)
        self.set_font('K', 'B', 11)
        self.set_text_color(0, 80, 130)
        self.cell(0, 7, f'{num}  {title}', 0, new_x='LMARGIN', new_y='NEXT')
        self.ln(1)
        self.set_text_color(51, 51, 51)

    def p(self, text):
        """Paragraph text"""
        self.set_font('K', '', 10)
        self.set_text_color(51, 51, 51)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def code(self, code, title=''):
        """Code block"""
        if title:
            self.set_font('K', 'B', 9)
            self.set_text_color(0, 80, 130)
            self.cell(0, 6, title, 0, new_x='LMARGIN', new_y='NEXT')
            self.ln(1)
        lines = code.strip().split('\n')
        h = len(lines) * 4.5 + 6
        y = self.get_y()
        if y + h > 272:
            self.add_page()
            y = self.get_y()
        self.set_fill_color(245, 245, 245)
        self.set_draw_color(200, 200, 200)
        self.rect(12, y, 186, h, 'DF')
        self.set_font('K', '', 7.5)
        self.set_text_color(51, 51, 51)
        self.set_xy(15, y + 3)
        for line in lines:
            self.cell(0, 4.5, line, 0, new_x='LMARGIN', new_y='NEXT')
            self.set_x(15)
        self.set_y(y + h + 3)

    def note(self, title, text, color=(0, 102, 153)):
        """Info/warning box"""
        self.ln(1)
        y = self.get_y()
        self.set_font('K', '', 9)
        # estimate height
        lines_needed = max(1, len(text) // 80 + 1)
        h = 10 + lines_needed * 5 + 4
        if y + h > 272:
            self.add_page()
            y = self.get_y()
        self.set_fill_color(color[0], color[1], color[2])
        self.rect(10, y, 3, h, 'F')
        self.set_fill_color(240, 248, 255)
        self.rect(13, y, 187, h, 'F')
        self.set_xy(16, y + 2)
        self.set_font('K', 'B', 9)
        self.set_text_color(color[0], color[1], color[2])
        self.cell(0, 6, title, 0, new_x='LMARGIN', new_y='NEXT')
        self.set_x(16)
        self.set_font('K', '', 8.5)
        self.set_text_color(51, 51, 51)
        self.multi_cell(178, 5, text)
        self.set_y(y + h + 3)

    def bullets(self, items):
        """Bullet list"""
        self.set_font('K', '', 10)
        self.set_text_color(51, 51, 51)
        for item in items:
            self.set_x(18)
            self.cell(5, 6, '-', 0, 0)
            self.multi_cell(167, 6, item)
            self.ln(0.5)
        self.ln(2)

    def tbl(self, headers, rows, widths=None):
        """Table"""
        if widths is None:
            n = len(headers)
            widths = [185 / n] * n
        # Header
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        self.set_font('K', 'B', 9)
        self.set_x(12)
        for i, h in enumerate(headers):
            self.cell(widths[i], 7, h, 1, 0, 'C', True)
        self.ln()
        # Rows
        self.set_text_color(51, 51, 51)
        self.set_font('K', '', 8.5)
        fill = False
        for row in rows:
            if fill:
                self.set_fill_color(240, 248, 255)
            else:
                self.set_fill_color(255, 255, 255)
            self.set_x(12)
            for i, cell_val in enumerate(row):
                self.cell(widths[i], 6.5, str(cell_val), 1, 0, 'L', True)
            self.ln()
            fill = not fill
        self.ln(3)

    def diagram(self, title, content):
        """ASCII diagram box"""
        self.ln(2)
        self.set_font('K', 'B', 10)
        self.set_text_color(0, 51, 102)
        self.cell(0, 7, title, 0, new_x='LMARGIN', new_y='NEXT', align='C')
        lines = content.strip().split('\n')
        h = len(lines) * 4.2 + 8
        y = self.get_y()
        if y + h > 272:
            self.add_page()
            y = self.get_y()
        self.set_fill_color(252, 252, 252)
        self.set_draw_color(0, 102, 153)
        self.rect(15, y, 180, h, 'DF')
        self.set_font('K', '', 7)
        self.set_text_color(51, 51, 51)
        self.set_xy(20, y + 4)
        for line in lines:
            self.cell(0, 4.2, line, 0, new_x='LMARGIN', new_y='NEXT')
            self.set_x(20)
        self.set_y(y + h + 3)
