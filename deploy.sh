#!/bin/bash

echo "🚀 Deploying to Render..."

# Check if render CLI is installed
if ! command -v render &> /dev/null; then
    echo "❌ Render CLI not found. Please install it first:"
    echo "   brew install render (macOS)"
    echo "   or visit: https://render.com/docs/using-render-cli"
    exit 1
fi

# Deploy using render.yaml
echo "📦 Deploying service..."
render deploy

echo "✅ Deployment initiated!"
echo "🔗 Check your Render dashboard for deployment status"
echo "📊 Monitor logs: render logs real-estate-api"
