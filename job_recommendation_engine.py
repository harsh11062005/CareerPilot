#!/usr/bin/env python3
"""
RAG-based Job Recommendation Engine
Uses semantic search and knowledge base for intelligent job matching
"""

import os
import json
from typing import List, Dict, Any
from dataclasses import dataclass
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle

@dataclass
class JobRecommendation:
    """Data class for job recommendations"""
    title: str
    company: str
    location: str
    salary_range: str
    description: str
    requirements: List[str]
    match_score: float
    reasoning: str
    skills_match: List[str]
    growth_potential: str
    industry_trend: str

class JobRecommendationEngine:
    """RAG-based job recommendation system"""
    
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.job_database = []
        self.vector_index = None
        self.index_file = "job_vector_index.pkl"
        self.job_db_file = "job_database.json"
        
        # Load or create job database
        self._load_job_database()
        self._build_vector_index()
    
    def _load_job_database(self):
        """Load job database from file or create sample data"""
        if os.path.exists(self.job_db_file):
            try:
                with open(self.job_db_file, 'r') as f:
                    self.job_database = json.load(f)
                print(f"Loaded {len(self.job_database)} jobs from database")
            except Exception as e:
                print(f"Error loading job database: {e}")
                self._create_sample_job_database()
        else:
            self._create_sample_job_database()
    
    def _create_sample_job_database(self):
        """Create a comprehensive sample job database"""
        self.job_database = [
            {
                "id": 1,
                "title": "Senior AI/ML Engineer",
                "company": "TechCorp",
                "location": "San Francisco, CA",
                "salary_range": "$150,000 - $200,000",
                "description": "Lead the development of cutting-edge AI/ML solutions for enterprise clients. Work with large-scale data processing and deep learning models.",
                "requirements": [
                    "5+ years Python experience",
                    "Deep learning frameworks (TensorFlow, PyTorch)",
                    "Cloud platforms (AWS, GCP, Azure)",
                    "Machine learning algorithms",
                    "Team leadership experience"
                ],
                "skills": ["python", "tensorflow", "pytorch", "aws", "machine learning", "deep learning", "team leadership"],
                "industry": "Technology",
                "experience_level": "Senior",
                "growth_potential": "High - AI/ML field expanding rapidly",
                "industry_trend": "Growing demand for AI specialists"
            },
            {
                "id": 2,
                "title": "Data Scientist",
                "company": "DataFlow Inc",
                "location": "New York, NY",
                "salary_range": "$120,000 - $160,000",
                "description": "Analyze complex datasets to drive business decisions. Build predictive models and statistical analyses.",
                "requirements": [
                    "3+ years data science experience",
                    "Python, R, SQL proficiency",
                    "Statistical modeling",
                    "Data visualization tools",
                    "Business acumen"
                ],
                "skills": ["python", "r", "sql", "statistics", "data analysis", "machine learning", "business intelligence"],
                "industry": "Technology",
                "experience_level": "Mid",
                "growth_potential": "High - Data-driven decisions crucial",
                "industry_trend": "Increasing demand for data insights"
            },
            {
                "id": 3,
                "title": "Full Stack Developer",
                "company": "WebSolutions",
                "location": "Austin, TX",
                "salary_range": "$90,000 - $130,000",
                "description": "Develop end-to-end web applications using modern frameworks and cloud technologies.",
                "requirements": [
                    "3+ years full-stack development",
                    "JavaScript, React, Node.js",
                    "Database design (SQL, NoSQL)",
                    "Cloud deployment experience",
                    "Agile methodology"
                ],
                "skills": ["javascript", "react", "nodejs", "sql", "nosql", "cloud", "web development"],
                "industry": "Technology",
                "experience_level": "Mid",
                "growth_potential": "Medium - Stable web development market",
                "industry_trend": "Consistent demand for web developers"
            },
            {
                "id": 4,
                "title": "DevOps Engineer",
                "company": "CloudScale",
                "location": "Seattle, WA",
                "salary_range": "$110,000 - $150,000",
                "description": "Design and maintain scalable cloud infrastructure. Implement CI/CD pipelines and monitoring systems.",
                "requirements": [
                    "4+ years DevOps experience",
                    "Docker, Kubernetes expertise",
                    "Cloud platforms (AWS, Azure)",
                    "Infrastructure as Code",
                    "Monitoring and logging"
                ],
                "skills": ["docker", "kubernetes", "aws", "azure", "terraform", "ci/cd", "monitoring"],
                "industry": "Technology",
                "experience_level": "Senior",
                "growth_potential": "High - Cloud adoption accelerating",
                "industry_trend": "Critical for digital transformation"
            },
            {
                "id": 5,
                "title": "Product Manager",
                "company": "InnovateCorp",
                "location": "Boston, MA",
                "salary_range": "$100,000 - $140,000",
                "description": "Lead product strategy and development. Work with cross-functional teams to deliver customer-focused solutions.",
                "requirements": [
                    "3+ years product management",
                    "Technical background preferred",
                    "Analytics and data-driven decisions",
                    "Cross-functional leadership",
                    "Market research skills"
                ],
                "skills": ["product management", "analytics", "leadership", "market research", "strategy", "technical background"],
                "industry": "Technology",
                "experience_level": "Mid",
                "growth_potential": "Medium - Steady product management demand",
                "industry_trend": "Focus on customer-centric products"
            },
            {
                "id": 6,
                "title": "Cybersecurity Analyst",
                "company": "SecureTech",
                "location": "Denver, CO",
                "salary_range": "$95,000 - $135,000",
                "description": "Protect organizational assets from cyber threats. Monitor security systems and respond to incidents.",
                "requirements": [
                    "2+ years cybersecurity experience",
                    "Security tools and frameworks",
                    "Incident response procedures",
                    "Risk assessment skills",
                    "Certifications (CISSP, CISM preferred)"
                ],
                "skills": ["cybersecurity", "incident response", "risk assessment", "security tools", "compliance", "network security"],
                "industry": "Technology",
                "experience_level": "Mid",
                "growth_potential": "Very High - Cybersecurity threats increasing",
                "industry_trend": "Critical for all organizations"
            }
        ]
        
        # Save to file
        with open(self.job_db_file, 'w') as f:
            json.dump(self.job_database, f, indent=2)
        print(f"Created sample job database with {len(self.job_database)} jobs")
    
    def _build_vector_index(self):
        """Build FAISS vector index for semantic search"""
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, 'rb') as f:
                    self.vector_index = pickle.load(f)
                print("Loaded existing vector index")
                return
            except Exception as e:
                print(f"Error loading vector index: {e}")
        
        # Create job embeddings
        job_texts = []
        for job in self.job_database:
            # Combine relevant job information for embedding
            job_text = f"""
            Title: {job['title']}
            Company: {job['company']}
            Description: {job['description']}
            Requirements: {' '.join(job['requirements'])}
            Skills: {' '.join(job['skills'])}
            Industry: {job['industry']}
            Experience Level: {job['experience_level']}
            """
            job_texts.append(job_text)
        
        # Generate embeddings
        embeddings = self.model.encode(job_texts)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.vector_index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        self.vector_index.add(embeddings)
        
        # Save index
        with open(self.index_file, 'wb') as f:
            pickle.dump(self.vector_index, f)
        
        print(f"Built vector index with {len(job_texts)} job embeddings")
    
    def _calculate_skill_match(self, user_skills: List[str], job_skills: List[str]) -> tuple[float, List[str]]:
        """Calculate skill matching score and matched skills"""
        user_skills_lower = [skill.lower() for skill in user_skills]
        job_skills_lower = [skill.lower() for skill in job_skills]
        
        matched_skills = []
        for job_skill in job_skills_lower:
            if any(user_skill in job_skill or job_skill in user_skill for user_skill in user_skills_lower):
                matched_skills.append(job_skill)
        
        match_score = len(matched_skills) / len(job_skills_lower) if job_skills_lower else 0
        return match_score, matched_skills
    
    def recommend_jobs(self, user_profile: str, user_skills: List[str] = None, num_recommendations: int = 5) -> List[JobRecommendation]:
        """
        Generate job recommendations using RAG approach
        
        Args:
            user_profile: User's career interests and background
            user_skills: List of user's technical skills
            num_recommendations: Number of recommendations to return
        
        Returns:
            List of JobRecommendation objects
        """
        if not user_skills:
            user_skills = []
        
        # Create user profile embedding
        user_embedding = self.model.encode([user_profile])
        faiss.normalize_L2(user_embedding)
        
        # Search for similar jobs
        scores, indices = self.vector_index.search(user_embedding, min(num_recommendations * 2, len(self.job_database)))
        
        recommendations = []
        for score, idx in zip(scores[0], indices[0]):
            if idx >= len(self.job_database):
                continue
                
            job = self.job_database[idx]
            
            # Calculate skill match
            skill_match_score, matched_skills = self._calculate_skill_match(user_skills, job['skills'])
            
            # Generate reasoning for recommendation
            reasoning = self._generate_recommendation_reasoning(user_profile, job, skill_match_score, matched_skills)
            
            # Create recommendation object
            recommendation = JobRecommendation(
                title=job['title'],
                company=job['company'],
                location=job['location'],
                salary_range=job['salary_range'],
                description=job['description'],
                requirements=job['requirements'],
                match_score=float(score),
                reasoning=reasoning,
                skills_match=matched_skills,
                growth_potential=job['growth_potential'],
                industry_trend=job['industry_trend']
            )
            
            recommendations.append(recommendation)
        
        # Sort by combined score (semantic + skill match)
        recommendations.sort(key=lambda x: (x.match_score + len(x.skills_match) * 0.1), reverse=True)
        
        return recommendations[:num_recommendations]
    
    def _generate_recommendation_reasoning(self, user_profile: str, job: Dict, skill_match_score: float, matched_skills: List[str]) -> str:
        """Generate reasoning for why this job is recommended"""
        reasoning_parts = []
        
        # Add semantic similarity reasoning
        if "ai" in user_profile.lower() or "machine learning" in user_profile.lower():
            if "ai" in job['title'].lower() or "ml" in job['title'].lower() or "data" in job['title'].lower():
                reasoning_parts.append("Your interest in AI/ML aligns with this role's focus")
        
        if "software" in user_profile.lower() or "development" in user_profile.lower():
            if "developer" in job['title'].lower() or "engineer" in job['title'].lower():
                reasoning_parts.append("Your development background matches this technical role")
        
        # Add skill match reasoning
        if skill_match_score > 0.5:
            reasoning_parts.append(f"Strong skill alignment: {', '.join(matched_skills[:3])}")
        elif skill_match_score > 0.2:
            reasoning_parts.append(f"Some relevant skills: {', '.join(matched_skills[:2])}")
        
        # Add growth potential reasoning
        if "high" in job['growth_potential'].lower():
            reasoning_parts.append("High growth potential in this field")
        
        # Add industry trend reasoning
        reasoning_parts.append(f"Industry trend: {job['industry_trend']}")
        
        return ". ".join(reasoning_parts) + "."
    
    def get_job_market_insights(self, user_profile: str) -> Dict[str, Any]:
        """Get market insights relevant to user profile"""
        recommendations = self.recommend_jobs(user_profile, num_recommendations=10)
        
        # Analyze salary ranges
        salaries = []
        industries = []
        locations = []
        
        for rec in recommendations:
            # Parse salary (simple extraction)
            salary_text = rec.salary_range
            if "$" in salary_text:
                try:
                    # Extract numbers and average them
                    import re
                    numbers = re.findall(r'\d+', salary_text)
                    if len(numbers) >= 2:
                        avg_salary = (int(numbers[0]) + int(numbers[1])) / 2
                        salaries.append(avg_salary)
                except:
                    pass
            
            industries.append(rec.company)  # Using company as proxy for industry
            locations.append(rec.location)
        
        insights = {
            "average_salary": np.mean(salaries) if salaries else 0,
            "salary_range": f"${min(salaries):,.0f} - ${max(salaries):,.0f}" if salaries else "N/A",
            "top_locations": list(set(locations))[:3],
            "market_demand": "High" if len(recommendations) > 5 else "Medium",
            "growth_opportunities": len([r for r in recommendations if "high" in r.growth_potential.lower()])
        }
        
        return insights

