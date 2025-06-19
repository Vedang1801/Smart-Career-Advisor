import spacy
from spacy.matcher import PhraseMatcher

# Load spaCy English model
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
