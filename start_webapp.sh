#!/bin/bash

if [ -z ${VIRTUAL_ENV} ]; then 
    source venv/bin/activate
fi
if ! pgrep -f "python3 -m backend.main" > /dev/null; then
    python3 -m backend.main &
fi

cd frontend
if ! pgrep -f "npm run dev" > /dev/null; then
    npm run dev
fi