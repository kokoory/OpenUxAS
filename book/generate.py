#!/usr/bin/env python3
"""Main generator script for OpenUxAS Book PDF"""
import sys
sys.path.insert(0, '/home/user/OpenUxAS/book')

from pdf_utils import BookPDF
from chapters_1_3 import write_chapter1, write_chapter2, write_chapter3
from chapters_4_6 import write_chapter4, write_chapter5, write_chapter6
from chapters_7_10 import write_chapter7, write_chapter8, write_chapter9, write_chapter10

def main():
    pdf = BookPDF()

    # Title page
    pdf.title_page()

    # Placeholder for TOC (will be inserted after)
    toc_page_placeholder = pdf.page_no() + 1

    # Write all chapters
    print("Writing Chapter 1: Introduction...")
    write_chapter1(pdf)

    print("Writing Chapter 2: Theory...")
    write_chapter2(pdf)

    print("Writing Chapter 3: Architecture...")
    write_chapter3(pdf)

    print("Writing Chapter 4: Installation...")
    write_chapter4(pdf)

    print("Writing Chapter 5: Task Types...")
    write_chapter5(pdf)

    print("Writing Chapter 6: Configuration...")
    write_chapter6(pdf)

    print("Writing Chapter 7: Examples...")
    write_chapter7(pdf)

    print("Writing Chapter 8: Multi-Vehicle...")
    write_chapter8(pdf)

    print("Writing Chapter 9: Results...")
    write_chapter9(pdf)

    print("Writing Chapter 10: Advanced...")
    write_chapter10(pdf)

    # Output
    output_path = '/home/user/OpenUxAS/OpenUxAS_Guide_Korean.pdf'
    pdf.output(output_path)
    print(f"\nPDF generated: {output_path}")

    import os
    size = os.path.getsize(output_path)
    print(f"File size: {size/1024:.1f} KB")
    print(f"Total pages: {pdf.page_no()}")

    # Now generate with TOC
    print("\nGenerating final version with TOC...")
    pdf2 = BookPDF()
    pdf2.title_page()

    write_chapter1(pdf2)
    write_chapter2(pdf2)
    write_chapter3(pdf2)
    write_chapter4(pdf2)
    write_chapter5(pdf2)
    write_chapter6(pdf2)
    write_chapter7(pdf2)
    write_chapter8(pdf2)
    write_chapter9(pdf2)
    write_chapter10(pdf2)

    # Insert TOC at page 2
    # Since fpdf2 doesn't support inserting pages, we create a new PDF with TOC
    final = BookPDF()
    final.toc = pdf2.toc  # Copy TOC entries

    final.title_page()
    final.add_toc_page()

    write_chapter1(final)
    write_chapter2(final)
    write_chapter3(final)
    write_chapter4(final)
    write_chapter5(final)
    write_chapter6(final)
    write_chapter7(final)
    write_chapter8(final)
    write_chapter9(final)
    write_chapter10(final)

    final.output(output_path)
    size = os.path.getsize(output_path)
    print(f"\nFinal PDF generated: {output_path}")
    print(f"File size: {size/1024:.1f} KB")
    print(f"Total pages: {final.page_no()}")

if __name__ == '__main__':
    main()
