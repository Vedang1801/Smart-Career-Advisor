import streamlit as st
import sys
import os
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from parsing import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt
from skills import extract_skills
from llm_enhancer import enhance_resume_section
from learning_resources import get_learning_resources
from project_ideas import generate_project_ideas
from fit_classifier import predict_fit
# Keep import but don't use it unless explicitly requested
from ner_skill_extractor import extract_skills_ner

load_dotenv()

# Sidebar for instructions and info
with st.sidebar:
    st.markdown('# 📋 How to Use')
    st.markdown('---')
    
    st.markdown('''
    ### Step-by-Step Guide:
    
    **1. 📄 Upload Documents**
    - Upload your resume (PDF/DOCX)
    - Upload job description (PDF/DOCX/TXT)
    
    **2. 🔍 Document Analysis**
    - Review extracted text
    - Check detected skills
    
    **3. 📊 Skill Matching**
    - View your compatibility score
    - Identify missing skills
    
    **4. 🎯 AI Recommendations**
    - Get learning resources
    - Generate project ideas
    - Improve your resume with AI
    ''')
    
    st.markdown('---')
    st.markdown('### 🔒 Privacy Notice')
    st.info('Your documents are processed locally and never stored on our servers.')
    
    st.markdown('### 🛠️ Technology Stack')
    with st.expander('View Tech Details'):
        st.markdown('''
        - **AI/ML**: OpenAI GPT, scikit-learn
        - **NLP**: spaCy, LangChain
        - **UI**: Streamlit
        - **Parsing**: PyPDF2, python-docx
        ''')

st.title('Smart Career Advisor AI')
st.markdown('''
<div style="text-align: center; padding: 10px; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 20px;">
    <span style="font-size:1.2em; color:white; font-weight:500;">AI-powered assistant for resume optimization, job matching, and career growth</span>
</div>
''', unsafe_allow_html=True)

# Try to use NER if available, otherwise fall back to basic extraction
try:
    # Create a flag to indicate which method is being used
    use_ner = True
    # Try importing spaCy to see if it's available
    import spacy
    try:
        # Check if model can be loaded
        spacy.load("en_core_web_sm")
    except:
        use_ner = False
except:
    use_ner = False

# UI indicator showing which extraction method is being used
extraction_mode = "spaCy NER" if use_ner else "Basic Extraction"
st.markdown(f"<div style='text-align:center; margin-bottom:10px;'><span style='background:#e0e7ff; color:#3730a3; padding:6px 18px; border-radius:20px; font-weight:600; font-size:1em;'>🧠 Skill Extraction Mode: <b>{extraction_mode}</b></span></div>", unsafe_allow_html=True)

st.divider()

st.markdown('## 📁 Upload Documents')
st.markdown('Upload your resume and job description to get started with AI-powered analysis.')

col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown('### 📄 Your Resume')
    resume_file = st.file_uploader(
        'Choose your resume file', 
        type=['pdf', 'docx'], 
        help='Supported formats: PDF, DOCX (max 10MB)',
        key='resume_upload'
    )
    if resume_file:
        st.success(f'✅ {resume_file.name} uploaded successfully!')
        
with col2:
    st.markdown('### 💼 Job Description')
    jd_file = st.file_uploader(
        'Choose job description file', 
        type=['pdf', 'docx', 'txt'], 
        help='Supported formats: PDF, DOCX, TXT (max 10MB)',
        key='jd_upload'
    )
    if jd_file:
        st.success(f'✅ {jd_file.name} uploaded successfully!')

resume_text = None
jd_text = None

if resume_file:
    if resume_file.type == 'application/pdf':
        resume_text = extract_text_from_pdf(resume_file)
    elif resume_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        resume_text = extract_text_from_docx(resume_file)
    else:
        st.warning('Unsupported resume file type.')

if jd_file:
    if jd_file.type == 'application/pdf':
        jd_text = extract_text_from_pdf(jd_file)
    elif jd_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        jd_text = extract_text_from_docx(jd_file)
    elif jd_file.type == 'text/plain':
        jd_text = extract_text_from_txt(jd_file)
    else:
        st.warning('Unsupported Job Description file type.')

