import spacy
from spacy.matcher import PhraseMatcher

# Try to load spaCy English model, fallback to basic extraction if not available
try:
    nlp = spacy.load('en_core_web_sm')
    USE_NER = True
except OSError:
    print("[WARNING] spaCy model 'en_core_web_sm' not found. Falling back to basic skill extraction.")
    nlp = None
    USE_NER = False

from skills import COMMON_SKILLS, extract_skills

if USE_NER and nlp:
    skill_patterns = [nlp.make_doc(skill) for skill in COMMON_SKILLS]
    matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
    matcher.add('SKILL', skill_patterns)

def extract_skills_ner(text):
    if USE_NER and nlp:
        doc = nlp(text)
        matches = matcher(doc)
        found = set()
        for match_id, start, end in matches:
            span = doc[start:end]
            found.add(span.text.lower())
        return sorted(found)
    else:
        # Fallback to basic extraction
        return extract_skills(text)
