
import requests
import os
from typing import Dict, List, Any
import json
from datetime import datetime, timedelta

class GitHubReliabilityMonitor:
    def __init__(self, token: str = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = 'https://api.github.com'
    
    def get_repository_insights(self, repo: str) -> Dict[str, Any]:
        """Get comprehensive repository insights"""
        insights = {
            'commits': self.get_commit_frequency(repo),
            'issues': self.get_issue_metrics(repo),
            'pull_requests': self.get_pr_metrics(repo),
            'releases': self.get_release_metrics(repo),
            'reliability_score': 0
        }
        
        insights['reliability_score'] = self._calculate_reliability_score(insights)
        return insights
    
    def get_commit_frequency(self, repo: str, days: int = 30) -> Dict[str, Any]:
        """Analyze commit frequency and patterns"""
        since = (datetime.now() - timedelta(days=days)).isoformat()
        
        try:
            response = requests.get(
                f'{self.base_url}/repos/{repo}/commits',
                headers=self.headers,
                params={'since': since, 'per_page': 100}
            )
            response.raise_for_status()
            commits = response.json()
            
            return {
                'total_commits': len(commits),
                'daily_average': len(commits) / days,
                'recent_activity': len(commits) > 0
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_issue_metrics(self, repo: str) -> Dict[str, Any]:
        """Get issue resolution metrics"""
        try:
            response = requests.get(
                f'{self.base_url}/repos/{repo}/issues',
                headers=self.headers,
                params={'state': 'all', 'per_page': 100}
            )
            response.raise_for_status()
            issues = response.json()
            
            open_issues = [i for i in issues if i['state'] == 'open']
            closed_issues = [i for i in issues if i['state'] == 'closed']
            
            return {
                'total_issues': len(issues),
                'open_issues': len(open_issues),
                'closed_issues': len(closed_issues),
                'resolution_rate': len(closed_issues) / len(issues) if issues else 0
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_pr_metrics(self, repo: str) -> Dict[str, Any]:
        """Get pull request metrics"""
        try:
            response = requests.get(
                f'{self.base_url}/repos/{repo}/pulls',
                headers=self.headers,
                params={'state': 'all', 'per_page': 100}
            )
            response.raise_for_status()
            prs = response.json()
            
            merged_prs = [pr for pr in prs if pr.get('merged_at')]
            
            return {
                'total_prs': len(prs),
                'merged_prs': len(merged_prs),
                'merge_rate': len(merged_prs) / len(prs) if prs else 0
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_release_metrics(self, repo: str) -> Dict[str, Any]:
        """Get release frequency metrics"""
        try:
            response = requests.get(
                f'{self.base_url}/repos/{repo}/releases',
                headers=self.headers,
                params={'per_page': 50}
            )
            response.raise_for_status()
            releases = response.json()
            
            return {
                'total_releases': len(releases),
                'latest_release': releases[0]['tag_name'] if releases else None,
                'release_frequency': 'regular' if len(releases) > 5 else 'infrequent'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_reliability_score(self, insights: Dict) -> float:
        """Calculate overall reliability score"""
        score = 50.0  # Base score
        
        if insights['commits'].get('recent_activity'):
            score += 20
        
        resolution_rate = insights['issues'].get('resolution_rate', 0)
        score += resolution_rate * 20
        
        merge_rate = insights['pull_requests'].get('merge_rate', 0)
        score += merge_rate * 10
        
        return min(100, score)
    
    def setup_alerts(self, repo: str, webhook_url: str) -> Dict[str, Any]:
        """Setup repository alerts"""
        webhook_config = {
            'name': 'web',
            'active': True,
            'events': ['issues', 'pull_request', 'push'],
            'config': {
                'url': webhook_url,
                'content_type': 'json'
            }
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/repos/{repo}/hooks',
                headers=self.headers,
                json=webhook_config
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': str(e)}

if __name__ == "__main__":
    monitor = GitHubReliabilityMonitor()
    print("GitHub reliability monitor initialized")
