from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')

# Make sure to set your OpenAI API key as an environment variable: OPENAI_API_KEY

def enhance_resume_section(resume_text, jd_text, missing_skills):
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
