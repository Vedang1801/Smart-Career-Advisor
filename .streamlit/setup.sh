#!/bin/bash


echo "Checking for spaCy installation..."
if ! python3 -c "import spacy" &> /dev/null; then
    echo "spaCy not found. Installing spaCy..."
    pip install spacy
fi

echo "Installing spaCy model..."

python3 -m spacy download en_core_web_sm

echo "spaCy model installation complete ✅"
