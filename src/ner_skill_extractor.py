import spacy
from spacy.matcher import PhraseMatcher
import subprocess
import sys

# Try to load spaCy English model, download if not available
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("en_core_web_sm model not found. Downloading...")
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load('en_core_web_sm')

# Use your COMMON_SKILLS list for phrase matching
from skills import COMMON_SKILLS

# Prepare PhraseMatcher for skills
skill_patterns = [nlp.make_doc(skill) for skill in COMMON_SKILLS]
matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
matcher.add('SKILL', skill_patterns)

def extract_skills_ner(text):
    doc = nlp(text)
    matches = matcher(doc)
    found = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        found.add(span.text.lower())
    return sorted(found)