if resume_text or jd_text:
    st.markdown('---')
    st.markdown('## 🔍 Document Analysis')
    st.markdown('Review the extracted text and detected skills from your documents.')
    
    tab1, tab2 = st.tabs(['📄 Resume Analysis', '💼 Job Description Analysis'])
    
    with tab1:
        if resume_text:
            # Stats about resume
            word_count = len(resume_text.split())
            char_count = len(resume_text)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric('Word Count', word_count)
            with col2:
                st.metric('Character Count', char_count)
            with col3:
                st.metric('Status', 'Processed ✅')
            
            with st.expander('View Extracted Resume Text', expanded=False):
                st.text_area('Resume Content', resume_text, height=200, key='resume_text_display')
            
            # Skills extraction
            with st.spinner('🔍 Extracting skills from resume...'):
                if use_ner:
                    try:
                        resume_skills = extract_skills_ner(resume_text)
                    except Exception as e:
                        st.warning(f"NER extraction failed, falling back to basic extraction: {str(e)}")
                        resume_skills = extract_skills(resume_text)
                        # Update the UI indicator if NER fails at runtime
                        st.markdown(f"<div style='text-align:center; margin-bottom:10px;'><span style='background:#e0e7ff; color:#3730a3; padding:6px 18px; border-radius:20px; font-weight:600; font-size:1em;'>🧠 Skill Extraction Mode: <b>Basic Extraction</b></span></div>", unsafe_allow_html=True)
                else:
                    resume_skills = extract_skills(resume_text)
            
            if resume_skills:
                st.success(f'✅ Found {len(resume_skills)} skills in your resume')
                with st.expander(' Skills Detected in Resume', expanded=True):
                    # Display skills in a nice grid
                    cols = st.columns(3)
                    for i, skill in enumerate(sorted(resume_skills)):
                        with cols[i % 3]:
                            st.markdown(f'🔸 **{skill}**')
            else:
                st.warning('⚠️ No common technical skills detected in resume')
        else:
            st.info('📤 Upload a resume to see detailed analysis')
    
    with tab2:
        if jd_text:
            # Stats about job description
            word_count_jd = len(jd_text.split())
            char_count_jd = len(jd_text)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric('Word Count', word_count_jd)
            with col2:
                st.metric('Character Count', char_count_jd)
            with col3:
                st.metric('Status', 'Processed ✅')
            
            with st.expander('View Extracted Job Description Text', expanded=False):
                st.text_area('Job Description Content', jd_text, height=200, key='jd_text_display')
            
            # Skills extraction
            with st.spinner('🔍 Extracting required skills...'):
                if use_ner:
                    try:
                        jd_skills = extract_skills_ner(jd_text)
                    except Exception as e:
                        st.warning(f"NER extraction failed, falling back to basic extraction: {str(e)}")
                        jd_skills = extract_skills(jd_text)
                else:
                    jd_skills = extract_skills(jd_text)
            
            if jd_skills:
                st.success(f'✅ Found {len(jd_skills)} required skills')
                with st.expander('Skills Required for Job', expanded=True):
                    # Display skills in a nice grid
                    cols = st.columns(3)
                    for i, skill in enumerate(sorted(jd_skills)):
                        with cols[i % 3]:
                            st.markdown(f'🔹 **{skill}**')
            else:
                st.warning('⚠️ No common technical skills detected in job description')
        else:
            st.info('📤 Upload a job description to see detailed analysis')

