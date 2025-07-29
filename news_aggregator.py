
import requests
import os
from typing import Dict, List, Any
import json

class NewsAggregator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('NEWS_API_KEY')
        self.base_url = 'https://newsapi.org/v2'
        self.headers = {'X-API-Key': self.api_key}
    
    def get_top_headlines(self, category: str = 'technology', country: str = 'us') -> List[Dict]:
        """Get top headlines by category"""
        params = {
            'category': category,
            'country': country,
            'pageSize': 20
        }
        
        try:
            response = requests.get(
                f'{self.base_url}/top-headlines',
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            return response.json().get('articles', [])
        except Exception as e:
            return []
    
    def search_news(self, query: str, days: int = 7) -> List[Dict]:
        """Search news articles by query"""
        from datetime import datetime, timedelta
        
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        params = {
            'q': query,
            'from': from_date,
            'sortBy': 'relevancy',
            'pageSize': 50
        }
        
        try:
            response = requests.get(
                f'{self.base_url}/everything',
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            return response.json().get('articles', [])
        except Exception as e:
            return []

if __name__ == "__main__":
    aggregator = NewsAggregator()
    print("News aggregator initialized")
