#!/bin/bash

echo "🔧 Setting up spaCy environment..."

# Download spaCy model using pip (more reliable than spacy download)
echo "📦 Installing spaCy model..."
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.4.1/en_core_web_sm-3.4.1-py3-none-any.whl

# Verify installation
if python3 -c "import en_core_web_sm; print('✅ spaCy model loaded successfully')" 2>/dev/null; then
    echo "✅ spaCy setup complete"
else
    echo "⚠️ spaCy model installation failed, app will use basic extraction"
fi
