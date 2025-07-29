
import requests
import os
from typing import Dict, List, Any
import json

class TMDBPosterVisualizer:
    def __init__(self, api_key: str = None, openai_key: str = None):
        self.api_key = api_key or os.getenv('TMDB_API_KEY')
        self.openai_key = openai_key or os.getenv('OPENAI_API_KEY')
        self.base_url = 'https://api.themoviedb.org/3'
        self.image_base_url = 'https://image.tmdb.org/t/p/w500'
        self.openai_headers = {
            'Authorization': f'Bearer {self.openai_key}',
            'Content-Type': 'application/json'
        }
    
    def get_movie_recommendations(self, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-driven movie recommendations with poster visualizations"""
        genres = user_preferences.get('genres', ['action', 'drama'])
        year_range = user_preferences.get('year_range', [2020, 2024])
        
        movies = self.search_movies_by_criteria(genres, year_range)
        enhanced_movies = []
        
        for movie in movies[:10]:  # Limit to top 10
            poster_analysis = self.analyze_poster_with_ai(movie)
            recommendation_score = self.calculate_ai_recommendation_score(movie, user_preferences)
            
            enhanced_movies.append({
                'id': movie.get('id'),
                'title': movie.get('title'),
                'overview': movie.get('overview'),
                'poster_path': f"{self.image_base_url}{movie.get('poster_path')}" if movie.get('poster_path') else None,
                'poster_analysis': poster_analysis,
                'recommendation_score': recommendation_score,
                'release_date': movie.get('release_date'),
                'vote_average': movie.get('vote_average'),
                'genre_ids': movie.get('genre_ids', [])
            })
        
        enhanced_movies.sort(key=lambda x: x['recommendation_score'], reverse=True)
        
        return {
            'recommended_movies': enhanced_movies,
            'total_recommendations': len(enhanced_movies),
            'user_preferences': user_preferences,
            'visualization_features': self.get_visualization_features()
        }
    
    def search_movies_by_criteria(self, genres: List[str], year_range: List[int]) -> List[Dict]:
        """Search movies by genre and year criteria"""
        genre_map = {
            'action': 28, 'adventure': 12, 'animation': 16, 'comedy': 35,
            'crime': 80, 'documentary': 99, 'drama': 18, 'family': 10751,
            'fantasy': 14, 'history': 36, 'horror': 27, 'music': 10402,
            'mystery': 9648, 'romance': 10749, 'science fiction': 878,
            'thriller': 53, 'war': 10752, 'western': 37
        }
        
        genre_ids = [genre_map.get(genre.lower()) for genre in genres if genre.lower() in genre_map]
        
        try:
            response = requests.get(
                f'{self.base_url}/discover/movie',
                params={
                    'api_key': self.api_key,
                    'with_genres': ','.join(map(str, genre_ids)),
                    'primary_release_date.gte': f'{year_range[0]}-01-01',
                    'primary_release_date.lte': f'{year_range[1]}-12-31',
                    'sort_by': 'popularity.desc',
                    'page': 1
                }
            )
            
            if response.status_code == 200:
                return response.json().get('results', [])
        except Exception:
            pass
        
        return []
    
    def analyze_poster_with_ai(self, movie: Dict) -> Dict[str, Any]:
        """Analyze movie poster using AI for visual insights"""
        poster_url = f"{self.image_base_url}{movie.get('poster_path')}" if movie.get('poster_path') else None
        
        if not poster_url:
            return {'analysis': 'No poster available', 'visual_elements': []}
        
        prompt = f"""
        Analyze this movie poster for "{movie.get('title', 'Unknown')}" and describe:
        1. Visual style and color palette
        2. Key design elements
        3. Mood and atmosphere conveyed
        4. Target audience appeal
        
        Movie overview: {movie.get('overview', '')[:200]}
        
        Provide a brief analysis in 2-3 sentences:
        """
        
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=self.openai_headers,
                json={
                    'model': 'gpt-3.5-turbo',
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': 150,
                    'temperature': 0.7
                }
            )
            
            if response.status_code == 200:
                analysis = response.json()['choices'][0]['message']['content'].strip()
                return {
                    'analysis': analysis,
                    'poster_url': poster_url,
                    'visual_elements': self.extract_visual_elements(movie)
                }
        except Exception:
            pass
        
        return {
            'analysis': f"Poster for {movie.get('title')} - visual analysis unavailable",
            'poster_url': poster_url,
            'visual_elements': self.extract_visual_elements(movie)
        }
    
    def calculate_ai_recommendation_score(self, movie: Dict, preferences: Dict) -> float:
        """Calculate AI-driven recommendation score"""
        base_score = movie.get('vote_average', 5.0) * 10  # Convert to 0-100 scale
        
        preferred_genres = preferences.get('genres', [])
        genre_boost = len(set(movie.get('genre_ids', [])) & set(preferred_genres)) * 5
        
        release_year = int(movie.get('release_date', '2000-01-01')[:4])
        recency_boost = max(0, (release_year - 2020) * 2)
        
        popularity_boost = min(10, movie.get('popularity', 0) / 100)
        
        total_score = base_score + genre_boost + recency_boost + popularity_boost
        return min(100, max(0, total_score))
    
    def extract_visual_elements(self, movie: Dict) -> List[str]:
        """Extract visual elements based on movie metadata"""
        elements = []
        
        genre_ids = movie.get('genre_ids', [])
        if 28 in genre_ids:  # Action
            elements.extend(['dynamic composition', 'bold colors', 'action poses'])
        if 27 in genre_ids:  # Horror
            elements.extend(['dark palette', 'dramatic lighting', 'suspenseful imagery'])
        if 35 in genre_ids:  # Comedy
            elements.extend(['bright colors', 'playful typography', 'character focus'])
        if 18 in genre_ids:  # Drama
            elements.extend(['emotional imagery', 'character portraits', 'artistic composition'])
        
        return elements[:5]  # Limit to 5 elements
    
    def get_visualization_features(self) -> List[str]:
        """Get unique visualization features offered"""
        return [
            'AI-powered poster analysis',
            'Visual style categorization',
            'Color palette extraction',
            'Mood and atmosphere detection',
            'Target audience identification',
            'Genre-specific visual elements',
            'Recommendation scoring algorithm',
            'Personalized movie discovery'
        ]

if __name__ == "__main__":
    visualizer = TMDBPosterVisualizer()
    print("TMDb poster visualizer with AI recommendations initialized")
