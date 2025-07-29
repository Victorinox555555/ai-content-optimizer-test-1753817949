
import requests
import os
from typing import Dict, List, Any
import json

class GitHubIssuesPrioritizer:
    def __init__(self, token: str = None, openai_key: str = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.openai_key = openai_key or os.getenv('OPENAI_API_KEY')
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.openai_headers = {
            'Authorization': f'Bearer {self.openai_key}',
            'Content-Type': 'application/json'
        }
    
    def prioritize_issues(self, repo: str, max_issues: int = 50) -> Dict[str, Any]:
        """Fetch and prioritize GitHub issues using AI"""
        issues = self.fetch_issues(repo, max_issues)
        prioritized = []
        
        for issue in issues:
            priority_score = self.calculate_ai_priority(issue)
            prioritized.append({
                'number': issue.get('number'),
                'title': issue.get('title'),
                'body': issue.get('body', '')[:200] + '...',
                'labels': [label['name'] for label in issue.get('labels', [])],
                'priority_score': priority_score,
                'urgency_level': self.get_urgency_level(priority_score),
                'url': issue.get('html_url')
            })
        
        prioritized.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return {
            'prioritized_issues': prioritized,
            'total_issues': len(prioritized),
            'high_priority_count': len([i for i in prioritized if i['priority_score'] >= 80]),
            'repo': repo
        }
    
    def fetch_issues(self, repo: str, max_issues: int) -> List[Dict]:
        """Fetch issues from GitHub repository"""
        try:
            response = requests.get(
                f'https://api.github.com/repos/{repo}/issues',
                headers=self.headers,
                params={
                    'state': 'open',
                    'per_page': max_issues,
                    'sort': 'created',
                    'direction': 'desc'
                }
            )
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        
        return []
    
    def calculate_ai_priority(self, issue: Dict) -> int:
        """Use AI to calculate issue priority score"""
        title = issue.get('title', '')
        body = issue.get('body', '')[:500]  # Limit body length
        labels = [label['name'] for label in issue.get('labels', [])]
        
        prompt = f"""
        Analyze this GitHub issue and assign a priority score from 1-100:
        
        Title: {title}
        Body: {body}
        Labels: {', '.join(labels)}
        
        Consider:
        - Security vulnerabilities (high priority)
        - Bug severity and user impact
        - Feature importance
        - Technical debt
        
        Return only a number from 1-100:
        """
        
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=self.openai_headers,
                json={
                    'model': 'gpt-3.5-turbo',
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': 10,
                    'temperature': 0.3
                }
            )
            
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content'].strip()
                score = int(''.join(filter(str.isdigit, content)))
                return max(1, min(100, score))
        except Exception:
            pass
        
        score = 50  # Base score
        
        if any(label in ['bug', 'critical', 'security'] for label in labels):
            score += 30
        if any(label in ['enhancement', 'feature'] for label in labels):
            score += 10
        
        text = f"{title} {body}".lower()
        if any(word in text for word in ['crash', 'error', 'fail', 'broken']):
            score += 20
        if any(word in text for word in ['security', 'vulnerability', 'exploit']):
            score += 40
        
        return max(1, min(100, score))
    
    def get_urgency_level(self, score: int) -> str:
        """Convert priority score to urgency level"""
        if score >= 90:
            return 'CRITICAL'
        elif score >= 70:
            return 'HIGH'
        elif score >= 50:
            return 'MEDIUM'
        else:
            return 'LOW'

if __name__ == "__main__":
    prioritizer = GitHubIssuesPrioritizer()
    print("GitHub Issues AI prioritizer initialized")
