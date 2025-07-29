
import requests
import os
from typing import Dict, List, Any
import json

class PersonalizedNewsSummarizer:
    def __init__(self, openai_key: str = None, news_key: str = None):
        self.openai_key = openai_key or os.getenv('OPENAI_API_KEY')
        self.news_key = news_key or os.getenv('NEWS_API_KEY')
        self.openai_headers = {
            'Authorization': f'Bearer {self.openai_key}',
            'Content-Type': 'application/json'
        }
        self.news_headers = {'X-API-Key': self.news_key}
    
    def get_personalized_summary(self, user_interests: List[str], max_articles: int = 10) -> Dict[str, Any]:
        """Generate personalized news summary based on user interests"""
        articles = self.fetch_relevant_articles(user_interests, max_articles)
        summaries = []
        
        for article in articles:
            summary = self.summarize_article(article, user_interests)
            if summary:
                summaries.append({
                    'title': article.get('title'),
                    'summary': summary,
                    'relevance_score': self.calculate_relevance(article, user_interests),
                    'source': article.get('source', {}).get('name'),
                    'url': article.get('url')
                })
        
        summaries.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return {
            'personalized_summaries': summaries,
            'total_articles': len(summaries),
            'user_interests': user_interests
        }
    
    def fetch_relevant_articles(self, interests: List[str], max_articles: int) -> List[Dict]:
        """Fetch articles relevant to user interests"""
        all_articles = []
        
        for interest in interests:
            try:
                response = requests.get(
                    'https://newsapi.org/v2/everything',
                    headers=self.news_headers,
                    params={
                        'q': interest,
                        'sortBy': 'relevancy',
                        'pageSize': max_articles // len(interests),
                        'language': 'en'
                    }
                )
                if response.status_code == 200:
                    articles = response.json().get('articles', [])
                    all_articles.extend(articles)
            except Exception:
                continue
        
        return all_articles[:max_articles]
    
    def summarize_article(self, article: Dict, user_interests: List[str]) -> str:
        """Summarize article content using OpenAI"""
        content = article.get('content') or article.get('description', '')
        if not content:
            return ""
        
        prompt = f"""
        Summarize this news article in 2-3 sentences, focusing on aspects relevant to these interests: {', '.join(user_interests)}
        
        Article: {content}
        
        Summary:
        """
        
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=self.openai_headers,
                json={
                    'model': 'gpt-3.5-turbo',
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': 150,
                    'temperature': 0.3
                }
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content'].strip()
        except Exception:
            pass
        
        return content[:200] + "..." if len(content) > 200 else content
    
    def calculate_relevance(self, article: Dict, interests: List[str]) -> float:
        """Calculate relevance score based on user interests"""
        text = f"{article.get('title', '')} {article.get('description', '')}".lower()
        
        score = 0
        for interest in interests:
            if interest.lower() in text:
                score += 1
        
        return score / len(interests) if interests else 0

if __name__ == "__main__":
    summarizer = PersonalizedNewsSummarizer()
    print("Personalized news summarizer initialized")
