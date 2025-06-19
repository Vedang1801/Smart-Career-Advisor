#!/bin/bash

echo "Setting up spaCy environment..."

# Check if spaCy model is available
if python3 -c "import en_core_web_sm" &> /dev/null; then
    echo "✅ spaCy model already available"
else
    echo "⚠️ spaCy model not found, but app will work with basic skill extraction"
fi

echo "Setup complete ✅"
