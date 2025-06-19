from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def generate_project_ideas(resume_text, skills):
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
            input_variables=["resume", "skills"],
            template=(
                "Based on the following resume and skills, suggest 3 impactful project topics and descriptions which tackle real life problems (not limited to AI/ML) that align with the candidate's background and would impress recruiters in their field.\n"
                "Resume:\n{resume}\n"
                "Skills:\n{skills}\n"
                "Project Ideas:"
            )
        )
        llm = OpenAI(temperature=0.5, api_key=openai_api_key)
        return llm.invoke(
            prompt.format(
                resume=resume_text,
                skills=", ".join(skills)
            )
        )
    except Exception as e:
        st.error(f"Error generating project ideas: {str(e)}")
        return "Unable to generate project ideas at this time. Please try again later."
