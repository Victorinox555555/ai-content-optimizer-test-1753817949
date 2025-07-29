
import requests
import os
from typing import Dict, List, Any
import json
from datetime import datetime

class OpenAIDigestProcessor:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        self.base_url = 'https://api.openai.com/v1'
    
    def create_real_time_digest(self, content_sources: List[str], digest_type: str = 'summary') -> Dict[str, Any]:
        """Create real-time content digest"""
        processed_content = []
        
        for source in content_sources:
            digest = self.process_content(source, digest_type)
            if digest:
                processed_content.append({
                    'source': source[:100] + "..." if len(source) > 100 else source,
                    'digest': digest,
                    'timestamp': datetime.now().isoformat(),
                    'type': digest_type
                })
        
        return {
            'digests': processed_content,
            'total_processed': len(processed_content),
            'processing_time': datetime.now().isoformat(),
            'pricing': f"${len(processed_content) * 0.05:.2f}"
        }
    
    def process_content(self, content: str, digest_type: str) -> str:
        """Process content using OpenAI"""
        if digest_type == 'summary':
            prompt = f"Provide a concise summary of this content in 2-3 sentences:\n\n{content}"
        elif digest_type == 'key_points':
            prompt = f"Extract 3-5 key points from this content:\n\n{content}"
        elif digest_type == 'sentiment':
            prompt = f"Analyze the sentiment of this content (positive/negative/neutral) and explain why:\n\n{content}"
        else:
            prompt = f"Analyze this content:\n\n{content}"
        
        try:
            response = requests.post(
                f'{self.base_url}/chat/completions',
                headers=self.headers,
                json={
                    'model': 'gpt-3.5-turbo',
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': 200,
                    'temperature': 0.3
                }
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f"Processing error: {str(e)}"
        
        return "Unable to process content"
    
    def batch_process(self, content_list: List[str], digest_type: str = 'summary') -> Dict[str, Any]:
        """Process multiple content pieces in batch"""
        results = []
        total_cost = 0
        
        for i, content in enumerate(content_list):
            digest = self.process_content(content, digest_type)
            results.append({
                'id': i + 1,
                'digest': digest,
                'cost': 0.05
            })
            total_cost += 0.05
        
        return {
            'batch_results': results,
            'total_items': len(results),
            'total_cost': f"${total_cost:.2f}",
            'average_cost_per_item': "$0.05"
        }

if __name__ == "__main__":
    processor = OpenAIDigestProcessor()
    print("OpenAI real-time digest processor initialized")
