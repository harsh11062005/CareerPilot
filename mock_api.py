#!/usr/bin/env python3
"""
Working Mock API for CareerAIpilot frontend testing
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import uvicorn
import json
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
    """Generate comprehensive interview prep results"""
    
    # Extract interview focus from user input
    interview_focus = user_input.lower()
    
    # Generate tailored questions based on focus
    if any(word in interview_focus for word in ['ai', 'ml', 'machine learning', 'artificial intelligence']):
        questions = [
            "Tell me about your experience with machine learning frameworks like TensorFlow or PyTorch.",
            "Describe a challenging AI project you've worked on and how you solved the problems.",
            "How do you handle model overfitting and what techniques do you use to prevent it?",
            "Explain the difference between supervised and unsupervised learning with examples.",
            "How would you approach building a recommendation system for an e-commerce platform?",
            "Describe your experience with MLOps and model deployment in production environments.",
            "What's your approach to feature engineering and selection for machine learning models?",
            "How do you evaluate the performance of different machine learning models?"
        ]
    elif any(word in interview_focus for word in ['data', 'analytics', 'data science']):
        questions = [
            "Walk me through your data analysis process from raw data to actionable insights.",
            "Describe a time when you had to work with messy or incomplete data. How did you handle it?",
            "How do you determine which statistical tests to use for different types of data analysis?",
            "Explain your experience with A/B testing and how you design effective experiments.",
            "Describe your approach to building predictive models and selecting the right algorithm.",
            "How do you communicate complex data insights to non-technical stakeholders?",
            "What tools and techniques do you use for data visualization and why?",
            "Describe your experience with big data technologies like Spark or Hadoop."
        ]
    elif any(word in interview_focus for word in ['software', 'developer', 'engineer', 'programming']):
        questions = [
            "Describe your experience with different programming languages and when you'd use each.",
            "Walk me through your software development process from requirements to deployment.",
            "How do you handle debugging complex issues in production systems?",
            "Describe your experience with version control and collaborative development workflows.",
            "Explain your approach to writing clean, maintainable code and code reviews.",
            "How do you design scalable software architectures for high-traffic applications?",
            "Describe your experience with testing strategies and ensuring code quality.",
            "How do you stay updated with new technologies and programming best practices?"
        ]
    else:
        questions = [
            "Tell me about yourself and your background in technology.",
            "What interests you most about this field and why are you passionate about it?",
            "Describe a challenging project you've worked on and how you overcame obstacles.",
            "How do you approach problem-solving when faced with complex technical challenges?",
            "What's your experience with working in teams and collaborating with others?",
            "How do you prioritize tasks and manage your time effectively?",
            "Describe a time when you had to learn a new technology quickly. How did you approach it?",
            "Where do you see yourself in your career in the next 5 years?"
        ]
    
    return f"""
    <div class="space-y-6">
        <div class="text-center mb-8">
            <h2 class="text-3xl font-bold text-gray-800 mb-2">💬 Personalized Mock Interview</h2>
            <p class="text-lg text-gray-600">Interview questions tailored to your interests: <strong>{user_input}</strong></p>
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
                    <span>Question <span id="questionNum">1</span> of {len(questions)}</span>
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
                        <p id="questionText" class="text-gray-700 text-lg">{questions[0]}</p>
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
            </div>
            
            <!-- Interview Complete -->
            <div id="complete" class="hidden mt-6 bg-green-50 rounded-lg p-6 text-center">
                <div class="text-green-600 text-4xl mb-4">🎉</div>
                <h4 class="text-xl font-bold text-green-800 mb-2">Interview Complete!</h4>
                <p class="text-green-700">Great job completing the mock interview! You've answered all {len(questions)} questions successfully.</p>
                <div class="mt-4">
                    <button onclick="viewFeedback()" class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg font-semibold transition-colors">
                        View Detailed Feedback
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Preparation Tips -->
        <div class="bg-gray-50 rounded-lg p-6">
            <h3 class="text-xl font-bold text-gray-800 mb-4">📚 Interview Preparation Tips</h3>
            <div class="grid gap-6 md:grid-cols-2">
                <div>
                    <h4 class="font-semibold text-gray-700 mb-3">Technical Preparation</h4>
                    <ul class="text-sm text-gray-600 space-y-2">
                        <li>• Practice coding problems on LeetCode, HackerRank, or Codility</li>
                        <li>• Review fundamental concepts and recent developments in your field</li>
                        <li>• Prepare specific examples using the STAR method (Situation, Task, Action, Result)</li>
                        <li>• Practice explaining complex technical concepts in simple terms</li>
                        <li>• Review your past projects and be ready to discuss them in detail</li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-semibold text-gray-700 mb-3">Behavioral & Soft Skills</h4>
                    <ul class="text-sm text-gray-600 space-y-2">
                        <li>• Research the company's products, services, and recent news</li>
                        <li>• Prepare thoughtful questions about their technology stack and challenges</li>
                        <li>• Practice discussing your career goals and why you're interested in the role</li>
                        <li>• Prepare examples of leadership, teamwork, and problem-solving</li>
                        <li>• Practice your elevator pitch and be ready to discuss your background</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <!-- Common Interview Questions -->
        <div class="bg-blue-50 rounded-lg p-6">
            <h3 class="text-xl font-bold text-blue-800 mb-4">🎯 Common Interview Questions</h3>
            <div class="grid gap-4 md:grid-cols-2">
                <div>
                    <h4 class="font-semibold text-blue-700 mb-2">Technical Questions:</h4>
                    <ul class="text-sm text-blue-600 space-y-1">
                        <li>• System design and architecture</li>
                        <li>• Algorithm and data structure problems</li>
                        <li>• Framework and technology-specific questions</li>
                        <li>• Debugging and troubleshooting scenarios</li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-semibold text-blue-700 mb-2">Behavioral Questions:</h4>
                    <ul class="text-sm text-blue-600 space-y-1">
                        <li>• Tell me about yourself</li>
                        <li>• Describe a challenging project</li>
                        <li>• How do you handle conflicts?</li>
                        <li>• Where do you see yourself in 5 years?</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <script>
    // Ensure functions are in global scope
    window.interviewState = {{
        currentQuestion: 0,
        answers: [],
        isComplete: false
    }};

    // Interview questions
    window.questions = {json.dumps(questions)};

    window.submitAnswer = function() {{
        console.log('submitAnswer called'); // Debug log
        
        const answerElement = document.getElementById('userAnswer');
        if (!answerElement) {{
            alert('Error: Answer field not found. Please refresh the page.');
            return;
        }}
        
        const answer = answerElement.value.trim();
        
        if (answer === '') {{
            alert('Please provide an answer before submitting.');
            return;
        }}
        
        console.log('Answer submitted:', answer); // Debug log
        
        // Save answer
        window.interviewState.answers[window.interviewState.currentQuestion] = answer;
        
        // Show feedback
        window.showFeedback(answer);
        
        // Move to next question after a short delay
        setTimeout(() => {{
            window.nextQuestion();
        }}, 2000);
    }};

    window.nextQuestion = function() {{
        window.interviewState.currentQuestion++;
        
        if (window.interviewState.currentQuestion >= window.questions.length) {{
            // Interview complete
            window.completeInterview();
            return;
        }}
        
        // Update question
        document.getElementById('questionNum').textContent = window.interviewState.currentQuestion + 1;
        document.getElementById('questionText').textContent = window.questions[window.interviewState.currentQuestion];
        document.getElementById('userAnswer').value = '';
        
        // Update progress
        const progress = ((window.interviewState.currentQuestion + 1) / window.questions.length) * 100;
        document.getElementById('progress').style.width = progress + '%';
        
        // Update status
        document.getElementById('interviewStatus').textContent = 'Answer the question above';
        
        // Focus on answer input
        document.getElementById('userAnswer').focus();
    }};

    window.showFeedback = function(answer) {{
        let feedback = '';
        let feedbackColor = 'blue';
        
        if (answer.length < 50) {{
            feedback = '💡 Tip: Try to provide more detail. Include specific examples and explain your thought process.';
            feedbackColor = 'yellow';
        }} else if (answer.length < 150) {{
            feedback = '✅ Good start! Consider adding more specific examples or technical details.';
            feedbackColor = 'blue';
        }} else if (answer.length < 300) {{
            feedback = '✅ Great answer length! You\\'re providing good detail while staying concise.';
            feedbackColor = 'green';
        }} else {{
            feedback = '✅ Excellent detail! Make sure your answer is well-structured and easy to follow.';
            feedbackColor = 'green';
        }}
        
        // Show feedback temporarily
        const feedbackDiv = document.createElement('div');
        feedbackDiv.className = `mt-4 p-3 bg-${{feedbackColor}}-50 border-l-4 border-${{feedbackColor}}-400 rounded`;
        feedbackDiv.innerHTML = `<p class="text-${{feedbackColor}}-800 text-sm">${{feedback}}</p>`;
        
        document.getElementById('submitBtn').parentNode.insertBefore(feedbackDiv, document.getElementById('submitBtn'));
        
        // Remove feedback after 5 seconds
        setTimeout(() => {{
            feedbackDiv.remove();
        }}, 5000);
    }};

    window.completeInterview = function() {{
        window.interviewState.isComplete = true;
        
        // Hide interview interface
        document.querySelector('.bg-white.rounded-lg.shadow-lg').classList.add('hidden');
        
        // Show completion message
        document.getElementById('complete').classList.remove('hidden');
        
        // Update status
        document.getElementById('interviewStatus').textContent = 'Interview completed successfully';
    }};

    window.viewFeedback = function() {{
        alert('Great job! You completed all ' + window.questions.length + ' interview questions. Continue practicing with different scenarios to improve your interview skills.');
    }};

    window.endInterview = function() {{
        if (confirm('Are you sure you want to end the interview? Your progress will be lost.')) {{
            // Reset state
            window.interviewState = {{
                currentQuestion: 0,
                answers: [],
                isComplete: false
            }};
            
            // Reset UI
            document.getElementById('questionNum').textContent = '1';
            document.getElementById('questionText').textContent = window.questions[0];
            document.getElementById('userAnswer').value = '';
            document.getElementById('progress').style.width = '0%';
            document.getElementById('interviewStatus').textContent = 'Ready to start';
            
            // Show submit button
            document.getElementById('submitBtn').classList.remove('hidden');
            
            // Hide completion message
            document.getElementById('complete').classList.add('hidden');
            
            // Show interview interface
            document.querySelector('.bg-white.rounded-lg.shadow-lg').classList.remove('hidden');
        }}
    }};

    // Initialize interview - run immediately and also on DOM ready
    window.initializeInterview = function() {{
        const statusElement = document.getElementById('interviewStatus');
        const answerElement = document.getElementById('userAnswer');
        if (statusElement) statusElement.textContent = 'Answer the question above';
        if (answerElement) answerElement.focus();
    }};
    
    // Initialize immediately
    window.initializeInterview();
    
    // Also initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', window.initializeInterview);
    
    // Initialize when content is dynamically loaded
    setTimeout(window.initializeInterview, 100);
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
