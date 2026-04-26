#!/bin/bash

echo "Installing system dependencies (FIX GLIB issue)..."

apt-get update -y

apt-get install -y \
    chromium \
    libglib2.0-0 \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    libxshmfence1

echo "Installing Playwright browsers with dependencies..."
python -m playwright install --with-deps chromium
