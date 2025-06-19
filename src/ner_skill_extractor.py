import streamlit as st
import spacy
from spacy.matcher import PhraseMatcher
from skills import COMMON_SKILLS

@st.cache_resource
def load_nlp():
    """Load spaCy model with multiple fallback methods for robust deployment."""
    try:
        # Method 1: Try direct import first (fastest if model is installed)
        try:
            import en_core_web_sm
            return en_core_web_sm.load()
        except ImportError:
            pass
        
        # Method 2: Try standard spacy load
        try:
            return spacy.load("en_core_web_sm")
        except (OSError, IOError):
            pass
        
        # Method 3: Try to install via pip and then load
        try:
            st.info("📦 Installing spaCy model for enhanced skill extraction...")
            import subprocess
            import sys
            
            # Try pip install first (more reliable than spacy download)
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.6.0/en_core_web_sm-3.6.0-py3-none-any.whl"
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                st.success("✅ spaCy model installed successfully!")
                try:
                    return spacy.load("en_core_web_sm")
                except:
                    # Try direct import after installation
                    import en_core_web_sm
                    return en_core_web_sm.load()
            
        except Exception as install_error:
            st.info(f"ℹ️ Model installation failed: {str(install_error)}")
        
        # Method 4: Try spaCy CLI download as fallback
        try:
            st.info("🔄 Trying alternative installation method...")
            result = subprocess.run([
                sys.executable, "-m", "spacy", "download", "en_core_web_sm"
            ], capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                st.success("✅ spaCy model downloaded via CLI!")
                return spacy.load("en_core_web_sm")
                
        except Exception as cli_error:
            st.info(f"ℹ️ CLI download failed: {str(cli_error)}")
        
        # If all methods fail, return None to trigger basic extraction
        st.info("ℹ️ Advanced NLP model not available - using basic skill extraction")
        return None
            
    except Exception as e:
        st.info("ℹ️ Using basic skill extraction")
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
