#!/bin/bash

# PDF Conversion Script using Pandoc
# Converts markdown documentation to professional PDFs

set -e  # Exit on error

echo "=========================================="
echo "PDF Conversion Script - Pandoc"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo -e "${YELLOW}Pandoc not found. Installing dependencies...${NC}"
    echo ""
    echo "This will install:"
    echo "  - pandoc"
    echo "  - texlive-latex-base"
    echo "  - texlive-fonts-recommended"
    echo "  - texlive-latex-extra"
    echo ""
    echo "Total size: ~500MB"
    echo "This may take 5-10 minutes..."
    echo ""
    read -p "Press Enter to continue or Ctrl+C to cancel..."

    sudo apt-get update
    sudo apt-get install -y pandoc texlive-latex-base texlive-fonts-recommended texlive-latex-extra

    echo -e "${GREEN}✓ Installation complete!${NC}"
    echo ""
else
    echo -e "${GREEN}✓ Pandoc is already installed${NC}"
    pandoc --version | head -1
    echo ""
fi

# Navigate to project directory
PROJECT_DIR="/home/vigoroth/mst_research/temporal 3D detection  BEV/learning_projects/project-02-perspective-transform"
cd "$PROJECT_DIR"

echo "Working directory: $PROJECT_DIR"
echo ""

# Convert first file
echo "=========================================="
echo "Converting math_foundations.md..."
echo "=========================================="

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

if [ -f docs/math_foundations.pdf ]; then
    SIZE=$(du -h docs/math_foundations.pdf | cut -f1)
    echo -e "${GREEN}✓ Successfully created docs/math_foundations.pdf (${SIZE})${NC}"
else
    echo -e "${RED}✗ Failed to create math_foundations.pdf${NC}"
    exit 1
fi

echo ""

# Convert second file
echo "=========================================="
echo "Converting implementation_notes.md..."
echo "=========================================="

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

if [ -f docs/implementation_notes.pdf ]; then
    SIZE=$(du -h docs/implementation_notes.pdf | cut -f1)
    echo -e "${GREEN}✓ Successfully created docs/implementation_notes.pdf (${SIZE})${NC}"
else
    echo -e "${RED}✗ Failed to create implementation_notes.pdf${NC}"
    exit 1
fi

echo ""
echo "=========================================="
echo "Conversion Complete!"
echo "=========================================="
echo ""
echo "Created files:"
ls -lh docs/*.pdf | awk '{print "  " $9 " (" $5 ")"}'
echo ""
echo "To view the PDFs:"
echo "  xdg-open docs/math_foundations.pdf"
echo "  xdg-open docs/implementation_notes.pdf"
echo ""
