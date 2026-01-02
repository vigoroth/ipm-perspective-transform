#!/usr/bin/env python3
"""
Convert markdown documentation files to PDF.

Usage:
    python convert_docs_to_pdf.py
"""

import markdown2
from weasyprint import HTML, CSS
import os
import sys

def convert_md_to_pdf(md_file, pdf_file):
    """
    Convert markdown to PDF with professional styling.

    Args:
        md_file: Path to input markdown file
        pdf_file: Path to output PDF file
    """
    print(f"Converting {md_file}...")

    # Read markdown content
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {md_file}")
        return False
    except Exception as e:
        print(f"Error reading file: {e}")
        return False

    # Convert to HTML with extras
    try:
        html_content = markdown2.markdown(
            md_content,
            extras=[
                'fenced-code-blocks',
                'tables',
                'code-friendly',
                'header-ids',
                'toc',
                'break-on-newline'
            ]
        )
    except Exception as e:
        print(f"Error converting markdown to HTML: {e}")
        return False

    # Professional CSS styling for technical documentation
    css_style = """
    @page {
        margin: 1in;
        size: letter;
        @bottom-center {
            content: counter(page);
            font-size: 9pt;
            color: #666;
        }
    }

    body {
        font-family: 'Georgia', 'Times New Roman', serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #333;
        max-width: 100%;
    }

    h1 {
        font-size: 24pt;
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
        margin-top: 30px;
        margin-bottom: 15px;
        page-break-before: auto;
        page-break-after: avoid;
    }

    h2 {
        font-size: 20pt;
        color: #34495e;
        margin-top: 25px;
        margin-bottom: 12px;
        page-break-after: avoid;
    }

    h3 {
        font-size: 16pt;
        color: #555;
        margin-top: 20px;
        margin-bottom: 10px;
        page-break-after: avoid;
    }

    h4 {
        font-size: 14pt;
        color: #666;
        margin-top: 15px;
        margin-bottom: 8px;
    }

    p {
        margin-bottom: 10px;
        text-align: justify;
    }

    code {
        font-family: 'Courier New', 'Consolas', monospace;
        background-color: #f4f4f4;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 10pt;
        color: #c7254e;
    }

    pre {
        background-color: #f8f8f8;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 15px;
        overflow-x: auto;
        font-size: 9pt;
        line-height: 1.4;
        page-break-inside: avoid;
        margin: 15px 0;
    }

    pre code {
        background-color: transparent;
        padding: 0;
        color: #333;
        font-size: 9pt;
    }

    table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
        page-break-inside: avoid;
    }

    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
        font-size: 10pt;
    }

    th {
        background-color: #3498db;
        color: white;
        font-weight: bold;
    }

    tr:nth-child(even) {
        background-color: #f9f9f9;
    }

    blockquote {
        border-left: 4px solid #3498db;
        padding-left: 15px;
        margin-left: 0;
        color: #666;
        font-style: italic;
        background-color: #f9f9f9;
        padding: 10px 10px 10px 15px;
        margin: 15px 0;
    }

    a {
        color: #3498db;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }

    ul, ol {
        margin-bottom: 10px;
        padding-left: 25px;
    }

    li {
        margin-bottom: 5px;
    }

    hr {
        border: none;
        border-top: 1px solid #ddd;
        margin: 20px 0;
    }

    /* Prevent orphans and widows */
    p, li {
        orphans: 3;
        widows: 3;
    }

    /* Keep code blocks and tables together */
    pre, table {
        page-break-inside: avoid;
    }
    """

    # Create full HTML document
    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{os.path.basename(md_file)}</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Convert to PDF
    try:
        HTML(string=full_html).write_pdf(
            pdf_file,
            stylesheets=[CSS(string=css_style)]
        )
        print(f"✓ Successfully created: {pdf_file}")
        return True
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return False


def main():
    """Main conversion function."""

    # Define file paths
    base_dir = os.path.dirname(os.path.abspath(__file__))

    files_to_convert = [
        ('docs/math_foundations.md', 'docs/math_foundations.pdf'),
        ('docs/implementation_notes.md', 'docs/implementation_notes.pdf')
    ]

    print("=" * 60)
    print("Markdown to PDF Converter")
    print("=" * 60)
    print()

    success_count = 0
    total_count = len(files_to_convert)

    for md_file, pdf_file in files_to_convert:
        md_path = os.path.join(base_dir, md_file)
        pdf_path = os.path.join(base_dir, pdf_file)

        if convert_md_to_pdf(md_path, pdf_path):
            success_count += 1
            # Get file size
            size_bytes = os.path.getsize(pdf_path)
            size_mb = size_bytes / (1024 * 1024)
            print(f"  File size: {size_mb:.2f} MB")
        print()

    # Summary
    print("=" * 60)
    print(f"Conversion complete: {success_count}/{total_count} files converted")
    print("=" * 60)

    if success_count < total_count:
        sys.exit(1)


if __name__ == '__main__':
    main()
