#!/bin/bash

set -e

echo "Deploying test-deploy-vercel to Vercel..."

if ! command -v vercel &> /dev/null; then
    echo "Installing Vercel CLI..."
    npm install -g vercel
fi

export VERCEL_TOKEN="test_vercel_token"

vercel --prod --yes --token "$VERCEL_TOKEN"

echo "Deployment complete!"
echo "Your app should be available at: https://test-deploy-vercel.vercel.app"
