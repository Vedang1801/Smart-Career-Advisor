# Smart Career Advisor AI

A Job Search and Resume Advisor AI assistant that:
- Takes your resume & job description as input
- Parses them
- Gives match score + improvement suggestions
- Uses LLMs to rewrite resume sections
- Shows skills gap + recommends learning resources
- Suggests project ideas based on user’s skills & goals

## Tech Stack
- Python, LangChain, OpenAI, Streamlit, scikit-learn, PyPDF, python-docx, BeautifulSoup

## Setup & Installation

### Prerequisites
- Python 3.11+ installed
- OpenAI API key

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Smart-Career-Advisor-AI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Setup environment variables**
   ```bash
   # Create .env file in the root directory
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   streamlit run app/main.py
   ```

The application will open in your default browser at `http://localhost:8501`

### Alternative Run Methods
```bash
# Using Python module
python -m streamlit run app/main.py

# Specify port
streamlit run app/main.py --server.port 8502
```

## Folder Structure
- `src/` - Core logic (parsing, LLM, ML, etc)
- `app/` - Streamlit app
- `data/` - Sample resumes/JDs

## Roadmap
- Resume/JD parsing
- Skill extraction & matching
- LLM-based resume enhancer
- Skill gap analysis & recommendations
- Project idea generator

---

> “Developed an AI-powered career assistant using LangChain, OpenAI, and ML models that dynamically analyzes job descriptions and optimizes resumes with actionable feedback, closing skill gaps and suggesting projects.”
