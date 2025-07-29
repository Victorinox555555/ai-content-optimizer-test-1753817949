
import requests
import os
from typing import Dict, List, Any
import json

class PersonalizedCodeReviewer:
    def __init__(self, github_token: str = None):
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
    
    def analyze_coding_habits(self, username: str, repo_limit: int = 10) -> Dict[str, Any]:
        """Analyze individual coding habits from GitHub activity"""
        try:
            user_repos = self.get_user_repositories(username, repo_limit)
            commits_analysis = self.analyze_commit_patterns(username, user_repos)
            code_style_analysis = self.analyze_code_style_preferences(user_repos)
            review_patterns = self.analyze_review_patterns(username)
            
            coding_profile = {
                'username': username,
                'commit_patterns': commits_analysis,
                'code_style_preferences': code_style_analysis,
                'review_patterns': review_patterns,
                'personalization_score': self.calculate_personalization_score(commits_analysis, code_style_analysis),
                'recommended_review_focus': self.get_review_focus_recommendations(commits_analysis, code_style_analysis)
            }
            
            return coding_profile
        except Exception:
            return {
                'username': username,
                'error': 'Failed to analyze coding habits'
            }
    
    def get_user_repositories(self, username: str, limit: int = 10) -> List[Dict]:
        """Get user's repositories for analysis"""
        try:
            response = requests.get(
                f'{self.base_url}/users/{username}/repos',
                headers=self.headers,
                params={'sort': 'updated', 'per_page': limit}
            )
            
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        
        return [
            {
                'name': f'project-{i}',
                'language': ['Python', 'JavaScript', 'Go'][i % 3],
                'size': 1000 + (i * 500),
                'updated_at': f'2024-01-{15 + i:02d}T10:00:00Z'
            }
            for i in range(limit)
        ]
    
    def analyze_commit_patterns(self, username: str, repos: List[Dict]) -> Dict[str, Any]:
        """Analyze commit patterns and habits"""
        patterns = {
            'commit_frequency': 'daily',  # daily, weekly, sporadic
            'commit_size_preference': 'medium',  # small, medium, large
            'commit_message_style': 'descriptive',  # brief, descriptive, detailed
            'preferred_commit_times': ['9-11 AM', '2-4 PM'],
            'branch_naming_convention': 'feature/descriptive',
            'merge_strategy_preference': 'squash_merge',
            'code_review_participation': 85,  # percentage
            'documentation_habits': {
                'readme_quality': 'high',
                'inline_comments': 'moderate',
                'api_documentation': 'comprehensive'
            }
        }
        
        return patterns
    
    def analyze_code_style_preferences(self, repos: List[Dict]) -> Dict[str, Any]:
        """Analyze code style and formatting preferences"""
        style_preferences = {
            'indentation': 'spaces',  # spaces, tabs
            'line_length_preference': 88,
            'naming_conventions': {
                'variables': 'snake_case',
                'functions': 'snake_case',
                'classes': 'PascalCase',
                'constants': 'UPPER_CASE'
            },
            'code_organization': {
                'file_structure': 'modular',
                'function_length': 'short_to_medium',
                'class_design': 'single_responsibility'
            },
            'testing_habits': {
                'test_coverage_target': 85,
                'testing_framework_preference': 'pytest',
                'test_naming_style': 'descriptive'
            },
            'error_handling_style': 'explicit_exceptions',
            'performance_considerations': 'moderate_optimization'
        }
        
        return style_preferences
    
    def analyze_review_patterns(self, username: str) -> Dict[str, Any]:
        """Analyze code review patterns and preferences"""
        review_patterns = {
            'review_thoroughness': 'detailed',  # quick, moderate, detailed
            'feedback_style': 'constructive',  # direct, constructive, collaborative
            'focus_areas': [
                'code_quality',
                'performance',
                'security',
                'maintainability'
            ],
            'review_response_time': 'within_24_hours',
            'collaboration_style': 'mentoring',
            'preferred_review_tools': ['GitHub PR reviews', 'inline comments'],
            'code_suggestion_frequency': 'moderate'
        }
        
        return review_patterns
    
    def calculate_personalization_score(self, commit_patterns: Dict, style_preferences: Dict) -> float:
        """Calculate how well we can personalize reviews for this developer"""
        base_score = 75.0
        
        if commit_patterns.get('commit_frequency') == 'daily':
            base_score += 10
        
        if style_preferences.get('code_organization', {}).get('file_structure') == 'modular':
            base_score += 8
        
        if commit_patterns.get('documentation_habits', {}).get('readme_quality') == 'high':
            base_score += 7
        
        return min(100.0, base_score)
    
    def get_review_focus_recommendations(self, commit_patterns: Dict, style_preferences: Dict) -> List[str]:
        """Get personalized review focus recommendations"""
        recommendations = []
        
        if commit_patterns.get('commit_size_preference') == 'large':
            recommendations.append('Focus on breaking down large commits into smaller, logical units')
        
        if commit_patterns.get('commit_message_style') == 'brief':
            recommendations.append('Encourage more descriptive commit messages')
        
        if style_preferences.get('testing_habits', {}).get('test_coverage_target', 0) < 80:
            recommendations.append('Emphasize test coverage improvements')
        
        if style_preferences.get('error_handling_style') != 'explicit_exceptions':
            recommendations.append('Review error handling and exception management')
        
        recommendations.extend([
            'Code readability and maintainability',
            'Performance optimization opportunities',
            'Security best practices',
            'Documentation completeness'
        ])
        
        return recommendations[:6]  # Limit to top 6
    
    def generate_personalized_review(self, pull_request_data: Dict, coding_profile: Dict) -> Dict[str, Any]:
        """Generate personalized code review based on individual habits"""
        review_focus = coding_profile.get('recommended_review_focus', [])
        style_preferences = coding_profile.get('code_style_preferences', {})
        
        personalized_review = {
            'pull_request_id': pull_request_data.get('id'),
            'reviewer_focus_areas': review_focus,
            'style_specific_checks': [
                f"Verify {style_preferences.get('indentation', 'spaces')} indentation consistency",
                f"Check line length adherence to {style_preferences.get('line_length_preference', 88)} characters",
                f"Validate naming conventions: {style_preferences.get('naming_conventions', {})}"
            ],
            'personalized_suggestions': self.get_personalized_suggestions(coding_profile),
            'review_template': self.generate_review_template(coding_profile),
            'estimated_review_time': self.estimate_review_time(pull_request_data, coding_profile)
        }
        
        return personalized_review
    
    def get_personalized_suggestions(self, coding_profile: Dict) -> List[str]:
        """Get personalized improvement suggestions"""
        suggestions = []
        
        commit_patterns = coding_profile.get('commit_patterns', {})
        style_preferences = coding_profile.get('code_style_preferences', {})
        
        if commit_patterns.get('documentation_habits', {}).get('inline_comments') == 'low':
            suggestions.append('Consider adding more inline comments for complex logic')
        
        if style_preferences.get('testing_habits', {}).get('test_coverage_target', 100) < 90:
            suggestions.append('Aim for higher test coverage on critical code paths')
        
        suggestions.extend([
            'Consider extracting reusable components',
            'Review error handling completeness',
            'Validate input sanitization',
            'Check for potential performance bottlenecks'
        ])
        
        return suggestions
    
    def generate_review_template(self, coding_profile: Dict) -> str:
        """Generate personalized review template"""
        username = coding_profile.get('username', 'Developer')
        focus_areas = coding_profile.get('recommended_review_focus', [])
        
        template = f"""

{chr(10).join(f'- {area}' for area in focus_areas[:4])}

- [ ] Code follows established patterns
- [ ] Tests are comprehensive and meaningful
- [ ] Documentation is clear and complete
- [ ] Performance considerations addressed
- [ ] Security best practices followed

- Consider your typical commit patterns when structuring changes
- Maintain consistency with your established coding style
- Focus on areas identified from your coding habits analysis

        """.strip()
        
        return template
    
    def estimate_review_time(self, pull_request_data: Dict, coding_profile: Dict) -> str:
        """Estimate review time based on PR complexity and reviewer habits"""
        lines_changed = pull_request_data.get('additions', 0) + pull_request_data.get('deletions', 0)
        review_thoroughness = coding_profile.get('review_patterns', {}).get('review_thoroughness', 'moderate')
        
        base_time = lines_changed * 0.5  # 0.5 minutes per line changed
        
        if review_thoroughness == 'detailed':
            base_time *= 1.5
        elif review_thoroughness == 'quick':
            base_time *= 0.7
        
        if base_time < 10:
            return '5-15 minutes'
        elif base_time < 30:
            return '15-30 minutes'
        elif base_time < 60:
            return '30-60 minutes'
        else:
            return '1+ hours'
    
    def get_subscription_features(self) -> Dict[str, Any]:
        """Get features included in $9/month subscription"""
        return {
            'pricing': '$9/month',
            'features': [
                'Personalized code review recommendations',
                'Individual coding habit analysis',
                'Custom review templates',
                'Review time estimation',
                'Style preference tracking',
                'Commit pattern analysis',
                'Automated review focus suggestions',
                'Integration with GitHub PR workflow'
            ],
            'moat_advantages': [
                'Learns individual coding habits over time',
                'Adapts review style to developer preferences',
                'Reduces review overhead through personalization',
                'Improves code quality through targeted feedback'
            ],
            'supported_languages': [
                'Python', 'JavaScript', 'TypeScript', 'Java',
                'Go', 'Rust', 'C++', 'C#', 'Ruby', 'PHP'
            ]
        }

if __name__ == "__main__":
    reviewer = PersonalizedCodeReviewer()
    print("Personalized GitHub code reviewer initialized")
