#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
from io import BytesIO
import tempfile
import shutil

from PyPDF2 import PdfReader, PdfWriter, PageObject
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def strip_booklet_conditionals(tex_file: Path) -> Path:
    r"""
    Copy .tex file into same dir with _booklet.tex suffix,
    stripping only the lines \ifdefined\BOOKLET and \fi.
    Keeps content inside untouched.
    """
    new_path = tex_file.with_name(tex_file.stem + "_booklet.tex")
    with open(tex_file, "r") as f_in, open(new_path, "w") as f_out:
        for line in f_in:
            if line.strip().startswith(r"\ifdefined\BOOKLET"):
                continue
            if line.strip() == r"\fi":
                continue
            f_out.write(line)
    return new_path


def run_pdflatex(tex_file: Path):
    """Run pdflatex on a given .tex file."""
    subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex_file.name],
        cwd=tex_file.parent,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def create_page_number_overlay(page_num, width=float(A4[0]), height=float(A4[1])):
    """Generate a single-page PDF overlay with optional page number."""
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    if page_num is not None:
        c.setFont("Times-Roman", 11)
        c.drawCentredString(width / 2.0, 20, str(page_num))
    c.showPage()
    c.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]


def main():
    sources = [
        Path("cover.tex"),
        Path("intro.tex"),
        Path("sample.tex"),
        Path("neighbours/statement/statement.tex"),
        Path("bus/statement/statement.tex"),
        Path("feed/statement/statement.tex"),
    ]

    generated_pdfs = []
    temp_tex_files = []

    # Process each .tex → *_booklet.tex → .pdf
    for tex in sources:
        processed = strip_booklet_conditionals(tex)
        temp_tex_files.append(processed)

        run_pdflatex(processed)
        pdf_file = processed.with_suffix(".pdf")
        if not pdf_file.exists():
            raise RuntimeError(f"Expected PDF not found: {pdf_file}")
        generated_pdfs.append(pdf_file)

    # Merge and overlay page numbers
    writer = PdfWriter()
    page_counter = 0

    for i, pdf_path in enumerate(generated_pdfs):
        reader = PdfReader(str(pdf_path))
        for page in reader.pages:
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)

            if i == 0:  # cover, no page number
                overlay = create_page_number_overlay(None, width, height)
            else:
                page_counter += 1
                overlay = create_page_number_overlay(page_counter, width, height)

            # Merge overlay
            new_page = PageObject.create_blank_page(width=width, height=height)
            new_page.merge_page(page)
            new_page.merge_page(overlay)
            writer.add_page(new_page)

    with open("booklet.pdf", "wb") as f_out:
        writer.write(f_out)

    print("booklet.pdf built successfully")

    # Cleanup intermediate files
    for f in temp_tex_files:
        base = f.with_suffix("")
        for ext in [".tex", ".aux", ".log", ".out", ".pdf"]:
            try:
                os.remove(str(base) + ext)
            except FileNotFoundError:
                pass


if __name__ == "__main__":
    main()
