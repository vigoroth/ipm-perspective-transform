# PDF Conversion Guide

This guide explains how to convert the markdown documentation files to PDF format.

## Files to Convert

1. `docs/math_foundations.md` (~1,019 lines)
2. `docs/implementation_notes.md` (~1,547 lines)

---

## Option 1: Using Pandoc (Recommended - Best Quality)

### Why Pandoc?
- Professional PDF output
- Excellent handling of mathematical notation
- Preserves code blocks and tables
- Industry standard for technical documentation

### Installation

```bash
sudo apt-get update
sudo apt-get install -y pandoc texlive-latex-base texlive-fonts-recommended texlive-latex-extra
```

Installation size: ~500MB

### Convert to PDF

```bash
cd /home/vigoroth/mst_research/temporal\ 3D\ detection\ \ BEV/learning_projects/project-02-perspective-transform

# Convert math_foundations.md
pandoc docs/math_foundations.md \
    -o docs/math_foundations.pdf \
    --pdf-engine=pdflatex \
    --variable geometry:margin=1in \
    --variable fontsize=11pt \
    --variable documentclass=article \
    --toc \
    --toc-depth=3 \
    --number-sections \
    --highlight-style=tango

# Convert implementation_notes.md
pandoc docs/implementation_notes.md \
    -o docs/implementation_notes.pdf \
    --pdf-engine=pdflatex \
    --variable geometry:margin=1in \
    --variable fontsize=11pt \
    --variable documentclass=article \
    --toc \
    --toc-depth=3 \
    --number-sections \
    --highlight-style=tango
```

### Verify Output

```bash
ls -lh docs/*.pdf
```

---

## Option 2: Using grip + Browser (No Installation Required)

### Installation

```bash
pip install grip
```

### Steps

1. **Start grip server for first file:**
   ```bash
   grip docs/math_foundations.md 6419
   ```

2. **Open in browser:**
   - Navigate to: `http://localhost:6419`
   - Press `Ctrl+P` (or `Cmd+P` on Mac)
   - Choose "Save as PDF"
   - Save to: `docs/math_foundations.pdf`

3. **Repeat for second file:**
   ```bash
   grip docs/implementation_notes.md 6420
   ```
   - Navigate to: `http://localhost:6420`
   - Save as: `docs/implementation_notes.pdf`

### Tips for Browser PDF:
- Set margins to "None" or "Minimal"
- Enable "Background graphics"
- Use "Letter" or "A4" paper size

---

## Option 3: Online Conversion (Quick but Manual)

### Websites

1. **CloudConvert** (Recommended)
   - URL: https://cloudconvert.com/md-to-pdf
   - Upload markdown file
   - Download PDF

2. **MarkdownToPDF**
   - URL: https://www.markdowntopdf.com/
   - Paste or upload markdown
   - Download result

3. **Aspose**
   - URL: https://products.aspose.app/pdf/conversion/md-to-pdf
   - Upload file (max 10MB)
   - Download PDF

### Pros:
- No installation required
- Quick for one-time use

### Cons:
- Privacy concerns (uploading files)
- May not handle large files well
- Limited styling control
- Must do each file separately

---

## Option 4: VS Code Extension (If using VS Code)

### Extension

Install "Markdown PDF" extension by yzane:
- Extension ID: `yzane.markdown-pdf`

### Steps

1. Open `docs/math_foundations.md` in VS Code
2. Press `Ctrl+Shift+P` (Command Palette)
3. Type "Markdown PDF: Export (pdf)"
4. Repeat for `docs/implementation_notes.md`

### Configuration

Add to VS Code `settings.json` for better output:
```json
{
    "markdown-pdf.format": "Letter",
    "markdown-pdf.margin.top": "1in",
    "markdown-pdf.margin.bottom": "1in",
    "markdown-pdf.margin.left": "1in",
    "markdown-pdf.margin.right": "1in",
    "markdown-pdf.displayHeaderFooter": true,
    "markdown-pdf.highlightStyle": "github.css"
}
```

---

## Comparison

