import streamlit as st
import spacy
from spacy.matcher import PhraseMatcher
from skills import COMMON_SKILLS

@st.cache_resource
def load_nlp():
    return spacy.load("en_core_web_sm")

def extract_skills_ner(text):
    nlp = load_nlp()  # ✅ Load only when needed, after model is downloaded
    doc = nlp(text)
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    matcher.add("SKILLS", [[nlp.make_doc(skill)] for skill in COMMON_SKILLS])
    matches = matcher(doc)
    skills_found = list(set([doc[start:end].text for match_id, start, end in matches]))
    return skills_found
