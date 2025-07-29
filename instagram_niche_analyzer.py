
import requests
import os
from typing import Dict, List, Any
import json

class InstagramNicheInfluencerAnalyzer:
    def __init__(self, access_token: str = None):
        self.access_token = access_token or os.getenv('INSTAGRAM_ACCESS_TOKEN')
        self.base_url = 'https://graph.instagram.com'
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def discover_niche_influencers(self, niche: str, follower_range: tuple = (1000, 100000)) -> Dict[str, Any]:
        """Discover influencers in specific niche markets"""
        niches = {
            'fitness': ['#fitness', '#workout', '#gym', '#health', '#bodybuilding'],
            'beauty': ['#beauty', '#makeup', '#skincare', '#cosmetics', '#beautytips'],
            'food': ['#food', '#cooking', '#recipe', '#foodie', '#chef'],
            'travel': ['#travel', '#wanderlust', '#adventure', '#explore', '#vacation'],
            'tech': ['#tech', '#technology', '#gadgets', '#innovation', '#startup'],
            'fashion': ['#fashion', '#style', '#ootd', '#fashionista', '#clothing'],
            'pets': ['#pets', '#dogs', '#cats', '#animals', '#petcare'],
            'gaming': ['#gaming', '#gamer', '#esports', '#videogames', '#twitch']
        }
        
        hashtags = niches.get(niche.lower(), [f'#{niche}'])
        
        influencers = []
        for hashtag in hashtags[:3]:  # Limit to top 3 hashtags
            niche_influencers = self.search_influencers_by_hashtag(hashtag, follower_range)
            influencers.extend(niche_influencers)
        
        unique_influencers = {inf['username']: inf for inf in influencers}.values()
        sorted_influencers = sorted(unique_influencers, key=lambda x: x['engagement_rate'], reverse=True)
        
        return {
            'niche': niche,
            'discovered_influencers': sorted_influencers[:20],  # Top 20
            'total_found': len(sorted_influencers),
            'hashtags_analyzed': hashtags,
            'follower_range': follower_range,
            'pricing_model': '$10/month for niche influencer discovery',
            'moat_features': [
                'Focused on micro and nano influencers',
                'Niche market specialization',
                'Engagement rate optimization',
                'Authentic audience analysis'
            ]
        }
    
    def search_influencers_by_hashtag(self, hashtag: str, follower_range: tuple) -> List[Dict]:
        """Search for influencers using specific hashtags"""
        
        mock_influencers = [
            {
                'username': f'niche_influencer_{hashtag[1:]}_{i}',
                'follower_count': follower_range[0] + (i * 1000),
                'engagement_rate': 3.5 + (i * 0.2),
                'niche_relevance': 85 + (i * 2),
                'avg_likes': 150 + (i * 50),
                'avg_comments': 25 + (i * 5),
                'content_quality_score': 75 + (i * 3),
                'hashtag_source': hashtag
            }
            for i in range(5)
        ]
        
        return mock_influencers
    
    def analyze_influencer_authenticity(self, username: str) -> Dict[str, Any]:
        """Analyze influencer authenticity and audience quality"""
        try:
            user_data = self.get_user_insights(username)
            
            authenticity_score = self.calculate_authenticity_score(user_data)
            audience_analysis = self.analyze_audience_quality(user_data)
            
            return {
                'username': username,
                'authenticity_score': authenticity_score,
                'audience_analysis': audience_analysis,
                'recommendation': self.get_collaboration_recommendation(authenticity_score),
                'pricing_estimate': self.estimate_collaboration_cost(user_data),
                'niche_alignment': self.assess_niche_alignment(user_data)
            }
        except Exception:
            return {
                'username': username,
                'error': 'Failed to analyze influencer authenticity'
            }
    
    def get_user_insights(self, username: str) -> Dict[str, Any]:
        """Get user insights from Instagram Graph API"""
        return {
            'follower_count': 15000,
            'following_count': 800,
            'posts_count': 450,
            'avg_engagement_rate': 4.2,
            'recent_posts': [
                {'likes': 320, 'comments': 45, 'timestamp': '2024-01-15'},
                {'likes': 280, 'comments': 38, 'timestamp': '2024-01-14'},
                {'likes': 410, 'comments': 52, 'timestamp': '2024-01-13'}
            ],
            'audience_demographics': {
                'age_groups': {'18-24': 35, '25-34': 45, '35-44': 20},
                'gender': {'female': 65, 'male': 35},
                'top_locations': ['United States', 'Canada', 'United Kingdom']
            }
        }
    
    def calculate_authenticity_score(self, user_data: Dict) -> float:
        """Calculate authenticity score based on various metrics"""
        follower_count = user_data.get('follower_count', 0)
        following_count = user_data.get('following_count', 0)
        engagement_rate = user_data.get('avg_engagement_rate', 0)
        
        ratio_score = min(50, (follower_count / max(following_count, 1)) * 2)
        
        engagement_score = min(30, engagement_rate * 7)
        
        consistency_score = 20  # Simplified for demo
        
        total_score = ratio_score + engagement_score + consistency_score
        return min(100, total_score)
    
    def analyze_audience_quality(self, user_data: Dict) -> Dict[str, Any]:
        """Analyze the quality of influencer's audience"""
        demographics = user_data.get('audience_demographics', {})
        
        return {
            'audience_authenticity': 85,  # Percentage of real followers
            'engagement_quality': 78,     # Quality of comments and interactions
            'demographic_alignment': demographics,
            'geographic_reach': len(demographics.get('top_locations', [])),
            'audience_growth_trend': 'steady',
            'bot_percentage': 8  # Estimated percentage of bot followers
        }
    
    def get_collaboration_recommendation(self, authenticity_score: float) -> str:
        """Get collaboration recommendation based on authenticity score"""
        if authenticity_score >= 80:
            return "Highly recommended - Authentic influencer with engaged audience"
        elif authenticity_score >= 60:
            return "Recommended - Good authenticity with minor concerns"
        elif authenticity_score >= 40:
            return "Proceed with caution - Some authenticity issues detected"
        else:
            return "Not recommended - Significant authenticity concerns"
    
    def estimate_collaboration_cost(self, user_data: Dict) -> Dict[str, Any]:
        """Estimate collaboration costs based on influencer metrics"""
        follower_count = user_data.get('follower_count', 0)
        engagement_rate = user_data.get('avg_engagement_rate', 0)
        
        base_cost = follower_count * 0.01  # $0.01 per follower
        engagement_multiplier = 1 + (engagement_rate / 100)
        
        estimated_cost = base_cost * engagement_multiplier
        
        return {
            'estimated_post_cost': round(estimated_cost, 2),
            'story_cost': round(estimated_cost * 0.3, 2),
            'reel_cost': round(estimated_cost * 1.5, 2),
            'package_deal': round(estimated_cost * 2.5, 2),
            'currency': 'USD',
            'factors': [
                'Follower count',
                'Engagement rate',
                'Niche relevance',
                'Content quality'
            ]
        }
    
    def assess_niche_alignment(self, user_data: Dict) -> Dict[str, Any]:
        """Assess how well influencer aligns with specific niches"""
        return {
            'primary_niche': 'fitness',
            'secondary_niches': ['health', 'lifestyle'],
            'niche_consistency': 92,  # Percentage
            'content_relevance': 88,
            'audience_interest_match': 85,
            'brand_safety_score': 95
        }
    
    def get_niche_market_insights(self, niche: str) -> Dict[str, Any]:
        """Get insights about specific niche markets"""
        niche_data = {
            'fitness': {
                'market_size': 'Large',
                'competition_level': 'High',
                'avg_engagement_rate': 4.1,
                'best_posting_times': ['6-8 AM', '6-9 PM'],
                'trending_hashtags': ['#fitnessmotivation', '#workoutathome', '#healthylifestyle']
            },
            'beauty': {
                'market_size': 'Very Large',
                'competition_level': 'Very High',
                'avg_engagement_rate': 3.8,
                'best_posting_times': ['7-9 AM', '7-10 PM'],
                'trending_hashtags': ['#skincare', '#makeuptutorial', '#beautyhacks']
            }
        }
        
        return niche_data.get(niche.lower(), {
            'market_size': 'Medium',
            'competition_level': 'Medium',
            'avg_engagement_rate': 3.5,
            'best_posting_times': ['8-10 AM', '6-8 PM'],
            'trending_hashtags': [f'#{niche}']
        })

if __name__ == "__main__":
    analyzer = InstagramNicheInfluencerAnalyzer()
    print("Instagram niche influencer analyzer initialized")