def get_intelligent_job_recommendations(user_profile: str, user_skills: List[str] = None) -> List[Dict]:
    """
    Main function to get intelligent job recommendations using RAG
    
    Args:
        user_profile: User's career interests and background
        user_skills: List of user's skills
    
    Returns:
        List of job recommendation dictionaries
    """
    try:
        engine = JobRecommendationEngine()
        recommendations = engine.recommend_jobs(user_profile, user_skills)
        
        # Convert to dictionary format for API response
        result = []
        for rec in recommendations:
            result.append({
                "title": rec.title,
                "company": rec.company,
                "location": rec.location,
                "salary_range": rec.salary_range,
                "description": rec.description,
                "requirements": rec.requirements,
                "match_score": round(rec.match_score * 100, 1),  # Convert to percentage
                "reasoning": rec.reasoning,
                "skills_match": rec.skills_match,
                "growth_potential": rec.growth_potential,
                "industry_trend": rec.industry_trend,
                "ats_compatibility": "High" if rec.match_score > 0.7 else "Medium"
            })
        
        return result
        
    except Exception as e:
        print(f"Error getting job recommendations: {e}")
        return []

if __name__ == "__main__":
    # Test the recommendation engine
    engine = JobRecommendationEngine()
    
    # Test with sample user profile
    user_profile = "I'm interested in AI and machine learning. I have experience with Python, TensorFlow, and cloud platforms. I want to work on cutting-edge AI solutions."
    user_skills = ["python", "tensorflow", "aws", "machine learning", "deep learning"]
    
    recommendations = engine.recommend_jobs(user_profile, user_skills)
    
    print("Job Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec.title} at {rec.company}")
        print(f"   Match Score: {rec.match_score:.2f}")
        print(f"   Reasoning: {rec.reasoning}")
        print(f"   Skills Match: {rec.skills_match}")
