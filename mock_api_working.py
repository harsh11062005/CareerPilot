#!/usr/bin/env python3
"""
Working Mock API for CareerAIpilot frontend testing
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import uvicorn
import os
from typing import List, Dict

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

def get_mock_interview_prep(user_input: str):
    """Generate mock interview prep results"""
    return f"""
    <div class="space-y-6">
        <div class="text-center mb-8">
            <h2 class="text-3xl font-bold text-gray-800 mb-2">💬 Personalized Mock Interview</h2>
            <p class="text-lg text-gray-600">Interview questions tailored to your interests</p>
        </div>
        
        <!-- Interactive Interview Interface -->
        <div class="bg-white rounded-lg shadow-lg p-8">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-2xl font-bold text-gray-800">🎯 Mock Interview</h3>
                <button onclick="endInterview()" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-semibold transition-colors">
                    End Interview
                </button>
            </div>
            
            <!-- Interview Status -->
            <div class="mb-6">
                <div class="flex justify-between text-sm text-gray-600 mb-2">
                    <span>Question <span id="questionNum">1</span> of 5</span>
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
                        <p id="questionText" class="text-gray-700 text-lg">Tell me about yourself and your experience with {user_input.lower()}.</p>
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
                <p class="text-green-700">Great job completing the mock interview! You've answered all questions successfully.</p>
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
                        <li>• Review recent developments in your field</li>
                        <li>• Prepare specific examples using the STAR method</li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-semibold text-gray-700 mb-2">Company Research</h4>
                    <ul class="text-sm text-gray-600 space-y-1">
                        <li>• Research the company's products and services</li>
                        <li>• Prepare thoughtful questions about their strategy</li>
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

    // Mock interview questions
    const questions = [
        "Tell me about yourself and your experience with {user_input.lower()}.",
        "What interests you most about this field?",
        "Describe a challenging project you've worked on.",
        "How do you stay updated with industry trends?",
        "Where do you see yourself in 5 years?"
    ];

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

@app.get("/")
async def serve_frontend():
    """Serve the main frontend HTML file."""
    try:
        with open("career_ai_frontend.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Frontend file not found</h1>", status_code=404)

@app.options("/api/career-analysis")
async def career_analysis_options():
    """Handle CORS preflight requests."""
    return {"message": "OK"}

@app.post("/api/career-analysis", response_model=CareerAnalysisResponse)
async def career_analysis(request: CareerAnalysisRequest):
    """Career analysis endpoint with mock data."""
    
    # Input validation
    if not request.user_input or not request.user_input.strip():
        error_html = """
        <div class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
            <div class="text-red-600 text-4xl mb-4">⚠️</div>
            <h3 class="text-xl font-bold text-red-800 mb-2">Invalid Input</h3>
            <p class="text-red-700">Please provide some input. Tell us about your interests, skills, or career goals.</p>
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
    
    if len(request.user_input.strip()) < 3:
        error_html = """
        <div class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
            <div class="text-red-600 text-4xl mb-4">⚠️</div>
            <h3 class="text-xl font-bold text-red-800 mb-2">Input Too Short</h3>
            <p class="text-red-700">Input is too short. Please provide more details about your interests or goals.</p>
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
    
    # Generate appropriate response based on analysis type
    if request.analysis_type == "career_discovery":
        result = get_mock_career_discovery(request.user_input)
    elif request.analysis_type == "resume_tailoring":
        result = get_mock_resume_tailoring(request.user_input)
    elif request.analysis_type == "interview_prep":
        result = get_mock_interview_prep(request.user_input)
    else:
        result = f"""
        <div class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
            <div class="text-red-600 text-4xl mb-4">❌</div>
            <h3 class="text-xl font-bold text-red-800 mb-2">Invalid Analysis Type</h3>
            <p class="text-red-700">Analysis type '{request.analysis_type}' is not supported.</p>
        </div>
        """
    
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
