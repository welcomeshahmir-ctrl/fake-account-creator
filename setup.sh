#!/bin/bash

echo "Installing system dependencies..."
apt-get update
apt-get install -y chromium

echo "Installing Playwright browsers..."
playwright install
playwright install chromium
