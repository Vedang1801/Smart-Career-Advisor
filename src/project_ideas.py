from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

def generate_project_ideas(resume_text, skills):
    prompt = PromptTemplate(
        input_variables=["resume", "skills"],
        template=(
            "Based on the following resume and skills, suggest 3 impactful project topic and decription  which tackle real life problems (not limited to AI/ML) that align with the candidate's background and would impress recruiters in their field.\n"
            "Resume:\n{resume}\n"
            "Skills:\n{skills}\n"
            "Project Ideas:"
        )
    )
    llm = OpenAI(temperature=0.5, openai_api_key=openai_api_key)
    return llm(
        prompt.format(
            resume=resume_text,
            skills=", ".join(skills)
        )
    )
