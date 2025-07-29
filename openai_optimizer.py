
import openai
import os
from typing import List, Dict, Any, Optional

class OpenAIContentOptimizer:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
    
    def optimize_content(self, content: str, target_audience: str = "general") -> Dict[str, Any]:
        """Optimize content for engagement using GPT"""
        if not self.api_key:
            return {"error": "OpenAI API key not configured", "original": content}
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a content optimization expert. Optimize content for {target_audience} audience to maximize engagement."},
                    {"role": "user", "content": f"Optimize this content: {content}"}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            optimized_content = response.choices[0].message.content
            
            return {
                "original": content,
                "optimized": optimized_content,
                "improvements": self._analyze_improvements(content, optimized_content),
                "engagement_score": self._calculate_engagement_score(optimized_content)
            }
        except Exception as e:
            return {"error": str(e), "original": content}
    
    def _analyze_improvements(self, original: str, optimized: str) -> List[str]:
        """Analyze what improvements were made"""
        improvements = []
        if len(optimized) > len(original):
            improvements.append("Enhanced detail and clarity")
        if "?" in optimized and "?" not in original:
            improvements.append("Added engaging questions")
        if any(word in optimized.lower() for word in ["you", "your"]) and not any(word in original.lower() for word in ["you", "your"]):
            improvements.append("Improved personal connection")
        return improvements
    
    def _calculate_engagement_score(self, content: str) -> int:
        """Calculate predicted engagement score"""
        score = 50  # Base score
        
        if len(content.split()) > 50:
            score += 10
        if "?" in content:
            score += 15
        if any(word in content.lower() for word in ["you", "your", "we", "us"]):
            score += 20
        if any(word in content.lower() for word in ["amazing", "incredible", "powerful", "transform"]):
            score += 10
        
        return min(100, score)

if __name__ == "__main__":
    optimizer = OpenAIContentOptimizer()
    result = optimizer.optimize_content("This is a basic product description.")
    print(f"Engagement Score: {result.get('engagement_score', 0)}")