if resume_text and jd_text and resume_skills and jd_skills:
    st.markdown('---')
    
    # Skill Match Analysis
    matched_skills = set(resume_skills) & set(jd_skills)
    missing_skills = set(jd_skills) - set(resume_skills)
    extra_skills = set(resume_skills) - set(jd_skills)
    match_score = len(matched_skills) / len(jd_skills) * 100 if jd_skills else 0
    
    st.markdown('## 📊 Skill Match Analysis')
    st.markdown('Comprehensive analysis of how well your skills align with job requirements.')
    
    # Display metrics in a beautiful card layout
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label='🎯 Match Score', 
            value=f'{match_score:.1f}%',
            delta=f"{match_score-50:.1f}% vs avg" if match_score > 0 else None
        )
    with col2:
        st.metric(
            label='✅ Matched Skills', 
            value=len(matched_skills),
            delta=f"{len(matched_skills)} found"
        )
    with col3:
        st.metric(
            label='❌ Missing Skills', 
            value=len(missing_skills),
            delta=f"{len(missing_skills)} to learn"
        )
    with col4:
        st.metric(
            label='Extra Skills', 
            value=len(extra_skills),
            delta=f"{len(extra_skills)} bonus"
        )
    
    # Enhanced progress bar with color coding and better messaging
    st.markdown('### 🏆 Compatibility Assessment')
    
    if match_score >= 80:
        st.success(f'🌟 Outstanding match! You have {match_score:.1f}% skill compatibility')
        progress_color = "🟢"
    elif match_score >= 60:
        st.success(f'✅ Excellent match! {match_score:.1f}% skill compatibility')
        progress_color = "🟢"
    elif match_score >= 40:
        st.warning(f'⚡ Good match with growth potential: {match_score:.1f}% compatibility')
        progress_color = "🟡"
    elif match_score >= 20:
        st.warning(f'🔄 Moderate match - skill development recommended: {match_score:.1f}% compatibility')
        progress_color = "🟡"
    else:
        st.error(f'🎯 Growth opportunity - consider targeted skill development: {match_score:.1f}% compatibility')
        progress_color = "🔴"
    
    # Progress bar
    progress_col1, progress_col2 = st.columns([8, 1])
    with progress_col1:
        st.progress(match_score/100)
    with progress_col2:
        st.markdown(f"**{progress_color}**")
    
    # Detailed skill breakdown with enhanced visualization
    with st.expander('🔍 Detailed Skill Breakdown', expanded=True):
        skill_tab1, skill_tab2, skill_tab3 = st.tabs(['✅ Matched Skills', '❌ Missing Skills', ' Extra Skills'])
        
        with skill_tab1:
            if matched_skills:
                st.markdown(f'**You have {len(matched_skills)} skills that match the job requirements:**')
                st.markdown('---')
                cols = st.columns(2)
                for i, skill in enumerate(sorted(matched_skills)):
                    with cols[i % 2]:
                        st.markdown(f'✅ **{skill}**')
            else:
                st.markdown('🚫 _No directly matched skills found_')
        
        with skill_tab2:
            if missing_skills:
                st.markdown(f'**Focus on developing these {len(missing_skills)} skills:**')
                st.markdown('---')
                cols = st.columns(2)
                for i, skill in enumerate(sorted(missing_skills)):
                    with cols[i % 2]:
                        st.markdown(f'🎯 **{skill}**')
            else:
                st.markdown('🎉 _You have all required skills!_')
        
        with skill_tab3:
            if extra_skills:
                st.markdown(f'**You have {len(extra_skills)} additional valuable skills:**')
                st.markdown('---')
                cols = st.columns(2)
                for i, skill in enumerate(sorted(extra_skills)):
                    with cols[i % 2]:
                        st.markdown(f'∙ **{skill}**')
            else:
                st.markdown('💼 _No additional skills detected beyond job requirements_')

    st.markdown('---')
    
    # ML Fit Classifier with enhanced presentation
    st.markdown('## AI Fit Assessment')
    st.markdown('Our machine learning model analyzes multiple factors to predict job compatibility.')
    
    with st.spinner('AI is analyzing your profile...'):
        pred, prob = predict_fit(match_score, len(matched_skills), len(missing_skills))
    
    fit_label = 'Strong Candidate' if pred == 1 else 'Needs Development'
    
    # Create assessment card
    assessment_col1, assessment_col2 = st.columns([2, 1])
    
    with assessment_col1:
        if pred == 1:
            st.success(f'🎉 **AI Prediction: {fit_label}**')
            st.markdown('The AI model indicates you are well-suited for this role based on your skill profile.')
        else:
            st.warning(f'📈 **AI Prediction: {fit_label}**')
            st.markdown('The AI suggests focusing on skill development to improve your candidacy.')
    
    with assessment_col2:
        # Confidence meter
        confidence_level = "High" if prob > 0.8 else "Medium" if prob > 0.6 else "Low"
        confidence_color = "🟢" if prob > 0.8 else "🟡" if prob > 0.6 else "🔴"
        
        st.metric(
            label='🎯 AI Confidence', 
            value=f'{prob*100:.1f}%',
            delta=f"{confidence_level} {confidence_color}"
        )
    
    # Additional insights
    with st.expander('🔍 AI Assessment Details', expanded=False):
        st.markdown('**Factors considered by the AI model:**')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'📊 **Match Score**: {match_score:.1f}%')
        with col2:
            st.markdown(f'✅ **Skills Matched**: {len(matched_skills)}')
        with col3:
            st.markdown(f'📚 **Skills to Learn**: {len(missing_skills)}')
        
        st.markdown('---')
        st.markdown(' **Recommendation**: ' + (
            'You have a strong foundation for this role. Consider highlighting your matched skills in your application.' 
            if pred == 1 else 
            'Focus on developing the missing skills through courses, projects, or certifications to improve your candidacy.'
        ))

    st.divider()
    
    # Learning Resources
    if missing_skills:
        st.subheader('📚 Skill Development Resources')
        resources = get_learning_resources(missing_skills)
        if resources:
            st.success(f'Found learning resources for {len(resources)} out of {len(missing_skills)} missing skills:')
            
            # Display resources in a nice format
            for skill, url in resources.items():
                st.markdown(f'🎯 **{skill.title()}** → [Learn Here]({url})')
            
            # Show skills without direct resources if any
            skills_without_resources = set(missing_skills) - set(resources.keys())
            if skills_without_resources:
                st.info(f'💡 No direct resources found for: {", ".join(sorted(skills_without_resources))}. Consider searching for these on platforms like Coursera, Udemy, or YouTube.')
        else:
            st.info('💡 No direct resources found for these skills. Consider searching for them on platforms like Coursera, Udemy, Codecademy, or YouTube.')
        
        st.divider()

    # AI-Powered Recommendations with improved layout
    st.markdown('##  AI-Powered Recommendations')

    # Initialize session state for storing generated content
    if 'resume_improvements' not in st.session_state:
        st.session_state.resume_improvements = None
    if 'project_ideas' not in st.session_state:
        st.session_state.project_ideas = None
    
    # Resume Enhancement Section
    st.markdown('### 📝 Resume Enhancement')
    st.markdown('Improve your resume with AI-powered suggestions tailored to the job requirements.')
    
    if st.button(' Get Resume Improvements', use_container_width=True, type='primary'):
        with st.spinner(' Analyzing resume and generating improvements...'):
            improved = enhance_resume_section(resume_text, jd_text, list(missing_skills))
            st.session_state.resume_improvements = improved
        st.success('✅ Resume improvements generated successfully!')
    
    # Display resume improvements if they exist in session state
    if st.session_state.resume_improvements:
        st.markdown('---')
        st.markdown('####  AI Resume Suggestions')
        st.markdown(st.session_state.resume_improvements)
        
        # Option to copy or download
        with st.expander('📋 View in Text Format (for copying)', expanded=False):
            st.text_area('Resume Improvements', st.session_state.resume_improvements, height=400, key='resume_copy')
        
        # Clear button
        if st.button(' Clear Resume Suggestions', key='clear_resume'):
            st.session_state.resume_improvements = None
            st.rerun()
    
    st.markdown('---')
    
    # Project Ideas Section  
    st.markdown('###  Project Ideas Generator')
    st.markdown('Get personalized project ideas to strengthen your portfolio and demonstrate your skills.')
    
    if st.button(' Get Project Ideas', use_container_width=True, type='primary'):
        with st.spinner(' Generating personalized project ideas...'):
            ideas = generate_project_ideas(resume_text, resume_skills)
            st.session_state.project_ideas = ideas
        st.success('✅ Project ideas generated successfully!')
    
    # Display project ideas if they exist in session state
    if st.session_state.project_ideas:
        st.markdown('---')
        st.markdown('####  Personalized Project Suggestions')
        st.markdown(st.session_state.project_ideas)
        
        # Option to copy or download
        with st.expander(' View in Text Format (for copying)', expanded=False):
            st.text_area('Project Ideas', st.session_state.project_ideas, height=400, key='projects_copy')
        
        # Clear button
        if st.button(' Clear Project Ideas', key='clear_projects'):
            st.session_state.project_ideas = None
            st.rerun()
else:
    st.info('Upload both resume and Job Description files to see skill match analysis and improvement suggestions.')
