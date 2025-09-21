"""
Enhanced RAG Pipeline for CareerPilot
Implements two specialized RAG agents:
1. CV Creator Agent - Processes user CVs with advanced document loaders
2. Interview Prep Generator Agent - Processes interview knowledge base
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import chromadb
from chromadb.config import Settings

# LangChain imports
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentenceTransformerEmbeddings:
    """
    Custom embedding wrapper for sentence transformers to work with LangChain
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents"""
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query"""
        embedding = self.model.encode([text])
        return embedding[0].tolist()

class EnhancedRAGPipeline:
    """
    Enhanced RAG pipeline with two specialized agents
    """
    
    def __init__(self, 
                 openai_api_key: Optional[str] = None,
                 persist_directory: str = "./chroma_db",
                 embedding_model: str = "text-embedding-ada-002"):
        """
        Initialize the enhanced RAG pipeline
        
        Args:
            openai_api_key: OpenAI API key for embeddings
            persist_directory: Directory to persist ChromaDB
            embedding_model: OpenAI embedding model to use
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.persist_directory = persist_directory
        self.embedding_model = embedding_model
        
        # Initialize embeddings
        if self.openai_api_key:
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=self.openai_api_key,
                model=self.embedding_model
            )
        else:
            logger.warning("No OpenAI API key provided. Using sentence transformers fallback.")
            from sentence_transformers import SentenceTransformer
            self.embeddings = SentenceTransformerEmbeddings('all-MiniLM-L6-v2')
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Initialize ChromaDB client
        self.chroma_client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize vector stores for each agent
        self.cv_vectorstore = None
        self.interview_vectorstore = None
        
    def _get_document_loader(self, file_path: str):
        """
        Get appropriate document loader based on file extension
        
        Args:
            file_path: Path to the document
            
        Returns:
            Appropriate document loader
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        if extension == '.pdf':
            return PyPDFLoader(str(file_path))
        elif extension in ['.doc', '.docx']:
            return Docx2txtLoader(str(file_path))
        elif extension == '.txt':
            return TextLoader(str(file_path), encoding='utf-8')
        else:
            raise ValueError(f"Unsupported file format: {extension}")
    
    def _load_and_split_documents(self, file_paths: Union[str, List[str]]) -> List[Document]:
        """
        Load and split documents into chunks
        
        Args:
            file_paths: Single file path or list of file paths
            
        Returns:
            List of document chunks
        """
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        
        all_documents = []
        
        for file_path in file_paths:
            try:
                logger.info(f"Loading document: {file_path}")
                loader = self._get_document_loader(file_path)
                documents = loader.load()
                
                # Split documents
                split_docs = self.text_splitter.split_documents(documents)
                all_documents.extend(split_docs)
                
                logger.info(f"Loaded {len(split_docs)} chunks from {file_path}")
                
            except Exception as e:
                logger.error(f"Error loading {file_path}: {str(e)}")
                continue
        
        return all_documents


