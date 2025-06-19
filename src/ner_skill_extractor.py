import streamlit as st
import spacy
from spacy.matcher import PhraseMatcher
from skills import COMMON_SKILLS

@st.cache_resource
def load_nlp():
    try:
        # Try multiple model loading approaches
        try:
            # Method 1: Direct import (works when installed via wheel)
            import en_core_web_sm
            return en_core_web_sm.load()
        except ImportError:
            pass
        
        # Method 2: Standard spacy.load
        return spacy.load("en_core_web_sm")
    except (OSError, IOError) as e:
        st.info("ℹ️ Advanced NLP model not available - using basic skill extraction")
        return None

def extract_skills_ner(text):
    try:
        nlp = load_nlp()
        if nlp is None:
            raise RuntimeError("spaCy NER model not available; use basic extraction instead.")
        
        doc = nlp(text)
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        
        # Create patterns correctly - flat list of Doc objects, not nested lists
        patterns = [nlp.make_doc(skill) for skill in COMMON_SKILLS]
        matcher.add("SKILLS", patterns)
        
        matches = matcher(doc)
        skills_found = list(set([doc[start:end].text for match_id, start, end in matches]))
        return skills_found
        
    except Exception as e:
        raise RuntimeError(f"spaCy NER extraction failed: {str(e)}")
