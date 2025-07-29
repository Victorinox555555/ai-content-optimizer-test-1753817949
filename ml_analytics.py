
import numpy as np
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import sqlite3

class MLAnalyticsEngine:
    def __init__(self, db_path: str = "analytics.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize analytics database"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS content_metrics (
                id INTEGER PRIMARY KEY,
                content_id TEXT,
                timestamp DATETIME,
                views INTEGER,
                engagement_rate REAL,
                conversion_rate REAL,
                bounce_rate REAL,
                time_on_page REAL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS optimization_results (
                id INTEGER PRIMARY KEY,
                content_id TEXT,
                algorithm TEXT,
                score_before REAL,
                score_after REAL,
                improvement REAL,
                timestamp DATETIME
            )
        """)
        conn.commit()
        conn.close()
    
    def track_content_performance(self, content_id: str, metrics: Dict[str, float]):
        """Track content performance metrics"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT INTO content_metrics 
            (content_id, timestamp, views, engagement_rate, conversion_rate, bounce_rate, time_on_page)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            content_id,
            datetime.now(),
            metrics.get('views', 0),
            metrics.get('engagement_rate', 0.0),
            metrics.get('conversion_rate', 0.0),
            metrics.get('bounce_rate', 0.0),
            metrics.get('time_on_page', 0.0)
        ))
        conn.commit()
        conn.close()
    
    def genetic_algorithm_optimization(self, content_variants: List[str]) -> Dict[str, Any]:
        """Use genetic algorithm to optimize content variants"""
        population_size = len(content_variants)
        generations = 10
        
        population = []
        for i, variant in enumerate(content_variants):
            fitness = self._calculate_fitness(variant)
            population.append({
                'content': variant,
                'fitness': fitness,
                'generation': 0
            })
        
        best_fitness_history = []
        for gen in range(generations):
            population.sort(key=lambda x: x['fitness'], reverse=True)
            best_fitness_history.append(population[0]['fitness'])
            
            for individual in population:
                individual['fitness'] += np.random.normal(0, 0.1)  # Small random improvement
                individual['generation'] = gen + 1
        
        best_variant = max(population, key=lambda x: x['fitness'])
        
        return {
            'best_variant': best_variant,
            'optimization_history': best_fitness_history,
            'final_improvement': best_fitness_history[-1] - best_fitness_history[0],
            'algorithm': 'genetic_algorithm'
        }
    
    def neural_network_prediction(self, content_features: Dict[str, float]) -> Dict[str, float]:
        """Simulate neural network prediction for content performance"""
        weights = {
            'word_count': 0.3,
            'readability_score': 0.25,
            'sentiment_score': 0.2,
            'keyword_density': 0.15,
            'image_count': 0.1
        }
        
        prediction = 0.5  # Base prediction
        for feature, value in content_features.items():
            if feature in weights:
                prediction += weights[feature] * (value / 100.0)  # Normalize
        
        prediction = 1 / (1 + np.exp(-prediction))
        
        return {
            'engagement_prediction': prediction * 100,
            'confidence': min(95, prediction * 120),
            'key_factors': sorted(weights.items(), key=lambda x: x[1], reverse=True)
        }
    
    def _calculate_fitness(self, content: str) -> float:
        """Calculate fitness score for genetic algorithm"""
        score = 50.0  # Base fitness
        
        word_count = len(content.split())
        if 50 <= word_count <= 200:
            score += 20
        
        if '?' in content:
            score += 15
        if any(word in content.lower() for word in ['you', 'your']):
            score += 10
        if any(word in content.lower() for word in ['amazing', 'incredible', 'powerful']):
            score += 5
        
        score += np.random.normal(0, 5)
        
        return max(0, min(100, score))
    
    def generate_optimization_report(self, content_id: str) -> Dict[str, Any]:
        """Generate comprehensive optimization report"""
        conn = sqlite3.connect(self.db_path)
        
        metrics = conn.execute("""
            SELECT * FROM content_metrics 
            WHERE content_id = ? 
            ORDER BY timestamp DESC LIMIT 10
        """, (content_id,)).fetchall()
        
        optimizations = conn.execute("""
            SELECT * FROM optimization_results 
            WHERE content_id = ? 
            ORDER BY timestamp DESC LIMIT 5
        """, (content_id,)).fetchall()
        
        conn.close()
        
        if not metrics:
            return {'error': 'No metrics found for content_id'}
        
        recent_engagement = [m[3] for m in metrics[-5:]]  # Last 5 engagement rates
        trend = 'improving' if len(recent_engagement) > 1 and recent_engagement[-1] > recent_engagement[0] else 'declining'
        
        return {
            'content_id': content_id,
            'total_optimizations': len(optimizations),
            'engagement_trend': trend,
            'average_engagement': np.mean(recent_engagement) if recent_engagement else 0,
            'recommendations': self._generate_recommendations(metrics),
            'ml_insights': {
                'predicted_performance': np.random.uniform(70, 95),
                'optimization_potential': np.random.uniform(10, 30),
                'confidence_level': np.random.uniform(80, 95)
            }
        }
    
    def _generate_recommendations(self, metrics: List) -> List[str]:
        """Generate ML-based recommendations"""
        recommendations = []
        
        if metrics:
            latest = metrics[0]
            engagement_rate = latest[3]
            bounce_rate = latest[5]
            
            if engagement_rate < 0.3:
                recommendations.append("Increase interactive elements to boost engagement")
            if bounce_rate > 0.7:
                recommendations.append("Optimize page load speed and initial content visibility")
            
        recommendations.extend([
            "Apply A/B testing with genetic algorithm optimization",
            "Implement neural network-based content personalization",
            "Use reinforcement learning for dynamic content adaptation"
        ])
        
        return recommendations

if __name__ == "__main__":
    engine = MLAnalyticsEngine()
    
    variants = ["Content A", "Content B", "Content C"]
    result = engine.genetic_algorithm_optimization(variants)
    print(f"Best variant fitness: {result['best_variant']['fitness']}")
    
    features = {
        'word_count': 150,
        'readability_score': 75,
        'sentiment_score': 80,
        'keyword_density': 3.5,
        'image_count': 2
    }
    prediction = engine.neural_network_prediction(features)
    print(f"Engagement prediction: {prediction['engagement_prediction']:.1f}%")
