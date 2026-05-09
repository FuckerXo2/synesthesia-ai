#!/bin/bash

# 🚀 SYNESTHESIA DEPLOYMENT SCRIPT

echo "=================================="
echo "🚀 SYNESTHESIA DEPLOYMENT"
echo "=================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git not initialized!"
    exit 1
fi

echo "✅ Git repository ready"
echo ""

# Check if remote exists
if git remote | grep -q "origin"; then
    echo "✅ GitHub remote already configured"
    REMOTE_URL=$(git remote get-url origin)
    echo "   Remote: $REMOTE_URL"
else
    echo "⚠️  No GitHub remote configured"
    echo ""
    echo "📝 NEXT STEPS:"
    echo "1. Create GitHub repo at: https://github.com/new"
    echo "2. Name it: synesthesia-ai"
    echo "3. Make it PUBLIC"
    echo "4. Run this command (replace YOUR_USERNAME):"
    echo ""
    echo "   git remote add origin https://github.com/YOUR_USERNAME/synesthesia-ai.git"
    echo "   git push -u origin main"
    echo ""
    exit 0
fi

# Check if we can push
echo ""
echo "🔄 Checking if we can push to GitHub..."

if git push --dry-run origin main 2>&1 | grep -q "Everything up-to-date"; then
    echo "✅ Already pushed to GitHub"
elif git push --dry-run origin main 2>&1 | grep -q "fatal"; then
    echo "⚠️  Need to push to GitHub first"
    echo ""
    read -p "Push to GitHub now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git push -u origin main
        echo "✅ Pushed to GitHub!"
    else
        echo "❌ Cancelled"
        exit 0
    fi
else
    echo "✅ Can push to GitHub"
fi

echo ""
echo "=================================="
echo "📦 DEPLOYMENT CHECKLIST"
echo "=================================="
echo ""
echo "✅ Git repository initialized"
echo "✅ Code committed"
echo "✅ GitHub remote configured"
echo ""
echo "🚂 NEXT: Deploy to Railway"
echo ""
echo "1. Go to: https://railway.app"
echo "2. Sign up with GitHub"
echo "3. Click 'New Project'"
echo "4. Select 'Deploy from GitHub repo'"
echo "5. Choose: synesthesia-ai"
echo "6. Add environment variables (see DEPLOYMENT_STEPS.md)"
echo "7. Get your Railway URL"
echo "8. Submit to hackathon!"
echo ""
echo "📝 Full instructions: DEPLOYMENT_STEPS.md"
echo ""
echo "=================================="
echo "🎯 HACKATHON SUBMISSION"
echo "=================================="
echo ""
echo "Submit this link:"
echo "https://synesthesia-production-xxxx.up.railway.app"
echo ""
echo "(Replace xxxx with your actual Railway URL)"
echo ""
echo "=================================="
echo "✨ You got this! 5 days left!"
echo "=================================="
