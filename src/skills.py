import re

COMMON_SKILLS = [
    # Programming Languages
    'python', 'java', 'c++', 'c#', 'go', 'rust', 'typescript', 'javascript', 'swift', 'kotlin', 'ruby', 'php', 'perl', 'objective-c', 'r', 'matlab', 'dart', 'scala', 'groovy', 'lua', 'visual basic', 'assembly', 'fortran', 'cobol', 'delphi', 'abap', 'sas',
    # Web & Frameworks (Frontend & Backend, old & new)
    'html', 'html5', 'css', 'css3', 'react', 'reactjs', 'react native', 'angular', 'angularjs', 'vue', 'vuejs', 'svelte', 'ember', 'backbone', 'jquery', 'jQuery', 'bootstrap', 'tailwind', 'material-ui', 'redux', 'webpack', 'babel', 'next.js', 'nuxt.js', 'meteor', 'express', 'expressjs', 'node', 'nodejs', 'fastapi', 'flask', 'django', 'spring', 'spring boot', 'struts', 'grails', 'laravel', 'symfony', 'cakephp', 'zend', 'codeigniter', 'yii', 'asp.net', 'dotnet', 'dotnet core', 'rails', 'ruby on rails', 'phoenix', 'play', 'fiber', 'hapi', 'koa', 'adonis', 'nestjs', 'quasar', 'alpinejs', 'stimulus', 'pyramid', 'tornado', 'bottle', 'web2py', 'cherrypy', 'coldfusion', 'servlet', 'jsp', 'blade', 'sinatra', 'mason', 'mojolicious', 'plack', 'rocket', 'actix', 'vapor', 'actix-web',
    # Full Stack/Backend/Frontend
    'full stack', 'frontend', 'backend', 'rest', 'graphql', 'grpc', 'microservices', 'api', 'mvc', 'spa', 'ssr', 'pwa',
    # Data & ML
    'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'xgboost', 'catboost', 'mlops', 'machine learning', 'deep learning', 'nlp', 'computer vision', 'data analysis', 'data science',
    # Databases
    'sql', 'mysql', 'postgresql', 'mssql', 'sqlite', 'oracle', 'mongodb', 'redis', 'cassandra', 'dynamodb', 'couchdb', 'elasticsearch', 'neo4j', 'arangodb', 'bigquery', 'snowflake', 'databricks', 'hadoop', 'spark', 'hive', 'redshift', 'clickhouse', 'influxdb', 'memcached', 'firestore', 'realm',
    # Cloud & DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'ansible', 'ci/cd', 'jenkins', 'airflow', 'bash', 'shell', 'bash/shell', 'powershell', 'vagrant', 'openshift', 'cloudformation', 'circleci', 'travis', 'github actions', 'gitlab ci', 'argo', 'helm', 'prometheus', 'grafana', 'datadog', 'new relic', 'splunk', 'puppet', 'chef', 'saltstack', 'consul', 'nomad',
    # Tools & Libraries
    'git', 'github', 'gitlab', 'bitbucket', 'jira', 'notion', 'slack', 'excel', 'powerbi', 'tableau', 'looker', 'matplotlib', 'seaborn', 'plotly', 'bokeh', 'd3.js', 'highcharts', 'sqlalchemy', 'pypdf2', 'docx', 'openpyxl', 'xlrd', 'xlwt', 'beautifulsoup', 'scrapy', 'requests', 'httpx', 'aiohttp', 'pytest', 'unittest', 'mocha', 'jest', 'junit', 'selenium', 'cypress', 'playwright', 'postman', 'swagger', 'openapi', 'soapui',
    # LLM & AI
    'prompt engineering', 'langchain', 'openai', 'llm', 'llms', 'huggingface', 'transformers', 'bert', 'gpt', 'llama', 'gemini', 'claude',
    # Other
    'agile', 'scrum', 'kanban','linux', 'waterfall', 'etl', 'project management', 'leadership', 'communication', 'testing', 'unit testing', 'tdd', 'bdd', 'oop', 'soa', 'design patterns', 'system design','ux', 'ui', 'a11y', 'i18n', 'l10n',
]

def normalize_skill(skill):
    return re.sub(r'[^a-z0-9]', '', skill.lower())

def extract_skills(text, skills=COMMON_SKILLS):
    found = set()
    text_lower = text.lower()
    text_normalized = re.sub(r'[^a-z0-9]', '', text_lower)
    for skill in skills:
        skill_norm = normalize_skill(skill)
        if skill_norm in text_normalized:
            found.add(skill)
    return sorted(found)
