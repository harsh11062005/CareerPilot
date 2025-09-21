#!/usr/bin/env python3
"""
Mock API for CareerAIpilot frontend testing with real system integration
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import uvicorn
import os
from typing import List, Dict

# Import the real system functions
try:
    from main import run_sequential_crew
    from enhanced_rag_pipeline import EnhancedRAGPipeline, generate_interview_questions
    from job_recommendation_engine import get_intelligent_job_recommendations
    from pdf_resume_processor import process_resume_pdf
    # Temporarily disable real system for testing
    REAL_SYSTEM_AVAILABLE = False
    print("Real system imports available but disabled for testing")
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

class CareerAnalysisResponse(BaseModel):
    success: bool
    result: str
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

def validate_input(user_input: str, analysis_type: str) -> tuple[bool, str]:
    """Validate user input and return (is_valid, error_message)"""
    
    # Check for empty input
    if not user_input or not user_input.strip():
        return False, "Please provide some input. Tell us about your interests, skills, or career goals."
    
    # Check minimum length
    if len(user_input.strip()) < 3:
        return False, "Input is too short. Please provide more details about your interests or goals."
    
    # Check for valid analysis type
    valid_types = ["career_discovery", "resume_tailoring", "interview_prep"]
    if analysis_type not in valid_types:
        return False, f"Invalid analysis type. Must be one of: {', '.join(valid_types)}"
    
    # Check for spam/inappropriate content (basic check)
    spam_keywords = ["spam", "test", "asdf", "qwerty", "123", "abc"]
    if any(keyword in user_input.lower() for keyword in spam_keywords):
        if len(user_input.strip()) < 10:  # Allow short spam words in longer meaningful text
            return False, "Please provide meaningful input about your career interests or goals."
    
    return True, ""

def extract_skills_from_input(user_input: str) -> List[str]:
    """Extract skills from user input using keyword matching"""
    user_input_lower = user_input.lower()
    
    # Common technical skills to look for
    skill_keywords = [
        "python", "javascript", "java", "c++", "c#", "go", "rust", "php", "ruby", "swift",
        "react", "angular", "vue", "nodejs", "django", "flask", "spring", "express",
        "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
        "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
        "sql", "mongodb", "postgresql", "mysql", "redis",
        "git", "jenkins", "ci/cd", "agile", "scrum",
        "machine learning", "deep learning", "ai", "data science", "analytics",
        "frontend", "backend", "full stack", "mobile", "ios", "android",
        "cybersecurity", "devops", "cloud", "microservices"
    ]
    
    found_skills = []
    for skill in skill_keywords:
        if skill in user_input_lower:
            found_skills.append(skill)
    
    return found_skills

def calculate_ats_score(cv_content: str, job_requirements: str) -> int:
    """Calculate ATS compatibility score"""
    score = 70  # Base score
    
    # Check for common ATS-friendly elements
    if "summary" in cv_content.lower() or "objective" in cv_content.lower():
        score += 5
    if "experience" in cv_content.lower():
        score += 5
    if "education" in cv_content.lower():
        score += 5
    if "skills" in cv_content.lower():
        score += 5
    
    # Check for keyword matching
    job_keywords = job_requirements.lower().split()
    cv_keywords = cv_content.lower().split()
    keyword_matches = sum(1 for keyword in job_keywords if keyword in cv_keywords)
    score += min(keyword_matches * 2, 10)
    
    # Check for quantifiable achievements
    if any(word in cv_content.lower() for word in ["%", "increased", "improved", "reduced", "saved"]):
        score += 5
    
    return min(score, 100)

def generate_resume_tailoring_html(tailored_content: str, ats_score: int, job_requirements: str, original_cv: str) -> str:
    """Generate HTML for resume tailoring results"""
    
    # Extract key improvements
    improvements = [
        "Enhanced keyword optimization for ATS compatibility",
        "Improved action verbs and quantifiable achievements",
        "Restructured content for better readability",
        "Added relevant skills and technologies",
        "Optimized formatting for digital parsing"
    ]
    
    return f"""
    <div class="space-y-6">
        <div class="text-center mb-8">
            <h2 class="text-3xl font-bold text-gray-800 mb-2">📝 AI-Optimized Resume</h2>
            <p class="text-lg text-gray-600">Powered by Enhanced RAG Pipeline and ATS Analysis</p>
            <p class="text-sm text-gray-500 mt-2">Job Requirements: "{job_requirements}"</p>
        </div>
        
        <!-- ATS Score Header -->
        <div class="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-6 mb-8">
            <div class="flex items-center justify-between">
                <div>
                    <h3 class="text-2xl font-bold text-gray-800 mb-2">📊 Resume Analysis Complete</h3>
                    <p class="text-gray-600">Your resume has been analyzed and optimized for ATS compatibility</p>
                </div>
                <div class="text-center">
                    <div class="bg-green-100 rounded-full w-20 h-20 flex items-center justify-center mb-2">
                        <span class="text-3xl font-bold text-green-600">{ats_score}</span>
                    </div>
                    <p class="text-sm font-semibold text-gray-700">ATS Score</p>
                    <p class="text-xs text-green-600">{'Excellent' if ats_score > 90 else 'Good' if ats_score > 80 else 'Fair'}</p>
                </div>
            </div>
        </div>
        
        <!-- PDF Upload Section -->
        <div class="bg-white rounded-lg shadow-lg p-8 mb-6">
            <h3 class="text-xl font-bold text-gray-800 mb-4">📄 PDF Resume Processing</h3>
            <div class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                <div class="text-gray-400 text-4xl mb-4">📁</div>
                <p class="text-gray-600 mb-4">Upload your PDF resume for AI optimization</p>
                <input type="file" accept=".pdf" class="mb-4" id="pdfUpload">
                <button onclick="processPDFResume()" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-semibold transition-colors">
                    Optimize PDF Resume
                </button>
                <p class="text-sm text-gray-500 mt-2">AI will analyze and optimize your resume, then generate an improved PDF</p>
            </div>
        </div>
        
        <!-- Optimized Content -->
        <div class="bg-white rounded-lg shadow-lg p-8">
            <h3 class="text-2xl font-bold text-gray-800 mb-4">📊 Optimized Resume Content</h3>
            <div class="prose max-w-none">
                <div class="text-gray-700 whitespace-pre-wrap bg-gray-50 p-4 rounded-lg">
                    {tailored_content if tailored_content else 'AI optimization in progress...'}
                </div>
            </div>
        </div>
        
        <!-- Key Improvements -->
        <div class="bg-blue-50 rounded-lg p-6">
            <h3 class="text-xl font-bold text-blue-800 mb-3">🔧 Key Improvements Made</h3>
            <ul class="text-blue-700 space-y-2">
                {''.join([f'<li>• {improvement}</li>' for improvement in improvements])}
            </ul>
        </div>
        
        <!-- Download Options -->
        <div class="bg-white rounded-lg shadow-lg p-6">
            <h3 class="text-xl font-bold text-gray-800 mb-4">💾 Download Options</h3>
            <div class="grid gap-4 md:grid-cols-2">
                <button onclick="downloadOptimizedPDF()" class="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors flex items-center justify-center">
                    <span class="mr-2">📄</span>
                    Download Optimized PDF
                </button>
                <button onclick="downloadTextVersion()" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold transition-colors flex items-center justify-center">
                    <span class="mr-2">📝</span>
                    Download Text Version
                </button>
            </div>
        </div>
        
        <script>
        function processPDFResume() {{
            const fileInput = document.getElementById('pdfUpload');
            const file = fileInput.files[0];
            
            if (!file) {{
                alert('Please select a PDF file first.');
                return;
            }}
            
            if (file.type !== 'application/pdf') {{
                alert('Please select a valid PDF file.');
                return;
            }}
            
            // Here you would implement the actual PDF processing
            alert('PDF processing feature will be implemented with the backend API endpoint.');
        }}
        
        function downloadOptimizedPDF() {{
            // This would trigger the PDF generation and download
            alert('PDF download will be implemented with the backend API endpoint.');
        }}
        
        function downloadTextVersion() {{
            const content = document.querySelector('.prose .text-gray-700').textContent;
            const blob = new Blob([content], {{ type: 'text/plain' }});
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'optimized_resume.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }}
        </script>
    </div>
    """

def generate_job_recommendations_html(job_recommendations: List[Dict], user_input: str) -> str:
    """Generate HTML for job recommendations"""
    
    # Generate job cards HTML
    job_cards_html = ""
    for i, job in enumerate(job_recommendations):
        match_color = "green" if job['match_score'] > 80 else "yellow" if job['match_score'] > 60 else "red"
        
        job_cards_html += f"""
        <div class="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow duration-300">
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-xl font-bold text-gray-800">{job['title']}</h3>
                <div class="flex items-center space-x-2">
                    <span class="bg-{match_color}-100 text-{match_color}-800 text-xs px-2 py-1 rounded-full font-semibold">
                        {job['match_score']}% Match
                    </span>
                    <div class="text-2xl">{'🎯' if i == 0 else '💼' if i == 1 else '🚀' if i == 2 else '⭐' if i == 3 else '🌟'}</div>
                </div>
            </div>
            
            <div class="mb-4">
                <p class="text-gray-600 font-semibold">{job['company']} • {job['location']}</p>
                <p class="text-green-600 font-semibold">{job['salary_range']}</p>
            </div>
            
            <p class="text-gray-600 mb-4">{job['description'][:150]}...</p>
            
            <div class="mb-4">
                <h4 class="font-semibold text-gray-700 mb-2">Key Requirements:</h4>
                <ul class="text-sm text-gray-600 space-y-1">
                    {''.join([f'<li>• {req}</li>' for req in job['requirements'][:3]])}
                </ul>
            </div>
            
            <div class="mb-4">
                <h4 class="font-semibold text-gray-700 mb-2">Your Skills Match:</h4>
                <div class="flex flex-wrap gap-1">
                    {''.join([f'<span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">{skill}</span>' for skill in job['skills_match'][:4]])}
                </div>
            </div>
            
            <div class="mb-4 p-3 bg-blue-50 rounded-lg">
                <h4 class="font-semibold text-blue-800 mb-1">Why This Role?</h4>
                <p class="text-blue-700 text-sm">{job['reasoning']}</p>
            </div>
            
            <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                    <span class="font-semibold text-gray-700">Growth:</span>
                    <span class="text-gray-600">{job['growth_potential']}</span>
                </div>
                <div>
                    <span class="font-semibold text-gray-700">ATS Score:</span>
                    <span class="text-gray-600">{job['ats_compatibility']}</span>
                </div>
            </div>
        </div>
        """
    
    return f"""
    <div class="space-y-6">
        <div class="text-center mb-8">
            <h2 class="text-3xl font-bold text-gray-800 mb-2">🎯 Intelligent Job Recommendations</h2>
            <p class="text-lg text-gray-600">Powered by RAG-based semantic matching and skill analysis</p>
            <p class="text-sm text-gray-500 mt-2">Your input: "{user_input}"</p>
        </div>
        
        <div class="bg-green-50 rounded-lg p-6 mb-6">
            <h3 class="text-lg font-semibold text-green-800 mb-2">🤖 AI Analysis Method</h3>
            <p class="text-green-700 text-sm">These recommendations are generated using semantic similarity search, skill matching, and market trend analysis rather than simple keyword matching.</p>
        </div>
        
        <div class="grid gap-6 md:grid-cols-1 lg:grid-cols-2">
            {job_cards_html}
        </div>
        
        <div class="bg-blue-50 rounded-lg p-6">
            <h3 class="text-xl font-bold text-blue-800 mb-3">💡 Next Steps</h3>
            <ul class="text-blue-700 space-y-2">
                <li>• Research the companies and their culture fit</li>
                <li>• Identify skill gaps and create a learning plan</li>
                <li>• Network with professionals in your target roles</li>
                <li>• Consider getting relevant certifications</li>
                <li>• Start building projects to showcase your skills</li>
            </ul>
        </div>
    </div>
    """

@app.post("/api/career-analysis", response_model=CareerAnalysisResponse)
async def career_analysis(request: CareerAnalysisRequest):
    """Career analysis endpoint with real system integration."""
    
    # Input validation
    is_valid, error_message = validate_input(request.user_input, request.analysis_type)
    if not is_valid:
        error_html = f"""
        <div class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
            <div class="text-red-600 text-4xl mb-4">⚠️</div>
            <h3 class="text-xl font-bold text-red-800 mb-2">Invalid Input</h3>
            <p class="text-red-700">{error_message}</p>
            <div class="mt-4">
                <button onclick="history.back()" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-semibold transition-colors">
                    Go Back
                </button>
            </div>
        </div>
        """
        return CareerAnalysisResponse(
            success=False,
            result=error_html,
            analysis_type=request.analysis_type
        )
    
    if request.analysis_type == "career_discovery":
        if REAL_SYSTEM_AVAILABLE:
            try:
                # Use the new RAG-based job recommendation engine
                print(f"--- Using RAG-based job recommendation engine: {request.user_input[:50]}... ---")
                
                # Extract skills from user input (basic extraction)
                user_skills = extract_skills_from_input(request.user_input)
                
                # Temporarily use CrewAI fallback for testing
                print("Using CrewAI fallback for testing...")
                career_result = run_sequential_crew(request.user_input)
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
        
    elif request.analysis_type == "resume_tailoring":
        if REAL_SYSTEM_AVAILABLE:
            try:
                # Use the enhanced RAG pipeline for resume tailoring with PDF support
                print(f"--- Using enhanced RAG system for resume tailoring: {request.user_input[:50]}... ---")
                cv_content = get_cv_content()
                
                # Use the enhanced RAG pipeline for resume analysis
                rag = EnhancedRAGPipeline()
                
                # Generate tailored resume content
                tailored_resume = rag.query_knowledge_base(
                    f"Optimize this resume for the following job requirements: {request.user_input}\n\nResume content: {cv_content}",
                    top_k=3
                )
                
                # Generate ATS score and optimization suggestions
                ats_score = calculate_ats_score(cv_content, request.user_input)
                
                result = generate_resume_tailoring_html(tailored_resume, ats_score, request.user_input, cv_content)
                
            except Exception as e:
                print(f"--- Real system error: {e} ---")
                # Fallback to mock data
                result = get_mock_resume_tailoring(request.user_input)
        else:
            # Use mock data if real system not available
            result = get_mock_resume_tailoring(request.user_input)
        
    elif request.analysis_type == "interview_prep":
        # Get actual CV content and generate personalized questions
        cv_content = get_cv_content()
        personalized_questions = generate_personalized_questions(request.user_input, cv_content)
        
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
        
        # Ensure result is set
        if 'result' not in locals():
            result = f"<div class='text-center p-8'><h2 class='text-2xl font-bold text-red-600'>Error: Unknown analysis type</h2><p class='text-gray-600'>Analysis type '{request.analysis_type}' is not supported.</p></div>"
        
        return CareerAnalysisResponse(
            success=True,
            result=result,
            analysis_type=request.analysis_type
        )

@app.post("/api/process-resume-pdf")
async def process_resume_pdf_endpoint(
    file: UploadFile = File(...),
    job_description: str = ""
):
    """Process uploaded PDF resume and return optimized version"""
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Save uploaded file temporarily
        temp_input_path = f"temp_input_{file.filename}"
        with open(temp_input_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process the PDF
        if REAL_SYSTEM_AVAILABLE:
            try:
                from pdf_resume_processor import process_resume_pdf
                output_path = f"optimized_{file.filename}"
                success, message = process_resume_pdf(temp_input_path, job_description, output_path)
                
                if success:
                    # Return the optimized PDF file
                    return FileResponse(
                        path=output_path,
                        filename=output_path,
                        media_type='application/pdf'
                    )
                else:
                    raise HTTPException(status_code=500, detail=f"PDF processing failed: {message}")
            except Exception as e:
                print(f"PDF processing error: {e}")
                raise HTTPException(status_code=500, detail=f"PDF processing error: {str(e)}")
        else:
            raise HTTPException(status_code=503, detail="PDF processing system not available")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
    finally:
        # Clean up temporary file
        if os.path.exists(temp_input_path):
            os.remove(temp_input_path)

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Mock API is running"}

if __name__ == "__main__":
    print("🚀 Starting CareerAIpilot Mock API...")
    print("🌐 Frontend: http://127.0.0.1:8001/")
    print("📚 API Docs: http://127.0.0.1:8001/docs")
    uvicorn.run(app, host="127.0.0.1", port=8001)
