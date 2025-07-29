
import requests
import os
from typing import Dict, List, Any
import json

class GitHubIssuesAnalyzer:
    def __init__(self, token: str = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def analyze_error_patterns(self, repo: str, days: int = 30) -> Dict[str, Any]:
        """Analyze error patterns in GitHub issues"""
        issues = self.get_recent_issues(repo, days)
        
        error_patterns = {}
        for issue in issues:
            title = issue.get('title', '').lower()
            body = issue.get('body', '').lower()
            
            error_keywords = ['error', 'bug', 'exception', 'crash', 'fail', 'broken']
            if any(keyword in title or keyword in body for keyword in error_keywords):
                error_type = self._classify_error(title, body)
                if error_type not in error_patterns:
                    error_patterns[error_type] = []
                error_patterns[error_type].append(issue)
        
        return {
            'total_errors': sum(len(errors) for errors in error_patterns.values()),
            'error_patterns': error_patterns,
            'recommendations': self._generate_recommendations(error_patterns)
        }
    
    def get_recent_issues(self, repo: str, days: int = 30) -> List[Dict]:
        """Get recent issues from repository"""
        url = f'https://api.github.com/repos/{repo}/issues'
        params = {
            'state': 'all',
            'per_page': 100,
            'sort': 'created',
            'direction': 'desc'
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return []
    
    def _classify_error(self, title: str, body: str) -> str:
        """Classify error type based on content"""
        text = f"{title} {body}".lower()
        
        if any(word in text for word in ['import', 'module', 'package']):
            return 'Import/Dependency Error'
        elif any(word in text for word in ['syntax', 'parse', 'invalid']):
            return 'Syntax Error'
        elif any(word in text for word in ['memory', 'ram', 'oom']):
            return 'Memory Error'
        elif any(word in text for word in ['network', 'connection', 'timeout']):
            return 'Network Error'
        elif any(word in text for word in ['permission', 'access', 'auth']):
            return 'Permission Error'
        else:
            return 'General Error'
    
    def _generate_recommendations(self, error_patterns: Dict) -> List[str]:
        """Generate recommendations based on error patterns"""
        recommendations = []
        
        for error_type, errors in error_patterns.items():
            if len(errors) > 5:
                recommendations.append(f"High frequency of {error_type} - consider adding automated checks")
        
        recommendations.extend([
            "Implement automated error detection in CI/CD pipeline",
            "Add comprehensive logging for better error diagnosis",
            "Create error documentation and troubleshooting guides"
        ])
        
        return recommendations

if __name__ == "__main__":
    analyzer = GitHubIssuesAnalyzer()
    print("GitHub Issues analyzer initialized")
