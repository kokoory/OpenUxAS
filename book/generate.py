#!/usr/bin/env python3
"""Main generator script for OpenUxAS Book PDF"""
import sys
sys.path.insert(0, '/home/user/OpenUxAS/book')

from pdf_utils import BookPDF
from chapters_1_3 import write_chapter1, write_chapter2, write_chapter3
from chapters_4_6 import write_chapter4, write_chapter5, write_chapter6, write_chapter5_extra
from chapters_7_10 import write_chapter7, write_chapter8, write_chapter9, write_chapter10

def write_all_chapters(pdf, verbose=False):
    """Write all chapters to pdf"""
    chapters = [
        ("Chapter 1: Introduction", write_chapter1),
        ("Chapter 2: Theory", write_chapter2),
        ("Chapter 3: Architecture", write_chapter3),
        ("Chapter 4: Installation", write_chapter4),
        ("Chapter 5: Task Types", write_chapter5),
        ("Chapter 5 Extra: Task State Machine", write_chapter5_extra),
        ("Chapter 6: Configuration", write_chapter6),
        ("Chapter 7: Examples", write_chapter7),
        ("Chapter 8: Multi-Vehicle", write_chapter8),
        ("Chapter 9: Results", write_chapter9),
        ("Chapter 10: Advanced", write_chapter10),
    ]
    for name, func in chapters:
        if verbose:
            print(f"Writing {name}...")
        func(pdf)

def main():
    import os
    output_path = '/home/user/OpenUxAS/OpenUxAS_Guide_Korean.pdf'

    # First pass: collect TOC
    print("First pass: collecting TOC...")
    pdf1 = BookPDF()
    pdf1.title_page()
    write_all_chapters(pdf1, verbose=True)

    # Final pass: with TOC
    print("\nFinal pass: generating with TOC...")
    final = BookPDF()
    final.toc = pdf1.toc
    final.title_page()
    final.add_toc_page()
    write_all_chapters(final)

    final.output(output_path)
    size = os.path.getsize(output_path)
    print(f"\nFinal PDF: {output_path}")
    print(f"File size: {size/1024:.1f} KB")
    print(f"Total pages: {final.page_no()}")

if __name__ == '__main__':
    main()