| Method | Quality | Installation | Time | Automation |
|--------|---------|-------------|------|------------|
| **Pandoc** | ⭐⭐⭐⭐⭐ | ~500MB | ~30s each | Yes |
| **grip + Browser** | ⭐⭐⭐⭐ | ~5MB | ~2min each | Manual |
| **Online** | ⭐⭐⭐ | None | ~1min each | Manual |
| **VS Code** | ⭐⭐⭐⭐ | ~10MB | ~15s each | Semi |

---

## Recommended Workflow

### For Best Quality:
```bash
# 1. Install pandoc (one-time)
sudo apt-get update && sudo apt-get install -y pandoc texlive-latex-base texlive-fonts-recommended texlive-latex-extra

# 2. Convert both files
cd "/home/vigoroth/mst_research/temporal 3D detection  BEV/learning_projects/project-02-perspective-transform"

pandoc docs/math_foundations.md -o docs/math_foundations.pdf --pdf-engine=pdflatex --variable geometry:margin=1in --variable fontsize=11pt --toc --toc-depth=3 --number-sections --highlight-style=tango

pandoc docs/implementation_notes.md -o docs/implementation_notes.pdf --pdf-engine=pdflatex --variable geometry:margin=1in --variable fontsize=11pt --toc --toc-depth=3 --number-sections --highlight-style=tango

# 3. Verify
ls -lh docs/*.pdf
```

### For Quick Conversion:
```bash
# Use grip (already works, no sudo needed)
pip install grip

# Terminal 1:
grip docs/math_foundations.md 6419
# Open http://localhost:6419, print to PDF

# Terminal 2:
grip docs/implementation_notes.md 6420
# Open http://localhost:6420, print to PDF
```

---

## Expected Output

After successful conversion:

```
docs/
├── math_foundations.md          (source, 1,019 lines)
├── math_foundations.pdf         (output, ~2-3 MB)
├── implementation_notes.md      (source, 1,547 lines)
└── implementation_notes.pdf     (output, ~3-5 MB)
```

### PDF Features:
- ✅ Table of contents with page numbers
- ✅ Numbered sections and subsections
- ✅ Syntax-highlighted code blocks
- ✅ Formatted tables
- ✅ Clickable internal links
- ✅ Professional formatting
- ✅ Page numbers in footer

---

## Troubleshooting

### Pandoc: "pdflatex not found"
```bash
# Install missing LaTeX packages
sudo apt-get install -y texlive-latex-extra texlive-fonts-extra
```

### Pandoc: "! LaTeX Error: File 'xxx.sty' not found"
```bash
# Install full LaTeX distribution (1.5GB)
sudo apt-get install -y texlive-full
```

### grip: Browser won't open
- Manually navigate to the URL shown in terminal
- Try different browser if needed

### Online: File too large
- Files are 60KB and 110KB - should work on all platforms
- If rejected, try splitting into smaller sections

---

## Quick Start (Recommended)

**Just run these commands:**

```bash
# Option A: If you have sudo access (best quality)
sudo apt-get install -y pandoc texlive-latex-base texlive-fonts-recommended texlive-latex-extra
cd "/home/vigoroth/mst_research/temporal 3D detection  BEV/learning_projects/project-02-perspective-transform"
pandoc docs/math_foundations.md -o docs/math_foundations.pdf --pdf-engine=pdflatex --variable geometry:margin=1in --variable fontsize=11pt --toc --toc-depth=3 --number-sections --highlight-style=tango
pandoc docs/implementation_notes.md -o docs/implementation_notes.pdf --pdf-engine=pdflatex --variable geometry:margin=1in --variable fontsize=11pt --toc --toc-depth=3 --number-sections --highlight-style=tango

# Option B: No sudo access (good quality, manual)
pip install grip
grip docs/math_foundations.md 6419
# Open http://localhost:6419 in browser and save as PDF
# Then Ctrl+C and run:
grip docs/implementation_notes.md 6420
# Open http://localhost:6420 in browser and save as PDF
```

---

## Need Help?

- **Pandoc documentation:** https://pandoc.org/MANUAL.html
- **grip documentation:** https://github.com/joeyespo/grip
- **Markdown syntax:** https://www.markdownguide.org/

---

*Generated for perspective transformation project documentation*
