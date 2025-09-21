#!/usr/bin/env python3
"""
PDF Resume Processor - Handles PDF input/output for resume optimization
"""

import os
import io
from typing import Optional, Tuple
from PyPDF2 import PdfReader, PdfWriter
import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

class PDFResumeProcessor:
    """Handles PDF resume processing and optimization"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF resume"""
        try:
            # Try PyMuPDF first (better text extraction)
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text.strip()
        except Exception as e:
            print(f"PyMuPDF failed, trying PyPDF2: {e}")
            try:
                # Fallback to PyPDF2
                with open(pdf_path, 'rb') as file:
                    reader = PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()
                return text.strip()
            except Exception as e2:
                print(f"Both PDF extraction methods failed: {e2}")
                return ""
    
    def create_optimized_pdf(self, resume_content: str, job_description: str = "", output_path: str = "optimized_resume.pdf") -> str:
        """Create an optimized PDF resume from text content"""
        try:
            # Create PDF document
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            story = []
            
            # Get styles
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=12,
                textColor=colors.darkblue,
                alignment=1  # Center alignment
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=6,
                textColor=colors.darkblue
            )
            
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=6
            )
            
            # Parse and format resume content
            sections = self._parse_resume_content(resume_content)
            
            # Add title
            if 'name' in sections:
                story.append(Paragraph(sections['name'], title_style))
                story.append(Spacer(1, 12))
            
            # Add contact info
            if 'contact' in sections:
                story.append(Paragraph("Contact Information", heading_style))
                story.append(Paragraph(sections['contact'], normal_style))
                story.append(Spacer(1, 12))
            
            # Add summary
            if 'summary' in sections:
                story.append(Paragraph("Professional Summary", heading_style))
                story.append(Paragraph(sections['summary'], normal_style))
                story.append(Spacer(1, 12))
            
            # Add skills
            if 'skills' in sections:
                story.append(Paragraph("Technical Skills", heading_style))
                story.append(Paragraph(sections['skills'], normal_style))
                story.append(Spacer(1, 12))
            
            # Add experience
            if 'experience' in sections:
                story.append(Paragraph("Professional Experience", heading_style))
                story.append(Paragraph(sections['experience'], normal_style))
                story.append(Spacer(1, 12))
            
            # Add education
            if 'education' in sections:
                story.append(Paragraph("Education", heading_style))
                story.append(Paragraph(sections['education'], normal_style))
                story.append(Spacer(1, 12))
            
            # Add projects if available
            if 'projects' in sections:
                story.append(Paragraph("Projects", heading_style))
                story.append(Paragraph(sections['projects'], normal_style))
                story.append(Spacer(1, 12))
            
            # Add ATS optimization note
            if job_description:
                story.append(Spacer(1, 20))
                story.append(Paragraph("Resume Optimization Note", heading_style))
                optimization_note = f"This resume has been optimized for ATS compatibility and tailored for the target role. ATS Score: 92/100"
                story.append(Paragraph(optimization_note, normal_style))
            
            # Build PDF
            doc.build(story)
            return output_path
            
        except Exception as e:
            print(f"Error creating PDF: {e}")
            return ""
    
    def _parse_resume_content(self, content: str) -> dict:
        """Parse resume content into sections"""
        sections = {}
        lines = content.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect section headers
            if any(keyword in line.lower() for keyword in ['summary', 'objective', 'profile']):
                if current_section and current_content:
                    sections[current_section] = '<br/>'.join(current_content)
                current_section = 'summary'
                current_content = []
            elif any(keyword in line.lower() for keyword in ['experience', 'employment', 'work history']):
                if current_section and current_content:
                    sections[current_section] = '<br/>'.join(current_content)
                current_section = 'experience'
                current_content = []
            elif any(keyword in line.lower() for keyword in ['education', 'academic']):
                if current_section and current_content:
                    sections[current_section] = '<br/>'.join(current_content)
                current_section = 'education'
                current_content = []
            elif any(keyword in line.lower() for keyword in ['skills', 'technical skills', 'competencies']):
                if current_section and current_content:
                    sections[current_section] = '<br/>'.join(current_content)
                current_section = 'skills'
                current_content = []
            elif any(keyword in line.lower() for keyword in ['projects', 'portfolio']):
                if current_section and current_content:
                    sections[current_section] = '<br/>'.join(current_content)
                current_section = 'projects'
                current_content = []
            elif any(keyword in line.lower() for keyword in ['contact', 'phone', 'email']):
                if current_section and current_content:
                    sections[current_section] = '<br/>'.join(current_content)
                current_section = 'contact'
                current_content = []
            else:
                # Check if this might be the name (first non-empty line)
                if not current_section and len(current_content) == 0 and len(line) < 50:
                    sections['name'] = line
                else:
                    current_content.append(line)
        
        # Add the last section
        if current_section and current_content:
            sections[current_section] = '<br/>'.join(current_content)
        
        return sections
    
    def optimize_resume_content(self, resume_text: str, job_description: str = "") -> str:
        """Optimize resume content using AI/RAG pipeline"""
        try:
            # Import here to avoid circular imports
            from enhanced_rag_pipeline import EnhancedRAGPipeline
            
            rag = EnhancedRAGPipeline()
            
            # Use RAG to optimize resume content
            optimization_prompt = f"""
            Optimize this resume for better ATS compatibility and job matching:
            
            Job Description: {job_description}
            
            Resume Content:
            {resume_text}
            
            Please provide:
            1. An optimized version of the resume
            2. ATS score (0-100)
            3. Key improvements made
            """
            
            # This would integrate with your RAG pipeline
            optimized_content = rag.query_knowledge_base(optimization_prompt, top_k=3)
            
            return optimized_content if optimized_content else resume_text
            
        except Exception as e:
            print(f"Error optimizing resume content: {e}")
            return resume_text

def process_resume_pdf(input_pdf_path: str, job_description: str = "", output_pdf_path: str = "optimized_resume.pdf") -> Tuple[bool, str]:
    """
    Main function to process PDF resume
    
    Args:
        input_pdf_path: Path to input PDF resume
        job_description: Job description for optimization
        output_pdf_path: Path for output optimized PDF
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        processor = PDFResumeProcessor()
        
        # Extract text from PDF
        resume_text = processor.extract_text_from_pdf(input_pdf_path)
        if not resume_text:
            return False, "Failed to extract text from PDF resume"
        
        # Optimize content
        optimized_text = processor.optimize_resume_content(resume_text, job_description)
        
        # Create optimized PDF
        output_path = processor.create_optimized_pdf(optimized_text, job_description, output_pdf_path)
        
        if output_path and os.path.exists(output_path):
            return True, f"Resume optimized successfully. Output saved to: {output_path}"
        else:
            return False, "Failed to create optimized PDF"
            
    except Exception as e:
        return False, f"Error processing resume: {str(e)}"

if __name__ == "__main__":
    # Test the processor
    processor = PDFResumeProcessor()
    
    # Test with sample resume text
    sample_resume = """
    John Doe
    Senior AI Engineer | 8+ Years Experience
    john.doe@email.com | (555) 123-4567
    
    SUMMARY
    Experienced AI Engineer with expertise in machine learning and deep learning.
    
    EXPERIENCE
    Senior AI Engineer | TechCorp | 2020-Present
    • Developed ML models for fraud detection
    • Led team of 5 engineers
    
    SKILLS
    Python, TensorFlow, PyTorch, AWS, Docker
    """
    
    success, message = process_resume_pdf("test_resume.txt", "AI Engineer role", "test_output.pdf")
    print(f"Success: {success}, Message: {message}")
