#!/bin/bash

# Git initialization and GitHub setup script for Project 2
# Usage: ./setup_git.sh <github-username>

if [ -z "$1" ]; then
    echo "Usage: ./setup_git.sh <github-username>"
    exit 1
fi

GITHUB_USER=$1
REPO_NAME="ipm-perspective-transform"

echo "=== Setting up Git repository for Project 2: IPM Perspective Transform ==="
echo ""

# Initialize git if not already initialized
if [ ! -d .git ]; then
    echo "Initializing Git repository..."
    git init
    echo "✓ Git initialized"
else
    echo "✓ Git already initialized"
fi

# Configure git user (if not set globally)
echo ""
echo "Configuring git user..."
git config user.name "$GITHUB_USER"
git config user.email "$GITHUB_USER@users.noreply.github.com"
echo "✓ Git user configured"

# Add all files
echo ""
echo "Staging files..."
git add .
echo "✓ Files staged"

# Create initial commit
echo ""
echo "Creating initial commit..."
git commit -m "Initial commit: IPM Perspective Transform project

- Complete DLT homography implementation
- IPMTransform class with 7 methods
- Educational Jupyter notebooks
- Comprehensive documentation
- GitHub Actions CI/CD setup
- 20+ unit tests with fixtures"
echo "✓ Initial commit created"

# Rename branch to main (if needed)
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo ""
    echo "Renaming branch to 'main'..."
    git branch -M main
    echo "✓ Branch renamed to main"
fi

# Add remote
echo ""
echo "Adding remote repository..."
git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
echo "✓ Remote added: https://github.com/$GITHUB_USER/$REPO_NAME.git"

echo ""
echo "=== Git setup complete! ==="
echo ""
echo "Next steps:"
echo "1. Create repository on GitHub: https://github.com/new"
echo "   - Repository name: $REPO_NAME"
echo "   - Description: Homography-based Inverse Perspective Mapping for BEV transformation (Project 2/12)"
echo "   - Public/Private: Your choice"
echo "   - Do NOT initialize with README, .gitignore, or license (we already have them)"
echo ""
echo "2. Push to GitHub:"
echo "   git push -u origin main"
echo ""
echo "3. Set up GitHub Pages (optional) for documentation"
echo ""
echo "Repository URL: https://github.com/$GITHUB_USER/$REPO_NAME"