class CVCreatorAgent(EnhancedRAGPipeline):
    """
    RAG Agent #1: CV Creator
    Processes user CVs with advanced document loaders and ChromaDB
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collection_name = "cv_documents"
        
    def build_cv_index(self, cv_paths: Union[str, List[str]]) -> bool:
        """
        Build CV index using PyPDFLoader, RecursiveCharacterTextSplitter, and ChromaDB
        
        Args:
            cv_paths: Path(s) to CV file(s)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("Building CV index with enhanced pipeline...")
            
            # Load and split documents
            documents = self._load_and_split_documents(cv_paths)
            
            if not documents:
                logger.error("No documents loaded")
                return False
            
            # Create ChromaDB collection
            self.cv_vectorstore = Chroma(
                client=self.chroma_client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )
            
            # Add documents to vector store
            logger.info(f"Adding {len(documents)} document chunks to CV vector store...")
            self.cv_vectorstore.add_documents(documents)
            
            logger.info(f"Successfully built CV index with {len(documents)} chunks")
            return True
            
        except Exception as e:
            logger.error(f"Error building CV index: {str(e)}")
            return False
    
    def query_cv_index(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Query the CV index for relevant information
        
        Args:
            query: Query string
            top_k: Number of top results to return
            
        Returns:
            List of relevant CV chunks with metadata
        """
        try:
            if self.cv_vectorstore is None:
                # Try to load existing vector store
                self.cv_vectorstore = Chroma(
                    client=self.chroma_client,
                    collection_name=self.collection_name,
                    embedding_function=self.embeddings,
                    persist_directory=self.persist_directory
                )
            
            # Perform similarity search
            results = self.cv_vectorstore.similarity_search_with_score(query, k=top_k)
            
            # Format results
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    'text': doc.page_content,
                    'score': float(score),
                    'metadata': doc.metadata,
                    'source': doc.metadata.get('source', 'Unknown')
                })
            
            logger.info(f"Found {len(formatted_results)} relevant CV chunks for query: '{query}'")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error querying CV index: {str(e)}")
            return []
    
    def get_cv_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the indexed CV
        
        Returns:
            Dictionary containing CV summary information
        """
        try:
            if self.cv_vectorstore is None:
                return {"error": "No CV index found"}
            
            # Get all documents from the collection
            collection = self.chroma_client.get_collection(self.collection_name)
            count = collection.count()
            
            # Get sample documents for analysis
            sample_docs = self.cv_vectorstore.similarity_search("", k=min(10, count))
            
            total_words = sum(len(doc.page_content.split()) for doc in sample_docs)
            
            # Extract key sections
            sections = {
                'experience': 0,
                'education': 0,
                'skills': 0,
                'projects': 0
            }
            
            keywords = {
                'experience': ['experience', 'work', 'employment', 'job', 'position', 'career'],
                'education': ['education', 'degree', 'university', 'college', 'school', 'graduated'],
                'skills': ['skills', 'technologies', 'programming', 'languages', 'tools', 'expertise'],
                'projects': ['project', 'portfolio', 'developed', 'built', 'created', 'implemented']
            }
            
            for doc in sample_docs:
                doc_lower = doc.page_content.lower()
                for section, section_keywords in keywords.items():
                    if any(keyword in doc_lower for keyword in section_keywords):
                        sections[section] += 1
            
            return {
                'total_chunks': count,
                'total_words': total_words,
                'sections': sections,
                'sample_text': sample_docs[0].page_content[:200] if sample_docs else ""
            }
            
        except Exception as e:
            logger.error(f"Error getting CV summary: {str(e)}")
            return {"error": str(e)}


class InterviewPrepGeneratorAgent(EnhancedRAGPipeline):
    """
    RAG Agent #2: Interview Prep Generator
    Processes interview questions, tips, and company-specific data
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collection_name = "interview_knowledge"
        
    def build_interview_knowledge_base(self, knowledge_paths: Union[str, List[str]]) -> bool:
        """
        Build interview knowledge base from curated data
        
        Args:
            knowledge_paths: Path(s) to knowledge base file(s)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("Building interview knowledge base...")
            
            # Load and split documents
            documents = self._load_and_split_documents(knowledge_paths)
            
            if not documents:
                logger.error("No knowledge base documents loaded")
                return False
            
            # Create ChromaDB collection
            self.interview_vectorstore = Chroma(
                client=self.chroma_client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )
            
            # Add documents to vector store
            logger.info(f"Adding {len(documents)} knowledge chunks to interview vector store...")
            self.interview_vectorstore.add_documents(documents)
            
            logger.info(f"Successfully built interview knowledge base with {len(documents)} chunks")
            return True
            
        except Exception as e:
            logger.error(f"Error building interview knowledge base: {str(e)}")
            return False
    
    def query_interview_knowledge(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Query the interview knowledge base
        
        Args:
            query: Query string
            top_k: Number of top results to return
            
        Returns:
            List of relevant knowledge chunks
        """
        try:
            if self.interview_vectorstore is None:
                # Try to load existing vector store
                self.interview_vectorstore = Chroma(
                    client=self.chroma_client,
                    collection_name=self.collection_name,
                    embedding_function=self.embeddings,
                    persist_directory=self.persist_directory
                )
            
            # Perform similarity search
            results = self.interview_vectorstore.similarity_search_with_score(query, k=top_k)
            
            # Format results
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    'text': doc.page_content,
                    'score': float(score),
                    'metadata': doc.metadata,
                    'source': doc.metadata.get('source', 'Unknown')
                })
            
            logger.info(f"Found {len(formatted_results)} relevant knowledge chunks for query: '{query}'")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error querying interview knowledge: {str(e)}")
            return []
    
    def generate_interview_questions(self, 
                                   job_description: str, 
                                   cv_content: str,
                                   question_types: List[str] = None) -> Dict[str, List[str]]:
        """
        Generate interview questions based on job description and CV
        
        Args:
            job_description: Job description text
            cv_content: CV content text
            question_types: Types of questions to generate
            
        Returns:
            Dictionary of generated questions by type
        """
        if question_types is None:
            question_types = ['technical', 'behavioral', 'situational', 'company_culture']
        
        try:
            generated_questions = {}
            
            for question_type in question_types:
                # Query knowledge base for relevant questions
                query = f"{question_type} interview questions for {job_description[:100]}"
                knowledge_results = self.query_interview_knowledge(query, top_k=3)
                
                # Extract questions from knowledge base
                questions = []
                for result in knowledge_results:
                    # Simple extraction of questions (ending with ?)
                    text = result['text']
                    question_sentences = [s.strip() for s in text.split('.') if '?' in s]
                    questions.extend(question_sentences[:2])  # Limit to 2 per result
                
                generated_questions[question_type] = questions[:5]  # Limit to 5 per type
            
            return generated_questions
            
        except Exception as e:
            logger.error(f"Error generating interview questions: {str(e)}")
            return {}


# Clean, callable functions for MCP server integration
def build_cv_index_enhanced(cv_paths: Union[str, List[str]], 
                          openai_api_key: Optional[str] = None) -> bool:
    """
    Enhanced CV index building function for MCP server
    
    Args:
        cv_paths: Path(s) to CV file(s)
        openai_api_key: OpenAI API key for embeddings
        
    Returns:
        True if successful, False otherwise
    """
    agent = CVCreatorAgent(openai_api_key=openai_api_key)
    return agent.build_cv_index(cv_paths)


def query_cv_index_enhanced(query: str, 
                          top_k: int = 5,
                          openai_api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Enhanced CV querying function for MCP server
    
    Args:
        query: Query string
        top_k: Number of top results to return
        openai_api_key: OpenAI API key for embeddings
        
    Returns:
        List of relevant CV chunks
    """
    agent = CVCreatorAgent(openai_api_key=openai_api_key)
    return agent.query_cv_index(query, top_k)


def build_interview_knowledge_base(knowledge_paths: Union[str, List[str]], 
                                 openai_api_key: Optional[str] = None) -> bool:
    """
    Interview knowledge base building function for MCP server
    
    Args:
        knowledge_paths: Path(s) to knowledge base file(s)
        openai_api_key: OpenAI API key for embeddings
        
    Returns:
        True if successful, False otherwise
    """
    agent = InterviewPrepGeneratorAgent(openai_api_key=openai_api_key)
    return agent.build_interview_knowledge_base(knowledge_paths)


def query_interview_knowledge(query: str, 
                            top_k: int = 5,
                            openai_api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Interview knowledge querying function for MCP server
    
    Args:
        query: Query string
        top_k: Number of top results to return
        openai_api_key: OpenAI API key for embeddings
        
    Returns:
        List of relevant knowledge chunks
    """
    agent = InterviewPrepGeneratorAgent(openai_api_key=openai_api_key)
    return agent.query_interview_knowledge(query, top_k)


def generate_interview_questions(job_description: str, 
                               cv_content: str,
                               question_types: List[str] = None,
                               openai_api_key: Optional[str] = None) -> Dict[str, List[str]]:
    """
    Interview question generation function for MCP server
    
    Args:
        job_description: Job description text
        cv_content: CV content text
        question_types: Types of questions to generate
        openai_api_key: OpenAI API key for embeddings
        
    Returns:
        Dictionary of generated questions by type
    """
    agent = InterviewPrepGeneratorAgent(openai_api_key=openai_api_key)
    return agent.generate_interview_questions(job_description, cv_content, question_types)


if __name__ == "__main__":
    """
    Test the enhanced RAG pipeline
    """
    print("=== Enhanced CareerPilot RAG Pipeline Test ===\n")
    
    # Create sample data
    sample_cv = """
    John Doe
    Senior Software Engineer
    
    EXPERIENCE:
    Senior Software Engineer at TechCorp (2020-2024)
    - Developed web applications using Python, Django, and React
    - Led a team of 5 developers
    - Implemented CI/CD pipelines using Docker and Jenkins
    - Improved system performance by 40%
    
    Software Engineer at StartupXYZ (2018-2020)
    - Built REST APIs using Python Flask
    - Worked with PostgreSQL and Redis
    - Collaborated with frontend team on React applications
    
    EDUCATION:
    Bachelor of Science in Computer Science
    University of Technology (2014-2018)
    GPA: 3.8/4.0
    
    SKILLS:
    Programming Languages: Python, JavaScript, Java, C++
    Frameworks: Django, Flask, React, Node.js
    Databases: PostgreSQL, MongoDB, Redis
    Tools: Docker, Jenkins, Git, AWS
    """
    
    sample_interview_knowledge = """
    TECHNICAL INTERVIEW QUESTIONS:
    
    Python Questions:
    1. What is the difference between a list and a tuple in Python?
    2. Explain the concept of decorators in Python.
    3. How do you handle exceptions in Python?
    4. What is the difference between __str__ and __repr__?
    5. Explain the GIL (Global Interpreter Lock) in Python.
    
    Django Questions:
    1. What is the difference between Django's class-based views and function-based views?
    2. Explain Django's ORM and how it works.
    3. What is Django middleware and how do you create custom middleware?
    4. How do you handle database migrations in Django?
    5. What is Django's template system and how do you create custom template tags?
    
    BEHAVIORAL INTERVIEW QUESTIONS:
    
    Leadership Questions:
    1. Tell me about a time when you had to lead a difficult team member.
    2. Describe a situation where you had to make a tough decision without all the information.
    3. How do you motivate your team when facing tight deadlines?
    4. Tell me about a time when you had to give difficult feedback to a colleague.
    5. Describe a situation where you had to resolve a conflict between team members.
    
    Problem-Solving Questions:
    1. Tell me about a time when you had to solve a complex technical problem.
    2. Describe a situation where you had to learn a new technology quickly.
    3. How do you approach debugging a difficult issue?
    4. Tell me about a time when you had to optimize performance in an application.
    5. Describe a situation where you had to work with legacy code.
    
    COMPANY CULTURE QUESTIONS:
    
    TechCorp Culture:
    1. How do you stay updated with the latest technology trends?
    2. What do you think makes a good software engineer?
    3. How do you balance technical debt with new feature development?
    4. What is your approach to code reviews?
    5. How do you ensure code quality in your projects?
    """
    
    # Create sample files
    sample_cv_path = "sample_cv.txt"
    sample_knowledge_path = "sample_interview_knowledge.txt"
    
    with open(sample_cv_path, 'w', encoding='utf-8') as f:
        f.write(sample_cv)
    
    with open(sample_knowledge_path, 'w', encoding='utf-8') as f:
        f.write(sample_interview_knowledge)
    
    print(f"Created sample files: {sample_cv_path}, {sample_knowledge_path}")
    
    # Test CV Creator Agent
    print("\n1. Testing CV Creator Agent...")
    cv_agent = CVCreatorAgent()
    
    success = cv_agent.build_cv_index(sample_cv_path)
    if success:
        print("✓ CV index built successfully!")
        
        # Test CV queries
        cv_queries = [
            "What programming languages does John know?",
            "Tell me about John's work experience",
            "What is John's educational background?"
        ]
        
        for query in cv_queries:
            print(f"\n   Query: {query}")
            results = cv_agent.query_cv_index(query, top_k=2)
            for i, result in enumerate(results, 1):
                print(f"   Result {i}: {result['text'][:100]}...")
    else:
        print("✗ Failed to build CV index")
    
    # Test Interview Prep Generator Agent
    print("\n2. Testing Interview Prep Generator Agent...")
    interview_agent = InterviewPrepGeneratorAgent()
    
    success = interview_agent.build_interview_knowledge_base(sample_knowledge_path)
    if success:
        print("✓ Interview knowledge base built successfully!")
        
        # Test interview knowledge queries
        interview_queries = [
            "Python technical interview questions",
            "Django framework questions",
            "Behavioral interview questions about leadership"
        ]
        
        for query in interview_queries:
            print(f"\n   Query: {query}")
            results = interview_agent.query_interview_knowledge(query, top_k=2)
            for i, result in enumerate(results, 1):
                print(f"   Result {i}: {result['text'][:100]}...")
        
        # Test question generation
        print("\n3. Testing Interview Question Generation...")
        job_desc = "Senior Python Developer with Django experience"
        cv_content = sample_cv
        
        questions = interview_agent.generate_interview_questions(
            job_desc, cv_content, ['technical', 'behavioral']
        )
        
        for q_type, q_list in questions.items():
            print(f"\n   {q_type.title()} Questions:")
            for i, question in enumerate(q_list, 1):
                print(f"   {i}. {question}")
    
    # Test standalone functions
    print("\n4. Testing standalone functions...")
    print("   Testing build_cv_index_enhanced...")
    success = build_cv_index_enhanced(sample_cv_path)
    print(f"   Result: {success}")
    
    print("   Testing query_cv_index_enhanced...")
    results = query_cv_index_enhanced("What skills does John have?", top_k=2)
    print(f"   Found {len(results)} results")
    
    # Cleanup
    print(f"\n5. Cleaning up sample files...")
    for file_path in [sample_cv_path, sample_knowledge_path]:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"   Removed {file_path}")
    
    print("\n=== Enhanced RAG Pipeline Test Completed! ===")
