"""
CV RAG Pipeline for CareerPilot
Implements CV indexing and querying using FAISS and sentence transformers
"""

import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Tuple, Optional
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CVRAGPipeline:
    """
    RAG pipeline for CV processing and querying
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the RAG pipeline
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.model_name = model_name
        self.model = None
        self.index = None
        self.documents = []
        self.index_path = "cv_index.faiss"
        self.documents_path = "cv_documents.pkl"
        
    def _load_model(self):
        """Load the sentence transformer model"""
        if self.model is None:
            logger.info(f"Loading sentence transformer model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info("Model loaded successfully")
    
    def _extract_text_from_file(self, file_path: str) -> str:
        """
        Extract text from various file formats
        
        Args:
            file_path: Path to the CV file
            
        Returns:
            Extracted text content
        """
        file_path = Path(file_path)
        text = ""
        
        try:
            if file_path.suffix.lower() == '.pdf':
                import PyPDF2
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                        
            elif file_path.suffix.lower() in ['.doc', '.docx']:
                from docx import Document
                doc = Document(file_path)
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                    
            elif file_path.suffix.lower() == '.txt':
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    
            else:
                logger.warning(f"Unsupported file format: {file_path.suffix}")
                return ""
                
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {str(e)}")
            return ""
            
        return text.strip()
    
    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Input text to chunk
            chunk_size: Size of each chunk
            overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        if not text:
            return []
            
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk.strip())
                
        return chunks
    
    def build_cv_index(self, cv_path: str) -> bool:
        """
        Build FAISS index from CV document
        
        Args:
            cv_path: Path to the CV file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Building CV index from: {cv_path}")
            
            # Extract text from CV
            text = self._extract_text_from_file(cv_path)
            if not text:
                logger.error("No text extracted from CV")
                return False
            
            # Chunk the text
            chunks = self._chunk_text(text)
            if not chunks:
                logger.error("No text chunks created")
                return False
            
            logger.info(f"Created {len(chunks)} text chunks")
            
            # Load model
            self._load_model()
            
            # Generate embeddings
            logger.info("Generating embeddings...")
            embeddings = self.model.encode(chunks, show_progress_bar=True)
            
            # Create FAISS index
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings)
            
            # Add embeddings to index
            self.index.add(embeddings.astype('float32'))
            
            # Store documents
            self.documents = chunks
            
            # Save index and documents
            self._save_index()
            
            logger.info(f"Successfully built index with {self.index.ntotal} vectors")
            return True
            
        except Exception as e:
            logger.error(f"Error building CV index: {str(e)}")
            return False
    
    def _save_index(self):
        """Save the FAISS index and documents to disk"""
        try:
            # Save FAISS index
            faiss.write_index(self.index, self.index_path)
            
            # Save documents
            with open(self.documents_path, 'wb') as f:
                pickle.dump(self.documents, f)
                
            logger.info("Index and documents saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving index: {str(e)}")
    
    def _load_index(self) -> bool:
        """Load the FAISS index and documents from disk"""
        try:
            if not os.path.exists(self.index_path) or not os.path.exists(self.documents_path):
                return False
                
            # Load FAISS index
            self.index = faiss.read_index(self.index_path)
            
            # Load documents
            with open(self.documents_path, 'rb') as f:
                self.documents = pickle.load(f)
                
            logger.info(f"Loaded index with {self.index.ntotal} vectors")
            return True
            
        except Exception as e:
            logger.error(f"Error loading index: {str(e)}")
            return False
    
    def query_cv_index(self, query: str, top_k: int = 5) -> List[Dict[str, any]]:
        """
        Query the CV index for relevant information
        
        Args:
            query: Query string
            top_k: Number of top results to return
            
        Returns:
            List of dictionaries containing relevant chunks and scores
        """
        try:
            # Load model if not already loaded
            self._load_model()
            
            # Load index if not already loaded
            if self.index is None:
                if not self._load_index():
                    logger.error("No index found. Please build the index first.")
                    return []
            
            # Generate query embedding
            query_embedding = self.model.encode([query])
            faiss.normalize_L2(query_embedding)
            
            # Search the index
            scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
            
            # Prepare results
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.documents):
                    results.append({
                        'text': self.documents[idx],
                        'score': float(score),
                        'index': int(idx)
                    })
            
            logger.info(f"Found {len(results)} relevant chunks for query: '{query}'")
            return results
            
        except Exception as e:
            logger.error(f"Error querying CV index: {str(e)}")
            return []
    
    def get_cv_summary(self) -> Dict[str, any]:
        """
        Get a summary of the indexed CV
        
        Returns:
            Dictionary containing CV summary information
        """
        if not self.documents:
            if not self._load_index():
                return {"error": "No CV index found"}
        
        # Basic statistics
        total_chunks = len(self.documents)
        total_words = sum(len(doc.split()) for doc in self.documents)
        
        # Extract key sections (simple keyword-based)
        sections = {
            'experience': [],
            'education': [],
            'skills': [],
            'projects': []
        }
        
        keywords = {
            'experience': ['experience', 'work', 'employment', 'job', 'position', 'career'],
            'education': ['education', 'degree', 'university', 'college', 'school', 'graduated'],
            'skills': ['skills', 'technologies', 'programming', 'languages', 'tools', 'expertise'],
            'projects': ['project', 'portfolio', 'developed', 'built', 'created', 'implemented']
        }
        
        for doc in self.documents:
            doc_lower = doc.lower()
            for section, section_keywords in keywords.items():
                if any(keyword in doc_lower for keyword in section_keywords):
                    sections[section].append(doc)
        
        return {
            'total_chunks': total_chunks,
            'total_words': total_words,
            'sections': {k: len(v) for k, v in sections.items()},
            'sample_text': self.documents[0] if self.documents else ""
        }


