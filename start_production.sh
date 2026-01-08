#!/bin/bash
# Source nvm and use Node 22
source ~/.nvm/nvm.sh
nvm use 22

# Build the project
npm run build

# Start the production server using PM2
pm2 delete infinite-canvas-charts || true
pm2 start "npx serve -s dist -l 4405" --name infinite-canvas-charts
