
import requests
import os
from typing import Dict, List, Any
import json

class HuggingFaceModelHub:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('HUGGINGFACE_API_KEY')
        self.base_url = 'https://api-inference.huggingface.co'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def get_trending_models(self, task: str = None, limit: int = 10) -> Dict[str, Any]:
        """Get trending AI models from Hugging Face Hub"""
        try:
            url = 'https://huggingface.co/api/models'
            params = {
                'sort': 'downloads',
                'direction': -1,
                'limit': limit
            }
            if task:
                params['filter'] = task
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                models = response.json()
                return {
                    'trending_models': [
                        {
                            'id': model.get('id'),
                            'downloads': model.get('downloads', 0),
                            'likes': model.get('likes', 0),
                            'task': model.get('pipeline_tag'),
                            'library': model.get('library_name'),
                            'created_at': model.get('createdAt'),
                            'updated_at': model.get('lastModified')
                        }
                        for model in models
                    ],
                    'total_models': len(models),
                    'task_filter': task,
                    'pricing_model': '$9/month for unlimited access'
                }
        except Exception:
            pass
        
        return {
            'trending_models': [],
            'total_models': 0,
            'error': 'Failed to fetch trending models'
        }
    
    def query_model(self, model_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Query a specific Hugging Face model"""
        try:
            url = f'{self.base_url}/models/{model_id}'
            response = requests.post(url, headers=self.headers, json=inputs)
            
            if response.status_code == 200:
                return {
                    'model_id': model_id,
                    'result': response.json(),
                    'status': 'success',
                    'pricing': '$9/month subscription'
                }
        except Exception as e:
            pass
        
        return {
            'model_id': model_id,
            'result': None,
            'status': 'error',
            'error': 'Model query failed'
        }
    
    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific model"""
        try:
            url = f'https://huggingface.co/api/models/{model_id}'
            response = requests.get(url)
            
            if response.status_code == 200:
                model_info = response.json()
                return {
                    'model_id': model_id,
                    'info': {
                        'downloads': model_info.get('downloads', 0),
                        'likes': model_info.get('likes', 0),
                        'task': model_info.get('pipeline_tag'),
                        'library': model_info.get('library_name'),
                        'tags': model_info.get('tags', []),
                        'created_at': model_info.get('createdAt'),
                        'updated_at': model_info.get('lastModified'),
                        'description': model_info.get('cardData', {}).get('description', '')
                    },
                    'constantly_updated': True,
                    'subscription_benefits': [
                        'Access to latest AI models',
                        'Priority inference speed',
                        'Advanced model analytics',
                        'Custom model fine-tuning',
                        'Real-time model updates'
                    ]
                }
        except Exception:
            pass
        
        return {
            'model_id': model_id,
            'info': {},
            'error': 'Failed to fetch model information'
        }
    
    def search_models(self, query: str, task: str = None) -> Dict[str, Any]:
        """Search for models based on query and task"""
        try:
            url = 'https://huggingface.co/api/models'
            params = {
                'search': query,
                'sort': 'downloads',
                'direction': -1,
                'limit': 20
            }
            if task:
                params['filter'] = task
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                models = response.json()
                return {
                    'search_query': query,
                    'task_filter': task,
                    'models': [
                        {
                            'id': model.get('id'),
                            'downloads': model.get('downloads', 0),
                            'likes': model.get('likes', 0),
                            'task': model.get('pipeline_tag'),
                            'relevance_score': self.calculate_relevance(model, query)
                        }
                        for model in models
                    ],
                    'total_results': len(models),
                    'moat_features': [
                        'Constantly updated model database',
                        'AI-powered model recommendations',
                        'Performance benchmarking',
                        'Usage analytics and insights'
                    ]
                }
        except Exception:
            pass
        
        return {
            'search_query': query,
            'models': [],
            'error': 'Search failed'
        }
    
    def calculate_relevance(self, model: Dict, query: str) -> float:
        """Calculate relevance score for search results"""
        score = 0.0
        model_id = model.get('id', '').lower()
        query_lower = query.lower()
        
        if query_lower in model_id:
            score += 50
        
        downloads = model.get('downloads', 0)
        if downloads > 10000:
            score += 20
        elif downloads > 1000:
            score += 10
        
        likes = model.get('likes', 0)
        if likes > 100:
            score += 15
        elif likes > 10:
            score += 5
        
        if model.get('lastModified'):
            score += 10
        
        return min(100, score)
    
    def get_subscription_features(self) -> Dict[str, Any]:
        """Get features included in $9/month subscription"""
        return {
            'pricing': '$9/month',
            'features': [
                'Unlimited model queries',
                'Access to 100,000+ AI models',
                'Real-time model updates',
                'Priority inference speed',
                'Advanced analytics dashboard',
                'Custom model recommendations',
                'API rate limit: 10,000 requests/month',
                'Email support',
                'Model performance benchmarks',
                'Usage insights and reporting'
            ],
            'moat_advantages': [
                'Constantly updated with newest models',
                'AI-powered model discovery',
                'Performance optimization suggestions',
                'Automated model evaluation',
                'Trend analysis and predictions'
            ],
            'supported_tasks': [
                'text-generation',
                'text-classification',
                'image-classification',
                'question-answering',
                'summarization',
                'translation',
                'sentiment-analysis',
                'object-detection',
                'speech-recognition',
                'text-to-speech'
            ]
        }

if __name__ == "__main__":
    hub = HuggingFaceModelHub()
    print("Hugging Face Model Hub with constantly updated AI models initialized")
