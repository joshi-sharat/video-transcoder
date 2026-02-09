#!/bin/bash

# Push to GitHub Script

echo "🚀 Video Transcoder - GitHub Push Helper"
echo "========================================"
echo ""

REPO_NAME="video-transcoder"
GITHUB_USER="joshi-sharat"
REPO_URL="https://github.com/$GITHUB_USER/$REPO_NAME.git"

echo "This script will help you push your project to GitHub."
echo ""
echo "Repository: $GITHUB_USER/$REPO_NAME"
echo "URL: $REPO_URL"
echo ""
echo "⚠️  IMPORTANT: Make sure you've created the repository on GitHub first!"
echo "   Go to: https://github.com/new"
echo "   Repository name: $REPO_NAME"
echo "   Do NOT initialize with README, .gitignore, or license"
echo ""

read -p "Have you created the repository on GitHub? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Please create the repository first, then run this script again."
    echo "Visit: https://github.com/new"
    exit 1
fi

echo ""
echo "📡 Adding remote repository..."
git remote add origin $REPO_URL 2>/dev/null || git remote set-url origin $REPO_URL

echo "🔄 Renaming branch to 'main'..."
git branch -M main

echo "📤 Pushing to GitHub..."
echo ""
echo "You may be prompted for your GitHub credentials."
echo "If you have 2FA enabled, use a Personal Access Token instead of your password."
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Success! Your code has been pushed to GitHub!"
    echo ""
    echo "🔗 Repository URL: https://github.com/$GITHUB_USER/$REPO_NAME"
    echo ""
    echo "Next steps:"
    echo "  1. Visit your repository: https://github.com/$GITHUB_USER/$REPO_NAME"
    echo "  2. Add a description and topics"
    echo "  3. Star your own repository! ⭐"
else
    echo ""
    echo "❌ Push failed. Common issues:"
    echo ""
    echo "1. Repository doesn't exist on GitHub"
    echo "   → Create it at: https://github.com/new"
    echo ""
    echo "2. Authentication failed"
    echo "   → If you have 2FA, create a Personal Access Token"
    echo "   → Visit: https://github.com/settings/tokens"
    echo ""
    echo "3. Wrong credentials"
    echo "   → Make sure you're using the correct username and password/token"
    echo ""
    echo "See GITHUB_SETUP.md for detailed instructions."
fi
