from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def enhance_resume_section(resume_text, jd_text, missing_skills):
    # Get API key from environment or Streamlit secrets
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        try:
            openai_api_key = st.secrets["OPENAI_API_KEY"]
        except:
            st.error("⚠️ OpenAI API key not found. Please set OPENAI_API_KEY in environment variables or Streamlit secrets.")
            return "OpenAI API key not configured. Please contact the administrator."
    
    if not openai_api_key:
        return "OpenAI API key not available. Please configure your API key to use this feature."
    
    try:
        prompt = PromptTemplate(
            input_variables=["resume", "jd", "missing_skills"],
            template=(
                "You are a career coach AI. Given the following resume section, job description, and missing skills, "
                "suggest improved wording for the resume section to better match the job description and address the missing skills.\n"
                "Resume Section:\n{resume}\n"
                "Job Description:\n{jd}\n"
                "Missing Skills:\n{missing_skills}\n"
                "Improved Resume Section:"
            )
        )
        llm = OpenAI(temperature=0.3, openai_api_key=openai_api_key)
        return llm(
            prompt.format(
                resume=resume_text,
                jd=jd_text,
                missing_skills=", ".join(missing_skills)
            )
        )
    except Exception as e:
        st.error(f"Error enhancing resume: {str(e)}")
        return "Unable to generate resume improvements at this time. Please try again later."
