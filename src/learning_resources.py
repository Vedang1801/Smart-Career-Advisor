SKILL_RESOURCES = {
    'python': 'https://www.coursera.org/specializations/python',
    'excel': 'https://www.coursera.org/professional-certificates/microsoft-excel-skills',
    'machine learning': 'https://www.coursera.org/learn/machine-learning',
    'deep learning': 'https://www.deeplearning.ai/deep-learning-specialization/',
    'data science': 'https://www.coursera.org/specializations/jhu-data-science',
    'rest': 'https://www.udemy.com/course/rest-api/',
    'api': 'https://www.codecademy.com/learn/paths/designing-apis-with-swagger-and-openapi',
    'c++': 'https://www.coursera.org/specializations/c-plus-plus-modern-development',
    'java': 'https://www.coursera.org/specializations/java-programming',
    'excel': 'https://www.coursera.org/learn/excel',
    'react': 'https://www.codecademy.com/learn/react-101',
    'aws': 'https://www.coursera.org/specializations/aws-fundamentals',
    'sql': 'https://www.coursera.org/learn/sql-for-data-science',
    'scikit-learn': 'https://scikit-learn.org/stable/tutorial/index.html',
    'tensorflow': 'https://www.coursera.org/professional-certificates/tensorflow-in-practice',
    'pandas': 'https://www.coursera.org/learn/data-analysis-with-python',
    'numpy': 'https://www.datacamp.com/courses/intro-to-python-for-data-science',
    'jira': 'https://www.udemy.com/course/jira-tutorial-a-comprehensive-guide-for-jira/',
    'git': 'https://www.codecademy.com/learn/learn-git',
    'docker': 'https://www.coursera.org/learn/docker',
    'kubernetes': 'https://www.coursera.org/learn/google-kubernetes-engine',

}

def get_learning_resources(skills):
    return {skill: SKILL_RESOURCES[skill] for skill in skills if skill in SKILL_RESOURCES}
