# CareerAIpilot - AI-Powered Career Assistant

CareerAIpilot is a comprehensive AI-powered career development platform that helps users with career discovery, resume optimization, and interview preparation through advanced AI agents and interactive interfaces.

## 🚀 Features

### 🎯 Career Discovery
- **Intelligent Career Path Analysis**: AI-powered recommendations based on your interests and skills
- **Comprehensive Career Information**: Detailed insights including salary ranges, growth prospects, and required skills
- **Industry-Specific Guidance**: Tailored recommendations for AI/ML, Data Science, Software Engineering, and more
- **Real-time Market Data**: Up-to-date information on job demand and career trends

### 📄 Resume Tailoring
- **AI-Optimized Resume Generation**: Intelligent resume customization for specific job roles
- **ATS Score Analysis**: Automated tracking system compatibility scoring
- **Keyword Optimization**: Strategic keyword placement for better visibility
- **PDF Processing**: Upload and optimize existing resumes in PDF format
- **Multiple Output Formats**: Download optimized resumes in PDF, DOCX, or copy to clipboard

### 💬 Interview Preparation
- **Interactive Mock Interviews**: Real-time question-and-answer sessions with AI coaching
- **Personalized Questions**: Tailored interview questions based on your field and experience level
- **Instant Feedback**: Real-time feedback on answer quality and structure
- **Progress Tracking**: Visual progress indicators and completion tracking
- **Multiple Interview Types**: Technical, behavioral, and role-specific interview preparation

## 🛠️ Technology Stack

- **Backend**: Python, FastAPI, Uvicorn
- **AI Framework**: CrewAI for multi-agent orchestration
- **LLM Integration**: Google Gemini API for AI-powered responses
- **RAG Pipeline**: FAISS, ChromaDB, and LangChain for document processing
- **Frontend**: HTML5, Tailwind CSS, Alpine.js
- **Document Processing**: PyPDF2, python-docx, ReportLab
- **Vector Search**: Sentence Transformers for semantic similarity

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key (for AI functionality)
- Modern web browser

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/harsh11062005/CareerPilot.git
cd CareerPilot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory:
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. Run the Application
```bash
python mock_api.py
```

### 5. Access the Application
Open your browser and navigate to: **http://127.0.0.1:8001/**

## 📖 Usage Guide

### Career Discovery
1. Click on the "Career Discovery" section
2. Enter your interests (e.g., "I want to work in AI and machine learning")
3. Click "Start Analysis"
4. Review personalized career recommendations with detailed insights

### Resume Tailoring
1. Click on the "Resume Tailoring" section
2. Enter job requirements or upload a PDF resume
3. Click "Start Analysis"
4. Get an optimized resume with ATS score and improvement suggestions

### Interview Preparation
1. Click on the "Interview Prep" section
2. Enter your interview focus (e.g., "I want to practice for software engineering interviews")
3. Click "Start Analysis"
4. Engage in an interactive mock interview with real-time feedback

## 🏗️ Architecture

### Multi-Agent System
- **Career Discovery Agent**: Analyzes user interests and provides career recommendations
- **Resume Tailoring Agent**: Optimizes resumes for specific job roles
- **Interview Prep Agent**: Generates personalized interview questions and feedback

### RAG Pipeline
- **Document Processing**: Extracts and processes resume content
- **Vector Indexing**: Creates searchable embeddings using FAISS and ChromaDB
- **Semantic Search**: Retrieves relevant information for personalized responses

### Frontend Interface
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Interactive Components**: Real-time feedback and progress tracking
- **Modern UI**: Clean, professional interface with Tailwind CSS

## 📁 Project Structure

```
CareerAIpilot/
├── agents.py                 # AI agent definitions
├── tasks.py                  # CrewAI task definitions
├── main.py                   # Main application entry point
├── mock_api.py              # FastAPI server and mock backend
├── career_ai_frontend.html  # Frontend interface
├── enhanced_rag_pipeline.py # Advanced RAG implementation
├── job_recommendation_engine.py # Intelligent job matching
├── pdf_resume_processor.py  # PDF processing utilities
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## 🔧 Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Google Gemini API key for AI functionality
- `FAISS_INDEX_PATH`: Path for FAISS vector index storage
- `CHROMA_DB_PATH`: Path for ChromaDB storage

### API Endpoints
- `GET /`: Serve the frontend interface
- `POST /api/career-analysis`: Main analysis endpoint
- `POST /api/process-resume-pdf`: PDF resume processing
- `GET /api/health`: Health check endpoint

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CrewAI** for multi-agent orchestration
- **LangChain** for RAG pipeline implementation
- **FastAPI** for robust backend API
- **Tailwind CSS** for beautiful UI components
- **Google Gemini** for AI-powered responses

## 📞 Support

For support, email harshitbhinde@gmail.com or create an issue in the repository.

## 🔮 Roadmap

- [ ] User authentication and profiles
- [ ] Advanced analytics and reporting
- [ ] Integration with job boards
- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Advanced AI model fine-tuning

---

**Made with ❤️ by Harshit Bhinde**