def build_cv_index(cv_path: str) -> bool:
    """
    Standalone function to build CV index
    
    Args:
        cv_path: Path to the CV file
        
    Returns:
        True if successful, False otherwise
    """
    pipeline = CVRAGPipeline()
    return pipeline.build_cv_index(cv_path)


def query_cv_index(query: str, top_k: int = 5) -> List[Dict[str, any]]:
    """
    Standalone function to query CV index
    
    Args:
        query: Query string
        top_k: Number of top results to return
        
    Returns:
        List of relevant CV chunks
    """
    pipeline = CVRAGPipeline()
    return pipeline.query_cv_index(query, top_k)


if __name__ == "__main__":
    """
    Test the RAG pipeline with sample data
    """
    print("=== CareerPilot CV RAG Pipeline Test ===\n")
    
    # Create a sample CV text file for testing
    sample_cv = """
    John Doe
    Software Engineer
    
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
    
    PROJECTS:
    E-commerce Platform (2023)
    - Built a full-stack e-commerce platform
    - Used Django for backend and React for frontend
    - Implemented payment integration with Stripe
    
    Task Management App (2022)
    - Developed a collaborative task management application
    - Real-time updates using WebSockets
    - Mobile-responsive design
    """
    
    # Create sample CV file
    sample_cv_path = "sample_cv.txt"
    with open(sample_cv_path, 'w', encoding='utf-8') as f:
        f.write(sample_cv)
    
    print(f"Created sample CV: {sample_cv_path}")
    
    # Test the pipeline
    pipeline = CVRAGPipeline()
    
    # Build index
    print("\n1. Building CV index...")
    success = pipeline.build_cv_index(sample_cv_path)
    if success:
        print("✓ Index built successfully!")
    else:
        print("✗ Failed to build index")
        exit(1)
    
    # Get CV summary
    print("\n2. CV Summary:")
    summary = pipeline.get_cv_summary()
    print(f"   Total chunks: {summary['total_chunks']}")
    print(f"   Total words: {summary['total_words']}")
    print(f"   Sections found: {summary['sections']}")
    
    # Test queries
    test_queries = [
        "What programming languages does John know?",
        "Tell me about John's work experience",
        "What projects has John worked on?",
        "What is John's educational background?",
        "What tools and technologies does John use?"
    ]
    
    print("\n3. Testing queries:")
    for i, query in enumerate(test_queries, 1):
        print(f"\n   Query {i}: {query}")
        results = pipeline.query_cv_index(query, top_k=3)
        
        for j, result in enumerate(results, 1):
            print(f"   Result {j} (score: {result['score']:.3f}):")
            print(f"   {result['text'][:150]}...")
    
    # Test standalone functions
    print("\n4. Testing standalone functions:")
    print("   Testing build_cv_index function...")
    success = build_cv_index(sample_cv_path)
    print(f"   build_cv_index result: {success}")
    
    print("   Testing query_cv_index function...")
    results = query_cv_index("What is John's current position?", top_k=2)
    print(f"   query_cv_index found {len(results)} results")
    
    # Cleanup
    print(f"\n5. Cleaning up sample file...")
    if os.path.exists(sample_cv_path):
        os.remove(sample_cv_path)
        print("   Sample CV file removed")
    
    print("\n=== Test completed successfully! ===")
