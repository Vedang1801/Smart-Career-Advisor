import streamlit as st
import spacy
import subprocess
from spacy.matcher import PhraseMatcher
from skills import COMMON_SKILLS

@st.cache_resource
def load_nlp():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        # Download model if not present
        subprocess.run(["python3", "-m", "spacy", "download", "en_core_web_sm"], check=True)
        return spacy.load("en_core_web_sm")

def extract_skills_ner(text):
    nlp = load_nlp()  # ✅ Load only when needed, after model is downloaded
    doc = nlp(text)
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    matcher.add("SKILLS", [[nlp.make_doc(skill)] for skill in COMMON_SKILLS])
    matches = matcher(doc)
    skills_found = list(set([doc[start:end].text for match_id, start, end in matches]))
    return skills_found
