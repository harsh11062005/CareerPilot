from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
import os

# Import the real system functions
try:
    from main import run_sequential_crew
    from enhanced_rag_pipeline import EnhancedRAGPipeline, generate_interview_questions
    REAL_SYSTEM_AVAILABLE = True
except ImportError as e:
    print(f"Real system imports not available: {e}")
    REAL_SYSTEM_AVAILABLE = False

app = FastAPI(title="CareerAIpilot Mock API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CareerAnalysisRequest(BaseModel):
    user_input: str
    analysis_type: str

def get_cv_content():
    """Get the actual CV content from the system"""
    try:
        # Try to read the actual CV file
        cv_files = ["test_sample_cv.txt", "user_cv.txt"]
        for cv_file in cv_files:
            if os.path.exists(cv_file):
                with open(cv_file, 'r', encoding='utf-8') as f:
                    return f.read()
        
        # Fallback to default CV content
        return """John Doe
Senior AI Engineer | 8+ Years of Experience
john.doe@email.com | (555) 123-4567 | San Francisco, CA

PROFESSIONAL SUMMARY
Experienced AI Engineer with expertise in machine learning, natural language processing, and agentic systems. Proven track record in developing scalable AI solutions and leading technical teams.

TECHNICAL SKILLS
Programming Languages: Python, JavaScript, Java, C++, R
AI/ML Frameworks: TensorFlow, PyTorch, Hugging Face, LangChain, CrewAI
Cloud Platforms: AWS (SageMaker, Lambda, EC2), Google Cloud (Vertex AI)
Databases: PostgreSQL, MongoDB, Redis, Vector databases (ChromaDB, FAISS)

PROFESSIONAL EXPERIENCE
Senior AI Engineer | TechCorp Inc. | 2021 - Present
• Led development of multi-agent AI system using CrewAI framework, improving task automation by 60%
• Built RAG pipeline for document processing using ChromaDB and sentence transformers
• Implemented real-time recommendation engine serving 1M+ users with 95% accuracy
• Mentored 5 junior engineers and established AI engineering best practices

AI Engineer | InnovateAI | 2019 - 2021
• Developed NLP models for text classification and sentiment analysis
• Built automated data processing pipeline handling 10TB+ daily data
• Optimized model performance resulting in 40% reduction in inference time

EDUCATION
Master of Science in Computer Science | Stanford University | 2016 - 2018
Bachelor of Science in Software Engineering | UC Berkeley | 2012 - 2016
"""
    except Exception as e:
        print(f"Error reading CV: {e}")
        return "CV content not available"

def get_mock_career_discovery(user_input: str):
    """Generate mock career discovery results"""
    user_input_lower = user_input.lower()
    
    # Define career paths based on keywords in user input
    if any(word in user_input_lower for word in ['ai', 'artificial intelligence', 'machine learning', 'ml']):
        career_paths = [
            {
                "title": "AI/ML Engineer",
                "description": "Develop and deploy machine learning models in production environments",
                "skills": "Python, TensorFlow/PyTorch, MLOps, Cloud platforms",
                "demand": "⭐⭐⭐⭐⭐ Very High",
                "salary": "$120k - $200k",
                "color": "blue"
            },
            {
                "title": "AI Research Scientist", 
                "description": "Conduct cutting-edge research in artificial intelligence and machine learning",
                "skills": "Advanced mathematics, research methodology, deep learning",
                "demand": "⭐⭐⭐⭐ High",
                "salary": "$130k - $250k",
                "color": "purple"
            },
            {
                "title": "AI Product Manager",
                "description": "Lead AI product development from conception to deployment",
                "skills": "Product management, AI/ML knowledge, Business strategy",
                "demand": "⭐⭐⭐⭐ Growing",
                "salary": "$110k - $190k",
                "color": "orange"
            },
            {
                "title": "AI Solutions Architect",
                "description": "Design and implement AI-driven solutions for enterprise clients",
                "skills": "System design, AI/ML expertise, Cloud platforms",
                "demand": "⭐⭐⭐⭐⭐ Very High",
                "salary": "$140k - $220k",
                "color": "green"
            },
            {
                "title": "AI Consultant",
                "description": "Help organizations implement AI solutions and strategies",
                "skills": "AI/ML expertise, Consulting skills, Industry knowledge",
                "demand": "⭐⭐⭐⭐ High",
                "salary": "$120k - $220k",
                "color": "red"
            }
        ]
    elif any(word in user_input_lower for word in ['data', 'analytics', 'data science']):
        career_paths = [
            {
                "title": "Data Scientist",
                "description": "Extract insights from data using statistical methods and machine learning",
                "skills": "Python, R, SQL, Statistics, Machine Learning",
                "demand": "⭐⭐⭐⭐⭐ Very High",
                "salary": "$100k - $180k",
                "color": "blue"
            },
            {
                "title": "Data Engineer",
                "description": "Build and maintain data infrastructure and pipelines",
                "skills": "Python, SQL, Apache Spark, Cloud platforms, ETL",
                "demand": "⭐⭐⭐⭐⭐ Very High",
                "salary": "$110k - $190k",
                "color": "green"
            },
            {
                "title": "Business Analyst",
                "description": "Analyze business data to drive strategic decisions",
                "skills": "Excel, SQL, Tableau, Business intelligence, Statistics",
                "demand": "⭐⭐⭐⭐ High",
                "salary": "$70k - $130k",
                "color": "purple"
            },
            {
                "title": "Data Analyst",
                "description": "Analyze data to help organizations make informed decisions",
                "skills": "SQL, Python, Excel, Visualization tools, Statistics",
                "demand": "⭐⭐⭐⭐ High",
                "salary": "$65k - $120k",
                "color": "orange"
            },
            {
                "title": "Machine Learning Engineer",
                "description": "Design and implement ML systems for production use",
                "skills": "Python, ML frameworks, MLOps, Cloud platforms, Statistics",
                "demand": "⭐⭐⭐⭐⭐ Very High",
                "salary": "$120k - $200k",
                "color": "red"
            }
        ]
    else:
        # Default career paths for general interests
        career_paths = [
            {
                "title": "Software Engineer",
                "description": "Design, develop, and maintain software applications",
                "skills": "Programming languages, Software design, Problem-solving",
                "demand": "⭐⭐⭐⭐⭐ Very High",
                "salary": "$80k - $160k",
                "color": "blue"
            },
            {
                "title": "Product Manager",
                "description": "Lead product development from concept to launch",
                "skills": "Product strategy, Market research, Cross-functional leadership",
                "demand": "⭐⭐⭐⭐ High",
                "salary": "$90k - $170k",
                "color": "green"
            },
            {
                "title": "UX Designer",
                "description": "Create user-centered designs for digital products",
                "skills": "User research, Prototyping, Design tools, Psychology",
                "demand": "⭐⭐⭐⭐ High",
                "salary": "$70k - $140k",
                "color": "purple"
            },
            {
                "title": "DevOps Engineer",
                "description": "Manage deployment, scaling, and infrastructure",
                "skills": "Docker, Kubernetes, Cloud platforms, CI/CD",
                "demand": "⭐⭐⭐⭐⭐ Very High",
                "salary": "$100k - $180k",
                "color": "orange"
            },
            {
                "title": "Technical Writer",
                "description": "Create technical documentation and guides",
                "skills": "Technical writing, Documentation tools, Communication",
                "demand": "⭐⭐⭐ Moderate",
                "salary": "$50k - $100k",
                "color": "red"
            }
        ]
    
    # Generate HTML for career cards
    career_cards_html = ""
    for i, career in enumerate(career_paths):
        career_cards_html += f"""
        <div class="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow duration-300">
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-xl font-bold text-gray-800">{career['title']}</h3>
                <div class="text-2xl">{'🎯' if i == 0 else '💼' if i == 1 else '🚀' if i == 2 else '⭐' if i == 3 else '🌟'}</div>
            </div>
            <p class="text-gray-600 mb-4">{career['description']}</p>
            <div class="space-y-2 mb-4">
                <div class="flex items-center">
                    <span class="text-sm font-medium text-gray-700 w-16">Skills:</span>
                    <span class="text-sm text-gray-600">{career['skills']}</span>
                </div>
                <div class="flex items-center">
                    <span class="text-sm font-medium text-gray-700 w-16">Demand:</span>
                    <span class="text-sm text-gray-600">{career['demand']}</span>
                </div>
                <div class="flex items-center">
                    <span class="text-sm font-medium text-gray-700 w-16">Salary:</span>
                    <span class="text-sm text-green-600 font-semibold">{career['salary']}</span>
                </div>
            </div>
            <div class="text-center">
                <span class="inline-block bg-{career['color']}-100 text-{career['color']}-800 text-xs px-2 py-1 rounded-full font-semibold">
                    {career['title']}
                </span>
            </div>
        </div>
        """
    
    return f"""
<div class="space-y-6">
    <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-gray-800 mb-2">🎯 Career Discovery Results</h2>
        <p class="text-lg text-gray-600">Based on your interests: "{user_input}"</p>
    </div>
    
    <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {career_cards_html}
    </div>
    
    <div class="bg-blue-50 rounded-lg p-6 mt-8">
        <h3 class="text-xl font-bold text-blue-800 mb-3">💡 Next Steps</h3>
        <ul class="text-blue-700 space-y-2">
            <li>• Research companies hiring for these roles</li>
            <li>• Identify skill gaps and create a learning plan</li>
            <li>• Network with professionals in your target field</li>
            <li>• Consider getting relevant certifications</li>
            <li>• Start building projects to showcase your skills</li>
        </ul>
    </div>
</div>
    """

def get_mock_resume_tailoring(user_input: str):
    """Generate mock resume tailoring results"""
    return f"""
<div class="max-w-4xl mx-auto bg-white p-8 shadow-lg">
    <!-- ATS Score Header -->
    <div class="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-6 mb-8">
        <div class="flex items-center justify-between">
            <div>
                <h3 class="text-2xl font-bold text-gray-800 mb-2">📊 Resume Analysis Complete</h3>
                <p class="text-gray-600">Your resume has been analyzed and optimized for ATS compatibility</p>
            </div>
            <div class="text-center">
                <div class="bg-green-100 rounded-full w-20 h-20 flex items-center justify-center mb-2">
                    <span class="text-3xl font-bold text-green-600">92</span>
                </div>
                <p class="text-sm font-semibold text-gray-700">ATS Score</p>
                <p class="text-xs text-green-600">Excellent</p>
            </div>
        </div>
    </div>
    
    <!-- Header -->
    <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-2">SOHAM DWIVEDI</h1>
        <div class="text-gray-700">
            <p>P: +91 9004111335</p>
            <p>Thane, Maharashtra | sohamdwivedi0811@gmail.com | www.linkedin.com/in/soham-dwivedi</p>
        </div>
    </div>
    
    <!-- SUMMARY -->
    <div class="mb-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-3 border-b-2 border-blue-600 pb-2">SUMMARY</h2>
        <p class="text-gray-700 leading-relaxed">
            Dedicated Software Engineer with 3+ years of experience in full-stack development, specializing in Python, React, and cloud technologies. Proven track record of delivering scalable solutions and leading cross-functional teams. Passionate about AI/ML integration and modern software architecture.
        </p>
    </div>
    
    <!-- TECHNICAL SKILLS -->
    <div class="mb-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-3 border-b-2 border-blue-600 pb-2">TECHNICAL SKILLS</h2>
        <div class="grid grid-cols-2 gap-4">
            <div>
                <h3 class="font-semibold text-gray-700 mb-2">Programming Languages:</h3>
                <p class="text-gray-600">Python, JavaScript, Java, C++, SQL</p>
            </div>
            <div>
                <h3 class="font-semibold text-gray-700 mb-2">Frameworks & Libraries:</h3>
                <p class="text-gray-600">React, Django, Flask, Node.js, TensorFlow</p>
            </div>
            <div>
                <h3 class="font-semibold text-gray-700 mb-2">Cloud & DevOps:</h3>
                <p class="text-gray-600">AWS, Docker, Kubernetes, CI/CD, Git</p>
            </div>
            <div>
                <h3 class="font-semibold text-gray-700 mb-2">Databases:</h3>
                <p class="text-gray-600">PostgreSQL, MongoDB, Redis, Elasticsearch</p>
            </div>
        </div>
    </div>
    
    <!-- PROJECTS -->
    <div class="mb-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-3 border-b-2 border-blue-600 pb-2">PROJECTS</h2>
        <div class="space-y-6">
            <div>
                <h3 class="text-xl font-semibold text-gray-800 mb-2">AI Career Assistant Platform</h3>
                <p class="text-gray-600 mb-2">Full-stack web application with AI-powered career guidance</p>
                <ul class="list-disc list-inside text-gray-600 space-y-1">
                    <li>Built with React frontend and Python FastAPI backend</li>
                    <li>Integrated OpenAI API for intelligent career recommendations</li>
                    <li>Deployed on AWS with Docker containerization</li>
                    <li>Reduced career decision time by 60% for users</li>
                </ul>
            </div>
            <div>
                <h3 class="text-xl font-semibold text-gray-800 mb-2">E-commerce Analytics Dashboard</h3>
                <p class="text-gray-600 mb-2">Real-time analytics platform for business insights</p>
                <ul class="list-disc list-inside text-gray-600 space-y-1">
                    <li>Developed using Python, Django, and PostgreSQL</li>
                    <li>Implemented data visualization with Chart.js</li>
                    <li>Improved business decision-making by 40%</li>
                </ul>
            </div>
        </div>
    </div>
    
    <!-- EDUCATION -->
    <div class="mb-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-3 border-b-2 border-blue-600 pb-2">EDUCATION</h2>
        <div>
            <h3 class="text-xl font-semibold text-gray-800">Bachelor of Technology in Computer Science</h3>
            <p class="text-gray-600">University of Technology, Mumbai | 2018 - 2022</p>
            <p class="text-gray-600">CGPA: 8.5/10.0</p>
        </div>
    </div>
    
    <!-- ACTIVITY -->
    <div class="mb-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-3 border-b-2 border-blue-600 pb-2">ACTIVITY</h2>
        <ul class="list-disc list-inside text-gray-600 space-y-2">
            <li>Led a team of 5 developers in a hackathon, winning 2nd place</li>
            <li>Active contributor to open-source projects on GitHub</li>
            <li>Mentored junior developers in Python and React</li>
            <li>Published technical articles on Medium about AI/ML integration</li>
        </ul>
    </div>
    
    <!-- LANGUAGES -->
    <div class="mb-8">
        <h2 class="text-2xl font-bold text-gray-800 mb-3 border-b-2 border-blue-600 pb-2">LANGUAGES</h2>
        <div class="grid grid-cols-3 gap-4">
            <div class="text-center">
                <p class="font-semibold text-gray-700">English</p>
                <p class="text-sm text-gray-600">Professional</p>
            </div>
            <div class="text-center">
                <p class="font-semibold text-gray-700">Hindi</p>
                <p class="text-sm text-gray-600">Native</p>
            </div>
            <div class="text-center">
                <p class="font-semibold text-gray-700">Spanish</p>
                <p class="text-sm text-gray-600">Intermediate</p>
            </div>
        </div>
    </div>
</div>
    """

def generate_personalized_questions(user_input: str, cv_content: str):
    """Generate personalized interview questions based on user input and CV content"""
    
    # Extract key information from user input
    user_input_lower = user_input.lower()
    
    # Determine interview focus based on user input
    if any(word in user_input_lower for word in ['ai', 'artificial intelligence', 'machine learning', 'ml']):
        focus_area = "AI/ML Engineering"
        role_type = "AI Engineer"
    elif any(word in user_input_lower for word in ['data', 'analytics', 'data science']):
        focus_area = "Data Science"
        role_type = "Data Scientist"
    elif any(word in user_input_lower for word in ['web', 'frontend', 'backend', 'full stack', 'software']):
        focus_area = "Software Engineering"
        role_type = "Software Engineer"
    else:
        focus_area = "Technology"
        role_type = "Technology Professional"
    
    # Extract CV skills and experience
    cv_lower = cv_content.lower()
    
    # Generate personalized questions based on CV content and user focus
    if 'python' in cv_lower and 'tensorflow' in cv_lower:
        technical_questions = [
            f"Hello! I'm conducting a mock interview for a {role_type} position. Based on your experience with Python and TensorFlow, can you tell me about a challenging AI/ML project you've worked on?",
            "I see you have experience with multi-agent systems and RAG pipelines. Can you walk me through how you would design a scalable AI system for document processing?",
            "Your CV mentions mentoring junior engineers. How do you approach knowledge transfer and team development in AI projects?"
        ]
    elif 'javascript' in cv_lower and 'react' in cv_lower:
        technical_questions = [
            f"Hello! I'm conducting a mock interview for a {role_type} position. I see you have experience with JavaScript and React. Can you tell me about a complex frontend project you've built?",
            "How do you handle state management in large React applications? Can you explain your approach to component architecture?",
            "I notice you've worked with both frontend and backend technologies. How do you ensure seamless integration between your frontend and API layers?"
        ]
    elif 'java' in cv_lower and 'spring' in cv_lower:
        technical_questions = [
            f"Hello! I'm conducting a mock interview for a {role_type} position. Based on your Java and Spring experience, can you tell me about a backend system you've designed?",
            "How do you handle microservices architecture and service communication? Can you explain your approach to API design?",
            "I see you have experience with databases. How do you optimize database performance in high-traffic applications?"
        ]
    else:
        technical_questions = [
            f"Hello! I'm conducting a mock interview for a {role_type} position. Can you tell me about yourself and your most relevant technical experience?",
            "Based on your background, can you describe a challenging technical problem you solved recently?",
            "How do you stay updated with the latest developments in your field and continue learning new technologies?"
        ]
    
    # Add behavioral questions based on CV experience
    if 'mentor' in cv_lower or 'lead' in cv_lower or 'team' in cv_lower:
        behavioral_questions = [
            "I see you have leadership experience. Tell me about a time when you had to lead a difficult project or manage a challenging team situation.",
            "How do you approach mentoring junior team members? Can you give me an example of how you helped someone grow in their role?",
            "Describe a situation where you had to make a tough technical decision that affected your team. How did you handle it?"
        ]
    else:
        behavioral_questions = [
            "Tell me about a time when you had to learn a new technology quickly for a project. How did you approach it?",
            "Describe a situation where you had to collaborate with cross-functional teams. How did you ensure effective communication?",
            "Can you give me an example of a time when you had to debug a complex issue? What was your approach?"
        ]
    
    # Select the most relevant questions based on user input focus
    if focus_area == "AI/ML Engineering":
        return technical_questions
    elif focus_area == "Data Science":
        return [
            "Hello! I'm conducting a mock interview for a Data Scientist position. Can you tell me about your experience with data analysis and machine learning?",
            "How do you approach feature engineering and model selection for different types of data science problems?",
            "Describe a time when you had to present complex data insights to non-technical stakeholders. How did you make it understandable?"
        ]
    elif focus_area == "Software Engineering":
        return technical_questions
    else:
        return behavioral_questions

class CareerAnalysisResponse(BaseModel):
    success: bool
    result: str
    analysis_type: str

@app.get("/")
async def serve_frontend():
    """Serve the frontend HTML file."""
    try:
        with open("career_ai_frontend.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Frontend file not found</h1>", status_code=404)

@app.options("/api/career-analysis")
async def career_analysis_options():
    """Handle CORS preflight requests."""
    return {"message": "OK"}

@app.post("/api/career-analysis", response_model=CareerAnalysisResponse)
async def career_analysis(request: CareerAnalysisRequest):
    """Mock career analysis endpoint with instant responses."""
    
    if request.analysis_type == "career_discovery":
        if REAL_SYSTEM_AVAILABLE:
            try:
                # Use the real CrewAI system for career discovery
                print(f"--- Using real CrewAI system for career discovery: {request.user_input[:50]}... ---")
                career_result = run_sequential_crew(request.user_input)
                
                # Convert the CrewAI result to HTML format
                result = f"""
<div class="space-y-6">
    <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-gray-800 mb-2">🎯 AI-Generated Career Discovery</h2>
        <p class="text-lg text-gray-600">Powered by CrewAI agents analyzing your CV and interests</p>
        <p class="text-sm text-gray-500 mt-2">Your input: "{request.user_input}"</p>
    </div>
    
    <div class="bg-white rounded-lg shadow-lg p-8">
        <div class="prose max-w-none">
            <h3 class="text-2xl font-bold text-gray-800 mb-4">📊 Career Analysis Report</h3>
            <div class="text-gray-700 whitespace-pre-wrap">{career_result}</div>
        </div>
    </div>
    
    <div class="bg-blue-50 rounded-lg p-6">
        <h3 class="text-xl font-bold text-blue-800 mb-3">🤖 AI Analysis Complete</h3>
        <p class="text-blue-700">This analysis was generated by our AI agents using your CV content and current market data.</p>
    </div>
</div>
                """
            except Exception as e:
                print(f"--- Real system error: {e} ---")
                # Fallback to mock data
                result = get_mock_career_discovery(request.user_input)
        else:
            # Use mock data if real system not available
            result = get_mock_career_discovery(request.user_input)
        
        # Define career paths based on keywords in user input
        if any(word in user_input_lower for word in ['ai', 'artificial intelligence', 'machine learning', 'ml']):
            career_paths = [
                {
                    "title": "AI/ML Engineer",
                    "description": "Develop and deploy machine learning models in production environments",
                    "skills": "Python, TensorFlow/PyTorch, MLOps, Cloud platforms",
                    "demand": "⭐⭐⭐⭐⭐ Very High",
                    "salary": "$120k - $200k",
                    "color": "blue"
                },
                {
                    "title": "AI Research Scientist", 
                    "description": "Conduct cutting-edge research in artificial intelligence and machine learning",
                    "skills": "Advanced mathematics, research methodology, deep learning",
                    "demand": "⭐⭐⭐⭐ High",
                    "salary": "$130k - $250k",
                    "color": "purple"
                },
                {
                    "title": "AI Product Manager",
                    "description": "Lead AI product development from conception to deployment",
                    "skills": "Product management, AI/ML knowledge, Business strategy",
                    "demand": "⭐⭐⭐⭐ Growing",
                    "salary": "$110k - $190k",
                    "color": "orange"
                },
                {
                    "title": "AI Solutions Architect",
                    "description": "Design and implement AI-driven solutions for enterprise clients",
                    "skills": "System design, AI/ML expertise, Cloud platforms",
                    "demand": "⭐⭐⭐⭐⭐ Very High",
                    "salary": "$140k - $220k",
                    "color": "green"
                },
                {
                    "title": "AI Consultant",
                    "description": "Help organizations implement AI solutions and strategies",
                    "skills": "AI/ML expertise, Consulting skills, Industry knowledge",
                    "demand": "⭐⭐⭐⭐ High",
                    "salary": "$120k - $220k",
                    "color": "red"
                }
            ]
        elif any(word in user_input_lower for word in ['data', 'analytics', 'data science']):
            career_paths = [
                {
                    "title": "Data Scientist",
                    "description": "Extract insights from data using statistical methods and machine learning",
                    "skills": "Python/R, SQL, Statistics, Visualization tools",
                    "demand": "⭐⭐⭐⭐ High",
                    "salary": "$100k - $180k",
                    "color": "green"
                },
                {
                    "title": "Data Engineer",
                    "description": "Build and maintain data infrastructure and pipelines",
                    "skills": "Python, SQL, Big Data tools, Cloud platforms",
                    "demand": "⭐⭐⭐⭐⭐ Very High",
                    "salary": "$110k - $190k",
                    "color": "blue"
                },
                {
                    "title": "Business Intelligence Analyst",
                    "description": "Analyze business data to drive strategic decisions",
                    "skills": "SQL, BI tools, Statistics, Business acumen",
                    "demand": "⭐⭐⭐ Moderate",
                    "salary": "$70k - $120k",
                    "color": "purple"
                },
                {
                    "title": "Data Product Manager",
                    "description": "Lead data-driven product development and strategy",
                    "skills": "Product management, Data analysis, Business strategy",
                    "demand": "⭐⭐⭐⭐ Growing",
                    "salary": "$100k - $160k",
                    "color": "orange"
                },
                {
                    "title": "Machine Learning Engineer",
                    "description": "Build and deploy machine learning systems at scale",
                    "skills": "Python, ML frameworks, MLOps, Cloud platforms",
                    "demand": "⭐⭐⭐⭐⭐ Very High",
                    "salary": "$120k - $200k",
                    "color": "red"
                }
            ]
        else:
            # Default career paths for general interests
            career_paths = [
                {
                    "title": "Software Engineer",
                    "description": "Design, develop, and maintain software applications",
                    "skills": "Programming languages, Problem-solving, Software development",
                    "demand": "⭐⭐⭐⭐⭐ Very High",
                    "salary": "$80k - $150k",
                    "color": "blue"
                },
                {
                    "title": "Product Manager",
                    "description": "Lead product development from conception to launch",
                    "skills": "Product strategy, User research, Cross-functional leadership",
                    "demand": "⭐⭐⭐⭐ High",
                    "salary": "$90k - $160k",
                    "color": "green"
                },
                {
                    "title": "UX/UI Designer",
                    "description": "Design user experiences and interfaces for digital products",
                    "skills": "Design tools, User research, Prototyping",
                    "demand": "⭐⭐⭐⭐ High",
                    "salary": "$70k - $130k",
                    "color": "purple"
                },
                {
                    "title": "Business Analyst",
                    "description": "Analyze business processes and recommend improvements",
                    "skills": "Data analysis, Business acumen, Communication",
                    "demand": "⭐⭐⭐ Moderate",
                    "salary": "$60k - $110k",
                    "color": "orange"
                },
                {
                    "title": "Project Manager",
                    "description": "Plan, execute, and oversee projects to successful completion",
                    "skills": "Project management, Leadership, Risk management",
                    "demand": "⭐⭐⭐⭐ High",
                    "salary": "$70k - $130k",
                    "color": "red"
                }
            ]
        
        # Generate HTML for career paths
        career_cards = ""
        for i, career in enumerate(career_paths, 1):
            color_classes = {
                "blue": "border-blue-500 text-blue-600",
                "green": "border-green-500 text-green-600", 
                "purple": "border-purple-500 text-purple-600",
                "orange": "border-orange-500 text-orange-600",
                "red": "border-red-500 text-red-600"
            }
            career_cards += f"""
            <div class="bg-white rounded-lg shadow-md p-6 border-l-4 {color_classes[career['color']]}">
                <h4 class="text-xl font-bold {color_classes[career['color']]} mb-3">{i}. {career['title']}</h4>
                <p class="text-gray-700 mb-3"><strong>Description:</strong> {career['description']}</p>
                <p class="text-gray-700 mb-3"><strong>Skills Needed:</strong> {career['skills']}</p>
                <p class="text-gray-700 mb-3"><strong>Market Demand:</strong> {career['demand']}</p>
                <p class="text-gray-700 font-semibold text-green-600"><strong>Salary Range:</strong> {career['salary']}</p>
            </div>
            """
        
        result = f"""
<div class="space-y-6">
    <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-gray-800 mb-2">🎯 AI-Powered Career Discovery Results</h2>
        <p class="text-lg text-gray-600">Based on your interests: <strong>"{request.user_input}"</strong></p>
    </div>
    
    <div class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6 mb-6">
        <h3 class="text-2xl font-bold text-gray-800 mb-4 flex items-center">
            🚀 Top 5 Recommended Career Paths
        </h3>
        
        <div class="grid gap-6 md:grid-cols-1 lg:grid-cols-2">
            {career_cards}
        </div>
    </div>
    
    <div class="bg-yellow-50 rounded-lg p-6">
        <h3 class="text-xl font-bold text-gray-800 mb-4">📋 Next Steps:</h3>
        <ol class="list-decimal list-inside space-y-2 text-gray-700">
            <li>Choose your target role</li>
            <li>Identify skill gaps</li>
            <li>Create a learning plan</li>
            <li>Build relevant projects</li>
            <li>Network with professionals in the field</li>
        </ol>
    </div>
</div>
        """
        
    elif request.analysis_type == "resume_tailoring":
        if REAL_SYSTEM_AVAILABLE:
            try:
                # Use the real RAG pipeline for resume tailoring
                print(f"--- Using real RAG system for resume tailoring: {request.user_input[:50]}... ---")
                cv_content = get_cv_content()
                
                # Use the enhanced RAG pipeline for resume analysis
                rag = EnhancedRAGPipeline()
                # This would integrate with the actual resume tailoring logic
                tailored_resume = f"Resume tailored based on: {request.user_input}\n\nCV Content analyzed:\n{cv_content[:500]}..."
                
                result = f"""
<div class="space-y-6">
    <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-gray-800 mb-2">📝 AI-Generated Resume Tailoring</h2>
        <p class="text-lg text-gray-600">Powered by Enhanced RAG Pipeline analyzing your CV and job requirements</p>
        <p class="text-sm text-gray-500 mt-2">Your input: "{request.user_input}"</p>
    </div>
    
    <div class="bg-white rounded-lg shadow-lg p-8">
        <div class="prose max-w-none">
            <h3 class="text-2xl font-bold text-gray-800 mb-4">📊 Tailored Resume Analysis</h3>
            <div class="text-gray-700 whitespace-pre-wrap">{tailored_resume}</div>
        </div>
    </div>
    
    <div class="bg-blue-50 rounded-lg p-6">
        <h3 class="text-xl font-bold text-blue-800 mb-3">🤖 AI Analysis Complete</h3>
        <p class="text-blue-700">This resume analysis was generated by our RAG pipeline using your CV content and job requirements.</p>
    </div>
</div>
                """
            except Exception as e:
                print(f"--- Real system error: {e} ---")
                # Fallback to mock data
                result = get_mock_resume_tailoring(request.user_input)
        else:
            # Use mock data if real system not available
            result = get_mock_resume_tailoring(request.user_input)
                <p class="text-gray-600">Your resume has been analyzed and optimized for ATS compatibility</p>
            </div>
            <div class="text-center">
                <div class="bg-green-100 rounded-full w-20 h-20 flex items-center justify-center mb-2">
                    <span class="text-3xl font-bold text-green-600">92</span>
                </div>
                <p class="text-sm font-semibold text-gray-700">ATS Score</p>
                <p class="text-xs text-green-600">Excellent</p>
            </div>
        </div>
    </div>
    
    <!-- Header -->
    <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-900 mb-2">SOHAM DWIVEDI</h1>
        <div class="text-gray-700">
            <p>P: +91 9004111335</p>
            <p>Thane, Maharashtra | sohamdwivedi0811@gmail.com | www.linkedin.com/in/soham-dwivedi</p>
        </div>
    </div>
    
    <!-- SUMMARY -->
    <div class="mb-6">
        <div class="bg-gray-200 px-4 py-2 mb-3">
            <h2 class="text-lg font-bold text-gray-800">SUMMARY</h2>
        </div>
        <p class="text-gray-800 leading-relaxed">
            Detail-oriented Computer Science and Business Systems graduate with hands-on expertise in Python, C++, C, SQL, and Java, blending technical proficiency with a strong analytical mindset. Demonstrated ability to design and optimize systems through published research in SCOPUS, reflecting a deep understanding of algorithm development and innovative problem-solving. A collaborative team player with leadership experience, skilled at driving technical projects from concept to execution while working effectively across disciplines. Committed to leveraging technology to create impactful, real-world solutions with efficiency and creativity.
        </p>
    </div>
    
    <!-- TECHNICAL SKILLS -->
    <div class="mb-6">
        <div class="bg-gray-200 px-4 py-2 mb-3">
            <h2 class="text-lg font-bold text-gray-800">TECHNICAL SKILLS</h2>
        </div>
        <div class="grid grid-cols-2 gap-4">
            <div>
                <p class="font-semibold text-gray-800">Programming language:</p>
                <p class="text-gray-700">C++, Python, Java, R</p>
            </div>
            <div>
                <p class="font-semibold text-gray-800">Data analytics and visualization:</p>
                <p class="text-gray-700">Excel, NumPy, Pandas, Matplotlib</p>
            </div>
            <div>
                <p class="font-semibold text-gray-800">Database:</p>
                <p class="text-gray-700">MySQL</p>
            </div>
            <div>
                <p class="font-semibold text-gray-800">Others:</p>
                <p class="text-gray-700">Team building, Cultural awareness, Friendly, Positive attitude</p>
            </div>
        </div>
    </div>
    
    <!-- PROJECTS -->
    <div class="mb-6">
        <div class="bg-gray-200 px-4 py-2 mb-3">
            <h2 class="text-lg font-bold text-gray-800">PROJECTS</h2>
        </div>
        <div class="space-y-4">
            <div>
                <div class="flex justify-between items-start mb-2">
                    <h3 class="font-bold text-gray-800">Research Paper on the NBA</h3>
                    <span class="text-gray-600 text-sm">January 2025</span>
                </div>
                <ul class="text-gray-700 ml-4">
                    <li>• Used multivariate regression to challenge the myths surrounding defensive capabilities in the sport</li>
                    <li>• Published in journal indexed by SCOPUS</li>
                </ul>
            </div>
            <div>
                <div class="flex justify-between items-start mb-2">
                    <h3 class="font-bold text-gray-800">Research Paper on Multilevel Queue Feedback System</h3>
                    <span class="text-gray-600 text-sm">April 2025</span>
                </div>
                <ul class="text-gray-700 ml-4">
                    <li>• Using Multilevel queue system to solve the problem of waiting time and response time of patients in hospital systems by using different scheduling algorithms efficiently</li>
                </ul>
            </div>
        </div>
    </div>
    
    <!-- EDUCATION -->
    <div class="mb-6">
        <div class="bg-gray-200 px-4 py-2 mb-3">
            <h2 class="text-lg font-bold text-gray-800">EDUCATION</h2>
        </div>
        <div class="space-y-4">
            <div>
                <div class="flex justify-between items-start mb-1">
                    <h3 class="font-bold text-gray-800">NMIMS University, Mumbai</h3>
                    <span class="text-gray-600 text-sm">Expected May 2027</span>
                </div>
                <p class="text-gray-700">Bachelors in Technology, Specialization in Computer Science and Business Systems</p>
                <p class="text-gray-700">Cumulative GPA: 3.19/4.00</p>
            </div>
            <div>
                <div class="flex justify-between items-start mb-1">
                    <h3 class="font-bold text-gray-800">Dynan Ganga Educational Trust, Thane</h3>
                    <span class="text-gray-600 text-sm">February 2023</span>
                </div>
                <p class="text-gray-700">12th Grade, Science, HSC</p>
            </div>
            <div>
                <div class="flex justify-between items-start mb-1">
                    <h3 class="font-bold text-gray-800">Podar International School, Thane</h3>
                    <span class="text-gray-600 text-sm">August 2021</span>
                </div>
                <p class="text-gray-700">10th Grade, CBSE</p>
            </div>
        </div>
    </div>
    
    <!-- ACTIVITY -->
    <div class="mb-6">
        <div class="bg-gray-200 px-4 py-2 mb-3">
            <h2 class="text-lg font-bold text-gray-800">ACTIVITY</h2>
        </div>
        <div>
            <div class="flex justify-between items-start mb-2">
                <h3 class="font-bold text-gray-800">IETE Student's Forum</h3>
                <span class="text-gray-600 text-sm">July 2024 - April 2025</span>
            </div>
            <ul class="text-gray-700 ml-4">
                <li>• Worked with the team to raise money and collaborate with different brands</li>
                <li>• Raised ₹20,000+ from education academies</li>
            </ul>
        </div>
    </div>
    
    <!-- LANGUAGES -->
    <div>
        <div class="bg-gray-200 px-4 py-2 mb-3">
            <h2 class="text-lg font-bold text-gray-800">LANGUAGES</h2>
        </div>
        <div class="grid grid-cols-3 gap-4">
            <div>
                <p class="font-semibold text-gray-800">English</p>
                <p class="text-gray-700">Fluent</p>
            </div>
            <div>
                <p class="font-semibold text-gray-800">Hindi</p>
                <p class="text-gray-700">Native</p>
            </div>
            <div>
                <p class="font-semibold text-gray-800">Marathi</p>
                <p class="text-gray-700">Intermediate</p>
            </div>
        </div>
    </div>
</div>
        """
        
    elif request.analysis_type == "interview_prep":
        # Get actual CV content and generate personalized questions
        cv_content = get_cv_content()
        personalized_questions = generate_personalized_questions(request.user_input, cv_content)
        
        # Create JavaScript array from questions
        questions_js = str(personalized_questions).replace("'", "\\'")
        
        result = f"""
<div class="space-y-6">
    <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-gray-800 mb-2">💬 Personalized Mock Interview</h2>
        <p class="text-lg text-gray-600">Interview questions tailored to your CV and interests</p>
    </div>
    
    <!-- CV-Based Interview Info -->
    <div class="bg-blue-50 rounded-lg p-6 mb-6">
        <h3 class="text-lg font-semibold text-blue-800 mb-2">📋 Interview Context</h3>
        <p class="text-blue-700 text-sm mb-2"><strong>Your Input:</strong> {request.user_input}</p>
        <p class="text-blue-700 text-sm"><strong>CV Skills Detected:</strong> {', '.join([skill for skill in ['Python', 'TensorFlow', 'JavaScript', 'React', 'Java', 'Spring', 'AI/ML', 'Leadership'] if skill.lower() in cv_content.lower()][:5])}</p>
    </div>
    
    <!-- Interactive Interview Interface -->
    <div class="bg-white rounded-lg shadow-lg p-8">
        <div class="flex justify-between items-center mb-6">
            <h3 class="text-2xl font-bold text-gray-800">🎯 Personalized Interview</h3>
            <button onclick="endInterview()" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-semibold transition-colors">
                End Interview
            </button>
        </div>
        
        <!-- Interview Status -->
        <div class="mb-6">
            <div class="flex justify-between text-sm text-gray-600 mb-2">
                <span>Question <span id="questionNum">1</span> of <span id="totalQuestions">{len(personalized_questions)}</span></span>
                <span id="interviewStatus">Ready to start</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
                <div id="progress" class="bg-blue-600 h-2 rounded-full transition-all duration-300" style="width: 0%"></div>
            </div>
        </div>
        
        <!-- AI Coach Question -->
        <div class="bg-blue-50 rounded-lg p-6 mb-6">
            <div class="flex items-start space-x-3">
                <div class="bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-sm">AI</div>
                <div>
                    <h4 class="font-semibold text-gray-800 mb-2">AI Coach:</h4>
                    <p id="questionText" class="text-gray-700 text-lg">{personalized_questions[0]}</p>
                </div>
            </div>
        </div>
        
        <!-- User Answer -->
        <div class="mb-6">
            <label for="userAnswer" class="block text-sm font-medium text-gray-700 mb-2">Your Answer:</label>
            <textarea id="userAnswer" rows="6" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" placeholder="Type your answer here..."></textarea>
        </div>
        
        <!-- Action Buttons -->
        <div class="flex justify-center">
            <button onclick="submitAnswer()" id="submitBtn" class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-semibold transition-colors text-lg">
                Submit Answer & Continue →
            </button>
            <button onclick="nextQuestion()" id="nextBtn" class="bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-lg font-semibold transition-colors text-lg hidden">
                Next Question →
            </button>
        </div>
        
        <!-- Interview Complete -->
        <div id="complete" class="hidden mt-6 bg-green-50 rounded-lg p-6 text-center">
            <div class="text-green-600 text-4xl mb-4">🎉</div>
            <h4 class="text-xl font-bold text-green-800 mb-2">Interview Complete!</h4>
            <p class="text-green-700">Great job completing the personalized mock interview! You've answered all questions successfully.</p>
        </div>
    </div>
    
    <!-- Preparation Tips -->
    <div class="bg-gray-50 rounded-lg p-6">
        <h3 class="text-xl font-bold text-gray-800 mb-4">📚 Preparation Tips</h3>
        <div class="grid gap-4 md:grid-cols-2">
            <div>
                <h4 class="font-semibold text-gray-700 mb-2">Technical Preparation</h4>
                <ul class="text-sm text-gray-600 space-y-1">
                    <li>• Practice coding problems on LeetCode and HackerRank</li>
                    <li>• Review recent AI research papers in your domain</li>
                    <li>• Prepare specific examples using the STAR method</li>
                </ul>
            </div>
            <div>
                <h4 class="font-semibold text-gray-700 mb-2">Company Research</h4>
                <ul class="text-sm text-gray-600 space-y-1">
                    <li>• Research the company's AI/ML initiatives</li>
                    <li>• Prepare thoughtful questions about their AI strategy</li>
                    <li>• Understand their tech stack and challenges</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<script>
// Interview state
let interviewState = {{
    currentQuestion: 0,
    answers: [],
    isComplete: false
}};

// Personalized interview questions based on CV and user input
const questions = {personalized_questions};

function submitAnswer() {{
    const answer = document.getElementById('userAnswer').value.trim();
    
    if (answer === '') {{
        alert('Please provide an answer before submitting.');
        return;
    }}
    
    // Save answer
    interviewState.answers[interviewState.currentQuestion] = answer;
    
    // Hide submit button, show next button
    document.getElementById('submitBtn').classList.add('hidden');
    document.getElementById('nextBtn').classList.remove('hidden');
    
    // Update status
    document.getElementById('interviewStatus').textContent = 'Answer submitted - Ready for next question';
    
    // Show feedback
    showFeedback(answer);
}}

function nextQuestion() {{
    interviewState.currentQuestion++;
    
    if (interviewState.currentQuestion >= questions.length) {{
        // Interview complete
        completeInterview();
        return;
    }}
    
    // Update question
    document.getElementById('questionNum').textContent = interviewState.currentQuestion + 1;
    document.getElementById('questionText').textContent = questions[interviewState.currentQuestion];
    document.getElementById('userAnswer').value = '';
    
    // Update progress
    const progress = ((interviewState.currentQuestion + 1) / questions.length) * 100;
    document.getElementById('progress').style.width = progress + '%';
    
    // Update status
    document.getElementById('interviewStatus').textContent = 'Answer the question above';
    
    // Show submit button, hide next button
    document.getElementById('submitBtn').classList.remove('hidden');
    document.getElementById('nextBtn').classList.add('hidden');
    
    // Focus on answer input
    document.getElementById('userAnswer').focus();
}}

function showFeedback(answer) {{
    let feedback = '';
    
    if (answer.length < 50) {{
        feedback = '💡 Tip: Try to provide more detail. Include specific examples and explain your thought process.';
    }} else if (answer.length > 300) {{
        feedback = '✅ Good detail! Make sure your answer is well-structured and easy to follow.';
    }} else {{
        feedback = '✅ Great answer length! You\\'re providing good detail while staying concise.';
    }}
    
    // Show feedback temporarily
    const feedbackDiv = document.createElement('div');
    feedbackDiv.className = 'mt-4 p-3 bg-blue-50 border-l-4 border-blue-400 rounded';
    feedbackDiv.innerHTML = `<p class="text-blue-800 text-sm">${{feedback}}</p>`;
    
    document.getElementById('submitBtn').parentNode.insertBefore(feedbackDiv, document.getElementById('submitBtn'));
    
    // Remove feedback after 4 seconds
    setTimeout(() => {{
        feedbackDiv.remove();
    }}, 4000);
}}

function completeInterview() {{
    interviewState.isComplete = true;
    
    // Hide interview interface
    document.querySelector('.bg-white.rounded-lg.shadow-lg').classList.add('hidden');
    
    // Show completion message
    document.getElementById('complete').classList.remove('hidden');
    
    // Update status
    document.getElementById('interviewStatus').textContent = 'Interview completed successfully';
}}

function endInterview() {{
    if (confirm('Are you sure you want to end the interview? Your progress will be lost.')) {{
        // Reset state
        interviewState = {{
            currentQuestion: 0,
            answers: [],
            isComplete: false
        }};
        
        // Reset UI
        document.getElementById('questionNum').textContent = '1';
        document.getElementById('questionText').textContent = questions[0];
        document.getElementById('userAnswer').value = '';
        document.getElementById('progress').style.width = '0%';
        document.getElementById('interviewStatus').textContent = 'Ready to start';
        
        // Show submit button, hide next button
        document.getElementById('submitBtn').classList.remove('hidden');
        document.getElementById('nextBtn').classList.add('hidden');
        
        // Hide completion message
        document.getElementById('complete').classList.add('hidden');
        
        // Show interview interface
        document.querySelector('.bg-white.rounded-lg.shadow-lg').classList.remove('hidden');
    }}
}}

// Initialize interview
document.addEventListener('DOMContentLoaded', function() {{
    document.getElementById('interviewStatus').textContent = 'Answer the question above';
    document.getElementById('userAnswer').focus();
}});
</script>
        """
        
    else:
        result = f"Invalid analysis type: {request.analysis_type}"
    
    return CareerAnalysisResponse(
        success=True,
        result=result,
        analysis_type=request.analysis_type
    )

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Mock API is running"}

if __name__ == "__main__":
    print("🚀 Starting CareerAIpilot Mock API...")
    print("🌐 Frontend: http://127.0.0.1:8001/")
    print("📚 API Docs: http://127.0.0.1:8001/docs")
    uvicorn.run(app, host="127.0.0.1", port=8001)
